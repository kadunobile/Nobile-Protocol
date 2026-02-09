import streamlit as st

def fase_0_intro():
    st.markdown("# 🎯 Protocolo Nóbile")
    st.markdown("### Engenharia de Carreira & Inteligência de Mercado via IA")
    st.markdown("---")
    
    # Hero section — 3 cards compactos
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🛡️ Blindagem ATS")
        st.caption("Otimize palavras-chave para passar pelos filtros automáticos de recrutamento.")
    
    with col2:
        st.markdown("#### ⚖️ Reality Check")
        st.caption("Análise fria: gaps, pontos fortes e fit real com o mercado.")
    
    with col3:
        st.markdown("#### ✍️ Reescrita Estratégica")
        st.caption("Transforme tarefas em conquistas de impacto com storytelling.")
    
    st.markdown("---")
    
    # Como funciona — versão ultra-compacta
    st.markdown("### ⚙️ Como Funciona")
    st.markdown("""
1. **📥 Upload** — Envie seu CV (PDF do LinkedIn recomendado)
2. **🧠 Diagnóstico** — IA analisa compatibilidade com o cargo
3. **🛠️ Otimização** — Refinamos cada seção do seu perfil
4. **💎 Entrega** — CV otimizado + LinkedIn + Carta de Apresentação
    """)
    
    st.info("⏱️ **Tempo estimado:** 20 minutos | Do Estagiário ao C-Level")
    
    st.markdown("---")
    
    # Botão CTA — sem API key (já autenticado pelo login)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 INICIAR DIAGNÓSTICO", use_container_width=True, type="primary"):
            if st.session_state.openai_client:
                st.session_state.fase = 'FASE_0_UPLOAD'
                st.rerun()
            else:
                st.error("⚠️ Erro de configuração. Contate o administrador.")

