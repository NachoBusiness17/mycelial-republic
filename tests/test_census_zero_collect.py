"""Zero-collect detector tests (Mickey17 W2, 2026-09-29; receipt
watch/inbox/W2_ZERO_COLLECT_20260929.md).

The wave ledger return 7 disease: a tests/*.py file that collects zero items
hides inside the aggregate denominators, because "N tests collected / M files"
never says WHICH files carry the items; tests/test_selffeed_integration.py (a
__main__ script wearing test_*.py naming) rode every census as a counted file
while contributing nothing, and the B2-247 instrument-gap line could only NAME
that class, never fail on it. W2 gives the --collect deep check teeth:
zero_collect_patrol (pure core) plus the run() wiring fail exit 1 with verdict
ZERO-COLLECT naming each offender, with ZERO_COLLECT_TOLERANT in the tool as
the only escape hatch for legitimately-empty fixtures (each entry owes a
receipt; seeded empty because the one real offender IS the disease, not a
fixture).

Bands mirror tests/test_census_drift_patrol.py house style: the pure verdict
core over a real tmp tree, the CLI exit codes through a subprocess against a
hermetic git estate, and the tolerant list end to end (module global read at
call time inside run(), so monkeypatching the tool's list is enough).
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date
from pathlib import Path

import tools.census_drift_patrol as cdp

# Module import, not from-imports (house rule from the sibling test file):
# a from-import of a test_-prefixed helper would drop it into this module's
# namespace for pytest to mis-collect. Call everything as cdp.<name>.
TOOL = Path(__file__).resolve().parents[1] / "tools" / "census_drift_patrol.py"

# HEADLESS law (ratchet tests/test_headless_law.py; bare-spawn-descent
# 2026-09-29): every subprocess spawn carries explicit creationflags.
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def _populate(root: Path, empty: bool, script_shaped: bool = False) -> None:
    """A tmp estate: one real test file, plus (optionally) one zero-collect
    file that is either truly empty or script-shaped (a main() with no test
    functions, the exact tests/test_selffeed_integration.py disease shape)."""
    tests = root / "tests"
    tests.mkdir(parents=True, exist_ok=True)
    (tests / "test_real.py").write_text("def test_a():\n    pass\n", encoding="utf-8")
    if empty:
        if script_shaped:
            (tests / "test_script.py").write_text(
                'def main():\n    return 0\n\n\n'
                'if __name__ == "__main__":\n    raise SystemExit(main())\n',
                encoding="utf-8",
            )
        else:
            (tests / "test_empty.py").write_text("", encoding="utf-8")


def _write_carrier(root: Path, items: int, files: int) -> None:
    (root / "AGENTS.md").write_text(
        f"- **Tests:** {items} tests collected / {files} files "
        f"({date.today().isoformat()} census, `pytest --collect-only -q`). "
        "Trust bytes, not reports.\n",
        encoding="utf-8",
    )


def _git_init_and_commit(root: Path, message: str = "init") -> None:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True, capture_output=True, creationflags=HEADLESS)
    subprocess.run(["git", "add", "-A"], cwd=root, check=True, capture_output=True, creationflags=HEADLESS)
    subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@example.com", "commit", "-q", "-m", message],
        cwd=root, check=True, capture_output=True, creationflags=HEADLESS,
    )


def _disk_rel(root: Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in cdp.candidate_files(root)}


# --- pure verdict core --------------------------------------------------------


def test_empty_test_file_is_named_by_the_detector(tmp_path):
    _populate(tmp_path, empty=True)
    disk = _disk_rel(tmp_path)
    verdict = cdp.zero_collect_patrol(disk, {"tests/test_real.py"})
    assert verdict["ok"] is False
    assert verdict["verdict"] == "ZERO-COLLECT"
    assert verdict["exit"] == 1
    assert verdict["files"] == ["tests/test_empty.py"]
    assert "tests/test_empty.py" in verdict["reason"]


def test_script_shaped_disease_file_is_named_too(tmp_path):
    # The real finding's shape (receipt W2_ZERO_COLLECT_20260929.md): content,
    # imports, a main(), zero test functions. Candidate by naming, zero items.
    _populate(tmp_path, empty=True, script_shaped=True)
    verdict = cdp.zero_collect_patrol(_disk_rel(tmp_path), {"tests/test_real.py"})
    assert verdict["ok"] is False
    assert verdict["files"] == ["tests/test_script.py"]


def test_all_populated_tree_passes(tmp_path):
    _populate(tmp_path, empty=False)
    verdict = cdp.zero_collect_patrol(_disk_rel(tmp_path), {"tests/test_real.py"})
    assert verdict["ok"] is True
    assert verdict["exit"] == 0
    assert "every disk candidate collects items" in verdict["reason"]


def test_tolerant_list_exempts_a_legitimately_empty_fixture(tmp_path):
    _populate(tmp_path, empty=True)
    verdict = cdp.zero_collect_patrol(
        _disk_rel(tmp_path), {"tests/test_real.py"}, {"tests/test_empty.py"}
    )
    assert verdict["ok"] is True
    assert "1 tolerated empty: tests/test_empty.py" in verdict["reason"]


def test_module_tolerant_list_is_seeded_empty():
    # Pin the seed decision (W2 receipt): the tolerant list ships EMPTY; the
    # only real zero-collect file found is the disease itself, so joining this
    # list requires a receipt, and this assert flips the day someone seeds it.
    assert cdp.ZERO_COLLECT_TOLERANT == frozenset()


# --- CLI band (real subprocess, hermetic git estate) --------------------------


def test_cli_collect_fails_exit_1_naming_the_empty_test_file(tmp_path):
    # The W2 teeth: an accurate carrier (items claim matches reality) still
    # fails when a disk candidate collects zero items; the old B2-247 behavior
    # (name it, stay exit 0) is superseded for the non-tolerated remainder.
    _populate(tmp_path, empty=True)
    _write_carrier(tmp_path, items=1, files=2)
    _git_init_and_commit(tmp_path)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path), "--collect"],
        capture_output=True, text=True, timeout=300, creationflags=HEADLESS,
    )
    assert out.returncode == 1, out.stdout + out.stderr
    assert "ZERO-COLLECT" in out.stdout
    assert "tests/test_empty.py" in out.stdout
    # The B2-247 evidence line survives (every candidate still named every run).
    assert "instrument gap: 1 zero-collect candidate(s): tests/test_empty.py" in out.stdout


def test_cli_collect_all_populated_estate_exits_0(tmp_path):
    _populate(tmp_path, empty=False)
    _write_carrier(tmp_path, items=1, files=1)
    _git_init_and_commit(tmp_path)
    out = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(tmp_path), "--collect"],
        capture_output=True, text=True, timeout=300, creationflags=HEADLESS,
    )
    assert out.returncode == 0, out.stdout + out.stderr
    assert "collect ok" in out.stdout
    assert "instrument gap: none" in out.stdout


def test_tolerant_list_works_end_to_end_through_run(tmp_path, monkeypatch, capsys):
    # run() reads the module global at call time (not a def-time default), so
    # flipping the tool's tolerant list is enough to exempt the fixture while
    # the deep check still runs the real pytest collection.
    _populate(tmp_path, empty=True)
    _write_carrier(tmp_path, items=1, files=2)
    _git_init_and_commit(tmp_path)
    monkeypatch.setattr(cdp, "ZERO_COLLECT_TOLERANT", frozenset({"tests/test_empty.py"}))
    exit_code = cdp.run(tmp_path, collect=True)
    captured = capsys.readouterr().out
    assert exit_code == 0, captured
    assert "collect ok" in captured
    assert "instrument gap: 1 zero-collect candidate(s): tests/test_empty.py" in captured
