import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt
from datetime import datetime

def fase_carta_apresentacao():
    st.markdown("# 📝 Gerador de Carta de Apresentação")
    st.markdown("---")
    
    st.info("💡 Gere uma carta personalizada baseada no seu CV e na vaga desejada")
    
    if not st.session_state.cv_texto:
        st.error("⚠️ CV não encontrado. Faça upload primeiro.")
        return
    
    with st.form("form_carta"):
        st.markdown("### 📋 Informações da Vaga")
        
        col1, col2 = st.columns(2)
        
        with col1:
            empresa = st.text_input(
                "**Nome da Empresa:**",
                placeholder="Ex: Google Brasil"
            )
            
            cargo_vaga = st.text_input(
                "**Cargo da Vaga:**",
                placeholder="Ex: Gerente de Vendas"
            )
        
        with col2:
            recrutador = st.text_input(
                "**Nome do Recrutador (opcional):**",
                placeholder="Ex: Maria Silva"
            )
            
            tom = st.selectbox(
                "**Tom da Carta:**",
                ["Formal e Profissional", "Entusiasmado", "Técnico e Direto", "Criativo"]
            )
        
        descricao_vaga = st.text_area(
            "**Descrição da Vaga (copie e cole):**",
            placeholder="Cole aqui a descrição completa da vaga...",
            height=200
        )
        
        pontos_destaque = st.text_area(
            "**O que você quer destacar? (opcional):**",
            placeholder="Ex: 'Quero enfatizar minha experiência com CRM Salesforce e gestão de equipes remotas'",
            height=80
        )
        
        submitted = st.form_submit_button("✨ Gerar Carta", use_container_width=True, type="primary")
    
    if submitted:
        if not empresa or not cargo_vaga or not descricao_vaga:
            st.error("⚠️ Preencha pelo menos: Empresa, Cargo e Descrição da Vaga")
            return
        
        with st.spinner("✍️ Escrevendo sua carta personalizada..."):
            # Prompt para gerar carta
            prompt_carta = f"""
Você é um especialista em redação de cartas de apresentação para processos seletivos executivos.

**CONTEXTO:**
- Candidato com o CV abaixo
- Vaga: {cargo_vaga} na empresa {empresa}
- Tom desejado: {tom}

**CV DO CANDIDATO (resumido):**
{st.session_state.cv_texto[:2000]}

**DESCRIÇÃO DA VAGA:**
{descricao_vaga}

**PONTOS A DESTACAR:**
{pontos_destaque if pontos_destaque else "Nenhum ponto específico"}

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
{datetime.now().strftime("%d de %B de %Y")}

Prezado(a) {"Sr(a). " + recrutador if recrutador else "equipe de recrutamento"},

[Parágrafo 1]

[Parágrafo 2]

[Parágrafo 3]

[Parágrafo 4]

Atenciosamente,
[Seu Nome]
"""
            
            msgs = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt_carta}
            ]
            
            carta = chamar_gpt(st.session_state.openai_client, msgs)
            
            if carta:
                st.success("✅ Carta gerada com sucesso!")
                st.markdown("---")
                
                # Exibe a carta em um container
                st.markdown("### 📄 Sua Carta de Apresentação")
                
                # Caixa editável
                carta_editada = st.text_area(
                    "Você pode editar antes de copiar:",
                    value=carta,
                    height=500,
                    key="carta_final"
                )
                
                # Botões de ação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.download_button(
                        "📥 Baixar TXT",
                        data=carta_editada,
                        file_name=f"carta_{empresa.replace(' ', '_').lower()}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    # Botão para copiar (usa clipboard via JavaScript)
                    if st.button("📋 Copiar", use_container_width=True):
                        st.code(carta_editada, language=None)
                        st.info("👆 Selecione o texto acima e copie (Ctrl+C)")
                
                with col3:
                    if st.button("🔄 Gerar Outra", use_container_width=True):
                        st.rerun()
    
    st.markdown("---")
    if st.button("⬅️ Voltar ao Chat", use_container_width=True):
        st.session_state.fase = 'CHAT'
        st.rerun()
