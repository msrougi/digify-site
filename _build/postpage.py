# -*- coding: utf-8 -*-
"""Digify — renderização dos artigos do blog a partir de blog/<slug>/post.json."""
import json, os, re, html, unicodedata
from build import head, header, footer, tail, wa_url, E, SITE
from content import PT

L0 = PT
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")

CAT_COLOR = {"SEO": "jade", "Criação de Sites": "flame", "Desenvolvimento de Apps": "ultra",
             "Marketing Digital": "violet", "E-commerce": "pink", "Sistemas": "cyan"}
CAT_SERVICE = {"SEO": "/servicos/seo/", "Criação de Sites": "/servicos/criacao-de-sites/",
               "Desenvolvimento de Apps": "/servicos/desenvolvimento-de-apps/",
               "Marketing Digital": "/servicos/marketing-digital/",
               "E-commerce": "/servicos/ecommerce/", "Sistemas": "/servicos/sistemas/"}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]

INNER_FT = "".join('<li><a href="%s">%s</a></li>' % (h, E(t)) for h, t in [
    ("/servicos/", "Todos os serviços"), ("/sobre/", "Sobre a Digify"),
    ("/blog/", "Blog"), ("/contato/", "Contato"),
    ("https://plugins.digify.live/", "Plugins WordPress"),
    ("/politica-de-privacidade/", "Política de privacidade")])


def color(cat):
    return CAT_COLOR.get(cat, "flame")


def br_date(iso):
    try:
        y, m, d = iso[:10].split("-")
        return "%d de %s de %s" % (int(d), MESES[int(m) - 1], y)
    except Exception:
        return iso[:10]


def strip_tags(s):
    return re.sub(r"<[^>]+>", " ", s)


def word_count(content):
    return len(strip_tags(content).split())


def read_time(content):
    return max(3, round(word_count(content) / 200))



# ============================================================ ENRIQUECIMENTO DO ARTIGO
# Termos que viram link interno para as páginas de dinheiro. Ordem importa:
# expressões mais longas primeiro, para não casar pedaço de outra.
ILINKS = [
    ("criação de sites",          "/servicos/criacao-de-sites/"),
    ("desenvolvimento de sites",  "/servicos/criacao-de-sites/"),
    ("criar um site profissional","/servicos/criacao-de-sites/"),
    ("landing page",              "/servicos/criacao-de-sites/"),
    ("loja virtual",              "/servicos/ecommerce/"),
    ("e-commerce",                "/servicos/ecommerce/"),
    ("desenvolvimento de aplicativos", "/servicos/desenvolvimento-de-apps/"),
    ("aplicativo mobile",         "/servicos/desenvolvimento-de-apps/"),
    ("tráfego pago",              "/servicos/marketing-digital/"),
    ("Google Ads",                "/servicos/marketing-digital/"),
    ("marketing digital",         "/servicos/marketing-digital/"),
    ("sistema sob medida",        "/servicos/sistemas/"),
    ("integração com ERP",        "/servicos/sistemas/"),
    ("auditoria de SEO",          "/servicos/seo/"),
    ("SEO técnico",               "/servicos/seo/"),
    ("consultoria de SEO",        "/servicos/seo/"),
]
MAX_ILINKS = 4

BANNER_COPY = {
    "SEO": ("Seu concorrente está na frente agora?",
            "A Digify faz auditoria técnica, conteúdo e autoridade para colocar seu site entre os primeiros resultados. Diagnóstico gratuito, sem compromisso."),
    "Criação de Sites": ("Seu site trabalha ou só existe?",
            "Criamos sites que carregam em menos de 2 segundos e são desenhados para transformar visita em orçamento. Landing page no ar em 10 dias úteis."),
    "Desenvolvimento de Apps": ("Da ideia ao app publicado.",
            "MVP funcionando em cerca de 6 semanas, entregas semanais e 100% do código no seu nome. Conte o que você precisa construir."),
    "Marketing Digital": ("Clique não paga conta. Cliente paga.",
            "Estruturamos campanhas com rastreamento configurado antes da primeira verba subir, para você saber quanto custa cada cliente."),
    "E-commerce": ("Quantos carrinhos sua loja perde por mês?",
            "Checkout curto, frete calculado cedo, Pix e integração com marketplace. Fazemos a auditoria da sua loja sem custo."),
    "Sistemas": ("Se alguém digita duas vezes, tem software faltando.",
            "Sistemas sob medida, APIs e automações que eliminam retrabalho. Levantamos o seu processo antes de propor qualquer linha de código."),
}


