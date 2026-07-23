# Digify — site completo

20 páginas HTML, 3 idiomas na home, blog com 32 artigos únicos, 4 hubs de categoria.
**Nenhuma URL antiga mudou de endereço.**

---

## SUBIR EM 5 PASSOS

### 1. Desative o workflow antigo (ANTES de tudo)
GitHub → Actions → "Gerar Artigo no Blog" → **Disable workflow**.
Se não fizer isso, o cron das 09h sobrescreve a home nova.

### 2. Copie os arquivos para o repositório
Sobrescreva o que existir. **Não apague** as pastas `blog/<slug>/` dos artigos
já publicados — elas continuam lá e serão reaproveitadas no passo 3.

### 3. Migre os artigos existentes (uma vez só)
```bash
python3 _build/migrate_posts.py            # simula e mostra o que vai extrair
python3 _build/migrate_posts.py --write    # grava os post.json
python3 _build/build.py                    # renderiza o site inteiro
```

### 4. Limpe o que ficou obsoleto
- `blog/post-template.html` — **está indexável hoje** em
  `digify.live/blog/post-template.html`, servindo `{{POST_TITLE}}` como título
- `blog/exemplo-do-novo-layout/` — amostra que fiz para você ver o layout
- `css/` e `js/` — só depois de conferir que nenhum artigo aponta para `/css/style.css`

### 5. Commit, push e reative o workflow
O `.github/workflows/generate-blog.yml` novo já roda `build.py` antes do commit.

---

## O QUE MUDOU NESTA ENTREGA

### WhatsApp
Novo número **(11) 98991-1000** em todo o site: header, footer, botão flutuante,
formulários, banners dos artigos e `contactPoint` do schema.

### Conversão dentro de cada artigo
Cada post agora tem **10 links para páginas de serviço e 8 para o contato**:

- **Banner escuro no meio do texto**, inserido automaticamente antes de um `<h2>`
  do miolo, com copy específica da categoria. O de SEO diz "Seu concorrente está
  na frente agora?", o de e-commerce "Quantos carrinhos sua loja perde por mês?".
- **CTA no fim** apontando para a página de serviço da categoria do artigo.
- **Links internos automáticos**: expressões como "criação de sites", "loja
  virtual", "Google Ads" ou "sistema sob medida" viram link para a página de
  serviço correspondente. Só a primeira ocorrência, nunca dentro de título,
  nunca dentro de link existente, máximo 4 por artigo — para não virar spam.
- **Caixa de autor** ao final, com link para `/sobre/` (sinal de E-E-A-T).
- **Índice automático** montado dos `<h2>`, com âncoras. Aumenta tempo de leitura
  e habilita o Google a mostrar links de seção direto no resultado.

### Hubs de categoria (novo)
`/blog/seo/`, `/blog/criacao-de-sites/`, `/blog/desenvolvimento-de-apps/` e
`/blog/marketing-digital/`. Cada um com H1 próprio atacando o termo da categoria,
texto de abertura original, lista dos artigos e link para a página de serviço.
São 4 páginas indexáveis a mais e caminhos de rastreamento melhores.

### Fontes locais (Core Web Vitals)
As três fontes saíram do Google Fonts e passaram a ser servidas do próprio
domínio, em WOFF2 variável com subset latino: **376 KB no total**, contra
1,25 MB dos TTF originais. Some duas conexões a terceiros e uma requisição
bloqueante de renderização. As duas fontes críticas têm `preload`.
Bônus de LGPD: o IP do visitante não vai mais para o Google.

### Canibalização resolvida
10 clusters identificados, 12 URLs redirecionadas com `301!` no `_redirects`,
índice podado de 44 para 32 artigos. Três clusters tinham três artigos sobre o
mesmo tema. Sitemap não contém nenhuma URL que redireciona.

### Bug do gerador corrigido
A v1 conferia duplicata com `slugify(assunto)` mas gravava `slugify(título)`.
Como nunca coincidiam, o catálogo era sorteado indefinidamente. Agora o assunto
é gravado no índice (campo `subject`) e conferido contra ele mesmo. Catálogo
ampliado de 42 para 110 assuntos, com E-commerce e Sistemas incluídos.

### Outros
- `404.html` customizada, com `noindex, follow` e três saídas úteis
- `llms.txt` — guia para crawlers de IA, aumenta a chance de a Digify ser citada
  em resposta gerada (ChatGPT, Perplexity, AI Overviews)
