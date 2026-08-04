"""Backlog + sprint board persistence (JSON + rendered markdown)."""
from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

# Repo root: .../mycelial-republic
ROOT = Path(__file__).resolve().parents[3]
SCRUM = ROOT / "scrum"
BACKLOG_JSON = SCRUM / "backlog.json"
BACKLOG_YAML = SCRUM / "backlog.yaml"
CURRENT = SCRUM / "sprints" / "current"
BOARD_MD = CURRENT / "board.md"
STANDUP_MD = CURRENT / "standup.md"
RETRO_MD = CURRENT / "retro.md"
META_JSON = CURRENT / "meta.json"
HANDOFFS = SCRUM / "handoffs"
WAIVERS = SCRUM / "waivers"
RAW_DIR = ROOT / "data" / "raw"

STATUSES = ("backlog", "ready", "doing", "review", "done", "blocked")


def ensure_dirs() -> None:
    for p in (SCRUM, CURRENT, HANDOFFS, WAIVERS, SCRUM / "sprints"):
        p.mkdir(parents=True, exist_ok=True)


def _try_yaml_load(text: str) -> dict[str, Any] | None:
    try:
        import yaml  # type: ignore

        data = yaml.safe_load(text)
        return data if isinstance(data, dict) else None
    except Exception:
        return None


def load_backlog() -> dict[str, Any]:
    ensure_dirs()
    if BACKLOG_JSON.is_file():
        return json.loads(BACKLOG_JSON.read_text(encoding="utf-8"))
    if BACKLOG_YAML.is_file():
        data = _try_yaml_load(BACKLOG_YAML.read_text(encoding="utf-8"))
        if data:
            save_backlog(data)
            return data
    return {"sprint_defaults": {"length_days": 7, "wip_per_role": 2}, "epics": {}, "tickets": []}


def save_backlog(data: dict[str, Any]) -> None:
    ensure_dirs()
    BACKLOG_JSON.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    # lightweight yaml export for humans
    BACKLOG_YAML.write_text(_to_simple_yaml(data), encoding="utf-8")
    render_board(data)


def _to_simple_yaml(data: dict[str, Any]) -> str:
    """Export readable YAML without requiring PyYAML to write."""
    lines = [
        "# Auto-synced from backlog.json — prefer `mycelia scrum` to edit status",
        f"# updated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "sprint_defaults:",
        f"  length_days: {data.get('sprint_defaults', {}).get('length_days', 7)}",
        f"  wip_per_role: {data.get('sprint_defaults', {}).get('wip_per_role', 2)}",
        "",
        "epics:",
    ]
    for k, v in (data.get("epics") or {}).items():
        lines.append(f"  {k}: {v}")
    lines.append("")
    lines.append("tickets:")
    for t in data.get("tickets") or []:
        lines.append(f"  - id: {t.get('id')}")
        lines.append(f"    title: {_q(t.get('title'))}")
        lines.append(f"    epic: {t.get('epic')}")
        lines.append(f"    status: {t.get('status')}")
        lines.append(f"    role: {t.get('role')}")
        lines.append(f"    priority: {t.get('priority')}")
        deps = t.get("depends_on") or []
        lines.append(f"    depends_on: [{', '.join(str(d) for d in deps)}]")
        lines.append(f"    blocks_r0: {str(bool(t.get('blocks_r0'))).lower()}")
        lines.append(f"    estimate: {t.get('estimate', 'M')}")
        if t.get("assignee"):
            lines.append(f"    assignee: {t.get('assignee')}")
        if t.get("evidence"):
            lines.append(f"    evidence: {_q(t.get('evidence'))}")
        if t.get("blocked_reason"):
            lines.append(f"    blocked_reason: {_q(t.get('blocked_reason'))}")
        if t.get("notes"):
            note = str(t.get("notes")).replace("\n", " ").strip()
            lines.append(f"    notes: {_q(note)}")
        lines.append("")
    return "\n".join(lines)


def _q(s: Any) -> str:
    t = str(s or "").replace('"', '\\"')
    return f'"{t}"'


def get_ticket(data: dict[str, Any], tid: str) -> dict[str, Any] | None:
    for t in data.get("tickets") or []:
        if str(t.get("id")) == str(tid):
            return t
    return None


