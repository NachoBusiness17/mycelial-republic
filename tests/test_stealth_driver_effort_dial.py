"""Q-036: the stealth driver's per-lane reasoning-effort dial.

Proves: every lane from _work_lanes carries its policy effort (free=low,
judgment/scarce5=max, unknown tiers fail closed to low), and the direct-API
dispatch body carries the knob in the family's wire shape (OpenRouter
reasoning.effort object; nous top-level reasoning_effort, the z.ai 5.3
shape) while knob-less transports (llm7, hermes) carry the config value but
no wire knob.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SD_PATH = ROOT / "tools" / "stealth_driver.py"


def _load_mod():
    """Load tools/stealth_driver.py as a fresh module (tools/ not on sys.path)."""
    name = "stealth_driver"
    if name in sys.modules:
        del sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, SD_PATH)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_lane_effort_dial_policy_and_wire(monkeypatch):
    """Q-036: the dial is stamped on every lane and rides the dispatch body."""
    mod = _load_mod()
    monkeypatch.setattr(mod, "_sdd_key", lambda: "sk-test-sdd")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-test-or1")
    monkeypatch.setenv("OPENROUTER_API_KEY_2", "sk-test-or2")

    # 1. POLICY: _work_lanes stamps effort per tier on every lane.
    lanes = mod._work_lanes()
    assert lanes, "expected lanes with fake keys set"
    by_tier = {}
    for ln in lanes:
        assert ln["effort"] == mod.lane_effort(ln["tier"]), ln
        by_tier.setdefault(ln["tier"], []).append(ln)
    assert mod.lane_effort("free") == "low"
    assert mod.lane_effort("judgment") == "max"
    assert mod.lane_effort("scarce5") == "max"
    assert mod.lane_effort("mystery-tier") == "low"  # fail closed to cheap
    assert mod.lane_effort("") == "low"
    assert {"free", "judgment", "scarce5"} <= set(by_tier), sorted(by_tier)

    # 2. WIRE: OpenRouter free lane -> reasoning.effort object = low.
    or_free = next(l for l in by_tier["free"] if l["family"] == "openrouter")
    body = mod.work_payload(or_free, "ASK", 100)
    assert body["reasoning"] == {"effort": "low"}
    assert body["max_tokens"] == 100 and body["messages"][0]["content"] == "ASK"

    # 3. WIRE: OpenRouter judgment lane -> reasoning.effort object = max.
    or_judge = next(l for l in by_tier["judgment"] if l["family"] == "openrouter")
    assert mod.work_payload(or_judge, "ASK", 100)["reasoning"] == {"effort": "max"}

    # 4. WIRE: nous scarce5 lane -> top-level reasoning_effort = max
    #    (z.ai 5.3 shape; docs/ref/ZAI_API_EXPERT_REFERENCE.md 10.2).
    nous_lane = next(l for l in by_tier["scarce5"] if l["family"] == "nous")
    assert mod.work_payload(nous_lane, "ASK", 100)["reasoning_effort"] == "max"

    # 5. KNOB-LESS: llm7 (non-reasoning model) body carries no knob; hermes
    #    is a CLI transport and still carries the config-level effort.
    llm7 = next(l for l in by_tier["free"] if l["family"] == "llm7")
    body = mod.work_payload(llm7, "ASK", 100)
    assert "reasoning" not in body and "reasoning_effort" not in body
    assert llm7["effort"] == "low"
    hermes = next(l for l in by_tier["free"] if l["family"] == "hermes")
    assert hermes["effort"] == "low"
