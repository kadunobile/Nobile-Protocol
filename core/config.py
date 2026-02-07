import os
import importlib
import logging
from dataclasses import dataclass
from typing import Optional


@dataclass
class Config:
    """
    Configuração centralizada do Protocolo Nóbile.
    
    Attributes:
        OPENAI_API_KEY: Chave da API OpenAI
        MODEL: Modelo GPT a ser utilizado
        TEMPERATURE: Temperatura para geração de texto
        MAX_TOKENS: Número máximo de tokens por resposta
        TIMEOUT: Timeout em segundos para requisições
        MAX_RETRIES: Número máximo de tentativas em caso de erro
        LOG_LEVEL: Nível de logging (DEBUG, INFO, WARNING, ERROR)
        MAX_PDF_SIZE_MB: Tamanho máximo de PDF em MB
    """
    OPENAI_API_KEY: Optional[str] = None
    MODEL: str = "gpt-4o"
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 4000
    TIMEOUT: int = 30
    MAX_RETRIES: int = 3
    LOG_LEVEL: str = "INFO"
    MAX_PDF_SIZE_MB: int = 10
    
    @classmethod
    def from_env(cls) -> "Config":
        """
        Carrega configuração a partir de variáveis de ambiente.
        
        Returns:
            Instância de Config com valores do ambiente
        """
        return cls(
            OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY"),
            MODEL=os.environ.get("OPENAI_MODEL", "gpt-4o"),
            TEMPERATURE=float(os.environ.get("OPENAI_TEMPERATURE", "0.7")),
            MAX_TOKENS=int(os.environ.get("OPENAI_MAX_TOKENS", "4000")),
            TIMEOUT=int(os.environ.get("OPENAI_TIMEOUT", "30")),
            MAX_RETRIES=int(os.environ.get("OPENAI_MAX_RETRIES", "3")),
            LOG_LEVEL=os.environ.get("LOG_LEVEL", "INFO"),
            MAX_PDF_SIZE_MB=int(os.environ.get("MAX_PDF_SIZE_MB", "10"))
        )
    
    def validate(self) -> None:
        """
        Valida os valores críticos da configuração.
        
        Raises:
            ValueError: Se algum valor crítico for inválido
        """
        if self.TEMPERATURE < 0 or self.TEMPERATURE > 2:
            raise ValueError(f"TEMPERATURE deve estar entre 0 e 2, recebido: {self.TEMPERATURE}")
        
        if self.MAX_TOKENS < 1 or self.MAX_TOKENS > 128000:
            raise ValueError(f"MAX_TOKENS deve estar entre 1 e 128000, recebido: {self.MAX_TOKENS}")
        
        if self.TIMEOUT < 1:
            raise ValueError(f"TIMEOUT deve ser maior que 0, recebido: {self.TIMEOUT}")
        
        if self.MAX_RETRIES < 1 or self.MAX_RETRIES > 10:
            raise ValueError(f"MAX_RETRIES deve estar entre 1 e 10, recebido: {self.MAX_RETRIES}")
        
        if self.MAX_PDF_SIZE_MB < 1 or self.MAX_PDF_SIZE_MB > 100:
            raise ValueError(f"MAX_PDF_SIZE_MB deve estar entre 1 e 100, recebido: {self.MAX_PDF_SIZE_MB}")


# Instância global de configuração
config = Config.from_env()


def setup_environment():
    """
    Configura o ambiente carregando variáveis de configuração.
    
    Tenta carregar de módulo config.py local e de arquivo .env
    """
    logger = logging.getLogger(__name__)
    
    try:
        cfg = importlib.import_module("config")
        if hasattr(cfg, "OPENAI_API_KEY"):
            os.environ["OPENAI_API_KEY"] = cfg.OPENAI_API_KEY
            logger.info("API key carregada de config.py local")
    except Exception as e:
        logger.debug(f"Não foi possível carregar config.py: {e}")

    try:
        from dotenv import load_dotenv
        load_dotenv(override=True)
        logger.info("Variáveis de ambiente carregadas de .env")
    except Exception as e:
        logger.debug(f"Não foi possível carregar .env: {e}")
    
    # Recarregar config global após setup do ambiente
    global config
    config = Config.from_env()
    
    try:
        config.validate()
        logger.info("Configuração validada com sucesso")
    except ValueError as e:
        logger.warning(f"Aviso na validação da configuração: {e}")
