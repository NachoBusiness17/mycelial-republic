# Overlap scan v2 for sweep-inference-efficiency-arxiv (2nd run, 2026-10-11).
# Fixed vs v1: each file is read and lowercased ONCE, all needles checked
# against the single lowercase copy (v1 re-read files once per needle).
# Pure file reads, no subprocess spawns.
import os

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"

NEEDLES = {
    "thinking-inertia":   ["2610.11765", "thinking inertia", "empty-thinking rate", "keep thinking when told not to"],
    "leap":               ["2610.02670", "learning efficient action proposals", "action speculation"],
    "ubtree":             ["2609.39972", "ubtree", "unigram and bigram"],
    "industryllm":        ["2609.31871", "industryllm", "failure-driven llm training"],
    "solving-no-stop":    ["2609.37326", "solving without stopping", "distillation filters stops"],
    "cascadia":           ["2609.38697", "control-plane-free", "cascadia-node"],
    "dysco":              ["2610.08268", "dysco", "depth-synchronized batching"],
    "token-cost":         ["2610.02491", "what does a token cost", "sufficient compute"],
}
ALL = [(item, nd) for item, nds in NEEDLES.items() for nd in nds]

real_hits, cache_hits, traj_hits = [], [], []

def classify_and_append(item, nd, path):
    full = os.path.relpath(path, REPO)
    base = os.path.basename(path)
    if "trajectory" in full or base == "steps.jsonl":
        traj_hits.append((item, nd, full))
    elif base.startswith("_") or (os.sep + "raw" + os.sep) in full:
        cache_hits.append((item, nd, full))
    else:
        real_hits.append((item, nd, full))

def scan_file(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            low = f.read(20_000_000).lower()
    except OSError:
        return
    for item, nd in ALL:
        if nd in low:
            classify_and_append(item, nd, path)

# 1. catalog.jsonl streamed once
cat_hits = []
CAT = os.path.join(REPO, "catalog", "catalog.jsonl")
needles_lc = {nd: nd.lower() for _, nd in ALL}
items_by_nd = {nd: item for item, nd in ALL}
with open(CAT, "r", encoding="utf-8", errors="replace") as f:
    for ln, line in enumerate(f, 1):
        ll = line.lower()
        for nd, ndl in needles_lc.items():
            if ndl in ll:
                cat_hits.append((items_by_nd[nd], nd, ln))

# 2. tree roots, one read per file
def walk_root(root, maxdepth=None):
    root = os.path.join(REPO, root)
    base_depth = root.count(os.sep)
    for dirpath, dirnames, filenames in os.walk(root):
        if maxdepth is not None and dirpath.count(os.sep) - base_depth >= maxdepth:
            dirnames[:] = []
        for fn in filenames:
            yield os.path.join(dirpath, fn)

count = 0
for p in walk_root("memory", maxdepth=3):
    try:
        if os.path.getsize(p) > 25_000_000:
            continue
    except OSError:
        continue
    scan_file(p); count += 1
for p in walk_root("corpus/steal"):
    try:
        if os.path.getsize(p) > 25_000_000:
            continue
    except OSError:
        continue
    scan_file(p); count += 1
for p in walk_root("watch/inbox"):
    try:
        if os.path.getsize(p) > 25_000_000:
            continue
    except OSError:
        continue
    scan_file(p); count += 1

print("files scanned (trees):", count)
print("=== catalog.jsonl hits (item, needle, line) ===")
for h in cat_hits:
    print(h)
print("catalog hit total:", len(cat_hits))
print("=== real-bank hits (item, needle, path) ===")
for h in real_hits:
    print(h)
print("real hit total:", len(real_hits))
print("=== cache/scratch + trajectory noise ===")
for h in cache_hits:
    print("cache:", h)
for h in traj_hits:
    print("traj:", h)
print("cache total:", len(cache_hits), "traj total:", len(traj_hits))