def slugify_head(text, used):
    s = unicodedata.normalize("NFD", strip_tags(text).lower())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"[^a-z0-9\s-]", "", s).strip()
    s = re.sub(r"\s+", "-", s)[:60] or "secao"
    n, base = 2, s
    while s in used:
        s = "%s-%d" % (base, n); n += 1
    used.add(s)
    return s


def add_heading_ids(content):
    """Dá id a cada <h2> e devolve a lista para montar o índice."""
    used, heads = set(), []

    def repl(m):
        inner = m.group(2)
        hid = slugify_head(inner, used)
        heads.append((hid, strip_tags(inner).strip()))
        return '<h2 id="%s"%s>%s</h2>' % (hid, m.group(1), inner)

    content = re.sub(r"<h2([^>]*)>(.*?)</h2>", repl, content, flags=re.S)
    return content, heads


def build_toc(heads, c):
    if len(heads) < 3:
        return ""
    items = "".join('<li><a href="#%s">%s</a></li>' % (h, html.escape(t)) for h, t in heads)
    return ('<details class="toc" open style="--c:var(--%s)">'
            '<summary>Neste artigo</summary><ol>%s</ol></details>' % (c, items))


def auto_link(content, own_service):
    """Liga a primeira ocorrência de cada termo à página de serviço. Nunca dentro de
    heading, nunca dentro de link que já existe, no máximo MAX_ILINKS por artigo."""
    used, count = set(), 0
    parts = re.split(r"(<[^>]+>)", content)
    in_a = in_head = False
    for i, tok in enumerate(parts):
        if tok.startswith("<"):
            low = tok.lower()
            if low.startswith("<a"): in_a = True
            elif low.startswith("</a"): in_a = False
            elif re.match(r"</?h[1-6]", low): in_head = not low.startswith("</")
            continue
        if in_a or in_head or count >= MAX_ILINKS or not tok.strip():
            continue
        for term, url in ILINKS:
            if count >= MAX_ILINKS or url in used or url == own_service:
                continue
            m = re.search(r"(?<![\w-])(%s)(?![\w-])" % re.escape(term), tok, re.I)
            if m:
                tok = (tok[:m.start()] + '<a class="ilink" href="%s">%s</a>' % (url, m.group(1))
                       + tok[m.end():])
                used.add(url); count += 1
        parts[i] = tok
    return "".join(parts)


def inject_banner(content, category, c, wa):
    """Banner de conversão no meio do artigo, antes de um <h2> do miolo."""
    title, sub = BANNER_COPY.get(category, BANNER_COPY["SEO"])
    svc = CAT_SERVICE.get(category, "/servicos/")
    banner = (
        '<aside class="abanner" style="--c:var(--%s)">'
        '<b>Digify · %s</b>'
        '<h3>%s</h3><p>%s</p>'
        '<div class="abtns">'
        '<a href="/contato/" class="btn btn--go">Solicitar proposta <span class="ar" aria-hidden="true">&rarr;</span></a>'
        '<a href="%s" class="btn btn--wa">Falar no WhatsApp</a>'
        '</div></aside>' % (c, html.escape(category), html.escape(title), html.escape(sub), wa))

    pos = [m.start() for m in re.finditer(r"<h2[ >]", content)]
    if len(pos) < 3:
        return content + banner
    at = pos[max(1, round(len(pos) * 0.45))]
    return content[:at] + banner + content[at:]


