"""
Sistema de Pontuação ATS (Applicant Tracking System) - v4.0.

v4.0: Análise contextual via LLM (GPT-4o) com fallback TF-IDF.
- Quando OpenAI client disponível: análise semântica inteligente
- Quando offline: TF-IDF + Cosine Similarity (v3.2)

v3.2 (fallback):
- TF-IDF + Cosine Similarity com stopwords NLTK (PT/EN) + termos customizados
- Prompt da JD focado em termos técnicos, ferramentas e siglas
- Filtro de n-grams genéricos nos gaps e pontos fortes

Retorna: Score + Pontos Fortes + Gaps + Plano de Ação.
"""

import re
import json
import logging
from typing import Dict, Optional, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk

# Garantir download dos stopwords na primeira execução
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords

from core.utils import chamar_gpt

logger = logging.getLogger(__name__)

# ─── STOPWORDS: NLTK (PT + EN) + Termos customizados de CV/JD ───
# Base robusta do NLTK (~400 stopwords PT + EN)
_nltk_stops = set(stopwords.words('portuguese')).union(set(stopwords.words('english')))

# Termos customizados específicos de CV e Job Descriptions
_custom_stops = {
    # ─── VERBOS GENÉRICOS DE JD (aparecem em QUALQUER vaga) ───
    'desenvolver', 'gerenciar', 'impulsionar', 'otimizar', 'garantir', 'implementar',
    'coordenar', 'supervisionar', 'elaborar', 'executar', 'planejar', 'monitorar',
    'acompanhar', 'realizar', 'conduzir', 'promover', 'apoiar', 'contribuir',
    'participar', 'atuar', 'assegurar', 'propor', 'definir', 'estabelecer',
    'manter', 'identificar', 'analisar', 'avaliar', 'gerir', 'liderar',
    'orientar', 'direcionar', 'facilitar', 'viabilizar', 'fomentar',
    'aprimorar', 'estruturar', 'organizar', 'controlar', 'reportar',
    'comunicar', 'interagir', 'colaborar', 'integrar', 'alinhar',
    'priorizar', 'delegar', 'negociar', 'articular', 'mapear',
    'diagnosticar', 'solucionar', 'resolver', 'mitigar', 'prevenir',
    'develop', 'manage', 'drive', 'optimize', 'ensure', 'implement',
    'coordinate', 'supervise', 'execute', 'plan', 'monitor',
    'track', 'conduct', 'promote', 'support', 'contribute',
    'participate', 'maintain', 'identify', 'analyze', 'evaluate',
    'lead', 'guide', 'direct', 'facilitate', 'foster',
    'enhance', 'structure', 'organize', 'control', 'report',
    'communicate', 'collaborate', 'integrate', 'align', 'prioritize',
    'delegate', 'negotiate', 'deliver', 'build', 'create', 'design',
    'establish', 'provide', 'work', 'handle', 'oversee', 'prepare',
    # ─── PALAVRAS GENÉRICAS DE JD / CV ───
    'empresa', 'área', 'equipe', 'time', 'profissional', 'candidato',
    'experiência', 'conhecimento', 'habilidade', 'capacidade', 'competência',
    'responsável', 'responsabilidade', 'atividade', 'atividades', 'função',
    'objetivo', 'resultado', 'resultados', 'processo', 'processos',
    'projeto', 'projetos', 'solução', 'soluções', 'estratégia', 'estratégias',
    'nível', 'alto', 'alta', 'forte', 'fortes', 'sólida', 'sólido',
    'bom', 'boa', 'bons', 'boas', 'excelente', 'excelentes',
    'desejável', 'desejáveis', 'necessário', 'necessária', 'obrigatório', 'obrigatória',
    'diferencial', 'diferenciais', 'requisito', 'requisitos',
    'mínimo', 'mínima', 'anos', 'ano', 'superior', 'completo', 'completa',
    'graduação', 'formação', 'pós', 'curso', 'cursos',
    'trabalho', 'mercado', 'negócio', 'negócios', 'cliente', 'clientes',
    'interno', 'interna', 'internos', 'internas', 'externo', 'externa',
    'relacionamento', 'relacionamentos', 'parceiro', 'parceiros',
    'demanda', 'demandas', 'necessidade', 'necessidades',
    'oportunidade', 'oportunidades', 'melhoria', 'melhorias',
    'indicador', 'indicadores', 'meta', 'metas',
    'relatório', 'relatórios', 'report', 'reports',
    'reunião', 'reuniões', 'apresentação', 'apresentações',
    'prazo', 'prazos', 'entrega', 'entregas',
    'qualidade', 'eficiência', 'produtividade',
    'inovação', 'transformação', 'crescimento',
    'visão', 'missão', 'valor', 'valores', 'cultura',
    'based', 'ability', 'skills', 'skill', 'experience', 'knowledge',
    'team', 'company', 'business', 'role', 'position',
    'responsible', 'required', 'preferred', 'minimum', 'years',
    'strong', 'excellent', 'good', 'proven', 'relevant',
    'including', 'related', 'across', 'within', 'using',
    'new', 'key', 'high', 'level', 'well',
    # ─── TERMOS DE CV (endereço, meses, etc.) ───
    'cargo', 'janeiro', 'fevereiro', 'março', 'abril',
    'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
    'novembro', 'dezembro', 'jan', 'fev', 'mar', 'abr', 'mai', 'jun',
    'jul', 'ago', 'set', 'out', 'nov', 'dez',
    'paulo', 'são', 'rio', 'brasil', 'br', 'rua', 'apto', 'cep',
    'presente', 'atual', 'atualmente',
    # ─── CONECTORES E TERMOS VAZIOS ───
    'além', 'disso', 'assim', 'ainda', 'sobre', 'cada', 'todo', 'toda',
    'todos', 'todas', 'outro', 'outra', 'outros', 'outras',
    'onde', 'aqui', 'ali', 'lá', 'então', 'portanto', 'porém',
    'contudo', 'entretanto', 'todavia', 'pois', 'porque', 'embora',
    'caso', 'conforme', 'segundo', 'através', 'meio', 'forma',
    'modo', 'tipo', 'parte', 'fim', 'base', 'dia', 'vez',
    'vezes', 'bem', 'mal', 'demais', 'menos', 'tanto',
    'quanto', 'tal', 'tais', 'apenas', 'somente',
    'principalmente', 'especialmente', 'geralmente', 'normalmente',
    'diretamente', 'indiretamente', 'constantemente', 'continuamente',
    'relacionadas', 'relacionados', 'relacionada', 'relacionado',
    'adequada', 'adequado', 'adequadas', 'adequados',
    'efetiva', 'efetivo', 'efetivas', 'efetivos',
}

