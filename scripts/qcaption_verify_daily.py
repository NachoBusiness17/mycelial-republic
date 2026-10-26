"""qcaption_verify_daily -- the B2-271 scheduled data-side verify beat.

CAUSE (B2-271, 2026-09-26): the B2-260 pre-push caption gate fires only when
the generator or verifier script changes, so data-side rot (a hand edit of
watch/inbox/qdrop_export/q_caption_ledger.jsonl, a qdrops.jsonl re-harvest, a
mid-flight concurrent regen) sat unverified indefinitely while nobody touched
the two scripts.
FIX: a daily schtask (MagQCaptionVerifyDaily, 07:30 local, before the 08:00
MagImproveDaily beat) runs the verifier (7 checks at the B2-271 landing,
8 since B2-239 added the check8 LF-only line-ending assertion) and lands
its RESULT line
plus row count in watch/inbox/QCAPTION_VERIFY_BEAT.jsonl (append-only, one
row per run; a FAIL row is the alarm the falsifier requires). Install line
and the delete-at-life line are in the B2-271 receipt.

RUN: .venv/Scripts/python.exe scripts/qcaption_verify_daily.py
"""
from __future__ import annotations

import datetime
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
VERIFY = REPO / "scripts" / "the50_t21_q_caption_ledger_verify.py"
LEDGER = REPO / "watch" / "inbox" / "qdrop_export" / "q_caption_ledger.jsonl"
BEAT = REPO / "watch" / "inbox" / "QCAPTION_VERIFY_BEAT.jsonl"


def main() -> int:
    proc = subprocess.run(
        [str(REPO / ".venv" / "Scripts" / "python.exe"), str(VERIFY)],
        capture_output=True, text=True, timeout=1800)
    out = (proc.stdout or "") + (proc.stderr or "")
    result_line = next((ln for ln in out.splitlines()
                        if ln.startswith("RESULT:")), "RESULT: NO-OUTPUT")
    ok = proc.returncode == 0 and "RESULT: PASS" in result_line
    rows = 0
    if LEDGER.is_file():
        rows = sum(1 for ln in LEDGER.read_text(encoding="utf-8").splitlines()
                   if ln.strip())
    beat = {"ts": datetime.datetime.now(datetime.timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"),
            "schema": "qcaption_verify_beat.v1",
            "result": "PASS" if ok else "FAIL",
            "result_line": result_line,
            "ledger_rows": rows,
            "verifier_exit": proc.returncode}
    with BEAT.open("a", encoding="utf-8") as f:
        f.write(json.dumps(beat, ensure_ascii=False) + "\n")
    print(result_line, "->", beat["result"], f"({rows} rows)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
