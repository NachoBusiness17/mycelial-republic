"""Name the drifted canon rows that mag/librarian_catalog.py verify_canon()
counts. Read-only diagnostic; same parse rules (seal headers/comments skipped).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
CANON = ROOT / "corpus" / "canon"

missing: list[str] = []
drifted: list[str] = []
checked = 0
for line in (CANON / "MANIFEST.sha256").read_text(encoding="utf-8",
                                                 errors="replace").splitlines():
    parts = line.split(None, 1)
    if len(parts) != 2:
        continue
    want, rel = parts[0], parts[1].strip().lstrip("*")
    if len(want) != 64 or any(c not in "0123456789abcdef" for c in want.lower()):
        continue
    checked += 1
    fp = CANON / rel
    try:
        h = hashlib.sha256(fp.read_bytes()).hexdigest()
    except OSError:
        missing.append(rel)
        continue
    if h != want:
        drifted.append(rel)
print(f"checked={checked} missing={len(missing)} drifted={len(drifted)}")
for rel in missing:
    print("MISSING " + rel)
for rel in drifted:
    print("DRIFT   " + rel)
sys.exit(0)
