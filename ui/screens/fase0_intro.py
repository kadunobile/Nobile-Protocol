import os
import streamlit as st
from core.utils import inicializar_cliente_openai

def fase_0_intro():
    st.markdown("# 🎯 Protocolo Nóbile")
    st.markdown("### Engenharia de Carreira & Inteligência de Mercado via IA")
    st.markdown("---")

    st.markdown("""
**Bem-vindo à sua nova vantagem competitiva.**

O Protocolo Nóbile não é apenas um "corretor de currículos". É uma plataforma de **Engenharia de Carreira** que utiliza Inteligência Artificial avançada para transformar seu histórico profissional em uma ferramenta de venda de alto valor.

Aqui, não reescrevemos somente, iremos analisar e te entregar o melhor pacote de melhorias possíveis, somados a suas experiências.

---

### 🚀 O Que Você Vai Conquistar Aqui:

* **🛡️ Blindagem contra Robôs (ATS Score):**
    * *O que é:* 75% dos currículos são descartados por "robôs recrutadores" antes de um humano ler.
    * *O que fazemos:* Otimizamos suas palavras-chave para garantir que você passe pelo filtro digital.

* **⚖️ Reality Check (Raio-X de Mercado):**
    * *O que é:* Uma análise fria e direta. Seu perfil realmente bate com a vaga?
    * *O que fazemos:* Identificamos seus "Gaps" (o que falta) e seus pontos fortes para a negociação salarial.

* **✍️ Reescrita Estratégica (Storytelling):**
    * Transformamos listas de tarefas ("Fazia relatórios") em conquistas de impacto ("Aumentei a eficiência em 20%").

* **🗣️ Treinador de Entrevista:**
    * Simulações reais baseadas na cultura da empresa alvo, com feedbacks táticos sobre sua performance.

---

### ⚙️ Como Funciona o Protocolo:

1. **📥 O Upload (Input):** Você cola seu CV atual (texto) e a descrição da vaga que deseja.
2. **🧠 O Diagnóstico:** Nossa IA assume o papel de um Headhunter Sênior e analisa sua compatibilidade.
3. **🛠️ A Engenharia:** Através de um chat interativo, refinamos cada linha do seu perfil até atingir a Alta Performance.
4. **💎 A Entrega:** Você sai com um CV pronto, carta de apresentação e roteiro de entrevista.

---

### 🎯 Para Quem é o Protocolo Nóbile?

Do **Estagiário ao C-Level**. A lógica de mercado é a mesma: **Quem comunica melhor seu valor, ganha mais.**

* Serve para: Transição de Carreira, Busca de Promoção, Recolocação e Aumento Salarial.

---

### ⚠️ Requisitos para o Sucesso:

* Tenha seu CV em texto (PDFs podem ser copiados).
* Reserve 20 minutos de foco total (Carreira se constrói com atenção).
* Esteja aberto a feedbacks duros e realistas.

**👉 Comece agora clicando no botão abaixo.**
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
