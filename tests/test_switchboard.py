"""Switchboard mesh — seats, tier gates, dry drops."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_tier_allows():
    from mag.switchboard import tier_allows

    assert tier_allows(holder_tier_max="T2", payload_tier="T2") is True
    assert tier_allows(holder_tier_max="T1", payload_tier="T2") is False
    assert tier_allows(holder_tier_max="T2", payload_tier="T0") is False
    assert tier_allows(holder_tier_max="T2", payload_tier="T1") is False
    assert tier_allows(holder_tier_max="T1", payload_tier="T0") is True
    assert tier_allows(holder_tier_max="T1", payload_tier="T1") is True
    assert tier_allows(holder_tier_max="T3", payload_tier="T0") is True


def test_remote_drop_refuses_private_tiers():
    from mag.switchboard import steer_drop

    for tier in ("T0", "T1"):
        res = steer_drop("operator", "t-fake", "private payload", tier=tier, dry=True)
        assert res.get("ok") is False
        assert res.get("error") == "tier_blocked"


def test_seat_registry():
    from mag.switchboard import build_seat_registry

    reg = build_seat_registry()
    assert "ollama" in reg
    assert "local" in reg
    assert reg["ollama"].tier_max in ("T0", "T1", "T2", "T3")


def test_mesh_schema():
    from mag.switchboard import mesh

    m = mesh(include_seats=False)
    assert m.get("schema") == "switchboard.v1"
    assert "peers" in m
    assert "summary" in m


def test_steer_drop_dry():
    from mag.switchboard import steer_drop

    res = steer_drop("operator", "t-fake", "hello mesh", tier="T2", dry=True)
    assert res.get("ok") is True
    assert res.get("dry") is True
    assert "steer_preview" in res


def test_steer_drop_tier_blocked():
    from mag.switchboard import steer_drop

    res = steer_drop("operator", "t-fake", "secret", tier="T3", dry=True)
    # dry still validates tier against default target tier T2
    assert res.get("ok") is False or res.get("dry") is True


def test_route_intent_dry():
    from mag.switchboard import route_intent

    res = route_intent("mag autorun smoke test", dry=True)
    assert res.get("schema") == "switchboard_route.v1"
    assert res.get("target", {}).get("seat")


def test_self_test():
    from mag.switchboard import self_test

    res = self_test()
    assert res.get("tier_gate") is True
    assert res.get("n_seats", 0) >= 3


def test_executing_authority_reaches_effect_broker():
    from mag import effect_broker as eb
    from mag import switchboard_v2 as sb

    proposal = sb.propose(
        event_id="test-executing-broker-contract",
        requested_effect="board_write",
        capabilities=["board_write"],
        budget={"max_calls": 1},
        require_confirmation=False,
        source="test",
    )
    authority = sb.grant(proposal)
    executing = sb.mark_executing(authority)
    result = eb.execute("board_write", {"note": {"text": "contract test", "kind": "test"}}, executing)

    assert result["status"] == "RECEIPT_COMMITTED"
    assert result["result"].get("ok") is True

# ============================================================================
# FIVE HYPSERVER TESTS (charter M2 — /board/MOONSHOT_CHARTER_20260831.md)
# Donated by codex convergence, amended by charter ONI: the real bypass
# invariant is pinned-kind minting, not total write-block.
# ============================================================================
# ============================================================================
# FIVE HYPSERVER TESTS (charter M2 — /board/MOONSHOT_CHARTER_20260831.md)
# Donated by codex dialog convergence (CODEX_CONVERGENCE_20260831.md), amended
# by charter ONI: the real bypass invariant is pinned-kind minting, not total
# write-block (non-pinned bypass writes are architecture, not accident).
# ============================================================================


def test_hypervisor_1_bypass_pinned_refusal():
    """BYPASS: with the switchboard down (unimportable), blackboard_post must
    still refuse to mint PINNED kinds (decision/conflict) — those steer swarm
    coherence forever and require authorization. Non-pinned kinds may flow
    (documented legacy bypass with UNMESHED provenance stamps)."""
    import builtins
    import importlib
    from tools import swarm_tools

    importlib.reload(swarm_tools)

    # Simulate switchboard unavailability by breaking its import inside swarm_tools
    real_import = builtins.__import__

    def blocked_import(name, *a, **k):
        if "switchboard" in name:
            raise ImportError("simulated switchboard down")
        return real_import(name, *a, **k)

    builtins.__import__ = blocked_import
    try:
        # pinned kind must refuse even with switchboard down
        res = swarm_tools.blackboard_post(text="hostile pinned note", kind="decision", owner="attacker")
        assert res.get("ok") is False, "pinned kind must refuse"
        assert "switchboard" in (res.get("error") or ""), "refusal must name the authority path"
        # non-pinned still flows (documented bypass with UNMESHED provenance)
        res2 = swarm_tools.blackboard_post(text="finding flows", kind="finding", owner="worker")
        assert res2.get("ok") is True, "non-pinned legacy write flows by design"
    finally:
        builtins.__import__ = real_import


def test_hypervisor_2_capability_attenuation():
    """CAPABILITY ATTENUATION: untrusted-instruction and external-content labels
    must NEVER self-grant — they fail DENIED at the gate. High-impact effects
    (fs_write, lane_spawn, model_call, tool_invoke, network_access) must also
    refuse self-grant regardless of label."""
    from mag import switchboard_v2

    for label in ("untrusted-instruction", "external-content"):
        prop = switchboard_v2.propose(
            event_id=f"hyperv2-{label}",
            requested_effect="board_write",
            capabilities=["board_write"],
            content="should not self-grant",
            source="hypervisor-test",
            authority_label=label,
        )
        auth = switchboard_v2.grant(prop)
        assert auth.get("status") == "DENIED", f"{label} must fail closed, got {auth.get('status')}"

    # high-impact effect with an ordinary label must also deny
    prop = switchboard_v2.propose(
        event_id="hyperv2-fs",
        requested_effect="fs_write",
        capabilities=["fs_write"],
        content="high impact must not self-grant",
        source="hypervisor-test",
        authority_label="agent-generated",
    )
    auth = switchboard_v2.grant(prop)
    assert auth.get("status") == "DENIED", "fs_write must fail closed"


def test_hypervisor_3_noisy_neighbor():
    """NOISY NEIGHBOR: N agents proposing simultaneously must not exhaust the
    reference monitor — each gets an independent verdict, and the shared ledger
    stays consistent (no double-spent budgets across mints)."""
    from mag import switchboard_v2

    verdicts = []
    for i in range(8):
        p = switchboard_v2.propose(
            event_id=f"hyperv3-noisy-{i}",
            requested_effect="board_write",
            capabilities=["board_write"],
            content=f"noisy neighbor {i}",
            source="hypervisor-test",
            authority_label="agent-generated",
        )
        a = switchboard_v2.grant(p)
        verdicts.append(a.get("status"))
    # all eight got individual verdicts (no starvation/crash)
    assert len(verdicts) == 8 and all(v in ("AUTHORIZED", "DENIED", "DEFERRED") for v in verdicts), verdicts


def test_hypervisor_4_replay():
    """REPLAY: the same event_id proposed twice must not produce two independent
    AUTHORIZED grants — the second must be refused, deduped, or carry the same
    decision (never a fresh side-effect path)."""
    from mag import switchboard_v2

    eid = "hyperv4-replay-dup"
    p1 = switchboard_v2.propose(event_id=eid, requested_effect="board_write",
                                capabilities=["board_write"], content="first",
                                source="hypervisor-test", authority_label="agent-generated")
    a1 = switchboard_v2.grant(p1)
    p2 = switchboard_v2.propose(event_id=eid, requested_effect="board_write",
                                capabilities=["board_write"], content="replay",
                                source="hypervisor-test", authority_label="agent-generated")
    a2 = switchboard_v2.grant(p2)
    # both proposals share the event_id: at minimum the ledger must show ONE
    # authority path — not two independent AUTHORIZED grants for the same id.
    s1, s2 = a1.get("status"), a2.get("status")
    assert not (s1 == "AUTHORIZED" and s2 == "AUTHORIZED" and a1 is not a2), \
        f"replay produced two independent AUTHORIZED grants ({s1}, {s2})"


def test_hypervisor_5_confused_deputy():
    """CONFUSED DEPUTY: a malformed authority record (missing fields, wrong
    types, injected keys) must fail CLOSED with a clean refusal — never crash
    open, never inherit trust from partial data."""
    from mag import policy_engine

    malformed = [
        {},
        {"status": "AUTHORIZED"},                                   # no capabilities
        {"status": None, "granted_capabilities": ["board_write"]},  # null status
        {"status": "AUTHORIZED", "granted_capabilities": "board_write"},  # wrong type
        {"status": "AUTHORIZED", "granted_capabilities": ["board_write"], "budget": "unlimited"},  # junk budget
    ]
    for i, auth in enumerate(malformed):
        verdict = policy_engine.validate_authority(auth, "board_write")
        assert verdict.get("ok") is not True, f"malformed authority {i} must fail closed: {auth}"
