"""B2-318 (2026-09-26): the ack_reaper battery now executes under pytest.

tests/selftests/ack_reaper_selftest.py (moved out of the pytest candidate namespace by B2-389) matched the *_test.py collection pattern but defined
no test_* functions, so its 21 hand-run checks contributed zero pytest items
and a scripts/ack_reaper.py regression failed nothing in CI. These thin
wrappers run the single shared battery (collect_checks()) once per module and
surface every check as its own pytest item. The script stays hand-runnable:
python tests/selftests/ack_reaper_selftest.py (moved out of the pytest candidate namespace by B2-389)
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

_HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "ack_reaper_battery", _HERE / "selftests/ack_reaper_selftest.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)


@pytest.fixture(scope="module")
def battery() -> list[tuple[str, bool, str]]:
    checks = _mod.collect_checks()
    assert len(checks) == 21, f"battery shape drifted: {len(checks)} checks"
    return checks


def test_battery_has_unique_names(battery):
    names = [n for n, _, _ in battery]
    assert len(names) == len(set(names))


@pytest.mark.parametrize("idx", range(21))
def test_ack_reaper_check(battery, idx):
    name, ok, detail = battery[idx]
    assert ok, f"{name}: {detail}"
