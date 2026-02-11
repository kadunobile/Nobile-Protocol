"""
Etapa 1.5: SEO Mapping (Target) - Perguntas sobre keywords essenciais

Este módulo implementa a etapa de SEO Mapping com as 10 keywords alvo para RevOps.
Faz uma pergunta por tela, apenas para keywords ausentes ou pouco detalhadas no CV.
Usa cache/resumo do CV para economia de tokens e anti-loop para evitar repetição.

HEADHUNTER ELITE: Perguntas cirúrgicas e contextuais para otimização ATS.
"""

import logging
import streamlit as st
from typing import List, Dict, Optional, Tuple
from core.cv_cache import get_cv_contexto_para_prompt
from core.dynamic_questions import adicionar_qa_historico, obter_historico_qa

logger = logging.getLogger(__name__)

# Constants for response validation
MIN_SUBSTANTIVE_RESPONSE_LENGTH = 15  # Minimum length for a substantive response (already defined in dynamic_questions.py)
MIN_NEGATIVE_RESPONSE_LENGTH = 20  # Responses shorter than this are checked for negative keywords

# 10 keywords alvo para RevOps (da especificação)
KEYWORDS_REVOPS = [
    'Revenue Operations (RevOps)',
    'Sales Operations (Sales Ops)',
    'Go-To-Market (GTM) Strategy',
    'Forecast Accuracy',
    'SaaS Metrics (CAC, LTV, Churn, ARR)',
    'Data-Driven Culture',
    'Pipeline Management',
    'Net Revenue Retention (NRR)',
    'Salesforce / CRM Governance',
    'Business Intelligence (Power BI/SQL)'
]

# Mapeamento de keywords para termos que indicam cobertura no CV
KEYWORD_COVERAGE_PATTERNS = {
    'Revenue Operations (RevOps)': ['revops', 'revenue operations', 'operações de receita'],
    'Sales Operations (Sales Ops)': ['sales ops', 'sales operations', 'operações de vendas'],
    'Go-To-Market (GTM) Strategy': ['gtm', 'go-to-market', 'go to market', 'estratégia de mercado', 'lançamento'],
    'Forecast Accuracy': ['forecast', 'previsão', 'acurácia', 'accuracy'],
    'SaaS Metrics (CAC, LTV, Churn, ARR)': ['cac', 'ltv', 'churn', 'arr', 'mrr', 'saas metrics', 'métricas saas'],
    'Data-Driven Culture': ['data-driven', 'data driven', 'cultura de dados', 'orientado a dados'],
    'Pipeline Management': ['pipeline', 'gestão de pipeline', 'gerenciamento de pipeline', 'funil'],
    'Net Revenue Retention (NRR)': ['nrr', 'net revenue retention', 'retenção de receita'],
    'Salesforce / CRM Governance': ['salesforce', 'crm', 'governança', 'governance'],
    'Business Intelligence (Power BI/SQL)': ['power bi', 'powerbi', 'sql', 'tableau', 'business intelligence', 'bi']
}

# Perguntas contextuais curtas para cada keyword (formato exemplo dado na issue)
KEYWORD_QUESTIONS = {
    'Revenue Operations (RevOps)': 
        "Você já estruturou ou liderou uma área de RevOps? Em qual empresa/cargo e qual foi o principal desafio resolvido?",
    'Sales Operations (Sales Ops)': 
        "Você já trabalhou com Sales Ops? Onde (empresa/cargo) e qual processo você otimizou?",
    'Go-To-Market (GTM) Strategy': 
        "Você já definiu ou executou uma estratégia GTM? Para qual produto/empresa e qual foi o resultado?",
    'Forecast Accuracy': 
        "Você já trabalhou com Forecast Accuracy? Onde (empresa/cargo) e qual melhoria (%) no forecast?",
    'SaaS Metrics (CAC, LTV, Churn, ARR)': 
        "Você já acompanhou métricas SaaS (CAC, LTV, Churn, ARR)? Qual métrica você mais monitorou e qual foi o impacto?",
    'Data-Driven Culture': 
        "Você já implementou práticas de Data-Driven Culture? Onde (empresa/cargo) e como mediu a adoção?",
    'Pipeline Management': 
        "Você já gerenciou pipeline de vendas? Qual volume (R$) e como melhorou a conversão ou ciclo de vendas?",
    'Net Revenue Retention (NRR)': 
        "Você já trabalhou com NRR (Net Revenue Retention)? Qual NRR você atingiu ou qual foi o crescimento?",
    'Salesforce / CRM Governance': 
        "Você já implementou governança de CRM/Salesforce? Onde (empresa/cargo) e qual ganho em qualidade de dados (%)?",
    'Business Intelligence (Power BI/SQL)': 
        "Você já criou dashboards ou análises em Power BI/SQL? Qual tipo de análise e para quem (stakeholder)?"
}


