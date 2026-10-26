"""Append-only, hash-linked JSONL rotation ledger.

Separate from the Mag verkle chain on purpose: own file under state/keyrot/, own
genesis, no import of chain code, no write to chain file, tip or ACL.
Row hash = sha256(prev_hash + canonical_json(row without hash)).
Events: detected, queued, planned_auto, rotated, stored, verified, verify_failed, revoked.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "state" / "keyrot" / "rotation_ledger.jsonl"
GENESIS = "0" * 64
EVENTS = {"detected", "queued", "planned_auto", "rotated", "stored", "verified",
          "verify_failed", "revoked"}


def _canon(row: dict) -> str:
    return json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def _rows(path: Path = LEDGER) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def tip(path: Path = LEDGER) -> tuple[int, str]:
    rows = _rows(path)
    return (rows[-1]["seq"], rows[-1]["hash"]) if rows else (-1, GENESIS)


def append(event: str, key_id: str, path: Path = LEDGER, **fields: Any) -> dict:
    if event not in EVENTS:
        raise ValueError(f"unknown ledger event {event}")
    for k, v in fields.items():  # defence in depth: refuse anything shaped like a raw value field
        if k.lower() in {"value", "secret", "key", "token", "api_key"}:
            raise ValueError(f"ledger refuses raw-value field {k}")
    path.parent.mkdir(parents=True, exist_ok=True)
    seq, prev = tip(path)
    row = {"seq": seq + 1, "ts": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
           "event": event, "key_id": key_id, "prev_hash": prev, **fields}
    row["hash"] = hashlib.sha256((prev + _canon(row)).encode()).hexdigest()
    with open(path, "a", encoding="utf-8") as f:
        f.write(_canon(row) + "\n")
    return row


def verify(path: Path = LEDGER) -> dict:
    prev, n = GENESIS, 0
    for i, row in enumerate(_rows(path)):
        h = row.pop("hash")
        if row.get("prev_hash") != prev or row.get("seq") != i:
            return {"ok": False, "broken_at": i, "reason": "link"}
        if hashlib.sha256((prev + _canon(row)).encode()).hexdigest() != h:
            return {"ok": False, "broken_at": i, "reason": "hash"}
        prev, n = h, n + 1
    return {"ok": True, "rows": n, "tip": prev}


def first_seen(key_id: str, path: Path = LEDGER) -> str | None:
    for row in _rows(path):
        if row["key_id"] == key_id and row["event"] == "detected":
            return row.get("first_seen") or row["ts"][:10]
    return None


def last_event(key_id: str, path: Path = LEDGER) -> str | None:
    ev = None
    for row in _rows(path):
        if row["key_id"] == key_id:
            ev = row["event"]
    return ev
