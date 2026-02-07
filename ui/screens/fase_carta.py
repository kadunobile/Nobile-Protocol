import streamlit as st
from core.carta_generator import gerar_carta_apresentacao
from core.utils import chamar_gpt
from core.prompts import SYSTEM_PROMPT

def fase_carta_apresentacao():
    st.markdown("# ✉️ Gerador de Carta de Apresentação")
    st.markdown("---")
    
    st.info("📝 Crie uma carta personalizada para a vaga desejada")
    
    if not st.session_state.cv_texto:
        st.error("⚠️ CV não encontrado. Faça upload primeiro.")
        return
    
    with st.form("form_carta"):
        st.markdown("### Dados da Vaga")
        
        col1, col2 = st.columns(2)
        
        with col1:
            empresa = st.text_input("Empresa *", placeholder="Ex: Google Brasil")
            cargo_vaga = st.text_input("Cargo *", placeholder="Ex: Product Manager")
        
        with col2:
            estilo = st.selectbox(
                "Estilo da Carta",
                ["formal", "descontraido", "tech"],
                format_func=lambda x: {
                    "formal": "🎩 Formal (Corporativo)",
                    "descontraido": "😊 Descontraído",
                    "tech": "💻 Tech (Inglês)"
                }[x]
            )
        
        descricao_vaga = st.text_area(
            "Descrição da Vaga (opcional)",
            height=150,
            placeholder="Cole aqui a descrição completa da vaga..."
        )
        
        requisitos = st.text_area(
            "Requisitos Principais (um por linha)",
            height=100,
            placeholder="Ex:\nExperiência com Scrum\nLiderança de equipes\nSQL avançado"
        )
        
        submitted = st.form_submit_button("✉️ Gerar Carta", use_container_width=True, type="primary")
    
    if submitted:
        if not empresa or not cargo_vaga:
            st.error("⚠️ Preencha empresa e cargo")
            return
        
        with st.spinner("✍️ Escrevendo carta personalizada..."):
            # Extrai dados do CV
            perfil = st.session_state.perfil or {}
            
            # Processa requisitos
            req_list = [r.strip() for r in requisitos.split('\n') if r.strip()]
            
            # Usa GPT para gerar carta inteligente
            prompt = f"""Com base no CV abaixo, gere uma carta de apresentação para:

**Empresa:** {empresa}
**Cargo:** {cargo_vaga}
**Estilo:** {estilo}

**Requisitos da vaga:**
{chr(10).join(f'- {r}' for r in req_list) if req_list else 'Não informados'}

**Descrição da vaga:**
{descricao_vaga if descricao_vaga else 'Não informada'}

**CV DO CANDIDATO:**
{st.session_state.cv_texto[:2000]}

**INSTRUÇÕES:**

1. **Abertura** personalizada mencionando a empresa e cargo
2. **Parágrafo 1:** Conecte experiências do CV com a vaga (seja específico)
3. **Parágrafo 2:** Destaque 2-3 realizações QUANTIFICÁVEIS do CV que sejam relevantes
4. **Parágrafo 3:** Mostre match com os requisitos (use evidências do CV)
5. **Fechamento:** Call to action (ex: disponibilidade para entrevista)

**IMPORTANTE:**
- Use TOM {estilo}
- Máximo 300 palavras
- NÃO invente informações que não estão no CV
- Seja ESPECÍFICO (evite genéricos como "sou dedicado")
- Use NÚMEROS do CV quando possível

**FORMATO:**
- Se formal: "Prezado(a) Recrutador(a)"
- Se descontraído: "Olá!"
- Se tech: "Hi there!" (em inglês)
"""
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ]
            
            carta = chamar_gpt(st.session_state.openai_client, messages)
            
            if carta:
                st.success("✅ Carta gerada com sucesso!")
                
                st.markdown("### 📄 Sua Carta de Apresentação")
                st.markdown("---")
                st.markdown(carta)
                st.markdown("---")
                
                # Botões de ação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "📥 Baixar TXT",
                        carta,
                        file_name=f"carta_{empresa.lower().replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    if st.button("✏️ Editar Carta", use_container_width=True):
                        st.session_state.carta_editavel = carta
                
                with col3:
                    if st.button("🔄 Nova Carta", use_container_width=True):
                        st.rerun()
                
                # Área de edição
                if 'carta_editavel' in st.session_state:
                    st.markdown("### ✏️ Edite a Carta")
                    carta_final = st.text_area(
                        "Edite livremente",
                        value=st.session_state.carta_editavel,
                        height=400
                    )
                    
                    st.download_button(
                        "📥 Baixar Versão Editada",
                        carta_final,
                        file_name=f"carta_{empresa.lower().replace(' ', '_')}_final.txt",
                        mime="text/plain"
                    )

    st.markdown("---")
    
    if st.button("⬅️ Voltar ao Chat", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
