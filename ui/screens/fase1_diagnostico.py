import streamlit as st
from core.utils import scroll_topo

def fase_1_diagnostico():
    scroll_topo()
    st.markdown("# 🔍 Diagnóstico Completo")
    st.markdown("---")
    st.markdown(st.session_state.analise_inicial)
    st.markdown("---")
    st.markdown("**Recebido. Li seu perfil completo. Vamos elevar o nível dessa narrativa.**")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✅ PROSSEGUIR PARA BRIEFING", use_container_width=True, type="primary"):
            st.session_state.fase = 'FASE_1_BRIEFING'
            st.rerun()
