"""
Etapa 1 DINÂMICA: Coleta Focada com geração dinâmica de perguntas.

Esta versão usa geração dinâmica de perguntas via GPT com base no contexto
acumulado (CV, gaps, respostas anteriores), implementando anti-loop e
stop conditions inteligentes.

HEADHUNTER ELITE: Deep dive contextual com inteligência adaptativa.
"""

import logging
import streamlit as st
from typing import Optional
from core.cv_cache import get_cv_contexto_para_prompt
from core.dynamic_questions import (
    gerar_proxima_pergunta_dinamica,
    adicionar_qa_historico,
    obter_historico_qa,
    verificar_stop_condition_experiencia,
    detectar_resposta_evasiva
)

logger = logging.getLogger(__name__)


def prompt_etapa1_coleta_dinamica_inicial() -> str:
    """
    Gera o prompt inicial da coleta focada que será processado pelo GPT
    para gerar a primeira pergunta dinâmica.
    
    Returns:
        Prompt inicial formatado
    """
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    gaps_respostas = st.session_state.get('gaps_respostas', {})
    
    # Preparar contexto dos gaps com experiência
    gaps_com_experiencia = [
        gap for gap, info in gaps_respostas.items() 
        if info.get('tem_experiencia')
    ]
    
    cv_contexto = get_cv_contexto_para_prompt()
    
    gaps_texto = ""
    if gaps_com_experiencia:
        gaps_texto = "\n".join([f"- {gap}" for gap in gaps_com_experiencia])
    
    return f"""📝 **ETAPA 1: DEEP DIVE - COLETA FOCADA**

**CARGO-ALVO:** {cargo}

{cv_contexto}

---

### 🎯 GAPS QUE VOCÊ TEM EXPERIÊNCIA:

{gaps_texto if gaps_texto else "*(Nenhum gap mapeado)*"}

---

### 📋 COMO FUNCIONA O DEEP DIVE:

Agora vou fazer perguntas **CIRÚRGICAS e ESPECÍFICAS** sobre suas experiências profissionais.

**FOCO em coletar:**
1. 📊 **Métricas e resultados quantificáveis** (%, R$, volume, impacto)
2. 🛠️ **Ferramentas e tecnologias específicas** (sistemas, linguagens, plataformas)
3. 👥 **Escala e contexto** (tamanho de equipe, stakeholders, orçamento)
4. 🎯 **Entregas e projetos** (conquistas, milestones, otimizações)

**IMPORTANTE:**
- As perguntas serão **adaptadas ao seu perfil** e às suas respostas
- Não vou repetir perguntas sobre temas já cobertos
- Você pode ser específico e detalhado - quanto mais dados, melhor!
- Se não souber alguma informação, pode dizer "não sei" ou "não lembro"

---

**Vamos começar com a primeira experiência relevante do seu CV...**

Qual foi a sua **experiência profissional mais recente ou mais relevante** para o cargo de **{cargo}**?

Por favor, me diga:
- **Empresa**
- **Cargo**
- **Período** (mês/ano início - fim)
- **Breve descrição** do que você fazia (2-3 linhas)"""


