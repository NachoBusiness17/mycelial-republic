"""break-economics drift adjudication (ouroboros R3, 2026-10-05).

Independent re-adjudication of the seal-patrol drifts at my moment: for each
drifted path, the LATEST seal row (ts/op/writer) from watch/inbox/index_events.jsonl
vs the file's mtime, plus a git-status check for tracked files. Read-only.
"""
import json
import os
import subprocess
import datetime

DRIFTS = [
    "watch/inbox/STEALTH_SWEEP_LATEST.md",
    "watch/inbox/PACK_OFFLOAD.jsonl",
    "watch/inbox/STEALTH_MINED_FINDINGS.jsonl",
    "watch/inbox/frontier_olm_2026-10-04/sweep/open-and-local-language-models-x.md",
    "watch/inbox/ractor_engine/2026-10-04-eleven-doors/DOORS.jsonl",
    "watch/inbox/frontier_olm_2026-10-04/steal/open-and-local-language-models via x.md",
    "watch/inbox/frontier_olm_2026-10-04/RECEIPT.md",
    "watch/inbox/ribvault_20261005/r06_free_probe.py",
    "watch/inbox/ractor_engine/2026-10-05-ouroboros-r2-gaps/moonshot-1.md",
    "watch/inbox/frontier_olm_2026-10-05/lens/laws.md",
    "corpus/steal/MASTER_EXECUTE_REGISTER.md",
]


def norm(p: str) -> str:
    return str(p).replace("\\", "/").replace("C:/Users/foste/Documents/projects/local_sovereign_agent/", "").lstrip("/")


last = {}
with open("watch/inbox/index_events.jsonl", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except Exception:
            continue
        if not row.get("sha256"):
            continue
        key = norm(row.get("file") or row.get("path") or "")
        if not key:
            continue
        prev = last.get(key)
        if prev is None or str(row.get("ts", "")) >= str(prev.get("ts", "")):
            last[key] = row

tracked = subprocess.run(
    ["git", "status", "--porcelain", "--"] + DRIFTS,
    capture_output=True, text=True, creationflags=0x08000000,
).stdout.splitlines()

now = datetime.datetime.now().astimezone()
for d in DRIFTS:
    row = last.get(norm(d))
    if row is None:
        print(f"{d}\n   NO SEAL ROW FOUND (patrol matches on suffix; key miss = adjudication gap)")
        continue
    ts = row.get("ts", "?")
    op = row.get("op", "?")
    writer = row.get("writer", "(none)")
    try:
        seal_dt = datetime.datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        mtime = datetime.datetime.fromtimestamp(os.path.getmtime(d)).astimezone()
        delta = (mtime - seal_dt).total_seconds()
        age_min = (now - mtime).total_seconds() / 60
        print(f"{d}\n   last seal: {ts} op={op} writer={writer}\n   mtime: {mtime.isoformat()} (seal+{delta/60:.1f} min; {age_min:.0f} min ago) git: {[l for l in tracked if l.endswith(os.path.basename(d))] or 'untracked/none'}")
    except FileNotFoundError:
        print(f"{d}\n   FILE MISSING ON DISK")
