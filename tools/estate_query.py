#!/usr/bin/env python3
"""estate_query — the provenance join the estate never had (IMP4, AE5 wishlist #1).

Problem (AE5 wishlist #1, 2026-09-30): no join key linked trajectory steps,
burns, and duels — provenance questions were grep-by-path across surfaces,
and a lane's story could not be reconstructed in one query. AH14 landed the
join field (corr_id, a uuid4 hex8 in env MAG_CORR_ID) on the three writers
(mag/trajectory_step.py steps.jsonl, mag/game_flow.py FLOW_LEDGER.jsonl,
tools/duel_harness.py duels.jsonl — receipt
watch/inbox/last_mile_20260930/AH14_CORR_ID.md). This tool is the reader
that spends it.

Surfaces read (a missing file reads as empty, never as an error):

    trajectory  memory/trajectory/steps.jsonl   every Bash step (command lines)
    burns       memory/burns/LEDGER.jsonl       burn verdict receipts (pre-AH14:
                                               no corr_id, joins by path/time)
    gameflow    memory/game/FLOW_LEDGER.jsonl   AH14's corr-carrying burns writer
    duel        logs/duel/duels.jsonl           model duels + judge verdicts

Note on the two "burns" ledgers: the AH14 corr stamp lives on the game-flow
writer (memory/game/FLOW_LEDGER.jsonl); memory/burns/LEDGER.jsonl is the
burn-receipt ledger the IMP4 brief named. Both are read so corr joins bind
the real AH14 streams AND the receipt rows still surface via path/time
joins. Old rows without corr_id read as null (absent = null, AH14 law) and
surface via --path; readers never break on either shape.

Queries (filters AND together; one is required — the unfiltered dump is
refused on purpose):

    python tools/estate_query.py query --corr deadbeef
    python tools/estate_query.py query --path tools/workflow_gate.py
    python tools/estate_query.py query --since 2026-09-30 --model glm-5.3-prime

Output: per-surface matched counts (the rollup) then ONE merged timeline,
oldest first, one line per event: ts, surface, kind, summary. Bad JSONL
lines are skipped and counted, never fatal (the live steps stream carries
34 of them at IMP4 time). Zero matches prints an explicit 0-rows line —
an honest empty, never a fabricated one.

Exit codes: 0 query ran (empty result included), 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SURFACE_FILES: tuple[tuple[str, str], ...] = (
    ("trajectory", "memory/trajectory/steps.jsonl"),
    ("burns", "memory/burns/LEDGER.jsonl"),
    ("gameflow", "memory/game/FLOW_LEDGER.jsonl"),
    ("duel", "logs/duel/duels.jsonl"),
)

SUMMARY_LIMIT = 140
DEFAULT_LIMIT = 200
# aware sentinel so ts-less rows sort after every dated row, deterministically
_TS_MAX = datetime.max.replace(tzinfo=timezone.utc)


@dataclass
class Event:
    """One provenance row, normalized for the merged timeline."""

    ts: datetime | None
    ts_raw: str
    surface: str
    kind: str
    summary: str
    corr_id: str | None
    text: str  # compact row JSON, the --path/--model match basis


def surface_paths(root: Path = ROOT) -> dict[str, Path]:
    return {name: root / rel for name, rel in SURFACE_FILES}


def parse_ts(raw) -> datetime | None:
    """ISO-8601 to aware UTC datetime; naive strings read as UTC; else None."""
    if not isinstance(raw, str) or not raw.strip():
        return None
    s = raw.strip()
    if s.endswith(("Z", "z")):
        s = s[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(s)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def parse_since(raw: str) -> datetime:
    """--since argument to aware UTC datetime (date-only means midnight UTC)."""
    parsed = parse_ts(raw)
    if parsed is None:
        raise ValueError(f"--since is not an ISO date/datetime: {raw!r}")
    return parsed


def _clip(text: str, limit: int = SUMMARY_LIMIT) -> str:
    line = " ".join((text or "").split())
    return line[:limit] + ("..." if len(line) > limit else "")


def kind_of(surface: str, row: dict) -> str:
    if surface == "trajectory":
        return str(row.get("face") or "bash")
    if surface == "burns":
        return "verdict"
    if surface == "gameflow":
        return str(row.get("action") or "step")
    return "duel"


def summary_of(surface: str, row: dict) -> str:
    if surface == "trajectory":
        return _clip(row.get("command") or "(no command)")
    if surface == "burns":
        return _clip(f"{row.get('slug', '?')} [{row.get('verdict', '?')}] "
                     f"{row.get('landing') or row.get('one_line', '')}")
    if surface == "gameflow":
        parts = [str(row.get("piece") or "?")]
        if row.get("module"):
            parts.append(str(row["module"]))
        if row.get("queue_id"):
            parts.append(f"queue={row['queue_id']}")
        return _clip(" ".join(parts))
    return _clip(f"{row.get('ask_id', '?')} winner={row.get('winner', '?')} "
                 f"{row.get('a_model', '?')} vs {row.get('b_model', '?')} "
                 f"judge={row.get('judge', '?')}")


def read_surface(name: str, path: Path) -> tuple[list[Event], int]:
    """Parse one JSONL surface into Events. Bad lines are counted, not fatal."""
    if not path.is_file():
        return [], 0
    events: list[Event] = []
    skipped = 0
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                skipped += 1
                continue
            if not isinstance(row, dict):
                skipped += 1
                continue
            events.append(Event(
                ts=parse_ts(row.get("ts")),
                ts_raw=str(row.get("ts") or "-"),
                surface=name,
                kind=kind_of(name, row),
                summary=summary_of(name, row),
                corr_id=row.get("corr_id"),
                text=json.dumps(row, ensure_ascii=False, sort_keys=True),
            ))
    return events, skipped


def collect(root: Path = ROOT) -> tuple[list[Event], dict[str, int], dict[str, int]]:
    """Every event from every surface + per-surface read/skipped stats."""
    events: list[Event] = []
    read_counts: dict[str, int] = {}
    skipped: dict[str, int] = {}
    for name, path in surface_paths(root).items():
        rows, bad = read_surface(name, path)
        events.extend(rows)
        read_counts[name] = len(rows)
        skipped[name] = bad
    return events, read_counts, skipped


def query(
    root: Path = ROOT,
    corr: str | None = None,
    path: str | None = None,
    since: datetime | None = None,
    model: str | None = None,
) -> tuple[list[Event], dict]:
    """Filter the estate to one merged timeline + honest stats.

    Filters AND together. corr matches the AH14 join field (case-insensitive
    hex8). path/model are case-insensitive substrings over the row text
    (path is the legacy grep-by-path join; model catches a_model/b_model/
    judge and command lines that name a model). since drops rows whose ts
    cannot be parsed — an unverifiable time is not a match.
    """
    events, read_counts, skipped = collect(root)
    corr_l = corr.strip().lower() if corr else None
    path_l = path.strip().lower() if path else None
    model_l = model.strip().lower() if model else None
    kept: list[Event] = []
    for ev in events:
        if corr_l is not None and (ev.corr_id or "").lower() != corr_l:
            continue
        if path_l is not None and path_l not in ev.text.lower():
            continue
        if model_l is not None and model_l not in ev.text.lower():
            continue
        if since is not None:
            if ev.ts is None or ev.ts < since:
                continue
        kept.append(ev)
    kept.sort(key=lambda e: (e.ts is None, e.ts or _TS_MAX))
    matched = {name: 0 for name, _ in SURFACE_FILES}
    for ev in kept:
        matched[ev.surface] += 1
    stats = {"read": read_counts, "skipped": skipped, "matched": matched}
    return kept, stats


def _ts_label(ev: Event) -> str:
    if ev.ts is not None:
        return ev.ts.strftime("%Y-%m-%dT%H:%M:%SZ")
    return f"{ev.ts_raw:<20}"


def print_report(events: list[Event], stats: dict, limit: int,
                 filters: str) -> None:
    """Rollup per surface, then the merged timeline. 0 rows says so."""
    skipped_total = sum(stats["skipped"].values())
    matched = stats["matched"]
    rollup = " | ".join(f"{name} {matched.get(name, 0)}"
                        for name, _ in SURFACE_FILES if matched.get(name, 0))
    print(f"estate_query: {len(events)} rows matched ({filters}) | "
          f"surfaces read: {stats['read']} | bad lines skipped: {skipped_total}")
    if not events:
        print("estate_query: 0 rows matched — no fabricated rows; "
              "check the filter spelling or widen the surfaces.")
        return
    print(f"rollup: {rollup}")
    print("timeline (oldest first):")
    for ev in events[:limit]:
        print(f"{_ts_label(ev)}  {ev.surface:<10} {ev.kind:<8} {ev.summary}")
    hidden = len(events) - limit
    if hidden > 0:
        print(f"... +{hidden} more rows (raise --limit to see them)")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="estate_query",
        description="Join provenance surfaces (trajectory steps, burns, duels) "
                    "by corr_id, path substring, or time+model into one timeline.")
    sub = p.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query", help="filter the estate, print one merged timeline")
    q.add_argument("--corr", help="AH14 join field corr_id (uuid4 hex8) — joins "
                                  "rows across all corr-carrying surfaces")
    q.add_argument("--path", help="legacy join: rows whose text mentions this "
                                  "path substring (surfaces pre-AH14 rows)")
    q.add_argument("--since", help="ISO date/datetime UTC, e.g. 2026-09-30 or "
                                   "2026-09-30T12:00:00Z (date = midnight UTC)")
    q.add_argument("--model", help="substring filter on model names (duel "
                                   "contenders/judge, command lines naming a model)")
    q.add_argument("--limit", type=int, default=DEFAULT_LIMIT,
                   help=f"timeline rows to print (default {DEFAULT_LIMIT})")
    q.add_argument("--root", type=Path, default=ROOT,
                   help="repo root holding the surface files (default: this repo)")
    args = p.parse_args(argv)

    given = [flag for flag, val in (("--corr", args.corr), ("--path", args.path),
                                    ("--since", args.since), ("--model", args.model))
             if val]
    if not given:
        p.error("refusing the unfiltered dump: name --corr, --path, --since, or --model")
    try:
        since = parse_since(args.since) if args.since else None
    except ValueError as e:
        p.error(str(e))

    events, stats = query(args.root, corr=args.corr, path=args.path,
                          since=since, model=args.model)
    filters = ", ".join(given)
    print_report(events, stats, max(args.limit, 0), filters)
    return 0


if __name__ == "__main__":
    # Windows consoles default to cp1252 and summaries carry arbitrary row
    # bytes; reconfigure when possible, degrade to a note when not (never a
    # silent pass — the ratchet forbids it and the operator should know).
    if (getattr(sys.stdout, "encoding", "") or "").lower() not in ("utf-8", "utf8"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            sys.stderr.write("note: stdout encoding stays "
                             f"{getattr(sys.stdout, 'encoding', '?')}\n")
    sys.exit(main())
