"""
Modelo de dados estruturado para acumular informações do CV ao longo do fluxo de otimização.

Este módulo define a estrutura JSON que armazena todos os dados coletados durante
o processo de otimização, permitindo que o output final use informações reais
ao invés de placeholders.
"""

import re
import streamlit as st
from typing import Dict, List, Any, Optional


def inicializar_cv_estruturado() -> Dict[str, Any]:
    """
    Inicializa estrutura de dados vazia para acumular informações do CV.
    
    Esta estrutura é preenchida ao longo das etapas do fluxo de otimização:
    - Diagnóstico: gaps identificados e respostas
    - Coleta: dados detalhados sobre experiências
    - Validação: posicionamento e estratégia
    - Reescrita: experiências otimizadas
    - LinkedIn: headline, skills, about
    
    Returns:
        Dict contendo estrutura completa inicializada com valores vazios
    """
    return {
        "header": {
            "nome": "",
            "telefone": "",
            "email": "",
            "linkedin": "",
            "localizacao": ""
        },
        "posicionamento": {
            "cargo_alvo": "",
            "estrategia": "",
            "senioridade_real": "",
            "diferencial": ""
        },
        "summary": "",
        "keywords_ats": [],
        "experiencias": [],  # Lista de dicts com empresa, cargo, periodo, conquistas
        "educacao": [],
        "idiomas": [],
        "certificacoes": [],
        "linkedin": {
            "headline": "",
            "headline_opcoes": [],  # Opções A, B, C geradas
            "skills": [],
            "about": ""
        },
        "gaps": {
            "identificados": [],
            "resolvidos": [],
            "nao_resolvidos": []
        },
        "metricas_coletadas": {
            "volumes": [],  # Ex: "Gerenciei 50+ processos/mês"
            "ferramentas": [],  # Ex: "SAP, Salesforce, Python"
            "resultados": [],  # Ex: "Reduzi custos em 30%"
            "equipe": []  # Ex: "Liderava equipe de 5 pessoas"
        }
    }


def salvar_dados_coleta(dados: Dict[str, Any]) -> None:
    """
    Salva dados coletados na estrutura de CV estruturado.
    
    Args:
        dados: Dicionário com dados coletados (raw_response, metricas, etc)
    """
    if 'cv_estruturado' not in st.session_state:
        st.session_state.cv_estruturado = inicializar_cv_estruturado()
    
    # Extrair e organizar dados coletados
    cv_est = st.session_state.cv_estruturado
    
    if 'raw_response' in dados:
        # Processar resposta bruta para identificar métricas
        resposta = dados['raw_response']
        
        # Buscar números e percentuais (métricas)
        metricas = re.findall(r'\d+[%]?|\d+\+', resposta)
        if metricas:
            cv_est['metricas_coletadas']['volumes'].extend(metricas)
    
    if 'ferramentas' in dados:
        cv_est['metricas_coletadas']['ferramentas'].extend(dados['ferramentas'])
    
    if 'resultados' in dados:
        cv_est['metricas_coletadas']['resultados'].extend(dados['resultados'])
    
    st.session_state.cv_estruturado = cv_est


def adicionar_experiencia(experiencia: Dict[str, Any]) -> None:
    """
    Adiciona uma experiência profissional otimizada à estrutura.
    
    Args:
        experiencia: Dict com empresa, cargo, periodo, conquistas
    """
    if 'cv_estruturado' not in st.session_state:
        st.session_state.cv_estruturado = inicializar_cv_estruturado()
    
    st.session_state.cv_estruturado['experiencias'].append(experiencia)


def atualizar_posicionamento(cargo_alvo: str, estrategia: str = "", 
                             senioridade: str = "", diferencial: str = "") -> None:
    """
    Atualiza o posicionamento estratégico do candidato.
    
    Args:
        cargo_alvo: Cargo desejado
        estrategia: Estratégia de posicionamento
        senioridade: Nível de senioridade identificado
        diferencial: Diferencial competitivo
    """
    if 'cv_estruturado' not in st.session_state:
        st.session_state.cv_estruturado = inicializar_cv_estruturado()
    
    pos = st.session_state.cv_estruturado['posicionamento']
    if cargo_alvo:
        pos['cargo_alvo'] = cargo_alvo
    if estrategia:
        pos['estrategia'] = estrategia
    if senioridade:
        pos['senioridade_real'] = senioridade
    if diferencial:
        pos['diferencial'] = diferencial


def atualizar_linkedin(headline: str = "", skills: List[str] = None, 
                       about: str = "", headline_opcoes: List[str] = None) -> None:
    """
    Atualiza dados de otimização do LinkedIn.
    
    Args:
        headline: Headline escolhida
        skills: Lista de skills otimizadas
        about: Texto do About/Summary otimizado
        headline_opcoes: Opções A/B/C geradas
    """
    if 'cv_estruturado' not in st.session_state:
        st.session_state.cv_estruturado = inicializar_cv_estruturado()
    
    linkedin = st.session_state.cv_estruturado['linkedin']
    if headline:
        linkedin['headline'] = headline
    if skills is not None:
        linkedin['skills'] = skills
    if about:
        linkedin['about'] = about
    if headline_opcoes is not None:
        linkedin['headline_opcoes'] = headline_opcoes


