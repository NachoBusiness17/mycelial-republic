"""Append-only router log + CURRENT.md sync."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from config import CURRENT_MD, LOGS_DIR, ROUTER_LOG, current_md, current_scratch


def _current_target() -> Path:
    """AG6 (2026-09-29): writer target for the CURRENT.md contract.

    Probe/test runs set MAG_CURRENT_SCRATCH=1 → config.current_scratch()
    returns state/CURRENT.scratch.md and a probe stub never becomes the live
    brief (the gala old-files probe wrote "probe run (fake harness)" into
    state/CURRENT.md through this exact writer — audit finding #5); the env
    outranks any override so a leaked probe can never reach production.
    Production writers set nothing and keep CURRENT.md; an explicit
    CURRENT_MD override (test redirection in tests/test_resume_contract.py
    patches both config and this module) still wins when no scratch env is set.
    """
    scratch = current_scratch()
    if scratch is not None:  # MAG_CURRENT_SCRATCH=1 routed the writer
        return scratch
    return CURRENT_MD


def log_event(event: dict[str, Any]) -> None:
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "ts": datetime.now(timezone.utc).isoformat(),
        **event,
    }
    with ROUTER_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, default=str) + "\n")


def sync_current(state: dict[str, Any]) -> None:
    target = _current_target()
    if current_scratch() is not None:
        # AG6: scratch routing is active — make the probe write observable in
        # the router log instead of it silently landing beside the live brief.
        log_event({"event": "current-scratch-write", "path": str(target)})
    target.parent.mkdir(parents=True, exist_ok=True)
    plan = state.get("plan") or []
    plan_txt = "\n".join(f"- {s}" for s in plan) if plan else "- (none)"
    trace = state.get("tool_trace") or []
    last_tools = "\n".join(
        f"- {t.get('tool')}: exit={t.get('exit_code')} ok={t.get('ok')}" for t in trace[-5:]
    ) or "- (none)"
    body = f"""# CURRENT

- **status:** {state.get('status')}
- **tier:** {state.get('tier')}
- **route:** {state.get('route')}
- **step_i:** {state.get('step_i')}
- **handoff_id:** {state.get('handoff_id')}
- **updated:** {datetime.now(timezone.utc).isoformat()}

## Goal

{state.get('goal')}

## Plan

{plan_txt}

## Last result

{(state.get('last_result') or '')[:2000]}

## Critique

{(state.get('critique') or '')[:1500]}

## Recent tools

{last_tools}
"""
    target.write_text(body, encoding="utf-8")
