# 🚀 Guia Rápido de Uso

## 1. Configuração Inicial (5 minutos)

### Passo 1: Configure as API Keys
```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione suas chaves
nano .env
```

No arquivo `.env`, adicione:
```env
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyxxxxxxxxxxxxxxxxx
```

### Passo 2: Prepare o Arquivo de Entrada

O arquivo `data/input/post.txt` já está criado como exemplo. Você pode editá-lo:

```bash
nano data/input/post.txt
```

Formato:
```
Fluxo: Post_Esportivo
Assunto: [Seu assunto aqui]
```

## 2. Executar com Docker (Recomendado)

```bash
# Build da imagem (primeira vez)
docker-compose build

# Executar o sistema
docker-compose up
```

## 3. OU Executar Localmente

```bash
# Criar ambiente virtual (opcional mas recomendado)
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Executar
python main.py
```

## 4. Verificar Resultados

Os arquivos gerados estarão em `data/output/`:

```bash
ls -l data/output/
```

Você encontrará:
- **Post.txt** - Post completo formatado em HTML
- **SEO.txt** - Dados de SEO (título, meta descrição, palavras-chave, slug)

## 5. Ver Logs

```bash
# Ver logs da execução
ls -l logs/

# Ver último log
tail -f logs/app_*.log

# Ver erros (se houver)
ls -l errors/
```

## ✅ Checklist de Troubleshooting

### ❌ Erro: "API keys não configuradas"
- [ ] Arquivo `.env` existe?
- [ ] As chaves estão corretas?
- [ ] Não há espaços extras nas chaves?

### ❌ Erro: "Nenhum arquivo .txt encontrado"
- [ ] Existe `data/input/post.txt`?
- [ ] O arquivo tem conteúdo?

### ❌ Erro: "Múltiplos arquivos encontrados"
- [ ] Há apenas UM arquivo `.txt` em `data/input/`?

### ❌ Erro: "Fluxo não encontrado"
- [ ] O nome do fluxo está correto? Use: `Post_Esportivo`
- [ ] O arquivo `config/flows.json` existe?

## 🎯 Exemplo de Uso Completo

```bash
# 1. Configurar API keys
cp .env.example .env
# Edite .env com suas chaves

# 2. Criar seu arquivo de entrada
echo "Fluxo: Post_Esportivo
Assunto: Melhores técnicas de respiração para corredores iniciantes" > data/input/post.txt

# 3. Executar
docker-compose up

# 4. Ver resultado
cat data/output/Post.txt
cat data/output/SEO.txt
```

## 📊 Fluxo de Execução

```
1. Sistema lê data/input/post.txt
2. Identifica o fluxo: Post_Esportivo
3. Executa 3 agentes em sequência:
   ├─ Researcher (Gemini) - Pesquisa dados atualizados
   ├─ Writer (Gemini) - Escreve o post
   └─ Reviewer (Claude) - Revisa e otimiza SEO
4. Gera arquivos em data/output/
5. Exibe resultado no console
```

## 🔄 Para Gerar Novo Post

```bash
# 1. Limpar output anterior
rm data/output/*

# 2. Atualizar assunto
echo "Fluxo: Post_Esportivo
Assunto: [Novo assunto]" > data/input/post.txt

# 3. Executar novamente
docker-compose up
```

## 💡 Dicas

1. **Primeira execução**: Pode demorar alguns minutos devido ao download de dependências do Docker
2. **Custos de API**: Cada execução consome créditos das APIs (Claude + Gemini)
3. **Qualidade do input**: Quanto mais específico o assunto, melhor o resultado
4. **Logs**: Sempre verifique os logs para entender o que está acontecendo

## 📚 Próximos Passos

- Leia o [README.md](README.md) completo para entender a arquitetura
- Veja o [claude.md](claude.md) para especificações detalhadas
- Customize os agentes em `agents/*/` para ajustar o comportamento
- Crie novos fluxos editando `config/flows.json`

---

**Pronto para criar conteúdo de qualidade automaticamente!** 🎉
