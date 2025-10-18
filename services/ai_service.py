"""
Interface base para serviços de IA
"""

from abc import ABC, abstractmethod
from typing import Optional
import logging
import time

logger = logging.getLogger("MultiAgentBlog")


class AIService(ABC):
    """Classe base para serviços de IA"""

    def __init__(self, api_key: str, max_retries: int = 3):
        """
        Inicializa o serviço de IA

        Args:
            api_key: Chave de API
            max_retries: Número máximo de tentativas em caso de erro
        """
        self.api_key = api_key
        self.max_retries = max_retries

    @abstractmethod
    def generate(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        Gera texto usando a API

        Args:
            prompt: Prompt para geração
            model: Nome do modelo
            temperature: Temperatura de geração
            max_tokens: Número máximo de tokens

        Returns:
            Texto gerado
        """
        pass

    def call_with_retry(self, prompt: str, model: str, temperature: float = 0.7, max_tokens: int = 4000) -> Optional[str]:
        """
        Chama a API com lógica de retry

        Args:
            prompt: Prompt para geração
            model: Nome do modelo
            temperature: Temperatura
            max_tokens: Máximo de tokens

        Returns:
            Resposta da API ou None
        """
        for attempt in range(self.max_retries):
            try:
                response = self.generate(prompt, model, temperature, max_tokens)
                return response

            except Exception as e:
                error_type = type(e).__name__

                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 5
                    logger.warning(f"Erro {error_type}. Tentativa {attempt + 1}/{self.max_retries}. Aguardando {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Falha após {self.max_retries} tentativas: {str(e)}")
                    raise

        return None
