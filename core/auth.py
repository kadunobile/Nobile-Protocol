"""
Sistema de Autenticação para o Protocolo Nóbile.

Gerencia login/logout de usuários usando credenciais armazenadas
no arquivo .streamlit/secrets.toml.
"""

import streamlit as st
import hashlib
import logging

logger = logging.getLogger(__name__)


def verificar_login(usuario: str, senha: str) -> bool:
    """
    Verifica credenciais contra st.secrets.
    
    Args:
        usuario: Nome de usuário
        senha: Senha em texto plano
        
    Returns:
        True se credenciais válidas, False caso contrário
    """
    try:
        users = st.secrets.get("users", {})
        if usuario in users:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            stored_hash = users[usuario].get("password_hash", "")
            is_valid = stored_hash == senha_hash
            
            if is_valid:
                logger.info(f"Login bem-sucedido para usuário: {usuario}")
            else:
                logger.warning(f"Tentativa de login falhou para usuário: {usuario}")
            
            return is_valid
        
        logger.warning(f"Usuário não encontrado: {usuario}")
        return False
        
    except Exception as e:
        logger.error(f"Erro ao verificar login: {e}", exc_info=True)
        return False


def get_api_key() -> str:
    """
    Retorna a API key do OpenAI armazenada em secrets.
    
    Returns:
        API key ou string vazia se não encontrada
    """
    try:
        return st.secrets.get("openai", {}).get("api_key", "")
    except Exception as e:
        logger.error(f"Erro ao obter API key: {e}")
        return ""


def is_authenticated() -> bool:
    """
    Verifica se o usuário está autenticado.
    
    Returns:
        True se autenticado, False caso contrário
    """
    return st.session_state.get("authenticated", False)


def logout():
    """Remove autenticação do usuário."""
    st.session_state.authenticated = False
    st.session_state.user = None
    logger.info("Usuário deslogado")


def render_login_page():
    """
    Renderiza a página de login.
    
    Esta função exibe um formulário de login centralizado e
    processa as credenciais quando submetido.
    """
    st.markdown("# 🎯 Protocolo Nóbile")
    st.markdown("### Acesse sua conta")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            usuario = st.text_input("👤 Usuário")
            senha = st.text_input("🔒 Senha", type="password")
            submitted = st.form_submit_button("Entrar", use_container_width=True, type="primary")
            
            if submitted:
                if not usuario or not senha:
                    st.error("❌ Por favor, preencha todos os campos")
                elif verificar_login(usuario, senha):
                    st.session_state.authenticated = True
                    st.session_state.user = usuario
                    st.success("✅ Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Usuário ou senha incorretos")
    
    st.markdown("---")
    st.caption("Não tem conta? Entre em contato com o administrador.")
