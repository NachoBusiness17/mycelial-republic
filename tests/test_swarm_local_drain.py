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


def test_drain_pass_does_not_require_deepseek_for_local_work(monkeypatch):
    # A missing DeepSeek key must not block local/free rightsized work.
    monkeypatch.setattr(
        sld, "key_reconcile",
        lambda: {"ok": True, "resolved_provider_key": False, "note": "test"},
    )

    monkeypatch.setattr(
        "mag.swarm_worker.run_rightsized_once",
        lambda **kwargs: {"done": 0, "failed": 0, "skipped": 0},
    )
    r = sld.drain_pass(limit=1)
    assert r["ok"] is True
    assert r["done"] == 0


def test_run_cadence_daily_cap_guard():
    # the drain is bounded: it never exceeds the daily cap
    r = sld.run_cadence(per_beat=2, daily_cap=0, persist=False)
    assert r["ok"] is True
    assert r["skipped"] == "daily-cap"
    assert r["daily_cap"] == 0
