"""
Testes unitários para o sistema de pontuação ATS.
"""

import pytest
from core.ats_scorer import (
    calcular_score_ats,
    classificar_score
)


class TestAtsScorer:
    """Testes para o módulo ATS Scorer."""
    
    def test_classificar_score_excelente(self):
        """Testa classificação de score excelente."""
        assert classificar_score(75) == "Excelente"
        assert classificar_score(100) == "Excelente"
    
    def test_classificar_score_bom(self):
        """Testa classificação de score bom."""
        assert classificar_score(55) == "Bom"
        assert classificar_score(65) == "Bom"
    
    def test_classificar_score_regular(self):
        """Testa classificação de score regular."""
        assert classificar_score(35) == "Regular"
        assert classificar_score(45) == "Regular"
    
    def test_classificar_score_precisa_melhorar(self):
        """Testa classificação de score baixo."""
        assert classificar_score(10) == "Precisa Melhorar"
        assert classificar_score(25) == "Precisa Melhorar"
    
    def test_calcular_score_ats_estrutura_basica(self):
        """Testa que calcular_score_ats retorna estrutura correta."""
        cv_texto = """
        João Silva
        email@example.com
        
        EXPERIÊNCIA
        Gerente | Empresa X | 2020-2023
        - Aumentei vendas em 30%
        
        EDUCAÇÃO
        MBA | FGV | 2019
        
        HABILIDADES
        Python, SQL
        """
        
        resultado = calcular_score_ats(cv_texto, "Gerente")
        
        # Verifica estrutura do resultado
        assert 'score_total' in resultado
        assert 'max_score' in resultado
        assert 'percentual' in resultado
        assert 'nivel' in resultado
        assert 'detalhes' in resultado
        assert 'pontos_fortes' in resultado
        assert 'gaps_identificados' in resultado
        assert 'plano_acao' in resultado
        
        # Verifica tipos
        assert isinstance(resultado['score_total'], (int, float))
        assert isinstance(resultado['max_score'], int)
        assert isinstance(resultado['percentual'], (int, float))
        assert isinstance(resultado['nivel'], str)
        assert isinstance(resultado['detalhes'], dict)
        assert isinstance(resultado['pontos_fortes'], list)
        assert isinstance(resultado['gaps_identificados'], list)
        assert isinstance(resultado['plano_acao'], list)
        
        # Verifica valores dentro dos limites
        assert 0 <= resultado['score_total'] <= 100
        assert resultado['max_score'] == 100
        assert 0 <= resultado['percentual'] <= 100
    
    def test_calcular_score_ats_detalhes(self):
        """Testa detalhamento do score ATS."""
        cv_texto = """
        João Silva
        email@example.com
        
        EXPERIÊNCIA
        Gerente | Empresa X | 2020-2023
        - Aumentei vendas em 30%
        
        EDUCAÇÃO
        MBA | FGV | 2019
        
        HABILIDADES
        Python, SQL
        """
        
        resultado = calcular_score_ats(cv_texto, "Gerente")
        detalhes = resultado['detalhes']
        
        # Verifica presença das informações básicas
        assert 'metodo' in detalhes
        assert 'ngrams' in detalhes
        assert 'stopwords' in detalhes
        assert 'TF-IDF + Cosine Similarity' in detalhes['metodo']
        assert detalhes['ngrams'] == '1-3'
        assert detalhes['stopwords'] == 'PT + EN + Verbos genéricos JD'
    
    def test_calcular_score_ats_cv_vazio(self):
        """Testa cálculo com CV vazio."""
        resultado = calcular_score_ats("", "Gerente")
        
        # Deve retornar score baixo mas não deve falhar
        assert resultado['score_total'] >= 0
        assert resultado['score_total'] <= 100
        assert resultado['nivel'] in ["Excelente", "Bom", "Regular", "Precisa Melhorar"]
    
    def test_calcular_score_ats_cv_completo(self):
        """Testa cálculo com CV bem estruturado."""
        cv_completo = """
        João Silva
        email@example.com | (11) 99999-9999 | linkedin.com/in/joao
        
        EXPERIÊNCIA PROFISSIONAL
        Gerente de Vendas | Empresa XYZ | 2020-2023
        - Aumentei vendas em 30%
        - Gerenciei equipe de 10 pessoas
        - Implementei CRM que resultou em 50% mais produtividade
        - Negociei contratos de R$ 1M+
        
        Analista | Empresa ABC | 2018-2020
        - Pipeline de 200+ leads mensais
        - Quota superada em 120%
        
        EDUCAÇÃO
        MBA em Gestão | FGV | 2019
        Graduação | USP | 2017
        
        HABILIDADES
        Vendas, CRM, Negociação, Gestão de Equipe, Planejamento Estratégico
        """
        
        resultado = calcular_score_ats(cv_completo, "Gerente de Vendas")
        
        # CV bem estruturado deve ter score válido
        assert resultado['score_total'] >= 0
        assert resultado['percentual'] >= 0
        
        # Verifica campos adicionais do novo sistema
        assert 'cargo_avaliado' in resultado
        assert resultado['cargo_avaliado'] == "Gerente de Vendas"
        assert 'jd_gerada' in resultado


class TestCvExporter:
    """Testes para o exportador de CV em DOCX."""
    
    def test_gerar_cv_docx_basico(self):
        """Testa geração de CV DOCX básico."""
        from core.cv_exporter import gerar_cv_docx
        
        dados_cv = {
            'nome': 'João Silva',
            'email': 'joao@example.com'
        }
        
        buffer = gerar_cv_docx(dados_cv)
        
        # Verifica que retornou um buffer
        assert buffer is not None
        assert hasattr(buffer, 'read')
        assert hasattr(buffer, 'seek')
        
        # Verifica que tem conteúdo
        conteudo = buffer.getvalue()
        assert len(conteudo) > 0
    
    def test_gerar_cv_docx_completo(self):
        """Testa geração de CV DOCX com todas as seções."""
        from core.cv_exporter import gerar_cv_docx
        
        dados_cv = {
            'nome': 'João Silva',
            'email': 'joao@example.com',
            'telefone': '(11) 99999-9999',
            'linkedin': 'linkedin.com/in/joao',
            'resumo': 'Profissional experiente',
            'experiencias': [{
                'cargo': 'Gerente',
                'empresa': 'Empresa X',
                'periodo': '2020-2023',
                'descricao': 'Liderança de equipe',
                'realizacoes': ['Aumentou vendas em 30%']
            }],
            'educacao': [{
                'curso': 'MBA',
                'instituicao': 'FGV',
                'periodo': '2019'
            }],
            'habilidades': {
                'Técnicas': ['Python', 'SQL'],
                'Soft Skills': ['Liderança']
            }
        }
        
        buffer = gerar_cv_docx(dados_cv)
        conteudo = buffer.getvalue()
        
        # Verifica que o arquivo é maior (tem mais conteúdo)
        assert len(conteudo) > 10000
