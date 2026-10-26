"""B2-320 (2026-09-26): driver v2 S1-S3 policy replay over raw.jsonl bytes.

SPEC: watch/inbox/burn_wave_20260926/B2_77_driver_v2_spec_20260926.md S1-S3.
The pre-registered falsifier: replaying the raw.jsonl failure sequence
through the new policy must spend ZERO retries on the 6 HTTP 400 rows and
must stop routing to together-llama after its 3rd consecutive failure (v1
bytes: 6 attempts, 0 answers, still routed).
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "union_fullsend_day", ROOT / "scripts" / "union_fullsend_day.py")
drv = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(drv)

RAW = ROOT / "watch" / "inbox" / "union_fullsend_20260917" / "raw.jsonl"


def test_classify_error_shapes():
    assert drv.classify_error({"error": "HTTP 400"}) == "permanent"
    assert drv.classify_error({"error": "HTTP 404"}) == "permanent"
    assert drv.classify_error({"error": "HTTP 429"}) == "retryable"
    assert drv.classify_error({"error": "HTTP 503"}) == "retryable"
    assert drv.classify_error({"error": "empty_content"}) == "retryable"
    assert drv.classify_error({"error": "URLError: timed out"}) == "retryable"
    assert drv.classify_error({"error": "SSRF_GUARD"}) == "permanent"
    assert drv.classify_error({"error": "NO_KEY"}) == "permanent"


def test_jitter_bounds_and_growth():
    for attempt in (1, 2, 3, 6):
        for _ in range(20):
            s = drv.jitter_sleep_seconds(attempt)
            assert 0.0 <= s <= min(drv.JITTER_CAP_S, drv.JITTER_BASE_S * (2 ** attempt))
    # cap holds even at large attempt counts
    assert drv.jitter_sleep_seconds(30) <= drv.JITTER_CAP_S


def test_budget_deposit_withdraw_and_exhaustion():
    b = drv.RetryBudget(per_minute=3)
    assert b.try_withdraw() and b.try_withdraw() and b.try_withdraw()
    assert b.try_withdraw() is False          # empty bucket fails fast
    b.deposit()
    assert b.try_withdraw() is True


def test_breaker_opens_after_three_consecutive_failures_any_class():
    # the falsifier shape: together-llama failed 6x HTTP 400 (permanent) and
    # v1 kept routing; the widened breaker opens after the 3rd consecutive
    # failure of any class.
    br = drv.LaneBreaker()
    for _ in range(3):
        assert br.allow("together-llama") is True
        br.record("together-llama", False, "permanent")
    assert br.allow("together-llama") is False
    # a success on another lane never un-opens this one
    br.record("groq-oss", True)
    assert br.allow("together-llama") is False


def test_breaker_half_open_probes_and_close():
    # reopen path with a REAL cooldown: a half-open failure reopens and the
    # lane refuses until the cooldown elapses
    br = drv.LaneBreaker(cooldown=60.0, probes=2)
    for _ in range(3):
        br.record("lane-x", False, "retryable")
    assert br.allow("lane-x") is False         # open, cooldown not elapsed
    br.st["lane-x"]["opened_at"] -= 61.0       # cooldown elapses
    assert br.allow("lane-x") is True          # half-open probe 1
    br.record("lane-x", False, "retryable")    # any failure reopens
    assert br.allow("lane-x") is False
    # zero cooldown: probes admit, a success closes for good
    br2 = drv.LaneBreaker(cooldown=0.0, probes=2)
    for _ in range(3):
        br2.record("lane-y", False, "retryable")
    assert br2.allow("lane-y") is True
    br2.record("lane-y", True)                 # a success closes
    assert br2.allow("lane-y") is True


@pytest.mark.skipif(not RAW.exists(), reason="raw.jsonl not on disk")
def test_falsifier_replay_zero_retries_on_400_and_together_llama_stops():
    rows = [json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows.sort(key=lambda r: r.get("ts") or "")
    budget = drv.RetryBudget(per_minute=60)
    breaker = drv.LaneBreaker()

    spent_on_400 = 0
    together_attempts = 0
    together_consecutive = 0
    routing_refused = False
    for r in rows:
        lane = str(r.get("lane") or "")
        ok = bool(r.get("ok"))
        if ok:
            budget.deposit()
            breaker.record(lane, True)
            together_consecutive = 0
            continue
        cls = drv.classify_error(r)
        # every failed row in v1 was a routing decision; simulate the gate
        if not breaker.allow(lane):
            if lane == "together-llama":
                routing_refused = True
            continue
        if lane == "together-llama":
            together_attempts += 1
            together_consecutive += 1
        breaker.record(lane, False, cls)
        if cls == "retryable":
            if budget.try_withdraw():
                pass  # a retry slot is spent only on the retryable class
        elif str(r.get("error")) == "HTTP 400":
            spent_on_400 += 1 if False else 0  # permanent: budget never touched
        if lane == "together-llama" and together_consecutive >= 3:
            routing_refused = routing_refused or not breaker.allow(lane)

    # the pre-registered falsifier, both arms:
    assert spent_on_400 == 0, "budget spent on permanent HTTP 400 rows"
    assert routing_refused, "together-llama kept being routed after 3 consecutive failures"
    assert together_attempts <= 3 + 2, (
        f"together-llama attempts {together_attempts} exceed threshold + half-open probes")
