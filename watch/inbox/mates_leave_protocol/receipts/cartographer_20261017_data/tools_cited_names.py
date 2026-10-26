"""Cycle 8: cited-name bank for corpus/tools, joined from the bounded refs pass.

Reads the banked bounded refs (tools_refs_bounded_20261017.txt, UTF-16) and the
inventory walk; classifies each reference line; writes tools_cited_names.json.
"""
import json
import os
from collections import Counter
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(ROOT, "logs", "mates", "cartographer", "tools_cited_names.json")

raw = [r.strip() for r in open(
    os.path.join(ROOT, "logs", "mates", "cartographer", "tools_refs_bounded_20261017.txt"),
    encoding="utf-16", errors="replace").read().splitlines() if r.strip()]

tools_root = os.path.join(ROOT, "corpus", "tools")
shelf_rel = set()
for dp, dn, fn in os.walk(tools_root):
    for name in fn:
        rel = os.path.relpath(os.path.join(dp, name), tools_root).replace("\\", "/")
        shelf_rel.add(rel.lower())

hit = Counter()
exact = set()
baseonly = set()
dironly = set()
for line in raw:
    tail = line.replace("\\", "/").split("corpus/tools/", 1)[1].strip(" \"'`),.:")
    rel = unquote(tail).lower()
    if rel in shelf_rel:
        exact.add(rel)
        hit[rel] += 1
    else:
        parts = rel.split("/")
        if parts[-1] and any(parts[-1].endswith(e) for e in (".py", ".java", ".json", ".md", ".bat", ".sh", ".txt")):
            baseonly.add(parts[-1])
            hit["basename:" + parts[-1]] += 1
        else:
            dironly.add("/".join(parts[:2]))
            hit["dir:" + "/".join(parts[:2])] += 1

with open(os.path.join(ROOT, "logs", "mates", "cartographer", "tools_inventory.json"), encoding="utf-8") as f:
    files = json.load(f)["totals"]["files"]

res = {
    "instrument": "join of tools_refs_bounded_20261017.txt (rg bounded pass: watch/inbox depth-3 + "
                  "docs mag configs state queue, text globs) against the tools inventory walk",
    "raw_lines": len(raw),
    "exact_path_hits": len(exact),
    "basename_only_names": len(baseonly),
    "dir_only_prefixes": len(dironly),
    "shelf_files": files,
    "exact_hit_rate_pct": round(len(exact) / files * 100.0, 4),
    "top_exact": hit.most_common(25),
    "exact_paths": sorted(exact),
    "basename_names": sorted(baseonly),
    "dir_prefixes": sorted(dironly)[:40],
}
json.dump(res, open(OUT, "w", encoding="utf-8"), indent=1)
print("raw:", len(raw), "exact:", len(exact), "baseonly:", len(baseonly), "dironly:", len(dironly))
for k, n in hit.most_common(12):
    print(n, k)