# Combinar: NLTK base (~400) + Custom (~150) = ~550+ stopwords
STOPWORDS_PT_EN = list(_nltk_stops.union(_custom_stops))

# ─── Termos genéricos que nunca devem aparecer como gap ───
_termos_genericos_gap = {
    'certified', 'certification', 'certificate',
    'qualified', 'qualification',
    'senior', 'junior', 'pleno', 'sênior', 'júnior',
    'manager', 'lead', 'head', 'director', 'chief',
    'gerente', 'coordenador', 'analista', 'especialista',
    'supervisor', 'diretor', 'líder',
    'six', 'sigma',
    'proficiency', 'proficient', 'fluent', 'fluency',
    'operations', 'operações', 'revenue', 'receita',
    'engineer', 'engenheiro', 'developer', 'desenvolvedor', 'software',
    'analyst', 'consultor', 'consultant',
}


def _limpar_texto(texto: str) -> str:
    """Padroniza o texto para análise."""
    texto = str(texto).lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto


def _analisar_compatibilidade(cv_texto: str, vaga_texto: str) -> Dict:
    """
    Executa análise completa: Score + Gaps + Pontos Fortes + Plano de Ação.
    
    Cria uma NOVA instância do TfidfVectorizer a cada chamada.
    
    Args:
        cv_texto: Texto completo do CV
        vaga_texto: Job Description para comparação
        
    Returns:
        Dict com score, pontos_fortes, gaps_identificados, plano_acao
    """
    cv_limpo = _limpar_texto(cv_texto)
    vaga_limpa = _limpar_texto(vaga_texto)
    
    if not cv_limpo or not vaga_limpa:
        logger.warning("CV ou JD vazio após limpeza")
        return {
            "score": 0.0,
            "pontos_fortes": [],
            "gaps_identificados": [],
            "plano_acao": ["❌ Texto insuficiente para análise."]
        }
    
    try:
        vectorizer = TfidfVectorizer(
            stop_words=STOPWORDS_PT_EN,
            ngram_range=(1, 3),
            min_df=1
        )
        
        tfidf_matrix = vectorizer.fit_transform([cv_limpo, vaga_limpa])
        feature_names = vectorizer.get_feature_names_out()
        
    except ValueError as e:
        logger.error(f"Erro na vetorização: {e}")
        return {
            "score": 0.0,
            "pontos_fortes": [],
            "gaps_identificados": [],
            "plano_acao": ["❌ Texto insuficiente para análise."]
        }
    
    # Score (Cosine Similarity)
    raw_similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    
    # Escalar para faixa realista
    if raw_similarity <= 0.0:
        score_final = 0.0
    elif raw_similarity >= 0.35:
        score_final = 95.0
    else:
        score_final = (raw_similarity / 0.35) * 90.0 + 5.0
    
    score_final = round(score_final, 1)
    
    logger.debug(f"Raw similarity: {raw_similarity:.4f}, Scaled score: {score_final}")
    logger.debug(f"Vocabulário: {len(feature_names)} termos (após stopwords)")
    
    # Análise de termos
    dense = tfidf_matrix.todense()
    lista_cv = dense[0].tolist()[0]
    lista_vaga = dense[1].tolist()[0]
    
    df_analise = pd.DataFrame({
        'termo': feature_names,
        'peso_vaga': lista_vaga,
        'peso_cv': lista_cv
    })
    
    # Gaps: termos da vaga que NÃO estão no CV
    termos_faltantes_raw = df_analise[
        (df_analise['peso_vaga'] > 0) & (df_analise['peso_cv'] == 0)
    ].sort_values(by='peso_vaga', ascending=False)
    
    # Filtrar: remover termos genéricos e n-grams que são apenas títulos de cargo
    def _is_generic_term(termo: str) -> bool:
        """Verifica se um termo deve ser filtrado dos gaps."""
        # Remover siglas muito curtas
        if len(termo) <= 2:
            return True
        
        # Remover se é termo genérico standalone
        if termo in _termos_genericos_gap:
            return True
        
        # Remover n-grams que contêm palavras genéricas
        palavras_termo = termo.split()
        for palavra in palavras_termo:
            if palavra in _termos_genericos_gap:
                return True
        
        return False
    
    termos_faltantes = termos_faltantes_raw[
        ~termos_faltantes_raw['termo'].apply(_is_generic_term)
    ].head(10)
    
    # Pontos fortes: termos que ambos têm
    pontos_fortes = df_analise[
        (df_analise['peso_vaga'] > 0) & (df_analise['peso_cv'] > 0)
    ].sort_values(by='peso_cv', ascending=False).head(8)
    
    # Plano de ação
    plano = []
    
    if score_final >= 70:
        plano.append("🏆 Excelente compatibilidade! Seu perfil está bem alinhado com o cargo. Foque em se preparar para entrevistas comportamentais.")
    elif score_final >= 50:
        plano.append("⚠️ Boa base, mas pode melhorar. Adicione as palavras-chave faltantes no seu perfil para aumentar suas chances nos filtros automáticos.")
    elif score_final >= 30:
        plano.append("🔶 Compatibilidade moderada. Seu perfil precisa de ajustes para passar pelos filtros ATS. Revise as palavras-chave e experiências.")
    else:
        plano.append("❌ Risco de eliminação automática. Seu perfil precisa de uma revisão estrutural para este cargo.")
    
    if not termos_faltantes.empty:
        lista_gaps = termos_faltantes['termo'].tolist()
        plano.append(
            f"🔍 Palavras-chave ausentes no seu perfil: **{', '.join(lista_gaps[:7]).upper()}**. "
            f"Tente incluí-las no Resumo, Competências ou Experiência."
        )
    
    return {
        "score": score_final,
        "pontos_fortes": pontos_fortes['termo'].tolist(),
        "gaps_identificados": termos_faltantes['termo'].tolist(),
        "plano_acao": plano
    }


