"""Fold census for frontier_olm_2026-10-06 (olm-mine:2026-10-06).

Measures byte counts of every file under the run directory and validates the
fold's two JSONL artifacts. Run with the repo venv python. No network, no
subprocess spawns; pure os.walk + json.loads.
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

rows = []
skipped = []
for dp, dn, fn in os.walk(ROOT):
    for f in fn:
        p = os.path.join(dp, f)
        try:
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            sz = os.path.getsize("\\\\?\\" + p)
        except (ValueError, OSError):
            skipped.append(f)
            continue
        rows.append((rel, sz))
for name in skipped:
    print("SKIPPED_UNREADABLE\t%s" % name)
rows.sort(key=lambda r: r[1])
for rel, sz in rows:
    print("%d\t%s" % (sz, rel))


def bucket(area, source):
    a = area or ""
    s = source or ""
    if a.endswith("via x"):
        return "x"
    if " via " in a:
        return a.split(" via ", 1)[1]
    if s.startswith("Hacker News") or "hn.algolia" in s:
        return "hn"
    if s.startswith("x.com") or s.startswith("X door"):
        return "x"
    if "reddit" in s.lower():
        return "reddit"
    if "arxiv" in s.lower():
        return "arxiv"
    return "other"


areas = {}
srcs = {}
n = 0
with open(os.path.join(ROOT, "register.jsonl"), encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        n += 1
        areas[o["area"]] = areas.get(o["area"], 0) + 1
        b = bucket(o.get("area"), o.get("source"))
        srcs[b] = srcs.get(b, 0) + 1
print("REGISTER_ROWS\t%d" % n)
print("BY_AREA\t%s" % json.dumps(areas, sort_keys=True))
print("BY_SOURCE\t%s" % json.dumps(srcs, sort_keys=True))

for name in ("register.jsonl", "percolator_candidates.jsonl"):
    cnt = 0
    err = 0
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            cnt += 1
            try:
                json.loads(line)
            except Exception:
                err += 1
    print("JSONL_VALIDATE\t%s\trows=%d\terrors=%d" % (name, cnt, err))
