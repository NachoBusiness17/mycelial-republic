"""GPS capability metabolism - alpha-decay + dispute-streak slashing +
drift-patrol-keyed epoch reset (D7, eleven-doors, 2026-10-05 night shift).

The stored capability row is the running mean (incremental, momentum
floor at ledger.py:433-443: a fail absorbs, never rewards) - the audit
trail. This module computes the ROUTING-FACING effective rate on top,
read-only, without touching one stored byte:

  decayed  = PRIOR + (stored - PRIOR) * exp(-age_days / TAU_DAYS)
             Old measurements lose weight because the world under a
             model moves (fine-tunes, deprecations, quantization); decay
             measures ABSENCE of fresh evidence, never merit (the Z15
             decay-measures-absence gap, ESTATE register).
  slashed  = decayed * SLASH_PER_FAIL ** min(fail_streak, SLASH_CAP)
             A live dispute streak carries information the lifetime mean
             dilutes; the cap keeps a 3-fail night from nuking a
             100-sample row.
  epoch    = a drift-patrol-keyed reset stamps an epoch marker; rows
             whose last_measured predates it collapse to PRIOR (tainted
             era: e.g. the pre-dedupe doubled-key re-fire class, 59.8%
             of arena spend) until re-measured in the fresh epoch. The
             marker is an explicit act (reset_epoch()), never automatic.

Read-only over the same sqlite file; the stored mean stays the raw
audit surface (verdict_log is the append-only ground).
"""
from __future__ import annotations

import argparse
import json
import math
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PRIOR = 0.5          # the uninformative prior stale evidence decays toward
TAU_DAYS = 14.0      # decay time constant (half-life ~9.7 days)
SLASH_PER_FAIL = 0.85
SLASH_CAP = 3        # slash bottoms at 0.85^3 ~= 0.614x, streaks beyond 3 flat

EPOCH_PATH = Path(__file__).parent / "metabolism_epoch.json"


@dataclass
class MetabolicRate:
    model_id: str
    task_shape: str
    stored_pass_rate: float
    sample_size: int
    last_measured: str
    age_days: float
    fail_streak: int
    decayed_rate: float
    slashed_rate: float
    epoch_reset: bool
    effective_rate: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "task_shape": self.task_shape,
            "stored_pass_rate": round(self.stored_pass_rate, 4),
            "sample_size": self.sample_size,
            "last_measured": self.last_measured,
            "age_days": round(self.age_days, 2),
            "fail_streak": self.fail_streak,
            "decayed_rate": round(self.decayed_rate, 4),
            "slashed_rate": round(self.slashed_rate, 4),
            "epoch_reset": self.epoch_reset,
            "effective_rate": round(self.effective_rate, 4),
        }


def _parse_ts(ts: str) -> datetime:
    # ledger timestamps are ISO with Z
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _fail_streak(conn: sqlite3.Connection, model_id: str, task_shape: str) -> int:
    """Consecutive fails from the freshest verdicts (dispute streak)."""
    rows = conn.execute(
        "SELECT verdict FROM verdict_log WHERE model_id = ? AND task_shape = ?"
        " ORDER BY ts DESC LIMIT 10",
        (model_id, task_shape),
    ).fetchall()
    streak = 0
    for (verdict,) in rows:
        if int(verdict) == 0:
            streak += 1
        else:
            break
    return streak


def reset_epoch(path: str | Path = EPOCH_PATH, *, reason: str, ts_utc: str) -> dict[str, Any]:
    """Stamp a fresh evidence epoch (the drift-patrol-keyed reset).

    Explicit act by design: a seat or the patrol operator calls this when
    a named drift event lands (dedupe cure, provider swap, quantization
    change). Rows last measured before the marker collapse to PRIOR in
    metabolic_rates until fresh evidence re-measures them.
    """
    marker = {"epoch_ts_utc": ts_utc, "reason": reason}
    p = Path(path)
    p.write_text(json.dumps(marker, ensure_ascii=False, indent=1), encoding="utf-8")
    return marker


def load_epoch(path: str | Path | None = EPOCH_PATH) -> dict[str, Any] | None:
    if path is None:
        return None
    p = Path(path)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 - a corrupt marker is no marker
        return None


