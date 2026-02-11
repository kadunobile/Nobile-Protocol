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
        assert 'DIAGNÓSTICO' in result.upper()
        assert 'Gerente de Vendas' in result
        assert 'gaps' in result.lower() or 'gap' in result.lower()
        # Deve mostrar introdução com lista de gaps
        assert '2' in result  # Quantidade de gaps
    
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
        """Testa se checkpoint de validação gera prompt COM DADOS REAIS."""
        from modules.otimizador.checkpoint_validacao import prompt_checkpoint_validacao
        from core.dynamic_questions import adicionar_qa_historico
        
        # Mock session state WITH REAL DATA
        mock_session_state.perfil = {'cargo_alvo': 'Product Manager'}
        mock_session_state.gaps_respostas = {
            'Product Discovery': {
                'tem_experiencia': True,
                'resposta': 'Trabalhei com discovery na empresa XYZ usando técnicas de design thinking'
            },
            'User Research': {
                'tem_experiencia': False,
                'resposta': None
            }
        }
        mock_session_state.seo_keywords_respostas = {
            'Product Vision': 'Defini a visão de produto na Startup ABC',
            'Roadmap Planning': 'Gerenciei roadmap de 3 squads com 20+ features/trimestre'
        }
        # Mock histórico de coleta
        mock_session_state.qa_history_coleta = [
            {
                'pergunta': 'Quantas features você entregava por trimestre?',
                'resposta': 'Cerca de 20-25 features por trimestre, com 3 squads'
            },
            {
                'pergunta': 'Quais métricas você acompanhava?',
                'resposta': 'NPS, engagement rate, retention, conversion rate'
            }
        ]
        mock_session_state.get = lambda key, default=None: getattr(mock_session_state, key, default)
        
        result = prompt_checkpoint_validacao()
        
        # Verificações básicas
        assert result is not None
        assert 'CHECKPOINT' in result.upper() or 'VALIDAÇÃO' in result.upper()
        assert 'Product Manager' in result
        
        # CRITICAL: Verificar que mostra DADOS REAIS, não templates
        assert 'Product Discovery' in result  # Gap com experiência
        assert 'design thinking' in result.lower()  # Parte da resposta real
        assert 'User Research' in result  # Gap sem experiência
        
        # Verificar keywords SEO reais
        assert 'Product Vision' in result
        assert 'Startup ABC' in result
        
        # Verificar dados do Deep Dive reais - test that question OR answer data is present
        # (Either the question text or the answer metrics should be visible in checkpoint)
        deep_dive_data_present = (
            'Quantas features' in result or  # Question text
            '20-25' in result or  # Answer metric
            'squads' in result.lower()  # Answer context
        )
        assert deep_dive_data_present, "Expected deep dive question or answer data in checkpoint"
        
        # Verificar que NÃO contém templates/placeholders
        assert '[Nome do gap]' not in result
        assert '[Empresa - Cargo]' not in result
        assert '[Dado coletado]' not in result
    
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
        assert 'DIAGNÓSTICO' in result.upper()
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


