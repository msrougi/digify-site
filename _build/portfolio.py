# -*- coding: utf-8 -*-
"""Digify — página de portfólio e cards de case."""
import json, os, re
from build import head, header, footer, tail, wa_url, E, SITE, PT
from cases_pt import CASES, PORTFOLIO

L0 = PT
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INNER_FT = "".join('<li><a href="%s">%s</a></li>' % (h, E(t)) for h, t in [
    ("/servicos/", "Todos os serviços"), ("/portfolio/", "Portfólio"),
    ("/sobre/", "Sobre a Digify"), ("/blog/", "Blog"), ("/contato/", "Contato"),
    ("/politica-de-privacidade/", "Política de privacidade")])


def shot(cs):
    """Usa a captura se existir; senão, bloco tipográfico. Nunca imagem quebrada."""
    for ext in ("jpg", "png", "webp"):
        rel = "assets/cases/%s.%s" % (cs["slug"], ext)
        if os.path.exists(os.path.join(ROOT, rel)):
            host = re.sub(r"^https?://", "", cs["url"]).rstrip("/")
            return ('<div class="case__shot">'
                    '<div class="case__bar"><i></i><i></i><i></i><u>%s</u></div>'
                    '<img src="/%s" alt="Site %s desenvolvido pela Digify" '
                    'width="1600" height="1000" loading="lazy" decoding="async"></div>'
                    % (E(host), rel, E(cs["name"])))
    return ('<div class="case__shot case__shot--none" aria-hidden="true">'
            '<b>%s</b><span>%s</span></div>' % (E(cs["name"]), E(cs["sector"])))


def case_card(cs, n):
    itens = "".join("<li>%s</li>" % E(x) for x in cs["escopo"])
    chips = "".join("<span>%s</span>" % E(x) for x in cs["stack"])
    ext = ""
    if cs.get("url"):
        ext = ('<a href="%s" class="btn btn--ghost" target="_blank" rel="noopener">'
               'Ver o site <span class="ar" aria-hidden="true">&rarr;</span></a>' % cs["url"])
    return ('<article class="case rv rv-%d" style="--c:var(--%s);--t:var(--%s-t)">'
            '<div>'
            '<div class="case__meta"><span>%s</span><span>%s</span><span>%s</span></div>'
            '<h3>%s</h3>'
            '<p class="case__tag">%s</p>'
            '<p class="case__prob">%s</p>'
            '<ul>%s</ul>'
            '<div class="case__foot">%s'
            '<a href="/contato/" class="btn btn--flame">Quero algo assim</a></div>'
            '<div class="chips" style="--c:var(--%s)">%s</div>'
            '</div>%s</article>'
            % (n % 3 + 1, cs["c"], cs["c"], E(cs["client"]), E(cs["sector"]), E(cs["year"]),
               E(cs["name"]), E(cs["tagline"]), E(cs["problem"]), itens, ext,
               cs["c"], chips, shot(cs)))


def home_cases():
    """Três cases em destaque, para entrar na home."""
    feat = [c for c in CASES if c.get("featured")][:3]
    cards = "".join(case_card(c, n) for n, c in enumerate(feat))
    return ('<section class="section section--mist" id="portfolio"><div class="wrap">'
            '<div class="head"><div>'
            '<p class="eyebrow rv">Portfólio</p>'
            '<h2 class="rv rv-1">Não é promessa. É o que já foi entregue.</h2>'
            '<p class="lede rv rv-2">Três dos últimos projetos que saíram daqui. Tem mais 300 atrás deles.</p>'
            '</div><a href="/portfolio/" class="btn btn--ghost rv rv-2">Ver o portfólio completo '
            '<span class="ar" aria-hidden="true">&rarr;</span></a></div>'
            '<div class="cases">%s</div></div></section>' % cards)


def portfolio_page():
    P = PORTFOLIO
    url = SITE + "/" + P["slug"]
    cards = "".join(case_card(c, n) for n, c in enumerate(CASES))
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": P["title"],
         "description": P["desc"], "inLanguage": "pt-BR",
         "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": SITE + "/#org"}},
        {"@type": "BreadcrumbList", "@id": url + "#crumbs", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Portfólio", "item": url}]},
        {"@type": "ItemList", "@id": url + "#list", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "item": {
                "@type": "CreativeWork", "name": c["name"], "url": c.get("url", url),
                "abstract": c["tagline"], "genre": c["sector"], "dateCreated": c["year"],
                "creator": {"@id": SITE + "/#org"}}}
            for n, c in enumerate(CASES)]}]}, ensure_ascii=False, indent=2)

    body = """<main id="main">
<div class="wrap"><nav class="crumbs" style="--c:var(--flame)" aria-label="Trilha">
  <a href="/">Home</a><span>&rsaquo;</span><b>Portfólio</b>
</nav></div>
<section class="phero" style="--c:var(--flame)">
  <div class="wrap phero__in">
    <p class="eyebrow rv">%s</p>
    <h1 class="rv rv-1">%s</h1>
    <p class="lede rv rv-2">%s</p>
    <div class="phero__cta rv rv-3">
      <a href="/contato/" class="btn btn--flame">Quero um projeto assim <span class="ar" aria-hidden="true">&rarr;</span></a>
      <a href="/servicos/" class="btn btn--ghost">Ver os serviços</a>
    </div>
  </div>
</section>
<section class="section section--tight"><div class="wrap"><div class="cases">%s</div></div></section>
<section class="section section--deep"><div class="wrap" style="text-align:center">
  <p class="eyebrow rv" style="justify-content:center">Próximo passo</p>
  <h2 class="rv rv-1">O próximo case pode ser o seu.</h2>
  <p class="lede rv rv-2" style="margin:22px auto 0">Conte o que você precisa. Respondemos em até um dia útil com um diagnóstico do cenário atual e os caminhos possíveis.</p>
  <div class="hero__cta rv rv-3" style="justify-content:center;margin-top:34px">
    <a href="/contato/" class="btn btn--flame">Solicitar proposta <span class="ar" aria-hidden="true">&rarr;</span></a>
    <a href="%s" class="btn btn--outlineDeep">Falar no WhatsApp</a>
  </div>
</div></section>
</main>
""" % (E(P["eyebrow"]), E(P["h1"]), E(P["lede"]), cards, wa_url(L0))

    return (head(L0, P["title"], P["desc"], url, alt=False)
            + header(L0, home_nav=False) + body + footer(L0, INNER_FT) + tail(ld))


def build_portfolio():
    d = os.path.join(ROOT, "portfolio")
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(portfolio_page())
    return "portfolio/"
