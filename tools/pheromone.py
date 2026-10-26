#!/usr/bin/env python3
"""pheromone: the swarm's attention bus (operator order 2026-10-07).

"Workflows give clear rules for bounded tasks - those outputs should be
PHEROMONE SIGNALS for the swarm: which items need attention next. Let
MULTIPLE solve it and take the best answer."

The ant-colony semantics:
  deposit   - any run/lane/lens drops a signal: this needs attention.
  reinforce - another arm hits the same item: heat rises (the Merkle
              triple-arm is the proof pattern - independent hits on one
              line are worth more than one).
  decay     - heat decays exponentially with age (the D7 GPS metabolism:
              law 10-05, not stamped until now): unsolved items stay warm
              only while unsolved.
  hottest   - the gradient: rank by decayed heat. The swarm reads THIS.
  claim     - a solver takes an item (instance-guard style, non-exclusive:
              MULTIPLE solvers may attempt one item - best answer wins at
              the fold, redundancy is the design, not a bug).
  solved    - mark with evidence; a solved item's heat collapses.

Store: memory/pheromone/pheromones.jsonl (append-only) + computed ranks.
Stdlib only. The bus never solves anything - it is the smell, not the legs.

Usage:
  python -m tools.pheromone deposit --id <item> --source <who> [--note ...]
  python -m tools.pheromone reinforce --id <item> --source <who>
  python -m tools.pheromone solved --id <item> --evidence <path-or-hash>
  python -m tools.pheromone hottest [--n 10]
  python -m tools.pheromone show --id <item>
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STORE = ROOT / "memory" / "pheromone" / "pheromones.jsonl"

# D7 metabolism: heat half-life in hours. An unsolved signal at 24h carries
# 1/16 of its original pull - old silence stops shouting.
HALF_LIFE_H = 6.0


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.isoformat().replace("+00:00", "Z")


def _parse(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
    except Exception:
        return None


def _load() -> list[dict]:
    if not STORE.exists():
        return []
    rows = []
    for line in STORE.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows


def _append(row: dict) -> None:
    STORE.parent.mkdir(parents=True, exist_ok=True)
    with open(STORE, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, sort_keys=True) + "\n")


def decayed_heat(events: list[dict], now: datetime) -> float:
    """Sum of every deposit/reinforce, each decayed from its moment to now.
    SOLVED items radiate zero: the swarm stops smelling them."""
    status = next((e for e in reversed(events) if e.get("type") == "solved"), None)
    if status:
        return 0.0
    heat = 0.0
    for e in events:
        if e.get("type") not in ("deposit", "reinforce"):
            continue
        ts = _parse(str(e.get("ts", "")))
        if ts is None:
            continue
        age_h = max(0.0, (now - ts).total_seconds()) / 3600.0
        heat += float(e.get("heat", 1.0)) * math.pow(0.5, age_h / HALF_LIFE_H)
    return heat


def cmd_deposit(args) -> int:
    _append({"type": "deposit", "id": args.id, "source": args.source,
             "ts": _iso(_now()), "heat": 1.0, "note": args.note or ""})
    print(f"DEPOSIT: {args.id} (source {args.source})")
    return 0


def cmd_reinforce(args) -> int:
    _append({"type": "reinforce", "id": args.id, "source": args.source,
             "ts": _iso(_now()), "heat": 1.0})
    print(f"REINFORCE: {args.id} (source {args.source})")
    return 0


def cmd_solved(args) -> int:
    _append({"type": "solved", "id": args.id, "source": args.source,
             "ts": _iso(_now()), "evidence": args.evidence})
    print(f"SOLVED: {args.id} (evidence {args.evidence})")
    return 0


def cmd_hottest(args) -> int:
    rows = _load()
    now = _now()
    by_id: dict[str, list[dict]] = {}
    for r in rows:
        by_id.setdefault(str(r.get("id")), []).append(r)
    ranked = []
    for iid, events in by_id.items():
        heat = decayed_heat(events, now)
        if heat <= 0:
            continue
        meta = next((e for e in reversed(events) if e.get("note")), {})
        ranked.append({"id": iid, "heat": round(heat, 4),
                       "sources": len({e.get("source") for e in events
                                       if e.get("type") in ("deposit", "reinforce")}),
                       "note": str(meta.get("note", ""))[:120]})
    ranked.sort(key=lambda r: -r["heat"])
    for r in ranked[: args.n]:
        print(json.dumps(r))
    print(f"PARAMONE-HOTTEST: {len(ranked)} hot items (half-life {HALF_LIFE_H}h)")
    return 0


def cmd_show(args) -> int:
    for e in _load():
        if str(e.get("id")) == args.id:
            print(json.dumps(e))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    d = sub.add_parser("deposit")
    d.add_argument("--id", required=True)
    d.add_argument("--source", required=True)
    d.add_argument("--note", default="")
    r = sub.add_parser("reinforce")
    r.add_argument("--id", required=True)
    r.add_argument("--source", required=True)
    s = sub.add_parser("solved")
    s.add_argument("--id", required=True)
    s.add_argument("--source", default="seat")
    s.add_argument("--evidence", default="")
    h = sub.add_parser("hottest")
    h.add_argument("--n", type=int, default=10)
    sh = sub.add_parser("show")
    sh.add_argument("--id", required=True)
    args = ap.parse_args()
    return {"deposit": cmd_deposit, "reinforce": cmd_reinforce,
            "solved": cmd_solved, "hottest": cmd_hottest,
            "show": cmd_show}[args.mode](args)


if __name__ == "__main__":
    sys.exit(main())
