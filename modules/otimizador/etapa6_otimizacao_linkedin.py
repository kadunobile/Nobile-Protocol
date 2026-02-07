"""
Etapa 6: Otimização LinkedIn - Gera headlines, skills e about section.

Esta etapa cria conteúdo otimizado para LinkedIn:
- 3 opções de Headline (A/B/C Testing)
- Top Skills reordenadas (máximo 10)
- About Section otimizada
- Conquistas por experiência
"""

import streamlit as st


def prompt_etapa6_otimizacao_linkedin():
    """
    Gera prompt para otimização de LinkedIn.
    
    Cria múltiplas versões de headline, reorganiza skills,
    e gera about section baseado no CV otimizado.
    
    Returns:
        str: Prompt formatado para o GPT
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_otimizado = st.session_state.get('cv_otimizado', '')
    
    if not cv_otimizado:
        cv_otimizado = st.session_state.get('cv_texto', '')
    
    return f"""🔵 **ETAPA 6: OTIMIZAÇÃO DE LINKEDIN**

**CARGO-ALVO:** {cargo}

---

**CV OTIMIZADO:**
{cv_otimizado}

---

**INSTRUÇÕES PARA O ASSISTENTE:**

Baseado no CV otimizado acima, crie conteúdo estratégico para LinkedIn.

---

## 🎯 PARTE 1: HEADLINES (A/B/C Testing)

Crie 3 versões de headline, cada uma com abordagem diferente:

### **Opção A: Foco em Resultado**
[Headline de até 220 caracteres focada em resultados/impacto]

**Exemplo:** "Gerente de Marketing Digital | Aumentei ROI em 150% | Especialista em Growth Hacking"

---

### **Opção B: Foco em Expertise**
[Headline de até 220 caracteres focada em habilidades/expertise]

**Exemplo:** "Product Manager | Agile & Scrum Expert | 8+ anos liderando produtos SaaS B2B"

---

### **Opção C: Foco em Proposta de Valor**
[Headline de até 220 caracteres focada em valor entregue]

**Exemplo:** "Transformo dados em estratégias de vendas | Data Analyst | SQL + Python + Tableau"

---

## 💡 QUAL ESCOLHER?

**Opção A** → Melhor se você tem resultados impressionantes  
**Opção B** → Melhor se você é especialista técnico  
**Opção C** → Melhor se você quer destacar valor único

---

⏸️ **Qual headline você prefere? Responda A, B ou C**

---

## 🛠️ PARTE 2: TOP SKILLS

Com base no seu CV e cargo-alvo, estas são as Top 10 Skills para colocar no LinkedIn (em ordem de prioridade):

1. [Skill 1] ⭐⭐⭐
2. [Skill 2] ⭐⭐⭐
3. [Skill 3] ⭐⭐
4. [Skill 4] ⭐⭐
5. [Skill 5] ⭐⭐
6. [Skill 6] ⭐
7. [Skill 7] ⭐
8. [Skill 8] ⭐
9. [Skill 9] ⭐
10. [Skill 10] ⭐

**⭐⭐⭐** = Skill crítica para o cargo  
**⭐⭐** = Skill importante  
**⭐** = Skill complementar

---

💡 **Dica:** No LinkedIn, as primeiras 3 skills aparecem com mais destaque. Coloque suas forças ali.

---

⏸️ **Essa ordem de skills faz sentido para você? Responda OK para continuar ou sugira mudanças.**

---

## 📝 PARTE 3: ABOUT SECTION

[Gere um About Section de 3-4 parágrafos curtos, máximo 1300 caracteres, seguindo esta estrutura:]

**Parágrafo 1: Quem você é + Proposta de valor**
[2-3 frases sobre sua identidade profissional e o que você entrega]

**Parágrafo 2: Experiência e conquistas principais**
[2-3 frases sobre suas conquistas mais relevantes com dados]

**Parágrafo 3: Expertise e diferenciais**
[2-3 frases sobre suas habilidades únicas e o que te diferencia]

**Parágrafo 4: Call-to-action (opcional)**
[1 frase sobre o que você busca ou como podem te contatar]

---

### 📋 EXEMPLO DE ABOUT GERADO:

[Escreva o About Section completo aqui]

---

⏸️ **Revise o About Section acima. Responda "APROVAR" para salvar ou sugira edições.**

---

## 🏆 PARTE 4: CONQUISTAS POR EXPERIÊNCIA

Para cada experiência no seu CV otimizado, destaque as 2-3 conquistas principais que devem estar visíveis no LinkedIn:

### **[Empresa 1] - [Cargo]**
• [Conquista 1 com métrica]
• [Conquista 2 com métrica]
• [Conquista 3 com métrica]

### **[Empresa 2] - [Cargo]**
• [Conquista 1 com métrica]
• [Conquista 2 com métrica]

[Continue para todas as experiências relevantes]

---

💡 **Dica:** No LinkedIn, adicione essas conquistas como "Media" (fotos, PDFs) para ganhar mais visibilidade.

---

### ✅ RESUMO DO CONTEÚDO LINKEDIN

Você agora tem pronto:
- ✅ 3 opções de Headline (escolha 1)
- ✅ Top 10 Skills ordenadas
- ✅ About Section completo
- ✅ Conquistas destacadas por experiência

---

⏸️ **Responda "CONTINUAR" para ir para a etapa de Validação de Score ATS.**
"""
