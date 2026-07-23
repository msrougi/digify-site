# -*- coding: utf-8 -*-
"""Digify — geração das páginas internas em PT-BR."""
import json, os
from build import head, header, footer, tail, wa_url, E, SITE, load_posts
from content import PT
from services_pt import SERVICES, SVC_INDEX
from pages_pt import PAGES

L0 = PT
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INNER_FT = "".join(f'<li><a href="{h}">{E(t)}</a></li>' for h, t in [
    ("/servicos/", "Todos os serviços"), ("/portfolio/", "Portfólio"), ("/sobre/", "Sobre a Digify"),
    ("/blog/", "Blog"), ("/contato/", "Contato"),
    ("https://plugins.digify.live/", "Plugins WordPress"),
    ("/politica-de-privacidade/", "Política de privacidade")])

STEPCOLS = ["var(--flame)", "#5B72FF", "#A57BFF", "#25C08A", "var(--cyan)"]
CAT_COLOR = {"SEO": "jade", "Criação de Sites": "flame", "Apps": "ultra",
             "Marketing Digital": "violet", "E-commerce": "pink", "Sistemas": "cyan"}


def crumbs(items, c):
    out = []
    for i, (href, name) in enumerate(items):
        out.append(f'<a href="{href}">{E(name)}</a>' if href else f"<b>{E(name)}</b>")
        if i < len(items) - 1:
            out.append("<span>&rsaquo;</span>")
    return ('<div class="wrap"><nav class="crumbs" style="--c:var(--%s)" aria-label="Trilha">%s</nav></div>'
            % (c, "".join(out)))


def crumb_ld(items, url):
    el = []
    for i, (href, name) in enumerate(items):
        el.append({"@type": "ListItem", "position": i + 1, "name": name,
                   "item": (SITE + href) if href else url})
    return {"@type": "BreadcrumbList", "@id": url + "#crumbs", "itemListElement": el}


def faq_block(faq):
    inner = "".join('<details><summary>%s</summary><div class="ans">%s</div></details>'
                    % (E(q), E(a)) for q, a in faq)
    return ('<section class="section" id="faq"><div class="wrap">'
            '<div style="text-align:center;margin-bottom:clamp(36px,4vw,56px)">'
            '<p class="eyebrow rv" style="justify-content:center">Dúvidas frequentes</p>'
            '<h2 class="rv rv-1">Sem letra miúda.</h2></div>'
            '<div class="faq rv rv-1">%s</div></div></section>' % inner)


def cta_block():
    return ('<section class="section section--deep"><div class="wrap" style="text-align:center">'
            '<p class="eyebrow rv" style="justify-content:center">Próximo passo</p>'
            '<h2 class="rv rv-1">Vamos começar pelo diagnóstico.</h2>'
            '<p class="lede rv rv-2" style="margin:22px auto 0">Conte o que você precisa. '
            'Respondemos em até um dia útil com um diagnóstico do cenário atual e os caminhos '
            'possíveis, sem compromisso.</p>'
            '<div class="hero__cta rv rv-3" style="justify-content:center;margin-top:34px">'
            '<a href="/contato/" class="btn btn--flame">Solicitar proposta '
            '<span class="ar" aria-hidden="true">&rarr;</span></a>'
            '<a href="%s" class="btn btn--outlineDeep">Falar no WhatsApp</a>'
            '</div></div></section>' % wa_url(L0))