def detectar_keywords_cobertas_no_cv(cv_texto: str) -> Dict[str, bool]:
    """
    Detecta quais keywords já estão cobertas (presentes) no CV.
    
    Args:
        cv_texto: Texto completo do CV
        
    Returns:
        Dict[str, bool]: Dicionário com keyword como chave e True/False indicando se está coberta
    """
    cv_lower = cv_texto.lower()
    cobertura = {}
    
    for keyword, patterns in KEYWORD_COVERAGE_PATTERNS.items():
        # Verifica se algum dos padrões está presente no CV
        coberta = any(pattern in cv_lower for pattern in patterns)
        cobertura[keyword] = coberta
        
    logger.debug(f"Keywords cobertas no CV: {sum(cobertura.values())}/{len(cobertura)}")
    return cobertura


def obter_keywords_a_perguntar() -> List[str]:
    """
    Retorna lista de keywords que ainda precisam ser perguntadas.
    
    Considera:
    1. Keywords não cobertas no CV (detectadas via cache)
    2. Keywords ainda não respondidas pelo usuário (anti-loop)
    
    Returns:
        List[str]: Lista de keywords que precisam ser perguntadas
    """
    # Obter texto do CV
    cv_texto = st.session_state.get('cv_texto', '')
    if not cv_texto:
        logger.warning("CV não encontrado para detecção de keywords")
        return []
    
    # Detectar cobertura no CV
    cobertura = detectar_keywords_cobertas_no_cv(cv_texto)
    
    # Obter keywords já respondidas (anti-loop)
    respondidas = st.session_state.get('seo_keywords_respondidas', set())
    
    # Filtrar keywords que precisam ser perguntadas
    # (não cobertas OU pouco detalhadas) E ainda não respondidas
    keywords_a_perguntar = []
    for keyword in KEYWORDS_REVOPS:
        if keyword not in respondidas:
            # Se não está coberta no CV, perguntar
            if not cobertura.get(keyword, False):
                keywords_a_perguntar.append(keyword)
                logger.debug(f"Keyword '{keyword}' não coberta - será perguntada")
    
    logger.info(f"Total de keywords a perguntar: {len(keywords_a_perguntar)}")
    return keywords_a_perguntar


def gerar_pergunta_keyword(keyword: str, keyword_index: int, total_keywords: int) -> str:
    """
    Gera pergunta contextual sobre uma keyword específica.
    
    Args:
        keyword: Keyword a perguntar
        keyword_index: Índice da keyword (0-based)
        total_keywords: Total de keywords a perguntar
        
    Returns:
        str: Pergunta formatada
    """
    cargo = st.session_state.get('perfil', {}).get('cargo_alvo', 'Gerência de RevOps')
    
    # Obter pergunta pré-definida para a keyword
    pergunta = KEYWORD_QUESTIONS.get(keyword, f"Você tem experiência com {keyword}?")
    
    return f"""🎯 **SEO MAPPING (TARGET)** ({keyword_index + 1}/{total_keywords})

**CARGO-ALVO:** {cargo}

---

### Keyword a Otimizar:
**"{keyword}"**

---

**Pergunta para você:**

{pergunta}

💡 **Dica:** Seja específico! Inclua empresa/cargo, contexto e resultados (% ou números quando possível).

❌ **Se não tiver experiência:** Digite "não tenho" para pularmos este item.
"""


def prompt_etapa1_5_seo_intro() -> str:
    """
    Gera prompt de introdução da etapa de SEO Mapping.
    
    Returns:
        str: Prompt formatado com introdução da etapa
    """
    cargo = st.session_state.get('perfil', {}).get('cargo_alvo', 'Gerência de RevOps')
    
    # Calcular quantas keywords serão perguntadas
    keywords_a_perguntar = obter_keywords_a_perguntar()
    total = len(keywords_a_perguntar)
    
    # NOTE: Esta função é chamada apenas se há keywords para perguntar,
    # então total > 0 é garantido pelo processor.py
    if total == 0:
        # Fallback de segurança - não deveria acontecer
        logger.warning("prompt_etapa1_5_seo_intro chamado sem keywords - retornando mensagem de skip")
        return """✅ Não há keywords SEO para otimizar no momento.

Todos os termos essenciais já estão presentes no seu CV!

Vamos prosseguir para a próxima etapa...

Digite "continuar" para prosseguir."""
    
    return f"""### 🎯 ETAPA 2: SEO MAPPING (TARGET)

**CARGO-ALVO:** {cargo}

---

Agora vamos fazer **{total} pergunta(s) curta(s)** sobre competências essenciais que ainda não estão claras no seu CV.

**Por que isso importa?**
- Sistemas ATS (de recrutamento) buscam keywords específicas
- Vou garantir que seu CV contenha as palavras-chave certas para {cargo}

**Como funciona:**
- 1 pergunta por vez, rápida e objetiva
- Se você tiver experiência → responda com contexto (empresa, cargo, resultado)
- Se NÃO tiver experiência → digite "não tenho" para pularmos

---

⏭️ **Vamos começar com a primeira keyword...**
"""


