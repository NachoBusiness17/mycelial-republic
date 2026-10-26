"""Overlap scan v4 (2026-10-10): the four candidates not covered by v3 tokens.

2609.31047 DynBranch, 2610.11245 ReadKV, 2610.11784 QCOC/Compile the Table,
2609.39131 HBF characterization. Scans catalog.jsonl (all rows), watch/inbox,
and memory/. Read-only; no subprocess spawns.
"""
import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
TOKENS = [
    "2609.31047", "dynbranch", "speculative subgraph",
    "2610.11245", "readkv", "query-adaptive quantization",
    "2610.11784", "compile the table", "operator compression",
    "2609.39131", "high bandwidth flash",
]
low = {t.lower() for t in TOKENS}

CATALOG = os.path.join(ROOT, "catalog", "catalog.jsonl")
with open(CATALOG, encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        ll = line.lower()
        for t in low:
            if t in ll:
                print(f"CATALOG {t!r} L{i}: {line.strip()[:160]}")

hits = 0
for d in [os.path.join(ROOT, "watch", "inbox"), os.path.join(ROOT, "memory")]:
    for dirpath, dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(dirpath, fn)
            try:
                rel = os.path.relpath(p, ROOT)
            except ValueError:
                continue
            if not fn.lower().endswith((".md", ".txt", ".json", ".jsonl", ".html")):
                continue
            try:
                with open(p, encoding="utf-8", errors="replace") as f:
                    for ln, line in enumerate(f, 1):
                        ll = line.lower()
                        for t in low:
                            if t in ll:
                                print(f"FS {t!r} -> {rel}:{ln}: {line.strip()[:140]}")
                                hits += 1
            except OSError:
                pass
print(f"V4_FS_HITS {hits}")
