"""
Serviço para API Google Gemini
"""

from google import genai
from google.genai.types import GenerateContentConfig, GoogleSearch, Tool
from .ai_service import AIService
import logging

logger = logging.getLogger("MultiAgentBlog")


class GeminiService(AIService):
    """Serviço para interagir com a API Gemini usando o novo Google GenAI SDK"""

    def __init__(self, api_key: str, max_retries: int = 3, enable_search: bool = False):
        """
        Inicializa o serviço Gemini

        Args:
            api_key: Chave da API Google
            max_retries: Número máximo de tentativas
            enable_search: Se True, habilita Google Search grounding
        """
        super().__init__(api_key, max_retries)
        self.client = genai.Client(api_key=api_key)
        self.enable_search = enable_search

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
        search_status = "com Google Search" if self.enable_search else "sem busca"
        logger.info(f"Chamando Gemini API - Modelo: {model} ({search_status})")

        try:
            # Configurar tools (Google Search se habilitado)
            tools = []
            if self.enable_search:
                tools.append(Tool(google_search=GoogleSearch()))
                logger.info("Google Search grounding habilitado para esta requisição")

            # Configurar geração
            config = GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                tools=tools if tools else None
            )

            # Gerar resposta
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=config
            )

            content = response.text

            logger.info(f"Gemini API respondeu com {len(content)} caracteres")

            return content

        except Exception as e:
            logger.error(f"Erro ao chamar Gemini API: {str(e)}")
            raise
