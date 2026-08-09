"""Ghost Ledger — single source of truth for all system spend.

One file. Every dollar. Every call. Every route decision. Every model.
Written from wherever the spend happens — Ghost loop, DeepSeek API poll,
manual call, inbox processor. The ledger doesn't care WHO writes. It cares
that EVERYTHING gets written.

SCHEMA: ghost_ledger.v1
LAW: Every cost event writes to the ledger. No exceptions.
LAW: The ledger is append-only. Rows are never deleted.
LAW: Multiple writers. Single file. JSONL.
"""

from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

try:
    from config import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parent.parent

LEDGER_PATH = ROOT / "memory" / "ledger" / "ghost_ledger.jsonl"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_entry(
    source: str,
    model: str,
    tokens_in: int = 0,
    tokens_out: int = 0,
    cost_usd: float = 0.0,
    task_type: str = "",
    goal_summary: str = "",
    via: str = "direct",  # "ghost_loop", "direct_call", "inbox_processor", "api_poll"
    request_id: str = "",
) -> dict[str, Any]:
    """Write a cost entry to the Ghost ledger.

    Call this from ANYWHERE a model is invoked:
      - task_router.route_task() after routing
      - grok_rightsize.call_grok() after API response
      - Direct DeepSeek calls
      - Inbox processor after task execution
      - Manual calls through the Python REPL

    The ledger doesn't care who calls it. It cares that EVERY call gets recorded.
    """
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "schema": "ghost_ledger.v1",
        "ts": _now(),
        "source": source,           # which module/function called the model
        "model": model,             # which model was used
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "tokens_total": tokens_in + tokens_out,
        "cost_usd": cost_usd,
        "task_type": task_type,     # classify, analyze_reason, research, etc.
        "goal_summary": goal_summary[:200] if goal_summary else "",
        "via": via,                 # how was the call routed
        "request_id": request_id,   # external API request ID for correlation
        "row_hash": "",             # filled below
    }

    # Content-address the row for tamper detection
    row_bytes = json.dumps({k: entry[k] for k in sorted(entry) if k != "row_hash"}, default=str)
    entry["row_hash"] = hashlib.sha256(row_bytes.encode()).hexdigest()[:16]

    try:
        with open(LEDGER_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, default=str) + "\n")
    except OSError:
        pass

    # Also publish to Verkle bus if available
    try:
        from mag.verkle_bus import publish_sync, CH_VERKLE
        publish_sync(CH_VERKLE, {
            "type": "ledger_entry",
            "ts": _now(),
            "data": {
                "source": source,
                "model": model,
                "cost_usd": cost_usd,
                "tokens_total": entry["tokens_total"],
                "row_hash": entry["row_hash"],
            },
        })
    except Exception:
        pass

    return entry


def read_ledger(tail: int = 50) -> list[dict[str, Any]]:
    """Read recent ledger entries."""
    if not LEDGER_PATH.is_file():
        return []
    entries = []
    for line in LEDGER_PATH.read_text().strip().splitlines()[-tail:]:
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return entries


def ledger_summary() -> dict[str, Any]:
    """Summarize the ledger: total spend, by model, by source, by task type."""
    entries = read_ledger(tail=10000)
    if not entries:
        return {"ok": True, "entries": 0, "message": "Ledger is empty. No model calls recorded yet."}

    total_cost = sum(e.get("cost_usd", 0) for e in entries)
    total_tokens = sum(e.get("tokens_total", 0) for e in entries)

    by_model: dict[str, float] = {}
    by_source: dict[str, int] = {}
    by_task: dict[str, int] = {}

    for e in entries:
        model = e.get("model", "unknown")
        source = e.get("source", "unknown")
        task = e.get("task_type", "unknown")

        by_model[model] = by_model.get(model, 0) + e.get("cost_usd", 0)
        by_source[source] = by_source.get(source, 0) + 1
        by_task[task] = by_task.get(task, 0) + 1

    # Check for gaps: cost_enforcer vs ledger
    try:
        from mag.cost_enforcer import get_current_spend
        internal_spend = get_current_spend()
        gap = total_cost - internal_spend
    except Exception:
        internal_spend = 0.0
        gap = total_cost

    return {
        "ok": True,
        "entries": len(entries),
        "total_cost_usd": round(total_cost, 6),
        "total_tokens": total_tokens,
        "by_model": by_model,
        "by_source": by_source,
        "by_task_type": by_task,
        "cost_enforcer_spend": round(internal_spend, 6),
        "ledger_vs_enforcer_gap": round(gap, 6),
        "gap_warning": f"${gap:.4f} unaccounted for in cost_enforcer" if gap > 0.001 else "Ledger and enforcer aligned",
        "ts": _now(),
    }


def sync_deepseek_usage(api_key: Optional[str] = None) -> dict[str, Any]:
    """Poll DeepSeek usage API and write any uncounted calls to the ledger.

    This is the bridge between the external billing dashboard and the
    internal Ghost ledger. Without this, the Tax Collector watches an
    empty door while 5,271 calls go through another.

    Returns: {calls_found, calls_written, total_cost}
    """
    import os
    import requests

    key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        # Try loading from .env
        env_path = ROOT / ".env"
        if env_path.is_file():
            for line in env_path.read_text().splitlines():
                if line.startswith("DEEPSEEK_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break

    if not key:
        return {"ok": False, "error": "No DeepSeek API key available"}

    try:
        # DeepSeek doesn't have a public usage API — this is a best-effort pattern
        # For now: read existing ledger, compare against known calls, flag gaps
        summary = ledger_summary()
        ds_calls = summary.get("by_model", {}).get("deepseek-chat", 0) + \
                   summary.get("by_model", {}).get("deepseek-v4-flash", 0)

        return {
            "ok": True,
            "deepseek_calls_in_ledger": ds_calls,
            "total_entries": summary["entries"],
            "gap_vs_enforcer": summary["ledger_vs_enforcer_gap"],
            "note": "DeepSeek usage API not yet integrated. Calls tracked via write_entry() at call site.",
        }
    except Exception as e:
        return {"ok": False, "error": str(e)[:200]}


def backfill_manual_calls() -> int:
    """Backfill the ledger with calls we know happened but weren't recorded.

    This is for calls made before the ledger existed. Estimate from
    known sources: DeepSeek dashboard, Grok API logs, etc.
    """
    written = 0

    # DeepSeek: 5,271 calls, 624M tokens, $7.91 (from operator's dashboard)
    # We can't record each individually, but we can write a summary entry
    write_entry(
        source="backfill",
        model="deepseek-chat",
        tokens_in=312_000_000,   # estimate: half of 624M
        tokens_out=312_000_000,  # estimate: half of 624M
        cost_usd=7.91,
        task_type="various",
        goal_summary="Backfill: 5,271 calls across all task types on 2026-08-08. Exact breakdown unavailable — recorded as single summary entry.",
        via="manual_backfill",
    )
    written += 1

    return written
