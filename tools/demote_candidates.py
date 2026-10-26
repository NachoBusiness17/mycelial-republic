#!/usr/bin/env python3
"""demote_candidates.py - frontier-gap task-shape route for improve candidates (Q-049, 2026-09-28).

The inverse of mag/gap_map.py. gap_map reads the cost ledger and flags a task
shape as a FRONTIER GAP when the cheap system's success rate on it is below
the bar ("Cheap success below this = frontier gap", mag/gap_map.py SUCCESS_BAR
0.6). This tool reads the candidate ledger the same way:

  - cheap     = local_feasible true (the ledger's cheap/local-capable marker;
                same string-ledger reading tools/auto_promote.py canonized:
                "true"/"yes" count, a real bool True counts, "unknown"/"false"/
                missing do not),
  - success   = a TERMINAL outcome: status promoted counts a cheap success,
                status rejected counts a cheap failure. Rows still open
                (new/hold) are not outcomes and stay out of the rate,
  - quality bar = the per-shape cheap success rate < success_bar (default 0.6,
                gap_map's SUCCESS_BAR), computed only for shapes with at least
                min_terminal (default 2) terminal rows (gap_map's n>=2 rule).

A shape failing that test is a frontier-gap shape. Every OPEN row (new/hold)
of a gap shape is then routed to the demotion path: status "demoted" (written
through mag.improve.update_candidate_status, the single status writer) plus
one audit row per decision in memory/improve/demoted.jsonl (mirrors
memory/improve/auto_promote.jsonl from Q-002).

Fail-closed by construction: rows without an explicit kind are never touched
(43 of 192 ledger rows as of 2026-09-28 are kind-less), terminal and already
demoted rows are never re-touched, and a shape with too few terminal rows is
never judged. The new status is inert by design: rank_candidates_for_brief
surfaces only new/hold (mag/improve.py), the Q-002 auto-promote gate touches
only new/hold (tools/auto_promote.py OPEN_STATUSES), and no consumer of the
ledger enumerates statuses, so "demoted" simply leaves the promote surface.

Note on the gates: demotion and auto-promotion are independent and can
disagree by design. A practice/tesuji shape whose cheap success rate fell
below the bar SHOULD have its open rows pulled from the auto-promote path;
if that ever bites, the demoted.jsonl audit trail is the receipt to read.

Standalone preview: python tools/demote_candidates.py --dry
Apply:               python tools/demote_candidates.py
Receipt: watch/inbox/burn_reset_20260927/queue/Q-049.md
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

DEMOTE_NOTE = "auto-demote: task-shape cheap success rate below bar (tools/demote_candidates.py)"
DEFAULT_SUCCESS_BAR = 0.6  # mag/gap_map.py SUCCESS_BAR
DEFAULT_MIN_TERMINAL = 2   # mag/gap_map.py per-shape n>=2 rule
TERMINAL_SUCCESS = "promoted"
TERMINAL_FAIL = "rejected"
OPEN_STATUSES = {"new", "hold"}


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _is_cheap(row: dict[str, Any]) -> bool:
    """local_feasible true, string-ledger semantics (mirrors tools/auto_promote._is_local_feasible)."""
    v = row.get("local_feasible")
    if isinstance(v, bool):
        return v
    return str(v or "").strip().lower() in ("true", "yes")


def shape_rate(rows: list[dict[str, Any]], kind: str) -> dict[str, Any]:
    """Cheap terminal outcomes for one task shape: n, successes, rate, open count."""
    n = succ = opened = 0
    for r in rows:
        if str(r.get("kind") or "").strip().lower() != kind or not _is_cheap(r):
            continue
        status = str(r.get("status") or "new").strip().lower()
        if status == TERMINAL_SUCCESS:
            n += 1
            succ += 1
        elif status == TERMINAL_FAIL:
            n += 1
        elif status in OPEN_STATUSES:
            opened += 1
    rate = (succ / n) if n else None
    return {"kind": kind, "terminal_n": n, "success_n": succ,
            "rate": round(rate, 3) if rate is not None else None, "open_n": opened}


def frontier_gap_shapes(
    rows: list[dict[str, Any]], *, success_bar: float, min_terminal: int
) -> tuple[list[str], list[dict[str, Any]]]:
    """Shapes whose cheap success rate is below the bar. (gap_map n>=2 rule.)"""
    kinds = sorted({
        str(r.get("kind") or "").strip().lower()
        for r in rows
        if str(r.get("kind") or "").strip()
    })
    shapes = [shape_rate(rows, k) for k in kinds]
    shapes.sort(key=lambda s: (-(s["rate"] if s["rate"] is not None else 1.0), s["kind"]))
    gaps = [
        s["kind"] for s in shapes
        if s["terminal_n"] >= min_terminal and s["rate"] is not None and s["rate"] < success_bar
    ]
    return gaps, shapes


def demotion_targets(
    rows: list[dict[str, Any]], gap_kinds: set[str]
) -> list[tuple[dict[str, Any], str]]:
    """Cheap open rows of a gap shape, with the shape name.

    The cheap marker is required on the row too: the shape is condemned by its
    CHEAP terminal outcomes, so only rows that share that marker get routed.
    A local_feasible-unknown row never claimed cheap and stays (fail-closed).
    Kind-less rows are never touched.
    """
    out: list[tuple[dict[str, Any], str]] = []
    for r in rows:
        kind = str(r.get("kind") or "").strip().lower()
        if not kind:
            continue
        if kind not in gap_kinds:
            continue
        if not _is_cheap(r):
            continue
        status = str(r.get("status") or "new").strip().lower()
        if status not in OPEN_STATUSES:
            continue
        out.append((r, kind))
    return out


def run(
    *,
    dry: bool = False,
    success_bar: float | None = None,
    min_terminal: int | None = None,
    paths: dict[str, Path] | None = None,
) -> dict[str, Any]:
    """Map candidate-ledger gap shapes and demote their open rows (or preview)."""
    from mag.improve import ensure_dirs, load_config, read_candidates

    cfg = load_config()
    demote_cfg = (cfg.get("demote") or {}) if isinstance(cfg.get("demote"), dict) else {}
    enabled = bool(demote_cfg.get("enabled", True))
    bar = float(
        success_bar
        if success_bar is not None
        else demote_cfg.get("success_bar", DEFAULT_SUCCESS_BAR)
    )
    min_term = int(
        min_terminal
        if min_terminal is not None
        else demote_cfg.get("min_terminal", DEFAULT_MIN_TERMINAL)
    )
    report: dict[str, Any] = {
        "ok": True,
        "tool": "demote_candidates",
        "dry": bool(dry),
        "enabled": enabled,
        "success_bar": bar,
        "min_terminal": min_term,
        "scanned": 0,
        "shapes": [],
        "frontier_gap_shapes": [],
        "demoted": [],
        "blocked": [],
        "skipped": {},
    }
    if not enabled:
        return report

    paths = paths or ensure_dirs(cfg)
    rows = read_candidates(paths, limit=10000)
    report["scanned"] = len(rows)

    gaps, shapes = frontier_gap_shapes(rows, success_bar=bar, min_terminal=min_term)
    report["shapes"] = shapes
    report["frontier_gap_shapes"] = gaps

    audit_path = paths["root"] / "demoted.jsonl"

    def _audit(entry: dict[str, Any]) -> None:
        audit_path.parent.mkdir(parents=True, exist_ok=True)
        with audit_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False, default=str) + "\n")

    for row, kind in demotion_targets(rows, set(gaps)):
        cid = row.get("id")
        shape = shape_rate(rows, kind)
        reason = f"kind:{kind} cheap_success_rate={shape['rate']}-below-{bar:g}"
        if dry:
            report["demoted"].append({"id": cid, "kind": kind, "action": "would_demote"})
            continue
        from mag.improve import update_candidate_status

        ok = update_candidate_status(
            cid, "demoted", note=DEMOTE_NOTE,
            extra={"demote_shape": kind, "demote_rate": shape["rate"]},
        )
        entry = {
            "ts": _utc_now().isoformat(),
            "id": cid,
            "kind": kind,
            "verdict": "demoted" if ok else "blocked",
            "reason": reason if ok else "update_candidate_status-false",
        }
        _audit(entry)
        if ok:
            report["demoted"].append({"id": cid, "kind": kind, "action": "demoted"})
        else:
            report["blocked"].append({"id": cid, "reason": reason})

    skipped: dict[str, int] = report["skipped"]
    for r in rows:
        kind = str(r.get("kind") or "").strip().lower()
        status = str(r.get("status") or "new").strip().lower()
        if not kind or kind not in set(gaps):
            key = "kind" if not kind else "shape"
            skipped[key] = skipped.get(key, 0) + 1
        elif status not in OPEN_STATUSES:
            skipped["status"] = skipped.get("status", 0) + 1
        elif not _is_cheap(r):
            skipped["cheap"] = skipped.get("cheap", 0) + 1
    report["ok"] = True
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="demote_candidates", description=__doc__.splitlines()[0])
    ap.add_argument("--dry", action="store_true", help="report gap shapes and target ids without demoting")
    ap.add_argument("--success-bar", type=float, default=None, help="override the quality bar (default 0.6)")
    ap.add_argument("--min-terminal", type=int, default=None, help="override the per-shape terminal minimum (default 2)")
    args = ap.parse_args(argv)
    report = run(dry=args.dry, success_bar=args.success_bar, min_terminal=args.min_terminal)
    print(json.dumps(report, indent=2, default=str))
    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
