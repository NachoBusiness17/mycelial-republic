"""Cost-per-commit scan over memory/runs/hermes_burn/usage.jsonl (moonshot-1 dogfood).

Buckets every usage row into the six-commit window (2026-09-30T20:00Z to
2026-10-02T11:00Z), sums cost and tokens per commit leg, and censuses doubled
(id, turn) keys. Read-only; no subprocess spawns.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"

BOUNDS = [
    ("pre-window", None),
    ("->5d2263f10 GAP ANALYSIS", "2026-10-02T00:46:30Z"),
    ("->962e41054 LIBRARIAN", "2026-10-02T00:54:07Z"),
    ("->f4cfcdf9b RACTORSWARM", "2026-10-02T01:57:07Z"),
    ("->0c9d72a06 MODEL GARDEN", "2026-10-02T04:18:32Z"),
    ("->3c83da5b0 FILL-BALL", "2026-10-02T06:54:04Z"),
    ("->e3c7d341c RACTOR DOGFOOD", "2026-10-02T07:31:54Z"),
    ("post-e3c7d341c to 11:00Z", "2026-10-02T11:00:00Z"),
]


def parse(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def main() -> None:
    rows = []
    with USAGE.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    w_start = parse("2026-09-30T20:00:00Z")
    w_end = parse("2026-10-02T11:00:00Z")

    buckets: dict[str, list[dict]] = defaultdict(list)
    pre = 0
    post = 0
    for r in rows:
        ts = parse(r["ts"])
        if ts < w_start:
            pre += 1
            continue
        if ts >= w_end:
            post += 1
            continue
        placed = False
        for i, (_, edge) in enumerate(BOUNDS):
            if edge is None:
                continue
            if ts < parse(edge):
                buckets[BOUNDS[i][0]].append(r)
                placed = True
                break
        if not placed:
            buckets["post-e3c7d341c to 11:00Z"].append(r)

    total_cost = 0.0
    total_tok = 0
    print(f"rows={len(rows)} pre-window={pre} post-window={post}")
    for name, _ in BOUNDS:
        items = buckets.get(name, [])
        if not items:
            print(f"{name:34s} rows=0 cost=$0 tokens=0")
            continue
        cost = sum(float(r.get("cost_usd") or 0) for r in items)
        tok = sum(
            int(r.get("prompt_tokens") or 0) + int(r.get("completion_tokens") or 0)
            for r in items
        )
        total_cost += cost
        total_tok += tok
        print(f"{name:34s} rows={len(items):3d} cost=${cost:8.4f} tokens={tok:,}")

    print(f"{'WINDOW TOTAL':34s} cost=${total_cost:.4f} tokens={total_tok:,}")

    # doubled (id, turn) census across the window
    key_counts: Counter[tuple[str, int]] = Counter()
    key_cost: dict[tuple[str, int], float] = {}
    for r in rows:
        ts = parse(r["ts"])
        if ts < w_start or ts >= w_end:
            continue
        k = (str(r.get("id")), int(r.get("turn") or 0))
        key_counts[k] += 1
        key_cost[k] = key_cost.get(k, 0.0) + float(r.get("cost_usd") or 0)
    doubled = {k: c for k, c in key_counts.items() if c > 1}
    excess = 0.0
    for k, c in doubled.items():
        per = key_cost[k] / c
        excess += per * (c - 1)
    print(f"doubled (id,turn) keys in window: {len(doubled)}; excess-pair cost ~${excess:.4f}")

    # hermes ledger grand total for context
    grand = sum(float(r.get("cost_usd") or 0) for r in rows)
    print(f"usage.jsonl grand total (all rows): ${grand:.4f}")


if __name__ == "__main__":
    main()
