"""Tests for tools/prepush_golden_vector.py (a11-commits row 3 instrument).

Contract under test: the FULL CAMPAIGN golden vector (11 byte tokens the
a11-commits lane byte-verified at a7d7d313d) must hold on the live
tools/dungeon.py, a known-bad fixture (any one token removed) must trip the
core naming exactly that law, and the CLI must exit 0 clean / 1 damaged /
2 cannot-verify.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import tools.prepush_golden_vector as ggv

REPO = Path(__file__).resolve().parents[1]
TOOL = REPO / "tools" / "prepush_golden_vector.py"
LIVE_DUNGEON = REPO / "tools" / "dungeon.py"
PY = sys.executable


def _live_text() -> str:
    return LIVE_DUNGEON.read_text(encoding="utf-8", errors="replace")


def test_vector_tokens_all_present_in_live_dungeon():
    """Known-answer: the real dungeon.py holds every token (banked live:
    GOLDEN-VECTOR: ok - 11/11)."""
    assert ggv.check_text(_live_text()) == []


def test_each_token_removal_trips_core():
    """Known-bad fixture per token: strip one token, the core names exactly
    that law and stays silent on the other ten."""
    text = _live_text()
    for name, needle in ggv.GOLDEN_VECTOR:
        damaged = text.replace(needle, "")
        assert needle not in damaged
        missing = ggv.check_text(damaged)
        assert name in missing, f"stripping {needle!r} did not trip {name!r}"
        assert len(missing) == 1, f"stripping {needle!r} tripped {missing}"


def test_cli_clean_copy_exits_zero(tmp_path):
    target = tmp_path / "dungeon.py"
    target.write_text(_live_text(), encoding="utf-8")
    r = subprocess.run([PY, str(TOOL), "--file", str(target)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, r.stdout + r.stderr
    assert r.stdout.startswith("GOLDEN-VECTOR: ok")


def test_cli_tampered_copy_exits_one(tmp_path):
    """Known-bad fixture at the CLI: the win-gate token moved from DC 15 to a
    fake DC, which removes the pinned token and must WARN exit 1."""
    target = tmp_path / "dungeon.py"
    damaged = _live_text().replace("[AUDIT root] successes at DC 15",
                                   "[AUDIT root] successes at DC 9")
    assert damaged != _live_text()
    target.write_text(damaged, encoding="utf-8")
    r = subprocess.run([PY, str(TOOL), "--file", str(target)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 1, r.stdout + r.stderr
    assert r.stdout.startswith("GOLDEN-VECTOR: MISS")
    assert "root-anchor win gate" in r.stdout
    assert "git show a7d7d313d:tools/dungeon.py" in r.stdout


def test_cli_missing_target_exits_two(tmp_path):
    r = subprocess.run([PY, str(TOOL), "--file", str(tmp_path / "nope.py")],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode == 2
    assert "cannot verify" in r.stdout


def test_vector_tokens_are_unique():
    """Every token must be distinct so the per-token trip matrix stays
    one-law-per-token (a duplicate token would trip two names at once)."""
    needles = [needle for _, needle in ggv.GOLDEN_VECTOR]
    assert len(needles) == len(set(needles)) == 11