def author_box(c):
    return ('<div class="abox" style="--c:var(--%s);--t:var(--%s-t)">'
            '<span class="abox__av" aria-hidden="true">D.</span>'
            '<div><b>Equipe Digify</b><p>Agência web full-stack com mais de 10 anos e '
            '300 projetos entregues em criação de sites, sistemas sob medida e SEO. '
            '<a href="/sobre/">Conheça a Digify</a>.</p></div></div>' % (c, c))


def render_post(p, content, image, related):
    """p = entrada do index.json; content = HTML do corpo; related = até 3 posts."""
    c = color(p["category"])
    slug = p["slug"]
    url = "%s/blog/%s/" % (SITE, slug)
    wa = wa_url(L0)

    # ── enriquecimento: âncoras, índice, links internos e banner ──
    content, heads = add_heading_ids(content)
    content = auto_link(content, CAT_SERVICE.get(p["category"]))
    content = inject_banner(content, p["category"], c, wa)
    toc = build_toc(heads, c)
    iso = p.get("dateISO") or p.get("date")
    label = br_date(iso)
    wc = word_count(content)

    if image and image.get("url"):
        cover = ('<figure class="acover"><img src="%s" alt="%s" width="1200" height="525" '
                 'loading="eager" fetchpriority="high"><figcaption>Foto: '
                 '<a href="%s?utm_source=digify&amp;utm_medium=referral" target="_blank" rel="noopener">%s</a>'
                 ' / Unsplash</figcaption></figure>'
                 % (image["url"], E(image.get("alt") or p["title"]),
                    image.get("authorUrl", "https://unsplash.com"), E(image.get("author", "Unsplash"))))
    else:
        cover = ('<figure class="acover acover--none" aria-hidden="true"><span>%s</span></figure>'
                 % E(p["category"]))

    rel = ""
    if related:
        cards = "".join(
            '<a class="post rv rv-%d" style="--c:var(--%s);--t:var(--%s-t)" href="/blog/%s/">'
            '<span class="post__cat">%s</span><h3>%s</h3><p>%s</p>'
            '<time datetime="%s">%s</time></a>'
            % (n + 1, color(r["category"]), color(r["category"]), r["slug"],
               E(r["category"]), E(r["title"]), E(r["excerpt"]),
               (r.get("dateISO") or "")[:10], E(br_date(r.get("dateISO") or r.get("date", ""))))
            for n, r in enumerate(related))
        rel = ('<section class="section section--mist"><div class="wrap">'
               '<div class="head"><div><p class="eyebrow rv">Continue lendo</p>'
               '<h2 class="rv rv-1">Sobre %s.</h2></div>'
               '<a href="/blog/" class="btn btn--ghost rv rv-1">Ver todos os artigos '
               '<span class="ar" aria-hidden="true">&rarr;</span></a></div>'
               '<div class="arel">%s</div></div></section>' % (E(p["category"].lower()), cards))

    svc = CAT_SERVICE.get(p["category"], "/servicos/")
    cta = ('<div class="acta rv" style="--c:var(--%s);--t:var(--%s-t)">'
           '<h2>Precisa de ajuda com %s?</h2>'
           '<p>A Digify trabalha com isso há mais de 10 anos. Conte o seu caso e receba um '
           'diagnóstico gratuito em até um dia útil.</p>'
           '<a href="/contato/" class="btn">Solicitar proposta '
           '<span class="ar" aria-hidden="true">&rarr;</span></a> '
           '<a href="%s" class="btn btn--ghost" style="margin-left:8px">Ver o serviço</a>'
           '</div>' % (c, c, E(p["category"].lower()), svc))

    graph = [
        {"@type": "BlogPosting", "@id": url + "#article",
         "headline": p["title"][:110], "description": p["excerpt"], "url": url,
         "datePublished": iso, "dateModified": p.get("dateModified", iso),
         "inLanguage": "pt-BR", "articleSection": p["category"], "wordCount": wc,
         "author": {"@type": "Organization", "name": "Digify Marketing Digital",
                    "url": SITE + "/sobre/"},
         "publisher": {"@id": SITE + "/#org"},
         "mainEntityOfPage": {"@id": url + "#webpage"},
         "isPartOf": {"@id": SITE + "/blog/#webpage"}},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": p["title"],
         "description": p["excerpt"], "inLanguage": "pt-BR",
         "isPartOf": {"@id": SITE + "/#site"}},
        {"@type": "BreadcrumbList", "@id": url + "#crumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": p["category"],
             "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 4, "name": p["title"], "item": url}]},
    ]
    if image and image.get("url"):
        graph[0]["image"] = {"@type": "ImageObject", "url": image["url"],
                             "caption": image.get("alt") or p["title"]}
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, indent=2)

    og_img = image["url"] if (image and image.get("url")) else SITE + "/assets/og-digify.png"
    extra = ('<meta property="article:published_time" content="%s">\n'
             '<meta property="article:section" content="%s">\n'
             '<link rel="alternate" type="application/rss+xml" title="Blog Digify" href="/blog/rss.xml">'
             % (iso, E(p["category"])))

    h = head(L0, "%s | Blog Digify" % p["title"], p["excerpt"], url, alt=False, extra=extra)
    h = h.replace('<meta property="og:type" content="website">',
                  '<meta property="og:type" content="article">')
    h = h.replace('content="%s/assets/og-digify.png"' % SITE, 'content="%s"' % og_img)

    body = """<main id="main">
<div class="wrap"><nav class="crumbs" style="--c:var(--%s)" aria-label="Trilha">
  <a href="/">Home</a><span>&rsaquo;</span><a href="/blog/">Blog</a><span>&rsaquo;</span><b>%s</b>
</nav></div>

<article>
<header class="ahero" style="--c:var(--%s)">
  <div class="wrap">
    <div class="ahead">
      <span class="acat" style="--c:var(--%s);--t:var(--%s-t)">%s</span>
      <h1>%s</h1>
      <p class="lede">%s</p>
      <div class="ameta">
        <span>Publicado em <b>%s</b></span>
        <span><b>%d</b> min de leitura</span>
        <span><b>%s</b> palavras</span>
        <span>Por <b>Digify</b></span>
      </div>
    </div>
  </div>
  <div class="wrap">%s</div>
</header>

<div class="section section--tight"><div class="wrap">
  <div class="article rv">%s
  %s</div>
  %s
  %s
</div></div>
</article>

%s
</main>
""" % (c, E(p["category"]), c, c, c, E(p["category"]), E(p["title"]), E(p["excerpt"]),
       label, read_time(content), "{:,}".format(wc).replace(",", "."), cover,
       toc, content, cta, author_box(c), rel)

    return h + header(L0, home_nav=False) + body + footer(L0, INNER_FT) + tail(ld)


