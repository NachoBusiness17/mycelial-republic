#!/usr/bin/env python3
"""census_drift_patrol.py - test-census freshness tripwire (B2-215, 2026-09-26).

The disease this meters (watch/inbox/burn_wave_20260926/B2_69_test_census_20260926.md):
the estate carried the hand-copied "1,341 tests / 264 files" headline for 12
days (2026-09-14 to 2026-09-26) while tests/ grew 31 files, because the boot
freshness gate watches boot docs and no gate watched the test-count carrier.

Bar stated in numbers BEFORE reading anything:

  the live census carrier (AGENTS.md, the "**Tests:**" bullet) is STALE when its
  census date is older than CENSUS_STALE_DAYS (default 7) AND tests/ has grown
  since that census day. Growth is measured from bytes two ways: test files added
  by git commits dated strictly after the census date, or the on-disk candidate
  count dropping BELOW the carrier's claimed file count (B2-247: candidates >=
  item-bearing files always holds, so the over-direction is the constant
  zero-collect instrument gap, never growth; only shrink is provable drift).

Inside the window a lagging carrier is tolerable: a census is a snapshot and lanes
land test files daily, so a same-day mismatch is reported as evidence, never as a
violation. The tripwire fires only when the snapshot is old AND the world moved under it.

Fail-closed by construction: a missing carrier file, a missing or unparseable
"**Tests:**" line (the claim must sit in the canonical shape "N tests [collected]
/ M files (YYYY-MM-DD census"; prose numbers elsewhere on the bullet never
parse, the B2-245 order-fragility fix), an unparseable census date, a
future-dated census (fabrication smell, freshness_gate.py convention), or a
git failure is exit 2, never a guess and never a pass.

Exit codes: 0 = census inside the bar; 1 = STALE or COLLECT-DRIFT (refresh:
rerun `pytest --collect-only -q`, then update the carrier with the new counts
and today's date); 2 = cannot verify.

Usage: python tools/census_drift_patrol.py [--root PATH] [--days N]
       [--collect] [--collect-tolerance N] [--self-test]

The default gate never runs pytest; growth is measured by git and disk bytes
only, which keeps pre-push fast and dependency-free (B2-69 receipt).

The --self-test body lives in tools/census_patrol_selftest.py (B2-248 split,
2026-09-26, which returned this file under the ratchet's 400-line bar, claim
8d41e611f98d3fa5); main() delegates to it with this module injected, so the
checks still run the live parser and verdict cores and no sibling import sits
at module scope.

The --collect byte-gatherers live in tools/census_collect.py (B2-365 split,
2026-09-26, same bar: this file stood at exactly 400/400 lines so the next
touch would have re-opened NEW file-too-long debt). The delegating defs
parse_collect_tail/parse_collect_files keep this module's attribute surface
frozen for census_patrol_selftest and tests/test_census_drift_patrol.py, and
run() reaches collect_report through the same lazy sibling import.

Deep check (B2-244, 2026-09-26): the file-growth signal is blind to items added
inside existing files (parametrize, cases appended to a suite), so a carrier can
read 1,837 collected while reality holds 1,879 and the default gate stays green
(that delta of 42 was measured live on 2026-09-26: base exit 0, deep check red).
The opt-in --collect flag reruns `pytest --collect-only -q` under --root with the
interpreter executing this tool, parses the "N tests collected" summary tail, and
fails exit 1 when the carrier's collected claim is COLLECT_DRIFT_TOLERANCE
(default 20) or more off the byte truth in either direction. It stays out of the
default pre-push path because it needs the venv and a full collection pass.
B2-247: the deep check also names the zero-collect candidates (the instrument
gap above) and the collected-files vs carrier-files delta every run, so the gap
never moves unnamed after a refresh.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
CARRIER_RELPATH = "AGENTS.md"

CENSUS_STALE_DAYS = 7
# D2 (arch-04, receipt wave5_repair/patrol-fix.md): FUTURE_TOLERANCE_DAYS was dead
# code (run() tolerated today+1, patrol() exit-2s any negative age); gate now > today.

# The live carrier line: the AGENTS.md Clippy bullet that opens "**Tests:**" (D1, arch-04: horizontal whitespace ONLY - "\s*" ate newlines, so a blank line before the bullet landed match.start() on the blank line and the extracted line was empty, an exit 2 with the lying "need the claim shape" message).
CARRIER_LINE_RE = re.compile(r"^[ \t]*[-*][ \t]*\*\*Tests:\*\*", re.MULTILINE)
# The census claim is read ONLY from the parenthesized census clause, where the
# counts and the census date are adjacent. B2-245 fix (2026-09-26; evidence:
# watch/inbox/burn_wave_20260926/B2_245_parser_order_20260926.md and probe
# B2_245_parser_order_probe.py, which read files=31 off the real carrier bytes
# reordered so the tripwire prose "31 files grown" preceded the claim): the
# retired DATE_RE/COLLECTED_RE/FILES_RE took the FIRST date and the FIRST
# "N tests"/"N files" match anywhere on the bullet, so prose numbers ahead of
# the claim silently became the parse. Anchored on the clause shape, a prose
# number can only poison the parse by itself forming a full census claim.
# Matches both carrier shapes: "N tests collected / M files (YYYY-MM-DD census"
# (live) and "N tests / M files (YYYY-MM-DD census" (retired fossil, kept
# parseable so the tripwire keeps catching it if it ever comes back).
#
# OWNERSHIP LAW (B2-274, 2026-09-26; cause: the carrier regression fixtures
# live in three hand-copied places while the live AGENTS.md bullet refreshes
# under its own laws, so the fixtures must stay frozen or a grammar break is
# invisible):
# - PARSER GRAMMAR is owned by THIS regex plus this comment block. Any change
#   to the claim shape is a spec change here first, with a receipt.
# - FROZEN REGRESSION VECTORS are owned by tools/census_patrol_selftest.py
#   (live/fossil/poisoned shapes) and tests/test_census_drift_patrol.py
#   (LIVE_SHAPE/FOSSIL_SHAPE). They are NEVER auto-synced to the live
#   AGENTS.md bullet: the live count moving (1,837 -> 1,879 -> 1,910 in one
#   day) must not move the fixtures, because a frozen vector is the only
#   witness that can catch a grammar break. Update a vector ONLY with a
#   named receipt explaining why the frozen number is no longer the truth
#   being pinned.
# - The gap this law exists to close (measured in the B2-274 receipt
#   experiment): reword the AGENTS.md bullet to any other grammar and the
#   parser unchanged leaves self-test and pytest GREEN while the live patrol
#   fail-closes exit 2 "need the claim shape" - the two frozen surfaces
#   cannot see a live-carrier reword, and the B2-249 shape-law sentence on
#   the AGENTS.md bullet is the only surface that warns the reworder.
CENSUS_CLAIM_RE = re.compile(
    r"(\d[\d,]*)\s+tests\b(?:\s+collected)?\s*/\s*(\d[\d,]*)\s+files\b\s*\(\s*(\d{4}-\d{2}-\d{2})\s+census\b"
)
TEST_FILE_SUFFIXES = ("test_*.py", "*_test.py")  # pytest python_files defaults

# B2-244 deep check: collected-claim drift bar. Below it the intra-day landing
# noise of a live estate is tolerated; at or above it the claim is materially
# wrong and the check fails, in either direction.
COLLECT_DRIFT_TOLERANCE = 20
# The collectors (COLLECT_TAIL_RE, parse_collect_tail, parse_collect_files,
# collect_report) live in tools/census_collect.py since the B2-365 split
# (2026-09-26; this file sat at exactly 400 of the ratchet's 400 lines, so the
# next fix would have re-opened file-too-long debt). The delegating defs below
# keep this module's attribute surface frozen for the self-test and tests,
# which reach cdp.parse_collect_tail / cdp.parse_collect_files by name.

# Mickey17 W2 zero-collect tolerant list (2026-09-29; receipt
# watch/inbox/W2_ZERO_COLLECT_20260929.md; cause: wave ledger return 7,
# test files that collect zero items hide inside the aggregate denominators
# because "N tests / M files" never says WHICH files carry the items, so
# test_selffeed_integration.py rode every census as a counted file while
# collecting nothing). Repo-relative posix paths of test-shaped files that are
# legitimately empty and may stay that way; everything else that collects zero
# fails the --collect deep check exit 1. Seeded EMPTY on purpose: the only real
# zero-collect file found (tests/test_selffeed_integration.py, the 08:30
# 2026-09-29 deep-check log) is the disease itself, a __main__ script wearing
# pytest naming, not a legitimately-empty fixture; the cure there is renaming
# or converting it, never tolerance. Add an entry ONLY with a receipt naming
# why the file may never collect items.
ZERO_COLLECT_TOLERANT: frozenset[str] = frozenset()


class PatrolError(Exception):
    """Cannot-verify condition; main() maps this to exit 2."""


def _collect_mod():
    """Lazy sibling import (no tools/__init__ pull on the CLI path, the
    B2-248 context rule): script dir first, then the collectors module."""
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import census_collect
    return census_collect


def parse_carrier(text: str) -> dict | None:
    """Parse the live census claim out of carrier text.

    Returns {"date": date, "collected": int, "files": int, "line": str} or None
    when no "**Tests:**" line exists or the line lacks the canonical claim shape
    "N tests [collected] / M files (YYYY-MM-DD census". Only the parenthesized
    census clause is read (B2-245, 2026-09-26): prose numbers elsewhere on the
    bullet cannot poison the parse, and a non-canonical bullet is fail-closed
    None (exit 2 upstream), never a guess.
    """
    match = CARRIER_LINE_RE.search(text)
    if match is None:
        return None
    line = text[match.start(): text.find("\n", match.start()) if text.find("\n", match.start()) != -1 else len(text)]
    claim = CENSUS_CLAIM_RE.search(line)
    if claim is None:
        return None
    return {
        "date": date.fromisoformat(claim.group(3)),
        "collected": int(claim.group(1).replace(",", "")),
        "files": int(claim.group(2).replace(",", "")),
        "line": line,
    }


def candidate_files(root: Path) -> set[Path]:
    """On-disk test-file candidates under tests/ (pytest default naming)."""
    tests_dir = root / "tests"
    seen: set[Path] = set()
    for pattern in TEST_FILE_SUFFIXES:
        seen.update(p for p in tests_dir.rglob(pattern) if p.is_file())
    return seen


def count_candidate_files(root: Path) -> int:
    """len(candidate_files(root)): the disk candidate count, gap included."""
    return len(candidate_files(root))


def parse_collect_tail(stdout: str) -> int | None:
    """Delegates to census_collect.parse_collect_tail (B2-365 split)."""
    return _collect_mod().parse_collect_tail(stdout)


def parse_collect_files(stdout: str) -> set[str]:
    """Delegates to census_collect.parse_collect_files (B2-365 split)."""
    return _collect_mod().parse_collect_files(stdout)


def collect_patrol(claimed: int | None, real: int,
                   tolerance: int = COLLECT_DRIFT_TOLERANCE) -> dict:
    """Pure deep-check verdict core. COLLECT-DRIFT = |real - claimed| >= bar.

    Symmetric on purpose: an under-claim is the B2-244 disease (items grown
    inside existing files while the carrier froze), an over-claim is worse
    (tests removed or a number invented). A carrier line without a parsable
    collected claim cannot be compared against bytes and is exit 2.
    """
    if claimed is None:
        return {"ok": False, "verdict": "UNVERIFIABLE", "exit": 2,
                "reason": "carrier line has no parsable collected claim to compare against pytest bytes"}
    delta = real - claimed
    if abs(delta) >= tolerance:
        return {"ok": False, "verdict": "COLLECT-DRIFT", "exit": 1,
                "reason": f"collected drift: pytest holds {real} vs carrier claim {claimed} "
                          f"(delta {delta:+d}, bar {tolerance})"}
    return {"ok": True, "verdict": "OK", "exit": 0,
            "reason": f"collected claim within bar: pytest {real} vs carrier {claimed} "
                      f"(delta {delta:+d}, bar {tolerance})"}


def zero_collect_patrol(disk_files: set[str], collected_files: set[str],
                        tolerant: "frozenset[str] | set[str]" = ZERO_COLLECT_TOLERANT) -> dict:
    """Pure deep-check verdict core (Mickey17 W2, 2026-09-29; receipt
    watch/inbox/W2_ZERO_COLLECT_20260929.md). ZERO-COLLECT = a pytest-named
    candidate file on disk that contributed zero collected node ids (empty
    file or collection-skipped) and is not in the tolerant list.

    Cause fixed on evidence: the wave ledger return 7 finding, the B2-247
    instrument-gap line could NAME these files but never fail on them, so
    tests/test_selffeed_integration.py (a __main__ script wearing test_*.py
    naming, zero items) hid inside "N tests / M files" denominators across
    every census refresh. disk minus collected minus tolerant, fail-closed on
    the remainder; the tolerant list is for legitimately-empty fixtures only
    and each entry owes a receipt (see ZERO_COLLECT_TOLERANT above).
    """
    zero = sorted(disk_files - collected_files - set(tolerant))
    if zero:
        return {"ok": False, "verdict": "ZERO-COLLECT", "exit": 1,
                "reason": f"{len(zero)} test file(s) collect zero items: {', '.join(zero)}",
                "files": zero}
    tolerated = sorted(disk_files - collected_files)
    detail = "every disk candidate collects items"
    if tolerated:
        detail += f" ({len(tolerated)} tolerated empty: {', '.join(tolerated)})"
    return {"ok": True, "verdict": "OK", "exit": 0, "reason": detail, "files": []}


def test_files_added_since(root: Path, census_date: date) -> list[str]:
    """Test files under tests/ added by commits dated strictly after census_date.

    Strictly-after-the-day (not after-the-instant): the census was taken some
    time during its own day, so same-day commits are ambiguous and are not
    counted against the snapshot. Git failure raises PatrolError (exit 2,
    refusing to guess), mirroring freshness_check.py's _git law.
    """
    out = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%cI", "--name-only", "--", "tests/"],
        cwd=root, capture_output=True, text=True, timeout=60,
    )
    if out.returncode != 0:
        raise PatrolError(f"git log failed: {out.stderr.strip()[:200]}")
    added: list[str] = []
    commit_day: date | None = None
    for raw in out.stdout.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("20"):
            try:
                commit_day = datetime.fromisoformat(line).astimezone().date()
            except ValueError:
                commit_day = None
            continue
        if commit_day is not None and commit_day > census_date and line.startswith("tests/"):
            added.append(f"{commit_day.isoformat()} {line}")
    return added


def patrol(census: date, today: date, added_since: int, disk_files: int | None,
           carrier_files: int | None, max_age_days: int = CENSUS_STALE_DAYS) -> dict:
    """Pure verdict core. STALE = age beyond bar AND growth since the census.

    Growth: commits added test files after the census day, or the disk count
    SHRANK below the claim (B2-247: item-bearing files are a subset of
    candidates, so the over-direction is the zero-collect instrument gap,
    evidence only, never growth; only shrink is provable drift).
    """
    age_days = (today - census).days
    committed_growth = added_since > 0
    disk_shrink = (
        carrier_files is not None and disk_files is not None and disk_files < carrier_files
    )
    grew = committed_growth or disk_shrink
    stale = age_days > max_age_days and grew
    if age_days < 0:
        return {"ok": False, "verdict": "UNVERIFIABLE", "exit": 2,
                "reason": f"census dated {age_days} days in the future (fabrication smell)"}
    if stale:
        signals = []
        if committed_growth:
            signals.append(f"{added_since} test file(s) added by commits after {census.isoformat()}")
        if disk_shrink:
            signals.append(f"disk holds {disk_files} candidate files vs carrier claim "
                           f"{carrier_files} (shrink: files deleted or claim invented)")
        return {"ok": False, "verdict": "STALE", "exit": 1,
                "reason": f"census {age_days}d old (bar {max_age_days}d) while tests/ grew: "
                          + "; ".join(signals),
                "age_days": age_days, "added_since": added_since}
    detail = f"census {age_days}d old of {max_age_days}d bar"
    if committed_growth:
        detail += f", growth noted but inside the window ({added_since} file(s) since census)"
    if disk_files is not None and carrier_files is not None and disk_files != carrier_files:
        detail += (f", disk {disk_files} vs carrier {carrier_files} (instrument lag: disk counts "
                   f"pytest-named candidates, carrier counts item-bearing files; zero-collect "
                   f"candidates named by --collect; same-window lag, evidence only)")
    return {"ok": True, "verdict": "OK", "exit": 0, "reason": detail,
            "age_days": age_days, "added_since": added_since}


def run(root: Path, max_age_days: int = CENSUS_STALE_DAYS, today: date | None = None,
        collect: bool = False, collect_tolerance: int = COLLECT_DRIFT_TOLERANCE) -> int:
    """Gather bytes and print the verdict. Returns the process exit code.

    With collect=True the deep check runs after the default gate: the base
    verdict prints first (exit 2 paths return before it), then the collect-only
    comparison may raise a green base result to exit 1 (COLLECT-DRIFT) or drop
    to exit 2 when the collection itself cannot be verified.
    """
    today = today or date.today()
    carrier_path = root / CARRIER_RELPATH
    if not carrier_path.is_file():
        print(f"CENSUS-PATROL: cannot verify, carrier missing: {CARRIER_RELPATH}")
        return 2
    parsed = parse_carrier(carrier_path.read_text(encoding="utf-8", errors="replace"))
    if parsed is None:
        print(f"CENSUS-PATROL: cannot verify, no parsable **Tests:** census line in {CARRIER_RELPATH} "
              "(need the claim shape: N tests [collected] / M files (YYYY-MM-DD census ...)")
        return 2
    if parsed["date"] > today:
        print(f"CENSUS-PATROL: cannot verify, census dated {parsed['date']} is in the future (fabrication smell)")
        return 2
    try:
        added = test_files_added_since(root, parsed["date"])
        disk_files = count_candidate_files(root)
    except PatrolError as exc:
        print(f"CENSUS-PATROL: cannot verify, {exc}")
        return 2
    verdict = patrol(parsed["date"], today, len(added), disk_files, parsed["files"], max_age_days)
    head = f"census {parsed['date']} ({parsed['collected']} collected / {parsed['files']} files)"
    # B2-338 (receipt watch/inbox/burn_wave_20260926/B2_338_case_fix_20260926.md):
    # the hook case-matches the START of this output against the lowercase
    # prefix "CENSUS-PATROL: ok"; the old uppercase OK head line took the WARN arm
    # on every fully green push, training operators to dismiss the channel.
    print(f"CENSUS-PATROL: {'ok' if verdict['ok'] else verdict['verdict']} - {head}")
    for row in added[:10]:
        print(f"  grew: {row}")
    if len(added) > 10:
        print(f"  ... and {len(added) - 10} more added since {parsed['date']}")
    print(f"  disk candidate files: {disk_files}")
    base_exit = 0
    if verdict["ok"]:
        print(f"CENSUS-PATROL: ok - {verdict['reason']}")
    elif verdict["exit"] == 1:
        print(f"CENSUS-PATROL: STALE - {verdict['reason']}")
        print("  Fix: rerun `.venv/Scripts/python.exe -m pytest --collect-only -q`, then refresh the "
              f"{CARRIER_RELPATH} **Tests:** bullet with the new counts and today's date.")
        base_exit = 1
    else:
        print(f"CENSUS-PATROL: {verdict['reason']}")
        return 2
    if not collect:
        return base_exit
    collectors = _collect_mod()
    try:
        report = collectors.collect_report(root)
    except collectors.CollectError as exc:
        print(f"CENSUS-PATROL: cannot verify collect deep check, {exc}")
        return 2
    except subprocess.TimeoutExpired:
        print("CENSUS-PATROL: cannot verify collect deep check, pytest --collect-only timed out")
        return 2
    real = report["items"]
    print(f"  collect-only tail: {real} tests collected")
    # B2-247: name the gap and the files delta every run; movement is named.
    disk_rel = {p.relative_to(root).as_posix() for p in candidate_files(root)}
    gap = sorted(disk_rel - report["files"])
    if gap:
        print(f"  instrument gap: {len(gap)} zero-collect candidate(s): {', '.join(gap)}")
    else:
        print("  instrument gap: none, every disk candidate collects items")
    print(f"  files: collected {len(report['files'])} vs carrier claim {parsed['files']}")
    deep = collect_patrol(parsed["collected"], real, collect_tolerance)
    # Mickey17 W2 (2026-09-29; receipt watch/inbox/W2_ZERO_COLLECT_20260929.md):
    # the B2-247 gap line above stays evidence for every candidate, and the
    # non-tolerated remainder now fails exit 1 naming each file, because the
    # aggregate denominators hid zero-item test files across every census
    # refresh (return 7: test_selffeed_integration.py collected 0 for weeks).
    # Module global read at call time (not a def-time default) so the tolerant
    # list stays overridable by tests without redefining the core.
    zero = zero_collect_patrol(disk_rel, report["files"], ZERO_COLLECT_TOLERANT)
    if deep["ok"] and zero["ok"]:
        print(f"CENSUS-PATROL: collect ok - {deep['reason']}; {zero['reason']}")
        return base_exit
    for verdict in (deep, zero):
        if not verdict["ok"]:
            print(f"CENSUS-PATROL: {verdict['verdict']} - {verdict['reason']}")
    if not deep["ok"]:
        print("  Fix: rerun `.venv/Scripts/python.exe -m pytest --collect-only -q`, then refresh the "
              f"{CARRIER_RELPATH} **Tests:** bullet with the real counts and today's date.")
    if not zero["ok"]:
        print("  Fix: give the named file(s) real test items or delete them; a fixture that is "
              "empty on purpose joins ZERO_COLLECT_TOLERANT in tools/census_drift_patrol.py "
              "only with a receipt.")
    # Both cores exit 0 or 1 here (collect_patrol's exit-2 arm needs a None
    # claim, impossible after parse_carrier), so any red verdict is exit 1.
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="test-census freshness tripwire (B2-215)")
    parser.add_argument("--root", type=Path, default=ESTATE_ROOT,
                        help="estate root holding AGENTS.md, tests/ and .git (default: this repo)")
    parser.add_argument("--days", type=int, default=CENSUS_STALE_DAYS,
                        help=f"stale bar in days (default {CENSUS_STALE_DAYS})")
    parser.add_argument("--self-test", action="store_true", help="run the self-test and exit")
    parser.add_argument("--collect", action="store_true",
                        help="deep check (B2-244): rerun pytest --collect-only -q and compare the "
                             "carrier's collected claim; needs the venv, never in the default path")
    parser.add_argument("--collect-tolerance", type=int, default=COLLECT_DRIFT_TOLERANCE,
                        help=f"collected-claim drift bar for --collect (default {COLLECT_DRIFT_TOLERANCE})")
    args = parser.parse_args(argv)
    if args.self_test:
        # B2-248 split: the self-test body lives in census_patrol_selftest and
        # this module is injected into it, so no sibling import sits at module
        # scope (the CLI path never pulls tools/__init__). The script's own
        # directory goes on sys.path first so the delegation works from any
        # consumer context: pre-push and the test subprocesses run this file
        # by path, and `python -m tools.census_drift_patrol` reaches here too.
        here = str(Path(__file__).resolve().parent)
        if here not in sys.path:
            sys.path.insert(0, here)
        from census_patrol_selftest import self_test
        return self_test(sys.modules[__name__])
    return run(args.root.resolve(), max_age_days=args.days, collect=args.collect,
               collect_tolerance=args.collect_tolerance)


if __name__ == "__main__":
    sys.exit(main())
