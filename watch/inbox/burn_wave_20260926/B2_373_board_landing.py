"""B2-373 board landing: retire claims, landing note, self-feeds (2026-09-26).

Targeted string surgery on QUEUE.md with an mtime guard (the B2-358 pattern):
the board is hot, so the script re-reads and retries when the mtime moves.
Self-feed numbers are computed at run time as board-highest+1 so concurrent
lanes cannot be collided (B2-167 renumber law); the landing note carries the
numbers actually used.
"""
from __future__ import annotations

import re
import sys
import time
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "QUEUE.md"
RECEIPT = "watch/inbox/burn_wave_20260926/B2_373_stanza_pin_20260926.md"
CLAIM_TS = "2026-09-26T17:48:37Z"

CLAIMS = [
    (
        f"- CLAIM B2-373 tests/test_seat_crash_guard.py {CLAIM_TS}",
        f"- CLAIMED B2-373 tests/test_seat_crash_guard.py {CLAIM_TS}",
    ),
    (
        f"- CLAIM B2-373 mag/agent_cli.py {CLAIM_TS}",
        f"- CLAIMED B2-373 mag/agent_cli.py {CLAIM_TS}",
    ),
    (
        f"- CLAIM B2-373 watch/inbox/burn_wave_20260926/QUEUE.md {CLAIM_TS}",
        f"- CLAIMED B2-373 watch/inbox/burn_wave_20260926/QUEUE.md {CLAIM_TS}",
    ),
]

ROW_TAIL_OLD = (
    "pointers mag/agent_cli.py _log_seat_crash, tests/test_seat_crash_guard.py, "
    "mag/improve.py _CRASH_STANZA_RE."
)


def self_feeds(n1: int, n2: int) -> str:
    return (
        f"- [ ] B2-{n1} Census and pin the writer set of logs/seat_crashes.log: "
        f"(self-fed by B2-373) crash_log_census stanza-splitting assumes every "
        f"stanza line in the log came from the guard, and the grep census on "
        f"2026-09-26 found exactly one writer (mag/agent_cli.py _log_seat_crash "
        f"line 2517) and one reader (mag/improve.py crash scout line 631), but "
        f"nothing pins that single-writer assumption, so a second writer "
        f"emitting a bracketed-ISO line inside or between stanza bodies would "
        f"corrupt entries with zero red tests (the same unpinned-writer disease "
        f"B2-373 just closed for the prefix); census every opener of "
        f"seat_crashes.log across mag/ tools/ scripts/ and add a source-level "
        f"pin that the writer set stays exactly the guard; falsifier: a foreign "
        f"writer appending a bracketed-ISO line between two crash bodies "
        f"changes the emitted census with no test red; pointers "
        f"mag/agent_cli.py _log_seat_crash, mag/improve.py crash_log_census, "
        f"watch/inbox/burn_wave_20260926/B2_373_stanza_pin_20260926.md.\n"
        f"- [ ] B2-{n2} _log_seat_crash swallows write failures silently: "
        f"(self-fed by B2-373) the writer wraps the append in except Exception: "
        f"pass, so a sink that cannot be written (MAG_SEAT_CRASH_LOG pointed at "
        f"an unwritable path, disk full, permissions) drops every crash with no "
        f"surface naming it; the B2-358 env tripwire warns only that the "
        f"variable is SET, never that its target failed, and the seat-crash-"
        f"guard console line names the log only on success; record the failure "
        f"(console line plus a count the census or doctor can surface) instead "
        f"of the bare pass; falsifier: point MAG_SEAT_CRASH_LOG at an "
        f"unwritable path, crash the seat, and show nothing anywhere records "
        f"that the crash was not logged; pointers mag/agent_cli.py "
        f"_log_seat_crash except block, mag/env_redirect.py REDIRECT_VARS, "
        f"watch/inbox/burn_wave_20260926/B2_358_env_tripwire_20260926.md.\n"
    )


def highest_b2(text: str) -> int:
    return max(int(m) for m in re.findall(r"B2-(\d+)", text))


def apply(text: str) -> str:
    if "Landed 2026-09-26 (writer pin, this landing earns the pre-checked [x]" in text:
        raise SystemExit("landing note already present; refusing to double-apply")
    for old, new in CLAIMS:
        if text.count(old) != 1:
            raise SystemExit(f"claim anchor not unique (count={text.count(old)}): {old}")
        idx = text.find(old)
        text = text[:idx] + new + text[idx + len(old):]
    if text.count(ROW_TAIL_OLD) != 1:
        raise SystemExit(f"B2-373 row tail not unique (count={text.count(ROW_TAIL_OLD)})")
    top = highest_b2(text)
    n1, n2 = top + 1, top + 2
    note = (
        " Landed 2026-09-26 (writer pin, this landing earns the pre-checked [x]"
        " that sat with no receipt, the B2-238 disease): "
        "tests/test_seat_crash_guard.py gained _assert_stanza_shape plus the "
        "dedicated test_writer_stanza_line_matches_census_reader_regex, wired "
        "into all three writer tests: every injected run's stanza first line "
        "must match mag.improve._CRASH_STANZA_RE imported from the reader so "
        "writer and reader cannot drift, must keep the documented "
        "'[<iso-utc>] stage=<stage>' field, the census reader must see exactly "
        f"the 2 stanza boundaries this boom flow writes, and its first boundary "
        "must land at the writer's first line (preamble bytes silently drop "
        "from every census entry); mag/agent_cli.py untouched by this lane, the "
        "falsifier mutated the stanza write line twice on real bytes and both "
        "restores are sha256-verified byte-identical "
        "682812abf25c1e2ad6dae05a904454fceb0a1c8f39152486d0431c1044e0491e; "
        "falsifier on bytes: pre-pin mutation left 14 passed ZERO red while "
        "the census on the writer's own bytes collapsed a 2-crash log (1 test, "
        "1 real) to entries=1 real=0 (the brief predicted census fixtures red; "
        "bytes say deader, nothing was wired to the writer), post-pin the same "
        "mutation gives 3 failed / 12 passed and the restore gives 15 passed; "
        "probe watch/inbox/burn_wave_20260926/B2_373_falsifier_probe.py on the "
        "REAL writer through the B2-86 temp sink, results JSON alongside; "
        "probe defect recorded (constructed exceptions carry no __traceback__, "
        "header-less stanza, census rightly 0; fixed by raising through a "
        "frame); ratchet NEW=0, em-dash 0 on added lines; B2-372's chain "
        "landing rebased mid-lane (scout suite 10 to 12 tests, census gained "
        "chains) and the numbers here are post-rebase; receipt "
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
        if "Landed 2026-09-26 (writer pin, this landing earns the pre-checked [x]" in text:
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
        print(f"board landing applied on attempt {attempt}: claims retired, landing note, 2 self-feeds")
        return 0
    print("FAILED: board too hot after 6 attempts; re-run this script")
    return 1


if __name__ == "__main__":
    sys.exit(main())
