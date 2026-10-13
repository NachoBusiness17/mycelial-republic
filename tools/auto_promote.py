#!/usr/bin/env python3
"""auto_promote.py - deterministic auto-promote gate for improve candidates (Q-002, 2026-09-28).

The ask: promote candidates that are (all three, deterministic):
  1. local_feasible is true (ledger stores strings: "true"/"yes" count,
     "unknown"/"false"/missing do not; a real bool True counts),
  2. kind is practice or tesuji (the transferable-practice kinds; model/risk/
     runtime/census kinds keep the human gate),
  3. at least 48h old (age from the ``created`` ISO timestamp, falling back to
     the ``date`` day string at midnight UTC when ``created`` is absent; 42 of
     192 ledger rows as of 2026-09-28 carry no ``created``).

Fail-closed by construction: an unparseable or missing timestamp makes a row
ineligible, never "old enough by guesswork". Rows already rejected or promoted
are never touched (status must be new or hold).

Apply reuses ``mag.improve.promote_apply`` so the mirror-lens verdict, the
practice playbook append and the promote training event keep a single writer.
Every applied or blocked decision appends one audit row to
``memory/improve/auto_promote.jsonl``.

Wired into the daily improve loop (``mag.improve.improve_once``, after eval).
Standalone preview: ``python tools/auto_promote.py --dry``.

The 48h soak is the design: a candidate a scout or the eval workhorse just
wrote gets two days of cooling before any automatic status change, so the gate
promotes survivors, not fresh noise. Receipt:
watch/inbox/burn_reset_20260927/queue/Q-002.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

AUTO_NOTE = "auto-promote: local_feasible + practice/tesuji kind + 48h soak (tools/auto_promote.py)"
DEFAULT_MIN_AGE_HOURS = 48.0
DEFAULT_KINDS = ("practice", "tesuji")
FEASIBLE_TRUE = {"true", "yes"}
OPEN_STATUSES = {"new", "hold"}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _parse_ts(value: Any) -> datetime | None:
    """Parse an ISO timestamp or a YYYY-MM-DD day string. Naive means UTC.

    Returns None on anything unparseable: the caller treats that as
    ineligible instead of guessing an age.
    """
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    s = str(value or "").strip()
    if not s:
        return None
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _candidate_age_hours(row: dict[str, Any], now: datetime) -> float | None:
    """Hours since ``created`` (fallback: the ``date`` day string). None = unknown."""
    dt = _parse_ts(row.get("created")) or _parse_ts(row.get("date"))
    if dt is None:
        return None
    return (now - dt).total_seconds() / 3600.0


def _is_local_feasible(row: dict[str, Any]) -> bool:
    v = row.get("local_feasible")
    if isinstance(v, bool):
        return v
    return str(v or "").strip().lower() in FEASIBLE_TRUE


def eligibility(row: dict[str, Any], *, now: datetime, min_age_hours: float, kinds: tuple[str, ...]) -> tuple[bool, str]:
    """The whole gate as one pure predicate. (True, "eligible") or (False, reason)."""
    kind = str(row.get("kind") or "").strip().lower()
    if kind not in kinds:
        return False, f"kind:{kind or 'none'}-not-in-allowlist"
    if not _is_local_feasible(row):
        return False, "local_feasible-not-true"
    status = str(row.get("status") or "new").strip().lower()
    if status not in OPEN_STATUSES:
        return False, f"status:{status}-not-open"
    age = _candidate_age_hours(row, now)
    if age is None:
        return False, "age-unparseable-or-missing"
    if age < min_age_hours:
        return False, f"age:{age:.1f}h-under-{min_age_hours:g}h"
    return True, "eligible"


def run(
    *,
    dry: bool = False,
    now: datetime | None = None,
    min_age_hours: float | None = None,
    kinds: tuple[str, ...] | list[str] | None = None,
    paths: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Select eligible candidates from the ledger and promote them (or preview).

    Returns a JSON-safe report; also the value embedded in the improve loop's
    daily output (improve_once phases.auto_promote).
    """
    from mag.improve import ensure_dirs, load_config, promote_apply, read_candidates

    cfg = load_config()
    auto_cfg = (cfg.get("promote") or {}).get("auto") or {}
    enabled = bool(auto_cfg.get("enabled", True))
    hours = float(
        min_age_hours
        if min_age_hours is not None
        else auto_cfg.get("min_age_hours", DEFAULT_MIN_AGE_HOURS)
    )
    kind_set = tuple(
        kinds
        if kinds is not None
        else (auto_cfg.get("kinds") or DEFAULT_KINDS)
    )
    report: dict[str, Any] = {
        "ok": True,
        "tool": "auto_promote",
        "dry": bool(dry),
        "enabled": enabled,
        "min_age_hours": hours,
        "kinds": list(kind_set),
        "scanned": 0,
        "promoted": [],
        "blocked": [],
        "skipped": {},
    }
    if not enabled:
        return report

    now = now or _utc_now()
    paths = paths or ensure_dirs(cfg)
    rows = read_candidates(paths, limit=10000)
    report["scanned"] = len(rows)

    eligible_ids: list[str] = []
    for row in rows:
        ok, reason = eligibility(row, now=now, min_age_hours=hours, kinds=kind_set)
        if ok:
            eligible_ids.append(row.get("id"))
        else:
            key = reason.split(":")[0].split("-")[0]
            report["skipped"][key] = report["skipped"].get(key, 0) + 1

    audit_path = paths["root"] / "auto_promote.jsonl"

    def _audit(entry: dict[str, Any]) -> None:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")

    for cid in eligible_ids:
        if dry:
            report["promoted"].append({"id": cid, "action": "would_promote"})
            continue
        res = promote_apply(cid, note=AUTO_NOTE)
        entry = {
            "ts": _utc_now().isoformat(),
            "id": cid,
            "verdict": "promoted" if res.get("ok") else "blocked",
            "action": res.get("action"),
            "reason": res.get("error", AUTO_NOTE if res.get("ok") else ""),
        }
        _audit(entry)
        if res.get("ok"):
            report["promoted"].append({"id": cid, "action": res.get("action")})
        else:
            report["blocked"].append({"id": cid, "reason": str(res.get("error"))[:200]})

    report["ok"] = True
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="auto_promote", description=__doc__.splitlines()[0])
    ap.add_argument("--dry", action="store_true", help="report eligible ids without promoting")
    ap.add_argument("--min-age-hours", type=float, default=None, help="override the 48h soak")
    args = ap.parse_args(argv)
    report = run(dry=args.dry, min_age_hours=args.min_age_hours)
    print(json.dumps(report, indent=2, default=str))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
