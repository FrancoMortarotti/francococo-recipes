#!/usr/bin/env python3
"""Generate the FrancoCoco recipe site from data/recipes/*.json.

Usage:  python3 build.py
Writes index.html and recipes/<slug>.html. Standard library only.
"""
import glob, html, json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
CATEGORIES = ["Appetizer", "Entree", "Salads", "Soup", "Sides", "Dessert", "Breakfast"]
SITE = "Franco &amp; Coco"
TAGLINE = "Recipes for a lifetime"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Lora:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">')

e = lambda s: html.escape(str(s), quote=True)


def load():
    recipes = []
    for f in glob.glob(os.path.join(ROOT, "data", "recipes", "*.json")):
        with open(f, encoding="utf-8") as fh:
            r = json.load(fh)
        r.setdefault("slug", os.path.splitext(os.path.basename(f))[0])
        recipes.append(r)
    cat = lambda r: CATEGORIES.index(r["category"]) if r["category"] in CATEGORIES else 99
    recipes.sort(key=lambda r: (cat(r), r.get("order", 999), r["title"]))
    return recipes


def head(title, prefix):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{FONTS}
<link rel="stylesheet" href="{prefix}style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🍝</text></svg>">
</head>
<body>
<header class="site-header">
  <a class="brand" href="{prefix}index.html"><span class="brand-name">{SITE}</span><span class="brand-tag">{TAGLINE}</span></a>
</header>
"""


def footer(prefix):
    return f"""<footer class="site-footer">
  <p>Franco and Coco's library of favorite recipes &middot; <em>tutto finisce a tarallucci e vino</em></p>
  <p>&copy; 2026 Mortarotti</p>
</footer>
</body>
</html>
"""


def render_list(items, tag):
    out, open_list = [], False
    for it in items:
        if it.startswith("## "):
            if open_list:
                out.append(f"</{tag}>"); open_list = False
            out.append(f"<h3>{e(it[3:])}</h3>")
        else:
            if not open_list:
                out.append(f"<{tag}>"); open_list = True
            out.append(f"<li>{mark_unclear(e(it))}</li>")
    if open_list:
        out.append(f"</{tag}>")
    return "\n".join(out)


def mark_unclear(s):
    # highlight [unclear ...] markers
    import re
    return re.sub(r"\[(unclear[^\]]*)\]", r'<span class="unclear">[\1]</span>', s)


def recipe_page(r):
    p = "../"
    meta = []
    if r.get("category"): meta.append(f'<span class="pill">{e(r["category"])}</span>')
    if r.get("servings"): meta.append(f'<span>Serves {e(r["servings"])}</span>')
    if r.get("time"): meta.append(f'<span>{e(r["time"])}</span>')
    parts = [head(f'{e(r["title"])} · {SITE}', p), '<main class="recipe">',
             f'<p class="back no-print"><a href="{p}index.html">&larr; All recipes</a></p>',
             '<article>',
             f'<h1>{e(r["title"])}</h1>',
             f'<div class="meta">{" ".join(meta)}</div>']
    if r.get("image"):
        parts.append(f'<img class="hero" src="{p}{e(r["image"])}" alt="{e(r["title"])}">')
    if r.get("intro"):
        parts.append(f'<p class="intro">{mark_unclear(e(r["intro"]))}</p>')
    parts.append('<div class="cols">')
    parts.append('<section class="ingredients"><h2>Ingredients</h2>' + render_list(r.get("ingredients", []), "ul") + '</section>')
    steps = r.get("steps", [])
    parts.append('<section class="steps"><h2>Instructions</h2>' +
                 (render_list(steps, "ol") if steps else '<p class="unclear">No instructions were included on the original page.</p>') +
                 '</section>')
    parts.append('</div>')
    if r.get("notes"):
        parts.append('<section class="notes"><h2>Notes</h2><ul>' + "".join(f"<li>{mark_unclear(e(n))}</li>" for n in r["notes"]) + '</ul></section>')
    if r.get("pdf"):
        parts.append(f'<p class="pdf no-print"><a href="{p}{e(r["pdf"])}">View the original recipe page (PDF)</a> &middot; <a href="#" onclick="window.print();return false;">Print this recipe</a></p>')
    parts.append('</article></main>')
    parts.append(footer(p))
    return "\n".join(parts)


def index_page(recipes):
    cats = [c for c in CATEGORIES if any(r["category"] == c for r in recipes)]
    btns = '<button class="chip active" data-cat="all">All</button>' + "".join(
        f'<button class="chip" data-cat="{e(c)}">{e(c)}</button>' for c in cats)
    cards = []
    for r in recipes:
        search = " ".join([r["title"], r["category"]] + [i for i in r.get("ingredients", []) if not i.startswith("## ")]).lower()
        img = f'<img src="{e(r["image"])}" alt="" loading="lazy">' if r.get("image") else '<div class="noimg">🍽️</div>'
        cards.append(f'''<a class="card" href="recipes/{e(r["slug"])}.html" data-cat="{e(r["category"])}" data-search="{e(search)}">
  <div class="thumb">{img}</div>
  <div class="card-body"><span class="pill">{e(r["category"])}</span><h2>{e(r["title"])}</h2></div>
</a>''')
    return head(f"{SITE} · Family Recipes", "") + f'''<main class="home">
<section class="welcome">
  <h1>Franco's Family Recipes</h1>
  <p class="lede">Franco and Coco's Library of Favorite Recipes</p>
  <p>And remember, &ldquo;<em>tutto finisce a tarallucci e vino</em>&rdquo;</p>
</section>
<div class="controls">
  <input id="q" type="search" placeholder="Search recipes or ingredients…" aria-label="Search recipes">
  <div class="chips" role="group" aria-label="Filter by category">{btns}</div>
</div>
<p id="count" class="count"></p>
<div class="grid" id="grid">
{chr(10).join(cards)}
</div>
<p id="empty" class="empty" hidden>No recipes match. Try another word.</p>
<p class="originals">Original site pages: <a href="pdfs/original-home-page.pdf">Home</a> &middot; <a href="pdfs/original-about-us.pdf">About Us</a> &middot; <a href="pdfs/original-gallery.pdf">Gallery</a></p>
</main>
<script>
(function(){{
  var q=document.getElementById('q'),cards=[].slice.call(document.querySelectorAll('.card')),
      chips=[].slice.call(document.querySelectorAll('.chip')),cat='all',
      count=document.getElementById('count'),empty=document.getElementById('empty');
  function apply(){{
    var t=q.value.trim().toLowerCase().split(/\\s+/).filter(Boolean),n=0;
    cards.forEach(function(c){{
      var ok=(cat==='all'||c.dataset.cat===cat)&&t.every(function(w){{return c.dataset.search.indexOf(w)>-1;}});
      c.hidden=!ok; if(ok)n++;
    }});
    count.textContent=n+(n===1?' recipe':' recipes'); empty.hidden=n>0;
  }}
  chips.forEach(function(b){{b.addEventListener('click',function(){{
    chips.forEach(function(x){{x.classList.remove('active');}}); b.classList.add('active'); cat=b.dataset.cat; apply();
  }});}});
  q.addEventListener('input',apply); apply();
}})();
</script>
''' + footer("")


def main():
    recipes = load()
    os.makedirs(os.path.join(ROOT, "recipes"), exist_ok=True)
    for r in recipes:
        with open(os.path.join(ROOT, "recipes", r["slug"] + ".html"), "w", encoding="utf-8") as fh:
            fh.write(recipe_page(r))
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as fh:
        fh.write(index_page(recipes))
    print(f"Built {len(recipes)} recipes.")


if __name__ == "__main__":
    main()
