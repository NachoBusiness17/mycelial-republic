"""B2-378 claim filing: two CLAIM lines under Open before any edit bytes.

Shared-file claim law (QUEUE.md header): mag/icon_drop.py is
working-tree-modified (B2-354 landed there at 17:40Z) and QUEUE.md is the hot
board, so both get a claim line appended directly under the "## Open" header
before this lane edits either. Anchored single insertion with an mtime guard;
re-reads and retries when a concurrent lane moves the board.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"

CLAIMS = (
    "- CLAIM B2-378 mag/icon_drop.py 2026-09-26T17:58:30Z (B2-378 fold outcome honesty: _fold_training passes the row status through to skill_ledger outcome, ok only when status dropped, else the status string; drop/drop_shortcut behavior untouched; re-read bytes before your edit per the claim law)",
    "- CLAIM B2-378 watch/inbox/burn_wave_20260926/QUEUE.md 2026-09-26T17:58:30Z (lane's own board: claim lines, B2-378 landing note, self-feed briefs; foreign CLAIMs B2-373 honored, anchored edits on freshly-read bytes, no whole-file rewrite)",
)


def main() -> int:
    for attempt in range(6):
        mtime_before = BOARD.stat().st_mtime_ns
        text = BOARD.read_text(encoding="utf-8")
        if "CLAIM B2-378 mag/icon_drop.py" in text:
            print("claims already filed; nothing to do")
            return 0
        anchor = "## Open\n"
        if text.count(anchor) != 1:
            raise SystemExit("Open header anchor not unique")
        text = text.replace(anchor, anchor + "\n".join(CLAIMS) + "\n", 1)
        time.sleep(0.2)
        if BOARD.stat().st_mtime_ns != mtime_before:
            print(f"attempt {attempt}: board moved mid-edit, re-reading")
            continue
        BOARD.write_text(text, encoding="utf-8", newline="")
        print(f"claims filed on attempt {attempt}")
        return 0
    print("FAILED: board too hot after 6 attempts; re-run this script")
    return 1


if __name__ == "__main__":
    sys.exit(main())
