#!/usr/bin/env python3
"""quota_ledger_report.py — receipt-side evidence + rendering for the
window-quota ledger (split from tools/quota_ledger.py for the 400-line cap,
same pattern as the census_patrol_selftest split B2-248; 2026-09-30).

Holds the SECONDARY evidence channel (watch/inbox receipt grep, mtime-bounded
to the scanned day — agent-record bytes always outrank these lines) and the
presentation (markdown + the JSON payload assembly). The ledger itself —
fires, windows, walls, verdict — lives in tools/quota_ledger.py.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

def grep_receipts(repo_root: Path, day: str, limit_files: int = 2000) -> list[dict]:
    """Secondary evidence: receipt lines (mtime on/after the day) naming
    1302/1308. Bytes in agent records outrank these."""
    inbox = repo_root / "watch" / "inbox"
    day_start = datetime.fromisoformat(day).replace(tzinfo=timezone.utc)
    hits: list[dict] = []
    scanned = 0
    for path in sorted(inbox.rglob("*.md")):
        if scanned >= limit_files:
            break
        try:
            mt = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        except OSError:
            continue
        if mt < day_start:
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            if "1302" in line or "1308" in line:
                hits.append({"file": str(path.relative_to(repo_root)).replace("\\", "/"),
                             "line": i, "text": line.strip()[:200]})
                if len(hits) >= 80:
                    return hits
    return hits

def load_drop_rows(repo_root: Path, day: str) -> list[dict]:
    """Wave context from DROP_LEDGER.jsonl — date-granular, not wall-clock."""
    ledger = repo_root / "watch" / "inbox" / "DROP_LEDGER.jsonl"
    rows: list[dict] = []
    if not ledger.is_file():
        return rows
    for line in ledger.read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            row = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            continue
        if str(row.get("ts", "")).startswith(day):
            rows.append(row)
    return rows

def render_markdown(rep, hours: int) -> str:
    """The receipt-shaped stdout report. `rep` is the Report dataclass from
    tools/quota_ledger (kept untyped here to avoid an import cycle)."""
    s = rep.stats
    t = s["tokens"]
    a: list[str] = [
        f"# Quota ledger — {rep.day} (v0, harness-side instrument)\n",
        f"- Fires on the day: **{s['fires_today']}** (completed {s['completed']} / "
        f"failed {s['failed']} / running {s['running_now']}); wall moments "
        f"**{s['walls_today']}** ({s['wall_deaths_today']} deaths coded 1302/1308)",
        f"- Current trailing-{hours}h window: **{s['current_window_fires']} fires**, "
        f"{s['running_now']} running, {s['walls_last_hour']} walls in the last hour "
        f"→ current shape **{s['current_shape']}**",
        f"- Peak rolling-{hours}h window: **{s['peak_window']}** at "
        f"{s['peak_window_at']}; peak in-flight width **{s['peak_concurrency']}** "
        f"at {s['peak_concurrency_at']}",
        f"- Tokens (ROUGH): {t['recorded_tokens']:,} recorded on "
        f"{t['recorded_fires']} fires + {t['unrecorded_fires']} unrecorded × mean "
        f"{t['mean_per_recorded']:,} ≈ **{t['estimated_total']:,}** total "
        f"(cache-inclusive, fire-time attributed)\n",
        f"## Day-shape verdict: **{rep.verdict}** (current dispatch signal: "
        f"{s['current_shape']})\n",
        rep.hold_line + "\n",
        "## Wall log (byte truth: failed-agent death payloads)\n",
        "| wall moment (UTC) | code(s) | lanes dead | reset / window ended |",
        "|---|---|---|---|",
    ]
    for w in rep.walls:
        lanes = "; ".join(l or "?" for l in w.lanes)
        a.append(f"| {w.ts.isoformat(timespec='seconds')} | "
                 f"{'+'.join(sorted(w.codes))} | {len(w.lanes)} "
                 f"({lanes[:117] + '...' if len(lanes) > 120 else lanes}) | "
                 f"{w.window_ended} |")
    a.append("\n## Receipt evidence naming the codes (secondary; bytes outrank prose)\n")
    if rep.receipt_hits:
        a += [f"- `{h['file']}:{h['line']}` — {h['text']}" for h in rep.receipt_hits[:15]]
        if len(rep.receipt_hits) > 15:
            a.append(f"- … {len(rep.receipt_hits) - 15} more lines (see --json)")
    else:
        a.append("(none)")
    a.append("\n## Honesty\n")
    a.append("- Tokens are ROUGH: usage bytes exist only for completed subagents "
             "(failed/running carry none — the lanes that died ON the wall are exactly "
             "the unrecorded ones); cache-inclusive; fire-time attributed; main-session "
             "turns invisible. Exact instrument = provider-side usage fields plus the "
             "account usage snapshot inside every 1302/1308 payload (request ids "
             "embedded). Provider clock offset (UTC+8) is inferred from 14 "
             "byte-consistent request-id stamps on 2026-09-30; wall-moment UTC times "
             "come from harness completedAt bytes.")
    return "\n".join(a)

def render_json(rep) -> str:
    """The --json payload (walls, stats, receipt hits, drop rows)."""
    return json.dumps({
        "day": rep.day, "verdict": rep.verdict, "hold_line": rep.hold_line,
        "stats": rep.stats, "receipt_hits": rep.receipt_hits,
        "walls": [{"ts": w.ts.isoformat(), "codes": sorted(w.codes),
                   "lanes": w.lanes, "reset_at": w.reset_at,
                   "provider_stamp": w.provider_stamp.isoformat()
                   if w.provider_stamp else None,
                   "window_ended": w.window_ended} for w in rep.walls],
        "drop_rows": [{"ts": r.get("ts"), "drop_type": r.get("drop_type"),
                       "lanes": len(r.get("lanes_fired") or []),
                       "spend": r.get("spend")} for r in rep.drop_rows],
    }, indent=1)
