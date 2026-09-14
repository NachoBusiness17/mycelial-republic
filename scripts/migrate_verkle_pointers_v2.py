#!/usr/bin/env python3
"""Backfill collision-free session pointers from verified live chain rows.

Only derived pointer files are added.  Chain rows, knot payloads, roots, and
legacy pointers are never changed.  Rows whose knot is missing or whose
session/hash does not agree are skipped for manual recovery review.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from mag import verkle_knot as vk  # noqa: E402


def main() -> int:
    written = skipped = 0
    with vk.verkle_lock():
        rows = vk._load_chain_rows()
        vk.KNOTS.mkdir(parents=True, exist_ok=True)
        for row in rows:
            sid = str(row.get("session_id") or "")
            filename = str(row.get("filename") or "")
            knot_path = vk.KNOTS / filename
            if not sid or not knot_path.is_file():
                skipped += 1
                continue
            try:
                knot = json.loads(knot_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                skipped += 1
                continue
            if knot.get("session_id") != sid or knot.get("leaf_hash") != row.get("leaf_hash"):
                skipped += 1
                continue
            pointer = vk.session_pointer_v2(sid)
            payload = {
                "schema": "verkle_session_pointer.v2",
                "session_id": sid,
                "filename": filename,
                "leaf_hash": row.get("leaf_hash"),
                "chain_index": row.get("index"),
                "chain_root": row.get("verkle_root"),
            }
            tmp = pointer.with_name(pointer.name + f".{os.getpid()}.tmp")
            tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
            os.replace(tmp, pointer)
            written += 1
    print(json.dumps({"ok": True, "schema": "verkle_pointer_migration.v1",
                      "written": written, "skipped": skipped,
                      "chain_rows": len(rows), "source_changes": []}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
