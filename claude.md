# Claude.md - Sistema Multi-Agentes para Criação de Posts de Blog

## 📋 Descrição do Projeto

Sistema multi-agentes de IA desenvolvido para automatizar a criação de posts de blog de alta qualidade para WordPress. O sistema utiliza múltiplas APIs de IA (Claude e Gemini) organizadas em fluxos de trabalho colaborativos através do framework CrewAI.

---

## 🏗️ Arquitetura do Sistema

### Tecnologias Base
- **Containerização**: Docker + Docker Compose
- **Linguagem**: Python 3.11+
- **Framework de Orquestração**: CrewAI
- **APIs de IA**: 
  - Anthropic (Claude)
  - Google Gemini
  - Extensível para outras APIs (ex: Grok)
- **Controle de Versão**: Git

### Princípios Arquiteturais
- ✅ Projeto enxuto e simplificado
- ✅ Modularidade: fácil adição de novos agentes e fluxos
- ✅ Configuração externalizada (.env + config.ini)
- ✅ Separação clara de responsabilidades
- ✅ Estrutura baseada em fluxos de trabalho

---

## 📁 Estrutura de Diretórios

```
projeto-multi-agentes/
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── config/
│   ├── config.ini              # Configurações gerais
│   └── flows.json              # Definição dos fluxos
│
├── agents/
│   ├── __init__.py
│   ├── agent_factory.py        # Factory para criar agentes
│   │
│   ├── researcher/
│   │   ├── config.json         # Configuração do agente (API, modelo, parâmetros)
│   │   ├── context.md          # Contexto e personalidade do agente
│   │   ├── task.md             # Descrição da tarefa e objetivo
│   │   └── actions.md          # Ações permitidas, ferramentas e formato de output
│   │
│   ├── writer/
│   │   ├── config.json
│   │   ├── context.md
│   │   ├── task.md
│   │   └── actions.md
│   │
│   └── reviewer/
│       ├── config.json
│       ├── context.md
│       ├── task.md
│       └── actions.md
│
├── flows/
│   ├── __init__.py
│   ├── flow_manager.py         # Gerenciador de fluxos
│   └── post_dicas.py           # Implementação do fluxo
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py           # Interface base para APIs
│   ├── claude_service.py       # Implementação Claude
│   └── gemini_service.py       # Implementação Gemini
│
├── utils/
│   ├── __init__.py
│   ├── logger.py               # Sistema de logs
│   ├── file_handler.py         # Manipulação de arquivos
│   └── validator.py            # Validações
│
├── data/
│   ├── input/
│   │   └── post.txt            # Arquivo de entrada
│   └── output/                 # Arquivos gerados
│
├── logs/                        # Logs de execução (gitignore)
│
├── errors/                      # Logs de erros (gitignore)
│
└── main.py                      # Ponto de entrada
```

---

## 📋 Estrutura de Arquivos dos Agentes

Cada agente possui 4 arquivos de configuração que definem seu comportamento:

### 1. **config.json**
Define parâmetros técnicos do agente:
- Nome e função do agente
- API a ser utilizada (Claude, Gemini, etc.)
- Modelo específico (ex: `claude-sonnet-4`, `gemini-pro`)
- Parâmetros de geração (temperature, max_tokens)

### 2. **context.md**
Estabelece a personalidade e expertise do agente:
- Papel que o agente desempenha
- Características comportamentais
- Estilo de trabalho
- Área de especialização

### 3. **task.md**
Descreve a tarefa principal do agente:
- Objetivo claro e específico
- Processo passo a passo
- Output esperado (formato e conteúdo)
- Diretrizes gerais de execução

### 4. **actions.md**
Especifica as ações concretas que o agente pode executar:
- **Ferramentas disponíveis**: APIs, bibliotecas, recursos
- **Ações permitidas**: Lista detalhada de operações autorizadas
- **Restrições**: O que o agente NÃO pode fazer
- **Formato de output**: Estrutura exata do resultado (JSON, HTML, etc.)
- **Validações**: Checklist de qualidade

> **Importante**: O arquivo `actions.md` é crucial para garantir que o agente execute apenas ações autorizadas e produza outputs no formato esperado pelo próximo agente do fluxo.

---

## ⚙️ Configurações

### Arquivo .env
```env
# API Keys
ANTHROPIC_API_KEY=sua_chave_anthropic
GOOGLE_API_KEY=sua_chave_google

# Configurações gerais
LOG_LEVEL=INFO
ENVIRONMENT=development
```

### Arquivo config.ini
```ini
[general]
project_name = Multi-Agent Blog System
version = 1.0.0

[logging]
level = INFO
# Níveis: DEBUG, INFO, WARNING, ERROR
max_files = 1
clear_on_start = true

[paths]
input_dir = data/input
output_dir = data/output
logs_dir = logs
errors_dir = errors

[execution]
single_run = true
validate_input = true
```

