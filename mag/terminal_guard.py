"""terminal_guard — the terminal is a stateful thing in a stateless system; it gets wedged.

"Self-aware" terminal = a guard the agent ALWAYS uses when touching the interactive shell:
  probe(out)  -> classify a terminal response (healthy / silent / wedged-" >> " / parse-error)
  heal()      -> the verified auto-fix: send a lone closing quote to break a stuck ">>"
                 continuation (unclosed string from a mangled multi-line command), OR reset.
  fold(...)   -> record the wedge to failure_kb + ghost trail so the LOOP learns the signature
                 and auto-handles it next time instead of a whole session of routing around it.

HONEST LIMIT: the interactive terminal is the operator's VS Code shell — the framework can't own
or drive it directly (it's not a supervised process). So "self-aware" means: the AGENT uses this
guard for every terminal command (probe before/after, heal on wedge, fold to learn), and the
signature is learned so the fix is instant. This is the same shape as process_supervisor's
self-healing doctrine, applied to the shell.

Schema: terminal_guard.v1 · deterministic $0 · reuse: failure_kb (learn), doctor (health)
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

SCHEMA = "terminal_guard.v1"

# Signature of a wedged/poisoned shell — the exact markers we saw on 2026-08-14.
WEDGE_MARKERS = [
    ">>",                       # PowerShell continuation prompt (unclosed string)
    "TerminatorExpectedAtEndOfString",
    "ParserError",
    "Missing closing",
    "Missing expression after",
]
SILENT = "command produced no output"   # swallow-everything state


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def probe(output: str | None) -> dict[str, Any]:
    """Classify a terminal response: healthy / silent / wedged. The agent feeds the output of a
    simple probe command (e.g. `Write-Output ok`) through this BEFORE trusting further commands."""
    if output is None or (isinstance(output, str) and output.strip() == ""):
        return {"ok": False, "schema": SCHEMA, "state": "silent",
                "detail": "no output — shell may be wedged/swallowing; do NOT fire work at it"}
    low = str(output).lower()
    for m in WEDGE_MARKERS:
        if m in low:
            return {"ok": False, "schema": SCHEMA, "state": "wedged",
                    "detail": f"shell in bad state (marker '{m}') — break the continuation first"}
    return {"ok": True, "schema": SCHEMA, "state": "healthy"}


def heal() -> dict[str, Any]:
    """Auto-heal a wedged '>>' continuation (the verified 2026-08-14 fix)."""
    return {
        "ok": True, "schema": SCHEMA, "action": "send_closing_quote",
        "command": '"',   # a lone closing double-quote + Enter breaks the unclosed string
        "then": 'verify with `Write-Output "ok"`; if still wedged, reset/restart the terminal',
        "note": ("a mangled multi-line inline command left an unclosed string -> the shell sat at "
                 "'>>' and swallowed everything. Sending the closing quote makes it parse the "
                 "broken command, error out, and return to a clean prompt."),
        "verified": "2026-08-14",
    }


def fold(goal: str, state: str, detail: str) -> None:
    """Fold the wedge to failure_kb so the loop learns the signature and self-handles it."""
    try:
        from mag import failure_kb
        failure_kb.log_failure(kind="terminal_wedge", detail=detail or state,
                               goal=goal or "terminal_guard", error=detail or state,
                               tool="terminal_guard", phase="terminal")
    except Exception:
        pass
    try:
        from mag import ghost
        ghost.ping("autorun", kind="terminal_wedge", text=f"{state}: {detail}"[:200], dry=True)
    except Exception:
        pass


def guard(result: dict[str, Any], *, goal: str = "") -> dict[str, Any]:
    """Convenience: run probe() on a command result; if wedged/silent, return heal() guidance and
    fold it. Returns the (possibly healed) verdict the agent should act on."""
    p = probe(result.get("output") if isinstance(result, dict) else result)
    if p["ok"]:
        return p
    h = heal()
    fold(goal, p["state"], p.get("detail", ""))
    p["heal"] = h
    return p
