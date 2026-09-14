#!/usr/bin/env python3
"""Reconcile percolator exploration status from drain outputs.

The script reads:
- memory/percolator/explore.jsonl
- every memory/percolator/explore_*.jsonl output file

It marks source rows as:
- done: canonical appears in any output file
- open: canonical does not appear in any output file

It writes the source file back atomically unless --dry-run is set.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "memory" / "percolator" / "explore.jsonl"
OUTPUT_GLOB = "explore_*.jsonl"


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON") from exc
    return rows


def collect_explored_canonicals(percolator_dir: Path) -> set[str]:
    explored: set[str] = set()
    for path in sorted(percolator_dir.glob(OUTPUT_GLOB)):
        if path.name == SOURCE_PATH.name:
            continue
        for row in read_jsonl(path):
            canonical = row.get("canonical")
            if isinstance(canonical, str) and canonical:
                explored.add(canonical)
    return explored


def reconcile_rows(rows: list[dict[str, Any]], explored: set[str]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    updated: list[dict[str, Any]] = []
    counts = {"total": 0, "explored": 0, "remaining": 0}
    for row in rows:
        counts["total"] += 1
        canonical = row.get("canonical")
        is_explored = isinstance(canonical, str) and canonical in explored
        new_status = "done" if is_explored else "open"
        if is_explored:
            counts["explored"] += 1
        else:
            counts["remaining"] += 1
        if row.get("status") != new_status:
            row = dict(row)
            row["status"] = new_status
        updated.append(row)
    return updated, counts


def write_jsonl_atomic(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f"{path.name}.", suffix=".tmp", dir=str(path.parent))
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False))
                handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_path, path)
    except Exception:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise


def format_changes(before: list[dict[str, Any]], after: list[dict[str, Any]]) -> dict[str, int]:
    changes: dict[str, int] = {}
    for old, new in zip(before, after):
        old_status = str(old.get("status", ""))
        new_status = str(new.get("status", ""))
        if old_status == new_status:
            continue
        key = f"{old_status}->{new_status}"
        changes[key] = changes.get(key, 0) + 1
    return changes


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="show the reconciliation summary without writing")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    percolator_dir = SOURCE_PATH.parent
    if not SOURCE_PATH.exists():
        raise FileNotFoundError(SOURCE_PATH)

    explored = collect_explored_canonicals(percolator_dir)
    before = read_jsonl(SOURCE_PATH)
    after, counts = reconcile_rows(before, explored)
    changes = format_changes(before, after)

    print(f"source: {SOURCE_PATH}")
    print(f"outputs: {len([p for p in sorted(percolator_dir.glob(OUTPUT_GLOB)) if p.name != SOURCE_PATH.name])}")
    print(f"total: {counts['total']}")
    print(f"explored: {counts['explored']}")
    print(f"remaining: {counts['remaining']}")
    if changes:
        change_bits = ", ".join(f"{k}={v}" for k, v in sorted(changes.items()))
        print(f"status changes: {change_bits}")
    else:
        print("status changes: none")

    if args.dry_run:
        print("dry-run: no file written")
        return 0

    write_jsonl_atomic(SOURCE_PATH, after)
    print("updated: wrote source atomically")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