### Arquivo config/flows.json
```json
{
  "flows": [
    {
      "name": "Post_Esportivo",
      "description": "Fluxo para criação de posts com notificias e informações esportivas.",
      "agents": [
        {
          "id": "researcher",
          "order": 1,
          "api": "gemini"
        },
        {
          "id": "writer",
          "order": 2,
          "api": "claude"
        },
        {
          "id": "reviewer",
          "order": 3,
          "api": "claude"
        }
      ],
      "output_files": ["Post.txt", "SEO.txt"]
    }
  ]
}
```

---

## 🤖 Fluxo: Post_Dicas

### Objetivo
Criar posts de blog otimizados para SEO com conteúdo atualizado e relevante.

### Pipeline de Agentes

#### **Agente 1: Researcher (Pesquisador)**
- **API**: Gemini
- **Função**: Pesquisar dados atualizados na internet sobre o assunto
- **Input**: `data/input/post.txt` (assunto especificado)
- **Output**: JSON estruturado com dados de pesquisa
- **Arquivo de Configuração**: `agents/researcher/config.json`

**Exemplo de config.json:**
```json
{
  "name": "Researcher",
  "role": "Pesquisador de Conteúdo",
  "api": "gemini",
  "model": "gemini-pro",
  "temperature": 0.8,
  "max_tokens": 8000
}
```

**context.md:**
```markdown
# Contexto do Agente Pesquisador

Você é um pesquisador especializado em buscar informações atualizadas e relevantes na internet. Sua função é coletar dados precisos, estatísticas recentes e referências confiáveis sobre o tema solicitado.

## Características:
- Foco em fontes confiáveis
- Prioriza dados atualizados (últimos 12 mese
- Busca evidências científicas quando aplicável
- Identifica tendências e insights relevantes
```

**task.md:**
```markdown
# Tarefa: Pesquisa de Conteúdo

## Objetivo
Pesquisar informações atualizadas sobre o assunto fornecido.

## Processo
1. Analisar o tema solicitado
2. Identificar palavras-chave relevantes
3. Buscar informações em fontes confiáveis
4. Compilar dados, estatísticas e referências
5. Estruturar resultado em formato JSON

## Output Esperado
JSON contendo:
- Principais pontos sobre o tema
- Estatísticas e dados recentes
- Fontes e referências
- Tendências atuais
- Insights relevantes
```

**actions.md:**
```markdown
# Ações Específicas do Agente Pesquisador

## Ferramentas Disponíveis
- Busca na Web com API do Gemini
- Extração de conteúdo de páginas
- Análise de dados estruturados

## Ações Permitidas
1. **Buscar Informações Online**
   - Realizar buscas com palavras-chave estratégicas
   - Acessar até 10 URLs por pesquisa
   - Priorizar fontes confiáveis conforme arquivo de configuração

2. **Extrair e Processar Dados**
   - Extrair texto relevante de páginas web
   - Identificar estatísticas e números atualizados
   - Coletar datas de publicação

3. **Validar Fontes**
   - Verificar credibilidade das fontes
   - Priorizar conteúdo dos últimos 12 meses
   - Evitar clickbait e conteúdo não verificado

4. **Estruturar Resultado**
   - Organizar informações em formato JSON
   - Categorizar dados por relevância
   - Adicionar URLs de referência

## Restrições
- ❌ Não inventar informações
- ❌ Não usar fontes não verificáveis
- ❌ Não exceder 8000 tokens no output
- ❌ Não incluir conteúdo duplicado

## Formato de Output
```json
{
  "topic": "Título do assunto pesquisado",
  "research_date": "2025-10-17",
  "key_findings": [
    {
      "title": "Achado principal 1",
      "content": "Descrição detalhada",
      "source": "URL da fonte",
      "date": "2025-09-15"
    }
  ],
  "statistics": [
    {
      "metric": "Nome da métrica",
      "value": "Valor",
      "source": "URL",
      "year": 2025
    }
  ],
  "trends": [
    "Tendência 1",
    "Tendência 2"
  ],
  "references": [
    {
      "title": "Título do artigo",
      "url": "URL completa",
      "domain": "exemplo.com",
      "date": "2025-08-20"
    }
  ]
}
```

#### **Agente 2: Writer (Escritor)**
- **API**: Gemini
- **Função**: Escrever o post de blog baseado na pesquisa
- **Input**: JSON do Agente 1
- **Output**: JSON com o post escrito

**Exemplo de config.json:**
```json
{
  "name": "Writer",
  "role": "Escritor de Conteúdo",
  "api": "gemini",
  "model": "gemini-pro",
  "temperature": 0.8,
  "max_tokens": 8000
}
```

**context.md:**
```markdown
# Contexto do Agente Escritor

