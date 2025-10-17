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
│   │   ├── config.json         # Configuração do agente
│   │   ├── context.md          # Contexto e personalidade
│   │   ├── task.md             # Descrição da tarefa
│   │   └── actions.md          # Ações específicas
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
      "name": "Post_Dicas",
      "description": "Fluxo para criação de posts com dicas",
      "agents": [
        {
          "id": "researcher",
          "order": 1,
          "api": "claude"
        },
        {
          "id": "writer",
          "order": 2,
          "api": "gemini"
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
- **API**: Claude
- **Função**: Pesquisar dados atualizados na internet sobre o assunto
- **Input**: `data/input/post.txt` (assunto especificado)
- **Output**: JSON estruturado com dados de pesquisa
- **Arquivo de Configuração**: `agents/researcher/config.json`

**Exemplo de config.json:**
```json
{
  "name": "Researcher",
  "role": "Pesquisador de Conteúdo",
  "api": "claude",
  "model": "claude-sonnet-4-20250514",
  "temperature": 0.7,
  "max_tokens": 4000
}
```

**context.md:**
```markdown
# Contexto do Agente Pesquisador

Você é um pesquisador especializado em buscar informações atualizadas e relevantes na internet. Sua função é coletar dados precisos, estatísticas recentes e referências confiáveis sobre o tema solicitado.

## Características:
- Foco em fontes confiáveis
- Prioriza dados atualizados (últimos 12 meses)
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

---

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

## 🤝 Contribuindo

Para contribuir com o projeto:
1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

## 📄 Licença

[Definir licença do projeto]

---

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no GitHub
- Consulte a documentação completa
- Entre em contato com a equipe de desenvolvimento

---

**Última atualização**: Outubro 2025  
**Versão**: 1.0.0