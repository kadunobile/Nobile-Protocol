import os
import streamlit as st
from core.utils import inicializar_cliente_openai

def fase_0_intro():
    st.markdown("# 🎯 Protocolo Nóbile")
    st.markdown("## Sistema de Inteligência de Carreira Executiva")
    st.markdown("---")

    st.markdown("""
### Bem-vindo. Eu sou a Inteligência Artificial do **Protocolo Nóbile**.

Minha função é realizar uma **auditoria completa da sua carreira** e reposicionar seu perfil para o mercado Executivo de Alta Performance, eliminando ruídos e focando em **ROI**.

### O que eu faço por você:

✅ **Otimização de CV e LinkedIn para ATS**  
✅ **SEO de Perfis Profissionais**  
✅ **Análise Estratégica de Carreira**  
✅ **Preparação Tática para Entrevistas**  

### Como Funciona:

**1️⃣ Deep Scan:** Análise completa do CV  
**2️⃣ Briefing:** Seus objetivos (cargo, salário, local)  
**3️⃣ Reality Check:** Cruzamento com mercado  
**4️⃣ Otimização:** Reescrita com dados quantitativos  
**5️⃣ Estratégia:** Empresas, vagas e entrevistas  

---

### 🚀 Requisitos:

- ✅ CV em formato PDF
- ✅ 20-30 minutos disponíveis
- ✅ Dados sobre suas experiências
    """)

    st.markdown("---")

    api_key = os.getenv("OPENAI_API_KEY")

    if api_key:
        if not st.session_state.openai_client:
            st.session_state.openai_client = inicializar_cliente_openai(api_key)
        st.success("✅ Sistema configurado e pronto!")
    else:
        st.warning("⚠️ Configure sua API Key no arquivo config.py")
        key_input = st.text_input("Ou insira manualmente:", type="password")
        if key_input:
            st.session_state.openai_client = inicializar_cliente_openai(key_input)
            st.success("✅ API Key configurada!")

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 INICIAR DIAGNÓSTICO", use_container_width=True, type="primary"):
            if st.session_state.openai_client:
                st.session_state.fase = 'FASE_0_UPLOAD'
                st.rerun()
            else:
                st.error("⚠️ Configure a API Key primeiro!")
