"""BREAK-OPERATIONS probe: forged re-seal rows erase drift (F2 core claim).

Copies the real seal ledger to a temp file, appends one autoseal-shaped row per
drifted file carrying the file's CURRENT bytes sha (what a forger who can write
the ledger would mint), then re-runs the patrol core over the forged copy.
Pure file ops; no subprocess spawned (win32 CREATE_NO_WINDOW law moot here).
"""
import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
sys.path.insert(0, str(REPO))
from tools.prepush_seal_patrol import parse_ledger, patrol  # noqa: E402

ledger = REPO / "watch/inbox/index_events.jsonl"
tmp = Path(tempfile.mkdtemp(prefix="break_seal_")) / "forged_index_events.jsonl"
shutil.copyfile(ledger, tmp)

rows, malformed = parse_ledger(tmp)
result = patrol(REPO, rows, 1000)
drifted = [p for p, _, _ in result["drifted"]]
print(f"before forge: drifted={len(drifted)} of {result['distinct']} distinct")

forged = 0
with tmp.open("a", encoding="utf-8") as fh:
    for path in drifted:
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        rel = path.relative_to(REPO).as_posix()
        fh.write(json.dumps({
            "ts": "2026-10-05T23:59:59+00:00", "op": "autoseal",
            "file": rel, "bytes": path.stat().st_size, "sha256": sha,
            "purpose": "autoseal (rib.md.record.v1)",
        }) + "\n")
        forged += 1
print(f"appended {forged} forged autoseal rows")

rows2, _ = parse_ledger(tmp)
result2 = patrol(REPO, rows2, 1000)
print(f"after forge: drifted={len(result2['drifted'])} matched={len(result2['matched'])} "
      f"missing={result2['missing']} of {result2['distinct']} distinct")
verdict = "ok" if not result2["drifted"] else "DRIFT"
print(f"patrol verdict on forged ledger: {verdict}")
print("note: forged rows carry no writer identity, no nonce, no chain field;")
print("parse_ledger keys on file+sha256 only (tools/prepush_seal_patrol.py:91).")
