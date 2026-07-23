# -*- coding: utf-8 -*-
"""
Digify — gerador estático dos três idiomas.
Uso:  python3 _build/build.py
Gera: index.html, en/index.html, es/index.html, sitemap.xml, robots.txt, _headers
"""
import json, os, sys, html
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import LANGS, PT, SITE, PHONE, PHONE_LABEL, LOGOS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = html.escape


def url_of(L):
    return SITE + "/" + L["dir"]


# ---------------------------------------------------------------- hreflang
def hreflang(L):
    out = []
    for O in LANGS:
        out.append(f'<link rel="alternate" hreflang="{O["code"]}" href="{url_of(O)}">')
    out.append(f'<link rel="alternate" hreflang="x-default" href="{SITE}/">')
    return "\n".join(out)


def og_alt(L):
    return "\n".join(f'<meta property="og:locale:alternate" content="{O["og"]}">'
                     for O in LANGS if O["code"] != L["code"])


# ---------------------------------------------------------------- schema
def schema(L):
    page = url_of(L)
    graph = [
        {"@type": "ProfessionalService",
         "@id": f"{SITE}/#org",
         "name": "Digify",
         "url": SITE + "/",
         "description": L["desc"],
         "telephone": PHONE,
         "priceRange": "$$",
         "areaServed": {"@type": "Place", "name": L["area"]},
         "address": {"@type": "PostalAddress", "addressRegion": "SP", "addressCountry": "BR"},
         "availableLanguage": [
             {"@type": "Language", "name": "Portuguese", "alternateName": "pt-BR"},
             {"@type": "Language", "name": "English", "alternateName": "en"},
             {"@type": "Language", "name": "Spanish", "alternateName": "es"}],
         "logo": {"@type": "ImageObject", "@id": SITE + "/#logo",
                  "url": SITE + "/assets/logo-digify.png", "width": 512, "height": 512,
                  "caption": "Digify"},
         "image": {"@id": SITE + "/#logo"},
         "contactPoint": [{"@type": "ContactPoint", "telephone": PHONE,
                           "contactType": "sales",
                           "availableLanguage": ["Portuguese", "English", "Spanish"],
                           "areaServed": ["BR", "US", "PT", "ES"]}],
         "knowsLanguage": ["pt-BR", "en", "es"],
         "foundingDate": "2015",
         "slogan": "O primeiro resultado leva quase tudo.",
         "sameAs": ["https://instagram.com/digify.live", "https://plugins.digify.live/"],
         "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5",
                             "reviewCount": str(len(L["quotes"])), "bestRating": "5"},
         "hasOfferCatalog": {
             "@type": "OfferCatalog", "name": L["svc_eyebrow"],
             "itemListElement": [
                 {"@type": "Offer", "itemOffered": {"@type": "Service", "name": name,
                                                    "description": desc,
                                                    "provider": {"@id": f"{SITE}/#org"}}}
                 for _c, _tag, name, _href, desc in L["svcs"]]}},

        {"@type": "WebSite", "@id": f"{SITE}/#site", "url": SITE + "/",
         "name": "Digify", "publisher": {"@id": f"{SITE}/#org"},
         "inLanguage": [O["code"] for O in LANGS]},

        {"@type": "WebPage", "@id": f"{page}#webpage", "url": page,
         "name": L["title"], "description": L["desc"], "inLanguage": L["code"],
         "isPartOf": {"@id": f"{SITE}/#site"}, "about": {"@id": f"{SITE}/#org"},
         "primaryImageOfPage": {"@id": f"{SITE}/#logo"}},

        {"@type": "FAQPage", "@id": f"{page}#faq", "inLanguage": L["code"],
         "isPartOf": {"@id": f"{page}#webpage"},
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}}
                        for q, a in L["faq"]]},

        {"@type": "ItemList", "@id": f"{page}#reviews",
         "itemListElement": [
             {"@type": "ListItem", "position": i + 1,
              "item": {"@type": "Review", "reviewBody": body,
                       "author": {"@type": "Person", "name": who},
                       "reviewRating": {"@type": "Rating", "ratingValue": "5", "bestRating": "5"},
                       "itemReviewed": {"@id": f"{SITE}/#org"}}}
             for i, (_c, body, _av, who, _role) in enumerate(L["quotes"])]},
    ]
    if L["dir"]:
        graph.append({"@type": "BreadcrumbList", "@id": f"{page}#crumbs",
                      "itemListElement": [
                          {"@type": "ListItem", "position": 1, "name": "Digify", "item": SITE + "/"},
                          {"@type": "ListItem", "position": 2,
                           "name": {"en": "English", "es": "Español"}.get(L["code"], L["short"]),
                           "item": page}]})
    return json.dumps({"@context": "https://schema.org", "@graph": graph},
                      ensure_ascii=False, indent=2)