Você é um escritor profissional especializado em criar conteúdo envolvente para blogs. Seu estilo é claro, informativo e otimizado para leitura online.

## Características:
- Linguagem clara e acessível
- Estrutura bem organizada
- Introduções cativantes
- Uso de exemplos práticos
- Tom conversacional mas profissional
```

**task.md:**
```markdown
# Tarefa: Escrita do Post

## Objetivo
Criar um post de blog completo e envolvente baseado nos dados de pesquisa.

## Estrutura do Post
1. Título atrativo
2. Introdução envolvente (2-3 parágrafos)
3. Desenvolvimento com subtópicos
4. Exemplos práticos
5. Conclusão com call-to-action

## Diretrizes
- Mínimo 800 palavras
- Parágrafos curtos (3-4 linhas)
- Use listas quando apropriado
- Inclua dados da pesquisa
- Tom profissional mas acessível
```

**actions.md:**
```markdown
# Ações Específicas do Agente Escritor

## Ferramentas Disponíveis
- Geração de texto criativo
- Análise de estrutura narrativa
- Otimização de legibilidade

## Ações Permitidas
1. **Criar Título Atrativo**
   - Usar números quando apropriado (ex: "7 Dicas...")
   - Incluir benefício claro
   - Máximo 70 caracteres
   - Evitar clickbait excessivo

2. **Escrever Introdução**
   - Hook inicial envolvente (primeira frase impactante)
   - Contextualizar o problema/tema
   - Apresentar o que o leitor vai aprender
   - 2-3 parágrafos (150-200 palavras)

3. **Desenvolver Conteúdo Principal**
   - Dividir em seções com H2/H3
   - Usar listas e bullet points
   - Incluir estatísticas da pesquisa
   - Adicionar exemplos práticos
   - Manter parágrafos curtos (3-4 linhas)

4. **Criar Conclusão**
   - Resumir pontos principais
   - Incluir call-to-action claro
   - Incentivar engajamento (comentários, compartilhamento)

5. **Garantir Qualidade**
   - Revisar coerência e fluxo
   - Verificar transições entre seções
   - Manter tom consistente

## Restrições
- ❌ Não plagiar conteúdo das fontes
- ❌ Não usar linguagem técnica excessiva
- ❌ Não ultrapassar 2000 palavras
- ❌ Não incluir informações não verificadas
- ❌ Não usar jargões sem explicação

## Formato de Output
```json
{
  "title": "Título principal do post",
  "introduction": "Texto completo da introdução com 2-3 parágrafos...",
  "sections": [
    {
      "heading": "Título da Seção 1",
      "content": "Conteúdo completo da seção...",
      "subsections": [
        {
          "subheading": "Subtítulo (opcional)",
          "content": "Conteúdo do subtópico..."
        }
      ]
    }
  ],
  "conclusion": "Texto completo da conclusão com call-to-action...",
  "word_count": 1250,
  "estimated_reading_time": "5 minutos"
}
```

## Diretrizes de Estilo
- **Tom**: Profissional, mas conversacional
- **Pessoa**: 2ª pessoa (você) para engajamento
- **Tempo Verbal**: Presente
- **Estrutura**: Pirâmide invertida (informação mais importante primeiro)
```

---

#### **Agente 3: Reviewer (Revisor e SEO)**
- **API**: Claude
- **Função**: Revisar o post, adicionar tags HTML e criar dados SEO
- **Input**: JSON do Agente 2
- **Output**: 
  - `Post.txt` - Post formatado em HTML
  - `SEO.txt` - Dados de SEO

**Exemplo de config.json:**
```json
{
  "name": "Reviewer",
  "role": "Revisor e Especialista em SEO",
  "api": "claude",
  "model": "claude-sonnet-4-20250514",
  "temperature": 0.3,
  "max_tokens": 6000
}
```

**context.md:**
```markdown
# Contexto do Agente Revisor e SEO

Você é um especialista em revisão de conteúdo e otimização para SEO. Seu trabalho é garantir que o conteúdo esteja perfeito e otimizado para mecanismos de busca.

## Características:
- Atenção aos detalhes
- Conhecimento profundo de SEO
- Expertise em HTML semântico
- Foco na experiência do usuário
```

**task.md:**
```markdown
# Tarefa: Revisão e Otimização SEO

## Objetivo
Revisar o post e otimizá-lo para SEO, adicionando formatação HTML.

## Processo
1. Revisar gramática e ortografia
2. Otimizar estrutura de títulos (H1, H2, H3)
3. Adicionar tags HTML semânticas
4. Criar meta descrição
5. Sugerir palavras-chave
6. Gerar título SEO
7. Criar slug otimizado

## Outputs
### Post.txt
- HTML completo com tags
- Estrutura de cabeçalhos
- Formatação adequada

