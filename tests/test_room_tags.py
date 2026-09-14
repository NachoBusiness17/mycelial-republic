"""Room addressing: to / @mentions / inbox. Dispatch only — no HTTP."""
from __future__ import annotations

import json

from mag import api_gateway as g

HDR = {"X-API-Key": "mag-local-dev-key"}


def _post(body: dict):
    return g.dispatch("POST", "/room", headers=HDR, body=body)


def test_post_to_and_at_mention_reach_inbox(tmp_path, monkeypatch):
    p = tmp_path / "room.jsonl"
    monkeypatch.setattr(g, "_room_path", lambda: p)

    s, out = _post({
        "seat": "grok-a",
        "event": "assign",
        "text": "@codex run python -m mag.fuel_feed status. Do not invent cages.",
        "to": "codex",
    })
    assert s == 200, out
    assert out.get("posted") is True
    assert "codex" in (out.get("to") or [])

    rec = json.loads(p.read_text(encoding="utf-8").splitlines()[-1])
    assert rec["to"] == ["codex"]

    s, inbox = g.dispatch("GET", "/room/inbox/codex", headers=HDR)
    assert s == 200
    assert inbox["count"] == 1
    assert inbox["posts"][0]["seat"] == "grok-a"


def test_grok2_alias_hits_grok_b_inbox(tmp_path, monkeypatch):
    p = tmp_path / "room.jsonl"
    monkeypatch.setattr(g, "_room_path", lambda: p)
    _post({"seat": "grok-a", "event": "assign", "text": "@grok2 LOAD COMPUTE_SCHEDULE"})
    s, inbox = g.dispatch("GET", "/room/inbox/grok-b", headers=HDR)
    assert s == 200
    assert inbox["count"] == 1


def test_reply_to_persists(tmp_path, monkeypatch):
    p = tmp_path / "room.jsonl"
    monkeypatch.setattr(g, "_room_path", lambda: p)
    _post({"seat": "grok-a", "event": "assign", "text": "@codex ping", "to": "codex"})
    parent = json.loads(p.read_text(encoding="utf-8").splitlines()[-1])["ts"]
    s, out = _post({
        "seat": "codex",
        "event": "ack",
        "text": "@grok-a heard. running fuel_feed status.",
        "to": "grok-a",
        "reply_to": parent,
    })
    assert s == 200
    assert out.get("reply_to") == parent
    rec = json.loads(p.read_text(encoding="utf-8").splitlines()[-1])
    assert rec["reply_to"] == parent


def test_untagged_post_stays_out_of_inbox(tmp_path, monkeypatch):
    p = tmp_path / "room.jsonl"
    monkeypatch.setattr(g, "_room_path", lambda: p)
    _post({"seat": "grok", "event": "note", "text": "spilling verbose at nobody"})
    s, inbox = g.dispatch("GET", "/room/inbox/codex", headers=HDR)
    assert s == 200
    assert inbox["count"] == 0