def contact_form():
    L = L0
    needs = "".join("<option>%s</option>" % E(o) for o in L["f_needs"])
    budgets = "".join("<option>%s</option>" % E(o) for o in L["f_budgets"])
    return ("""<section class="section section--deep cta" id="proposta"><div class="wrap cta__grid">
  <div>
    <p class="eyebrow rv">Formulário</p>
    <h2 class="rv rv-1">Conte o seu caso.</h2>
    <p class="lede rv rv-2">Quanto mais contexto, mais útil fica o diagnóstico. Se preferir, o WhatsApp resolve igual.</p>
    <div class="cta__side rv rv-3">
      <div class="cta__item" style="--c:var(--flame)"><b>01</b><span>Você envia o contexto do projeto.</span></div>
      <div class="cta__item" style="--c:#5B72FF"><b>02</b><span>Analisamos o site, os concorrentes e o mercado.</span></div>
      <div class="cta__item" style="--c:#25C08A"><b>03</b><span>Você recebe o diagnóstico e a proposta com escopo fechado.</span></div>
    </div>
    <div style="margin-top:36px" class="rv rv-4">
      <a href="%s" class="btn btn--outlineDeep">Prefiro falar no WhatsApp</a>
    </div>
  </div>
  <form class="form rv rv-2" name="contato-pt" method="POST" data-netlify="true" netlify-honeypot="bot-field">
    <input type="hidden" name="form-name" value="contato-pt">
    <input type="hidden" name="lang" value="pt-BR">
    <p class="hp"><label>Não preencha: <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
    <div class="form__row">
      <label class="field"><span>%s</span><input type="text" name="name" required autocomplete="name" placeholder="%s"></label>
      <label class="field"><span>%s</span><input type="text" name="company" autocomplete="organization" placeholder="%s"></label>
    </div>
    <div class="form__row">
      <label class="field"><span>%s</span><input type="email" name="email" required autocomplete="email" placeholder="%s"></label>
      <label class="field"><span>%s</span><input type="tel" name="phone" required autocomplete="tel" placeholder="%s"></label>
    </div>
    <label class="field"><span>%s</span><select name="service" required><option value="">%s</option>%s</select></label>
    <label class="field"><span>%s</span><select name="budget"><option value="">%s</option>%s</select></label>
    <label class="field"><span>%s</span><textarea name="message" placeholder="%s"></textarea></label>
    <button type="submit" class="btn btn--flame">%s <span class="ar" aria-hidden="true">&rarr;</span></button>
    <p class="form__note">%s</p>
  </form>
</div></section>""" % (wa_url(L), E(L["f_name"]), E(L["f_name_ph"]), E(L["f_comp"]), E(L["f_comp_ph"]),
                       E(L["f_mail"]), E(L["f_mail_ph"]), E(L["f_wa"]), E(L["f_wa_ph"]),
                       E(L["f_need"]), E(L["f_need_ph"]), needs,
                       E(L["f_budget"]), E(L["f_budget_ph"]), budgets,
                       E(L["f_msg"]), E(L["f_msg_ph"]), E(L["f_send"]), E(L["f_note"])))


