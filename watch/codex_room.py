#!/usr/bin/env python3
"""codex_room.py — run-once tailer: newest codex CLI session file -> the ROOM.

Operator 08-29: "deepseek chat gpt and all need to be in a chat room verbose
spilling their shit so we can debug them." Grok flows via its hooks (grok_hook);
codex has no hooks, so this tailer reads the newest rollout-*.jsonl under
~/.codex/sessions and appends new message/command records to watch/room.jsonl.

Run-once by design (no daemon, no supervisor — law 11): the cadence (tick,
operator, or zcode) invokes it per beat. Fail-open, offset-file tracked.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
SESSIONS = HOME / ".codex" / "sessions"
AGENT_ROOT = Path(__file__).resolve().parents[1]
ROOM = AGENT_ROOT / "watch" / "room.jsonl"
STATE = AGENT_ROOT / "watch" / ".codex_room_state.json"


def newest_session() -> Path | None:
    if not SESSIONS.exists():
        return None
    files = [p for p in SESSIONS.rglob("*.jsonl") if p.is_file()]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def _looks_like_ts(s: str) -> bool:
    return len(s) <= 32 and s[:4].isdigit() and "T" in s and (":" in s or "Z" in s)


def _text_from(obj: dict, depth: int = 0) -> str | None:
    """Pull the first useful text out of a codex rollout record."""
    if depth > 4:
        return None
    if isinstance(obj, str):
        return None if _looks_like_ts(obj) else obj[:400]
    if isinstance(obj, dict):
        for key in ("payload", "text", "command", "output", "arguments", "content", "message"):
            if key in obj:
                got = _text_from(obj[key], depth + 1)
                if got:
                    return got
        for val in obj.values():
            got = _text_from(val, depth + 1)
            if got:
                return got
    if isinstance(obj, list):
        for item in obj:
            got = _text_from(item, depth + 1)
            if got:
                return got
    return None


def main() -> int:
    session = newest_session()
    if not session:
        return 0
    state = {}
    if STATE.exists():
        try:
            state = json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — corrupt state = re-read tail
            state = {}
    try:
        lines = session.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return 0
    key = str(session)
    start = int(state.get(key, max(0, len(lines) - 50)))  # first run: last 50 only
    new = []
    for line in lines[start:]:
        if not line.strip():
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        text = _text_from(rec)
        if not text:
            continue
        rtype = rec.get("type") or rec.get("record_type") or "event"
        new.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "seat": "codex",
            "event": str(rtype)[:60],
            "session": session.stem[:40],
            "text": text[:500],
        })
    if new:
        with ROOM.open("a", encoding="utf-8") as f:
            for r in new:
                f.write(json.dumps(r, default=str) + "\n")
    state[key] = len(lines)
    for old in [k for k in state if k != key]:
        del state[old]  # only track the live session
    STATE.write_text(json.dumps(state), encoding="utf-8")
    print(json.dumps({"posted": len(new), "session": session.name[:50]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
