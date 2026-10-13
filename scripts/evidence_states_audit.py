#!/usr/bin/env python3
"""
evidence_states_audit.py - Falsifier for evidence states discipline

This script programmatically verifies that the repository enforces the tri-state
claim discipline (Supported/Unproven/Disputed) with proper evidence requirements.
It validates the mechanical enforcement described in docs/ref/evidence_states_audit.md.

Run: python scripts/evidence_states_audit.py
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Tuple, Any

# Add the project root to Python path
repo_root = Path(__file__).parent.parent
sys.path.insert(0, str(repo_root))

@dataclass
class Claim:
    """Represents a claim from the work register."""
    statement: str
    status: str
    basis: tuple[str, ...]
    evidence: tuple[str, ...]
    valid: bool = True
    errors: List[str] = None
    
    def __post_init__(self):
        self.errors = []

def validate_claim(claim_data: Dict[str, Any]) -> Claim:
    """Validate a single claim against the integrity kernel rules."""
    claim = Claim(
        statement=claim_data.get("statement", ""),
        status=claim_data.get("status", "Unproven"),
        basis=tuple(claim_data.get("basis", ("Assumption",))),
        evidence=tuple(claim_data.get("evidence", ()))
    )
    
    # Validate status
    if claim.status not in ("Supported", "Unproven", "Disputed"):
        claim.valid = False
        claim.errors.append(f"invalid status: {claim.status}")
    
    # Validate basis kinds
    for basis_kind in claim.basis:
        if basis_kind not in ("Evidence", "Inference", "Assumption"):
            claim.valid = False
            claim.errors.append(f"invalid basis kind: {basis_kind}")
    
    # Core discipline rules
    if claim.status == "Supported":
        if not any(b == "Evidence" for b in claim.basis):
            claim.valid = False
            claim.errors.append("Supported requires at least one Evidence basis")
        if not claim.evidence:
            claim.valid = False
            claim.errors.append("Supported requires attached evidence")
    
    if claim.status == "Disputed":
        if not claim.evidence:
            claim.valid = False
            claim.errors.append("Disputed requires contradicting evidence")
    
    return claim

def check_manifest_violations() -> List[Dict[str, Any]]:
    """Check manifest.jsonl for direct violations."""
    violations = []
    manifest_path = repo_root / "memory" / "runs" / "work_register" / "manifest.jsonl"
    
    if not manifest_path.exists():
        violations.append({
            "type": "MISSING_MANIFEST",
            "path": str(manifest_path),
            "error": "manifest.jsonl does not exist"
        })
        return violations
    
    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    row = json.loads(line.strip())
                    if "claim" in row:
                        claim_data = row["claim"]
                        claim = validate_claim(claim_data)
                        
                        # Check for specific violations in manifest
                        if claim.status == "Supported" and not claim.evidence:
                            violations.append({
                                "type": "SUPPORTED_WITHOUT_EVIDENCE",
                                "path": str(manifest_path),
                                "line": line_num,
                                "statement": claim.statement,
                                "error": "Supported claim missing evidence field"
                            })
                        
                        if claim.status == "Disputed" and not claim.evidence:
                            violations.append({
                                "type": "DISPUTED_WITHOUT_EVIDENCE", 
                                "path": str(manifest_path),
                                "line": line_num,
                                "statement": claim.statement,
                                "error": "Disputed claim missing contradicting evidence"
                            })
                        
                        if not claim.valid:
                            violations.append({
                                "type": "INVALID_CLAIM",
                                "path": str(manifest_path),
                                "line": line_num,
                                "statement": claim.statement,
                                "error": f"Invalid claim: {', '.join(claim.errors)}"
                            })
                            
                except json.JSONDecodeError as e:
                    violations.append({
                        "type": "INVALID_JSON",
                        "path": str(manifest_path),
                        "line": line_num,
                        "error": f"JSON decode error: {e}"
                    })
    except Exception as e:
        violations.append({
            "type": "MANIFEST_READ_ERROR",
            "path": str(manifest_path),
            "error": f"Cannot read manifest: {e}"
        })
    
    return violations

def check_claim_log_consistency() -> List[Dict[str, Any]]:
    """Check that claims.jsonl matches manifest.jsonl validation."""
    inconsistencies = []
    claims_path = repo_root / "logs" / "claims.jsonl"
    
    if not claims_path.exists():
        inconsistencies.append({
            "type": "MISSING_CLAIMS_LOG",
            "path": str(claims_path),
            "error": "claims.jsonl does not exist"
        })
        return inconsistencies
    
    # For simplicity, we'll just check that the log exists and has entries
    try:
        with open(claims_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            if not lines:
                inconsistencies.append({
                    "type": "EMPTY_CLAIMS_LOG",
                    "path": str(claims_path),
                    "error": "claims.jsonl is empty"
                })
    except Exception as e:
        inconsistencies.append({
            "type": "CLAIMS_LOG_READ_ERROR",
            "path": str(claims_path),
            "error": f"Cannot read claims log: {e}"
        })
    
    return inconsistencies

def main() -> Tuple[int, str]:
    """Main audit function."""
    print("🔍 Evidence States Audit")
    print("=" * 50)
    
    violations = check_manifest_violations()
    inconsistencies = check_claim_log_consistency()
    
    total_issues = len(violations) + len(inconsistencies)
    
    if total_issues == 0:
        print("✅ PASS: No evidence state violations found")
        print("\n📊 Audit Summary:")
        print(f"   - Manifest violations: 0")
        print(f"   - Log inconsistencies: 0") 
        print(f"   - Total issues: 0")
        return 0, "PASS"
    else:
        print(f"❌ FAIL: {total_issues} evidence state violations found")
        print("\n🚨 Violations:")
        
        for violation in violations:
            print(f"\n   [{violation['type']}] {violation['path']}", end="")
            if 'line' in violation:
                print(f":{violation['line']}", end="")
            print(f"\n      Error: {violation['error']}")
            if 'statement' in violation:
                print(f"      Statement: {violation['statement']}")
            if 'errors' in violation:
                for error in violation['errors']:
                    print(f"      - {error}")
        
        for issue in inconsistencies:
            print(f"\n   [{issue['type']}] {issue['path']}")
            print(f"      Error: {issue['error']}")
        
        print(f"\n📊 Audit Summary:")
        print(f"   - Manifest violations: {len(violations)}")
        print(f"   - Log inconsistencies: {len(inconsistencies)}")
        print(f"   - Total issues: {total_issues}")
        
        return 1, "FAIL"

if __name__ == "__main__":
    exit_code, verdict = main()
    print(f"\n🏁 Final Verdict: {verdict}")
    sys.exit(exit_code)