#!/usr/bin/env node
/**
 * DIGIFY BLOG AUTO-GENERATOR v2 — Gemini 2.5 Flash
 *
 * MUDANÇAS EM RELAÇÃO À v1:
 *  1. Deduplicação corrigida. A v1 comparava slugify(assunto) contra uma lista
 *     que guardava slugify(título). Como os dois quase nunca coincidem, o mesmo
 *     assunto era sorteado de novo indefinidamente — resultado: 14 pares de
 *     artigos canibalizando a mesma palavra-chave. Agora o assunto é gravado
 *     no índice e conferido contra ele.
 *  2. Catálogo ampliado de 42 para 100+ assuntos, incluindo E-commerce e
 *     Sistemas, que existiam no site mas não na lista.
 *  3. Não escreve mais HTML nem mexe no index.html. Grava o artigo em
 *     blog/<slug>/post.json e o build.py renderiza tudo com o design do site.
 *     Uma mudança de layout passa a valer para os 44 artigos já publicados.
 *
 * USO:  node generate-posts.js [--count N]
 */

const fs   = require('fs');
const path = require('path');

const BLOG_DIR   = path.join(__dirname, 'blog');
const INDEX_FILE = path.join(BLOG_DIR, 'index.json');
const API_KEY      = process.env.GEMINI_API_KEY;
const UNSPLASH_KEY = process.env.UNSPLASH_ACCESS_KEY;
const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`;

if (!API_KEY) { console.error('❌  Defina GEMINI_API_KEY antes de rodar.'); process.exit(1); }

const TOPICS = [
  { category: 'SEO', subjects: [
    'Como criar um site que rankeia no Google',
    'SEO local: como aparecer no Google Maps da sua cidade',
    'Core Web Vitals: o que são e como melhorar a nota do seu site',
    'Link building white hat: estratégias seguras para ganhar autoridade',
    'Como fazer uma auditoria de SEO completa no seu site',
    'SEO para e-commerce: guia completo para lojas virtuais',
    'Palavras-chave de cauda longa: como encontrar e usar',
    'SEO on-page: o checklist completo para otimizar cada página',
    'Como aparecer na posição zero do Google',
    'Velocidade do site e SEO: por que cada segundo importa',
    'O que é E-E-A-T e como aplicar no seu site',
    'Como usar o Google Search Console do zero',
    'Dados estruturados: como marcar seu site com Schema.org',
    'SEO técnico: rastreamento, indexação e arquitetura de site',
    'Como recuperar tráfego orgânico depois de uma queda',
    'Search intent: como alinhar conteúdo à intenção de busca',
    'Canonical, noindex e robots.txt: quando usar cada um',
    'Como o SEO funciona dentro das respostas geradas por IA',
    'Redirecionamento 301 sem perder posição no Google',
    'SEO para site multilíngue: hreflang na prática',
    'Como escolher palavras-chave para um negócio local',
    'Sitemap XML: como montar e enviar corretamente',
    'Pilar e cluster: como estruturar conteúdo que rankeia',
    'Como analisar a concorrência orgânica passo a passo',
  ]},
  { category: 'Criação de Sites', subjects: [
    'Quanto custa criar um site profissional',
    'WordPress ou site em HTML: qual escolher para seu negócio',
    'Landing page que converte: os elementos indispensáveis',
    'Como escolher a agência certa para criar o site da sua empresa',
    'Site responsivo: por que mobile-first é obrigatório hoje',
    'Como criar um site rápido: guia técnico para iniciantes',
    'UX design para sites: princípios que aumentam conversão',
    'Copywriting para sites: como escrever textos que vendem',
    'Hospedagem de sites: como escolher a melhor opção',
    'O que é um site institucional e quando sua empresa precisa de um',
    'Quantas páginas o site da sua empresa realmente precisa',
    'Como estruturar a página de serviços para gerar orçamento',
    'Formulário de contato: quantos campos antes de espantar o cliente',
    'Acessibilidade web: o mínimo que todo site deveria ter',
    'Como migrar de site sem perder tráfego',
    'Prova social em site: depoimento, número e case',
    'Tipografia para web: como escolher fontes que não pesam',
    'Página 404: como transformar erro em oportunidade',
    'Site próprio ou construtor pronto: o custo real em três anos',
    'Checklist antes de colocar um site no ar',
  ]},
  { category: 'Desenvolvimento de Apps', subjects: [
    'MVP de aplicativo: como validar sua ideia antes de investir',
    'React Native ou Flutter: qual usar no seu app',
    'Quanto custa desenvolver um aplicativo do zero',
    'UX para aplicativos: princípios que retêm usuários',
    'Como monetizar um aplicativo: modelos que funcionam',
    'Aplicativo nativo ou PWA: quando escolher cada um',
    'Como preparar o briefing do seu app para uma agência',
    'App Store Optimization: como rankear nas lojas',
    'Segurança em apps móveis: o que toda empresa precisa saber',
    'Como integrar APIs no seu aplicativo mobile',
    'Push notification sem irritar o usuário',
    'Onboarding de app: as primeiras telas decidem tudo',
    'Como publicar na App Store e no Google Play sem surpresa',
    'Offline first: apps que funcionam sem conexão',
    'Métricas de app que realmente importam',
    'Como testar um app antes do lançamento',
  ]},
  { category: 'Marketing Digital', subjects: [
    'Google Ads ou Meta Ads: onde investir primeiro',
    'Como criar uma estratégia de conteúdo que gera leads',
    'Taxa de conversão: como calcular e melhorar a sua',
    'E-mail marketing ainda funciona? Dados e estratégias atuais',
    'Como usar o Google Analytics 4 para tomar decisões',
    'Funil de vendas digital: da atração ao fechamento',
    'Como medir ROI de campanhas digitais com precisão',
    'O que é tráfego pago e como começar do zero',
    'Remarketing: como recuperar visitantes que não converteram',
    'Como criar anúncios no Google Ads que realmente convertem',
    'Custo por aquisição: quanto você pode pagar por cliente',
    'Landing page para tráfego pago: o que muda',
    'Como estruturar campanha por intenção de busca',
    'Teste A/B: como fazer sem enganar a si mesmo',
    'Rastreamento de conversão: configurar antes de gastar',
    'Automação de marketing para empresa pequena',
    'Como calcular o valor de um lead para o seu negócio',
    'Nutrição de leads: o que enviar e quando',
  ]},
  { category: 'E-commerce', subjects: [
    'Como reduzir o abandono de carrinho na sua loja',
    'Checkout que converte: quantos passos até a compra',
    'Pix no e-commerce: taxa, aprovação e como configurar',
    'Como calcular frete sem perder venda',
    'WooCommerce ou plataforma fechada: o custo em três anos',
    'Página de produto que vende: estrutura completa',
    'Como integrar sua loja com marketplaces',
    'Antifraude no e-commerce: como reduzir chargeback',
    'Recuperação de carrinho abandonado por e-mail e WhatsApp',
    'Como organizar categorias e filtros numa loja grande',
    'Avaliações de produto: como coletar e exibir',
    'Migração de loja virtual sem perder SEO',
  ]},
  { category: 'Sistemas', subjects: [
    'Quando vale desenvolver um sistema sob medida',
    'Como integrar ERP com loja virtual',
    'Planilha que virou sistema: sinais de que passou da hora',
    'API REST explicada para quem não é desenvolvedor',
    'Automação de processos: por onde começar',
    'Como escrever um briefing de sistema para uma agência',
    'Controle de acesso e perfis: o básico que evita problema',
    'Webhooks: como fazer dois sistemas conversarem',
    'Backup e continuidade: o que sua empresa precisa ter',
    'Como migrar dados de um sistema antigo sem perder nada',
  ]},
];

const slugify = s => s.toLowerCase()
  .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
  .replace(/[^a-z0-9\s-]/g, '').trim().replace(/\s+/g, '-').substring(0, 80);

const readableDate = iso => new Date(iso).toLocaleDateString('pt-BR',
  { day: '2-digit', month: 'long', year: 'numeric' });

const pickRandom = a => a[Math.floor(Math.random() * a.length)];

function loadIndex() {
  if (!fs.existsSync(INDEX_FILE)) return [];
  try { return JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8')); } catch { return []; }
}

async function callGemini(prompt) {
  const resp = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: [{ text: prompt }] }],
      generationConfig: { temperature: 0.7, maxOutputTokens: 8192 },
    }),
  });
  if (!resp.ok) throw new Error(`Gemini API ${resp.status}: ${(await resp.text()).slice(0, 200)}`);
  const data = await resp.json();
  const text = data.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!text) throw new Error('Resposta inesperada: ' + JSON.stringify(data).slice(0, 200));
  return text.trim();
}

const CONTEXT = `Você é especialista em marketing digital, SEO e tecnologia web com mais de 10 anos de experiência. Escreve para o blog da Digify, agência web brasileira de criação de sites, sistemas e SEO. Português brasileiro natural, tom profissional e direto, sem jargão vazio.`;

async function generateArticle(subject, category) {
  console.log(`\n🤖  Gerando: "${subject}" (${category})`);

  const metaRaw = await callGemini(
    `${CONTEXT}\n\nPara o tema "${subject}" (categoria: ${category}), responda APENAS com duas linhas:\nLINHA1: [título SEO com até 60 caracteres]\nLINHA2: [meta description de 150-160 caracteres com a palavra-chave principal]`
  );
  const lines = metaRaw.split('\n')
    .map(l => l.replace(/^LINHA\d:\s*/i, '').replace(/^\[|\]$/g, '').trim())
    .filter(Boolean);
  const title   = lines[0] || subject;
  const excerpt = lines[1] || `Guia completo da Digify sobre ${subject.toLowerCase()}.`;
  console.log(`   📝 ${title}`);

  await new Promise(r => setTimeout(r, 2000));

  const content = await callGemini(
    `${CONTEXT}\n\nEscreva um artigo completo em HTML sobre: "${title}"\nCategoria: ${category}\n\nREGRAS:\n- Retorne APENAS o HTML do corpo (sem DOCTYPE, html, head ou body)\n- Use h2, h3, p, ul, ol, strong. NÃO use h1\n- Mínimo 1200 palavras, ao menos 5 seções com h2\n- Introdução, desenvolvimento detalhado e conclusão\n- Seja concreto: números, exemplos e passos, não generalidade\n- No final, mencione com naturalidade que a Digify trabalha com ${category.toLowerCase()}`
  );

  return { title, excerpt, content };
}

async function fetchUnsplashImage(category, fallbackAlt) {
  if (!UNSPLASH_KEY) return null;
  const kw = {
    'SEO': 'seo analytics dashboard',
    'Criação de Sites': 'web design workspace laptop',
    'Desenvolvimento de Apps': 'mobile app development smartphone',
    'Marketing Digital': 'digital marketing team meeting',
    'E-commerce': 'ecommerce online shopping delivery',
    'Sistemas': 'software engineer code server',
  }[category] || 'technology business';
  try {
    const r = await fetch(`https://api.unsplash.com/photos/random?query=${encodeURIComponent(kw)}&orientation=landscape&client_id=${UNSPLASH_KEY}`);
    if (!r.ok) return null;
    const d = await r.json();
    return {
      url: d.urls?.regular || null,
      alt: d.alt_description || fallbackAlt,
      author: d.user?.name || 'Unsplash',
      authorUrl: d.user?.links?.html || 'https://unsplash.com',
    };
  } catch { return null; }
}