def prompt_etapa1_5_seo_keyword(keyword_index: int) -> Optional[str]:
    """
    Gera prompt para perguntar sobre uma keyword específica.
    
    Args:
        keyword_index: Índice da keyword a perguntar (0-based)
        
    Returns:
        str: Prompt formatado ou None se não há mais keywords
    """
    keywords_a_perguntar = obter_keywords_a_perguntar()
    
    if keyword_index >= len(keywords_a_perguntar):
        # Não há mais keywords para perguntar
        logger.info("Todas as keywords foram perguntadas")
        return None
    
    keyword = keywords_a_perguntar[keyword_index]
    total = len(keywords_a_perguntar)
    
    return gerar_pergunta_keyword(keyword, keyword_index, total)


def processar_resposta_keyword(resposta: str, keyword: str) -> bool:
    """
    Processa a resposta do usuário sobre uma keyword.
    
    Args:
        resposta: Resposta do usuário
        keyword: Keyword que foi perguntada
        
    Returns:
        bool: True se usuário tem experiência, False caso contrário
    """
    # Verificar se é resposta negativa
    NEGATIVE_KEYWORDS = [
        'não tenho', 'nao tenho', 'não possuo', 'nao possuo',
        'nunca tive', 'nunca usei', 'não sei', 'nao sei',
        'desconheço', 'desconheco', 'jamais',
        'sem experiência', 'sem experiencia'
    ]
    
    resposta_lower = resposta.lower().strip()
    
    # Resposta muito curta que é negativa
    if len(resposta_lower) < MIN_NEGATIVE_RESPONSE_LENGTH:
        tem_experiencia = not any(kw in resposta_lower for kw in NEGATIVE_KEYWORDS)
    else:
        # Resposta mais longa - verificar se começa com negativa
        tem_experiencia = True
        for kw in NEGATIVE_KEYWORDS:
            if resposta_lower.startswith(kw):
                tem_experiencia = False
                break
    
    # Adicionar ao histórico de Q&A (para anti-loop)
    adicionar_qa_historico('seo_mapping', KEYWORD_QUESTIONS[keyword], resposta)
    
    # Marcar keyword como respondida
    if 'seo_keywords_respondidas' not in st.session_state:
        st.session_state.seo_keywords_respondidas = set()
    st.session_state.seo_keywords_respondidas.add(keyword)
    
    # Salvar resposta se tem experiência
    if tem_experiencia:
        if 'seo_keywords_respostas' not in st.session_state:
            st.session_state.seo_keywords_respostas = {}
        st.session_state.seo_keywords_respostas[keyword] = resposta
        logger.info(f"Keyword '{keyword}' respondida com experiência")
    else:
        logger.info(f"Keyword '{keyword}' respondida sem experiência")
    
    return tem_experiencia


def gerar_resumo_seo_mapping() -> str:
    """
    Gera resumo da etapa de SEO Mapping após todas as perguntas.
    
    Returns:
        str: Resumo formatado
    """
    respostas = st.session_state.get('seo_keywords_respostas', {})
    respondidas = st.session_state.get('seo_keywords_respondidas', set())
    
    keywords_com_experiencia = list(respostas.keys())
    keywords_sem_experiencia = [k for k in respondidas if k not in respostas]
    
    cargo = st.session_state.get('perfil', {}).get('cargo_alvo', 'Gerência de RevOps')
    
    resumo = f"""### ✅ SEO MAPPING CONCLUÍDO

**CARGO-ALVO:** {cargo}

---

"""
    
    if keywords_com_experiencia:
        resumo += f"""#### ✅ Keywords que você TEM experiência ({len(keywords_com_experiencia)}):

"""
        for keyword in keywords_com_experiencia:
            resposta = respostas[keyword]
            resposta_preview = resposta[:100] + ('...' if len(resposta) > 100 else '')
            resumo += f"""**{keyword}**
📝 _{resposta_preview}_

"""
    
    if keywords_sem_experiencia:
        resumo += f"""
#### ⚠️ Keywords que você NÃO tem experiência ({len(keywords_sem_experiencia)}):

"""
        for keyword in keywords_sem_experiencia:
            resumo += f"- {keyword}\n"
    
    resumo += """
---

### 🎯 Próximo Passo

Agora vou usar essas informações para otimizar seu CV e garantir que ele passe pelos filtros ATS!

"""
    
    return resumo