def _analisar_com_llm(client, cv_texto: str, cargo_alvo: str) -> Optional[Dict]:
    """
    Analisa CV usando LLM (GPT-4o) para análise contextual inteligente.
    
    Substitui a análise TF-IDF quando o client OpenAI está disponível.
    A LLM entende contexto, sinônimos e variações, gerando gaps e pontos fortes
    mais relevantes e específicos.
    
    Args:
        client: Cliente OpenAI inicializado
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo para o qual está se candidatando
        
    Returns:
        Dict com score, pontos_fortes, gaps_identificados, plano_acao ou None em caso de erro
    """
    logger.info(f"Analisando CV com LLM para cargo: {cargo_alvo}")
    
    # Prompt engineering baseado nas regras de ouro do problema
    msgs = [
        {"role": "system", "content": (
            "Você é um Especialista Sênior em ATS (Applicant Tracking System) e Recrutamento Tech.\n\n"
            "Sua missão é analisar o CV do candidato em comparação com as expectativas REAIS do cargo informado.\n\n"
            "REGRAS DE OURO:\n\n"
            "1. **Pontos Fortes**: Liste APENAS Hard Skills, Ferramentas (Software), Metodologias específicas e "
            "Métricas de Negócio que o candidato REALMENTE demonstra no CV.\n"
            "   - ✅ INCLUIR: Salesforce, HubSpot, Power BI, Tableau, SQL, Python, Scrum, OKRs, pipeline management, B2B SaaS, métricas específicas\n"
            "   - ❌ NÃO INCLUIR: termos genéricos como 'gestão', 'vendas', 'liderança', 'comunicação', 'dados'\n\n"
            "2. **Gaps**: Liste APENAS Hard Skills, Ferramentas e Certificações que são padrão OBRIGATÓRIO "
            "para o cargo no mercado real.\n"
            "   - ✅ INCLUIR: Ferramentas específicas faltantes (Tableau, Looker, Marketo), certificações relevantes (PMP, AWS), SQL avançado, ABM\n"
            "   - ❌ NÃO INCLUIR: stopwords ('TÉCNICOS', 'PREVISÃO', 'DESEMPENHO', 'INTEGRAÇÃO'), verbos genéricos, "
            "erros de tradução, fragmentos sem contexto ('RATE', 'RATE TAXA', 'BI' isolado), n-grams genéricos\n\n"
            "3. **Considere Sinônimos e Variações**:\n"
            "   - 'BI' = 'Power BI' = 'Business Intelligence'\n"
            "   - 'automação de marketing' pode cobrir 'Marketing Automation'\n"
            "   - Avalie contextualmente — se o CV menciona algo relacionado, não marque como gap\n\n"
            "4. **Score (0-100)**: Avalie considerando:\n"
            "   - Presença de ferramentas específicas: 40%\n"
            "   - Métricas quantificáveis: 20%\n"
            "   - Alinhamento de experiência com o cargo: 20%\n"
            "   - Formatação ATS-friendly: 10%\n"
            "   - Keywords estratégicas: 10%\n\n"
            "5. **Plano de Ação**: Dê 2-3 recomendações práticas e específicas, começando com emoji relevante "
            "(🔍, ⚠️, 🏆, ❌, 🔶 dependendo do score).\n\n"
            "RESPONDA APENAS COM UM JSON VÁLIDO (sem markdown, sem explicações extras):\n"
            "```json\n"
            # Exemplo de JSON esperado (mantido inline para clareza do prompt)
            "{\n"
            '    "score": 65.0,\n'
            '    "pontos_fortes": ["Salesforce", "HubSpot", "Power BI", "pipeline management", "B2B SaaS"],\n'
            '    "gaps_identificados": ["Tableau", "Looker", "SQL avançado", "Marketo", "ABM"],\n'
            '    "plano_acao": ["🔍 Palavras-chave ausentes...", "⚠️ Boa base, mas..."]\n'
            "}\n"
            "```"
        )},
        {"role": "user", "content": (
            f"CARGO ALVO: {cargo_alvo}\n\n"
            f"CV DO CANDIDATO:\n{cv_texto[:8000]}\n\n"  # Limitar a ~8000 chars (evita contextos muito grandes)
            f"Analise este CV para o cargo '{cargo_alvo}' e retorne o JSON conforme as regras."
        )}
    ]
    
    # Chamar LLM com máxima consistência
    resposta = chamar_gpt(client, msgs, temperature=0.2, seed=42)
    
    if not resposta:
        logger.warning("Falha ao obter resposta da LLM")
        return None
    
    # Parse do JSON da resposta
    try:
        # A resposta pode vir com blocos ```json ou JSON puro
        resposta_limpa = resposta.strip()
        
        # Remover blocos markdown se existirem
        if resposta_limpa.startswith("```json"):
            resposta_limpa = resposta_limpa.split("```json", 1)[1]
            resposta_limpa = resposta_limpa.rsplit("```", 1)[0]
        elif resposta_limpa.startswith("```"):
            resposta_limpa = resposta_limpa.split("```", 1)[1]
            resposta_limpa = resposta_limpa.rsplit("```", 1)[0]
        
        resposta_limpa = resposta_limpa.strip()
        
        # Parse do JSON
        resultado = json.loads(resposta_limpa)
        
        # Validar estrutura esperada
        if not all(k in resultado for k in ['score', 'pontos_fortes', 'gaps_identificados', 'plano_acao']):
            logger.error("Resposta LLM não contém todas as chaves esperadas")
            return None
        
        # Validar tipos
        if not isinstance(resultado['score'], (int, float)):
            logger.error("Score não é numérico")
            return None
        if not isinstance(resultado['pontos_fortes'], list):
            logger.error("pontos_fortes não é lista")
            return None
        if not isinstance(resultado['gaps_identificados'], list):
            logger.error("gaps_identificados não é lista")
            return None
        if not isinstance(resultado['plano_acao'], list):
            logger.error("plano_acao não é lista")
            return None
        
        logger.info(f"Análise LLM concluída com sucesso. Score: {resultado['score']}")
        return resultado
        
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao fazer parse do JSON da LLM: {e}")
        logger.debug(f"Resposta recebida: {resposta[:500]}")
        return None
    except Exception as e:
        logger.error(f"Erro inesperado ao processar resposta da LLM: {e}", exc_info=True)
        return None


