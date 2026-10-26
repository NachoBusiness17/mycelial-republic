#!/usr/bin/env python3
"""shape_tripwire: the GPS-EMBED cold-start crossover counter (compost 2026-10-09).

The GPS-EMBED substrate (EmbeddingGemma-2 vector-key GPS router) was killed
2026-10-07 by its own filed falsifier: string keys 210/210 vs embedding-kNN
208/210 on held-out rows, 74-97 ms/ask against the 5 ms bar, and the thesis's
own cold-start regime (leave-one-shape-out) scored 2.84 pct - at 10
task_shapes the string keys ARE the coordinates (receipt
watch/inbox/gps_embed/GPS_EMBED_TRIAL.md section 4 VERDICT: KILL). The kill
was cheap because the revival condition was filed at death: the ledger row
(watch/inbox/compost_20260109/COMPOST_LEDGER.jsonl, id gps-embed-substrate)
names it - "gps ledger grows semantic shape families with shared winners
(distinct task_shapes explodes); rerun python -m tools.gps_mcp.gps_embed_trial".

This tool is that condition made countable (COMPOST_MAP.md section 5,
revival 1). It reads the production gps ledger verdict_log READ-ONLY (same
law as the trial: production bytes untouched, tools/gps_mcp/gps_ledger.db3)
and counts DISTINCT task_shapes that meet the evidence gate: at least
MIN_ROWS verdict rows each. The gate matches the router's evidence-gate
shape (ml3, git 9bac820a1: "evidence gate >=5 rows per shape") - a shape
backed by a handful of rows is not evidence that winner clustering exists.

When the gated count reaches CROSSOVER_MIN the trial's premise has room to
flip (more shapes = more room for semantic families with shared winners),
so the run appends one memory/attention.md line and exits 1, same shape as
the disk_smith alert. NO scheduled task is registered for this tool by
design: the operator runs it by hand until he says otherwise (revival lane
order 2026-10-09).

Usage:
  python -m tools.shape_tripwire            # count; breach appends attention, exit 1
  python -m tools.shape_tripwire --dry      # print the count, never write, exit 0
  python -m tools.shape_tripwire --db PATH  # count an alternate ledger copy

Exit: 0 quiet / 1 breach (attention line written) / 2 cannot-verify
(missing or unreadable ledger - an incident to fix, not a clean reading).
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# The production GPS ledger the trial itself read (GPS_EMBED_TRIAL section 2:
# "tools/gps_mcp/gps_ledger.db3 verdict_log ... read-only opens; production
# bytes untouched").
LEDGER = ROOT / "tools" / "gps_mcp" / "gps_ledger.db3"
ALERT = ROOT / "memory" / "attention.md"

# Evidence gate: minimum verdict_log rows backing a shape before it counts
# toward the crossover (router evidence-gate shape, git 9bac820a1).
MIN_ROWS = 5
# Crossover tripwire: at trial time the ledger held 10 distinct shapes and
# the cold-start arm scored 2.84 pct; the compost map's revival-1 pre-warm
# named "25+ shapes with winner clustering" as the page-the-operator level.
CROSSOVER_MIN = 25

TRIAL_COMMAND = "python -m tools.gps_mcp.gps_embed_trial"
TRIAL_RECEIPT = "watch/inbox/gps_embed/GPS_EMBED_TRIAL.md"


def count_shapes(db_path: str | Path) -> dict:
    """Read-only census of the ledger's task_shapes.

    Returns {"db": path, "verdict_rows": total, "distinct_shapes": all,
    "gated_shapes": shapes with >= MIN_ROWS rows, "counts": per-shape row
    counts for the gated shapes}. Opens the file in SQLite read-only URI
    mode so a wrong path can never create or mutate a ledger. Raises
    FileNotFoundError / sqlite3.Error upward; the CLI maps those to exit 2
    (cannot-verify), the census-patrol convention for a broken instrument
    rather than a quiet zero.
    """
    path = Path(db_path)
    if not path.is_file():
        raise FileNotFoundError(f"ledger not found: {path}")
    conn = sqlite3.connect(f"file:{path.as_posix()}?mode=ro", uri=True)
    try:
        rows = conn.execute(
            "SELECT task_shape, COUNT(*) AS n FROM verdict_log"
            " GROUP BY task_shape ORDER BY n DESC, task_shape ASC"
        ).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM verdict_log").fetchone()[0]
    finally:
        conn.close()
    gated = [(shape, int(n)) for shape, n in rows if int(n) >= MIN_ROWS]
    return {
        "db": str(path),
        "verdict_rows": int(total),
        "distinct_shapes": len(rows),
        "gated_shapes": len(gated),
        "counts": {shape: n for shape, n in gated},
        "min_rows": MIN_ROWS,
        "crossover_min": CROSSOVER_MIN,
    }


def breach(census: dict) -> bool:
    """Does the gated shape count reach the crossover tripwire?"""
    return int(census["gated_shapes"]) >= CROSSOVER_MIN


def attention_line(census: dict) -> str:
    """The one attention.md line a breach appends (disk_smith alert shape)."""
    stamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    n = int(census["gated_shapes"])
    return (
        f"- {stamp} SHAPE_TRIPWIRE GPS-EMBED cold-start crossover near: "
        f"{n} distinct shapes; rerun the one-command trial "
        f"({TRIAL_COMMAND}; receipt {TRIAL_RECEIPT})"
    )


def run(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry", action="store_true",
                    help="print the count, never write attention, exit 0")
    ap.add_argument("--db", type=Path, default=LEDGER,
                    help=f"gps ledger db to read (default {LEDGER})")
    args = ap.parse_args(argv)

    try:
        census = count_shapes(args.db)
    except (FileNotFoundError, sqlite3.Error) as exc:
        # Cannot-verify (census-patrol convention, exit 2): a missing or
        # unreadable ledger is an incident to fix, never a clean zero-count
        # reading that would silently disarm the tripwire.
        print(f"CANNOT-VERIFY: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(census, ensure_ascii=False, sort_keys=True))

    if not breach(census):
        return 0

    line = attention_line(census)
    print("ALERT: " + line)
    if args.dry:
        return 0
    ALERT.parent.mkdir(parents=True, exist_ok=True)
    with open(ALERT, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return 1


def main() -> int:
    return run(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
