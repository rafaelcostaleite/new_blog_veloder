"""
Factory para criação de agentes
"""

import os
from pathlib import Path
from typing import Dict
import json
import logging
import configparser

from services.claude_service import ClaudeService
from services.gemini_service import GeminiService
from utils.file_handler import read_json_file, read_markdown_file

logger = logging.getLogger("MultiAgentBlog")


class AgentFactory:
    """Factory para criar e configurar agentes"""

    def __init__(self, anthropic_key: str, google_key: str, config: configparser.ConfigParser = None):
        """
        Inicializa a factory

        Args:
            anthropic_key: Chave da API Anthropic
            google_key: Chave da API Google
            config: Configuração do sistema
        """
        self.anthropic_key = anthropic_key
        self.google_key = google_key
        self.config = config
        self.log_agent = config.getboolean('logging', 'log_agent', fallback=False) if config else False

    def create_agent(self, agent_id: str, api_override: str = None) -> Dict:
        """
        Cria um agente a partir de sua configuração

        Args:
            agent_id: ID do agente (ex: 'researcher', 'writer')
            api_override: API a usar (sobrescreve config.json)

        Returns:
            Dicionário com configuração do agente e serviço de IA
        """
        agent_dir = Path(f"agents/{agent_id}")

        if not agent_dir.exists():
            raise ValueError(f"Agente '{agent_id}' não encontrado em {agent_dir}")

        # Ler arquivos de configuração
        config = read_json_file(agent_dir / "config.json")
        context = read_markdown_file(agent_dir / "context.md")
        task = read_markdown_file(agent_dir / "task.md")
        actions = read_markdown_file(agent_dir / "actions.md")

        # Determinar API a usar
        api = api_override if api_override else config.get('api', 'gemini')

        # Criar serviço apropriado
        if api == 'claude':
            service = ClaudeService(self.anthropic_key)
        elif api == 'gemini':
            # Habilitar Google Search apenas para o agente researcher
            enable_search = (agent_id == 'researcher')
            service = GeminiService(self.google_key, enable_search=enable_search)
            if enable_search:
                logger.info(f"Google Search grounding habilitado para agente '{agent_id}'")
        else:
            raise ValueError(f"API '{api}' não suportada. Use: claude, gemini")

        # Construir agente
        agent = {
            'id': agent_id,
            'name': config['name'],
            'role': config['role'],
            'api': api,
            'model': config['model'],
            'temperature': config.get('temperature', 0.7),
            'max_tokens': config.get('max_tokens', 4000),
            'context': context,
            'task': task,
            'actions': actions,
            'service': service
        }

        logger.info(f"Agente '{agent['name']}' criado - API: {api}, Modelo: {agent['model']}")

        return agent

    def build_prompt(self, agent: Dict, input_data: str) -> str:
        """
        Constrói o prompt completo para o agente

        Args:
            agent: Configuração do agente
            input_data: Dados de entrada

        Returns:
            Prompt formatado
        """
        prompt = f"""
{agent['context']}

---

{agent['task']}

---

{agent['actions']}

---

## INPUT

{input_data}

---

Gere o output seguindo EXATAMENTE o formato especificado em "Formato de Output".
"""
        return prompt

    def execute_agent(self, agent: Dict, input_data: str) -> str:
        """
        Executa um agente com os dados fornecidos

        Args:
            agent: Configuração do agente
            input_data: Dados de entrada

        Returns:
            Resultado da execução
        """
        logger.info(f"Executando agente: {agent['name']}")

        # Construir prompt
        prompt = self.build_prompt(agent, input_data)

        # Logar input se log_agent estiver ativo
        if self.log_agent:
            logger.info("="*60)
            logger.info("AGENT INPUT")
            logger.info("="*60)
            logger.info(f"Agent: {agent['name']} ({agent['id']})")
            logger.info(f"API: {agent['api']} | Model: {agent['model']}")
            logger.info("-"*60)
            logger.info(prompt)
            logger.info("="*60)

        # Chamar API
        service = agent['service']
        result = service.call_with_retry(
            prompt=prompt,
            model=agent['model'],
            temperature=agent['temperature'],
            max_tokens=agent['max_tokens']
        )

        if not result:
            raise Exception(f"Agente '{agent['name']}' não retornou resposta")

        # Logar output se log_agent estiver ativo
        if self.log_agent:
            logger.info("="*60)
            logger.info("AGENT OUTPUT")
            logger.info("="*60)
            logger.info(f"Agent: {agent['name']} ({agent['id']})")
            logger.info("-"*60)
            logger.info(result)
            logger.info("="*60)

        logger.info(f"Agente '{agent['name']}' concluído")

        return result
