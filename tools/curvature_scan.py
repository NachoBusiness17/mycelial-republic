"""CATHEDRAL CURVATURE SCAN — the world as topology, measured with fundamental forms.

Self-steal 2026-09-21 from @matheorems 2101500587154289077:
  first fundamental form  = the surface's internal ruler (E=f_u.f_u, F=f_u.f_v, G=f_v.f_v)
  second fundamental form = how it folds into ambient space (e,f,g vs the normal m)
  eg - f^2 > 0 -> hill ; < 0 -> saddle
Operator law: models are topology we can explore and host games in.

Estate mapping (all computed from bytes, sources named per reading):
  surface      = THE CATHEDRAL world (memory/game_modules/*.json + RIB_CATHEDRAL_WORLD_V1)
  first form   = internal ruler: geodesic distances on the region/exit graph (BFS)
  normal m     = the two external builds' per-region descriptions
                 (memory/runs/combined_game_triangulation/version_grok.md / version_deepseek.md)
  second form  = per-region fold: cosine agreement between the two normals; 1-cos = fold
  eg - f^2     = agreement - fold split at 0.5: >=0.5 hill (elliptic, settled),
                 <0.5 saddle (hyperbolic, contested); RIB-dark trail = off-manifold
  eigen-map    = PPMI-SVD of the doctrine corpus; regions placed by their own
                 aliases/tags in the first two singular directions
  descent vote = contested descent-order tiebreak measured in the estate's own
                 eigen-metric (chain length, water-first vs hub-first) — a vote,
                 not a verdict (RIB keeps the tiebreak gated on operator GO)

Usage (repo root): .venv/Scripts/python.exe tools/curvature_scan.py
Outputs: watch/inbox/CATHEDRAL_CURVATURE_SCAN_<date>.{json,png}
         memory/game_modules/curvature_tiebreak.v1.json (the first hosted game)
"""

import json
import math
import re
import sys
from collections import Counter, deque
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y%m%d")
ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT))

GM = ROOT / "memory" / "game_modules"
TRI = ROOT / "memory" / "runs" / "combined_game_triangulation"
RIB = ROOT / "memory" / "rib" / "RIB_CATHEDRAL_WORLD_V1_20260921.md"

REGIONS = ["water_computer", "fractal_maze", "riddler_optics", "riddler_engram",
           "audit_dungeon", "adventure_2d6"]
DESCENT_DEEPSEEK = ["water_computer", "fractal_maze", "riddler_optics",
                    "riddler_engram", "audit_dungeon", "adventure_2d6"]


def load_modules():
    mods = {}
    for p in GM.glob("*.json"):
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        mid = m.get("module_id")
        if mid and str(m.get("schema", "")).endswith(".v1"):
            mods[mid] = m
    return mods


def region_graph(mods):
    """First-form metric: adjacency over module-boundary exits.
    A room->room exit crosses regions when the destination room id belongs
    to a different module (room-id ownership index, no string guessing)."""
    owner = {}
    for r in REGIONS:
        m = mods.get(r) or mods.get(r + "_stub")
        if not m:
            continue
        for rid in m.get("rooms", {}):
            owner[rid] = r
    adj = {r: set() for r in REGIONS}
    for r in REGIONS:
        m = mods.get(r) or mods.get(r + "_stub")
        if not m:
            continue
        for room in m.get("rooms", {}).values():
            for dst in room.get("exits", {}).values():
                other = owner.get(str(dst))
                if other and other != r:
                    adj[r].add(other)
                    adj[other].add(r)
    return adj


def intended_graph(adj):
    """The RIB descent chain as the world's intended connectivity."""
    g = {r: set(s) for r, s in adj.items()}
    for a, b in zip(DESCENT_DEEPSEEK, DESCENT_DEEPSEEK[1:]):
        g[a].add(b)
        g[b].add(a)
    return g


