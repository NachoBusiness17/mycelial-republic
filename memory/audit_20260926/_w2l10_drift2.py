"""Lane 10 part 2: noise-excluded drift + full mismatch list."""
import json
from pathlib import Path

d = json.load(open(r"C:/Users/foste/Documents/projects/local_sovereign_agent/memory/audit_20260926/_w2l10_drift.json", encoding="utf-8"))

NOISE = (".mimosa/", "__pycache__/", ".git/")
import os
INBOX = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox")
idx = json.loads((INBOX / "INDEX.json").read_text(encoding="utf-8"))
CONTROL = {"INDEX.json", "INDEX.md", "SHARED_SURFACE_CONTRACT.json", "index_events.jsonl"}

def rel_of(p):
    raw = str(p or "").replace("\\", "/")
    for pref in ("/board/inbox/", "/app/inbox/", "inbox/"):
        if raw.startswith(pref):
            raw = raw[len(pref):]; break
    return raw.lstrip("/")

indexed = {rel_of(i.get("path")): i for i in idx.get("items", []) if isinstance(i, dict)}

rows = []
for dirpath, dirnames, filenames in os.walk(INBOX):
    for fn in filenames:
        full = Path(dirpath) / fn
        rel = str(full.relative_to(INBOX)).replace("\\", "/")
        rows.append(rel)

noise = [r for r in rows if r.startswith(NOISE)]
real = [r for r in rows if not r.startswith(NOISE)]
real_unindexed = [r for r in real if r not in indexed and r.rsplit("/", 1)[-1] not in CONTROL]
real_indexed = [r for r in real if r in indexed]

# bucket the unindexed real files by top-level dir
from collections import Counter
buckets = Counter(r.split("/")[0] if "/" in r else "(top level)" for r in real_unindexed)

print("== DISK (recursive) ==")
print("all files:", len(rows))
print("tool-cache noise (.mimosa/__pycache__/.git):", len(noise))
print("real files:", len(real), " of which indexed:", len(real_indexed), " unindexed:", len(real_unindexed))
print()
print("== UNINDEXED REAL FILES BY DIR ==")
for k, v in buckets.most_common(25): print(f"  {v:5d}  {k}")
print()
print("== UNINDEXED REAL, TOP-LEVEL ONLY ==")
for r in sorted(r for r in real_unindexed if "/" not in r): print("   ", r)
print()
print("== HASH MISMATCHES (all", len(d["hash_mismatch"]), "shown) ==")
for rel, kind in d["hash_mismatch"]:
    it = indexed.get(rel, {})
    print(f"  {kind:14s} {rel}   [living={bool(it.get('living'))} seal={it.get('seal')}]")
print()
print("== INDEX ITEMS WITHOUT sha256 ==", d["index_items_without_sha_count"])
print("== INDEXED ITEM WITH NO FILE ==", d["index_missing_files"])
