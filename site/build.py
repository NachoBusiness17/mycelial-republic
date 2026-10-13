#!/usr/bin/env python3
"""build.py — the estuary shore. Converts the onboard kit + stack + thesis to a
static, curated, READ-ONLY site. No fleet internals, no live organs, no secrets.
Re-run after editing any source: python site/build.py
"""
import markdown, os, shutil, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent  # repo root
OUT = ROOT / "site" / "dist"
SRC = ROOT / "site"

PAGES = [
    # (source md, out path, title)
    ("watch/onboard/STORY.md", "index.html", "Nacho Business — a sovereign fleet, built in the open"),
    ("watch/onboard/WORK_WITH_ME.md", "work.html", "Work with me — verified receipts, shipped things"),
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
GAMES = ["maze_arena.html", "arrakis.html", "arena_operator_field.html", "mud.html", "swarm.html", "toy.html", "frontier_souls.html",
         "shadowbonk.html", "wipeout_v2.html", "wipeout_sunset.html", "wipeout_lightmaze.html", "spectral_maze.html",
         "shadow_walk.html", "eraser_maze.html", "universe_within.html", "worldline_dungeon.html", "tavern_brawl.html",
         "calabi_yau.html", "chaos_refract.html", "phase_particles.html", "bad_apple_field.html", "mesh_gallery.html"]

CSS = """*{box-sizing:border-box}body{margin:0;background:#0B0E14;color:#E7EAF2;
font:17px/1.7 Georgia,'Times New Roman',serif;padding:0 0 4em}
main{max-width:46rem;margin:0 auto;padding:2rem 1.2rem}
h1,h2,h3,h4{font-family:'Segoe UI',system-ui,sans-serif;color:#f0ede5;line-height:1.25;letter-spacing:-0.01em}
h1{font-size:2em;margin-top:1.2em;color:#8B95FF}h2{font-size:1.3em;margin-top:2em;border-bottom:1px solid #242C3C;padding-bottom:.25em;color:#A5B4FF}
h3{font-size:1.1em;margin-top:1.5em;color:#A5B4FF}
a{color:#7AA5FF;text-decoration:none;transition:color .15s}a:hover{color:#AFC6FF;text-decoration:underline}
blockquote{margin:1.2em 0;padding:.6em 1.2em;border-left:3px solid #8B95FF;color:#B9C2E8;background:linear-gradient(90deg,rgba(139,149,255,.06),transparent)}
code{font-family:Consolas,monospace;font-size:.85em;background:#1F2633;padding:.1em .35em;border-radius:3px;color:#c9d3e0}
pre{background:#14171c;padding:.8em;overflow-x:auto;border-radius:4px;border:1px solid #1F2633}
table{border-collapse:collapse;width:100%;margin:1em 0}td,th{border:1px solid #242C3C;padding:.4em .6em;text-align:left}
th{color:#8B95FF;font-family:'Segoe UI',system-ui,sans-serif;font-size:.9em}
hr{border:none;border-top:1px solid #242C3C;margin:2em 0}
nav{font-family:'Segoe UI',system-ui,sans-serif;font-size:.88em;background:linear-gradient(90deg,#0B0E14,#141B2E,#0B0E14);border-bottom:1px solid #242C3C;padding:.7em 1rem;position:sticky;top:0;z-index:10}
nav .in{max-width:46rem;margin:0 auto;display:flex;gap:1.1em;flex-wrap:wrap}
nav a{color:#9a8a6a;transition:color .15s}nav a:hover{color:#8B95FF}nav a.home{color:#8B95FF;font-weight:700}
footer{max-width:46rem;margin:3em auto 0;padding:1.2em;border-top:1px solid #1F2633;color:#4a4a42;font-size:.82em;text-align:center}
.md h1:first-child{margin-top:.3em}
li{margin:.35em 0}
strong{color:#f0ede5}
em{color:#A5B4FF}
.game-link{display:inline-block;padding:.4em 1em;margin:.2em;border:1px solid #2a4a3a;border-radius:4px;color:#6abf6a;font-family:'Segoe UI',system-ui,sans-serif;font-size:.9em}
.game-link:hover{background:rgba(80,200,100,.1);color:#8fdf8f;text-decoration:none}"""

NAV = """<nav><div class="in"><a class="home" href="/index.html">Nacho Business</a>
<a href="/work.html" style="color:#8B95FF;font-weight:600">Work with me</a>
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

WORK_CSS = """*{box-sizing:border-box}
html{scroll-behavior:smooth;scroll-snap-type:y proximity}
body{margin:0;background:#07090B;color:#E7EAF2;font:16px/1.65 'Segoe UI',system-ui,-apple-system,sans-serif}
body::after{content:"";position:fixed;inset:0;z-index:2;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(255,255,255,.016) 0 1px,transparent 1px 3px)}
canvas.shader{position:fixed;inset:0;width:100vw;height:100vh;z-index:0}
a{color:#7AA5FF;text-decoration:none}a:hover{color:#AFC6FF}
.room{min-height:100vh;scroll-snap-align:start;position:relative;z-index:1;display:flex;align-items:center;padding:5.2rem 0 3.6rem;border-bottom:1px solid rgba(255,255,255,.045)}
.room .inner{width:100%;max-width:1120px;margin:0 auto;padding:0 1.4rem}
.plate{display:block;font-family:ui-monospace,Consolas,monospace;text-transform:uppercase;letter-spacing:.14em;color:#8B95FF;font-size:.78rem;margin-bottom:1.1rem}
.plate .no{color:#3ED6C4}
h1.hero-h{font-size:clamp(2rem,5vw,3.4rem);line-height:1.08;color:#F2F4F8;margin:0 0 .8rem;letter-spacing:-.02em}
h1.hero-h em{font-style:normal;color:#8B95FF}
h2.room-h{font-size:clamp(1.5rem,3.4vw,2.4rem);line-height:1.15;color:#F2F4F8;margin:0 0 1.1rem;letter-spacing:-.015em}
h2.room-h .n{color:#3ED6C4;font-family:ui-monospace,Consolas,monospace;font-size:.8em;margin-right:.5em}
.sub{font-size:1.1rem;color:#A3ABBD;max-width:46rem;margin:0 0 1.5rem}
.cta-row{display:flex;gap:.8rem;flex-wrap:wrap;align-items:center}
.btn{display:inline-block;padding:.72em 1.45em;border-radius:8px;font-weight:600;font-size:.96rem;border:1px solid transparent}
.btn.gold{background:linear-gradient(135deg,#6D7CFF,#37D5D0);color:#fff}.btn.gold:hover{filter:brightness(1.14)}
.btn.line{border-color:#242C3C;color:#cfd6e2}.btn.line:hover{border-color:#7AA5FF;color:#AFC6FF}
.stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.9rem;margin:2.2rem 0 0}
.stat{background:rgba(12,15,20,.72);border:1px solid #1F2633;border-radius:10px;padding:1rem 1.1rem;backdrop-filter:blur(4px)}
.stat b{display:block;font-size:1.45rem;color:#3ED6C4;letter-spacing:-.01em}
.stat span{font-size:.82rem;color:#8A93A6}
.hint{margin-top:1.4rem;font-family:ui-monospace,Consolas,monospace;font-size:.78rem;color:#8A93A6;animation:pulse 2.4s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:.55}50%{opacity:1}}
@media(prefers-reduced-motion:reduce){.hint{animation:none}}
.door{display:flex;justify-content:space-between;align-items:center;margin-top:2.4rem;font-family:ui-monospace,Consolas,monospace;font-size:.82rem;text-transform:uppercase;letter-spacing:.1em}
.door a{color:#3ED6C4}.door a:hover{color:#7FF2E2}
.door .back{color:#6E7686}.door .back:hover{color:#AFC6FF}
.frame-outer{width:min(1200px,94vw);margin:0 auto;background:#0c0f14;border:1px solid #1F2633;border-radius:12px;overflow:hidden}
.frame-bar{display:flex;gap:.45rem;align-items:center;padding:.55rem .9rem;background:#10141B;border-bottom:1px solid #1F2633;font-family:ui-monospace,Consolas,monospace;font-size:.76rem;color:#8A93A6}
.dot{width:.6rem;height:.6rem;border-radius:50%;background:#242C3C}.dot.g{background:#3f8f5f}
.frame-outer iframe{display:block;width:100%;border:0;background:#05060a;aspect-ratio:16/9}
.bubble-row{display:grid;grid-template-columns:repeat(3,1fr);gap:.9rem;margin-top:1rem;width:min(1200px,94vw);margin-left:auto;margin-right:auto}
@media(max-width:900px){.bubble-row{grid-template-columns:1fr}}
.bubble{background:rgba(12,15,20,.78);border:1px solid #1F2633;border-radius:10px;padding:1rem 1.1rem;backdrop-filter:blur(4px)}
.bubble b{color:#F2F4F8}
.bubble p{margin:.35rem 0 0;font-size:.9rem;color:#A3ABBD}
.arcade-cta{background:linear-gradient(90deg,rgba(109,124,255,.12),rgba(55,213,208,.10));border:1px solid rgba(109,124,255,.3);border-radius:10px;padding:1rem 1.1rem}
.arcade-cta b{color:#8B95FF}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #1F2633;padding:.55em .75em;text-align:left;font-size:.93rem}
th{color:#3ED6C4;font-family:ui-monospace,Consolas,monospace;font-size:.82rem;text-transform:uppercase;letter-spacing:.08em;background:rgba(16,20,27,.85)}
td{color:#C6CBD8}td b{color:#F2F4F8}
tr td:first-child{color:#F2F4F8;font-weight:600}
.fresh{background:rgba(12,15,20,.78);border:1px solid #1F2633;border-radius:12px;padding:1.4rem 1.5rem;backdrop-filter:blur(4px)}
.fresh ul{margin:.6rem 0 0;padding-left:1.2rem}
.fresh li{margin:.5rem 0;color:#C6CBD8}
.fresh li b{color:#F2F4F8}
.date-pill{float:right;font-size:.75rem;color:#8A93A6;border:1px solid #242C3C;border-radius:999px;padding:.15em .8em;font-family:ui-monospace,Consolas,monospace}
.pills{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0 0}
.pill{font-size:.82rem;color:#cfd6e2;background:rgba(16,20,27,.85);border:1px solid #242C3C;border-radius:999px;padding:.35em .9em}
.hud{position:fixed;left:1rem;bottom:1rem;z-index:30;font-family:ui-monospace,Consolas,monospace;font-size:.74rem;color:#A3ABBD;background:rgba(7,9,11,.85);border:1px solid #1F2633;border-radius:8px;padding:.5rem .85rem;backdrop-filter:blur(6px)}
.hud b{color:#3ED6C4}
.hud a{color:#8B95FF}
.map{position:fixed;right:1rem;bottom:1rem;z-index:30;background:rgba(7,9,11,.85);border:1px solid #1F2633;border-radius:8px;padding:.7rem .6rem;backdrop-filter:blur(6px);display:flex;flex-direction:column;gap:.45rem;align-items:center}
.map .mn{width:.7rem;height:.7rem;border-radius:50%;background:#242C3C;border:1px solid #2E3850;display:block}
.map .mn.on{background:#3ED6C4;border-color:#3ED6C4;box-shadow:0 0 8px rgba(62,214,196,.7)}
.map .link{width:1px;height:.5rem;background:#1F2633}
.gate{min-height:80vh}
.gate .inner{text-align:center}
.gate h2{font-size:clamp(1.7rem,4vw,2.6rem);color:#F2F4F8;margin:0 0 .6rem}
nav.top{position:fixed;top:0;left:0;right:0;z-index:40;background:rgba(7,9,11,.86);backdrop-filter:blur(8px);border-bottom:1px solid rgba(255,255,255,.06)}
nav.top .in{max-width:1120px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;padding:.75rem 1.4rem}
nav.top a{font-family:ui-monospace,Consolas,monospace;font-size:.8rem;text-transform:uppercase;letter-spacing:.1em;color:#A3ABBD}
nav.top a:hover{color:#E7EAF2}
nav.top .brand{color:#F2F4F8;font-weight:600;font-size:.9rem}
nav.top .cta{color:#3ED6C4;border:1px solid rgba(62,214,196,.4);border-radius:6px;padding:.35em .8em}"""
_LEGACY_CSS_UNUSED = """*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:#0B0E14;color:#E7EAF2;font:16px/1.65 'Segoe UI',system-ui,-apple-system,sans-serif}
a{color:#7AA5FF;text-decoration:none}a:hover{color:#AFC6FF}
.wrap{max-width:1080px;margin:0 auto;padding:0 1.4rem}
header.hero{position:relative;overflow:hidden;background:radial-gradient(1200px 500px at 70% -10%,rgba(109,124,255,.13),transparent),radial-gradient(900px 420px at 10% 110%,rgba(55,213,208,.10),transparent),#0B0E14;border-bottom:1px solid #1F2633;padding:4.2rem 0 3.2rem}
canvas.shader{position:absolute;inset:0;width:100%;height:100%;z-index:0}
header.hero .wrap{position:relative;z-index:1}
.kicker{display:inline-block;font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:#3ED6C4;border:1px solid rgba(62,214,196,.35);border-radius:999px;padding:.3em .9em;margin-bottom:1.3rem;background:rgba(62,214,196,.06)}
h1.hero-h{font-size:clamp(1.9rem,4.4vw,3rem);line-height:1.12;color:#f0ede5;margin:0 0 .7rem;letter-spacing:-.02em}
h1.hero-h em{font-style:normal;color:#8B95FF}
.sub{font-size:1.12rem;color:#a9a598;max-width:44rem;margin:0 0 1.6rem}
.cta-row{display:flex;gap:.8rem;flex-wrap:wrap;align-items:center}
.btn{display:inline-block;padding:.75em 1.5em;border-radius:8px;font-weight:600;font-size:.98rem;border:1px solid transparent}
.btn.gold{background:linear-gradient(135deg,#6D7CFF,#37D5D0);color:#fff}.btn.gold:hover{filter:brightness(1.12)}
.btn.line{border-color:#242C3C;color:#cfd6e2}.btn.line:hover{border-color:#7AA5FF;color:#AFC6FF}
.stat-row{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:.9rem;margin:2.6rem 0 0}
.stat{background:#0c0f14;border:1px solid #1F2633;border-radius:10px;padding:1rem 1.1rem}
.stat b{display:block;font-size:1.45rem;color:#3ED6C4;font-family:'Segoe UI',system-ui,sans-serif;letter-spacing:-.01em}
.stat span{font-size:.82rem;color:#8f8b80}
section{padding:3.2rem 0;border-bottom:1px solid #14181f}
section:last-of-type{border-bottom:none}
h2{font-size:1.5rem;color:#f0ede5;margin:0 0 1.2rem;letter-spacing:-.01em}
h2 .n{color:#8B95FF;font-family:Consolas,monospace;font-size:.85em;margin-right:.5em}
h3{color:#A5B4FF;font-size:1.05rem;margin:1.6rem 0 .6rem}
.play-grid{display:grid;grid-template-columns:1.25fr 1fr;gap:1.2rem;align-items:stretch}
@media(max-width:820px){.play-grid{grid-template-columns:1fr}}
.frame{background:#0c0f14;border:1px solid #1F2633;border-radius:12px;overflow:hidden;display:flex;flex-direction:column}
.frame .bar{display:flex;gap:.45rem;align-items:center;padding:.55rem .9rem;background:#10141b;border-bottom:1px solid #1F2633;font-size:.78rem;color:#8f8b80}
.dot{width:.6rem;height:.6rem;border-radius:50%;background:#242C3C}.dot.g{background:#3f8f5f}
.frame iframe{flex:1;width:100%;border:0;background:#05060a;min-height:460px;aspect-ratio:16/9.6}
.play-side{display:flex;flex-direction:column;gap:.9rem}
.play-card{background:#0c0f14;border:1px solid #1F2633;border-radius:10px;padding:1rem 1.1rem}
.play-card b{color:#f0ede5}
.play-card p{margin:.35rem 0 0;font-size:.9rem;color:#9a968a}
.arcade-cta{margin-top:auto;background:linear-gradient(90deg,rgba(139,149,255,.10),rgba(106,180,248,.08));border:1px solid rgba(139,149,255,.3);border-radius:10px;padding:1rem 1.1rem}
.arcade-cta b{color:#8B95FF}
.receipts{display:grid;grid-template-columns:1fr 1fr;gap:.9rem}
@media(max-width:760px){.receipts{grid-template-columns:1fr}}
.receipt{background:#0c0f14;border:1px solid #1F2633;border-radius:10px;padding:1rem 1.1rem;display:flex;gap:.9rem}
.receipt .v{font-family:Consolas,monospace;color:#3ED6C4;font-size:1.02rem;min-width:5.2em}
.receipt .k{font-size:.9rem;color:#b9b5a8}
.fresh{background:linear-gradient(180deg,#0d1017,#0c0f14);border:1px solid #1F2633;border-radius:12px;padding:1.4rem 1.5rem}
.fresh ul{margin:.6rem 0 0;padding-left:1.2rem}
.fresh li{margin:.45rem 0;color:#c5c1b4}
.fresh li b{color:#f0ede5}
.date-pill{float:right;font-size:.75rem;color:#8f8b80;border:1px solid #232a35;border-radius:999px;padding:.15em .8em}
table{border-collapse:collapse;width:100%}td,th{border:1px solid #1F2633;padding:.5em .7em;text-align:left;font-size:.92rem}th{color:#8B95FF;font-weight:600;background:#10141b}
.pills{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0 0}
.pill{font-size:.82rem;color:#cfd6e2;background:#10141b;border:1px solid #232a35;border-radius:999px;padding:.35em .9em}
.contact{background:radial-gradient(900px 400px at 50% 130%,rgba(139,149,255,.12),transparent),#0B0E14;text-align:center;padding:3.6rem 0}
.contact h2{font-size:1.7rem}"""

WORK_NAV = """<nav class="top"><div class="in"><a class="brand" href="/index.html">Nacho Business</a><div style="display:flex;gap:1.4rem;flex-wrap:wrap;align-items:center"><a href="#play">Play</a><a href="#receipts">Ledger</a><a href="#fresh">Fresh</a><a href="#craft">Craft</a><a class="cta" href="mailto:nachobusinesscorp@gmail.com">Work with me</a></div></div></nav>"""

WALKER_JS = """(function () {
  const rooms = [].slice.call(document.querySelectorAll('.room'));
  const hud = document.getElementById('hud');
  const nodes = [].slice.call(document.querySelectorAll('.map .mn'));
  let cur = 0, lock = 0;
  function paint(i) {
    if (hud) hud.innerHTML = '<b>ROOM ' + (i + 1) + '/' + rooms.length + '</b> · ' +
      (rooms[i].dataset.name || '') +
      ' · walk with ↑/↓ · <a href="mailto:nachobusinesscorp@gmail.com">reach the gate ↗</a>';
    nodes.forEach(function (n, j) { n.classList.toggle('on', j === i); });
  }
  function set(i) {
    i = Math.max(0, Math.min(rooms.length - 1, i));
    cur = i;
    lock = Date.now() + 1100;
    rooms[i].scrollIntoView({ behavior: 'smooth', block: 'start' });
    paint(i);
  }
  window.addEventListener('keydown', function (e) {
    if (e.target && /INPUT|TEXTAREA/.test(e.target.tagName)) return;
    const k = e.key;
    if (k === 'ArrowDown' || k === 'PageDown' || k === 'j') { e.preventDefault(); set(cur + 1); }
    else if (k === 'ArrowUp' || k === 'PageUp' || k === 'k') { e.preventDefault(); set(cur - 1); }
  });
  nodes.forEach(function (n, i) {
    n.addEventListener('click', function (ev) { ev.preventDefault(); set(i); });
  });
  setInterval(function () {
    if (Date.now() < lock) return;
    const mid = window.scrollY + window.innerHeight / 2;
    let best = 0;
    rooms.forEach(function (r, i) { if (mid >= r.offsetTop) best = i; });
    if (best !== cur) { cur = best; paint(best); }
  }, 220);
  paint(0);
})();"""

ROOMS = [("top", "THE BEACON"), ("play", "PLAY THE PROOF"), ("receipts", "THE LEDGER"),
         ("fresh", "FRESH RECEIPTS"), ("craft", "THE CRAFT"), ("gate", "THE GATE")]
MINIMAP = '<div class="map" title="you are here — the eigen-map">' + "".join(
    ('<a class="mn" href="#%s" title="%s"></a>' % (rid, name)) + ('<div class="link"></div>' if rid != ROOMS[-1][0] else "")
    for rid, name in ROOMS) + "</div>"

SHADER_JS = """(function () {
  const cv = document.getElementById("bgshader");
  if (!cv) return;
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const gl = cv.getContext("webgl", { antialias: false });
  if (!gl) return;
  const VS = "attribute vec2 p;void main(){gl_Position=vec4(p,0.,1.);}";
  const FS = "precision mediump float;uniform vec2 u_res;uniform float u_t;" +
    "float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}" +
    "float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);" +
    "return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);}" +
    "float fbm(vec2 p){float v=0.,a=.5;for(int i=0;i<5;i++){v+=a*noise(p);p*=2.03;a*=.5;}return v;}" +
    "void main(){vec2 uv=gl_FragCoord.xy/u_res;float t=u_t*.045;" +
    "vec2 q=vec2(fbm(uv*1.9+t),fbm(uv*1.9-t*1.25));" +
    "float n=fbm(uv*2.4+q*1.7);" +
    "vec3 a=vec3(.026,.032,.05);" +
    "vec3 b=vec3(.10,.12,.34);" +
    "vec3 c=vec3(.04,.26,.28);" +
    "vec3 col=a+b*pow(n,2.1)*1.35+c*pow(1.-abs(uv.y-.32),2.6)*.20;" +
    "col+=vec3(.07,.08,.19)*pow(q.y,2.)*.85;" +
    "float vig=smoothstep(1.3,.3,length(uv-vec2(.5,.45)));" +
    "gl_FragColor=vec4(col*vig+a*.3,1.);}";
  function sh(type, src) { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; }
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uRes = gl.getUniformLocation(prog, "u_res");
  const uT = gl.getUniformLocation(prog, "u_t");
  function resize() {
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    const w = Math.max(2, Math.floor(cv.clientWidth * dpr * .5));
    const h = Math.max(2, Math.floor(cv.clientHeight * dpr * .5));
    if (cv.width !== w || cv.height !== h) { cv.width = w; cv.height = h; gl.viewport(0, 0, w, h); }
    gl.uniform2f(uRes, cv.width, cv.height);
  }
  resize();
  window.addEventListener("resize", resize);
  const t0 = performance.now();
  function frame(now) {
    resize();
    gl.uniform1f(uT, (now - t0) / 1000);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    if (!reduced) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
})();"""

def work_page(hero, rest):
    head = ("<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n"
            "<title>Nacho Quixotic — a website you walk. Every claim carries a receipt.</title>\n"
            "<meta name=\"description\" content=\"Multi-agent AI systems, verification tooling, and shipped software — every claim carries a receipt. Walk the beacon.\">\n"
            "<style>" + WORK_CSS + "</style></head><body>")
    gate = ("<section class=\"room gate\" id=\"gate\" data-name=\"THE GATE\"><div class=\"inner\">"
            "<span class=\"plate\">ROOM 6/6 · <span class=\"no\">THE GATE</span></span>"
            "<h2>The checks are real. So is the work.</h2>"
            "<p class=\"sub\" style=\"margin:0 auto 1.6rem\">Every line in every room has a receipt behind it. "
            "Ask to see any of them — I built all of it, and I can show every seam.</p>"
            "<div class=\"cta-row\" style=\"justify-content:center\">"
            "<a class=\"btn gold\" href=\"mailto:nachobusinesscorp@gmail.com\">Email nachobusinesscorp@gmail.com</a>"
            "&nbsp;<a class=\"btn line\" href=\"https://x.com/NachoQuixotic\">DM @NachoQuixotic</a>"
            "&nbsp;<a class=\"btn line\" href=\"/index.html\">Read the constitution</a></div>"
            "<div class=\"door\"><a class=\"back\" href=\"#craft\">↑ BACK: THE CRAFT</a><span></span></div>"
            "</div></section>")
    return (head + WORK_NAV +
            '<canvas class="shader" id="bgshader"></canvas>' +
            '<div id="hud" class="hud"><b>ROOM 1/6</b> · THE BEACON · walk with ↑/↓ · click the game to play</div>' +
            MINIMAP + hero + "<main>" + rest + "</main>" + gate +
            "<footer style=\"position:relative;z-index:1;text-align:center;color:#6E7686;font-size:.78rem;padding:1.4rem 0;border-top:1px solid rgba(255,255,255,.05)\">"
            "estuary shore · a game-as-a-website · built in the open · " + datetime.date.today().isoformat() + "</footer>" +
            "<script>" + SHADER_JS + "</script><script>" + WALKER_JS + "</script></body></html>")

def _legacy_work_page(hero, rest):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Nacho Quixotic — AI systems, measured not demonstrated</title>
<meta name="description" content="Multi-agent AI systems, verification tooling, and shipped software — every claim carries a receipt.">
<style>{WORK_CSS}</style></head><body>
{WORK_NAV}
<header class="hero"><canvas class="shader" id="bgshader"></canvas><div class="wrap">{hero}</div></header>
<main>{rest}</main>
<section class="contact"><div class="wrap"><h2>The checks are real. So is the work.</h2>
<p style="color:#a9a598;max-width:36rem;margin:.8rem auto 1.6rem">Every line on this page has a receipt behind it. Ask to see any of them — I built all of it, and I can show every seam.</p>
<a class="btn gold" href="mailto:nachobusinesscorp@gmail.com">Email nachobusinesscorp@gmail.com</a>
&nbsp;<a class="btn line" href="https://x.com/NachoQuixotic">DM @NachoQuixotic</a>
&nbsp;<a class="btn line" href="/index.html">Read the constitution</a></div></section>
<footer style="text-align:center;color:#6E7686;font-size:.8rem;padding:1.6rem 0;border-top:1px solid #1F2633">estuary shore · built in the open · {datetime.date.today().isoformat()}</footer>
<script>
(function () {{
  const cv = document.getElementById("bgshader");
  if (!cv) return;
  const reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const gl = cv.getContext("webgl", {{ antialias: false }});
  if (!gl) return;
  const VS = "attribute vec2 p;void main(){{gl_Position=vec4(p,0.,1.);}}";
  const FS = "precision mediump float;uniform vec2 u_res;uniform float u_t;" +
    "float hash(vec2 p){{return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}}" +
    "float noise(vec2 p){{vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);" +
    "return mix(mix(hash(i),hash(i+vec2(1.,0.)),f.x),mix(hash(i+vec2(0.,1.)),hash(i+vec2(1.,1.)),f.x),f.y);}}" +
    "float fbm(vec2 p){{float v=0.,a=.5;for(int i=0;i<5;i++){{v+=a*noise(p);p*=2.03;a*=.5;}}return v;}}" +
    "void main(){{vec2 uv=gl_FragCoord.xy/u_res;float t=u_t*.05;" +
    "vec2 q=vec2(fbm(uv*2.1+t),fbm(uv*2.1-t*1.3));" +
    "float n=fbm(uv*2.6+q*1.7);" +
    "vec3 a=vec3(.043,.055,.088);" +
    "vec3 b=vec3(.13,.16,.42);" +
    "vec3 c=vec3(.05,.30,.32);" +
    "vec3 col=a+b*pow(n,2.2)*1.5+c*pow(1.-abs(uv.y-.28),2.5)*.22;" +
    "col+=vec3(.08,.09,.20)*pow(q.y,2.)*.9;" +
    "float vig=smoothstep(1.25,.35,length(uv-vec2(.5,.42)));" +
    "gl_FragColor=vec4(col*vig+a*.25,1.);}}";
  function sh(type, src) {{ const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; }}
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, VS));
  gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, FS));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) return;
  gl.useProgram(prog);
  const buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, "p");
  gl.enableVertexAttribArray(loc);
  gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uRes = gl.getUniformLocation(prog, "u_res");
  const uT = gl.getUniformLocation(prog, "u_t");
  function resize() {{
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    const w = Math.max(2, Math.floor(cv.clientWidth * dpr * .6));
    const h = Math.max(2, Math.floor(cv.clientHeight * dpr * .6));
    if (cv.width !== w || cv.height !== h) {{ cv.width = w; cv.height = h; gl.viewport(0, 0, w, h); }}
    gl.uniform2f(uRes, cv.width, cv.height);
  }}
  resize();
  window.addEventListener("resize", resize);
  const t0 = performance.now();
  function frame(now) {{
    resize();
    gl.uniform1f(uT, (now - t0) / 1000);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    if (!reduced) requestAnimationFrame(frame);
  }}
  requestAnimationFrame(frame);
}})();
</script>
</body></html>"""

WORK_HERO = """
<section class="room" id="top" data-name="THE BEACON"><div class="inner">
<span class="plate">ROOM 1/6 · <span class="no">THE BEACON</span> · available for remote work · now</span>
<h1 class="hero-h">A website you <em>walk</em>. A builder you can <em>check</em>.</h1>
<p class="sub">I build multi-agent AI systems, verification tooling, and shipped software.
This page is a maze, not a scroll: walk the rooms with your arrow keys. Every claim in
every room carries a receipt — a live URL, a machine-checked number, or a filed corrections
table. A stranger who never met me can check all of it. That's the design.</p>
<div class="cta-row">
<a class="btn gold" href="mailto:nachobusinesscorp@gmail.com">nachobusinesscorp@gmail.com</a>
<a class="btn line" href="https://x.com/NachoQuixotic">DM @NachoQuixotic</a>
<a class="btn line" href="#play">Start walking ↓</a>
</div>
<div class="stat-row">
<div class="stat"><b>48/48</b><span>research lift lanes returned</span></div>
<div class="stat"><b>0</b><span>fabrications in 275 checked citations</span></div>
<div class="stat"><b>10/10</b><span>games live &amp; playtested on prod</span></div>
<div class="stat"><b>95.7%</b><span>cache-hit ratio, own production bill</span></div>
<div class="stat"><b>$0.05</b><span>60-experiment battery, total spend</span></div>
</div>
<div class="hint">▸ walk with ↑/↓ or the doors — the map on your right is where you are</div>
<div class="door"><span></span><a href="#play">NEXT: ROOM 2 — PLAY THE PROOF ↓</a></div>
</div></section>
"""
_LEGACY_HERO_UNUSED = """
<span class="kicker">Available for remote work · now</span>
<h1 class="hero-h">I build <em>AI systems that are measured</em> — not demonstrated.</h1>
<p class="sub">Multi-agent orchestration, verification tooling, and shipped software.
Every claim below carries a receipt: a live URL, a machine-checked number, or a filed
corrections table. A stranger who never met me can check all of it — that's the design.</p>
<div class="cta-row">
<a class="btn gold" href="mailto:nachobusinesscorp@gmail.com">nachobusinesscorp@gmail.com</a>
<a class="btn line" href="https://x.com/NachoQuixotic">DM @NachoQuixotic</a>
<a class="btn line" href="#play">Play the proof ↓</a>
<a class="btn line" href="/index.html">The constitution</a>
</div>
<div class="stat-row">
<div class="stat"><b>48/48</b><span>research lift lanes returned</span></div>
<div class="stat"><b>0</b><span>fabrications in 275 checked citations</span></div>
<div class="stat"><b>10/10</b><span>games live &amp; playtested on prod</span></div>
<div class="stat"><b>95.7%</b><span>cache-hit ratio, own production bill</span></div>
<div class="stat"><b>$0.05</b><span>60-experiment battery, total spend</span></div>
</div>
"""

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
        if out == "work.html":
            html = work_page(WORK_HERO, html)
        else:
            html = page(html, title)
        (OUT / out).write_text(html, encoding="utf-8")
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
