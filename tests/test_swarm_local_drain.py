"""tests for swarm_local_drain — the ROOT-CAUSE fix: a LOCAL drainer for the swarm queue (the k8s
CronJob drainer never runs on Windows). Deterministic coordinator + bounded swarm work.

RIB (frozen spec):
  key_reconcile() -> reconcile the key env: provider reads DEEPSEEK_SWARM_API_KEY, local .env sets
      DEEPSEEK_API_KEY; alias the present key into the provider env (in-process). Never logs the
      value. Honest resolved_provider_key flag.
  drain_pass(limit) -> run the EXISTING swarm_worker.run_once() LOCALLY (bounded) with the key
      reconciled. If no key resolves, honest ok:False (does NOT silently queue-fail).
  run_cadence(per_beat, daily_cap) -> bounded + daily-capped self-healing drain beat; skips when the
      daily cap is hit.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import swarm_local_drain as sld  # noqa: E402


def test_status_contract_and_fixes():
    st = sld.status()
    assert st["ok"] is True
    assert st["schema"] == "swarm_local_drain.v1"
    # it names the two things it fixes
    assert "dead k8s CronJob drain" in st["fixes"]
    assert "key env mismatch" in st["fixes"]
    assert "swarm_worker" in st["reuses"]


def test_key_reconcile_never_logs_value():
    kr = sld.key_reconcile()
    assert kr["ok"] is True
    assert kr["resolved_provider_key"] in (True, False)
    # the key VALUE must never appear in the output (name only)
    import json
    blob = json.dumps(kr).lower()
    for secret_marker in ("sk-", "deepseek_swarm_api_key=sk"):
        assert secret_marker not in blob


def test_drain_pass_honest_when_no_key():
    # force no resolved key -> honest ok:False (never silently queue-fail)
    import os
    saved_provider = os.environ.get(sld.PROVIDER_KEY_ENV)
    saved_local = os.environ.get(sld.LOCAL_KEY_ENV)
    try:
        os.environ.pop(sld.PROVIDER_KEY_ENV, None)
        os.environ.pop(sld.LOCAL_KEY_ENV, None)
        r = sld.drain_pass(limit=1)
        assert r["ok"] is False
        assert "no deepseek key resolves" in r["error"]
    finally:
        if saved_provider is not None:
            os.environ[sld.PROVIDER_KEY_ENV] = saved_provider
        if saved_local is not None:
            os.environ[sld.LOCAL_KEY_ENV] = saved_local


def test_run_cadence_daily_cap_guard():
    # the drain is bounded: it never exceeds the daily cap
    r = sld.run_cadence(per_beat=2, daily_cap=0, persist=False)
    assert r["ok"] is True
    assert r["skipped"] == "daily-cap"
    assert r["daily_cap"] == 0