def rich_page(P, kind="service"):
    url = "%s/%s" % (SITE, P["slug"])
    c = P["c"]
    trail = [("/", "Home")]
    if kind == "service":
        trail.append(("/servicos/", "Serviços"))
    trail.append((None, P["eyebrow"]))

    prose = "".join("<p>%s</p>" % b for b in P["problem"])
    feats = "".join(
        '<div class="feat rv rv-%d" style="--c:var(--%s);--t:var(--%s-t)"><b>%s</b><h3>%s</h3><p>%s</p></div>'
        % (i % 3 + 1, c, c, E(tag), E(t), E(d))
        for i, (tag, t, d) in enumerate(P["deliver"]))
    steps = "".join(
        '<div class="step rv rv-%d" style="--c:%s"><b>0%d</b><h3>%s</h3><p>%s</p></div>'
        % (i + 1, STEPCOLS[i % 5], i + 1, E(t), E(d))
        for i, (t, d) in enumerate(P["how"]))
    chips = "".join("<span>%s</span>" % E(x) for x in P["tech"])
    rel = "".join(
        '<a href="/%s" style="--c:var(--%s);--t:var(--%s-t)"><b>Serviço</b><strong>%s</strong><span>%s</span></a>'
        % (sl, SVC_INDEX[sl][2], SVC_INDEX[sl][2], E(SVC_INDEX[sl][0]), E(SVC_INDEX[sl][1]))
        for sl in P["related"])

    graph = [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": P["title"],
         "description": P["desc"], "inLanguage": "pt-BR",
         "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": SITE + "/#org"}},
        crumb_ld(trail, url),
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "pt-BR",
         "isPartOf": {"@id": url + "#webpage"},
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P["faq"]]},
    ]
    if kind == "service":
        graph.append({"@type": "Service", "@id": url + "#service", "name": P["eyebrow"],
                      "description": P["desc"], "serviceType": P["eyebrow"], "url": url,
                      "provider": {"@id": SITE + "/#org"},
                      "areaServed": {"@type": "Country", "name": "Brasil"}})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, indent=2)

    body = """<main id="main">
%s
<section class="phero" style="--c:var(--%s)">
  <div class="wrap phero__in">
    <p class="eyebrow rv">%s</p>
    <h1 class="rv rv-1">%s</h1>
    <p class="lede rv rv-2">%s</p>
    <div class="phero__cta rv rv-3">
      <a href="/contato/" class="btn btn--flame">Solicitar proposta <span class="ar" aria-hidden="true">&rarr;</span></a>
      <a href="#faq" class="btn btn--ghost">Ver dúvidas frequentes</a>
    </div>
  </div>
</section>

<section class="section section--tight"><div class="wrap">
  <h2 class="rv">%s</h2>
  <div class="prose rv rv-1" style="margin-top:24px">%s</div>
</div></section>

<section class="section section--mist"><div class="wrap">
  <p class="eyebrow rv">Entrega</p>
  <h2 class="rv rv-1">%s</h2>
  <div class="feats">%s</div>
  <div class="chips rv rv-2" style="--c:var(--%s)">%s</div>
</div></section>

<section class="section section--deep"><div class="wrap">
  <p class="eyebrow rv">Processo</p>
  <h2 class="rv rv-1">%s</h2>
  <div class="steps">%s</div>
</div></section>

<section class="section section--tight"><div class="wrap">
  <p class="eyebrow rv">Continue por aqui</p>
  <h2 class="rv rv-1">Costuma vir junto.</h2>
  <div class="rel">%s</div>
</div></section>

%s
%s
</main>
""" % (crumbs(trail, c), c, E(P["eyebrow"]), E(P["h1"]), E(P["lede"]),
       E(P["problem_h"]), prose, E(P["deliver_h"]), feats, c, chips,
       E(P["how_h"]), steps, rel, faq_block(P["faq"]),
       contact_form() if P.get("kind") == "contact" else cta_block())

    return (head(L0, P["title"], P["desc"], url, alt=False)
            + header(L0, home_nav=False) + body + footer(L0, INNER_FT) + tail(ld))


def legal_page(P):
    url = "%s/%s" % (SITE, P["slug"])
    trail = [("/", "Home"), (None, P.get("crumb", P["eyebrow"]))]
    body_sections = "".join("<h2>%s</h2>%s" % (E(h), "".join(b)) for h, b in P["sections"])
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": P["title"],
         "description": P["desc"], "inLanguage": "pt-BR",
         "isPartOf": {"@id": SITE + "/#site"}},
        crumb_ld(trail, url)]}, ensure_ascii=False, indent=2)
    body = """<main id="main">
%s
<section class="phero" style="--c:var(--%s)">
  <div class="wrap phero__in">
    <p class="eyebrow rv">%s</p>
    <h1 class="rv rv-1">%s</h1>
    <p class="lede rv rv-2">%s</p>
    <p class="rv rv-3" style="font-family:var(--mono);font-size:.7rem;letter-spacing:.1em;color:var(--muted);margin-top:26px">ATUALIZADA EM %s</p>
  </div>
</section>
<section class="section section--tight"><div class="wrap"><div class="legal rv">%s</div></div></section>
</main>
""" % (crumbs(trail, P["c"]), P["c"], E(P["eyebrow"]), E(P["h1"]), E(P["lede"]),
       E(P["updated"]).upper(), body_sections)
    return (head(L0, P["title"], P["desc"], url, alt=False)
            + header(L0, home_nav=False) + body + footer(L0, INNER_FT) + tail(ld))



