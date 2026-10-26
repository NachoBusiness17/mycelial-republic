"""queue_dupes_check -- the queue double-claim census as a gate (B2-486).

The B2-167 dedupe ran its census by hand (watch/inbox/burn_wave_20260926/
B2_167_census.py) and found four post-sweep doubles no gate saw. This module
promotes that census into a gate-checkable command so the census "bites on
its own":

  exit 0  every row-start id is single-claimed (within the scanned board)
  exit 1  any id is claimed by two or more brief rows
  exit 2  board file missing / unreadable (cannot verify)

Row-start forms: strict "- [x] B2-123 " plus tolerant row starts
("-\t[x] B2-123", extra spaces) that the strict regex misses; rows matching
the tolerant form but not the strict form are reported as MALFORMED warnings
(exit stays 0) so a malformed-but-single-claimed row is visible without
failing the fold. BOARD default is the burn-wave queue; pass a path to scan
another board. Read-only: never writes the board.

Ride: tools/refold_gate.py runs this next to the restore-guard audit (the
B2-343 payload pattern).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BOARD = REPO_ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"

STRICT_ROW = re.compile(r"^- \[([ x])\] B2-(\d+) ", re.M)
TOLERANT_ROW = re.compile(r"^-[ \t]+\[[ x]\] B2-(\d+)\b", re.M)


def scan(board: Path) -> dict:
    raw = board.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()

    strict = Counter(int(m.group(2)) for m in STRICT_ROW.finditer(text))
    tolerant = Counter(int(m.group(1)) for m in TOLERANT_ROW.finditer(text))

    malformed = []
    for lineno, line in enumerate(lines, 1):
        if TOLERANT_ROW.match(line) and not STRICT_ROW.match(line):
            malformed.append({"line": lineno, "prefix": line[:40]})

    dupes = sorted(i for i, c in tolerant.items() if c > 1)
    strict_dupes = sorted(i for i, c in strict.items() if c > 1)

    return {
        "ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "board": board.as_posix(),
        "bytes": len(raw),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "rows_strict": sum(strict.values()),
        "rows_tolerant": sum(tolerant.values()),
        "distinct_ids": len(tolerant),
        "highest_row_id": max(tolerant) if tolerant else None,
        "double_claimed_ids": dupes,
        "double_claimed_strict": strict_dupes,
        "malformed_row_starts": malformed,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Queue double-claim census gate (B2-486)")
    ap.add_argument("--board", default=str(DEFAULT_BOARD),
                    help="board path, repo-relative or absolute")
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent))
    ap.add_argument("--json", default="", help="optional results output path")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    board = Path(args.board)
    if not board.is_absolute():
        board = root / board
    if not board.is_file():
        print(f"QUEUE-DUPES: FAIL, cannot verify, board missing: {board}")
        return 2
    result = scan(board)
    if args.json:
        Path(args.json).write_text(json.dumps(result, indent=1), encoding="utf-8")
    if result["double_claimed_ids"]:
        print(f"QUEUE-DUPES: FAIL, {len(result['double_claimed_ids'])} id(s) "
              f"claimed by 2+ briefs: {result['double_claimed_ids']}")
        return 1
    for m in result["malformed_row_starts"]:
        print(f"QUEUE-DUPES: WARN malformed row start (counts tolerant-only): "
              f"line {m['line']}: {m['prefix']}")
    print(f"QUEUE-DUPES: ok, {result['rows_tolerant']} rows, "
          f"{result['distinct_ids']} distinct ids, 0 doubles")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
