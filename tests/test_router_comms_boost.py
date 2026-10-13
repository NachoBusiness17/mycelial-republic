"""Q-009 (2026-09-28): comms_trail consumption wired into routing.

The wire: mag.router._comms_lane_boost promotes provider lanes whose seat family has a
PROVEN comms-consumption record (mycelium consumption edges reduced by
mag.comms_trail.consumption_signal) within each route() branch's allowed lanes, never
ahead of the free local lane (ollama). Route()-level tests inject signals and patch the
provider registry, so no live graph or API state is needed for the hermetic cases; one
test feeds the REAL consumption_signal() output through the boost as a shape check.
"""
from __future__ import annotations


CC = {  # mirrors mag.comms_trail.consumption_signal() shape (live 2026-09-28)
    "total_consumption_edges": 13,
    "seats": {
        "grok_free": {"count": 5, "weight": 49.43},
        "cheap_swarm": {"count": 6, "weight": 57.91},
        "weak_seat": {"count": 2, "weight": 0.1},  # under the 0.5 proven floor
        "zero_seat": {"count": 0, "weight": 9.0},  # zero count
    },
    "proven_seats": ["cheap_swarm", "grok_free"],
}


# --- unit: seat -> lane mapping ---

def test_proven_lanes_respect_count_and_weight_floor():
    from mag.router import _proven_comms_lanes

    lanes = _proven_comms_lanes(CC)
    assert lanes == ["ollama", "xai"]  # sorted; weak_seat + zero_seat filtered
    assert lanes == sorted(lanes)


def test_proven_lanes_fallback_and_garbage_inputs():
    from mag.router import _proven_comms_lanes

    assert _proven_comms_lanes({"proven_seats": ["grok_free"]}) == ["xai"]
    assert _proven_comms_lanes(None) == []
    assert _proven_comms_lanes("nope") == []
    assert _proven_comms_lanes({"seats": {"bad": "not-a-dict"}}) == []


def test_specific_provider_token_beats_generic_token():
    # regression: "deepseek_swarm" must map to deepseek, not the generic swarm->ollama
    from mag.router import _proven_comms_lanes

    cc = {"seats": {"deepseek_swarm": {"count": 3, "weight": 4.0}}}
    assert _proven_comms_lanes(cc) == ["deepseek"]


# --- unit: the boost itself ---

def test_boost_promotes_within_tail_and_keeps_ollama_head():
    from mag.router import _comms_lane_boost

    base = ["ollama", "deepseek", "xai", "groq", "openrouter"]
    boosted, moved = _comms_lane_boost(base, CC)
    assert boosted == ["ollama", "xai", "deepseek", "groq", "openrouter"]
    assert moved == ["xai"]
    assert base == ["ollama", "deepseek", "xai", "groq", "openrouter"]  # no mutation


def test_boost_without_ollama_moves_proven_lane_to_front():
    from mag.router import _comms_lane_boost

    base = ["deepseek", "deepseek_overmind", "anthropic", "xai", "vast"]
    boosted, moved = _comms_lane_boost(base, CC)
    assert boosted == ["xai", "deepseek", "deepseek_overmind", "anthropic", "vast"]
    assert moved == ["xai"]


def test_boost_identity_when_no_proven_lane_in_list():
    from mag.router import _comms_lane_boost

    base = ["deepseek", "deepseek_overmind", "anthropic", "vast"]
    boosted, moved = _comms_lane_boost(base, CC)  # xai/ollama absent from the list
    assert boosted == base
    assert moved == []


def test_boost_identity_when_order_would_not_change():
    from mag.router import _comms_lane_boost

    base = ["ollama", "xai", "deepseek"]
    boosted, moved = _comms_lane_boost(base, CC)
    assert boosted == base
    assert moved == []


# --- e2e: route() branches consume the wire ---

_CONV_GOAL = "tell me about the meaning of attention in society today my friend"
_HEAVY_GOAL = "implement multi-file orchestrator heal loop with tests"


def _patch_providers(monkeypatch, providers, budget, routing):
    cfg = {
        "providers": providers,
        "defaults": {"never_remote_tiers": ["T0", "T1"]},
        "routing": routing,
    }
    monkeypatch.setattr("models.providers.load_providers", lambda: cfg)
    monkeypatch.setattr("models.providers.list_provider_ids", lambda: list(providers.keys()))
    monkeypatch.setattr("models.providers.get_provider", lambda pid: dict(providers.get(pid) or {}))
    monkeypatch.setattr(
        "models.quota.provider_budget",
        lambda pid: budget.get(pid) or {"configured": False, "budget_ok": False},
    )
    monkeypatch.setenv("MAG_DISABLE_REMOTE_PROVIDER_LOCK", "1")