def services_hub():
    """Página pai de /servicos/ — hub que faltava."""
    url = SITE + "/servicos/"
    trail = [("/", "Home"), (None, "Serviços")]
    cards = "".join(
        '<a class="svc rv rv-%d" href="/%s" style="--c:var(--%s);--t:var(--%s-t)">'
        '<span class="svc__tag">%s</span><h3>%s</h3><p>%s</p>'
        '<span class="svc__go">Ver serviço <span class="ar" aria-hidden="true">&rarr;</span></span></a>'
        % (n % 3 + 1, S["slug"], S["c"], S["c"], E(S["eyebrow"]), E(S["h1"]), E(S["lede"]))
        for n, S in enumerate(SERVICES))

    faq = [
     ("Posso contratar só um serviço?",
      "Pode, e é o mais comum. A maioria dos clientes começa por um site ou por SEO e amplia depois, "
      "quando o primeiro projeto já mostrou resultado. Não trabalhamos com pacote fechado obrigatório."),
     ("Vocês fazem tudo internamente?",
      "Sim. Design, desenvolvimento, SEO e mídia paga são executados pelo nosso time. Isso importa porque "
      "terceirizar SEO para quem não mexe no código transforma qualquer correção técnica numa negociação de semanas."),
     ("Qual serviço eu devo contratar primeiro?",
      "Depende de onde está o gargalo. Se as visitas chegam e não viram cliente, o problema é o site. "
      "Se ninguém chega, é SEO ou mídia paga. Se a equipe perde horas digitando, é sistema. "
      "O diagnóstico gratuito existe para responder exatamente isso antes de você gastar."),
     ("Um serviço atrapalha o outro?",
      "Ao contrário. Site rápido melhora o SEO, SEO barato reduz o custo da mídia paga, e sistema "
      "integrado alimenta os dois com dado real. Quando tudo passa pelo mesmo time, uma correção resolve "
      "em três frentes de uma vez."),
    ]

    graph = [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url,
         "name": "Serviços | Digify", "inLanguage": "pt-BR",
         "description": "Criação de sites, desenvolvimento de apps, SEO, marketing digital, e-commerce e sistemas sob medida.",
         "isPartOf": {"@id": SITE + "/#site"}, "about": {"@id": SITE + "/#org"}},
        crumb_ld(trail, url),
        {"@type": "ItemList", "@id": url + "#list", "itemListElement": [
            {"@type": "ListItem", "position": n + 1, "url": "%s/%s" % (SITE, S["slug"]),
             "name": S["eyebrow"]} for n, S in enumerate(SERVICES)]},
        {"@type": "FAQPage", "@id": url + "#faq", "inLanguage": "pt-BR",
         "isPartOf": {"@id": url + "#webpage"},
         "mainEntity": [{"@type": "Question", "name": q,
                         "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph},
                    ensure_ascii=False, indent=2)

    body = """<main id="main">
%s
<section class="phero" style="--c:var(--flame)">
  <div class="wrap phero__in">
    <p class="eyebrow rv">Serviços</p>
    <h1 class="rv rv-1">Um parceiro, não seis fornecedores.</h1>
    <p class="lede rv rv-2">Criação de sites, apps, SEO, mídia paga, e-commerce e sistemas sob medida — executados pelo mesmo time, o que evita o jogo de empurra que trava projeto digital.</p>
    <div class="phero__cta rv rv-3">
      <a href="/contato/" class="btn btn--flame">Solicitar proposta <span class="ar" aria-hidden="true">&rarr;</span></a>
      <a href="#faq" class="btn btn--ghost">Ver dúvidas frequentes</a>
    </div>
  </div>
</section>

<section class="section section--tight"><div class="wrap">
  <h2 class="rv">Por que isso importa.</h2>
  <div class="prose rv rv-1" style="margin-top:24px">
    <p>A divisão clássica é conhecida: uma agência cuida do site, outra do SEO, um freelancer mexe no sistema. Quando algo quebra, <strong>cada um aponta para o outro</strong> e o prejuízo fica com você.</p>
    <p>O caso mais frequente é o SEO travado por uma limitação técnica do site. Quem faz SEO não tem acesso ao código, quem fez o site não entende a exigência, e a correção que levaria uma tarde vira três semanas de e-mail.</p>
    <p>Aqui as seis frentes passam pelo mesmo time. <strong>Não porque vender tudo junto é melhor negócio para nós</strong> — e sim porque uma correção técnica resolve em site, SEO e conversão de uma vez só.</p>
  </div>
</div></section>

<section class="section section--mist"><div class="wrap">
  <p class="eyebrow rv">O que fazemos</p>
  <h2 class="rv rv-1">Seis frentes, um objetivo.</h2>
  <p class="lede rv rv-2" style="margin-top:18px">Cada projeto começa pelo problema do negócio, não pelo catálogo.</p>
  <div class="svcs" style="margin-top:clamp(36px,4vw,52px)">%s</div>
</div></section>

<section class="section section--deep"><div class="wrap">
  <p class="eyebrow rv">Como trabalhamos</p>
  <h2 class="rv rv-1">Diagnóstico. Plano. Código. Crescimento.</h2>
  <div class="steps">%s</div>
</div></section>

%s
%s
</main>
""" % (crumbs(trail, "flame"), cards,
       "".join('<div class="step rv rv-%d" style="--c:%s"><b>0%d</b><h3>%s</h3><p>%s</p></div>'
               % (n + 1, STEPCOLS[n], n + 1, E(t), E(d))
               for n, (t, d) in enumerate(L0["steps"])),
       faq_block(faq), cta_block())

    return (head(L0, "Serviços | Criação de Sites, Apps, SEO e Sistemas | Digify",
                 "Criação de sites, desenvolvimento de apps, SEO, marketing digital, e-commerce e sistemas sob medida. Seis frentes executadas pelo mesmo time.",
                 url, alt=False)
            + header(L0, home_nav=False) + body + footer(L0, INNER_FT) + tail(ld))


def blog_index():
    url = SITE + "/blog/"
    posts = load_posts()
    trail = [("/", "Home"), (None, "Blog")]
    items = ""
    for i, p in enumerate(posts):
        col = p.get("color") or CAT_COLOR.get(p["cat"], "flame")
        items += ('<a class="bitem rv rv-%d" href="%s" style="--c:var(--%s);--t:var(--%s-t)">'
                  '<div><span class="bitem__cat">%s</span><h3>%s</h3><p>%s</p></div>'
                  '<time datetime="%s">%s</time></a>'
                  % (i % 3 + 1, p["url"], col, col, E(p["cat"]), E(p["title"]),
                     E(p["desc"]), p["date"], E(p["label"])))
    ld = json.dumps({"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": url + "#webpage", "url": url, "name": "Blog | Digify",
         "description": "Estratégias práticas sobre criação de sites, SEO, desenvolvimento e marketing digital.",
         "inLanguage": "pt-BR", "isPartOf": {"@id": SITE + "/#site"}},
        crumb_ld(trail, url),
        {"@type": "ItemList", "@id": url + "#list", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": SITE + p["url"], "name": p["title"]}
            for i, p in enumerate(posts)]}]}, ensure_ascii=False, indent=2)
    body = """<main id="main">
%s
<section class="phero" style="--c:var(--flame)">
  <div class="wrap phero__in">
    <p class="eyebrow rv">Conteúdo</p>
    <h1 class="rv rv-1">O que está acontecendo.</h1>
    <p class="lede rv rv-2">Estratégias práticas sobre criação de sites, SEO, desenvolvimento e marketing digital, publicadas com frequência e escritas para serem usadas.</p>
  </div>
</section>
<section class="section section--tight"><div class="wrap">%s<div class="blist">%s</div></div></section>
%s
</main>
""" % (crumbs(trail, "flame"), __import__("postpage").cat_nav(), items, cta_block())
    return (head(L0, "Blog | Criação de Sites, SEO e Marketing Digital | Digify",
                 "Estratégias práticas sobre criação de sites, desenvolvimento de apps, SEO e marketing digital. Conteúdo prático para crescer na internet.",
                 url, alt=False)
            + header(L0, home_nav=False) + body + footer(L0, INNER_FT) + tail(ld))


def write(path, txt):
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(txt)
    print("  ->", path + "index.html")


def build_all():
    urls = []
    write("servicos/", services_hub())
    urls.append("servicos/")
    for S in SERVICES:
        write(S["slug"], rich_page(S, "service"))
        urls.append(S["slug"])
    for P in PAGES:
        if P.get("kind") == "legal":
            write(P["slug"], legal_page(P))
        else:
            write(P["slug"], rich_page(P, "page"))
        urls.append(P["slug"])
    write("blog/", blog_index())
    urls.append("blog/")
    return urls, [p["url"].strip("/") + "/" for p in load_posts()]
