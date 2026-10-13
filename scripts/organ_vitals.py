"""ORGAN VITALS — the liveness spine (self-steal of dead_hand.py, 2026-09-13).

Bones stolen from scripts/dead_hand.py: read real surfaces, fail safe,
be LOUD on breach. The reinterpretation: dead_hand watches ONE heart (the
operator's voice); organ_vitals watches EVERY organ's heartbeat. This is
the W-fold's prescribed minimum detection organ: registry of
organ -> path -> max_age, ticked on existing cron slots, breaches produce
hash-chained alert rows the ack/reaper loop screams.

Two structural absences it closes (W-fold "corruption genesis"):
  (a) health self-reported by the thing it describes -> vitals reads file
      mtimes, not self-reports.
  (b) freshness with no TTL -> every organ here carries a max_age.

Breach rows append to logs/failure_kb_alerts.jsonl with sig "vitals:<organ>"
so the EXISTING alert_reader -> ack_reaper loop acks and screams them.
Self-watch: the face (dashboard/static/organ_vitals.json) carries its own
generated_at — a stale or missing face is itself the alarm; the night
shift's wire line is its witness.

$0. Read-only except its own outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

# (name, path, max_age_hours). Paths audited against the real tree 09-13.
# A path that does not exist at all = DARK (cite_gate is the standing specimen).
ORGANS: list[tuple[str, str, float]] = [
    ("chain", "memory/biography/verkle_chain.jsonl", 30),
    ("convo_wire", "queue/handoff/zcode/CONVO.md", 30),
    ("overseer", "dashboard/static/overseer.json", 30),
    ("refeed_guard", "state/refeed_guard_latest.json", 120),  # Sep-8 re-arm was its last act
    ("cite_gate", "memory/runs/cite_gate_latest.json", 120),
    ("m12_baseline", "state/m12_baseline.jsonl", 30),
    ("operator_pulse", "state/operator_pulse.json", 48),
    ("dead_hand_state", "state/dead_hand_state.json", 25),  # night shift ticks 3x
    ("trailer_telemetry", "dashboard/static/trailer_telemetry.json", 96),
    ("hermes_receipts", "memory/runs/hermes_jobs", 72),  # newest receipt mtime
]
FACE = REPO / "dashboard" / "static" / "organ_vitals.json"
ALERTS = REPO / "logs" / "failure_kb_alerts.jsonl"
CHAIN_STATE = REPO / "state" / "organ_vitals_chain.json"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _age_hours(p: Path, now: datetime) -> float | None:
    try:
        if p.is_dir():
            mtimes = [f.stat().st_mtime for f in p.rglob("*") if f.is_file()]
            if not mtimes:
                return None
            mtime = max(mtimes)
        else:
            mtime = p.stat().st_mtime
    except OSError:
        return None
    return max(0.0, (now.timestamp() - mtime) / 3600)


def grade(now: datetime | None = None) -> list[dict]:
    """Grade every organ: fresh / STALE / DARK."""
    now = now or _now()
    rows = []
    for name, rel, max_age in ORGANS:
        p = REPO / rel
        age = _age_hours(p, now)
        if age is None:
            state, detail = "DARK", f"missing: {rel}"
        elif age > max_age:
            state, detail = "STALE", f"{age:.1f}h old (max {max_age:g}h)"
        else:
            state, detail = "fresh", f"{age:.1f}h old (max {max_age:g}h)"
        rows.append({"organ": name, "path": rel, "state": state,
                     "age_hours": None if age is None else round(age, 2),
                     "max_age_hours": max_age, "detail": detail})
    return rows


def _prev_hash() -> str:
    try:
        return json.loads(CHAIN_STATE.read_text(encoding="utf-8")).get("last_hash", "0" * 64)
    except (OSError, json.JSONDecodeError):
        return "0" * 64


def emit_alerts(rows: list[dict], now: datetime) -> int:
    """Hash-chained breach rows into the fleet alerts log (reaper picks them up)."""
    breaching = [r for r in rows if r["state"] in ("STALE", "DARK")]
    if not breaching:
        return 0
    ALERTS.parent.mkdir(parents=True, exist_ok=True)
    prev = _prev_hash()
    n = 0
    with ALERTS.open("a", encoding="utf-8") as fh:
        for r in breaching:
            row = {
                "ts": now.isoformat(),
                "kind": "vitals_breach",
                "sig": f"vitals:{r['organ']}",
                "detail": f"{r['organ']} {r['state']}: {r['detail']}",
                "prev_hash": prev,
            }
            row["hash"] = hashlib.sha256(
                json.dumps(row, sort_keys=True).encode("utf-8")
            ).hexdigest()
            prev = row["hash"]
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            n += 1
    CHAIN_STATE.parent.mkdir(parents=True, exist_ok=True)
    CHAIN_STATE.write_text(json.dumps({"last_hash": prev, "ts": now.isoformat()},
                                      indent=2), encoding="utf-8")
    return n


def write_face(rows: list[dict], now: datetime) -> Path:
    FACE.parent.mkdir(parents=True, exist_ok=True)
    face = {
        "generated_at": now.isoformat(),
        "breaches": sum(1 for r in rows if r["state"] in ("STALE", "DARK")),
        "organs": rows,
        "note": "organ -> path -> max_age liveness spine (self-steal of dead_hand, 09-13); "
                "a stale or missing face is itself the alarm",
    }
    tmp = FACE.with_suffix(".tmp")
    tmp.write_text(json.dumps(face, indent=2), encoding="utf-8")
    tmp.replace(FACE)
    return FACE


def tick() -> dict:
    now = _now()
    rows = grade(now)
    n_alerts = emit_alerts(rows, now)
    face = write_face(rows, now)
    breaches = [r for r in rows if r["state"] in ("STALE", "DARK")]
    return {
        "tick": now.isoformat(),
        "organs": len(rows),
        "breaches": [f"{r['organ']}:{r['state']}" for r in breaches],
        "alerts_emitted": n_alerts,
        "face": str(face.relative_to(REPO)),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Organ vitals — liveness spine tick")
    ap.add_argument("--tick", action="store_true", help="grade + alert + face (default)")
    ap.add_argument("--grade-only", action="store_true", help="no alert rows, no face")
    args = ap.parse_args()
    if args.grade_only:
        print(json.dumps({"tick": _now().isoformat(),
                          "organs": grade()}, indent=2))
        return 0
    print(json.dumps(tick(), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