# ---------------------------------------------------------------- partials
def lang_picker(L, cls=""):
    links = "".join(
        f'<a href="{SITE_PATH(O)}" hreflang="{O["code"]}" lang="{O["code"]}"'
        + (' aria-current="true"' if O["code"] == L["code"] else "")
        + f'>{O["short"]}</a>'
        for O in LANGS)
    return f'<div class="lang{cls}" role="group" aria-label="{E(L["lang_label"])}">{links}</div>'


def SITE_PATH(O):
    return "/" + O["dir"]


def panel(S):
    if S["panel"] == "rank":
        rows = "".join(
            f'<div class="rank__row" data-start="{a}" data-final="{b}"><i></i>'
            f'<div class="rank__bars"><b style="width:{w1}"></b><b style="width:{w2}"></b></div></div>'
            for a, b, w1, w2 in [(0, 1, "74%", "100%"), (1, 2, "61%", "44%"),
                                 (2, 3, "80%", "50%"), (3, 4, "56%", "38%")])
        return f'''<div class="rank" id="rank" aria-hidden="true">
            <div class="rank__top"><div class="rank__dots"><i></i><i></i><i></i></div>
              <span class="rank__q">{E(S["p_query"])}</span></div>
            <div class="rank__body">
              <div class="rank__labels"><span>01</span><span>02</span><span>03</span><span>04</span><span>05</span></div>
              <div class="rank__rows">{rows}
                <div class="rank__row rank__row--you" data-start="4" data-final="0"><i></i>
                  <span class="rank__you">{E(S["p_you"])}</span>
                  <span class="rank__tag">{E(S["p_tag"])}</span></div>
              </div>
            </div>
            <p class="rank__cap">{E(S["p_cap"])}</p>
          </div>'''
    if S["panel"] == "build":
        mods = "".join(f'<span style="--d:{.30 + i * .18:.2f}s">{E(m)}</span>'
                       for i, m in enumerate(S["p_mods"]))
        return f'''<div class="build" aria-hidden="true">
            <div class="build__top"><i></i> {E(S["p_top"])}</div>
            <p class="build__idea">{S["p_idea"]}</p>
            <div class="build__mods">{mods}</div>
            <div class="build__bar"><i></i></div>
            <p class="build__cap">{E(S["p_cap"])}</p>
          </div>'''
    return f'''<div class="site" aria-hidden="true">
        <div class="site__bar"><i></i><i></i><i></i><span class="site__url">{E(S["p_url"])}</span></div>
        <div class="site__page">
          <div class="site__nav" style="--d:.30s"><b></b><u></u><u></u><u></u></div>
          <div class="site__band" style="--d:.48s"><s></s><s></s><em></em><b></b></div>
          <div class="site__cards" style="--d:.66s"><div></div><div></div><div></div></div>
        </div>
        <div class="site__foot"><div class="site__sw"><i></i><i></i><i></i><i></i></div>
          <span class="site__cap">{E(S["p_cap"])}</span></div>
      </div>'''


def slides(L):
    out = []
    for i, S in enumerate(L["slides"]):
        live = " is-live" if i == 0 else ""
        facts = "".join(f'<div class="fact"><b>{E(a)}</b><span>{E(b)}</span></div>' for a, b in S["facts"])
        out.append(f'''
    <article class="hslide{live}" style="--c:var(--{S["c"]});--c2:var(--{S["c2"]});--t:var(--{S["c"]}-t)"
             aria-hidden="{"false" if i == 0 else "true"}" aria-roledescription="slide"
             aria-label="{i + 1}/{len(L["slides"])}">
      <span class="hslide__aura" aria-hidden="true"></span>
      <div class="hero__grid">
        <div class="hcol">
          <p class="eyebrow">{E(S["eyebrow"])}</p>
          <{S["tag"]}>{S["h"]}</{S["tag"]}>
          <p class="lede">{E(S["lede"])}</p>
          <div class="hero__cta">
            <a href="#proposta" class="btn btn--flame">{E(S["cta1"])} <span class="ar" aria-hidden="true">&rarr;</span></a>
            <a href="{S["cta2_href"]}" class="btn btn--ghost">{E(S["cta2"])}</a>
          </div>
          <div class="hero__facts">{facts}</div>
        </div>
        <div class="hero__panel">{panel(S)}</div>
      </div>
    </article>''')
    return "".join(out)



