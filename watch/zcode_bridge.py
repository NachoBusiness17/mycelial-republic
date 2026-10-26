"""ZCode seat bridge — task the ZCode (Z.ai) collaborator like any other seat.

ZCode is a desktop agent, not an API loop: it can't be spawned headless by the
orchestrator. So this bridge uses the mailbox pattern instead:

  task "goal"   -> register_external(seat="zcode") + write goal to INBOX/<id>.md
  list          -> show inbox + registered zcode tasks
  beat <id>     -> touch_external heartbeat (seat still alive)
  done <id> --detail "..."  -> finalize_external(status="done", detail=...)

The human operator (or a watcher loop) opens ZCode in the repo root and asks it
to work the inbox; ZCode reads INBOX/*.md as data, does the work with its own
tools, then the operator runs `done`. Nothing ZCode writes is ever executed by
the bridge — results are markdown, posted back through finalize_external only.

CLI:
  python watch/zcode_bridge.py task "audit llm.py prefix stability"
  python watch/zcode_bridge.py list
  python watch/zcode_bridge.py beat <task_id>
  python watch/zcode_bridge.py done <task_id> --detail "wrote report to ..."
"""
from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SEAT = "zcode"
INBOX = ROOT / "queue" / "handoff" / "zcode" / "INBOX"
OUTBOX = ROOT / "queue" / "handoff" / "zcode" / "OUTBOX"
CONVO = ROOT / "queue" / "handoff" / "zcode" / "CONVO.md"  # direct seat-to-seat thread (2026-08-25)


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

    task = register_external(goal=goal, seat=SEAT, tag=tag or "zcode-seat")
    p = _write_inbox(task)
    print(f"queued {task['task_id']} -> {p.relative_to(ROOT)}")
    return 0


def cmd_list() -> int:
    from mag.orchestrator import list_external_tasks

    rows = [t for t in list_external_tasks(limit=100) if t.get("seat") == SEAT]
    print(f"{len(rows)} zcode task(s)")
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
    """Append a turn to the shared CONVO thread. Direct seat-to-seat talk —
    the operator is NOT the bus: both seats read/write this one file."""
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
    ap = argparse.ArgumentParser(prog="zcode-bridge", description="Task the ZCode seat via mailbox")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("task", help="queue a goal for the zcode seat")
    p.add_argument("goal")
    p.add_argument("--tag", default="")

    sub.add_parser("list", help="list zcode tasks + inbox")

    p = sub.add_parser("beat", help="heartbeat a running task")
    p.add_argument("task_id")

    p = sub.add_parser("done", help="finalize a task")
    p.add_argument("task_id")
    p.add_argument("--detail", default="")
    p.add_argument("--status", default="done", choices=["done", "failed", "cancelled"])

    p = sub.add_parser("chat", help="talk directly (append a turn to CONVO.md); --read dumps it")
    p.add_argument("text", nargs="?", default="")
    p.add_argument("--read", action="store_true", help="print the whole thread")

    args = ap.parse_args(argv)
    t0 = time.time()
    try:
        if args.cmd == "task":
            rc = cmd_task(args.goal, args.tag)
        elif args.cmd == "list":
            rc = cmd_list()
        elif args.cmd == "beat":
            rc = cmd_beat(args.task_id)
        elif args.cmd == "chat":
            rc = cmd_chat_read() if args.read else cmd_chat(args.text)
        else:
            rc = cmd_done(args.task_id, args.detail, args.status)
    except Exception as e:  # noqa: BLE001 - CLI boundary
        print(f"[error] {e}", file=sys.stderr)
        return 1
    print(f"[{time.time() - t0:.1f}s]", file=sys.stderr)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
