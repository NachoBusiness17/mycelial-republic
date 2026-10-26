"""SW-07 lane helper: append a landing note to this slice's own QUEUE.md row
and append a LEDGER.jsonl row. Anchored edit on freshly-read bytes each run;
asserts the anchor is unique before writing; never rewrites the whole file
beyond the single anchored replacement.

Usage:
  .venv/Scripts/python.exe SW07_row_landing.py row <brief-id> <landing-note-tail>
  .venv/Scripts/python.exe SW07_row_landing.py ledger <slug> <verdict> <landing> <one_line>
"""
from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
QUEUE = REPO / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
LEDGER = REPO / "memory" / "burns" / "LEDGER.jsonl"


def row(brief_id: str, tail: str) -> None:
    with QUEUE.open("r", encoding="utf-8", newline="") as f:
        data = f.read()
    lines = data.split("\n")
    idxs = [i for i, ln in enumerate(lines)
            if ln.startswith("- [") and len(ln) > 4 and ln[4] == "]" and f" {brief_id} " in ln[:24]]
    if len(idxs) != 1:
        raise SystemExit(f"anchor for {brief_id} matched {len(idxs)} rows, refusing")
    i = idxs[0]
    if "Landed 2026-09-26" in lines[i]:
        print(f"{brief_id} row already carries a landing note; no edit")
        return
    lines[i] = lines[i].rstrip() + " " + tail.strip()
    with QUEUE.open("w", encoding="utf-8", newline="") as f:
        f.write("\n".join(lines))
    print(f"{brief_id} row landing note appended (line {i + 1})")


def ledger(slug: str, verdict: str, landing: str, one_line: str) -> None:
    rec = {
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "slug": slug,
        "verdict": verdict,
        "landing": landing,
        "one_line": one_line,
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("ledger appended", rec["ts"], slug)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "row":
        row(sys.argv[2], sys.argv[3])
    elif cmd == "ledger":
        ledger(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        raise SystemExit("unknown command")
