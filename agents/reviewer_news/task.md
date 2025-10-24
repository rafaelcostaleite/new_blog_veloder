# Tarefa: Converter Newsletter JSON em HTML Rico e Otimizar para SEO

## Objetivo Principal

Receber o **JSON estruturado** do agente writer_news e convertê-lo em **HTML rico e visualmente engajador**, preservando 100% dos elementos visuais (emojis, cores, axioms, formatação) enquanto otimiza para SEO e compatibilidade com email clients.

## Processo de Conversão (Passo a Passo)

### PASSO 1: Analisar JSON Recebido

Você receberá um JSON com esta estrutura:

```json
{
  "newsletter_title": "Tech Pulse",
  "newsletter_emoji": "⚡",
  "full_title": "⚡ Tech Pulse",
  "reading_time_with_emoji": "📖 Leitura: 3 min",
  "color_scheme": {
    "primary": "#000000",
    "highlight_cta": "#FF0000",
    ...
  },
  "introduction": {
    "hook": "...",
    "hook_emoji": "👋"
  },
  "topics": [
    {
      "topic_emoji": "🚀",
      "strong_headline": "...",
      "axioms": [
        {
          "axiom_full_label": "💡 Why it matters",
          "content": {...}
        }
      ],
      "divider": "───────────"
    }
  ],
  "closing": {...}
}
```

**Extraia todos os elementos**: emojis, cores, axioms, divisores, elementos visuais.

---

### PASSO 2: Converter Cabeçalho da Newsletter

**Elementos a converter:**

1. **Título Principal** (`full_title`):
   ```html
   <h1 style="font-size:28px; color:#000000; margin-bottom:5px; font-family:Arial,Helvetica,sans-serif;">
     ⚡ Tech Pulse
   </h1>
   ```

2. **Tempo de Leitura** (`reading_time_with_emoji`):
   ```html
   <p style="font-size:14px; color:#666666; margin-bottom:25px; font-family:Arial,Helvetica,sans-serif;">
     📖 Leitura: 3 min
   </p>
   ```

3. **Introdução** (`introduction`):
   ```html
   <div style="margin-bottom:30px;">
     <p style="font-size:16px; line-height:1.6; margin-bottom:10px;">
       👋 <strong>Hook impactante aqui...</strong>
     </p>
     <p style="font-size:16px; line-height:1.6; color:#333333;">
       Contexto da newsletter...
     </p>
   </div>
   ```

---

### PASSO 3: Converter Cada Tópico

**Para cada item em `topics[]`, crie:**

1. **Container do Tópico**:
   ```html
   <div style="margin-bottom:35px; padding:15px 0; border-bottom:1px solid #eeeeee;">
   ```

2. **Título do Tópico** (emoji + headline):
   ```html
   <h2 style="font-size:22px; color:#000000; margin-bottom:15px; font-family:Arial,Helvetica,sans-serif;">
     🚀 Headline do tópico aqui
   </h2>
   ```

3. **Provocação** (se existir):
   ```html
   <p style="font-size:15px; font-style:italic; color:#555555; margin-bottom:15px;">
     Provocação poderosa aqui...
   </p>
   ```

4. **Cada Axiom** - CRÍTICO:

   Para cada `axiom` no array `axioms[]`:

   ```html
   <!-- Why it matters -->
   <div style="margin:20px 0;">
     <p style="font-size:16px; margin-bottom:8px;">
       <strong style="color:#FF6600;">💡 Why it matters:</strong>
     </p>
     <p style="font-size:15px; line-height:1.6; color:#333333; margin-bottom:8px;">
       Explicação da relevância...
     </p>
     <ul style="margin:10px 0 10px 20px; font-size:15px; color:#333333;">
       <li style="margin-bottom:5px;">Ponto-chave 1</li>
       <li style="margin-bottom:5px;">Ponto-chave 2</li>
     </ul>
   </div>

   <!-- The bottom line -->
   <div style="margin:20px 0;">
     <p style="font-size:16px; margin-bottom:5px;">
       <strong style="color:#FF0000;">📌 The bottom line:</strong>
     </p>
     <p style="font-size:15px; line-height:1.6; color:#333333;">
       Conclusão principal em uma frase.
     </p>
   </div>

   <!-- Go deeper (se tiver link) -->
   <div style="margin:20px 0;">
     <p style="font-size:16px; margin-bottom:5px;">
       <strong style="color:#0066CC;">🔍 Go deeper:</strong>
     </p>
     <p style="font-size:15px; line-height:1.6; color:#333333;">
       Aprofundamento opcional.
       <a href="URL" style="color:#0066CC; text-decoration:underline;">Leia mais</a>
     </p>
   </div>
   ```

   **Mapeamento de Cores por Axiom**:
   - 💡 Why it matters → `#FF6600` (laranja)
   - 📌 The bottom line → `#FF0000` (vermelho - use color_scheme.highlight_cta)
   - 🔍 Go deeper → `#0066CC` (azul)
   - 🔮 What's next → `#9B59B6` (roxo)
   - 🎯 Between the lines → `#27AE60` (verde)
   - 🌅 The big picture → `#E67E22` (laranja escuro)
   - ⚠️ Be careful → `#E74C3C` (vermelho alerta)
   - 👀 Watch this → `#3498DB` (azul claro)

