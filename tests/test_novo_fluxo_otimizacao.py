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
    def test_etapa0_diagnostico_gera_prompt_introducao(self, mock_session_state):
        """Testa se etapa0 gera prompt de diagnóstico introdutório corretamente."""
        from modules.otimizador.etapa0_diagnostico import prompt_etapa0_diagnostico
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Gerente de Vendas'}
        mock_session_state.cv_texto = 'CV de teste com experiência em vendas'
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.gaps_alvo = ['Falta métrica de vendas', 'Falta gestão de equipe']
        
        result = prompt_etapa0_diagnostico()
        
        assert result is not None
        # Novo prompt com persona Headhunter Elite
        assert 'HEADHUNTER ELITE' in result.upper()
        assert 'Gerente de Vendas' in result
        assert 'gap' in result.lower()
        # Deve incluir as novas seções do fluxo refinado
        assert 'SEO MAPPING' in result.upper() or 'SEO' in result
        assert 'DEEP DIVE' in result.upper() or 'DADOS CONCRETOS' in result.upper()
        assert 'ARQUIVO MESTRE' in result.upper() or 'ARQUIVO' in result.upper()
    
    @patch('streamlit.session_state')
    def test_etapa0_diagnostico_gap_individual(self, mock_session_state):
        """Testa se etapa0 pergunta sobre gap individual corretamente."""
        from modules.otimizador.etapa0_diagnostico import prompt_etapa0_diagnostico_gap_individual
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Gerente de Vendas'}
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.gaps_alvo = ['Falta métrica de vendas', 'Falta gestão de equipe']
        
        # Testar primeiro gap
        result = prompt_etapa0_diagnostico_gap_individual(0)
        
        assert result is not None
        assert 'Falta métrica de vendas' in result
        assert 'experiência' in result.lower()
        assert '1/2' in result  # Indica gap 1 de 2
        
        # Testar segundo gap
        result2 = prompt_etapa0_diagnostico_gap_individual(1)
        
        assert result2 is not None
        assert 'Falta gestão de equipe' in result2
        assert '2/2' in result2  # Indica gap 2 de 2
    
    @patch('streamlit.session_state')
    def test_etapa1_coleta_focada_gera_prompt_contextual(self, mock_session_state):
        """Testa se etapa1 coleta focada gera prompt com instruções contextuais."""
        from modules.otimizador.etapa1_coleta_focada import prompt_etapa1_coleta_focada
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista de Dados'}
        mock_session_state.cv_texto = 'CV com experiência em análise'
        mock_session_state.gaps_respostas = {
            'Python': {'tem_experiencia': True, 'resposta': 'Usei na empresa X'}
        }
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        result = prompt_etapa1_coleta_focada()
        
        assert result is not None
        assert 'COLETA FOCADA' in result.upper()
        assert 'Analista de Dados' in result
        assert 'headhunter' in result.lower()
        assert 'contextual' in result.lower() or 'específica' in result.lower()
        # Deve incluir instruções sobre perguntas específicas ao cargo
        assert 'métrica' in result.lower() or 'kpi' in result.lower()
    
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
    def test_processor_etapa0_diagnostico_introducao(self, mock_session_state):
        """Testa transição para ETAPA_0_DIAGNOSTICO (introdução)."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Gerente'}
        mock_session_state.cv_texto = 'CV teste'
        mock_session_state.gaps_alvo = ['Gap 1', 'Gap 2']
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'ETAPA_0_DIAGNOSTICO'
        
        result = processar_modulo_otimizador("")
        
        assert result is not None
        # Novo prompt com persona Headhunter Elite
        assert 'HEADHUNTER ELITE' in result.upper() or 'OTIMIZAÇÃO' in result.upper()
        assert 'Gerente' in result
    
    @patch('streamlit.session_state')
    def test_processor_etapa0_gap_individual(self, mock_session_state):
        """Testa transição para ETAPA_0_GAP_INDIVIDUAL."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.gaps_alvo = ['Python', 'SQL']
        mock_session_state.gap_atual_index = 0
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'ETAPA_0_GAP_INDIVIDUAL'
        
        result = processar_modulo_otimizador("")
        
        assert result is not None
        assert 'Python' in result
        assert 'experiência' in result.lower()
    
    @patch('streamlit.session_state')
    def test_processor_aguardando_resposta_gap_com_experiencia(self, mock_session_state):
        """Testa processamento de resposta de gap com experiência."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.gaps_alvo = ['Python', 'SQL']
        mock_session_state.gap_atual_index = 0
        mock_session_state.gaps_respostas = {}
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'AGUARDANDO_RESPOSTA_GAP'
        
        result = processar_modulo_otimizador("Sim, usei Python na empresa X para análise de dados")
        
        # Deve salvar resposta e ir para próximo gap
        assert mock_session_state.gaps_respostas.get('Python') is not None
        assert mock_session_state.gaps_respostas['Python']['tem_experiencia'] is True
        assert 'empresa X' in mock_session_state.gaps_respostas['Python']['resposta']
    
    @patch('streamlit.session_state')
    def test_processor_aguardando_resposta_gap_sem_experiencia(self, mock_session_state):
        """Testa processamento de resposta de gap sem experiência."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.gaps_alvo = ['Python', 'SQL']
        mock_session_state.gap_atual_index = 0
        mock_session_state.gaps_respostas = {}
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'AGUARDANDO_RESPOSTA_GAP'
        
        result = processar_modulo_otimizador("não tenho")
        
        # Deve marcar como sem experiência
        assert mock_session_state.gaps_respostas.get('Python') is not None
        assert mock_session_state.gaps_respostas['Python']['tem_experiencia'] is False
    
    @patch('streamlit.session_state')
    def test_processor_gerar_resumo_diagnostico(self, mock_session_state):
        """Testa geração de resumo após todos os gaps."""
        from modules.otimizador.processor import gerar_resumo_diagnostico
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.gaps_respostas = {
            'Python': {'tem_experiencia': True, 'resposta': 'Usei na empresa X'},
            'SQL': {'tem_experiencia': False, 'resposta': None}
        }
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        result = gerar_resumo_diagnostico()
        
        assert result is not None
        assert 'RESUMO' in result.upper()
        assert 'Python' in result
        assert 'SQL' in result
        assert mock_session_state.gaps_resolviveis_count == 1
        assert mock_session_state.gaps_nao_resolviveis_count == 1
    
    @patch('streamlit.session_state')
    def test_processor_aguardando_ok_diagnostico_avanca_coleta(self, mock_session_state):
        """Testa que após resumo, avança para coleta focada."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.cv_texto = 'CV teste'
        mock_session_state.gaps_respostas = {}
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'AGUARDANDO_OK_DIAGNOSTICO'
        
        result = processar_modulo_otimizador("")
        
        # Deve retornar prompt de coleta focada
        assert result is not None
        assert 'COLETA' in result.upper()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
