"""R4b heartbeat-scaled staleness bar (2026-10-06, ouroboros R4 fold S9).

The flat 7d bar PASSED a 1.7d-stale state/CURRENT.md while HEAD was hours old
(the estate's biggest night); the bar now scales with the repo heartbeat:
min(STALE_DAYS, max(STALE_FLOOR_DAYS, head_age * STALE_SCALE)). These pins run
against the pure function, no git calls, no repo-state dependence.
"""
from __future__ import annotations

from tools.freshness_check import (
    HEARTBEAT_DAYS,
    STALE_DAYS,
    STALE_FLOOR_DAYS,
    STALE_SCALE,
    effective_stale_days,
)


def test_fast_heartbeat_tightens_to_the_floor():
    # Hours-old heartbeat (2026-10-06's live case): the bar is the 1.0d floor,
    # so a 1.7d-stale doc now exceeds it instead of hiding under a flat week.
    assert effective_stale_days(0.1) == STALE_FLOOR_DAYS == 1.0


def test_bar_scales_with_head_age():
    assert effective_stale_days(0.5) == 2.0
    assert effective_stale_days(1.0) == 4.0


def test_bar_never_exceeds_the_one_decay_constant():
    assert effective_stale_days(5.0) == STALE_DAYS
    assert effective_stale_days(100.0) == STALE_DAYS


def test_unknown_heartbeat_falls_back_to_the_constant():
    assert effective_stale_days(None) == float(STALE_DAYS)


def test_constants_keep_their_contract():
    assert HEARTBEAT_DAYS == 2
    assert STALE_SCALE == 4.0
    assert STALE_FLOOR_DAYS == 1.0