def raw_empty() -> bool:
    if not RAW_DIR.is_dir():
        return True
    # any non-hidden file?
    for p in RAW_DIR.rglob("*"):
        if p.is_file() and not p.name.startswith("."):
            return False
    return True


def gate_check(ticket: dict[str, Any]) -> tuple[bool, str]:
    """Return (ok, reason)."""
    if ticket.get("blocks_r0") and raw_empty():
        if str(ticket.get("id")) in {"W0.0"} or ticket.get("role") == "PO":
            return True, ""
        # docs-only exceptions
        if str(ticket.get("id")).startswith("SCRUM") or str(ticket.get("id")).startswith("INST"):
            return True, ""
        if ticket.get("status") in {"done", "backlog"}:
            return True, ""
        return False, "BLOCKED_W0.0: data/raw empty — refuse train/data pipeline until archive or waiver"
    return True, ""


def render_board(data: dict[str, Any] | None = None) -> str:
    data = data or load_backlog()
    meta = {}
    if META_JSON.is_file():
        meta = json.loads(META_JSON.read_text(encoding="utf-8"))
    knot = meta.get("knot") or "(unnamed — set via mycelia scrum plan --knot '...')"
    goal = meta.get("goal") or ""
    end = meta.get("end_date") or ""

    by: dict[str, list] = {s: [] for s in STATUSES}
    for t in data.get("tickets") or []:
        st = t.get("status") or "backlog"
        if st not in by:
            st = "backlog"
        by[st].append(t)

    lines = [
        f"# Sprint board",
        f"",
        f"- **knot:** {knot}",
        f"- **goal:** {goal}",
        f"- **end:** {end}",
        f"- **updated:** {datetime.now(timezone.utc).isoformat()}",
        f"- **data/raw empty:** {raw_empty()}",
        f"",
        f"See `docs/SCRUM.md`. Evidence → `docs/MILESTONES.md` on major Done.",
        f"",
    ]
    for st in STATUSES:
        lines.append(f"## {st.upper()}")
        lines.append("")
        if not by[st]:
            lines.append("_none_")
            lines.append("")
            continue
        for t in sorted(by[st], key=lambda x: (x.get("priority") or "P9", x.get("id") or "")):
            dep = ",".join(t.get("depends_on") or []) or "—"
            asg = t.get("assignee") or "—"
            br = f" · **blocked:** {t.get('blocked_reason')}" if t.get("blocked_reason") else ""
            ev = f" · evidence: `{t.get('evidence')}`" if t.get("evidence") else ""
            lines.append(
                f"- **{t.get('id')}** [{t.get('priority')}] `{t.get('role')}` — {t.get('title')} "
                f"(dep: {dep}; assignee: {asg}){br}{ev}"
            )
        lines.append("")

    lines.append("## WIP check")
    lines.append("")
    wip: dict[str, int] = {}
    for t in by["doing"]:
        r = str(t.get("role") or "?")
        wip[r] = wip.get(r, 0) + 1
    limit = (data.get("sprint_defaults") or {}).get("wip_per_role", 2)
    if not wip:
        lines.append(f"_no doing tickets_ (limit {limit}/role)")
    else:
        for r, n in sorted(wip.items()):
            flag = " ⚠️ OVER" if n > limit else ""
            lines.append(f"- {r}: {n}/{limit}{flag}")
    lines.append("")

    ensure_dirs()
    BOARD_MD.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


def deps_satisfied(data: dict[str, Any], ticket: dict[str, Any]) -> tuple[bool, list[str]]:
    missing = []
    for d in ticket.get("depends_on") or []:
        dt = get_ticket(data, str(d))
        if not dt or dt.get("status") != "done":
            missing.append(str(d))
    return (len(missing) == 0, missing)


def append_standup(who: str, did: str, doing: str, block: str) -> None:
    ensure_dirs()
    if not STANDUP_MD.is_file():
        STANDUP_MD.write_text("# Standup log\n\n", encoding="utf-8")
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    block = block or "none"
    entry = (
        f"### {ts} — {who}\n"
        f"- **did:** {did or '—'}\n"
        f"- **doing:** {doing or '—'}\n"
        f"- **blocked:** {block}\n\n"
    )
    with STANDUP_MD.open("a", encoding="utf-8") as f:
        f.write(entry)
