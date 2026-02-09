"""
Unit tests for salary banding module.
"""

import pytest
from core.salary_bands import (
    normalizar_cargo,
    detectar_porte_regiao,
    obter_banda_salarial,
    validar_salario_banda,
    formatar_banda_display,
)


class TestNormalizarCargo:
    """Tests for cargo normalization."""
    
    def test_normaliza_cargo_simples(self):
        """Test simple cargo normalization."""
        assert normalizar_cargo("Gerente de Vendas") == "gerente de vendas"
    
    def test_normaliza_cargo_com_espacos(self):
        """Test cargo with extra spaces."""
        assert normalizar_cargo("  Coordenador de Compras  ") == "coordenador de compras"
    
    def test_normaliza_cargo_vazio(self):
        """Test empty cargo."""
        assert normalizar_cargo("") == ""
    
    def test_normaliza_cargo_none(self):
        """Test None cargo."""
        assert normalizar_cargo(None) == ""


class TestDetectarPorteRegiao:
    """Tests for porte/região detection."""
    
    def test_detecta_sao_paulo(self):
        """Test detection of São Paulo."""
        assert detectar_porte_regiao("São Paulo, SP") == "sp_capitais"
    
    def test_detecta_sp_abreviado(self):
        """Test detection of SP abbreviation."""
        assert detectar_porte_regiao("SP") == "sp_capitais"
    
    def test_detecta_rio_de_janeiro(self):
        """Test detection of Rio de Janeiro."""
        assert detectar_porte_regiao("Rio de Janeiro") == "sp_capitais"
    
    def test_detecta_capital_outras(self):
        """Test detection of other capitals."""
        assert detectar_porte_regiao("Curitiba") == "sp_capitais"
        assert detectar_porte_regiao("Porto Alegre") == "sp_capitais"
        assert detectar_porte_regiao("Brasília") == "sp_capitais"
    
    def test_detecta_interior(self):
        """Test detection of interior cities (defaults to 'default')."""
        assert detectar_porte_regiao("Campinas") == "default"
        assert detectar_porte_regiao("Sorocaba") == "default"
    
    def test_detecta_remoto(self):
        """Test remote location."""
        assert detectar_porte_regiao("Remoto") == "default"
    
    def test_detecta_vazio(self):
        """Test empty location."""
        assert detectar_porte_regiao("") == "default"


class TestObterBandaSalarial:
    """Tests for salary band retrieval."""
    
    def test_obtem_banda_coordenador_compras_default(self):
        """Test band for Coordenador de Compras with default category."""
        banda = obter_banda_salarial("Coordenador de Compras")
        
        assert banda['min'] == 14000
        assert banda['max'] == 18000
        assert banda['median'] == 16000
        assert banda['cargo'] == "Coordenador de Compras"
        assert banda['category'] == 'default'
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_coordenador_compras_pequena(self):
        """Test band for Coordenador de Compras in small companies."""
        banda = obter_banda_salarial("Coordenador de Compras", categoria='pequena')
        
        assert banda['min'] == 12000
        assert banda['max'] == 15000
        assert banda['median'] == 13500
        assert banda['category'] == 'pequena'
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_coordenador_compras_grande(self):
        """Test band for Coordenador de Compras in large companies."""
        banda = obter_banda_salarial("Coordenador de Compras", categoria='grande')
        
        assert banda['min'] == 16000
        assert banda['max'] == 20000
        assert banda['median'] == 18000
        assert banda['category'] == 'grande'
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_coordenador_compras_sp(self):
        """Test band for Coordenador de Compras in SP/capitals."""
        banda = obter_banda_salarial("Coordenador de Compras", categoria='sp_capitais')
        
        assert banda['min'] == 15000
        assert banda['max'] == 19000
        assert banda['median'] == 17000
        assert banda['category'] == 'sp_capitais'
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_gerente_revops_default(self):
        """Test band for Gerente de RevOps with default category."""
        banda = obter_banda_salarial("Gerente de RevOps")
        
        assert banda['min'] == 18000
        assert banda['max'] == 24000
        assert banda['median'] == 21000
        assert banda['cargo'] == "Gerente de RevOps"
        assert banda['category'] == 'default'
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_gerente_revops_media(self):
        """Test band for Gerente de RevOps in medium companies."""
        banda = obter_banda_salarial("Gerente de RevOps", categoria='media')
        
        assert banda['min'] == 18000
        assert banda['max'] == 24000
        assert banda['median'] == 21000
        assert banda['category'] == 'media'
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_gerente_revops_multi(self):
        """Test band for Gerente de RevOps in multinationals."""
        banda = obter_banda_salarial("Gerente de RevOps", categoria='multi')
        
        assert banda['min'] == 20000
        assert banda['max'] == 28000
        assert banda['median'] == 24000
        assert banda['category'] == 'multi'
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_cargo_nao_mapeado(self):
        """Test fallback band for unmapped cargo."""
        banda = obter_banda_salarial("Analista de Dados Quânticos")
        
        assert banda['min'] == 5000
        assert banda['max'] == 25000
        assert banda['median'] == 12000
        assert banda['cargo'] == "Analista de Dados Quânticos"
        assert banda['category'] == 'estimativa'
        assert banda['is_fallback'] is True
    
    def test_obtem_banda_coordenadora_feminino(self):
        """Test band for Coordenadora (feminine form)."""
        banda = obter_banda_salarial("Coordenadora de Compras")
        
        assert banda['min'] == 14000
        assert banda['max'] == 18000
        assert banda['median'] == 16000
        assert banda['is_fallback'] is False
    
    def test_obtem_banda_case_insensitive(self):
        """Test case-insensitive cargo lookup."""
        banda = obter_banda_salarial("GERENTE DE REVOPS")
        
        assert banda['min'] == 18000
        assert banda['max'] == 24000
        assert banda['median'] == 21000
        assert banda['is_fallback'] is False


