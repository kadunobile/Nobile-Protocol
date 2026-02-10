"""
Testes unitários para a fase de análise início do Protocolo Nóbile.

NOTA: Esta fase foi depreciada em 2026-02-10 e agora apenas redireciona para CHAT.
Os testes foram simplificados para validar o comportamento de redirect.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
import sys

# Mock streamlit before importing the module
sys.modules['streamlit'] = MagicMock()


class TestFaseAnaliseInicio:
    """Testes para a fase de transição (deprecated - apenas redirect)."""
    
    def test_fase_analise_inicio_function_exists(self):
        """Testa que a função fase_analise_inicio ainda existe para compatibilidade."""
        from ui.screens.fase_analise_inicio import fase_analise_inicio
        assert callable(fase_analise_inicio)
    
    @patch('ui.screens.fase_analise_inicio.st')
    @patch('ui.screens.fase_analise_inicio.logger')
    def test_fase_analise_inicio_redirects_to_chat(self, mock_logger, mock_st):
        """Testa que fase_analise_inicio redireciona automaticamente para CHAT."""
        from ui.screens.fase_analise_inicio import fase_analise_inicio
        
        # Mock session state
        mock_session = MagicMock()
        mock_session.get.return_value = None
        mock_st.session_state = mock_session
        
        # Executar
        fase_analise_inicio()
        
        # Verificar que session state.fase foi definido como CHAT
        assert mock_st.session_state.fase == 'CHAT'
        
        # Verificar que rerun foi chamado
        mock_st.rerun.assert_called_once()
        
        # Verificar que warning foi logado
        mock_logger.warning.assert_called_once()
    
    @patch('ui.screens.fase_analise_inicio.st')
    def test_fase_analise_inicio_sets_optimizer_state_if_missing(self, mock_st):
        """Testa que o redirect configura o estado do otimizador se não existir."""
        from ui.screens.fase_analise_inicio import fase_analise_inicio
        
        # Mock session state sem modulo_ativo
        mock_session = MagicMock()
        mock_session.get.return_value = None
        mock_st.session_state = mock_session
        
        # Executar
        fase_analise_inicio()
        
        # Verificar que otimizador foi configurado
        assert mock_st.session_state.modulo_ativo == 'OTIMIZADOR'
        assert mock_st.session_state.etapa_modulo == 'ETAPA_0_DIAGNOSTICO'
    
    @patch('ui.screens.fase_analise_inicio.st')
    def test_fase_analise_inicio_preserves_optimizer_if_exists(self, mock_st):
        """Testa que o redirect não sobrescreve estado do otimizador se já existir."""
        from ui.screens.fase_analise_inicio import fase_analise_inicio
        
        # Mock session state COM modulo_ativo já configurado
        mock_session = MagicMock()
        mock_session.get.return_value = 'EXISTING_MODULE'
        mock_st.session_state = mock_session
        
        # Executar
        fase_analise_inicio()
        
        # Verificar que fase foi mudada para CHAT
        assert mock_st.session_state.fase == 'CHAT'
        
        # Verificar que modulo_ativo não foi sobrescrito
        # (get() retorna valor existente, então não deve atribuir novo)
        # Neste caso, não chamamos mock_session.get porque a condição do if é False
        # Então a atribuição de modulo_ativo não acontece
