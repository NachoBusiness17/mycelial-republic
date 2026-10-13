"""Tests for VERB stones five-to-nine (sift/witness/vow/abide/meter) and the
kifu chain. All offline: lanes are monkeypatched; the trace is redirected to
tmp_path so the live kifu is never touched by tests."""
import json

import pytest

from mag import verb


@pytest.fixture
def trace(tmp_path, monkeypatch):
    t = tmp_path / "verb_trace.jsonl"
    monkeypatch.setattr(verb, "TRACE", t)
    return t


def _lane(ans):
    return lambda q, key, model="openai/gpt-oss-20b": ans


def test_sift_rejects_compound_and_two_judgments(trace):
    out = verb.sift(["Is the user angry and confused?", "Is it A? Is it B?"])
    assert len(out["rejected"]) == 2
    reasons = " | ".join(r["reason"] for r in out["rejected"])
    assert "atomicity" in reasons and "one-judgment" in reasons


def test_sift_decomposes_wide_choice(trace):
    out = verb.sift([{"question": "Which lane?", "options": list("abcde")}])
    assert all(q["kind"] != "CHOICE" for q in out["ok"])
    assert len(out["decomposed"]["Which lane?"]) == 5


def test_sift_keeps_legal_choice_and_warns_state_isolation(trace):
    out = verb.sift([{"question": "Which lane?", "options": ["a", "b"]},
                     "Given Q1, is the transaction fraudulent?"])
    kinds = [q["kind"] for q in out["ok"]]
    assert kinds == ["CHOICE", "NOUL"]
    assert "state isolation" in out["warnings"][0]["reason"]


def test_witness_green_on_full_agreement(trace, monkeypatch):
    monkeypatch.setattr(verb, "_ask_lane", _lane("GROUNDED YES CONFIDENCE: 90"))
    v = verb.witness("Is the chain green?",
                     pack=[("a", "m1", 1), ("b", "m2", 2)], kpack=False)
    assert v["verdict"] == "GREEN" and v["vote"] == "YES"


def test_witness_purple_on_disagreement(trace, monkeypatch):
    answers = iter(["GROUNDED YES CONFIDENCE: 80", "GROUNDED NO CONFIDENCE: 75"])
    monkeypatch.setattr(verb, "_ask_lane",
                        lambda q, key, model="m": next(answers))
    v = verb.witness("Is x true?", pack=[("a", "m1", 1), ("b", "m2", 2)], kpack=False)
    assert v["verdict"] == "PURPLE" and v["route"] == "ESCALATE_MODEL"


def test_witness_transport_death_never_green(trace, monkeypatch):
    def boom(q, key, model="m"):
        raise RuntimeError("404 stealth death")
    monkeypatch.setattr(verb, "_ask_lane", boom)
    v = verb.witness("Is x true?", pack=[("a", "m1", 1), ("b", "m2", 2)], kpack=False)
    assert v["verdict"] == "PURPLE" and all(x is None for x in v["votes"])


def test_feels_silence_routes_by_risk(trace, monkeypatch):
    def down(q, key, model="m"):
        raise RuntimeError("lane down")
    monkeypatch.setattr(verb, "_ask_lane", down)
    for risk, route in [("low", "PASS_UNVERIFIED"), ("medium", "QUEUE_RETRY"),
                        ("high", "ESCALATE_MODEL"),
                        ("irreversible", "WAKE_HUMAN")]:
        v = verb.feels("q?", kpack=False, risk=risk)
        assert v["route"] == route


def test_vow_closes_when_stop_holds(trace, monkeypatch):
    monkeypatch.setattr(verb, "_ask_lane", _lane("GROUNDED YES CONFIDENCE: 95"))
    fired = []
    row = verb.vow("Should the drive stop?", lambda: fired.append(1))
    assert row["verb"] == "WHILE_CLOSED" and not fired


def test_vow_extends_and_acts(trace, monkeypatch):
    monkeypatch.setattr(verb, "_ask_lane", _lane("GROUNDED NO CONFIDENCE: 95"))
    fired = []
    row = verb.vow("Should the drive stop?", lambda: fired.append(1))
    assert row["verb"] == "WHILE_EXTENDED" and row["acted"] and fired == [1]


def test_abide_uncited_rule_never_gates(trace, monkeypatch):
    monkeypatch.setattr(verb, "_ask_lane", _lane("GROUNDED YES CONFIDENCE: 80"))
    out = verb.abide("not a bug but a feature -- amazing", ["", "No em-dashes"])
    assert len(out["fires"]) == 2
    assert all(f["gate"] is False for f in out["fires"])
    assert out["gate"] is False


def test_kifu_chain_and_tamper_detection(trace):
    verb._emit({"verb": "A"})
    verb._emit({"verb": "B"})
    assert verb.verify_trace()["healthy"]
    rows = [json.loads(ln) for ln in trace.read_text().splitlines()]
    rows[0]["verb"] = "TAMPERED"
    trace.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    assert not verb.verify_trace()["healthy"]


def test_meter_refuses_decoration(trace, monkeypatch):
    monkeypatch.setattr(verb, "FLEET_BENCH", trace.parent / "fb")
    with pytest.raises(ValueError):
        verb.meter_record("m1", "A", "YES", "YES", evidence="")


def test_meter_rows_feed_weekly_trigger(trace, monkeypatch):
    monkeypatch.setattr(verb, "FLEET_BENCH", trace.parent / "fb")
    for i in range(45):
        verb.meter_record(f"m{i}", "A", "YES", "YES",
                          evidence="arithmetic: 2+2=4")
    t = verb.weekly_trigger()
    assert t["meter_valid"] and t["n"] == 45 and t["accuracy"] == 1.0
    assert t["trigger_ge_0880"] is True


def test_meter_idempotent_by_id(trace, monkeypatch):
    monkeypatch.setattr(verb, "FLEET_BENCH", trace.parent / "fb")
    verb.meter_record("s-1", "A", "YES", "YES", evidence="arithmetic: 1")
    again = verb.meter_record("s-1", "A", "NO", "YES", evidence="arithmetic: 1")
    assert again.get("dup") is True and again["correct"] is True
    rows = (trace.parent / "fb" / "scores.jsonl").read_text().splitlines()
    assert len(rows) == 1
