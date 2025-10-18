"""
Sistema Multi-Agentes para Criação de Posts de Blog
Ponto de entrada principal da aplicação
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import configparser
import json

from utils.logger import setup_logger, clean_logs
from utils.validator import validate_input_file, validate_api_keys
from utils.file_handler import read_input_file, ensure_directories
from flows.flow_manager import FlowManager


class MultiAgentSystem:
    """Classe principal do sistema multi-agentes"""

    def __init__(self):
        """Inicializa o sistema"""
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.flow_manager = None

    def _load_config(self):
        """Carrega configurações do arquivo config.ini"""
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        return config

    def _setup_logging(self):
        """Configura sistema de logs"""
        log_level = self.config.get('logging', 'level', fallback='INFO')
        clear_on_start = self.config.getboolean('logging', 'clear_on_start', fallback=True)

        if clear_on_start:
            clean_logs(
                logs_dir=self.config.get('paths', 'logs_dir'),
                errors_dir=self.config.get('paths', 'errors_dir')
            )

        return setup_logger(log_level)

    def _validate_environment(self):
        """Valida ambiente e dependências"""
        self.logger.info("Validando ambiente...")

        # Validar API keys
        api_keys = {
            'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
            'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY')
        }

        if not validate_api_keys(api_keys):
            self.logger.error("API keys não configuradas corretamente")
            sys.exit(1)

        # Garantir que diretórios existem
        ensure_directories([
            self.config.get('paths', 'input_dir'),
            self.config.get('paths', 'output_dir'),
            self.config.get('paths', 'logs_dir'),
            self.config.get('paths', 'errors_dir')
        ])

        self.logger.info("Ambiente validado com sucesso")

    def _validate_input(self):
        """Valida arquivo de entrada"""
        self.logger.info("Validando arquivo de entrada...")

        input_dir = self.config.get('paths', 'input_dir')

        # Verificar se existe apenas um arquivo
        input_files = list(Path(input_dir).glob('*.txt'))

        if len(input_files) == 0:
            self.logger.error(f"Nenhum arquivo .txt encontrado em {input_dir}")
            self.logger.info("Crie um arquivo 'post.txt' com o formato:")
            self.logger.info("Fluxo: Post_Esportivo")
            self.logger.info("Assunto: Seu assunto aqui")
            sys.exit(1)

        if len(input_files) > 1:
            self.logger.warning(f"Múltiplos arquivos encontrados em {input_dir}")
            self.logger.warning("Mantenha apenas um arquivo .txt na pasta input/")
            self.logger.info("Arquivos encontrados:")
            for f in input_files:
                self.logger.info(f"  - {f.name}")
            sys.exit(1)

        input_file = input_files[0]
        self.logger.info(f"Arquivo de entrada: {input_file.name}")

        # Validar formato do arquivo
        if not validate_input_file(input_file):
            self.logger.error("Formato do arquivo inválido")
            sys.exit(1)

        return input_file

    def _parse_input_file(self, input_file):
        """Faz parse do arquivo de entrada"""
        content = read_input_file(input_file)

        flow_name = None
        subject = None

        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('Fluxo:'):
                flow_name = line.replace('Fluxo:', '').strip()
            elif line.startswith('Assunto:'):
                subject = line.replace('Assunto:', '').strip()

        if not flow_name or not subject:
            self.logger.error("Arquivo deve conter 'Fluxo:' e 'Assunto:'")
            sys.exit(1)

        return flow_name, subject

    def _load_flow_config(self, flow_name):
        """Carrega configuração do fluxo"""
        flows_config_file = Path('config/flows.json')

        if not flows_config_file.exists():
            self.logger.error("Arquivo config/flows.json não encontrado")
            sys.exit(1)

        with open(flows_config_file, 'r', encoding='utf-8') as f:
            flows_config = json.load(f)

        # Buscar fluxo específico
        for flow in flows_config.get('flows', []):
            if flow['name'] == flow_name:
                return flow

        # Fluxo não encontrado
        self.logger.error(f"Fluxo '{flow_name}' não encontrado")
        self.logger.info("Fluxos disponíveis:")
        for flow in flows_config.get('flows', []):
            self.logger.info(f"  - {flow['name']}: {flow['description']}")
        sys.exit(1)

    def run(self):
        """Executa o sistema"""
        try:
            self.logger.info("="*60)
            self.logger.info("Sistema Multi-Agentes para Criação de Posts")
            self.logger.info("="*60)

            # Validar ambiente
            self._validate_environment()

            # Validar e ler arquivo de entrada
            input_file = self._validate_input()
            flow_name, subject = self._parse_input_file(input_file)

            self.logger.info(f"Fluxo selecionado: {flow_name}")
            self.logger.info(f"Assunto: {subject}")

            # Carregar configuração do fluxo
            flow_config = self._load_flow_config(flow_name)

            # Inicializar Flow Manager
            self.flow_manager = FlowManager(
                config=self.config,
                logger_instance=self.logger
            )

            # Executar fluxo
            self.logger.info("-"*60)
            self.logger.info("Iniciando execução do fluxo...")
            self.logger.info("-"*60)

            result = self.flow_manager.execute_flow(
                flow_config=flow_config,
                subject=subject
            )

            if result['success']:
                self.logger.info("="*60)
                self.logger.info("✓ Fluxo executado com sucesso!")
                self.logger.info("="*60)
                self.logger.info("Arquivos gerados:")
                for output_file in result.get('output_files', []):
                    self.logger.info(f"  ✓ {output_file}")
                self.logger.info("="*60)
            else:
                self.logger.error("="*60)
                self.logger.error("✗ Erro na execução do fluxo")
                self.logger.error(f"Erro: {result.get('error', 'Erro desconhecido')}")
                self.logger.error("="*60)
                sys.exit(1)

        except KeyboardInterrupt:
            self.logger.warning("\n\nExecução interrompida pelo usuário")
            sys.exit(0)

        except Exception as e:
            self.logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
            sys.exit(1)


def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_dotenv()

    # Inicializar e executar sistema
    system = MultiAgentSystem()
    system.run()


if __name__ == "__main__":
    main()