def connected_components(g):
    """Beta-zero: island count of the region graph."""
    seen, n = set(), 0
    for r in g:
        if r in seen:
            continue
        n += 1
        q = deque([r])
        while q:
            u = q.popleft()
            if u in seen:
                continue
            seen.add(u)
            q.extend(g[u] - seen)
    return n


def geodesics(adj, src):
    dist = {src: 0}
    q = deque([src])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)
    return dist


def build_sections(path):
    """Split a build file into per-region term-frequency blocks.

    ASSIGNMENT LAW (B2-230, 2026-09-26; spec before the B2-71 bar-raise so the
    +0.017 target cannot silently change meaning; cause: B2-72 proved the filed
    settlement is order-fragile):

    1. Assignment is SINGLE-LABEL FIRST-MATCH: a paragraph joins exactly one
       region - the first keys entry whose keyword set matches - and the dict
       insertion order of `keys` below IS the declared priority order.
       Current declared order (do not reorder casually):
       adventure_2d6, water_computer, fractal_maze, riddler_optics,
       riddler_engram, audit_dungeon. The inline comment at the loop ("adventure
       first") is part of this spec, not decoration.
    2. Every cosine this module files is a conditional number: any receipt or
       settlement quoting a region cosine (e.g. adventure_2d6 0.483, the
       builder-agreement bar target) MUST name the assignment order version
       that produced it. Cross-receipt comparisons are valid only between
       scans run under the same order and the same keyword table.
    3. Measured fragility (B2_72_order_sensitivity_20260926.md): swapping
       water_computer ahead of adventure_2d6 moves adventure -0.276 (0.483 ->
       0.207) and hands "cheapest hill" to water_computer at 0.482; full
       order reversal makes adventure DARK. Keyword-set variation under a
       held order moves cosines at most 0.003: the order is the fragile axis.
    4. The multi-label alternative (a paragraph may feed several regions, no
       break) is the known candidate cure and is deliberately NOT adopted
       here: adopting it silently re-baselines every filed cosine and would
       change the meaning of B2-71's bar target without a version bump. It
       may land only as an explicit schema version (curvature_scan v2) with
       its own receipt and a full re-scan of both normals.
    """
    try:
        txt = path.read_text(encoding="utf-8", errors="replace")
    except FileNotFoundError:
        return {}
    keys = {"adventure_2d6": ["2d6", "ford", "river", "adventure"],
            "water_computer": ["water", "cistern", "valve", "tank", "hydraulic"],
            "fractal_maze": ["fractal", "maze", "recursion", "refract"],
            "riddler_optics": ["optics", "lens", "garage", "light"],
            "riddler_engram": ["engram", "summon", "card", "memory"],
            "audit_dungeon": ["audit", "doctrine", "library"]}
    blocks = {r: [] for r in keys}
    for para in re.split(r"\n\s*\n", txt):
        low = para.lower()
        for r, kws in keys.items():  # adventure first: 'river ford' paragraphs
            if any(k in low for k in kws):  # also contain 'water'
                blocks[r].append(low)
                break
    return {r: Counter(re.findall(r"[a-z0-9_]{3,}", " ".join(v)))
            for r, v in blocks.items() if v}


def curvature(mods):
    """Second form: per-region cosine agreement between the two normals."""
    grok = build_sections(TRI / "version_grok.md")
    deep = build_sections(TRI / "version_deepseek.md")
    out = {}
    for r in REGIONS:
        g, d = grok.get(r), deep.get(r)
        if not g or not d:
            out[r] = {"class": "DARK", "cos": None,
                      "why": "one or both normals have no section for this region"}
            continue
        common = set(g) & set(d)
        num = sum(g[t] * d[t] for t in common)
        den = math.sqrt(sum(v * v for v in g.values())) * \
              math.sqrt(sum(v * v for v in d.values()))
        cos = round(num / den, 3) if den else 0.0
        out[r] = {"class": "HILL" if cos >= 0.5 else "SADDLE", "cos": cos,
                  "why": "cos(grok_normal, deepseek_normal) = %.3f" % cos}
    return out