def test_route_default_branch_boosts_proven_lane(monkeypatch):
    from mag.router import route

    # default branch is reached via force_seat=remote (depth seats are local/deepseek/grok_tui)
    _patch_providers(
        monkeypatch,
        {
            "ollama": {"default_model": "g2b", "tier_max": "T2", "free_local": True},
            "openrouter": {"default_model": "or", "tier_max": "T2"},
            "xai": {"default_model": "gk", "tier_max": "T2"},
        },
        {
            "openrouter": {"configured": True, "budget_ok": True},
            "xai": {"configured": True, "budget_ok": True},
        },
        {"default": ["ollama", "openrouter", "xai"]},
    )
    r = route(_CONV_GOAL, force_seat="remote", signals={"comms_consumption": CC})
    assert r["depth"] == "conversation"
    assert "comms_lane_boost=xai" in r["why"]
    assert r["provider"] == "xai"


def test_route_default_branch_control_keeps_base_order(monkeypatch):
    from mag.router import route

    _patch_providers(
        monkeypatch,
        {
            "ollama": {"default_model": "g2b", "tier_max": "T2", "free_local": True},
            "openrouter": {"default_model": "or", "tier_max": "T2"},
            "xai": {"default_model": "gk", "tier_max": "T2"},
        },
        {
            "openrouter": {"configured": True, "budget_ok": True},
            "xai": {"configured": True, "budget_ok": True},
        },
        {"default": ["ollama", "openrouter", "xai"]},
    )
    r = route(_CONV_GOAL, force_seat="remote",
              signals={"comms_consumption": {"seats": {}, "proven_seats": []}})
    assert r["provider"] == "openrouter"
    assert not any(w.startswith("comms_lane_boost") for w in r["why"])


def test_route_heavy_branch_boosts_deepseek_proven_seat(monkeypatch):
    from mag.router import route

    pro = {
        "vast": {"default_model": "v", "tier_max": "T2"},
        "deepseek": {"default_model": "ds", "tier_max": "T2"},
        "deepseek_overmind": {"default_model": "dso", "tier_max": "T2"},
        "anthropic": {"default_model": "an", "tier_max": "T2"},
    }
    _patch_providers(monkeypatch, pro, {p: {"configured": True, "budget_ok": True} for p in pro}, {})
    sig = {"comms_consumption": {"seats": {"deepseek_swarm": {"count": 3, "weight": 4.0}},
                                 "proven_seats": ["deepseek_swarm"]}}
    r = route(_HEAVY_GOAL, signals=sig)
    assert r["depth"] == "heavy_code"
    assert "comms_lane_boost=deepseek" in r["why"]
    assert r["provider"] == "deepseek"


def test_route_heavy_branch_control_keeps_vast_first(monkeypatch):
    from mag.router import route

    pro = {
        "vast": {"default_model": "v", "tier_max": "T2"},
        "deepseek": {"default_model": "ds", "tier_max": "T2"},
    }
    _patch_providers(monkeypatch, pro, {p: {"configured": True, "budget_ok": True} for p in pro}, {})
    r = route(_HEAVY_GOAL, signals={"comms_consumption": {"seats": {}, "proven_seats": []}})
    assert r["provider"] == "vast"
    assert not any(w.startswith("comms_lane_boost") for w in r["why"])


def test_route_local_branch_never_moves_ollama_but_boosts_tail(monkeypatch):
    from mag.router import route

    pro = {
        "ollama": {"default_model": "g2b", "tier_max": "T2", "free_local": True},
        "deepseek": {"default_model": "ds", "tier_max": "T2"},
        "groq": {"default_model": "gq", "tier_max": "T2"},
    }
    _patch_providers(monkeypatch, pro, {p: {"configured": True, "budget_ok": True} for p in pro}, {})
    sig = {
        "cheap_tier_confidence": "high",
        "comms_consumption": {"seats": {"groq_seat": {"count": 2, "weight": 3.0}},
                              "proven_seats": ["groq_seat"]},
    }
    r = route("doctor health status", signals=sig)
    assert r["depth"] == "scut"
    assert r["seat"] == "local"
    assert r["provider"] == "ollama"  # cost-doctrine guard: ollama stays first
    assert "comms_lane_boost=groq" in r["why"]


# --- integration: the REAL signal feeds the wire ---

def test_real_consumption_signal_feeds_boost():
    from mag.comms_trail import consumption_signal
    from mag.router import _comms_lane_boost

    cs = consumption_signal()
    assert cs.get("ok") is True
    assert cs.get("schema") == "comms_consumption.v1"
    base = ["ollama", "deepseek", "xai"]
    boosted, moved = _comms_lane_boost(base, cs)
    assert boosted[0] == "ollama"  # guard holds on live graph data
    assert set(moved) <= {"xai", "groq", "openrouter", "deepseek"}


def test_gather_signals_still_carries_comms_consumption():
    from mag.router import gather_signals

    sig = gather_signals()
    cc = sig.get("comms_consumption") or {}
    assert "total_consumption_edges" in cc
    assert "proven_seats" in cc
    assert "cheap_tier_confidence" in sig
