"""Stateless tests for seat_steer — the architecture path for live seat actions (no shell).
RIB: seat_steer.v1 — send() steers a seat via the driver module + folds answer/spend; enqueue()
writes a queue task file (no shell, no hand-run); execute_goal() parses `[seat-steer] surface | msg`;
REST POST /api/v1/seat/steer is registered. Stateless: tmp_path report dir, monkeypatched seat."""
from __future__ import annotations


def test_send_reuses_seat_and_folds(tmp_path, monkeypatch):
    import mag.seat_steer as m
    import mag.browser_driver as bd
    import mag.frontier_council as fc
    monkeypatch.setattr(m, "REPORT_DIR", tmp_path)
    monkeypatch.setattr(fc, "ALLOWANCE", tmp_path / "allowance.jsonl")
    monkeypatch.setattr(fc, "CAPS", tmp_path / "caps.json")
    captured = {}

    def fake_ask(goal, *, surface="deepseek", max_wait_s=120):
        captured["goal"] = goal
        return {"ok": True, "surface": surface, "answer": "hi from mag"}

    monkeypatch.setattr(bd, "ask", fake_ask)
    r = m.send("deepseek", "say hi")
    assert r["ok"] is True and "hi from mag" in r["answer"]
    assert captured["goal"] == "say hi"
    assert r["report"]  # folded
    assert r["spend"]["ok"] is True  # routed through frontier_council


def test_send_unknown_surface():
    import mag.seat_steer as m
    assert m.send("nope", "hi")["ok"] is False


def test_send_empty_message():
    import mag.seat_steer as m
    assert m.send("chatgpt", "")["ok"] is False


def test_execute_goal_parses_prefix(tmp_path, monkeypatch):
    import mag.seat_steer as m
    import mag.browser_driver as bd
    import mag.frontier_council as fc
    monkeypatch.setattr(m, "REPORT_DIR", tmp_path)
    monkeypatch.setattr(fc, "ALLOWANCE", tmp_path / "allowance.jsonl")
    monkeypatch.setattr(fc, "CAPS", tmp_path / "caps.json")

    def fake_ask(goal, *, surface="deepseek", max_wait_s=120):
        return {"ok": True, "surface": surface, "answer": "re:" + goal}

    monkeypatch.setattr(bd, "ask", fake_ask)
    r = m.execute_goal("[seat-steer] deepseek | say hi")
    assert r["ok"] is True and r["surface"] == "deepseek"
    assert "say hi" in r["message"]


def test_enqueue_writes_queue_file(tmp_path, monkeypatch):
    import mag.seat_steer as m
    import mag.orchestrator as o
    captured = {}

    def fake_enqueue(goal, *, provider="deepseek", model=None, timeout=600, tag="",
                     priority=0, tier=None, require_build=None):
        captured["goal"] = goal
        captured["tag"] = tag
        return {"ok": True, "queue_id": "q-test", "goal": goal}

    monkeypatch.setattr(o, "enqueue", fake_enqueue)
    r = m.enqueue("chatgpt", "say hi")
    assert r["ok"] is True and r["queue_id"] == "q-test"
    assert captured["goal"].startswith("[seat-steer] chatgpt | say hi")
    assert captured["tag"] == "seat-steer"