class TestHeadhunterEliteModules:
    """Testes para os novos módulos do Headhunter Elite."""
    
    def test_market_knowledge_cobertura(self):
        """Testa se todas as áreas têm keywords, metrics e verbos."""
        from modules.otimizador.market_knowledge import MARKET_KNOWLEDGE
        
        # Verificar se temos 22+ áreas
        assert len(MARKET_KNOWLEDGE) >= 22
        
        # Verificar estrutura de cada área
        for area, conhecimento in MARKET_KNOWLEDGE.items():
            assert 'keywords' in conhecimento
            assert 'metrics' in conhecimento
            assert 'verbos_fortes' in conhecimento
            assert 'ferramentas' in conhecimento
            
            # Verificar quantidade mínima de itens
            assert len(conhecimento['keywords']) >= 10, f"{area} deve ter 10+ keywords"
            assert len(conhecimento['metrics']) >= 5, f"{area} deve ter 5+ metrics"
            assert len(conhecimento['verbos_fortes']) >= 5, f"{area} deve ter 5+ verbos"
            assert len(conhecimento['ferramentas']) >= 5, f"{area} deve ter 5+ ferramentas"
    
    def test_detectar_area_por_cargo(self):
        """Testa detecção de área profissional por cargo."""
        from modules.otimizador.market_knowledge import detectar_area_por_cargo
        
        # Testes de detecção
        assert detectar_area_por_cargo("Gerente de Vendas") == "Sales Manager"
        assert detectar_area_por_cargo("Software Engineer") == "Software Engineer"
        # "Desenvolvedor Backend" pode retornar "Software Engineer" ou "Backend Developer"
        # dependendo da ordem de matching - ambos são válidos
        backend_area = detectar_area_por_cargo("Desenvolvedor Backend")
        assert backend_area in ["Backend Developer", "Software Engineer"]
        assert detectar_area_por_cargo("Data Scientist") == "Data Scientist"
        assert detectar_area_por_cargo("Product Manager") == "Product Manager"
        assert detectar_area_por_cargo("DevOps Engineer") == "DevOps Engineer"
        assert detectar_area_por_cargo("Marketing Manager") == "Marketing Manager"
        
        # Teste de cargo não mapeado
        assert detectar_area_por_cargo("Cargo Desconhecido XYZ") == "Generalista"
        assert detectar_area_por_cargo("") == "Generalista"
    
    def test_obter_conhecimento_mercado(self):
        """Testa obtenção de conhecimento de mercado."""
        from modules.otimizador.market_knowledge import obter_conhecimento_mercado
        
        # Área existente
        conhecimento = obter_conhecimento_mercado("Software Engineer")
        assert conhecimento is not None
        assert 'keywords' in conhecimento
        assert 'API' in conhecimento['keywords']
        
        # Área não existente (deve retornar genérico)
        conhecimento_gen = obter_conhecimento_mercado("Área Inexistente")
        assert conhecimento_gen is not None
        assert 'keywords' in conhecimento_gen
        assert len(conhecimento_gen['keywords']) > 0
    
    def test_classificador_senioridade(self):
        """Testa classificação correta de junior/pleno/senior/executivo."""
        from modules.otimizador.classificador_perfil import classificar_senioridade_e_estrategia
        
        # Teste Junior
        result = classificar_senioridade_e_estrategia("CV básico", "Analista Junior de Vendas")
        assert result['senioridade'] == 'junior'
        assert result['modo_interrogatorio'] == 'operacional'
        
        # Teste Pleno
        result = classificar_senioridade_e_estrategia("CV intermediário", "Analista de Dados")
        assert result['senioridade'] == 'pleno'
        assert result['modo_interrogatorio'] == 'estrategico'
        
        # Teste Senior
        result = classificar_senioridade_e_estrategia("Liderança técnica", "Tech Lead")
        assert result['senioridade'] == 'senior'
        assert result['modo_interrogatorio'] == 'estrategico'
        
        # Teste Executivo
        result = classificar_senioridade_e_estrategia("Gestão de P&L", "Diretor de Vendas")
        assert result['senioridade'] == 'executivo'
        assert result['modo_interrogatorio'] == 'executivo'
        
        # Verificar estrutura completa
        assert 'foco_metricas' in result
        assert 'template_pergunta' in result
        assert 'area_profissional' in result
    
    def test_detector_verbos_fracos(self):
        """Testa detecção de verbos fracos em bullets."""
        from modules.otimizador.analisador_bullets import analisar_bullets_fracos, VERBOS_FRACOS
        
        # Verificar lista de verbos fracos
        assert len(VERBOS_FRACOS) > 10
        assert 'ajudei' in VERBOS_FRACOS
        assert 'participei' in VERBOS_FRACOS
        
        # CV com bullets fracos
        cv_teste = """
        • Ajudei na implementação do projeto
        • Participei do desenvolvimento
        • Trabalhava com Python
        """
        
        result = analisar_bullets_fracos(cv_teste, "Software Engineer", "pleno")
        
        # Deve detectar problemas
        assert len(result) > 0
        
        # Verificar estrutura do resultado
        for item in result:
            assert 'bullet_original' in item
            assert 'problemas' in item
            assert 'pergunta_direcionada' in item
            assert 'metricas_esperadas' in item
    
    def test_contar_bullets_fracos(self):
        """Testa contador de bullets fracos."""
        from modules.otimizador.analisador_bullets import contar_bullets_fracos
        
        cv_teste = """
        • Ajudei na implementação
        • Participei do projeto
        • Trabalhava com equipe
        """
        
        count = contar_bullets_fracos(cv_teste, "Software Engineer", "pleno")
        assert count >= 0
        assert isinstance(count, int)
    
    def test_gerador_bullet_star(self):
        """Testa geração de bullets otimizados por senioridade."""
        from modules.otimizador.engenheiro_texto import gerar_bullet_star, VERBOS_UPGRADE
        
        # Verificar mapeamento de verbos
        assert len(VERBOS_UPGRADE) >= 20
        assert 'ajudei' in VERBOS_UPGRADE
        assert VERBOS_UPGRADE['ajudei'] != 'ajudei'  # Deve ter upgrade
        
        # Teste de geração - Junior
        componentes = {
            'acao': 'Processei',
            'contexto': 'relatórios financeiros',
            'ferramenta': 'Excel',
            'resultado_numerico': '500 relatórios/mês',
            'impacto': '95% de acuracidade'
        }
        
        bullet = gerar_bullet_star(componentes, 'junior', 'Financial Analyst')
        assert bullet is not None
        assert '•' in bullet
        assert 'Excel' in bullet or 'relatórios' in bullet
        
        # Teste de geração - Executivo
        componentes_exec = {
            'acao': 'Liderei',
            'contexto': 'transformação digital',
            'ferramenta': 'budget de R$ 5M',
            'resultado_numerico': '30% crescimento',
            'impacto': 'aumento de receita'
        }
        
        bullet_exec = gerar_bullet_star(componentes_exec, 'executivo', 'Sales Manager')
        assert bullet_exec is not None
        assert '•' in bullet_exec
    
    def test_aplicar_star_method_completo(self):
        """Testa aplicação do método STAR em experiência completa."""
        from modules.otimizador.engenheiro_texto import aplicar_star_method_completo
        
        experiencia = {
            'cargo': 'Analista de Dados',
            'empresa': 'Tech Corp',
            'periodo': '2020-2022',
            'senioridade': 'pleno',
            'bullets': [
                'Ajudei na análise de dados',
                'Participei de projetos'
            ]
        }
        
        result = aplicar_star_method_completo(experiencia, 'Data Scientist')
        
        assert result is not None
        assert 'bullets_originais' in result
        assert 'bullets_otimizados' in result
        assert 'diferencas_destacadas' in result
        assert len(result['bullets_otimizados']) == len(experiencia['bullets'])
    
    def test_prompt_headhunter_elite(self):
        """Testa geração do prompt completo com inteligência."""
        # Importar apenas se streamlit estiver disponível
        try:
            import streamlit as st
            from modules.otimizador.etapa0_diagnostico import prompt_etapa0_diagnostico
        except ImportError:
            pytest.skip("Streamlit não disponível no ambiente de teste")
            return
        
        # Mock session state manualmente
        class MockSessionState:
            perfil = {'cargo_alvo': 'Software Engineer'}
            cv_texto = """
        Desenvolvedor Python
        • Trabalhei com Django
        • Participei de projetos
        • Ajudei na implementação
        """
            gaps_alvo = ['Falta testes automatizados', 'Falta CI/CD']
            gaps_respostas = {}
            
            def get(self, key, default=None):
                return getattr(self, key, default)
            
            def __contains__(self, key):
                return hasattr(self, key)
        
        # Substituir session_state temporariamente
        original_session_state = st.session_state if hasattr(st, 'session_state') else None
        st.session_state = MockSessionState()
        
        try:
            result = prompt_etapa0_diagnostico()
            
            # Verificar estrutura do Headhunter Elite
            assert result is not None
            assert 'HEADHUNTER ELITE' in result.upper()
            assert 'SENIORIDADE' in result.upper()
            assert 'ÁREA' in result.upper()
            assert 'Software Engineer' in result or 'GENERALISTA' in result.upper()
            assert 'GAPS CRÍTICOS' in result.upper()
            assert 'BULLETS FRACOS' in result.upper()
            
            # Verificar menção às 7 etapas
            assert '7 etapas' in result.lower() or '7️⃣' in result
            
            # Verificar menção a pausas obrigatórias
            assert 'pausa' in result.lower() or 'Pausas' in result
        finally:
            # Restaurar session_state original
            if original_session_state is not None:
                st.session_state = original_session_state


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
