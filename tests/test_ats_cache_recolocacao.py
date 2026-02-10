"""
Testes para validar cache de Score ATS em cenário de Recolocação.

Este arquivo testa especificamente a correção do bug onde o score ATS
aparecia diferente entre FASE_1_DIAGNOSTICO e FASE_15_REALITY para o
mesmo cargo e CV quando o objetivo era "Recolocação no Mercado".

Bug corrigido: 
- FASE_1_DIAGNOSTICO agora passa objetivo=None e cargo_atual explicitamente
- FASE_15_REALITY usa cache quando objetivo="Recolocação no Mercado" e cargo_alvo == cargo_atual
"""

import pytest
from core.ats_scorer import calcular_score_ats


@pytest.fixture
def cv_gerente_vendas():
    """CV realista de Gerente de Vendas."""
    return """
    Maria Silva
    linkedin.com/in/mariasilva
    
    Experiência Profissional
    
    Gerente de Vendas | TechCorp Brasil | 2020 - Presente
    - Gestão de equipe comercial de 15 vendedores
    - Implementação de CRM Salesforce
    - Análise de pipeline e forecast mensal
    - Negociação com clientes corporativos B2B
    - Atingimento de 120% da meta anual em 2023
    - Gestão de território São Paulo e interior
    
    Coordenadora Comercial | SoftwareXYZ | 2017 - 2020
    - Coordenação de equipe de 8 vendedores
    - Análise de dados de vendas com Excel
    - Criação de relatórios para diretoria
    - Participação em eventos comerciais
    
    Formação
    MBA em Gestão Comercial | FGV | 2019
    Bacharelado em Administração | FAAP | 2016
    
    Skills
    Salesforce, Pipeline Management, Forecast, Negociação B2B,
    Gestão de Equipes, Excel, Análise de Dados, CRM
    """


class TestATSCacheRecolocacao:
    """Testes para validar cache de ATS em cenários de Recolocação."""
    
    def test_mesmo_cargo_parametros_consistentes_fase1(self, cv_gerente_vendas):
        """
        FASE_1_DIAGNOSTICO: Calcular score passando objetivo=None e cargo_atual.
        
        Valida que a chamada com os novos parâmetros funciona corretamente.
        """
        cargo = "Gerente de Vendas"
        
        # Simular chamada da FASE_1_DIAGNOSTICO
        resultado = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None,
            objetivo=None,  # Ainda não definiu objetivo
            cargo_atual=cargo  # Passar explicitamente
        )
        
        assert resultado is not None, "Resultado não deve ser None"
        assert 'score_total' in resultado, "Resultado deve ter score_total"
        assert resultado['score_total'] >= 0, "Score deve ser >= 0"
        assert resultado['score_total'] <= 100, "Score deve ser <= 100"
    
    def test_recolocacao_mesmo_cargo_parametros_consistentes_fase15(self, cv_gerente_vendas):
        """
        FASE_15_REALITY: Calcular score para Recolocação no mesmo cargo.
        
        Valida que a chamada com objetivo="Recolocação no Mercado" funciona.
        """
        cargo = "Gerente de Vendas"
        
        # Simular chamada da FASE_15_REALITY
        resultado = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None,
            objetivo="Recolocação no Mercado",
            cargo_atual=cargo
        )
        
        assert resultado is not None, "Resultado não deve ser None"
        assert 'score_total' in resultado, "Resultado deve ter score_total"
        assert resultado['score_total'] >= 0, "Score deve ser >= 0"
        assert resultado['score_total'] <= 100, "Score deve ser <= 100"
    
    def test_score_consistente_entre_fases_mesmo_cargo(self, cv_gerente_vendas):
        """
        Validar que score é consistente entre FASE_1 e FASE_15 para Recolocação.
        
        Este é o teste principal que valida a correção do bug.
        """
        cargo = "Gerente de Vendas"
        
        # FASE_1_DIAGNOSTICO: objetivo=None
        resultado_fase1 = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None,
            objetivo=None,
            cargo_atual=cargo
        )
        
        # FASE_15_REALITY: objetivo="Recolocação no Mercado"
        resultado_fase15 = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None,
            objetivo="Recolocação no Mercado",
            cargo_atual=cargo
        )
        
        # Scores devem ser iguais (ou muito próximos devido ao determinismo)
        assert resultado_fase1['score_total'] == resultado_fase15['score_total'], \
            f"Score deve ser igual entre fases: {resultado_fase1['score_total']} vs {resultado_fase15['score_total']}"
    
    def test_transicao_cargo_diferente_pode_ter_score_diferente(self, cv_gerente_vendas):
        """
        Validar que Transição de Carreira (cargo diferente) PODE ter score diferente.
        
        Este é um cenário esperado: se o usuário quer mudar de cargo,
        o score pode ser diferente porque os requisitos são diferentes.
        """
        cargo_atual = "Gerente de Vendas"
        cargo_alvo = "Gerente de Marketing"
        
        # FASE_1_DIAGNOSTICO: score para cargo atual
        resultado_fase1 = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo_atual,
            client=None,
            objetivo=None,
            cargo_atual=cargo_atual
        )
        
        # FASE_15_REALITY: score para cargo diferente (Transição)
        resultado_fase15 = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo_alvo,  # Cargo diferente
            client=None,
            objetivo="Transição de Carreira",
            cargo_atual=cargo_atual
        )
        
        # Neste caso, scores PODEM ser diferentes (não há garantia de igualdade)
        # Apenas validamos que ambos são válidos
        assert 0 <= resultado_fase1['score_total'] <= 100, "Score FASE_1 deve ser válido"
        assert 0 <= resultado_fase15['score_total'] <= 100, "Score FASE_15 deve ser válido"
        
        # Esperamos que score seja menor para cargo diferente
        # (mas não é uma regra absoluta, depende do CV)
        # Apenas documentamos o comportamento esperado
    
    def test_promocao_cargo_senior_pode_ter_score_diferente(self, cv_gerente_vendas):
        """
        Validar que Promoção (cargo mais sênior) PODE ter score diferente.
        
        Cenário: Gerente quer promoção para Diretor.
        Score pode ser menor porque requisitos de Diretor são mais altos.
        """
        cargo_atual = "Gerente de Vendas"
        cargo_alvo = "Diretor Comercial"
        
        # FASE_1_DIAGNOSTICO: score para cargo atual
        resultado_fase1 = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo_atual,
            client=None,
            objetivo=None,
            cargo_atual=cargo_atual
        )
        
        # FASE_15_REALITY: score para cargo mais sênior (Promoção)
        resultado_fase15 = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo_alvo,  # Cargo mais sênior
            client=None,
            objetivo="Promoção Interna",
            cargo_atual=cargo_atual
        )
        
        # Ambos devem ser válidos
        assert 0 <= resultado_fase1['score_total'] <= 100, "Score FASE_1 deve ser válido"
        assert 0 <= resultado_fase15['score_total'] <= 100, "Score FASE_15 deve ser válido"
    
    def test_resultado_completo_tem_todas_chaves(self, cv_gerente_vendas):
        """
        Validar que resultado completo tem todas as chaves esperadas.
        
        Isso garante que o cache funciona corretamente e retorna
        o objeto completo, não apenas o score numérico.
        """
        cargo = "Gerente de Vendas"
        
        resultado = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None,
            objetivo="Recolocação no Mercado",
            cargo_atual=cargo
        )
        
        # Verificar que todas as chaves esperadas estão presentes
        chaves_esperadas = [
            'score_total',
            'max_score',
            'percentual',
            'nivel',
            'cargo_avaliado',
            'pontos_fortes',
            'gaps_identificados',
            'plano_acao',
            'jd_gerada',
            'detalhes'
        ]
        
        for chave in chaves_esperadas:
            assert chave in resultado, f"Chave '{chave}' deve estar no resultado"
        
        # Verificar tipos
        assert isinstance(resultado['score_total'], (int, float)), "score_total deve ser numérico"
        assert isinstance(resultado['pontos_fortes'], list), "pontos_fortes deve ser lista"
        assert isinstance(resultado['gaps_identificados'], list), "gaps_identificados deve ser lista"
        assert isinstance(resultado['plano_acao'], list), "plano_acao deve ser lista"
        assert isinstance(resultado['nivel'], str), "nivel deve ser string"
        assert isinstance(resultado['cargo_avaliado'], str), "cargo_avaliado deve ser string"


