"""TOOL GENOME PROJECT - analysis pass over tool_genome_data.json."""
import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "tool_genome_data.json"), encoding="utf-8"))
G = D["genomes"]
for g in G.values():
    g["callers"] = [c for c in g["callers"] if "__init__" not in c]
G.pop("__init__", None)

live = {n: g for n, g in G.items() if not g["death"]}
print(f"analysis population: {len(G)} tools (excl __init__), live={len(live)}")

# --- caller / test / fossil distributions
callers_n = {n: len(g["callers"]) for n, g in G.items()}
tests_n = {n: len(g["test_files"]) for n, g in G.items()}
rec_n = {n: g["receipt_files"] for n, g in G.items()}
print("\n== TOP 20 callers (clean) ==")
for n, c in sorted(callers_n.items(), key=lambda kv: -kv[1])[:20]:
    print(f"{c:4d} callers {tests_n[n]:3d} tests {rec_n[n]:4d} receiptfiles  {n}")
print("\n== TOP 15 by receipt files (fossil record) ==")
for n, c in sorted(rec_n.items(), key=lambda kv: -kv[1])[:15]:
    print(f"{c:5d} receiptfiles {callers_n[n]:3d} callers  {n}")

zero_caller = [n for n in live if callers_n[n] == 0]
zero_fossil = [n for n in live if rec_n[n] == 0]
dead_end = [n for n in live if callers_n[n] == 0 and rec_n[n] == 0
            and tests_n[n] == 0]
print(f"\nlive tools with ZERO code callers: {len(zero_caller)}")
print(f"live tools with ZERO fossil mentions: {len(zero_fossil)}")
print(f"live tools with NO callers, NO fossils, NO tests: {len(dead_end)}")
print("dead ends:", ", ".join(sorted(dead_end)))

testcov = [n for n in live if tests_n[n] > 0]
print(f"\nimmune-covered live tools: {len(testcov)}/{len(live)}")
print("covered:", ", ".join(sorted(testcov)))

# --- mag ancestry: which mag modules do tools import
magc = Counter()
for g in G.values():
    for m in g["imports_mag"]:
        magc[m.split(".")[0] + "." + (m.split(".")[1] if "." in m else "")] += 1
print("\n== TOP 15 mag.* ancestors imported by tools ==")
for m, c in magc.most_common(15):
    print(f"{c:4d} tools import {m}")
notools_mag = [n for n, g in G.items() if not g["imports_mag"]]
print(f"tools importing NO mag.* at all: {len(notools_mag)}")

# --- third-party ancestry
extc = Counter()
for g in G.values():
    for m in g["imports_other"]:
        extc[m] += 1
print("\n== third-party gene families (top 15) ==")
print(extc.most_common(15))

# --- birth histogram by ISO week
weeks = Counter()
for n, g in G.items():
    if g["birth"]:
        d = datetime.strptime(g["birth"], "%Y-%m-%d")
        wk = (d - timedelta(days=d.weekday())).date().isoformat()
        weeks[wk] += 1
print("\n== births per week (week-start Monday) ==")
for w, c in sorted(weeks.items()):
    print(f"{w}  {'#' * c} {c}")

# --- cohort survival: orphan rate by month
cohort = defaultdict(lambda: [0, 0])
for n, g in G.items():
    if g["birth"]:
        mth = g["birth"][:7]
        cohort[mth][0] += 1
        if n in dead_end:
            cohort[mth][1] += 1
print("\n== cohort size vs dead-ends by month ==")
for m in sorted(cohort):
    tot, de = cohort[m]
    print(f"{m}: born {tot:3d}, now dead-ends {de:3d} ({100 * de // max(tot,1)}%)")

# --- genome size
locs = sorted(((g["loc"], n) for n, g in G.items()), reverse=True)
print(f"\n== genome size: total LOC {sum(l for l, _ in locs)}, "
      f"max {locs[0]}, min {locs[-1]} ==")
print("largest 10:", [(n, l) for l, n in locs[:10]])

# --- speciation: tools with real child imports (the flat graph)
child = Counter({n: len(g["import_children"]) for n, g in G.items()
                 if g["import_children"]})
print("\n== import graph edges total ==",
      sum(len(g["import_children"]) for g in G.values()))
print("tools with >=1 import child:", len(child))

# --- contamination audit for top claims
for probe in ("filesystem", "shell", "research", "swarm_tools", "autopilot",
              "steer_grok_whole", "pile_classify", "pupeteer_gauntlet",
              "sense_tools", "tier_probe"):
    g = G.get(probe)
    if not g:
        continue
    print(f"\n-- {probe}: callers sample ({len(g['callers'])})")
    for c in g["callers"][:8]:
        print("   ", c)

# --- scheduled metabolism: tools named from scripts/*.ps1
ps1 = set()
for n, g in G.items():
    for c in g["callers"]:
        if c.startswith("scripts/") and c.endswith((".ps1", ".cmd", ".bat")):
            ps1.add(n)
print(f"\ntools invoked from scripts/ shell+task layer: {len(ps1)}")
print(sorted(ps1))
