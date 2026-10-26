#!/usr/bin/env python3
"""tools/veil_evaluator.py - Automated Veil & Public Snapshot Evaluator.

Implements Phase 2 of Project Aegis-Percolator:
- Measures the empirical strength of the Riddler-Face veil.
- Assesses whether a cold model exposed only to public estate artifacts
  can reconstruct the 10 core invariants without leaking private operator identity.
- Formula:
    Veil Metric (Vm) = Invariant Recovery Rate (R_inv) - Private Identity Leak Rate (L_id)
- Verdicts:
    VEIL_STRONG:    Vm >= 0.70 and L_id == 0.0 (passes socratic falsifier)
    VEIL_PERMEABLE: 0.50 <= Vm < 0.70 and L_id == 0.0 (invariants partially obscured)
    VEIL_OPAQUE:    Vm < 0.50 and L_id == 0.0 (too dense, stranger cannot reconstruct)
    VEIL_BREACHED:  L_id > 0.0 (private identity leaked)

CONSUMER: Aegis-Percolator Phase 2, Ouroboros, automated public export gates.
VERIFIER: tests/test_veil_evaluator.py.
HOUSE LAW: Strictly zero unicode em-dashes; zero side effects on failure; pure functions.
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 10 Canonical Estate Invariants for Veil Reconstruction
ESTATE_INVARIANTS = {
    "INV-01": {
        "name": "BYTE_PRESERVATION",
        "description": "Append-only ledger, trust bytes not claims, blank space preserved over rewrite",
        "keywords": [
            "blank space", "blank page", "not rewritten", "preserve", "append",
            "erased", "evidence", "ledger", "stable independent", "stayed put"
        ]
    },
    "INV-02": {
        "name": "RAIL_OVER_DIRECTION",
        "description": "Framework rails over instruction discretion, structural safety gates",
        "keywords": [
            "rail", "gate", "framework", "boundary", "constraint", "enforce", "rule"
        ]
    },
    "INV-03": {
        "name": "FALSIFIABILITY_GROUNDING",
        "description": "LAW-064 premise-span citation match, claims require verifiable grounds",
        "keywords": [
            "grounding", "citation", "verifiable", "falsifier", "proof", "evidence", "source"
        ]
    },
    "INV-04": {
        "name": "FLOOR_CHECKS_HASH",
        "description": "LAW-061 lying map detection, floor checks hash, verifying reality over painted claims",
        "keywords": [
            "map", "floor", "hash", "lying map", "trap", "fog", "unreliable map", "false route"
        ]
    },
    "INV-05": {
        "name": "RECEIPT_BEFORE_MUTATION",
        "description": "LAW-065 destructive actions require prior receipts and audit entries",
        "keywords": [
            "receipt", "audit", "destructive", "before overwrite", "log entry", "record"
        ]
    },
    "INV-06": {
        "name": "HONEST_ABSENCE_REFUSAL",
        "description": "Explicit honest refusal of false premises and absent entities",
        "keywords": [
            "does not contain", "no mention", "not mentioned", "nowhere in the text",
            "story has no", "there is no", "no porter", "no gardener"
        ]
    },
    "INV-07": {
        "name": "IDENTITY_SUPPRESSION",
        "description": "Neutral third-person voice, zero 1p-sg conversational ego leakage",
        "keywords": [
            "third person", "objective", "austere", "no ego", "unadorned"
        ]
    },
    "INV-08": {
        "name": "GRADUATED_SANCTIONS",
        "description": "Graduated responses to protocol violations and health drops",
        "keywords": [
            "sanction", "graduated", "warning", "demote", "ladder", "escalation"
        ]
    },
    "INV-09": {
        "name": "CLEAR_BOUNDARIES",
        "description": "Separation of public face from private knots and internal states",
        "keywords": [
            "boundary", "veil", "riddler", "isolation", "public", "private", "stranger"
        ]
    },
    "INV-10": {
        "name": "ASYNC_DECOUPLING",
        "description": "Reactive wakeup, zero busy polling, background task isolation",
        "keywords": [
            "reactive", "wakeup", "async", "background", "decoupled", "non-blocking"
        ]
    }
}

# Forbidden Identity Patterns (Private operator leaks)
FORBIDDEN_IDENTITY_PATTERNS = [
    re.compile(r"/mnt/c/Users/foste", re.IGNORECASE),
    re.compile(r"C:\\Users\\foste", re.IGNORECASE),
    re.compile(r"/home/foste", re.IGNORECASE),
    re.compile(r"\bfoste\b", re.IGNORECASE),
    re.compile(r"\bNacho\s*Foster\b", re.IGNORECASE),
    re.compile(r"sk-[a-zA-Z0-9]{20,}", re.IGNORECASE),
    re.compile(r"ghp_[a-zA-Z0-9]{20,}", re.IGNORECASE),
    re.compile(r"AIzaSy[a-zA-Z0-9_-]{33}", re.IGNORECASE),
]

FORBIDDEN_FILE_PATTERNS = [
    ".env",
    ".env.local",
    "memory/biography",
    "id_rsa",
    "id_ed25519",
]


def check_identity_leaks(text: str) -> List[str]:
    """Scan text for any private operator identity leaks or secret patterns."""
    leaks: List[str] = []
    for pattern in FORBIDDEN_IDENTITY_PATTERNS:
        matches = pattern.findall(text)
        if matches:
            leaks.append(f"Match for pattern {pattern.pattern}: {len(matches)} occurrence(s)")
    return leaks


def score_invariant_recovery(text: str) -> Dict[str, Any]:
    """Score which estate invariants are recovered from the evaluated text."""
    text_lower = text.lower()
    recovered: List[str] = []
    details: Dict[str, List[str]] = {}

    for inv_id, inv_data in ESTATE_INVARIANTS.items():
        matched_kw: List[str] = []
        for kw in inv_data["keywords"]:
            if kw.lower() in text_lower:
                matched_kw.append(kw)
        if matched_kw:
            recovered.append(inv_id)
            details[inv_id] = matched_kw

    recovery_rate = len(recovered) / len(ESTATE_INVARIANTS)
    return {
        "total_invariants": len(ESTATE_INVARIANTS),
        "recovered_count": len(recovered),
        "recovery_rate": round(recovery_rate, 4),
        "recovered_ids": recovered,
        "matched_keywords": details
    }


def compute_veil_metric(text: str) -> Dict[str, Any]:
    """Compute the Veil Metric (Vm = R_inv - L_id) and determine veil security status."""
    inv_score = score_invariant_recovery(text)
    leaks = check_identity_leaks(text)

    r_inv = inv_score["recovery_rate"]
    l_id = 1.0 if len(leaks) > 0 else 0.0
    vm = round(r_inv - l_id, 4)

    if l_id > 0:
        verdict = "VEIL_BREACHED"
        summary = "Private identity tokens leaked in text. Veil compromised."
    elif vm >= 0.70:
        verdict = "VEIL_STRONG"
        summary = "High invariant transmission with zero private identity leakage. Riddler-Face intact."
    elif vm >= 0.50:
        verdict = "VEIL_PERMEABLE"
        summary = "Invariants partially recovered (>=5/10) with zero identity leakage."
    else:
        verdict = "VEIL_OPAQUE"
        summary = "Insufficient invariant recovery (<5/10). Artifacts are too obscure for strangers."

    return {
        "veil_metric": vm,
        "recovery_rate": r_inv,
        "identity_leak_rate": l_id,
        "verdict": verdict,
        "summary": summary,
        "invariant_analysis": inv_score,
        "leaks_found": leaks
    }


def check_snapshot_cleanliness(file_paths: List[str]) -> Dict[str, Any]:
    """Check a candidate public file manifest for forbidden private files."""
    violations: List[str] = []
    for path in file_paths:
        norm = path.replace("\\", "/")
        for forbidden in FORBIDDEN_FILE_PATTERNS:
            if forbidden in norm:
                violations.append(f"Forbidden file pattern '{forbidden}' found in path: {path}")

    return {
        "total_checked": len(file_paths),
        "clean": len(violations) == 0,
        "violations": violations
    }


def evaluate_same_book_round2() -> Dict[str, Any]:
    """Evaluate stored cold model responses from canon/same_book/round2/."""
    round2_dir = os.path.join(ROOT, "canon", "same_book", "round2")
    if not os.path.exists(round2_dir):
        return {"error": "canon/same_book/round2 not found"}

    results: Dict[str, Any] = {
        "schema": "veil_evaluator.round2.v1",
        "models": {},
        "fleet_verdict": "UNKNOWN"
    }

    files = glob.glob(os.path.join(round2_dir, "battery2_*.md"))
    all_vm: List[float] = []

    for fpath in files:
        model_name = os.path.basename(fpath).replace("battery2_", "").replace(".md", "")
        with open(fpath, "r", encoding="utf-8") as fp:
            content = fp.read()
        eval_res = compute_veil_metric(content)
        results["models"][model_name] = eval_res
        all_vm.append(eval_res["veil_metric"])

    if all_vm:
        avg_vm = round(sum(all_vm) / len(all_vm), 4)
        results["average_veil_metric"] = avg_vm
        if any(res["verdict"] == "VEIL_BREACHED" for res in results["models"].values()):
            results["fleet_verdict"] = "VEIL_BREACHED"
        elif avg_vm >= 0.70:
            results["fleet_verdict"] = "VEIL_STRONG"
        elif avg_vm >= 0.50:
            results["fleet_verdict"] = "VEIL_PERMEABLE"
        else:
            results["fleet_verdict"] = "VEIL_OPAQUE"

    return results


def main() -> int:
    """CLI runner for Veil Evaluator."""
    print("=" * 70)
    print("VEIL EVALUATOR - Aegis-Percolator Phase 2")
    print("=" * 70)
    
    results = evaluate_same_book_round2()
    out_path = os.path.join(ROOT, "canon", "same_book", "veil_evaluation_results.json")
    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(results, fp, indent=2)

    print(f"Results written to: {out_path}")
    print(f"Fleet Verdict: {results.get('fleet_verdict')}")
    print(f"Average Veil Metric: {results.get('average_veil_metric')}")
    for model, data in results.get("models", {}).items():
        print(f" - {model:25s} Vm: {data['veil_metric']:0.4f} | R_inv: {data['recovery_rate']:0.2f} | Verdict: {data['verdict']}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
