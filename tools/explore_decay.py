#!/usr/bin/env python3
"""explore_decay -- age dead explore rows out of the active backlog.

WAVE: invariant-percolator, wave 6 (2026-10-21). Append-only. Stdlib. $0.

WHY: `memory/percolator/explore.jsonl` only grows. On 2026-10-21 it held 2,874
rows, 1,764 open, 838 of them older than 14 days (median age 2 days, max 58).
The queue metric counted every one of those as live work, so the backlog number
rose all day while nothing was draining. Aging them out is not deletion: the
rows stay exactly where they are, and a classification row is appended.

LAW: never rewrite explore.jsonl (a live writer appends to it by the minute; a
read-modify-write can drop concurrent rows - the 2026-10-20 index lesson). This
tool only APPENDS to `explore_decay.jsonl`; readers join on `canonical`.

Idempotent: a canonical already classified stale is never re-emitted.

Exit ladder (self-stolen from tools/claim_drift_patrol.py):
  0 ok        ledger written (or nothing to do)
  1 REFUSED   ledger exists but is unwritable / unparsable
  2 UNVERIFY  explore queue missing
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parents[1]
EXPLORE = Path("memory") / "percolator" / "explore.jsonl"
LEDGER = Path("memory") / "percolator" / "explore_decay.jsonl"

SCHEMA = "explore_decay.v1"
OK_PREFIX = "EXPLORE-DECAY: ok"
UNVER_PREFIX = "EXPLORE-DECAY: UNVERIFIABLE"
DEFAULT_DAYS = 14


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _ts(value) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def load_rows(path: Path) -> list[dict]:
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def stale_map(path: Path) -> dict[str, dict]:
    """canonical -> latest decay row (append-only ledger, later rows win)."""
    latest: dict[str, dict] = {}
    if not path.is_file():
        return latest
    for row in load_rows(path):
        if row.get("schema") == SCHEMA and row.get("canonical"):
            latest[row["canonical"]] = row
    return latest


def plan(rows: list[dict], already: dict[str, dict], days: float, now: datetime) -> list[dict]:
    out = []
    for row in rows:
        if row.get("status") != "open":
            continue
        canonical = row.get("canonical")
        if not canonical or canonical in already:
            continue
        stamp = _ts(row.get("ts"))
        if stamp is None:
            continue
        age = (now - stamp).total_seconds() / 86400.0
        if age <= days:
            continue
        out.append({
            "schema": SCHEMA,
            "ts": now.isoformat().replace("+00:00", "Z"),
            "canonical": canonical,
            "status": "stale",
            "age_days": round(age, 2),
            "first_ts": row.get("ts"),
            "domain": row.get("domain"),
            "days_bar": days,
            "reason": f"open > {days:g}d without resolution",
        })
    return out


def backlog(rows: list[dict], already: dict[str, dict], now: datetime) -> dict:
    open_rows = [r for r in rows if r.get("status") == "open"]
    stale = [r for r in open_rows if r.get("canonical") in already]
    live = [r for r in open_rows if r.get("canonical") not in already]
    ages = []
    for r in live:
        stamp = _ts(r.get("ts"))
        if stamp:
            ages.append((now - stamp).total_seconds() / 86400.0)
    ages.sort()
    return {
        "rows": len(rows),
        "open": len(open_rows),
        "stale": len(stale),
        "live": len(live),
        "live_share_pct": round(100.0 * len(live) / len(rows), 1) if rows else 0.0,
        "stale_share_of_open_pct": round(100.0 * len(stale) / len(open_rows), 1) if open_rows else 0.0,
        "live_median_age_days": round(ages[len(ages) // 2], 1) if ages else 0.0,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Age dead explore rows out of the active backlog")
    ap.add_argument("--root", default=None, help="estate root (default: this repo)")
    ap.add_argument("--days", type=float, default=DEFAULT_DAYS,
                    help=f"age bar in days (default {DEFAULT_DAYS})")
    ap.add_argument("--apply", action="store_true", help="append classifications to the ledger")
    ap.add_argument("--json", action="store_true", help="machine receipt only")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve() if args.root else ESTATE_ROOT
    explore_path = root / EXPLORE
    ledger_path = root / LEDGER

    if not explore_path.is_file():
        print(f"{UNVER_PREFIX}: explore queue missing: {explore_path}")
        return 2
    try:
        rows = load_rows(explore_path)
        already = stale_map(ledger_path)
    except OSError as exc:
        print(f"{UNVER_PREFIX}: {exc}")
        return 2

    now = _now()
    batch = plan(rows, already, args.days, now)
    wrote = 0
    if args.apply and batch:
        try:
            ledger_path.parent.mkdir(parents=True, exist_ok=True)
            with ledger_path.open("a", encoding="utf-8") as fh:
                for row in batch:
                    fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            wrote = len(batch)
            already = stale_map(ledger_path)
        except OSError as exc:
            print(f"EXPLORE-DECAY: REFUSED -- {exc}")
            return 1

    stats = backlog(rows, already, now)
    receipt = {"schema": "explore_decay_receipt.v1", "ts": now.isoformat().replace("+00:00", "Z"),
               "applied": bool(args.apply), "days_bar": args.days,
               "written": wrote, "pending": 0 if args.apply else len(batch),
               "ledger": str(ledger_path), "stats": stats}

    if args.json:
        print(json.dumps(receipt, indent=2))
    else:
        print(f"{OK_PREFIX} ({'applied' if args.apply else 'dry-run'}) -- bar {args.days:g}d")
        print(f"  rows {stats['rows']} | open {stats['open']} | stale {stats['stale']} "
              f"| live {stats['live']} ({stats['live_share_pct']}% of rows)")
        print(f"  live median age {stats['live_median_age_days']}d | "
              f"stale share of open {stats['stale_share_of_open_pct']}%")
        print(f"  classifications {'written' if args.apply else 'pending'}: {len(batch)} "
              f"-> {ledger_path}")
        if not args.apply and batch:
            print("  rerun with --apply (explore.jsonl is never rewritten)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
