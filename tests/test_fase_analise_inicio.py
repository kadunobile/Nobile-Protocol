"""
Testes unitários para a fase de análise início do Protocolo Nóbile.
"""

import pytest
from unittest.mock import Mock, patch


class TestFaseAnaliseInicio:
    """Testes para a fase de transição antes do chat de otimização."""
    
    @patch('ui.screens.fase_analise_inicio.st')
    @patch('ui.screens.fase_analise_inicio.forcar_topo')
    def test_fase_analise_inicio_renders_correctly(self, mock_forcar_topo, mock_st):
        """Testa que a tela de análise início renderiza corretamente."""
        from ui.screens.fase_analise_inicio import fase_analise_inicio
        
        # Mock session state
        mock_st.session_state = Mock()
        mock_st.button = Mock(return_value=False)
        mock_st.columns = Mock(return_value=[Mock(), Mock(), Mock()])
        mock_st.markdown = Mock()
        mock_st.info = Mock()
        
        # Executar
        fase_analise_inicio()
        
        # Verificar que forcar_topo foi chamado
        assert mock_forcar_topo.called
        
        # Verificar que a página foi renderizada
        assert mock_st.markdown.called
        assert mock_st.info.called
    
    @patch('ui.screens.fase_analise_inicio.st')
    @patch('ui.screens.fase_analise_inicio.forcar_topo')
    def test_fase_analise_inicio_button_transitions_to_chat(self, mock_forcar_topo, mock_st):
        """Testa que o botão 'Abrir chat' transiciona para a fase CHAT."""
        from ui.screens.fase_analise_inicio import fase_analise_inicio
        
        # Mock session state
        mock_st.session_state = Mock()
        mock_st.rerun = Mock()
        
        # Mock para simular clique no botão
        def mock_button_side_effect(*args, **kwargs):
            return True
        
        mock_st.button = Mock(side_effect=mock_button_side_effect)
        mock_col = Mock()
        mock_col.__enter__ = Mock(return_value=mock_col)
        mock_col.__exit__ = Mock(return_value=False)
        mock_st.columns = Mock(return_value=[mock_col, mock_col, mock_col])
        mock_st.markdown = Mock()
        mock_st.info = Mock()
        
        # Executar
        fase_analise_inicio()
        
        # Verificar que session state foi atualizado
        assert mock_st.session_state.fase == 'CHAT'
        assert mock_st.session_state.force_scroll_top == True
        
        # Verificar que rerun foi chamado
        assert mock_st.rerun.called
    
    @patch('ui.screens.fase_analise_inicio.st')
    @patch('ui.screens.fase_analise_inicio.forcar_topo')
    def test_fase_analise_inicio_displays_correct_heading(self, mock_forcar_topo, mock_st):
        """Testa que a tela exibe o heading correto."""
        from ui.screens.fase_analise_inicio import fase_analise_inicio
        
        # Mock session state
        mock_st.session_state = Mock()
        mock_st.button = Mock(return_value=False)
        mock_st.columns = Mock(return_value=[Mock(), Mock(), Mock()])
        mock_st.markdown = Mock()
        mock_st.info = Mock()
        
        # Executar
        fase_analise_inicio()
        
        # Verificar que o heading "Aqui começa a análise" foi renderizado
        markdown_calls = [call[0][0] for call in mock_st.markdown.call_args_list]
        heading_found = any("Aqui começa a análise" in call for call in markdown_calls)
        assert heading_found, "O heading 'Aqui começa a análise' não foi encontrado"
