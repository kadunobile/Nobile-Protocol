"""
Teste para validar que placeholders de gaps são filtrados corretamente.
"""

import pytest
import json
from unittest.mock import Mock, patch
from core.ats_scorer import _analisar_com_llm


class TestPlaceholderFiltering:
    """Testes para verificar a filtragem de placeholders nos gaps."""
    
    @patch('core.ats_scorer.chamar_gpt')
    def test_placeholders_removidos_dos_gaps(self, mock_chamar_gpt):
        """
        Testa que placeholders comuns são removidos dos gaps_identificados.
        """
        # Mock resposta da LLM com placeholders
        resposta_com_placeholders = json.dumps({
            "score": 65.0,
            "arquetipo_cargo": "VENDAS",
            "pontos_fortes": ["CRM Salesforce", "Pipeline Management"],
            "gaps_identificados": [
                "ferramenta_especifica_1",
                "metodologia_2",
                "HubSpot",
                "<nome_da_ferramenta>",
                "Python",
                "exemplo_skill"
            ],
            "gaps_falsos_ignorados": ["Tableau (não é padrão para vendas)"],
            "plano_acao": ["🔍 Adicione keywords relevantes"]
        })
        
        mock_chamar_gpt.return_value = resposta_com_placeholders
        
        # Mock client
        mock_client = Mock()
        
        # Executar análise
        resultado = _analisar_com_llm(
            mock_client, 
            "CV de teste", 
            "Gerente de Vendas"
        )
        
        # Verificar que placeholders foram removidos
        assert resultado is not None
        gaps = resultado['gaps_identificados']
        
        # Placeholders devem ter sido removidos
        assert "ferramenta_especifica_1" not in gaps
        assert "metodologia_2" not in gaps
        assert "<nome_da_ferramenta>" not in gaps
        assert "exemplo_skill" not in gaps
        
        # Skills reais devem permanecer
        assert "HubSpot" in gaps
        assert "Python" in gaps
    
    @patch('core.ats_scorer.chamar_gpt')
    def test_exemplos_parafraseados_filtrados_gaps_falsos(self, mock_chamar_gpt):
        """
        Testa que exemplos parafraseados (SQL, Python, Tableau) são removidos 
        dos gaps_falsos_ignorados, mesmo que não sejam cópias literais.
        """
        # Mock resposta da LLM com exemplos parafraseados
        resposta_com_parafrase = json.dumps({
            "score": 75.0,
            "arquetipo_cargo": "GESTÃO",
            "pontos_fortes": ["Gestão de Equipes", "P&L Management"],
            "gaps_identificados": ["Power BI", "SAP"],
            "gaps_falsos_ignorados": [
                "SQL (não mencionado, mas pode ser usado indiretamente nas ferramentas de dados)",
                "Python (não é essencial para o nível de gestão, mas pode ser útil para análise de dados)",
                "Tableau (não é padrão para este cargo)",
                "SAP APO (candidato usa outro ERP compatível)"
            ],
            "plano_acao": ["✅ Continue desenvolvendo"]
        })
        
        mock_chamar_gpt.return_value = resposta_com_parafrase
        mock_client = Mock()
        
        resultado = _analisar_com_llm(
            mock_client, 
            "CV Head of Pricing", 
            "Head of Pricing"
        )
        
        # Verificar que exemplos parafraseados foram filtrados
        assert resultado is not None
        gaps_falsos = resultado['gaps_falsos_ignorados']
        
        # Extrair nomes de skills (primeira palavra antes do parêntese)
        def extract_skill_name(gap_falso):
            """Extrai o nome da skill do gap falso."""
            words = gap_falso.lower().split('(')[0].strip().split()
            return words[0] if words else ''
        
        skill_names = [extract_skill_name(gf) for gf in gaps_falsos]
        
        # Exemplos parafraseados devem ter sido removidos (SQL, Python, Tableau)
        assert 'sql' not in skill_names
        assert 'python' not in skill_names
        assert 'tableau' not in skill_names
        
        # Gaps falsos reais devem permanecer
        assert "SAP APO (candidato usa outro ERP compatível)" in gaps_falsos
        
        # Deve ter exatamente 1 item (apenas o gap falso real)
        assert len(gaps_falsos) == 1
    
    @patch('core.ats_scorer.chamar_gpt')
    def test_gaps_falsos_reais_mantidos(self, mock_chamar_gpt):
        """
        Testa que gaps falsos reais e específicos para o cargo não são removidos.
        """
        resposta_gaps_reais = json.dumps({
            "score": 80.0,
            "arquetipo_cargo": "VENDAS",
            "pontos_fortes": ["Salesforce", "Gestão de Pipeline"],
            "gaps_identificados": ["HubSpot Marketing"],
            "gaps_falsos_ignorados": [
                "Outreach (candidato já usa ferramenta similar de sales engagement)",
                "ZoomInfo (não é obrigatório, apenas nice-to-have)"
            ],
            "plano_acao": ["✅ Forte candidato"]
        })
        
        mock_chamar_gpt.return_value = resposta_gaps_reais
        mock_client = Mock()
        
        resultado = _analisar_com_llm(
            mock_client, 
            "CV Gerente de Vendas", 
            "Gerente de Vendas B2B"
        )
        
        # Todos os gaps falsos devem estar presentes pois são reais
        assert len(resultado['gaps_falsos_ignorados']) == 2
        assert any('outreach' in gf.lower() for gf in resultado['gaps_falsos_ignorados'])
        assert any('zoominfo' in gf.lower() for gf in resultado['gaps_falsos_ignorados'])
        
    @patch('core.ats_scorer.chamar_gpt')
    def test_todos_gaps_validos_mantidos(self, mock_chamar_gpt):
        """
        Testa que gaps válidos (sem placeholders) não são removidos.
        """
        resposta_valida = json.dumps({
            "score": 70.0,
            "arquetipo_cargo": "TÉCNICO",
            "pontos_fortes": ["Java", "Spring Boot"],
            "gaps_identificados": [
                "Docker",
                "Kubernetes",
                "AWS",
                "CI/CD"
            ],
            "gaps_falsos_ignorados": [],
            "plano_acao": ["✅ Continue assim"]
        })
        
        mock_chamar_gpt.return_value = resposta_valida
        mock_client = Mock()
        
        resultado = _analisar_com_llm(
            mock_client, 
            "CV desenvolvedor", 
            "Desenvolvedor Backend"
        )
        
        # Todos os gaps devem estar presentes
        assert len(resultado['gaps_identificados']) == 4
        assert "Docker" in resultado['gaps_identificados']
        assert "Kubernetes" in resultado['gaps_identificados']
        assert "AWS" in resultado['gaps_identificados']
        assert "CI/CD" in resultado['gaps_identificados']
    
    @patch('core.ats_scorer.chamar_gpt')
    def test_lista_vazia_se_todos_placeholders(self, mock_chamar_gpt):
        """
        Testa que retorna lista vazia se todos os gaps são placeholders.
        """
        resposta_so_placeholders = json.dumps({
            "score": 60.0,
            "arquetipo_cargo": "GESTÃO",
            "pontos_fortes": ["Liderança"],
            "gaps_identificados": [
                "ferramenta_especifica_1",
                "ferramenta_especifica_2",
                "metodologia_1",
                "<placeholder>"
            ],
            "gaps_falsos_ignorados": [],
            "plano_acao": ["⚠️ Melhorias necessárias"]
        })
        
        mock_chamar_gpt.return_value = resposta_so_placeholders
        mock_client = Mock()
        
        resultado = _analisar_com_llm(
            mock_client, 
            "CV gerente", 
            "Gerente de Projetos"
        )
        
        # Lista de gaps deve estar vazia após filtragem
        assert resultado['gaps_identificados'] == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
