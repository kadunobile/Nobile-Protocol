def prompt_etapa1(cargo):
    return f"""Inicie a ETAPA 1 do otimizador de CV.

Analise o CV do candidato (no contexto) e identifique as 10 KEYWORDS mais importantes para o cargo de {cargo}.

Compare cada keyword com o CV atual.

Formato EXATO:

🎯 **ETAPA 1: MAPEAMENTO DE SEO - {cargo.upper()}**

**TOP 10 KEYWORDS DO MERCADO:**

---

### ✅ **PRESENTE NO SEU CV:**

[Para cada keyword PRESENTE, liste:]
1. **[Keyword 1]** - [Breve explicação de onde/como aparece no CV - ex: "Mencionado 3 vezes nas experiências", "Você já demonstra liderança"]

[Continue para todas as keywords presentes]

---

### ❌ **FALTANDO NO SEU CV:**

[Para cada keyword AUSENTE, forneça:]

**[Número]. [Nome da Keyword]**

📚 **O que é:** [Definição clara e objetiva em 1-2 linhas]

💡 **Por que importa:** [Explicação da relevância para o cargo - ex: "90% das vagas de {cargo} exigem", "Habilidade core para crescimento"]

✍️ **Como adicionar:** [Orientação prática sobre como incluir no CV - ex: "Descreva como você organizava o funil de vendas", "Mencione indicadores que você monitorava"]

[Repita para cada keyword ausente]

---

### 🔴 **AÇÃO NECESSÁRIA:**

Preencha as lacunas abaixo com informações REAIS da sua experiência para cada keyword faltante:

[Para cada keyword ausente, adicione:]

**Box [Número] - [Nome da Keyword]:**
[Espaço para o usuário preencher - será solicitado via interface interativa]

---

⏸️ **Após analisar as keywords acima, você será solicitado a preencher informações sobre as keywords faltantes em boxes interativas.**

**Aguardando seu preenchimento para continuar a otimização...**

---

### 📝 IMPORTANTE:

- Você DEVE preencher pelo menos 1 keyword faltante antes de continuar
- Use informações REAIS da sua experiência profissional
- Seja específico e inclua números/métricas quando possível

Após preencher, clique em **"🚀 CONTINUAR OTIMIZAÇÃO"** para avançar para a ETAPA 2 (Interrogatório Tático).
"""
