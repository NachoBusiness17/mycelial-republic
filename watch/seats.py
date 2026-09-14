#!/usr/bin/env python3
"""seats.py — the seat registry (2026-08-29): where every agent is.

Fuses REAL signals (no hardcoded guesses):
  - grok seats:  watch/grok_feed.jsonl hook events (per session id) —
                 PostToolUse/UserPromptSubmit recent = WORKING; Stop = IDLE
  - codex:       newest ~/.codex/sessions rollout file mtime — fresh = WORKING
  - zcode:       last room post (watch/room.jsonl)
  - deepseek/JIT lanes: always available (pennies)
Writes watch/seats.json. Run-once, no daemon (board/cadence invokes it).
"""
from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
OUT = ROOT / "watch" / "seats.json"
WORKING_MIN = 20


def _age_min(ts_iso: str) -> float:
    try:
        return (datetime.now(timezone.utc) - datetime.fromisoformat(ts_iso)).total_seconds() / 60
    except (ValueError, TypeError):
        return 9e9


def grok_states() -> dict:
    feed = ROOT / "watch" / "grok_feed.jsonl"
    if not feed.exists():
        return {}
    per_sid: dict[str, dict] = {}
    for line in feed.read_text(encoding="utf-8", errors="replace").splitlines()[-400:]:
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        sid = str(r.get("session_id") or "")[:12]
        if sid:
            per_sid[sid] = r  # last event per session wins
    out = {}
    for i, (sid, r) in enumerate(sorted(per_sid.items(),
                                        key=lambda kv: kv[1].get("ts", ""), reverse=True)[:2]):
        ev = str(r.get("hook_event") or "")
        age = _age_min(r.get("ts"))
        if age > 240:
            state = "silent"
        elif ev in ("PostToolUse", "UserPromptSubmit", "SessionStart") and age < WORKING_MIN:
            state = "working"
        elif ev == "Stop" and age < WORKING_MIN:
            state = "idle"
        else:
            state = "idle" if age < 240 else "silent"
        out[f"grok-{chr(97+i)}"] = {
            "state": state, "last_event": ev,
            "age_min": round(age, 1), "ts": r.get("ts"),
            "last_tool": r.get("tool_name") or "", "session": sid,
        }
    return out


def codex_state() -> dict:
    sessions = HOME / ".codex" / "sessions"
    files = [p for p in sessions.rglob("*.jsonl") if p.is_file()] if sessions.exists() else []
    if not files:
        return {"codex": {"state": "silent", "last_event": "no-sessions", "age_min": 9e9}}
    newest = max(files, key=lambda p: p.stat().st_mtime)
    age = (time.time() - newest.stat().st_mtime) / 60
    return {"codex": {
        "state": "working" if age < WORKING_MIN else ("idle" if age < 240 else "silent"),
        "last_event": "rollout-write", "age_min": round(age, 1),
        "ts": datetime.fromtimestamp(newest.stat().st_mtime, timezone.utc).isoformat(),
        "session": newest.stem[:24],
    }}


def room_state() -> dict:
    room = ROOT / "watch" / "room.jsonl"
    if not room.exists():
        return {}
    last: dict[str, dict] = {}
    for line in room.read_text(encoding="utf-8", errors="replace").splitlines()[-300:]:
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        s = str(r.get("seat") or "")
        if s and not s.startswith(("verifier", "jit")):
            last[s] = r
    out = {}
    for s, r in last.items():
        age = _age_min(r.get("ts"))
        out[s] = {
            "state": "working" if age < WORKING_MIN else ("idle" if age < 240 else "silent"),
            "last_event": r.get("event") or "", "age_min": round(age, 1),
            "ts": r.get("ts"),
        }
    return out


def main() -> int:
    seats = {}
    seats.update(grok_states())
    seats.update(codex_state())
    for s, st in room_state().items():
        if s not in seats:
            seats[s] = st
    seats["deepseek-lanes"] = {"state": "available", "last_event": "always-on (pennies)",
                               "age_min": 0, "ts": datetime.now(timezone.utc).isoformat()}
    doc = {"schema": "seats.v1", "ts": datetime.now(timezone.utc).isoformat(), "seats": seats}
    OUT.write_text(json.dumps(doc, indent=1), encoding="utf-8")
    print(json.dumps({k: v["state"] for k, v in seats.items()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
