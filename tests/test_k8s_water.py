"""k8s_water_sim tests — WD's K8s-as-water v0 (2026-09-30).

Mission properties: priority ordering respected (high-priority pods drain
before low), quota caps enforced (per-tick service <= quota), shed happens at
the sill threshold, no pod ever goes negative, the economy never leaks.
The engine (mag/water_graph.py) is untouched — these tests pin the mapping.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from k8s_water_sim import (  # noqa: E402
    k8s_scenario,
    simulate,
    spec_from_workload,
    workload_from_ledger,
)


def _spec(pods, classes=None, quota=2, burst=None, budget=0, ticks=24, **kw):
    return {
        "quota": quota, "burst": burst,
        "classes": classes or [
            {"name": "critical", "elev": 60, "sill": 1},
            {"name": "burstable", "elev": 40, "sill": 1},
            {"name": "best-effort", "elev": 20, "sill": 1},
        ],
        "pods": pods,
        "escalation": {"tier_elev": 200, "budget": budget},
        "ticks": ticks, **kw,
    }


def _events(res):
    return [ev for row in res["trace"] for ev in row["events"]]


def test_k8s_scenario_maps_spec_to_graph():
    spec = _spec(
        [{"name": "a", "class": "critical", "pending": 3, "limit": 2},
         {"name": "b", "class": "best-effort", "pending": 1, "limit": 1}],
        classes=[{"name": "critical", "elev": 60, "sill": 1},
                 {"name": "best-effort", "elev": 20, "sill": 2}])
    sc = k8s_scenario(spec)
    g = sc.graph
    # pod = Node(elev = PriorityClass, volume = pending requests)
    assert g.nodes["pod:a"].elev == 60 and g.nodes["pod:a"].volume == 3
    assert g.nodes["pod:b"].elev == 20 and g.nodes["pod:b"].volume == 1
    assert g.nodes["pod:a"].elev > g.nodes["pod:b"].elev, "priority ladder encoded in elevation"
    # load shedding = sill junction at the class dispatch
    d = g.nodes["dispatch:best-effort"]
    assert d.kind == "sill" and d.sill == 2 and d.elev == 20 - 5
    # quota = pipe cap on the trunk
    assert g.pipes["baseline"].cap == 2
    # escalation = boil to the highest cold node
    colds = [n for n in g.nodes.values() if n.kind == "cold"]
    assert [n.name for n in colds] == ["escalation_tier"] and colds[0].elev == 200
    # autoscaler = siphon with crest (spec without burst has no siphon)
    assert "burst" not in g.pipes
    sc2 = k8s_scenario(_spec([{"name": "a", "class": "critical", "pending": 1, "limit": 1}],
                             burst={"cap": 2, "crest": 3}))
    assert sc2.graph.pipes["burst"].siphon and sc2.graph.pipes["burst"].crest == 3


def test_priority_ordering_respected():
    spec = _spec(
        [{"name": "crit", "class": "critical", "pending": 5, "limit": 2},
         {"name": "beef", "class": "burstable", "pending": 5, "limit": 2}],
        quota=2, ticks=16)
    res = simulate(spec)
    crit = [r["tick"] for r in res["trace"] if "crit" in r["admitted"]]
    beef = [r["tick"] for r in res["trace"] if "beef" in r["admitted"]]
    assert crit and beef, "both pods must be served eventually"
    assert max(crit) < min(beef), "every critical unit drains before the first low unit"
    crit_empty = min(r["tick"] for r in res["trace"] if r["pending"]["crit"] == 0)
    assert min(beef) >= crit_empty, "low-priority service starts only once critical is empty"
    assert res["served"] == 10 and res["waste"] == 0


def test_quota_caps_enforced():
    spec = _spec([{"name": "crit", "class": "critical", "pending": 12, "limit": 2}],
                 quota=2, ticks=16)
    res = simulate(spec)
    assert all(r["served"] <= 2 for r in res["trace"]), "per-tick service never exceeds quota"
    assert all(r["admitted"].get("crit", 0) <= 2 for r in res["trace"]), "per-pod limit holds"
    assert res["served"] == 12 and res["waste"] == 0


def test_shed_at_sill_threshold():
    classes = [{"name": "best-effort", "elev": 20, "sill": 2}]
    # one delivering pod < sill 2: held below the gate, then starved to waste
    spec = _spec([{"name": "solo", "class": "best-effort", "pending": 1, "limit": 1}],
                 classes=classes, quota=2, ticks=8)
    res = simulate(spec)
    assert any(r["held"] == 1 for r in res["trace"]), "below-sill inflow is held, pooled"
    assert any("STARVED" in ev for ev in _events(res)), "engine names the starvation"
    assert res["served"] == 0 and res["waste"] == 1, "sub-threshold batch is shed, not served"


def test_sill_passes_at_threshold():
    classes = [{"name": "best-effort", "elev": 20, "sill": 2}]
    # two delivering pods >= sill 2: admitted and served
    spec = _spec([{"name": "one", "class": "best-effort", "pending": 1, "limit": 1},
                  {"name": "two", "class": "best-effort", "pending": 1, "limit": 1}],
                 classes=classes, quota=2, ticks=8)
    res = simulate(spec)
    assert res["served"] == 2 and res["waste"] == 0
    assert not any("STARVED" in ev for ev in _events(res))


def test_no_negative_volume_and_conservation():
    spec = _spec(
        [{"name": "crit", "class": "critical", "pending": 6, "limit": 2},
         {"name": "burst", "class": "burstable", "pending": 5, "limit": 2},
         {"name": "beef", "class": "best-effort", "pending": 3, "limit": 1}],
        classes=[{"name": "critical", "elev": 60, "sill": 1},
                 {"name": "burstable", "elev": 40, "sill": 1},
                 {"name": "best-effort", "elev": 20, "sill": 2}],
        quota=2, burst={"cap": 2, "crest": 2}, budget=1, ticks=40,
        arrivals=[{"tick": 2, "pod": "crit", "units": 2}], waste_seed=1)
    res = simulate(spec)  # check_invariants=True asserts live, every tick
    assert res["total"] == 17, "6+5+3 pending, +2 arrivals, +1 waste seed"
    assert all(v >= 0 for r in res["trace"] for v in r["pending"].values()), \
        "no pod ever holds negative volume"
    assert res["served"] + res["waste"] + res["mux"] + res["escalation_tier"] == 17
    # everything eventually recovered through shed -> boil -> top tier
    assert res["served"] == 17 and res["waste"] == 0


def test_autoscaler_siphon_primes_and_breaks():
    spec = _spec([{"name": "crit", "class": "critical", "pending": 6, "limit": 3}],
                 quota=1, burst={"cap": 2, "crest": 3}, ticks=16)
    res = simulate(spec)
    evs = _events(res)
    assert any("Siphon burst primes at crest (3)" in ev for ev in evs), \
        "backlog at crest primes the autoscaler"
    assert any("Siphon burst breaks (intake dry)" in ev for ev in evs), \
        "drained mux scales the burst pool back in"
    assert max(r["served"] for r in res["trace"]) == 3, "burst adds cap over the baseline 1"
    assert res["served"] == 6, "nothing lost scaling up and down"


def test_escalation_boils_shed_work_to_top_tier():
    classes = [{"name": "best-effort", "elev": 20, "sill": 2}]
    spec = _spec([{"name": "solo", "class": "best-effort", "pending": 1, "limit": 1}],
                 classes=classes, quota=1, budget=1, ticks=12)
    res = simulate(spec)
    evs = _events(res)
    assert any("STARVED" in ev for ev in evs), "unit sheds at the sill first"
    assert any("Steam condenses at escalation_tier" in ev for ev in evs), \
        "boil lifts it past every pipe to the cold crown"
    assert res["served"] == 1 and res["waste"] == 0 and res["escalation_tier"] == 0, \
        "shed work is re-served through the top-tier lane"


def test_ledger_workload_feeds_simulator():
    db = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"
    if not db.exists():
        pytest.skip(f"ledger absent: {db}")
    wl = workload_from_ledger(db)
    assert wl["meta"]["events"] >= 10, "verdict_log currently holds 10 rows"
    assert len(wl["pods"]) >= 2, "glm-prime and mountain-world pods expected"
    assert wl["waste_seed"] == 1, "the one failed verdict seeds the waste basin"
    spec = spec_from_workload(
        wl,
        classes=[{"name": "critical", "elev": 60, "sill": 1},
                 {"name": "burstable", "elev": 40, "sill": 2}],
        quota=2, burst={"cap": 2, "crest": 2}, budget=1, ticks=40)
    res = simulate(spec)
    assert res["served"] == res["total"], "every ledger unit eventually served"
    assert res["waste"] == 0
    assert any(r["shed"] > 0 for r in res["trace"]), \
        "the single-pod burstable batch below sill 2 gets shed then escalated"
