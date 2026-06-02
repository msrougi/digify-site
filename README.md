# Digify.live — Site HTML + Blog Automático com IA

## Estrutura do Projeto

```
digify/
├── index.html                    # Homepage
├── blog/
│   ├── index.html                # Listagem do blog
│   ├── index.json                # Índice dos posts (gerado automaticamente)
│   └── post-template.html        # Template para posts
├── css/style.css                 # Design system completo
├── js/main.js                    # JavaScript do site
├── generate-posts.js             # Script de geração de artigos via Claude
├── seo-foda.html                 # Plano FODA de SEO
└── .github/workflows/
    └── generate-blog.yml         # GitHub Action para agendamento
```

## Como publicar

### Opção 1 — GitHub Pages (gratuito)
1. Crie um repositório no GitHub: `github.com/seu-usuario/digify-site`
2. Faça upload de todos os arquivos
3. Em Settings > Pages: selecione branch `main`, pasta `/root`
4. Configure o domínio `digify.live` nas configurações de DNS

### Opção 2 — Netlify (gratuito, mais recursos)
1. Arraste a pasta `digify/` para app.netlify.com
2. Configure domínio personalizado nas configurações
3. O deploy é automático a cada push no GitHub

### Opção 3 — Vercel (gratuito)
1. `npm install -g vercel`
2. `cd digify && vercel`
3. Siga as instruções e configure o domínio

---

## Blog Automático com IA

### Configuração inicial

1. Instale Node.js 18+ no seu servidor ou máquina
2. Defina a variável de ambiente com sua API key da Anthropic:
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-api03-..."
   ```

### Gerar artigos manualmente
```bash
node generate-posts.js            # 1 artigo
node generate-posts.js --count 5  # 5 artigos de uma vez
```

### Agendamento automático com GitHub Actions

1. No seu repositório GitHub, vá em **Settings > Secrets > Actions**
2. Clique em "New repository secret"
3. Nome: `ANTHROPIC_API_KEY`
4. Valor: sua chave da API Anthropic (sk-ant-...)
5. O arquivo `.github/workflows/generate-blog.yml` já está configurado para rodar todo dia às 09:00 (horário de Brasília)
6. Você também pode disparar manualmente em **Actions > Gerar Artigo no Blog > Run workflow**

### Agendamento com cron (servidor VPS)
```bash
# Edite o crontab
crontab -e

# Adicione esta linha para gerar 1 artigo por dia às 08:00
0 8 * * * cd /var/www/digify && node generate-posts.js >> logs/blog.log 2>&1
```

---

## Plano FODA de SEO

Abra `seo-foda.html` no navegador para ver o plano completo de SEO com:
- Análise FODA detalhada
- Mapa de palavras-chave com volumes
- Estrutura de páginas recomendada
- Roadmap de 6 meses
- Checklist de Schemas

---

## Próximos passos (páginas a criar)

- [ ] `/servicos/criacao-de-sites/index.html`
- [ ] `/servicos/desenvolvimento-de-apps/index.html`
- [ ] `/servicos/seo/index.html`
- [ ] `/servicos/marketing-digital/index.html`
- [ ] `/servicos/ecommerce/index.html`
- [ ] `/sobre/index.html`
- [ ] `/contato/index.html`
- [ ] `/sitemap.xml`
- [ ] `/robots.txt`

---

## Custos

| Item | Custo |
|------|-------|
| Hospedagem (GitHub Pages / Netlify) | Gratuito |
| Domínio digify.live | ~R$ 60/ano |
| Blog com IA (1 artigo/dia) | ~R$ 15-30/mês |
| Blog com IA (1 artigo/semana) | ~R$ 5/mês |
| WordPress anterior | Economizado 🎉 |
