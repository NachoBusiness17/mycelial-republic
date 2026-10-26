"""numerology-6-7 lane audit: how often do 6 and 7 appear in the estate's own numbers?

Three surfaces, all byte-read from the repo:
  A. test-census claims in AGENTS.md (the tests-N claims the clippy bullet carries)
  B. leaf/session/ledger counts measured live from estate ledgers
  C. every small integer stored in a bounded set of structured state files
     (trails, rollups, warm_state, registries) -> terminal-digit histogram
     and a chi-square against uniform terminal digits for values >= 10
  D. prose mentions of 60-79 and of the pairs 5-6 / 6-7 / 7-8 in watch/inbox + memory/rib

Honest instrument note: terminal-digit uniformity is the standard check used in
digit-preference auditing (Nigrini's forensic work); it is a heuristic here, and
sample sizes are small, so the output reports raw counts next to every statistic.
No em-dashes in this file or its output.
"""
import json, os, re, sys
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

def rel(*parts):
    return os.path.join(ROOT, *parts)

out = []

def say(s=""):
    out.append(s)
    print(s)

def count_lines(path):
    n = 0
    with open(rel(path), "rb") as f:
        for _ in f:
            n += 1
    return n

def walk_json_ints(node, bucket):
    if isinstance(node, bool):
        return
    if isinstance(node, int):
        if abs(node) < 100000:
            bucket.append(node)
        return
    if isinstance(node, float):
        return
    if isinstance(node, dict):
        for v in node.values():
            walk_json_ints(v, bucket)
        return
    if isinstance(node, list):
        for v in node:
            walk_json_ints(v, bucket)

say("=== NUMEROLOGY 6-7 ESTATE AUDIT ===")
say("repo: " + ROOT)

# --- A. census claims in AGENTS.md -------------------------------------------
say("")
say("--- A. test-census claims in AGENTS.md ---")
agents = open(rel("AGENTS.md"), encoding="utf-8", errors="replace").read()
census = re.findall(r"([\d][\d,]*)\s+tests", agents)
census_vals = [int(c.replace(",", "")) for c in census]
say("claims matching '<N> tests': " + repr(census_vals))
# patrol grammar: 'read N ... / M files'
patrol = re.findall(r"read\s+([\d,]+)\s*(?:/\s*([\d,]+))?", agents)
patrol_vals = []
for a, b in patrol:
    if a and a.replace(",", "").isdigit():
        patrol_vals.append(int(a.replace(",", "")))
    if b and b.replace(",", "").isdigit():
        patrol_vals.append(int(b.replace(",", "")))
say("patrol-grammar numbers (collected/files pairs): " + repr(patrol_vals))
all_census = census_vals + patrol_vals
ends67 = [v for v in all_census if v % 10 in (6, 7)]
say("census numbers ending in 6 or 7: %d of %d (%.1f%%); expected under uniform last digit: 20%%"
    % (len(ends67), len(all_census), 100.0 * len(ends67) / max(1, len(all_census))))
say("which ones: " + repr(ends67))

# --- B. live leaf/session/ledger counts ---------------------------------------
say("")
say("--- B. leaf/session/ledger counts measured live ---")
live = {}
live["catalog/catalog.jsonl rows"] = count_lines("catalog/catalog.jsonl")
live["catalog/tags.jsonl rows"] = count_lines("catalog/tags.jsonl")
live["catalog/junctions.jsonl rows"] = count_lines("catalog/junctions.jsonl")
live["memory/workflows/REGISTRY.jsonl rows"] = count_lines("memory/workflows/REGISTRY.jsonl")
live["queue/lanes dir count (lanes)"] = len([d for d in os.listdir(rel("queue/lanes")) if os.path.isdir(rel("queue/lanes", d))])
live["watch/inbox subdir count (intake sessions)"] = len([d for d in os.listdir(rel("watch/inbox")) if os.path.isdir(rel("watch/inbox", d))])
live["memory/rib .md count (ribs)"] = len([f for f in os.listdir(rel("memory/rib")) if f.endswith(".md")])
live["watch/inbox .md count (receipts)"] = sum(len([f for f in fs if f.endswith(".md")]) for _, _, fs in os.walk(rel("watch/inbox")))
lane_rows = {}
for lane in sorted(os.listdir(rel("queue/lanes"))):
    tp = rel("queue/lanes", lane, "trail.jsonl")
    if os.path.isfile(tp):
        with open(tp, "rb") as f:
            lane_rows[lane] = sum(1 for _ in f)
