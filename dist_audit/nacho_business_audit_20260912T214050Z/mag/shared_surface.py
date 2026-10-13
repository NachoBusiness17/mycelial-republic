"""Validate and expose the cross-client Mag shared surface.

This module is deliberately read-only. It does not move files or grant effects;
it gives host, container, WSL, editor, and CLI workers one deterministic way to
find the durable inbox and detect drift in its discovery pointers.

CLI::
    python -m mag.shared_surface path
    python -m mag.shared_surface status
    python -m mag.shared_surface validate
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
WATCH = ROOT / "watch"
INBOX = WATCH / "inbox"
INDEX = INBOX / "INDEX.json"
CONTRACT = INBOX / "SHARED_SURFACE_CONTRACT.json"
WARM_PACK = WATCH / "WARM_PACK.json"
CONTROL_FILES = {"INDEX.json", "INDEX.md", "SHARED_SURFACE_CONTRACT.json"}


def _load(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def inspect_surface() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    index: dict[str, Any] = {}
    contract: dict[str, Any] = {}
    warm: dict[str, Any] = {}

    if not INBOX.is_dir():
        errors.append(f"missing inbox: {INBOX}")
    if not INDEX.is_file():
        errors.append(f"missing index: {INDEX}")
    else:
        try:
            index = _load(INDEX)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid INDEX.json: {exc}")
    if not CONTRACT.is_file():
        errors.append(f"missing contract: {CONTRACT}")
    else:
        try:
            contract = _load(CONTRACT)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid SHARED_SURFACE_CONTRACT.json: {exc}")
    if WARM_PACK.is_file():
        try:
            warm = _load(WARM_PACK)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            errors.append(f"invalid WARM_PACK.json: {exc}")
    else:
        warnings.append(f"warm pack not found: {WARM_PACK}")

    indexed = {Path(str(item.get("path", ""))).name for item in index.get("items", [])
               if isinstance(item, dict)}
    files = sorted(path.name for path in INBOX.iterdir() if path.is_file()) if INBOX.is_dir() else []
    unindexed = [name for name in files if name not in indexed and name not in CONTROL_FILES]
    if unindexed:
        warnings.append("unindexed inbox files: " + ", ".join(unindexed))

    expected_root = "/board/inbox"
    if index.get("root") != expected_root:
        errors.append(f"INDEX root is {index.get('root')!r}, expected {expected_root!r}")
    if contract.get("canonical", {}).get("container") != expected_root:
        errors.append("contract container path does not match /board/inbox")
    warm_pointer = warm.get("discovery", {}).get("shared_inbox")
    if warm_pointer and warm_pointer.get("path") != "/board/inbox/INDEX.json":
        errors.append("WARM_PACK shared inbox pointer is incorrect")
    elif not warm_pointer:
        warnings.append("WARM_PACK has no shared inbox discovery pointer")

    indexed_items: list[dict[str, Any]] = []
    for item in index.get("items", []):
        if not isinstance(item, dict):
            errors.append("INDEX contains a non-object item")
            continue
        rel = Path(str(item.get("path", ""))).name
        target = INBOX / rel
        record = {"path": item.get("path"), "exists": target.is_file()}
        if not target.is_file():
            errors.append(f"indexed item missing: {item.get('path')}")
        recorded_hash = str(item.get("sha256") or "").upper()
        if recorded_hash and target.is_file():
            actual_hash = _sha256(target)
            record["sha256_match"] = actual_hash == recorded_hash
            if actual_hash != recorded_hash:
                errors.append(f"hash mismatch: {item.get('path')}")
        indexed_items.append(record)

    return {
        "schema": "shared_surface.status.v1",
        "ok": not errors,
        "root": str(ROOT),
        "paths": {
            "host": str(INBOX),
            "container": "/board/inbox",
            "wsl": "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox",
            "index": "/board/inbox/INDEX.json",
            "contract": "/board/inbox/SHARED_SURFACE_CONTRACT.json"
        },
        "files": files,
        "indexed_items": indexed_items,
        "unindexed_items": unindexed,
        "errors": errors,
        "warnings": warnings
    }


def main() -> int:
    parser = argparse.ArgumentParser(prog="python -m mag.shared_surface")
    parser.add_argument("command", choices=("path", "status", "validate"), nargs="?", default="status")
    args = parser.parse_args()
    if args.command == "path":
        print(json.dumps({
            "schema": "shared_surface.path.v1",
            "host": str(INBOX),
            "container": "/board/inbox",
            "wsl": "/mnt/c/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox",
            "read_first": "/board/inbox/INDEX.json"
        }, indent=2))
        return 0
    result = inspect_surface()
    print(json.dumps(result, indent=2))
    return 0 if result["ok"] or args.command == "status" else 1


if __name__ == "__main__":
    raise SystemExit(main())
