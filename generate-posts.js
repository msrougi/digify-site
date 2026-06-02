#!/usr/bin/env node
/**
 * DIGIFY BLOG AUTO-GENERATOR — Gemini 2.5 Flash (100% gratuito)
 * USO:
 *   node generate-posts.js            # gera 1 artigo
 *   node generate-posts.js --count 3  # gera 3 artigos
 *
 * CONFIGURAÇÃO:
 *   export GEMINI_API_KEY="AQ..."
 */

const fs   = require('fs');
const path = require('path');

const BLOG_DIR   = path.join(__dirname, 'blog');
const INDEX_FILE = path.join(BLOG_DIR, 'index.json');
const TEMPLATE   = fs.readFileSync(path.join(BLOG_DIR, 'post-template.html'), 'utf8');
const API_KEY    = process.env.GEMINI_API_KEY;
const API_URL    = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`;

if (!API_KEY) {
  console.error('❌  Defina GEMINI_API_KEY antes de rodar.');
  process.exit(1);
}

const TOPICS = [
  {
    category: 'SEO',
    subjects: [
      'Como criar um site que rankeia no Google em 2025',
      'SEO local: como aparecer no Google Maps da sua cidade',
      'Core Web Vitals: o que são e como melhorar a nota do seu site',
      'Link building white hat: estratégias seguras para ganhar autoridade',
      'Como fazer uma auditoria de SEO completa no seu site',
      'SEO para e-commerce: guia completo para lojas virtuais',
      'Palavras-chave de cauda longa: como encontrar e usar',
      'SEO on-page: o checklist completo para otimizar cada página',
      'Como aparecer na posição zero do Google (featured snippets)',
      'Velocidade do site e SEO: por que cada segundo importa',
      'O que é E-E-A-T e como aplicar no seu site',
      'Como usar o Google Search Console do zero',
    ]
  },
  {
    category: 'Criação de Sites',
    subjects: [
      'Quanto custa criar um site profissional em 2025?',
      'WordPress vs site em HTML: qual escolher para seu negócio?',
      'Landing page que converte: 10 elementos indispensáveis',
      'Como escolher a agência certa para criar o site da sua empresa',
      'Site responsivo: por que mobile-first é obrigatório hoje',
      'Como criar um site rápido: guia técnico para iniciantes',
      'UX design para sites: princípios que aumentam conversão',
      'Copywriting para sites: como escrever textos que vendem',
      'Hospedagem de sites: como escolher a melhor opção',
      'O que é um site institucional e quando sua empresa precisa de um',
    ]
  },
  {
    category: 'Desenvolvimento de Apps',
    subjects: [
      'MVP de aplicativo: como validar sua ideia antes de investir',
      'React Native vs Flutter: qual usar para seu app em 2025?',
      'Quanto custa desenvolver um aplicativo do zero?',
      'UX para aplicativos: os 7 princípios que retêm usuários',
      'Como monetizar um aplicativo: modelos que funcionam',
      'Aplicativo nativo vs PWA: quando escolher cada um',
      'Como preparar o briefing do seu app para uma agência',
      'App Store Optimization: como rankear na App Store',
      'Segurança em apps móveis: o que toda empresa precisa saber',
      'Como integrar APIs no seu aplicativo mobile',
    ]
  },
  {
    category: 'Marketing Digital',
    subjects: [
      'Google Ads vs Meta Ads: onde investir em 2025',
      'Como criar uma estratégia de conteúdo que gera leads',
      'Taxa de conversão: como calcular e melhorar a sua',
      'E-mail marketing ainda funciona? Dados e estratégias atuais',
      'Como usar o Google Analytics 4 para tomar decisões',
      'Funil de vendas digital: da atração ao fechamento',
      'Como medir ROI de campanhas digitais com precisão',
      'O que é tráfego pago e como começar do zero',
      'Remarketing: como recuperar visitantes que não converteram',
      'Como criar anúncios no Google Ads que realmente convertem',
    ]
  },
];

function slugify(str) {
  return str.toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9\s-]/g, '').trim()
    .replace(/\s+/g, '-').substring(0, 80);
}

function readableDate(iso) {
  return new Date(iso).toLocaleDateString('pt-BR', {
    day: '2-digit', month: 'long', year: 'numeric'
  });
}

function estimateReadTime(text) {
  return Math.max(3, Math.round(text.split(/\s+/).length / 200));
}

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function loadIndex() {
  if (!fs.existsSync(INDEX_FILE)) return [];
  try { return JSON.parse(fs.readFileSync(INDEX_FILE, 'utf8')); }
  catch { return []; }
}

function saveIndex(posts) {
  fs.writeFileSync(INDEX_FILE, JSON.stringify(posts, null, 2), 'utf8');
}

// ── Injeta os 3 posts mais recentes direto no index.html ─────────────────────
function injectPostsIntoHome(posts) {
  const homeFile = path.join(__dirname, 'index.html');
  if (!fs.existsSync(homeFile)) return;

  const emojis = {
    'SEO': '🔍',
    'Criação de Sites': '🖥️',
    'Desenvolvimento de Apps': '📱',
    'Marketing Digital': '📣',
    'E-commerce': '🛒',
    'Sistemas': '⚙️',
  };

  const recent = posts.slice(0, 3);
  const cards = recent.map(p => `      <div class="blog-card reveal">
        <div class="blog-thumb-placeholder">${emojis[p.category] || '📝'}</div>
        <div class="blog-card-body">
          <span class="blog-cat">${p.category}</span>
          <h3>${p.title}</h3>
          <p>${p.excerpt}</p>
          <div class="blog-meta-row">
            <span>${p.date}</span>
            <a href="/blog/${p.slug}/" class="blog-arrow">Ler →</a>
          </div>
        </div>
      </div>`).join('\n');

  let home = fs.readFileSync(homeFile, 'utf8');
  const start = '<!-- BLOG_POSTS_START -->';
  const end   = '<!-- BLOG_POSTS_END -->';
  const before = home.indexOf(start);
  const after  = home.indexOf(end);

  if (before === -1 || after === -1) {
    console.log('⚠️  Marcadores BLOG_POSTS não encontrados no index.html');
    return;
  }

  home = home.substring(0, before) +
    start + '\n' +
    '    <div class="blog-grid">\n' +
    cards + '\n' +
    '    </div>\n    ' +
    end +
    home.substring(after + end.length);

  fs.writeFileSync(homeFile, home, 'utf8');
  console.log('🏠  Home atualizada com os 3 posts mais recentes.');
}

// Chama a API Gemini com um prompt simples e retorna o texto puro
async function callGemini(prompt) {
  const body = {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: 0.7,
      maxOutputTokens: 8192,
    },
  };

  const resp = await fetch(API_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!resp.ok) {
    const err = await resp.text();
    throw new Error(`Gemini API error ${resp.status}: ${err}`);
  }

  const data = await resp.json();

  if (!data.candidates?.[0]?.content?.parts?.[0]?.text) {
    throw new Error('Resposta inesperada: ' + JSON.stringify(data).substring(0, 200));
  }

  return data.candidates[0].content.parts[0].text.trim();
}

// Gera cada campo separadamente para evitar JSON truncado
async function generateArticle(topic, category) {
  console.log(`\n🤖  Gerando: "${topic}" (${category})`);

  const context = `Você é especialista em marketing digital, SEO e tecnologia web com mais de 10 anos de experiência. Escreve conteúdo para o blog da Digify, agência web brasileira especializada em criação de sites, desenvolvimento de apps e SEO. Use português brasileiro natural, tom profissional mas acessível.`;

  // Passo 1: título e excerpt
  const metaRaw = await callGemini(
    `${context}\n\nPara o tema "${topic}" (categoria: ${category}), responda APENAS com duas linhas, sem explicação:\nLINHA1: [título SEO com até 60 caracteres]\nLINHA2: [meta description de 150-160 caracteres com a palavra-chave principal]`
  );

  const metaLines = metaRaw.split('\n').map(l => l.replace(/^LINHA\d:\s*/i, '').replace(/^\[|\]$/g, '').trim()).filter(Boolean);
  const title   = metaLines[0] || topic;
  const excerpt = metaLines[1] || `Aprenda tudo sobre ${topic} neste guia completo da Digify.`;

  console.log(`   📝 Título: ${title}`);

  // Pausa entre chamadas
  await new Promise(r => setTimeout(r, 2000));

  // Passo 2: conteúdo HTML completo
  const content = await callGemini(
    `${context}\n\nEscreva um artigo completo em HTML sobre: "${title}"\nCategoria: ${category}\n\nREGRAS:\n- Retorne APENAS o HTML do corpo do artigo (sem <!DOCTYPE>, sem <html>, sem <head>, sem <body>)\n- Use h2, h3, p, ul, ol, strong\n- NÃO inclua h1\n- Mínimo 1200 palavras\n- Pelo menos 5 seções com h2\n- Inclua introdução, desenvolvimento detalhado e conclusão\n- No final, mencione sutilmente que a Digify pode ajudar com ${category.toLowerCase()}`
  );

  return { title, excerpt, content };
}

function savePost(article, category, slug, dateISO) {
  const postDir = path.join(BLOG_DIR, slug);
  fs.mkdirSync(postDir, { recursive: true });

  const html = TEMPLATE
    .replace(/\{\{POST_TITLE\}\}/g,     article.title)
    .replace(/\{\{POST_EXCERPT\}\}/g,   article.excerpt)
    .replace(/\{\{POST_CATEGORY\}\}/g,  category)
    .replace(/\{\{POST_SLUG\}\}/g,      slug)
    .replace(/\{\{POST_DATE_ISO\}\}/g,  dateISO)
    .replace(/\{\{POST_DATE\}\}/g,      readableDate(dateISO))
    .replace(/\{\{POST_READ_TIME\}\}/g, estimateReadTime(article.content))
    .replace(/\{\{POST_CONTENT\}\}/g,   article.content);

  fs.writeFileSync(path.join(postDir, 'index.html'), html, 'utf8');
  console.log(`✅  Salvo: /blog/${slug}/index.html`);
}

async function main() {
  const args  = process.argv.slice(2);
  const count = parseInt(args[args.indexOf('--count') + 1] || '1', 10) || 1;

  console.log(`\n🚀  Digify Blog Generator (Gemini 2.5 Flash) — ${count} artigo(s)`);
  console.log(`📅  ${new Date().toLocaleDateString('pt-BR')}\n`);

  const index = loadIndex();
  const existingSlugs = new Set(index.map(p => p.slug));

  let generated = 0;
  const maxAttempts = count * 5;
  let attempts = 0;

  while (generated < count && attempts < maxAttempts) {
    attempts++;

    const topicGroup = pickRandom(TOPICS);
    const subject    = pickRandom(topicGroup.subjects);
    const slug       = slugify(subject);

    if (existingSlugs.has(slug)) {
      console.log(`⏭️  Pulando (já existe): ${slug}`);
      continue;
    }

    try {
      const article = await generateArticle(subject, topicGroup.category);
      const dateISO = new Date().toISOString();
      const finalSlug = slugify(article.title) || slug;

      savePost(article, topicGroup.category, finalSlug, dateISO);

      index.unshift({
        slug:     finalSlug,
        title:    article.title,
        excerpt:  article.excerpt,
        category: topicGroup.category,
        date:     readableDate(dateISO),
        dateISO,
      });

      existingSlugs.add(finalSlug);
      generated++;

      if (generated < count) {
        console.log('⏳  Aguardando 4s...');
        await new Promise(r => setTimeout(r, 4000));
      }

    } catch (err) {
      console.error(`❌  Erro: ${err.message}`);
    }
  }

  saveIndex(index);
  injectPostsIntoHome(index);
  console.log(`\n✨  Pronto! ${generated} artigo(s) gerado(s).`);

  if (generated === 0) {
    console.error('⚠️  Nenhum artigo gerado.');
    process.exit(1);
  }
}

main().catch(err => { console.error('Erro fatal:', err); process.exit(1); });
