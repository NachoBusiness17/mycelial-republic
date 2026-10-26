# Quick targeted overlap check (catalog.jsonl full stream + likely memory
# surfaces) while the full-depth scan runs. Same needle set, single pass.
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
ALL = [(i, n) for i, ns in NEEDLES.items() for n in ns]

def scan(path, hits):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            low = f.read(20_000_000).lower()
    except OSError:
        return
    for item, nd in ALL:
        if nd in low:
            hits.append((item, nd, os.path.relpath(path, REPO)))

hits = []
with open(os.path.join(REPO, "catalog", "catalog.jsonl"), "r", encoding="utf-8", errors="replace") as f:
    cat = []
    for ln, line in enumerate(f, 1):
        ll = line.lower()
        for item, nd in ALL:
            if nd in ll:
                cat.append((item, nd, ln))
print("=== catalog.jsonl ===")
for h in cat:
    print(h)
print("catalog total:", len(cat))

roots = ["memory/rib", "memory/research_polished", "memory/frontier",
         "memory/improve", "memory/press", "memory/briefs", "memory/law"]
for r in roots:
    for dp, dn, fn in os.walk(os.path.join(REPO, r)):
        for f in fn:
            scan(os.path.join(dp, f), hits)
# top-level memory *.md and *.json / jsonl
for f in os.listdir(os.path.join(REPO, "memory")):
    p = os.path.join(REPO, "memory", f)
    if os.path.isfile(p):
        scan(p, hits)
# corpus/steal (small)
for dp, dn, fn in os.walk(os.path.join(REPO, "corpus", "steal")):
    for f in fn:
        scan(os.path.join(dp, f), hits)
# sibling sweep banks (real .md banks only, skip _ scratch)
sw = os.path.join(REPO, "watch", "inbox", "frontier_olm_adhoc", "sweep")
for f in os.listdir(sw):
    if f.endswith(".md"):
        scan(os.path.join(sw, f), hits)

print("=== targeted-surface hits ===")
for h in hits:
    print(h)
print("targeted total:", len(hits))
