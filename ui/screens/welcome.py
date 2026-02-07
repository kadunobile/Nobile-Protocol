"""
Tela de boas-vindas do Protocolo Nóbile.

Apresenta a plataforma, funcionalidades principais e glossário de termos.
"""

import streamlit as st


def render_welcome():
    """
    Renderiza a tela de boas-vindas com visão geral da plataforma.
    """
    st.markdown("""
    # 🎯 Bem-vindo ao Protocolo Nóbile
    
    ### Inteligência Artificial para Otimização de Currículos
    
    **Para profissionais de todos os níveis: júnior, pleno, sênior, especialista, gerente, diretor...**
    
    ---
    
    ## ✨ O que você pode fazer aqui:
    
    ### 🔍 **Análise de CV**
    - **Score ATS** - Descubra se seu CV passa pelos sistemas automáticos das empresas
    - **Reality Check** - Análise honesta com identificação de gaps
    - **Chat com IA** - Otimize interativamente seu currículo
    
    ### 📝 **Documentos Profissionais**
    - **Carta de Apresentação** - Gerada automaticamente para cada vaga
    - **4 Tons Disponíveis** - Formal, Entusiasmado, Técnico, Criativo
    
    ### 🎤 **Preparação para Entrevistas**
    - **Perguntas Personalizadas** - Baseadas no seu perfil
    - **Método STAR** - Estruture respostas vencedoras
    - **Prática Guiada** - Rascunhe respostas antes da entrevista real
    
    ### 🔄 **Validação de Melhorias**
    - **Comparador de CVs** - Veja o impacto das otimizações
    - **Scores Lado a Lado** - Antes vs. Depois
    - **Análise Detalhada** - 5 categorias avaliadas
    
    ---
    
    ## 📚 Glossário Rápido
    
    | Termo | O que significa |
    |-------|-----------------|
    | **ATS** | Sistema automático que filtra CVs (Applicant Tracking System) |
    | **Score ATS** | Nota 0-100 da chance do seu CV ser aprovado |
    | **Keywords** | Palavras-chave técnicas que o ATS procura |
    | **STAR** | Método para responder perguntas (Situação-Tarefa-Ação-Resultado) |
    | **Reality Check** | Análise crítica do seu CV identificando pontos fortes e fracos |
    
    ---
    
    ## 🚀 Como Começar
    
    1. **📤 Faça upload do seu CV** (texto)
    2. **🎯 Complete o Briefing** (cargo-alvo, objetivos)
    3. **📊 Veja seu Score ATS** atual
    4. **💬 Chat com a IA** para otimizar
    5. **✨ Use as ferramentas extras** (carta, prep. entrevista, comparador)
    
    ---
    
    <div style="background: #f0f8ff; padding: 20px; border-radius: 10px; border-left: 4px solid #1e90ff;">
    <strong>💡 Dica:</strong> Mesmo se você não for executivo, o Protocolo Nóbile funciona para <strong>qualquer cargo</strong>: 
    desenvolvedor, designer, analista, assistente, coordenador, gerente, etc.
    </div>
    
    ---
    
    ### 👈 Use a barra lateral para navegar!
    """, unsafe_allow_html=True)
    
    # Estatísticas (opcional)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Score Médio", "75/100", "+12 após otimização")
    
    with col2:
        st.metric("Ferramentas", "8", "Análise completa")
    
    with col3:
        st.metric("Usuários", "100+", "Profissionais atendidos")
    
    with col4:
        st.metric("Taxa de Sucesso", "89%", "Aprovação em ATS")