def load_index():
    f = os.path.join(BLOG, "index.json")
    return json.load(open(f, encoding="utf-8")) if os.path.exists(f) else []


def build_posts():
    """Renderiza todo post que tenha blog/<slug>/post.json."""
    index = load_index()
    by_cat = {}
    for p in index:
        by_cat.setdefault(p["category"], []).append(p)

    done = 0
    for p in index:
        pj = os.path.join(BLOG, p["slug"], "post.json")
        if not os.path.exists(pj):
            continue
        data = json.load(open(pj, encoding="utf-8"))
        related = [r for r in by_cat.get(p["category"], []) if r["slug"] != p["slug"]][:3]
        html_out = render_post(p, data.get("content", ""), data.get("image"), related)
        open(os.path.join(BLOG, p["slug"], "index.html"), "w", encoding="utf-8").write(html_out)
        done += 1
    return done, len(index)


def rss():
    """Feed RSS — descoberta mais rápida de post novo pelo Google."""
    index = load_index()[:30]
    items = ""
    for p in index:
        iso = p.get("dateISO") or p.get("date")
        items += ("\n  <item>\n    <title>%s</title>\n    <link>%s/blog/%s/</link>\n"
                  "    <guid isPermaLink=\"true\">%s/blog/%s/</guid>\n"
                  "    <description>%s</description>\n    <category>%s</category>\n"
                  "    <pubDate>%s</pubDate>\n  </item>"
                  % (html.escape(p["title"]), SITE, p["slug"], SITE, p["slug"],
                     html.escape(p["excerpt"]), html.escape(p["category"]), iso))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0"><channel>\n'
            '  <title>Blog Digify</title>\n'
            '  <link>%s/blog/</link>\n'
            '  <description>Criação de sites, SEO, apps e marketing digital.</description>\n'
            '  <language>pt-BR</language>%s\n</channel></rss>\n' % (SITE, items))