- `blog/rss.xml` com os 30 posts mais recentes
- `sitemap.xml` com 50 URLs, `lastmod` nos artigos e alternates de idioma
- Organization com `logo`, `contactPoint`, `knowsLanguage` e `slogan`
- Cache imutável de um ano para `/assets/*` no `_headers`

---

## COMO EDITAR

Nunca edite os `index.html` — são gerados. Edite em `_build/` e rode
`python3 _build/build.py`. Sem dependências além do Python 3.

| Arquivo | O que contém |
|---|---|
| `_build/content.py` | texto das 3 home, telefone, lista de clientes |
| `_build/services_pt.py` | as 6 páginas de serviço |
| `_build/pages_pt.py` | sobre, contato, privacidade |
| `_build/cases_pt.py` | os 6 projetos do portfólio |
| `_build/postpage.py` | artigos, hubs de categoria, banner, autolink |
| `_build/inner.py` | hub de serviços, blog, institucionais |
| `_build/build.py` | home, sitemap, robots, 404, llms.txt |

Para mudar a copy dos banners dos artigos: `BANNER_COPY` em `postpage.py`.
Para mudar os termos que viram link interno: `ILINKS`, no mesmo arquivo.

---

### Portfólio (novo)
`/portfolio/` com 6 projetos e uma seção de 3 cases em destaque na home, entre
serviços e processo. Cada case tem cliente, setor, ano, o problema, o escopo
entregue em itens, a stack e link para o site no ar.

As seis capturas já estão processadas em `assets/cases/`: recortadas em 16:10 pelo
topo, redimensionadas para 1600×1000 e comprimidas para 689 KB no total, com
`width`, `height` e `loading="lazy"` para não penalizar o LCP. Para trocar
qualquer uma, é só substituir o `.jpg` e rodar `build.py`.

**O campo `resultado` de cada case está VAZIO de propósito.** Número de cliente é
afirmação séria e eu não invento. Preencha em `_build/cases_pt.py` com o que
você puder comprovar — o card omite o bloco sozinho enquanto estiver vazio.

Também vale conferir os textos: escrevi cada case a partir do que sei dos
projetos que fizemos juntos, mas você é quem sabe se o escopo está completo.

## O QUE AINDA FALTA (por ordem de impacto)

1. **Search Console.** Verifique a propriedade do tipo Domínio e envie o sitemap
   **depois** do deploy (hoje ele responde 404).
2. **Páginas internas em EN e ES.** Só as home estão traduzidas.
4. **Autoridade.** Nada de link building, Perfil da Empresa no Google ou
   citações. É a perna que decide termo competitivo.
5. **Revisar meus números.** Prazos e faixas de orçamento no FAQ e nas páginas
   de serviço são plausíveis mas foram escritos por mim.
6. **`aggregateRating`** provavelmente não renderiza estrela: o Google trata
   avaliação publicada pela própria empresa como self-serving.

---

# Como rodar a migração (passo 3)

O script precisa dos arquivos do repositório, então roda **dentro dele** — não
adianta rodar só na pasta do ZIP. Duas formas:

## Opção A — pelo GitHub, sem instalar nada (recomendada)

Já vai um workflow pronto para isso.

1. Suba o ZIP para o repositório (inclusive `.github/workflows/`)
2. GitHub → **Actions** → "🔧 Migração dos artigos (rodar UMA vez)"
3. **Run workflow** → no campo de confirmação, digite `MIGRAR` → **Run**
4. Espera cerca de um minuto e acompanha o log

Ele simula, migra, renderiza o site, apaga o `post-template.html` e a pasta de
exemplo, e commita sozinho. O Netlify publica em seguida.

**Depois que rodar com sucesso, apague `.github/workflows/migrar-uma-vez.yml`.**
Ele não serve mais e só ocupa espaço no menu de Actions.

A confirmação por digitação existe de propósito: é um workflow que reescreve 44
arquivos, e clique acidental sai caro.

## Opção B — local

Precisa de Python 3 instalado (`python3 --version` para conferir).

```bash
git clone https://github.com/msrougi/digify-site.git
cd digify-site
# descompacte o ZIP por cima aqui

python3 _build/migrate_posts.py           # simula
python3 _build/migrate_posts.py --write   # grava
python3 _build/build.py                   # renderiza

git add -A
git commit -m "Site novo + migração dos artigos"
git push
```

No Windows, troque `python3` por `python`.

A vantagem da opção B é que você vê o resultado antes de publicar: abra
`blog/<qualquer-slug>/index.html` no navegador e confira se o artigo ficou certo.