def buscar_variacoes_cargo(client, cargo: str) -> List[str]:
    """
    Usa IA para encontrar variações REAIS de mercado de um cargo.
    """
    logger.info(f"Buscando variações de mercado para: {cargo}")
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento no Brasil e mercado de trabalho. "
            "Dado um cargo, liste entre 5 e 8 variações REAIS desse cargo como aparecem "
            "em vagas publicadas no LinkedIn, Gupy, Catho e Indeed. "
            "Inclua variações em português E inglês que recrutadores REALMENTE usam. "
            "Mantenha o mesmo nível hierárquico (se é gerente, liste cargos de gerência). "
            "NÃO invente cargos — liste apenas os que EXISTEM no mercado real. "
            "Responda APENAS com a lista, um cargo por linha, sem numeração nem explicação."
        )},
        {"role": "user", "content": f"Cargo: {cargo}"}
    ]
    
    resposta = chamar_gpt(client, msgs, temperature=0.3, seed=42)
    
    if not resposta:
        logger.warning("Falha ao buscar variações — usando cargo original")
        return [cargo]
    
    variacoes = [v.strip() for v in resposta.strip().split('\n') if v.strip()]
    if cargo not in variacoes:
        variacoes.insert(0, cargo)
    
    logger.info(f"Variações encontradas: {variacoes}")
    return variacoes


