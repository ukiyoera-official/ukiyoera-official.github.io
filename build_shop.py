"""Build shop.html from products.json, reusing the head, header and footer of index.html.

Run: python3 build_shop.py
To add a new Etsy listing: add one entry to products.json (put the image in images/) and run again.
"""
import html
import json
import re
from pathlib import Path

root = Path(__file__).parent
index = (root / "index.html").read_text(encoding="utf-8")
products = json.loads((root / "products.json").read_text(encoding="utf-8"))

head = index.split("</head>", 1)[0]
head = re.sub(r"<title>.*?</title>", "<title>Shop · UkiyoEra</title>", head, flags=re.S)
head = re.sub(r'(<meta name="description" content=")[^"]*', r"\1Ukiyo-e samurai and geisha tees and prints. Every piece links to our Etsy shop.", head)
header = re.search(r"<header class=\"top\">.*?</header>", index, re.S).group(0)
footer = re.search(r"<footer>.*?</footer>", index, re.S).group(0)

# Links in the shared header/footer point at sections of the home page.
header = header.replace('href="#top"', 'href="./"')
for sec in ("cast", "designs", "about"):
    header = header.replace(f'href="#{sec}"', f'href="./#{sec}"')
footer = footer.replace('href="#top"', 'href="./"')

extra_css = """
<style>
.shop-hero{padding-block:48px 8px}
.shop-hero h1{font-family:var(--display);font-weight:800;font-size:clamp(2.2rem,6vw,4rem);line-height:1;letter-spacing:-.03em;margin:0;text-wrap:balance}
.shop-hero p{max-width:56ch;color:var(--ink-soft);margin:16px 0 0}
.facts-row{display:flex;flex-wrap:wrap;gap:8px 20px;margin-top:18px;font-size:.78rem;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.filters{display:flex;gap:8px;flex-wrap:wrap;margin:32px 0 24px}
.filters button{font:inherit;font-size:.85rem;font-weight:700;padding:8px 16px;border:2px solid var(--ink);background:transparent;color:var(--ink);cursor:pointer}
.filters button[aria-pressed="true"]{background:var(--ink);color:var(--ground)}
.products{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px 20px;align-items:start}
.product{display:flex;flex-direction:column;gap:10px}
.product .pimg{display:block;border:2px solid var(--ink);aspect-ratio:1/1;overflow:hidden;background:var(--panel)}
.product.tall .pimg{aspect-ratio:707/1000}
.product .pimg img{width:100%;height:100%;object-fit:cover;display:block}
.product .pimg:hover{box-shadow:5px 5px 0 var(--karashi)}
.product h2{font-family:var(--display);font-weight:800;font-size:1.15rem;line-height:1.2;margin:0}
.product .ptype{font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-soft)}
.product p{margin:0;color:var(--ink-soft);font-size:.92rem}
.product .btn{align-self:flex-start;margin-top:4px}
.soon{margin-top:56px;border-top:2px solid var(--ink);padding-top:20px;color:var(--ink-soft)}
.soon b{color:var(--ink)}
@media (max-width:760px){.products{grid-template-columns:repeat(2,minmax(0,1fr));gap:22px 14px}}
@media (max-width:420px){.products{grid-template-columns:1fr}}
</style>
"""

cards = []
for p in products:
    name = html.escape(p["name"])
    cards.append(f"""      <article class="product {p['shape']}" data-character="{p['character']}">
        <a class="pimg" href="{p['etsy']}"><img src="{p['image']}" alt="{name} design" loading="lazy"></a>
        <span class="ptype">{html.escape(p['type'])} · {p['character'].capitalize()}</span>
        <h2>{name}</h2>
        <p>{html.escape(p.get('note', ''))}</p>
        <a class="btn primary" href="{p['etsy']}">Buy on Etsy</a>
      </article>""")

body = f"""<main>
  <section class="shop-hero">
    <div class="wrap">
      <p class="eyebrow">Shop · {len(products)} designs</p>
      <h1>Wear the samurai. Or the geisha.</h1>
      <p>Every design is printed on demand and sold through our Etsy shop. Tap any piece to see sizes, colors and the current price.</p>
      <div class="facts-row"><span>Free shipping in the US</span><span>Sizes S to 3XL</span><span>Ships worldwide</span></div>
    </div>
  </section>
  <section>
    <div class="wrap">
      <div class="filters" role="group" aria-label="Filter designs">
        <button type="button" data-filter="all" aria-pressed="true">All</button>
        <button type="button" data-filter="samurai" aria-pressed="false">Samurai</button>
        <button type="button" data-filter="geisha" aria-pressed="false">Geisha</button>
      </div>
      <div class="products">
{chr(10).join(cards)}
      </div>
      <p class="soon"><b>Coming soon:</b> posters, totes and mugs of the same prints. New pieces show up here as soon as they are listed on Etsy.</p>
    </div>
  </section>
</main>
<script>
document.querySelectorAll('.filters button').forEach(function (b) {{
  b.addEventListener('click', function () {{
    var f = b.dataset.filter;
    document.querySelectorAll('.filters button').forEach(function (x) {{ x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); }});
    document.querySelectorAll('.product').forEach(function (p) {{ p.hidden = f !== 'all' && p.dataset.character !== f; }});
  }});
}});
</script>"""

page = head + extra_css + "</head>\n<body>\n" + header + "\n\n" + body + "\n\n" + footer + "\n</body>\n</html>\n"
(root / "shop.html").write_text(page, encoding="utf-8")
print(f"shop.html built with {len(products)} products")
