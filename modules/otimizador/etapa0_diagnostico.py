"""
Etapa 0: Diagnóstico - Identificar onde cada gap pode ser resolvido no CV.

Esta etapa pergunta ao usuário onde no CV cada gap identificado foi ou pode ser resolvido,
ajudando a identificar as experiências relevantes para otimização.
"""

import streamlit as st


def prompt_etapa0_diagnostico():
    """
    Gera prompt para a etapa de diagnóstico.
    
    Identifica onde cada gap do Reality Check pode ser preenchido
    nas experiências profissionais do candidato.
    
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
    
    # Preparar lista de gaps formatada
    gaps_texto = "\n".join([f"- {gap}" for gap in gaps]) if gaps else "- Melhorar estrutura geral do CV"
    
    return f"""🔍 **ETAPA 0: DIAGNÓSTICO ESTRATÉGICO**

**CARGO-ALVO:** {cargo}

**GAPS IDENTIFICADOS NO REALITY CHECK:**
{gaps_texto}

---

**CV DO CANDIDATO:**
{cv_texto}

---

**INSTRUÇÃO PARA O ASSISTENTE:**

Analise o CV acima e identifique em QUAIS experiências profissionais cada gap pode ser resolvido ou reforçado.

Para CADA gap listado:

1. Identifique a(s) experiência(s) profissional(is) mais relevante(s) onde esse gap pode ser abordado
2. Explique BREVEMENTE como essa experiência pode demonstrar resolução do gap
3. Se o gap não puder ser resolvido com as experiências atuais, sugira como abordar isso

**FORMATO DA RESPOSTA:**

### 🎯 DIAGNÓSTICO DE GAPS

**Gap 1:** [Nome do gap]

📍 **Experiência relacionada:** [Empresa - Cargo - Período]

💡 **Como abordar:** [1-2 frases explicando como essa experiência pode resolver o gap]

---

**Gap 2:** [Nome do gap]

📍 **Experiência relacionada:** [Empresa - Cargo - Período]

💡 **Como abordar:** [1-2 frases explicando como essa experiência pode resolver o gap]

---

[Repita para cada gap]

---

### 📋 RESUMO DE EXPERIÊNCIAS A OTIMIZAR

Liste as experiências profissionais que precisam ser trabalhadas:

1. **[Empresa - Cargo]** → Vai resolver gaps: [lista de gaps]
2. **[Empresa - Cargo]** → Vai resolver gaps: [lista de gaps]
3. (etc)

---

⏸️ **Revise o diagnóstico acima. Responda "OK" para prosseguir para a coleta de dados.**
"""
