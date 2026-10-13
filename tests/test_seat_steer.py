"""Stateless tests for seat_steer — the architecture path for live seat actions (no shell).
RIB: seat_steer.v1 — send() steers a seat via the driver module + folds answer/spend; enqueue()
writes a queue task file (no shell, no hand-run); execute_goal() parses `[seat-steer] surface | msg`;
REST POST /api/v1/seat/steer is registered. Stateless: tmp_path report dir, monkeypatched seat."""
from __future__ import annotations


def test_send_reuses_seat_and_folds(tmp_path, monkeypatch):
    import mag.seat_steer as m
    import mag.browser_driver as bd
    import mag.frontier_council as fc
    import mag.party_subchain as party_subchain
    import mag.rib_bus as rib_bus
    monkeypatch.setattr(m, "REPORT_DIR", tmp_path)
    monkeypatch.setattr(fc, "ALLOWANCE", tmp_path / "allowance.jsonl")
    monkeypatch.setattr(fc, "CAPS", tmp_path / "caps.json")
    monkeypatch.setattr(party_subchain, "mount", lambda **_kwargs: {"transcript": "nothing yet"})
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})
    monkeypatch.setattr(rib_bus, "inject_for", lambda goal, **_kwargs: goal)
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


def test_alias_and_driver_response_shapes_are_normalized(tmp_path, monkeypatch):
    import mag.seat_steer as m
    import mag.party_subchain as party_subchain
    import mag.rib_bus as rib_bus

    monkeypatch.setattr(m, "REPORT_DIR", tmp_path)
    monkeypatch.setattr(m, "_allowance_surface", lambda _surface: None)
    monkeypatch.setattr(party_subchain, "mount", lambda **_kwargs: {"transcript": "nothing yet"})
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})
    monkeypatch.setattr(rib_bus, "inject_for", lambda goal, **_kwargs: goal)
    calls = []

    def fake_drive(module, driver_surface, message, max_wait_s):
        calls.append((module, driver_surface, message, max_wait_s))
        return {"ok": True, "content": "one normalized answer"}

    monkeypatch.setattr(m, "_drive", fake_drive)
    r = m.send("supergrok", "share this", max_wait_s=7)
    assert r["ok"] is True
    assert r["requested_surface"] == "supergrok"
    assert r["surface"] == "grok"
    assert r["answer"] == "one normalized answer"
    assert calls == [("grok_bot", "grok", "share this", 7)]


def test_surface_aliases_cover_party_and_historical_names():
    import mag.seat_steer as m

    assert m.resolve_surface("grok_web") == "grok"
    assert m.resolve_surface("v4-pro") == "deepseek"
    assert m.resolve_surface("chatgpt-desktop") == "chatgpt_desktop"
    assert m.resolve_surface("grok-desktop") == "grok_desktop"


def test_execute_goal_parses_prefix(tmp_path, monkeypatch):
    import mag.seat_steer as m
    import mag.browser_driver as bd
    import mag.frontier_council as fc
    import mag.party_subchain as party_subchain
    import mag.rib_bus as rib_bus
    monkeypatch.setattr(m, "REPORT_DIR", tmp_path)
    monkeypatch.setattr(fc, "ALLOWANCE", tmp_path / "allowance.jsonl")
    monkeypatch.setattr(fc, "CAPS", tmp_path / "caps.json")
    monkeypatch.setattr(party_subchain, "mount", lambda **_kwargs: {"transcript": "nothing yet"})
    monkeypatch.setattr(party_subchain, "append", lambda **_kwargs: {"ok": True})
    monkeypatch.setattr(rib_bus, "inject_for", lambda goal, **_kwargs: goal)

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


def test_enqueue_normalizes_alias(monkeypatch):
    import mag.seat_steer as m
    import mag.orchestrator as o

    captured = {}

    def fake_enqueue(goal, **_kwargs):
        captured["goal"] = goal
        return {"ok": True}

    monkeypatch.setattr(o, "enqueue", fake_enqueue)
    assert m.enqueue("v4-pro", "take a turn")["ok"] is True
    assert captured["goal"] == "[seat-steer] deepseek | take a turn"


def test_rest_route_can_invoke_roundtable(monkeypatch):
    from dashboard.rest import h_seat_steer
    from mag import frontier_salon

    captured = {}

    def fake_roundtable(question, **kwargs):
        captured["question"] = question
        captured.update(kwargs)
        return {"ok": True, "mode": "roundtable", "n_contributions": 4}

    monkeypatch.setattr(frontier_salon, "roundtable", fake_roundtable)
    status, result = h_seat_steer({}, {
        "mode": "roundtable",
        "message": "find a moonshot",
        "participants": ["chatgpt", "supergrok"],
        "rounds": 2,
        "max_wait_s": 5,
    })
    assert status == 200 and result["ok"] is True
    assert captured == {
        "question": "find a moonshot",
        "participants": ["chatgpt", "supergrok"],
        "rounds": 2,
        "max_wait_s": 5,
    }
