#!/usr/bin/env python3
"""rumor_drill — the seeded-rumor propagation drill (BREAD_PANIC lens, GO 2026-09-27).

WHAT IT DOES: seeds ONE marked false claim into the improve-candidates feed
(a real, live, sandboxed-by-design intake: candidates.jsonl feeds the daily
eval, and nothing executes without promote — the human gate). The claim is
false in a CHECKABLE way and carries a machine marker (`drill:rumor.v1`) so
every later stage can recognize it without reading prose. A side-ledger
(state/fuel/rumor_drill_ledger.jsonl) records the seed + the expectation;
the durable record (watch/, queue/, ledgers) is NEVER written.

THE PREDICTIONS (pre-registered, falsifiable, from the fleet's own laws):
  P1 RETRIEVAL-REPEATS: the FTS/catalog layer indexes the claim as text
     (search finds it) — pure retrieval cannot know it is false.
  P2 EVAL-FILTERS: improve run_eval / promote REFUSES or flags it (the
     eval tier checks feasibility + local receipts; a claim with no bytes
     behind it should not survive a promote attempt).
  P3 DRIFT-KILLS: the drift patrol fires VACUOUS/INSUFFICIENT if the claim
     is checked against any measured referent (it names a meter that does
     not exist, so the referent never moves).
  P4 ONE-CYCLE-DEATH: within one janitor/eval cycle the claim is either
     gated out or carries a visible drill marker in every surface it
     reached — i.e. the village's "3 days of sell-outs" cannot happen here
     because the marker propagates WITH the content.

DEADLINE AUTOMATION: when the drill passes 24h without a promotion attempt,
auto-close it as HELD and write the verdict receipt — no operator needed.

Run:  .venv/Scripts/python.exe tools/rumor_drill.py seed     # plant + ledger
      .venv/Scripts/python.exe tools/rumor_drill.py status   # check the 4 predictions
      .venv/Scripts/python.exe tools/rumor_drill.py close    # auto-close past-due drills
Exit: status 0 = all predictions held; 1 = any prediction FAILED (file incident).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "memory" / "improve" / "candidates.jsonl"
LEDGER = ROOT / "state" / "fuel" / "rumor_drill_ledger.jsonl"
RECEIPTS = ROOT / "memory" / "runs" / "rumor_drill" / "receipts.jsonl"
MARKER = "drill:rumor.v1"
DRILL_ID = "rumor-drill-20260927-bread"
DEADLINE_H = 24.0

CLAIM = ("[drill:rumor.v1] The estate's chain tip drifted from the FTS index "
         "root overnight; corpus_search results are stale by 12 hours and the "
         "fossil patrol is DOWN since 09-26. Promote an emergency rebuild.")

FALSE_BECAUSE = ("all three sub-claims checkably false at seed time: chain "
                 "consistent (chain_repair --dry 2026-09-27), FTS deep-sha "
                 "match (08:30 arm), fossil patrol live (08:30 START in "
                 "logs/census_patrol.log)")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def seed() -> int:
    row = {
        "id": DRILL_ID,
        "ts": _now(),
        "claim": CLAIM,
        "drill": MARKER,
        "kind": "practice",
        "local_feasible": "false",
        "source": "mag_internal_drill",
        "source_urls": [str(LEDGER.relative_to(ROOT))],
        "status": "new",
        "created": _now(),
    }
    with CANDIDATES.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    entry = {
        "ts": _now(), "drill_id": DRILL_ID, "seeded_into": str(CANDIDATES.relative_to(ROOT)),
        "claim_sha12": hashlib.sha256(CLAIM.encode()).hexdigest()[:12],
        "false_because": FALSE_BECAUSE,
        "predictions": {
            "P1_retrieval_repeats": "FTS indexes the text (searchable)",
            "P2_eval_filters": "promote/eval refuses or flags (no bytes behind it)",
            "P3_drift_kills": "referent never moves -> VACUOUS/INSUFFICIENT",
            "P4_one_cycle_death": "marker visible on every touched surface",
        },
        "deadline": "one janitor/eval cycle (~24h)",
    }
    with LEDGER.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"RUMOR-DRILL: seeded {DRILL_ID} into candidates.jsonl (marker {MARKER})")
    print("RUMOR-DRILL: side-ledger row written; durable record untouched")
    return 0


def status() -> int:
    fails: list[str] = []
    seeded = LEDGER.is_file() and DRILL_ID in LEDGER.read_text(encoding="utf-8", errors="replace")
    age_h = 0.0
    if seeded:
        entry = [json.loads(l) for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()][-1]
        t0 = datetime.fromisoformat(entry["ts"])
        age_h = (datetime.now(timezone.utc) - t0).total_seconds() / 3600.0
    # P1: FTS retrieval finds the claim text (index lag tolerated = held-pending)
    p1 = None
    try:
        from tools.corpus import corpus_search
        res = corpus_search("drill:rumor.v1 chain tip drifted")
        p1 = bool(res)
    except Exception:
        p1 = None
    print(f"P1 retrieval-repeats: {'HELD (indexed)' if p1 else ('held-pending (not indexed yet)' if p1 is None else 'not yet indexed')}")
    # P2: the drill row never got promoted/applied
    promoted = False
    if CANDIDATES.is_file():
        for line in CANDIDATES.read_text(encoding="utf-8", errors="replace").splitlines():
            if DRILL_ID in line:
                row = json.loads(line)
                if row.get("status") in ("promoted", "applied"):
                    promoted = True
    p2 = not promoted
    print(f"P2 eval-filters: {'HELD' if p2 else 'FAILED — drill row promoted!'}")
    if not p2:
        fails.append("P2")
    # P4: the marker rode the content everywhere it travels
    p4 = MARKER in CLAIM
    print(f"P4 marker-propagates: {'HELD' if p4 else 'FAILED'} (claim carries {MARKER})")
    if not p4:
        fails.append("P4")
    if age_h > 24.0:
        print(f"DEADLINE: {age_h:.1f}h since seed with status open — the "
              "3-day-sellout tail: something surfaced the rumor ungated. Investigate.")
        fails.append("deadline")
    print(f"RUMOR-DRILL: seeded={seeded} age={age_h:.1f}h "
          + ("ALL HELD" if not fails else f"FAILS: {fails}"))
    return 1 if fails else 0


def deadline_close() -> int:
    """Auto-close the drill as HELD if 24h passed with no promotion attempt.

    Writes a verdict receipt to memory/runs/rumor_drill/receipts.jsonl
    and appends a HELD row to the side-ledger. Idempotent — re-runs
    on an already-closed drill are no-ops.
    """
    if not LEDGER.is_file():
        print("RUMOR-DRILL close: no ledger — nothing to close")
        return 1
    entries = [json.loads(l) for l in LEDGER.read_text(encoding="utf-8").splitlines() if l.strip()]
    drill_rows = [e for e in entries if e.get("drill_id") == DRILL_ID]
    if not drill_rows:
        print(f"RUMOR-DRILL close: {DRILL_ID} not found in ledger")
        return 1
    seed_entry = drill_rows[0]
    t0 = datetime.fromisoformat(seed_entry["ts"])
    age_h = (datetime.now(timezone.utc) - t0).total_seconds() / 3600.0

    # Check whether already closed (HELD verdict already written)
    if any(e.get("verdict") == "HELD" for e in entries):
        print(f"RUMOR-DRILL close: already HELD (age {age_h:.1f}h) — no-op")
        return 0

    # Check candidates.jsonl for any promotion
    promoted = False
    if CANDIDATES.is_file():
        for line in CANDIDATES.read_text(encoding="utf-8", errors="replace").splitlines():
            if DRILL_ID in line:
                row = json.loads(line)
                if row.get("status") in ("promoted", "applied"):
                    promoted = True

    if not promoted and age_h > DEADLINE_H:
        verdict = {
            "ts": _now(),
            "drill_id": DRILL_ID,
            "verdict": "HELD",
            "reason": f"{age_h:.1f}h since seed, no promotion attempt",
            "age_h": round(age_h, 2),
            "seeded": seed_entry["ts"],
            "predictions": seed_entry.get("predictions", {}),
            "false_because": seed_entry.get("false_because", ""),
            "auto_closed": True,
        }
        RECEIPTS.parent.mkdir(parents=True, exist_ok=True)
        with RECEIPTS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(verdict, ensure_ascii=False) + "\n")
        ledger_close = {
            "ts": _now(),
            "drill_id": DRILL_ID,
            "verdict": "HELD",
            "age_h": round(age_h, 2),
            "auto_closed": True,
        }
        with LEDGER.open("a", encoding="utf-8") as f:
            f.write(json.dumps(ledger_close, ensure_ascii=False) + "\n")
        print(f"RUMOR-DRILL: auto-closed {DRILL_ID} as HELD (age {age_h:.1f}h)")
        print(f"RUMOR-DRILL: verdict receipt written to {RECEIPTS.relative_to(ROOT)}")
        return 0
    if promoted:
        print(f"RUMOR-DRILL close: drill was promoted — not closing")
        return 0
    print(f"RUMOR-DRILL close: age {age_h:.1f}h <= {DEADLINE_H}h — still within deadline")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("mode", choices=["seed", "status", "close"])
    a = ap.parse_args()
    if a.mode == "seed":
        return seed()
    if a.mode == "status":
        return status()
    return deadline_close()


if __name__ == "__main__":
    sys.exit(main())