def gerar_job_description(client, cargo: str) -> Optional[str]:
    """
    Gera uma Job Description focada em TERMOS TÉCNICOS reais do cargo,
    sem exemplos genéricos que contaminam a análise.
    """
    logger.info(f"Gerando Job Description técnica para: {cargo}")
    
    variacoes = buscar_variacoes_cargo(client, cargo)
    variacoes_texto = "\n".join(f"- {v}" for v in variacoes)
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento técnico e sistemas ATS no Brasil.\n\n"
            "Gere uma Job Description para o cargo informado focada EXCLUSIVAMENTE em:\n"
            "- Ferramentas e softwares ESPECÍFICOS da área desse cargo\n"
            "- Metodologias e frameworks REALMENTE usados nesse cargo\n"
            "- Siglas e termos técnicos ESPECÍFICOS dessa função\n"
            "- Certificações relevantes APENAS para esse cargo\n"
            "- Tecnologias REALMENTE exigidas nessa função\n"
            "- Conceitos técnicos ESPECÍFICOS dessa área\n\n"
            "REGRAS CRÍTICAS:\n"
            "- NÃO inclua termos genéricos de outras áreas\n"
            "- NÃO use exemplos que não sejam da área do cargo\n"
            "- NÃO inclua ferramentas/metodologias irrelevantes para a função\n"
            "- Cada termo mencionado deve ser algo que um recrutador REALMENTE "
            "buscaria ao filtrar candidatos para ESSE cargo específico\n"
            "- NÃO use verbos genéricos como 'desenvolver', 'gerenciar', 'implementar'\n"
            "- NÃO use frases genéricas como 'trabalho em equipe', 'boa comunicação'\n\n"
            "A JD deve cobrir o cargo principal E suas variações de mercado.\n"
            "Inclua termos em português E inglês.\n"
            "Responda APENAS com a Job Description, sem introdução."
        )},
        {"role": "user", "content": (
            f"Cargo principal: {cargo}\n\n"
            f"Variações de mercado:\n{variacoes_texto}\n\n"
            f"Gere a Job Description TÉCNICA cobrindo APENAS termos relevantes "
            f"para esse cargo específico e suas variações."
        )}
    ]
    
    jd = chamar_gpt(client, msgs, temperature=0.3, seed=42)
    
    if jd:
        logger.info(f"JD técnica gerada ({len(jd)} chars)")
    else:
        logger.error("Falha ao gerar JD")
    
    return jd


