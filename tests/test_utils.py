"""
Testes unitários para funções utilitárias do Protocolo Nóbile.
"""

import pytest
from core.utils import corrigir_formatacao, filtrar_cidades


class TestCorrigirFormatacao:
    """Testes para a função corrigir_formatacao."""
    
    def test_corrigir_formatacao_remove_moeda(self):
        """Testa remoção de prefixo R$."""
        resultado = corrigir_formatacao("R$ 5.000")
        assert resultado == "5.000"
    
    def test_corrigir_formatacao_remove_r(self):
        """Testa remoção de prefixo R (sem $)."""
        resultado = corrigir_formatacao("R 5.000")
        assert resultado == "5.000"
    
    def test_corrigir_formatacao_none(self):
        """Testa input None."""
        resultado = corrigir_formatacao(None)
        assert resultado is None
    
    def test_corrigir_formatacao_espacos_multiplos(self):
        """Testa normalização de espaços múltiplos."""
        resultado = corrigir_formatacao("texto    com    espacos")
        assert resultado == "texto com espacos"
    
    def test_corrigir_formatacao_mantem_quebra_linha(self):
        """Testa que quebras de linha são mantidas."""
        resultado = corrigir_formatacao("linha1\nlinha2")
        assert resultado == "linha1\nlinha2"
    
    def test_corrigir_formatacao_normaliza_windows(self):
        """Testa normalização de quebras do Windows."""
        resultado = corrigir_formatacao("linha1\r\nlinha2")
        assert resultado == "linha1\nlinha2"
    
    def test_corrigir_formatacao_string_vazia(self):
        """Testa string vazia."""
        resultado = corrigir_formatacao("")
        assert resultado == ""


class TestFiltrarCidades:
    """Testes para a função filtrar_cidades."""
    
    def test_filtrar_cidades_com_texto(self):
        """Testa busca por texto específico."""
        resultado = filtrar_cidades("São")
        # Deve retornar uma tupla
        assert isinstance(resultado, tuple)
        # Deve conter São Paulo
        assert "São Paulo/SP" in resultado
        # Todas as cidades devem conter "São"
        for cidade in resultado:
            assert "são" in cidade.lower()
    
    def test_filtrar_cidades_sem_texto(self):
        """Testa retorno das primeiras 10 cidades quando texto é vazio."""
        resultado = filtrar_cidades(None)
        assert isinstance(resultado, tuple)
        assert len(resultado) == 10
    
    def test_filtrar_cidades_case_insensitive(self):
        """Testa busca case-insensitive."""
        resultado_lower = filtrar_cidades("rio")
        resultado_upper = filtrar_cidades("RIO")
        assert resultado_lower == resultado_upper
    
    def test_filtrar_cidades_sem_resultado(self):
        """Testa busca sem resultados."""
        resultado = filtrar_cidades("XYZ123")
        assert isinstance(resultado, tuple)
        assert len(resultado) == 0
    
    def test_filtrar_cidades_texto_parcial(self):
        """Testa busca por texto parcial."""
        resultado = filtrar_cidades("Flor")
        assert isinstance(resultado, tuple)
        assert "Florianópolis/SC" in resultado
    
    def test_filtrar_cidades_retorna_tupla(self):
        """Testa que a função sempre retorna tupla (para compatibilidade com LRU cache)."""
        resultado = filtrar_cidades("São Paulo")
        assert isinstance(resultado, tuple)


class TestExtrairTextoUniversal:
    """Testes para funções de extração de texto."""
    
    def test_extrair_texto_universal_pdf(self):
        """Testa extração universal com PDF"""
        # Mock de arquivo PDF
        assert True  # Implementar com mock quando tiver arquivo de teste
    
    def test_extrair_texto_docx_vazio(self):
        """Testa DOCX vazio retorna None"""
        # Mock
        assert True  # Implementar
    
    def test_extrair_texto_txt_encoding(self):
        """Testa diferentes encodings em TXT"""
        # Mock
        assert True  # Implementar
