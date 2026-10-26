"""Per-item overlap check for the kv-cache-context arxiv sweep (2026-10-10).

For each candidate item, greps catalog/catalog.jsonl (full content), the
state/arxiv banking tree, watch/inbox, and memory/ for the arxiv id and
distinctive title tokens. Read-only, no subprocess spawns.
"""
import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CATALOG = os.path.join(ROOT, "catalog", "catalog.jsonl")

ITEMS = {
    "2609.38706": ["2609.38706", "Shared KV Caches for LLM Serving", "provenance-blind"],
    "2610.07863": ["2610.07863", "ReFold", "Inter-Turn Context Folding"],
    "2610.07782": ["2610.07782", "Persistent Memory in Multi-Agent LLM Inference"],
    "2609.37012": ["2609.37012", "CADOC"],
    "2610.02766": ["2610.02766", "Memory-Time Optimization", "Prefix-Cached Language Model Serving"],
    "2610.06597": ["2610.06597", "HEAR Protocol"],
    "2609.32278": ["2609.32278", "RR-Evict"],
    "2610.11358": ["2610.11358", "RaReCache", "Rank Disagreement"],
    "2609.34432": ["2609.34432", "Understanding Agent Serving at Production Scale"],
}

# 1) catalog full-content grep
with open(CATALOG, encoding="utf-8") as f:
    cat_lines = f.readlines()
print(f"catalog rows scanned: {len(cat_lines)}")
for iid, tokens in ITEMS.items():
    for tok in tokens:
        n = sum(1 for l in cat_lines if tok.lower() in l.lower())
        if n:
            print(f"CATALOG {iid} token={tok!r} hits={n}")
            for i, l in enumerate(cat_lines, 1):
                if tok.lower() in l.lower():
                    print(f"   L{i}: {l.strip()[:180]}")

# 2) filesystem grep: state/arxiv tree, watch/inbox, memory (filenames + content)
SCAN_DIRS = [os.path.join(ROOT, "state", "arxiv"), os.path.join(ROOT, "watch", "inbox"), os.path.join(ROOT, "memory")]
all_tokens = {t for toks in ITEMS.values() for t in toks}
low_tokens = {t.lower(): t for t in all_tokens}
hits = 0
for d in SCAN_DIRS:
    if not os.path.isdir(d):
        continue
    for dirpath, dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            name_low = fn.lower()
            for t in low_tokens:
                if t in name_low:
                    print(f"FSNAME {t!r} -> {rel}")
                    hits += 1
            if fn.lower().endswith((".md", ".txt", ".json", ".jsonl")):
                try:
                    with open(p, encoding="utf-8", errors="replace") as f:
                        for ln, line in enumerate(f, 1):
                            ll = line.lower()
                            for t in low_tokens:
                                if t in ll:
                                    print(f"FSCONTENT {t!r} -> {rel}:{ln}: {line.strip()[:140]}")
                                    hits += 1
                                    if hits > 120:
                                        raise SystemExit(0)
                except OSError:
                    pass
print(f"FS_HITS {hits}")