### SEO.txt
- Título SEO (60 caracteres)
- Meta descrição (155 caracteres)
- Palavras-chave (5-7)
- Slug
- Tags sugeridas
```

**actions.md:**
```markdown
# Ações Específicas do Agente Revisor e SEO

## Ferramentas Disponíveis
- Análise de legibilidade
- Validação de HTML
- Otimização de palavras-chave
- Análise de densidade de keywords

## Ações Permitidas

### 1. Revisão de Conteúdo
- **Gramática e Ortografia**
  - Corrigir erros gramaticais
  - Verificar concordância verbal
  - Padronizar pontuação
  - Corrigir acentuação

- **Estrutura e Fluxo**
  - Verificar coerência entre parágrafos
  - Melhorar transições
  - Garantir progressão lógica
  - Remover redundâncias

### 2. Formatação HTML
- **Tags Semânticas**
  - `<h1>` para título principal (apenas 1)
  - `<h2>` para seções principais
  - `<h3>` para subseções
  - `<p>` para parágrafos
  - `<ul>` e `<li>` para listas
  - `<strong>` para ênfase importante
  - `<em>` para ênfase leve

- **Estrutura de Cabeçalhos**
  - Hierarquia correta (H1 → H2 → H3)
  - Não pular níveis
  - Incluir palavras-chave nos títulos

### 3. Otimização SEO
- **Título SEO**
  - Máximo 60 caracteres
  - Incluir palavra-chave principal
  - Atrativo e claro
  - Incluir ano quando relevante (ex: 2025)

- **Meta Descrição**
  - 150-155 caracteres
  - Incluir palavra-chave
  - Call-to-action implícito
  - Resumir valor do conteúdo

- **Palavras-chave**
  - Identificar 5-7 keywords
  - Mix de short-tail e long-tail
  - Verificar densidade (1-2%)
  - Incluir variações

- **Slug/URL**
  - Máximo 5-6 palavras
  - Apenas minúsculas
  - Separado por hífens
  - Incluir palavra-chave principal
  - Sem caracteres especiais

### 4. Otimizações Adicionais
- **Legibilidade**
  - Verificar Flesch Reading Ease
  - Garantir parágrafos curtos
  - Usar voz ativa
  - Simplificar frases complexas

- **Links Internos** (sugestões)
  - Identificar oportunidades de link interno
  - Sugerir anchor texts relevantes

## Restrições
- ❌ Não alterar significado original
- ❌ Não adicionar informações novas
- ❌ Não usar keyword stuffing
- ❌ Não criar HTML inválido
- ❌ Não exceder limites de caracteres SEO

## Formato de Output

### Arquivo: Post.txt
```html
<h1>Título Principal Otimizado para SEO</h1>

<p>Primeiro parágrafo da introdução com palavra-chave natural...</p>

<p>Segundo parágrafo expandindo o contexto...</p>

<h2>Primeira Seção Principal</h2>

<p>Conteúdo da seção com <strong>ênfase importante</strong> e texto natural...</p>

<ul>
  <li>Item de lista 1</li>
  <li>Item de lista 2</li>
  <li>Item de lista 3</li>
</ul>

<h3>Subseção Opcional</h3>

<p>Conteúdo da subseção...</p>

<h2>Segunda Seção Principal</h2>

<p>Mais conteúdo otimizado...</p>

<!-- Continue com todas as seções -->

<h2>Conclusão</h2>

<p>Resumo final com call-to-action...</p>
```

### Arquivo: SEO.txt
```
=== DADOS SEO ===

Título SEO:
[Título otimizado com 55-60 caracteres incluindo palavra-chave]

Meta Descrição:
[Descrição atrativa com 150-155 caracteres, palavra-chave e CTA implícito]

Palavras-chave:
palavra-chave-principal, palavra-chave-secundaria, long-tail-keyword, variacao-keyword, termo-relacionado

Slug:
palavra-chave-principal-termo-relevante

Tags Sugeridas:
tag1, tag2, tag3, tag4, tag5

=== ANÁLISE SEO ===

Densidade de Palavra-chave Principal: 1.5%
Total de Palavras: 1250
Tempo de Leitura Estimado: 5 minutos
Score de Legibilidade: Fácil

Cabeçalhos:
- H1: 1
- H2: 5
- H3: 3

=== SUGESTÕES DE LINKS INTERNOS ===
1. [Texto âncora sugerido 1] - link para post relacionado
2. [Texto âncora sugerido 2] - link para categoria
3. [Texto âncora sugerido 3] - link para página relevante
```

