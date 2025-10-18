"""
Serviço para API Google Gemini
"""

import google.generativeai as genai
from .ai_service import AIService
import logging

logger = logging.getLogger("MultiAgentBlog")


class GeminiService(AIService):
    """Serviço para interagir com a API Gemini"""

    def __init__(self, api_key: str, max_retries: int = 3):
        """
        Inicializa o serviço Gemini

        Args:
            api_key: Chave da API Google
            max_retries: Número máximo de tentativas
        """
        super().__init__(api_key, max_retries)
        genai.configure(api_key=api_key)

    def generate(self, prompt: str, model: str = "gemini-pro", temperature: float = 0.7, max_tokens: int = 4000) -> str:
        """
        Gera texto usando Gemini

        Args:
            prompt: Prompt para geração
            model: Modelo Gemini a usar
            temperature: Temperatura (0-1)
            max_tokens: Máximo de tokens

        Returns:
            Texto gerado
        """
        logger.info(f"Chamando Gemini API - Modelo: {model}")

        try:
            # Configurar modelo
            generation_config = {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            }

            model_instance = genai.GenerativeModel(
                model_name=model,
                generation_config=generation_config
            )

            # Gerar resposta
            response = model_instance.generate_content(prompt)
            content = response.text

            logger.info(f"Gemini API respondeu com {len(content)} caracteres")

            return content

        except Exception as e:
            logger.error(f"Erro ao chamar Gemini API: {str(e)}")
            raise
