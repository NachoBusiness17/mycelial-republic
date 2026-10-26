"""B2-217 probe: read-only pre-verification for the guard-bearing W40 stamp run.

Discipline: probe-then-edit (the B2-68 pattern). This script writes nothing.
It reads real bytes, reproduces the live T6 number the brief names, runs the
guard dry at both candidate W40 run dates, and prints the sensitivity table
the receipt's T6-recovery judgment rests on.
"""
from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import tools.drift_pairs_stamp as dps  # noqa: E402


def load(path: Path) -> list[dict]:
    return dps._read_jsonl(path)


def series_table(built: dict) -> list[tuple[str, int, int]]:
    return [(d.isoformat(), m, r)
            for d, m, r in zip(built["span"], built["metric"], built["referent"])]


def main() -> int:
    print("== probe B2-217, read-only, no writes ==")

    # ---- live T6 reproduction from bytes
    t6 = dps.pair_t6()
    live = dps.drift_check(t6["metric"], t6["referent"], label="T6 live probe")
    print("T6 live:", json.dumps({k: live[k] for k in
                                  ("verdict", "corr_dm_dr", "deltas_used")}))
    burns = load(dps.BURNS)
    steps = load(dps.STEPS)
    burn_d = dps._dates_of(burns, "ts")
    step_d = dps._dates_of(steps, "ts")
    print("burns rows:", len(burns), "dated:", len(burn_d),
          "min:", min(burn_d), "max:", max(burn_d))
    print("steps rows:", len(steps), "dated:", len(step_d),
          "min:", min(step_d), "max:", max(step_d))
    print("T6 window (date, metric=fold steps, referent=burn receipts):")
    for row in series_table(t6):
        print("  ", row)
    nonzero_ref = [(d, r) for d, m, r in series_table(t6) if r]
    print("T6 referent nonzero days:", nonzero_ref)

    # ---- sensitivity: how much of the corr is the two flood days
    def corr_excluding(after: date) -> dict:
        bd = [d for d in burn_d if d < after]
        sd = [d for d in step_d if d < after]
        span = dps._aligned_window(sd, bd, 21)
        return dps.drift_check(dps._counts(sd, span), dps._counts(bd, span),
                               label=f"T6 frozen before {after}")

    for cut in (date(2026, 9, 25), date(2026, 9, 26)):
        v = corr_excluding(cut)
        print(f"T6 with both layers frozen before {cut}:",
              json.dumps({k: v[k] for k in ("verdict", "corr_dm_dr", "deltas_used")}))

    # ---- guard dry-run at both candidate W40 run dates (no writes)
    for run in (date(2026, 9, 28), date(2026, 10, 1)):
        print(f"-- dry guard run for week {dps._week_key(run)}, run_date {run}")
        for pid, spec in dps.PAIRS.items():
            built = spec["build"]()
            verdict = dps.drift_check(built["metric"], built["referent"],
                                      label=f"{pid} dry")
            age = dps._referent_age_days(built.get("referent_first"), run)
            guarded = dps._apply_aging_guard(verdict, age)
            print(f"   {pid} raw={verdict.get('verdict')} corr={verdict.get('corr_dm_dr')} "
                  f"age={age} guarded={guarded.get('verdict')} "
                  f"downgraded={guarded is not verdict}")

    # ---- idempotency precheck: what is already stamped
    rows = load(dps.LEDGER)
    print("already stamped keys:", sorted(dps._stamped_keys(rows)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
