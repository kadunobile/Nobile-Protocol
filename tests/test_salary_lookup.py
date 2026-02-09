"""
Unit tests for salary lookup module.
"""

import pytest
from core.salary_lookup import (
    _normalizar_cargo_para_slug,
    _extrair_valor_salario,
    formatar_dados_salariais_para_prompt,
)


class TestNormalizarCargoParaSlug:
    """Tests for cargo slug normalization."""
    
    def test_normaliza_cargo_simples(self):
        """Test simple cargo slug normalization."""
        assert _normalizar_cargo_para_slug("Coordenador de Compras") == "coordenador-de-compras"
    
    def test_normaliza_cargo_com_espacos_extras(self):
        """Test cargo with extra spaces."""
        assert _normalizar_cargo_para_slug("  Gerente  de  RevOps  ") == "gerente-de-revops"
    
    def test_normaliza_cargo_com_caracteres_especiais(self):
        """Test cargo with special characters."""
        # Note: Accented characters are preserved in URL slugs
        assert _normalizar_cargo_para_slug("Analista (Júnior)") == "analista-júnior"
    
    def test_normaliza_cargo_vazio(self):
        """Test empty cargo."""
        assert _normalizar_cargo_para_slug("") == ""
    
    def test_normaliza_cargo_com_numeros(self):
        """Test cargo with numbers."""
        assert _normalizar_cargo_para_slug("Developer 2") == "developer-2"


class TestExtrairValorSalario:
    """Tests for salary value extraction."""
    
    def test_extrai_valor_com_rs(self):
        """Test extraction with R$ prefix."""
        assert _extrair_valor_salario("R$ 8.774,00") == 8774.0
    
    def test_extrai_valor_sem_rs(self):
        """Test extraction without R$ prefix."""
        assert _extrair_valor_salario("8.774,50") == 8774.5
    
    def test_extrai_valor_sem_decimais(self):
        """Test extraction without decimal places."""
        assert _extrair_valor_salario("R$ 14.500") == 14500.0
    
    def test_extrai_valor_com_espacos(self):
        """Test extraction with extra spaces."""
        assert _extrair_valor_salario("  R$  8.774,00  ") == 8774.0
    
    def test_extrai_valor_invalido(self):
        """Test extraction with invalid value."""
        assert _extrair_valor_salario("abc") is None
    
    def test_extrai_valor_vazio(self):
        """Test extraction with empty string."""
        assert _extrair_valor_salario("") is None
    
    def test_extrai_valor_none(self):
        """Test extraction with None."""
        assert _extrair_valor_salario(None) is None


class TestFormatarDadosSalariaisParaPrompt:
    """Tests for salary data prompt formatting."""
    
    def test_formata_dados_completos(self):
        """Test formatting with complete data."""
        dados = {
            'piso': 6500.0,
            'media': 8774.0,
            'teto': 12000.0,
            'fonte': 'salario.com.br (CAGED/MTE)'
        }
        texto = formatar_dados_salariais_para_prompt(dados)
        
        assert "DADOS SALARIAIS REAIS DO MERCADO" in texto
        assert "salario.com.br (CAGED/MTE)" in texto
        assert "R$" in texto
        # Check for Brazilian format (periods for thousands)
        assert "6.500,00" in texto
        assert "8.774,00" in texto
        assert "12.000,00" in texto
    
    def test_formata_dados_none(self):
        """Test formatting with None data."""
        texto = formatar_dados_salariais_para_prompt(None)
        assert texto == ""
    
    def test_formata_dados_vazios(self):
        """Test formatting with empty dict."""
        dados = {}
        texto = formatar_dados_salariais_para_prompt(dados)
        
        # Empty dict is treated as falsy, should return empty string
        assert texto == ""


# Note: We're not testing buscar_salario_real() because it makes external HTTP requests
# In a real production environment, you would mock the requests to test the scraping logic
