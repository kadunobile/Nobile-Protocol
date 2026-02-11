"""
Checkpoint 1: Validação - Mapeia Gap → Experiência e valida dados coletados.

Este checkpoint mostra um resumo de todos os dados coletados e como
cada gap será preenchido com dados de cada experiência, permitindo
que o usuário confirme ou corrija antes da reescrita.
"""

import streamlit as st
import logging
from core.dynamic_questions import obter_historico_qa

logger = logging.getLogger(__name__)


def prompt_checkpoint_validacao():
    """
    Gera prompt para checkpoint de validação COM DADOS REAIS.
    
    Mostra mapeamento completo de:
    - Quais gaps serão resolvidos (com respostas do usuário)
    - Com quais dados de quais experiências (do histórico de coleta)
    - Confirma se tudo está correto antes de reescrever
    
    Returns:
        str: Prompt formatado COM DADOS REAIS da sessão
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    
    # ===== OBTER DADOS REAIS DA SESSÃO =====
    
    # 1. Gaps diagnosticados
    gaps_respostas = st.session_state.get('gaps_respostas', {})
    gaps_com_experiencia = {gap: info for gap, info in gaps_respostas.items() if info.get('tem_experiencia')}
    gaps_sem_experiencia = [gap for gap, info in gaps_respostas.items() if not info.get('tem_experiencia')]
    
    # 2. Keywords SEO coletadas
    seo_respostas = st.session_state.get('seo_keywords_respostas', {})
    
    # 3. Dados da coleta (Deep Dive)
    historico_coleta = obter_historico_qa('coleta')
    
    # ===== RENDERIZAR DADOS REAIS =====
    
    checkpoint = f"""✅ **CHECKPOINT 1: VALIDAÇÃO DE DADOS**

**CARGO-ALVO:** {cargo}

---

### 📊 MAPEAMENTO GAP → EXPERIÊNCIA → DADOS

"""
    
    # Renderizar gaps com experiência
    if gaps_com_experiencia:
        for i, (gap, info) in enumerate(gaps_com_experiencia.items(), 1):
            resposta = info.get('resposta', '(resposta não capturada)')
            # Truncar resposta longa
            resposta_display = resposta[:200] + ('...' if len(resposta) > 200 else '')
            
            checkpoint += f"""**Gap {i}: {gap}**

✅ **Você tem experiência:**
📝 _{resposta_display}_

---

"""
    else:
        checkpoint += "*(Nenhum gap com experiência foi identificado)*\n\n---\n\n"
    
    # Renderizar Keywords SEO coletadas
    if seo_respostas:
        checkpoint += f"""### 🎯 KEYWORDS SEO MAPEADAS ({len(seo_respostas)})

"""
        for keyword, resposta in seo_respostas.items():
            resposta_display = resposta[:200] + ('...' if len(resposta) > 200 else '')
            checkpoint += f"""**{keyword}**
📝 _{resposta_display}_

"""
        checkpoint += "\n---\n\n"
    
    # Renderizar dados coletados no Deep Dive
    if historico_coleta:
        checkpoint += f"""### 📋 DADOS COLETADOS NO DEEP DIVE ({len(historico_coleta)} perguntas)

"""
        for i, qa in enumerate(historico_coleta, 1):
            pergunta = qa['pergunta'][:150] + ('...' if len(qa['pergunta']) > 150 else '')
            resposta = qa['resposta'][:200] + ('...' if len(qa['resposta']) > 200 else '')
            
            checkpoint += f"""**P{i}:** {pergunta}
**R{i}:** _{resposta}_

"""
        checkpoint += "\n---\n\n"
    else:
        checkpoint += "### 📋 DADOS COLETADOS NO DEEP DIVE\n\n*(Nenhum dado coletado no Deep Dive)*\n\n---\n\n"
    
    # Renderizar gaps sem experiência (apenas lista)
    if gaps_sem_experiencia:
        checkpoint += f"""### ⚠️ GAPS SEM EXPERIÊNCIA ({len(gaps_sem_experiencia)})

Estes gaps não poderão ser resolvidos diretamente (você indicou não ter experiência):

"""
        for gap in gaps_sem_experiencia:
            checkpoint += f"- {gap}\n"
        
        checkpoint += "\n---\n\n"
    
    # Estatísticas de cobertura
    total_gaps = len(gaps_respostas)
    total_resolvidos = len(gaps_com_experiencia)
    total_keywords = len(seo_respostas)
    total_perguntas = len(historico_coleta)
    
    checkpoint += f"""### 🔍 VERIFICAÇÃO DE QUALIDADE

✅ **Gaps com experiência:** {total_resolvidos} de {total_gaps}  
✅ **Keywords SEO coletadas:** {total_keywords}  
✅ **Perguntas do Deep Dive respondidas:** {total_perguntas}

---

⏸️ **Revise o mapeamento acima.**

**Todas as informações estão corretas?**

✅ **Digite "APROVAR"** para iniciar a reescrita do CV com esses dados.

❌ **Se precisar corrigir algo**, indique o que precisa ser ajustado.
"""
    
    return checkpoint
