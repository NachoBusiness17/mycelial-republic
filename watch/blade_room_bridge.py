#!/usr/bin/env python3
"""Run-once bridge for blade lifecycle logs into the blades room thread."""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ROOM = ROOT / "watch" / "room.jsonl"
STATE = ROOT / "watch" / ".blade_room_bridge_state.json"
SOURCES = (ROOT / "state" / "vast" / "blade_buyer.log",
           ROOT / "state" / "vast" / "boot_watch.log")

_EVENTS = (
    ("contract_signed", re.compile(r"blade contract|contract signed", re.I)),
    ("gate_passed", re.compile(r"gate passed", re.I)),
    ("proxy_dark", re.compile(r"proxy-dark", re.I)),
    ("ready", re.compile(r"phase:\s*[^-]+->\s*ready|\bREADY\b", re.I)),
    ("reap", re.compile(r"reap|lifetime cap|destroying", re.I)),
)


def _event(line: str) -> str | None:
    return next((name for name, pattern in _EVENTS if pattern.search(line)), None)


def run() -> int:
    try:
        state = json.loads(STATE.read_text(encoding="utf-8")) if STATE.exists() else {}
    except (OSError, json.JSONDecodeError):
        state = {}
    posts: list[dict] = []
    next_state: dict[str, int] = {}
    for source in SOURCES:
        key = str(source)
        try:
            lines = source.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            next_state[key] = 0
            continue
        start = max(0, int(state.get(key, 0)))
        for line in lines[start:]:
            event = _event(line)
            if event:
                posts.append({"ts": datetime.now(timezone.utc).isoformat(),
                              "seat": "blade_buyer", "thread": "blades",
                              "event": event, "source": source.name,
                              "text": line[:1000]})
        next_state[key] = len(lines)
    if posts:
        with ROOM.open("a", encoding="utf-8") as handle:
            for post in posts:
                handle.write(json.dumps(post) + "\n")
    STATE.write_text(json.dumps(next_state, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"posted": len(posts), "thread": "blades"}))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(run())
    except Exception:  # fail-open: a room bridge cannot stop lifecycle work
        raise SystemExit(0)
