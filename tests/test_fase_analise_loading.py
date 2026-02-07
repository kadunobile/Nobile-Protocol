"""
Testes unitários para a fase de análise loading do Protocolo Nóbile.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import streamlit as st


class TestFaseAnaliseLoading:
    """Testes para a fase de loading da análise de CV."""
    
    @patch('ui.screens.fase_analise_loading.st')
    @patch('ui.screens.fase_analise_loading.chamar_gpt')
    @patch('ui.screens.fase_analise_loading.time.sleep')
    def test_executar_analise_cv_with_consistency_params(self, mock_sleep, mock_chamar_gpt, mock_st):
        """Testa que executar_analise_cv usa parâmetros de consistência."""
        from ui.screens.fase_analise_loading import executar_analise_cv
        
        # Mock session state
        mock_st.session_state.cv_texto = "Test CV content"
        mock_st.session_state.perfil = {'cargo_alvo': 'Desenvolvedor Python'}
        mock_st.session_state.openai_client = Mock()
        
        # Mock resposta
        mock_chamar_gpt.return_value = "Análise completa do CV"
        
        # Executar
        result = executar_analise_cv()
        
        # Verificar que chamar_gpt foi chamado com parâmetros corretos
        assert mock_chamar_gpt.called
        call_kwargs = mock_chamar_gpt.call_args[1]
        assert call_kwargs['temperature'] == 0.3
        assert call_kwargs['seed'] == 42
        assert result == "Análise completa do CV"
    
    @patch('ui.screens.fase_analise_loading.st')
    @patch('ui.screens.fase_analise_loading.chamar_gpt')
    @patch('ui.screens.fase_analise_loading.time.sleep')
    def test_executar_analise_cv_includes_cargo_alvo(self, mock_sleep, mock_chamar_gpt, mock_st):
        """Testa que a análise inclui o cargo alvo nas mensagens."""
        from ui.screens.fase_analise_loading import executar_analise_cv
        
        # Mock session state
        mock_st.session_state.cv_texto = "Test CV"
        mock_st.session_state.perfil = {'cargo_alvo': 'Gerente de Produto'}
        mock_st.session_state.openai_client = Mock()
        
        mock_chamar_gpt.return_value = "Análise"
        
        # Executar
        executar_analise_cv()
        
        # Verificar que as mensagens incluem cargo alvo
        call_args = mock_chamar_gpt.call_args[0]
        messages = call_args[1]
        
        assert len(messages) == 2
        assert "Gerente de Produto" in messages[0]['content']
        assert "Gerente de Produto" in messages[1]['content']
    
    @patch('ui.screens.fase_analise_loading.st')
    @patch('ui.screens.fase_analise_loading.chamar_gpt')
    @patch('ui.screens.fase_analise_loading.time.sleep')
    def test_executar_analise_cv_handles_none_response(self, mock_sleep, mock_chamar_gpt, mock_st):
        """Testa que executar_analise_cv lida com resposta None."""
        from ui.screens.fase_analise_loading import executar_analise_cv
        
        # Mock session state
        mock_st.session_state.cv_texto = "Test CV"
        mock_st.session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_st.session_state.openai_client = Mock()
        
        # Mock resposta None (erro)
        mock_chamar_gpt.return_value = None
        
        # Executar
        result = executar_analise_cv()
        
        # Verificar que retorna None
        assert result is None
    
    @patch('ui.screens.fase_analise_loading.st')
    @patch('ui.screens.fase_analise_loading.chamar_gpt')
    @patch('ui.screens.fase_analise_loading.scroll_topo')
    @patch('ui.screens.fase_analise_loading.time.sleep')
    @patch('ui.screens.fase_analise_loading.executar_analise_cv')
    def test_fase_analise_loading_success_flow(self, mock_executar, mock_sleep, mock_scroll, mock_chamar_gpt, mock_st):
        """Testa o fluxo de sucesso da fase de loading."""
        from ui.screens.fase_analise_loading import fase_analise_loading
        
        # Mock session state
        mock_st.session_state.cv_texto = "Test CV"
        mock_st.session_state.perfil = {'cargo_alvo': 'Desenvolvedor'}
        mock_st.session_state.openai_client = Mock()
        mock_st.rerun = Mock()
        
        # Mock análise bem-sucedida
        mock_executar.return_value = "Análise completa"
        
        # Executar
        fase_analise_loading()
        
        # Verificar que análise foi executada
        assert mock_executar.called
        
        # Verificar que session state foi configurado
        assert mock_st.session_state.analise_cv_completa == "Análise completa"
        assert mock_st.session_state.modulo_ativo == "OTIMIZADOR"
        assert mock_st.session_state.etapa_modulo == "AGUARDANDO_OK"
        assert mock_st.session_state.force_scroll_top == True
        assert mock_st.session_state.fase == 'CHAT'
        
        # Verificar que rerun foi chamado
        assert mock_st.rerun.called
    
    @patch('ui.screens.fase_analise_loading.st')
    @patch('ui.screens.fase_analise_loading.chamar_gpt')
    @patch('ui.screens.fase_analise_loading.scroll_topo')
    @patch('ui.screens.fase_analise_loading.time.sleep')
    @patch('ui.screens.fase_analise_loading.executar_analise_cv')
    def test_fase_analise_loading_error_flow(self, mock_executar, mock_sleep, mock_scroll, mock_chamar_gpt, mock_st):
        """Testa o fluxo de erro da fase de loading."""
        from ui.screens.fase_analise_loading import fase_analise_loading
        
        # Mock session state
        mock_st.session_state.cv_texto = "Test CV"
        mock_st.session_state.perfil = {'cargo_alvo': 'Desenvolvedor'}
        mock_st.session_state.openai_client = Mock()
        mock_st.rerun = Mock()
        mock_st.error = Mock()
        
        # Mock análise falhou
        mock_executar.return_value = None
        
        # Executar
        fase_analise_loading()
        
        # Verificar que erro foi exibido
        assert mock_st.error.called
        error_message = mock_st.error.call_args[0][0]
        assert "Erro ao analisar CV" in error_message
        
        # Verificar que rerun NÃO foi chamado
        assert not mock_st.rerun.called
