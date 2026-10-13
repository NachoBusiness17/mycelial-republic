"""Tide amendment strike clock — the FW-18 3-strike counter.

The amendment obligation's own falsifier (state/fuel/amendments.jsonl row 1): "if three
consecutive tides produce no amendment a later reader would accept, the obligation is
ritual burden and this row self-voids." Until 2026-09-28 nothing counted the strikes, so
the falsifier could fire silently. This clock makes it loud:

  - a tide day counts as AMENDED when state/fuel/amendments.jsonl has a row whose "day"
    equals the tide day, OR the tide file carries an examined-no line ("AMENDMENT NO:");
  - strikes = consecutive most-recent tide days with no amendment;
  - exit 0 clean (<2 strikes) / exit 3 WARN (exactly 2 — the obligation is one tide from
    its falsifier) / exit 2 VOID-CONDITION-MET (>=3 — per the row-122 precedent the void
    itself stays an operator gate; the clock only refuses to let it fire silently).

Usage:
    .venv\\Scripts\\python.exe scripts\\tide_strike_clock.py
    .venv\\Scripts\\python.exe scripts\\tide_strike_clock.py --root <alt state root>   # tests

Prints one human line plus a JSON status object. The tide template runs this every cycle
and copies the verdict into the tide file, so the count is visible on the card itself.
"""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMINED_NO = re.compile(r"AMENDMENT NO\b", re.I)


def tide_days(tide_dir: Path) -> list[str]:
    days = []
    for p in tide_dir.glob("tide_*.md"):
        m = re.search(r"tide_(\d{4}-\d{2}-\d{2})\.md$", p.name)
        if m:
            days.append(m.group(1))
    return sorted(set(days))


def amendment_days(amendments_path: Path) -> set[str]:
    days = set()
    if not amendments_path.exists():
        return days
    for line in amendments_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        day = row.get("day")
        if isinstance(day, str):
            days.add(day)
    return days


def count_strikes(tide_dir: Path, amendments_path: Path) -> dict:
    days = tide_days(tide_dir)
    amended = amendment_days(amendments_path)
    strikes = 0
    first_unamended = None
    for day in reversed(days):
        tide_file = tide_dir / f"tide_{day}.md"
        examined_no = tide_file.exists() and bool(EXAMINED_NO.search(tide_file.read_text(encoding="utf-8")))
        if day in amended or examined_no:
            break
        strikes += 1
        if first_unamended is None:
            first_unamended = day
    return {
        "tides": len(days),
        "last_tide": days[-1] if days else None,
        "strikes": strikes,
        "first_unamended": first_unamended,
        "warn": strikes == 2,
        "void_condition_met": strikes >= 3,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", type=Path, default=ROOT,
                    help="repo root (override for synthetic-state tests)")
    args = ap.parse_args()

    status = count_strikes(args.root / "state" / "fuel" / "tide",
                           args.root / "state" / "fuel" / "amendments.jsonl")
    if status["void_condition_met"]:
        verdict = "VOID-CONDITION-MET (3+ consecutive no-amendment tides; row-1 falsifier satisfied - void is an operator gate, this clock only makes it loud)"
        code = 2
    elif status["warn"]:
        verdict = "WARN (2 consecutive no-amendment tides - one more and the obligation's falsifier fires)"
        code = 3
    else:
        verdict = "ok"
        code = 0
    status["verdict"] = verdict
    status["exit"] = code
    print(json.dumps(status))
    return code


if __name__ == "__main__":
    sys.exit(main())
