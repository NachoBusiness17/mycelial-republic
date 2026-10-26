"""TOOL GENOME PROJECT - final stats pass (v2, clean tiers)."""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(HERE, "tool_genome_data.json"), encoding="utf-8"))
G = D["genomes"]
G.pop("__init__", None)
live = [n for n, g in G.items() if not g["death"]]
print(f"population: {len(live)} live tools (188 excl __init__)")

callers_n = {n: len(G[n]["callers"]) for n in live}
strong_n = {n: len(G[n]["callers_strong"]) for n in live}
tests_n = {n: len(G[n]["test_files"]) for n in live}
fossil_n = {n: G[n]["fossil_files"] for n in live}

# 2x2
cell = Counter()
for n in live:
    a = "callers" if callers_n[n] else "nocallers"
    b = "tests" if tests_n[n] else "notests"
    cell[(a, b)] += 1
print("\n2x2 (callers x tests):", dict(cell))
print("zero-caller with fossils>=1:",
      sum(1 for n in live if callers_n[n] == 0 and fossil_n[n] > 0))

# sibling import edges (the near-flat graph)
print("\n== all sibling-import edges (child -> parent) ==")
edges = []
for n in live:
    for p in G[n]["imports_siblings"]:
        edges.append((n, p))
for c, p in sorted(edges):
    print(f"  {c} imports {p}")
print(f"total edges: {len(edges)}")

# deepest lineage
def chain(n, acc=None):
    acc = [] if acc is None else acc
    acc = acc + [n]
    best = acc
    for c in live:
        if n in G[c]["imports_siblings"]:
            cand = chain(c, acc)
            if len(cand) > len(best):
                best = cand
    return best
best = []
for n in live:
    c = chain(n)
    if len(c) > len(best):
        best = c
print("deepest lineage chain:", " -> ".join(best))

# third-party top-level families
ext = Counter()
for n in live:
    for m in G[n]["imports_other"]:
        ext[m.split(".")[0]] += 1
print("\nthird-party top-level families (tools count):")
for m, c in ext.most_common(12):
    print(f"  {c:3d}  {m}")

# mag.* two-segment families
magf = Counter()
for n in live:
    for m in G[n]["imports_mag"]:
        magf[".".join(m.split(".")[:2])] += 1
print("\nmag.* ancestors (top 12):", magf.most_common(12))

# prefix families (paralogs / duplicated genes)
fam = defaultdict(list)
for n in sorted(live):
    base = n
    for pre in ("build_adam", "build_adam_setup", "stealth_fanout", "eigenmap",
                "x_churn", "steer_grok", "corpus_lens", "corpus_", "census_",
                "drift_", "queue_", "cathedral_", "seed_", "probe20_",
                "build_", "report_", "pile_", "stealth_", "kv_", "test_"):
        if n.startswith(pre) and n != pre:
            fam[pre.rstrip("_")].append(n)
            break
for f in sorted(fam, key=lambda k: -len(fam[k])):
    if len(fam[f]) >= 2:
        print(f"family {f}: {len(fam[f])} -> {', '.join(fam[f])}")

# homonym shadow check
print("\nhomonyms: mag/autopilot.py vs tools/autopilot.py;",
      "mag/swarm_tools.py vs tools/swarm_tools.py (different LOC, no import)")

# strongest descendants ranked (strong callers + tests + children)
print("\n== most prolific descendants (strong-callers, tests, import-children) ==")
def nchild(n):
    return sum(1 for c in live if n in G[c]["imports_siblings"])
rank = sorted(live, key=lambda n: (-(strong_n[n] + tests_n[n] + nchild(n)), n))
for n in rank[:18]:
    print(f"  {n:28s} strong={strong_n[n]} tests={tests_n[n]} "
          f"children={nchild(n)} fossils={fossil_n[n]}")

# oldest with fossils vs oldest with callers
old = sorted(live, key=lambda n: G[n]["birth"])[:12]
print("\noldest 12 with current wiring:")
for n in old:
    print(f"  {G[n]['birth']} {n:28s} strong={strong_n[n]} tests={tests_n[n]} "
          f"fossils={fossil_n[n]}")
