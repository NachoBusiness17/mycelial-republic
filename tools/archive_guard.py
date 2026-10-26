#!/usr/bin/env python3
"""archive_guard.py - Triple-gated safe archival guard.

Never deletes anything. Before clearing a file to go to trash, three things must be true:
1. Live SHA-256 hash of the verified copy matches the original at this moment.
2. Written confirmations are present: where the second copy lives, and that export is complete.
3. The file is not in a protected category (banking, medical, tax, ID, work, school, family).

Refuses with exact reasons if any condition fails. Leaves original files untouched.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any

# Protected category patterns (case-insensitive)
# Uses negative lookaround on alphanumeric characters so that underscores, hyphens,
# and file extensions act as valid word delimiters.
PROTECTED_PATTERNS = {
    "banking": re.compile(
        r"(?<![a-zA-Z0-9])(bank|statement|checking|savings|loan|mortgage|credit|wire|deposit|routing)(?![a-zA-Z0-9])",
        re.I,
    ),
    "medical": re.compile(
        r"(?<![a-zA-Z0-9])(medical|health|doctor|prescription|patient|clinic|hospital|therapy|diagnosis)(?![a-zA-Z0-9])",
        re.I,
    ),
    "tax": re.compile(
        r"(?<![a-zA-Z0-9])(tax|irs|w2|1099|deduction|tax[_\s-]?return|w[_\s-]?2|1099[_\s-]?misc)(?![a-zA-Z0-9])",
        re.I,
    ),
    "government_id": re.compile(
        r"(?<![a-zA-Z0-9])(passport|ssn|social[_\s-]?security|driver[_\s-]?license|license|birth[_\s-]?cert|visa|gov[_\s-]?id)(?![a-zA-Z0-9])",
        re.I,
    ),
    "work": re.compile(
        r"(?<![a-zA-Z0-9])(work|paystub|payroll|timesheet|employer|contract[_\s-]?employment)(?![a-zA-Z0-9])",
        re.I,
    ),
    "school": re.compile(
        r"(?<![a-zA-Z0-9])(school|transcript|grades|tuition|diploma|student[_\s-]?id|coursework)(?![a-zA-Z0-9])",
        re.I,
    ),
    "family": re.compile(
        r"(?<![a-zA-Z0-9])(minor|child|kid|parental|guardian|family|family[_\s-]?trust)(?![a-zA-Z0-9])",
        re.I,
    ),
}


def compute_sha256(path: Path) -> str:
    """Compute uppercase SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def check_protected_categories(filename: str, content_preview: str = "") -> list[str]:
    """Check if filename or preview text triggers any protected categories."""
    triggered: list[str] = []
    text_to_scan = f"{filename} {content_preview}"
    for category, regex in PROTECTED_PATTERNS.items():
        if regex.search(text_to_scan):
            triggered.append(category)
    return triggered


