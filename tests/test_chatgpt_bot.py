"""Stateless tests for chatgpt_bot — steer ChatGPT like grok bot (surface + seat + test_artifact).
RIB: chatgpt_bot.v1 — spec() controlled task spec; steer() drives browser_driver chatgpt surface and
reads the answer (honest if down); test_artifact() renders the surface-rightsized artifact + steers
it; heartbeat() liveness. Also verifies the chatgpt surface exists in browser_driver (no CDP/network
needed — the surfaces dict + ask contenteditable branch are pure config/code)."""
from __future__ import annotations


def test_spec_controlled_task():
    import mag.chatgpt_bot as m
    s = m.spec("start the dungeon")
    assert s["seat"] == "chatgpt-bot"
    assert "paid" in " ".join(s["directives"]).lower()
    assert s["report"].endswith("chatgpt_bot")  # the report dir for the seat


def test_steer_empty_goal():
    import mag.chatgpt_bot as m
    r = m.steer("")
    assert r["ok"] is False and "empty goal" in r["error"]


def test_steer_honest_when_browser_down(monkeypatch):
    import mag.chatgpt_bot as m
    import mag.browser_driver as bd

    def fake_ask(goal, *, surface="deepseek", max_wait_s=120):
        return {"ok": False, "error": "cannot connect to container CDP"}

    monkeypatch.setattr(bd, "ask", fake_ask)
    r = m.steer("hello", surface="chatgpt")
    assert r["ok"] is False  # never fabricates an answer when the seat is down
    assert "cannot connect" in r["error"]


def test_test_artifact_renders_and_steers(monkeypatch):
    import mag.chatgpt_bot as m
    import mag.browser_driver as bd

    def fake_ask(goal, *, surface="deepseek", max_wait_s=120):
        return {"ok": True, "surface": surface, "answer": "The party arrives at the first room...",
                "url": "https://chatgpt.com"}

    monkeypatch.setattr(bd, "ask", fake_ask)
    r = m.test_artifact(module="dnd", surface="generic_ai")
    assert r["ok"] is True
    assert r["module"] == "dnd"
    assert "party" in r["answer"].lower()


def test_chatgpt_surface_registered_in_browser_driver():
    import mag.browser_driver as bd
    cfg = bd.SURFACES.get("chatgpt")
    assert cfg is not None, "chatgpt surface must be registered in browser_driver"
    assert cfg["url"] == "https://chatgpt.com"
    assert cfg["mode"] == "contenteditable"  # ProseMirror box, not a textarea
