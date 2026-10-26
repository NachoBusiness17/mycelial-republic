"""Overlap-baseline scanner for the kv-cache-context arxiv sweep (2026-10-10).

Counts and lists catalog rows matching cache/context terms, then greps memory/
for the same vocabulary plus estate-specific markers (overflow_reason, frozen
prefix, kv-cache provenance). Read-only; no subprocess spawns.
"""
import json
import os
import re
import sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CATALOG = os.path.join(ROOT, "catalog", "catalog.jsonl")
MEM = os.path.join(ROOT, "memory")

TERMS = {
    "kv_cache": ["kv-cache", "kv cache", "kv_cache", "kvcache"],
    "prefix_caching": ["prefix cach", "prefix-cach", "cache-aware", "sticky routing", "cache reuse", "cache hit"],
    "named_systems": ["lmcache", "cachegen", "cacheblend", "vllm"],
    "context_compression": ["context compression", "context_compression"],
    "compaction_overflow": ["compaction", "overflow_reason", "stalled compaction"],
    "frozen_prefix": ["frozen prefix", "frozen-prefix"],
    "provenance": ["provenance"],
}

rows = []
with open(CATALOG, encoding="utf-8") as f:
    for i, line in enumerate(f):
        line = line.strip()
        if line:
            rows.append((i + 1, line))

print(f"TOTAL_CATALOG_ROWS {len(rows)}")

hits = {k: [] for k in TERMS}
for n, line in rows:
    low = line.lower()
    for k, variants in TERMS.items():
        if any(v in low for v in variants):
            hits[k].append((n, line))

for k in TERMS:
    print(f"HITS {k} {len(hits[k])}")


def show(k, limit=50):
    print(f"--- {k} sample ---")
    for n, line in hits[k][:limit]:
        try:
            d = json.loads(line)
        except Exception:
            print(f"  L{n} UNPARSED {line[:100]}")
            continue
        t = d.get("title") or d.get("name") or ""
        p = d.get("path") or d.get("url") or d.get("source") or d.get("origin") or ""
        ident = d.get("id") or d.get("arxiv_id") or d.get("uid") or ""
        dom = d.get("domain") or d.get("collection") or d.get("lens") or ""
        print(f"  L{n} [{ident}] dom={dom} {str(t)[:100]} | {str(p)[:90]}")


for k in ["kv_cache", "prefix_caching", "named_systems", "compaction_overflow", "frozen_prefix", "provenance"]:
    show(k)

print("=== corpus/library top level ===")
lib = os.path.join(ROOT, "corpus", "library")
if os.path.isdir(lib):
    for name in sorted(os.listdir(lib)):
        print(" ", name)
else:
    print("  no corpus/library dir")

print("=== MEMORY SCAN (capped) ===")
pattern = re.compile("|".join(re.escape(v) for vs in TERMS.values() for v in vs), re.I)
count = 0
for dirpath, dirs, files in os.walk(MEM):
    for fn in files:
        if not fn.lower().endswith((".md", ".json", ".jsonl", ".txt")):
            continue
        p = os.path.join(dirpath, fn)
        try:
            with open(p, encoding="utf-8", errors="replace") as f:
                for ln, line in enumerate(f, 1):
                    if pattern.search(line):
                        rel = os.path.relpath(p, ROOT)
                        print(f"{rel}:{ln}: {line.strip()[:150]}")
                        count += 1
                        if count >= 150:
                            print("MEMORY SCAN CAP REACHED")
                            sys.exit(0)
        except OSError:
            pass
print(f"MEMORY_HITS {count}")
