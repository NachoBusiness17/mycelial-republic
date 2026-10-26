import os
REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
NEED = {
    "thinking-inertia": ["2610.11765", "thinking inertia", "empty-thinking rate", "keep thinking when told not to"],
    "leap": ["2610.02670", "learning efficient action proposals", "action speculation"],
    "ubtree": ["2609.39972", "ubtree", "unigram and bigram"],
    "industryllm": ["2609.31871", "industryllm", "failure-driven llm training"],
    "solving-no-stop": ["2609.37326", "solving without stopping", "distillation filters stops"],
    "cascadia": ["2609.38697", "control-plane-free", "cascadia-node"],
    "dysco": ["2610.08268", "dysco", "depth-synchronized batching"],
    "token-cost": ["2610.02491", "what does a token cost", "sufficient compute"],
}
ALL = [(i, n) for i, ns in NEED.items() for n in ns]
SUBS = ["memory/burns", "memory/zknot", "memory/session", "memory/worldline",
        "memory/lenses", "memory/mycelium", "memory/mesh", "memory/game",
        "memory/workflows", "memory/percolator", "memory/rib_bus", "memory/proofs"]
hits = []
for sub in SUBS:
    for dp, dn, fn in os.walk(os.path.join(REPO, sub)):
        for f in fn:
            p = os.path.join(dp, f)
            try:
                if os.path.getsize(p) > 25_000_000:
                    continue
                low = open(p, encoding="utf-8", errors="replace").read(20_000_000).lower()
            except OSError:
                continue
            for it, nd in ALL:
                if nd in low:
                    hits.append((it, nd, os.path.relpath(p, REPO)))
print(hits if hits else "zero hits in remaining memory subdirs")