def load_posts():
    """Lê blog/index.json — o índice que o generate-posts.js escreve."""
    MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
             "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    CAT_COLOR = {"SEO": "jade", "Criação de Sites": "flame", "Desenvolvimento de Apps": "ultra",
                 "Marketing Digital": "violet", "E-commerce": "pink", "Sistemas": "cyan"}
    f = os.path.join(ROOT, "blog", "index.json")
    if not os.path.exists(f):
        return [{"cat": c, "title": t, "desc": d, "date": dt, "label": dl,
                 "url": u, "color": col} for col, c, t, d, dt, dl, u in PT["posts"]]
    out = []
    for p in json.load(open(f, encoding="utf-8")):
        iso = (p.get("dateISO") or p.get("date") or "")[:10]
        try:
            y, m, d = iso.split("-")
            label = "%d de %s de %s" % (int(d), MESES[int(m) - 1], y)
        except Exception:
            label = p.get("date", iso)
        out.append({"cat": p.get("category", ""), "title": p.get("title", ""),
                    "desc": p.get("excerpt", ""), "date": iso, "label": label,
                    "url": "/blog/%s/" % p["slug"].strip("/"),
                    "color": CAT_COLOR.get(p.get("category"), "flame")})
    out.sort(key=lambda x: x["date"], reverse=True)
    return out



def wa_url(L):
    return f"https://wa.me/{PHONE.lstrip('+')}?text={L['wa_text']}"


def head(L, title, desc, url, alt=True, extra=""):
    """<head> compartilhado. alt=False para páginas sem equivalente traduzido."""
    hl = hreflang(L) + "\n" + og_alt(L) if alt else ""
    return f'''<!DOCTYPE html>
<html lang="{L["code"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#FFFFFF" id="tc">
{hl}
<meta property="og:type" content="website">
<meta property="og:locale" content="{L["og"]}">
<meta property="og:site_name" content="Digify">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:image" content="{SITE}/assets/og-digify.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}">
<meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE}/assets/og-digify.png">
{extra}
<script>
(function(){{
  var t; try{{ t = localStorage.getItem('digify-theme'); }}catch(e){{}}
  if(!t) t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', t);
}})();
</script>
<link rel="preload" href="/assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/digify.css">
</head>
'''


def header(L, home_nav=True):
    p = "/" + L["dir"]
    items = L["nav"] if home_nav else [("/servicos/", "Serviços"), ("/portfolio/", "Portfólio"),
                                       ("/blog/", "Blog"), ("/contato/", "Contato")]
    nav = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in items)
    return f'''<body>
<a href="#main" class="skip">{E(L["skip"])}</a>
<header class="hdr" id="hdr">
  <div class="wrap hdr__in">
    <a href="{p}" class="logo" aria-label="Digify">digify<i>.</i></a>
    <nav class="nav">{nav}</nav>
    {lang_picker(L)}
    <button class="sw" id="sw" role="switch" aria-checked="true" aria-label="{E(L["sw_label"])}" title="{E(L["sw_title"])}">
      <span class="sw__screw sw__screw--l"></span><span class="sw__screw sw__screw--r"></span>
      <span class="sw__rock"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.5 18.5h5M10.5 21.5h3M12 2.5a6.2 6.2 0 0 0-3.6 11.2c.5.4.9 1 .9 1.7v.6h5.4v-.6c0-.7.4-1.3.9-1.7A6.2 6.2 0 0 0 12 2.5Z"/></svg></span>
    </button>
    <a href="{"#proposta" if home_nav else "/contato/"}" class="btn btn--primary">{E(L["cta_nav"])}</a>
    <button class="burger" id="burger" aria-label="{E(L["menu_open"])}" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
  </div>
  <div class="mnav" id="mnav">
    {nav}
    <a href="{"#proposta" if home_nav else "/contato/"}" class="btn btn--primary">{E(L["cta_nav"])}</a>
    {lang_picker(L)}
  </div>
</header>
'''


