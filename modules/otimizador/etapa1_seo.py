import streamlit as st

def prompt_etapa1(cargo):
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

🎯 **ETAPA 1: ANÁLISE DE KEYWORDS - {cargo.upper()}**

**TOP 10 KEYWORDS ESSENCIAIS:**

---

### ✅ **PRESENTES NO SEU CV**

[Para cada keyword PRESENTE, liste de forma concisa:]
**[Número]. [Keyword]** - Encontrada no contexto: [breve menção]

---

### ⚠️ **PODEM SER REFORÇADAS**

[Para keywords que aparecem implicitamente:]
**[Número]. [Keyword]** - Como reforçar: [sugestão breve]

---

### ❌ **AUSENTES NO SEU CV**

[IMPORTANTE: Só liste aqui se REALMENTE ausente após busca por sinônimos]

[Para cada keyword AUSENTE:]
**[Número]. [Keyword]** - Relevância: [explicação breve]

---

### 📊 **RESUMO:**

✅ Presentes: [X] keywords  
⚠️ Para reforçar: [Y] keywords  
❌ Ausentes: [Z] keywords

**Próxima etapa:** Vou fazer perguntas específicas sobre suas experiências para complementar seu CV com dados quantitativos.

---

⏸️ **Revise as keywords acima. Responda "CONTINUAR" quando estiver pronto para a próxima etapa.**
"""
