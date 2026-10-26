"""f-26 targeted queries against _f26_raw.json + git sanity checks."""
import json
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
raw = json.load(open(os.path.join(HERE, "_f26_raw.json"), encoding="utf-8"))
recs = raw["records"]
by = {r["path"]: r for r in recs}
CF = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}

print("== check-ignore -v sanity ==")
for t in ["logs/kpi.jsonl", "memory/mail", "corpus/oral_history",
          "memory/runs/swarm_health/trail.jsonl", "agents", "watch/inbox/index_events.jsonl"]:
    p = subprocess.run(["git", "check-ignore", "-v", t], cwd=REPO,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, **CF)
    print(t, "-> rc", p.returncode, p.stdout.decode("utf-8", "replace").strip()[:120])

print("\n== parse_bad files ==")
for r in recs:
    if r["parse_bad"] > 0:
        print("%6d bad /%7d rows first_bad_line=%-7s %s" %
              (r["parse_bad"], r["rows"], r["first_bad_line"], r["path"]))

print("\n== zero-row files ==")
z = [r["path"] for r in recs if r["rows"] == 0]
print("count:", len(z))
for p in z[:15]:
    print("  ", p)

print("\n== named cross-checks ==")
for name in ["watch/inbox/LINKS.jsonl", "watch/INBOX_LINKS.jsonl",
             "watch/inbox/index_events.jsonl", "memory/percolator/invariants.jsonl",
             "memory/workflows/REGISTRY.jsonl", "state/shared_activity.jsonl"]:
    r = by.get(name)
    if r:
        print("%-40s rows=%-8d tracked=%s delta=%s age=%.2fd keysets=%d" %
              (name, r["rows"], r["tracked"], r["delta_vs_head"], r["mtime_age_days"], len(r["keysets"])))
        if r["keysets"]:
            print("     keys:", [k[0] for k in r["keysets"][:3]])
    else:
        print(name, "-> NOT FOUND (check name)")

print("\n== readers for operational ledgers (count>=1) ==")
ops = [r for r in recs if r["reader_hits"]["count"] > 0]
ops.sort(key=lambda r: -r["reader_hits"]["count"])
print("files with >=1 literal reader hit:", len(ops))
for r in ops[:40]:
    s = r["reader_hits"]["samples"][0]
    print("%4d hits  %-52s  e.g. %s:%d" % (r["reader_hits"]["count"], r["path"], s["file"], s["line"]))

print("\n== schema drift: files with >1 distinct keyset (top 25 by rows) ==")
multi = [r for r in recs if len(r["keysets"]) > 1]
multi.sort(key=lambda r: -r["rows"])
print("files with >1 keyset:", len(multi))
for r in multi[:25]:
    print("%8d rows %-9d keysets  %s" % (r["rows"], len(r["keysets"]), r["path"]))

print("\n== untracked runtime ledgers (delta=None, mtime<=1d, rows>=1000) ==")
u = [r for r in recs if not r["tracked"] and r["mtime_age_days"] <= 1 and r["rows"] >= 1000]
u.sort(key=lambda r: -r["rows"])
for r in u[:30]:
    print("%9d rows %-44s keysets=%d %s" % (r["rows"], r["path"], len(r["keysets"]), r["mtime"]))

print("\n== tracked-by-dir ==")
from collections import Counter
c = Counter()
for r in recs:
    if r["tracked"]:
        c[r["path"].split("/")[0]] += 1
print(dict(c))

print("\n== non-dict row files ==")
for r in recs:
    if r["nondict_rows"] > 0:
        print("%7d/%7d nondict  %s" % (r["nondict_rows"], r["rows"], r["path"]))
