"""B2-17 independent recompute of the Cathedral curvature cosines.

Reimplements tools/curvature_scan.py build_sections+curvature from the
documented method (blank-line paragraphs, first-match keyword assignment in
declared order, [a-z0-9_]{3,} term counters, cosine = common-dot over full
norms, round 3). Reads the raw normals bytes directly. Also recomputes the
settlement arithmetic and the walk-compare DEBT counts from the kifu files.
No import of the original tool: independent by construction.
"""
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRI = ROOT / "memory" / "runs" / "combined_game_triangulation"
INBOX = ROOT / "watch" / "inbox"

KEYS = {
    "adventure_2d6": ["2d6", "ford", "river", "adventure"],
    "water_computer": ["water", "cistern", "valve", "tank", "hydraulic"],
    "fractal_maze": ["fractal", "maze", "recursion", "refract"],
    "riddler_optics": ["optics", "lens", "garage", "light"],
    "riddler_engram": ["engram", "summon", "card", "memory"],
    "audit_dungeon": ["audit", "doctrine", "library"],
}


def build_sections(path):
    txt = path.read_text(encoding="utf-8", errors="replace")
    blocks = {r: [] for r in KEYS}
    assigned = {r: 0 for r in KEYS}
    for para in re.split(r"\n\s*\n", txt):
        low = para.lower()
        for r, kws in KEYS.items():
            if any(k in low for k in kws):
                blocks[r].append(low)
                assigned[r] += 1
                break
    counters = {r: Counter(re.findall(r"[a-z0-9_]{3,}", " ".join(v)))
                for r, v in blocks.items() if v}
    return counters, assigned


def cosine(g, d):
    common = set(g) & set(d)
    num = sum(g[t] * d[t] for t in common)
    den = math.sqrt(sum(v * v for v in g.values())) * \
          math.sqrt(sum(v * v for v in d.values()))
    return (num / den) if den else 0.0


grok, ga = build_sections(TRI / "version_grok.md")
deep, da = build_sections(TRI / "version_deepseek.md")
print("paragraph assignments (grok):", ga)
print("paragraph assignments (deepseek):", da)
print("sections present grok:", sorted(grok))
print("sections present deepseek:", sorted(deep))

mine = {}
for r in KEYS:
    g, d = grok.get(r), deep.get(r)
    if not g or not d:
        mine[r] = None  # DARK
        print(f"{r:16s} DARK (missing section: grok={r in grok} deep={r in deep})")
        continue
    c = round(cosine(g, d), 3)
    mine[r] = c
    print(f"{r:16s} cos={c:.3f}  |grok|terms={len(g)} |deep|terms={len(d)} "
          f"common={len(set(g) & set(d))}")

scan = json.loads((INBOX / "CATHEDRAL_CURVATURE_SCAN_20260921.json").read_text(encoding="utf-8"))
scan22 = json.loads((INBOX / "CATHEDRAL_CURVATURE_SCAN_20260922.json").read_text(encoding="utf-8"))
print("\nfiled vs recomputed:")
ok = True
for r, c in scan["regions"].items():
    filed, m = c["cos"], mine.get(r)
    match = (filed == m) or (filed is None and m is None)
    ok = ok and match
    print(f"  {r:16s} filed={filed} recomputed={m} match={match}")

a2d6 = mine["adventure_2d6"]
bar = 0.5
delta = round(bar - a2d6, 3)
gaps = {r: round(bar - v, 3) for r, v in mine.items() if v is not None}
cheapest = min(gaps, key=gaps.get)
print(f"\nsettlement arithmetic: bar {bar} - adventure_2d6 {a2d6} = +{delta}")
print(f"gaps to HILL bar: {gaps}")
print(f"cheapest hill = {cheapest} (gap {gaps[cheapest]})")

dv21, dv22 = scan["descent_vote"], scan22["descent_vote"]
print(f"\ndescent_vote 09-21: chain {dv21['water_first_chain_len']} vs star {dv21['hub_first_star_len']}"
      f"  -> shorter: {dv21['shorter_in_own_metric']}")
print(f"descent_vote 09-22: chain {dv22['water_first_chain_len']} vs star {dv22['hub_first_star_len']}"
      f"  -> shorter: {dv22['shorter_in_own_metric']}")

for name, want_steps, want_debt in [("WALK_WATERFIRST_20260921.md", 17, 4),
                                    ("WALK_HUBFIRST_20260921.md", 17 + 2, 6)]:
    t = (INBOX / name).read_text(encoding="utf-8")
    steps = int(re.search(r"steps taken \(incl\. gate work\): \*\*(\d+)\*\*", t).group(1))
    debts = t.count("[DEBT]")
    print(f"{name}: declared steps={steps} (want {want_steps}) DEBT markers={debts} (want {want_debt})")
print("\nALL REGION COSINES REPRODUCE:", ok)
