"""
Sistema de Logs do Multi-Agent Blog System
"""

import logging
import os
from datetime import datetime
from pathlib import Path
import shutil


def clean_logs(logs_dir: str = "logs", errors_dir: str = "errors"):
    """
    Limpa logs e erros anteriores

    Args:
        logs_dir: Diretório de logs
        errors_dir: Diretório de erros
    """
    # Limpar logs
    if os.path.exists(logs_dir):
        for file in Path(logs_dir).glob("*.log"):
            file.unlink()

    # Limpar erros
    if os.path.exists(errors_dir):
        for file in Path(errors_dir).glob("*.log"):
            file.unlink()


def setup_logger(log_level: str = "INFO", logs_dir: str = "logs", errors_dir: str = "errors"):
    """
    Configura o sistema de logs

    Args:
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR)
        logs_dir: Diretório para logs gerais
        errors_dir: Diretório para logs de erro

    Returns:
        Logger configurado
    """
    # Criar diretórios se não existirem
    Path(logs_dir).mkdir(exist_ok=True)
    Path(errors_dir).mkdir(exist_ok=True)

    # Nome do arquivo de log com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = Path(logs_dir) / f"app_{timestamp}.log"
    error_file = Path(errors_dir) / f"error_{timestamp}.log"

    # Configurar logger principal
    logger = logging.getLogger("MultiAgentBlog")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Remover handlers existentes
    logger.handlers.clear()

    # Formato dos logs
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo de log
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Handler para arquivo de erros (apenas erros)
    error_handler = logging.FileHandler(error_file, encoding='utf-8')
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    logger.addHandler(error_handler)

    return logger
