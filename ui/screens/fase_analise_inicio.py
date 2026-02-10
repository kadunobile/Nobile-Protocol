"""
DEPRECATED: Fase removida do fluxo principal (2026-02-10).
Agora Reality Check vai direto para CHAT.
Este arquivo existe apenas para fallback/redirect.
"""

import streamlit as st
import logging

logger = logging.getLogger(__name__)


def fase_analise_inicio():
    """
    DEPRECATED: Esta fase foi removida do fluxo.
    Redireciona automaticamente para CHAT com otimizador ativo.
    """
    logger.warning("fase_analise_inicio deprecated - redirecting to CHAT")
    
    # Garantir que otimizador está configurado
    if not st.session_state.get('modulo_ativo'):
        st.session_state.modulo_ativo = 'OTIMIZADOR'
        st.session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO'
    
    st.session_state.fase = 'CHAT'
    st.rerun()
