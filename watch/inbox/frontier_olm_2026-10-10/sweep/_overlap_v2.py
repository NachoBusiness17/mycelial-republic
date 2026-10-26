"""Focused overlap scan v2 for the 8 final bank candidates (2026-10-10).

Catalog and state/arxiv were fully grepped by _overlap_ids.py (zero hits for
these 8). This pass covers watch/inbox and memory/, which the v1 FS walk never
reached (it hit its output cap inside watch/inbox on unrelated 'refold' noise).
Read-only, no subprocess spawns.
"""
import os

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
SCAN_DIRS = [os.path.join(ROOT, "watch", "inbox"), os.path.join(ROOT, "memory")]

TOKENS = [
    "2609.28870", "fancy eviction",
    "2609.24991", "who pays for the kv cache",
    "2609.34432", "agent serving at production scale",
    "2609.36526", "counterfactual continuations",
    "2609.37012", "cadoc",
    "2610.02766", "prefix-cache retention",
    "2609.32278", "rr-evict",
    "2610.11358", "rarecache",
]

low = {t.lower() for t in TOKENS}
hits = 0
for d in SCAN_DIRS:
    for dirpath, dirs, files in os.walk(d):
        for fn in files:
            p = os.path.join(dirpath, fn)
            rel = os.path.relpath(p, ROOT)
            if not fn.lower().endswith((".md", ".txt", ".json", ".jsonl", ".html")):
                continue
            try:
                with open(p, encoding="utf-8", errors="replace") as f:
                    for ln, line in enumerate(f, 1):
                        ll = line.lower()
                        for t in low:
                            if t in ll:
                                print(f"HIT {t!r} -> {rel}:{ln}: {line.strip()[:150]}")
                                hits += 1
            except OSError:
                pass
print(f"V2_FS_HITS {hits}")