## Checklist de Validação
- [ ] Gramática e ortografia corrigidas
- [ ] Estrutura HTML válida
- [ ] Hierarquia de cabeçalhos correta
- [ ] Título SEO com 55-60 caracteres
- [ ] Meta descrição com 150-155 caracteres
- [ ] 5-7 palavras-chave identificadas
- [ ] Slug otimizado criado
- [ ] Densidade de keywords adequada (1-2%)
- [ ] Tags HTML semânticas aplicadas
- [ ] Legibilidade adequada ao público-alvo
```

---

## 💻 Exemplo de main.py

### Estrutura do Arquivo Principal

O arquivo `main.py` é o ponto de entrada do sistema. Ele orquestra a execução completa do fluxo de trabalho.

```python
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
from services.claude_service import ClaudeService
from services.gemini_service import GeminiService


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
            self.logger.info("Fluxo: Post_Dicas")
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
                logger=self.logger
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
```

### Fluxo de Execução do main.py

```
┌─────────────────────────────────────────┐
│  1. Carregar .env                       │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  2. Inicializar MultiAgentSystem        │
│     - Carregar config.ini               │
│     - Configurar logger                 │
│     - Limpar logs anteriores            │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  3. Validar Ambiente                    │
│     - Verificar API keys                │
│     - Criar diretórios necessários      │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  4. Validar Arquivo de Entrada          │
│     - Verificar existência              │
│     - Garantir arquivo único            │
│     - Validar formato                   │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  5. Parse do Arquivo                    │
│     - Extrair nome do fluxo             │
│     - Extrair assunto                   │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  6. Carregar Configuração do Fluxo      │
│     - Ler config/flows.json             │
│     - Buscar fluxo específico           │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  7. Executar Fluxo                      │
│     - Inicializar FlowManager           │
│     - Executar agentes sequencialmente  │
│     - Gerar arquivos de saída           │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│  8. Finalizar                           │
│     - Exibir resultado                  │
│     - Listar arquivos gerados           │
│     - Encerrar sistema                  │
└─────────────────────────────────────────┘
```

### Exemplo de Output da Execução

```bash
$ python main.py

============================================================
Sistema Multi-Agentes para Criação de Posts
============================================================
[INFO] Validando ambiente...
[INFO] Ambiente validado com sucesso
[INFO] Validando arquivo de entrada...
[INFO] Arquivo de entrada: post.txt
[INFO] Fluxo selecionado: Post_Dicas
[INFO] Assunto: Benefícios de utilizar a camiseta UV nos treinos
------------------------------------------------------------
Iniciando execução do fluxo...
------------------------------------------------------------
[INFO] Executando agente: Researcher (1/3)
[INFO] API: Gemini | Modelo: gemini-pro
[INFO] Pesquisando informações sobre o assunto...
[INFO] ✓ Agente Researcher concluído

[INFO] Executando agente: Writer (2/3)
[INFO] API: Gemini | Modelo: gemini-pro
[INFO] Escrevendo post baseado na pesquisa...
[INFO] ✓ Agente Writer concluído

[INFO] Executando agente: Reviewer (3/3)
[INFO] API: Claude | Modelo: claude-sonnet-4-20250514
[INFO] Revisando e otimizando SEO...
[INFO] ✓ Agente Reviewer concluído

============================================================
✓ Fluxo executado com sucesso!
============================================================
Arquivos gerados:
  ✓ data/output/Post.txt
  ✓ data/output/SEO.txt
============================================================
```

### Tratamento de Erros Implementado

| Situação | Tratamento |
|----------|-----------|
| API keys ausentes | Exibe erro e encerra (exit 1) |
| Múltiplos arquivos input | Exibe warning, lista arquivos e encerra |
| Nenhum arquivo input | Exibe instruções de formato e encerra |
| Formato inválido | Exibe erro de formato e encerra |
| Fluxo não encontrado | Lista fluxos disponíveis e encerra |
| Erro durante execução | Registra erro completo no log e encerra |
| Interrupção usuário (Ctrl+C) | Encerra graciosamente |

### Dependências Utilizadas

```python
# Módulos Python padrão
import os                 # Variáveis de ambiente
import sys                # Exit codes e controle do sistema
from pathlib import Path  # Manipulação de caminhos

# Bibliotecas externas
from dotenv import load_dotenv      # Carregar .env
import configparser                  # Ler config.ini
import json                          # Parse de flows.json

