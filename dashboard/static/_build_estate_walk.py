"""Build estate_walk.html — the repo as a dark navigable space.

Two floors, one clock:
  mycelium  — graph_snapshot nodes + edges.jsonl corridors, lane lanterns
              replaying queue/lanes/*/trail.jsonl
  estate    — file constellation from git history + trail artifacts,
              commit pulses light real files

Self-contained output (no server, no assets). Deterministic: seed 1197,
md5-based placement (never salted hash()).

Lantern honesty: trail rows reference neither node ids nor positions, so
waypoints are a deterministic projection (md5 of the event row); every
lantern walk follows real mycelium corridors between waypoints. Commits
and artifact pulses ARE placed exactly. The HUD says so.
"""

import hashlib
import json
import math
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "dashboard" / "static" / "estate_walk.html"
OUT_LOD = ROOT / "dashboard" / "static" / "estate_walk.lod.html"
SEED = 1197
ZONE_GRID = 4  # estate index (LOD): 4x4 spatial zones, summaries only until a zone opens
SPAN_REPLAY_S = 120.0
MAX_DETAIL = 140
MAX_STARS = 1200  # the 144 commits touch 75k files; keep the load-bearing ones

LANES = [
    ("research", "#6fd6ff"),
    ("day_work", "#fff2c8"),
    ("builder", "#8dff7a"),
    ("forge", "#ff7a4d"),
    ("bard_ledger", "#c98bff"),
    ("elder", "#ffb347"),
]


def md5(s):
    return int(hashlib.sha256(s.encode("utf-8")).hexdigest()[:12], 16)


