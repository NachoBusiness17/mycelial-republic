"""B2-383 board landing: retire claims, landing note, self-feeds (2026-09-26).

Targeted string surgery on QUEUE.md with an mtime guard (the B2-358/B2-373
pattern): the board is hot, so the script re-reads and retries when the
mtime moves. Self-feed numbers are computed at run time as board-highest+1
so concurrent lanes cannot be collided (B2-167 renumber law); the landing
note carries the numbers actually used. The landing note anchors on this
lane's unique row text, never the bare B2-383 token, because B2-383 is
double-spent on this board (the B2-358-fed env-var census row carries the
same number and must not be touched).
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_383_chain_quote_pin_20260926.md"
CLAIM_TS = "2026-09-26T18:05:44Z"
EARNED_GUARD = "Landed 2026-09-26 (chain-quote pin, this landing earns the pre-checked [x]"

CLAIMS = [
    (
        f"- CLAIM B2-383 mag/improve.py {CLAIM_TS}",
        f"- CLAIMED B2-383 mag/improve.py {CLAIM_TS}",
    ),
    (
        f"- CLAIM B2-383 tests/test_improve_crash_scout.py {CLAIM_TS}",
        f"- CLAIMED B2-383 tests/test_improve_crash_scout.py {CLAIM_TS}",
    ),
    (
        f"- CLAIM B2-383 watch/inbox/burn_wave_20260926/QUEUE.md {CLAIM_TS}",
        f"- CLAIMED B2-383 watch/inbox/burn_wave_20260926/QUEUE.md {CLAIM_TS}",
    ),
]

ROW_TAIL_OLD = (
    "falsifier: a single-entry log whose exception message quotes a "
    "chain-marker sentence mid-message reports chains=1 with entries=1."
)


def self_feeds(n1: int, n2: int) -> str:
    return (
        f"- [ ] B2-{n1} Pin the Traceback-header block count against quoted "
        f"headers: (self-fed by B2-383) crash_log_census still counts blocks "
        f"with the plain substring body.count(_CRASH_HEADER) "
        f"(mag/improve.py), the same disease class B2-383 just closed for "
        f"the chain markers and B2-357 for the INJECTED- marker, so an "
        f"operator crash whose message quotes 'Traceback (most recent call "
        f"last):' mid-line inflates blocks, the surface the claim and the "
        f"'guard caught N total' phrasing print, with entries and real "
        f"unchanged; add a column-0 start-anchored header count fixture-"
        f"first (tests/test_improve_crash_scout.py pattern) and keep the "
        f"guard-caught phrasing honest or drop it; falsifier: a single-entry "
        f"stanza whose message quotes the header mid-line reports blocks=2 "
        f"with entries=1 and no red test; pointers mag/improve.py "
        f"crash_log_census blocks line, tests/test_improve_crash_scout.py, "
        f"watch/inbox/burn_wave_20260926/B2_383_chain_quote_pin_20260926.md.\n"
        f"- [ ] B2-{n2} Pin chain-marker placement between the two headers: "
        f"(self-fed by B2-383) the B2-383 hardening counts a column-0 marker "
        f"sentence in any stanza holding 2+ headers, but CPython prints the "
        f"sentence BETWEEN the two sections, so a multi-line exception "
        f"message inside the SECOND traceback of a genuine chained stanza "
        f"could still land a quoted marker at column 0 and count a phantom "
        f"second link; tighten to between-headers placement (marker line "
        f"index strictly between the first and last header line index of the "
        f"stanza) fixture-first; falsifier: a 2-header stanza whose final "
        f"exception message embeds a newline plus the exact marker sentence "
        f"at column 0 reports chains=2 where the trace holds one join; "
        f"pointers mag/improve.py _CRASH_CHAIN_MARKER_RE, "
        f"tests/test_improve_crash_scout.py CHAIN_QUOTED_MULTILINE_MESSAGE, "
        f"watch/inbox/burn_wave_20260926/B2_383_chain_quote_pin_20260926.md "
        f"Falsifier.\n"
    )


def highest_b2(text: str) -> int:
    return max(int(m) for m in re.findall(r"B2-(\d+)", text))


def apply(text: str) -> str:
    if EARNED_GUARD in text:
        raise SystemExit("landing note already present; refusing to double-apply")
    for old, new in CLAIMS:
        if text.count(old) != 1:
            raise SystemExit(f"claim anchor not unique (count={text.count(old)}): {old}")
        idx = text.find(old)
        text = text[:idx] + new + text[idx + len(old):]
    if text.count(ROW_TAIL_OLD) != 1:
        raise SystemExit(f"B2-383 row tail not unique (count={text.count(ROW_TAIL_OLD)})")
    top = highest_b2(text)
    n1, n2 = top + 1, top + 2
    note = (
        " Landed 2026-09-26 (chain-quote pin, this landing earns the "
        "pre-checked [x] that sat with no receipt from its B2-372 self-feed, "
        "the B2-238 disease): crash_log_census chains counting hardened from "
        "the plain substring count to column-0 anchored matching "
        "(_CRASH_CHAIN_MARKER_RE built from _CRASH_CHAIN_MARKERS by "
        "re.escape) plus a two-header structural rule (a chain link needs "
        "two Traceback headers in the stanza), so a QUOTED marker sentence "
        "mid-message, after a type prefix, in an indented source echo, or "
        "alone on a multi-line message line never counts; owning docstring "
        "contract updated in the same breath; fixture-first red run 5 failed "
        "/ 12 passed with the brief falsifier verbatim (single-entry "
        "mid-message quote chains=1 entries=1, artifact "
        "B2_383_red_run_20260926.txt), post-fix 20 passed scout plus guard, "
        "8 adjacent passed; live census byte-still 424/424/372/52/0 on 4830 "
        "lines; ratchet NEW=0, em-dash 0 on added lines; mag/improve.py "
        "rebased on the concurrent B2-374 landing per the claim law (crash "
        "census region byte-identical, rebase named in the receipt); B2-383 "
        "double-spend flagged (this chain-quote row vs the B2-358-fed "
        "env-var census row, untouched) for a B2-255-style sweep; receipt "
        + RECEIPT
        + f"; self-fed B2-{n1}, B2-{n2} UNCHECKED."
    )
    idx = text.find(ROW_TAIL_OLD)
    text = text[:idx] + ROW_TAIL_OLD + note + text[idx + len(ROW_TAIL_OLD):]
    feeds = self_feeds(n1, n2)
    if not text.endswith("\n"):
        text += "\n"
    text += feeds
    print(f"self-fed B2-{n1}, B2-{n2}")
    return text


def main() -> int:
    for attempt in range(6):
        mtime_before = BOARD.stat().st_mtime_ns
        text = BOARD.read_bytes().decode("utf-8")
        if EARNED_GUARD in text:
            print("already applied by a prior run; nothing to do")
            return 0
        try:
            new_text = apply(text)
        except SystemExit as e:
            print(f"anchor failure: {e}")
            return 1
        time.sleep(0.2)
        if BOARD.stat().st_mtime_ns != mtime_before:
            print(f"attempt {attempt}: board moved mid-edit, re-reading")
            continue
        BOARD.write_bytes(new_text.encode("utf-8"))
        print(f"board landing applied on attempt {attempt}: claims retired, landing note, self-feeds")
        return 0
    print("FAILED: board too hot after 6 attempts; re-run this script")
    return 1


if __name__ == "__main__":
    sys.exit(main())
