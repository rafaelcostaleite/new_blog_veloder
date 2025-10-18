"""
Utilitários de validação
"""

from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger("MultiAgentBlog")


def validate_api_keys(api_keys: Dict[str, Optional[str]]) -> bool:
    """
    Valida se as API keys estão configuradas

    Args:
        api_keys: Dicionário com as chaves de API

    Returns:
        True se todas as chaves estão configuradas, False caso contrário
    """
    missing_keys = [key for key, value in api_keys.items() if not value]

    if missing_keys:
        logger.error(f"API keys ausentes: {', '.join(missing_keys)}")
        logger.info("Configure as chaves no arquivo .env")
        return False

    return True


def validate_input_file(file_path: Path) -> bool:
    """
    Valida o formato do arquivo de entrada

    Args:
        file_path: Caminho do arquivo

    Returns:
        True se o formato está correto, False caso contrário
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Verificar se contém as palavras-chave obrigatórias
        if 'Fluxo:' not in content:
            logger.error("Arquivo de entrada deve conter 'Fluxo:'")
            return False

        if 'Assunto:' not in content:
            logger.error("Arquivo de entrada deve conter 'Assunto:'")
            return False

        return True

    except Exception as e:
        logger.error(f"Erro ao validar arquivo de entrada: {str(e)}")
        return False


def validate_agent_output(output: dict, expected_keys: list) -> bool:
    """
    Valida o output de um agente

    Args:
        output: Output do agente
        expected_keys: Chaves esperadas no output

    Returns:
        True se o output é válido, False caso contrário
    """
    if not isinstance(output, dict):
        logger.error("Output do agente deve ser um dicionário")
        return False

    missing_keys = [key for key in expected_keys if key not in output]

    if missing_keys:
        logger.error(f"Output do agente está faltando as chaves: {', '.join(missing_keys)}")
        return False

    return True
