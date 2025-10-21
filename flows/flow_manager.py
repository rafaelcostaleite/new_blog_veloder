"""
Gerenciador de fluxos de trabalho
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List
import configparser

from agents.agent_factory import AgentFactory
from utils.file_handler import write_output_file

logger = logging.getLogger("MultiAgentBlog")


class FlowManager:
    """Gerenciador de fluxos de agentes"""

    def __init__(self, config: configparser.ConfigParser, logger_instance: logging.Logger):
        """
        Inicializa o gerenciador de fluxos

        Args:
            config: Configuração do sistema
            logger_instance: Logger configurado
        """
        self.config = config
        self.logger = logger_instance
        self.output_dir = Path(config.get('paths', 'output_dir'))

        # Inicializar factory
        self.agent_factory = AgentFactory(
            anthropic_key=os.getenv('ANTHROPIC_API_KEY'),
            google_key=os.getenv('GOOGLE_API_KEY'),
            config=config
        )

    def execute_flow(self, flow_config: Dict, subject: str) -> Dict:
        """
        Executa um fluxo completo

        Args:
            flow_config: Configuração do fluxo
            subject: Assunto a ser processado

        Returns:
            Dicionário com resultado da execução
        """
        try:
            flow_name = flow_config['name']
            agents_config = flow_config['agents']
            output_files = flow_config.get('output_files', [])

            self.logger.info(f"Iniciando fluxo: {flow_name}")
            self.logger.info(f"Total de agentes: {len(agents_config)}")

            # Ordenar agentes por ordem
            agents_config = sorted(agents_config, key=lambda x: x['order'])

            # Executar pipeline de agentes
            current_input = f"Assunto: {subject}"
            all_generated_files = []

            for i, agent_config in enumerate(agents_config, 1):
                agent_id = agent_config['id']
                api = agent_config.get('api')

                self.logger.info(f"\n{'='*60}")
                self.logger.info(f"Agente {i}/{len(agents_config)}: {agent_id}")
                self.logger.info(f"{'='*60}")

                # Criar e executar agente
                agent = self.agent_factory.create_agent(agent_id, api_override=api)
                result = self.agent_factory.execute_agent(agent, current_input)

                # Processar resultado do agente específico
                agent_files = self._process_agent_result(agent_id, result)
                all_generated_files.extend(agent_files)

                # Preparar input para próximo agente
                # Resultado sempre se torna input do próximo agente
                current_input = result

                self.logger.info(f"Agente {agent_id} concluído com sucesso\n")

            # Processar resultado final
            final_result = {'files': all_generated_files}

            return {
                'success': True,
                'flow': flow_name,
                'output_files': final_result['files']
            }

        except Exception as e:
            self.logger.error(f"Erro na execução do fluxo: {str(e)}", exc_info=True)
            return {
                'success': False,
                'error': str(e)
            }

    def _process_agent_result(self, agent_id: str, result: str) -> List[str]:
        """
        Processa resultado de um agente específico e salva arquivos quando necessário

        Args:
            agent_id: ID do agente
            result: Resultado do agente

        Returns:
            Lista de arquivos gerados
        """
        generated_files = []

        try:
            # Reviewer: salva Post.txt e SEO.txt
            if agent_id == 'reviewer':
                if "=== POST HTML ===" in result and "=== DADOS SEO ===" in result:
                    # Separar POST e SEO
                    parts = result.split("=== DADOS SEO ===")

                    # Extrair HTML
                    html_part = parts[0].replace("=== POST HTML ===", "").strip()
                    post_file = self.output_dir / "Post.txt"
                    write_output_file(post_file, html_part)
                    generated_files.append(str(post_file))
                    self.logger.info(f"Arquivo gerado: {post_file}")

                    # Extrair SEO
                    seo_part = parts[1].strip()
                    seo_file = self.output_dir / "SEO.txt"
                    write_output_file(seo_file, seo_part)
                    generated_files.append(str(seo_file))
                    self.logger.info(f"Arquivo gerado: {seo_file}")
                else:
                    self.logger.warning(f"Formato inesperado do reviewer: {result[:100]}")

            # Art Creator: salva apenas image.txt
            elif agent_id == 'art_creator':
                image_file = self.output_dir / "image.txt"
                write_output_file(image_file, result)
                generated_files.append(str(image_file))
                self.logger.info(f"Arquivo gerado: {image_file}")

            # Outros agentes: não salvam arquivos
            else:
                pass

            return generated_files

        except Exception as e:
            self.logger.error(f"Erro ao processar resultado do agente {agent_id}: {str(e)}")
            return []

    def _process_final_result(self, result: str, output_files: List[str]) -> Dict:
        """
        Processa resultado final e salva arquivos

        Args:
            result: Resultado final do último agente
            output_files: Lista de arquivos esperados

        Returns:
            Dicionário com arquivos gerados
        """
        generated_files = []

        try:
            # Tentar parsear como JSON
            try:
                result_data = json.loads(result)

                # Se for JSON com estrutura esperada do reviewer
                if 'post_html' in result_data and 'seo_data' in result_data:
                    # Salvar Post.txt
                    post_file = self.output_dir / "Post.txt"
                    write_output_file(post_file, result_data['post_html'])
                    generated_files.append(str(post_file))
                    self.logger.info(f"Arquivo gerado: {post_file}")

                    # Salvar SEO.txt
                    seo_file = self.output_dir / "SEO.txt"
                    write_output_file(seo_file, result_data['seo_data'])
                    generated_files.append(str(seo_file))
                    self.logger.info(f"Arquivo gerado: {seo_file}")
                else:
                    # Salvar JSON como está
                    output_file = self.output_dir / "output.json"
                    write_output_file(output_file, json.dumps(result_data, indent=2, ensure_ascii=False))
                    generated_files.append(str(output_file))
                    self.logger.info(f"Arquivo gerado: {output_file}")

            except json.JSONDecodeError:
                # Não é JSON, tentar separar manualmente se contiver marcadores

                # Verificar se contém output do art_creator (image prompts)
                if "=== PROMPTS PARA GERAÇÃO DE IMAGENS ===" in result:
                    # Separar as três partes: POST, SEO e IMAGE

                    # Extrair Post HTML (entre início e === DADOS SEO ===)
                    if "=== POST HTML ===" in result and "=== DADOS SEO ===" in result:
                        post_start = result.find("=== POST HTML ===") + len("=== POST HTML ===")
                        post_end = result.find("=== DADOS SEO ===")
                        html_part = result[post_start:post_end].strip()

                        post_file = self.output_dir / "Post.txt"
                        write_output_file(post_file, html_part)
                        generated_files.append(str(post_file))
                        self.logger.info(f"Arquivo gerado: {post_file}")

                    # Extrair SEO (entre === DADOS SEO === e === PROMPTS)
                    seo_start = result.find("=== DADOS SEO ===") + len("=== DADOS SEO ===")
                    seo_end = result.find("=== PROMPTS PARA GERAÇÃO DE IMAGENS ===")
                    seo_part = result[seo_start:seo_end].strip()

                    seo_file = self.output_dir / "SEO.txt"
                    write_output_file(seo_file, seo_part)
                    generated_files.append(str(seo_file))
                    self.logger.info(f"Arquivo gerado: {seo_file}")

                    # Extrair Image Prompts
                    image_start = result.find("=== PROMPTS PARA GERAÇÃO DE IMAGENS ===")
                    image_part = result[image_start:].strip()

                    image_file = self.output_dir / "image.txt"
                    write_output_file(image_file, image_part)
                    generated_files.append(str(image_file))
                    self.logger.info(f"Arquivo gerado: {image_file}")

                elif "=== POST HTML ===" in result and "=== SEO DATA ===" in result:
                    # Apenas POST e SEO (reviewer sem art_creator)
                    parts = result.split("=== SEO DATA ===")

                    # Extrair HTML
                    html_part = parts[0].replace("=== POST HTML ===", "").strip()
                    post_file = self.output_dir / "Post.txt"
                    write_output_file(post_file, html_part)
                    generated_files.append(str(post_file))
                    self.logger.info(f"Arquivo gerado: {post_file}")

                    # Extrair SEO
                    seo_part = parts[1].strip()
                    seo_file = self.output_dir / "SEO.txt"
                    write_output_file(seo_file, seo_part)
                    generated_files.append(str(seo_file))
                    self.logger.info(f"Arquivo gerado: {seo_file}")
                else:
                    # Salvar como texto simples
                    output_file = self.output_dir / "output.txt"
                    write_output_file(output_file, result)
                    generated_files.append(str(output_file))
                    self.logger.info(f"Arquivo gerado: {output_file}")

            return {
                'files': generated_files
            }

        except Exception as e:
            self.logger.error(f"Erro ao processar resultado final: {str(e)}")
            raise
