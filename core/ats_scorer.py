"""
Sistema de Pontuação ATS (Applicant Tracking System) - v2.1.

Usa TF-IDF + Cosine Similarity para calcular compatibilidade real
entre o CV do candidato e uma Job Description gerada por IA.

Melhorias v2.1:
- Nova instância do vectorizer a cada cálculo (elimina estado sujo)
- Removido max_df que filtrava termos relevantes
- IA gera variações de mercado do cargo antes da JD
- JD composta cobre cargo original + variações
- Escala do score ajustada para faixa realista
"""

import re
import logging
from typing import Dict, Optional, List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core.utils import chamar_gpt

# Configurar logger
logger = logging.getLogger(__name__)

# Constantes para escala de score
# Baseado em observações empíricas: cosine similarity entre CV e JD tipicamente fica entre 0.05-0.40
RAW_SCORE_MAX = 0.35  # Valores acima de 0.35 são considerados excelentes
SCALED_SCORE_MAX = 95.0  # Score máximo escalado (deixamos 5 pontos de margem para 100)
SCALED_SCORE_MIN = 5.0   # Score mínimo quando há alguma similaridade
SCALED_RANGE = 90.0      # Faixa de escala (95 - 5)


def _clean_text(text: str) -> str:
    """Limpeza de texto para padronização."""
    if not text:
        return ""
    text = re.sub(r'[^\w\s]', ' ', str(text).lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def _calculate_tfidf_score(cv_text: str, job_description: str) -> float:
    """
    Calcula similaridade TF-IDF entre CV e JD.
    
    Cria uma NOVA instância do TfidfVectorizer a cada chamada
    para evitar estado sujo de chamadas anteriores.
    
    Args:
        cv_text: Texto do CV (já limpo ou não)
        job_description: Texto da JD (já limpo ou não)
        
    Returns:
        Score de 0.0 a 100.0 (já escalado)
    """
    cv_clean = _clean_text(cv_text)
    job_clean = _clean_text(job_description)
    
    if not cv_clean or not job_clean:
        logger.warning("CV ou JD vazio após limpeza")
        return 0.0
    
    try:
        # NOVA instância a cada cálculo — sem estado sujo
        vectorizer = TfidfVectorizer(
            ngram_range=(1, 3),
            min_df=1
            # SEM max_df — com apenas 2 docs, max_df filtra os termos relevantes
        )
        
        tfidf_matrix = vectorizer.fit_transform([cv_clean, job_clean])
        sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        raw_score = sim_matrix[0][0]
        
        logger.debug(f"Raw cosine similarity: {raw_score:.4f}")
        logger.debug(f"Vocabulário: {len(vectorizer.vocabulary_)} termos")
        
        # Escalar o score para faixa realista usando constantes definidas
        # Fórmula: valores de 0 até RAW_SCORE_MAX são mapeados linearmente para SCALED_RANGE
        if raw_score <= 0.0:
            scaled_score = 0.0
        elif raw_score >= RAW_SCORE_MAX:
            scaled_score = SCALED_SCORE_MAX
        else:
            scaled_score = (raw_score / RAW_SCORE_MAX) * SCALED_RANGE + SCALED_SCORE_MIN
        
        logger.debug(f"Scaled score: {scaled_score:.2f}")
        return round(scaled_score, 2)
        
    except ValueError as e:
        logger.error(f"ValueError no TF-IDF: {e}")
        return 0.0
    except Exception as e:
        logger.error(f"Erro no cálculo TF-IDF: {e}")
        return 0.0


def buscar_variacoes_cargo(client, cargo: str) -> List[str]:
    """
    Usa IA para encontrar variações de mercado de um cargo.
    
    Exemplo:
        Input: "Gerente de Inteligência de Negócios & Sales Ops"
        Output: [
            "Gerente de Business Intelligence",
            "Sales Operations Manager",
            "Gerente de Inteligência Comercial",
            "Head de Revenue Operations",
            "Gerente de BI & Analytics"
        ]
    
    Args:
        client: Cliente OpenAI inicializado
        cargo: Nome do cargo original
        
    Returns:
        Lista de variações do cargo (5 variações)
    """
    logger.info(f"Buscando variações de mercado para: {cargo}")
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento e mercado de trabalho. "
            "Dado um cargo, liste 5 variações desse cargo como aparecem em vagas reais no mercado. "
            "Inclua variações em português e inglês que recrutadores usam. "
            "Responda APENAS com a lista, um cargo por linha, sem numeração nem explicação."
        )},
        {"role": "user", "content": f"Cargo: {cargo}"}
    ]
    
    resposta = chamar_gpt(
        client,
        msgs,
        temperature=0.3,
        seed=42
    )
    
    if not resposta:
        logger.warning("Falha ao buscar variações — usando cargo original")
        return [cargo]
    
    variacoes = [v.strip() for v in resposta.strip().split('\n') if v.strip()]
    
    # Garantir que o cargo original está incluído (case-insensitive check para evitar duplicatas)
    cargo_lower = cargo.lower()
    if not any(v.lower() == cargo_lower for v in variacoes):
        variacoes.insert(0, cargo)
    
    logger.info(f"Variações encontradas: {variacoes}")
    return variacoes


