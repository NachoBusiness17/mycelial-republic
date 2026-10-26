"""ghost_voice_ops steer -> room row delivery (2026-10-23). No model call, no live room write."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
import ghost_voice_ops as g  # noqa: E402
from mag import grok_steer as gs  # noqa: E402


def test_steer_appends_one_room_row(tmp_path, monkeypatch, capsys):
    room = tmp_path / "room.jsonl"
    monkeypatch.setattr(g, "ROOM", room)
    monkeypatch.setattr(gs, "decide_steer", lambda line: {"steer": "name the real constraint", "channel": "stub"})
    assert g.main(["steer", "hermes", "add a fallback retry", "--allow-paid"]) == 0
    rows = [json.loads(x) for x in room.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1 and rows[0]["kind"] == "steer" and rows[0]["to"] == "hermes"
    assert rows[0]["detail"] == "name the real constraint"
    assert "Delivered" in capsys.readouterr().out


def test_no_deliver_and_no_paid_write_nothing(tmp_path, monkeypatch):
    room = tmp_path / "room.jsonl"
    monkeypatch.setattr(g, "ROOM", room)
    monkeypatch.setattr(gs, "decide_steer", lambda line: {"steer": "x", "channel": "stub"})
    assert g.main(["steer", "hermes", "add a fallback retry", "--allow-paid", "--no-deliver"]) == 0
    assert g.main(["steer", "hermes", "add a fallback retry"]) == 0  # gate only, no paid call
    assert not room.exists()