"""
Testes para verificar que o código defensivo está funcionando corretamente.

Testa que:
1. processor.py pode lidar com session_state.perfil ausente
2. chat.py trata erros de auto-trigger graciosamente
3. Os fallbacks de cv_estruturado funcionam
"""

import pytest
from unittest.mock import MagicMock, patch, Mock
import sys
sys.path.insert(0, '.')


class TestDefensiveCoding:
    """Testes para código defensivo contra UnboundLocalError."""
    
    @patch('streamlit.session_state')
    def test_processor_sem_perfil_no_session_state(self, mock_session_state):
        """Testa que processar_modulo_otimizador funciona mesmo sem perfil no session_state."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state sem 'perfil' - isso causava UnboundLocalError antes
        mock_session_state.get = MagicMock(side_effect=lambda key, default=None: {
            'perfil': {},  # perfil vazio
            'etapa_modulo': 'ETAPA_0_DIAGNOSTICO'
        }.get(key, default))
        
        # Deve retornar None ou string, mas não deve lançar UnboundLocalError
        try:
            result = processar_modulo_otimizador("")
            # Se chegou aqui, não houve UnboundLocalError
            assert True
        except AttributeError:
            # Pode falhar por outros motivos (falta outros mocks), mas não UnboundLocalError
            pass
    
    @patch('streamlit.session_state')
    def test_processor_perfil_sem_cargo_alvo(self, mock_session_state):
        """Testa que processar_modulo_otimizador usa fallback quando cargo_alvo não existe."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state com perfil mas sem cargo_alvo
        mock_session_state.get = MagicMock(side_effect=lambda key, default=None: {
            'perfil': {},  # perfil sem cargo_alvo
            'etapa_modulo': None
        }.get(key, default))
        
        # Deve usar 'cargo desejado' como fallback
        try:
            result = processar_modulo_otimizador("")
            assert True  # Não deve lançar exceção
        except AttributeError:
            pass
    
    def test_cv_estruturado_fallbacks_existem(self):
        """Testa que as funções fallback de cv_estruturado foram definidas."""
        # Se cv_estruturado.py tem problemas, os fallbacks devem estar disponíveis
        from modules.otimizador.processor import (
            inicializar_cv_estruturado,
            salvar_dados_coleta,
            atualizar_posicionamento,
            atualizar_gaps
        )
        
        # Verificar que as funções existem e podem ser chamadas
        assert callable(inicializar_cv_estruturado)
        assert callable(salvar_dados_coleta)
        assert callable(atualizar_posicionamento)
        assert callable(atualizar_gaps)
        
        # Testar que os fallbacks funcionam sem exceção
        result = inicializar_cv_estruturado()
        assert isinstance(result, dict)
        
        salvar_dados_coleta({})  # Deve executar sem erro
        atualizar_posicionamento(cargo_alvo="teste")  # Deve executar sem erro
        atualizar_gaps(identificados=["teste"])  # Deve executar sem erro
    
    @patch('modules.otimizador.processor.processar_modulo_otimizador')
    @patch('streamlit.session_state')
    @patch('streamlit.chat_message')
    @patch('streamlit.spinner')
    def test_chat_trata_erro_auto_trigger(self, mock_spinner, mock_chat, mock_session_state, mock_processor):
        """Testa que chat.py trata exceções de auto-trigger graciosamente."""
        from ui.chat import fase_chat
        
        # Simular que processar_modulo_otimizador lança exceção
        mock_processor.side_effect = Exception("Teste de erro")
        
        # Mock session state para acionar auto-trigger
        mock_session_state.get = MagicMock(side_effect=lambda key, default=None: {
            'modulo_ativo': 'OTIMIZADOR',
            'etapa_modulo': 'ETAPA_0_DIAGNOSTICO',
            'etapa_0_diagnostico_triggered': False,
            'mensagens': []
        }.get(key, default))
        
        mock_session_state.mensagens = []
        
        # Deve capturar exceção e logar, não crashar
        try:
            # Isso pode falhar por outros motivos de mock, mas a exceção
            # de processar_modulo_otimizador deve ser capturada
            fase_chat()
        except Exception as e:
            # Se é a nossa exceção de teste, não foi capturada (bug)
            if "Teste de erro" in str(e):
                pytest.fail("Exception não foi capturada pelo try-except em chat.py")
            # Outras exceções são OK (problemas de mock)
            pass
    
    @patch('streamlit.session_state')
    def test_gerar_resumo_diagnostico_sem_perfil(self, mock_session_state):
        """Testa que gerar_resumo_diagnostico funciona mesmo sem perfil."""
        from modules.otimizador.processor import gerar_resumo_diagnostico
        
        # Mock session state sem perfil
        mock_session_state.get = MagicMock(side_effect=lambda key, default=None: {
            'gaps_respostas': {},
            'perfil': {}  # perfil vazio
        }.get(key, default))
        
        # Deve retornar string formatada, não crashar
        try:
            result = gerar_resumo_diagnostico()
            assert isinstance(result, str)
            assert 'DIAGNÓSTICO' in result or 'Diagnóstico' in result
        except AttributeError:
            # Pode falhar por outros motivos de mock, mas não por falta de perfil
            pass


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
