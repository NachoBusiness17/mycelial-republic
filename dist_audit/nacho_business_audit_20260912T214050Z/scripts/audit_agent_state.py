#!/usr/bin/env python3
"""Read-only audit for the versioned agent-state chain.

This reports concurrency damage without rewriting history.  The chain is an
append-only receipt source; any repair must be emitted as a new derived chain
and reviewed before readers are redirected.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from mag import agent_state as ast  # noqa: E402

SCHEMA = "agent_state_chain_audit.v1"


def _rows() -> tuple[list[dict], int]:
    if not ast.CHAIN.is_file():
        return [], 0
    rows: list[dict] = []
    malformed = 0
    for line in ast.CHAIN.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            malformed += 1
            continue
        if isinstance(value, dict):
            rows.append(value)
        else:
            malformed += 1
    return rows, malformed


def audit() -> dict:
    rows, malformed = _rows()
    parent_breaks: list[int] = []
    duplicate_commits: list[str] = []
    seen_commits: set[str] = set()
    row_count_breaks: list[int] = []
    leaf_hashes: list[str] = []
    chain_files: set[str] = set()
    for index, row in enumerate(rows):
        expected = "" if index == 0 else str(rows[index - 1].get("content_commit") or "")
        if str(row.get("parent_commit") or "") != expected:
            parent_breaks.append(index + 1)
        commit = str(row.get("content_commit") or "")
        if commit in seen_commits and commit:
            duplicate_commits.append(commit)
        seen_commits.add(commit)
        leaf = str(row.get("leaf_hash") or "")
        if leaf:
            leaf_hashes.append(leaf)
        filename = str(row.get("filename") or "")
        if filename:
            chain_files.add(filename)
        if row.get("n_versions") != len(leaf_hashes):
            row_count_breaks.append(index + 1)

    version_json = {p.name for p in ast.VERSIONS.glob("*.json")} if ast.VERSIONS.is_dir() else set()
    missing_versions = sorted(chain_files - version_json)
    unreferenced_versions = sorted(version_json - chain_files)
    tip = None
    if ast.TIP.is_file():
        try:
            tip = json.loads(ast.TIP.read_text(encoding="utf-8", errors="replace"))
        except json.JSONDecodeError:
            tip = None
    computed_root = ast._merkle_root(leaf_hashes) if leaf_hashes else ast._merkle_root([])
    return {
        "schema": SCHEMA,
        "read_only": True,
        "chain": str(ast.CHAIN.relative_to(ROOT)),
        "rows": len(rows),
        "malformed_rows": malformed,
        "broken_parent_links": len(parent_breaks),
        "broken_parent_row_samples": parent_breaks[:20],
        "duplicate_content_commits": len(duplicate_commits),
        "row_n_versions_mismatches": len(row_count_breaks),
        "row_n_versions_mismatch_samples": row_count_breaks[:20],
        "computed_root": computed_root,
        "version_json_files": len(version_json),
        "chain_filenames": len(chain_files),
        "missing_version_files": len(missing_versions),
        "missing_version_samples": missing_versions[:20],
        "unreferenced_version_files": len(unreferenced_versions),
        "unreferenced_version_samples": unreferenced_versions[:20],
        "tip_file_root": (tip or {}).get("root"),
        "tip_file_n_versions": (tip or {}).get("n_versions"),
        "repair_policy": "preserve legacy chain; emit reviewed recovered chain v2 before redirecting readers",
        "source_changes": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="write a derived audit receipt")
    args = parser.parse_args()
    result = audit()
    if args.write:
        out = ROOT / "memory/runs/verkle_recovery/agent_state_audit_20260901.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        result["receipt"] = str(out.relative_to(ROOT))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
