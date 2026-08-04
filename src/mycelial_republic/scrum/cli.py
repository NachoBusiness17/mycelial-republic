"""mycelia scrum subcommands."""
from __future__ import annotations

import argparse
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from . import store


def add_scrum_parser(sub: argparse._SubParsersAction) -> None:
    p = sub.add_parser("scrum", help="Agent/project scrum board (plan, pull, standup, done)")
    sp = p.add_subparsers(dest="scrum_cmd", required=True)

    sp.add_parser("status", help="Show sprint board + gates")

    p_plan = sp.add_parser("plan", help="Open/refresh sprint (set knot + ready set)")
    p_plan.add_argument("--knot", required=True, help="Knot this sprint strikes")
    p_plan.add_argument("--goal", default="", help="Sprint goal one-liner")
    p_plan.add_argument("--days", type=int, default=7)
    p_plan.add_argument(
        "--ready",
        default="",
        help="Comma ticket ids to mark ready (optional)",
    )

    p_pull = sp.add_parser("pull", help="Claim ticket → doing")
    p_pull.add_argument("ticket_id")
    p_pull.add_argument("--role", required=True)
    p_pull.add_argument("--who", default="", help="Assignee name (default role)")

    p_done = sp.add_parser("done", help="Mark ticket done with evidence")
    p_done.add_argument("ticket_id")
    p_done.add_argument("--evidence", required=True, help="Path or proof string")
    p_done.add_argument("--who", default="")

    p_block = sp.add_parser("block", help="Mark ticket blocked")
    p_block.add_argument("ticket_id")
    p_block.add_argument("--reason", required=True)

    p_ready = sp.add_parser("ready", help="Move ticket backlog → ready")
    p_ready.add_argument("ticket_id")

    p_st = sp.add_parser("standup", help="Append daily standup line")
    p_st.add_argument("--who", required=True)
    p_st.add_argument("--did", default="")
    p_st.add_argument("--doing", default="")
    p_st.add_argument("--block", default="")

    p_retro = sp.add_parser("retro", help="Scaffold retro file")
    p_retro.add_argument("--loops", default="")
    p_retro.add_argument("--keep", default="")
    p_retro.add_argument("--change", default="")

    sp.add_parser("sync-yaml", help="Re-import backlog.yaml if PyYAML available")


def run_scrum(args: argparse.Namespace) -> int:
    cmd = args.scrum_cmd
    if cmd == "status":
        return cmd_status()
    if cmd == "plan":
        return cmd_plan(args.knot, args.goal, args.days, args.ready)
    if cmd == "pull":
        return cmd_pull(args.ticket_id, args.role, args.who or args.role)
    if cmd == "done":
        return cmd_done(args.ticket_id, args.evidence, args.who)
    if cmd == "block":
        return cmd_block(args.ticket_id, args.reason)
    if cmd == "ready":
        return cmd_ready(args.ticket_id)
    if cmd == "standup":
        store.append_standup(args.who, args.did, args.doing, args.block)
        print(f"standup appended → {store.STANDUP_MD}")
        return 0
    if cmd == "retro":
        return cmd_retro(args.loops, args.keep, args.change)
    if cmd == "sync-yaml":
        return cmd_sync_yaml()
    print("unknown scrum cmd")
    return 2


def cmd_status() -> int:
    data = store.load_backlog()
    board = store.render_board(data)
    print(board)
    print("---")
    print(f"backlog: {store.BACKLOG_JSON}")
    print(f"raw_empty: {store.raw_empty()}")
    doing = [t["id"] for t in data.get("tickets") or [] if t.get("status") == "doing"]
    blocked = [t["id"] for t in data.get("tickets") or [] if t.get("status") == "blocked"]
    print(f"doing: {doing or '—'}")
    print(f"blocked: {blocked or '—'}")
    return 0


def cmd_plan(knot: str, goal: str, days: int, ready: str) -> int:
    store.ensure_dirs()
    data = store.load_backlog()
    end = (date.today() + timedelta(days=days)).isoformat()
    meta = {
        "knot": knot,
        "goal": goal or knot,
        "start_date": date.today().isoformat(),
        "end_date": end,
        "planned_at": datetime.now(timezone.utc).isoformat(),
    }
    store.META_JSON.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    if ready.strip():
        for tid in [x.strip() for x in ready.split(",") if x.strip()]:
            t = store.get_ticket(data, tid)
            if not t:
                print(f"warn: missing {tid}")
                continue
            if t.get("status") in {"done"}:
                continue
            ok, miss = store.deps_satisfied(data, t)
            if not ok:
                print(f"warn: {tid} deps not done: {miss} — left as backlog")
                continue
            gate_ok, reason = store.gate_check(t)
            if not gate_ok and t.get("status") != "ready":
                t["status"] = "blocked"
                t["blocked_reason"] = reason
                print(f"blocked {tid}: {reason}")
            else:
                t["status"] = "ready"
                t.pop("blocked_reason", None)
                print(f"ready {tid}")
    # default: promote P0 with deps met that aren't done
    store.save_backlog(data)
    if not store.STANDUP_MD.is_file():
        store.STANDUP_MD.write_text("# Standup log\n\n", encoding="utf-8")
    print(f"Sprint planned. knot={knot!r} end={end}")
    print(store.render_board(data))
    return 0


