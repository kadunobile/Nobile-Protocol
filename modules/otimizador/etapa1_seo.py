def prompt_etapa1(cargo):
    import streamlit as st
    
    # Get CV from session state
    cv_texto = st.session_state.get('cv_texto', '')
    
    if not cv_texto:
        return """⚠️ **ERRO:** CV não encontrado na sessão.

Por favor, retorne ao início e faça upload do seu CV novamente.

**Clique em "🔄 Recomeçar" na barra lateral.**"""
    
    return f"""Inicie a ETAPA 1 do otimizador de CV.

**CV DO CANDIDATO:**
{cv_texto}

---

Analise o CV acima e identifique as 10 KEYWORDS mais importantes para o cargo de **{cargo}**.

**IMPORTANTE - REGRAS DE ANÁLISE:**
1. ANTES de marcar algo como ausente, busque SINÔNIMOS e VARIAÇÕES no CV
   - Ex: "liderança" pode aparecer como "gestão de equipe", "coordenação", "supervisão"
   - Ex: "Python" pode estar em contextos de "automação", "scripts", "análise de dados"
   - Ex: "gestão de projetos" pode aparecer como "coordenação de iniciativas"
2. Só marque como FALTANDO se não encontrado em NENHUMA forma
3. Se encontrado mas fraco/implícito, marque como "presente mas pode ser reforçado"

Compare cada keyword com o CV atual.

Formato EXATO:

🎯 **ETAPA 1: MAPEAMENTO DE SEO - {cargo.upper()}**

**TOP 10 KEYWORDS DO MERCADO:**

---

### ✅ **PRESENTE NO SEU CV:**

[Para cada keyword PRESENTE, liste:]
**[Número]. [Keyword]**

📍 **Evidência:** [Onde/como aparece no CV - cite frase específica ou contexto]  
💡 **Contexto:** [Breve explicação de como é demonstrado]

[Continue para todas as keywords presentes]

---

### ⚠️ **PRESENTE MAS PODE SER REFORÇADO:**

[Para keywords que aparecem implicitamente ou de forma fraca:]

**[Número]. [Keyword]**

📍 **Evidência atual:** [O que foi encontrado - seja específico]  
💡 **Como reforçar:** [Sugestão concreta de como destacar melhor]

---

### ❌ **FALTANDO NO SEU CV:**

[IMPORTANTE: Só liste aqui se REALMENTE ausente após busca por sinônimos]

[Para cada keyword AUSENTE, forneça:]

**[Número]. [Nome da Keyword]**

📚 **O que é:** [Definição clara e objetiva em 1-2 linhas]

💡 **Por que importa:** [Explicação da relevância para o cargo - ex: "90% das vagas de {cargo} exigem", "Habilidade core para crescimento"]

✍️ **Como adicionar:** [Orientação prática sobre como incluir no CV - ex: "Descreva como você organizava o funil de vendas", "Mencione indicadores que você monitorava"]

[Repita para cada keyword ausente]

---

### 🎯 **RESUMO:**

✅ **Presentes:** [X] keywords  
⚠️ **Para reforçar:** [Y] keywords  
❌ **Ausentes:** [Z] keywords

---

⏸️ **Revise as keywords acima. Se concordar com a análise, responda "CONTINUAR" para avançar para a próxima etapa.**
"""
