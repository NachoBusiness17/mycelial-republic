#!/usr/bin/env python
'''build_vislab_catalog.py — one surface for everything built, with health.

Walks the real filesystem each run and regenerates:
  dashboard/static/vislab/catalog.json   (the source of truth)
  dashboard/static/vislab/catalog.html   (self-contained viewer, data embedded, works offline)

Also syncs deployed games under the dashboard so they can LAUNCH:
  site/dist/games/*.html        -> dashboard/static/games/
  site/dist/static/rounds_real.json -> dashboard/static/rounds_real.json (+ games/)

If dashboard/static/vislab/health.json exists (scripts/sweep_vislab_health.py),
its verdicts are merged into every entry as a health chip.

Run:  ./.venv/Scripts/python.exe scripts/build_vislab_catalog.py
'''
from __future__ import annotations
import glob, hashlib, json, os, re, shutil, sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "dashboard" / "static" / "vislab"

STAR_SUMMARIES = {
    "viz_gallery.html": "THE VIZ LAB — the visual deck gallery (3D Verkle knot chain, Knot Wave, swarm, horses); the operator's 'vislab/static'.",
    "maze_arena.html": "maze_arena — arena/arcade game; steering bends light through dense medium (optics law live).",
    "mud.html": "mud — the web MUD client surface (complexity-ramp tier 2).",
    "swarm.html": "swarm — the swarm simulator view (the substrate the game renders on).",
    "arrakis.html": "arrakis — arena skin/field view.",
    "arena_operator_field.html": "arena_operator_field — operator's field view of the arena.",
    "calabi_yau.html": "calabi_yau — Calabi-Yau manifold visual deck.",
    "aos.html": "aos — atom-of-shapes visual deck.",
    "bad_apple_field.html": "bad_apple_field — field render of the bad-apple stream.",
    "burn_board.html": "burn_board — the burn-down board.",
    "agents.html": "agents — fleet agent roster view.",
    "vislab/belt_trick.html": "belt_trick — THE BELT TRICK DOMAIN LATTICE (CV5 revival of the operator's own math from the sovereign-mirror-scaffold worktree): 360° false close shown failing vs 720° true untangle, Lipschitz-bounded SDF march with the bound displayed live; constants ported verbatim from belt_domain.js + engine.js, provenance table on the plaque.",
}

GAME_TYPE_FOR_MODULE = {
    "fractal_maze": "roguelite-dungeon / optics-puzzle (ray bends through dense field)",
    "audit_dungeon": "exploration-dungeon (audit shadow-work; dungeon-is-waves)",
    "adventure_2d6_stub": "tabletop (tier 1)",
    "dnd_classic_stub": "tabletop system (tier 1 ruleset)",
    "water_computer": "puzzle-toy (analog compute)",
    "riddler_optics": "narrative-optics gallery / writing instrument (prose ray-tracing)",
    "riddler_engram": "content-engine, not a game (summon card: 'summon the riddlers')",
}

GAME_TYPE_FOR_DEPLOYED = {
    "maze_arena.html": "arena/arcade (optics steering; constellation mode)",
    "mud.html": "MUD (ramp tier 2)",
    "swarm.html": "swarm sim / idle loop (the substrate)",
    "arrakis.html": "arena reskin / field",
    "arena_operator_field.html": "operator field view (spectator)",
}

ENGINE_SUMMARIES = {
    "game_entry.py": "STONE 2 — entry surface: 'walk forward and a building appears' gate (gate/reveal/walk/svg).",
    "game_ramp.py": "THE RAMP — tabletop -> mud -> roguelite complexity ladder; work() folds real tasks as knots.",
    "game_world_render.py": "intent-gated world render + optics: attention is light; temperature is the refractive index; the ray bends toward brightness.",
    "game_dfhack.py": "DFHack-style overlay: agent drives the game (status/force/script/autoplay/edit).",
    "persona_recall.py": "STONE 1 — inhabitants recount what happened while you were gone.",
    "distill.py": "the liquid-intelligence machine: distill.game() boils open tasks through the lattice into maze.jsonl.",
    "campaign.py": "campaign engine (hosts the audit dungeon).",
    "game_campaign.py": "game-side campaign glue — handle_game powers /api/v1/game.",
}

def _mtime(p: Path) -> str:
    try:
        return datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")
    except OSError:
        return "?"

def _sha8(p: Path) -> str:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:8]
    except OSError:
        return "?"

