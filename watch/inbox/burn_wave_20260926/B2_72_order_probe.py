"""B2-72 keyword-order sensitivity probe for tools/curvature_scan.py build_sections.

Question: build_sections assigns each paragraph to the FIRST region whose
keyword set matches (tools/curvature_scan.py:140-145, adventure_2d6 declared
before water_computer at :133-134). adventure_2d6 sits at cos 0.483, +0.017
under the 0.5 HILL bar. Does that +0.017 margin survive if the assignment
order is swapped or the keyword sets are varied?

Method: faithful reimplementation of build_sections (same blank-line split,
errors="replace" read, any-keyword first-match with break, [a-z0-9_]{3,}
token counters, common-dot cosine over full norms, round 3), parameterized by
an ORDERED config so order is an experimental variable. Baseline must
reproduce the filed scan bit-for-bit before any variant counts.
No import of the production tool: independent by construction (B2-17 precedent).
"""
import json
import math
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TRI = ROOT / "memory" / "runs" / "combined_game_triangulation"
INBOX = ROOT / "watch" / "inbox"

ADV = ["2d6", "ford", "river", "adventure"]
WAT = ["water", "cistern", "valve", "tank", "hydraulic"]

BASELINE = [
    ("adventure_2d6", ADV),
    ("water_computer", WAT),
    ("fractal_maze", ["fractal", "maze", "recursion", "refract"]),
    ("riddler_optics", ["optics", "lens", "garage", "light"]),
    ("riddler_engram", ["engram", "summon", "card", "memory"]),
    ("audit_dungeon", ["audit", "doctrine", "library"]),
]

VARIANTS = {
    "baseline_as_shipped": BASELINE,
    "swap_water_first": [BASELINE[1], BASELINE[0]] + BASELINE[2:],
    "full_reverse_order": BASELINE[::-1],
    "kw_adv_minus_river": [("adventure_2d6", [k for k in ADV if k != "river"])]
                          + BASELINE[1:],
    "kw_adv_minus_river_ford": [("adventure_2d6", ["2d6", "adventure"])]
                               + BASELINE[1:],
    "kw_adv_minus_adventure": [("adventure_2d6", ["2d6", "ford", "river"])]
                              + BASELINE[1:],
    "kw_water_plus_river_ford_order_same":
        [BASELINE[0], ("water_computer", WAT + ["river", "ford"])] + BASELINE[2:],
    "swap_plus_adv_minus_river_ford":
        [("water_computer", WAT), ("adventure_2d6", ["2d6", "adventure"])]
        + BASELINE[2:],
}


def build_sections(path, cfg):
    txt = path.read_text(encoding="utf-8", errors="replace")
    blocks = {r: [] for r, _ in cfg}
    assigned = {r: 0 for r, _ in cfg}
    for para in re.split(r"\n\s*\n", txt):
        low = para.lower()
        for r, kws in cfg:
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


def run(cfg):
    grok, ga = build_sections(TRI / "version_grok.md", cfg)
    deep, da = build_sections(TRI / "version_deepseek.md", cfg)
    out = {}
    for r, _ in cfg:
        g, d = grok.get(r), deep.get(r)
        if not g or not d:
            out[r] = {"cos": None, "gp": ga[r], "dp": da[r]}
            continue
        out[r] = {"cos": cosine(g, d), "gp": ga[r], "dp": da[r],
                  "gt": len(g), "dt": len(d),
                  "common": len(set(g) & set(d))}
    return out


def gap(c):
    return None if c is None else round(0.5 - c, 3)


base = run(VARIANTS["baseline_as_shipped"])

# 0. gate: baseline must equal the filed scan bit-for-bit
scan = json.loads((INBOX / "CATHEDRAL_CURVATURE_SCAN_20260921.json")
                  .read_text(encoding="utf-8"))
print("== baseline gate vs filed CATHEDRAL_CURVATURE_SCAN_20260921.json ==")
gate_ok = True
for r, c in scan["regions"].items():
    filed = c["cos"]
    mine = None if base[r]["cos"] is None else round(base[r]["cos"], 3)
    ok = filed == mine
    gate_ok = gate_ok and ok
    print("  %-16s filed=%s recomputed=%s match=%s" % (r, filed, mine, ok))