class TestValidarSalarioBanda:
    """Tests for salary validation against bands."""
    
    def test_valida_salario_dentro_banda(self):
        """Test salary within band."""
        resultado = validar_salario_banda(
            "16000",
            "Coordenador de Compras",
            "São Paulo"
        )
        
        assert resultado['valor'] == 16000.0
        assert resultado['dentro_banda'] is True
        assert resultado['mensagem'] == ''
        assert resultado['nivel'] == 'ok'
    
    def test_valida_salario_no_limite(self):
        """Test salary at band maximum."""
        resultado = validar_salario_banda(
            "18000",
            "Coordenador de Compras"
        )
        
        assert resultado['valor'] == 18000.0
        assert resultado['dentro_banda'] is True
        assert resultado['nivel'] == 'ok'
    
    def test_valida_salario_pouco_acima(self):
        """Test salary slightly above band (up to 20%)."""
        resultado = validar_salario_banda(
            "20000",  # 11% above 18000
            "Coordenador de Compras"
        )
        
        assert resultado['valor'] == 20000.0
        assert resultado['dentro_banda'] is False
        assert resultado['nivel'] == 'acima'
        assert "acima da média de mercado" in resultado['mensagem']
        # Brazilian currency format uses periods for thousands
        assert "R$ 14.000,00 - R$ 18.000,00" in resultado['mensagem']
    
    def test_valida_salario_muito_acima(self):
        """Test salary well above band (>20%)."""
        resultado = validar_salario_banda(
            "30000",  # 67% above 18000
            "Coordenador de Compras"
        )
        
        assert resultado['valor'] == 30000.0
        assert resultado['dentro_banda'] is False
        assert resultado['nivel'] == 'muito_acima'
        assert "muito acima da média de mercado" in resultado['mensagem']
        assert "dificultar significativamente" in resultado['mensagem']
    
    def test_valida_salario_formatado_br(self):
        """Test salary with Brazilian formatting."""
        resultado = validar_salario_banda(
            "R$ 25.000,00",
            "Gerente de RevOps"
        )
        
        assert resultado['valor'] == 25000.0
        # 25000 is slightly above 24000 (4% over)
        assert resultado['dentro_banda'] is False
        assert resultado['nivel'] == 'acima'
    
    def test_valida_salario_invalido(self):
        """Test invalid salary string."""
        resultado = validar_salario_banda(
            "abc",
            "Coordenador de Compras"
        )
        
        assert resultado['valor'] is None
        assert resultado['nivel'] == 'invalido'
        assert resultado['banda'] is None
    
    def test_valida_salario_cargo_nao_mapeado(self):
        """Test validation with unmapped cargo."""
        resultado = validar_salario_banda(
            "50000",
            "Arquiteto de Blockchain"
        )
        
        assert resultado['valor'] == 50000.0
        assert resultado['dentro_banda'] is False
        assert resultado['nivel'] == 'muito_acima'
        assert "estimativa" in resultado['mensagem']
    
    def test_valida_salario_gerente_revops_sp(self):
        """Test salary validation for Gerente RevOps in SP."""
        resultado = validar_salario_banda(
            "23000",
            "Gerente de RevOps",
            "São Paulo"
        )
        
        # SP band for RevOps: 20-26k
        assert resultado['valor'] == 23000.0
        assert resultado['dentro_banda'] is True
        assert resultado['nivel'] == 'ok'
    
    def test_valida_salario_coordenador_pequena_empresa(self):
        """Test salary for Coordenador in small company context."""
        # Note: This test uses default detection, which doesn't detect 'pequena' from location
        # In real usage, porte would come from user profile or other context
        resultado = validar_salario_banda(
            "14000",
            "Coordenador de Compras",
            "Interior SP"
        )
        
        assert resultado['valor'] == 14000.0
        assert resultado['dentro_banda'] is True
        assert resultado['nivel'] == 'ok'


class TestFormatarBandaDisplay:
    """Tests for salary band display formatting."""
    
    def test_formata_banda_coordenador_default(self):
        """Test formatting for Coordenador default band."""
        banda = obter_banda_salarial("Coordenador de Compras")
        texto = formatar_banda_display(banda)
        
        assert "R$ 14.000 - R$ 18.000" in texto
        assert "mediana ~R$ 16.000" in texto
        assert "*[estimativa]*" not in texto
    
    def test_formata_banda_gerente_revops(self):
        """Test formatting for Gerente RevOps band."""
        banda = obter_banda_salarial("Gerente de RevOps")
        texto = formatar_banda_display(banda)
        
        assert "R$ 18.000 - R$ 24.000" in texto
        assert "mediana ~R$ 21.000" in texto
    
    def test_formata_banda_fallback(self):
        """Test formatting for fallback band."""
        banda = obter_banda_salarial("Cargo Não Mapeado")
        texto = formatar_banda_display(banda)
        
        assert "R$ 5.000 - R$ 25.000" in texto
        assert "*[estimativa]*" in texto
    
    def test_formata_banda_com_decimais(self):
        """Test formatting uses period for thousands separator."""
        banda = obter_banda_salarial("Gerente de RevOps", categoria='multi')
        texto = formatar_banda_display(banda)
        
        # Should have periods as thousands separator (BR format)
        assert "R$ 20.000" in texto
        assert "R$ 28.000" in texto
        assert "R$ 24.000" in texto