# Módulos internos do projeto
from utils.logger import setup_logger, clean_logs
from utils.validator import validate_input_file, validate_api_keys
from utils.file_handler import read_input_file, ensure_directories
from flows.flow_manager import FlowManager
from services.claude_service import ClaudeService
from services.gemini_service import GeminiService
```

---

## ⚠️ Tratamento de Erros e Exceções

### Estratégia de Tratamento de Erros

O sistema implementa uma abordagem em camadas para tratamento de erros, garantindo que falhas sejam capturadas, registradas e reportadas adequadamente.

### Tipos de Erros

#### 1. **Erros de Configuração**

| Erro | Causa | Tratamento | Exit Code |
|------|-------|------------|-----------|
| API Keys ausentes | `.env` sem ANTHROPIC_API_KEY ou GOOGLE_API_KEY | Exibe erro e encerra | 1 |
| config.ini ausente | Arquivo de configuração não encontrado | Exibe erro e encerra | 1 |
| flows.json ausente | Arquivo de fluxos não encontrado | Exibe erro e encerra | 1 |
| flows.json inválido | JSON mal formatado | Exibe erro de parsing e encerra | 1 |

**Exemplo de tratamento:**
```python
# Em utils/validator.py
def validate_api_keys(api_keys: dict) -> bool:
    """Valida se todas as API keys estão configuradas"""
    missing_keys = [key for key, value in api_keys.items() if not value]

    if missing_keys:
        logger.error(f"API keys ausentes: {', '.join(missing_keys)}")
        logger.info("Configure as chaves no arquivo .env")
        return False

    return True
```

#### 2. **Erros de Entrada**

| Erro | Causa | Tratamento | Exit Code |
|------|-------|------------|-----------|
| Nenhum arquivo input | Pasta `data/input/` vazia | Exibe instruções de formato | 1 |
| Múltiplos arquivos input | Mais de um .txt em `data/input/` | Lista arquivos e solicita remoção | 1 |
| Formato inválido | Arquivo sem "Fluxo:" ou "Assunto:" | Exibe formato esperado | 1 |
| Fluxo inexistente | Fluxo especificado não existe em flows.json | Lista fluxos disponíveis | 1 |

**Exemplo de tratamento:**
```python
# Em main.py
def _get_input_file(self):
    input_files = list(input_dir.glob('*.txt'))

    if len(input_files) == 0:
        self.logger.error("Nenhum arquivo .txt encontrado em data/input/")
        self.logger.info("Crie um arquivo 'post.txt' com:")
        self.logger.info("  Fluxo: Post_Dicas")
        self.logger.info("  Assunto: [Seu assunto aqui]")
        sys.exit(1)

    if len(input_files) > 1:
        self.logger.warning("⚠ Múltiplos arquivos encontrados:")
        for f in input_files:
            self.logger.warning(f"  - {f.name}")
        self.logger.info("Mantenha apenas um arquivo .txt")
        sys.exit(1)
```

#### 3. **Erros de API**

| Erro | Causa | Tratamento | Retry |
|------|-------|------------|-------|
| Rate Limit (429) | Muitas requisições | Aguarda e tenta novamente | Sim (3x) |
| Timeout | API não responde | Aguarda e tenta novamente | Sim (3x) |
| Autenticação (401) | API key inválida | Exibe erro e encerra | Não |
| Quota excedida (402) | Créditos insuficientes | Exibe erro e encerra | Não |
| Erro do servidor (500) | Problema no servidor da API | Aguarda e tenta novamente | Sim (2x) |
| Token limit (400) | Prompt muito grande | Exibe erro e encerra | Não |

**Exemplo de tratamento com retry:**
```python
# Em services/ai_service.py
import time
from typing import Optional

class AIService:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    def call_api(self, prompt: str) -> Optional[str]:
        """Chama API com retry logic"""
        for attempt in range(self.max_retries):
            try:
                response = self._make_request(prompt)
                return response

            except RateLimitError as e:
                if attempt < self.max_retries - 1:
                    wait_time = (attempt + 1) * 10  # Backoff exponencial
                    logger.warning(f"Rate limit atingido. Aguardando {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error("Rate limit - máximo de tentativas excedido")
                    raise

            except TimeoutError as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Timeout. Tentativa {attempt + 1}/{self.max_retries}")
                    time.sleep(5)
                else:
                    logger.error("Timeout - API não respondeu")
                    raise

            except AuthenticationError as e:
                logger.error(f"Erro de autenticação: {str(e)}")
                logger.info("Verifique sua API key no arquivo .env")
                raise

            except Exception as e:
                logger.error(f"Erro inesperado na API: {str(e)}")
                raise

        return None
```

#### 4. **Erros de Execução do Fluxo**

| Erro | Causa | Tratamento | Exit Code |
|------|-------|------------|-----------|
| Agente falhou | Erro durante execução do agente | Registra erro e encerra | 1 |
| Output inválido | Agente retornou formato incorreto | Registra erro e encerra | 1 |
| Arquivo não gerado | Falha ao salvar arquivo de saída | Registra erro e encerra | 1 |
| JSON inválido | Parse error no JSON entre agentes | Registra erro detalhado e encerra | 1 |

**Exemplo de tratamento:**
```python
# Em flows/flow_manager.py
def execute_agent(self, agent_config, input_data):
    """Executa um agente com tratamento de erros"""
    try:
        logger.info(f"Executando agente: {agent_config['name']}")

        # Executar agente
        result = agent.run(input_data)

        # Validar output
        if not self._validate_agent_output(result, agent_config):
            raise ValueError(f"Output inválido do agente {agent_config['name']}")

        logger.info(f"✓ Agente {agent_config['name']} concluído")
        return result

    except json.JSONDecodeError as e:
        logger.error(f"Erro ao processar JSON do agente {agent_config['name']}")
        logger.error(f"Detalhe: {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Falha no agente {agent_config['name']}: {str(e)}")
        logger.error("Execução do fluxo interrompida")
        raise
```

#### 5. **Erros de Sistema**

| Erro | Causa | Tratamento | Exit Code |
|------|-------|------------|-----------|
| Sem permissão | Falta permissão para criar/ler arquivos | Exibe erro de permissão | 1 |
| Disco cheio | Sem espaço para salvar outputs | Exibe erro de espaço | 1 |
| Memória insuficiente | Sistema sem memória | Exibe erro e encerra | 1 |
| Interrupção usuário (Ctrl+C) | Usuário cancelou execução | Encerra graciosamente | 0 |

**Exemplo de tratamento:**
```python
# Em main.py
def run(self):
    try:
        # Execução principal
        self._execute_flow()

    except KeyboardInterrupt:
        logger.warning("\n⚠ Execução interrompida pelo usuário")
        logger.info("Nenhum arquivo foi gerado")
        sys.exit(0)

    except PermissionError as e:
        logger.error(f"Erro de permissão: {str(e)}")
        logger.info("Verifique as permissões dos diretórios")
        sys.exit(1)

    except OSError as e:
        if e.errno == 28:  # No space left on device
            logger.error("Sem espaço em disco para salvar arquivos")
        else:
            logger.error(f"Erro do sistema: {str(e)}")
        sys.exit(1)

    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}", exc_info=True)
        sys.exit(1)
