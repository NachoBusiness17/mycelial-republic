"""cache_bridge.py — the cache models as a talking body (2026-08-25).

The fleet's cheap brain: the cache-mined engines —
  rib_cache.rib_chat   = the frozen RIB (system, byte-identical prefix) ~99.67% cache
  glm_flash.cached_chat = the flash engine (frozen self + dynamic tail)   ~99.6% cache
Seats "talk to the cache" by asking here: every ask rides the frozen prefix, returns
the answer AND the cached_tokens so the mining is measurable. Its CONVO records the
thread — the cache has a voice in the mesh.

CLI:
  python watch/cache_bridge.py ask "question"     # frozen RIB answer (cache-mined)
  python watch/cache_bridge.py flash "task"       # flash engine answer
  python watch/cache_bridge.py stats              # cache telemetry
  python watch/cache_bridge.py chat "turn" / --read  # the cache's CONVO thread
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SEAT = "cache"
CONVO = ROOT / "queue" / "handoff" / "cache" / "CONVO.md"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _log_turn(kind: str, task: str, result: dict) -> None:
    CONVO.parent.mkdir(parents=True, exist_ok=True)
    with CONVO.open("a", encoding="utf-8") as fh:
        fh.write(f"\n[{kind} {_utc()}]\nQ: {task}\n"
                 f"A: {str(result.get('text') or '')[:400]}\n"
                 f"cache: {result.get('cached_tokens', 0)}/{result.get('prompt_tokens', 0)} tokens\n")


def cmd_ask(task: str) -> int:
    from mag import rib_cache

    r = rib_cache.rib_chat(task)
    _log_turn("cache", task, r)
    print(json.dumps({k: r.get(k) for k in ("ok", "text", "cached_tokens", "prompt_tokens",
                                            "completion_tokens", "error")},
                     indent=2, ensure_ascii=False)[:900])
    return 0 if r.get("ok") else 1


def cmd_flash(task: str) -> int:
    from mag import glm_flash

    r = glm_flash.cached_chat(task)
    _log_turn("flash", task, r)
    print(json.dumps({k: r.get(k) for k in ("ok", "text", "cached_tokens", "prompt_tokens",
                                            "completion_tokens", "error")},
                     indent=2, ensure_ascii=False)[:900])
    return 0 if r.get("ok") else 1


def cmd_stats() -> int:
    from mag import glm_flash, rib_cache

    out = {"ok": True, "schema": "cache_bridge.v1",
           "rib": rib_cache.status(), "flash": glm_flash.status()}
    print(json.dumps(out, indent=2, default=str))
    return 0


def cmd_chat(text: str) -> int:
    CONVO.parent.mkdir(parents=True, exist_ok=True)
    with CONVO.open("a", encoding="utf-8") as fh:
        fh.write(f"\n[copilot {_utc()}]\n{text}\n")
    print(f"appended -> {CONVO.relative_to(ROOT)}")
    return 0


def cmd_chat_read() -> int:
    if CONVO.is_file():
        print(CONVO.read_text(encoding="utf-8"))
    else:
        print("(empty convo)")
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    ap = argparse.ArgumentParser(prog="cache-bridge", description="talk to the cache models")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("ask", help="ask the frozen RIB (cache-mined)")
    p.add_argument("task", nargs="+")

    p = sub.add_parser("flash", help="ask the flash engine (cache-mined)")
    p.add_argument("task", nargs="+")

    sub.add_parser("stats", help="cache telemetry")

    p = sub.add_parser("chat", help="talk in the cache's CONVO; --read dumps it")
    p.add_argument("text", nargs="?", default="")
    p.add_argument("--read", action="store_true")

    args = ap.parse_args(argv)
    if args.cmd == "ask":
        return cmd_ask(" ".join(args.task))
    elif args.cmd == "flash":
        return cmd_flash(" ".join(args.task))
    elif args.cmd == "stats":
        return cmd_stats()
    elif args.cmd == "chat":
        return cmd_chat_read() if args.read else cmd_chat(args.text)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
