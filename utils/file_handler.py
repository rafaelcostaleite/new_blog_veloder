"""
Utilitários para manipulação de arquivos
"""

import os
from pathlib import Path
from typing import List
import json


def ensure_directories(directories: List[str]):
    """
    Garante que os diretórios existam

    Args:
        directories: Lista de caminhos de diretórios
    """
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)


def read_input_file(file_path: Path) -> str:
    """
    Lê o arquivo de entrada

    Args:
        file_path: Caminho do arquivo

    Returns:
        Conteúdo do arquivo
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def write_output_file(file_path: Path, content: str):
    """
    Escreve arquivo de saída

    Args:
        file_path: Caminho do arquivo
        content: Conteúdo a ser escrito
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)


def read_json_file(file_path: Path) -> dict:
    """
    Lê arquivo JSON

    Args:
        file_path: Caminho do arquivo JSON

    Returns:
        Dicionário com dados do JSON
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json_file(file_path: Path, data: dict):
    """
    Escreve arquivo JSON

    Args:
        file_path: Caminho do arquivo
        data: Dados a serem escritos
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_markdown_file(file_path: Path) -> str:
    """
    Lê arquivo markdown

    Args:
        file_path: Caminho do arquivo

    Returns:
        Conteúdo do arquivo markdown
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()
