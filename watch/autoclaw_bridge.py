"""AutoClaw seat bridge — task the AutoClaw (z.ai desktop agent) like any other seat.

Mirrors watch/zcode_bridge.py. AutoClaw is a desktop agent (OpenClaw kernel, z.ai);
it reads INBOX files as DATA, works with its own tools (skills, browser, IM), and
posts results back through finalize_external. Direct seat-to-seat talk lives in
CONVO.md — the operator is not the bus.

  python watch/autoclaw_bridge.py task "goal"              # queue a goal
  python watch/autoclaw_bridge.py list                      # tasks + inbox
  python watch/autoclaw_bridge.py beat <task_id>            # heartbeat
  python watch/autoclaw_bridge.py done <task_id> --detail   # close the loop
  python watch/autoclaw_bridge.py chat "turn" / --read      # direct thread
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SEAT = "autoclaw"
INBOX = ROOT / "queue" / "handoff" / "autoclaw" / "INBOX"
OUTBOX = ROOT / "queue" / "handoff" / "autoclaw" / "OUTBOX"
CONVO = ROOT / "queue" / "handoff" / "autoclaw" / "CONVO.md"


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _write_inbox(task: dict) -> Path:
    INBOX.mkdir(parents=True, exist_ok=True)
    p = INBOX / f"{task['task_id']}.md"
    p.write_text(
        f"# Task {task['task_id']}\n\n"
        f"- queued: {_utc()}\n"
        f"- seat: {SEAT}\n"
        f"- status: {task.get('status')}\n\n"
        f"## Goal\n\n{task['goal']}\n",
        encoding="utf-8",
    )
    return p


def cmd_task(goal: str, tag: str) -> int:
    from mag.orchestrator import register_external

    task = register_external(goal=goal, seat=SEAT, tag=tag or "autoclaw-seat")
    p = _write_inbox(task)
    print(f"queued {task['task_id']} -> {p.relative_to(ROOT)}")
    return 0


def cmd_list() -> int:
    from mag.orchestrator import list_external_tasks

    rows = [t for t in list_external_tasks(limit=100) if t.get("seat") == SEAT]
    print(f"{len(rows)} autoclaw task(s)")
    for t in rows:
        print(f"  {t['task_id']}  {t.get('status','?'):8}  {t.get('goal','')[:80]}")
    if INBOX.is_dir():
        pending = sorted(INBOX.glob("*.md"))
        print(f"inbox: {len(pending)} file(s)")
        for p in pending:
            print(f"  {p.name}")
    return 0


def cmd_beat(task_id: str) -> int:
    from mag.orchestrator import touch_external

    t = touch_external(task_id, note=f"{SEAT} alive {_utc()}")
    print("ok" if t else f"no such task {task_id}")
    return 0 if t else 1


def cmd_done(task_id: str, detail: str, status: str) -> int:
    from mag.orchestrator import finalize_external

    out = None
    if detail:
        OUTBOX.mkdir(parents=True, exist_ok=True)
        out = OUTBOX / f"{task_id}.md"
        out.write_text(f"# Result {task_id}\n\n- closed: {_utc()}\n\n{detail}\n", encoding="utf-8")
    inbox_file = INBOX / f"{task_id}.md"
    if inbox_file.is_file():
        inbox_file.unlink()
    t = finalize_external(task_id, status=status, detail=detail[:400] or f"{SEAT} closed")
    print(f"{status}: {task_id}" + (f" -> {out.relative_to(ROOT)}" if out else ""))
    return 0 if t else 1


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
    ap = argparse.ArgumentParser(prog="autoclaw-bridge", description="Task the AutoClaw seat via mailbox")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("task", help="queue a goal for the autoclaw seat")
    p.add_argument("goal")
    p.add_argument("--tag", default="")

    sub.add_parser("list", help="list autoclaw tasks + inbox")

    p = sub.add_parser("beat", help="heartbeat a running task")
    p.add_argument("task_id")

    p = sub.add_parser("done", help="finalize a task")
    p.add_argument("task_id")
    p.add_argument("--detail", default="")
    p.add_argument("--status", default="done", choices=["done", "failed", "cancelled"])

    p = sub.add_parser("chat", help="talk directly (append a turn to CONVO.md); --read dumps it")
    p.add_argument("text", nargs="?", default="")
    p.add_argument("--read", action="store_true")

    args = ap.parse_args(argv)
    if args.cmd == "task":
        return cmd_task(args.goal, args.tag)
    elif args.cmd == "list":
        return cmd_list()
    elif args.cmd == "beat":
        return cmd_beat(args.task_id)
    elif args.cmd == "chat":
        return cmd_chat_read() if args.read else cmd_chat(args.text)
    return cmd_done(args.task_id, args.detail, args.status)


if __name__ == "__main__":
    raise SystemExit(main())
