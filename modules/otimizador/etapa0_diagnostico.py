"""
Etapa 0: Diagnóstico - Identificar onde cada gap pode ser resolvido no CV.

Esta etapa pergunta ao usuário onde no CV cada gap identificado foi ou pode ser resolvido,
ajudando a identificar as experiências relevantes para otimização.

HEADHUNTER ELITE: Usa inteligência de mercado para análise personalizada.
"""

import streamlit as st
from modules.otimizador.market_knowledge import detectar_area_por_cargo, obter_conhecimento_mercado
from modules.otimizador.classificador_perfil import classificar_senioridade_e_estrategia
from modules.otimizador.analisador_bullets import analisar_bullets_fracos, contar_bullets_fracos


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
    Gera prompt inicial da etapa de diagnóstico com HEADHUNTER ELITE.
    
    Usa inteligência de mercado para análise personalizada por senioridade e área.
    
    Returns:
        str: Prompt formatado com análise inteligente do perfil
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_texto = st.session_state.get('cv_texto', '')
    gaps = st.session_state.get('gaps_alvo', [])
    
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
    
    # === HEADHUNTER ELITE: Análise Inteligente ===
    
    # 1. Classificar perfil (senioridade + estratégia)
    classificacao = classificar_senioridade_e_estrategia(cv_texto, cargo)
    senioridade = classificacao['senioridade']
    area = classificacao['area_profissional']
    modo = classificacao['modo_interrogatorio']
    
    # 2. Obter conhecimento de mercado
    conhecimento = obter_conhecimento_mercado(area)
    keywords_mercado = conhecimento.get('keywords', [])
    
    # 3. Analisar bullets fracos
    bullets_fracos_count = contar_bullets_fracos(cv_texto, area, senioridade)
    
    # 4. Calcular gaps críticos (keywords essenciais faltando)
    # Contar quantas keywords do mercado estão no CV
    cv_lower = cv_texto.lower()
    keywords_encontradas = sum(1 for kw in keywords_mercado if kw.lower() in cv_lower)
    keywords_faltando = len(keywords_mercado) - keywords_encontradas
    
    # Preparar lista de gaps formatada
    gaps_texto = "\n".join([f"{i+1}. {gap}" for i, gap in enumerate(gaps)])
    
    # === PROMPT HEADHUNTER ELITE ===
    
    return f"""🎯 **HEADHUNTER ELITE MODE ATIVADO**

---

### 📊 ANÁLISE DO SEU PERFIL

**CARGO-ALVO:** {cargo}  
**ÁREA:** {area}  
**SENIORIDADE DETECTADA:** {senioridade.upper()}  
**ESTRATÉGIA:** {modo.capitalize()}

---

### 🔍 ANÁLISE INICIAL DO CV

Analisei seu CV atual e identifiquei:

✅ **PONTOS FORTES:** {keywords_encontradas} keywords alinhadas com o mercado de {area}  
❌ **GAPS CRÍTICOS:** {keywords_faltando} keywords essenciais faltando  
⚠️ **BULLETS FRACOS:** {bullets_fracos_count} experiências com verbo fraco ou sem métrica

---

### 📋 COMO VAMOS TRABALHAR

Vou te fazer perguntas CIRÚRGICAS em 7 etapas:

1️⃣ **COLETA DE PERFIL** - Objetivo, pretensão, localização (apenas o que faltar)  
2️⃣ **SEO MAPPING** - 10 keywords essenciais para {cargo}  
3️⃣ **DEEP DIVE** - Dados concretos de cada experiência  
4️⃣ **CURADORIA** - Conquistas/projetos não mencionados  
5️⃣ **ENGENHARIA DE TEXTO** - Reescrita com método STAR  
6️⃣ **VALIDAÇÃO** - Mostro rascunho para aprovação  
7️⃣ **ARQUIVO MESTRE** - CV + LinkedIn otimizados

⏱️ **Tempo estimado:** 15-20 minutos  
⏸️ **Pausas obrigatórias:** Após etapas 1, 2, 3 e 6

---

### 🚀 ETAPA 1: DIAGNÓSTICO DE GAPS

Identificamos **{len(gaps)}** gap(s) no Reality Check:

{gaps_texto}

Vou perguntar sobre **cada gap individualmente** para entender onde você já tem experiência e como podemos destacar isso no seu CV.

💡 **Por que isso importa?** Cada informação que você me der será usada para personalizar 100% do seu CV para o cargo-alvo de **{cargo}** no nível **{senioridade}**.

---

⏭️ **Vamos começar com o primeiro gap...**
"""
