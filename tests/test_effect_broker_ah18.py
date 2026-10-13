"""effect_broker model_call + lane_spawn de-stub — AH18 tests.

AUDIT (§3.5, watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md; receipt
watch/inbox/last_mile_20260930/AH18_BROKER_STUBS.md): the broker claimed
"every side effect routes through me" while model_call and lane_spawn were
stubs returning ok=True stub=True — a fake pass.  These tests pin the
real-but-narrow behavior:

    1. unauthorized  -> denied by the authority gate, delegate never called
    2. authorized    -> dispatched through the real delegate
                        (models.providers.chat_provider / mag.seat_dispatch.task)
                        and metered as a row on effects.jsonl
    3. budget exceeded (max_cost_usd) -> denied PRE-CALL, delegate never called

The delegates are monkeypatched so no live provider/subprocess is spent;
the broker code path under test is the real one.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _auth(effect: str, event_id: str) -> dict:
    """A clean authority record that passes the reference-monitor gate."""
    return {
        "status": "AUTHORIZED",
        "granted_capabilities": [effect],
        "event_id": event_id,
        "budget": {"max_calls": 5},
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ttl_seconds": 900,
    }


def _rows(eb, tmp_path):
    """Effect rows currently in the (redirected) effects.jsonl ledger."""
    log = tmp_path / eb.EFFECTS_LOG_NAME
    if not log.exists():
        return []
    return [json.loads(line) for line in
            log.read_text(encoding="utf-8").splitlines() if line.strip()]


# ── model_call ───────────────────────────────────────────────────────────────

def test_model_call_unauthorized_denied_delegate_never_called(monkeypatch, tmp_path):
    from mag import effect_broker as eb
    import models.providers as mp

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)

    def _must_not_run(*a, **kw):  # pragma: no cover - fail loud if called
        raise AssertionError("provider layer reached without authority")

    monkeypatch.setattr(mp, "chat_provider", _must_not_run)

    auth = _auth("fs_write", "ah18-unauth-model")  # wrong capability
    rec = eb.execute("model_call",
                     {"provider": "z_ai", "user": "hello"}, auth)

    # authority-gate failures leave result empty and carry the failure in
    # rec["error"] (the broker's established receipt grammar)
    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"].get("ok") is not True
    assert "authority check failed" in (rec.get("error") or "")
    assert _rows(eb, tmp_path) == [], "denied call must not meter a row"


def test_model_call_authorized_dispatched_and_logged(monkeypatch, tmp_path):
    from mag import effect_broker as eb
    import models.providers as mp

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    seen = {}

    def fake_chat_provider(provider_id, system, user, *, model=None,
                           max_tokens=0, tier="", session_id="",
                           timeout=None, allow_peak=False):
        seen.update(provider=provider_id, system=system, user=user,
                    model=model, max_tokens=max_tokens, tier=tier,
                    session_id=session_id)
        return {
            "ok": True, "text": "pong", "provider": provider_id,
            "model": model or "glm-4.7-flash",
            "usage": {"prompt_tokens": 10, "completion_tokens": 5},
            "budget_after": {"budget_ok": True},
        }

    monkeypatch.setattr(mp, "chat_provider", fake_chat_provider)

    auth = _auth("model_call", "ah18-auth-model")
    rec = eb.execute(
        "model_call",
        {"provider": "z_ai", "system": "be brief", "user": "say pong",
         "model": "glm-4.7-flash", "max_tokens": 512, "max_cost_usd": 1.0},
        auth)

    # the delegate really ran, with the broker's narrow defaults
    assert seen["provider"] == "z_ai"
    assert seen["user"] == "say pong"
    assert seen["tier"] == "T2"
    assert seen["session_id"].startswith("broker:ah18-auth-model")

    assert rec["status"] == "RECEIPT_COMMITTED"
    res = rec["result"]
    assert res["ok"] is True, rec.get("error")
    assert res["delegate"] == "models.providers.chat_provider"
    assert res["prompt_tokens"] == 10 and res["completion_tokens"] == 5
    expected_cost = round((10 + 5) / 1_000_000 * eb.USD_PER_MTOK, 8)
    assert res["cost_usd"] == expected_cost
    assert res["corr_id"] == "ah18-auth-model"

    # the meter row landed on effects.jsonl with model/tokens/cost/corr_id
    rows = _rows(eb, tmp_path)
    assert len(rows) == 1
    row = rows[0]
    assert row["effect"] == "model_call"
    assert row["corr_id"] == "ah18-auth-model"
    assert row["model"] == "glm-4.7-flash"
    assert row["prompt_tokens"] == 10 and row["completion_tokens"] == 5
    assert row["cost_usd"] == expected_cost

    ev = rec["postcondition_evidence"]
    assert ev["delegate"] == "models.providers.chat_provider"
    assert ev["total_tokens"] == 15
    assert ev["effect_row_logged"] is True


def test_model_call_budget_exceeded_denied_pre_call(monkeypatch, tmp_path):
    from mag import effect_broker as eb
    import models.providers as mp

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)

    def _must_not_run(*a, **kw):  # pragma: no cover - fail loud if called
        raise AssertionError("provider called past an exceeded max_cost_usd")

    monkeypatch.setattr(mp, "chat_provider", _must_not_run)

    auth = _auth("model_call", "ah18-budget-model")
    # worst-case estimate for max_tokens=2048 at USD_PER_MTOK is ~$0.03;
    # a $0.000001 cap must deny BEFORE the provider layer is touched.
    rec = eb.execute(
        "model_call",
        {"provider": "z_ai", "user": "hello", "max_tokens": 2048,
         "max_cost_usd": 0.000001},
        auth)

    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"].get("ok") is False
    err = rec.get("error") or ""
    assert "budget exceeded" in err
    assert "max_cost_usd" in err
    assert rec["result"]["estimated_cost_usd"] > 0.000001
    assert _rows(eb, tmp_path) == [], "denied call must not meter a row"


# ── lane_spawn ───────────────────────────────────────────────────────────────

def test_lane_spawn_unauthorized_denied_delegate_never_called(monkeypatch, tmp_path):
    from mag import effect_broker as eb
    import mag.seat_dispatch as sd

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)

    def _must_not_run(*a, **kw):  # pragma: no cover - fail loud if called
        raise AssertionError("seat_dispatch reached without authority")

    monkeypatch.setattr(sd, "task", _must_not_run)

    auth = _auth("tool_invoke", "ah18-unauth-lane")  # wrong capability
    rec = eb.execute("lane_spawn", {"task": "do work", "seat": "openclaw"}, auth)

    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"].get("ok") is not True
    assert "authority check failed" in (rec.get("error") or "")
    assert _rows(eb, tmp_path) == []


def test_lane_spawn_authorized_delegated_and_logged(monkeypatch, tmp_path):
    from mag import effect_broker as eb
    import mag.seat_dispatch as sd

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    seen = {}

    def fake_task(goal, *, seat="auto", tag="", model=""):
        seen.update(goal=goal, seat=seat, tag=tag, model=model)
        return {"ok": True, "task_id": "t-ah18-1", "seat": seat,
                "status": "done", "detail": "worked"}

    monkeypatch.setattr(sd, "task", fake_task)

    auth = _auth("lane_spawn", "ah18-auth-lane")
    rec = eb.execute("lane_spawn",
                     {"task": "gopher the inbox", "seat": "openclaw"}, auth)

    assert seen["goal"] == "gopher the inbox"
    assert seen["seat"] == "openclaw"
    assert seen["tag"].startswith("broker-ah18-auth-lane")

    assert rec["status"] == "RECEIPT_COMMITTED"
    res = rec["result"]
    assert res["ok"] is True, rec.get("error")
    assert res["delegate"] == "mag.seat_dispatch.task"
    assert res["task_id"] == "t-ah18-1"
    assert res["corr_id"] == "ah18-auth-lane"

    rows = _rows(eb, tmp_path)
    assert len(rows) == 1
    row = rows[0]
    assert row["effect"] == "lane_spawn"
    assert row["corr_id"] == "ah18-auth-lane"
    assert row["seat"] == "openclaw"
    assert row["task_id"] == "t-ah18-1"
    assert row["goal_head"] == "gopher the inbox"

    assert rec["postcondition_evidence"]["effect_row_logged"] is True


def test_lane_spawn_failed_dispatch_not_metered(monkeypatch, tmp_path):
    """A delegate failure is a FAILED receipt (full audit trail), never a
    metered effects row — the ledger meters dispatched work, not attempts."""
    from mag import effect_broker as eb
    import mag.seat_dispatch as sd

    monkeypatch.setattr(eb, "RECEIPTS_DIR", tmp_path)
    monkeypatch.setattr(sd, "task",
                        lambda goal, **kw: {"ok": False, "task_id": "t-x",
                                            "seat": "ghost", "status": "failed",
                                            "error": "unknown seat ghost"})

    auth = _auth("lane_spawn", "ah18-fail-lane")
    rec = eb.execute("lane_spawn", {"task": "x", "seat": "ghost"}, auth)

    assert rec["status"] == "RECEIPT_COMMITTED"
    assert rec["result"].get("ok") is False
    assert "unknown seat ghost" in (rec.get("error") or "")
    assert _rows(eb, tmp_path) == []
