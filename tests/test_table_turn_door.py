"""Regression: the table door (channel=table) must resolve mag.table_turn.

mag/table_turn.py was swept into attic/kill_list_20260908/ by a basename string
scan that missed lazy dotted imports. Live callers: backend/server.py
(POST /api/v1/voice/turn), mag/voice_turn.py (channel == "table", which is what
dashboard/static/wave.html sends), and mag/table_turn_cli.py.
These tests stub handle() so they never touch campaign state.
"""
from __future__ import annotations

import importlib
import io
import json
import sys


def test_table_turn_module_importable():
    mod = importlib.import_module("mag.table_turn")
    assert callable(mod.handle)
    assert mod.SCHEMA == "mag_table_turn.v1"


def test_table_turn_cli_resolves_handle(monkeypatch, capsys):
    import mag.table_turn as tt
    from mag import table_turn_cli

    seen: dict = {}

    def fake(body):
        seen.update(body)
        return {"ok": True, "route": "table_engine"}

    monkeypatch.setattr(tt, "handle", fake)
    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"text": "look", "session_id": "t"})))
    assert table_turn_cli.main() == 0
    assert json.loads(capsys.readouterr().out)["route"] == "table_engine"
    assert seen["text"] == "look"


def test_voice_turn_table_channel_routes_to_table_door(monkeypatch):
    import mag.table_turn as tt
    from mag.voice_turn import handle_voice_turn

    monkeypatch.setattr(
        tt, "handle", lambda body: {"ok": True, "route": "table_engine", "channel": body.get("channel")}
    )
    out = handle_voice_turn({"text": "look around", "session_id": "pytest-table", "channel": "table"})
    assert out["route"] == "table_engine"
    assert out["channel"] == "table"
