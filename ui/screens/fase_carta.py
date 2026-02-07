import streamlit as st
from datetime import datetime
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
            recrutador = st.text_input("Nome do Recrutador (opcional)", placeholder="Ex: Maria Silva")
        
        with col2:
            tom = st.selectbox(
                "Tom da Carta *",
                ["Formal", "Entusiasmado", "Técnico", "Criativo"],
                format_func=lambda x: {
                    "Formal": "🎩 Formal",
                    "Entusiasmado": "⚡ Entusiasmado",
                    "Técnico": "💻 Técnico",
                    "Criativo": "🎨 Criativo"
                }[x]
            )
        
        descricao_vaga = st.text_area(
            "Descrição da Vaga",
            height=150,
            placeholder="Cole aqui a descrição completa da vaga..."
        )
        
        pontos_destaque = st.text_area(
            "Pontos a Destacar (opcional)",
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
            
            # Usa GPT para gerar carta inteligente com formato específico
            prompt_carta = f"""
Você é um especialista em redação de cartas de apresentação para processos seletivos executivos.

**CONTEXTO:**
- Candidato com o CV abaixo
- Vaga: {cargo_vaga} na empresa {empresa}
- Tom desejado: {tom}

**CV DO CANDIDATO (resumido):**
{st.session_state.cv_texto[:2000]}

**DESCRIÇÃO DA VAGA:**
{descricao_vaga if descricao_vaga else 'Não informada'}

**PONTOS A DESTACAR:**
{pontos_destaque if pontos_destaque else 'Nenhum ponto específico'}

**INSTRUÇÕES:**
1. Crie uma carta de apresentação de 3-4 parágrafos
2. Estrutura:
   - Parágrafo 1: Abertura com interesse na vaga e empresa
   - Parágrafo 2-3: Conexão entre experiências do CV e requisitos da vaga (seja ESPECÍFICO)
   - Parágrafo 4: Encerramento com call-to-action
3. Use dados REAIS do CV (números, empresas, conquistas)
4. NÃO invente informações que não estão no CV
5. {"Dirigir a carta para " + recrutador if recrutador else "Use saudação genérica"}
6. Máximo 400 palavras

**FORMATO:**

[Seu Nome extraído do CV]
[Email e Telefone do CV]

{empresa}
{"À atenção de " + recrutador if recrutador else ""}
{datetime.now().strftime("%d/%m/%Y")}

Prezado(a) {"Sr(a). " + recrutador if recrutador else "equipe de recrutamento"},

[Parágrafo 1]

[Parágrafo 2]

[Parágrafo 3]

[Parágrafo 4]

Atenciosamente,
[Seu Nome]
"""
            
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_carta}
            ]
            
            carta = chamar_gpt(st.session_state.openai_client, messages)
            
            if carta:
                st.success("✅ Carta gerada com sucesso!")
                
                # Text area editável com a carta gerada
                st.markdown("### 📄 Sua Carta de Apresentação")
                carta_editavel = st.text_area(
                    "Edite a carta conforme necessário:",
                    value=carta,
                    height=400
                )
                st.markdown("---")
                
                # Botões de ação
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.download_button(
                        "📥 Baixar TXT",
                        carta_editavel,
                        file_name=f"carta_{empresa.lower().replace(' ', '_')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    # Botão de copiar usando código JavaScript
                    if st.button("📋 Copiar", use_container_width=True):
                        st.code(carta_editavel, language=None)
                        st.info("💡 Selecione o texto acima e pressione Ctrl+C (ou Cmd+C) para copiar")
                
                with col3:
                    if st.button("🔄 Gerar Outra", use_container_width=True):
                        st.rerun()
                
                with col4:
                    if st.button("⬅️ Voltar ao Chat", use_container_width=True, key="voltar_carta_2"):
                        st.session_state.fase = 'CHAT'
                        st.rerun()

    st.markdown("---")
    
    if st.button("⬅️ Voltar ao Chat", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