def sync_games() -> list[str]:
    """LAW of launchability: a game the dashboard can't serve can't launch."""
    src = ROOT / "site/dist/games"
    dst = ROOT / "dashboard/static/games"
    dst.mkdir(parents=True, exist_ok=True)
    copied = []
    for f in sorted(src.glob("*.html")):
        shutil.copy2(f, dst / f.name)
        copied.append(f.name)
    rr = ROOT / "site/dist/static/rounds_real.json"
    if rr.is_file():
        shutil.copy2(rr, ROOT / "dashboard/static/rounds_real.json")
        shutil.copy2(rr, dst / "rounds_real.json")
    return copied

def entry(path: Path, bucket: str, title: str, summary: str = "", game_type: str = "",
          status: str = "live", version: str = "", launch: str = "", cmd: str = "") -> dict:
    rel = path.relative_to(ROOT).as_posix()
    if not version:
        m = re.search(r"\.v(\d+)\.", path.name)
        version = f"v{m.group(1)}" if m else "sha:" + _sha8(path)
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    return {
        "bucket": bucket, "title": title, "path": rel, "summary": summary,
        "game_type": game_type, "status": status, "version": version,
        "updated": _mtime(path), "bytes": size, "launch": launch, "cmd": cmd,
    }

def build() -> dict:
    items: list[dict] = []

    # GAME MODULES (memory/game_modules/*.json) — launch via the live /api/v1/game route
    for p in sorted(glob.glob(str(ROOT / "memory/game_modules/*.json"))):
        p = Path(p)
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            data = {}
        mid = data.get("module_id", p.stem)
        title = data.get("title") or mid
        st = data.get("status")
        status = "stub" if "stub" in p.stem else "live"
        if isinstance(st, str) and "declared" in st:
            status = "live"
        items.append(entry(p, "GAME MODULES", title,
                           summary=f"{mid}: {len(data.get('rooms', {}))} rooms, system={data.get('system', '?')}" if "rooms" in data else mid,
                           game_type=GAME_TYPE_FOR_MODULE.get(mid, "game module"), status=status,
                           version=re.search(r"\.v(\d+)\.", p.name).group(0).strip(".") if re.search(r"\.v(\d+)\.", p.name) else "v1",
                           launch=f"/static/vislab/play.html?module={mid}",
                           cmd=f"./.venv/Scripts/python.exe main.py campaign --module {p.relative_to(ROOT).as_posix()} --all"))

    # DEPLOYED GAMES (synced to dashboard/static/games so they actually launch)
    for name in sorted(sync_games()):
        if not name.endswith(".html"):
            continue
        p = ROOT / "dashboard/static/games" / name
        items.append(entry(p, "DEPLOYED GAMES", name[:-5].replace("_", " "),
                           summary=STAR_SUMMARIES.get(name, "deployed game build (synced from site/dist/games)"),
                           game_type=GAME_TYPE_FOR_DEPLOYED.get(name, "game build"),
                           launch=f"/static/games/{name}"))

    # ENGINE (mag game surfaces)
    engine_files = sorted(set(glob.glob(str(ROOT / "mag/game_*.py"))) |
                          {str(ROOT / "mag/persona_recall.py"), str(ROOT / "mag/distill.py"),
                           str(ROOT / "mag/campaign.py")})
    for p in engine_files:
        p = Path(p)
        if not p.is_file():
            continue
        cmd = "./.venv/Scripts/python.exe main.py game status" if p.name == "game_ramp.py" else ""
        items.append(entry(p, "ENGINE", p.name, summary=ENGINE_SUMMARIES.get(p.name, "game engine surface"),
                           game_type="engine", status="live", cmd=cmd))

    # VIZ DECKS (dashboard/static top-level html + key js)
    deck_files = sorted(glob.glob(str(ROOT / "dashboard/static/*.html"))) + \
                 [str(ROOT / "dashboard/static/app.js"), str(ROOT / "dashboard/static/board.js")]
    for p in deck_files:
        p = Path(p)
        if not p.is_file():
            continue
        t = ""
        try:
            head = p.read_text(encoding="utf-8", errors="ignore")[:2048]
            m = re.search(r"<title>(.*?)</title>", head, re.S | re.I)
            if m:
                t = m.group(1).strip()[:80]
        except OSError:
            pass
        name = p.name
        title = t or name
        items.append(entry(p, "VIZ DECKS", title,
                           summary=STAR_SUMMARIES.get(name, "visual deck / dashboard surface"),
                           game_type=("visual deck (ambience candidate)" if name.endswith(".html") else "shared UI logic"),
                           launch=f"/static/{name}"))

    # VISLAB (dashboard/static/vislab/*.html — self-contained vis pages; CV5 2026-09-16)
    for p in sorted(glob.glob(str(ROOT / "dashboard/static/vislab/*.html"))):
        p = Path(p)
        if p.name in ("catalog.html", "play.html"):
            continue  # the catalog's own surfaces
        rel_key = "vislab/" + p.name
        items.append(entry(p, "VISLAB", p.name[:-5].replace("_", " "),
                           summary=STAR_SUMMARIES.get(rel_key, "vislab vis page"),
                           game_type="vis (webgl/math surface)",
                           launch=f"/static/vislab/{p.name}"))

    # SHADERS
    for p in sorted(glob.glob(str(ROOT / "dashboard/static/shaders/**/*.glsl"), recursive=True) +
                    glob.glob(str(ROOT / "dashboard/static/shaders/**/*.frag"), recursive=True)):
        p = Path(p)
        items.append(entry(p, "SHADERS", p.stem.replace("_", " "),
                           summary="shader library — world-skin preset for decks/games",
                           game_type="world-skin / visual preset"))

    # PROMPT LIBRARY
    for p in sorted(glob.glob(str(ROOT / "prompts/*"))) + \
             sorted(glob.glob(str(ROOT / "docs/ref/prompts/*"))) + \
             sorted(glob.glob(str(ROOT / "memory/knowledge_packs/*/*"))):
        p = Path(p)
        if not p.is_file():
            continue
        items.append(entry(p, "PROMPT LIBRARY", p.name,
                           summary="prompt surface (DM voice / passage / desk)",
                           game_type="content-generator"))

    # GAME DOCTRINE (memory/game)
    doctrine_files = ["STATE.md", "PLAN_THE_GAME_VERTICAL_ADOPTION.md", "SYSTEM_MAP.md",
                      "STORY_ORG.md", "hero_journey.md", "maze.jsonl", "game_observer_steer.json",
                      "live_fed.json", "FLOW_IMAGE.json", "FLOW_LEDGER.jsonl"]
    for name in doctrine_files:
        p = ROOT / "memory/game" / name
        if p.is_file():
            items.append(entry(p, "GAME DOCTRINE", name,
                               summary="the game's self-knowledge / plan / run trail",
                               game_type="doctrine"))
    for sub, label in (("campaign_runs", "campaign run trails"), ("adventure", "adventure state"), ("world", "world state")):
        d = ROOT / "memory/game" / sub
        if d.is_dir():
            n = sum(1 for _ in d.glob("*"))
            items.append({"bucket": "GAME DOCTRINE", "title": f"memory/game/{sub}/ ({n} files)",
                          "path": d.relative_to(ROOT).as_posix(), "summary": label,
                          "game_type": "doctrine", "status": "live", "version": "-",
                          "updated": _mtime(d), "bytes": 0, "launch": "", "cmd": ""})

    # RIDDLER WING (built 2026-09-14)
    for p in sorted(glob.glob(str(ROOT / "memory/corpus/ractors/*/MANIFEST.json"))):
        p = Path(p)
        items.append(entry(p, "RIDDLER WING", f"shelf: {p.parent.name}",
                           summary="riddler ractor shelf — bibliography + interactions (author-mask canon)",
                           game_type="content-engine", status="live"))
    for name, summ in (("riddler_engram.v1.json", "summon card — 'summon the riddlers'"),
                       ("riddler_optics.v1.json", "THE RIDDLER OPTICS dungeon — 12 rooms, clerk ray, refraction receipts")):
        p = ROOT / "memory/game_modules" / name
        if p.is_file():
            items.append(entry(p, "RIDDLER WING", name, summary=summ, game_type=GAME_TYPE_FOR_MODULE.get(name.split(".")[0], ""), status="live"))
    wl = ROOT / "memory/corpus/ractors/WISH_LIST.md"
    if wl.is_file():
        items.append(entry(wl, "RIDDLER WING", "WISH_LIST.md (riddler wave)", summary="walled library, named never pirated + next PD pull wave", game_type="doctrine"))

    buckets: dict[str, list[dict]] = {}
    for it in items:
        buckets.setdefault(it["bucket"], []).append(it)
    return {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "totals": {"entries": len(items), "buckets": len(buckets)},
        "buckets": {k: v for k, v in sorted(buckets.items())},
    }

