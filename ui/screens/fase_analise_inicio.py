"""
Fase Análise Início - Tela de transição antes de entrar no chat de otimização.

Mostra "Aqui começa a análise", um plano de ação, e um botão para iniciar a otimização.
"""

import streamlit as st
from core.utils import forcar_topo


def fase_analise_inicio():
    """
    Tela de transição que mostra "Aqui começa a análise", um plano de ação,
    e um botão para iniciar a otimização.
    
    Esta tela aparece após o usuário clicar em "INICIAR OTIMIZAÇÃO COMPLETA" no bridge,
    e antes de entrar no chat de otimização.
    """
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    forcar_topo()

    st.markdown("# 🎯 Aqui começa a análise")
    st.markdown("---")

    st.info("""
    ### 📋 Plano de Ação

    1. 🔍 Explore ferramentas de sales engagement como Outreach para otimizar ainda mais a eficiência do time de vendas.

    2. ⚠️ Considere a integração de ferramentas de análise de conversas como Gong.io para insights mais profundos sobre interações de vendas.
    """)

    st.markdown("")
    st.markdown("")

    # Botão centralizado para iniciar otimização
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 Iniciar otimização", use_container_width=True, type="primary"):
            st.session_state.fase = 'CHAT'
            st.session_state.force_scroll_top = True
            st.rerun()
