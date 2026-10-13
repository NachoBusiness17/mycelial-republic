"""Sense tools for MCP — voice packets + image-whisper scan for dumb bodies.

Operator 2026-08-28: MCP is the bus; voice/image are realtime coordinates.
The 8B/VL never gets the stream — they get these tool results. Same args =
same gps.key (cache coordinate). A miss is a new frame.

Schema: mag_sense_mcp.v1
"""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

SCHEMA = "mag_sense_mcp.v1"


def gps_key(tool: str, args: dict[str, Any]) -> dict[str, Any]:
    """Canonical MCP cache coordinate: tool + sorted args → sha256[:16]."""
    blob = json.dumps({"tool": tool, "args": args}, sort_keys=True, ensure_ascii=False, default=str)
    return {
        "tool": tool,
        "key": hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16],
        "ts": datetime.now(timezone.utc).isoformat(),
    }


def voice_turn(text: str, session_id: str = "") -> dict[str, Any]:
    """STT packet → Mag voice janitor. Dumb body never hears audio — only this text."""
    text = (text or "").strip()
    sid = (session_id or "").strip()
    gps = gps_key("voice_turn", {"text": text, "session_id": sid})
    if not text:
        return {"ok": False, "schema": SCHEMA, "error": "empty transcript — pass text", "gps": gps}
    from mag.voice_turn import handle_voice_turn

    out = handle_voice_turn({"text": text, "session_id": sid})
    if not isinstance(out, dict):
        out = {"ok": False, "raw": str(out)[:400]}
    out["schema"] = out.get("schema") or SCHEMA
    out["gps"] = gps
    return out


def whisper_decode(path: str, secret: str = "") -> dict[str, Any]:
    """Scan a PNG's LSBs for a whisper payload. $0 numpy — no VL required to recover bytes."""
    path = (path or "").strip()
    secret = secret or ""
    gps = gps_key("whisper_decode", {"path": path, "secret": secret})
    if not path:
        return {"ok": False, "schema": SCHEMA, "error": "path required", "gps": gps}
    from mag.whisper_image import decode_image

    out = decode_image(path, secret=secret)
    if not isinstance(out, dict):
        out = {"ok": False, "raw": str(out)[:400]}
    out["schema"] = out.get("schema") or SCHEMA
    out["gps"] = gps
    return out
