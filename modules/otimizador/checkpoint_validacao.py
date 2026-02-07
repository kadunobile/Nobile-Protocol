"""
Checkpoint 1: Validação - Mapeia Gap → Experiência e valida dados coletados.

Este checkpoint mostra um resumo de todos os dados coletados e como
cada gap será preenchido com dados de cada experiência, permitindo
que o usuário confirme ou corrija antes da reescrita.
"""

import streamlit as st


def prompt_checkpoint_validacao():
    """
    Gera prompt para checkpoint de validação.
    
    Mostra mapeamento completo de:
    - Quais gaps serão resolvidos
    - Com quais dados de quais experiências
    - Confirma se tudo está correto antes de reescrever
    
    Returns:
        str: Prompt formatado para o GPT
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    
    return f"""✅ **CHECKPOINT 1: VALIDAÇÃO DE DADOS**

**CARGO-ALVO:** {cargo}

---

**INSTRUÇÕES PARA O ASSISTENTE:**

Com base nas respostas do usuário na etapa anterior, crie um MAPEAMENTO CLARO de:

1. Quais gaps serão resolvidos
2. Com quais dados coletados
3. Em quais experiências

---

### 📊 MAPEAMENTO GAP → EXPERIÊNCIA → DADOS

**Gap 1:** [Nome do gap]

🔗 **Será resolvido com dados de:**
- **Experiência:** [Empresa - Cargo]
- **Resultado:** [Dado coletado]
- **Métrica:** [Dado coletado]
- **Como resolve:** [Contexto fornecido pelo usuário]

---

**Gap 2:** [Nome do gap]

🔗 **Será resolvido com dados de:**
- **Experiência:** [Empresa - Cargo]
- **Resultado:** [Dado coletado]
- **Métrica:** [Dado coletado]
- **Como resolve:** [Contexto fornecido pelo usuário]

---

[Repita para todos os gaps]

---

### 📋 DADOS COLETADOS POR EXPERIÊNCIA

**Experiência 1: [Empresa - Cargo - Período]**

✅ **Dados coletados:**
- Resultado quantificável: [resposta]
- Métrica usada: [resposta]
- Contexto do gap: [resposta]

🎯 **Vai resolver:** [Lista de gaps]

---

**Experiência 2: [Empresa - Cargo - Período]**

✅ **Dados coletados:**
- Resultado quantificável: [resposta]
- Métrica usada: [resposta]
- Contexto do gap: [resposta]

🎯 **Vai resolver:** [Lista de gaps]

---

[Repita para todas as experiências]

---

### 🔍 VERIFICAÇÃO DE QUALIDADE

**Dados completos:** [X de X experiências] ✅  
**Gaps cobertos:** [Y de Z gaps] ✅  
**Métricas quantificáveis:** [Todas/Algumas/Nenhuma]

---

### ⚠️ PONTOS DE ATENÇÃO

[Se houver dados faltando ou inconsistentes, liste aqui:]

- [Ponto 1]
- [Ponto 2]

---

⏸️ **Revise o mapeamento acima.**

**Se estiver tudo correto, responda "APROVAR" para iniciar a reescrita.**

**Se quiser fazer alguma correção, indique qual experiência e o que precisa ser ajustado.**
"""