def merge_health(catalog: dict) -> int:
    hp = OUT_DIR / "health.json"
    if not hp.is_file():
        return 0
    try:
        health = json.loads(hp.read_text(encoding="utf-8"))
    except Exception:
        return 0
    n = 0
    results = health.get("results", health)
    for bucket in catalog["buckets"].values():
        for it in bucket:
            h = results.get(it["path"]) or results.get(it["path"].removeprefix("dashboard/static/"))
            if h:
                it["health"] = h
                n += 1
    return n

TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>VISLAB CATALOG — everything built, one surface</title>
<style>
:root{--bg:#0b0e14;--panel:#121722;--line:#232b3b;--txt:#c9d4e8;--dim:#7c8aa5;--acc:#7fb0ff;--ok:#7ee2a8;--warn:#ffd479;--bad:#ff7b7b;--mut:#5a6478}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:14px/1.5 ui-monospace,Consolas,monospace;padding:24px}
h1{font-size:18px;letter-spacing:.12em;margin:0 0 4px}h1 span{color:var(--acc)}
.sub{color:var(--dim);font-size:12px;margin-bottom:16px}
.bar{position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);z-index:5}
input{width:100%;background:var(--panel);border:1px solid var(--line);color:var(--txt);padding:8px 10px;font:inherit;outline:none}
.tabs{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.tab{cursor:pointer;border:1px solid var(--line);background:var(--panel);color:var(--dim);padding:4px 10px;font-size:12px;user-select:none}
.tab.on{color:var(--acc);border-color:var(--acc)}
.tab .n{color:var(--mut)}
.bucket{margin:22px 0 8px;font-size:13px;letter-spacing:.14em;color:var(--acc);border-bottom:1px solid var(--line);padding-bottom:4px}
.card{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--mut);padding:8px 12px;margin:8px 0}
.card:hover{border-left-color:var(--acc)}
.t{font-weight:700}
.chip{display:inline-block;border:1px solid var(--line);color:var(--dim);padding:0 6px;font-size:11px;margin-left:6px;vertical-align:1px}
.chip.s-live{color:var(--ok);border-color:var(--ok)}.chip.s-stub{color:var(--warn);border-color:var(--warn)}.chip.s-declared-not-done{color:var(--warn)}
.chip.h-ok{color:var(--ok);border-color:var(--ok)}.chip.h-soft{color:var(--warn);border-color:var(--warn)}.chip.h-hard{color:var(--bad);border-color:var(--bad)}
.launch{display:inline-block;margin-left:8px;border:1px solid var(--ok);color:var(--ok);padding:0 8px;font-size:11px;cursor:pointer}
.launch:hover{background:var(--ok);color:var(--bg)}
.cmd{color:var(--warn);font-size:11px;cursor:copy}
.path{color:var(--dim);font-size:12px;word-break:break-all}
.sum{color:var(--txt);font-size:12px;margin-top:2px}
.miss{color:var(--bad);font-size:11px;margin-top:2px}
.gt{color:var(--acc);font-size:12px}
a{color:var(--acc);text-decoration:none}a:hover{text-decoration:underline}
#err{color:var(--warn);white-space:pre-wrap}
.k{color:var(--mut);font-size:11px;margin-top:8px}
</style></head><body>
<h1>VISLAB <span>CATALOG</span></h1>
<div class="sub" id="meta"></div>
<div class="bar"><input id="q" placeholder="filter: title / path / game type / summary / health…">
<div class="tabs" id="tabs"></div></div>
<div class="k" style="margin:6px 0 0">▶ <a href="/static/vislab/play.html" style="color:var(--ok)">OPEN THE GAME PLAYER</a> — every module dungeon playable in the browser (pick dungeon → name character → play)</div>
<div id="err"></div><div id="out"></div>
<div class="k">regenerate: <b>./.venv/Scripts/python.exe scripts/build_vislab_catalog.py</b> · health sweep: <b>scripts/sweep_vislab_health.py</b> — the walk is the truth; this page embeds the last walk so it never breaks on load.</div>
<script id="data" type="application/json">__CATALOG_JSON__</script>
<script>
let DATA=null;
try{DATA=JSON.parse(document.getElementById('data').textContent);}
catch(e){document.getElementById('err').textContent='catalog data failed to parse: '+e;}
function esc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;');}
if(DATA){
 const T=document.getElementById('tabs'),O=document.getElementById('out'),Q=document.getElementById('q');
 const names=Object.keys(DATA.buckets);
 let cur='ALL';
 document.getElementById('meta').textContent='generated '+DATA.generated+' — '+DATA.totals.entries+' entries in '+DATA.totals.buckets+' buckets — everything below is real files on disk at build time';
 function tabs(){T.innerHTML='';['ALL'].concat(names).forEach(n=>{const d=document.createElement('div');d.className='tab'+(cur===n?' on':'');d.innerHTML=n+' <span class="n">('+(n==='ALL'?DATA.totals.entries:DATA.buckets[n].length)+')</span>';d.onclick=()=>{cur=n;render();tabs();};T.appendChild(d);});}
 function launch(it){
  if(it.launch)return '<a class="launch" target="_blank" href="'+esc(it.launch)+'">▶ LAUNCH</a>';
  if(it.cmd)return '<span class="launch cmd" title="click to copy" onclick="navigator.clipboard&&navigator.clipboard.writeText('+JSON.stringify(JSON.stringify(it.cmd))+').catch(()=>{});this.textContent=\\'copied ✓\\'">⧉ '+esc(it.cmd)+'</span>';
  return '';}
 function health(it){
  const h=it.health;if(!h)return '';
  const cls=h.state==='ok'?'h-ok':(h.state==='soft'?'h-soft':'h-hard');
  const label=h.state==='ok'?'HEALTHY':(h.state==='soft'?'PAGES LOADS, '+(h.missing||[]).length+' ASSET(S) 404':'DOWN '+h.code);
  const tip=(h.missing||[]).slice(0,5).join('\\n')+(h.born?'\\nborn: '+h.born:'');
  return '<span class="chip '+cls+'" title="'+esc(tip)+'">'+label+'</span>';}
 function render(){const q=Q.value.toLowerCase();O.innerHTML='';
  names.filter(n=>cur==='ALL'||cur===n).forEach(n=>{
   const rows=DATA.buckets[n].filter(it=>!q||((it.title+' '+it.path+' '+it.game_type+' '+it.summary+' '+(it.health?it.health.state:''))).toLowerCase().includes(q));
   if(!rows.length)return;
   const h=document.createElement('div');h.className='bucket';h.textContent=n+' — '+rows.length;O.appendChild(h);
   rows.forEach(it=>{const c=document.createElement('div');c.className='card';
    c.innerHTML='<div class="t">'+esc(it.title)
     +'<span class="chip s-'+esc(it.status)+'">'+esc(it.status)+'</span>'
     +'<span class="chip">'+esc(it.version)+'</span>'
     +'<span class="chip">'+esc(it.updated)+'</span>'
     +health(it)+launch(it)+'</div>'
     +'<div class="path"><a href="/static/" title="static index">'+esc(it.path)+'</a> <span class="chip">'+(it.bytes>1024?Math.round(it.bytes/1024)+'kb':it.bytes+'b')+'</span></div>'
     +(it.summary?'<div class="sum">'+esc(it.summary)+'</div>':'')
     +(it.health&&it.health.missing&&it.health.missing.length?'<div class="miss">404: '+esc(it.health.missing.slice(0,4).join(' · '))+(it.health.missing.length>4?' +'+(it.health.missing.length-4)+' more':'')+'</div>':'')
     +(it.game_type?'<div class="gt">⌁ game-type candidate: '+esc(it.game_type)+'</div>':'');
    O.appendChild(c);});});
  if(!O.innerHTML)O.innerHTML='<div class="sub">no matches.</div>';}
 Q.oninput=render;tabs();render();
}
</script></body></html>
"""

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    catalog = build()
    merged = merge_health(catalog)
    (OUT_DIR / "catalog.json").write_text(json.dumps(catalog, indent=1, ensure_ascii=False), encoding="utf-8")
    payload = json.dumps(catalog, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("__CATALOG_JSON__", payload)
    (OUT_DIR / "catalog.html").write_text(html, encoding="utf-8")
    print(f"catalog: {catalog['totals']['entries']} entries / {len(catalog['buckets'])} buckets / {merged} health verdicts merged")
    for k, v in catalog["buckets"].items():
        print(f"  {k:16s} {len(v)}")
    print(f"wrote {OUT_DIR/'catalog.json'} and {OUT_DIR/'catalog.html'}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
