"""Lane effort tiers -- the three Anthropic tiers verbatim + value-per-token gate.

Fold row: corpus/steal/MASTER_MICKEY17_V2_20260924.md #6 [lane: anthropic-multiagent].
Closes G4_4_wiring.md:38 "effort budgets as first-class lane parameter".
"""
from mag import lane_effort as le


def test_selftest_full_pass():
    assert le.selftest() is True


def test_tiers_are_verbatim():
    t1 = le.EFFORT_TIERS["fact_finding"]
    t2 = le.EFFORT_TIERS["comparison"]
    assert (t1["max_lanes"], t1["min_calls"], t1["max_calls"]) == (1, 3, 10)
    assert (t2["min_lanes"], t2["max_lanes"], t2["min_calls"], t2["max_calls"]) == (2, 4, 10, 15)
    assert le.EFFORT_TIERS["complex"]["min_lanes"] == 11  # ">10 lanes"


def test_gate_blocks_overinvestment_in_simple_queries():
    # Named failure mode: a trivial task must not buy comparison-grade fan-out.
    r = le.fanout_gate(width=3, value=0.1, tokens=1000)
    assert r["admitted"] is False
    assert r["tier"] == "comparison"  # budget still handed out; gate blocks the spend
