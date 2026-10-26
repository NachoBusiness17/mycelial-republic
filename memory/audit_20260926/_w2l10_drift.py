"""Lane 10: two-directional index drift for watch/inbox (full recursive)."""
import hashlib, json, os
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent")
INBOX = ROOT / "watch" / "inbox"
INDEX = INBOX / "INDEX.json"
CONTROL = {"INDEX.json", "INDEX.md", "SHARED_SURFACE_CONTRACT.json"}

idx = json.loads(INDEX.read_text(encoding="utf-8"))
items = [i for i in idx.get("items", []) if isinstance(i, dict)]

def rel_of(pathval):
    raw = str(pathval or "").replace("\\", "/")
    for pref in ("/board/inbox/", "/app/inbox/", "inbox/"):
        if raw.startswith(pref):
            raw = raw[len(pref):]
            break
    return raw.lstrip("/")

# --- index side ---
indexed = {}          # rel -> item
dupes = Counter()
for it in items:
    rel = rel_of(it.get("path"))
    if rel in indexed:
        dupes[rel] += 1
    indexed[rel] = it

missing = []          # indexed but no file
for rel, it in indexed.items():
    t = INBOX / rel
    if not t.is_file():
        missing.append(rel)

# --- disk side: FULL recursive walk ---
on_disk = {}
for dirpath, dirnames, filenames in os.walk(INBOX):
    for fn in filenames:
        full = Path(dirpath) / fn
        rel = str(full.relative_to(INBOX)).replace("\\", "/")
        on_disk[rel] = full

disk_no_index = [r for r in on_disk
                 if r not in indexed and r.rsplit("/", 1)[-1] not in CONTROL]
top_level = {r for r in on_disk if "/" not in r}
subdir_files = {r for r in on_disk if "/" in r}
top_no_index = [r for r in disk_no_index if "/" not in r]
sub_no_index = [r for r in disk_no_index if "/" in r]

# --- hash drift on indexed-and-present items (whole-file, living-aware) ---
def sha(p):
    h = hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest().upper()

mismatch, living, living_prefix_ok, living_open, no_hash, match = [], [], 0, 0, [], 0
for rel, it in indexed.items():
    t = INBOX / rel
    if not t.is_file():
        continue
    rec = str(it.get("sha256") or "").upper()
    if not rec:
        no_hash.append(rel)
        continue
    if it.get("living"):
        living.append(rel)
        if it.get("seal") == "open":
            living_open += 1
        else:
            n = it.get("size")
            if isinstance(n, int) and n > 0 and t.stat().st_size >= n:
                with t.open("rb") as f:
                    pre = f.read(n)
                if hashlib.sha256(pre).hexdigest().upper() == rec:
                    living_prefix_ok += 1
                else:
                    mismatch.append((rel, "living-prefix"))
            else:
                mismatch.append((rel, "living-unsealed"))
    else:
        if sha(t) == rec:
            match += 1
        else:
            mismatch.append((rel, "whole-file"))

out = {
    "index_items_total": len(items),
    "index_unique_rel": len(indexed),
    "index_duplicate_rel": len(dupes),
    "index_missing_file_count": len(missing),
    "index_missing_files": missing[:40],
    "disk_files_recursive": len(on_disk),
    "disk_top_level": len(top_level),
    "disk_in_subdirs": len(subdir_files),
    "disk_not_in_index_total": len(disk_no_index),
    "disk_not_in_index_top_level": len(top_no_index),
    "disk_not_in_index_subdirs": len(sub_no_index),
    "unindexed_top_level_list": sorted(top_no_index),
    "unindexed_subdir_sample": sorted(sub_no_index)[:40],
    "hash_verified_match": match,
    "hash_mismatch_count": len(mismatch),
    "hash_mismatch": mismatch[:60],
    "living_indexed": len(living),
    "living_prefix_ok": living_prefix_ok,
    "living_open": living_open,
    "index_items_without_sha": len(no_hash),
    "index_items_without_sha_list": no_hash[:40],
}
print(json.dumps(out, indent=2))
Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/memory/audit_20260926/_w2l10_drift.json").write_text(
    json.dumps(out, indent=2), encoding="utf-8")
