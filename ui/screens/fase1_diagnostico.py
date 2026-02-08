import streamlit as st
from core.utils import scroll_topo
from core.ats_scorer import calcular_score_ats, extrair_cargo_do_cv

# Constante para fallback de cargo
CARGO_FALLBACK = "Profissional"


def limpar_cache_ats():
    """Limpa o cache de score ATS do session_state."""
    if 'score_ats_inicial' in st.session_state:
        del st.session_state.score_ats_inicial
    if 'cargo_atual' in st.session_state:
        del st.session_state.cargo_atual


def fase_1_diagnostico():
    scroll_topo()
    
    st.markdown("# 🔍 Diagnóstico do Perfil")
    st.markdown("---")
    
    # ─── Score ATS baseado no cargo atual ───
    # Calcular apenas uma vez e salvar no session_state
    if 'score_ats_inicial' not in st.session_state or 'cargo_atual' not in st.session_state:
        with st.spinner("📊 Calculando seu Score ATS..."):
            # Extrair cargo atual do CV
            cargo_atual = extrair_cargo_do_cv(
                st.session_state.openai_client,
                st.session_state.cv_texto
            )
            
            if not cargo_atual:
                cargo_atual = CARGO_FALLBACK
            
            st.session_state.cargo_atual = cargo_atual
            
            # Calcular score ATS com JD gerada por IA
            resultado_ats = calcular_score_ats(
                st.session_state.cv_texto,
                cargo_atual,
                client=st.session_state.openai_client
            )
            
            st.session_state.score_ats_inicial = resultado_ats
    
    resultado_ats = st.session_state.score_ats_inicial
    cargo_atual = st.session_state.cargo_atual
    score = resultado_ats['score_total']
    nivel = resultado_ats['nivel']
    
    # ─── Card de Score ATS ───
    # Cor baseada no nível
    if score >= 70:
        cor = "#2ecc71"
        emoji = "🟢"
    elif score >= 50:
        cor = "#f39c12"
        emoji = "🟡"
    elif score >= 30:
        cor = "#e67e22"
        emoji = "🟠"
    else:
        cor = "#e74c3c"
        emoji = "🔴"
    
    st.markdown(f"""
    <div style="background: rgba(255,255,255,0.05); border: 2px solid {cor}; 
                border-radius: 12px; padding: 1.5rem; margin: 1rem 0; text-align: center;">
        <p style="margin: 0; font-size: 0.9rem; color: #aaa;">Score ATS para <strong>{cargo_atual}</strong></p>
        <p style="margin: 0.5rem 0; font-size: 3rem; font-weight: 700; color: {cor};">{score:.0f}<span style="font-size: 1.5rem; color: #888;">/100</span></p>
        <p style="margin: 0; font-size: 1.1rem; color: {cor};">{emoji} {nivel}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    # ─── Explicação rápida do score ───
    st.info(
        "📊 **O que é o Score ATS?** É a compatibilidade do seu perfil com o que "
        "sistemas automatizados de recrutamento buscam para seu cargo atual. "
        "Quanto maior, mais chances de seu CV passar pelos filtros automáticos."
    )
    
    st.markdown("---")
    
    # ─── Diagnóstico da IA ───
    st.markdown("### 📋 Diagnóstico Completo")
    st.markdown(st.session_state.analise_inicial)
    
    st.markdown("---")
    
    # ─── Botões de ação ───
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("⬅️ Voltar", use_container_width=True):
            # Limpar score para recalcular se voltar
            limpar_cache_ats()
            st.session_state.fase = 'FASE_0_UPLOAD'
            st.rerun()
    
    with col2:
        if st.button("🚀 PROSSEGUIR PARA BRIEFING", use_container_width=True, type="primary"):
            st.session_state.fase = 'FASE_1_BRIEFING'
            st.rerun()
