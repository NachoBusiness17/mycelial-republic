"""SCOUT DECK builder — the fleet's Pro-surface, one interface, zero tabbing.

STATIC RENDER LAW: this script reads the live sources and BAKES them into a
single self-contained HTML file. The page needs nothing at view time — no
fetch, no API, no server-side anything. Regenerate when sources change:

    python dashboard/static/_build_scout_deck.py

Baked columns:
  SURFACES  launcher links (x.com FYP / bookmarks / top_posts / trending / grok / pro deck)
  TAPE      last 15 rows of watch/room.jsonl (kind + ts + detail, trimmed 160)
  CARDS     newest 12 watch/INTAKE_*.md + their ## SCORE line
  RECORDER  mag.flight_recorder.summarize() output (errors shown honestly)
  QUEUE     watch/organ_queue.jsonl rows + operator GO list
  DOCTRINE  AUTONOMY_WHEEL / BURST_DOCTRINE / TRI_PARTY / SWARM_SCALE_PLAN / X_SCOUT_DOCTRINE
            copied into static/doctrine/ as baked reader pages (served by the 8765 server)
"""
from __future__ import annotations

import html
import io
import json
import re
import shutil
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

STATIC = Path(__file__).resolve().parent
ROOT = STATIC.parent.parent
WATCH = ROOT / "watch"
OUT = STATIC / "scout_deck.html"
DOCTRINE_DIR = STATIC / "doctrine"
GO_JSON = WATCH / "scout_deck_go.json"

DOCTRINE = [
    ("AUTONOMY WHEEL", "AUTONOMY_WHEEL"),
    ("BURST DOCTRINE", "BURST_DOCTRINE"),
    ("TRI-PARTY", "TRI_PARTY"),
    ("SWARM SCALE PLAN", "SWARM_SCALE_PLAN"),
    ("X SCOUT DOCTRINE", "X_SCOUT_DOCTRINE"),
]


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def trim(s: str, n: int) -> str:
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "\u2026"


def tail_jsonl(path: Path, n: int) -> list:
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except Exception:  # noqa: BLE001 - torn row must not kill the bake
            continue
    return rows[-n:]


# ------------------------------------------------------------------ columns


def build_tape() -> str:
    rows = tail_jsonl(WATCH / "room.jsonl", 15)
    if not rows:
        return '<p class="empty">room.jsonl empty or missing</p>'
    out = []
    for r in rows:
        detail = r.get("detail") or r.get("item") or ""
        if not detail:
            detail = " | ".join(
                filter(None, (r.get("verdict", ""), r.get("route", ""))))
        out.append(
            '<div class="row"><span class="k">%s</span>'
            '<span class="ts">%s</span>'
            '<span class="d">%s</span></div>'
            % (esc(r.get("kind", "?")), esc(r.get("ts", "")),
               esc(trim(detail, 160))))
    return "\n".join(out)


def build_cards() -> str:
    cards = sorted(WATCH.glob("INTAKE_*.md"), key=lambda p: p.stat().st_mtime,
                   reverse=True)[:12]
    if not cards:
        return '<p class="empty">no INTAKE_*.md in watch/</p>'
    out = []
    for p in cards:
        score = ""
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("## SCORE"):
                score = trim(line.replace("## SCORE", "").strip(" \u2014-*"), 120)
                break
        out.append(
            '<div class="card"><span class="fname">%s</span>%s</div>'
            % (esc(p.name),
               ('<span class="score">%s</span>' % esc(score)) if score else ""))
    return "\n".join(out)


def build_recorder() -> str:
    try:
        sys.path.insert(0, str(ROOT))
        import mag.flight_recorder as fr  # noqa: PLC0415 - build-time only

        buf = io.StringIO()
        fr.summarize(out=buf)
        text = buf.getvalue().strip()
        if not text:
            return ('<p class="err">RECORDER ERROR (honest): summarize() returned '
                    'empty output — watch/flight_recorder.jsonl missing or rowless</p>')
        return "<pre>%s</pre>" % esc(text)
    except Exception:  # noqa: BLE001 - bake the error, never fake the data
        return "<pre>RECORDER ERROR (honest):\n%s</pre>" % esc(
            traceback.format_exc(limit=3))


def build_queue() -> str:
    rows = tail_jsonl(WATCH / "organ_queue.jsonl", 100)
    if not rows:
        return '<p class="empty">organ_queue.jsonl empty or missing</p>'
    out = []
    for r in rows:
        out.append(
            '<div class="qrow"><span class="qid">%s</span>'
            '<span class="qbrief">%s</span>'
            '<span class="qbuild">%s</span></div>'
            % (esc(r.get("id", "?")), esc(trim(r.get("brief", ""), 200)),
               esc(r.get("build", ""))))
    return "\n".join(out)


