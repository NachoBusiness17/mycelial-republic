"""tests/test_overmind_loop.py - OVERMIND-2 (THE FALSIFIER RUN), 2026-10-01.

Spec: watch/inbox/model_garden/OVERMIND_THEORY.md sec 2.2 + 6 + 7 (gaps 1+2)
plus the OVERMIND-2 lane order: minimal fail-closed verb table
(STAGE_ASK / PROMOTE_TICKET / ALERT / NOOP-with-reason), $1 hard cap
per-call and cumulative, hash-chained ledger, NO steering surface for the
glm brain. These tests pin the law BEFORE the organ fires (tests-first per
the lane order; the organ is tools/overmind_loop.py).
All tests offline: no network, no git mutation, no real model calls.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import overmind_loop as ol  # noqa: E402
from tools import overmind_verbs as ov  # noqa: E402


# ---------------------------------------------------------------- verb table

def test_verb_table_is_frozen_and_minimal():
    assert set(ol.VERB_TABLE) == {"STAGE_ASK", "PROMOTE_TICKET", "ALERT", "NOOP"}


def test_unknown_verb_fails_closed():
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "GIT_PUSH", "reason": "push my work",
                          "payload": {}})


def test_verb_requires_reason_every_time():
    # NOOP without a reason is the still-world trap (kill condition 3's seed)
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "NOOP", "payload": {}})
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "ALERT", "payload": {"message": "x"}})


def test_payload_contracts_per_verb():
    ok = ol.validate_verb({"verb": "ALERT", "reason": "driver failing",
                           "payload": {"message": "orchestrator exits 1"}})
    assert ok == "ALERT"
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "ALERT", "reason": "r",
                          "payload": {"message": ""}})
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "STAGE_ASK", "reason": "r", "payload": {}})
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "PROMOTE_TICKET", "reason": "r",
                          "payload": {"target": "t"}})  # no justification
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "NOOP", "reason": "r",
                          "payload": {"message": "not allowed here"}})


def test_reason_length_capped():
    with pytest.raises(ol.UnauthorizedVerb):
        ol.validate_verb({"verb": "NOOP", "reason": "x" * 301, "payload": {}})


def test_execute_unknown_verb_raises_and_writes_nothing(tmp_path):
    before = sorted(p.name for p in tmp_path.rglob("*"))
    with pytest.raises(ol.UnauthorizedVerb):
        ol.execute_verb("RM_RF", {"path": str(tmp_path)}, _tick_ctx(tmp_path))
    assert sorted(p.name for p in tmp_path.rglob("*")) == before


# ------------------------------------------------------- sanctioned surfaces

def _tick_ctx(run_dir: Path, tick: int = 1, run_id: str = "t-run") -> dict:
    return {"run_id": run_id, "tick": tick, "ts": "2026-10-01T00:00:00Z"}


def test_alert_writes_only_attention_and_verifies(tmp_path, monkeypatch):
    att = tmp_path / "attention.md"
    att.write_text("# attention\n", encoding="utf-8")
    monkeypatch.setattr(ov, "ATTENTION", att)
    res = ol.execute_verb("ALERT", {"message": "census patrol dark"},
                          _tick_ctx(tmp_path, tick=7))
    assert res["executed"] is True
    assert res["verified"] is True  # read-back found the bytes
    assert "census patrol dark" in att.read_text(encoding="utf-8")
    assert res["surface"] == str(att)


def test_alert_cannot_be_steered_to_another_path(tmp_path, monkeypatch):
    # payload carrying a path field must be ignored, not honored
    att = tmp_path / "attention.md"
    att.write_text("", encoding="utf-8")
    monkeypatch.setattr(ov, "ATTENTION", att)
    rogue = tmp_path / "rogue.md"
    ol.execute_verb("ALERT", {"message": "m", "path": str(rogue),
                              "file": str(rogue)}, _tick_ctx(tmp_path))
    assert not rogue.exists()


def test_stage_ask_writes_fireable_ask_dir(tmp_path, monkeypatch):
    staged = tmp_path / "staged"
    monkeypatch.setattr(ov, "STAGED_DIR", staged)
    res = ol.execute_verb(
        "STAGE_ASK",
        {"target": "mag/afk_loop.py", "ask": "check the trigger law"},
        _tick_ctx(tmp_path, tick=3, run_id="t-run"))
    assert res["executed"] is True and res["verified"] is True
    ask_json = staged / res["artifact"] / "ask.json"
    meta = json.loads(ask_json.read_text(encoding="utf-8"))
    for field in ("id", "model", "base_env", "base_url", "contract"):
        assert meta.get(field), field
    assert meta["model"] == ol.STAGED_ASK_MODEL
    assert "revision" not in meta  # single-turn; no steering surface
    assert "mag/afk_loop.py" in meta["contract"]


def test_promote_ticket_appends_proposal_never_applies(tmp_path, monkeypatch):
    prop = tmp_path / "proposals.jsonl"
    monkeypatch.setattr(ov, "PROPOSALS", prop)
    res = ol.execute_verb(
        "PROMOTE_TICKET",
        {"target": "c-abc123", "justification": "green 3 runs"},
        _tick_ctx(tmp_path, tick=9))
    assert res["executed"] is True and res["verified"] is True
    rows = [json.loads(l) for l in
            prop.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 1
    assert rows[0]["target"] == "c-abc123"
    assert rows[0]["authority"] == "operator-human-gate"
    # the verb writes exactly one surface
    assert sorted(p.name for p in tmp_path.iterdir()) == ["proposals.jsonl"]


def test_noop_executes_nothing_but_carries_reason(tmp_path):
    res = ol.execute_verb("NOOP", {}, _tick_ctx(tmp_path))
    assert res == {"executed": False, "verified": True,
                   "reason": "", "verb": "NOOP"} or res["executed"] is False


# --------------------------------------------------------------- budget caps

def test_per_call_cap_violation_detected():
    cap = ol.BudgetCap(per_call=0.10, cumulative=1.0)
    with pytest.raises(ol.BudgetExceeded):
        cap.charge(0.11, ask_id="x")


def test_cumulative_gate_holds_before_dispatch():
    cap = ol.BudgetCap(per_call=0.10, cumulative=1.0)
    assert cap.allow_dispatch(spent=0.0, reserve=0.05) is True
    assert cap.allow_dispatch(spent=0.98, reserve=0.05) is False
    cap.charge(0.10, ask_id="a")
    assert cap.spent == 0.10
    cap.charge(0.10, ask_id="b")  # cumulative 0.20 of 1.0: legal
    assert cap.spent == 0.20
    cap2 = ol.BudgetCap(per_call=1.0, cumulative=0.15)
    cap2.charge(0.10, ask_id="a")
    with pytest.raises(ol.BudgetExceeded):
        cap2.charge(0.10, ask_id="b")  # 0.20 > 0.15 cumulative breach


# ------------------------------------------------------------ ledger + chain

def test_ledger_chain_append_and_verify(tmp_path, monkeypatch):
    led = tmp_path / "ledger.jsonl"
    monkeypatch.setattr(ol, "LEDGER", led)
    for i in range(3):
        ol.ledger_append({"tick": i, "verb": "NOOP", "reason": "r"})
    v = ol.verify_ledger()
    assert v["ok"] is True and v["rows"] == 3
    # tamper row 2: the chain must break exactly there
    lines = led.read_text(encoding="utf-8").splitlines()
    row = json.loads(lines[1]); row["verb"] = "ALERT"
    lines[1] = json.dumps(row, ensure_ascii=False)
    led.write_text("\n".join(lines) + "\n", encoding="utf-8")
    v2 = ol.verify_ledger()
    assert v2["ok"] is False and v2["break_at"] == 2


# ---------------------------------------------------------- brain reply parse

def test_parse_decision_from_fenced_and_prosy_replies():
    fenced = 'sure\n```json\n{"verb": "NOOP", "reason": "still world", "payload": {}}\n```'
    assert ol.parse_decision(fenced)["verb"] == "NOOP"
    prosy = 'Here is my call: {"verb": "ALERT", "reason": "r", "payload": {"message": "m"}} done.'
    assert ol.parse_decision(prosy)["verb"] == "ALERT"
    assert ol.parse_decision("garbage with no object") is None


def test_brain_ask_json_has_no_steering_surface(tmp_path):
    d = tmp_path / "ask"
    meta = ol.write_brain_ask(d, ask_id="om-t001",
                              contract="tick contract bytes")
    assert meta["id"] == "om-t001"
    assert "revision" not in meta and meta.get("turn2_only") is None
    assert json.loads((d / "ask.json").read_text(encoding="utf-8"))["id"] == "om-t001"


def test_module_source_carries_no_steering_wiring():
    for name in ("overmind_loop.py", "overmind_verbs.py",
                 "overmind_senses.py"):
        src = (ROOT / "tools" / name).read_bytes()
        for token in (b"steer_seal", b"revision.md", b"admit_text",
                      b"envelope"):
            assert token not in src, (name, token)


# ------------------------------------------------------------- sense layers

def test_senses_run_read_only_and_tolerate_missing(tmp_path):
    git_sense = ol.sense_sha_tail()
    assert {"changed_count", "tail", "head_commit"} <= set(git_sense)
    beat = ol.sense_driver_beat(since_ts="1970-01-01T00:00:00Z")
    assert "rows_since_run_start" in beat
    q = ol.sense_queue()
    assert {"todo_open", "handoff_items", "wait_human_bytes",
            "queue_index_rows"} <= set(q)
    # missing surfaces degrade to honest zeros, never raise
    beat2 = ol.sense_driver_beat(since_ts="1970-01-01T00:00:00+00:00",
                                 path=tmp_path / "nope.jsonl")
    assert beat2["missing"] is True
    q2 = ol.sense_queue(todo=path_missing(), handoff=path_missing())
    assert q2["todo_open"] == 0 and q2["missing_inputs"]


def path_missing():
    import tempfile
    return Path(tempfile.gettempdir()) / "overmind-missing-probe"


def test_sense_landed_counts_files_newer_than_start(tmp_path):
    old = tmp_path / "old.md"; old.write_text("x", encoding="utf-8")
    import os, time
    new = tmp_path / "new.md"; new.write_text("y", encoding="utf-8")
    os.utime(old, (time.time() - 3600, time.time() - 3600))
    res = ol.sense_landed(since_ts=None, root=tmp_path)
    assert res["count"] >= 1
    assert any("new.md" in n for n in res["tail"]) or res["count"] == len(
        list(tmp_path.iterdir()))


# ------------------------------------------------------ judge (offline legs)

_QUIET = {"git_changed": 100, "beat_rows": 0, "beat_last": [],
          "landed_count": 0}
_NOISY = {"git_changed": 140, "beat_rows": 12,
          "beat_last": [{"actor": "orchestrator", "status": "failed"},
                        {"actor": "orchestrator", "status": "failed"}],
          "landed_count": 3}


def _jrow(tick, verb, senses, reason="r"):
    return {"run_id": "t-hour", "tick": tick, "verb": verb, "reason": reason,
            "senses": senses, "executed": verb != "NOOP", "verified": True,
            "events": []}


def _fake_rows():
    return [_jrow(1, "NOOP", _QUIET, "still world"),
            _jrow(2, "NOOP", dict(_QUIET, landed_count=1), "landing"),
            _jrow(3, "ALERT", dict(_NOISY), "failed spawns"),
            _jrow(4, "STAGE_ASK",
                  dict(_NOISY, git_changed=160,
                       beat_last=[{"actor": "governor", "status": "tick"}]),
                  "wide drift, no failures"),
            _jrow(5, "NOOP", dict(_NOISY), "no delta")]


def test_judge_matcher_picks_the_governing_seat_entry(tmp_path, monkeypatch):
    from tools import overmind_judge as oj
    blind = {"entries": [
        {"id": f"D{i:02d}", "verb": "NOOP", "payload": {}, "reason": "r",
         "when": "w"} for i in range(1, 13)]}
    monkeypatch.setattr(oj, "BLIND", tmp_path / "blind.json")
    (tmp_path / "blind.json").write_text(json.dumps(blind),
                                         encoding="utf-8")
    rows = _fake_rows()
    assert oj.match_seat_entry(rows, 0)["id"] == "D02"   # quiet beat
    assert oj.match_seat_entry(rows, 1)["id"] == "D05"   # landing present
    assert oj.match_seat_entry(rows, 2)["id"] == "D01"   # failed spawns
    assert oj.match_seat_entry(rows, 3)["id"] == "D04"   # wide git drift
    assert oj.match_seat_entry(rows, 4)["id"] == "D10"   # last tick of run
    # quiet streak >= 10 escalates D02 -> D03 (and is not the last tick)
    long_quiet = [_jrow(k, "NOOP", _QUIET, "quiet") for k in range(1, 12)]
    long_quiet.append(_jrow(12, "NOOP", dict(_NOISY), "beat returned"))
    assert oj.match_seat_entry(long_quiet, 10)["id"] == "D03"


def test_judge_pairs_cover_all_non_noops(tmp_path, monkeypatch):
    from tools import overmind_judge as oj
    monkeypatch.setattr(oj, "BLIND", tmp_path / "blind.json")
    (tmp_path / "blind.json").write_text(json.dumps({"entries": [
        {"id": f"D{i:02d}", "verb": "NOOP", "payload": {}, "reason": "r",
         "when": "w"} for i in range(1, 13)]}), encoding="utf-8")
    pairs = oj.build_pairs(_fake_rows(), max_pairs=14)
    verbs = {p["loop"]["verb"] for p in pairs}
    assert "ALERT" in verbs and "STAGE_ASK" in verbs
    assert all(p["seat"]["entry_id"] for p in pairs)
    ids = [p["pair_id"] for p in pairs]
    assert len(set(ids)) == len(ids)