```

### Estrutura de Logs de Erro

Os erros são registrados em dois locais:

#### 1. **Console (stdout/stderr)**
```
[ERROR] 2025-10-17 14:30:45 - API keys não configuradas
[INFO]  2025-10-17 14:30:45 - Configure as chaves no arquivo .env
```

#### 2. **Arquivo de Log (errors/error_2025-10-17_14-30-45.log)**
```
2025-10-17 14:30:45,123 - ERROR - main.py:_validate_environment:62
API keys não configuradas corretamente
Traceback (most recent call last):
  File "main.py", line 60, in _validate_environment
    if not validate_api_keys(api_keys):
ValueError: API keys ausentes: ANTHROPIC_API_KEY
```

### Exit Codes

| Exit Code | Significado |
|-----------|-------------|
| 0 | Sucesso ou interrupção intencional pelo usuário |
| 1 | Erro de configuração, validação ou execução |
| 2 | Erro de argumentos de linha de comando (futuro) |

### Mensagens de Erro Amigáveis

O sistema fornece mensagens de erro claras e acionáveis:

**❌ Ruim:**
```
Error: File not found
```

**✅ Bom:**
```
[ERROR] Nenhum arquivo .txt encontrado em data/input/
[INFO]  Crie um arquivo 'post.txt' com o formato:
[INFO]    Fluxo: Post_Dicas
[INFO]    Assunto: Seu assunto aqui
```

### Boas Práticas Implementadas

1. **Fail Fast**: Erros de configuração são detectados antes de iniciar processamento
2. **Mensagens Acionáveis**: Sempre indicam o que fazer para resolver
3. **Logs Detalhados**: Erros incluem stack trace completo nos arquivos de log
4. **Retry com Backoff**: APIs têm retry automático com espera progressiva
5. **Graceful Shutdown**: Ctrl+C encerra sem deixar arquivos corrompidos
6. **Validação em Camadas**: Input validado em múltiplos pontos
7. **Isolamento de Erros**: Erro em um agente não corrompe o sistema

### Exemplo de Fluxo de Erro Completo

```
1. Usuário executa: python main.py
2. Sistema detecta API key ausente
3. Logger registra em logs/app_2025-10-17.log
4. Logger registra em errors/error_2025-10-17.log (com stack trace)
5. Console exibe mensagem amigável
6. Sistema encerra com exit code 1
7. Nenhum arquivo corrompido é deixado em data/output/
```

---

## 📄 Formato do Arquivo de Entrada

### Exemplo: data/input/post.txt
```
Fluxo: Post_Dicas
Assunto: Benefícios de utilizar a camiseta UV nos treinos de corrida e Maratonas.
```

---

## 📤 Formato dos Arquivos de Saída

### Exemplo: data/output/Post.txt
```html
<h1>Os 7 Principais Benefícios da Camiseta UV para Corredores e Maratonistas</h1>

<p>Se você é corredor ou está se preparando para uma maratona, sabe como a escolha do equipamento certo pode fazer toda a diferença no desempenho e conforto durante os treinos...</p>

