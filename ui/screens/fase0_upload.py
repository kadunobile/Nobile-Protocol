import streamlit as st
from core.prompts import SYSTEM_PROMPT
from core.utils import extrair_texto_pdf, chamar_gpt

def fase_0_upload():
    st.markdown("# 📄 Envie seu Currículo")
    st.markdown("---")
    st.info("📌 Para iniciar o Diagnóstico, **anexe seu CV em PDF** abaixo.")

    arquivo = st.file_uploader("📄 Seu currículo em PDF", type=['pdf'])

    if arquivo:
        with st.spinner("🔍 Varredura Integral (Deep Scan)... Lendo 100% do conteúdo..."):
            texto = extrair_texto_pdf(arquivo)
            if texto:
                st.session_state.cv_texto = texto
                msgs = [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"""Faça a VARREDURA INTEGRAL deste CV.

INSTRUÇÕES CRÍTICAS:

1. **SENIORIDADE REAL:** Baseie-se em anos de experiência, tamanho de budget, equipe gerenciada
2. **STACK TÉCNICO:** Liste TODAS as ferramentas, metodologias e tecnologias mencionadas
3. **RESULTADOS QUANTIFICÁVEIS:** Identifique números, percentuais, valores (ex: "aumentou vendas em 30%")
4. **GAPS CONTEXTUAIS:** Identifique APENAS lacunas relevantes para cargos similares ao histórico do candidato

⚠️ **PROIBIDO:**
- Sugerir "experiência internacional" sem contexto justificado
- Mencionar gaps genéricos que não sejam diretamente relacionados ao perfil
- Inventar necessidades que não façam sentido para o nível/área do candidato

CV COMPLETO:
{texto}

FORMATO DE RESPOSTA:

### 🔍 ANÁLISE EXECUTIVA DO CV

**Nome:** [extrair do CV]
**Senioridade Detectada:** [Júnior/Pleno/Sênior/Especialista/Gerencial/Executivo]

---

### 💼 HISTÓRICO PROFISSIONAL

**Cargo Atual/Mais Recente:** [cargo] na [empresa]
**Tempo na Posição:** [X anos]

**Trajetória:**
• [Empresa 1] - [Cargo] ([período])
• [Empresa 2] - [Cargo] ([período])
[continuar...]

**Padrão Identificado:** [Ex: "Crescimento progressivo em vendas B2B" ou "Especialização em gestão de produtos tech"]

---

### 🛠️ STACK TÉCNICO COMPLETO

**Ferramentas:**
• [Ferramenta 1]
• [Ferramenta 2]
[listar TODAS mencionadas]

**Metodologias:**
• [Metodologia 1]
• [Metodologia 2]

**Certificações:**
• [Certificação 1 se houver]

---

### 📊 RESULTADOS QUANTIFICÁVEIS ENCONTRADOS

✅ [Resultado 1 com número]
✅ [Resultado 2 com número]
✅ [Resultado 3 com número]

⚠️ **Se não encontrar números:** "CV carece de métricas quantificáveis"

---

### ⚠️ GAPS CRÍTICOS IDENTIFICADOS

[REGRA: Liste APENAS gaps que sejam diretamente relevantes para o próximo passo na carreira do candidato, baseado no histórico dele]

1. **[Gap Específico 1]:** [Explicação objetiva do que falta e POR QUE é relevante para o perfil DELE]
2. **[Gap Específico 2]:** [Mesma lógica]
3. **[Gap Específico 3]:** [Mesma lógica]

**Exemplo CORRETO:**
"Para Gerente Comercial com histórico em vendas B2B: Falta demonstração clara de gestão de pipeline com CRM (crucial para cargos gerenciais comerciais)"

**Exemplo ERRADO (NÃO FAZER):**
"Falta experiência internacional" (quando o candidato sempre atuou localmente e não há indicação de que busca isso)

---

### 🎯 RESUMO ESTRATÉGICO

**Perfil Resumido em 1 Frase:**
[Descrição sintética: Ex: "Gerente Comercial Sênior com 8 anos em vendas B2B tech, especializado em SaaS"]

**Posicionamento Recomendado:**
[Cargos que fazem sentido para o próximo passo]

NÃO mostre o CV completo de volta."""}
                ]
                analise = chamar_gpt(st.session_state.openai_client, msgs)
                if analise:
                    st.session_state.analise_inicial = analise
                    st.session_state.fase = 'FASE_1_DIAGNOSTICO'
                    st.rerun()
