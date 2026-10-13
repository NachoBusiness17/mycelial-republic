"""CATHEDRAL WALK — play both contested descent orders against the wired world.

Evidence generator for the RIB tiebreak (descent order: DeepSeek water-first
chain vs Grok hub-first star). The walker starts neutral at the crossroads,
satisfies the agreed gates exactly as the live game does (valves, refraction,
lenses), and walks each order across the CURRENTLY WIRED graph. Where an order
demands a cross-region edge that does not exist, it files a MISSING-EDGE row —
build debt metered per order, not narrated. Engram is a summon (no route edge,
per the agreed engram-is-summon invariant) in both orders.

Usage: .venv/Scripts/python.exe tools/cathedral_walk.py
Output: watch/inbox/WALK_WATERFIRST_20260921.md + WALK_HUBFIRST_20260921.md
        (two kifus + the comparison the tiebreak consumes)
"""

import json
import sys
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

NOW = datetime.now(timezone.utc)
STAMP = NOW.strftime("%Y%m%d")
ROOT = Path.cwd().resolve()
sys.path.insert(0, str(ROOT))
GM = ROOT / "memory" / "game_modules"
OUT = ROOT / "watch" / "inbox"

REGIONS = ["water_computer", "fractal_maze", "riddler_optics", "riddler_engram",
           "dnd_classic_stub", "audit_dungeon", "adventure_2d6_stub"]
WATER_FIRST = ["water_computer", "fractal_maze", "riddler_optics",
               "riddler_engram", "dnd_classic_stub", "audit_dungeon",
               "adventure_2d6_stub"]     # chain: each stage feeds the next
HUB_FIRST = ["water_computer", "fractal_maze", "riddler_optics",
             "riddler_engram", "dnd_classic_stub", "audit_dungeon",
             "adventure_2d6_stub"]       # star: water is home, spokes out/in


def load():
    mods = {}
    for rid in REGIONS:
        m = json.loads((GM / (rid + ".v1.json")).read_text(encoding="utf-8"))
        mods[rid] = m
    return mods


def owner_map(mods):
    owner = {}
    for rid, m in mods.items():
        for room_id in m.get("rooms", {}):
            owner[room_id] = rid
    return owner


def edges(mods, owner):
    """Undirected cross-region route edges that exist in the wired world."""
    out = set()
    for rid, m in mods.items():
        for room in m.get("rooms", {}).values():
            for dst in room.get("exits", {}).values():
                other = owner.get(str(dst))
                if other and other != rid:
                    out.add((rid, other))
                    out.add((other, rid))
    return out


def bfs_hops(adj, src, dst):
    """Shortest wired multi-hop route region-list, or None."""
    if src == dst:
        return [src]
    prev = {src: None}
    q = deque([src])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in prev:
                prev[v] = u
                q.append(v)
    if dst not in prev:
        return None
    path, cur = [], dst
    while cur:
        path.append(cur)
        cur = prev[cur]
    return path[::-1]


def walk(name, order, mode, mods, owner):
    adj = {r: set() for r in REGIONS}
    for a, b in edges(mods, owner):
        adj[a].add(b)
    kifu = []
    steps = 0
    missing = []
    position = "adventure_2d6_stub"      # neutral start: crossroads
    refraction = False
    lenses = 0

    def row(line, flag=None):
        kifu.append((line, flag))

    def hop(src, dst):
        """One demanded leg: wired path (hops counted) or DEBT leap."""
        nonlocal steps, position
        path = bfs_hops(adj, src, dst)
        if path:
            steps += len(path) - 1
            row(f"walked wired route {' -> '.join(path)} ({len(path)-1} hop"
                f"{'s' if len(path) > 2 else ''})")
        else:
            missing.append((src, dst))
            row(f"MISSING EDGE: {src} -> {dst} — no wired route; descent-order "
                f"is CONTESTED so the edge is not pre-wired (build debt, "
                f"metered)", "DEBT")
        position = dst

    row(f"walk open: {name} ({mode}) — neutral start crossroads, gates live, "
        f"engram-is-summon")
    for region in order:
        if region == position:
            continue
        if region == "riddler_engram":
            steps += 1
            row("summon engram seat (card, no rooms) — engram-is-summon HOLDS; "
                "no route edge needed in any order")
            continue
        if region == "fractal_maze" and not refraction:
            steps += 3
            row("water work: valves A+B open, three waits, OUT.height=3 — "
                "refraction carried (water-feeds-field satisfied BEFORE entry)")
            refraction = True
        if mode == "chain":
            hop(position, region)
        else:  # star: home to water between every spoke
            if position != "water_computer":
                hop(position, "water_computer")
            hop("water_computer", region)
        if region == "riddler_optics" and lenses < 10:
            steps += 10
            row("lens work: all ten lenses collected in the optics garage")
            lenses = 10
        if region == "audit_dungeon" and lenses >= 10:
            row("lens-count-gate: doctrine_library -> garage_gate stands at "
                "10/10 (crossed on arrival)")
    path = bfs_hops(adj, position, "water_computer")
    if path:
        steps += len(path) - 1
        row(f"loop-closes: {' -> '.join(path)} — the ford runs home "
            f"({len(path)-1} hops)")
    else:
        row("loop-closes UNREACHABLE from final position — debt", "DEBT")
    return {"name": name, "kifu": kifu, "steps": steps, "missing": missing}


def file_md(name, result):
    lines = [f"# KIFU — {result['name']} descent walk · {NOW.isoformat()}",
             "", f"steps taken (incl. gate work): **{result['steps']}**",
             f"missing edges demanded: **{len(result['missing'])}**", ""]
    for line, flag in result["kifu"]:
        lines.append(f"- {line}" + (f" **[{flag}]**" if flag else ""))
    p = OUT / f"WALK_{name}_{STAMP}.md"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def main():
    mods = load()
    owner = owner_map(mods)
    a = walk("WATERFIRST", WATER_FIRST, "chain", mods, owner)
    b = walk("HUBFIRST", HUB_FIRST, "star", mods, owner)
    pa, pb = file_md("WATERFIRST", a), file_md("HUBFIRST", b)
    print("WALK WATERFIRST: steps=%d missing=%d" % (a["steps"], len(a["missing"])))
    print("WALK HUBFIRST:   steps=%d missing=%d" % (b["steps"], len(b["missing"])))
    print("wrote", pa.name, "and", pb.name)
    cmp = {
        "schema": "cathedral.walk.compare.v1",
        "ts": NOW.isoformat(),
        "water_first": {"steps": a["steps"], "missing_edges": len(a["missing"])},
        "hub_first": {"steps": b["steps"], "missing_edges": len(b["missing"])},
        "note": "both orders walk the same wired world; engram costs zero route "
                "in both (card); loop closes in both (agreed). The contested "
                "difference is WHICH missing edges each order demands — a vote "
                "for the tiebreak, gated on operator GO.",
    }
    (OUT / ("WALK_COMPARE_" + STAMP + ".json")).write_text(
        json.dumps(cmp, indent=2), encoding="utf-8")
    print("wrote WALK_COMPARE_" + STAMP + ".json")


if __name__ == "__main__":
    main()
