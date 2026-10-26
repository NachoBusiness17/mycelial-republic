#!/usr/bin/env python3
"""root_temp_sweep_patrol.py - Root directory %TEMP%* fossil patrol and sweeper.

G1 Organ 4 Contract Widening (2026-10-18, watch/inbox/ORG_SYSTEM_V2_20261018.md).
Detects and sweeps transient files dumped into the repository root by scripts
that failed to properly expand %TEMP% or prefix destination paths.

Contract:
- B2-338 headline output:
    Clean:   ROOT-TEMP-PATROL: ok (0 fossils)
    Warning: ROOT-TEMP-PATROL: WARN (<n> root temp fossils found)
- Exit code 0 for clean or warnings (WARN-first discipline), exit 1 with --strict,
  exit 2 on error/cannot verify.
- Sweep action (--sweep / --quarantine) safely relocates fossils into a quarantine
  directory instead of destructive deletion, preserving evidence.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUARANTINE = ROOT / "watch" / "inbox" / "quarantine_temp_fossils"

# Exact fossil patterns matching root transient dump signatures
PROHIBITED_PATTERNS = [
    "%TEMP%*",
    "C?Users*Temp*",
    "Users*Temp*",
    "Temp",
]


def is_root_fossil(name: str) -> bool:
    """Return True if name matches any root temp fossil pattern."""
    for pat in PROHIBITED_PATTERNS:
        if fnmatch.fnmatch(name, pat):
            return True
    return False


def scan_root_fossils(root_path: Path) -> list[Path]:
    """Scan the root directory for any file or directory matching fossil patterns."""
    if not root_path.is_dir():
        raise ValueError(f"Root path is not a directory: {root_path}")
    found: list[Path] = []
    for item in root_path.iterdir():
        if is_root_fossil(item.name):
            found.append(item)
    return sorted(found, key=lambda p: p.name.lower())


def quarantine_fossils(fossils: list[Path], dest_dir: Path) -> list[dict[str, str]]:
    """Move fossils into destination quarantine directory preserving names."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    moved: list[dict[str, str]] = []
    for f in fossils:
        target = dest_dir / f.name
        # If target already exists, append a safe suffix
        if target.exists():
            target = dest_dir / f"{f.name}.quarantined_{f.stat().st_mtime_ns}"
        shutil.move(str(f), str(target))
        moved.append({"source": f.name, "destination": str(target)})
    return moved


def render_report(fossils: list[Path], root_path: Path, quarantine_results: list[dict[str, str]] | None = None) -> dict[str, Any]:
    return {
        "schema": "root_temp_sweep_patrol.v1",
        "root": str(root_path),
        "total_fossils": len(fossils),
        "fossils": [f.name for f in fossils],
        "quarantined": quarantine_results or [],
        "ok": len(fossils) == 0,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="root_temp_sweep_patrol",
        description="Patrol and sweep root %TEMP%* fossils in repository root.",
    )
    parser.add_argument("--root", type=Path, default=ROOT, help="Target repository root")
    parser.add_argument("--json", action="store_true", help="Output pure JSON")
    parser.add_argument("--strict", action="store_true", help="Exit 1 if fossils found")
    parser.add_argument("--sweep", action="store_true", help="Quarantine found fossils")
    parser.add_argument("--quarantine-dir", type=Path, default=DEFAULT_QUARANTINE, help="Destination directory for swept fossils")

    args = parser.parse_args(argv)

    try:
        fossils = scan_root_fossils(args.root)
    except Exception as exc:
        if args.json:
            print(json.dumps({"schema": "root_temp_sweep_patrol.v1", "ok": False, "error": str(exc)}))
        else:
            print(f"ROOT-TEMP-PATROL: ERROR - {exc}")
        return 2

    quarantined = None
    if args.sweep and fossils:
        quarantined = quarantine_fossils(fossils, args.quarantine_dir)
        # Re-scan after quarantine
        fossils = scan_root_fossils(args.root)

    report = render_report(fossils, args.root, quarantined)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        count = report["total_fossils"]
        if count == 0:
            print("ROOT-TEMP-PATROL: ok (0 fossils)")
        else:
            print(f"ROOT-TEMP-PATROL: WARN ({count} root temp fossils found)")
            for name in report["fossils"][:20]:
                print(f"  - {name}")
            if count > 20:
                print(f"  ... and {count - 20} more")
        if quarantined:
            print(f"  Swept {len(quarantined)} fossils to: {args.quarantine_dir}")

    if args.strict and report["total_fossils"] > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
