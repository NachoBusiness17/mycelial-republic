"""B2-318 (2026-09-26): the lesson_gate battery now executes under pytest.

tests/selftests/lesson_gate_selftest.py (moved out of the pytest candidate namespace by B2-389) matched the *_test.py collection pattern but ran its
22 checks only under a hand-run main(), so pytest collected zero items and a
scripts/lesson_gate.py regression failed nothing in CI. These thin wrappers
run the single shared battery (collect_checks()) once per module and surface
every check as its own pytest item. The script stays hand-runnable:
python tests/selftests/lesson_gate_selftest.py (moved out of the pytest candidate namespace by B2-389)
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "lesson_gate_battery", _HERE / "selftests/lesson_gate_selftest.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


@pytest.fixture(scope="module")
def battery() -> list[tuple[str, bool, str]]:
    checks = _mod.collect_checks()
    assert len(checks) == 22, f"battery shape drifted: {len(checks)} checks"
    return checks


def test_battery_has_unique_names(battery):
    names = [n for n, _, _ in battery]
    assert len(names) == len(set(names))


@pytest.mark.parametrize("idx", range(22))
def test_lesson_gate_check(battery, idx):
    name, ok, detail = battery[idx]
    assert ok, f"{name}: {detail}"