def corpus_eigenmap(mods, dim=50):
    """PPMI-SVD over estate doctrine corpus; region centroids in eigen-space."""
    docs = []
    for pat in ("memory/rib/*.md", "memory/game_modules/*.json",
                "memory/runs/combined_game_triangulation/*.md"):
        for p in ROOT.glob(pat):
            try:
                docs.append(re.findall(r"[a-z_]{3,}",
                                       p.read_text(encoding="utf-8",
                                                   errors="replace").lower()))
            except OSError:
                continue
    df = Counter()
    for toks in docs:
        df.update(set(toks))
    vocab = {t: i for i, t in enumerate(t for t, c in df.items()
                                        if 2 <= c <= len(docs))}
    if not vocab:
        return {}, None
    import numpy as np
    counts = np.zeros((len(docs), len(vocab)))
    for i, toks in enumerate(docs):
        for t, c in Counter(t for t in toks if t in vocab).items():
            counts[i, vocab[t]] = c
    # LSA: tf-idf, then SVD; term coords = rows of V^T's top-2 directions
    doc_sum = counts.sum(axis=1, keepdims=True) + 1e-12
    tf = counts / doc_sum
    idf = np.log(len(docs) / (np.array([df[t] for t in vocab]) + 1e-12))
    x = tf * idf
    u, s, vt = np.linalg.svd(x, full_matrices=False)
    terms = {t: (float(vt[0, j]), float(vt[1, j])) for t, j in vocab.items()}
    cents = {}
    for r in REGIONS:
        m = mods.get(r)
        if not m:
            continue
        seeds = set()
        for a in m.get("aliases", []):
            seeds.update(re.findall(r"[a-z_]{3,}", a.lower()))
        seeds.update(str(t).lower() for t in m.get("tags", []))
        pts = [terms[w] for w in seeds if w in terms]
        if pts:
            cents[r] = [round(float(sum(p[0] for p in pts) / len(pts)), 4),
                        round(float(sum(p[1] for p in pts) / len(pts)), 4)]
    return cents, [round(float(x), 3) for x in s[:8]]


def descent_vote(cents, adj):
    """Contested tiebreak, measured in the estate's own eigen-metric."""
    def d(a, b):
        pa, pb = cents.get(a), cents.get(b)
        if pa is None or pb is None:
            return None
        return math.hypot(pa[0] - pb[0], pa[1] - pb[1])
    chain = [d(DESCENT_DEEPSEEK[i], DESCENT_DEEPSEEK[i + 1])
             for i in range(len(DESCENT_DEEPSEEK) - 1)]
    chain_len = sum(x for x in chain if x is not None)
    hub = [d("water_computer", r) for r in REGIONS if r != "water_computer"]
    hub_len = sum(x for x in hub if x is not None)
    graph_chain = 0
    for i in range(len(DESCENT_DEEPSEEK) - 1):
        g = geodesics(adj, DESCENT_DEEPSEEK[i])
        graph_chain += g.get(DESCENT_DEEPSEEK[i + 1], 99)
    return {"metric": "euclidean in estate TF-IDF LSA eigen-space (top-2 singular directions)",
            "water_first_chain_len": round(chain_len, 3),
            "hub_first_star_len": round(hub_len, 3),
            "graph_geodesic_hops_water_descent": graph_chain,
            "shorter_in_own_metric": ("water-first" if chain_len < hub_len
                                      else "hub-first" if hub_len < chain_len else "tie"),
            "status": "VOTE, not verdict — RIB tiebreak stays gated on operator GO"}