def build_go() -> str:
    """Operator GO list: watch/scout_deck_go.json first; else derive from
    queue rows whose brief says BUILD NOW. Never invent a GO."""
    if GO_JSON.is_file():
        try:
            data = json.loads(GO_JSON.read_text(encoding="utf-8"))
            items = []
            for it in data:
                if isinstance(it, str):
                    items.append((it, "source: scout_deck_go.json"))
                else:
                    items.append((it.get("id", "?"),
                                  it.get("note") or it.get("source") or "scout_deck_go.json"))
            return "\n".join(
                '<div class="go"><span class="gold">\u25b6 GO</span> <span class="gid">%s</span>'
                '<span class="gsrc">%s</span></div>' % (esc(i), esc(s))
                for i, s in items) or '<p class="empty">go json present but empty</p>'
        except Exception as e:  # noqa: BLE001
            return '<p class="err">GO JSON UNREADABLE (honest): %s</p>' % esc(e)
    rows = tail_jsonl(WATCH / "organ_queue.jsonl", 100)
    gos = [(r.get("id", "?"), trim(r.get("brief", ""), 90))
           for r in rows if "BUILD NOW" in str(r.get("brief", ""))]
    if not gos:
        return '<p class="empty">no operator GO on file (queue has no BUILD NOW rows)</p>'
    return "\n".join(
        '<div class="go"><span class="gold">\u25b6 GO</span> <span class="gid">%s</span>'
        '<span class="gsrc">%s</span></div>' % (esc(i), esc(s)) for i, s in gos)


def find_doctrine_file(stem_prefix: str) -> Path | None:
    for base in (WATCH, ROOT / "docs" / "ref"):
        hits = sorted(base.glob(stem_prefix + "*.md"))
        if hits:
            return hits[0]
    return None


def bake_doctrine() -> list:
    """Copy each doctrine doc into static/doctrine/<name>.html (dark reader page,
    zero fetch) and return link rows. Missing files are shown honestly."""
    DOCTRINE_DIR.mkdir(exist_ok=True)
    links = []
    for label, stem in DOCTRINE:
        src = find_doctrine_file(stem)
        if src is None:
            links.append('<span class="missing">%s — FILE NOT FOUND (honest)</span>'
                         % esc(label))
            continue
        body = src.read_text(encoding="utf-8", errors="replace")
        page = DOCTRINE_READER % (esc(src.name), esc(label), esc(str(src.relative_to(ROOT))),
                                  esc(body))
        dst = DOCTRINE_DIR / (stem + ".html")
        dst.write_text(page, encoding="utf-8")
        links.append('<a href="/static/doctrine/%s" target="_blank">%s'
                     '<span class="src">%s</span></a>'
                     % (esc(dst.name), esc(label), esc(src.relative_to(ROOT))))
    return links