live["lane trail rows per lane"] = lane_rows
for k, v in live.items():
    say("%s = %s" % (k, v))

# --- C. structured small integers from bounded state files --------------------
say("")
say("--- C. small integers from structured estate state ---")
state_files = [
    "memory/warm_state.json",
    "memory/workflows/REGISTRY.jsonl",
    "memory/percolator/invariants.json",
    "memory/lenses/corpus_index.json",
    "dashboard/static/index_data/rollup.json",
    "dashboard/static/index_data/last_run.json",
    "watch/ESTATE_INDEX/rollup.json",
    "watch/ESTATE_INDEX/last_run.json",
    "memory/game/FLOW_LEDGER.jsonl",
    "memory/burns/LEDGER.jsonl",
]
ints = []
for sf in state_files:
    p = rel(sf)
    if not os.path.isfile(p):
        say("missing: " + sf)
        continue
    try:
        text = open(p, encoding="utf-8", errors="replace").read()
        if sf.endswith(".jsonl"):
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    walk_json_ints(json.loads(line), ints)
                except Exception:
                    pass
        else:
            walk_json_ints(json.loads(text), ints)
        say("read: %s" % sf)
    except Exception as e:
        say("error reading %s: %s" % (sf, e))
say("structured ints collected: %d (raw, with repeats); distinct: %d" % (len(ints), len(set(ints))))
c_small = Counter(i for i in ints if 0 <= i < 100000)
say("value frequencies, 0..20 and 66..68: " + repr({v: c_small[v] for v in sorted(set(list(range(0, 21)) + [66, 67, 68])) if c_small[v]}))
multi = [abs(i) for i in ints if abs(i) >= 10 and abs(i) < 100000]
dig = Counter(i % 10 for i in multi)
say("multi-digit ints (>=10): %d; terminal-digit histogram: %s" % (len(multi), {d: dig[d] for d in range(10)}))
if len(multi) >= 50:
    n = len(multi)
    exp = n / 10.0
    chi2 = sum((dig[d] - exp) ** 2 / exp for d in range(10))
    say("chi-square vs uniform terminal digits: %.2f, df=9 (p=0.05 critical value 16.919, standard table)" % chi2)
# birthday paradox under uniform terminal digit
say("")
for K in (10, 20, 50, len(multi)):
    if K > 0:
        say("P(at least one of %d uniform-terminal-digit counts ends in 6 or 7) = %.4f" % (K, 1 - 0.8 ** K))

# --- D. prose mentions ---------------------------------------------------------
say("")
say("--- D. prose mentions in watch/inbox/**/*.md + memory/rib/*.md ---")
prose_files = []
for base in ("watch/inbox", "memory/rib"):
    for dirpath, _, files in os.walk(rel(base)):
        for f in files:
            if f.endswith(".md"):
                prose_files.append(os.path.join(dirpath, f))
say("prose files scanned: %d" % len(prose_files))
two = Counter()
pairs = Counter()
pair_re = re.compile(r"\b([4-8])[-/]([4-8])\b")
two_re = re.compile(r"\b(6[0-9]|7[0-9])\b")
for pf in prose_files:
    try:
        t = open(pf, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    for m in two_re.findall(t):
        two[m] += 1
    for m in pair_re.findall(t):
        pairs[m[0] + "-" + m[1]] += 1
say("two-digit 6x/7x mentions (top): " + repr(two.most_common(12)))
say("hyphen/slash pairs 4x..8x (top): " + repr(pairs.most_common(12)))
p67 = pairs.get("6-7", 0) + pairs.get("6/7", 0)
say("the literal pair 6-7 (either separator): %d mentions" % p67)

say("")
say("=== END AUDIT ===")
