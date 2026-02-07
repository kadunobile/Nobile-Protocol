import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import chamar_gpt, scroll_topo

def fase_15_reality_check():
    scroll_topo()
    st.markdown("# 🧠 Reality Check - Análise Crítica")
    st.markdown("---")
    
    st.info("""
    **O que é Reality Check?**  
    Uma análise honesta e detalhada do seu CV, identificando:
    - ✅ Pontos fortes que você deve enfatizar
    - ❌ Gaps (lacunas) que precisam ser corrigidos
    - 💡 Oportunidades de melhoria
    
    Esta análise funciona para **qualquer cargo**: júnior, pleno, sênior, gerente, diretor, etc.
    """)

    with st.spinner("🧠 Cruzando CV × Cargo × Salário × Região..."):
        perfil = st.session_state.perfil
        pretensao = perfil['pretensao_salarial']
        cargo = perfil['cargo_alvo']
        local = perfil['localizacao']

        msgs = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"""REALITY CHECK:

P1 Objetivo: {perfil['objetivo']}
P2 Cargo: {cargo}
P3 Pretensão: {pretensao} mensal
P4 Local: {local}
Remoto: {'Sim' if perfil.get('remoto') else 'Não'}

DEEP SCAN:
{st.session_state.analise_inicial}

FORMATO EXATO OBRIGATÓRIO:

🎯 **REALITY CHECK - ANÁLISE ESTRATÉGICA**

**CARGO DESEJADO:** {cargo}

**NOMENCLATURAS SIMILARES NO MERCADO:**
• [Variação 1]
• [Variação 2]
• [Variação 3]

*(Recrutadores usam diferentes nomes para a mesma função)*

---

### 📊 ANÁLISE SALARIAL

**Pretensão Informada:** {pretensao} mensal

**Faixa Salarial Geral:** [mínimo] a [máximo]

**Veredito:** [Abaixo/Na Média/Acima]

[Contexto]

---

### ⚠️ ANÁLISE DE GAP - CIRÚRGICA

**Contexto:** Você busca **{cargo}** com pretensão de **{pretensao}** mensal em **{local}**.

**O que o mercado espera VS o que seu CV demonstra:**

| EXPECTATIVA DO MERCADO | SEU CV HOJE | STATUS |
|------------------------|-------------|--------|
| [Skill/experiência 1] | [Tem/Não tem/Parcial] | [✅/⚠️/❌] |
| [Skill/experiência 2] | [Tem/Não tem/Parcial] | [✅/⚠️/❌] |
| [Skill/experiência 3] | [Tem/Não tem/Parcial] | [✅/⚠️/❌] |

**Gaps Prioritários para Corrigir no CV:**

1. **[Gap Real 1]:** [Por que isso importa especificamente para {cargo}] → **Ação:** [O que fazer]
2. **[Gap Real 2]:** [Por que isso importa especificamente para {cargo}] → **Ação:** [O que fazer]
3. **[Gap Real 3]:** [Por que isso importa especificamente para {cargo}] → **Ação:** [O que fazer]

⚠️ **REGRA CRÍTICA:** APENAS mencione gaps que sejam:
- Diretamente relacionados ao cargo {cargo}
- Corrigíveis (não invente barreiras inexistentes)
- Relevantes para o mercado de {local}

❌ **NÃO MENCIONE:**
- "Falta experiência internacional" (a menos que o cargo EXIJA isso explicitamente)
- "Falta conhecimento em [tecnologia aleatória]" (a menos que seja padrão no cargo)
- Gaps genéricos de livros de carreira

---

### 🎯 VEREDITO DO HEADHUNTER

**Nível de Desafio:** [Baixo/Médio/Alto]

**Estratégia:** Focar em [ponto forte] para justificar {pretensao}

---

### ✅ PRÓXIMOS PASSOS

Use os **botões na barra lateral** para continuar:

• 🔧 **Otimizar CV + LinkedIn**
• 🏢 **Empresas Discovery**
• 🎯 **Analisar Vaga**
• 🎤 **Prep. Entrevista**
• 📊 **Análise de Mercado**"""}
        ]

        reality = chamar_gpt(st.session_state.openai_client, msgs)

        if reality:
            st.session_state.mensagens = [
                {"role": "system", "content": SYSTEM_PROMPT + f"\n\nCV DO CANDIDATO (uso interno): {st.session_state.cv_texto}\n\nCARGO-ALVO: {cargo}"},
                {"role": "assistant", "content": reality}
            ]
            st.session_state.force_scroll_top = True
            st.session_state.fase = 'CHAT'
            st.rerun()