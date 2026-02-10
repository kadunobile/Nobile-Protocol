"""
Fase Análise Início - Tela de transição antes de entrar no chat de otimização.

Mostra uma mensagem simples "Aqui começa a análise" e um botão para abrir o chat.
"""

import streamlit as st
from core.utils import forcar_topo


def fase_analise_inicio():
    """
    Tela de transição que mostra "Aqui começa a análise" e um botão para abrir o chat.
    
    Esta tela aparece após o usuário clicar em "INICIAR OTIMIZAÇÃO COMPLETA" no bridge,
    e antes de entrar no chat de otimização.
    """
    st.markdown('<div id="top-anchor"></div>', unsafe_allow_html=True)
    forcar_topo()

    st.markdown("# 🎯 Aqui começa a análise")
    st.markdown("---")

    st.info("""
    ### 🚀 Vamos começar a otimização do seu CV!

    O processo será interativo e guiado. Você terá controle total sobre cada mudança
    e poderá validar as informações antes de aplicá-las ao seu CV.

    Clique no botão abaixo para abrir o chat e iniciar a conversa com o otimizador.
    """)

    st.markdown("")
    st.markdown("")

    # Botão centralizado para abrir o chat
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("💬 Abrir chat", use_container_width=True, type="primary"):
            st.session_state.fase = 'CHAT'
            st.session_state.force_scroll_top = True
            st.rerun()
