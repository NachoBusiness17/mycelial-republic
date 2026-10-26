"""B2-204 pins: pick_provider must never return a dormant provider.

Falsifier shape from the brief: pick_provider('default') would return a
dormant provider the moment someone re-adds it to a routing list. These
fixtures use the five lanes dormant on 2026-09-26 (cerebras, nvidia, gemini,
mistral, saelis per the B2-61/B2-36 purge receipts quoted in
configs/providers.yaml) with keys AND budget green, i.e. exactly the
configuration the old loop handed back as ok.
"""
from __future__ import annotations

DORMANT_FIVE = ["cerebras", "nvidia", "gemini", "mistral", "saelis"]


def _patch_catalog(monkeypatch):
    cfg = {
        "providers": {
            "ollama": {"default_model": "qwen2.5-coder:7b", "free_local": True},
            "openrouter": {"default_model": "or-model"},
            **{pid: {"default_model": pid + "-model", "dormant": True}
               for pid in DORMANT_FIVE},
        },
        "defaults": {"never_remote_tiers": ["T0", "T1"]},
        "routing": {"default": DORMANT_FIVE + ["openrouter"]},
    }
    monkeypatch.setattr("models.providers.load_providers", lambda: cfg)
    monkeypatch.setattr("models.providers.list_provider_ids",
                        lambda: list(cfg["providers"].keys()))
    monkeypatch.setattr("models.providers.get_provider",
                        lambda pid: dict(cfg["providers"].get(pid) or {}))


def _green_budget(monkeypatch):
    monkeypatch.setattr(
        "models.quota.provider_budget",
        lambda pid: {"provider": pid, "configured": True, "budget_ok": True},
    )


def test_routing_list_readd_of_dormant_five_never_wins(monkeypatch):
    from models.quota import pick_provider

    _patch_catalog(monkeypatch)
    _green_budget(monkeypatch)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)

    out = pick_provider(job="default", tier="T2")
    # the routing list leads with all five dormant lanes, every one has a key
    # and budget: the old loop returned cerebras here (falsifier fired)
    assert out["ok"] is True
    assert out["provider"] == "openrouter"
    skips = {c.get("provider"): c.get("skip") for c in out["candidates"]}
    for pid in DORMANT_FIVE:
        assert skips.get(pid) == "dormant", pid


def test_dormant_only_list_refuses_instead_of_returning_a_dead_lane(monkeypatch):
    from models.quota import pick_provider

    _patch_catalog(monkeypatch)
    _green_budget(monkeypatch)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)

    out = pick_provider(job="default", tier="T2",
                        prefer=["saelis", "nvidia"])
    assert out["ok"] is False
    assert [c.get("skip") for c in out["candidates"]] == ["dormant", "dormant"]


def test_dormant_flag_absent_still_pickable(monkeypatch):
    from models.quota import pick_provider

    _patch_catalog(monkeypatch)
    _green_budget(monkeypatch)
    monkeypatch.delenv("MAG_REMOTE_PROVIDER_LOCK", raising=False)
    monkeypatch.delenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", raising=False)

    out = pick_provider(job="default", tier="T2", prefer=["openrouter"])
    assert out["ok"] is True
    assert out["provider"] == "openrouter"