# ============================================================ HUBS DE CATEGORIA
CAT_SLUG = {"SEO": "seo", "Criação de Sites": "criacao-de-sites",
            "Desenvolvimento de Apps": "desenvolvimento-de-apps",
            "Marketing Digital": "marketing-digital",
            "E-commerce": "ecommerce", "Sistemas": "sistemas"}

CAT_COPY = {
 "SEO": ("SEO na prática, sem promessa mágica.",
   "Auditoria técnica, palavra-chave, autoridade e Core Web Vitals. Tudo o que a gente aplica nos projetos de SEO, explicado do jeito que funciona de verdade — inclusive o que não funciona.",
   "artigos sobre SEO"),
 "Criação de Sites": ("Como se constrói um site que vende.",
   "Performance, estrutura, conversão e as decisões técnicas que separam um site que trabalha de um site que só existe. Escrito por quem entrega site há mais de 10 anos.",
   "artigos sobre criação de sites"),
 "Desenvolvimento de Apps": ("Aplicativo que sobrevive ao primeiro mês.",
   "MVP, escolha de tecnologia, publicação nas lojas e retenção de usuário. O que descobrimos construindo aplicativos para clientes reais, com orçamento real.",
   "artigos sobre desenvolvimento de apps"),
 "Marketing Digital": ("Mídia paga medida por cliente, não por clique.",
   "Google Ads, Meta Ads, rastreamento e funil. Como estruturar campanha que se paga e como reconhecer a métrica que só serve para enfeitar relatório.",
   "artigos sobre marketing digital"),
 "E-commerce": ("Loja virtual: onde o funil vaza.",
   "Checkout, frete, meios de pagamento e integração. O caminho completo do primeiro clique ao pedido pago.",
   "artigos sobre e-commerce"),
 "Sistemas": ("Software que tira trabalho da mão de gente.",
   "Sistemas sob medida, APIs, automação e integração. Quando vale desenvolver e quando é melhor integrar o que já existe.",
   "artigos sobre sistemas"),
}


def cat_nav(active=None):
    idx = load_index()
    cats = sorted({p["category"] for p in idx})
    links = ['<a href="/blog/"%s>Todos</a>' % ('' if active else ' aria-current="page"')]
    for c in cats:
        s = CAT_SLUG.get(c)
        if not s:
            continue
        links.append('<a href="/blog/%s/"%s>%s</a>'
                     % (s, ' aria-current="page"' if active == c else '', html.escape(c)))
    return '<nav class="catnav" aria-label="Categorias do blog">%s</nav>' % "".join(links)