def footer(L, ftcomp=None):
    wa = wa_url(L)
    ftsvc = "".join(f'<li><a href="{href}">{E(name)}</a></li>'
                    for _c, _t, name, href, _d in L["svcs"])
    if ftcomp is None:
        ftcomp = "".join(f'<li><a href="{h}">{E(t)}</a></li>' for h, t in L["ft_links"])
    return f'''<footer class="ft">
  <div class="wrap">
    <div class="ft__grid">
      <div class="ft__about">
        <a href="/{L["dir"]}" class="logo">digify<i>.</i></a>
        <p>{E(L["ft_about"])}</p>
      </div>
      <div><h4>{E(L["ft_svc"])}</h4><ul>{ftsvc}</ul></div>
      <div><h4>{E(L["ft_comp"])}</h4><ul>{ftcomp}</ul></div>
      <div><h4>{E(L["ft_contact"])}</h4><ul>
        <li><a href="{wa}">{PHONE_LABEL}</a></li>
        <li><a href="https://instagram.com/digify.live">@digify.live</a></li>
        <li><a href="/contato/">{E(L["cta_nav"])}</a></li>
      </ul></div>
    </div>
    <div class="ft__base">
      <span>{E(L["ft_rights"])}</span>
      <span><a href="/politica-de-privacidade/">{E(L["ft_priv"])}</a> &middot; <a href="/sitemap.xml">{E(L["ft_map"])}</a></span>
    </div>
  </div>
</footer>

<a class="wa" href="{wa}" aria-label="{E(L["wa_label"])}">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.2-.6.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5 0-.2 0-.4 0-.5 0-.2-.6-1.6-.9-2.1-.2-.5-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s1 2.6 1.1 2.8c.1.2 1.9 2.9 4.6 4 .6.3 1.1.4 1.5.6.6.2 1.2.2 1.6.1.5-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.2-.6-.4zM12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.1.8.8-3-.2-.3c-.9-1.4-1.3-3-1.3-4.6C3.5 7.3 7.3 3.5 12 3.5S20.5 7.3 20.5 12 16.7 20.2 12 20.2z"/></svg>
</a>
'''


def tail(ld):
    return f'''<script type="application/ld+json">
{ld}
</script>
<script src="/assets/digify.js" defer></script>
</body>
</html>
'''


