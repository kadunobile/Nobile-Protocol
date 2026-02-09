"""
Testes para o módulo de CV estruturado (core/cv_estruturado.py).

Testa inicialização, salvamento de dados coletados, e geração de contexto
para uso em prompts finais.
"""

import pytest
from unittest.mock import patch
import sys
sys.path.insert(0, '.')


class TestCVEstruturado:
    """Testes para estrutura de CV."""
    
    def test_inicializar_cv_estruturado(self):
        """Testa inicialização da estrutura de CV."""
        from core.cv_estruturado import inicializar_cv_estruturado
        
        cv_est = inicializar_cv_estruturado()
        
        assert cv_est is not None
        assert 'header' in cv_est
        assert 'posicionamento' in cv_est
        assert 'summary' in cv_est
        assert 'keywords_ats' in cv_est
        assert 'experiencias' in cv_est
        assert 'educacao' in cv_est
        assert 'idiomas' in cv_est
        assert 'certificacoes' in cv_est
        assert 'linkedin' in cv_est
        assert 'gaps' in cv_est
        assert 'metricas_coletadas' in cv_est
        
        # Verificar estruturas aninhadas
        assert 'nome' in cv_est['header']
        assert 'telefone' in cv_est['header']
        assert 'cargo_alvo' in cv_est['posicionamento']
        assert 'headline' in cv_est['linkedin']
        assert 'skills' in cv_est['linkedin']
        assert 'identificados' in cv_est['gaps']
        assert 'volumes' in cv_est['metricas_coletadas']
    
    @patch('streamlit.session_state')
    def test_salvar_dados_coleta(self, mock_session_state):
        """Testa salvamento de dados coletados."""
        from core.cv_estruturado import salvar_dados_coleta, inicializar_cv_estruturado
        
        # Mock session state
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        dados = {
            'raw_response': 'Gerenciei 50+ processos com SAP, reduzindo tempo em 30%',
            'ferramentas': ['SAP', 'Excel'],
            'resultados': ['Redução de 30% no tempo']
        }
        
        salvar_dados_coleta(dados)
        
        # Verificar que dados foram salvos
        cv_est = mock_session_state.cv_estruturado
        assert len(cv_est['metricas_coletadas']['volumes']) > 0  # Deve ter extraído "50", "30"
        assert 'SAP' in cv_est['metricas_coletadas']['ferramentas']
        assert 'Excel' in cv_est['metricas_coletadas']['ferramentas']
        assert 'Redução de 30% no tempo' in cv_est['metricas_coletadas']['resultados']
    
    @patch('streamlit.session_state')
    def test_adicionar_experiencia(self, mock_session_state):
        """Testa adição de experiência profissional."""
        from core.cv_estruturado import adicionar_experiencia, inicializar_cv_estruturado
        
        # Mock session state
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        experiencia = {
            'empresa': 'LBCA',
            'cargo': 'Controler Jurídico',
            'periodo': 'Set 2022 - Ago 2024',
            'conquistas': [
                'Gestão de 50+ processos',
                'Operação em PJE, ESAJ, PROJUDI'
            ]
        }
        
        adicionar_experiencia(experiencia)
        
        cv_est = mock_session_state.cv_estruturado
        assert len(cv_est['experiencias']) == 1
        assert cv_est['experiencias'][0]['empresa'] == 'LBCA'
        assert cv_est['experiencias'][0]['cargo'] == 'Controler Jurídico'
        assert len(cv_est['experiencias'][0]['conquistas']) == 2
    
    @patch('streamlit.session_state')
    def test_atualizar_posicionamento(self, mock_session_state):
        """Testa atualização de posicionamento estratégico."""
        from core.cv_estruturado import atualizar_posicionamento, inicializar_cv_estruturado
        
        # Mock session state
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        atualizar_posicionamento(
            cargo_alvo='Gerente de Vendas',
            estrategia='Foco em gestão de equipe e resultados',
            senioridade='Pleno/Sênior',
            diferencial='Experiência em vendas B2B'
        )
        
        cv_est = mock_session_state.cv_estruturado
        assert cv_est['posicionamento']['cargo_alvo'] == 'Gerente de Vendas'
        assert cv_est['posicionamento']['estrategia'] == 'Foco em gestão de equipe e resultados'
        assert cv_est['posicionamento']['senioridade_real'] == 'Pleno/Sênior'
        assert cv_est['posicionamento']['diferencial'] == 'Experiência em vendas B2B'
    
    @patch('streamlit.session_state')
    def test_atualizar_linkedin(self, mock_session_state):
        """Testa atualização de dados de LinkedIn."""
        from core.cv_estruturado import atualizar_linkedin, inicializar_cv_estruturado
        
        # Mock session state
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        atualizar_linkedin(
            headline='Gerente de Vendas | B2B | SaaS',
            skills=['Vendas', 'Gestão', 'Negociação', 'CRM'],
            about='Profissional com 10 anos de experiência...',
            headline_opcoes=['Opção A', 'Opção B', 'Opção C']
        )
        
        cv_est = mock_session_state.cv_estruturado
        assert cv_est['linkedin']['headline'] == 'Gerente de Vendas | B2B | SaaS'
        assert len(cv_est['linkedin']['skills']) == 4
        assert 'Vendas' in cv_est['linkedin']['skills']
        assert cv_est['linkedin']['about'].startswith('Profissional')
        assert len(cv_est['linkedin']['headline_opcoes']) == 3
    
    @patch('streamlit.session_state')
    def test_atualizar_gaps(self, mock_session_state):
        """Testa atualização de gaps identificados."""
        from core.cv_estruturado import atualizar_gaps, inicializar_cv_estruturado
        
        # Mock session state
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        atualizar_gaps(
            identificados=['Python', 'SQL', 'Power BI'],
            resolvidos=['Python', 'SQL'],
            nao_resolvidos=['Power BI']
        )
        
        cv_est = mock_session_state.cv_estruturado
        assert len(cv_est['gaps']['identificados']) == 3
        assert len(cv_est['gaps']['resolvidos']) == 2
        assert len(cv_est['gaps']['nao_resolvidos']) == 1
        assert 'Python' in cv_est['gaps']['resolvidos']
        assert 'Power BI' in cv_est['gaps']['nao_resolvidos']
    
    @patch('streamlit.session_state')
    def test_gerar_contexto_para_prompt(self, mock_session_state):
        """Testa geração de contexto formatado para prompts."""
        from core.cv_estruturado import (
            inicializar_cv_estruturado, 
            gerar_contexto_para_prompt,
            atualizar_posicionamento,
            atualizar_gaps,
            adicionar_experiencia
        )
        
        # Mock session state com dados completos
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        # Preencher dados
        atualizar_posicionamento(
            cargo_alvo='Analista de Dados',
            estrategia='Foco em BI e analytics',
            senioridade='Pleno'
        )
        
        atualizar_gaps(
            identificados=['Python', 'SQL'],
            resolvidos=['Python'],
            nao_resolvidos=['SQL']
        )
        
        adicionar_experiencia({
            'cargo': 'Analista',
            'empresa': 'Empresa X',
            'periodo': '2022-2024',
            'conquistas': ['Criou dashboards', 'Analisou dados']
        })
        
        # Adicionar métricas
        cv_est = mock_session_state.cv_estruturado
        cv_est['metricas_coletadas']['ferramentas'] = ['Python', 'Pandas']
        cv_est['metricas_coletadas']['volumes'] = ['50+', '100']
        
        contexto = gerar_contexto_para_prompt()
        
        assert contexto is not None
        assert 'DADOS COLETADOS' in contexto
        assert 'Analista de Dados' in contexto
        assert 'Python' in contexto
        assert 'GAPS RESOLVIDOS' in contexto
        assert 'NUNCA invente' in contexto
        assert 'Empresa X' in contexto


