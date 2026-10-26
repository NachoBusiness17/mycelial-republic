"""reflux_delta_probe.py - ReFlux delta-not-state conversion probe (lane d08-reflux-delta).

The ReFlux re-derivation (watch/inbox/X_INTEL_REFLUX_20261005.md, arXiv
2609.32457: feed back the depth INCREMENT, not the full state) applied to the
estate's own state organs. Audit verdict, measured 2026-10-06:

  memory/game/FLOW_LEDGER.jsonl      ALREADY DELTA. Append-only via
      mag/game_flow.py:75 (LEDGER.open("a")), one row per enqueue with
      ts + queue_id + corr_id stamped at the single choke point
      (mag/game_flow.py:69-76). 214 rows on disk. The pattern this probe
      copies; no conversion needed.
  memory/game/world/world_state.json HYBRID DISEASE. Whole-file rewrite per
      set_state (mag/game_world.py:63-64 atomic_write_text over the entire
      store) while the delta log (state["changes"], mag/game_world.py:95)
      rides INSIDE the rewritten blob: measured 2107 live keys + 4237
      embedded change rows. One torn write destroys state AND provenance
      together; the corrupt-store refusal at mag/game_world.py:54-57 proves
      torn writes happen on this surface. The cure shape: the changes log
      becomes its own append-only file, the snapshot becomes fold(log).
  memory/warm_state.json             STATE-AS-VIEW, LOWEST SEVERITY. Full
      rewrite every boot (mag/hermes_warm_boot.py:243 STATE.write_text).
      Benign in one direction: its delta source already exists as the
      append-only memory/biography/verkle_chain.jsonl, so warm_state is a
      materialized view, not the record. Still, each rewrite silently drops
      the previous boot's tip: there is no boot history, so "when did the
      seat last arm and on which chain index" is unprovable after the fact.
      Cure shape: one delta row per boot, warm_state.json stays as the O(1)
      read cache of fold(log).
  queue/lanes/*/runner_state.json    PUREST DISEASE. A CURSOR (inbox_offset)
      plus last_result stored in a whole-state snapshot rewrite
      (mag/lane_runner.py:124-149; cursor update at :404; last_result
      overwrite at :1145-1146). Every run destroys the previous
      last_result: zero provenance on what the lane last did. The estate's
      own errno-22 wound (910 rows, corpus/steal/MASTER_READ_ESTATE.md
      section 10) is this exact surface: a snapshot is a single point of
      failure, an append-only delta chain is not, because a partial write
      costs at most the last row, never the whole state.

DELTA SCHEMA (delta_state.v1) - one JSONL row per mutation, hash-chained:

  {"schema": "delta_state.v1",
   "surface": "runner_state:builder",   # which organ the delta applies to
   "seq": 3,                            # 1-based; a gap means a lost row
   "ts": "2026-10-06T12:00:00.000000Z",
   "op": "genesis" | "set" | "note",    # genesis = base snapshot row
   "key": "last_result",                # field the op touches (note: null)
   "value": <op payload>,               # genesis: whole snapshot dict
   "note": "optional provenance text",  # note rows carry the map here
   "prev_leaf": "<hex|null>",           # chain link to the previous row
   "leaf": "<hex>"}                     # sha256 over the canonical row body

Canonical form: json.dumps(body, sort_keys=True, separators=(",", ":"),
ensure_ascii=False). The leaf covers every field except "leaf" itself.

Fold law: the live value of a key is the LAST row in seq order that touches
it (genesis updates every key it carries, "set" updates one). The snapshot is
always re-derivable as fold(chain); any single row is independently
re-verifiable from its prev_leaf. Append never truncates, so the failure mode
of the errno-22 class (O_TRUNC on the live file) is structurally absent.

CLI (probe only - no live writer is switched yet; adopting this chain in
mag/lane_runner.py is a later, separately-gated ask):

  .venv/Scripts/python.exe tools/reflux_delta_probe.py init builder
  .venv/Scripts/python.exe tools/reflux_delta_probe.py note builder "..."
  .venv/Scripts/python.exe tools/reflux_delta_probe.py append builder last_result "..."
  .venv/Scripts/python.exe tools/reflux_delta_probe.py verify builder
  .venv/Scripts/python.exe tools/reflux_delta_probe.py fold builder

LAW: this probe appends ONLY to queue/lanes/<lane>/runner_state.delta.jsonl.
It never writes runner_state.json - the lane runner owns that file until the
conversion is adopted upstream. verify() reports fold-vs-live drift as
informational: pre-adoption the snapshot writer does not consume deltas, so
drift on hot lanes is expected, not a defect.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
LANES = ROOT / "queue" / "lanes"
SCHEMA = "delta_state.v1"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _leaf(body: dict) -> str:
    return hashlib.sha256(_canon(body).encode("utf-8")).hexdigest()


def _delta_path(lane: str) -> Path:
    return LANES / lane / "runner_state.delta.jsonl"


def _rows(lane: str) -> list[dict]:
    p = _delta_path(lane)
    if not p.exists():
        return []
    rows: list[dict] = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def _append_row(lane: str, op: str, key: str | None, value: Any,
                note: str | None) -> dict:
    rows = _rows(lane)
    prev = rows[-1]["leaf"] if rows else None
    seq = (rows[-1]["seq"] + 1) if rows else 1
    body = {"schema": SCHEMA, "surface": f"runner_state:{lane}", "seq": seq,
            "ts": _now(), "op": op, "key": key, "value": value,
            "note": note, "prev_leaf": prev}
    row = dict(body, leaf=_leaf(body))
    p = _delta_path(lane)
    p.parent.mkdir(parents=True, exist_ok=True)
    # newline="\n" (2026-10-06): plain text-mode "a" on win32 translates \n to
    # \r\n, landing CR bytes in the delta chain - the exact EOL disease the
    # trail cure killed on queue/lanes/*/trail.jsonl (MASTER_READ_ESTATE.md
    # section 9 row 7: "strip CR at key load and normalize trail EOL",
    # CR-byte mirror deltas measured). The chain must stay LF-clean.
    with p.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return row


def _live_snapshot(lane: str) -> dict:
    p = LANES / lane / "runner_state.json"
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {}


def cmd_init(lane: str) -> dict:
    snap = _live_snapshot(lane)
    row = _append_row(lane, "genesis", None, snap,
                      "base snapshot recorded; chain starts here")
    return {"ok": True, "action": "init", "lane": lane, "row": row}


def cmd_note(lane: str, note: str) -> dict:
    row = _append_row(lane, "note", None, None, note)
    return {"ok": True, "action": "note", "lane": lane, "row": row}


def cmd_append(lane: str, key: str, value: str) -> dict:
    row = _append_row(lane, "set", key, value, None)
    return {"ok": True, "action": "append", "lane": lane, "row": row}


def cmd_fold(lane: str) -> dict:
    rows = _rows(lane)
    state: dict = {}
    for r in rows:
        if r["op"] == "genesis":
            if r["key"] is not None:
                state[r["key"]] = r["value"]
            elif isinstance(r["value"], dict):
                state.update(r["value"])
        elif r["op"] == "set":
            state[r["key"]] = r["value"]
    return {"ok": True, "action": "fold", "lane": lane,
            "rows": len(rows), "state": state}


def cmd_verify(lane: str) -> dict:
    rows = _rows(lane)
    problems: list[str] = []
    prev: str | None = None
    for r in rows:
        body = {k: v for k, v in r.items() if k != "leaf"}
        if r.get("prev_leaf") != prev:
            problems.append(f"seq {r.get('seq')}: prev_leaf chain break")
        if _leaf(body) != r.get("leaf"):
            problems.append(f"seq {r.get('seq')}: leaf hash mismatch")
        prev = r.get("leaf")
    seqs = [r.get("seq") for r in rows]
    if seqs != list(range(1, len(seqs) + 1)):
        problems.append(f"seq gap or reorder: {seqs}")
    folded = cmd_fold(lane)["state"]
    live = _live_snapshot(lane)
    drift = {}
    for k in sorted(set(folded) | set(live)):
        if folded.get(k) != live.get(k):
            drift[k] = {"fold": folded.get(k), "live": live.get(k)}
    return {"ok": not problems, "action": "verify", "lane": lane,
            "rows": len(rows), "problems": problems,
            "fold_vs_live_drift": drift,
            "drift_note": "pre-adoption the live snapshot writer does not consume deltas, so drift on hot lanes is expected, not a defect"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="ReFlux delta-not-state conversion probe (delta_state.v1)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("init", "fold", "verify"):
        p = sub.add_parser(name)
        p.add_argument("lane")
    p = sub.add_parser("note")
    p.add_argument("lane")
    p.add_argument("note")
    p = sub.add_parser("append")
    p.add_argument("lane")
    p.add_argument("key")
    p.add_argument("value")
    args = ap.parse_args(argv)
    if args.cmd == "init":
        out = cmd_init(args.lane)
    elif args.cmd == "note":
        out = cmd_note(args.lane, args.note)
    elif args.cmd == "append":
        out = cmd_append(args.lane, args.key, args.value)
    elif args.cmd == "fold":
        out = cmd_fold(args.lane)
    else:
        out = cmd_verify(args.lane)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
