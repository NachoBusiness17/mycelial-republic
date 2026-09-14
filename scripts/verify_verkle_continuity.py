#!/usr/bin/env python3
"""
Sanity script: verify verkle chain continuity.
Run: python scripts/verify_verkle_continuity.py
Exit 0 on success, 1 on break.
"""
import json
import sys
from pathlib import Path

# Absolute path to the verkle chain file from repo root
CHAIN_PATH = Path(__file__).resolve().parents[1] / "memory/biography/verkle_chain.jsonl"


def main():
    if not CHAIN_PATH.exists():
        print(f"ERROR: {CHAIN_PATH} missing")
        return 1

    prev = None
    for i, line in enumerate(CHAIN_PATH.open(encoding="utf-8")):
        try:
            k = json.loads(line)
        except json.JSONDecodeError as e:
            print(f"ERROR: line {i+1} JSON decode failed: {e}")
            return 1

        if prev is None:
            prev = k
            continue

        if k.get("parent_verkle_root") != prev.get("verkle_root"):
            print(f"BREAK at index {i}: parent_verkle_root mismatch")
            print(f"  Expected: {prev.get('verkle_root')}")
            print(f"  Got:      {k.get('parent_verkle_root')}")
            return 1

        prev = k

    print("Continuity OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
