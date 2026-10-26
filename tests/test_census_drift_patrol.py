"""Census drift patrol tests (B2-215, 2026-09-26).
# B2-274 ownership law (2026-09-26): these shapes are FROZEN regression vectors, never auto-synced to the live AGENTS.md bullet; update only with a named receipt. Grammar itself is owned by CENSUS_CLAIM_RE in tools/census_drift_patrol.py (see its OWNERSHIP LAW comment block).

Covers the contract in four bands, following tests/test_freshness_gate.py
house style: the pure verdict cores (patrol/parse_carrier, plus the B2-244
deep-check pair parse_collect_tail/collect_patrol) including the real
retired 09-14 fossil line as the regression case, the byte collectors
(candidate file count, git added-since), the real CLI exit codes
(0 fresh, 1 STALE / COLLECT-DRIFT, 2 cannot-verify) pinned through a
subprocess against a synthetic mini-estate in tmp_path, and the B2-244
falsifier: a carrier 20+ behind with zero new files passes the default gate
and fails the --collect deep check. B2-247 adds the instrument-gap band: the
disk candidate count is candidates (zero-collect files included), the carrier
counts item-bearing files, only shrink is a stale signal, and every --collect
run names the zero-collect candidates so the gap never moves unnamed. B2-338
adds the fifth band, the hook pairing: the FIRST output line is the contract
githooks/pre-push case-matches (lowercase "CENSUS-PATROL: ok" opens a green
run; red verdicts keep their uppercase tokens and fall to the WARN arm), pinned
through the CLI subprocess and a sh replay of the hook's real case-arm bytes.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

# Module import, not from-imports: the tool exports a test_files_added_since
# helper, and importing that name (or aliasing it at module level) drops a
# test_-prefixed object into this module's namespace for pytest to
# mis-collect (the 2026-09-26 collection error). Call it as cdp.test_files_added_since.
import tools.census_drift_patrol as cdp

count_candidate_files = cdp.count_candidate_files
parse_carrier = cdp.parse_carrier
patrol = cdp.patrol
run = cdp.run

TOOL = Path(__file__).resolve().parents[1] / "tools" / "census_drift_patrol.py"

LIVE_SHAPE = (
    "- **Tests:** 1,837 tests collected / 301 files (2026-09-26 census, "
    "`pytest --collect-only -q`, receipt `watch/inbox/x.md`; retired 1,341). "
    "**Trust bytes, not reports.**"
)
FOSSIL_SHAPE = (
    "- **Tests:** 1,341 tests / 264 files (2026-09-14 census: 1305 passed / 34 failed / "
    "9 skipped, ~12 min). Run `pytest -q` before claiming done. **Trust bytes, not reports.**"
)


# --- parse_carrier -----------------------------------------------------------

def test_live_carrier_shape_parses():
    parsed = parse_carrier(LIVE_SHAPE)
    assert parsed == {
        "date": date(2026, 9, 26), "collected": 1837, "files": 301, "line": LIVE_SHAPE,
    }


def test_fossil_carrier_shape_parses():
    parsed = parse_carrier(FOSSIL_SHAPE)
    assert parsed is not None
    assert parsed["date"] == date(2026, 9, 14)
    assert parsed["collected"] == 1341
    assert parsed["files"] == 264


def test_missing_tests_line_is_none():
    assert parse_carrier("# rules\n- **Deliberate-ask:** small asks.\n") is None


def test_tests_line_without_date_is_none():
    assert parse_carrier("- **Tests:** the big suite, trust bytes.\n") is None


def test_prose_numbers_before_claim_cannot_poison_parse():
    # B2-245 falsifier regression: the tripwire sentence moved ahead of the
    # claim. The old first-match parser read files=31 off the real carrier
    # bytes reordered this way (B2_245_parser_order_probe.py evidence).
    poisoned = (
        "- **Tests:** Census-carrier tripwire (B2-215, 2026-09-26): the retired 1,341 headline "
        "rode 12 days stale with 31 files grown and no gate noticed. Live: 1,837 tests collected "
        "/ 301 files (2026-09-26 census, pytest --collect-only -q). Trust bytes, not reports."
    )
    parsed = parse_carrier(poisoned)
    assert parsed == {
        "date": date(2026, 9, 26), "collected": 1837, "files": 301, "line": poisoned,
    }


def test_prose_date_before_claim_cannot_poison_parse():
    # Same mechanism on the date branch: a stale prose date ahead of the claim
    # must not become the census date.
    poisoned = (
        "- **Tests:** Carrier note (retired 2026-09-14 headline, 31 files grown since). "
        "Live: 1,837 tests collected / 301 files (2026-09-26 census). Trust bytes, not reports."
    )
    parsed = parse_carrier(poisoned)
    assert parsed is not None
    assert parsed["date"] == date(2026, 9, 26)
    assert parsed["collected"] == 1837
    assert parsed["files"] == 301


def test_non_canonical_tests_line_is_none():
    # Fail-closed (B2-245): counts and a date without the census clause shape
    # no longer parse. The old first-match parser read this line as
    # files=31, date=2026-09-14, a silent wrong parse; None is exit 2 upstream.
    assert parse_carrier(
        "- **Tests:** 31 files grown since 2026-09-14, trust bytes.\n"
    ) is None


def test_line_extraction_stops_at_newline():
    text = LIVE_SHAPE + "\n- **Deliberate-ask:** 2026-09-01 should not leak.\n"
    parsed = parse_carrier(text)
    assert parsed["date"] == date(2026, 9, 26)


def test_blank_line_before_canonical_claim_still_parses():
    # D1 (arch-04, 2026-09-28; receipt watch/inbox/wave5_repair/patrol-fix.md):
    # the old CARRIER_LINE_RE "^\s*[-*]" matched newlines, so a blank line
    # before the bullet put match.start() on the blank line and the extracted
    # line was empty: exit 2 with the lying "need the claim shape" message.
    # Every frozen vector had the bullet as line 1 or after non-blank content,
    # exactly the B2-274 blind spot; the canonical claim must survive reflow.
    text = "\n\n" + LIVE_SHAPE
    parsed = parse_carrier(text)
    assert parsed == {
        "date": date(2026, 9, 26), "collected": 1837, "files": 301, "line": LIVE_SHAPE,
    }


def test_blank_line_before_malformed_claim_stays_none():
    # The fail-closed direction of the same layout: a preceding blank line must
    # not magically validate a malformed claim.
    assert parse_carrier("\n- **Tests:** the big suite, trust bytes.\n") is None


# --- patrol (pure verdict core) ----------------------------------------------

def test_boundary_age_at_bar_passes_with_growth():
    assert patrol(date(2026, 9, 19), date(2026, 9, 26), 5, None, None)["ok"] is True


def test_age_bar_plus_one_with_growth_is_stale_exit_1():
    verdict = patrol(date(2026, 9, 18), date(2026, 9, 26), 5, None, None)
    assert verdict["verdict"] == "STALE"
    assert verdict["exit"] == 1


def test_age_bar_plus_one_without_growth_is_ok():
    assert patrol(date(2026, 9, 18), date(2026, 9, 26), 0, 301, 301)["ok"] is True


def test_disk_shrink_below_claim_counts_as_growth():
    # B2-247: only shrink below the claim is a provable disk signal (files
    # deleted, or the claim invented). The old both-directions comparison sat
    # permanently true under the zero-collect instrument gap.
    assert patrol(date(2026, 9, 18), date(2026, 9, 26), 0, 264, 303)["verdict"] == "STALE"


def test_over_direction_is_instrument_lag_not_stale():
    # B2-247 falsifier frame: disk 305 vs carrier 303 with zero commits and a
    # stale date is the constant zero-collect instrument gap, named as
    # evidence, never a STALE verdict (the old code made any census >7d fire
    # on it forever).
    verdict = patrol(date(2026, 9, 18), date(2026, 9, 26), 0, 305, 303)
    assert verdict["ok"] is True
    assert "instrument lag" in verdict["reason"]
    assert "evidence only" in verdict["reason"]


def test_same_window_divergence_is_evidence_only():
    verdict = patrol(date(2026, 9, 25), date(2026, 9, 26), 0, 303, 301)
    assert verdict["ok"] is True
    assert "evidence only" in verdict["reason"]


def test_carrier_without_file_count_leans_on_commits_only():
    assert patrol(date(2026, 9, 18), date(2026, 9, 26), 0, 303, None)["ok"] is True


def test_future_census_is_unverifiable_exit_2():
    assert patrol(date(2026, 10, 1), date(2026, 9, 26), 0, None, None)["exit"] == 2


def test_census_dated_tomorrow_is_unverifiable_exit_2():
    # D2 (arch-04) removal pin: FUTURE_TOLERANCE_DAYS=1 pretended to tolerate a
    # census dated today+1, but patrol() has always exit-2d any negative age,
    # so the constant never changed an outcome. The boundary stays UNVERIFIABLE
    # after the removal.
    assert patrol(date.today() + timedelta(days=1), date.today(), 0, None, None)["exit"] == 2


def test_the_real_12_day_fossil_verdict():
    # 2026-09-14 carrier read at 2026-09-26 with 31 files grown: the disease.
    verdict = patrol(date(2026, 9, 14), date(2026, 9, 26), 31, 303, 264)
    assert verdict["verdict"] == "STALE"
    assert "31 test file(s)" in verdict["reason"]


# --- byte collectors ---------------------------------------------------------

def test_count_candidate_files_counts_pytest_named_only(tmp_path):
    tests = tmp_path / "tests"
    (tests / "pkg").mkdir(parents=True)
    (tests / "test_a.py").write_text("", encoding="utf-8")
    (tests / "pkg" / "test_b.py").write_text("", encoding="utf-8")
    (tests / "pkg" / "suite_test.py").write_text("", encoding="utf-8")
    (tests / "helper.py").write_text("", encoding="utf-8")
    (tests / "not_a_test.txt").write_text("", encoding="utf-8")
    assert count_candidate_files(tmp_path) == 3


def test_count_candidate_files_missing_dir_is_zero(tmp_path):
    assert count_candidate_files(tmp_path) == 0


def _git_init_and_commit(root: Path, message: str = "init") -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", message],
        cwd=root, check=True, capture_output=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )


def test_files_added_since_sees_post_census_commits(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_new.py").write_text("", encoding="utf-8")
    _git_init_and_commit(tmp_path)  # commit day = today, after 2026-09-01
    added = cdp.test_files_added_since(tmp_path, date(2026, 9, 1))
    assert len(added) == 1
    assert added[0].endswith("tests/test_new.py")


def test_files_added_since_excludes_census_day_and_non_tests(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_new.py").write_text("", encoding="utf-8")
    _git_init_and_commit(tmp_path)
    # Strictly-after rule: a commit on the census day itself is ambiguous
    # (the snapshot was taken some time during that day), so it never counts.
    assert cdp.test_files_added_since(tmp_path, date.today()) == []


def test_files_added_since_git_failure_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_DIR", str(tmp_path / "nowhere.git"))
    with pytest.raises(Exception):
        cdp.test_files_added_since(tmp_path, date(2026, 9, 1))


# --- CLI exit codes (real subprocess, synthetic estate) ----------------------

def _write_carrier(root: Path, text: str) -> None:
    (root / "AGENTS.md").write_text(text + "\n", encoding="utf-8")


def test_cli_self_test_passes():
    out = subprocess.run(
        [sys.executable, str(TOOL), "--self-test"], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CENSUS-PATROL SELF-TEST: PASS" in out.stdout


def test_cli_self_test_passes_from_foreign_cwd(tmp_path):
    # B2-248 split: --self-test delegates to tools/census_patrol_selftest.py;
    # the delegation must not depend on the caller's cwd (the tool is invoked
    # by absolute path, not only from the repo root pre-push uses).
    out = subprocess.run(
        [sys.executable, str(TOOL), "--self-test"], capture_output=True, text=True,
        timeout=120, cwd=tmp_path, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CENSUS-PATROL SELF-TEST: PASS" in out.stdout


def test_self_test_delegation_works_in_package_context():
    # B2-248 split: main() must resolve the sibling self-test module even when
    # this file was imported as tools.census_drift_patrol (script dir not on
    # sys.path), the exact context the in-process import cannot shortcut.
    assert cdp.main(["--self-test"]) == 0


def test_cli_fresh_synthetic_estate_exits_0(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_a.py").write_text("", encoding="utf-8")
    _write_carrier(
        tmp_path,
        f"- **Tests:** 42 tests collected / 1 files ({date.today().isoformat()} census, pytest). "
        f"Trust bytes, not reports.",
    )
    _git_init_and_commit(tmp_path)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "CENSUS-PATROL: ok" in out.stdout


def test_cli_stale_synthetic_estate_exits_1(tmp_path):
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_new.py").write_text("", encoding="utf-8")
    _write_carrier(
        tmp_path,
        "- **Tests:** 1,341 tests / 264 files (2026-09-01 census: 1305 passed / 34 failed / "
        "9 skipped, ~12 min). Trust bytes, not reports.",
    )
    _git_init_and_commit(tmp_path)  # lands today: growth after the 09-01 census
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 1, out.stdout + out.stderr
    assert "CENSUS-PATROL: STALE" in out.stdout
    assert "pytest --collect-only -q" in out.stdout  # the fix names the falsifier


def test_cli_missing_carrier_exits_2(tmp_path):
    (tmp_path / "tests").mkdir()
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 2
    assert "carrier missing" in out.stdout


def test_cli_unparsable_carrier_exits_2(tmp_path):
    (tmp_path / "tests").mkdir()
    _write_carrier(tmp_path, "# rules, no Tests bullet at all")
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 2
    assert "no parsable" in out.stdout


def test_cli_future_census_exits_2(tmp_path):
    (tmp_path / "tests").mkdir()
    _write_carrier(
        tmp_path,
        "- **Tests:** 10 tests / 1 files (2999-01-01 census). Trust bytes, not reports.",
    )
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 2
    assert "future" in out.stdout


def test_cli_census_dated_tomorrow_exits_2(tmp_path):
    # The D2 boundary through the real CLI: tomorrow is the only date the
    # removed FUTURE_TOLERANCE_DAYS pretended to allow; the tightened gate
    # (strictly > today) must keep it exit 2.
    (tmp_path / "tests").mkdir()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    _write_carrier(
        tmp_path,
        f"- **Tests:** 10 tests / 1 files ({tomorrow} census). Trust bytes, not reports.",
    )
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 2
    assert "future" in out.stdout


# --- B2-244 deep check: parse_collect_tail / collect_patrol (pure) -----------

def test_parse_collect_tail_reads_the_summary():
    out = (
        "tests/test_a.py::test_one\ntests/test_a.py::test_two\n"
        "2 tests collected in 0.01s\n"
    )
    assert cdp.parse_collect_tail(out) == 2


def test_parse_collect_tail_handles_singular_and_commas():
    assert cdp.parse_collect_tail("1 test collected in 0.01s") == 1
    assert cdp.parse_collect_tail("1,879 tests collected in 2.49s") == 1879


def test_parse_collect_tail_without_summary_is_none():
    assert cdp.parse_collect_tail("nothing collected here") is None


# --- B2-247 instrument gap: parse_collect_files (pure) ------------------------

def test_parse_collect_files_reads_the_item_bearing_set():
    out = (
        "tests/a.py::test_one\ntests/a.py::test_two\ntests/b.py::TestX::test_y\n"
        "2 tests collected in 0.01s\n"
    )
    assert cdp.parse_collect_files(out) == {"tests/a.py", "tests/b.py"}


def test_parse_collect_files_ignores_summary_and_prose():
    assert cdp.parse_collect_files("no node ids here\n1 test collected in 0.01s\n") == set()


def test_collect_patrol_tolerates_delta_below_bar():
    assert cdp.collect_patrol(1837, 1856)["ok"] is True


def test_collect_patrol_fires_at_the_bar_underclaim():
    # The B2-244 disease direction: reality grew past the frozen claim by
    # exactly the bar (20) and the verdict must be COLLECT-DRIFT exit 1.
    verdict = cdp.collect_patrol(1837, 1857)
    assert verdict["verdict"] == "COLLECT-DRIFT"
    assert verdict["exit"] == 1
    assert "pytest holds 1857" in verdict["reason"]


def test_collect_patrol_fires_on_overclaim_too():
    assert cdp.collect_patrol(1900, 1879)["verdict"] == "COLLECT-DRIFT"


def test_collect_patrol_missing_claim_is_exit_2():
    assert cdp.collect_patrol(None, 1879)["exit"] == 2


# --- B2-244 deep check: CLI against a real pytest collection ------------------

def _write_parametrize_estate(root: Path, cases: int) -> None:
    # Growth inside an EXISTING file, the exact class the file-growth signal
    # cannot see: one test file, no new files, N parametrized items.
    tests = root / "tests"
    tests.mkdir(exist_ok=True)
    (tests / "test_many.py").write_text(
        "import pytest\n\n\n"
        f"@pytest.mark.parametrize('i', range({cases}))\n"
        "def test_case(i):\n    assert i is not None\n",
        encoding="utf-8",
    )


def test_cli_collect_accurate_carrier_exits_0(tmp_path):
    _write_parametrize_estate(tmp_path, cases=22)
    _write_carrier(
        tmp_path,
        f"- **Tests:** 22 tests collected / 1 files ({date.today().isoformat()} census, "
        "`pytest --collect-only -q`). Trust bytes, not reports.",
    )
    # wave5 suite-burn (2026-09-29): the estate must be a real git estate - the
    # tool's own --root contract is "AGENTS.md, tests/ and .git", and run() calls
    # test_files_added_since (git log, exit 2 on failure, never a guess) BEFORE
    # the deep check. These CLI tests used to pass only when pytest's tmp root
    # happened to live inside a git repo (git found the repo's .git by parent
    # traversal); the mandated isolated out-of-repo basetemp exposed the hidden
    # dependency as "git log failed: fatal: not a git repository". Hermetic now.
    _git_init_and_commit(tmp_path)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path), "--collect"],
        capture_output=True, text=True, timeout=300, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "collect ok" in out.stdout
    assert "collect-only tail: 22 tests collected" in out.stdout


def test_cli_falsifier_green_gate_then_deep_check_fails(tmp_path):
    # The pre-registered B2-244 falsifier, byte-for-byte: the census is fresh
    # (today) and there are zero new files, so the default gate passes, yet
    # the carrier's collected claim is 20+ behind reality inside one file.
    # The deep check must fail it with exit 1.
    _write_parametrize_estate(tmp_path, cases=22)
    _write_carrier(
        tmp_path,
        f"- **Tests:** 2 tests collected / 1 files ({date.today().isoformat()} census, "
        "`pytest --collect-only -q`). Trust bytes, not reports.",
    )
    # hermetic git estate (see test_cli_collect_accurate_carrier_exits_0)
    _git_init_and_commit(tmp_path)
    base = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)],
        capture_output=True, text=True, timeout=300, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert base.returncode == 0, base.stdout + base.stderr
    assert "CENSUS-PATROL: ok" in base.stdout
    deep = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path), "--collect"],
        capture_output=True, text=True, timeout=300, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert deep.returncode == 1, deep.stdout + deep.stderr
    assert "COLLECT-DRIFT" in deep.stdout
    assert "pytest holds 22 vs carrier claim 2" in deep.stdout


def test_cli_collect_names_the_zero_collect_instrument_gap(tmp_path):
    # B2-247 falsifier pin: every --collect refresh must NAME the zero-collect
    # candidates, so the instrument gap can never move by an unnamed amount.
    # The synthetic estate mirrors the live disease: a standalone self-test
    # script named *_test.py (candidate by naming, zero items by content).
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_real.py").write_text("def test_a():\n    pass\n", encoding="utf-8")
    (tests / "script_self_test.py").write_text(
        'def main():\n    return 0\n\n\n'
        'if __name__ == "__main__":\n    raise SystemExit(main())\n',
        encoding="utf-8",
    )
    _write_carrier(
        tmp_path,
        f"- **Tests:** 1 tests collected / 1 files ({date.today().isoformat()} census, "
        "`pytest --collect-only -q`). Trust bytes, not reports.",
    )
    # hermetic git estate (see test_cli_collect_accurate_carrier_exits_0)
    _git_init_and_commit(tmp_path)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path), "--collect"],
        capture_output=True, text=True, timeout=300, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "instrument gap: 1 zero-collect candidate(s): tests/script_self_test.py" in out.stdout
    assert "files: collected 1 vs carrier claim 1" in out.stdout


def test_cli_collect_broken_collection_is_exit_2(tmp_path):
    # Fail-closed: a collection error means the byte truth is unavailable,
    # never a pass.
    tests = tmp_path / "tests"
    tests.mkdir()
    (tests / "test_broken.py").write_text("def broken(:\n", encoding="utf-8")
    _write_carrier(
        tmp_path,
        f"- **Tests:** 2 tests collected / 1 files ({date.today().isoformat()} census). "
        "Trust bytes, not reports.",
    )
    # hermetic git estate (see test_cli_collect_accurate_carrier_exits_0)
    _git_init_and_commit(tmp_path)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path), "--collect"],
        capture_output=True, text=True, timeout=300, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 2
    assert "cannot verify collect deep check" in out.stdout


def test_run_on_this_repo_currently_ok():
    # The live carrier is a fresh 2026-09-26 census: the patrol must pass on
    # the estate as landed. If this fails, the census went stale in reality.
    assert run(TOOL.parents[1]) == 0


# --- B2-338 hook pairing: the FIRST output line is the contract ---------------
# githooks/pre-push's census block captures the whole tool output (2>&1) and
# case-matches its START against the lowercase prefix "CENSUS-PATROL: ok"; the
# old head line printed the uppercase verdict OK there, so every fully green
# push took the WARN arm and trained operators to dismiss the channel.

HOOK_OK_PREFIX = "CENSUS-PATROL: ok"  # the hook's exact case-arm prefix bytes


def _green_estate(root: Path) -> None:
    tests = root / "tests"
    tests.mkdir()
    (tests / "test_a.py").write_text("", encoding="utf-8")
    _write_carrier(
        root,
        f"- **Tests:** 42 tests collected / 1 files ({date.today().isoformat()} census, "
        "pytest). Trust bytes, not reports.",
    )
    _git_init_and_commit(root)  # census day itself: strictly-after rule, no growth


def test_cli_green_output_starts_with_the_hook_ok_prefix(tmp_path):
    _green_estate(tmp_path)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path)], capture_output=True, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert out.stdout.startswith(HOOK_OK_PREFIX), repr(out.stdout.splitlines()[:1])


@pytest.mark.skipif(shutil.which("sh") is None, reason="sh not on PATH")
def test_hook_census_case_arm_replay_green_ok_arm_stale_warn_arm(tmp_path):
    # The brief's falsifier, byte-true in both directions: the ok-arm PATTERN is
    # read from the real githooks/pre-push bytes at test time and evaluated by
    # real sh against the tool's captured output (2>&1, exactly what the hook
    # does). The arm bodies are this test's echoes; the pattern is the hook's.
    hook_text = (TOOL.parents[1] / "githooks" / "pre-push").read_text(encoding="utf-8")
    match = re.search(r'\n\s*("(?:CENSUS-PATROL: ok)"\*)\) : ;;', hook_text)
    assert match, "census ok arm not found in githooks/pre-push bytes"
    pattern = match.group(1)

    green_root = tmp_path / "green"
    green_root.mkdir()
    _green_estate(green_root)
    green = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(green_root)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    stale_root = tmp_path / "stale"
    stale_root.mkdir()
    (stale_root / "tests").mkdir()
    (stale_root / "tests" / "test_new.py").write_text("", encoding="utf-8")
    _write_carrier(
        stale_root,
        "- **Tests:** 1,341 tests / 264 files (2026-09-01 census: 1305 passed / 34 failed / "
        "9 skipped, ~12 min). Trust bytes, not reports.",
    )
    _git_init_and_commit(stale_root)  # lands today: growth after the census
    stale = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(stale_root)],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert green.returncode == 0, green.stdout
    assert stale.returncode == 1, stale.stdout
    replay = 'case "$1" in ' + pattern + ') echo OK_ARM ;; *) echo WARN_ARM ;; esac'
    green_arm = subprocess.run(
        ["sh", "-c", replay, "sh", green.stdout], capture_output=True, text=True, timeout=60, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    stale_arm = subprocess.run(
        ["sh", "-c", replay, "sh", stale.stdout], capture_output=True, text=True, timeout=60, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0x08000000) if sys.platform == 'win32' else 0
    )
    assert green_arm.stdout.strip() == "OK_ARM", green_arm.stdout + green_arm.stderr
    assert stale_arm.stdout.strip() == "WARN_ARM", stale_arm.stdout + stale_arm.stderr
