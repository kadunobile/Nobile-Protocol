"""
Sistema de Pontuação ATS (Applicant Tracking System) - v3.1.

Usa TF-IDF + Cosine Similarity com stopwords PT/EN expandidas
para calcular compatibilidade entre CV e Job Description gerada por IA.

v3.1 melhorias:
- Stopwords expandidas com verbos genéricos de JD
- Prompt da JD focado em termos técnicos, ferramentas e siglas
- Filtro de n-grams genéricos nos gaps e pontos fortes

Retorna: Score + Pontos Fortes + Gaps + Plano de Ação.
"""

import re
import logging
from typing import Dict, Optional, List

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from core.utils import chamar_gpt

logger = logging.getLogger(__name__)

# Stopwords PT + EN — palavras que o ATS deve ignorar
# Inclui verbos genéricos de Job Descriptions que aparecem em QUALQUER vaga
STOPWORDS_PT_EN = [
    # Artigos, preposições, pronomes PT
    'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no',
    'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu',
    'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só', 'pelo',
    'pela', 'até', 'isso', 'ela', 'entre', 'era', 'depois', 'sem', 'mesmo', 'aos', 'ter', 'seus',
    'quem', 'nas', 'me', 'esse', 'eles', 'estão', 'você', 'tinha', 'foram', 'essa', 'num', 'nem',
    'suas', 'meu', 'às', 'minha', 'têm', 'numa', 'pelos', 'elas', 'havia', 'seja', 'qual', 'será',
    'nós', 'tenho', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'fosse', 'dele', 'tu', 'te',
    'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos',
    'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas',
    'isto', 'aquilo', 'estou', 'estamos', 'estive', 'esteve', 'estivemos', 'estiveram',
    'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 'estejam',
    'estivesse', 'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei',
    'havemos', 'hão', 'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos',
    'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos', 'houverem', 'houverei',
    'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos',
    'são', 'éramos', 'eram', 'fui', 'fomos', 'fora', 'fôramos',
    'sejamos', 'sejam', 'fôssemos', 'fossem', 'for', 'formos', 'forem', 'serei',
    'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'temos', 'tém',
    'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha',
    'tenhamos', 'tenham', 'tivesse', 'tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei',
    'terá', 'teremos', 'terão', 'teria', 'teríamos', 'teriam',
    # Preposições e conjunções EN
    'and', 'to', 'the', 'of', 'in', 'for', 'with', 'on', 'at', 'from', 'by', 'about', 'as', 'into',
    'like', 'through', 'after', 'over', 'between', 'out', 'against', 'during', 'without', 'before',
    'under', 'around', 'among', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'shall',
    'can', 'need', 'must', 'it', 'its', 'this', 'that', 'these', 'those', 'we', 'they', 'you',
    'he', 'she', 'i', 'my', 'your', 'his', 'her', 'our', 'their', 'an', 'a', 'or', 'but', 'not',
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
    # ─── PALAVRAS GENÉRICAS DE JD ───
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
]


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
    termos_faltantes = df_analise[
        (df_analise['peso_vaga'] > 0) & (df_analise['peso_cv'] == 0)
    ].sort_values(by='peso_vaga', ascending=False).head(10)
    
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


def buscar_variacoes_cargo(client, cargo: str) -> List[str]:
    """
    Usa IA para encontrar variações de mercado de um cargo.
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
    Gera uma Job Description focada em TERMOS TÉCNICOS, ferramentas,
    metodologias e siglas da área — não em verbos genéricos.
    """
    logger.info(f"Gerando Job Description técnica para: {cargo}")
    
    variacoes = buscar_variacoes_cargo(client, cargo)
    variacoes_texto = "\n".join(f"- {v}" for v in variacoes)
    
    msgs = [
        {"role": "system", "content": (
            "Você é um especialista em recrutamento técnico e sistemas ATS. "
            "Gere uma Job Description para o cargo informado focada EXCLUSIVAMENTE em:\n"
            "- Ferramentas e softwares específicos (ex: Salesforce, Power BI, HubSpot, SAP)\n"
            "- Metodologias e frameworks (ex: Scrum, Kanban, OKR, Six Sigma)\n"
            "- Siglas e termos técnicos da área (ex: CAC, LTV, NRR, ARR, SQL, KPI)\n"
            "- Certificações relevantes (ex: PMP, AWS, Google Analytics)\n"
            "- Tecnologias e linguagens (ex: Python, SQL, Power Query, DAX)\n"
            "- Conceitos técnicos específicos (ex: forecasting, pipeline, churn, revenue operations)\n\n"
            "NÃO use verbos genéricos como 'desenvolver', 'gerenciar', 'implementar', 'coordenar'. "
            "NÃO use frases genéricas como 'trabalho em equipe', 'boa comunicação', 'proatividade'. "
            "Foque 100% em termos que DIFERENCIAM candidatos em sistemas ATS.\n\n"
            "A JD deve cobrir o cargo principal E suas variações de mercado.\n"
            "Inclua termos em português E inglês.\n"
            "Responda APENAS com a Job Description, sem introdução."
        )},
        {"role": "user", "content": (
            f"Cargo principal: {cargo}\n\n"
            f"Variações de mercado:\n{variacoes_texto}\n\n"
            f"Gere a Job Description TÉCNICA cobrindo todos esses perfis."
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
    
    Args:
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo para gerar a Job Description
        client: Cliente OpenAI (opcional, mas recomendado)
        
    Returns:
        Dict com score_total, percentual, nivel, pontos_fortes,
        gaps_identificados, plano_acao e detalhes
    """
    logger.info(f"Calculando score ATS para cargo: {cargo_alvo}")
    
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
            'metodo': 'TF-IDF + Cosine Similarity (v3.1)',
            'ngrams': '1-3',
            'stopwords': 'PT + EN + Verbos genéricos JD',
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
