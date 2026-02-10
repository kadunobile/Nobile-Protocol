"""
Etapa 0 DINÂMICA: Diagnóstico com geração dinâmica de perguntas sobre gaps.

Esta versão usa geração dinâmica para aprofundar em cada gap identificado,
adaptando as perguntas com base nas respostas do candidato.

HEADHUNTER ELITE: Diagnóstico adaptativo e contextual.
"""

import logging
import streamlit as st
from typing import Optional
from core.cv_cache import get_cv_contexto_para_prompt
from core.dynamic_questions import (
    gerar_proxima_pergunta_dinamica,
    adicionar_qa_historico,
    obter_historico_qa
)

logger = logging.getLogger(__name__)


def gerar_pergunta_dinamica_gap(
    client,
    gap: str,
    gap_index: int,
    total_gaps: int,
    resposta_anterior: Optional[str] = None
) -> Optional[str]:
    """
    Gera uma pergunta dinâmica sobre um gap específico.
    
    Se é a primeira pergunta sobre o gap, pergunta se tem experiência.
    Se já perguntou antes, aprofunda com base na resposta.
    
    Args:
        client: Cliente OpenAI
        gap: Gap a ser explorado
        gap_index: Índice do gap (0-based)
        total_gaps: Total de gaps identificados
        resposta_anterior: Resposta anterior do usuário (se houver)
        
    Returns:
        Pergunta gerada ou None em caso de erro
    """
    logger.info(f"Gerando pergunta dinâmica para gap: {gap}")
    
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    
    # Verificar se já perguntamos sobre este gap antes
    historico = obter_historico_qa('diagnostico')
    perguntas_sobre_gap = [
        qa for qa in historico 
        if gap.lower() in qa['pergunta'].lower()
    ]
    
    # Se é a primeira vez perguntando sobre este gap, usar pergunta padrão
    if not perguntas_sobre_gap:
        return f"""🔍 **DIAGNÓSTICO ESTRATÉGICO** ({gap_index + 1}/{total_gaps})

**CARGO-ALVO:** {cargo}

---

### Gap a Analisar:
**"{gap}"**

---

**Pergunta para você:**

Você tem experiência prática com **{gap}**?

- ✅ Se **SIM**: Por favor, responda em qual empresa/cargo você trabalhou com isso e descreva brevemente o contexto (1-2 frases).
  
  *Exemplo: "Sim, na ARQUIVEI como RevOps Manager eu usava Tableau para criar dashboards de receita recorrente."*

- ❌ Se **NÃO**: Digite "não tenho" ou "não" para pularmos este gap.

💡 **Dica:** Seja específico! Quanto mais detalhes você fornecer agora, melhor será a otimização do seu CV."""
    
    # Se já perguntamos e o usuário tem experiência, aprofundar
    if resposta_anterior and resposta_anterior.strip():
        # Adicionar ao histórico se ainda não foi
        if perguntas_sobre_gap:
            ultima_pergunta = perguntas_sobre_gap[-1]['pergunta']
            adicionar_qa_historico('diagnostico', ultima_pergunta, resposta_anterior)
        
        # Contexto para aprofundamento
        contexto_especifico = f"""Esta é uma pergunta de APROFUNDAMENTO sobre o gap "{gap}".

O candidato JÁ disse que tem experiência com este gap.

**RESPOSTA ANTERIOR DO CANDIDATO:**
{resposta_anterior}

**OBJETIVO:**
Fazer UMA pergunta adicional para aprofundar e coletar mais detalhes sobre este gap:
- Se ele mencionou uma empresa/contexto → pergunte sobre métricas, resultados ou impacto
- Se ele mencionou ferramentas → pergunte sobre volume de uso, frequência ou casos específicos
- Se foi vago → peça um exemplo concreto ou projeto específico

**IMPORTANTE:**
- Seja BREVE e direto (máx 2 linhas)
- Pergunte apenas UMA coisa
- Não exija resposta longa - aceite respostas curtas e objetivas"""
        
        objetivo = f"Aprofundar conhecimento sobre '{gap}' para documentar no CV"
        
        pergunta = gerar_proxima_pergunta_dinamica(
            client=client,
            etapa='diagnostico',
            contexto_especifico=contexto_especifico,
            cargo_alvo=cargo,
            gaps_mapeados=[gap],
            objetivo=objetivo,
            contexto_gpt='diagnostico'
        )
        
        return pergunta
    
    return None


def verificar_resposta_negativa_gap(resposta: str) -> bool:
    """
    Verifica se a resposta indica que o usuário NÃO tem experiência com o gap.
    
    Args:
        resposta: Resposta do usuário
        
    Returns:
        True se é resposta negativa, False caso contrário
    """
    resposta_lower = resposta.lower().strip()
    
    NEGATIVE_KEYWORDS = [
        'não tenho', 'nao tenho',
        'não possuo', 'nao possuo',
        'nunca tive', 'nunca usei',
        'não sei', 'nao sei',
        'não conheço', 'nao conheço',
        'desconheço', 'desconheco',
        'nunca trabalhei', 'nunca utilizei',
        'sem experiência', 'sem experiencia',
        'jamais',
        'não', 'nao'  # Apenas "não" sozinho
    ]
    
    # Resposta muito curta que é negativa
    if len(resposta_lower) < 20:
        return any(kw in resposta_lower for kw in NEGATIVE_KEYWORDS)
    
    # Resposta mais longa - verificar se começa com negativa
    for kw in NEGATIVE_KEYWORDS:
        if resposta_lower.startswith(kw):
            return True
    
    return False


def deve_aprofundar_gap(resposta: str) -> bool:
    """
    Verifica se a resposta indica que o usuário TEM experiência mas foi superficial.
    
    Se a resposta for muito curta (< 50 chars) ou não contiver detalhes (empresa, contexto),
    vale a pena aprofundar com outra pergunta.
    
    Args:
        resposta: Resposta do usuário
        
    Returns:
        True se deve fazer pergunta de aprofundamento, False caso contrário
    """
    # Se é resposta negativa, não aprofundar
    if verificar_resposta_negativa_gap(resposta):
        return False
    
    # Se resposta muito curta, aprofundar
    if len(resposta.strip()) < 50:
        return True
    
    # Se não menciona contexto (empresa, cargo, projeto), aprofundar
    contexto_keywords = [
        'empresa', 'projeto', 'cargo', 'função', 'trabalhei',
        'desenvolvi', 'criei', 'gerenciei', 'liderei'
    ]
    
    tem_contexto = any(kw in resposta.lower() for kw in contexto_keywords)
    
    # Se não tem contexto, vale aprofundar
    return not tem_contexto
