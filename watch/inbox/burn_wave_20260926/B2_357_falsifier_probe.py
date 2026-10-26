"""B2-357 falsifier probe: old scout math vs pinned census on one fixture set.

Run with the repo venv BEFORE the mag/improve.py fix to record what the old
header-minus-marker string count reports, and again AFTER to record the
pinned crash_log_census verdicts on the same bytes.

Falsifier (B2-357 brief): a crash log holding ONE chained-exception real
crash (two Traceback headers, one exception whose message quotes the literal
INJECTED- string in both sections) reports real=0 under the old math.

Fixtures mirror tests/test_improve_crash_scout.py (same constants, imported
post-fix so the two artifacts cannot drift).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tests"))

HEADER = "Traceback (most recent call last):"

QUOTED_CHAINED_REAL = (
    "\n[2026-09-26T12:00:02+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "scrub.py", line 3, in scrub\n'
    "    check(line)\n"
    "ValueError: marker INJECTED- seen in line 12\n"
    "\n"
    "During handling of the above exception, another exception occurred:\n"
    "\n"
    "Traceback (most recent call last):\n"
    '  File "seat.py", line 9, in do_turn\n'
    "    scrub(line)\n"
    "RuntimeError: marker INJECTED- escaped scrub\n"
)

PLAIN_QUOTED_REAL = (
    "\n[2026-09-26T12:00:03+00:00] stage=do_turn\n"
    "Traceback (most recent call last):\n"
    '  File "audit.py", line 7, in audit\n'
    "    scan(text)\n"
    "ValueError: pollution marker INJECTED- found in operator log line\n"
)

CHAINED_REAL_UNQUOTED = (
    "\n[2026-09-26T12:00:04+00:00] stage=one_shot\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 5, in persist\n'
    "    save()\n"
    "OSError: disk full\n"
    "\n"
    "During handling of the above exception, another exception occurred:\n"
    "\n"
    "Traceback (most recent call last):\n"
    '  File "m.py", line 9, in run\n'
    "    run_agent()\n"
    "RuntimeError: persist failed after disk full\n"
)


def old_math(text: str) -> int:
    """The pre-B2-357 scout arithmetic, verbatim from mag/improve.py."""
    return text.count(HEADER) - text.count("INJECTED-")


def main() -> None:
    print("old scout math (headers minus INJECTED- occurrences):")
    for name, text in (
        ("QUOTED_CHAINED_REAL", QUOTED_CHAINED_REAL),
        ("PLAIN_QUOTED_REAL", PLAIN_QUOTED_REAL),
        ("CHAINED_REAL_UNQUOTED", CHAINED_REAL_UNQUOTED),
    ):
        headers = text.count(HEADER)
        markers = text.count("INJECTED-")
        print(
            f"  {name}: headers={headers} INJECTED={markers} "
            f"old_real={old_math(text)} (crashes on disk: 1)"
        )
    try:
        import test_improve_crash_scout as fx  # type: ignore

        from mag.improve import crash_log_census  # type: ignore

        print("pinned crash_log_census (post-fix):")
        for name, text in (
            ("QUOTED_CHAINED_REAL", fx.QUOTED_CHAINED_REAL),
            ("PLAIN_QUOTED_REAL", fx.PLAIN_QUOTED_REAL),
            ("CHAINED_REAL_UNQUOTED", fx.CHAINED_REAL_UNQUOTED),
        ):
            c = crash_log_census(text)
            print(f"  {name}: {c}")
    except ImportError as exc:
        print(f"pinned census: N/A at this run ({exc})")


if __name__ == "__main__":
    main()
