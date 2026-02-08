"""
Testes unitários para validação de PDF do LinkedIn no módulo fase0_upload.
"""

import pytest
from ui.screens.fase0_upload import validar_pdf_linkedin


class TestValidarPdfLinkedin:
    """Testes para a função validar_pdf_linkedin."""
    
    def test_valido_com_linkedin_no_texto(self):
        """Testa que PDF com menção ao LinkedIn é aceito."""
        texto = """
        John Doe
        linkedin.com/in/johndoe
        
        Experience
        Senior Software Engineer at Tech Corp
        
        Education
        Bachelor's in Computer Science
        
        Skills
        Python, JavaScript, AWS
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is True
        assert resultado['motivo'] == ''
    
    def test_valido_com_estrutura_linkedin(self):
        """Testa que PDF com estrutura típica do LinkedIn é aceito."""
        texto = """
        Maria Silva
        
        Experience
        Desenvolvedora Full Stack na Empresa XYZ
        - Desenvolveu aplicações web
        
        Education
        Bacharelado em Ciência da Computação
        
        Skills
        Java, React, Node.js
        
        Languages
        Português, Inglês
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is True
        assert resultado['motivo'] == ''
    
    def test_valido_com_secoes_pt(self):
        """Testa que PDF com seções em português do LinkedIn é aceito."""
        texto = """
        João Santos
        
        Experiência
        Gerente de Projetos na ABC Ltda
        
        Formação
        MBA em Gestão de Projetos
        
        Competências
        Liderança, Scrum, Kanban
        
        Idiomas
        Português, Inglês, Espanhol
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is True
    
    def test_invalido_cv_tradicional(self):
        """Testa que CV tradicional brasileiro é rejeitado."""
        texto = """
        CURRICULUM VITAE
        
        Dados Pessoais:
        Nome: Carlos Silva
        Estado Civil: Casado
        
        Objetivo Profissional:
        Atuar como Analista de Sistemas
        
        Pretensão Salarial:
        R$ 5.000,00
        
        Experiência:
        - Trabalhou na empresa X
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is False
        assert 'CV tradicional' in resultado['motivo']
    
    def test_invalido_sem_estrutura(self):
        """Testa que PDF sem estrutura LinkedIn é rejeitado."""
        texto = """
        Este é apenas um texto qualquer
        sem nenhuma estrutura de currículo
        ou perfil profissional.
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is False
        assert 'não foi possível identificar' in resultado['motivo'].lower()
    
    def test_aviso_caso_ambiguo(self):
        """Testa que caso ambíguo retorna aviso."""
        texto = """
        Professional Profile
        
        Experience
        Software Developer
        
        Education
        Computer Science Degree
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is True
        assert resultado['motivo'] == 'aviso'
    
    def test_case_insensitive(self):
        """Testa que a validação é case-insensitive."""
        texto = """
        LINKEDIN.COM/IN/JOHNDOE
        
        EXPERIENCE
        Senior Developer
        
        EDUCATION
        Bachelor's Degree
        
        SKILLS
        Python, Java
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is True
    
    def test_secoes_mistas_pt_en(self):
        """Testa que PDF com seções mistas PT/EN é aceito."""
        texto = """
        Ana Costa
        linkedin.com/in/anacosta
        
        Experience
        Desenvolvedora na Empresa Y
        
        Formação Acadêmica
        Engenharia de Software
        
        Skills
        React, Node.js, MongoDB
        
        Certificações
        AWS Certified Developer
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is True
    
    def test_texto_vazio(self):
        """Testa comportamento com texto vazio."""
        resultado = validar_pdf_linkedin("")
        assert resultado['valido'] is False
    
    def test_apenas_uma_secao(self):
        """Testa que apenas uma seção LinkedIn não é suficiente."""
        texto = """
        John Doe
        
        Experience
        Some work experience here
        """
        resultado = validar_pdf_linkedin(texto)
        assert resultado['valido'] is False
