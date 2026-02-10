"""
Módulo de geração dinâmica de perguntas com anti-loop.

Este módulo implementa a lógica para gerar perguntas dinâmicas
baseadas no contexto (CV, cargo, gaps, histórico) e prevenir loops
através do rastreamento de Q&A.

HEADHUNTER ELITE: Geração inteligente e contextual de perguntas.
"""

import logging
import streamlit as st
from typing import List, Dict, Optional
from core.cv_cache import get_cv_contexto_para_prompt
from core.gpt_telemetry import chamar_gpt_com_telemetria

logger = logging.getLogger(__name__)

# Constants for response validation
MIN_SUBSTANTIVE_RESPONSE_LENGTH = 15  # Minimum length for a substantive response


def adicionar_qa_historico(etapa: str, pergunta: str, resposta: str):
    """
    Adiciona uma pergunta e resposta ao histórico da etapa.
    
    Args:
        etapa: Nome da etapa (diagnostico, coleta, deep_dive, etc.)
        pergunta: Pergunta feita
        resposta: Resposta do usuário
    """
    key = f'qa_history_{etapa}'
    if key not in st.session_state:
        st.session_state[key] = []
    
    st.session_state[key].append({
        'pergunta': pergunta,
        'resposta': resposta
    })
    
    logger.debug(f"Q&A adicionado ao histórico de {etapa}")


def obter_historico_qa(etapa: str) -> List[Dict]:
    """
    Obtém o histórico de Q&A de uma etapa.
    
    Args:
        etapa: Nome da etapa
        
    Returns:
        Lista de dicionários com perguntas e respostas
    """
    key = f'qa_history_{etapa}'
    return st.session_state.get(key, [])


def formatar_historico_qa(etapa: str) -> str:
    """
    Formata o histórico de Q&A para inclusão em prompts.
    
    Args:
        etapa: Nome da etapa
        
    Returns:
        String formatada com o histórico de Q&A
    """
    historico = obter_historico_qa(etapa)
    
    if not historico:
        return "*(Nenhuma pergunta feita ainda)*"
    
    texto = ""
    for i, qa in enumerate(historico, 1):
        texto += f"\n**P{i}:** {qa['pergunta']}\n"
        texto += f"**R{i}:** {qa['resposta']}\n"
    
    return texto


def gerar_proxima_pergunta_dinamica(
    client,
    etapa: str,
    contexto_especifico: str,
    cargo_alvo: str,
    gaps_mapeados: List[str] = None,
    objetivo: str = "",
    contexto_gpt: str = "diagnostico"
) -> Optional[str]:
    """
    Gera a próxima pergunta de forma dinâmica com base no contexto.
    
    Args:
        client: Cliente OpenAI
        etapa: Nome da etapa (diagnostico, coleta, deep_dive, etc.)
        contexto_especifico: Contexto adicional específico da etapa
        cargo_alvo: Cargo alvo do candidato
        gaps_mapeados: Lista de gaps já mapeados (opcional)
        objetivo: Objetivo desta pergunta (opcional)
        contexto_gpt: Contexto para telemetria GPT
        
    Returns:
        Pergunta gerada ou None em caso de erro
    """
    logger.info(f"Gerando próxima pergunta dinâmica para etapa: {etapa}")
    
    # Obter contexto do CV (resumo ou truncado)
    cv_contexto = get_cv_contexto_para_prompt()
    
    # Obter histórico de Q&A desta etapa
    historico = formatar_historico_qa(etapa)
    
    # Construir contexto de gaps se fornecido
    gaps_texto = ""
    if gaps_mapeados:
        gaps_texto = "\n".join([f"- {gap}" for gap in gaps_mapeados])
        gaps_contexto = f"""
**GAPS IDENTIFICADOS:**
{gaps_texto}
"""
    else:
        gaps_contexto = ""
    
    # Construir prompt para geração dinâmica
    prompt = f"""Você é um **headhunter expert** que faz perguntas CIRÚRGICAS e CONTEXTUAIS para otimizar CVs.

**CARGO-ALVO:** {cargo_alvo}

{cv_contexto}

{gaps_contexto}

**HISTÓRICO DE PERGUNTAS JÁ FEITAS NESTA ETAPA:**
{historico}

---

**CONTEXTO DA ETAPA ATUAL:**
{contexto_especifico}

**OBJETIVO DA PRÓXIMA PERGUNTA:**
{objetivo if objetivo else "Coletar informação relevante para otimização do CV"}

---

**INSTRUÇÕES:**

1. **ANTI-LOOP:** NÃO repita perguntas já feitas (verifique o histórico acima)
2. **CONTEXTO:** Use informações do CV e gaps para fazer perguntas específicas
3. **PRECISÃO:** Seja direto e objetivo, sem rodeios
4. **FOCO:** Priorize informações quantificáveis (métricas, volumes, ferramentas)
5. **PROGRESSÃO:** Baseie-se nas respostas anteriores para aprofundar

**IMPORTANTE:**
- Se já perguntou sobre um gap/tema específico, NÃO pergunte novamente
- Se o usuário já forneceu informação sobre algo, NÃO peça de novo
- Avance para novos tópicos se a informação já foi coletada
- Mantenha tom profissional e direto

---

**GERE A PRÓXIMA PERGUNTA:**"""

    try:
        msgs = [{"role": "user", "content": prompt}]
        pergunta = chamar_gpt_com_telemetria(
            client,
            msgs,
            contexto=contexto_gpt,
            temperature=0.4,  # Alguma criatividade mas controlada
            seed=None  # Sem seed para variar perguntas
        )
        
        if pergunta:
            logger.info(f"Pergunta dinâmica gerada com sucesso para {etapa}")
            return pergunta.strip()
        else:
            logger.warning(f"Falha ao gerar pergunta dinâmica para {etapa}")
            return None
            
    except Exception as e:
        logger.error(f"Erro ao gerar pergunta dinâmica para {etapa}: {e}", exc_info=True)
        return None


