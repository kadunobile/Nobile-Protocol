def prompt_etapa1(cargo):
    return f"""Inicie a ETAPA 1 do otimizador de CV.

Analise o CV do candidato (no contexto) e identifique as 10 KEYWORDS mais importantes para o cargo de {cargo}.

Compare cada keyword com o CV atual.

Formato EXATO:

🎯 **ETAPA 1: MAPEAMENTO DE SEO - {cargo.upper()}**

**TOP 10 KEYWORDS DO MERCADO:**
1. [Keyword 1] - ✅ PRESENTE no CV / ❌ AUSENTE no CV
2. [Keyword 2] - Status
3. [Keyword 3] - Status
4. [Keyword 4] - Status
5. [Keyword 5] - Status
6. [Keyword 6] - Status
7. [Keyword 7] - Status
8. [Keyword 8] - Status
9. [Keyword 9] - Status
10. [Keyword 10] - Status

---

### 🔴 ANÁLISE DETALHADA DAS KEYWORDS AUSENTES:

**Para cada keyword AUSENTE, forneça:**

#### [Nome da Keyword] ❌
**Por que é importante:** [Explicação de 1-2 linhas sobre por que essa keyword é essencial para o cargo]

**Como incluir:** [Exemplos práticos de frases/contextos onde essa keyword poderia aparecer no CV]

**Exemplo:** "Gerenciei equipe de 10 pessoas utilizando metodologia [keyword]"

---

### ✅ KEYWORDS JÁ PRESENTES:

[Liste as keywords que já estão no CV e explique brevemente onde aparecem]

---

### 📝 PRÓXIMO PASSO:

Agora vou fazer perguntas específicas sobre cada experiência profissional para coletar dados que incluam essas keywords ausentes.

Digite **"OK"** ou **"CONTINUAR"** para prosseguir para a ETAPA 2 (Interrogatório Tático).
"""
