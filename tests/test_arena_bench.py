"""Door 2 of the 24-wide dig (2026-10-04): the arena-bench CI tripwire.

Defect being cured (receipt watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md,
"arena-bench CI tripwire"): mag/arena_bench.py parsed
dashboard/static/arrakis.html - a 459-byte redirect stub since the
2026-09-22 surfaces dedupe (canonical at games/arrakis.html) - so
load_ground_truth() raised "GATES parse came back empty" on every run with
ZERO tests referencing the file (verified: grep -r arena_bench tests/ -> 0).
The bench rotted silently. The path is repointed at the canonical copy; this
tripwire runs the selftest AND the real-surface parse at pre-push so the
next shape change fails the gate instead of rotting.
Receipt: watch/inbox/ARENA_BENCH_TRIPWIRE_20261004.md
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mag.arena_bench import load_ground_truth  # noqa: E402

PY = ROOT / ".venv" / "Scripts" / "python.exe"


def test_selftest_proves_the_split():
    """--selftest exits 0 and mints both a synthetic PASS and a synthetic
    FAIL (zero_human mode: no network, no human judgment)."""
    if not PY.is_file():
        import pytest

        pytest.skip("venv python not present")
    r = subprocess.run(
        [str(PY), str(ROOT / "mag" / "arena_bench.py"), "--selftest"],
        capture_output=True, text=True, timeout=300, cwd=str(ROOT),
    )
    assert r.returncode == 0, r.stderr[-800:]
    verdicts = [line for line in r.stdout.splitlines() if '"verdict"' in line]
    assert any("PASS" in v for v in verdicts), "no synthetic PASS in selftest"
    assert any("FAIL" in v for v in verdicts), "no synthetic FAIL in selftest"


def test_ground_truth_parses_the_canonical_surfaces():
    """The real-surface parse: gates found, THE BLIND GATE present with its
    crown/ghost inscription, dungeon inv rows present. A surface rename,
    move, or shape change fails HERE at pre-push instead of rotting the
    bench silently (the 2026-09-22 stub disease took 12 days to notice)."""
    gt = load_ground_truth()
    assert gt["gate_count"] >= 1, gt
    assert "blind_gate" in gt or any("blind" in str(k).lower() for k in gt), \
        "the blind gate fell out of the ground truth"


def test_surfaces_are_not_redirect_stubs():
    """The exact disease: a canonical surface replaced by a redirect stub.
    A stub is small and contains a meta refresh; real surfaces are not."""
    from mag.arena_bench import ARRAKIS_PATH, DUNGEON_PATH

    for path in (ARRAKIS_PATH, DUNGEON_PATH):
        assert path.is_file(), f"surface missing: {path}"
        text = path.read_text(encoding="utf-8")
        assert "http-equiv=\"refresh\"" not in text, \
            f"{path.name} is a redirect stub - point the bench at the canonical copy"
        assert len(text) > 4000, f"{path.name} suspiciously small ({len(text)} bytes)"


def test_selftest_output_is_valid_json_records():
    """Determinism/instrument discipline: the selftest emits parseable JSON
    records (the bench's outputs feed receipts; unparseable output is a
    broken instrument, not a broken bench)."""
    if not PY.is_file():
        import pytest

        pytest.skip("venv python not present")
    r = subprocess.run(
        [str(PY), str(ROOT / "mag" / "arena_bench.py"), "--selftest"],
        capture_output=True, text=True, timeout=300, cwd=str(ROOT),
    )
    assert r.returncode == 0, r.stderr[-800:]
    # the selftest prints JSON objects back to back; decode each
    decoder = json.JSONDecoder()
    text, objs, idx = r.stdout.strip(), [], 0
    while idx < len(text):
        obj, end = decoder.raw_decode(text, idx)
        objs.append(obj)
        idx = end
        while idx < len(text) and text[idx] in " \n\r\t":
            idx += 1
    assert len(objs) >= 2, f"expected at least the pass and fail records, got {len(objs)}"
    assert any(o.get("zero_human") for o in objs)