def gerar_job_description(client, cargo: str) -> Optional[str]:
    """
    Gera uma Job Description composta que cobre o cargo original
    e suas variações de mercado.
    
    Args:
        client: Cliente OpenAI inicializado
        cargo: Nome do cargo para gerar a JD
        
    Returns:
        Job Description gerada ou None em caso de erro
    """
    logger.info(f"Gerando Job Description para: {cargo}")
    
    # Buscar variações de mercado
    variacoes = buscar_variacoes_cargo(client, cargo)
    variacoes_texto = "\n".join(f"- {v}" for v in variacoes)
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento. "
            "Gere uma Job Description (descrição de vaga) realista e completa. "
            "A JD deve cobrir o cargo principal E suas variações de mercado listadas. "
            "Inclua: responsabilidades, requisitos técnicos, soft skills, ferramentas, "
            "qualificações desejadas e diferenciais. "
            "Use termos que sistemas ATS reais buscam. "
            "Inclua palavras-chave tanto em português quanto em inglês. "
            "Responda APENAS com a Job Description, sem introdução nem comentários. "
            "Escreva em português brasileiro."
        )},
        {"role": "user", "content": (
            f"Cargo principal: {cargo}\n\n"
            f"Variações de mercado deste cargo:\n{variacoes_texto}\n\n"
            f"Gere a Job Description cobrindo todos esses perfis."
        )}
    ]
    
    jd = chamar_gpt(
        client,
        msgs,
        temperature=0.3,
        seed=42
    )
    
    if jd:
        logger.info(f"JD composta gerada com sucesso ({len(jd)} caracteres)")
    else:
        logger.error("Falha ao gerar JD")
    
    return jd


def extrair_cargo_do_cv(client, cv_texto: str) -> Optional[str]:
    """
    Extrai o cargo atual/mais recente do candidato a partir do CV.
    
    Args:
        client: Cliente OpenAI inicializado
        cv_texto: Texto completo do CV
        
    Returns:
        Nome do cargo extraído ou None
    """
    logger.info("Extraindo cargo atual do CV")
    
    msgs = [
        {"role": "system", "content": (
            "Analise o CV abaixo e identifique o cargo ATUAL ou MAIS RECENTE do candidato. "
            "Responda APENAS com o nome do cargo, nada mais. "
            "Exemplo de resposta: Gerente de Vendas"
        )},
        {"role": "user", "content": f"CV:\n{cv_texto[:3000]}"}
    ]
    
    cargo = chamar_gpt(
        client,
        msgs,
        temperature=0.1,
        seed=42
    )
    
    if cargo:
        cargo = cargo.strip().strip('"').strip("'")
        logger.info(f"Cargo extraído: {cargo}")
    else:
        logger.error("Falha ao extrair cargo do CV")
    
    return cargo


def calcular_score_ats(cv_texto: str, cargo_alvo: str, client=None) -> Dict:
    """
    Calcula Score ATS usando TF-IDF + Cosine Similarity.
    
    Se um client OpenAI for fornecido, gera uma JD composta via IA
    que cobre o cargo original e variações de mercado.
    Caso contrário, usa o cargo como JD simplificada (fallback).
    
    Args:
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo para gerar a Job Description
        client: Cliente OpenAI (opcional, mas recomendado)
        
    Returns:
        Dict com score_total, percentual, nivel e detalhes
    """
    logger.info(f"Calculando score ATS para cargo: {cargo_alvo}")
    
    # Gerar Job Description composta (com variações de mercado)
    job_description = None
    if client:
        job_description = gerar_job_description(client, cargo_alvo)
    
    # Fallback: usar cargo como texto base
    if not job_description:
        logger.warning("Usando cargo como JD simplificada (sem client OpenAI)")
        job_description = (
            f"Vaga para {cargo_alvo}. "
            f"Requisitos: experiência na área, habilidades técnicas relevantes, "
            f"capacidade de trabalho em equipe, boa comunicação, "
            f"resultados mensuráveis, gestão de projetos, liderança, "
            f"análise de dados, planejamento estratégico."
        )
    
    # Calcular score (nova instância do vectorizer a cada chamada)
    score = _calculate_tfidf_score(cv_texto, job_description)
    
    # Classificar
    nivel = classificar_score(score)
    
    resultado = {
        'score_total': score,
        'max_score': 100,
        'percentual': score,
        'nivel': nivel,
        'cargo_avaliado': cargo_alvo,
        'jd_gerada': job_description is not None,
        'detalhes': {
            'metodo': 'TF-IDF + Cosine Similarity (v2.1)',
            'ngrams': '1-3',
        }
    }
    
    logger.info(f"Score ATS: {score}/100 ({nivel})")
    return resultado


def classificar_score(score: float) -> str:
    """
    Classifica o score ATS em níveis qualitativos.
    
    Args:
        score: Pontuação total (0-100)
        
    Returns:
        Classificação textual do score
    """
    if score >= 70:
        return "Excelente"
    elif score >= 50:
        return "Bom"
    elif score >= 30:
        return "Regular"
    else:
        return "Precisa Melhorar"
