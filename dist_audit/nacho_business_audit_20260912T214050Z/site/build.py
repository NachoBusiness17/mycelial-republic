#!/usr/bin/env python3
"""build.py — the estuary shore. Converts the onboard kit + stack + thesis to a
static, curated, READ-ONLY site. No fleet internals, no live organs, no secrets.
Re-run after editing any source: python site/build.py
"""
import markdown, os, shutil, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
OUT = ROOT / "site" / "dist"
SRC = ROOT / "site"

PAGES = [
    # (source md, out path, title)
    ("watch/onboard/STORY.md", "index.html", "Nacho Business — a sovereign fleet, built in the open"),
    ("watch/onboard/WELCOME.md", "onboard/index.html", "Welcome — start here"),
    ("watch/onboard/ORIENT.md", "onboard/orient.html", "Orientation"),
    ("watch/onboard/GAMEBOOK.md", "onboard/gamebook.html", "The Gamebook"),
    ("watch/onboard/GLOSSARY.md", "onboard/glossary.html", "Glossary"),
    ("watch/onboard/GUEST_PROTOCOL.md", "onboard/guest-protocol.html", "Guest Protocol"),
    ("watch/onboard/FAQ.md", "onboard/faq.html", "FAQ"),
    ("watch/onboard/FIRST_WEEK.md", "onboard/first-week.html", "Your First Week"),
    ("docs/ref/STACK_V1.md", "stack.html", "The Stack, v1"),
    ("watch/THE_STONE_THESIS_20260911.md", "thesis.html", "The Stone Thesis"),
    ("LETTER_ADAM_CRIGLER.md", "letter.html", "For Adam — from the machine room"),
]
GAMES = ["maze_arena.html", "arrakis.html", "arena_operator_field.html", "mud.html", "swarm.html"]

CSS = """*{box-sizing:border-box}body{margin:0;background:#0d0f12;color:#d6d3cb;
font:17px/1.65 Georgia,'Times New Roman',serif;padding:0 0 4em}
main{max-width:46rem;margin:0 auto;padding:1.2rem}
h1,h2,h3,h4{font-family:'Segoe UI',system-ui,sans-serif;color:#f0ede5;line-height:1.25}
h1{font-size:1.7em;margin-top:1.6em}h2{font-size:1.25em;margin-top:1.8em;border-bottom:1px solid #2a2e35;padding-bottom:.25em}
a{color:#8ab4f8;text-decoration:none}a:hover{text-decoration:underline}
blockquote{margin:1em 0;padding:.4em 1em;border-left:3px solid #8a7a4a;color:#bdb9ae;background:#14171c}
code{font-family:Consolas,monospace;font-size:.85em;background:#1a1e24;padding:.1em .35em;border-radius:3px}
pre{background:#14171c;padding:.8em;overflow-x:auto;border-radius:4px}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #2a2e35;padding:.35em .6em;text-align:left}
hr{border:none;border-top:1px solid #2a2e35;margin:2em 0}
nav{font-family:'Segoe UI',system-ui,sans-serif;font-size:.92em;background:#101318;border-bottom:1px solid #2a2e35;padding:.7em 1rem}
nav .in{max-width:46rem;margin:0 auto;display:flex;gap:1.1em;flex-wrap:wrap}
nav a{color:#bdb9ae}nav a.home{color:#f0ede5;font-weight:600}
footer{max-width:46rem;margin:3em auto 0;padding:1em 1.2rem;border-top:1px solid #2a2e35;color:#6f6b62;font-size:.85em}
.md h1:first-child{margin-top:.4em}li{margin:.3em 0}"""

NAV = """<nav><div class="in"><a class="home" href="/index.html">Nacho Business</a>
<a href="/letter.html">For Adam</a><a href="/onboard/index.html">Start here</a>
<a href="/onboard/gamebook.html">The game</a>
<a href="/onboard/glossary.html">Glossary</a><a href="/stack.html">The stack</a>
<a href="/thesis.html">Stone thesis</a><a href="/games/maze_arena.html">Games</a>
<a href="/onboard/faq.html">FAQ</a></div></nav>"""
FOOT = """<footer>Signed record first, this mirror second. Curated, read-only, built in the open.
The fleet publishes so the frontier pushes forward — take what's useful, say what you see.
<br>estuary shore v0 · {date}</footer>"""

def page(body_html, title):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{CSS}</style></head>
<body>{NAV}<main class="md">{body_html}</main>{FOOT}</body></html>"""

def main():
    if OUT.exists(): shutil.rmtree(OUT)
    (OUT / "onboard").mkdir(parents=True)
    (OUT / "games").mkdir(parents=True)
    md = markdown.Markdown(extensions=["extra", "sane_lists", "toc"])
    for src, out, title in PAGES:
        p = ROOT / src
        if not p.exists():
            print("MISSING:", src); continue
        md.reset()
        html = md.convert(p.read_text(encoding="utf-8"))
        (OUT / out).write_text(page(html, title), encoding="utf-8")
        print("built", out)
    for g in GAMES:
        gp = ROOT / "dashboard" / "static" / g
        if gp.exists():
            shutil.copy(gp, OUT / "games" / g); print("built games/" + g)
    mp3 = ROOT / "dashboard" / "static" / "suno" / "flat_beat_loop.mp3"
    if mp3.exists():
        (OUT / "suno").mkdir(exist_ok=True)
        shutil.copy(mp3, OUT / "suno" / "flat_beat_loop.mp3"); print("built suno/flat_beat_loop.mp3")
    print("dist ready:", OUT)

if __name__ == "__main__":
    main()
