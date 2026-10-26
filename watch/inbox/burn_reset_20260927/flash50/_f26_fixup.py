"""f-26 fixup + reader mapping.

1. Patch _f26_raw.json with the corrected batch check-ignore result
   (_f26_ignored.txt from the verified rerun).
2. Map major operational ledgers to their code readers/writers: grep each
   literal basename across mag/ tools/ scripts/ backend/ *.py + root *.py,
   record file:line.
"""
import json
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CF = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}

raw_path = os.path.join(HERE, "_f26_raw.json")
raw = json.load(open(raw_path, encoding="utf-8"))
recs = raw["records"]

ignored = set()
for line in open(os.path.join(HERE, "_f26_ignored.txt"), encoding="utf-8"):
    t = line.strip()
    if t:
        ignored.add(t)
n = 0
for r in recs:
    want = r["path"] in ignored
    if r["ignored"] != want:
        r["ignored"] = want
        n += 1
raw["ignored_fixup"] = {"patched": n, "ignored_total": len(ignored & {r["path"] for r in recs})}
json.dump(raw, open(raw_path, "w", encoding="utf-8"), indent=1)
print("ignored flags patched on %d records; ignored total now: %s"
      % (n, sum(1 for r in recs if r["ignored"])))

un = [r["path"] for r in recs if not r["tracked"] and not r["ignored"]]
print("untracked AND not ignored (%d):" % len(un))
for p in un:
    print("  ", p)

# ---- reader mapping for named operational ledgers ----
MAJOR = [
    "watch/inbox/index_events.jsonl", "watch/inbox/LINKS.jsonl",
    "watch/INBOX_LINKS.jsonl", "memory/decisions_log.jsonl",
    "memory/biography/verkle_chain.jsonl", "memory/trajectory/steps.jsonl",
    "memory/agent_state/chain.jsonl", "state/shared_activity.jsonl",
    "logs/behavioral_events.jsonl", "logs/kpi.jsonl", "logs/usage.jsonl",
    "logs/provider_usage.jsonl", "logs/supervisor.jsonl", "logs/failure_kb.jsonl",
    "memory/ingest/registry.jsonl", "watch/room.jsonl", "watch/grok_feed.jsonl",
    "watch/session_digest.jsonl", "catalog/catalog.jsonl", "catalog/tags.jsonl",
    "catalog/junctions.jsonl", "memory/runs/swarm_health/trail.jsonl",
    "memory/runs/governor_autorun_trail.jsonl", "memory/runs/orchestrator_trail.jsonl",
    "memory/bard/breadcrumbs.jsonl", "dashboard/data/ESTATE_INDEX.jsonl",
    "watch/ESTATE_INDEX/ESTATE_INDEX.jsonl", "queue/lanes/research/trail.jsonl",
    "memory/mail/mail_log.jsonl", "memory/percolator/explore.jsonl",
    "memory/facts/behavioral.jsonl", "state/fuel/full_scan_ledger.jsonl",
    "research/destructive_receipts.jsonl", "training/events.jsonl",
    "memory/training/events.jsonl", "memory/workflows/REGISTRY.jsonl",
    "memory/ghost/noise/behavioral.jsonl", "watch/flight_recorder.jsonl",
    "memory/runs/ghost/trail.jsonl", "state/decisions_done.jsonl",
    "watch/inbox/DATED_METERS.jsonl", "watch/overnight_queue.jsonl",
]
basenames = {os.path.basename(p).lower(): p for p in MAJOR}

py_files = []
for d in ("mag", "tools", "scripts", "backend"):
    root = os.path.join(REPO, d)
    if not os.path.isdir(root):
        continue
    for dp, dn, fns in os.walk(root):
        dn[:] = [x for x in dn if x not in (".venv", ".git", "__pycache__")]
        for fn in fns:
            if fn.endswith(".py"):
                py_files.append(os.path.join(dp, fn))
for fn in os.listdir(REPO):
    if fn.endswith(".py") and os.path.isfile(os.path.join(REPO, fn)):
        py_files.append(os.path.join(REPO, fn))
print("py files grepped:", len(py_files))

out = {}
for cf in py_files:
    try:
        text = open(cf, "rb").read().decode("utf-8", "replace")
    except OSError:
        continue
    if ".jsonl" not in text.lower():
        continue
    crel = os.path.relpath(cf, REPO).replace("\\", "/")
    for lineno, line in enumerate(text.splitlines(), 1):
        low = line.lower()
        if ".jsonl" not in low:
            continue
        for name, target in basenames.items():
            if name in low:
                out.setdefault(target, []).append(
                    {"file": crel, "line": lineno,
                     "snippet": line.strip()[:110].encode("ascii", "replace").decode("ascii")})

json.dump(out, open(os.path.join(HERE, "_f26_readers_major.json"), "w", encoding="utf-8"), indent=1)
for t in MAJOR:
    hits = out.get(t, [])
    print("%-46s %3d hits" % (t, len(hits)))
    for h in hits[:4]:
        print("      %s:%d  %s" % (h["file"], h["line"], h["snippet"]))
