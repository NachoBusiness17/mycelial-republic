"""B2-167 step 1: append CLAIM lines to QUEUE.md before any byte is read for
editing (the shared-file claim law). Two lines: the board file claim for this
lane, and the lane-id band pre-claim for the numbers this landing will use
(four renumber slots plus three self-feed slots), the convention this lane
codifies. Appends only; never rewrites existing bytes.
"""
from __future__ import annotations

import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
QUEUE = os.path.join(HERE, "QUEUE.md")

ROW_ID = re.compile(r"^-[ \t]+\[[ x]\] B2-(\d+)\b", re.M)


def guard(text):
    if "\u2014" in text:
        raise SystemExit("em-dash law violation in appended text")
    return text


def main():
    with open(QUEUE, encoding="utf-8", errors="replace") as f:
        text = f.read()

    if "- CLAIM B2-167 watch/inbox/burn_wave_20260926/QUEUE.md " in text:
        print("B2-167 board claim already present; nothing to do")
        return 0

    top = max(int(m) for m in ROW_ID.findall(text))
    low, high = top + 1, top + 7
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    claim_board = guard(
        "- CLAIM B2-167 watch/inbox/burn_wave_20260926/QUEUE.md %s "
        "(B2-167 own board: renumber the 4 post-sweep double-claimed pairs "
        "B2-407/B2-408/B2-427/B2-428 later claimants highest+1, codify the "
        "lane-id claim law in the header block, land the B2-167 row note and "
        "earned flip, self-feed briefs; foreign active CLAIMs on this file "
        "honored, anchored edits on freshly-read bytes, no whole-file rewrite)"
        % ts
    )
    claim_band = guard(
        "- CLAIM B2-%d..B2-%d watch/inbox/burn_wave_20260926/QUEUE.md %s "
        "(B2-167 number band pre-claimed before filing rows, per the lane-id "
        "claim law this lane codifies: the first four ids for the later-"
        "claimant renumbers this lane moves in the same landing, the last "
        "three for its self-feed briefs; concurrent lanes read this band as "
        "taken and number past B2-%d)"
        % (low, high, ts, high)
    )

    with open(QUEUE, "a", encoding="utf-8", newline="") as f:
        f.write("\n".join(["", claim_board, claim_band]) + "\n")
    print("claims filed at %s: board B2-167 + band B2-%d..B2-%d" % (ts, low, high))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.exit(main())
