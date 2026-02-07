import streamlit as st

def prompt_etapa4():
    # Get CV from session to check original format
    cv_texto = st.session_state.get('cv_texto', '')
    
    return f"""✅ **Perfeito! Dados coletados.**

### ✍️ ETAPA 4: REESCRITA ESTRATÉGICA

Agora vou reescrever seu CV seguindo o **FORMATO ORIGINAL** que você usou, mas com as melhorias:
- Integrar keywords identificadas
- Adicionar métricas e dados quantitativos
- Destacar resultados de impacto
- Manter a estrutura que você já usa

---

**INSTRUÇÕES CRÍTICAS:**

1. **MANTER O FORMATO DO CV ORIGINAL**
   - Analise a estrutura atual do CV do candidato
   - Se usa seções como "Foco do Cargo:", "Liderança:", etc., MANTENHA
   - Se usa bullets simples, MANTENHA
   - Não force modelo STAR ou outros padrões

2. **EXEMPLO DE FORMATO (se o CV usar):**
   ```
   Gerente de Inteligência de Negócios & Sales Ops
   Foco do Cargo: [descrição com métricas]
   Liderança de Data Analytics: [descrição com resultados]
   Salesforce/CRM Management: [descrição com impacto]
   Dashboards & KPIs: [descrição com dados]
   Eficiência Operacional: [descrição com números]
   Palavras-chave: [keywords integradas]
   ```

3. **PRINCÍPIOS DE REESCRITA:**
   - Adicionar números e métricas (R$, %, tempo, tamanho equipe)
   - Usar verbos de ação fortes
   - Quantificar resultados sempre que possível
   - Integrar keywords naturalmente
   - Ser específico, não genérico

4. **O QUE USAR:**
   - Dados da ETAPA 2 (impacto, equipe, orçamento, resultados)
   - Informações da ETAPA 3 (contexto, projetos, skills)
   - Keywords da ETAPA 1

---

**CV ORIGINAL PARA REFERÊNCIA:**
(Primeiros caracteres mostrados como exemplo do formato a manter)
{cv_texto[:1000]}...

---

Agora reescreva CADA experiência profissional do CV seguindo o formato original mas com as melhorias aplicadas.

Após reescrever, mostre o resultado e adicione o botão: "Ver CV Revisado Completo"
"""