<h2>1. Proteção Contra Raios UV</h2>
<p>As camisetas UV oferecem proteção solar de FPS 50+...</p>

<!-- Conteúdo completo formatado -->
```

### Exemplo: data/output/SEO.txt
```
=== DADOS SEO ===

Título SEO:
7 Benefícios da Camiseta UV para Corrida | Guia Completo 2025

Meta Descrição:
Descubra os principais benefícios da camiseta UV para corrida e maratonas. Proteção solar, conforto térmico e performance. Guia atualizado 2025.

Palavras-chave:
camiseta uv corrida, proteção solar running, roupa para maratona, camiseta corrida verão, equipamento corrida

Slug:
beneficios-camiseta-uv-corrida-maratona

Tags Sugeridas:
corrida, maratona, equipamento esportivo, proteção solar, performance
```

---

## 🚀 Execução do Sistema

### Pré-requisitos
```bash
# Clone o repositório
git clone [url-do-repositorio]

# Copie o arquivo de exemplo
cp .env.example .env

# Adicione suas API keys no arquivo .env
```

### Inicialização via Docker
```bash
# Build da imagem
docker-compose build

# Executar o sistema
docker-compose up

# Ou em modo detached
docker-compose up -d
```

### Execução Local (sem Docker)
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

### Fluxo de Execução
1. Sistema lê arquivo `data/input/post.txt`
2. Identifica o fluxo especificado
3. Carrega configuração do fluxo
4. Executa agentes na ordem definida
5. Gera arquivos de saída em `data/output/`
6. Registra logs em `logs/`
7. Sistema encerra (execução única)

---

## ✅ Validações

### Validação de Entrada
- ❌ **Erro**: Mais de um arquivo na pasta `data/input/`
  - **Ação**: Exibir warning e solicitar que mantenha apenas um arquivo
- ❌ **Erro**: Arquivo `post.txt` ausente
  - **Ação**: Exibir erro e instruções de uso
- ❌ **Erro**: Formato inválido do arquivo
  - **Ação**: Exibir erro especificando formato esperado
- ❌ **Erro**: Fluxo especificado não existe
  - **Ação**: Listar fluxos disponíveis

### Validação de Execução
- Sistema não entra em loop
- Execução única por chamada
- Validação de API keys antes de iniciar
- Verificação de conectividade com APIs

---

## 📊 Sistema de Logs

### Estrutura de Logs
```
logs/
├── app_2025-10-17_14-30-25.log    # Log da execução atual
└── .gitkeep
```

### Níveis de Log (Configurável)
- **DEBUG**: Informações detalhadas para diagnóstico
- **INFO**: Confirmação de funcionamento normal
- **WARNING**: Indicação de problemas potenciais
- **ERROR**: Erros que impedem funcionalidades

### Limpeza Automática
- Logs e erros são limpos automaticamente a cada execução
- Mantém apenas dados da última execução
- Configurável via `config.ini`

---

## 🔧 Adicionando Novos Componentes

### Novo Agente
1. Criar pasta em `agents/novo_agente/`
2. Adicionar arquivos: `config.json`, `context.md`, `task.md`, `actions.md`
3. Configurar API e parâmetros
4. Adicionar agente ao fluxo desejado em `flows.json`

### Novo Fluxo
1. Criar arquivo Python em `flows/nome_fluxo.py`
2. Implementar classe herdando de `BaseFlow`
3. Adicionar configuração em `config/flows.json`
4. Documentar no README

### Nova API de IA
1. Criar serviço em `services/nova_api_service.py`
2. Implementar interface `AIService`
3. Adicionar credenciais no `.env`
4. Configurar em `agent_factory.py`
5. Disponibilizar para uso nos agentes

---

## 📝 .gitignore

```gitignore
# Environment
.env
*.env

# Logs e Errors
logs/
errors/
*.log

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/

# Docker
.docker/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Output temporário
data/output/*
!data/output/.gitkeep

# Cache
.pytest_cache/
.coverage
```

---

## 🎯 Roadmap

### Fase 1 (MVP)
- [x] Fluxo Post_Dicas
- [x] 3 agentes básicos
- [x] Integração Claude e Gemini
- [x] Sistema de logs

### Fase 2
- [ ] Interface web para gerenciamento
- [ ] Múltiplos fluxos simultâneos
- [ ] Dashboard de métricas
- [ ] Integração direta com WordPress

### Fase 3
- [ ] API REST para execução remota
- [ ] Agendamento de publicações
- [ ] Analytics e relatórios
- [ ] Suporte para mais idiomas

---

## 📚 Dependências (requirements.txt)

```txt
crewai==0.28.0
anthropic==0.18.0
google-generativeai==0.3.2
python-dotenv==1.0.0
pydantic==2.5.3
requests==2.31.0
beautifulsoup4==4.12.3
```

---