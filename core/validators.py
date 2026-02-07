"""
Validadores de dados para o Protocolo Nóbile.

Este módulo contém funções de validação para entrada de dados do usuário,
incluindo validação de cargos, salários e arquivos PDF.
"""

import re
from typing import Tuple, Optional


def validar_arquivo_cv(arquivo) -> Tuple[bool, Optional[str]]:
    """
    Valida arquivo de CV (formato e tamanho).
    
    Args:
        arquivo: Arquivo uploaded do Streamlit
    
    Returns:
        Tuple[bool, Optional[str]]: (válido, mensagem_erro)
    """
    if not arquivo:
        return False, "Nenhum arquivo fornecido"
    
    # Valida extensão
    extensao = arquivo.name.split('.')[-1].lower()
    formatos_validos = ['pdf', 'docx', 'doc', 'txt']
    
    if extensao not in formatos_validos:
        return False, f"Formato .{extensao} não suportado. Use: {', '.join(formatos_validos)}"
    
    # Valida tamanho (máximo 15MB para Word que pode ser maior)
    tamanho_mb = arquivo.size / (1024 * 1024)
    max_mb = 15
    min_size_bytes = 1024  # 1KB mínimo
    
    if tamanho_mb > max_mb:
        return False, f"Arquivo muito grande ({tamanho_mb:.1f}MB). Máximo: {max_mb}MB"
    
    if arquivo.size < min_size_bytes:
        return False, "Arquivo muito pequeno ou vazio"
    
    return True, None


def validar_cargo(cargo: str) -> Tuple[bool, Optional[str]]:
    """
    Valida o nome de um cargo profissional.
    
    Args:
        cargo: Nome do cargo a ser validado
        
    Returns:
        Tupla contendo:
        - bool: True se válido, False caso contrário
        - str: Mensagem de erro se inválido, None se válido
        
    Examples:
        >>> validar_cargo("Desenvolvedor Python")
        (True, None)
        >>> validar_cargo("AB")
        (False, "Cargo deve ter pelo menos 3 caracteres")
    """
    if not cargo or not isinstance(cargo, str):
        return False, "Cargo não pode ser vazio"
    
    cargo = cargo.strip()
    
    # Verificar comprimento mínimo
    if len(cargo) < 3:
        return False, "Cargo deve ter pelo menos 3 caracteres"
    
    # Verificar comprimento máximo
    if len(cargo) > 100:
        return False, "Cargo deve ter no máximo 100 caracteres"
    
    # Aceitar apenas letras, espaços, hífen, barra e parênteses
    pattern = r'^[a-zA-ZÀ-ÿ\s\-/()]+$'
    if not re.match(pattern, cargo):
        return False, "Cargo contém caracteres inválidos. Use apenas letras, espaços, hífen, barra ou parênteses"
    
    return True, None


def validar_salario(salario: str) -> Tuple[bool, Optional[str], Optional[float]]:
    """
    Valida e converte uma string de salário para float.
    
    Remove formatação monetária (R$, espaços) e valida o range de valores.
    
    Args:
        salario: String representando o salário (ex: "R$ 5.000,00" ou "5000")
        
    Returns:
        Tupla contendo:
        - bool: True se válido, False caso contrário
        - str: Mensagem de erro se inválido, None se válido
        - float: Valor convertido se válido, None se inválido
        
    Examples:
        >>> validar_salario("R$ 5.000,00")
        (True, None, 5000.0)
        >>> validar_salario("500")
        (False, "Salário deve ser no mínimo R$ 1.000", None)
    """
    if not salario or not isinstance(salario, str):
        return False, "Salário não pode ser vazio", None
    
    # Remover formatação
    salario_limpo = salario.strip()
    
    # Remover R$ e espaços
    salario_limpo = re.sub(r'R\$\s*', '', salario_limpo)
    salario_limpo = salario_limpo.replace(' ', '')
    
    # Substituir separadores brasileiros por formato padrão
    # Remover pontos (separadores de milhares)
    salario_limpo = salario_limpo.replace('.', '')
    # Trocar vírgula (decimal) por ponto
    salario_limpo = salario_limpo.replace(',', '.')
    
    # Tentar converter para float
    try:
        valor = float(salario_limpo)
    except ValueError:
        return False, "Formato de salário inválido", None
    
    # Validar range mínimo
    if valor < 1000:
        return False, "Salário deve ser no mínimo R$ 1.000", None
    
    # Validar range máximo
    if valor > 1000000:
        return False, "Salário deve ser no máximo R$ 1.000.000", None
    
    return True, None, valor


def validar_pdf(arquivo) -> Tuple[bool, Optional[str]]:
    """
    Valida um arquivo PDF uploadado.
    
    Verifica extensão, tamanho e se o arquivo não está corrompido.
    
    Args:
        arquivo: Objeto de arquivo do Streamlit (UploadedFile)
        
    Returns:
        Tupla contendo:
        - bool: True se válido, False caso contrário
        - str: Mensagem de erro se inválido, None se válido
        
    Examples:
        >>> validar_pdf(uploaded_file)
        (True, None)
    """
    if arquivo is None:
        return False, "Nenhum arquivo foi enviado"
    
    # Verificar extensão
    nome_arquivo = getattr(arquivo, 'name', '')
    if not nome_arquivo.lower().endswith('.pdf'):
        return False, "Arquivo deve ter extensão .pdf"
    
    # Verificar tamanho (10MB = 10 * 1024 * 1024 bytes)
    tamanho_max_bytes = 10 * 1024 * 1024
    
    # Tentar obter o tamanho do arquivo
    try:
        # Para UploadedFile do Streamlit
        if hasattr(arquivo, 'size'):
            tamanho = arquivo.size
        elif hasattr(arquivo, 'getbuffer'):
            tamanho = len(arquivo.getbuffer())
        else:
            # Fallback: tentar ler e verificar
            arquivo.seek(0, 2)  # Ir para o final
            tamanho = arquivo.tell()
            arquivo.seek(0)  # Voltar ao início
    except Exception as e:
        return False, f"Erro ao verificar tamanho do arquivo: {str(e)}"
    
    if tamanho > tamanho_max_bytes:
        tamanho_mb = tamanho / (1024 * 1024)
        return False, f"Arquivo muito grande ({tamanho_mb:.1f}MB). Máximo permitido: 10MB"
    
    # Verificar se o arquivo não está vazio
    if tamanho == 0:
        return False, "Arquivo PDF está vazio"
    
    # Verificar se arquivo não está corrompido (tentativa básica)
    try:
        # Tentar ler os primeiros bytes para verificar header PDF
        arquivo.seek(0)
        header = arquivo.read(5)
        arquivo.seek(0)
        
        if not header.startswith(b'%PDF-'):
            return False, "Arquivo não é um PDF válido ou está corrompido"
    except Exception as e:
        return False, f"Erro ao validar arquivo: {str(e)}"
    
    return True, None