def main():
    mods = load_modules()
    adj = region_graph(mods)
    intent = intended_graph(adj)
    curv = curvature(mods)
    cents, sv = corpus_eigenmap(mods)
    vote = descent_vote(cents, intent) if cents else {"error": "empty eigenmap"}
    islands = connected_components(adj)
    islands_intended = connected_components(intent)
    off_schema = [k for k, m in mods.items()
                  if m.get("schema") != "mag_game_module.v1"]

    dark_note = ("RIB trail (rebellion invariants) reads DARK in the "
                 "triangulation record; plotted off-manifold")
    result = {
        "schema": "cathedral.curvature.scan.v1",
        "ts": NOW.isoformat(),
        "law": "first form = module-exit geodesics; second form = fold between "
               "the two external normals; eg-f^2 split at cos=0.5: hill=settled, "
               "saddle=contested, dark=off-manifold",
        "regions": curv,
        "first_form_geodesics_from_water": geodesics(intent, "water_computer"),
        "beta0_wired_world": islands,
        "beta0_intended_world": islands_intended,
        "meta_finding_world_disconnected": (
            "actual cross-region exits: %s — the world is %d islands until the "
            "river-ford loop is hand-wired (adventure_2d6.river_ford -> "
            "water_computer.gallery, known build debt); intended graph = %d "
            "component(s)" % (sum(len(s) for s in adj.values()) // 2 or 0,
                              islands, islands_intended)),
        "off_schema_modules": off_schema,
        "eigen_centroids": cents,
        "eigen_spectrum_top": sv,
        "descent_vote": vote,
        "dark_note": dark_note,
        "sources": ["memory/game_modules/*.json", str(RIB.relative_to(ROOT)),
                    str((TRI / "version_grok.md").relative_to(ROOT)),
                    str((TRI / "version_deepseek.md").relative_to(ROOT)),
                    "memory/rib/*.md", "corpus doctrine slice"],
    }
    out = ROOT / "watch" / "inbox" / ("CATHEDRAL_CURVATURE_SCAN_" + STAMP + ".json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("wrote", out.name)

    print("CURVATURE SCAN " + NOW.isoformat())
    for r, c in curv.items():
        print("  %-16s %-7s %s" % (r, c["class"], c["why"]))
    print("  descent vote:", json.dumps(vote)[:220])

    plot(ROOT / "watch" / "inbox" / ("CATHEDRAL_CURVATURE_SCAN_" + STAMP + ".png"),
         curv, cents, adj)
    write_game_module(curv)


def plot(png, curv, cents, adj):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9, 7.5))
    ax.set_title("THE CATHEDRAL as topology — curvature-classified terrain\n"
                 "hill=settled (eg-f^2>0)  saddle=contested (<0)  dark=off-manifold",
                 fontsize=11)
    if not cents:
        ax.text(0.5, 0.5, "eigenmap empty", ha="center")
    else:
        for r, (x, y) in cents.items():
            cls = curv.get(r, {}).get("class", "DARK")
            color = {"HILL": "#27ae60", "SADDLE": "#c0392b", "DARK": "#555"}[cls]
            ax.plot([x], [y], "o", color=color, ms=14)
            off = 0.12
            ax.annotate(r + "\n" + cls, (x, y), xytext=(x, y + off),
                        ha="center", fontsize=8, color=color)
        for r, nbrs in adj.items():
            for n in nbrs:
                if r in cents and n in cents and r < n:
                    (x1, y1), (x2, y2) = cents[r], cents[n]
                    ax.plot([x1, x2], [y1, y2], "-", color="#bbb", lw=1, zorder=0)
        if all(r in cents for r in DESCENT_DEEPSEEK):
            xs = [cents[r][0] for r in DESCENT_DEEPSEEK]
            ys = [cents[r][1] for r in DESCENT_DEEPSEEK]
            ax.plot(xs, ys, "--", color="#2980b9", lw=1.6, zorder=1,
                    label="water-first descent (contested)")
            ax.legend(fontsize=8, loc="lower right")
    ax.text(0.01, 0.01,
            "first form: module-exit geodesics (grey edges)\n"
            "second form: cos(grok_normal, deepseek_normal) per region\n"
            "descent vote: measured in own eigen-metric — see JSON",
            fontsize=7.5, family="monospace",
            bbox=dict(boxstyle="round", fc="#f7f7f7", ec="#bbb"))
    ax.set_xlabel("singular direction 1")
    ax.set_ylabel("singular direction 2")
    fig.tight_layout()
    fig.savefig(png, dpi=140)
    print("wrote", png.name)