async function main() {
  const args  = process.argv.slice(2);
  const count = parseInt(args[args.indexOf('--count') + 1] || '1', 10) || 1;

  console.log(`\n🚀  Digify Blog Generator v2 — ${count} artigo(s)`);

  const index = loadIndex();
  const usedSlugs    = new Set(index.map(p => p.slug));
  // ↓ a correção: o assunto é conferido contra o assunto, não contra o título
  const usedSubjects = new Set(index.map(p => p.subject).filter(Boolean));

  const pool = TOPICS.flatMap(g => g.subjects.map(s => ({ subject: s, category: g.category })))
                     .filter(t => !usedSubjects.has(t.subject));

  console.log(`📚  ${pool.length} assunto(s) inéditos disponíveis de ${TOPICS.reduce((n, g) => n + g.subjects.length, 0)}\n`);

  if (!pool.length) {
    console.error('⚠️  Catálogo de assuntos esgotado. Adicione novos itens em TOPICS.');
    process.exit(1);
  }

  let generated = 0;
  for (let attempt = 0; generated < count && pool.length && attempt < count * 4; attempt++) {
    const idx = Math.floor(Math.random() * pool.length);
    const { subject, category } = pool.splice(idx, 1)[0];

    try {
      const article = await generateArticle(subject, category);
      const dateISO = new Date().toISOString();
      let slug = slugify(article.title) || slugify(subject);
      if (usedSlugs.has(slug)) slug = `${slug}-${dateISO.slice(0, 10)}`;

      console.log('🖼️  Buscando imagem...');
      const image = await fetchUnsplashImage(category, article.title);
      console.log(image ? `   ✅ ${image.author}` : '   ⚠️  sem imagem');

      const dir = path.join(BLOG_DIR, slug);
      fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(path.join(dir, 'post.json'),
        JSON.stringify({ content: article.content, image }, null, 2), 'utf8');

      index.unshift({
        slug, title: article.title, excerpt: article.excerpt, category,
        subject,                       // ← guardado para a deduplicação funcionar
        date: readableDate(dateISO), dateISO,
      });
      usedSlugs.add(slug);
      generated++;
      console.log(`✅  blog/${slug}/post.json`);

      if (generated < count) await new Promise(r => setTimeout(r, 4000));
    } catch (err) {
      console.error(`❌  ${err.message}`);
    }
  }

  fs.writeFileSync(INDEX_FILE, JSON.stringify(index, null, 2), 'utf8');
  console.log(`\n✨  ${generated} artigo(s). Agora rode: python3 _build/build.py`);
  if (!generated) process.exit(1);
}

main().catch(e => { console.error('Erro fatal:', e); process.exit(1); });
