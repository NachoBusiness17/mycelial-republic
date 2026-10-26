"""mag/contract_widening.py - Organ 4 Contract Widening verification engine.

Spec: watch/inbox/ORG_SYSTEM_V2_20261018.md (Organ 4 - CONTRACT WIDENING).
Widens the shared surface contract to cover:
1. Extended surfaces: queue/ and bridge/ directories and structures.
2. Handoff integrity: every handoff row crossing surfaces must carry sha256 and receipt (Falsifier F4).
3. Recursive subdirectory orphan detection: walks watch/inbox to full depth.
4. Root %TEMP%* fossil patrol: checks repo root for transient file leaks.
5. Promotion ledger verification: ensures accepted artifacts land via watch/inbox/PROMOTION_LEDGER.jsonl.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.root_temp_sweep_patrol import scan_root_fossils
from tools.surface_orphan_walk import (
    CONTROL_FILES,
    find_orphans,
    strip_inbox_prefix,
    walk_inbox_files,
)

WIDENING_TS_THRESHOLD = "2026-10-18T00:00:00Z"


def check_extended_surfaces(
    root: Path, errors: list[str], warnings: list[str]
) -> dict[str, Any]:
    """Verify queue/ and bridge/ directories exist and are structured."""
    queue_dir = root / "queue"
    bridge_dir = root / "bridge"

    queue_ok = queue_dir.is_dir()
    bridge_ok = bridge_dir.is_dir()

    if not queue_ok:
        errors.append(f"missing extended surface queue: {queue_dir}")
    if not bridge_ok:
        errors.append(f"missing extended surface bridge: {bridge_dir}")

    queue_subdirs = ["handoff", "lanes", "results"]
    bridge_subdirs = ["inbox", "outboxes"]

    missing_queue_subs = [s for s in queue_subdirs if not (queue_dir / s).is_dir()]
    missing_bridge_subs = [s for s in bridge_subdirs if not (bridge_dir / s).is_dir()]

    if missing_queue_subs:
        warnings.append(
            f"queue missing standard subdirs: {', '.join(missing_queue_subs)}"
        )
    if missing_bridge_subs:
        warnings.append(
            f"bridge missing standard subdirs: {', '.join(missing_bridge_subs)}"
        )

    return {
        "queue_ok": queue_ok,
        "bridge_ok": bridge_ok,
        "missing_subdirs": missing_queue_subs + missing_bridge_subs,
    }


def check_handoff_integrity(
    root: Path, errors: list[str], warnings: list[str]
) -> dict[str, Any]:
    """Check that handoff rows in queue/handoff and bridge/ carry sha256 and receipt.

    Falsifier F4: if handoff rows still cross surfaces hashless, Organ 4 is a cow.
    Legacy rows prior to WIDENING_TS_THRESHOLD are grandfathered; new rows require hashes.
    """
    queue_handoff = root / "queue" / "handoff"
    bridge_inbox = root / "bridge" / "inbox"

    scanned = 0
    grandfathered = 0
    compliant = 0
    violations: list[str] = []

    if queue_handoff.is_dir():
        for p in queue_handoff.glob("*.json"):
            if not p.is_file():
                continue
            scanned += 1
            try:
                data = json.loads(p.read_text(encoding="utf-8"))
            except Exception:
                continue

            # Check if this object is a handoff record
            is_handoff = (
                isinstance(data, dict)
                and (
                    "handoff" in str(data.get("schema", "")).lower()
                    or p.name.startswith("HANDOFF-")
                    or p.name.startswith("peer-")
                )
            )
            if not is_handoff:
                continue

            has_hash = bool(data.get("sha256") or data.get("hash"))
            has_receipt = bool(data.get("receipt") or data.get("receipt_path"))
            ts = str(data.get("ts") or "")
            if not ts:
                import datetime
                mtime = p.stat().st_mtime
                ts = datetime.datetime.fromtimestamp(mtime, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

            if has_hash and has_receipt:
                compliant += 1
            elif ts < WIDENING_TS_THRESHOLD:
                grandfathered += 1
            else:
                violations.append(f"{p.name} (missing sha256 or receipt)")

    if bridge_inbox.is_dir():
        for p in bridge_inbox.glob("*.jsonl"):
            if not p.is_file():
                continue
            try:
                lines = p.read_text(encoding="utf-8").splitlines()
            except Exception:
                continue
            for line_no, line in enumerate(lines, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except Exception:
                    continue
                scanned += 1
                ts = str(row.get("ts") or "")
                if not ts:
                    import datetime
                    mtime = p.stat().st_mtime
                    ts = datetime.datetime.fromtimestamp(mtime, tz=datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
                has_hash = bool(row.get("sha256") or row.get("hash"))
                has_receipt = bool(row.get("receipt") or row.get("receipt_path"))

                if has_hash and has_receipt:
                    compliant += 1
                elif ts < WIDENING_TS_THRESHOLD:
                    grandfathered += 1
                else:
                    violations.append(
                        f"{p.name}:{line_no} (missing sha256 or receipt)"
                    )

    for v in violations:
        errors.append(f"handoff row missing sha256 or receipt: {v}")

    return {
        "scanned": scanned,
        "compliant": compliant,
        "grandfathered": grandfathered,
        "violations": violations,
    }


def check_subdirectory_orphans(
    inbox: Path, index: dict[str, Any], warnings: list[str]
) -> dict[str, Any]:
    """Walk watch/inbox to full depth and report unindexed orphans by relative path."""
    if not inbox.is_dir():
        return {"orphans_total": 0, "orphans": []}

    try:
        report = find_orphans(inbox, inbox / "INDEX.json")
        total = report["orphans_total"]
        if total > 0:
            sample = report["orphans"][:10]
            warnings.append(
                f"unindexed inbox files: {total} orphans across subdirectories "
                f"(sample: {', '.join(sample)})"
            )
        return report
    except Exception as exc:
        warnings.append(f"surface orphan walk failed: {exc}")
        return {"orphans_total": 0, "orphans": [], "error": str(exc)}


def check_root_temp_fossils(root: Path, warnings: list[str]) -> list[str]:
    """Detect transient %TEMP%* fossils in repository root."""
    try:
        fossils = scan_root_fossils(root)
        fossil_names = [f.name for f in fossils]
        if fossil_names:
            warnings.append(
                f"root temp fossils detected: {len(fossil_names)} items "
                f"(run tools/root_temp_sweep_patrol.py to sweep)"
            )
        return fossil_names
    except Exception as exc:
        warnings.append(f"root temp scan failed: {exc}")
        return []


def check_promotion_ledger(
    inbox: Path, errors: list[str], warnings: list[str]
) -> dict[str, Any]:
    """Validate watch/inbox/PROMOTION_LEDGER.jsonl exists and has required schema."""
    ledger_path = inbox / "PROMOTION_LEDGER.jsonl"
    if not ledger_path.is_file():
        errors.append(f"missing promotion ledger: {ledger_path}")
        return {"ok": False, "count": 0}

    required = [
        "schema",
        "ts",
        "source_path",
        "sha256",
        "dest_path",
        "promoted_by",
        "receipt_path",
    ]
    count = 0
    invalid_rows = 0

    try:
        lines = ledger_path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            count += 1
            missing = [k for k in required if not row.get(k)]
            if missing:
                invalid_rows += 1
                errors.append(
                    f"promotion ledger line {idx} missing fields: {', '.join(missing)}"
                )
    except Exception as exc:
        errors.append(f"unreadable promotion ledger: {exc}")
        return {"ok": False, "count": count}

    return {"ok": invalid_rows == 0, "count": count, "invalid_rows": invalid_rows}


def widened_contract_check(
    root: Path,
    contract: dict[str, Any],
    index: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    """Run full widened contract verification pass."""
    inbox = root / "watch" / "inbox"

    surfaces = check_extended_surfaces(root, errors, warnings)
    handoffs = check_handoff_integrity(root, errors, warnings)
    orphans = check_subdirectory_orphans(inbox, index, warnings)
    root_fossils = check_root_temp_fossils(root, warnings)
    promotions = check_promotion_ledger(inbox, errors, warnings)

    return {
        "schema": "contract_widening.status.v1",
        "extended_surfaces": surfaces,
        "handoffs": handoffs,
        "orphans": {
            "total": orphans.get("orphans_total", 0),
            "sample": orphans.get("orphans", [])[:10],
        },
        "root_temp_fossils": {
            "total": len(root_fossils),
            "sample": root_fossils[:10],
        },
        "promotion_ledger": promotions,
    }
