"""Seed the capability ledger with synthetic fixture data.

6 synthetic models x 5 task shapes with varied plausible pass-rates,
so tests and first runs work offline with zero real API calls. All
numbers are hand-picked literals: deterministic, no RNG. last_measured
is pinned to a fixed seed date so runs are reproducible byte-for-byte
(updated_at still stamps real write time).

Usage (repo root, repo venv):
    .venv/Scripts/python.exe -m tools.gps_mcp.seed_fixtures
    .venv/Scripts/python.exe -m tools.gps_mcp.seed_fixtures --db path/to/led.db3

Idempotent: existing rows for the fixture model ids are deleted first.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):  # allow direct script execution
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools.gps_mcp.ledger import CapabilityLedger

SEED_DATE = "2026-09-28T00:00:00+00:00"

# model_id -> cost_usd_per_call (mirrors config.json so the ledger's
# cost column and the live config price never disagree for fixtures)
FIXTURE_COSTS = {
    "scut-2b": 0.00005,
    "gemma-worker-4b": 0.0002,
    "yesno-tiny": 0.00002,
    "flash-mid-1": 0.004,
    "flash-mid-2": 0.009,
    "frontier-opus": 0.12,
}

# (model_id, task_shape) -> (pass_rate, sample_size)
# Deliberately varied: tiny models shine on yes/no, collapse on design;
# the frontier wins everything but costs 30x the mid tier.
FIXTURE_RATES: dict[tuple[str, str], tuple[float, int]] = {
    ("scut-2b", "code_review"): (0.41, 64),
    ("scut-2b", "summarize"): (0.78, 120),
    ("scut-2b", "yes_no_decision"): (0.70, 150),
    ("scut-2b", "tool_call_parse"): (0.35, 40),
    ("scut-2b", "design_judgment"): (0.12, 18),
    ("gemma-worker-4b", "code_review"): (0.72, 90),
    ("gemma-worker-4b", "summarize"): (0.90, 140),
    ("gemma-worker-4b", "yes_no_decision"): (0.83, 110),
    ("gemma-worker-4b", "tool_call_parse"): (0.66, 55),
    ("gemma-worker-4b", "design_judgment"): (0.30, 24),
    ("yesno-tiny", "code_review"): (0.18, 30),
    ("yesno-tiny", "summarize"): (0.12, 22),
    ("yesno-tiny", "yes_no_decision"): (0.94, 160),
    ("yesno-tiny", "tool_call_parse"): (0.09, 20),
    ("yesno-tiny", "design_judgment"): (0.05, 16),
    ("flash-mid-1", "code_review"): (0.88, 75),
    ("flash-mid-1", "summarize"): (0.93, 130),
    ("flash-mid-1", "yes_no_decision"): (0.89, 95),
    ("flash-mid-1", "tool_call_parse"): (0.90, 60),
    ("flash-mid-1", "design_judgment"): (0.61, 35),
    ("flash-mid-2", "code_review"): (0.91, 80),
    ("flash-mid-2", "summarize"): (0.90, 125),
    ("flash-mid-2", "yes_no_decision"): (0.86, 100),
    ("flash-mid-2", "tool_call_parse"): (0.87, 58),
    ("flash-mid-2", "design_judgment"): (0.72, 42),
    ("frontier-opus", "code_review"): (0.97, 50),
    ("frontier-opus", "summarize"): (0.96, 45),
    ("frontier-opus", "yes_no_decision"): (0.95, 40),
    ("frontier-opus", "tool_call_parse"): (0.98, 48),
    ("frontier-opus", "design_judgment"): (0.96, 52),
}


def seed(db_path: str | Path) -> int:
    ledger = CapabilityLedger(db_path)
    conn = ledger.connection()
    with conn:
        placeholders = ",".join("?" for _ in FIXTURE_COSTS)
        conn.execute(
            f"DELETE FROM capability WHERE model_id IN ({placeholders})",
            tuple(FIXTURE_COSTS),
        )
    count = 0
    for (model_id, task_shape), (rate, size) in sorted(FIXTURE_RATES.items()):
        ledger.upsert_measurement(
            model_id=model_id,
            task_shape=task_shape,
            pass_rate=rate,
            sample_size=size,
            cost_usd_per_call=FIXTURE_COSTS[model_id],
            last_measured=SEED_DATE,
        )
        count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="seed gps-mcp ledger fixtures")
    parser.add_argument(
        "--db",
        default=str(Path(__file__).resolve().parent / "gps_ledger.db3"),
        help="path to the ledger sqlite file (default: package-local gps_ledger.db3)",
    )
    args = parser.parse_args(argv)
    count = seed(args.db)
    print(f"seeded {count} fixture rows into {args.db}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