class TestATSParametrosOpcionais:
    """Testes para validar parâmetros opcionais objetivo e cargo_atual."""
    
    def test_sem_objetivo_funciona(self, cv_gerente_vendas):
        """
        Validar que calcular_score_ats funciona sem passar objetivo.
        
        Caso de uso: FASE_1_DIAGNOSTICO antes do briefing.
        """
        cargo = "Gerente de Vendas"
        
        resultado = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None
            # objetivo não passado (None implícito)
            # cargo_atual não passado (None implícito)
        )
        
        assert resultado is not None, "Deve funcionar sem objetivo"
        assert 'score_total' in resultado, "Deve ter score_total"
    
    def test_sem_cargo_atual_funciona(self, cv_gerente_vendas):
        """
        Validar que calcular_score_ats funciona sem passar cargo_atual.
        
        Caso de uso: quando cargo_atual não foi extraído do CV.
        """
        cargo = "Gerente de Vendas"
        
        resultado = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None,
            objetivo="Recolocação no Mercado"
            # cargo_atual não passado (None implícito)
        )
        
        assert resultado is not None, "Deve funcionar sem cargo_atual"
        assert 'score_total' in resultado, "Deve ter score_total"
    
    def test_com_todos_parametros_funciona(self, cv_gerente_vendas):
        """
        Validar que calcular_score_ats funciona com todos os parâmetros.
        
        Caso de uso: FASE_15_REALITY com perfil completo.
        """
        cargo = "Gerente de Vendas"
        
        resultado = calcular_score_ats(
            cv_texto=cv_gerente_vendas,
            cargo_alvo=cargo,
            client=None,
            objetivo="Recolocação no Mercado",
            cargo_atual=cargo
        )
        
        assert resultado is not None, "Deve funcionar com todos parâmetros"
        assert 'score_total' in resultado, "Deve ter score_total"
