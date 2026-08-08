"""Live session-state brief — drop current state into the file chat agents already load.

Closes the "re-teach every session" loop: AGENTS.md tells every chat agent to load
`memory/briefs/latest.md`, but nothing regenerated it at session START (only at
session-END, so it was stale). This module regenerates it with LIVE state so every
new chat window self-briefs: verkle tip, drainer, queue, fleet, pending handoffs,
current goal, open loops.

Schema: session_state_brief.v1

CLI:
  python -m mag.session_state_brief            # write memory/briefs/latest.md (idempotent)
  python -m mag.session_state_brief --json     # print the payload, don't write

Wired into: watch/sancho_boot_hook.py (SessionStart) so every session self-briefs.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from config import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BRIEFS = ROOT / "memory" / "briefs"
LATEST = BRIEFS / "latest.md"
SCHEMA = "session_state_brief.v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def gather_state() -> dict[str, Any]:
    out: dict[str, Any] = {"ts": _now(), "schema": SCHEMA}

    # --- verkle tip ---
    try:
        tip = json.loads(_read(ROOT / "memory" / "biography" / "verkle_tip.json") or "{}")
        out["verkle"] = {
            "root": str(tip.get("root") or "")[:16],
            "n_leaves": tip.get("n_leaves"),
            "last_session_id": tip.get("last_session_id"),
            "last_filename": tip.get("last_filename"),
        }
    except Exception as e:
        out["verkle"] = {"error": str(e)[:120]}

    # --- drainer + operator ---
    try:
        from mag.preferences import drainer_status, operator_status

        d = drainer_status()
        o = operator_status()
        out["drainer"] = {
            "enabled": bool(d.get("enabled")),
            "autorun_allowed": bool(d.get("autorun_allowed")),
            "operator_active": bool(d.get("operator_active")),
        }
        out["operator_active"] = bool(o.get("operator_active"))
    except Exception as e:
        out["drainer"] = {"error": str(e)[:120]}

    # --- queue ---
    try:
        from mag.orchestrator import list_queue, queue_status

        qs = queue_status()
        out["queue"] = {"total": qs.get("total"), "counts": qs.get("counts"), "running_task_id": qs.get("running_task_id")}
        q = list_queue(limit=60)
        out["queue_active"] = [
            {
                "queue_id": i.get("queue_id"),
                "goal": (i.get("goal") or "")[:90],
                "status": i.get("status"),
                "provider": i.get("provider"),
                "tag": i.get("tag"),
            }
            for i in q
            if i.get("status") not in ("done", "failed", "killed", "timeout", "died")
        ]
    except Exception as e:
        out["queue"] = {"error": str(e)[:120]}

    # --- fleet (live) ---
    try:
        from mag.orchestrator import TERMINAL, list_tasks

        tasks = list_tasks(limit=200) or []
        live = []
        for t in tasks:
            if t.get("status") not in TERMINAL:
                live.append({
                    "task_id": t.get("task_id"),
                    "goal": (t.get("goal") or "")[:70],
                    "status": t.get("status"),
                    "provider": t.get("provider"),
                })
        out["fleet_live_n"] = len(live)
        out["fleet_live"] = live[:8]
    except Exception as e:
        out["fleet_live_n"] = 0
        out["fleet_error"] = str(e)[:120]

    # --- pending handoffs ---
    try:
        from mag.peer_handoff import list_peer_handoffs

        ph = list_peer_handoffs(limit=12)
        pending = [h for h in ph if h.get("status") == "filed"]
        out["pending_handoffs_n"] = len(pending)
        out["pending_handoffs"] = [
            {"from": h.get("from_seat"), "to": h.get("to_seat"), "goal": (h.get("goal") or "")[:80]}
            for h in pending
        ]
    except Exception as e:
        out["pending_handoffs_n"] = 0
        out["handoff_error"] = str(e)[:120]

    # --- current goal (CURRENT.md) ---
    current_md = _read(ROOT / "state" / "CURRENT.md")
    goal_m = re.search(r"^## Goal\s*\n+(.*?)\s*\n(?=^## |\Z)", current_md, re.M | re.S)
    status_m = re.search(r"^\*\*status:\*\*\s*(.*)", current_md, re.M)
    out["current_goal"] = (goal_m.group(1).strip()[:200] if goal_m else "") or "(none)"
    out["current_status"] = (status_m.group(1).strip() if status_m else "") or "?"

    # --- open loops (working.md) ---
    wm = _read(ROOT / "memory" / "working.md")
    loops = []
    for line in wm.splitlines():
        s = line.strip()
        if s.startswith("- [ ]") or s.startswith("- [DOING]") or "**DOING**" in s:
            loops.append(re.sub(r"^-\s*\[[^]]*\]\s*", "", s)[:120])
        if len(loops) >= 8:
            break
    out["open_loops"] = loops

    return out


def render_brief(s: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# Session state · {s.get('ts', '')[:19]}Z")
    lines.append("")
    lines.append("_Auto-generated at session start by the overseer (session_state_brief.v1). "
                 "This is the LIVE state — no need to re-teach._")
    lines.append("")

    vk = s.get("verkle") or {}
    if vk.get("root"):
        lines.append(f"- **verkle tip:** `{vk.get('root')}` · {vk.get('n_leaves')} leaves · last session `{vk.get('last_session_id','')[:8]}`")
    else:
        lines.append("- **verkle tip:** (unavailable)")

    d = s.get("drainer") or {}
    q = s.get("queue") or {}
    counts = q.get("counts") or {}
    lines.append(f"- **drainer:** {'ON' if d.get('enabled') else 'OFF'} · {'paused (operator active)' if d.get('operator_active') else 'operator idle'}")
    if counts:
        lines.append(f"- **queue:** " + " · ".join(f"{k}={v}" for k, v in counts.items()))
    lines.append(f"- **fleet live:** {s.get('fleet_live_n', 0)}")
    lines.append(f"- **pending handoffs:** {s.get('pending_handoffs_n', 0)}")
    lines.append(f"- **status:** {s.get('current_status', '?')} · **current goal:** {s.get('current_goal', '')}")

    lines.append("")
    lines.append("## In-flight / queued")
    active = s.get("queue_active") or []
    if active:
        for i in active[:10]:
            lines.append(f"- [{i.get('status','?')}] {i.get('goal')} ({i.get('provider')})")
        if len(active) > 10:
            lines.append(f"- … +{len(active)-10} more")
    else:
        lines.append("- (queue empty)")

    if s.get("pending_handoffs"):
        lines.append("")
        lines.append("## Pending handoffs")
        for h in s.get("pending_handoffs")[:8]:
            lines.append(f"- {h.get('from')} → {h.get('to')}: {h.get('goal')}")

    if s.get("open_loops"):
        lines.append("")
        lines.append("## Open loops")
        for l in s.get("open_loops"):
            lines.append(f"- {l}")

    lines.append("")
    lines.append("---")
    lines.append("_Regenerate: `python -m mag.session_state_brief`. Next step: load context-pack, "
                 "read CURRENT.md, and continue from the current goal / in-flight work._")
    return "\n".join(lines)


def write_brief(s: dict[str, Any] | None = None) -> dict[str, Any]:
    s = s or gather_state()
    text = render_brief(s)
    BRIEFS.mkdir(parents=True, exist_ok=True)
    LATEST.write_text(text, encoding="utf-8")
    return {"ok": True, "schema": SCHEMA, "path": str(LATEST), "ts": s.get("ts"), "state": s}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="session-state-brief", description="Write live session state to memory/briefs/latest.md")
    ap.add_argument("--json", action="store_true", help="Print payload, don't write")
    ap.add_argument("--dry", action="store_true", help="Print the rendered brief, don't write")
    args = ap.parse_args(argv)
    s = gather_state()
    if args.json:
        print(json.dumps(s, indent=2, default=str))
        return 0
    if args.dry:
        print(render_brief(s))
        return 0
    res = write_brief(s)
    print(f"[session-state-brief] wrote {res.get('path')} · drainer={s.get('drainer',{}).get('enabled')} · queue_active={len(s.get('queue_active') or [])} · handoffs={s.get('pending_handoffs_n')}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
