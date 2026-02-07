"""
Testes unitários para os validadores do Protocolo Nóbile.
"""

import pytest
from core.validators import validar_cargo, validar_salario, validar_pdf, validar_arquivo_cv


class TestValidarArquivoCv:
    """Testes para a função validar_arquivo_cv."""
    
    def test_validar_arquivo_cv_formato_invalido(self):
        """Testa rejeição de formato inválido."""
        class FakeFile:
            name = "cv.exe"
            size = 1024
        
        valid, error = validar_arquivo_cv(FakeFile())
        assert not valid
        assert "não suportado" in error
    
    def test_validar_arquivo_cv_muito_grande(self):
        """Testa rejeição de arquivo grande."""
        class FakeFile:
            name = "cv.pdf"
            size = 20 * 1024 * 1024  # 20MB
        
        valid, error = validar_arquivo_cv(FakeFile())
        assert not valid
        assert "muito grande" in error
    
    def test_validar_arquivo_cv_valido(self):
        """Testa arquivo válido."""
        class FakeFile:
            name = "cv.docx"
            size = 500 * 1024  # 500KB
        
        valid, error = validar_arquivo_cv(FakeFile())
        assert valid
        assert error is None
    
    def test_validar_arquivo_cv_pdf(self):
        """Testa arquivo PDF válido."""
        class FakeFile:
            name = "curriculo.pdf"
            size = 2 * 1024 * 1024  # 2MB
        
        valid, error = validar_arquivo_cv(FakeFile())
        assert valid
        assert error is None
    
    def test_validar_arquivo_cv_txt(self):
        """Testa arquivo TXT válido."""
        class FakeFile:
            name = "resume.txt"
            size = 10 * 1024  # 10KB
        
        valid, error = validar_arquivo_cv(FakeFile())
        assert valid
        assert error is None
    
    def test_validar_arquivo_cv_doc(self):
        """Testa arquivo DOC válido."""
        class FakeFile:
            name = "cv.doc"
            size = 1 * 1024 * 1024  # 1MB
        
        valid, error = validar_arquivo_cv(FakeFile())
        assert valid
        assert error is None
    
    def test_validar_arquivo_cv_vazio(self):
        """Testa arquivo vazio."""
        class FakeFile:
            name = "cv.pdf"
            size = 100  # < 1KB
        
        valid, error = validar_arquivo_cv(FakeFile())
        assert not valid
        assert "muito pequeno ou vazio" in error
    
    def test_validar_arquivo_cv_none(self):
        """Testa arquivo None."""
        valid, error = validar_arquivo_cv(None)
        assert not valid
        assert "Nenhum arquivo fornecido" in error


class TestValidarCargo:
    """Testes para a função validar_cargo."""
    
    def test_validar_cargo_valido(self):
        """Testa cargo válido."""
        valido, erro = validar_cargo("Desenvolvedor Python")
        assert valido is True
        assert erro is None
    
    def test_validar_cargo_muito_curto(self):
        """Testa cargo com menos de 3 caracteres."""
        valido, erro = validar_cargo("AB")
        assert valido is False
        assert "pelo menos 3 caracteres" in erro
    
    def test_validar_cargo_muito_longo(self):
        """Testa cargo com mais de 100 caracteres."""
        cargo_longo = "A" * 101
        valido, erro = validar_cargo(cargo_longo)
        assert valido is False
        assert "no máximo 100 caracteres" in erro
    
    def test_validar_cargo_caracteres_invalidos(self):
        """Testa cargo com caracteres especiais inválidos."""
        valido, erro = validar_cargo("Dev@Python123")
        assert valido is False
        assert "caracteres inválidos" in erro
    
    def test_validar_cargo_com_hifen(self):
        """Testa cargo válido com hífen."""
        valido, erro = validar_cargo("Analista-Programador")
        assert valido is True
        assert erro is None
    
    def test_validar_cargo_com_parenteses(self):
        """Testa cargo válido com parênteses."""
        valido, erro = validar_cargo("Desenvolvedor (Senior)")
        assert valido is True
        assert erro is None
    
    def test_validar_cargo_vazio(self):
        """Testa cargo vazio."""
        valido, erro = validar_cargo("")
        assert valido is False
        assert "não pode ser vazio" in erro


class TestValidarSalario:
    """Testes para a função validar_salario."""
    
    def test_validar_salario_valido(self):
        """Testa conversão correta de salário simples."""
        valido, erro, valor = validar_salario("5000")
        assert valido is True
        assert erro is None
        assert valor == 5000.0
    
    def test_validar_salario_com_formatacao(self):
        """Testa salário com formatação brasileira."""
        valido, erro, valor = validar_salario("R$ 25.000,00")
        assert valido is True
        assert erro is None
        assert valor == 25000.0
    
    def test_validar_salario_muito_baixo(self):
        """Testa salário abaixo do mínimo."""
        valido, erro, valor = validar_salario("500")
        assert valido is False
        assert "no mínimo R$ 1.000" in erro
        assert valor is None
    
    def test_validar_salario_muito_alto(self):
        """Testa salário acima do máximo."""
        valido, erro, valor = validar_salario("1500000")
        assert valido is False
        assert "no máximo R$ 1.000.000" in erro
        assert valor is None
    
    def test_validar_salario_formato_invalido(self):
        """Testa formato de salário inválido."""
        valido, erro, valor = validar_salario("abc")
        assert valido is False
        assert "inválido" in erro
        assert valor is None
    
    def test_validar_salario_vazio(self):
        """Testa salário vazio."""
        valido, erro, valor = validar_salario("")
        assert valido is False
        assert "não pode ser vazio" in erro
        assert valor is None
    
    def test_validar_salario_com_espacos(self):
        """Testa salário com espaços."""
        valido, erro, valor = validar_salario("R$ 10.000")
        assert valido is True
        assert erro is None
        assert valor == 10000.0