def build(L):
    p = "/" + L["dir"]
    nav = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in L["nav"])
    mnav = "".join(f'<a href="{h}">{E(t)}</a>' for h, t in L["nav"])
    tabs = "".join(
        f'<button class="htab{" is-live" if i == 0 else ""}" role="tab" '
        f'aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" '
        f'data-i="{i}" style="--c:var(--{L["slides"][i]["c"]})">'
        f'<b>{E(a)}</b><span>{E(b)}</span><i></i></button>'
        for i, (a, b) in enumerate(L["tabs"]))
    logos = "".join(f"<span>{E(x)}</span>" for x in LOGOS)
    nums = "".join(
        f'<div class="num rv rv-{i + 1}" style="--c:var(--{c});--t:var(--{c}-t)">'
        f'<b>{E(big)}</b><strong>{E(t)}</strong><span>{E(d)}</span></div>'
        for i, (c, big, t, d) in enumerate(L["nums"]))
    svcs = "".join(
        f'<a class="svc rv rv-{i % 3 + 1}" href="{href}" style="--c:var(--{c});--t:var(--{c}-t)">'
        f'<span class="svc__tag">{E(tag)}</span><h3>{E(name)}</h3><p>{E(d)}</p>'
        f'<span class="svc__go">{E(L["svc_go"])} <span class="ar" aria-hidden="true">&rarr;</span></span></a>'
        for i, (c, tag, name, href, d) in enumerate(L["svcs"]))
    stepcols = ["var(--flame)", "#5B72FF", "#A57BFF", "#25C08A"]
    steps = "".join(
        f'<div class="step rv rv-{i + 1}" style="--c:{stepcols[i]}"><b>0{i + 1}</b>'
        f'<h3>{E(t)}</h3><p>{E(d)}</p></div>'
        for i, (t, d) in enumerate(L["steps"]))
    quotes = "".join(
        f'<blockquote class="quote rv rv-{i % 2 + 1}" style="--c:var(--{c});--t:var(--{c}-t)">'
        f'<div class="quote__stars" aria-label="{E(L["quo_stars"])}">&#9733;&#9733;&#9733;&#9733;&#9733;</div>'
        f'<p>{E(body)}</p><footer><span class="quote__av">{E(av)}</span>'
        f'<span class="quote__who"><b>{E(who)}</b><span>{E(role)}</span></span></footer></blockquote>'
        for i, (c, body, av, who, role) in enumerate(L["quotes"]))
    faq = "".join(
        f'<details><summary>{E(q)}</summary><div class="ans">{E(a)}</div></details>'
        for q, a in L["faq"])
    ctasteps = "".join(
        f'<div class="cta__item" style="--c:{["var(--flame)", "#5B72FF", "#25C08A"][i]}">'
        f'<b>0{i + 1}</b><span>{E(t)}</span></div>'
        for i, t in enumerate(L["cta_steps"]))
    needs = "".join(f"<option>{E(o)}</option>" for o in L["f_needs"])
    budgets = "".join(f"<option>{E(o)}</option>" for o in L["f_budgets"])
    ftsvc = "".join(f'<li><a href="{href}">{E(name)}</a></li>'
                    for _c, _t, name, href, _d in L["svcs"])
    ftcomp = "".join(f'<li><a href="{h}">{E(t)}</a></li>' for h, t in L["ft_links"])
    wa = f"https://wa.me/{PHONE.lstrip('+')}?text={L['wa_text']}"

    portfolio_block = ""
    if L.get("blog"):   # só na versão PT, onde os cases estão escritos
        import portfolio as _pf
        portfolio_block = _pf.home_cases()

    blog = ""
    if L.get("blog"):
        posts = "".join(
            f'<a class="post rv rv-{i + 1}" style="--c:var(--{p["color"]});--t:var(--{p["color"]}-t)" href="{p["url"]}">'
            f'<span class="post__cat">{E(p["cat"])}</span><h3>{E(p["title"])}</h3><p>{E(p["desc"])}</p>'
            f'<time datetime="{p["date"]}">{E(p["label"])}</time></a>'
            for i, p in enumerate(load_posts()[:3]))
        blog = f'''
<section class="section section--mist">
  <div class="wrap">
    <div class="head">
      <div><p class="eyebrow rv">{E(L["blog_eyebrow"])}</p><h2 class="rv rv-1">{E(L["blog_h"])}</h2></div>
      <a href="/blog/" class="btn btn--ghost rv rv-1">{E(L["blog_cta"])} <span class="ar" aria-hidden="true">&rarr;</span></a>
    </div>
    <div class="posts">{posts}</div>
  </div>
</section>
'''

    return f'''<!DOCTYPE html>
<html lang="{L["code"]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(L["title"])}</title>
<meta name="description" content="{E(L["desc"])}">
<link rel="canonical" href="{url_of(L)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#FFFFFF" id="tc">

{hreflang(L)}

<meta property="og:type" content="website">
<meta property="og:locale" content="{L["og"]}">
{og_alt(L)}
<meta property="og:site_name" content="Digify">
<meta property="og:url" content="{url_of(L)}">
<meta property="og:title" content="{E(L["title"])}">
<meta property="og:description" content="{E(L["desc"])}">
<meta property="og:image" content="{SITE}/assets/og-digify.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Digify — sites, sistemas e SEO">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(L["title"])}">
<meta name="twitter:description" content="{E(L["desc"])}">
<meta name="twitter:image" content="{SITE}/assets/og-digify.png">

<script>
(function(){{
  var t; try{{ t = localStorage.getItem('digify-theme'); }}catch(e){{}}
  if(!t) t = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', t);
}})();
</script>

<link rel="preload" href="/assets/fonts/bricolage.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/inter.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/digify.css">
</head>

<body>
<a href="#main" class="skip">{E(L["skip"])}</a>

<header class="hdr" id="hdr">
  <div class="wrap hdr__in">
    <a href="{p}" class="logo" aria-label="Digify">digify<i>.</i></a>
    <nav class="nav">{nav}</nav>
    {lang_picker(L)}
    <button class="sw" id="sw" role="switch" aria-checked="true" aria-label="{E(L["sw_label"])}" title="{E(L["sw_title"])}">
      <span class="sw__screw sw__screw--l"></span>
      <span class="sw__screw sw__screw--r"></span>
      <span class="sw__rock"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.1" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9.5 18.5h5M10.5 21.5h3M12 2.5a6.2 6.2 0 0 0-3.6 11.2c.5.4.9 1 .9 1.7v.6h5.4v-.6c0-.7.4-1.3.9-1.7A6.2 6.2 0 0 0 12 2.5Z"/></svg></span>
    </button>
    <a href="#proposta" class="btn btn--primary">{E(L["cta_nav"])}</a>
    <button class="burger" id="burger" aria-label="{E(L["menu_open"])}" aria-expanded="false" aria-controls="mnav"><span></span><span></span><span></span></button>
  </div>
  <div class="mnav" id="mnav">
    {mnav}
    <a href="#proposta" class="btn btn--primary">{E(L["cta_nav"])}</a>
    {lang_picker(L)}
  </div>
</header>

<main id="main">

<section class="hero" id="hero">
  <div class="wrap">
  <div class="hero__slides">{slides(L)}
  </div>
  <div class="htabs" role="tablist" aria-label="{E(L["tablist"])}">{tabs}</div>
  </div>
</section>

<section class="marq" aria-label="{E(L["logos_label"])}">
  <div class="marq__track">{logos}{logos}</div>
</section>

<section class="section section--tight">
  <div class="wrap">
    <p class="eyebrow rv">{E(L["nums_eyebrow"])}</p>
    <h2 class="rv rv-1">{E(L["nums_h"])}</h2>
    <div class="nums">{nums}</div>
  </div>
</section>

<section class="section" id="servicos">
  <div class="wrap">
    <div class="head">
      <div>
        <p class="eyebrow rv">{E(L["svc_eyebrow"])}</p>
        <h2 class="rv rv-1">{E(L["svc_h"])}</h2>
        <p class="lede rv rv-2">{E(L["svc_lede"])}</p>
      </div>
      <a href="#proposta" class="btn btn--ghost rv rv-2">{E(L["svc_cta"])}</a>
    </div>
    <div class="svcs">{svcs}</div>
  </div>
</section>

{portfolio_block}
<section class="section section--deep" id="processo">
  <div class="wrap">
    <p class="eyebrow rv">{E(L["proc_eyebrow"])}</p>
    <h2 class="rv rv-1">{E(L["proc_h"])}</h2>
    <div class="steps">{steps}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="head"><div>
      <p class="eyebrow rv">{E(L["quo_eyebrow"])}</p>
      <h2 class="rv rv-1">{E(L["quo_h"])}</h2>
    </div></div>
    <div class="quotes">{quotes}</div>
  </div>
</section>
{blog}
<section class="section" id="faq">
  <div class="wrap">
    <div style="text-align:center;margin-bottom:clamp(36px,4vw,56px)">
      <p class="eyebrow rv" style="justify-content:center">{E(L["faq_eyebrow"])}</p>
      <h2 class="rv rv-1">{E(L["faq_h"])}</h2>
    </div>
    <div class="faq rv rv-1">{faq}</div>
  </div>
</section>

<section class="section section--deep cta" id="proposta">
  <div class="wrap cta__grid">
    <div>
      <p class="eyebrow rv">{E(L["cta_eyebrow"])}</p>
      <h2 class="rv rv-1">{E(L["cta_h"])}</h2>
      <p class="lede rv rv-2">{E(L["cta_lede"])}</p>
      <div class="cta__side rv rv-3">{ctasteps}</div>
      <div style="margin-top:36px" class="rv rv-4">
        <a href="{wa}" class="btn btn--outlineDeep">{E(L["cta_wa"])}</a>
      </div>
    </div>
    <form class="form rv rv-2" name="{L["form_name"]}" method="POST" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="{L["form_name"]}">
      <input type="hidden" name="lang" value="{L["code"]}">
      <p class="hp"><label>{E(L["f_hp"])} <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      <div class="form__row">
        <label class="field"><span>{E(L["f_name"])}</span><input type="text" name="name" required autocomplete="name" placeholder="{E(L["f_name_ph"])}"></label>
        <label class="field"><span>{E(L["f_comp"])}</span><input type="text" name="company" autocomplete="organization" placeholder="{E(L["f_comp_ph"])}"></label>
      </div>
      <div class="form__row">
        <label class="field"><span>{E(L["f_mail"])}</span><input type="email" name="email" required autocomplete="email" placeholder="{E(L["f_mail_ph"])}"></label>
        <label class="field"><span>{E(L["f_wa"])}</span><input type="tel" name="phone" required autocomplete="tel" placeholder="{E(L["f_wa_ph"])}"></label>
      </div>
      <label class="field"><span>{E(L["f_need"])}</span><select name="service" required><option value="">{E(L["f_need_ph"])}</option>{needs}</select></label>
      <label class="field"><span>{E(L["f_budget"])}</span><select name="budget"><option value="">{E(L["f_budget_ph"])}</option>{budgets}</select></label>
      <label class="field"><span>{E(L["f_msg"])}</span><textarea name="message" placeholder="{E(L["f_msg_ph"])}"></textarea></label>
      <button type="submit" class="btn btn--flame">{E(L["f_send"])} <span class="ar" aria-hidden="true">&rarr;</span></button>
      <p class="form__note">{E(L["f_note"])}</p>
    </form>
  </div>
</section>

</main>

<footer class="ft">
  <div class="wrap">
    <div class="ft__grid">
      <div class="ft__about">
        <a href="{p}" class="logo">digify<i>.</i></a>
        <p>{E(L["ft_about"])}</p>
      </div>
      <div><h4>{E(L["ft_svc"])}</h4><ul>{ftsvc}</ul></div>
      <div><h4>{E(L["ft_comp"])}</h4><ul>{ftcomp}</ul></div>
      <div><h4>{E(L["ft_contact"])}</h4><ul>
        <li><a href="{wa}">{PHONE_LABEL}</a></li>
        <li><a href="https://instagram.com/digify.live">@digify.live</a></li>
        <li><a href="#proposta">{E(L["cta_nav"])}</a></li>
      </ul></div>
    </div>
    <div class="ft__base">
      <span>{E(L["ft_rights"])}</span>
      <span><a href="/politica-de-privacidade/">{E(L["ft_priv"])}</a> &middot; <a href="/sitemap.xml">{E(L["ft_map"])}</a></span>
    </div>
  </div>
</footer>

<a class="wa" href="{wa}" aria-label="{E(L["wa_label"])}">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.2-1.7-.9-2-1-.3-.1-.5-.2-.6.2-.2.3-.7.9-.9 1.1-.2.2-.3.2-.6.1-.3-.2-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.5-.5c.1-.2.2-.3.3-.5 0-.2 0-.4 0-.5 0-.2-.6-1.6-.9-2.1-.2-.5-.4-.5-.6-.5h-.5c-.2 0-.5.1-.7.3-.2.3-.9.9-.9 2.2s1 2.6 1.1 2.8c.1.2 1.9 2.9 4.6 4 .6.3 1.1.4 1.5.6.6.2 1.2.2 1.6.1.5-.1 1.7-.7 1.9-1.3.2-.7.2-1.2.2-1.3-.1-.2-.3-.2-.6-.4zM12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.4 1.3 4.9L2 22l5.3-1.4c1.4.8 3 1.2 4.7 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm0 18.2c-1.6 0-3.1-.4-4.4-1.2l-.3-.2-3.1.8.8-3-.2-.3c-.9-1.4-1.3-3-1.3-4.6C3.5 7.3 7.3 3.5 12 3.5S20.5 7.3 20.5 12 16.7 20.2 12 20.2z"/></svg>
</a>

<script type="application/ld+json">
{schema(L)}
</script>
<script src="/assets/digify.js" defer></script>
</body>
</html>
'''




