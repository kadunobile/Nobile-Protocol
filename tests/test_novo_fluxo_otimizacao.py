"""
Testes para o novo fluxo de otimização CV + LinkedIn.

Testa os novos módulos de diagnóstico, coleta focada, validação,
reescrita progressiva e otimização de LinkedIn.
"""

import pytest
from unittest.mock import MagicMock, patch
import sys
sys.path.insert(0, '.')


class TestNovoFluxoOtimizacao:
    """Testes para o novo fluxo de otimização."""
    
    @patch('streamlit.session_state')
    def test_etapa0_diagnostico_gera_prompt(self, mock_session_state):
        """Testa se etapa0 gera prompt de diagnóstico corretamente."""
        from modules.otimizador.etapa0_diagnostico import prompt_etapa0_diagnostico
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Gerente de Vendas'}
        mock_session_state.cv_texto = 'CV de teste com experiência em vendas'
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.gaps_alvo = ['Falta métrica de vendas', 'Falta gestão de equipe']
        
        result = prompt_etapa0_diagnostico()
        
        assert result is not None
        assert 'DIAGNÓSTICO' in result.upper()
        assert 'Gerente de Vendas' in result
        assert 'gaps' in result.lower()
    
    @patch('streamlit.session_state')
    def test_etapa1_coleta_focada_gera_prompt(self, mock_session_state):
        """Testa se etapa1 coleta focada gera prompt corretamente."""
        from modules.otimizador.etapa1_coleta_focada import prompt_etapa1_coleta_focada
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista de Dados'}
        mock_session_state.cv_texto = 'CV com experiência em análise'
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        result = prompt_etapa1_coleta_focada()
        
        assert result is not None
        assert 'COLETA FOCADA' in result.upper()
        assert 'Analista de Dados' in result
        assert '3 perguntas' in result.lower() or 'pergunta' in result.lower()
    
    @patch('streamlit.session_state')
    def test_checkpoint_validacao_gera_prompt(self, mock_session_state):
        """Testa se checkpoint de validação gera prompt corretamente."""
        from modules.otimizador.checkpoint_validacao import prompt_checkpoint_validacao
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Product Manager'}
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        result = prompt_checkpoint_validacao()
        
        assert result is not None
        assert 'CHECKPOINT' in result.upper() or 'VALIDAÇÃO' in result.upper()
        assert 'Product Manager' in result
        assert 'mapeamento' in result.lower() or 'gap' in result.lower()
    
    @patch('streamlit.session_state')
    def test_etapa2_reescrita_progressiva_gera_prompt(self, mock_session_state):
        """Testa se etapa2 reescrita progressiva gera prompt corretamente."""
        from modules.otimizador.etapa2_reescrita_progressiva import prompt_etapa2_reescrita_progressiva
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Designer UX'}
        mock_session_state.cv_texto = 'CV com experiência em design'
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        result = prompt_etapa2_reescrita_progressiva(1)
        
        assert result is not None
        assert 'REESCRITA' in result.upper()
        assert 'EXPERIÊNCIA #1' in result.upper()
        assert 'Designer UX' in result
    
    @patch('streamlit.session_state')
    def test_etapa6_otimizacao_linkedin_gera_prompt(self, mock_session_state):
        """Testa se etapa6 LinkedIn gera prompt corretamente."""
        from modules.otimizador.etapa6_otimizacao_linkedin import prompt_etapa6_otimizacao_linkedin
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Engenheiro de Software'}
        mock_session_state.cv_otimizado = 'CV otimizado'
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        result = prompt_etapa6_otimizacao_linkedin()
        
        assert result is not None
        assert 'LINKEDIN' in result.upper()
        assert 'HEADLINE' in result.upper()
        assert 'Engenheiro de Software' in result
        assert 'A/B/C' in result or 'opção' in result.lower()


class TestHelpersExport:
    """Testes para helpers de exportação."""
    
    def test_gerar_txt_basico(self):
        """Testa geração de TXT básico."""
        from modules.otimizador.helpers_export import gerar_txt
        
        cv_texto = "Este é um CV de teste\nCom múltiplas linhas"
        result = gerar_txt(cv_texto)
        
        assert result is not None
        assert isinstance(result, bytes)
        assert b"Este" in result
    
    def test_gerar_analytics_data(self):
        """Testa geração de dados de analytics."""
        from modules.otimizador.helpers_export import gerar_analytics_data
        
        score_inicial = {
            'score_total': 60.0,
            'detalhes': {
                'keywords': {'encontradas': 5},
                'metricas': {'quantidade': 3}
            }
        }
        
        score_final = {
            'score_total': 82.0,
            'detalhes': {
                'keywords': {'encontradas': 9},
                'metricas': {'quantidade': 8}
            },
            'nivel': 'Excelente'
        }
        
        gaps_alvo = ['Gap 1', 'Gap 2', 'Gap 3']
        
        analytics = gerar_analytics_data(score_inicial, score_final, gaps_alvo)
        
        assert analytics is not None
        assert analytics['score_melhoria'] == 22.0
        assert analytics['keywords_adicionadas'] == 4
        assert analytics['metricas_adicionadas'] == 5
        assert analytics['gaps_resolvidos'] == 3
        assert analytics['atingiu_meta'] is True
    
    def test_formatar_comparacao_antes_depois(self):
        """Testa formatação de comparação antes/depois."""
        from modules.otimizador.helpers_export import formatar_comparacao_antes_depois
        
        score_inicial = {
            'score_total': 50.0,
            'nivel': 'Regular',
            'detalhes': {
                'secoes': {'encontradas': 3, 'total': 4},
                'keywords': {'encontradas': 4, 'total': 10},
                'metricas': {'quantidade': 2},
                'formatacao': {'bullets': 5, 'datas': 3},
                'tamanho': {'palavras': 300}
            }
        }
        
        score_final = {
            'score_total': 78.0,
            'nivel': 'Bom',
            'detalhes': {
                'secoes': {'encontradas': 4, 'total': 4},
                'keywords': {'encontradas': 8, 'total': 10},
                'metricas': {'quantidade': 10},
                'formatacao': {'bullets': 8, 'datas': 5},
                'tamanho': {'palavras': 450}
            }
        }
        
        comparacao = formatar_comparacao_antes_depois(score_inicial, score_final)
        
        assert comparacao is not None
        assert 'ANTES' in comparacao
        assert 'DEPOIS' in comparacao
        assert '50.0' in comparacao
        assert '78.0' in comparacao
        assert 'Regular' in comparacao
        assert 'Bom' in comparacao


class TestProcessorNovoFluxo:
    """Testes para o processador com novo fluxo."""
    
    @patch('streamlit.session_state')
    def test_processor_etapa0_diagnostico(self, mock_session_state):
        """Testa transição para ETAPA_0_DIAGNOSTICO."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Gerente'}
        mock_session_state.cv_texto = 'CV teste'
        mock_session_state.gaps_alvo = []
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO'
        
        result = processar_modulo_otimizador("")
        
        assert result is not None
        assert 'DIAGNÓSTICO' in result.upper()
    
    @patch('streamlit.session_state')
    def test_processor_aguardando_ok_diagnostico(self, mock_session_state):
        """Testa transição de AGUARDANDO_OK_DIAGNOSTICO para ETAPA_1_COLETA_FOCADA."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.cv_texto = 'CV teste'
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'AGUARDANDO_OK_DIAGNOSTICO'
        
        result = processar_modulo_otimizador("ok")
        
        assert result is not None
        assert 'COLETA' in result.upper()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
