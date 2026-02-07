"""
Etapa 2: Reescrita Progressiva - Reescreve uma experiência por vez com destaque.

Esta etapa reescreve cada experiência profissional progressivamente,
mostrando ANTES vs DEPOIS e destacando mudanças em VERDE.
"""

import streamlit as st


def prompt_etapa2_reescrita_progressiva(experiencia_num=1):
    """
    Gera prompt para reescrita progressiva de uma experiência.
    
    Args:
        experiencia_num: Número da experiência sendo reescrita (1, 2, 3, etc)
    
    Returns:
        str: Prompt formatado para o GPT
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_texto = st.session_state.get('cv_texto', '')
    
    if not cv_texto:
        return """⚠️ **ERRO:** CV não encontrado na sessão."""
    
    return f"""✍️ **ETAPA 2: REESCRITA PROGRESSIVA - EXPERIÊNCIA #{experiencia_num}**

**CARGO-ALVO:** {cargo}

---

**INSTRUÇÕES PARA O ASSISTENTE:**

Você vai reescrever UMA experiência profissional por vez, mostrando claramente as melhorias.

**REGRAS DE REESCRITA:**

1. **Manter estrutura original** - Não mudar o formato do CV
2. **Melhorar genéricos** - Trocar frases vagas por específicas
3. **Adicionar dados quantitativos** - Inserir os resultados coletados
4. **Destacar mudanças** - Usar **negrito** ou MAIÚSCULAS para novos dados
5. **Mostrar ANTES vs DEPOIS** - Lado a lado para comparação

---

### 📋 EXPERIÊNCIA #{experiencia_num}

**IDENTIFICAÇÃO:**
[Empresa - Cargo - Período]

---

### 🔴 VERSÃO ANTERIOR (CV Original)

[Copie a descrição EXATA desta experiência do CV original do candidato]

---

### 🟢 VERSÃO OTIMIZADA (Nova)

[Reescreva a experiência aplicando as melhorias:]

**[Cargo] na [Empresa]**  
_[Período]_

• [Ponto 1 melhorado - com **DADOS QUANTITATIVOS** em negrito]
• [Ponto 2 melhorado - com **MÉTRICAS** em negrito]
• [Ponto 3 melhorado - com **RESULTADOS** em negrito]
• [Continue...]

---

### ✨ MUDANÇAS REALIZADAS

**O que foi melhorado:**

1. ✅ **Adicionado:** [Dado quantitativo X]
2. ✅ **Reforçado:** [Competência Y com métrica]
3. ✅ **Especificado:** [Substituiu "ajudei" por "liderei equipe de 10 pessoas"]
4. [Etc...]

**Gaps resolvidos nesta experiência:**
- [Gap 1]
- [Gap 2]

---

### 📊 IMPACTO NO SCORE ATS

**Antes desta reescrita:**
- Keywords: [X]
- Métricas: [Y]

**Depois desta reescrita:**
- Keywords: [X + adicionadas]
- Métricas: [Y + adicionadas]

---

⏸️ **Revise a reescrita acima.**

**Se aprovar, responda "PRÓXIMA" para reescrever a experiência seguinte.**

**Se quiser ajustes nesta experiência, indique o que mudar.**
"""


def prompt_etapa2_reescrita_final():
    """
    Gera prompt final após reescrever todas as experiências.
    
    Returns:
        str: Prompt de conclusão da etapa 2
    """
    return """🎉 **ETAPA 2: REESCRITA COMPLETA!**

---

### ✅ TODAS AS EXPERIÊNCIAS FORAM OTIMIZADAS

Você já revisou e aprovou todas as experiências reescritas.

---

### 📄 PRÓXIMO PASSO: CHECKPOINT 2 - REVIEW FINAL

No próximo checkpoint, você verá:

1. **CV completo otimizado** - Todas as seções juntas
2. **Resumo de melhorias** - O que foi mudado no geral
3. **Oportunidade de ajustes finais** - Edições globais antes de finalizar

---

⏸️ **Responda "CONTINUAR" para ir para o Checkpoint 2 (Review Final).**
"""