def extrair_cargo_do_cv(client, cv_texto: str) -> Optional[str]:
    """
    Extrai o cargo atual/mais recente do candidato a partir do CV.
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
    
    cargo = chamar_gpt(client, msgs, temperature=0.1, seed=42)
    
    if cargo:
        cargo = cargo.strip().strip('"').strip("'")
        logger.info(f"Cargo extraído: {cargo}")
    else:
        logger.error("Falha ao extrair cargo do CV")
    
    return cargo


def calcular_score_ats(cv_texto: str, cargo_alvo: str, client=None) -> Dict:
    """
    Calcula Score ATS completo com análise de gaps técnicos.
    
    v4.0: Usa LLM quando client disponível, senão fallback para TF-IDF.
    
    Args:
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo para gerar a Job Description
        client: Cliente OpenAI (opcional, mas recomendado para análise LLM)
        
    Returns:
        Dict com score_total, percentual, nivel, pontos_fortes,
        gaps_identificados, plano_acao e detalhes
    """
    logger.info(f"Calculando score ATS para cargo: {cargo_alvo}")
    
    # ─── TENTATIVA 1: Análise LLM (v4.0) ───
    if client:
        logger.info("Client OpenAI disponível - usando análise LLM (v4.0)")
        analise_llm = _analisar_com_llm(client, cv_texto, cargo_alvo)
        
        if analise_llm:
            # Usar resultado da LLM
            score = analise_llm['score']
            nivel = classificar_score(score)
            
            logger.info(f"Análise LLM bem-sucedida. Score: {score}/100 ({nivel})")
            
            return {
                'score_total': score,
                'max_score': 100,
                'percentual': score,
                'nivel': nivel,
                'cargo_avaliado': cargo_alvo,
                'pontos_fortes': analise_llm['pontos_fortes'],
                'gaps_identificados': analise_llm['gaps_identificados'],
                'plano_acao': analise_llm['plano_acao'],
                'jd_gerada': True,
                'detalhes': {
                    'metodo': 'LLM Contextual Analysis (v4.0)',
                    'modelo': 'GPT-4o',
                    'fallback': False,
                    # Compatibilidade com UI existente - campos vazios mas presentes
                    'secoes': {'score': 0, 'encontradas': 0, 'total': 0},
                    'keywords': {'score': 0, 'encontradas': 0, 'total': 0, 'faltando': []},
                    'metricas': {'score': 0, 'quantidade': 0},
                    'formatacao': {'score': 0, 'bullets': 0, 'datas': 0},
                    'tamanho': {'score': 0, 'palavras': 0, 'ideal': 'N/A'},
                }
            }
        else:
            logger.warning("Análise LLM falhou - caindo para fallback TF-IDF")
    else:
        logger.info("Client OpenAI não disponível - usando fallback TF-IDF (v3.2)")
    
    # ─── FALLBACK: Análise TF-IDF (v3.2) ───
    job_description = None
    if client:
        job_description = gerar_job_description(client, cargo_alvo)
    
    if not job_description:
        logger.warning("Usando JD simplificada")
        job_description = (
            f"Vaga para {cargo_alvo}. "
            f"Requisitos: experiência na área, habilidades técnicas relevantes, "
            f"capacidade de trabalho em equipe, boa comunicação, "
            f"resultados mensuráveis, gestão de projetos, liderança, "
            f"análise de dados, planejamento estratégico."
        )
    
    analise = _analisar_compatibilidade(cv_texto, job_description)
    
    score = analise['score']
    nivel = classificar_score(score)
    
    resultado = {
        'score_total': score,
        'max_score': 100,
        'percentual': score,
        'nivel': nivel,
        'cargo_avaliado': cargo_alvo,
        'pontos_fortes': analise['pontos_fortes'],
        'gaps_identificados': analise['gaps_identificados'],
        'plano_acao': analise['plano_acao'],
        'jd_gerada': job_description is not None,
        'detalhes': {
            'metodo': 'TF-IDF + Cosine Similarity (v3.2 - Fallback)',
            'ngrams': '1-3',
            'stopwords': 'NLTK (PT + EN) + Custom CV/JD (~550+)',
            'fallback': True,
        }
    }
    
    logger.info(f"Score ATS: {score}/100 ({nivel})")
    return resultado


def classificar_score(score: float) -> str:
    """Classifica o score ATS em níveis qualitativos."""
    if score >= 70:
        return "Excelente"
    elif score >= 50:
        return "Bom"
    elif score >= 30:
        return "Regular"
    else:
        return "Precisa Melhorar"
