#!/usr/bin/env python3
"""break-communication hostile probe (ouroboros R3): byte-check the lens's
fold claims by importing the fold instrument's own functions.

Read-only over all run archives; reports per-archive deep_tier2 census
(total, verdict split, joining vs orphan) and the crash-key join proof
using a REAL claim from the 2026-10-04-0 archive.
"""
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO))

from tools.mickey17_v2_fold import RUN_ROOT, load_lanes, load_checks, norm  # noqa: E402


def deep_keys(lid, claim):
    # byte-faithful copy of tools/mickey17_v2_fold.py:339-342 (nested in
    # main(), so not importable); the authoritative check is the full fold
    # execution on the temp archive copy, which does not use this copy.
    c = str(claim or "")
    return {norm(lid + ": " + " ".join(c.split(" ")[:6])),
            norm(lid + ": " + " ".join(c.split()[:6]))}


def census(run_dir: Path) -> dict:
    lanes_dir = run_dir / "lanes"
    lanes = load_lanes(lanes_dir)
    checks = load_checks(lanes_dir)
    rows_by_lane = {}
    for lid, l in lanes.items():
        rows_by_lane[lid] = [r for r in l.get("rows", []) if isinstance(r, dict)]
    total = 0
    verdicts = Counter()
    joining = Counter()
    orphan = Counter()
    join_hits = Counter()
    for lid, c in checks.items():
        for x in (c.get("deep_tier2") or []):
            if not isinstance(x, dict):
                continue
            total += 1
            v = (x.get("verdict") or "").strip() or "?"
            verdicts[v] += 1
            rk = norm(str(x.get("row_key", "")))
            if not rk:
                orphan[v + " (empty row_key)"] += 1
                continue
            hits = 0
            for r in rows_by_lane.get(lid, []):
                if deep_keys(lid, r.get("claim")) & {rk}:
                    hits += 1
            if hits:
                joining[v] += 1
                join_hits[v] += hits
            else:
                orphan[v] += 1
    return {"total": total, "verdicts": dict(verdicts), "joining": dict(joining),
            "join_hits": dict(join_hits), "orphan": dict(orphan),
            "rows": sum(len(v) for v in rows_by_lane.values())}


def main() -> int:
    runs = RUN_ROOT / "runs"
    for run_dir in sorted(runs.iterdir()):
        if not (run_dir / "lanes").is_dir():
            continue
        c = census(run_dir)
        print(f"== {run_dir.name}: rows={c['rows']} deep_tier2={c['total']} "
              f"verdicts={c['verdicts']} joining={c['joining']} "
              f"(row hits {c['join_hits']}) orphan={c['orphan']}")

    # crash-key proof on real bytes: a crashed entry mints '<lane>: crashed';
    # can that key EVER join a lane row's six-word key? Take the real lane +
    # real first claim from 2026-10-04-0 and test both directions.
    probe_dir = runs / "2026-10-04-0"
    lanes = load_lanes(probe_dir / "lanes")
    lid0 = next(iter(sorted(lanes)))
    claim0 = (lanes[lid0]["rows"][0].get("claim") or "")
    crash_key = norm(lid0 + ": crashed")
    joined = crash_key in deep_keys(lid0, claim0)
    print(f"crash-key proof: lane={lid0} claim[:60]={claim0[:60]!r}")
    print(f"  norm('{lid0}: crashed') in deep_keys(lane, claim) = {joined}")
    # also: does any row_key in ANY archive literally end ': crashed'?
    crash_shaped = 0
    for run_dir in sorted(runs.iterdir()):
        if not (run_dir / "lanes").is_dir():
            continue
        for c in load_checks(run_dir / "lanes").values():
            for x in (c.get("deep_tier2") or []):
                if isinstance(x, dict) and norm(str(x.get("row_key", ""))).endswith(": crashed"):
                    crash_shaped += 1
    print(f"  row_keys literally ending ': crashed' across all archives: {crash_shaped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
