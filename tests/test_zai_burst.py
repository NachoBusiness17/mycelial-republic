"""Coding-plan Max/Lite must fail fast on raw API and burst to DeepSeek."""
from __future__ import annotations

import urllib.request

from models.providers import burst_mill, chat_provider, should_burst


def test_max_handshake_is_miss():
    from harness.opencode_coder import is_handshake_noop

    assert is_handshake_noop("I understand. Ready to help with your Mag project. What would you like me to do?")
    assert not is_handshake_noop("Wrote mag/foo.py: def pick_free_glm(lane): return 'glm-4.7-flash'")


def test_should_burst_on_hang_and_1305():
    assert should_burst("The read operation timed out")
    assert should_burst('HTTP 429: {"error":{"code":"1305"}}')
    assert should_burst("opencode_only: coding-plan key refused")
    assert should_burst("concurrency timeout")
    assert not should_burst("missing API key")


def test_coding_plan_raw_api_refused_before_network(monkeypatch):
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("coding-plan must not hit /paas/v4")),
    )
    out = chat_provider("z_ai", "sys", "hi", tier="T2")
    assert out.get("ok") is False
    assert "opencode_only" in str(out.get("error"))
    assert out.get("burst_hint") == "deepseek"


def test_max_coding_plan_key_also_refused(monkeypatch):
    monkeypatch.setattr(
        urllib.request,
        "urlopen",
        lambda *a, **k: (_ for _ in ()).throw(AssertionError("z_ai4 must not hit network")),
    )
    out = chat_provider("z_ai4", "sys", "hi", tier="T2")
    assert out.get("ok") is False
    assert "opencode_only" in str(out.get("error"))


def test_pick_free_glm_drops_to_clerk_on_overload(monkeypatch):
    from mag import lane_cadence as lc

    monkeypatch.setattr(lc, "cooldown", lambda lane: 0)
    monkeypatch.setattr(
        lc,
        "_ledger_rows",
        lambda: [{"lane": "z_ai3", "ok": False, "error": "HTTP 429 1305 overloaded"}],
    )
    assert lc.pick_free_glm("z_ai3") == "glm-4.5-flash"


def test_pick_free_glm_rides_47_when_calm(monkeypatch):
    from mag import lane_cadence as lc

    monkeypatch.setattr(lc, "cooldown", lambda lane: 0)
    monkeypatch.setattr(lc, "_ledger_rows", lambda: [{"lane": "z_ai3", "ok": True, "error": ""}])
    assert lc.pick_free_glm("z_ai3") == "glm-4.7-flash"


def test_fuel_feed_includes_lite_cache_lane():
    # 2026-10-03 (operator order: the Lite lane was given to adam and pulled
    # from rotation): this test asserted the RELIT world (z_ai3 in FREE_LANES
    # + CACHE_LANES). It now pins the PULLED world instead - z_ai3 is out of
    # both tables via the B2-133 dormant gate and cache mining rides nothing
    # until an operator routing call names a replacement lane.
    # Receipt: watch/inbox/LITE_LANE_PULL_20261003.md
    from mag.fuel_feed import CACHE_LANES, FREE_LANES

    names = {ln[0] for ln in FREE_LANES}
    cache = {ln[0] for ln in CACHE_LANES}
    assert "z_ai3" not in names
    assert "z_ai3" not in cache
    assert cache == set()  # no replacement cache lane named yet
    assert "z_ai" not in cache  # coding-plan never in cache mill


def test_burst_mill_allow_peak_and_deepseek(monkeypatch):
    seen = {}

    def fake_chat(provider, system, user, **kw):
        seen.update({"provider": provider, **kw})
        return {"ok": True, "text": "burst ok", "provider": provider}

    import models.providers as p

    monkeypatch.setattr(p, "chat_provider", fake_chat)
    out = burst_mill("sys", "user", max_tokens=50, reason="timed out")
    assert out.get("ok") is True
    assert seen.get("provider") == "deepseek"
    assert seen.get("model") == "deepseek-v4-flash"
    assert seen.get("allow_peak") is True
    assert seen.get("timeout") == 45
    assert out.get("burst") is True