def iso_to_epoch(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()


def load_nodes_edges():
    snap = json.loads((ROOT / "memory/mycelium/graph_snapshot.json").read_text(encoding="utf-8"))
    nodes, by_id = [], {}
    for row in snap["nodes"]:  # first row wins on id collision (27 in snapshot)
        if row["id"] in by_id:
            continue
        by_id[row["id"]] = len(nodes)
        nodes.append({
            "id": row["id"],
            "title": (row.get("title") or row["id"])[:90],
            "type": row.get("type", "artifact"),
            "trust": round(float(row.get("trust") or 0.5), 2),
        })
    edges, selfloops = [], 0
    for line in (ROOT / "memory/mycelium/edges.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        e = json.loads(line)
        si, di = by_id.get(e["src"]), by_id.get(e["dst"])
        if si is None or di is None:
            continue
        if si == di:
            selfloops += 1
            continue  # rings, not corridors
        edges.append([si, di, e.get("type", "produced"), round(float(e.get("weight") or 0.5), 2)])
    return nodes, edges, selfloops


def layout_nodes(nodes, edges, iters=400):
    rng = np.random.default_rng(SEED)
    n = len(nodes)
    pos = rng.standard_normal((n, 2)) * 120.0
    adj = np.array([[e[0], e[1]] for e in edges], dtype=int) if edges else np.zeros((0, 2), int)
    for it in range(iters):
        diff = pos[None, :, :] - pos[:, None, :]
        d2 = (diff ** 2).sum(-1) + 1e-6
        np.fill_diagonal(d2, 1e6)
        repulse = (diff / np.sqrt(d2)[..., None] * 3000.0 / d2[..., None]).sum(1)
        spring = np.zeros_like(pos)
        if len(adj):
            delta = pos[adj[:, 0]] - pos[adj[:, 1]]
            dist = np.sqrt((delta ** 2).sum(-1)) + 1e-6
            f = (dist - 80.0)[:, None] * delta / dist[:, None] * 0.05
            np.add.at(spring, adj[:, 0], -f)
            np.add.at(spring, adj[:, 1], f)
        pos += (repulse + spring - pos * 0.004) * min(1.0, 2.0 * (1.0 - it / iters) + 0.02)
    pos -= pos.min(0)
    pos /= max(pos.max(), 1e-6)
    pos = pos * 1500.0 + 60.0
    center = pos.mean(0)  # stretch the connected mass so it reads next to the star fan
    pos = (pos - center) * 1.7 + center
    np.clip(pos, 30.0, 1730.0, out=pos)
    for i, p in enumerate(pos):
        nodes[i]["x"] = round(float(p[0]), 1)
        nodes[i]["y"] = round(float(p[1]), 1)
    return pos


def git_commits():
    out = subprocess.run(
        ["git", "log", "--name-only", "--format=%ct|%h|%s"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
    commits = []
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3 and parts[0].isdigit():
            commits.append({
                "t": int(parts[0]), "h": parts[1], "m": parts[2][:80], "f": [],
            })
        elif commits:
            commits[-1]["f"].append(line.replace("\\", "/"))
    return commits


def load_trails():
    trails = {}
    for lane, _ in LANES:
        p = ROOT / "queue" / "lanes" / lane / "trail.jsonl"
        rows = []
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        r = json.loads(line)
                        r["_t"] = iso_to_epoch(r["ts"])
                        rows.append(r)
                    except Exception:
                        pass
        rows.sort(key=lambda r: r["_t"])
        trails[lane] = rows
    return trails


def compute_lod_zones(nodes, edges, stars, grid=ZONE_GRID):
    """Zone-level LOD: spatial grid over the estate bounds; per-zone counts,
    dominant types and a few titles. Small enough to parse at startup so the
    index view never has to load (or even JSON.parse) every node."""
    xs = [n["x"] for n in nodes] + [s["x"] for s in stars]
    ys = [n["y"] for n in nodes] + [s["y"] for s in stars]
    x0, x1 = min(xs) - 20.0, max(xs) + 20.0
    y0, y1 = min(ys) - 20.0, max(ys) + 20.0
    w, h = (x1 - x0) / grid, (y1 - y0) / grid

    def cell(x, y):
        return (min(grid - 1, int((x - x0) / w)), min(grid - 1, int((y - y0) / h)))

    zones = [{"n": 0, "e": 0, "s": 0, "types": defaultdict(int), "titles": []}
             for _ in range(grid * grid)]
    for n in nodes:
        cx, cy = cell(n["x"], n["y"])
        z = zones[cy * grid + cx]
        z["n"] += 1
        z["types"][n["type"]] += 1
        z["titles"].append(n["title"])
    for e in edges:  # e = [src_ix, dst_ix, type, weight]
        za = cell(nodes[e[0]]["x"], nodes[e[0]]["y"])
        zb = cell(nodes[e[1]]["x"], nodes[e[1]]["y"])
        if za == zb:
            zones[za[1] * grid + za[0]]["e"] += 1
    for s in stars:
        cx, cy = cell(s["x"], s["y"])
        zones[cy * grid + cx]["s"] += 1

    out = []
    for i, z in enumerate(zones):
        gx, gy = i % grid, i // grid
        out.append({
            "id": i,
            "x": round(x0 + gx * w, 1), "y": round(y0 + gy * h, 1),
            "w": round(w, 1), "h": round(h, 1),
            "n": z["n"], "e": z["e"], "s": z["s"],
            "types": dict(sorted(z["types"].items(), key=lambda kv: -kv[1])[:4]),
            "top": sorted(z["titles"])[:6],
        })
    return {"grid": grid, "bounds": [round(x0, 1), round(y0, 1), round(x1, 1), round(y1, 1)],
            "zones": out}


def build(lod_only=False):
    nodes, edges, selfloops = load_nodes_edges()
    pos = layout_nodes(nodes, edges)
    commits = git_commits()
    trails = load_trails()

    # --- file constellation: union of git-touched files + trail artifacts ---
    star_ix = {}
    touch_count = defaultdict(int)
    artifacts = defaultdict(set)  # lane -> {path}
    for lane, _ in LANES:
        for r in trails[lane]:
            for a in (r.get("artifacts") or []):
                a = str(a).replace("\\", "/").strip()
                if a and not a.startswith(("http", "n-")):
                    artifacts[lane].add(a)
                    touch_count[a] += 3
                    star_ix.setdefault(a, len(star_ix))
    for c in commits:
        for f in c["f"]:
            touch_count[f] += 1
            star_ix.setdefault(f, len(star_ix))

    if len(star_ix) > MAX_STARS:  # keep the most-touched paths; commits remap below
        keep = set(sorted(star_ix, key=lambda p: -touch_count[p])[:MAX_STARS])
        star_ix = {p: i for i, p in enumerate(sorted(keep))}

    paths = sorted(star_ix)
    dirs = defaultdict(list)
    for p in paths:
        top = p.split("/")[0] if "/" in p else "(root)"
        dirs[top].append(p)
    stars = []
    dir_names = sorted(dirs, key=lambda d: (-len(dirs[d]), d))
    for di, dname in enumerate(dir_names):
        angle0 = 2.0 * math.pi * di / len(dir_names)
        members = dirs[dname]
        rad = 40.0 + 13.0 * math.sqrt(len(members))
        for p in members:
            h = md5(p)
            ang = angle0 + ((h % 997) / 997.0 - 0.5) * (2.0 * math.pi / len(dir_names)) * 0.9
            r = rad * math.sqrt((h >> 12) % 1000 / 1000.0)
            cx, cy = 800 + 1.28 * rad * math.cos(angle0), 520 + 1.28 * rad * math.sin(angle0)
            stars.append({"p": p, "x": round(cx + r * math.cos(ang), 1),
                          "y": round(cy + r * math.sin(ang), 1), "d": dname})
    star_ix = {s["p"]: i for i, s in enumerate(stars)}

    for c in commits:
        c["s"] = sorted({star_ix[f] for f in c["f"] if f in star_ix})
        del c["f"]
    commits.sort(key=lambda c: c["t"])

    # --- lanes: deterministic waypoint projection, walks over real corridors ---
    lanes_out = []
    for lane, color in LANES:
        rows = trails[lane]
        events = []
        for r in rows:
            waypoint = md5(lane + r["ts"] + str(r.get("event")) + str(r.get("detail", ""))[:40]) % len(nodes)
            hit_rows = [star_ix[a] for a in (r.get("artifacts") or [])
                        if str(a).replace("\\", "/").strip() in star_ix]
            events.append({
                "t": round(r["_t"], 1), "n": waypoint,
                "e": str(r.get("event", ""))[:40],
                "a": str(r.get("actor", ""))[:30],
                "d": str(r.get("detail", ""))[:MAX_DETAIL],
                "s": sorted(set(hit_rows)),
            })
        lanes_out.append({"name": lane, "color": color, "events": events})

    t0 = min([c["t"] for c in commits] + [e["t"] for l in lanes_out for e in l["events"]])
    t1 = max([c["t"] for c in commits] + [e["t"] for l in lanes_out for e in l["events"]])

    data = {
        "nodes": nodes, "edges": edges, "stars": stars, "commits": commits,
        "lanes": lanes_out, "t0": t0, "t1": t1, "spanReplay": SPAN_REPLAY_S,
        "selfloops": selfloops,
        "meta": {
            "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "nodes": len(nodes), "edges": len(edges), "stars": len(stars),
            "commits": len(commits),
            "trail_events": sum(len(l["events"]) for l in lanes_out),
            "sources": ["memory/mycelium/graph_snapshot.json", "memory/mycelium/edges.jsonl",
                        "queue/lanes/*/trail.jsonl", "git log --name-only"],
        },
    }

    lod = compute_lod_zones(nodes, edges, stars)
    data["lod"] = lod  # ride along on the main walk too; its template ignores it

    def _safe(s):  # "</" would close an application/json script block early
        return s.replace("</", "<\\/")

    lod_body = LOD_TEMPLATE.replace("__LOD__", _safe(json.dumps(lod, separators=(",", ":"))))
    lod_body = lod_body.replace("__DATA__", _safe(json.dumps(data, separators=(",", ":"))))
    OUT_LOD.write_text(lod_body, encoding="utf-8")

    window_str = f"{datetime.fromtimestamp(t0, timezone.utc):%Y-%m-%d}..{datetime.fromtimestamp(t1, timezone.utc):%Y-%m-%d}"
    print(f"estate_walk.lod.html: {OUT_LOD.stat().st_size // 1024} KB | "
          f"zones {len(lod['zones'])} (grid {lod['grid']}x{lod['grid']}) "
          f"detail-inert-until-open | window {window_str}")
    if not lod_only:
        body = TEMPLATE.replace("__DATA__", json.dumps(data, separators=(",", ":")))
        OUT.write_text(body, encoding="utf-8")
        kb = OUT.stat().st_size // 1024
        print(f"estate_walk.html: {kb} KB | nodes {len(nodes)} edges {len(edges)} "
              f"(+{selfloops} self-loops as rings) stars {len(stars)} commits {len(commits)} "
              f"trail_events {data['meta']['trail_events']} | window {window_str}")


TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ESTATE WALK</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  html,body{margin:0;height:100%;background:#07090d;overflow:hidden;font:13px/1.4 ui-monospace,Consolas,monospace;color:#8fa3b8}
  #c{position:absolute;inset:0;cursor:grab}
  #c.drag{cursor:grabbing}
  #hud{position:absolute;top:14px;left:16px;pointer-events:none;text-shadow:0 1px 4px #000}
  #hud h1{margin:0;font-size:15px;letter-spacing:.35em;color:#d8e6f2;font-weight:600}
  #hud .sub{margin-top:4px;font-size:11px;color:#5c7186}
  #clock{position:absolute;top:14px;right:16px;text-align:right;pointer-events:none;text-shadow:0 1px 4px #000}
  #clock .t{font-size:15px;color:#ffd9a0;letter-spacing:.1em}
  #clock .w{font-size:10px;color:#54687c;margin-top:2px}
  #panel{position:absolute;left:16px;bottom:14px;right:16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;
         background:rgba(7,10,14,.82);border:1px solid #1a2634;border-radius:8px;padding:10px 14px}
  .btn{background:#101a26;border:1px solid #24384e;color:#bcd2e4;border-radius:5px;padding:4px 12px;cursor:pointer;font:inherit}
  .btn:hover{border-color:#3d5a7a;color:#eaf4fc}
  #seek{flex:1;min-width:160px;accent-color:#ffb347}
  #legend{display:flex;gap:10px;flex-wrap:wrap}
  .lane{cursor:pointer;user-select:none;padding:2px 6px;border-radius:4px;border:1px solid transparent}
  .lane.off{opacity:.28}
  .lane:hover{border-color:#24384e}
  .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;vertical-align:middle}
  #tip{position:absolute;display:none;background:rgba(9,13,19,.94);border:1px solid #24384e;border-radius:6px;
       padding:7px 10px;max-width:340px;font-size:11px;color:#a8bdd0;pointer-events:none;z-index:5}
  #tip b{color:#e8f2fa}
  #note{position:absolute;right:16px;bottom:64px;font-size:10px;color:#43566b;max-width:300px;text-align:right;pointer-events:none}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="hud"><h1>ESTATE WALK</h1><div class="sub" id="counts"></div></div>
<div id="clock"><div class="t" id="clockT">—</div><div class="w" id="clockW"></div></div>
<div id="note">lantern waypoints are a deterministic projection (trail rows carry no graph ids) — every walk follows real corridors. commits &amp; artifact pulses are placed exactly.</div>
<div id="tip"></div>
<div id="panel">
  <button class="btn" id="play">❚❚ pause</button>
  <button class="btn" id="speed">2×</button>
  <button class="btn" id="floor">floor: both</button>
  <input id="seek" type="range" min="0" max="1000" value="0">
  <div id="legend"></div>
</div>
<script>
const D = __DATA__;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const T0 = D.t0, T1 = D.t1, SPAN = D.spanReplay;
let clock = 0, playing = true, speed = 2, floor = 0; // floor: 0 both, 1 mycelium, 2 estate
const SPEEDS = [0.5, 1, 2, 4, 8];
let speedIx = 2;

// adjacency for corridor walks
const adj = D.nodes.map(() => []);
D.edges.forEach((e, i) => { adj[e[0]].push(e[1]); adj[e[1]].push(e[0]); });

function bfsPath(a, b) {
  if (a === b) return [a];
  const prev = new Array(D.nodes.length).fill(-1); prev[a] = a;
  const q = [a];
  while (q.length) {
    const u = q.shift();
    for (const v of adj[u]) if (prev[v] === -1) { prev[v] = u; if (v === b) { const p = [b]; let x = b; while (x !== a) { x = prev[x]; p.push(x); } return p.reverse(); } q.push(v); }
  }
  return [a, b];
}

// camera
let cam = { x: 0, y: 0, s: 1 };
function fit() {
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
  for (const n of D.nodes) { x0 = Math.min(x0, n.x); y0 = Math.min(y0, n.y); x1 = Math.max(x1, n.x); y1 = Math.max(y1, n.y); }
  for (const s of D.stars) { x0 = Math.min(x0, s.x); y0 = Math.min(y0, s.y); x1 = Math.max(x1, s.x); y1 = Math.max(y1, s.y); }
  const W = cv.width / devicePixelRatio, H = cv.height / devicePixelRatio;
  cam.s = Math.min(W / (x1 - x0 + 80), H / (y1 - y0 + 80)) * 0.96;
  cam.x = (x0 + x1) / 2; cam.y = (y0 + y1) / 2;
}
function resize() { cv.width = innerWidth * devicePixelRatio; cv.height = innerHeight * devicePixelRatio; cv.style.width = innerWidth + 'px'; cv.style.height = innerHeight + 'px'; if (!fitted) { fit(); fitted = true; } }
let fitted = false;
addEventListener('resize', resize); resize();

// lantern state
const lanterns = D.lanes.map((l, li) => ({ li, path: [l.events.length ? l.events[0].n : 0], seg: 0, x: 0, y: 0, trail: [], lastWaypoint: -1 }));

function laneStateAt(L, realT) {
  const evs = L.events;
  if (!evs.length) return { ix: -1, target: 0, frac: 1 };
  if (realT <= evs[0].t) return { ix: 0, target: evs[0].n, frac: 1 };
  let lo = 0, hi = evs.length - 1;
  while (lo < hi) { const m = (lo + hi + 1) >> 1; if (evs[m].t <= realT) lo = m; else hi = m - 1; }
  const gap = lo + 1 < evs.length ? evs[lo + 1].t - evs[lo].t : 1;
  const frac = lo + 1 < evs.length ? Math.min(1, (realT - evs[lo].t) / gap) : 1;
  return { ix: lo, target: evs[lo].n, frac };
}

// pulses
const pulses = []; // {x,y,t0,c,star}
function firePulse(x, y, c, star) { pulses.push({ x, y, t0: clock, c, star }); }

let lastReal = null, lastFiredCommit = 0, firedArtifacts = new Set();
function fireEvents(realT) {
  while (lastFiredCommit < D.commits.length && D.commits[lastFiredCommit].t <= realT) {
    const c = D.commits[lastFiredCommit++];
    for (const si of c.s) { const s = D.stars[si]; firePulse(s.x, s.y, '#ffd9a0', true); }
  }
  D.lanes.forEach((L, li) => {
    if (lanesOff.has(li)) return;
    for (const ev of L.events) {
      const key = li + ':' + ev.t;
      if (ev.t <= realT && !firedArtifacts.has(key)) {
        firedArtifacts.add(key);
        for (const si of ev.s || []) { const s = D.stars[si]; firePulse(s.x, s.y, L.color, true); }
      }
    }
  });
}

const lanesOff = new Set();
function buildLegend() {
  const el = document.getElementById('legend');
  D.lanes.forEach((L, li) => {
    const sp = document.createElement('span'); sp.className = 'lane';
    sp.innerHTML = '<span class="dot" style="background:' + L.color + '"></span>' + L.name + ' · ' + L.events.length;
    sp.onclick = () => { sp.classList.toggle('off'); lanesOff.has(li) ? lanesOff.delete(li) : lanesOff.add(li); };
    el.appendChild(sp);
  });
}
buildLegend();
document.getElementById('counts').textContent =
  D.meta.nodes + ' nodes · ' + D.meta.edges + ' corridors · ' + D.meta.commits + ' commits · ' +
  D.meta.stars + ' files · ' + D.meta.trail_events + ' trail events · generated ' + D.meta.generated;

// controls
const $ = id => document.getElementById(id);
$('play').onclick = () => { playing = !playing; $('play').textContent = playing ? '❚❚ pause' : '▶ play'; };
$('speed').onclick = () => { speedIx = (speedIx + 1) % SPEEDS.length; $('speed').textContent = SPEEDS[speedIx] + '×'; };
$('floor').onclick = () => { floor = (floor + 1) % 3; $('floor').textContent = 'floor: ' + ['both', 'mycelium', 'estate'][floor]; };
$('seek').oninput = e => {
  clock = (e.target.value / 1000) * SPAN;
  pulses.length = 0;
  lastFiredCommit = 0;
  while (lastFiredCommit < D.commits.length && D.commits[lastFiredCommit].t <= realT()) lastFiredCommit++;
  firedArtifacts.clear();
  D.lanes.forEach((L, li) => { for (const ev of L.events) if (ev.t <= realT()) firedArtifacts.add(li + ':' + ev.t); });
};
addEventListener('keydown', e => { if (e.code === 'Space') { e.preventDefault(); $('play').onclick(); } if (e.key === 'f') $('floor').onclick(); });

// pan/zoom
let drag = null;
cv.addEventListener('mousedown', e => { drag = { x: e.clientX, y: e.clientY, cx: cam.x, cy: cam.y }; cv.classList.add('drag'); });
addEventListener('mouseup', () => { drag = null; cv.classList.remove('drag'); });
addEventListener('mousemove', e => {
  if (drag) { cam.x = drag.cx - (e.clientX - drag.x) / cam.s; cam.y = drag.cy - (e.clientY - drag.y) / cam.s; }
  else hover(e);
});
cv.addEventListener('wheel', e => {
  e.preventDefault();
  const k = Math.exp(-e.deltaY * 0.0012);
  const wx = cam.x + (e.clientX - cv.width / (2 * devicePixelRatio)) / cam.s;
  const wy = cam.y + (e.clientY - cv.height / (2 * devicePixelRatio)) / cam.s;
  cam.s = Math.max(0.05, Math.min(12, cam.s * k));
  cam.x = wx - (e.clientX - cv.width / (2 * devicePixelRatio)) / cam.s;
  cam.y = wy - (e.clientY - cv.height / (2 * devicePixelRatio)) / cam.s;
}, { passive: false });

// hover tooltip
function hover(e) {
  const mx = cam.x + (e.clientX - cv.width / (2 * devicePixelRatio)) / cam.s;
  const my = cam.y + (e.clientY - cv.height / (2 * devicePixelRatio)) / cam.s;
  const r = 14 / cam.s; let best = null, bd = r;
  if (floor !== 2) for (const n of D.nodes) { const d = Math.hypot(n.x - mx, n.y - my); if (d < bd) { bd = d; best = { n, star: null }; } }
  if (floor !== 1) for (const s of D.stars) { const d = Math.hypot(s.x - mx, s.y - my); if (d < bd) { bd = d; best = { n: null, star: s }; } }
  const tip = document.getElementById('tip');
  if (!best) { tip.style.display = 'none'; return; }
  tip.style.display = 'block';
  tip.style.left = Math.min(e.clientX + 14, innerWidth - 360) + 'px';
  tip.style.top = (e.clientY + 14) + 'px';
  if (best.n) tip.innerHTML = '<b>' + esc(best.n.title) + '</b><br>' + best.n.type + ' · trust ' + best.n.trust;
  else tip.innerHTML = '<b>' + esc(best.star.p) + '</b><br>' + best.star.d;
}
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

function realT() { return T0 + (clock / SPAN) * (T1 - T0); }
function fmtClock(t) {
  const d = new Date(t * 1000);
  return d.toISOString().replace('T', ' ').slice(0, 16) + 'Z';
}

let prevStamp = 0;
function step(now) {
  const dt = Math.min(0.1, (now - prevStamp) / 1000 || 0); prevStamp = now;
  if (playing) {
    clock += dt * SPEEDS[speedIx];
    if (clock > SPAN) { clock = 0; firedArtifacts.clear(); lastFiredCommit = 0; pulses.length = 0; }
  }
  $('seek').value = Math.round(1000 * clock / SPAN);
  const realTcur = realT();
  $('clockT').textContent = fmtClock(realTcur);
  $('clockW').textContent = 'replay ' + (clock / SPAN * 100).toFixed(1) + '%';
  fireEvents(realTcur);

  // lantern positions
  D.lanes.forEach((L, li) => {
    const lt = lanterns[li];
    if (lanesOff.has(li)) { lt.hidden = true; return; } lt.hidden = false;
    const st = laneStateAt(L, realTcur);
    const ev = L.events[st.ix];
    if (!ev) { lt.hidden = true; return; }
    if (ev.n !== lt.lastWaypoint) {
      lt.lastWaypoint = ev.n;
      const from = lt.path[lt.path.length - 1];
      lt.path = bfsPath(from, ev.n);
      lt.seg = 0;
    }
    // walk fraction across whole path driven by frac toward next event
    const total = lt.path.length - 1;
    if (total < 1) { lt.x = D.nodes[lt.path[0]].x; lt.y = D.nodes[lt.path[0]].y; }
    else {
      const along = st.frac * total;
      lt.seg = Math.min(total - 1, Math.floor(along));
      const f = along - lt.seg;
      const a = D.nodes[lt.path[lt.seg]], b = D.nodes[lt.path[lt.seg + 1]];
      lt.x = a.x + (b.x - a.x) * f;
      lt.y = a.y + (b.y - a.y) * f;
    }
    if (playing && dt > 0) { lt.trail.push([lt.x, lt.y]); if (lt.trail.length > 26) lt.trail.shift(); }
  });

  // age pulses
  for (let i = pulses.length - 1; i >= 0; i--) if (clock - pulses[i].t0 > 2.2 || clock < pulses[i].t0) pulses.splice(i, 1);

  draw();
  requestAnimationFrame(step);
}

function draw() {
  const W = cv.width, H = cv.height;
  ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
  ctx.fillStyle = '#07090d'; ctx.fillRect(0, 0, W, H);
  ctx.setTransform(devicePixelRatio * cam.s, 0, 0, devicePixelRatio * cam.s,
    W / 2 / devicePixelRatio - cam.x * cam.s * devicePixelRatio,
    H / 2 / devicePixelRatio - cam.y * cam.s * devicePixelRatio);

  // estate floor: star field
  if (floor !== 1) {
    for (const s of D.stars) { ctx.fillStyle = '#2e3d52'; ctx.fillRect(s.x - 1.1, s.y - 1.1, 2.2, 2.2); }
  }
  // mycelium floor: corridors + nodes
  if (floor !== 2) {
    ctx.strokeStyle = '#1c2a3d'; ctx.lineWidth = 1.2 / cam.s;
    ctx.beginPath();
    for (const e of D.edges) { const a = D.nodes[e[0]], b = D.nodes[e[1]]; ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); }
    ctx.stroke();
    for (const n of D.nodes) {
      ctx.fillStyle = n.type === 'seat' ? '#33486a' : '#28394e';
      ctx.beginPath(); ctx.arc(n.x, n.y, 2.6 / Math.sqrt(cam.s), 0, 7); ctx.fill();
    }
  }
  // pulses (composite light)
  ctx.globalCompositeOperation = 'lighter';
  for (const p of pulses) {
    const age = (clock - p.t0) / 2.2;
    if (age < 0 || age > 1) continue;
    const rr = (floor === 1 ? 6 : 10) + age * 30;
    ctx.strokeStyle = p.c; ctx.globalAlpha = (1 - age) * 0.8; ctx.lineWidth = (floor === 1 ? 1.2 : 1.8) / cam.s;
    ctx.beginPath(); ctx.arc(p.x, p.y, rr / (floor === 2 ? 2.2 : 1), 0, 7); ctx.stroke();
  }
  ctx.globalAlpha = 1;
  // lanterns
  D.lanes.forEach((L, li) => {
    const lt = lanterns[li];
    if (lt.hidden) return;
    for (let i = 0; i < lt.trail.length; i++) {
      const a = i / lt.trail.length;
      ctx.globalAlpha = a * 0.22;
      ctx.fillStyle = L.color;
      ctx.beginPath(); ctx.arc(lt.trail[i][0], lt.trail[i][1], 1.6 + a * 2.4, 0, 7); ctx.fill();
    }
    ctx.globalAlpha = 0.2;
    const g = ctx.createRadialGradient(lt.x, lt.y, 0, lt.x, lt.y, 64);
    g.addColorStop(0, L.color); g.addColorStop(1, 'rgba(0,0,0,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(lt.x, lt.y, 64, 0, 7); ctx.fill();
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(lt.x, lt.y, 2.6, 0, 7); ctx.fill();
    ctx.fillStyle = L.color; ctx.beginPath(); ctx.arc(lt.x, lt.y, 4.2, 0, 7); ctx.fill();
    ctx.fillStyle = '#07090d'; ctx.beginPath(); ctx.arc(lt.x, lt.y, 1.6, 0, 7); ctx.fill();
  });
  ctx.globalCompositeOperation = 'source-over';
}
requestAnimationFrame(step);
</script>
</body>
</html>
"""

LOD_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ESTATE INDEX — zone LOD</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  html,body{margin:0;height:100%;background:#07090d;overflow:hidden;font:13px/1.4 ui-monospace,Consolas,monospace;color:#8fa3b8}
  #c{position:absolute;inset:0;cursor:grab}
  #c.drag{cursor:grabbing}
  #hud{position:absolute;top:14px;left:16px;pointer-events:none;text-shadow:0 1px 4px #000}
  #hud h1{margin:0;font-size:15px;letter-spacing:.35em;color:#d8e6f2;font-weight:600}
  #hud .sub{margin-top:4px;font-size:11px;color:#5c7186}
  #panel{position:absolute;left:16px;bottom:14px;right:16px;display:flex;gap:14px;align-items:center;flex-wrap:wrap;
         background:rgba(7,10,14,.82);border:1px solid #1a2634;border-radius:8px;padding:10px 14px}
  .btn{background:#101a26;border:1px solid #24384e;color:#bcd2e4;border-radius:5px;padding:4px 12px;cursor:pointer;font:inherit}
  .btn:hover{border-color:#3d5a7a;color:#eaf4fc}
  #state{font-size:11px;color:#54687c}
  #tip{position:absolute;display:none;background:rgba(9,13,19,.94);border:1px solid #24384e;border-radius:6px;
       padding:7px 10px;max-width:360px;font-size:11px;color:#a8bdd0;pointer-events:none;z-index:5}
  #tip b{color:#e8f2fa}
  #note{position:absolute;right:16px;bottom:64px;font-size:10px;color:#43566b;max-width:300px;text-align:right;pointer-events:none}
</style>
</head>
<body>
<canvas id="c"></canvas>
<div id="hud"><h1>ESTATE INDEX</h1><div class="sub" id="counts"></div></div>
<div id="note">zone LOD — the index starts from summaries only; the full estate payload sits inert below until a zone is opened.</div>
<div id="tip"></div>
<div id="panel">
  <button class="btn" id="back">&larr; overview</button>
  <button class="btn" id="all">expand: full estate</button>
  <span id="state">detail: not loaded</span>
</div>
<script type="application/json" id="full">__DATA__</script>
<script>
const LOD = __LOD__;
const cv = document.getElementById('c'), ctx = cv.getContext('2d');
const $ = id => document.getElementById(id);
let full = null;              // lazily JSON.parse'd estate payload
let mode = 'overview', zoneIx = -1;

function ensureFull() {
  if (full) return full;
  full = JSON.parse($('full').textContent);
  $('state').textContent = 'detail: loaded · ' + full.meta.nodes + ' nodes · ' +
    full.meta.edges + ' corridors · ' + full.meta.stars + ' stars';
  return full;
}
$('counts').textContent = LOD.zones.length + ' zones · grid ' + LOD.grid + '×' + LOD.grid +
  ' · overview parses summaries only';

// camera
let cam = { x: 0, y: 0, s: 1 };
const [BX0, BY0, BX1, BY1] = LOD.bounds;
function fitRect(x0, y0, x1, y1) {
  const W = cv.width / devicePixelRatio, H = cv.height / devicePixelRatio;
  cam.s = Math.min(W / Math.max(1, x1 - x0 + 80), H / Math.max(1, y1 - y0 + 80)) * 0.94;
  cam.x = (x0 + x1) / 2; cam.y = (y0 + y1) / 2;
}
function resize() { cv.width = innerWidth * devicePixelRatio; cv.height = innerHeight * devicePixelRatio; cv.style.width = innerWidth + 'px'; cv.style.height = innerHeight + 'px'; if (!fitted) { fit(); fitted = true; } }
let fitted = false;
function fit() { fitRect(BX0, BY0, BX1, BY1); }
addEventListener('resize', resize); resize();

function openZone(i) {
  const z = LOD.zones[i]; ensureFull();
  mode = 'zone'; zoneIx = i;
  fitRect(z.x, z.y, z.x + z.w, z.y + z.h);
}
function openAll() { ensureFull(); mode = 'full'; zoneIx = -1; fit(); }
function backToOverview() { mode = 'overview'; zoneIx = -1; fit(); }
$('back').onclick = backToOverview;
$('all').onclick = openAll;
addEventListener('keydown', e => { if (e.key === 'Escape') backToOverview(); });

function inView(p) {
  if (mode !== 'zone') return true;
  const z = LOD.zones[zoneIx];
  return p.x >= z.x && p.x < z.x + z.w && p.y >= z.y && p.y < z.y + z.h;
}

// pan/zoom (click opens a zone only when the pointer stayed put)
let drag = null, moved = false;
cv.addEventListener('mousedown', e => { drag = { x: e.clientX, y: e.clientY, cx: cam.x, cy: cam.y }; moved = false; cv.classList.add('drag'); });
addEventListener('mouseup', () => { drag = null; cv.classList.remove('drag'); });
addEventListener('mousemove', e => {
  if (drag) {
    if (Math.abs(e.clientX - drag.x) + Math.abs(e.clientY - drag.y) > 4) moved = true;
    cam.x = drag.cx - (e.clientX - drag.x) / cam.s; cam.y = drag.cy - (e.clientY - drag.y) / cam.s;
  } else hover(e);
});
cv.addEventListener('wheel', e => {
  e.preventDefault();
  const k = Math.exp(-e.deltaY * 0.0012);
  const wx = cam.x + (e.clientX - cv.width / (2 * devicePixelRatio)) / cam.s;
  const wy = cam.y + (e.clientY - cv.height / (2 * devicePixelRatio)) / cam.s;
  cam.s = Math.max(0.05, Math.min(12, cam.s * k));
  cam.x = wx - (e.clientX - cv.width / (2 * devicePixelRatio)) / cam.s;
  cam.y = wy - (e.clientY - cv.height / (2 * devicePixelRatio)) / cam.s;
}, { passive: false });
cv.addEventListener('click', e => {
  if (moved) return;
  if (mode === 'overview') {
    const m = worldAt(e);
    const z = LOD.zones.find(z => m.x >= z.x && m.x < z.x + z.w && m.y >= z.y && m.y < z.y + z.h);
    if (z && (z.n || z.s)) openZone(z.id);
  }
});
function worldAt(e) {
  return { x: cam.x + (e.clientX - cv.width / (2 * devicePixelRatio)) / cam.s,
           y: cam.y + (e.clientY - cv.height / (2 * devicePixelRatio)) / cam.s };
}

// hover tooltip
function hover(e) {
  const m = worldAt(e), tip = $('tip');
  const show = html => { tip.style.display = 'block'; tip.style.left = Math.min(e.clientX + 14, innerWidth - 380) + 'px'; tip.style.top = (e.clientY + 14) + 'px'; tip.innerHTML = html; };
  if (mode === 'overview') {
    const z = LOD.zones.find(z => m.x >= z.x && m.x < z.x + z.w && m.y >= z.y && m.y < z.y + z.h);
    if (!z) { tip.style.display = 'none'; return; }
    const dom = Object.keys(z.types).map(k => k + '×' + z.types[k]).join(' · ');
    show('<b>zone ' + z.id + '</b> — click to open<br>' + z.n + ' nodes · ' + z.e +
      ' internal corridors · ' + z.s + ' stars<br>' + (dom || 'empty') +
      (z.top.length ? '<br>' + z.top.map(esc).join('<br>') : ''));
    return;
  }
  const r = 12 / cam.s; let best = null, bd = r;
  if (mode !== 'full') for (const n of full.nodes) {
    if (!inView(n)) continue;
    const d = Math.hypot(n.x - m.x, n.y - m.y); if (d < bd) { bd = d; best = { n, star: null }; }
  }
  for (const s of full.stars) {
    if (!inView(s)) continue;
    const d = Math.hypot(s.x - m.x, s.y - m.y); if (d < bd) { bd = d; best = { n: null, star: s }; }
  }
  if (!best) { tip.style.display = 'none'; return; }
  show(best.n ? '<b>' + esc(best.n.title) + '</b><br>' + best.n.type + ' · trust ' + best.n.trust
              : '<b>' + esc(best.star.p) + '</b><br>' + best.star.d);
}
function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); }

function maxCount() { return Math.max(1, ...LOD.zones.map(z => z.n + z.s)); }

function draw() {
  const W = cv.width, H = cv.height;
  ctx.setTransform(devicePixelRatio, 0, 0, devicePixelRatio, 0, 0);
  ctx.fillStyle = '#07090d'; ctx.fillRect(0, 0, W, H);
  ctx.setTransform(devicePixelRatio * cam.s, 0, 0, devicePixelRatio * cam.s,
    W / 2 / devicePixelRatio - cam.x * cam.s * devicePixelRatio,
    H / 2 / devicePixelRatio - cam.y * cam.s * devicePixelRatio);
  if (mode === 'overview') drawOverview(); else drawDetail();
}

function drawOverview() {
  const mx = maxCount();
  ctx.strokeStyle = '#1a2634'; ctx.lineWidth = 1 / cam.s;
  ctx.strokeRect(BX0, BY0, BX1 - BX0, BY1 - BY0);
  for (const z of LOD.zones) {
    const hot = (z.n + z.s) / mx;
    ctx.fillStyle = z.e >= z.s ? 'rgba(63,94,133,' + (0.10 + hot * 0.40).toFixed(3) + ')'
                               : 'rgba(74,86,112,' + (0.08 + hot * 0.32).toFixed(3) + ')';
    ctx.fillRect(z.x, z.y, z.w, z.h);
    ctx.strokeStyle = '#22344a'; ctx.lineWidth = 1 / cam.s;
    ctx.strokeRect(z.x, z.y, z.w, z.h);
    ctx.fillStyle = '#7d93a9'; ctx.font = (11 / cam.s) + 'px ui-monospace,Consolas,monospace';
    ctx.fillText('Z' + z.id + (mode === 'overview' && zoneIx === z.id ? ' ●' : ''), z.x + 6 / cam.s, z.y + 15 / cam.s);
    ctx.fillStyle = '#54687c';
    ctx.fillText(z.n + 'n ' + z.e + 'e ' + z.s + 's', z.x + 6 / cam.s, z.y + 30 / cam.s);
  }
}

function drawDetail() {
  if (mode === 'zone') {
    const z = LOD.zones[zoneIx];
    ctx.strokeStyle = '#3d5a7a'; ctx.lineWidth = 1.5 / cam.s;
    ctx.strokeRect(z.x, z.y, z.w, z.h);
  }
  ctx.strokeStyle = '#1c2a3d'; ctx.lineWidth = 1 / cam.s;
  ctx.beginPath();
  for (const e of full.edges) {
    const a = full.nodes[e[0]], b = full.nodes[e[1]];
    if (!inView(a) || !inView(b)) continue;
    ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y);
  }
  ctx.stroke();
  for (const n of full.nodes) {
    if (!inView(n)) continue;
    ctx.fillStyle = n.type === 'seat' ? '#33486a' : '#28394e';
    ctx.beginPath(); ctx.arc(n.x, n.y, 2.4 / Math.sqrt(cam.s), 0, 7); ctx.fill();
  }
  for (const s of full.stars) {
    if (!inView(s)) continue;
    ctx.fillStyle = '#2e3d52'; ctx.fillRect(s.x - 1.1, s.y - 1.1, 2.2, 2.2);
  }
}
requestAnimationFrame(draw);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    sys.exit(build(lod_only="--lod-only" in sys.argv))
