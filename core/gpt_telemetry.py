"""
Módulo de telemetria de chamadas GPT - rastreamento de uso da API.

Este módulo fornece funções para rastrear e exibir o número de chamadas
GPT realizadas durante uma sessão, permitindo visibilidade sobre o uso
da API e custos associados.

HEADHUNTER ELITE: Telemetria transparente de chamadas GPT.
"""

import logging
import streamlit as st
from typing import Optional
from core.utils import chamar_gpt as chamar_gpt_original

logger = logging.getLogger(__name__)

# Contextos de chamadas GPT (para rastreamento detalhado)
CONTEXTO_DIAGNOSTICO = "diagnostico"
CONTEXTO_COLETA = "coleta_focada"
CONTEXTO_REESCRITA = "reescrita"
CONTEXTO_LINKEDIN = "linkedin"
CONTEXTO_VALIDACAO = "validacao"
CONTEXTO_OUTROS = "outros"


def inicializar_telemetria():
    """
    Inicializa as variáveis de telemetria no session state.
    
    Deve ser chamado no início da sessão (em state.py).
    """
    if 'gpt_calls_count' not in st.session_state:
        st.session_state.gpt_calls_count = 0
    
    if 'gpt_calls_by_context' not in st.session_state:
        st.session_state.gpt_calls_by_context = {
            CONTEXTO_DIAGNOSTICO: 0,
            CONTEXTO_COLETA: 0,
            CONTEXTO_REESCRITA: 0,
            CONTEXTO_LINKEDIN: 0,
            CONTEXTO_VALIDACAO: 0,
            CONTEXTO_OUTROS: 0,
        }


def incrementar_contador_gpt(contexto: str = CONTEXTO_OUTROS):
    """
    Incrementa o contador de chamadas GPT.
    
    Args:
        contexto: Contexto da chamada (diagnostico, coleta_focada, etc.)
    """
    # Incrementar contador geral
    if 'gpt_calls_count' not in st.session_state:
        st.session_state.gpt_calls_count = 0
    st.session_state.gpt_calls_count += 1
    
    # Incrementar contador por contexto
    if 'gpt_calls_by_context' not in st.session_state:
        inicializar_telemetria()
    
    if contexto in st.session_state.gpt_calls_by_context:
        st.session_state.gpt_calls_by_context[contexto] += 1
    else:
        st.session_state.gpt_calls_by_context[CONTEXTO_OUTROS] += 1
    
    logger.debug(f"GPT call #{st.session_state.gpt_calls_count} (contexto: {contexto})")


def chamar_gpt_com_telemetria(
    client,
    msgs: list,
    contexto: str = CONTEXTO_OUTROS,
    **kwargs
) -> Optional[str]:
    """
    Wrapper para chamar_gpt que incrementa o contador de telemetria.
    
    Args:
        client: Cliente OpenAI
        msgs: Lista de mensagens
        contexto: Contexto da chamada para categorização
        **kwargs: Argumentos adicionais passados para chamar_gpt
        
    Returns:
        Resposta do GPT ou None em caso de erro
    """
    # Incrementar contador ANTES da chamada (para contar tentativas mesmo que falhem)
    incrementar_contador_gpt(contexto)
    
    # Fazer a chamada GPT
    try:
        resposta = chamar_gpt_original(client, msgs, **kwargs)
        return resposta
    except Exception as e:
        logger.error(f"Erro na chamada GPT com telemetria (contexto: {contexto}): {e}", exc_info=True)
        raise  # Re-raise para manter comportamento original


def obter_contador_gpt() -> int:
    """
    Obtém o número total de chamadas GPT na sessão.
    
    Returns:
        Número de chamadas GPT realizadas
    """
    return st.session_state.get('gpt_calls_count', 0)


def obter_estatisticas_gpt() -> dict:
    """
    Obtém estatísticas detalhadas de chamadas GPT.
    
    Returns:
        Dicionário com estatísticas de uso da API
    """
    return {
        'total': st.session_state.get('gpt_calls_count', 0),
        'por_contexto': st.session_state.get('gpt_calls_by_context', {})
    }


def resetar_telemetria():
    """
    Reseta os contadores de telemetria.
    
    Útil para reiniciar a contagem em uma nova sessão.
    """
    st.session_state.gpt_calls_count = 0
    inicializar_telemetria()
    logger.info("Telemetria de GPT resetada")


def renderizar_badge_gpt_calls():
    """
    Renderiza o badge de contagem de chamadas GPT no topo da interface.
    
    Deve ser chamado no início da interface de chat.
    """
    total_calls = obter_contador_gpt()
    
    # Definir cor baseada no número de chamadas
    if total_calls == 0:
        color = "#888888"  # Cinza
        emoji = "⚪"
    elif total_calls <= 5:
        color = "#4CAF50"  # Verde
        emoji = "🟢"
    elif total_calls <= 15:
        color = "#FFC107"  # Amarelo
        emoji = "🟡"
    elif total_calls <= 30:
        color = "#FF9800"  # Laranja
        emoji = "🟠"
    else:
        color = "#F44336"  # Vermelho
        emoji = "🔴"
    
    # Renderizar badge com estilo inline
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {color}22 0%, {color}11 100%);
        border: 2px solid {color};
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    ">
        {emoji} <span style="color: {color};">Chamadas GPT nesta sessão:</span> <span style="font-size: 18px; color: {color};">{total_calls}</span>
    </div>
    """, unsafe_allow_html=True)


def renderizar_detalhes_telemetria():
    """
    Renderiza detalhes expandidos da telemetria (para debugging).
    
    Mostra breakdown por contexto das chamadas GPT.
    """
    stats = obter_estatisticas_gpt()
    
    with st.expander("📊 Detalhes de Uso da API", expanded=False):
        st.markdown("**Chamadas GPT por etapa:**")
        
        contexto_labels = {
            CONTEXTO_DIAGNOSTICO: "🔍 Diagnóstico",
            CONTEXTO_COLETA: "📝 Coleta Focada",
            CONTEXTO_REESCRITA: "✍️ Reescrita",
            CONTEXTO_LINKEDIN: "🔵 LinkedIn",
            CONTEXTO_VALIDACAO: "✅ Validação",
            CONTEXTO_OUTROS: "💬 Outros",
        }
        
        for contexto, count in stats['por_contexto'].items():
            label = contexto_labels.get(contexto, contexto)
            st.text(f"{label}: {count}")
        
        st.markdown("---")
        st.markdown(f"**Total Geral:** {stats['total']}")
