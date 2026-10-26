#!/usr/bin/env python3
"""chain_no_rewrite_check - rolling baseline: red only on a NEW rewrite.

Historical sealed prefix (ab595c33 / 0da8026d, n=12016) stays as an INFO line
via tools/chain_prefix_seal_check.py (non-failing in ratchet). This tool stores
state/chain_no_rewrite_baseline.json = {rows, prefix_bytes, prefix_sha256, ts}
and each run asserts live[:prefix_bytes] is unchanged, then advances the baseline
to the current tip. Exit 1 only when the protected prefix was rewritten.

Never repairs. Never takes verkle_lock. Never writes the chain file.
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAIN = ROOT / "memory" / "biography" / "verkle_chain.jsonl"
BASE = ROOT / "state" / "chain_no_rewrite_baseline.json"


def prefix_bytes_for_rows(raw: bytes, n: int) -> bytes:
    if n <= 0:
        return b""
    count = 0
    for i, b in enumerate(raw):
        if b == 10:
            count += 1
            if count == n:
                return raw[: i + 1]
    return raw


def main() -> int:
    if not CHAIN.is_file():
        print("NO-REWRITE: cannot-run missing live chain")
        return 2
    raw = CHAIN.read_bytes()
    lines = [ln for ln in raw.splitlines() if ln.strip()]
    rows = len(lines)
    full_sha = hashlib.sha256(raw).hexdigest()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    if not BASE.is_file():
        # Seed baseline at current tip (today is the working baseline).
        doc = {
            "schema": "chain_no_rewrite_baseline.v1",
            "rows": rows,
            "prefix_bytes": len(raw),
            "prefix_sha256": full_sha,
            "full_sha256": full_sha,
            "seeded_utc": now,
            "note": "seeded 2026-10-20; sealed 10/16 prefix is history only",
        }
        BASE.parent.mkdir(parents=True, exist_ok=True)
        BASE.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        print(f"NO-REWRITE: SEEDED rows={rows} sha={full_sha[:16]}")
        return 0
    base = json.loads(BASE.read_text(encoding="utf-8"))
    b_rows = int(base["rows"])
    b_bytes = int(base["prefix_bytes"])
    b_sha = str(base["prefix_sha256"])
    if len(raw) < b_bytes:
        print(f"NO-REWRITE: FAIL chain shrunk ({len(raw)} < baseline_bytes {b_bytes})")
        return 1
    live_pref = raw[:b_bytes]
    live_sha = hashlib.sha256(live_pref).hexdigest()
    if live_sha != b_sha:
        print(
            f"NO-REWRITE: FAIL prefix rewritten baseline_rows={b_rows} "
            f"expect={b_sha[:16]} live={live_sha[:16]}"
        )
        return 1
    # Advance baseline to current tip (append-only growth is green).
    doc = {
        "schema": "chain_no_rewrite_baseline.v1",
        "rows": rows,
        "prefix_bytes": len(raw),
        "prefix_sha256": full_sha,
        "full_sha256": full_sha,
        "prev_rows": b_rows,
        "prev_sha256": b_sha,
        "advanced_utc": now,
        "seeded_utc": base.get("seeded_utc"),
    }
    BASE.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
    print(f"NO-REWRITE: PASS advanced {b_rows}->{rows} sha={full_sha[:16]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