def atualizar_gaps(identificados: List[str] = None, resolvidos: List[str] = None,
                   nao_resolvidos: List[str] = None) -> None:
    """
    Atualiza informações sobre gaps identificados e resolvidos.
    
    Args:
        identificados: Lista de gaps identificados no diagnóstico
        resolvidos: Lista de gaps que o candidato tem experiência
        nao_resolvidos: Lista de gaps que o candidato não tem experiência
    """
    if 'cv_estruturado' not in st.session_state:
        st.session_state.cv_estruturado = inicializar_cv_estruturado()
    
    gaps = st.session_state.cv_estruturado['gaps']
    if identificados is not None:
        gaps['identificados'] = identificados
    if resolvidos is not None:
        gaps['resolvidos'] = resolvidos
    if nao_resolvidos is not None:
        gaps['nao_resolvidos'] = nao_resolvidos


def obter_cv_estruturado() -> Optional[Dict[str, Any]]:
    """
    Obtém a estrutura de CV estruturado atual.
    
    Returns:
        Dict com estrutura de CV ou None se não inicializada
    """
    return st.session_state.get('cv_estruturado')


def gerar_contexto_para_prompt() -> str:
    """
    Gera texto formatado com todos os dados coletados para incluir em prompts.
    
    Este texto pode ser injetado em prompts de etapas finais (reescrita, output)
    para garantir que a LLM use dados reais ao invés de inventar.
    
    Returns:
        String formatada com todos os dados coletados
    """
    cv_est = obter_cv_estruturado()
    if not cv_est:
        return "⚠️ Nenhum dado estruturado coletado ainda."
    
    contexto = "### 📊 DADOS COLETADOS (Use APENAS estes dados reais)\n\n"
    
    # Posicionamento
    pos = cv_est.get('posicionamento', {})
    posicionamento_adicionado = False
    if pos.get('cargo_alvo'):
        contexto += f"**CARGO-ALVO:** {pos['cargo_alvo']}\n"
        posicionamento_adicionado = True
    if pos.get('estrategia'):
        contexto += f"**ESTRATÉGIA:** {pos['estrategia']}\n"
        posicionamento_adicionado = True
    if pos.get('senioridade_real'):
        contexto += f"**SENIORIDADE:** {pos['senioridade_real']}\n"
        posicionamento_adicionado = True
    if pos.get('diferencial'):
        contexto += f"**DIFERENCIAL:** {pos['diferencial']}\n"
        posicionamento_adicionado = True
    
    if posicionamento_adicionado:
        contexto += "\n"
    
    # Gaps
    gaps = cv_est.get('gaps', {})
    if gaps.get('resolvidos'):
        contexto += f"**GAPS RESOLVIDOS ({len(gaps['resolvidos'])}):**\n"
        for gap in gaps['resolvidos']:
            contexto += f"- {gap}\n"
        contexto += "\n"
    
    if gaps.get('nao_resolvidos'):
        contexto += f"**GAPS NÃO RESOLVIDOS ({len(gaps['nao_resolvidos'])}):**\n"
        for gap in gaps['nao_resolvidos']:
            contexto += f"- {gap}\n"
        contexto += "\n"
    
    # Métricas coletadas
    metricas = cv_est.get('metricas_coletadas', {})
    if metricas.get('ferramentas'):
        contexto += f"**FERRAMENTAS/TECNOLOGIAS:** {', '.join(metricas['ferramentas'])}\n"
    if metricas.get('volumes'):
        contexto += f"**VOLUMES/MÉTRICAS:** {', '.join(str(v) for v in metricas['volumes'])}\n"
    if metricas.get('resultados'):
        contexto += f"**RESULTADOS QUANTIFICADOS:**\n"
        for resultado in metricas['resultados']:
            contexto += f"- {resultado}\n"
    if metricas.get('equipe'):
        contexto += f"**GESTÃO DE EQUIPE:** {', '.join(metricas['equipe'])}\n"
    
    contexto += "\n"
    
    # Experiências otimizadas
    experiencias = cv_est.get('experiencias', [])
    if experiencias:
        contexto += f"**EXPERIÊNCIAS OTIMIZADAS ({len(experiencias)}):**\n\n"
        for i, exp in enumerate(experiencias, 1):
            contexto += f"{i}. **{exp.get('cargo', 'N/A')}** | {exp.get('empresa', 'N/A')}\n"
            contexto += f"   Período: {exp.get('periodo', 'N/A')}\n"
            if exp.get('conquistas'):
                contexto += "   Conquistas:\n"
                for conquista in exp['conquistas']:
                    contexto += f"   • {conquista}\n"
            contexto += "\n"
    
    # LinkedIn
    linkedin = cv_est.get('linkedin', {})
    if linkedin.get('headline'):
        contexto += f"**LINKEDIN HEADLINE:** {linkedin['headline']}\n"
    if linkedin.get('skills'):
        contexto += f"**LINKEDIN SKILLS:** {', '.join(linkedin['skills'][:10])}\n"
    
    contexto += "\n⚠️ **IMPORTANTE:** Use SOMENTE os dados acima. NUNCA invente informações.\n"
    
    return contexto