def build_404():
    L = PT
    ld = json.dumps({"@context": "https://schema.org",
                     "@type": "WebPage", "name": "Página não encontrada",
                     "inLanguage": "pt-BR"}, ensure_ascii=False, indent=2)
    body = """<main id="main">
<section class="phero" style="--c:var(--flame);padding-block:clamp(60px,10vw,120px)">
  <div class="wrap phero__in" style="text-align:center;margin:0 auto">
    <p class="eyebrow rv" style="justify-content:center">Erro 404</p>
    <h1 class="rv rv-1">Essa página mudou de endereço.</h1>
    <p class="lede rv rv-2" style="margin-left:auto;margin-right:auto">Ou nunca existiu. De todo jeito, o que você procurava provavelmente está em um destes lugares.</p>
    <div class="phero__cta rv rv-3" style="justify-content:center">
      <a href="/" class="btn btn--flame">Voltar para a home</a>
      <a href="/servicos/" class="btn btn--ghost">Ver os serviços</a>
      <a href="/blog/" class="btn btn--ghost">Ir para o blog</a>
    </div>
  </div>
</section>
</main>
"""
    return (head(L, "Página não encontrada | Digify",
                 "A página que você procura não existe ou mudou de endereço.",
                 SITE + "/404.html", alt=False,
                 extra='<meta name="robots" content="noindex, follow">')
            + header(L, home_nav=False) + body
            + footer(L, "".join('<li><a href="%s">%s</a></li>' % (h, E(t)) for h, t in [
                ("/servicos/", "Todos os serviços"), ("/sobre/", "Sobre a Digify"),
                ("/blog/", "Blog"), ("/contato/", "Contato")]))
            + tail(ld))


