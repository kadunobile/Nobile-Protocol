"""
Módulo para cache e resumo de CV - redução de tokens em chamadas GPT.

Este módulo fornece funções para gerar e cachear um resumo curto do CV
que pode ser usado em prompts subsequentes, reduzindo significativamente
o número de tokens enviados para a API do GPT.

HEADHUNTER ELITE: Cache inteligente de CV para economia de tokens.
"""

import logging
import streamlit as st
from typing import Optional
from core.utils import chamar_gpt

logger = logging.getLogger(__name__)

# Tamanho máximo do resumo em tokens (aproximado)
MAX_RESUMO_TOKENS = 500  # ~375 palavras


def gerar_resumo_cv(client, cv_texto: str, cargo_alvo: str = "") -> Optional[str]:
    """
    Gera um resumo conciso do CV para uso em prompts subsequentes.
    
    O resumo inclui:
    - Perfil profissional (senioridade, área)
    - Experiências principais (empresas, cargos, períodos)
    - Competências chave
    - Formação acadêmica
    
    Args:
        client: Cliente OpenAI
        cv_texto: Texto completo do CV
        cargo_alvo: Cargo alvo do candidato (opcional)
        
    Returns:
        Resumo do CV (máx ~500 tokens) ou None em caso de erro
    """
    logger.info("Gerando resumo do CV para cache")
    
    if not cv_texto or not cv_texto.strip():
        logger.warning("CV vazio fornecido para resumo")
        return None
    
    cargo_contexto = f" para o cargo-alvo de {cargo_alvo}" if cargo_alvo else ""
    
    prompt = f"""Analise o CV abaixo e crie um RESUMO ULTRA-CONCISO{cargo_contexto}.

O resumo DEVE ter no máximo 400 palavras e incluir:

1. **PERFIL**: Senioridade + área profissional (1 linha)
2. **EXPERIÊNCIAS**: Top 3 experiências (empresa, cargo, período, 1-2 conquistas cada)
3. **COMPETÊNCIAS**: 5-8 skills mais relevantes
4. **FORMAÇÃO**: Graduação/pós (se houver)

**IMPORTANTE:**
- Seja EXTREMAMENTE conciso
- Foque em dados quantificáveis e ferramentas específicas
- Não invente informações
- Use bullet points

---

**CV COMPLETO:**

{cv_texto[:10000]}

---

**RESUMO CONCISO:**"""
    
    # NOTA: Enviamos até 10.000 caracteres do CV (~2500 tokens de input) para
    # gerar um resumo de ~500 tokens (400 palavras). O GPT-4 precisa ver contexto
    # suficiente para criar um resumo representativo, mas não precisamos do CV completo.
    
    try:
        msgs = [{"role": "user", "content": prompt}]
        resumo = chamar_gpt(
            client,
            msgs,
            temperature=0.3,
            seed=42,
            timeout=45
        )
        
        if resumo:
            logger.info(f"Resumo gerado com sucesso ({len(resumo)} caracteres)")
            return resumo
        else:
            logger.warning("Falha ao gerar resumo do CV")
            return None
            
    except Exception as e:
        logger.error(f"Erro ao gerar resumo do CV: {e}", exc_info=True)
        return None


def obter_resumo_cv_cached(client, force_regenerate: bool = False) -> Optional[str]:
    """
    Obtém o resumo do CV do cache ou gera um novo se necessário.
    
    Args:
        client: Cliente OpenAI
        force_regenerate: Se True, força regeneração do resumo mesmo se existir cache
        
    Returns:
        Resumo do CV ou None se falhar
    """
    # Verificar se já temos o resumo em cache
    if not force_regenerate and 'cv_resumo_cache' in st.session_state:
        logger.debug("Usando resumo do CV do cache")
        return st.session_state.cv_resumo_cache
    
    # Obter CV e cargo do session state
    cv_texto = st.session_state.get('cv_texto', '')
    perfil = st.session_state.get('perfil', {})
    cargo_alvo = perfil.get('cargo_alvo', '')
    
    if not cv_texto or not cv_texto.strip():
        logger.warning("CV não encontrado no session state")
        return None
    
    # Gerar novo resumo
    logger.info("Gerando novo resumo do CV")
    resumo = gerar_resumo_cv(client, cv_texto, cargo_alvo)
    
    if resumo:
        # Cachear o resumo
        st.session_state.cv_resumo_cache = resumo
        logger.info("Resumo do CV cacheado com sucesso")
    
    return resumo


def get_cv_contexto_para_prompt() -> str:
    """
    Retorna o contexto do CV para uso em prompts.
    
    Prioriza o resumo cacheado se disponível, caso contrário usa
    uma versão truncada do CV completo.
    
    Returns:
        Texto do CV (resumo ou truncado) formatado para inclusão em prompt
    """
    # Tentar usar o resumo cacheado primeiro
    if 'cv_resumo_cache' in st.session_state:
        resumo = st.session_state.cv_resumo_cache
        if resumo and resumo.strip():
            return f"""**CV DO CANDIDATO (Resumo):**

{resumo}

---"""
    
    # Fallback: usar CV completo truncado
    cv_texto = st.session_state.get('cv_texto', '')
    if cv_texto and cv_texto.strip():
        # Truncar para ~3000 caracteres (aproximadamente 750 tokens)
        cv_truncado = cv_texto[:3000]
        if len(cv_texto) > 3000:
            cv_truncado += "\n\n[... CV truncado para economia de tokens ...]"
        
        return f"""**CV DO CANDIDATO:**

{cv_truncado}

---"""
    
    # Se não houver CV, retornar string vazia
    return ""


def invalidar_cache_cv():
    """
    Invalida o cache do resumo do CV.
    
    Deve ser chamado quando o CV é modificado ou reupload é feito.
    """
    if 'cv_resumo_cache' in st.session_state:
        del st.session_state.cv_resumo_cache
        logger.info("Cache do resumo do CV invalidado")


def inicializar_cache_cv_async(client):
    """
    Inicializa o cache do CV de forma assíncrona (em background).
    
    Esta função pode ser chamada logo após o upload do CV para
    pré-gerar o resumo e cachear, melhorando a experiência do usuário.
    
    Args:
        client: Cliente OpenAI
    """
    if 'cv_resumo_cache' not in st.session_state:
        logger.info("Inicializando cache do CV em background")
        obter_resumo_cv_cached(client, force_regenerate=True)
