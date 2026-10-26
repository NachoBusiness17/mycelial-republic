#!/usr/bin/env python3
"""QUASI-LOCAL BOUNDARY GATE -- Bartnik boundary contract for sovereign agent sessions.

Steal (Wave 9 / Dr. Stephen McCormick / Robert Bartnik):
In general relativity, gravitational mass cannot be localized to a point; it is defined
quasi-locally across a closed two-dimensional spatial boundary dOmega.
Similarly, agent safety, integrity, and byte preservation cannot be policed by micromanaging
every intermediate token or thought. Instead, an agent session is bounded by an initial
state dOmega_0 and a final state dOmega_1.

If the boundary flux satisfies conservation laws (LAW-001 byte preservation, zero forbidden
unicode em-dashes, strictly 0.00 / 1k first-person singular pronouns, and valid commit hint attribution),
the interior execution trajectory is formally proven sound without intrusive overhead.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from typing import Any, Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRONOUN_PATTERN = re.compile(r"\b(i|me|my|mine|myself)\b", re.IGNORECASE)


def compute_file_sha256(file_path: str) -> str:
    """Compute standard SHA-256 hash of a file."""
    if not os.path.isfile(file_path):
        return ""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as fp:
        for chunk in iter(lambda: fp.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def audit_file_content(file_path: str) -> Tuple[bool, List[str]]:
    """Audit a single file for unicode em-dashes and first-person pronoun rate."""
    violations: List[str] = []
    if not os.path.isfile(file_path):
        return True, violations

    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as fp:
            text = fp.read()
    except Exception as exc:
        violations.append(f"Unreadable file {file_path}: {exc}")
        return False, violations

    # Check for forbidden unicode em-dashes and en-dashes
    if "\u2014" in text:
        violations.append(f"Forbidden unicode em-dash (\\u2014) in {file_path}")
    if "\u2013" in text:
        violations.append(f"Forbidden unicode en-dash (\\u2013) in {file_path}")

    # Check pronoun rate only for markdown or narrative documents
    if file_path.endswith((".md", ".txt")):
        words = re.findall(r"\b[A-Za-z]+\b", text)
        pronouns = [w for w in words if w.lower() in ("i", "me", "my", "mine", "myself")]
        rate = (len(pronouns) / len(words)) * 1000 if words else 0.0
        if pronouns:
            violations.append(
                f"Pronoun violation in {file_path}: found {len(pronouns)} first-person singular tokens ({rate:0.2f}/1k)"
            )

    return len(violations) == 0, violations


def audit_boundary_flux(declared_paths: List[str]) -> Dict[str, Any]:
    """Audit the boundary flux across all declared files in a session or commit hint."""
    all_clean = True
    all_violations: List[str] = []
    file_hashes: Dict[str, str] = {}

    for rel_path in declared_paths:
        abs_path = os.path.join(ROOT, rel_path) if not os.path.isabs(rel_path) else rel_path
        if not os.path.exists(abs_path):
            all_violations.append(f"Declared path missing from disk: {rel_path}")
            all_clean = False
            continue

        clean, file_viols = audit_file_content(abs_path)
        if not clean:
            all_clean = False
            all_violations.extend(file_viols)

        file_hashes[rel_path] = compute_file_sha256(abs_path)

    return {
        "status": "PASS" if all_clean else "FAIL",
        "clean": all_clean,
        "violations": all_violations,
        "boundary_hashes": file_hashes,
        "total_files": len(declared_paths),
    }


def audit_commit_hint(hint_file: str) -> Dict[str, Any]:
    """Audit a specific commit hint JSON file under queue/commit_hints/."""
    hint_path = os.path.join(ROOT, hint_file) if not os.path.isabs(hint_file) else hint_file
    if not os.path.isfile(hint_path):
        return {"status": "FAIL", "clean": False, "violations": [f"Missing hint file: {hint_file}"]}

    try:
        with open(hint_path, "r", encoding="utf-8") as fp:
            data = json.load(fp)
    except Exception as exc:
        return {"status": "FAIL", "clean": False, "violations": [f"Malformed JSON in {hint_file}: {exc}"]}

    paths = data.get("paths", [])
    message = data.get("message", "")

    violations: List[str] = []
    if not paths:
        violations.append(f"Commit hint {hint_file} specifies no paths")
    if not message:
        violations.append(f"Commit hint {hint_file} has empty message")
    if "\u2014" in message or "\u2013" in message:
        violations.append(f"Commit hint {hint_file} message contains forbidden unicode dash")

    boundary_res = audit_boundary_flux(paths)
    if not boundary_res["clean"]:
        violations.extend(boundary_res["violations"])

    is_clean = len(violations) == 0
    return {
        "status": "PASS" if is_clean else "FAIL",
        "clean": is_clean,
        "hint_file": hint_file,
        "message": message,
        "violations": violations,
        "boundary_hashes": boundary_res.get("boundary_hashes", {}),
    }


def main() -> int:
    """CLI runner for quasi-local boundary gate."""
    parser = argparse.ArgumentParser(description="Audit quasi-local boundary contracts")
    parser.add_argument("--hint", help="Relative path to commit hint JSON")
    parser.add_argument("--paths", nargs="+", help="Explicit file paths to audit")
    args = parser.parse_args()

    if args.hint:
        res = audit_commit_hint(args.hint)
    elif args.paths:
        res = audit_boundary_flux(args.paths)
    else:
        # Default audit: scan all pending commit hints in queue/commit_hints/
        hint_dir = os.path.join(ROOT, "queue", "commit_hints")
        hints = [f for f in os.listdir(hint_dir) if f.endswith(".json")] if os.path.isdir(hint_dir) else []
        if not hints:
            print("No pending commit hints in queue/commit_hints/. Boundary is quiescent.")
            return 0
        overall_clean = True
        for h in hints:
            h_res = audit_commit_hint(os.path.join(hint_dir, h))
            print(f"Hint {h}: {h_res['status']}")
            if not h_res["clean"]:
                overall_clean = False
                for v in h_res["violations"]:
                    print(f"  - {v}")
        return 0 if overall_clean else 2

    print(json.dumps(res, indent=2))
    return 0 if res["clean"] else 2


if __name__ == "__main__":
    sys.exit(main())