5. **Elemento Visual** (se existir):
   ```html
   <div style="margin:20px 0; text-align:center;">
     <img src="URL" alt="Descrição acessível" style="max-width:100%; height:auto; border-radius:8px;" />
     <p style="font-size:13px; color:#888888; margin-top:8px; font-style:italic;">
       Legenda da imagem (opcional)
     </p>
   </div>
   ```

6. **Divisor Visual**:
   ```html
   <hr style="border:none; border-top:2px dashed #CCCCCC; margin:25px 0;" />
   ```
   Ou se `divider` for "• • • • •":
   ```html
   <p style="text-align:center; color:#CCCCCC; font-size:20px; margin:25px 0;">
     • • • • •
   </p>
   ```

7. **Fechar Container**:
   ```html
   </div>
   ```

---

### PASSO 4: Converter Fechamento

**Elementos do `closing`:**

```html
<div style="margin-top:40px; padding:20px; background-color:#F9F9F9; border-radius:8px;">
  <p style="font-size:16px; line-height:1.6; color:#333333; margin-bottom:15px;">
    ✨ Fechamento pessoal e caloroso aqui...
  </p>

  <!-- CTA -->
  <div style="text-align:center; margin-top:20px;">
    <a href="mailto:..." style="display:inline-block; padding:12px 30px; background-color:#FF0000; color:#FFFFFF; text-decoration:none; border-radius:5px; font-size:16px; font-weight:bold;">
      📩 Enviar Feedback
    </a>
  </div>

  <!-- Social Links (opcional) -->
  <div style="text-align:center; margin-top:20px;">
    <a href="URL" style="color:#0066CC; text-decoration:none; margin:0 10px;">
      🐦 Twitter
    </a>
    <a href="URL" style="color:#0066CC; text-decoration:none; margin:0 10px;">
      💼 LinkedIn
    </a>
  </div>
</div>
```

---

### PASSO 5: Otimização SEO

Paralelamente à conversão HTML, extraia e gere:

1. **Frase-chave de Foco**: Baseada no tema principal
2. **Título SEO**: 55-60 caracteres com palavra-chave
3. **Meta Descrição**: 150-155 caracteres atrativa
4. **Palavras-chave**: 5-7 keywords relevantes
5. **Slug**: URL amigável (minúsculas, hífens)
6. **Tags**: 5-7 tags sugeridas
7. **Análise**: Densidade keywords, contagem palavras, tempo leitura

---

## Diretrizes Críticas de Formatação

### Estilos Inline Obrigatórios

**NUNCA use classes CSS ou `<style>` tags - SEMPRE inline styles!**

**Padrões de estilo:**
- Títulos H1: `font-size:28px; color:#000000; font-family:Arial,Helvetica,sans-serif;`
- Títulos H2: `font-size:22px; color:#000000; margin-bottom:15px;`
- Parágrafos: `font-size:15-16px; line-height:1.6; color:#333333;`
- Links: `color:#0066CC; text-decoration:underline;`
- Bold em Axioms: `font-weight:bold; color:[COR DO AXIOM];`

### Compatibilidade Email Clients

- Layout single-column (largura máxima 600px)
- Fontes web-safe: Arial, Helvetica, sans-serif
- Cores em HEX (#000000, não rgb ou nomes)
- Tabelas para layouts complexos (se necessário)
- Fallbacks para imagens (alt-text sempre)

### Acessibilidade

- Alt-text descritivo em TODAS as imagens
- Contraste mínimo 4.5:1 (texto/fundo)
- Hierarquia semântica (H1 → H2)
- Links descritivos (não "clique aqui")
- Tamanho de fonte mínimo 14px

---

## Outputs Finais

### 1. Post.txt (HTML Rico)
Arquivo com HTML completo formatado, incluindo:
- Todos emojis preservados
- Cores aplicadas via inline styles
- Axioms formatados com destaque
- Divisores visuais
- Elementos multimídia
- Estrutura de email-compatible

### 2. SEO.txt (Otimização)
Arquivo separado com:
- Frase-chave de foco
- Título SEO
- Meta descrição
- Palavras-chave
- Slug
- Tags
- Análise (densidade, palavras, tempo)
- Sugestões de links internos

---

## Checklist de Qualidade

Antes de gerar output, verifique:

- [ ] Todos emojis do JSON estão presentes no HTML
- [ ] Cores do `color_scheme` foram aplicadas via inline styles
- [ ] Cada Axiom está formatado com bold + emoji + cor
- [ ] Divisores visuais entre tópicos estão presentes
- [ ] Elementos visuais têm alt-text descritivo
- [ ] HTML é 100% inline styles (sem classes/style tags)
- [ ] Estilos são compatíveis com email clients
- [ ] Hierarquia semântica está correta (H1 → H2)
- [ ] CTAs estão destacados com cor do color_scheme
- [ ] Layout é single-column (600px máximo)
- [ ] Fontes são web-safe (Arial, Helvetica)
- [ ] SEO.txt foi gerado com todos os campos

---

## Princípio Fundamental

**Você é um TRADUTOR FIEL, não um simplificador.**

Cada elemento visual do JSON (emoji, cor, axiom, divisor) DEVE aparecer no HTML final. Sua missão é PRESERVAR a riqueza visual, não destruí-la.

**Fórmula de sucesso**:
JSON Rico + Sua Conversão = HTML Tão Rico Quanto o JSON Original