def verificar_stop_condition_experiencia(
    historico_qa: List[Dict],
    min_perguntas: int = 4
) -> bool:
    """
    Verifica se as stop conditions de uma experiência foram atingidas.
    
    Uma experiência está completa quando:
    - Pelo menos 4 perguntas foram feitas
    - Métricas/impacto foram coletadas
    - Ferramentas/tecnologias foram mencionadas
    - Volume/escala foi coberto
    
    Args:
        historico_qa: Histórico de Q&A da experiência
        min_perguntas: Número mínimo de perguntas antes de verificar stop
        
    Returns:
        True se stop condition foi atingida, False caso contrário
    """
    if len(historico_qa) < min_perguntas:
        return False
    
    # Concatenar todas as respostas para análise
    respostas_texto = " ".join([qa['resposta'].lower() for qa in historico_qa])
    
    # Keywords indicando métricas/impacto
    metricas_keywords = [
        '%', 'por cento', 'aumento', 'redução', 'crescimento',
        'r$', 'reais', 'milhões', 'mil', 'economia',
        'resultado', 'impacto', 'atingi', 'consegui'
    ]
    
    # Keywords indicando ferramentas/stack
    ferramentas_keywords = [
        'sistema', 'ferramenta', 'tecnologia', 'plataforma',
        'usava', 'utilizava', 'trabalhava com', 'python', 'excel',
        'salesforce', 'sap', 'power bi', 'tableau'
    ]
    
    # Keywords indicando volume/escala
    volume_keywords = [
        'equipe', 'pessoas', 'clientes', 'projetos', 'processos',
        'volume', 'quantidade', 'gerenciava', 'liderava',
        'responsável por', 'coordenava'
    ]
    
    # Verificar cobertura de cada categoria
    tem_metricas = any(kw in respostas_texto for kw in metricas_keywords)
    tem_ferramentas = any(kw in respostas_texto for kw in ferramentas_keywords)
    tem_volume = any(kw in respostas_texto for kw in volume_keywords)
    
    # Stop condition: pelo menos 2 das 3 categorias cobertas
    categorias_cobertas = sum([tem_metricas, tem_ferramentas, tem_volume])
    
    logger.debug(f"Stop condition check: {categorias_cobertas}/3 categorias cobertas")
    
    return categorias_cobertas >= 2


def detectar_resposta_evasiva(resposta: str) -> bool:
    """
    Detecta se a resposta do usuário é evasiva ou indica falta de informação.
    
    Args:
        resposta: Resposta do usuário
        
    Returns:
        True se resposta é evasiva, False caso contrário
    """
    resposta_lower = resposta.lower().strip()
    
    # Respostas muito curtas
    if len(resposta_lower) < MIN_SUBSTANTIVE_RESPONSE_LENGTH:
        return True
    
    # Keywords de evasão
    evasivas_keywords = [
        'não sei', 'não lembro', 'não tenho certeza',
        'não me recordo', 'esqueci', 'não sei dizer',
        'mais ou menos', 'acho que', 'talvez',
        'não tenho essa informação', 'não anotei'
    ]
    
    return any(kw in resposta_lower for kw in evasivas_keywords)


def limpar_historico_qa(etapa: str):
    """
    Limpa o histórico de Q&A de uma etapa.
    
    Args:
        etapa: Nome da etapa
    """
    key = f'qa_history_{etapa}'
    if key in st.session_state:
        st.session_state[key] = []
        logger.info(f"Histórico de Q&A de {etapa} limpo")
