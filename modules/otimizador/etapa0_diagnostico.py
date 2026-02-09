"""
Etapa 0: Diagnóstico - Identificar onde cada gap pode ser resolvido no CV.

Esta etapa pergunta ao usuário onde no CV cada gap identificado foi ou pode ser resolvido,
ajudando a identificar as experiências relevantes para otimização.
"""

import streamlit as st


def prompt_etapa0_diagnostico_gap_individual(gap_index):
    """
    Gera prompt para perguntar sobre um gap específico ao usuário.
    
    Args:
        gap_index: Índice do gap atual (0-based)
    
    Returns:
        str: Prompt formatado perguntando sobre o gap específico
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    gaps = st.session_state.get('gaps_alvo', [])
    
    if not gaps or gap_index >= len(gaps):
        return None
    
    gap_atual = gaps[gap_index]
    total_gaps = len(gaps)
    
    return f"""🔍 **ETAPA 0: DIAGNÓSTICO ESTRATÉGICO** ({gap_index + 1}/{total_gaps})

**CARGO-ALVO:** {cargo}

---

### Gap a Analisar:
**"{gap_atual}"**

---

**Pergunta para você:**

Você tem experiência prática com **{gap_atual}**?

- ✅ Se **SIM**: Por favor, responda em qual empresa/cargo você trabalhou com isso e descreva brevemente o contexto (1-2 frases).
  
  *Exemplo: "Sim, na ARQUIVEI como RevOps Manager eu usava Tableau para criar dashboards de receita recorrente."*

- ❌ Se **NÃO**: Digite "não tenho" ou "não" para pularmos este gap.

💡 **Dica:** Seja específico! Quanto mais detalhes você fornecer agora, melhor será a otimização do seu CV.
"""


def prompt_etapa0_diagnostico():
    """
    Gera prompt inicial da etapa de diagnóstico.
    
    Inicia o processo de perguntar sobre cada gap individualmente.
    
    Returns:
        str: Prompt formatado para o GPT
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_texto = st.session_state.get('cv_texto', '')
    gaps = st.session_state.get('gaps_alvo', [])
    
    if not cv_texto:
        return """⚠️ **ERRO:** CV não encontrado na sessão.
        
Por favor, retorne ao início e faça upload do seu CV novamente.

**Clique em "🔄 Recomeçar" na barra lateral.**"""
    
    if not gaps:
        gaps = ["Melhorar estrutura geral do CV"]
        st.session_state.gaps_alvo = gaps
    
    # Inicializar estado para rastrear gaps
    if 'gaps_respostas' not in st.session_state:
        st.session_state.gaps_respostas = {}
    
    # Preparar lista de gaps formatada
    gaps_texto = "\n".join([f"{i+1}. {gap}" for i, gap in enumerate(gaps)])
    
    return f"""🔍 **ETAPA 0: DIAGNÓSTICO ESTRATÉGICO**

**CARGO-ALVO:** {cargo}

---

### 📊 Gaps Identificados no Reality Check

Identificamos **{len(gaps)}** gap(s) que podem ser otimizados no seu CV:

{gaps_texto}

---

### 🎯 Como Funciona

Vamos perguntar sobre **cada gap individualmente** para entender:
- ✅ Onde você já tem experiência com essa skill/conhecimento
- ✅ Em qual empresa/cargo você trabalhou com isso
- ✅ Como podemos destacar isso no seu CV otimizado

Se você não tiver experiência com algum gap, sem problemas! Vamos focar nos pontos fortes que você já tem.

---

⏭️ **Vamos começar com o primeiro gap...**
"""
