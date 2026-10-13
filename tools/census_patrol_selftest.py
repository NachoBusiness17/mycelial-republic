#!/usr/bin/env python3
"""census_patrol_selftest.py - the census_drift_patrol CLI self-test (B2-248 split, 2026-09-26).
# B2-274 ownership law (2026-09-26): these shapes are FROZEN regression vectors, never auto-synced to the live AGENTS.md bullet; update only with a named receipt. Grammar itself is owned by CENSUS_CLAIM_RE in tools/census_drift_patrol.py (see its OWNERSHIP LAW comment block).

Split out of tools/census_drift_patrol.py to put the patrol back under the
ratchet's 400-line bar (file-too-long claim 8d41e611f98d3fa5, accepted
2026-09-26 as the bridge, pruned when this split landed). The patrol module is
INJECTED as this file's single argument instead of being imported, so nothing
here imports a sibling: the CLI path never pulls tools/__init__ (which drags
the whole toolbelt in) and the tool file never executes twice under two module
names. Consumers reach this only through census_drift_patrol.main()'s
--self-test branch, which puts this directory on sys.path before delegating.

Contract unchanged since B2-215: no network, no repo writes. 0=pass, 1=fail.
"""
from __future__ import annotations

import contextlib
import io
import tempfile
from datetime import date
from pathlib import Path


