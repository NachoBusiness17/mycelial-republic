"""f-26 analysis: roll up _f26_raw.json into the shapes the census doc needs."""
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
raw = json.load(open(os.path.join(HERE, "_f26_raw.json"), encoding="utf-8"))
recs = raw["records"]
print("head_sha:", raw["head_sha"], " generated:", raw["generated"])

top = Counter()
rows_top = Counter()
bytes_top = Counter()
for r in recs:
    t = r["path"].split("/")[0]
    top[t] += 1
    rows_top[t] += r["rows"]
    bytes_top[t] += r["size_bytes"]
print("\n== top-level dir rollup (files / rows / MB) ==")
for t, n in top.most_common():
    print("%-28s %6d %12d %10.1f" % (t, n, rows_top[t], bytes_top[t] / 1e6))

# second-level for corpus and watch
def two(p):
    parts = p.split("/")
    return "/".join(parts[:2])
for rootname in ("corpus", "watch", "memory", "logs", "state", "queue"):
    agg = defaultdict(lambda: [0, 0, 0])
    for r in recs:
        if r["path"].startswith(rootname + "/"):
            k = two(r["path"])
            agg[k][0] += 1
            agg[k][1] += r["rows"]
            agg[k][2] += r["size_bytes"]
    print("\n== %s/ second-level ==" % rootname)
    for k in sorted(agg, key=lambda k: -agg[k][1]):
        n, rr, bb = agg[k]
        print("%-46s %6d %12d %10.1fMB" % (k, n, rr, bb / 1e6))

print("\n== top 25 files by rows ==")
for r in sorted(recs, key=lambda r: -r["rows"])[:25]:
    print("%9d rows %10.1fMB  delta=%-8s age=%6.1fd %s"
          % (r["rows"], r["size_bytes"] / 1e6, r["delta_vs_head"], r["mtime_age_days"], r["path"]))

print("\n== top 15 files by bytes ==")
for r in sorted(recs, key=lambda r: -r["size_bytes"])[:15]:
    print("%9d rows %10.1fMB  %s" % (r["rows"], r["size_bytes"] / 1e6, r["path"]))

print("\n== status counts ==")
print("tracked:", sum(1 for r in recs if r["tracked"]))
print("ignored:", sum(1 for r in recs if r["ignored"]))
print("untracked-not-ignored:", sum(1 for r in recs if not r["tracked"] and not r["ignored"]))
grow = [r for r in recs if (r["delta_vs_head"] or 0) > 0]
shrink = [r for r in recs if (r["delta_vs_head"] or 0) < 0]
same = [r for r in recs if r["delta_vs_head"] == 0]
print("delta>0 (grew vs HEAD):", len(grow), " rows gained:", sum(r["delta_vs_head"] for r in grow))
print("delta<0 (shrank vs HEAD):", len(shrink))
print("delta==0 (stable):", len(same))
print("mtime <= 1 day:", sum(1 for r in recs if r["mtime_age_days"] <= 1))
print("mtime <= 7 days:", sum(1 for r in recs if r["mtime_age_days"] <= 7))
print("mtime > 90 days:", sum(1 for r in recs if r["mtime_age_days"] > 90))
print("parse_bad > 0:", sum(1 for r in recs if r["parse_bad"] > 0))
print("schema_sampled:", sum(1 for r in recs if r["schema_sampled"]))
print("empty rows (0 rows):", sum(1 for r in recs if r["rows"] == 0))

print("\n== grew-most vs HEAD (top 20) ==")
for r in sorted(grow, key=lambda r: -r["delta_vs_head"])[:20]:
    print("%+9d  age=%6.1fd  %s" % (r["delta_vs_head"], r["mtime_age_days"], r["path"]))

print("\n== recently touched (mtime <=1d), top 30 by rows ==")
for r in sorted([r for r in recs if r["mtime_age_days"] <= 1], key=lambda r: -r["rows"])[:30]:
    print("%9d rows delta=%-9s %s  %s" % (r["rows"], r["delta_vs_head"], r["mtime"], r["path"]))

print("\n== files outside corpus/ and watch/ ==")
out = [r for r in recs if not r["path"].startswith(("corpus/", "watch/"))]
print("count:", len(out), "rows:", sum(r["rows"] for r in out), "bytes:", sum(r["size_bytes"] for r in out))
