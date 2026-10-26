"""horizon_mint - mint the session-exit horizon object (horizon.v1).

Composes the estate's existing organs into one append-only math line
(the design: watch/inbox/HORIZON_OBJECT_20261016.md; self-steal:
watch/inbox/HORIZON_SELF_STEAL_20261016.md). Every field is computed from
bytes on disk; nothing is hand-written. Genesis (n=1) is the hand-minted
state/HORIZON_20261016.jsonl; this tool appends n>=2 to state/HORIZONS.jsonl,
chaining prev_hash to the last self_hash.

Fields and their organs:
  bulk.verkle_root      <- memory/biography/verkle_tip.json (rib_boot anchor)
  bulk.census           <- the B2-249 carrier claim parsed from AGENTS.md
  surface.*             <- sha256 over the touched-surface files (fixed list
                           + --surface extras; missing files are skipped and
                           reported, never invented)
  wave                  <- pointer facts (hydrology, delta_index, pheromone
                           field, percolator decay) - static identifiers
  trajectory.free_lane  <- today's ok:true H247_ rows in the usage ledger
  exit_clause.predicates<- evaluated from logs/census_patrol.log tail and
                           the usage ledger (beacon bytes, not vibes)
  chariot               <- self=null, parts_only=true; the no-self law

Usage:
  .venv/Scripts/python.exe tools/horizon_mint.py --seat zcode-seat-YYYYMMDD \
      [--surface extra/path.md ...]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HORIZONS = ROOT / "state" / "HORIZONS.jsonl"
GENESIS = ROOT / "state" / "HORIZON_20261016.jsonl"
USAGE = ROOT / "memory" / "runs" / "hermes_burn" / "usage.jsonl"
PATROL_LOG = ROOT / "logs" / "census_patrol.log"
AGENTS = ROOT / "AGENTS.md"
BONDS = ROOT / "memory" / "bonds_active.json"
VERKLE_TIP = ROOT / "memory" / "biography" / "verkle_tip.json"

DEFAULT_SURFACES = [
    "state/SOAK_BEACON_20261016.md",
    "memory/rib/RIB_HANDOFF_20261015.md",
    "watch/inbox/SELF_ARCHAEOLOGY_S1_20261016.md",
    "watch/inbox/SELF_ARCHAEOLOGY_S2_20261016.md",
    "watch/inbox/INTERPRETIVE_LAYER_CARD_20261016.md",
    "watch/inbox/HORIZON_OBJECT_20261016.md",
    "watch/inbox/HORIZON_SELF_STEAL_20261016.md",
    "watch/inbox/GSTD_MAP_20261016.md",
    "watch/inbox/FORGOTTEN_REGISTER_20261016.md",
]


def sha(rel: str) -> str | None:
    p = ROOT / rel
    if not p.is_file():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def last_horizon() -> dict:
    for path in (HORIZONS, GENESIS):
        if path.is_file():
            lines = [l for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
            if lines:
                return json.loads(lines[-1])
    raise SystemExit("no genesis horizon found")


def census_from_carrier() -> dict:
    text = AGENTS.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"(\d[\d,]*) tests collected / (\d+) files \((\d{4}-\d{2}-\d{2}) census", text)
    if not m:
        return {"error": "carrier shape not found (B2-249)"}
    return {"collected": int(m.group(1).replace(",", "")),
            "files": int(m.group(2)), "census_date": m.group(3)}


def free_lane_today() -> dict:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ok = tok = 0
    if USAGE.is_file():
        for line in USAGE.read_text(encoding="utf-8", errors="replace").splitlines():
            if '"ok": true' not in line or "H247_" not in line or today not in line:
                continue
            row = json.loads(line)
            ok += 1
            tok += row.get("prompt_tokens", 0) + row.get("completion_tokens", 0)
    return {"fires_ok": ok, "tokens_banked": tok, "cost_usd": 0.0}


def predicates() -> list[dict]:
    out = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    census_exit = None
    if PATROL_LOG.is_file():
        for line in PATROL_LOG.read_text(encoding="utf-8", errors="replace").splitlines():
            if today in line and "END exit=" in line:
                m = re.search(r"END exit=(\d+)", line)
                if m:
                    census_exit = int(m.group(1))
    out.append({"id": "P1", "state": {"census_patrol_exit_today": census_exit},
                "then": "census_incident_closed" if census_exit == 0 else "incident_open_or_pending"})
    fl = free_lane_today()
    out.append({"id": "P2", "state": {"fires_ok_today": fl["fires_ok"]},
                "then": "free_lane_healthy" if fl["fires_ok"] >= 1 else "free_lane_cold"})
    return out


def bonds_field() -> dict | None:
    if not BONDS.is_file():
        return None
    age = datetime.now(timezone.utc) - datetime.fromtimestamp(
        BONDS.stat().st_mtime, tz=timezone.utc)
    if age > timedelta(hours=24):
        return None
    d = json.loads(BONDS.read_text(encoding="utf-8"))
    return {k: d.get(k) for k in ("n_bonds", "n_moves", "n_conflicts") if k in d}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seat", default="unknown-seat")
    ap.add_argument("--surface", action="append", default=[])
    args = ap.parse_args()

    prev = last_horizon()
    surfaces = {}
    skipped = []
    for rel in DEFAULT_SURFACES + args.surface:
        h = sha(rel)
        if h is None:
            skipped.append(rel)
        else:
            surfaces[Path(rel).name] = h

    verkle_root = None
    if VERKLE_TIP.is_file():
        try:
            tip = json.loads(VERKLE_TIP.read_text(encoding="utf-8"))
            verkle_root = tip.get("root") or tip.get("verkle_root")
        except Exception:
            verkle_root = None

    horizon = {
        "schema": "horizon.v1",
        "n": prev.get("n", 0) + 1,
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "prev_hash": prev.get("self_hash"),
        "bulk": {"verkle_root": verkle_root,
                  "census": census_from_carrier()},
        "surface": surfaces,
        "surface_skipped_missing": skipped,
        "wave": {"propagator": "mag/hydrology.py",
                  "surface_index": "memory/mesh/delta_index.json",
                  "pheromone_field": "watch/inbox/index_events.jsonl",
                  "decay_organ": "memory/percolator/invariants.json"},
        "trajectory": {"free_lane": free_lane_today(), "bonds": bonds_field()},
        "exit_clause": {"successor_entry": "state rows 0a-c sniff",
                          "predicates": predicates()},
        "chariot": {"self": None, "parts_only": True, "designation": args.seat},
    }
    horizon["self_hash"] = hashlib.sha256(
        json.dumps(horizon, sort_keys=True).encode()).hexdigest()
    with HORIZONS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(horizon, sort_keys=True) + "\n")
    print(f"MINTED horizon n={horizon['n']} self_hash={horizon['self_hash']}")
    print(f"surfaces={len(surfaces)} skipped={len(skipped)} "
          f"free_lane_ok={horizon['trajectory']['free_lane']['fires_ok']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