def metabolic_rates(
    db: sqlite3.Connection | str | Path,
    *,
    now: str | None = None,
    epoch: dict[str, Any] | None = None,
    task_shape: str | None = None,
) -> list[MetabolicRate]:
    """Effective rates for every capability row (or one task shape)."""
    if isinstance(db, (str, Path)):
        conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            return metabolic_rates(conn, now=now, epoch=epoch, task_shape=task_shape)
        finally:
            conn.close()
    now_dt = _parse_ts(now) if now else datetime.now(timezone.utc)
    epoch_ts = None
    if epoch and epoch.get("epoch_ts_utc"):
        try:
            epoch_ts = _parse_ts(epoch["epoch_ts_utc"])
        except ValueError:
            epoch_ts = None
    query = (
        "SELECT model_id, task_shape, pass_rate, sample_size, last_measured"
        " FROM capability"
    )
    params: tuple[Any, ...] = ()
    if task_shape:
        query += " WHERE task_shape = ?"
        params = (task_shape,)
    out: list[MetabolicRate] = []
    for model_id, shape, pass_rate, sample_size, last_measured in db.execute(query, params):
        measured_dt = _parse_ts(last_measured)
        age_days = max((now_dt - measured_dt).total_seconds() / 86400.0, 0.0)
        decayed = PRIOR + (float(pass_rate) - PRIOR) * math.exp(-age_days / TAU_DAYS)
        streak = _fail_streak(db, model_id, shape)
        slashed = decayed * (SLASH_PER_FAIL ** min(streak, SLASH_CAP))
        epoch_reset = bool(epoch_ts and measured_dt < epoch_ts)
        effective = PRIOR if epoch_reset else slashed
        out.append(
            MetabolicRate(
                model_id=model_id,
                task_shape=shape,
                stored_pass_rate=float(pass_rate),
                sample_size=int(sample_size),
                last_measured=last_measured,
                age_days=age_days,
                fail_streak=streak,
                decayed_rate=decayed,
                slashed_rate=slashed,
                epoch_reset=epoch_reset,
                effective_rate=effective,
            )
        )
    out.sort(key=lambda r: (-r.effective_rate, r.model_id, r.task_shape))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="GPS capability metabolism (effective rates)")
    parser.add_argument("--db", default=str(Path(__file__).parent / "gps_ledger.db3"))
    parser.add_argument("--task-shape", default=None)
    parser.add_argument("--epoch", default=str(EPOCH_PATH),
                        help="epoch marker json (drift-patrol-keyed reset); 'none' to ignore")
    parser.add_argument("--set-epoch", default=None,
                        help="stamp an epoch marker then exit: REASON|TS_UTC")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.set_epoch:
        reason, _, ts = args.set_epoch.partition("|")
        marker = reset_epoch(reason=reason.strip(), ts_utc=ts.strip() or None or "")
        print(json.dumps(marker, indent=1))
        return 0

    epoch = None if args.epoch == "none" else load_epoch(args.epoch)
    rates = metabolic_rates(args.db, epoch=epoch, task_shape=args.task_shape)
    if args.json:
        print(json.dumps({
            "epoch": epoch,
            "rates": [r.as_dict() for r in rates],
        }, indent=1))
        return 0
    print("GPS METABOLISM (effective rates; stored mean stays the audit surface)")
    if epoch:
        print(f"  epoch: {epoch.get('epoch_ts_utc')} ({epoch.get('reason')})")
    else:
        print("  epoch: none (no drift-patrol reset stamped)")
    hdr = (f"  {'model':38s} {'shape':28s} {'stored':>7s} {'age_d':>6s}"
           f" {'strk':>4s} {'decayed':>7s} {'epoch':>5s} {'EFFECTIVE':>9s}")
    print(hdr)
    for r in rates:
        print(
            f"  {r.model_id:38s} {r.task_shape:28s} {r.stored_pass_rate:7.3f}"
            f" {r.age_days:6.1f} {r.fail_streak:4d} {r.decayed_rate:7.3f}"
            f" {'RESET' if r.epoch_reset else '-':>5s} {r.effective_rate:9.3f}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