print("  GATE:", "PASS" if gate_ok else "FAIL")

ba = base["adventure_2d6"]["cos"]
bw = base["water_computer"]["cos"]
print("  unrounded: adventure_2d6 cos=%.8f  margin_to_bar=%.8f" % (ba, 0.5 - ba))
print("  unrounded: water_computer cos=%.8f  margin_to_bar=%.8f" % (bw, 0.5 - bw))

# 1. contested-boundary census: paragraphs matching BOTH families
print("\n== contested paragraphs (both families present) ==")
for name in ("version_grok.md", "version_deepseek.md"):
    txt = (TRI / name).read_text(encoding="utf-8", errors="replace")
    n = 0
    for para in re.split(r"\n\s*\n", txt):
        low = para.lower()
        if any(k in low for k in ADV) and any(k in low for k in WAT):
            n += 1
            head = " ".join(para.split())[:90]
            print("  %s: %s" % (name, head))
    print("  %s contested total: %d" % (name, n))

# 2. variant table
print("\n== variant run table ==")
hdr = "%-38s %-27s %-27s %s" % ("variant", "adventure_2d6", "water_computer",
                                "cheapest-to-bar")
print(hdr)
rows = []
for name, cfg in VARIANTS.items():
    res = base if name == "baseline_as_shipped" else run(cfg)
    a, w = res["adventure_2d6"], res["water_computer"]
    gaps = {r: (0.5 - v["cos"]) for r, v in res.items() if v["cos"] is not None}
    cheapest = min(gaps, key=gaps.get)
    ca = "DARK" if a["cos"] is None else "%.3f (%+.3f) %s p=%d/%d" % (
        a["cos"], a["cos"] - ba,
        "HILL" if a["cos"] >= 0.5 else "SADDLE", a["gp"], a["dp"])
    cw = "DARK" if w["cos"] is None else "%.3f (%+.3f) %s p=%d/%d" % (
        w["cos"], w["cos"] - bw,
        "HILL" if w["cos"] >= 0.5 else "SADDLE", w["gp"], w["dp"])
    print("%-38s %-27s %-27s %s(%.3f)" % (name, ca, cw, cheapest,
                                          gaps[cheapest]))
    rows.append({"variant": name, "adv_cos": None if a["cos"] is None
                 else round(a["cos"], 3), "adv_delta": None if a["cos"] is None
                 else round(a["cos"] - ba, 3),
                 "adv_class": None if a["cos"] is None
                 else ("HILL" if a["cos"] >= 0.5 else "SADDLE"),
                 "adv_paras": [a["gp"], a["dp"]],
                 "water_cos": None if w["cos"] is None
                 else round(w["cos"], 3),
                 "water_delta": None if w["cos"] is None
                 else round(w["cos"] - bw, 3),
                 "water_class": None if w["cos"] is None
                 else ("HILL" if w["cos"] >= 0.5 else "SADDLE"),
                 "water_paras": [w["gp"], w["dp"]],
                 "cheapest_to_bar": cheapest,
                 "cheapest_gap": round(gaps[cheapest], 3)})

# 3. settlement robustness: rank of adventure_2d6 among all regions, per variant
print("\n== settlement robustness (adventure_2d6 rank by gap to 0.5) ==")
for row in rows:
    print("  %-38s cheapest=%s gap=%.3f  adv_gap=%.3f class=%s" % (
        row["variant"], row["cheapest_to_bar"], row["cheapest_gap"],
        0.5 - (row["adv_cos"] or 0), row["adv_class"]))

(INBOX / "burn_wave_20260926" / "B2_72_results.json").write_text(
    json.dumps({"baseline_gate_pass": gate_ok,
                "adv_baseline_full": ba, "water_baseline_full": bw,
                "rows": rows}, indent=2), encoding="utf-8")
print("\nwrote B2_72_results.json")
