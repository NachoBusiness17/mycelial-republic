#!/usr/bin/env python3
"""Build a collision-free, non-destructive index of the Mag estate.

The index is a derived view. It never deletes, moves, rewrites, or consolidates
source files. Every scanned file receives a stable relative path, artifact
class, byte size, and mtime. Small shared text artifacts receive SHA-256;
Verkle knot payloads use their stored leaf hash and chain membership instead of
duplicating large file hashing work.

Usage:
  python scripts/build_verkle_artifact_index.py --write
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from scripts.verkle_territory_audit import (  # noqa: E402
    MAX_HASH_BYTES,
    SCAN_ROOTS,
    SKIP_DIRS,
    TEXT_SUFFIXES,
    artifact_class,
    load_jsonl,
    pointer_name,
    sha256_file,
)
from mag import verkle_knot as vk  # noqa: E402

SCHEMA = "verkle_artifact_index.v1"
INDEX_PATHS = (
    "memory/biography",
    "memory/ghost/q_state",
    "memory/game",
    "memory/game_modules",
    "memory/lenses",
    "memory/mycelium",
    "memory/rib_bus",
    "memory/runs",
    "memory/knowledge_graph.json",
    "memory/cost",
    "watch",
    "docs/ref",
    "docs/REPRO_SERIALIZE_SPEC.md",
    "mag",
    "scripts",
    "bridge",
    "models",
    "artifacts",
    "handoff",
    "tools",
    "tests",
    "configs",
)
INDEX_SKIP_DIRS = SKIP_DIRS | {
    "dead_drops", "agent_uploads", "biography_backup", "biography_backup_20260825",
    "biography_backup_postrepair_20260825", "__pycache__",
}


def utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def walk_files() -> list[Path]:
    paths: list[Path] = []
    seen: set[Path] = set()
    for root_name in INDEX_PATHS:
        base = ROOT / root_name
        if base.is_file():
            if base not in seen:
                paths.append(base)
                seen.add(base)
            continue
        if not base.is_dir():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in INDEX_SKIP_DIRS and not d.startswith(".pytest-") and not d.startswith("biography_backup")]
            for name in filenames:
                path = Path(dirpath) / name
                if path not in seen:
                    paths.append(path)
                    seen.add(path)
    return paths


def chain_membership() -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    chain = ROOT / "memory/biography/verkle_chain.jsonl"
    rows, malformed = load_jsonl(chain)
    hashes = [str(row.get("leaf_hash")) for row in rows if row.get("leaf_hash")]
    roots = vk._merkle_prefix_roots(hashes) if hashes else []
    members: dict[str, dict[str, Any]] = {}
    for i, row in enumerate(rows):
        filename = str(row.get("filename") or "")
        if not filename:
            continue
        members[f"memory/biography/knots/{filename}"] = {
            "chain_index": i,
            "chain_root": roots[i] if i < len(roots) else None,
            "leaf_hash": row.get("leaf_hash"),
            "session_id": row.get("session_id"),
            "pointer_key": pointer_name(str(row.get("session_id") or "")),
        }
    return members, {"rows": len(rows), "malformed": malformed, "root": roots[-1] if roots else vk._h(b"empty")}


def knot_metadata(path: Path) -> dict[str, Any]:
    if path.suffix.lower() != ".json" or "/knots/" not in rel(path).lower():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        if isinstance(value, dict):
            return {k: value.get(k) for k in ("session_id", "leaf_hash", "schema", "filename") if value.get(k) is not None}
    except (OSError, json.JSONDecodeError):
        return {"parse": "failed"}
    return {}


def build() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    members, chain = chain_membership()
    entries: list[dict[str, Any]] = []
    counts: dict[str, dict[str, int]] = {}
    for path in walk_files():
        try:
            stat = path.stat()
        except OSError:
            continue
        relative = rel(path)
        cls = artifact_class(path)
        entry: dict[str, Any] = {
            "path": relative,
            "class": cls,
            "bytes": stat.st_size,
            "mtime_ns": stat.st_mtime_ns,
        }
        if relative in members:
            entry["chain"] = members[relative]
        if cls == "live_sha256_verkle" and "/knots/" in relative.lower():
            entry.update({f"knot_{k}": v for k, v in knot_metadata(path).items()})
            entry["hash_basis"] = "stored_leaf_hash"
        elif path.suffix.lower() in TEXT_SUFFIXES and stat.st_size <= MAX_HASH_BYTES and (
            cls in {"kzg_spec_or_fixture", "rib_or_trajectory", "receipt_or_manifest"}
            or relative.startswith("docs/")
            or relative.startswith("watch/")
            or relative.startswith("memory/runs/")
        ):
            digest = sha256_file(path)
            if digest:
                entry["sha256"] = digest
                entry["hash_basis"] = "file_bytes"
        counts.setdefault(cls, {"files": 0, "bytes": 0})
        counts[cls]["files"] += 1
        counts[cls]["bytes"] += stat.st_size
        entries.append(entry)
    entries.sort(key=lambda e: e["path"])
    meta = {
        "schema": SCHEMA,
        "built_at": utc(),
        "read_only_sources": True,
        "entry_count": len(entries),
        "total_bytes": sum(int(e["bytes"]) for e in entries),
        "by_class": dict(sorted(counts.items())),
        "chain": chain,
        "pointer_key_rule": "full session identity belongs in the index; truncated by-session filenames are legacy hints only",
        "lineages": {
            "live_sha256_verkle": "memory/biography/verkle_chain.jsonl + knots",
            "q_state_chain": "memory/ghost/q_state",
            "rib_or_trajectory": "watch and RIB/trajectory artifacts",
            "kzg_spec_or_fixture": "normative design only until executable proof code exists",
            "physical_or_model_artifact": "metadata-indexed; no model bytes copied or moved",
        },
        "source_changes": [],
    }
    return meta, entries


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--write", action="store_true", help="write derived JSONL index and metadata")
    args = parser.parse_args()
    meta, entries = build()
    if args.write:
        out_dir = ROOT / "memory/runs/verkle_recovery"
        out_dir.mkdir(parents=True, exist_ok=True)
        index_path = out_dir / "artifact_index_20260901.jsonl"
        meta_path = out_dir / "artifact_index_20260901.meta.json"
        index_path.write_text("".join(json.dumps(e, ensure_ascii=False, separators=(",", ":")) + "\n" for e in entries), encoding="utf-8")
        meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        meta["index_path"] = rel(index_path)
        meta["meta_path"] = rel(meta_path)
    print(json.dumps(meta, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
