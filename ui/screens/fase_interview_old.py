import streamlit as st
from core.interview_prep import gerar_perguntas_entrevista
from core.utils import chamar_gpt
from core.prompts import SYSTEM_PROMPT

def fase_interview_prep():
    st.markdown("# 🎤 Preparação para Entrevistas")
    st.markdown("---")
    
    if not st.session_state.cv_texto:
        st.error("⚠️ CV não encontrado.")
        return
    
    perfil = st.session_state.perfil or {}
    cargo = perfil.get('cargo_alvo', 'Cargo Geral')
    
    st.info(f"🎯 Preparação focada para: **{cargo}**")
    
    # Tabs para organizar
    tab1, tab2, tab3 = st.tabs(["📋 Perguntas Comuns", "💡 Respostas Personalizadas", "🎯 Dicas Estratégicas"])
    
    with tab1:
        st.markdown("### 📋 Perguntas Típicas por Categoria")
        
        # Detecta área
        cargo_lower = cargo.lower()
        if any(x in cargo_lower for x in ['dev', 'engineer', 'tech', 'software']):
            area = 'tech'
        elif any(x in cargo_lower for x in ['vend', 'comercial', 'sales']):
            area = 'vendas'
        elif any(x in cargo_lower for x in ['market', 'brand', 'digital']):
            area = 'marketing'
        elif any(x in cargo_lower for x in ['gerente', 'manager', 'director']):
            area = 'gerencial'
        else:
            area = 'geral'
        
        perguntas = gerar_perguntas_entrevista(cargo, 'senior', area)
        
        for categoria, lista in perguntas.items():
            with st.expander(f"**{categoria}** ({len(lista)} perguntas)"):
                for i, pergunta in enumerate(lista, 1):
                    st.markdown(f"{i}. {pergunta}")
    
    with tab2:
        st.markdown("### 💡 Gerador de Respostas Personalizadas")
        st.caption("Baseadas no seu CV")
        
        pergunta_selecionada = st.selectbox(
            "Escolha uma pergunta para praticar:",
            [
                "Fale sobre você e sua trajetória",
                "Quais são seus pontos fortes?",
                "Por que você quer este cargo?",
                "Conte sobre um desafio que superou",
                "Onde você se vê em 5 anos?",
                "Qual foi seu maior erro profissional?",
                "Como você lida com pressão?",
                "Customizada..."
            ]
        )
        
        if pergunta_selecionada == "Customizada...":
            pergunta_custom = st.text_input("Digite sua pergunta:")
            pergunta_final = pergunta_custom
        else:
            pergunta_final = pergunta_selecionada
        
        if st.button("💡 Gerar Resposta Modelo", type="primary", use_container_width=True):
            if not pergunta_final:
                st.error("Digite uma pergunta primeiro")
            else:
                with st.spinner("🤔 Analisando seu CV e gerando resposta..."):
                    prompt = f"""Com base no CV abaixo, gere uma resposta STELLAR para a pergunta de entrevista.

**PERGUNTA:** {pergunta_final}

**CV DO CANDIDATO:**
{st.session_state.cv_texto[:3000]}

**INSTRUÇÕES:**

1. Use o método STAR (Situação, Tarefa, Ação, Resultado)
2. Seja ESPECÍFICO - mencione números, nomes de projetos, resultados reais do CV
3. Mantenha resposta entre 60-90 segundos de fala (~150-200 palavras)
4. Tom profissional mas natural
5. Termine com aprendizado ou resultado positivo

**FORMATO DA RESPOSTA:**

**Resposta Sugerida:**
[Texto da resposta usando STAR]

**⏱️ Tempo estimado:** X segundos

**💡 Dicas extras:**
- [Dica 1]
- [Dica 2]

**❌ Evite dizer:**
- [Armadilha 1]
- [Armadilha 2]
"""
                    
                    messages = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": prompt}
                    ]
                    
                    resposta = chamar_gpt(st.session_state.openai_client, messages)
                    
                    if resposta:
                        st.markdown(resposta)
                        
                        # Gravador de áudio (futuro)
                        st.markdown("---")
                        st.info("💡 **Dica:** Grave você falando esta resposta e ouça para praticar!")
    
    with tab3:
        st.markdown("### 🎯 Dicas Estratégicas")
        
        st.markdown("""
        #### ✅ Antes da Entrevista
        
        - [ ] Pesquise a empresa (site, LinkedIn, notícias recentes)
        - [ ] Prepare 3-5 perguntas inteligentes para fazer
        - [ ] Revise a descrição da vaga e seus requisitos
        - [ ] Tenha exemplos STAR prontos para competências-chave
        - [ ] Teste câmera/áudio se for remoto
        
        #### 💬 Durante a Entrevista
        
        - **Ouça atentamente** antes de responder
        - **Use o método STAR** para respostas comportamentais
        - **Seja específico** - números > adjetivos
        - **Faça perguntas** - mostra interesse genuíno
        - **Linguagem corporal** - mantenha contato visual
        
        #### 🚫 Evite
        
        - ❌ Falar mal de empregadores anteriores
        - ❌ Responder com "não sei" sem tentar
        - ❌ Mentir sobre experiências
        - ❌ Divagar sem estrutura
        - ❌ Não fazer perguntas no final
        
        #### 📞 Após a Entrevista
        
        - Envie email de agradecimento em 24h
        - Reforce 1-2 pontos que discutiu
        - Reitere interesse na posição
        """)
    
    st.markdown("---")
    
    if st.button("⬅️ Voltar", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
