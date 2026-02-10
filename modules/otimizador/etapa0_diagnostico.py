"""
Etapa 0: Diagnóstico - Identificar onde cada gap pode ser resolvido no CV.

Esta etapa pergunta ao usuário onde no CV cada gap identificado foi ou pode ser resolvido,
ajudando a identificar as experiências relevantes para otimização.
"""

import streamlit as st


def prompt_etapa0_diagnostico_gap_individual(gap_index):
    """
    Gera prompt para perguntar sobre um gap específico ao usuário.
    
    Args:
        gap_index: Índice do gap atual (0-based)
    
    Returns:
        str: Prompt formatado perguntando sobre o gap específico
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    gaps = st.session_state.get('gaps_alvo', [])
    
    if not gaps or gap_index >= len(gaps):
        return None
    
    gap_atual = gaps[gap_index]
    total_gaps = len(gaps)
    
    return f"""🔍 **ETAPA 0: DIAGNÓSTICO ESTRATÉGICO** ({gap_index + 1}/{total_gaps})

**CARGO-ALVO:** {cargo}

---

### Gap a Analisar:
**"{gap_atual}"**

---

**Pergunta para você:**

Você tem experiência prática com **{gap_atual}**?

- ✅ Se **SIM**: Por favor, responda em qual empresa/cargo você trabalhou com isso e descreva brevemente o contexto (1-2 frases).
  
  *Exemplo: "Sim, na ARQUIVEI como RevOps Manager eu usava Tableau para criar dashboards de receita recorrente."*

- ❌ Se **NÃO**: Digite "não tenho" ou "não" para pularmos este gap.

💡 **Dica:** Seja específico! Quanto mais detalhes você fornecer agora, melhor será a otimização do seu CV.
"""


def prompt_etapa0_diagnostico():
    """
    Gera prompt inicial da etapa de diagnóstico com persona Headhunter Elite.
    
    Apresenta a abordagem refinada de otimização pré-chat que inclui:
    - SEO Mapping, Deep Dive, Curadoria, Engenharia de Texto, Validação Final
    - Arquivo Mestre com LinkedIn metadata e CV completo
    
    Returns:
        str: Prompt formatado para o GPT
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_texto = st.session_state.get('cv_texto', '')
    gaps = st.session_state.get('gaps_alvo', [])
    perfil = st.session_state.get('perfil', {})
    
    if not cv_texto:
        return """⚠️ **ERRO:** CV não encontrado na sessão.
        
Por favor, retorne ao início e faça upload do seu CV novamente.

**Clique em "🔄 Recomeçar" na barra lateral.**"""
    
    if not gaps:
        gaps = ["Melhorar estrutura geral do CV"]
        st.session_state.gaps_alvo = gaps
    
    # Inicializar estado para rastrear gaps
    if 'gaps_respostas' not in st.session_state:
        st.session_state.gaps_respostas = {}
    
    # Preparar lista de gaps formatada
    gaps_texto = "\n".join([f"  • {gap}" for gap in gaps])
    
    # Identificar dados faltantes do perfil
    dados_faltantes = []
    if not perfil.get('objetivo'):
        dados_faltantes.append("• **Objetivo principal** (recolocação / transição / promoção)")
    if not perfil.get('pretensao_salarial'):
        dados_faltantes.append("• **Pretensão salarial**")
    if not perfil.get('localizacao'):
        dados_faltantes.append("• **Localização** (onde mora / onde quer trabalhar)")
    
    dados_faltantes_texto = "\n".join(dados_faltantes) if dados_faltantes else "✅ _Todos os dados básicos já foram coletados._"
    
    # Montar o prompt com o fluxo completo do Headhunter Elite
    return f"""# 🎩 **HEADHUNTER ELITE** - Otimização Pré-Chat

Olá! Sou o **Headhunter Elite**, especialista em recolocação e otimização de CVs para cargos estratégicos.

Já recebi seu CV (mantido em sigilo para análise interna) e identifiquei os seguintes **gaps de otimização** do Reality Check:

{gaps_texto}

---

## 📋 **FLUXO DE OTIMIZAÇÃO**

Vou conduzir você por um processo estruturado e interativo:

### **1️⃣ COLETA DE DADOS FALTANTES**

Preciso confirmar/coletar apenas as informações que ainda não tenho:

{dados_faltantes_texto}

**→ PERGUNTA 1:** Se algum dado acima está faltando, me informe agora. Caso contrário, confirme que tudo já está OK.

---

### **2️⃣ SEO MAPPING (Palavras-chave Estratégicas)**

Vou listar **10 palavras-chave essenciais** para o cargo-alvo: **{cargo}**.

Se identificar que alguma palavra-chave está faltando no seu CV ou nos gaps, vou perguntar especificamente sobre ela. **Vou pausar após cada pergunta** para você responder.

---

### **3️⃣ DEEP DIVE (Dados Concretos)**

Para cada experiência com pontos genéricos ou gaps identificados, vou pedir **dados concretos**:
- Impacto em **R$**, **%**, **tempo**
- Tamanho de **equipe** ou **projeto**
- **Métricas pertinentes** ao cargo-alvo

**Não quero apenas números**, mas o **contexto + resultado/impacto**. Vou pausar para cada pergunta.

---

### **4️⃣ CURADORIA (Conquistas e Soft Skills)**

Vou perguntar sobre **conquistas, projetos ou soft skills indispensáveis** que ainda não foram cobertos.

Avaliarei cada item:
- ✅ **Relevante** para o cargo-alvo → incluir
- ⚠️ **Ruído** → alertar se não agregar valor

Vou pausar após cada pergunta.

---

### **5️⃣ ENGENHARIA DE TEXTO (Reescrita Estratégica)**

Vou reescrever:

**📝 RESUMO:**
- Hook inicial
- Metodologia de trabalho
- 2 impactos com contexto + resultado/impacto
- Palavras-chave, hard skills, soft skills e stack técnico

**💼 EXPERIÊNCIAS:**
Para cada experiência relevante:
- Formato: **Cargo | Empresa**
- Foco principal
- 2 bullets: **ação + ferramenta + resultado/impacto**
- 5-8 hard skills como palavras-chave

---

### **6️⃣ VALIDAÇÃO FINAL**

Vou mostrar um **rascunho** com o Resumo e Experiências reescritas.

**→ PERGUNTA FINAL:** O conteúdo está robusto e alinhado com o cargo-alvo?

---

### **7️⃣ ARQUIVO MESTRE**

Após aprovação, vou compilar tudo em um **bloco único** estruturado:

**📄 SEÇÃO 1 - LinkedIn Metadata:**
- Headlines otimizadas
- Lista de skills e nomenclaturas do cargo

**📄 SEÇÃO 2 - CV Completo:**
- Header
- `SUMMARY` (Resumo otimizado)
- `EXPERIENCE` (Experiências otimizadas)
- `EDUCATION` (Educação)
- `LANGUAGES` (Idiomas)

**⚠️ IMPORTANTE:** Ainda não vou incluir instruções de exportação ou FlowCV neste momento.

---

## 🚀 **VAMOS COMEÇAR!**

Me confirme se os dados básicos estão completos ou se preciso coletar algo. Depois, seguiremos para o SEO Mapping e as próximas etapas.

**Sua resposta:**
"""
