#!/usr/bin/env python3
"""reputation_router - the reputation-gated cell board (Phase 4 babystep 3).

Reads worker_reputation from the lattice snapshot (written by hot-lattice.ts,
the trusted instrument). Zero-network: serves from the file, not the chain.

The flywheel: more settles -> more reputation -> more work routed to you ->
more settles. The routing signal is on-chain reputation, not self-reported.

Usage:
  .venv/Scripts/python.exe tools/reputation_router.py
"""
import json
import os
import sys
import time
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
LATTICE_JSON = os.path.join(HERE, "..", "reference", "gstdcoin", "contracts", "lattice.json")


def main() -> int:
    if not os.path.isfile(LATTICE_JSON):
        print("lattice.json not found - run scripts/hot-lattice.ts to refresh")
        return 1
    snap = json.load(open(LATTICE_JSON, encoding="utf-8"))
    cells = snap.get("cells", {})
    age = round(time.time() - os.path.getmtime(LATTICE_JSON))
    print("=== REPUTATION-GATED CELL BOARD ===")
    print(f"snapshot: {snap.get('captured_at', '?')} | age: {age}s")
    ranked = []
    for name, c in sorted(cells.items()):
        rep = c.get("reputation", 0)
        ton = c.get("ton", 0)
        state = c.get("state", "?")
        ranked.append({"name": name, "reputation": rep, "ton": ton, "state": state})
        print(f"  {name}: rep {rep} | {ton} TON | {state}")
    ranked.sort(key=lambda x: x["reputation"], reverse=True)
    print("\n  ROUTING ORDER (highest reputation first):")
    for r in ranked:
        print(f"    {r['name']} (rep {r['reputation']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
