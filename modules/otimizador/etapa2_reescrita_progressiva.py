"""
Etapa 2: Reescrita Progressiva - Reescreve uma experiência por vez com destaque.

Esta etapa reescreve cada experiência profissional progressivamente,
mostrando apenas o texto reescrito final + opção de aprovar/editar.
"""

import streamlit as st
import logging
from core.cv_cache import get_cv_contexto_para_prompt
from core.dynamic_questions import obter_historico_qa

logger = logging.getLogger(__name__)

# Constants
MAX_CV_LENGTH_FOR_PROMPT = 3000  # Maximum CV length to include in prompt (preserves ~2-3 experiences)


def prompt_etapa2_reescrita_progressiva(experiencia_num=1):
    """
    Gera prompt para reescrita progressiva de UMA experiência.
    
    Mostra apenas o texto reescrito + opção de aprovar/editar,
    SEM reemitir instruções longas repetitivas.
    
    Args:
        experiencia_num: Número da experiência sendo reescrita (1, 2, 3, etc)
    
    Returns:
        str: Prompt formatado COM DADOS REAIS
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    cv_texto = st.session_state.get('cv_texto', '')
    
    if not cv_texto:
        return """⚠️ **ERRO:** CV não encontrado na sessão."""
    
    # Obter contexto compacto do CV (não o CV completo)
    cv_contexto = get_cv_contexto_para_prompt()
    
    # Obter dados coletados
    gaps_respostas = st.session_state.get('gaps_respostas', {})
    gaps_com_experiencia = [gap for gap, info in gaps_respostas.items() if info.get('tem_experiencia')]
    
    seo_respostas = st.session_state.get('seo_keywords_respostas', {})
    historico_coleta = obter_historico_qa('coleta')
    
    # Preparar contexto de dados coletados
    dados_coletados = ""
    
    if gaps_com_experiencia:
        dados_coletados += f"**GAPS RESOLVIDOS ({len(gaps_com_experiencia)}):**\n"
        for gap, info in gaps_respostas.items():
            if info.get('tem_experiencia'):
                resposta = info.get('resposta', '')[:150]
                dados_coletados += f"- {gap}: {resposta}...\n"
        dados_coletados += "\n"
    
    if seo_respostas:
        dados_coletados += f"**KEYWORDS SEO COLETADAS ({len(seo_respostas)}):**\n"
        for kw, resp in list(seo_respostas.items())[:5]:  # Top 5
            dados_coletados += f"- {kw}\n"
        dados_coletados += "\n"
    
    if historico_coleta:
        dados_coletados += f"**DADOS DO DEEP DIVE ({len(historico_coleta)} respostas):**\n"
        for i, qa in enumerate(historico_coleta[:3], 1):  # Top 3
            dados_coletados += f"{i}. {qa['resposta'][:100]}...\n"
        dados_coletados += "\n"
    
    total_exp = st.session_state.get('total_experiencias', 3)
    
    # Truncate CV text intelligently - try to preserve complete sections
    cv_para_prompt = cv_texto
    if len(cv_texto) > MAX_CV_LENGTH_FOR_PROMPT:
        # Try to find a good breaking point (end of line) near the limit
        truncate_at = cv_texto.rfind('\n', 0, MAX_CV_LENGTH_FOR_PROMPT)
        if truncate_at < MAX_CV_LENGTH_FOR_PROMPT * 0.8:  # If break point is too early, use hard limit
            truncate_at = MAX_CV_LENGTH_FOR_PROMPT
        cv_para_prompt = cv_texto[:truncate_at]
        logger.info(f"CV truncated from {len(cv_texto)} to {truncate_at} characters for prompt")
    
    # Prompt COMPACTO e DATA-DRIVEN (não template)
    return f"""✍️ **REESCRITA - EXPERIÊNCIA #{experiencia_num} de {total_exp}**

**CARGO-ALVO:** {cargo}

---

**INSTRUÇÕES INTERNAS (não mostrar ao usuário):**

{cv_contexto}

{dados_coletados}

Com base no CV completo abaixo e nos dados coletados acima:

```
{cv_para_prompt}
[CV {'truncado' if len(cv_texto) > MAX_CV_LENGTH_FOR_PROMPT else 'completo'} para economia de tokens]
```

**TAREFA:**

1. Identifique a **experiência profissional #{experiencia_num}** (mais recente = #1, segunda mais recente = #2, etc.)
2. Reescreva essa experiência para o cargo-alvo de **{cargo}** usando os dados coletados
3. Aplique método STAR (Situação, Tarefa, Ação, Resultado)
4. Adicione métricas quantificáveis dos dados coletados
5. Mantenha formato profissional e conciso

**IMPORTANTE:**
- Use APENAS informações do CV e dados coletados (NUNCA invente)
- Se não há dados suficientes, mantenha descrição original mas otimize verbos e estrutura
- Destaque keywords ATS relevantes
- Máximo 4-5 bullets por experiência

---

**FORMATO DA RESPOSTA (mostrar ao usuário):**

### 🟢 EXPERIÊNCIA #{experiencia_num} OTIMIZADA

**[Cargo]** | [Empresa]
_[Período]_

• [Conquista 1 com métrica quantificada]
• [Conquista 2 com métrica quantificada]
• [Conquista 3 com impacto no negócio]
• [Conquista 4 com keywords ATS]

---

✨ **Principais melhorias aplicadas:**
- Adicionadas métricas quantificáveis
- Fortalecidos verbos de ação
- Incluídas keywords para {cargo}
- Aplicado método STAR

---

⏸️ **Revise a experiência acima.**

✅ **Se aprovar**, responda **"PRÓXIMA"** para continuar.
✏️ **Se quiser editar**, indique o que mudar.
"""


def prompt_etapa2_reescrita_final():
    """
    Gera prompt final após reescrever todas as experiências.
    
    Returns:
        str: Prompt de conclusão da etapa 2
    """
    return """🎉 **ETAPA 2: REESCRITA COMPLETA!**

---

### ✅ TODAS AS EXPERIÊNCIAS FORAM OTIMIZADAS

Você já revisou e aprovou todas as experiências reescritas.

---

### 📄 PRÓXIMO PASSO: CHECKPOINT 2 - REVIEW FINAL

No próximo checkpoint, você verá:

1. **CV completo otimizado** - Todas as seções juntas
2. **Resumo de melhorias** - O que foi mudado no geral
3. **Oportunidade de ajustes finais** - Edições globais antes de finalizar

---

⏸️ **Responda "CONTINUAR" para ir para o Checkpoint 2 (Review Final).**
"""