def category_page(cat, posts):
    cslug = CAT_SLUG[cat]
    c = color(cat)
    url = "%s/blog/%s/" % (SITE, cslug)
    h1, intro, kw = CAT_COPY[cat]
    trail = [("/", "Home"), ("/blog/", "Blog"), (None, cat)]

    items = ""
    for n, p in enumerate(posts):
        items += ('<a class="bitem rv rv-%d" href="/blog/%s/" style="--c:var(--%s);--t:var(--%s-t)">'
                  '<div><span class="bitem__cat">%s</span><h3>%s</h3><p>%s</p></div>'
                  '<time datetime="%s">%s</time></a>'
                  % (n % 3 + 1, p["slug"], c, c, html.escape(cat), html.escape(p["title"]),
                     html.escape(p["excerpt"]), (p.get("dateISO") or "")[:10],
                     html.escape(br_date(p.get("dateISO") or ""))))

    svc = CAT_SERVICE.get(cat, "/servicos/")
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url,
         "name": "%s | Blog Digify" % cat, "description": intro, "inLanguage": "pt-BR",
         "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": SITE + "/#org"}},
        {"@type": "BreadcrumbList", "@id": url + "#crumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
            {"@type": "ListItem", "position": 3, "name": cat, "item": url}]},
        {"@type": "ItemList", "@id": url + "#list", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "url": "%s/blog/%s/" % (SITE, p["slug"]),
             "name": p["title"]} for n, p in enumerate(posts)]}],
    }, ensure_ascii=False, indent=2)

    body = """<main id="main">
<div class="wrap"><nav class="crumbs" style="--c:var(--%s)" aria-label="Trilha">
  <a href="/">Home</a><span>&rsaquo;</span><a href="/blog/">Blog</a><span>&rsaquo;</span><b>%s</b>
</nav></div>
<section class="phero" style="--c:var(--%s)">
  <div class="wrap phero__in">
    <p class="eyebrow rv">%s &middot; %d artigos</p>
    <h1 class="rv rv-1">%s</h1>
    <p class="lede rv rv-2">%s</p>
    <div class="phero__cta rv rv-3">
      <a href="%s" class="btn btn--flame">Ver o serviço de %s <span class="ar" aria-hidden="true">&rarr;</span></a>
      <a href="/contato/" class="btn btn--ghost">Solicitar proposta</a>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap">
  %s
  <div class="blist">%s</div>
</div></section>
%s
</main>
""" % (c, html.escape(cat), c, html.escape(cat), len(posts), html.escape(h1),
       html.escape(intro), svc, html.escape(cat.lower()), cat_nav(cat), items, cta_section(c))

    title = "%s | Blog Digify" % cat
    return (head(L0, title, intro[:158], url, alt=False)
            + header(L0, home_nav=False) + body + footer(L0, INNER_FT) + tail(ld))


def cta_section(c):
    return ('<section class="section section--deep"><div class="wrap" style="text-align:center">'
            '<p class="eyebrow rv" style="justify-content:center">Próximo passo</p>'
            '<h2 class="rv rv-1">Vamos começar pelo diagnóstico.</h2>'
            '<p class="lede rv rv-2" style="margin:22px auto 0">Ler é bom, resolver é melhor. '
            'Conte o seu caso e responda em até um dia útil com um diagnóstico do cenário atual.</p>'
            '<div class="hero__cta rv rv-3" style="justify-content:center;margin-top:34px">'
            '<a href="/contato/" class="btn btn--flame">Solicitar proposta '
            '<span class="ar" aria-hidden="true">&rarr;</span></a>'
            '<a href="%s" class="btn btn--outlineDeep">Falar no WhatsApp</a>'
            '</div></div></section>' % wa_url(L0))


def build_categories():
    idx = load_index()
    groups = {}
    for p in idx:
        groups.setdefault(p["category"], []).append(p)
    urls = []
    for cat, posts in groups.items():
        if cat not in CAT_SLUG or not posts:
            continue
        posts.sort(key=lambda x: x.get("dateISO", ""), reverse=True)
        d = os.path.join(BLOG, CAT_SLUG[cat])
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(category_page(cat, posts))
        urls.append("blog/%s/" % CAT_SLUG[cat])
    return urls
