"""Unified router — one classifier, honest failures."""
from __future__ import annotations

import pytest


def test_route_scut_local():
    from mag.router import route

    r = route("doctor health status")
    assert r["depth"] == "scut"
    assert r["seat"] == "local"
    assert r["provider"] == "ollama"
    assert r["executable"] is True
    assert r["ok"] is True


def test_route_simple_typo_local():
    from mag.router import route

    r = route("fix typo in README one file")
    assert r["depth"] == "simple_code"
    assert r["seat"] == "local"
    assert r["executable"] is True


def test_route_overview_grok_pack_only():
    from mag.router import route

    r = route("big picture interlink map of the ecosystem")
    assert r["depth"] == "overview"
    assert r["seat"] == "grok_tui"
    assert r["launch"] is False
    assert r["executable"] is False
    assert r["provider"] is None
    assert r["ok"] is True


def test_route_overview_never_ollama():
    from mag.router import route

    r = route("Give me a big picture interlink map of the ecosystem")
    assert r["provider"] != "ollama"
    assert r["seat"] == "grok_tui"


def test_route_heavy_without_keys_fails_loud(monkeypatch):
    from mag.router import route

    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    monkeypatch.delenv("DEEPSEEK_OVERMIND_API_KEY", raising=False)
    r = route("implement multi-file orchestrator heal loop with tests")
    assert r["depth"] == "heavy_code"
    if not r.get("executable"):
        assert r["ok"] is False
        assert r["error"] == "no_execution_provider"


def test_route_cursor_marker():
    from mag.router import route

    r = route("via cursor implement seat identity in mag/seats.py")
    assert r["seat"] == "cursor"
    assert r["executable"] is False
    assert r["mode"] == "defer_cursor"


def test_classifiers_agree():
    from mag.coordination import classify_depth
    from mag.dispatch import _classify_job
    from mag.router import route

    goals = [
        "doctor health status",
        "fix typo in README",
        "implement multi-file refactor",
        "big picture ecosystem map",
        "via cursor wire dashboard",
    ]
    for g in goals:
        rt = route(g)
        cd = classify_depth(g)
        assert rt["depth"] == cd["depth"], f"depth mismatch for {g!r}"


def test_activity_dedupes_stale_running(tmp_path, monkeypatch):
    import mag.coordination as c

    act = tmp_path / "state" / "shared_activity.jsonl"
    act.parent.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(c, "ACTIVITY_PATH", act)
    aid = "act-test-1"
    c.log_activity(seat="local", depth="scut", goal="task", status="running", activity_id=aid)
    c.log_activity(seat="local", depth="scut", goal="task", status="done", activity_id=aid)
    rows = c.read_activity(limit=10)
    assert len(rows) == 1
    assert rows[0]["status"] == "done"
    summary = c.activity_summary(limit=10)
    assert summary["running_n"] == 0


def test_rest_route_smoke():
    from dashboard.rest import h_route

    code, body = h_route({}, {"goal": "doctor health", "launch": False})
    assert code == 200
    assert body.get("ok") is True
    assert body.get("schema") == "mag_intent.v1"
    assert (body.get("decision") or {}).get("route")


def test_rest_route_heavy_prefers_deepseek_lock(monkeypatch):
    from dashboard.rest import h_route

    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)

    cfg = {
        "providers": {
            "deepseek": {"default_model": "ds-model", "tier_max": "T2"},
            "deepseek_overmind": {"default_model": "dso-model", "tier_max": "T2"},
            "anthropic": {"default_model": "an-model", "tier_max": "T2"},
        },
        "defaults": {"never_remote_tiers": ["T0", "T1"]},
        "routing": {},
    }
    monkeypatch.setattr("models.providers.load_providers", lambda: cfg)
    monkeypatch.setattr("models.providers.list_provider_ids", lambda: list(cfg["providers"].keys()))
    monkeypatch.setattr("models.providers.get_provider", lambda pid: dict(cfg["providers"].get(pid) or {}))
    monkeypatch.setattr(
        "models.quota.provider_budget",
        lambda pid: {"provider": pid, "configured": True, "budget_ok": True},
    )

    code, body = h_route({}, {"goal": "implement multi-file router cleanup with tests", "launch": False})
    assert code == 200
    route = ((body.get("decision") or {}).get("route") or {})
    assert route.get("provider") == "deepseek"


def test_router_status_exposes_provider_policy(monkeypatch):
    from dashboard.rest import h_router_status

    monkeypatch.setenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", "1")
    code, body = h_router_status({}, None)
    assert code == 200
    assert body.get("schema") == "mag_router_status.v1"
    pol = body.get("provider_policy") or {}
    assert pol.get("schema") == "remote_provider_policy.v1"
    assert pol.get("enabled") is False