class TestProcessorIntegration:
    """Testes de integração do processor com CV estruturado."""
    
    @patch('streamlit.session_state')
    def test_processor_inicializa_cv_estruturado_na_coleta(self, mock_session_state):
        """Testa que processor inicializa CV estruturado ao entrar em coleta."""
        from modules.otimizador.processor import processar_modulo_otimizador
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.cv_texto = 'CV teste'
        mock_session_state.gaps_respostas = {
            'Python': {'tem_experiencia': True, 'resposta': 'Usei na empresa X'}
        }
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'ETAPA_1_COLETA_FOCADA'
        
        result = processar_modulo_otimizador("")
        
        # Verificar que CV estruturado foi inicializado
        assert hasattr(mock_session_state, 'cv_estruturado')
        assert mock_session_state.cv_estruturado is not None
        assert mock_session_state.cv_estruturado['posicionamento']['cargo_alvo'] == 'Analista'
        assert 'Python' in mock_session_state.cv_estruturado['gaps']['resolvidos']
    
    @patch('streamlit.session_state')
    def test_processor_salva_dados_coleta_incrementalmente(self, mock_session_state):
        """Testa que processor salva dados coletados incrementalmente."""
        from modules.otimizador.processor import processar_modulo_otimizador
        from core.cv_estruturado import inicializar_cv_estruturado
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.cv_texto = 'CV teste'
        mock_session_state.gaps_respostas = {}
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.dados_coleta_historico = []
        mock_session_state.dados_coleta_count = 0
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'AGUARDANDO_DADOS_COLETA'
        
        # Simular resposta do usuário com conteúdo substantivo
        result = processar_modulo_otimizador("Trabalhei com Python na empresa X, gerenciando 50 processos")
        
        # Verificar que dados foram salvos
        assert len(mock_session_state.dados_coleta_historico) == 1
        assert mock_session_state.dados_coleta_count == 1
        assert 'Python' in mock_session_state.dados_coleta_historico[0]
        
        # Verificar que retornou None para continuar chat
        assert result is None
    
    @patch('streamlit.session_state')
    def test_processor_avanca_com_comando_continuar(self, mock_session_state):
        """Testa que processor avança ao receber comando 'continuar'."""
        from modules.otimizador.processor import processar_modulo_otimizador
        from core.cv_estruturado import inicializar_cv_estruturado
        
        # Mock session state
        mock_session_state.perfil = {'cargo_alvo': 'Analista'}
        mock_session_state.cv_texto = 'CV teste'
        mock_session_state.gaps_respostas = {}
        mock_session_state.cv_estruturado = inicializar_cv_estruturado()
        mock_session_state.dados_coleta_historico = ['Resposta 1', 'Resposta 2']
        mock_session_state.dados_coleta_count = 2
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        mock_session_state.etapa_modulo = 'AGUARDANDO_DADOS_COLETA'
        
        # Simular comando de avançar
        result = processar_modulo_otimizador("continuar")
        
        # Verificar que avançou para checkpoint
        assert mock_session_state.etapa_modulo == 'CHECKPOINT_1_VALIDACAO'
        assert result is not None  # Deve retornar prompt de checkpoint
        assert 'CHECKPOINT' in result.upper() or 'VALIDAÇÃO' in result.upper()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
