"""Grey Swan steal: Mag Lab episode uses Observation for legal actions + admitted skill."""
from __future__ import annotations

from mag.lab_episode import (
    SHARED_DEP_SKILL,
    ActionType,
    Observation,
    Seen,
    Svc,
    fire_shared_dep,
    legal_actions,
    new_blackout,
    run_blackout,
    shock,
)
from mag.max_distill import validate_skill


def test_shared_dep_skill_admitted():
    v = validate_skill(SHARED_DEP_SKILL)
    assert v["admitted"] is True, v


def test_legal_actions_unknown_is_inspect_not_repair():
    ep = new_blackout(1)
    legal = set(legal_actions(ep.obs, ep.topo))
    assert (ActionType.INSPECT, "S1") in legal
    assert (ActionType.REPAIR, "S1") not in legal
    assert (ActionType.SACRIFICE, "C1") not in legal  # service UNKNOWN, not UNPOWERED


def test_legal_sacrifice_from_observation_not_world():
    ep = shock(new_blackout(0))
    ep.world.sacrificed = frozenset({"C1"})  # world-only; skill/legal must ignore
    legal = set(legal_actions(ep.obs, ep.topo))
    if ep.obs.service.get("C1") is Svc.UNPOWERED and "C1" not in ep.obs.sacrificed:
        assert (ActionType.SACRIFICE, "C1") in legal


def test_skill_inspects_shared_unknown_upstream():
    ep = shock(new_blackout(0))
    fired = fire_shared_dep(ep.obs, ep.topo)
    unpowered = [c for c, s in ep.obs.service.items() if s is Svc.UNPOWERED]
    if len(unpowered) >= 2:
        assert fired is not None
        assert fired[0] is ActionType.INSPECT
        assert ep.obs.entity[fired[1]] is Seen.UNKNOWN


def test_run_blackout_small():
    out = run_blackout(8)
    assert out["ok"] is True
    assert out["admission"]["admitted"] is True
    assert "TRUE" in out["summary"]["SKILL"]
    assert out["true_improvement_skill_minus_greedy"] is not None
