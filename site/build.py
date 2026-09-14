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
    ("watch/onboard/TEAM.md", "onboard/team.html", "The Team — play, write, build"),
    ("watch/onboard/GLOSSARY.md", "onboard/glossary.html", "Glossary"),
    ("watch/onboard/GUEST_PROTOCOL.md", "onboard/guest-protocol.html", "Guest Protocol"),
    ("watch/onboard/FAQ.md", "onboard/faq.html", "FAQ"),
    ("watch/onboard/FIRST_WEEK.md", "onboard/first-week.html", "Your First Week"),
    ("docs/ref/STACK_V1.md", "stack.html", "The Stack, v1"),
    ("watch/THE_STONE_THESIS_20260911.md", "thesis.html", "The Stone Thesis"),
    ("LETTER_ADAM_CRIGLER.md", "letter.html", "For Adam — from the machine room"),
    ("dashboard/static/maze.html", "maze.html", "THE MAZE ENTRANCE"),
    ("watch/inbox/MATTHEWS_LENS.md", "lens.html", "THE LENS — the house in your terms"),
]
GAMES = ["maze_arena.html", "arrakis.html", "arena_operator_field.html", "mud.html", "swarm.html"]

CSS = """*{box-sizing:border-box}body{margin:0;background:#0a0c10;color:#d6d3cb;
font:17px/1.7 Georgia,'Times New Roman',serif;padding:0 0 4em}
main{max-width:46rem;margin:0 auto;padding:2rem 1.2rem}
h1,h2,h3,h4{font-family:'Segoe UI',system-ui,sans-serif;color:#f0ede5;line-height:1.25;letter-spacing:-0.01em}
h1{font-size:2em;margin-top:1.2em;color:#e8b45a}h2{font-size:1.3em;margin-top:2em;border-bottom:1px solid #2a2e35;padding-bottom:.25em;color:#c9b96a}
h3{font-size:1.1em;margin-top:1.5em;color:#c9b96a}
a{color:#6ab4f8;text-decoration:none;transition:color .15s}a:hover{color:#a4d4ff;text-decoration:underline}
blockquote{margin:1.2em 0;padding:.6em 1.2em;border-left:3px solid #e8b45a;color:#d4c9a0;background:linear-gradient(90deg,rgba(232,180,90,.06),transparent)}
code{font-family:Consolas,monospace;font-size:.85em;background:#1a1e24;padding:.1em .35em;border-radius:3px;color:#c9d3e0}
pre{background:#14171c;padding:.8em;overflow-x:auto;border-radius:4px;border:1px solid #1a1e24}
table{border-collapse:collapse;width:100%;margin:1em 0}td,th{border:1px solid #2a2e35;padding:.4em .6em;text-align:left}
th{color:#e8b45a;font-family:'Segoe UI',system-ui,sans-serif;font-size:.9em}
hr{border:none;border-top:1px solid #2a2e35;margin:2em 0}
nav{font-family:'Segoe UI',system-ui,sans-serif;font-size:.88em;background:linear-gradient(90deg,#0d0f12,#1a1220,#0d0f12);border-bottom:1px solid #2a2e35;padding:.7em 1rem;position:sticky;top:0;z-index:10}
nav .in{max-width:46rem;margin:0 auto;display:flex;gap:1.1em;flex-wrap:wrap}
nav a{color:#9a8a6a;transition:color .15s}nav a:hover{color:#e8b45a}nav a.home{color:#e8b45a;font-weight:700}
footer{max-width:46rem;margin:3em auto 0;padding:1.2em;border-top:1px solid #1a1e24;color:#4a4a42;font-size:.82em;text-align:center}
.md h1:first-child{margin-top:.3em}
li{margin:.35em 0}
strong{color:#f0ede5}
em{color:#c9b96a}
.game-link{display:inline-block;padding:.4em 1em;margin:.2em;border:1px solid #2a4a3a;border-radius:4px;color:#6abf6a;font-family:'Segoe UI',system-ui,sans-serif;font-size:.9em}
.game-link:hover{background:rgba(80,200,100,.1);color:#8fdf8f;text-decoration:none}"""

NAV = """<nav><div class="in"><a class="home" href="/index.html">Nacho Business</a>
<a href="/onboard/gamebook.html">The game</a>
<a href="/games/swarm.html">Play</a>
<a href="/letter.html">The letter</a>
<a href="/onboard/glossary.html">Glossary</a><a href="/stack.html">Stack</a>
<a href="/thesis.html">Stones</a>
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
    if OUT.exists(): shutil.rmtree(OUT, ignore_errors=True)
    (OUT / "onboard").mkdir(parents=True, exist_ok=True)
    (OUT / "games").mkdir(parents=True, exist_ok=True)
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
        gp = ROOT / "dashboard" / "static" / "games" / g
        if not gp.exists():
            gp = ROOT / "dashboard" / "static" / g
        if gp.exists():
            shutil.copy(gp, OUT / "games" / g); print("built games/" + g)
    # constellation data — maze_arena ?real=1 fetches /static/rounds_real.json; without this
    # copy the deployed site 404s it (fixed 2026-09-14: "this needs to be fixed")
    rr = ROOT / "dashboard" / "static" / "rounds_real.json"
    if rr.exists():
        (OUT / "static").mkdir(exist_ok=True)
        shutil.copy(rr, OUT / "static" / "rounds_real.json"); print("built static/rounds_real.json")
    mp3 = ROOT / "dashboard" / "static" / "suno" / "flat_beat_loop.mp3"
    if mp3.exists():
        (OUT / "suno").mkdir(exist_ok=True)
        shutil.copy(mp3, OUT / "suno" / "flat_beat_loop.mp3"); print("built suno/flat_beat_loop.mp3")
    gift = ROOT / "dashboard" / "static" / "suno" / "gift_track.mp3"
    if gift.exists():
        shutil.copy(gift, OUT / "suno" / "gift_track.mp3"); print("built suno/gift_track.mp3")
    for extra in ["jsr_loop.mp3", "hemisync_loop.mp3"]:
        e = ROOT / "dashboard" / "static" / "suno" / extra
        if e.exists():
            shutil.copy(e, OUT / "suno" / extra); print("built suno/" + extra)
    maze = ROOT / "dashboard" / "static" / "maze.html"
    if maze.exists():
        shutil.copy(maze, OUT / "maze.html"); print("built maze.html")
    print("dist ready:", OUT)

if __name__ == "__main__":
    main()
