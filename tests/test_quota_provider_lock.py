"""Regression tests for remote provider lock defaults in pick_provider."""
from __future__ import annotations


def _patch_provider_catalog(monkeypatch):
    cfg = {
        "providers": {
            "openrouter": {"default_model": "or-model"},
            "deepseek": {"default_model": "ds-model"},
            "deepseek_overmind": {"default_model": "dso-model"},
            "anthropic": {"default_model": "an-model"},
        },
        "defaults": {"never_remote_tiers": ["T0", "T1"]},
        "routing": {},
    }
    monkeypatch.setattr("models.providers.load_providers", lambda: cfg)
    monkeypatch.setattr("models.providers.list_provider_ids", lambda: list(cfg["providers"].keys()))
    monkeypatch.setattr("models.providers.get_provider", lambda pid: dict(cfg["providers"].get(pid) or {}))


def test_pick_provider_lock_defaults_to_deepseek(monkeypatch):
    from models.quota import pick_provider

    _patch_provider_catalog(monkeypatch)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.setattr(
        "models.quota.provider_budget",
        lambda pid: {"provider": pid, "configured": True, "budget_ok": True},
    )

    out = pick_provider(job="default", tier="T2", prefer=["openrouter", "anthropic"])
    assert out["ok"] is True
    assert out["provider"] == "deepseek"


def test_pick_provider_lock_can_be_disabled(monkeypatch):
    from models.quota import pick_provider

    _patch_provider_catalog(monkeypatch)
    monkeypatch.setenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", "1")
    monkeypatch.setattr(
        "models.quota.provider_budget",
        lambda pid: {"provider": pid, "configured": True, "budget_ok": True},
    )

    out = pick_provider(job="default", tier="T2", prefer=["openrouter", "anthropic"])
    assert out["ok"] is True
    assert out["provider"] == "openrouter"


def test_pick_provider_lock_falls_back_to_overmind(monkeypatch):
    from models.quota import pick_provider

    _patch_provider_catalog(monkeypatch)
    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)

    def fake_budget(pid: str):
        if pid == "deepseek":
            return {"provider": pid, "configured": False, "budget_ok": True}
        return {"provider": pid, "configured": True, "budget_ok": True}

    monkeypatch.setattr("models.quota.provider_budget", fake_budget)

    out = pick_provider(job="default", tier="T2", prefer=["anthropic"])
    assert out["ok"] is True
    assert out["provider"] == "deepseek_overmind"


def test_pick_provider_lock_ignored_for_private_tiers(monkeypatch):
    from models.quota import pick_provider

    _patch_provider_catalog(monkeypatch)
    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.setattr(
        "models.quota.provider_budget",
        lambda pid: {"provider": pid, "configured": True, "budget_ok": True},
    )

    out = pick_provider(job="default", tier="T0", prefer=["openrouter", "anthropic"])
    assert out["ok"] is False
    assert any(c.get("skip") == "tier_block" for c in out.get("candidates") or [])


def test_pick_provider_lock_does_not_override_explicit_local_prefer(monkeypatch):
    from models.quota import pick_provider

    _patch_provider_catalog(monkeypatch)
    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)

    def fake_budget(pid: str):
        if pid == "ollama":
            return {"provider": pid, "configured": True, "budget_ok": True}
        return {"provider": pid, "configured": True, "budget_ok": True}

    monkeypatch.setattr("models.quota.provider_budget", fake_budget)
    monkeypatch.setattr(
        "models.providers.get_provider",
        lambda pid: {"default_model": f"{pid}-model", "free_local": pid == "ollama"},
    )

    out = pick_provider(job="default", tier="T2", prefer=["ollama", "openrouter", "anthropic"])
    assert out["ok"] is True
    assert out["provider"] == "ollama"


def test_remote_provider_policy_defaults(monkeypatch):
    from models.quota import remote_provider_policy

    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)
    pol = remote_provider_policy()
    assert pol["schema"] == "remote_provider_policy.v1"
    assert pol["enabled"] is True
    assert pol["lock_provider"] == "deepseek"


def test_remote_provider_policy_disabled(monkeypatch):
    from models.quota import remote_provider_policy

    monkeypatch.setenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", "true")
    pol = remote_provider_policy()
    assert pol["enabled"] is False
    assert pol["lock_provider"] is None
