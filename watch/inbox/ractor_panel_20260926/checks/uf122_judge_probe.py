"""uf122 judge probe: verify both candidates' measured claims against bytes.

Run: .venv/Scripts/python.exe watch/inbox/ractor_panel_20260926/checks/uf122_judge_probe.py
Raw output -> watch/inbox/ractor_panel_20260926/checks/uf122.judge.txt
"""
import json
import os
import re
import sys
import time
import urllib.request

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
sys.path.insert(0, REPO)
from mag.catalog_scan import zone_of  # noqa: E402

OUTP = os.path.join(REPO, "watch", "inbox", "ractor_panel_20260926",
                    "checks", "uf122.judge.txt")
out = open(OUTP, "w", encoding="utf-8", newline="\n")


def p(*a):
    print(*a)
    print(*a, file=out)


t0 = time.time()

# S1 catalog stats: stored vs live zone_of
cat = os.path.join(REPO, "catalog", "catalog.jsonl")
rows = 0
last = {}
dup = 0
stored_zone_rows = {}
with open(cat, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        rows += 1
        path = r.get("path")
        if not path:
            continue
        if path in last:
            dup += 1
        last[path] = r
        z = r.get("zone", "")
        stored_zone_rows[z] = stored_zone_rows.get(z, 0) + 1
p("S1 catalog rows total:", rows, "unique paths:", len(last), "dup rows:", dup)

live = {}
mismatch = 0
mm_examples = []
mag_stored = {}
for path, r in last.items():
    z = zone_of(path)
    live[z] = live.get(z, 0) + 1
    if z != r.get("zone"):
        mismatch += 1
        if len(mm_examples) < 8:
            mm_examples.append((path, r.get("zone"), z))
    if path.replace("\\", "/").lower().startswith("local_sovereign_agent/mag/"):
        mag_stored[r.get("zone", "")] = mag_stored.get(r.get("zone", ""), 0) + 1
p("S1 live-zone histogram (unique paths, last-row-wins), top 18:")
for z, c in sorted(live.items(), key=lambda kv: -kv[1])[:18]:
    p("   ", z, c)
p("S1 stored-zone histogram (all rows), top 18:")
for z, c in sorted(stored_zone_rows.items(), key=lambda kv: -kv[1])[:18]:
    p("   ", z, c)
p("S1 stored-vs-live mismatches (unique paths):", mismatch)
p("S1 mismatch examples (path, stored, live):", mm_examples)
p("S1 mag/ subset stored zones:", mag_stored)
p("S1 live counts named zones:",
  {z: live.get(z, 0) for z in ["memory", "lsa", "runs", "intake", "watch",
                               "code", "queue", "doctrine", "dashboard",
                               "research", "astra", "games", "campaigns",
                               "basecamp", "catalog"]})
p("S1 stored counts named zones:",
  {z: stored_zone_rows.get(z, 0) for z in ["memory", "lsa", "runs", "intake",
                                           "watch", "code", "queue",
                                           "doctrine", "dashboard",
                                           "research", "astra", "games",
                                           "campaigns", "basecamp",
                                           "catalog"]})
for target in ["local_sovereign_agent/AGENTS.md",
               "local_sovereign_agent/tests/test_catalog_tags.py",
               "local_sovereign_agent/tools/corpus.py"]:
    hit = [r for pth, r in last.items() if pth.lower() == target]
    if hit:
        p("S1 row for", target, "-> zone:", hit[0].get("zone"),
          "title:", str(hit[0].get("title"))[:80])
    else:
        p("S1 row for", target, "-> NO ROW")

# S2 tags.jsonl schema
tagsp = os.path.join(REPO, "catalog", "tags.jsonl")
n = 0
first = None
have_owner = 0
have_created = 0
with open(tagsp, encoding="utf-8") as fh:
    for line in fh:
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except Exception:
            continue
        n += 1
        if first is None:
            first = r
        if r.get("owner"):
            have_owner += 1
        if r.get("created"):
            have_created += 1
p("S2 tags.jsonl rows:", n,
  "first row keys:", sorted(first.keys()) if first else None)
p("S2 rows with owner:", have_owner, "rows with created:", have_created)

# S3 holdout vault dirs existence
for d in [r"C:\Users\foste\.mag_holdout\uf122",
          r"C:\Users\foste\.mag_eval\uf122",
          r"C:\Users\foste\.mag_holdout",
          r"C:\Users\foste\.mag_eval"]:
    p("S3 exists?", d, os.path.exists(d))

# S4 boot files: the auto-loaded set, checked for error-string span content
boot = ["AGENTS.md", "LOAD.md", "CONSTITUTION.md", "docs/FRAMEWORK_LOAD.md",
        "docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md",
        "memory/briefs/latest.md", "queue/todo.md"]
needles_boot = ["No module named", "B2-186", "12.352s"]
for b in boot:
    fp = os.path.join(REPO, b)
    if not os.path.exists(fp):
        p("S4", b, "MISSING")
        continue
    data = open(fp, "rb").read()[:300000].decode("utf-8", "replace")
    found = [x for x in needles_boot if x in data]
    p("S4", b, "head bytes read:", len(data), "needles found:", found)

# S5 echo spot-check over repo tree (scope: repo only, machinery skipped)
needles = ["B2-186", "SEED_SELF_STEAL_AUDIT_20260926.md", "12.352s",
           "a54ff182c7e8"]
SKIP = {".git", ".venv", "venv", "node_modules", "__pycache__", ".mimosa",
        ".ruff_cache", ".pytest_cache", "catalog"}
hits = {x: [] for x in needles}
scanned = 0
t1 = time.time()
for root, dirs, files in os.walk(REPO):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in files:
        fp = os.path.join(root, f)
        try:
            if os.path.getsize(fp) > 262144:
                continue
            with open(fp, "rb") as fh:
                raw = fh.read()
        except OSError:
            continue
        if b"\x00" in raw[:1024]:
            continue
        scanned += 1
        txt = raw.decode("utf-8", "replace").lower()
        for x in needles:
            if x.lower() in txt and len(hits[x]) < 500:
                hits[x].append(os.path.relpath(fp, REPO))
p("S5 repo scan (machinery skipped, <=256KB, no NUL in head) files:", scanned,
  "seconds:", round(time.time() - t1, 1))
for x in needles:
    p("S5 needle", repr(x), "files containing:", len(hits[x]),
      "sample:", hits[x][:8])

# S6 B2-186 results file in-repo + published seed
res = os.path.join(REPO, "watch", "inbox", "burn_wave_20260926",
                   "B2_186_uf122_results.json")
p("S6 B2-186 results file exists:", os.path.exists(res))
if os.path.exists(res):
    d = json.load(open(res, encoding="utf-8"))
    if isinstance(d, dict):
        p("S6 results top keys:", sorted(d.keys()))
        for k in ("questions", "rows", "results"):
            if k in d and d[k]:
                p("S6 first", k, "row:", json.dumps(d[k][0])[:300])
src186 = open(os.path.join(REPO, "watch", "inbox", "burn_wave_20260926",
                           "B2_186_uf122_eval.py"), encoding="utf-8").read()
p("S6 'SEED = 20260926' in B2-186 script:", "SEED = 20260926" in src186)

# S7 queue.jsonl line 122 (print 121-123 to pin indexing)
qp = os.path.join(REPO, "watch", "inbox", "union_fullsend_20260917",
                  "queue.jsonl")
p("S7 queue.jsonl exists:", os.path.exists(qp))
if os.path.exists(qp):
    with open(qp, encoding="utf-8") as fh:
        for i, line in enumerate(fh, 1):
            if i in (121, 122, 123):
                try:
                    r = json.loads(line)
                    p("S7 line", i, "card:", r.get("card") or r.get("id"),
                      "| title:", str(r.get("title") or r.get("want")
                                      or "")[:100])
                    for k in ("output", "deliverable", "Output"):
                        if r.get(k):
                            p("S7 line", i, k, ":", str(r.get(k))[:220])
                except Exception as e:
                    p("S7 line", i, "parse error:", e, line[:160])
            if i > 123:
                break

# S8 tests/test_catalog_tags.py: exists, function count, catalog rows
tp = os.path.join(REPO, "tests", "test_catalog_tags.py")
p("S8 test file exists:", os.path.exists(tp))
if os.path.exists(tp):
    srct = open(tp, encoding="utf-8").read()
    p("S8 def test_ count:", len(re.findall(r"def test_", srct)))
p("S8 catalog rows for tests/test_catalog_tags.py:",
  sum(1 for pth in last
      if pth.lower().endswith("tests/test_catalog_tags.py")))

# S9 ollama loopback probe (candidate two's S8 dependency)
try:
    with urllib.request.urlopen("http://127.0.0.1:11434/api/tags",
                                timeout=4) as resp:
        data = json.loads(resp.read().decode("utf-8", "replace"))
        names = [m.get("name") for m in data.get("models", [])]
        p("S9 ollama OK, models:", names)
        p("S9 gemma:2b present:",
          any(n == "gemma:2b" or (n or "").startswith("gemma:2b")
              for n in names))
except Exception as e:
    p("S9 ollama probe FAILED:", type(e).__name__, str(e)[:200])

p("DONE total seconds:", round(time.time() - t0, 1))
out.close()
print("WROTE", OUTP)
