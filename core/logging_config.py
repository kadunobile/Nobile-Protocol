"""
Configuração centralizada do sistema de logging do Protocolo Nóbile.

Este módulo configura logging para arquivo e console com diferentes níveis,
rotação automática de logs por data, e criação automática do diretório de logs.
"""

import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


def setup_logging():
    """
    Configura o sistema de logging para o Protocolo Nóbile.
    
    Configura dois handlers:
    - Arquivo: Logs de nível DEBUG com rotação diária
    - Console: Logs de nível ERROR apenas
    
    Os logs são salvos na pasta logs/ com formato rotativo por data.
    """
    # Criar diretório de logs se não existir
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configurar logger raiz
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Remover handlers existentes para evitar duplicação
    logger.handlers.clear()
    
    # Formato estruturado com timestamp, módulo, nível e mensagem
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para arquivo (DEBUG) com rotação diária
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "nobile_protocol.log",
        when="midnight",
        interval=1,
        backupCount=30,  # Manter últimos 30 dias
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)
    
    # Handler para console (ERROR apenas)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # Log inicial indicando que o sistema foi inicializado
    logger.info("Sistema de logging inicializado com sucesso")
    
    return logger


# Inicializar logging automaticamente ao importar o módulo
logger = setup_logging()
