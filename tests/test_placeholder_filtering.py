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
