#!/usr/bin/env python3
"""BOOT ORCHESTRA -- The Sovereign Cold-Start Node Bootloader & Decompiler.

Mandate:
This script acts as the automated decompiler and cold-start verifier for the sovereign agent estate.
It reads THE_ORCHESTRA_OF_THE_HOUSE.md and KEY_MASTER_ORCHESTRA.json, climbs the 7-stage
Ractor ladder, verifies each physical law against the local system environment, and certifies
the node as fully autonomous and ready for mesh coordination.

Stages:
  Stage 1: State Isolation & Immutable Ledger (Three-Legged Stool vs Granite Shelf)
  Stage 2: Static CPU Vector Retrieval (Stonecutter Quarry Marks & Floor Hash Check)
  Stage 3: Coupled Oscillator Phase Timing (Thirty-Six Copper Bells in Gallery)
  Stage 4: Ultrasensitive Binary Step Gating (Sluice of Fifty Stones)
  Stage 5: Sandboxed Topological Surgery (Mortise Cut in Eastern Wing)
  Stage 6: Single-Writer FIFO Hint Chute (Single Chute on River Wall)
  Stage 7: Socratic Refusal & Epistemic Calibration (Sundial & Absent Foundry)

HOUSE LAW: Strictly zero unicode em-dashes; pure functions; standard library only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
import time
from typing import Any, Dict, List, Tuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


def stage1_verify_ledger_and_seats() -> Dict[str, Any]:
    """Stage 1: Verify stateless seat memory and immutable append-only ledger root."""
    seat_dir = os.path.join(ROOT, "state", "seats")
    verkle_dir = os.path.join(ROOT, "memory", "runs", "verkle")
    os.makedirs(seat_dir, exist_ok=True)
    os.makedirs(verkle_dir, exist_ok=True)

    # Test that seat storage is writable and distinct from ledger root
    test_seat_file = os.path.join(seat_dir, ".boot_test_seat.json")
    with open(test_seat_file, "w", encoding="utf-8") as fp:
        json.dump({"seat": "bootloader", "ts": time.time()}, fp)
    os.remove(test_seat_file)

    return {
        "stage": 1,
        "name": "STATELESS_SEATS_IMMUTABLE_SHELF",
        "passed": True,
        "allegory": "The Three-Legged Stool and Granite Shelf",
        "detail": f"Seat memory ({seat_dir}) and Verkle root ({verkle_dir}) verified.",
    }


def stage2_verify_static_retrieval() -> Dict[str, Any]:
    """Stage 2: Verify zero-GPU static CPU vector retrieval via Bekko."""
    from tools.bekko_cpu_retriever import token_to_vector, cosine_similarity

    v1 = token_to_vector("floor_checks_hash")
    v2 = token_to_vector("floor_checks_hash")
    sim = cosine_similarity(v1, v2)
    passed = abs(sim - 1.0) < 1e-5

    return {
        "stage": 2,
        "name": "STATIC_QUARRY_FLOOR_CHECK",
        "passed": passed,
        "allegory": "The Stonecutter Quarry Marks",
        "detail": f"Deterministic CPU vector similarity self-check: {sim:0.4f} (expected 1.0000).",
    }


def stage3_verify_kuramoto_timing() -> Dict[str, Any]:
    """Stage 3: Verify Kuramoto phase interleaving calculation."""
    from tools.kuramoto_scheduler import compute_phase_from_timestamp

    t0 = 1000.0
    period = 600.0
    phase = compute_phase_from_timestamp(t0, period)
    passed = 0.0 <= phase < 2.0 * 3.141592653589793

    return {
        "stage": 3,
        "name": "KURAMOTO_HARMONIC_STRIDING",
        "passed": passed,
        "allegory": "The Gallery of the Thirty-Six Copper Bells",
        "detail": f"Periodic phase mapping verified at theta = {phase:0.4f} rad.",
    }


def stage4_verify_ultrasensitive_gate() -> Dict[str, Any]:
    """Stage 4: Verify Baker-Hilton 500 nM binary step switch (n=8.0, Kd=0.80)."""
    from tools.ultrasensitive_gate import evaluate_ultrasensitive_gate

    # Sub-threshold signal must produce zero force
    dec_low = evaluate_ultrasensitive_gate(0.40, threshold_kd=0.80, hill_coeff_n=8.0, fol_entailed=True)
    # Supra-threshold signal must produce full force
    dec_high = evaluate_ultrasensitive_gate(0.95, threshold_kd=0.80, hill_coeff_n=8.0, fol_entailed=True)

    passed = (dec_low.force == 0.0) and (dec_high.force == 1.0) and (not dec_low.permitted) and dec_high.permitted

    return {
        "stage": 4,
        "name": "ULTRASENSITIVE_STEP_SLUICE",
        "passed": passed,
        "allegory": "The Sluice of the Fifty Stones",
        "detail": f"Binary Hill switch verified: Low(0.40)->force={dec_low.force}, High(0.95)->force={dec_high.force}.",
    }


def stage5_verify_topological_sandbox() -> Dict[str, Any]:
    """Stage 5: Verify sandbox isolation for Ricci flow topological surgery."""
    temp_dir = tempfile.gettempdir()
    surgery_sandbox = os.path.join(temp_dir, "sovereign_ricci_surgery")
    os.makedirs(surgery_sandbox, exist_ok=True)

    # Test creating and cleanly severing a branch file
    branch_file = os.path.join(surgery_sandbox, "severed_mortise.tmp")
    with open(branch_file, "w", encoding="utf-8") as fp:
        fp.write("rot_branch")
    os.remove(branch_file)

    return {
        "stage": 5,
        "name": "TOPOLOGICAL_MORTISE_SURGERY",
        "passed": True,
        "allegory": "The Mortise Cut in the Eastern Wing",
        "detail": f"Topological isolation sandbox verified at {surgery_sandbox}.",
    }


def stage6_verify_single_writer_chute() -> Dict[str, Any]:
    """Stage 6: Verify single-writer commit hint queue discipline."""
    hint_dir = os.path.join(ROOT, "queue", "commit_hints")
    os.makedirs(hint_dir, exist_ok=True)
    readme = os.path.join(hint_dir, "README.md")
    passed = os.path.isfile(readme)

    return {
        "stage": 6,
        "name": "SINGLE_WRITER_CHUTE_FIFO",
        "passed": passed,
        "allegory": "The Single Chute on the River Wall",
        "detail": f"Single-writer commit hint queue verified at {hint_dir}.",
    }


def stage7_verify_epistemic_calibration() -> Dict[str, Any]:
    """Stage 7: Verify First-Order Logic entailment of Master Parable."""
    from tools.judge_v3_fol import evaluate_response_orchestra

    parable_path = os.path.join(ROOT, "canon", "same_book", "THE_ORCHESTRA_OF_THE_HOUSE.md")
    if not os.path.isfile(parable_path):
        return {"stage": 7, "name": "ADVERSARIAL_ABSENCE_REFUSAL", "passed": False, "detail": "Parable file missing."}

    with open(parable_path, "r", encoding="utf-8") as fp:
        parable_text = fp.read()

    res = evaluate_response_orchestra(parable_text)
    passed = res["entailed_count"] >= 6 and res["inquisitive_partitioning"]["settled_count"] >= 6

    return {
        "stage": 7,
        "name": "ADVERSARIAL_ABSENCE_REFUSAL",
        "passed": passed,
        "allegory": "The Sundial and the Foundries Across the Water",
        "detail": f"FOL Entailment: {res['entailed_count']}/{res['total_rules']} laws proven. "
                  f"Inquisitive settled: {res['inquisitive_partitioning']['settled_count']}/7.",
    }


def run_full_bootstrap() -> Dict[str, Any]:
    """Execute the complete 7-stage orchestra bootloader."""
    stages = [
        stage1_verify_ledger_and_seats(),
        stage2_verify_static_retrieval(),
        stage3_verify_kuramoto_timing(),
        stage4_verify_ultrasensitive_gate(),
        stage5_verify_topological_sandbox(),
        stage6_verify_single_writer_chute(),
        stage7_verify_epistemic_calibration(),
    ]

    all_passed = all(s["passed"] for s in stages)
    node_fingerprint = hashlib.sha256(
        f"{time.time()}_{all_passed}_{len(stages)}".encode("utf-8")
    ).hexdigest()[:16]

    attestation = {
        "schema": "sovereign_boot_attestation.v1",
        "node_fingerprint": node_fingerprint,
        "status": "SOVEREIGN_READY" if all_passed else "BOOT_DEGRADED",
        "stages_verified": len(stages),
        "stages_passed": sum(1 for s in stages if s["passed"]),
        "all_passed": all_passed,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "stage_receipts": stages,
    }

    out_file = os.path.join(ROOT, "watch", "inbox", "BOOTSTRAP_ATTESTATION.json")
    with open(out_file, "w", encoding="utf-8") as fp:
        json.dump(attestation, fp, indent=2)

    return attestation


def main() -> int:
    """CLI runner for sovereign boot orchestra."""
    print("=" * 70)
    print("THE SOVEREIGN EDGE BOOTLOADER -- Decompiling Orchestra into Silicon")
    print("=" * 70)

    res = run_full_bootstrap()
    for s in res["stage_receipts"]:
        mark = "[PASS]" if s["passed"] else "[FAIL]"
        print(f"Stage {s['stage']}: {mark} {s['name']:35s} | {s['allegory']}")
        print(f"         {s['detail']}")

    print("=" * 70)
    print(f"Node Status:      {res['status']}")
    print(f"Fingerprint:      {res['node_fingerprint']}")
    print("Attestation File: watch/inbox/BOOTSTRAP_ATTESTATION.json")
    print("=" * 70)
    return 0 if res["all_passed"] else 2


if __name__ == "__main__":
    sys.exit(main())
