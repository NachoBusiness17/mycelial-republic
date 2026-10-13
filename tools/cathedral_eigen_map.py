"""cathedral_eigen_map — render the in-game map FROM the curvature scan's eigen_centroids.

The queue candidate build (2026-09-21, promoted 09-26): overlay position/distance/
bearing on the walker view, paired with the referee outcome (water_first = operative
lean, RIB CONTESTED stands — see watch/inbox/REFEREE_VERDICT_20260926.md).

Solid segment  = wired cross-region exit exists (both builders' world).
Via segment    = reachable through wired hops, no direct exit (thin line).
Dashed segment = MISSING STITCH: the walk demands an edge that does not exist
                 (the contested difference; identities per the referee criterion).

Output: watch/inbox/CATHEDRAL_EIGEN_MAP_20260926.html (self-contained, no deps).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools.cathedral_walk import HUB_FIRST, REGIONS, WATER_FIRST, bfs_hops, edges, load, owner_map  # noqa: E402

SCAN = ROOT / "watch" / "inbox" / "CATHEDRAL_CURVATURE_SCAN_20260921.json"
OUT = ROOT / "watch" / "inbox" / "CATHEDRAL_EIGEN_MAP_20260926.html"

CLASS_COLOR = {"SADDLE": "#d9a441", "DARK": "#5b4b8a", "HILL": "#4c9a6a"}


def load_scan() -> dict:
    return json.loads(SCAN.read_text(encoding="utf-8"))


def scale(points: dict[str, list[float]], w: float, h: float, pad: float) -> dict[str, tuple[float, float]]:
    xs = [p[0] for p in points.values()]
    ys = [p[1] for p in points.values()]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    sx = (w - 2 * pad) / max(x1 - x0, 1e-9)
    sy = (h - 2 * pad) / max(y1 - y0, 1e-9)
    return {k: (pad + (p[0] - x0) * sx, pad + (p[1] - y0) * sy) for k, p in points.items()}


def bearing(a: tuple[float, float], b: tuple[float, float]) -> float:
    deg = math.degrees(math.atan2(b[0] - a[0], -(b[1] - a[1])))  # 0 = north, clockwise
    return round((deg + 360.0) % 360.0, 1)


def route_segments(order: list[str], wired: set, owner: dict, pos: dict) -> list[dict]:
    segs = []
    for i in range(len(order) - 1):
        a, b = order[i], order[i + 1]
        path = bfs_hops({r: set() for r in []} if False else _adj(wired), a, b)
        if path is None:
            kind, via = "missing", [b]
        elif len(path) == 2:
            kind, via = "wired", []
        else:
            kind, via = "via", path[1:-1]
        dist = round(math.dist(pos[a], pos[b]), 1)
        segs.append({"a": a, "b": b, "kind": kind, "via": via,
                     "dist": dist, "bearing": bearing(pos[a], pos[b])})
    return segs


def _adj(wired: set) -> dict[str, set]:
    adj: dict[str, set] = {r: set() for r in REGIONS}
    for a, b in wired:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj


def main() -> int:
    scan = load_scan()
    mods = load()
    owner = owner_map(mods)
    wired = edges(mods, owner)
    cents = {k: v for k, v in scan["eigen_centroids"].items() if k in REGIONS and len(v) >= 2}
    missing = [r for r in REGIONS if r not in cents]
    W, H, PAD = 920.0, 640.0, 70.0
    pos = scale(cents, W, H, PAD)
    # routes render only over mapped regions; stub modules without an eigen
    # centroid are off-map by construction (recorded, not silently dropped)
    water_order = [r for r in WATER_FIRST if r in pos]
    hub_order = [r for r in HUB_FIRST if r in pos]
    off_route = sorted({r for r in WATER_FIRST + HUB_FIRST if r not in pos})
    water = route_segments(water_order, wired, owner, pos)
    hub = route_segments(hub_order, wired, owner, pos)

    def polyline(segs: list[dict], color: str, width: float, dash: str, opacity: float) -> list[str]:
        out = []
        for s in segs:
            a, b = pos[s["a"]], pos[s["b"]]
            if s["kind"] == "missing":
                out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                           f'stroke="{color}" stroke-width="{width}" stroke-dasharray="7 5" opacity="{opacity}"/>')
            elif s["kind"] == "via":
                pts = [a] + [pos[v] for v in s["via"]] + [b]
                pl = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
                out.append(f'<polyline points="{pl}" fill="none" stroke="{color}" stroke-width="{max(width - 1, 0.8)}" '
                           f'opacity="{opacity * 0.8}"/>')
            else:
                out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                           f'stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>')
        return out

    nodes = []
    for rid, p in pos.items():
        info = scan["regions"].get(rid, {})
        cls = info.get("class", "?")
        cos = info.get("cos")
        color = CLASS_COLOR.get(cls, "#888")
        r_node = 13 if rid != "water_computer" else 16
        nodes.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r_node}" fill="{color}" stroke="#111" stroke-width="1.2"/>')
        label = f'{rid} ({cls}{"" if cos is None else f" cos {cos}"})'
        nodes.append(f'<text x="{p[0] + 16:.1f}" y="{p[1] - 10:.1f}" font-size="12" fill="#222">{label}</text>')
    for rid in missing:
        nodes.append(f'<text x="{W - 40}" y="{H - 20}" font-size="11" fill="#777">off-map (no eigen centroid): {", ".join(missing)}</text>')
    if off_route:
        nodes.append(f'<text x="16" y="{H - 60}" font-size="11" fill="#777">route regions outside eigen space (not drawn): {", ".join(off_route)}</text>')

    hop_rows = "".join(
        f'<tr><td>{i + 1}</td><td>{s["a"]} &#8594; {s["b"]}</td><td>{s["kind"]}</td>'
        f'<td>{s["dist"]}</td><td>{s["bearing"]}&deg;</td></tr>'
        for i, s in enumerate(water))

    wired_n = len({tuple(sorted(e)) for e in wired})
    missing_water = sum(1 for s in water if s["kind"] == "missing")
    missing_hub = sum(1 for s in hub if s["kind"] == "missing")
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Cathedral eigen-map — water_first operative lean</title>
<style>
body {{ font-family: Georgia, serif; background: #f7f4ee; color: #222; margin: 24px; }}
h1 {{ font-size: 20px; }} .ref {{ background: #efe9dc; border-left: 4px solid #d9a441; padding: 8px 12px; font-size: 13px; }}
svg {{ background: #fbf9f4; border: 1px solid #ddd; }}
table {{ border-collapse: collapse; font-size: 12px; }} td, th {{ border: 1px solid #ccc; padding: 3px 8px; }}
</style></head><body>
<h1>The Cathedral in eigen-coordinates — descent map (2026-09-26)</h1>
<p class="ref"><b>Referee (GLM prime, cold, 09-26):</b> water_first, confidence 0.6 — a LEAN, not a proof.
Saddle-law ruling: a third vote adds a fourth path; the RIB descent-order invariant stays CONTESTED.
Settlement path: raise adventure_2d6 cosine +0.017 to the 0.5 HILL bar (cheapest hill) and render
riddler_engram on-manifold. Full verdict: watch/inbox/REFEREE_VERDICT_20260926.md</p>
<svg width="{W:.0f}" height="{H:.0f}" viewBox="0 0 {W:.0f} {H:.0f}">
{''.join(polyline(hub, '#8a7fb0', 1.6, '2 4', 0.45))}
{''.join(polyline(water, '#b3562c', 2.4, '', 0.95))}
{''.join(nodes)}
<text x="16" y="{H - 46}" font-size="11" fill="#b3562c">solid/dashed rust = water_first chain (operative lean; dashed = missing stitch)</text>
<text x="16" y="{H - 30}" font-size="11" fill="#8a7fb0">faint violet = hub_first star (alternate, CONTESTED)</text>
<text x="16" y="{H - 14}" font-size="11" fill="#555">wired cross-region edges: {wired_n} &middot; water_first demands {missing_water} stitches, hub_first {missing_hub} &middot; &beta;0 wired vs intended per scan</text>
</svg>
<h2>water_first hop table (position &middot; distance &middot; bearing in eigen units)</h2>
<table><tr><th>#</th><th>hop</th><th>segment</th><th>dist (eigen)</th><th>bearing</th></tr>{hop_rows}</table>
<p>Region positions are the scan's eigen_centroids (top-2 singular directions of the doctrine corpus,
spectrum head: {json.dumps(scan['eigen_spectrum_top'][:4])}). Colors: amber SADDLE, violet DARK, green HILL.
Generator: tools/cathedral_eigen_map.py (deterministic; data: CATHEDRAL_CURVATURE_SCAN_20260921.json + wired module exits).</p>
</body></html>"""
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.name}: {len(REGIONS)} regions, wired edges {wired_n}, "
          f"water stitches {missing_water}, hub stitches {missing_hub}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
