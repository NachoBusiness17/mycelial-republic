#!/usr/bin/env python3
"""B2-95 prune-gap close: re-accept the 25 mimosa claims a routine prune reaped.

The brief said the mimosa claims from B2-11 "are reaped by design on the next
prune"; the bytes say the reap already happened. HEAD's
configs/violation_baseline.json (updated 2026-09-26T08:05:18) holds 902
accepted claims including the 25 mimosa-* entries; the working tree after a
midday prune (updated 2026-09-26T13:37:24) holds 876 and zero mimosa entries,
exactly the reap B2-11's falsifier named in advance
(watch/inbox/burn_wave_20260926/B2_11_mimosa_close_20260926.md: "prune reaps
the mimosa claims and nobody re-accepts them (check register size 901 after
any prune)").

Source of truth for re-acceptance: HEAD's baseline bytes, not a rewrite. This
script reads `git show HEAD:configs/violation_baseline.json`, copies every
accepted claim whose rule starts with "mimosa-" that is missing from the
working baseline, and leaves every other byte of the register untouched. The
reap itself is closed at the design level by the tools/violation_ratchet.py
prune-domain fix (prune keeps externally sourced claims), pinned by
tests/test_violation_ratchet.py.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASELINE = ROOT / "configs" / "violation_baseline.json"
BY = "agent:B2-95 flash-lane burn 2026-09-26 (prune-gap close, re-accept from HEAD)"


def main() -> int:
    head = subprocess.run(
        ["git", "show", "HEAD:configs/violation_baseline.json"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=60,
    )
    if head.returncode != 0:
        print(f"B2-95 reaccept: git show failed: {head.stderr.strip()}")
        return 2
    head_accepted = json.loads(head.stdout).get("accepted", {})
    mimosa = {fp: e for fp, e in head_accepted.items()
              if str(e.get("rule", "")).startswith("mimosa-")}
    baseline = json.loads(BASELINE.read_text(encoding="utf-8"))
    accepted = baseline.setdefault("accepted", {})
    readded, already = [], 0
    for fp, entry in sorted(mimosa.items()):
        if fp in accepted:
            already += 1
            continue
        restored = dict(entry)
        restored["reaccepted"] = datetime.now().isoformat(timespec="seconds")
        restored["reaccepted_by"] = BY
        accepted[fp] = restored
        readded.append(fp)
    baseline["updated"] = datetime.now().isoformat(timespec="seconds")
    BASELINE.write_text(json.dumps(baseline, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8")
    print(f"B2-95 reaccept: HEAD-mimosa={len(mimosa)}; RE-ADDED={len(readded)}; "
          f"already-present={already}; register now {len(accepted)} "
          f"-> {BASELINE.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
