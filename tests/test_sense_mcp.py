"""MCP sense tools: declared args, GPS key stability, whisper roundtrip."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.mcp_server import tools_manifest
from mag.whisper_image import encode_image
from tools import dispatch, sense_tools


def test_mcp_manifest_declares_sense_args() -> None:
    names = {t["name"]: t for t in tools_manifest()}
    assert "voice_turn" in names
    assert "whisper_decode" in names
    vt = names["voice_turn"]["inputSchema"]["properties"]
    assert "text" in vt
    wd = names["whisper_decode"]["inputSchema"]["properties"]
    assert "path" in wd
    assert "text" in (names["voice_turn"]["inputSchema"].get("required") or [])


def test_gps_key_stable_for_same_args() -> None:
    a = sense_tools.gps_key("voice_turn", {"text": "hello", "session_id": "s1"})
    b = sense_tools.gps_key("voice_turn", {"text": "hello", "session_id": "s1"})
    c = sense_tools.gps_key("voice_turn", {"text": "hello!", "session_id": "s1"})
    assert a["key"] == b["key"]
    assert a["key"] != c["key"]


def test_whisper_decode_roundtrip() -> None:
    out_dir = ROOT / "memory" / "runs" / "sense_gps"
    out_dir.mkdir(parents=True, exist_ok=True)
    png = out_dir / "test_carrier.png"
    enc = encode_image("gps-home", secret="k", out=str(png), w=64, h=64)
    assert enc.get("ok"), enc
    r = dispatch("whisper_decode", {"path": str(png), "secret": "k"})
    assert r.get("ok"), r
    assert r.get("payload") == "gps-home"
    assert r.get("gps", {}).get("key")
    miss = dispatch("whisper_decode", {"path": str(png), "secret": "wrong"})
    assert miss.get("gps", {}).get("key") != r["gps"]["key"]


def test_voice_turn_empty_is_declared_error() -> None:
    r = dispatch("voice_turn", {"text": ""})
    assert r.get("ok") is False
    assert "empty" in str(r.get("error") or "").lower()
    assert r.get("gps", {}).get("tool") == "voice_turn"