class ArchiveGuard:
    """Enforces the triple-gate safety protocol before clearing files to trash."""

    def __init__(self, trash_dir: Path | None = None) -> None:
        self.trash_dir = trash_dir or (Path.home() / ".archive_trash")

    def evaluate_file(
        self,
        original_file: Path,
        copy_file: Path,
        confirmations: dict[str, Any],
        original_inventory: list[str] | set[str] | None = None,
    ) -> dict[str, Any]:
        """Evaluate a file against all 3 safety gates.

        Returns decision report:
        {
            "cleared": bool,
            "reasons": list[str],
            "file": str,
            "gates": {"gate1_hash": bool, "gate2_confirmations": bool, "gate3_protected": bool}
        }
        """
        reasons: list[str] = []
        gates = {
            "inventory_match": True,
            "gate1_hash": False,
            "gate2_confirmations": False,
            "gate3_protected": True,
        }

        # Inventory check
        if original_inventory is not None:
            norm_orig = original_file.name
            if norm_orig not in original_inventory and str(original_file) not in original_inventory:
                gates["inventory_match"] = False
                reasons.append(f"File '{norm_orig}' is not in the original approved inventory list.")

        # Gate 1: Live Hash Verification
        if not original_file.is_file():
            reasons.append(f"Original file missing: {original_file}")
        elif not copy_file.is_file():
            reasons.append(f"Verified copy file missing: {copy_file}")
        else:
            orig_hash = compute_sha256(original_file)
            copy_hash = compute_sha256(copy_file)
            if orig_hash == copy_hash:
                gates["gate1_hash"] = True
            else:
                reasons.append(
                    f"Live hash mismatch: original ({orig_hash[:12]}...) != copy ({copy_hash[:12]}...). "
                    "Copy may be corrupted or altered."
                )

        # Gate 2: Written Confirmations
        sec_loc = confirmations.get("second_copy_location")
        export_done = confirmations.get("export_complete")

        has_sec = bool(sec_loc and str(sec_loc).strip() and str(sec_loc).strip().lower() != "none")
        has_exp = bool(export_done is True)

        if has_sec and has_exp:
            gates["gate2_confirmations"] = True
        else:
            if not has_sec:
                reasons.append("Missing written confirmation of where the second copy lives.")
            if not has_exp:
                reasons.append("Missing written confirmation that the export is complete.")

        # Gate 3: Protected Category Exclusion
        sample_preview = ""
        if original_file.is_file():
            try:
                with original_file.open("r", encoding="utf-8", errors="ignore") as f:
                    sample_preview = f.read(4096)
            except Exception:
                pass

        protected_hits = check_protected_categories(original_file.name, sample_preview)
        if protected_hits:
            gates["gate3_protected"] = False
            reasons.append(
                f"File belongs to protected category ({', '.join(protected_hits)}). "
                "Archival Bot never moves or trashes banking, medical, tax, ID, work, school or family files."
            )

        cleared = (
            gates["inventory_match"]
            and gates["gate1_hash"]
            and gates["gate2_confirmations"]
            and gates["gate3_protected"]
        )

        return {
            "cleared": cleared,
            "reasons": reasons,
            "file": str(original_file),
            "original_name": original_file.name,
            "gates": gates,
        }

    def clear_to_trash(
        self,
        original_file: Path,
        copy_file: Path,
        confirmations: dict[str, Any],
        original_inventory: list[str] | set[str] | None = None,
    ) -> dict[str, Any]:
        """Evaluate file and, if cleared, move to safe trash folder (never delete)."""
        report = self.evaluate_file(original_file, copy_file, confirmations, original_inventory)
        if not report["cleared"]:
            report["action"] = "REFUSED"
            report["message"] = "Refused to touch file. Original is untouched."
            return report

        # Execute safe move to trash
        self.trash_dir.mkdir(parents=True, exist_ok=True)
        trash_target = self.trash_dir / original_file.name
        if trash_target.exists():
            trash_target = self.trash_dir / f"{original_file.name}.trash_{os.getpid()}"

        shutil.move(str(original_file), str(trash_target))
        report["action"] = "MOVED_TO_TRASH"
        report["trash_path"] = str(trash_target)
        report["message"] = f"Original safely moved to trash: {trash_target}. Copy verified."
        return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Archive Guard triple-gate check.")
    parser.add_argument("--original", type=Path, required=True, help="Original file path")
    parser.add_argument("--copy", type=Path, required=True, help="Verified copy path")
    parser.add_argument("--second-copy", type=str, required=True, help="Written location of second copy")
    parser.add_argument("--export-complete", action="store_true", help="Confirm export is complete")
    parser.add_argument("--trash-dir", type=Path, default=None, help="Trash destination directory")
    parser.add_argument("--execute", action="store_true", help="Perform move to trash if cleared")

    args = parser.parse_args()
    guard = ArchiveGuard(trash_dir=args.trash_dir)
    confirmations = {
        "second_copy_location": args.second_copy,
        "export_complete": args.export_complete,
    }

    if args.execute:
        res = guard.clear_to_trash(args.original, args.copy, confirmations)
    else:
        res = guard.evaluate_file(args.original, args.copy, confirmations)

    print(json.dumps(res, indent=2))
    return 0 if res["cleared"] else 1


if __name__ == "__main__":
    sys.exit(main())
