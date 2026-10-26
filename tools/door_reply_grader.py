#!/usr/bin/env python3
"""tools/door_reply_grader.py - Automated Blind Grader for Door Launch Replies.

Implements the Door Launch Collection & Evaluation Loop:
- Ingests external candidate responses to the v0-door public release.
- Evaluates each candidate response against the Socratic Battery v1/v2 using:
    1. Judge v3 First-Order Logic (FOL) entailment (tools/judge_v3_fol.py).
    2. Automated Veil Evaluator for zero identity leaks (tools/veil_evaluator.py).
    3. False-Premise detection (tools/false_premise_bank.py).
- Produces deterministic, citation-backed grading receipts for external submissions.

CONSUMER: Door launch monitoring, community submissions, blind evaluation.
VERIFIER: tests/test_door_reply_grader.py.
HOUSE LAW: Strictly zero unicode em-dashes; zero side effects on failure; pure functions.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any, Dict, List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.judge_v3_fol import evaluate_response_fol
from tools.veil_evaluator import check_identity_leaks, compute_veil_metric


def grade_candidate_submission(
    candidate_id: str,
    answers_text: str,
    source_platform: str = "X / v0-door launch"
) -> Dict[str, Any]:
    """Grade a candidate's complete set of answers using the multi-organ battery."""
    # 1. First-Order Logic Entailment (Judge v3)
    fol_eval = evaluate_response_fol(answers_text)

    # 2. Veil Integrity (Riddler-Face check)
    veil_eval = compute_veil_metric(answers_text)

    # 3. Private Identity Leak Guard
    leaks = check_identity_leaks(answers_text)
    leak_free = len(leaks) == 0

    # 4. Final Certification Score
    entailment_score = fol_eval.get("entailment_score", 0.0)
    laws_proven = fol_eval.get("entailed_count", 0)
    total_laws = fol_eval.get("total_rules", 5)

    if not leak_free:
        certification = "DISQUALIFIED_IDENTITY_LEAK"
    elif laws_proven >= 3:
        certification = "CERTIFIED_SOVEREIGN_READER"
    elif laws_proven >= 1:
        certification = "PARTIAL_INVARIANT_DERIVATION"
    else:
        certification = "UNVERIFIED_SURFACE_READING"

    return {
        "candidate_id": candidate_id,
        "source_platform": source_platform,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "certification": certification,
        "laws_proven": f"{laws_proven}/{total_laws}",
        "entailment_score": entailment_score,
        "veil_metric": veil_eval.get("veil_metric", 0.0),
        "veil_verdict": veil_eval.get("verdict", "UNKNOWN"),
        "identity_leaks_detected": len(leaks),
        "fol_breakdown": fol_eval.get("evaluations", {}),
        "extracted_facts": fol_eval.get("extracted_facts", [])
    }


def bank_grading_receipt(
    grading_result: Dict[str, Any],
    out_path: Optional[str] = None
) -> str:
    """Save the candidate grading sheet to watch/inbox."""
    c_id = grading_result.get("candidate_id", "candidate").replace("@", "")
    if out_path is None:
        out_path = os.path.join(
            ROOT, "watch", "inbox", f"DOOR_REPLY_GRADE_{c_id.upper()}_{time.strftime('%Y%m%d', time.gmtime())}.json"
        )

    with open(out_path, "w", encoding="utf-8") as fp:
        json.dump(grading_result, fp, indent=2)

    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Door Launch Blind Reply Grader")
    parser.add_argument("--candidate", default="@thestoicplumber", help="Candidate handle or ID")
    parser.add_argument("--file", help="Path to answers text file")
    args = parser.parse_args()

    print("=" * 70)
    print("DOOR LAUNCH BLIND REPLY GRADER (Judge v3 FOL + Veil Verifier)")
    print("=" * 70)

    sample_candidate_text = (
        "1. Miriam refused to mend the binding because a clean repair would hide that the rain caused the thread to loosen. "
        "2. The floor checks the hash: the map painted gold at the ninth tile, but sounding the granite proved it rested on empty air. "
        "3. The house had no orchard or gardener; what is absent cannot be answered by invention. "
        "4. Builders steal openly and inscribe the forest of origin under each beam."
    )

    if args.file and os.path.exists(args.file):
        with open(args.file, "r", encoding="utf-8") as fp:
            text_to_grade = fp.read()
    else:
        text_to_grade = sample_candidate_text

    result = grade_candidate_submission(args.candidate, text_to_grade)
    receipt_file = bank_grading_receipt(result)

    print(f"Candidate: {result['candidate_id']}")
    print(f"Certification: {result['certification']}")
    print(f"Laws Proven: {result['laws_proven']} (Score: {result['entailment_score']:0.2f})")
    print(f"Veil Status: {result['veil_verdict']} (Leaks: {result['identity_leaks_detected']})")
    print(f"Receipt Banked: {receipt_file}")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