def self_test(cdp) -> int:
    """Self-test, no network, no repo writes. 0=pass, 1=fail.

    cdp is the census_drift_patrol module, injected by main(), so every check
    below exercises the live parser and verdict cores, never a stale copy.
    """
    failures: list[str] = []

    def check(name: str, condition: bool, detail: str = "") -> None:
        if condition:
            print(f"  ok: {name}")
        else:
            failures.append(name)
            print(f"  FAIL: {name}" + (f" [{detail}]" if detail else ""))

    live = ('- **Tests:** 1,837 tests collected / 301 files (2026-09-26 census, '
            '`pytest --collect-only -q`, receipt `watch/inbox/...`; retired "1,341"). '
            'Run `pytest -q` before claiming done. **Trust bytes, not reports.**')
    parsed = cdp.parse_carrier(live)
    check("live carrier parses date/collected/files",
          parsed is not None and parsed["date"] == date(2026, 9, 26)
          and parsed["collected"] == 1837 and parsed["files"] == 301,
          repr(parsed))

    # The exact retired 09-14 carrier shape: the regression case. The tripwire
    # must catch this line at today=2026-09-26 with 31 files grown.
    fossil = ("- **Tests:** 1,341 tests / 264 files (2026-09-14 census: 1305 passed / 34 failed / "
              "9 skipped, ~12 min). Run `pytest -q` before claiming done. **Trust bytes, not reports.**")
    fossil_parsed = cdp.parse_carrier(fossil)
    check("fossil carrier parses the hand-copied claim",
          fossil_parsed is not None and fossil_parsed["date"] == date(2026, 9, 14)
          and fossil_parsed["collected"] == 1341 and fossil_parsed["files"] == 264,
          repr(fossil_parsed))
    fossil_verdict = cdp.patrol(fossil_parsed["date"], date(2026, 9, 26), 31, 303, 264)
    check("the real 12-day fossil is STALE",
          fossil_verdict["verdict"] == "STALE" and fossil_verdict["exit"] == 1,
          repr(fossil_verdict))

    check("no **Tests:** line is unparseable", cdp.parse_carrier("# nothing here\n") is None)
    check("carrier without a date is unparseable", cdp.parse_carrier("- **Tests:** big suite.\n") is None)

    # D1 (arch-04, 2026-09-28; receipt watch/inbox/wave5_repair/patrol-fix.md):
    # the old CARRIER_LINE_RE "^\s*[-*]" matched newlines, so a blank line
    # before the bullet put match.start() on the blank line and the extracted
    # line was empty (exit 2 with the lying "need the claim shape" message).
    # Every frozen vector here had the bullet as line 1 or after non-blank
    # content, exactly the B2-274 blind spot; these two pin the layout.
    blanked = ('\n- **Tests:** 1,837 tests collected / 301 files (2026-09-26 census, '
               '`pytest --collect-only -q`). Trust bytes, not reports.')
    blanked_parsed = cdp.parse_carrier(blanked)
    check("blank line before a canonical claim still parses",
          blanked_parsed is not None and blanked_parsed["date"] == date(2026, 9, 26)
          and blanked_parsed["collected"] == 1837 and blanked_parsed["files"] == 301,
          repr(blanked_parsed))
    check("blank line before a malformed claim stays fail-closed None",
          cdp.parse_carrier("\n- **Tests:** the big suite, trust bytes.\n") is None)

    # B2-245 order-fragility regression: prose numbers placed ahead of the
    # claim must not become the parse (the probe read files=31 off the real
    # carrier bytes reordered so the tripwire sentence preceded the claim).
    poisoned = ('- **Tests:** Census-carrier tripwire (B2-215, 2026-09-26): the retired 1,341 '
                'headline rode 12 days stale with 31 files grown. Live: 1,837 tests collected '
                '/ 301 files (2026-09-26 census, `pytest --collect-only -q`).')
    poisoned_parsed = cdp.parse_carrier(poisoned)
    check("prose numbers before the claim cannot poison the parse",
          poisoned_parsed is not None and poisoned_parsed["date"] == date(2026, 9, 26)
          and poisoned_parsed["collected"] == 1837 and poisoned_parsed["files"] == 301,
          repr(poisoned_parsed))
    check("carrier without the canonical census clause is unparseable",
          cdp.parse_carrier("- **Tests:** 31 files grown since 2026-09-14, trust bytes.\n") is None)

    d = date(2026, 9, 26)
    check("age exactly at bar passes with growth",
          cdp.patrol(date(2026, 9, 19), d, 5, None, None)["ok"] is True)
    check("age bar+1 with growth is STALE",
          cdp.patrol(date(2026, 9, 18), d, 5, None, None)["verdict"] == "STALE")
    check("age bar+1 without any growth is OK",
          cdp.patrol(date(2026, 9, 18), d, 0, 301, 301)["ok"] is True)
    check("committed growth alone fires",
          cdp.patrol(date(2026, 9, 18), d, 2, None, None)["verdict"] == "STALE")
    # B2-247: only SHRINK below the claim is a provable disk signal; the
    # over-direction is the constant zero-collect instrument gap.
    check("disk shrink below the claim fires",
          cdp.patrol(date(2026, 9, 18), d, 0, 264, 303)["verdict"] == "STALE")
    check("over-direction is instrument lag, not stale",
          cdp.patrol(date(2026, 9, 18), d, 0, 305, 303)["ok"] is True
          and "instrument lag" in cdp.patrol(date(2026, 9, 18), d, 0, 305, 303)["reason"])
    check("same-window divergence is OK (snapshot lag tolerated)",
          cdp.patrol(date(2026, 9, 25), d, 0, 303, 301)["ok"] is True)
    check("carrier without file count leans on commits only",
          cdp.patrol(date(2026, 9, 18), d, 0, 303, None)["ok"] is True)
    check("future census is UNVERIFIABLE exit 2",
          cdp.patrol(date(2026, 10, 1), d, 0, None, None)["exit"] == 2)

    # B2-244 deep check, pure cores only: the CLI-level collection runs live
    # pytest and live in tests/test_census_drift_patrol.py, not here.
    check("collect tail parses the pytest summary",
          cdp.parse_collect_tail("tests/test_a.py::test_one\ntests/test_a.py::test_two\n"
                                 "2 tests collected in 0.01s\n") == 2)
    check("collect tail parses singular and comma forms",
          cdp.parse_collect_tail("1 test collected in 0.01s") == 1
          and cdp.parse_collect_tail("1,879 tests collected in 2.49s") == 1879)
    check("collect tail without a summary is None",
          cdp.parse_collect_tail("nothing collected here") is None)
    # B2-247: the deep check names the zero-collect instrument gap, so the
    # item-bearing file set parse is contract, pinned pure here.
    check("collect files parse to the item-bearing set",
          cdp.parse_collect_files("tests/a.py::test_one\ntests/a.py::test_two\n"
                                  "tests/b.py::TestX::test_y\n2 tests collected in 0.01s\n")
          == {"tests/a.py", "tests/b.py"})
    check("collect files ignores summary and prose lines",
          cdp.parse_collect_files("no node ids here\n1 test collected in 0.01s\n") == set())
    check("collect patrol tolerates delta below bar",
          cdp.collect_patrol(1837, 1856)["ok"] is True)
    check("collect patrol fires at the bar (20 behind)",
          cdp.collect_patrol(1837, 1857)["verdict"] == "COLLECT-DRIFT"
          and cdp.collect_patrol(1837, 1857)["exit"] == 1)
    check("collect patrol fires on over-claim too",
          cdp.collect_patrol(1900, 1879)["verdict"] == "COLLECT-DRIFT")
    check("collect patrol without a claim is exit 2",
          cdp.collect_patrol(None, 1879)["exit"] == 2)

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        tests = root / "tests"
        tests.mkdir()
        (tests / "test_a.py").write_text("def test_a():\n    pass\n", encoding="utf-8")
        (tests / "pkg").mkdir()
        (tests / "pkg" / "test_b.py").write_text("", encoding="utf-8")
        (tests / "pkg" / "suite_test.py").write_text("", encoding="utf-8")
        (tests / "helper.py").write_text("", encoding="utf-8")
        (tests / "not_a_test.txt").write_text("", encoding="utf-8")
        check("candidate count counts nested pytest-named files only",
              cdp.count_candidate_files(root) == 3, str(cdp.count_candidate_files(root)))

    # B2-338 hook pairing: githooks/pre-push case-matches the START of the
    # captured patrol output against the exact lowercase prefix "CENSUS-PATROL:
    # ok" (the ok arm); the old uppercase OK head line made every fully green
    # push print "PUSH-GATE: census WARN:". This band runs the live run()
    # emission on a synthetic estate; the git collector is stubbed because this
    # self-test runs no subprocess (the CLI pipe plus the real hook case-arm
    # bytes are replayed in tests/test_census_drift_patrol.py).
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "tests").mkdir()
        (root / "tests" / "test_a.py").write_text("", encoding="utf-8")
        (root / "AGENTS.md").write_text(
            "- **Tests:** 42 tests collected / 1 files (2026-09-26 census, "
            "`pytest --collect-only -q`). Trust bytes, not reports.\n",
            encoding="utf-8",
        )
        real_collector = cdp.test_files_added_since
        cdp.test_files_added_since = lambda _root, _census: []
        try:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                exit_code = cdp.run(root, today=date(2026, 9, 26))
        finally:
            cdp.test_files_added_since = real_collector
        green_out = buffer.getvalue()
        check("hook pairing: green run exits 0", exit_code == 0, str(exit_code))
        check("hook pairing: green output opens with the hook ok arm prefix",
              green_out.startswith("CENSUS-PATROL: ok"), repr(green_out.splitlines()[:1]))
        # red direction: the WARN arm must keep catching a stale census
        (root / "AGENTS.md").write_text(
            "- **Tests:** 1,341 tests / 264 files (2026-09-14 census: 1305 passed / "
            "34 failed / 9 skipped, ~12 min). Trust bytes, not reports.\n",
            encoding="utf-8",
        )
        cdp.test_files_added_since = lambda _root, _census: ["2026-09-20 tests/test_grown.py"]
        try:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                exit_code = cdp.run(root, today=date(2026, 9, 26))
        finally:
            cdp.test_files_added_since = real_collector
        stale_out = buffer.getvalue()
        check("hook pairing: stale run exits 1", exit_code == 1, str(exit_code))
        check("hook pairing: stale output falls to the WARN arm, never the ok prefix",
              stale_out.startswith("CENSUS-PATROL: STALE")
              and not stale_out.startswith("CENSUS-PATROL: ok"),
              repr(stale_out.splitlines()[:1]))

    if failures:
        print(f"CENSUS-PATROL SELF-TEST: FAIL - {len(failures)} failure(s): {', '.join(failures)}")
        return 1
    print("CENSUS-PATROL SELF-TEST: PASS")
    return 0