DOCTRINE_READER = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>%s — fleet doctrine</title>
<style>
body{background:#030806;color:#c8d6d0;font:14px/1.6 ui-monospace,'Cascadia Mono',Consolas,monospace;
margin:0;padding:32px 40px;max-width:980px}
h1{color:#3ff2d0;font-size:18px;letter-spacing:2px;border-bottom:1px solid #0e2a22;padding-bottom:10px}
.src{color:#5a7a6e;font-size:11px;margin-bottom:24px}
pre{white-space:pre-wrap;word-wrap:break-word;margin:0}
a{color:#f2c14e}
</style></head><body>
<h1>%s</h1><div class="src">baked snapshot of %s \u2014 regen scout_deck to refresh</div>
<pre>%s</pre></body></html>
"""


# ------------------------------------------------------------------ render

SURFACES = [
    ("FYP", "https://x.com/home", "the for-you page \u2014 scout intake ground"),
    ("BOOKMARKS \u2192 HISTORY", "https://x.com/i/bookmarks", "saved signal \u2014 the history page"),
    ("TOP POSTS \u2014 MOST BOOKMARKS", "https://x.com/i/jf/creators/inspiration/top_posts",
     "sort by Most Bookmarks \u2014 the save-signal is the signal"),
    ("GLOBAL TRENDING", "https://x.com/i/jf/global-trending", "NOISE \u2014 labeled noise, enter at own risk"),
    ("GROK", "https://grok.com", "complex research primer lane"),
    ("PRO DECK", "https://pro.x.com", "pro.x.com \u2014 the heavy console"),
]


def render(baked_ts: str) -> str:
    tape = build_tape()
    cards = build_cards()
    recorder = build_recorder()
    queue = build_queue()
    go = build_go()
    doctrine = bake_doctrine()
    surfaces = "\n".join(
        '<a class="surf" href="%s" target="_blank" rel="noopener">'
        '<span class="sname">%s</span><span class="sdesc">%s</span></a>'
        % (esc(url), esc(name), esc(desc)) for name, url, desc in SURFACES)

    return HTML % {
        "ts": esc(baked_ts),
        "regen": esc("python dashboard/static/_build_scout_deck.py"),
        "surfaces": surfaces,
        "tape": tape,
        "cards": cards,
        "recorder": recorder,
        "queue": queue,
        "go": go,
        "doctrine": "\n".join(doctrine),
    }


HTML = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MAG // SCOUT DECK</title>
<style>
:root{
  --bg:#030806; --panel:#07110d; --line:#0e2a22; --line2:#14453a;
  --cyan:#3ff2d0; --gold:#f2c14e; --ink:#c8d6d0; --dim:#5a7a6e; --dimmer:#3a554b;
  --mono:ui-monospace,'Cascadia Mono',Consolas,'Courier New',monospace;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);font-family:var(--mono);margin:0;
  font-size:12.5px;line-height:1.5}
header{border-bottom:1px solid var(--line);padding:14px 22px;display:flex;
  flex-wrap:wrap;gap:10px 26px;align-items:baseline}
header h1{color:var(--cyan);font-size:17px;letter-spacing:3px;margin:0;font-weight:600}
header h1 .g{color:var(--gold)}
.meta{color:var(--dim);font-size:11px}
.meta b{color:var(--ink);font-weight:500}
.grid{display:grid;gap:14px;padding:14px 22px 28px;
  grid-template-columns:repeat(auto-fit,minmax(330px,1fr))}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:6px;
  padding:12px 14px;min-width:0;overflow-wrap:break-word}
.panel h2{color:var(--gold);font-size:11px;letter-spacing:3px;margin:0 0 10px;
  border-bottom:1px solid var(--line);padding-bottom:7px;font-weight:600}
.panel h2 .n{color:var(--dimmer);letter-spacing:0;float:right}
a{color:var(--cyan);text-decoration:none}
a:hover{text-decoration:underline}
.surf{display:flex;flex-direction:column;gap:1px;padding:8px 9px;margin-bottom:7px;
  border:1px solid var(--line);border-radius:4px}
.surf:hover{border-color:var(--cyan);text-decoration:none;background:#0a1a14}
.sname{color:var(--cyan);letter-spacing:1px;font-size:12.5px}
.sdesc{color:var(--dim);font-size:10.5px}
.noise .sname{color:#b08430}
.row,.card,.qrow,.go{padding:5px 0;border-bottom:1px dashed #0c1f19}
.row:last-child,.card:last-child,.qrow:last-child{border-bottom:0}
.k{color:var(--gold);margin-right:8px;font-size:11px}
.ts{color:var(--dimmer);font-size:10px;display:block}
.d{color:var(--ink);display:block}
.fname{color:var(--cyan);display:block;font-size:11.5px}
.score{color:var(--gold);display:block;font-size:10.5px}
.qid{color:var(--cyan);display:block}
.qbrief{color:var(--ink);display:block;font-size:11.5px}
.qbuild{color:var(--dimmer);display:block;font-size:9.5px;word-break:break-all}
.gold{color:var(--gold)}
.gid{color:var(--ink)}
.gsrc{color:var(--dimmer);font-size:10px;display:block}
.panel.doctrine a{display:flex;flex-direction:column;padding:7px 0;
  border-bottom:1px dashed #0c1f19}
.panel.doctrine a:last-child{border-bottom:0}
.panel.doctrine .src{color:var(--dimmer);font-size:9.5px}
.missing{color:#c96a5a;display:block;padding:7px 0}
.empty{color:var(--dimmer)}
.err{color:#c96a5a}
pre{white-space:pre-wrap;word-break:break-word;margin:0;color:var(--ink);
  font-size:11px;line-height:1.55}
.recorder{grid-column:span 1}
@media(min-width:1050px){
  .grid{grid-template-columns:repeat(3,1fr)}
  .tape{grid-column:span 1}
  .recorder{grid-column:span 1}
}
footer{color:var(--dimmer);font-size:10px;padding:0 22px 26px}
</style>
</head>
<body>
<header>
  <h1>MAG <span class="g">//</span> SCOUT DECK</h1>
  <span class="meta">BAKED <b>%(ts)s</b></span>
  <span class="meta">STATIC RENDER LAW \u2014 zero fetch at view time</span>
  <span class="meta">REGEN <b>%(regen)s</b></span>
</header>
<div class="grid">
  <section class="panel surfaces"><h2>SURFACES <span class="n">launcher</span></h2>
%(surfaces)s
  </section>
  <section class="panel tape"><h2>TAPE <span class="n">room.jsonl last 15</span></h2>
%(tape)s
  </section>
  <section class="panel cards"><h2>CARDS <span class="n">newest 12 intake</span></h2>
%(cards)s
  </section>
  <section class="panel recorder"><h2>RECORDER <span class="n">flight_recorder.summarize()</span></h2>
%(recorder)s
  </section>
  <section class="panel queue"><h2>QUEUE <span class="n">organ_queue + GO list</span></h2>
<h2 style="border:0;margin:0 0 4px;padding:0;color:var(--cyan);letter-spacing:2px">OPERATOR GO</h2>
%(go)s
<h2 style="margin:12px 0 8px">ORGAN QUEUE</h2>
%(queue)s
  </section>
  <section class="panel doctrine"><h2>DOCTRINE <span class="n">baked readers</span></h2>
%(doctrine)s
  </section>
</div>
<footer>scout_deck v0 \u2014 one surface, no tabbing. baked snapshot; regen after room/card/queue/recorder changes.</footer>
</body>
</html>
"""


def main() -> None:
    baked_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    page = render(baked_ts)
    OUT.write_text(page, encoding="utf-8")
    print("OK", OUT, "size", OUT.stat().st_size, "baked", baked_ts)


if __name__ == "__main__":
    main()
