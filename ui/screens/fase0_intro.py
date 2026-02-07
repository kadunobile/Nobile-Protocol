import os
import streamlit as st
from core.utils import inicializar_cliente_openai

def fase_0_intro():
    st.markdown("# 🎯 Protocolo Nóbile")
    st.markdown("## Inteligência Artificial para Otimização de Currículos")
    st.markdown("---")

    st.markdown("""
### Bem-vindo ao **Protocolo Nóbile**.

Uma plataforma completa que utiliza IA para ajudar profissionais de **todos os níveis e áreas** a aprimorarem seus currículos e se prepararem para processos seletivos.

### O que você pode fazer aqui:

✅ **Análise de CV e Score ATS**  
✅ **Reality Check com Identificação de Gaps**  
✅ **Otimização Interativa com IA**  
✅ **Geração de Carta de Apresentação**  
✅ **Preparação para Entrevistas**  
✅ **Comparador de CVs (Antes/Depois)**

### Como Funciona:

**1️⃣ Upload:** Cole seu CV em texto  
**2️⃣ Briefing:** Defina cargo-alvo e objetivos  
**3️⃣ Análise:** Receba Score ATS e Reality Check  
**4️⃣ Otimização:** Chat com IA para melhorar  
**5️⃣ Ferramentas:** Carta, prep. entrevista, comparador  

---

### 🎯 Para Quem é?

**Todos os níveis:** Júnior, Pleno, Sênior, Gerente, Diretor, C-Level  
**Todas as áreas:** Tech, Vendas, Marketing, RH, Financeiro, Operações, Design, etc.

---

### 🚀 Requisitos:

- ✅ CV em formato texto (copie de PDF/Word)
- ✅ 20-30 minutos disponíveis
- ✅ Informações sobre suas experiências
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