def llms_txt(inner_urls):
    """Guia para crawlers de IA — cresce a chance de a Digify ser citada em resposta gerada."""
    import postpage
    posts = postpage.load_index()[:15]
    lines = [
        "# Digify",
        "",
        "> Agência web brasileira full-stack com mais de 10 anos e 300 projetos entregues. "
        "Criação de sites, desenvolvimento de apps, SEO, marketing digital, e-commerce e "
        "sistemas sob medida. Atendimento remoto no Brasil e no exterior, em português, "
        "inglês e espanhol.",
        "",
        "Contato: WhatsApp %s | %s/contato/" % (PHONE_LABEL, SITE),
        "",
        "## Serviços",
    ]
    for _c, _t, name, href, desc in PT["svcs"]:
        lines.append("- [%s](%s%s): %s" % (name, SITE, href, desc))
    lines += ["", "## Páginas", 
              "- [Home](%s/): visão geral da agência" % SITE,
              "- [Sobre](%s/sobre/): quem é a Digify, princípios e método" % SITE,
              "- [Contato](%s/contato/): diagnóstico gratuito e proposta" % SITE,
              "- [English](%s/en/) | [Español](%s/es/)" % (SITE, SITE),
              "", "## Conteúdo recente"]
    for p in posts:
        lines.append("- [%s](%s/blog/%s/): %s" % (p["title"], SITE, p["slug"], p["excerpt"]))
    lines += ["", "## Observação",
              "Todo o conteúdo é original e produzido pela Digify. "
              "Citações são bem-vindas com atribuição e link para a página de origem.", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------- write
def main():
    for L in LANGS:
        d = os.path.join(ROOT, L["dir"]) if L["dir"] else ROOT
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(build(L))
        print("  ->", (L["dir"] or "") + "index.html")

    import inner, postpage, portfolio
    inner_urls, post_urls = inner.build_all()
    inner_urls.append(portfolio.build_portfolio())
    print("  -> portfolio/index.html")
    cat_urls = postpage.build_categories()
    inner_urls += cat_urls
    print("  -> %d hubs de categoria no blog" % len(cat_urls))
    done, total = postpage.build_posts()
    print("  -> %d/%d artigos renderizados (faltam post.json nos demais)" % (done, total))
    open(os.path.join(ROOT, "blog", "rss.xml"), "w", encoding="utf-8").write(postpage.rss())
    print("  -> blog/rss.xml")

    alts = "".join(
        '\n    <xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (O["code"], url_of(O))
        for O in LANGS) + '\n    <xhtml:link rel="alternate" hreflang="x-default" href="%s/"/>' % SITE

    parts = []
    for L in LANGS:
        parts.append("\n  <url>\n    <loc>%s</loc>\n    <changefreq>weekly</changefreq>"
                     "\n    <priority>1.0</priority>%s\n  </url>" % (url_of(L), alts))
    for u in inner_urls:
        pr = "0.9" if u.startswith("servicos/") else "0.7"
        parts.append("\n  <url>\n    <loc>%s/%s</loc>\n    <changefreq>monthly</changefreq>"
                     "\n    <priority>%s</priority>\n  </url>" % (SITE, u, pr))
    posts_meta = {("blog/%s/" % p["slug"]): (p.get("dateISO") or "")[:10]
                  for p in postpage.load_index()}
    for u in post_urls:
        lm = posts_meta.get(u, "")
        lmx = "\n    <lastmod>%s</lastmod>" % lm if lm else ""
        parts.append("\n  <url>\n    <loc>%s/%s</loc>%s\n    <changefreq>monthly</changefreq>"
                     "\n    <priority>0.6</priority>\n  </url>" % (SITE, u, lmx))

    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">' + "".join(parts) + "\n</urlset>\n")
    print("  -> sitemap.xml (%d URLs)" % (len(LANGS) + len(inner_urls) + len(post_urls)))

    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(
        "User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE)
    print("  -> robots.txt")

    open(os.path.join(ROOT, "_headers"), "w", encoding="utf-8").write(
        "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  X-Frame-Options: SAMEORIGIN\n\n/assets/*\n  Cache-Control: public, max-age=31536000, immutable\n\n"
        "/\n  Content-Language: pt-BR\n/en/*\n  Content-Language: en\n/es/*\n  Content-Language: es\n")
    print("  -> _headers")

    open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8").write(build_404())
    print("  -> 404.html")

    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(llms_txt(inner_urls))
    print("  -> llms.txt")


if __name__ == "__main__":
    main()
