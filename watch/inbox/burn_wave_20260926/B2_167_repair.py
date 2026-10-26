"""B2-167 repair pass: the first landing apply had a prefix-slicing defect
(old_prefix carried the id, line[len(prefix):] dropped the row title), so the
four moved rows kept their old id and lost their title while the collision
notes already carried the new ids. This pass restores each title byte-exact
from the landing script's own MOVES prefixes and applies the id the note
names. Anchored, mtime-guarded, one write.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"

REPAIRS = [
    (
        "- [ ] B2-407  the B2-12 builder",
        "- [ ] B2-482 Matched-copy identity audit: the B2-12 builder",
    ),
    (
        "- [ ] B2-408  media_recovered_register",
        "- [ ] B2-483 Reconcile the 314 recovered media into the caption ledger: media_recovered_register",
    ),
    (
        "- [ ] B2-427  re-run",
        "- [ ] B2-484 File the LAW-12 clause verdict on or before 2026-10-10: re-run",
    ),
    (
        "- [ ] B2-428  once its CLAIM lines",
        "- [ ] B2-485 Verify the B2-164 scenario-suite-at-pre-push landing once its CLAIM lines",
    ),
]


def main() -> int:
    for attempt in range(8):
        mtime_before = BOARD.stat().st_mtime_ns
        text = BOARD.read_bytes().decode("utf-8")
        if "- [ ] B2-482 Matched-copy identity audit:" in text:
            print("repair already applied; nothing to do")
            return 0
        ok = True
        for old, new in REPAIRS:
            c = text.count(old)
            if c != 1:
                print("anchor not unique (%d): %s" % (c, old[:60]))
                ok = False
        if not ok:
            return 1
        for old, new in REPAIRS:
            text = text.replace(old, new, 1)
        time.sleep(0.2)
        if BOARD.stat().st_mtime_ns != mtime_before:
            print("attempt %d: board moved mid-edit, re-reading" % attempt)
            continue
        BOARD.write_bytes(text.encode("utf-8"))
        print("repair applied on attempt %d: 4 titles restored, ids 482-485 applied" % attempt)
        return 0
    print("FAILED: board too hot after 8 attempts")
    return 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