def cmd_pull(tid: str, role: str, who: str) -> int:
    data = store.load_backlog()
    t = store.get_ticket(data, tid)
    if not t:
        print(f"unknown ticket {tid}")
        return 1
    ok, miss = store.deps_satisfied(data, t)
    if not ok:
        print(f"deps not satisfied: {miss}")
        return 1
    gate_ok, reason = store.gate_check({**t, "status": "doing"})
    # W0.0 PO work always ok
    if not gate_ok and tid != "W0.0":
        t["status"] = "blocked"
        t["blocked_reason"] = reason
        store.save_backlog(data)
        print(f"cannot pull: {reason}")
        return 1
    # WIP
    limit = (data.get("sprint_defaults") or {}).get("wip_per_role", 2)
    doing_n = sum(
        1
        for x in data.get("tickets") or []
        if x.get("status") == "doing" and x.get("role") == role
    )
    if doing_n >= limit and t.get("priority") != "P0":
        print(f"WIP limit {limit} for role {role} (use P0 to override manually in board)")
        return 1
    if t.get("role") and t.get("role") != role and role not in {"KERNEL", "PO"}:
        print(f"role mismatch: ticket wants {t.get('role')}, you claimed {role}")
        return 1
    t["status"] = "doing"
    t["assignee"] = who
    t.pop("blocked_reason", None)
    store.save_backlog(data)
    store.append_standup(who, did="", doing=f"pulled {tid}", block="")
    print(f"pulled {tid} → doing (assignee={who})")
    return 0


def cmd_done(tid: str, evidence: str, who: str) -> int:
    data = store.load_backlog()
    t = store.get_ticket(data, tid)
    if not t:
        print(f"unknown ticket {tid}")
        return 1
    if not evidence.strip():
        print("evidence required")
        return 1
    t["status"] = "done"
    t["evidence"] = evidence.strip()
    t["done_at"] = datetime.now(timezone.utc).isoformat()
    if who:
        t["assignee"] = who
    t.pop("blocked_reason", None)
    store.save_backlog(data)
    store.append_standup(who or t.get("assignee") or "agent", did=f"done {tid} ({evidence})", doing="", block="")
    print(f"done {tid}")
    print(f"  evidence: {evidence}")
    print("  If milestone-gated, update docs/MILESTONES.md with this evidence path.")
    return 0


def cmd_block(tid: str, reason: str) -> int:
    data = store.load_backlog()
    t = store.get_ticket(data, tid)
    if not t:
        print(f"unknown ticket {tid}")
        return 1
    t["status"] = "blocked"
    t["blocked_reason"] = reason
    store.save_backlog(data)
    print(f"blocked {tid}: {reason}")
    return 0


def cmd_ready(tid: str) -> int:
    data = store.load_backlog()
    t = store.get_ticket(data, tid)
    if not t:
        print(f"unknown ticket {tid}")
        return 1
    ok, miss = store.deps_satisfied(data, t)
    if not ok:
        print(f"deps not satisfied: {miss}")
        return 1
    t["status"] = "ready"
    t.pop("blocked_reason", None)
    store.save_backlog(data)
    print(f"ready {tid}")
    return 0


def cmd_retro(loops: str, keep: str, change: str) -> int:
    store.ensure_dirs()
    body = f"""# Sprint retro

- **when:** {datetime.now(timezone.utc).isoformat()}

## Loops that appeared

{loops or "_fill in_"}

## Keep

{keep or "_fill in_"}

## Change (1–3 process moves)

{change or "_fill in_"}

## Capture risks this sprint

- 

## Chord?

- [ ] Major deliverable had chord strike in logs/chord_strikes/
"""
    store.RETRO_MD.write_text(body, encoding="utf-8")
    print(f"retro scaffold → {store.RETRO_MD}")
    return 0


def cmd_sync_yaml() -> int:
    if not store.BACKLOG_YAML.is_file():
        print("no backlog.yaml")
        return 1
    data = store._try_yaml_load(store.BACKLOG_YAML.read_text(encoding="utf-8"))
    if not data:
        print("PyYAML missing or parse failed. pip install pyyaml")
        return 1
    store.save_backlog(data)
    print("synced yaml → json + board")
    return 0
