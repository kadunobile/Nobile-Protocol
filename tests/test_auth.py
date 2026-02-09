"""
Testes unitários para o módulo de autenticação.
"""

import pytest
import hashlib
from unittest.mock import MagicMock, patch
import streamlit as st
from core.auth import (
    verificar_login,
    get_api_key,
    is_authenticated,
    logout
)


class TestAuth:
    """Testes para o módulo de autenticação."""
    
    def setup_method(self):
        """Configura o ambiente de teste antes de cada teste."""
        # Limpar session_state
        if hasattr(st, 'session_state'):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
    
    @patch('streamlit.secrets')
    def test_verificar_login_sucesso(self, mock_secrets):
        """Testa login com credenciais válidas."""
        # Criar hash da senha "test123"
        senha_hash = hashlib.sha256("test123".encode()).hexdigest()
        
        mock_secrets.get.return_value = {
            "testuser": {
                "password_hash": senha_hash,
                "display_name": "Test User"
            }
        }
        
        resultado = verificar_login("testuser", "test123")
        assert resultado is True
    
    @patch('streamlit.secrets')
    def test_verificar_login_senha_incorreta(self, mock_secrets):
        """Testa login com senha incorreta."""
        senha_hash = hashlib.sha256("test123".encode()).hexdigest()
        
        mock_secrets.get.return_value = {
            "testuser": {
                "password_hash": senha_hash,
                "display_name": "Test User"
            }
        }
        
        resultado = verificar_login("testuser", "senhaerrada")
        assert resultado is False
    
    @patch('streamlit.secrets')
    def test_verificar_login_usuario_inexistente(self, mock_secrets):
        """Testa login com usuário que não existe."""
        mock_secrets.get.return_value = {
            "testuser": {
                "password_hash": "hash123",
                "display_name": "Test User"
            }
        }
        
        resultado = verificar_login("usuarioinexistente", "qualquersenha")
        assert resultado is False
    
    @patch('streamlit.secrets')
    def test_verificar_login_sem_users_config(self, mock_secrets):
        """Testa login quando não há configuração de usuários."""
        mock_secrets.get.return_value = {}
        
        resultado = verificar_login("qualquerusuario", "qualquersenha")
        assert resultado is False
    
    @patch('streamlit.secrets')
    def test_get_api_key_sucesso(self, mock_secrets):
        """Testa obtenção da API key."""
        mock_secrets.get.return_value = {
            "api_key": "sk-test123"
        }
        
        api_key = get_api_key()
        assert api_key == "sk-test123"
    
    @patch('streamlit.secrets')
    def test_get_api_key_nao_encontrada(self, mock_secrets):
        """Testa quando API key não está configurada."""
        mock_secrets.get.return_value = {}
        
        api_key = get_api_key()
        assert api_key == ""
    
    def test_is_authenticated_true(self):
        """Testa verificação de autenticação quando usuário está logado."""
        st.session_state.authenticated = True
        
        resultado = is_authenticated()
        assert resultado is True
    
    def test_is_authenticated_false(self):
        """Testa verificação de autenticação quando usuário não está logado."""
        st.session_state.authenticated = False
        
        resultado = is_authenticated()
        assert resultado is False
    
    def test_is_authenticated_campo_inexistente(self):
        """Testa verificação quando campo authenticated não existe."""
        # Garantir que não existe
        if 'authenticated' in st.session_state:
            del st.session_state['authenticated']
        
        resultado = is_authenticated()
        assert resultado is False
    
    def test_logout(self):
        """Testa função de logout."""
        # Configurar estado autenticado
        st.session_state.authenticated = True
        st.session_state.user = "testuser"
        
        logout()
        
        assert st.session_state.authenticated is False
        assert st.session_state.user is None
    
    def test_hash_senha_consistency(self):
        """Testa que o hash da mesma senha é sempre o mesmo."""
        senha = "minhasenha123"
        hash1 = hashlib.sha256(senha.encode()).hexdigest()
        hash2 = hashlib.sha256(senha.encode()).hexdigest()
        
        assert hash1 == hash2
    
    def test_hash_senhas_diferentes(self):
        """Testa que senhas diferentes geram hashes diferentes."""
        senha1 = "senha123"
        senha2 = "senha456"
        
        hash1 = hashlib.sha256(senha1.encode()).hexdigest()
        hash2 = hashlib.sha256(senha2.encode()).hexdigest()
        
        assert hash1 != hash2
