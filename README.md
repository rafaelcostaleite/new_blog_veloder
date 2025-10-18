# 🤖 Sistema Multi-Agentes para Criação de Posts de Blog

Sistema automatizado de geração de conteúdo para blogs usando múltiplas APIs de IA (Claude e Gemini) organizadas em fluxos de trabalho colaborativos.

## 📋 Descrição

Este projeto utiliza o conceito de **agentes especializados** que trabalham em sequência para criar posts de blog de alta qualidade, otimizados para SEO e prontos para publicação no WordPress.

### Pipeline de Agentes

1. **Researcher** (Gemini) - Pesquisa informações atualizadas na web
2. **Writer** (Gemini) - Escreve o conteúdo do post
3. **Reviewer** (Claude) - Revisa, formata em HTML e otimiza para SEO

## 🏗️ Tecnologias

- **Python 3.11+**
- **Docker & Docker Compose**
- **APIs de IA:**
  - Anthropic Claude (Sonnet 4)
  - Google Gemini Pro
- **Bibliotecas:**
  - CrewAI
  - python-dotenv
  - anthropic
  - google-generativeai

## 📁 Estrutura do Projeto

```
projeto-multi-agentes/
├── agents/                  # Configurações dos agentes
│   ├── researcher/         # Agente pesquisador
│   ├── writer/            # Agente escritor
│   └── reviewer/          # Agente revisor
├── config/                 # Arquivos de configuração
│   ├── config.ini
│   └── flows.json
├── flows/                  # Gerenciador de fluxos
├── services/              # Serviços de API
├── utils/                 # Utilitários
├── data/
│   ├── input/            # Arquivos de entrada
│   └── output/           # Posts gerados
├── logs/                  # Logs de execução
├── errors/               # Logs de erros
├── main.py              # Ponto de entrada
├── Dockerfile
└── docker-compose.yml
```

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd new_blog_veloder

# Copie o arquivo de exemplo de variáveis de ambiente
cp .env.example .env

# Edite o arquivo .env e adicione suas API keys
# ANTHROPIC_API_KEY=sua_chave_aqui
# GOOGLE_API_KEY=sua_chave_aqui
```

### 2. Crie o Arquivo de Entrada

Crie um arquivo `data/input/post.txt` com o seguinte formato:

```
Fluxo: Post_Esportivo
Assunto: Benefícios de utilizar a camiseta UV nos treinos de corrida e Maratonas
```

### 3. Execute com Docker

```bash
# Build da imagem
docker-compose build

# Executar o sistema
docker-compose up
```

### 4. OU Execute Localmente

```bash
# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

### 5. Resultado

Os arquivos gerados estarão em `data/output/`:
- `Post.txt` - Post formatado em HTML
- `SEO.txt` - Dados de SEO (título, meta descrição, palavras-chave, slug)

## ⚙️ Configuração

### Arquivo de Entrada (`data/input/post.txt`)

```
Fluxo: Post_Esportivo
Assunto: [Seu assunto aqui]
```

### Fluxos Disponíveis

Veja os fluxos disponíveis em `config/flows.json`:
- **Post_Esportivo** - Criação de posts sobre esportes

## 🔧 Adicionando Novos Componentes

### Novo Agente

1. Crie uma pasta em `agents/novo_agente/`
2. Adicione 4 arquivos:
   - `config.json` - Configuração técnica
   - `context.md` - Personalidade e expertise
   - `task.md` - Descrição da tarefa
   - `actions.md` - Ações permitidas e formato de output

### Novo Fluxo

1. Edite `config/flows.json`
2. Adicione a configuração do novo fluxo
3. Especifique agentes e ordem de execução

### Nova API de IA

1. Crie `services/nova_api_service.py`
2. Implemente a interface `AIService`
3. Adicione credenciais no `.env`
4. Configure em `agent_factory.py`

## 📊 Sistema de Logs

- **Logs gerais:** `logs/app_YYYY-MM-DD_HH-MM-SS.log`
- **Logs de erro:** `errors/error_YYYY-MM-DD_HH-MM-SS.log`
- Logs são limpos automaticamente a cada execução (configurável)

## ✅ Validações

O sistema valida:
- Presença de API keys
- Formato do arquivo de entrada
- Existência de apenas um arquivo em `data/input/`
- Fluxo especificado existe em `flows.json`

## 🎯 Exemplo de Saída

### Post.txt
```html
<h1>7 Benefícios da Camiseta UV para Corredores</h1>

<p>Se você é corredor ou está se preparando para uma maratona...</p>

<h2>1. Proteção Contra Raios UV</h2>
<p>As camisetas UV oferecem proteção solar de FPS 50+...</p>
```

### SEO.txt
```
=== DADOS SEO ===

Título SEO:
7 Benefícios da Camiseta UV para Corrida | Guia 2025

Meta Descrição:
Descubra os principais benefícios da camiseta UV para corrida e maratonas. Proteção solar, conforto térmico e performance.

Palavras-chave:
camiseta uv corrida, proteção solar running, roupa para maratona

Slug:
beneficios-camiseta-uv-corrida-maratona
```

## 🐛 Troubleshooting

### Erro: "API keys não configuradas"
- Verifique se o arquivo `.env` existe
- Confirme que as chaves estão corretas

### Erro: "Nenhum arquivo .txt encontrado"
- Crie o arquivo `data/input/post.txt`
- Siga o formato especificado

### Erro: "Múltiplos arquivos encontrados"
- Mantenha apenas um arquivo `.txt` em `data/input/`

## 📝 Licença

Este projeto é de código aberto.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
1. Fazer fork do projeto
2. Criar uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abrir um Pull Request

## 📧 Contato

Para dúvidas e sugestões, abra uma issue no repositório.

---

**Desenvolvido com IA para criar conteúdo de qualidade automaticamente** 🚀
