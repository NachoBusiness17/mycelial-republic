#!/usr/bin/env python3
"""deepseek_room.py — run-once tailer: DeepSeek VS Code seat -> the ROOM.

Modeled on watch/codex_room.py (offset file, ISO-ts skip, 50-line first-run cap,
fail-open, exit 0 always). Posts seat=deepseek, no thread (main room).

Discovery (read-only, 2026-08-29):
  vizards.deepseek-v4-for-copilot is a Copilot languageModelChatProvider.
  It does NOT keep its own chat store. Request dumps
  (%APPDATA%/Code/User/globalStorage/vizards.deepseek-v4-for-copilot/request-dumps)
  only appear when debugMode=verbose and were ABSENT at bind (debugMode=minimal).
  storage.json had no vizards/deepseek keys.
  Best live trails:
    1. request-dumps jsonl/json (preferred if they appear)
    2. Copilot chatSessions jsonl with vendor/model deepseek
       (%APPDATA%/Code/User/workspaceStorage/*/chatSessions/*.jsonl)
    3. OutputChannel log DeepSeek.log under Code/logs (sparse: activation + tokens)

--source notes which trail was used (auto | request-dumps | chat-sessions | vscode-log).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

AGENT_ROOT = Path(__file__).resolve().parents[1]
ROOM = AGENT_ROOT / "watch" / "room.jsonl"
STATE = AGENT_ROOT / "watch" / ".deepseek_room_state.json"

APPDATA = Path(os.environ["APPDATA"]) if os.environ.get("APPDATA") else Path.home() / "AppData" / "Roaming"
CODE_USER = APPDATA / "Code" / "User"
DUMPS = CODE_USER / "globalStorage" / "vizards.deepseek-v4-for-copilot" / "request-dumps"
DUMPS_TMP = Path(os.environ.get("TEMP") or Path.home() / "AppData" / "Local" / "Temp") / "deepseek-request-dumps"
WORKSPACE = CODE_USER / "workspaceStorage"
EMPTY_CHATS = CODE_USER / "globalStorage" / "emptyWindowChatSessions"
LOGS = APPDATA / "Code" / "logs"

SOURCES = ("auto", "request-dumps", "chat-sessions", "vscode-log")


def _looks_like_ts(s: str) -> bool:
    return len(s) <= 32 and s[:4].isdigit() and "T" in s and (":" in s or "Z" in s)


def _text_from(obj: object, depth: int = 0) -> str | None:
    """Pull the first useful text out of a dump/session record (codex_room pattern)."""
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


def _is_deepseek_blob(s: str) -> bool:
    low = s.lower()
    return "deepseek" in low or '"vendor": "deepseek"' in low or "vizards.deepseek" in low


def _is_deepseek_session(path: Path) -> bool:
    try:
        with path.open(encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                if i >= 24:
                    break
                if _is_deepseek_blob(line):
                    return True
    except OSError:
        return False
    return False


def newest_dumps() -> Path | None:
    files: list[Path] = []
    for root in (DUMPS, DUMPS_TMP):
        if not root.exists():
            continue
        files.extend(p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".jsonl", ".json", ".txt"})
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def newest_chat_session() -> Path | None:
    files: list[Path] = []
    if WORKSPACE.exists():
        files.extend(
            p for p in WORKSPACE.rglob("*.jsonl")
            if p.is_file() and "chatSessions" in p.parts
        )
    if EMPTY_CHATS.exists():
        files.extend(p for p in EMPTY_CHATS.glob("*.jsonl") if p.is_file())
    ds = [p for p in files if _is_deepseek_session(p)]
    return max(ds, key=lambda p: p.stat().st_mtime) if ds else None


def newest_log() -> Path | None:
    if not LOGS.exists():
        return None
    files = [p for p in LOGS.rglob("DeepSeek.log") if p.is_file()]
    return max(files, key=lambda p: p.stat().st_mtime) if files else None


def pick_source(requested: str) -> tuple[str, Path | None]:
    if requested == "request-dumps":
        return "request-dumps", newest_dumps()
    if requested == "chat-sessions":
        return "chat-sessions", newest_chat_session()
    if requested == "vscode-log":
        return "vscode-log", newest_log()
    dumps = newest_dumps()
    if dumps:
        return "request-dumps", dumps
    chats = newest_chat_session()
    if chats:
        return "chat-sessions", chats
    return "vscode-log", newest_log()


def _from_log_line(line: str) -> tuple[str, str] | None:
    """VS Code OutputChannel line: '2026-08-28 21:08:24.192 [info] message'."""
    rb = line.find(" [")
    re_ = line.find("] ", rb) if rb >= 0 else -1
    if rb >= 0 and re_ > rb:
        level = line[rb + 2 : re_].strip() or "event"
        rest = line[re_ + 2 :].strip()
        if rest:
            return level[:60], rest[:500]
        return None
    text = line.strip()
    if not text or _looks_like_ts(text):
        return None
    return "event", text[:500]


def _event_and_text(line: str, source: str) -> tuple[str, str] | None:
    if not line.strip():
        return None
    if source == "vscode-log":
        return _from_log_line(line)
    try:
        rec = json.loads(line)
    except json.JSONDecodeError:
        return _from_log_line(line)
    if not isinstance(rec, dict):
        text = _text_from(rec)
        return ("event", text[:500]) if text else None
    text = _text_from(rec)
    if not text:
        return None
    rtype = rec.get("type") or rec.get("record_type") or rec.get("kind") or rec.get("event") or "event"
    return str(rtype)[:60], text[:500]


def _run(argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(description="Tail DeepSeek VS Code seat into watch/room.jsonl")
    parser.add_argument(
        "--source",
        choices=SOURCES,
        default="auto",
        help="trail to tail (auto: dumps if present, else deepseek chatSessions, else DeepSeek.log)",
    )
    args = parser.parse_args(argv)
    source, session = pick_source(args.source)
    if not session:
        print(json.dumps({
            "posted": 0,
            "session": None,
            "source": source,
            "note": "no file trail for this source (dumps absent; debugMode=minimal)",
        }))
        return 0
    state: dict = {}
    if STATE.exists():
        try:
            state = json.loads(STATE.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — corrupt state = re-read tail
            state = {}
    try:
        lines = session.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        print(json.dumps({"posted": 0, "session": session.name[:50], "source": source}))
        return 0
    key = str(session)
    start = int(state.get(key, max(0, len(lines) - 50)))  # first run: last 50 only
    new = []
    for line in lines[start:]:
        parsed = _event_and_text(line, source)
        if not parsed:
            continue
        rtype, text = parsed
        new.append({
            "ts": datetime.now(timezone.utc).isoformat(),
            "seat": "deepseek",
            "event": rtype,
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
    print(json.dumps({
        "posted": len(new),
        "session": session.name[:50],
        "source": source,
    }))
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return _run(argv)
    except Exception:  # noqa: BLE001 — fail-open
        return 0


if __name__ == "__main__":
    sys.exit(main())
