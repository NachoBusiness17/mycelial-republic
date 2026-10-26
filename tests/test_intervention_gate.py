"""Intervention gate - inject-vs-silent memory gate (Thread B minimal build).

pytest mirror of `python -m mag.intervention_gate --self-test`. The 164418Z
false-positive-injection test (silence must beat a wrong reminder) is a
first-class case here, not a bonus.
"""
from __future__ import annotations

import json

import pytest

from mag import intervention_gate as ig


@pytest.fixture(autouse=True)
def _isolate_register(tmp_path, monkeypatch):
    reg_path = tmp_path / "memory_interventions.jsonl"
    monkeypatch.setattr(ig, "REGISTER_PATH", reg_path)
    yield reg_path


def test_schema_rejects_unknown_memory_type():
    with pytest.raises(ValueError):
        ig.MemoryEntry(0, "preference", "x", 0.5)


def test_schema_accepts_the_three_types():
    for mt in ig.MEMORY_TYPES:
        m = ig.MemoryEntry(0, mt, "value text", 0.5)
        assert m.memory_type == mt
        assert m.memory_id  # stable handle derived when omitted


def test_decay_trigger_full_vanish_only():
    m = ig.MemoryEntry(0, "constraint", "never push to main without tests passing", 0.9)
    # fully out of the window -> decayed
    assert ig.state_decayed(m, ["wire the endpoint", "update route table"], k=3)
    # partial overlap (token 'tests' still visible) -> NOT decayed (abstain side)
    assert not ig.state_decayed(m, ["run the tests now"], k=3)
    # empty window -> no evidence is not evidence of decay
    assert not ig.state_decayed(m, [], k=3)


def test_gate_decision_order_relevance_cooldown_decay():
    m = ig.MemoryEntry(0, "history", "last attempt failed on rate-limit backoff", 0.5)
    d = ig.decide(m, 3, ["auth retry paths"], None, ig.GatePolicy())
    assert (d.decision, d.reason) == ("silent", "relevance_floor")

    hi = ig.MemoryEntry(0, "constraint", "never push to main without tests passing", 0.9)
    d = ig.decide(hi, 4, ["wire endpoints"], 2, ig.GatePolicy(cooldown_steps=5))
    assert (d.decision, d.reason) == ("silent", "cooldown")

    d = ig.decide(hi, 4, ["run the tests"], None, ig.GatePolicy())
    assert (d.decision, d.reason) == ("silent", "state_live")

    d = ig.decide(hi, 4, ["wire the refresh endpoint"], None, ig.GatePolicy())
    assert (d.decision, d.reason) == ("inject", "decay_detected")


def test_worked_example_shape():
    ex = ig.worked_example(do_register=False)
    by = {(d.memory_id, d.step): d for d in ex["decisions"]}
    assert by[("c_tests", 5)].decision == "inject"
    assert by[("c_tests", 6)].reason == "cooldown"
    assert by[("c_tests", 10)].decision == "inject"
    goal_injects = [s for s in range(1, 13) if by[("g_refresh", s)].decision == "inject"]
    assert len(goal_injects) == 1
    assert all(by[("h_backoff", s)].reason == "relevance_floor" for s in range(1, 13))


def test_false_positive_injection_test():
    """The 164418Z caution: a wrong reminder must be worse than silence."""
    ex = ig.worked_example(do_register=False)
    for d in ex["decisions"]:
        d.was_relevant = (d.memory_id in ("c_tests", "g_refresh")
                          and d.decision == "inject")
    wrong = ig.MemoryEntry(6, "goal", "draft the endpoint docs today", 0.7, "g_docs_wrong")
    probe = ig.decide(wrong, 6, ["wire the refresh endpoint", "update route table",
                                 "token docs touched"], None, ig.GatePolicy())
    assert (probe.decision, probe.reason) == ("silent", "state_live")
    probe.was_relevant = False
    score = ig.score_run(ex["decisions"] + [probe])
    assert score["false_positive_injections"] == 0
    assert score["true_positive_injections"] >= 2
    assert score["passed"] is True


def test_register_roundtrip_and_cooldown(_isolate_register):
    ex = ig.worked_example(register_path=_isolate_register)
    rows = [r for r in ig.load_register(_isolate_register)
            if r.get("run_id") == ex["run_id"]]
    assert len(rows) == len(ex["decisions"])
    assert all(isinstance(json.loads(json.dumps(r)), dict) for r in rows)
    assert ig.last_injected_step("c_tests", rows) == 10
    s = ig.summarize(_isolate_register)
    assert s["rows"] == len(rows)
    assert s["injects"] == sum(1 for d in ex["decisions"] if d.decision == "inject")


def test_builtin_self_test_green():
    report = ig.self_test()  # runs against the real register path
    assert report["ok"] is True, report["checks"]
