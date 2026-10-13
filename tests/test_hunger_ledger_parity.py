"""Hunger-ledger cage/canonical drift pin (B2-401 lineage, B2-440, 2026-09-26).

mag/lane_runner.py cycle_economist runs watch/cage_bin/hunger_ledger.py first
and falls back to scripts/hunger_ledger.py on rc 2. The two copies DIFFER on
bytes (sha256 e0c0ce77... vs c4a00b72.../2cbae494... at triage time) and
nothing pinned which write behavior is canonical, so a cage copy that drifts
or disappears silently changes which ledger write path runs.

This pin runs BOTH copies end-to-end (real subprocess, real file writes) over
an identical fixture WATCH tree and requires byte-identical HUNGER_LEDGER.md
output, so mutating either copy's LEDGER write shape goes red here. It also
pins the lane_runner precedence order (cage first, scripts fallback) at the
source level.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAGE = ROOT / "watch" / "cage_bin" / "hunger_ledger.py"
CANON = ROOT / "scripts" / "hunger_ledger.py"
RUNNER = ROOT / "mag" / "lane_runner.py"
DAY = "20260926"

# HEADLESS law: explicit creationflags (ratchet tests/test_headless_law.py; bare-spawn-descent 2026-09-29)
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0

FIXTURE_FILES = {
    # dated card, dispositioned (marker band text)
    "INTAKE_B2_440_CARD_20260926.md": "route: shelf\n",
    # dated card, undispositioned
    "NOTE_20260926.md": "plain card text\n",
    # undated file (shelf only)
    "STANDING.md": "standing shelf file\n",
}


def _make_repo(tmp_path: Path, script: Path, home: str) -> Path:
    """Build a minimal repo tree so each copy's __file__-derived REPO resolves
    exactly as in the real tree: canonical at repo/scripts/ (REPO =
    parents[1]), cage copy at repo/watch/cage_bin/ (REPO = parents[2])."""
    repo = tmp_path / home
    (repo / "watch").mkdir(parents=True)
    rel = Path(script).parent.name
    dest = repo / "watch" / rel if rel == "cage_bin" else repo / rel
    dest.mkdir(parents=True)
    shutil.copy2(script, dest / Path(script).name)
    for name, text in FIXTURE_FILES.items():
        (repo / "watch" / name).write_text(text, encoding="utf-8")
    return repo


def _run_one(tmp_path: Path, script: Path, home: str) -> bytes:
    repo = _make_repo(tmp_path, script, home)
    rel = Path(script).parent.name
    script_dir = repo / "watch" / rel if rel == "cage_bin" else repo / rel
    script_copy = script_dir / Path(script).name
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run(
        [sys.executable, str(script_copy), "--date", DAY],
        capture_output=True, env=env, timeout=120, creationflags=HEADLESS,
    )
    assert r.returncode == 0, (script, r.stdout[-400:], r.stderr[-400:])
    ledger = repo / "watch" / "HUNGER_LEDGER.md"
    assert ledger.is_file(), f"no ledger written by {script}"
    return ledger.read_bytes().replace(b"\r\n", b"\n")


def test_cage_and_canonical_write_identical_ledger(tmp_path):
    """The drift pin: same fixture tree, byte-identical DATA ROWS.

    The two copies' HEADER intentionally differs (each names its own file as
    the generator; the cage copy self-identifies as "cage copy of
    scripts/hunger_ledger.py" — declared intentional here per the B2-440
    either/or). The per-day table rows are the LEDGER WRITE SHAPE the
    falsifier mutates; they must stay byte-identical."""
    out_canon = _run_one(tmp_path, CANON, "scripts_copy_repo")
    out_cage = _run_one(tmp_path, CAGE, "cage_copy_repo")
    rows_canon = [ln for ln in out_canon.splitlines() if ln.startswith(b"| ")]
    rows_cage = [ln for ln in out_cage.splitlines() if ln.startswith(b"| ")]
    assert rows_canon, "canonical copy wrote no table rows"
    assert rows_canon == rows_cage
    assert any(b"2026-09-26" in ln for ln in rows_canon)
    # both copies must count the fixture: 1 new dated card, 3 shelf files
    data_rows = [ln for ln in rows_canon if b"2026-09-26" in ln]
    assert data_rows and b"| 1 |" in data_rows[0]
    # the known intentional header divergence is real (guards against the
    # copies silently converging in a way that hides which writer ran)
    assert out_canon != out_cage


def test_cage_copy_disappearing_is_visible_in_runner_source():
    """The runner must reference the cage copy BEFORE the scripts fallback, so
    a cage copy that disappears changes behavior loudly (this source pin keeps
    the precedence order from drifting without a lane noticing)."""
    src = RUNNER.read_text(encoding="utf-8")
    i_cage = src.find("cage_bin/hunger_ledger")
    i_canon = src.find("scripts/hunger_ledger")
    assert i_cage != -1 and i_canon != -1, "runner no longer references both copies"
    assert i_cage < i_canon, "cage copy must run first, scripts fallback second"


def test_row_shape_mutation_goes_red(tmp_path, monkeypatch):
    """The B2-440 falsifier, executed: mutate the cage copy's LEDGER write
    shape on a sandboxed copy (extra space in the row separator) and the pin
    must go red. Proves the comparison bites, i.e. a real drift is named."""
    out_canon = _run_one(tmp_path, CANON, "scripts_repo_mut")
    # cage repo tree, but with the MUTATED script at repo/watch/cage_bin/
    repo = tmp_path / "cage_repo_mut"
    (repo / "watch" / "cage_bin").mkdir(parents=True)
    src = CAGE.read_text(encoding="utf-8")
    needle = 'f"| {date_iso} | {len(new)}'
    assert needle in src, "mutation needle not found in cage copy"
    monkeytarget = src.replace(needle, 'f"| {date_iso} |  {len(new)}', 1)
    (repo / "watch" / "cage_bin" / "hunger_ledger.py").write_text(
        monkeytarget, encoding="utf-8")
    for name, text in FIXTURE_FILES.items():
        (repo / "watch" / name).write_text(text, encoding="utf-8")
    r = subprocess.run(
        [sys.executable, str(repo / "watch" / "cage_bin" / "hunger_ledger.py"),
         "--date", DAY],
        capture_output=True, timeout=120, creationflags=HEADLESS,
    )
    assert r.returncode == 0, r.stderr[-300:]
    out_cage = (repo / "watch" / "HUNGER_LEDGER.md").read_bytes().replace(b"\r\n", b"\n")
    rows_canon = [ln for ln in out_canon.splitlines() if ln.startswith(b"| ")]
    rows_cage = [ln for ln in out_cage.splitlines() if ln.startswith(b"| ")]
    assert rows_canon != rows_cage, "row-shape mutation was NOT detected"
