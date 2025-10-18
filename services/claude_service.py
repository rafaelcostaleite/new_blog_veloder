"""
Serviço para API Claude (Anthropic)
"""

from anthropic import Anthropic
from .ai_service import AIService
import logging

logger = logging.getLogger("MultiAgentBlog")


class ClaudeService(AIService):
    """Serviço para interagir com a API Claude"""

    def __init__(self, api_key: str, max_retries: int = 3):
        """
        Inicializa o serviço Claude

        Args:
            api_key: Chave da API Anthropic
            max_retries: Número máximo de tentativas
        """
        super().__init__(api_key, max_retries)
        self.client = Anthropic(api_key=api_key)

    def generate(self, prompt: str, model: str = "claude-sonnet-4-20250514", temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        Gera texto usando Claude

        Args:
            prompt: Prompt para geração
            model: Modelo Claude a usar
            temperature: Temperatura (0-1)
            max_tokens: Máximo de tokens

        Returns:
            Texto gerado
        """
        logger.info(f"Chamando Claude API - Modelo: {model}")

        try:
            response = self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Extrair texto da resposta
            content = response.content[0].text
            logger.info(f"Claude API respondeu com {len(content)} caracteres")

            return content

        except Exception as e:
            logger.error(f"Erro ao chamar Claude API: {str(e)}")
            raise