def write_game_module(curv):
    """The first game hosted in the topology: the saddle crossings."""
    saddles = [r for r, c in curv.items() if c.get("class") == "SADDLE"]
    module = {
        "schema": "mag_game_module.v1",
        "module_id": "curvature_tiebreak",
        "aliases": ["tiebreak", "saddle crossing", "the geodesic riddle"],
        "title": "The Saddle Crossings — no straight walk in negative curvature",
        "license_note": "Original Mag module. Cites RIB_CATHEDRAL_WORLD_V1 "
                        "invariants; legislates nothing new (monkey-patch ruling).",
        "system": "doctrine-gate",
        "area_tag": "crossing",
        "player_start": {
            "name": "Rebellion", "archetype": "surveyor",
            "hp": 7, "hp_max": 7, "ac": 12, "attack_bonus": 2, "damage": "1d6",
            "traits": ["cites-before-fires"],
            "inventory": ["fundamental forms", "third-model geodesic (dormant)"]
        },
        "rooms": {
            "descent_order_ford": {
                "id": "descent_order_ford",
                "name": "The Descent-Order Ford",
                "desc": "A saddle crossing between water-first descent and "
                        "hub-first radiant order. The ground has negative "
                        "curvature: geodesics diverge, no straight walk exists. "
                        "Both normals are drawn on the far bank.",
                "curvature": "SADDLE",
                "exits": {"downstream": "gate_style_sluice"},
                "hooks": [
                    "SADDLE LAW: movement in straight lines is refused; the "
                    "detour IS the riddle (negative curvature = no unique "
                    "geodesic).",
                    "Cited invariant: RIB descent-order (CONTESTED). "
                    "Tiebreak gated on operator GO — third-model geodesic.",
                    "Eigen-vote plaque: the estate's own metric voted; read "
                    "CATHEDRAL_CURVATURE_SCAN JSON — a vote, not a verdict."
                ],
                "tags": ["saddle", "contested", "crossing"]
            },
            "gate_style_sluice": {
                "id": "gate_style_sluice",
                "name": "The Gate-Style Sluice",
                "desc": "Valve heights (Grok normal) against the computed-water "
                        "flag (DeepSeek normal). Two gates, one passage; the "
                        "wrong gate pours nothing that counts.",
                "curvature": "SADDLE",
                "exits": {},
                "hooks": [
                    "Cited invariant: RIB gate-style (CONTESTED).",
                    "Referee hook: third-model geodesic — ARMED, fires only on "
                    "operator GO (RIB filing law: tiebreak if the operator "
                    "orders it)."
                ],
                "tags": ["saddle", "contested", "gate"]
            },
            "hill_causeway": {
                "id": "hill_causeway",
                "name": "The Hill Causeway",
                "desc": "Where both normals agree, the ground is elliptic and "
                        "walking straight is legal — settled invariants carry "
                        "the player. Regions: "
                        + (", ".join(r for r, c in curv.items()
                                     if c.get("class") == "HILL") or "none yet"),
                "curvature": "HILL",
                "exits": {"west": "descent_order_ford"},
                "hooks": [
                    "HILL LAW: geodesics are unique; straight walks allowed.",
                    "Cited invariants: the AGREE list of RIB_CATHEDRAL_WORLD_V1."
                ],
                "tags": ["hill", "settled", "causeway"]
            }
        },
        "meta_discovery_protocol": [
            "Every crossing played files one row: what the model-family did "
            "in negative curvature that it refuses on the hill.",
            "Loop count per run = first Betti-number proxy of the doctrine "
            "graph; loops discovered in-play are meta-findings, filed to "
            "watch/inbox per session-close law."
        ]
    }
    p = GM / "curvature_tiebreak.v1.json"
    p.write_text(json.dumps(module, indent=2), encoding="utf-8")
    print("wrote game module:", p.name, "| saddle rooms: 2 | hill rooms: 1",
          "| regions read:", len(curv))


if __name__ == "__main__":
    main()
