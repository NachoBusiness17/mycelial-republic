"""Ops-triage move 5 (morning-block 2026-10-07): the FIRED-BELOW-ARCHIVE gate
in tools/mickey17_v2_fold.py.

The defect species: --fired below the archive count folded
"missing (no file): <negative>" into the casualty header as a computed fact;
the one banked sighting rode out only as a seat's prose patch
(corpus/steal/MASTER_DOGFOOD_100M_20261006.md: "the minus sign is the file
surplus, not absence"). A negative count rendered as fact is a
fabrication-shaped hole, so the fold now exits 2 before any write. These
tests run main() in-process against a tmp lanes archive (monkeypatched
module globals), so the real estate archive is never read or written.
"""
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))
import mickey17_v2_fold as fold  # noqa: E402


def make_archive(tmp_path, n_files=2):
    lanes = tmp_path / "lanes"
    lanes.mkdir()
    for i in range(n_files):
        (lanes / f"lane-{i}.json").write_text(
            json.dumps({"ok": True, "rows": [
                {"lane": f"lane-{i}", "source": "s.md", "quote": "q",
                 "steal": "s", "estate_status": "executed", "leverage": "low"}]}),
            encoding="utf-8")
    return lanes


def run_fold(tmp_path, lanes_dir, fired):
    fold.LANES_DIR = lanes_dir
    fold.RUN_ROOT = tmp_path
    argv = ["mickey17_v2_fold.py"]
    if fired is not None:
        argv += ["--fired", str(fired)]
    monkey = pytest.MonkeyPatch()
    monkey.setattr(sys, "argv", argv)
    try:
        fold.main()
    finally:
        monkey.undo()


def test_fired_below_archive_exits_2_and_writes_nothing(tmp_path, capsys):
    lanes_dir = make_archive(tmp_path)
    out_file = tmp_path / fold.OUT_NAME
    # 1 < 2 files: the surplus species, and a directly negative --fired:
    # both must fail closed before the casualty header can render a
    # negative missing count as fact.
    for fired in (1, -5):
        out_file.unlink(missing_ok=True)
        with pytest.raises(SystemExit) as ei:
            run_fold(tmp_path, lanes_dir, fired)
        assert ei.value.code == 2, f"--fired {fired}: expected gate exit 2"
        out = capsys.readouterr().out
        assert "FIRED-BELOW-ARCHIVE GATE" in out
        assert "fabrication-shaped hole" in out
        assert not out_file.exists(), "the fold must not write past the gate"


def test_fired_at_or_above_archive_folds_with_nonnegative_missing(tmp_path, capsys):
    lanes_dir = make_archive(tmp_path)
    out_file = tmp_path / fold.OUT_NAME
    # Controls: fired == count and fired > count both keep folding, and the
    # missing render stays a nonnegative integer.
    for fired, missing in ((2, "0"), (3, "1")):
        out_file.unlink(missing_ok=True)
        run_fold(tmp_path, lanes_dir, fired)
        text = out_file.read_text(encoding="utf-8")
        assert f"missing (no file): {missing}" in text
        assert "- missing (no file): -" not in text
    # Default (no --fired): fired adopts the archive count, gate silent.
    out_file.unlink(missing_ok=True)
    run_fold(tmp_path, lanes_dir, None)
    assert "missing (no file): 0" in out_file.read_text(encoding="utf-8")
