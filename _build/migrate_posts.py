# -*- coding: utf-8 -*-
"""
Digify — migração dos artigos antigos.

Roda UMA vez, dentro do repositório. Lê cada blog/<slug>/index.html gerado pelo
template antigo, extrai o corpo do artigo e a imagem do Unsplash, e grava
blog/<slug>/post.json. A partir daí o build.py renderiza todos os artigos com o
design novo — inclusive os 44 já publicados.

Uso:  python3 _build/migrate_posts.py         (simula, não escreve)
      python3 _build/migrate_posts.py --write (grava de verdade)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
WRITE = "--write" in sys.argv


def extract_content(html):
    """Corpo do artigo: conteúdo de <div class="post-content-wrap" ...>."""
    m = re.search(r'<div class="post-content-wrap"[^>]*>(.*?)</div>\s*(?=<!--\s*CTA|<div style="max-width:760px)',
                  html, re.S)
    if not m:
        m = re.search(r'<div class="post-content-wrap"[^>]*>(.*)', html, re.S)
        if not m:
            return None
        body = m.group(1)
        cut = body.find('<!-- CTA')
        if cut == -1:
            cut = body.find('<div style="max-width:760px')
        body = body[:cut] if cut != -1 else body
    else:
        body = m.group(1)

    body = body.strip()
    # remove um </div> órfão de fechamento, se sobrar
    if body.endswith("</div>"):
        opens = len(re.findall(r"<div\b", body))
        closes = len(re.findall(r"</div>", body))
        if closes > opens:
            body = body[: body.rfind("</div>")].rstrip()
    return body


def extract_image(html):
    """Imagem do Unsplash no bloco .post-thumb-hero, se houver."""
    block = re.search(r'<div class="post-thumb-hero">(.*?)</div>\s*</div>', html, re.S)
    if not block:
        return None
    b = block.group(1)
    img = re.search(r'<img\s+src="([^"]+)"\s+alt="([^"]*)"', b)
    if not img:
        return None
    credit = re.search(r'<a href="([^"?]+)[^"]*"[^>]*>([^<]+)</a>', b)
    return {
        "url": img.group(1),
        "alt": img.group(2),
        "author": credit.group(2).strip() if credit else "Unsplash",
        "authorUrl": credit.group(1) if credit else "https://unsplash.com",
    }


def guess_subject(title):
    """Sem o assunto original, usa o título como chave de deduplicação."""
    return title


def main():
    idx_file = os.path.join(BLOG, "index.json")
    if not os.path.exists(idx_file):
        print("blog/index.json não encontrado. Rode dentro do repositório.")
        return
    index = json.load(open(idx_file, encoding="utf-8"))

    ok = skip = fail = 0
    for p in index:
        d = os.path.join(BLOG, p["slug"])
        src = os.path.join(d, "index.html")
        dst = os.path.join(d, "post.json")

        if os.path.exists(dst):
            skip += 1
            continue
        if not os.path.exists(src):
            print("  ausente   %s" % p["slug"][:56])
            fail += 1
            continue

        html = open(src, encoding="utf-8").read()
        content = extract_content(html)
        if not content or len(content) < 400:
            print("  vazio     %s" % p["slug"][:56])
            fail += 1
            continue

        image = extract_image(html)
        words = len(re.sub(r"<[^>]+>", " ", content).split())
        print("  ok  %5d palavras  %s  %s" % (words, "IMG" if image else "   ", p["slug"][:48]))
        if WRITE:
            json.dump({"content": content, "image": image},
                      open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        ok += 1

        if "subject" not in p:
            p["subject"] = guess_subject(p["title"])

    if WRITE:
        json.dump(index, open(idx_file, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("\n  %d migrados | %d já tinham post.json | %d falharam" % (ok, skip, fail))
    if not WRITE:
        print("  (simulação — rode com --write para gravar)")
    else:
        print("  Agora rode: python3 _build/build.py")


if __name__ == "__main__":
    main()