def gerar_proxima_pergunta_coleta(
    client,
    ultima_resposta: Optional[str] = None
) -> Optional[str]:
    """
    Gera a próxima pergunta da coleta focada de forma dinâmica.
    
    Args:
        client: Cliente OpenAI
        ultima_resposta: Última resposta do usuário (para adicionar ao histórico)
        
    Returns:
        Próxima pergunta gerada ou None se stop condition atingida
    """
    logger.info("Gerando próxima pergunta dinâmica da coleta focada")
    
    # Se há uma resposta, adicionar ao histórico
    if ultima_resposta:
        # A última pergunta está nas mensagens
        mensagens = st.session_state.get('mensagens', [])
        ultima_pergunta = ""
        
        # Buscar a última mensagem do assistente (a pergunta)
        for msg in reversed(mensagens):
            if msg.get('role') == 'assistant' and not msg.get('internal'):
                ultima_pergunta = msg.get('content', '')
                break
        
        if ultima_pergunta:
            adicionar_qa_historico('coleta', ultima_pergunta, ultima_resposta)
    
    # Obter histórico de Q&A
    historico = obter_historico_qa('coleta')
    
    # Verificar stop condition (mínimo 5 perguntas, cobertura de métricas/ferramentas/volume)
    if verificar_stop_condition_experiencia(historico, min_perguntas=5):
        logger.info("Stop condition atingida para coleta focada")
        return None  # Sinaliza que deve avançar
    
    # Verificar se resposta foi evasiva e precisamos de mais informação
    resposta_evasiva = False
    if ultima_resposta:
        resposta_evasiva = detectar_resposta_evasiva(ultima_resposta)
        if resposta_evasiva:
            logger.debug("Resposta evasiva detectada - perguntar de forma diferente")
    
    # Preparar contexto específico para geração da pergunta
    cargo = st.session_state.perfil.get('cargo_alvo', 'cargo desejado')
    gaps_respostas = st.session_state.get('gaps_respostas', {})
    gaps_com_experiencia = [
        gap for gap, info in gaps_respostas.items() 
        if info.get('tem_experiencia')
    ]
    
    contexto_especifico = f"""Esta é a etapa de COLETA FOCADA (Deep Dive).

Você já fez **{len(historico)} pergunta(s)** sobre as experiências do candidato.

**GAPS A EXPLORAR:**
{chr(10).join([f'- {gap}' for gap in gaps_com_experiencia])}

**O QUE AINDA FALTA COLETAR:**
Analise o histórico de perguntas/respostas e identifique o que AINDA NÃO foi coberto:
- Se faltam MÉTRICAS/RESULTADOS → pergunte sobre números, %, impacto, ROI
- Se faltam FERRAMENTAS/STACK → pergunte sobre tecnologias, sistemas, plataformas específicas
- Se faltam VOLUME/ESCALA → pergunte sobre tamanho de equipe, número de projetos, stakeholders
- Se faltam ENTREGAS → pergunte sobre projetos específicos, conquistas, otimizações

**FORMATO DA PERGUNTA:**
- Seja ESPECÍFICO ao cargo-alvo ({cargo})
- Seja DIRETO e objetivo
- Pergunte UMA coisa por vez
- Use dados do CV quando relevante
- NÃO repita temas já cobertos no histórico"""

    if resposta_evasiva:
        contexto_especifico += "\n\n**ATENÇÃO:** O candidato deu uma resposta vaga. Reformule a pergunta de forma mais específica ou passe para outro tópico."
    
    objetivo = "Coletar dados concretos (métricas, ferramentas, volume) para otimização do CV"
    
    # Gerar próxima pergunta
    pergunta = gerar_proxima_pergunta_dinamica(
        client=client,
        etapa='coleta',
        contexto_especifico=contexto_especifico,
        cargo_alvo=cargo,
        gaps_mapeados=gaps_com_experiencia,
        objetivo=objetivo,
        contexto_gpt='coleta_focada'
    )
    
    return pergunta


def verificar_pronto_para_avancar_coleta() -> bool:
    """
    Verifica se a coleta focada está pronta para avançar para a próxima etapa.
    
    Returns:
        True se pode avançar, False caso contrário
    """
    historico = obter_historico_qa('coleta')
    
    # Mínimo de 5 perguntas respondidas
    if len(historico) < 5:
        return False
    
    # Verificar stop condition
    return verificar_stop_condition_experiencia(historico, min_perguntas=5)


def gerar_mensagem_transicao_coleta() -> str:
    """
    Gera mensagem de transição ao finalizar a coleta focada.
    
    Returns:
        Mensagem formatada de transição
    """
    total_perguntas = len(obter_historico_qa('coleta'))
    pergunta_texto = "pergunta" if total_perguntas == 1 else "perguntas"
    
    return f"""✅ **COLETA FOCADA CONCLUÍDA!**

Coletei **{total_perguntas} {pergunta_texto} importantes** sobre suas experiências.

---

### 📊 RESUMO DO QUE FOI COLETADO:

Agora tenho dados detalhados sobre:
- ✅ Métricas e resultados quantificáveis
- ✅ Ferramentas e tecnologias específicas
- ✅ Escala e contexto das suas experiências
- ✅ Entregas e projetos relevantes

---

### 🎯 PRÓXIMO PASSO: VALIDAÇÃO

Vou compilar tudo que você me contou e mostrar um resumo para validação antes de começar a reescrever seu CV.

**Digite "continuar" quando estiver pronto para prosseguir.**"""
