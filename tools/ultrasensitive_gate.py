#!/usr/bin/env python3
"""tools/ultrasensitive_gate.py - Ultrasensitive Non-Linear Step-Function Gate.

Implements the Wave 6 Steal (@O_Borkowski / David Baker & Isaac Hilton 2026):
- Replaces linear confidence heuristics with an ultrasensitive non-linear Hill switch.
- Biological basis: Transcription factor coactivator recruitment exhibits a sharp,
  ultrasensitive threshold (e.g. the 500 nM affinity cliff); activity below threshold
  is zero, while activity above threshold snaps to 100%.
- Eliminates agent dithering: AI agents often fail by executing hesitant, half-finished
  mutations when evaluated on linear probability scales. This gate converts continuous
  signals into crisp, binary execution decisions.
- Dual-rail certification: Requires formal First-Order Logic proof entailment
  (tools/judge_v3_fol.py) AND ultrasensitive step satisfaction before permitting state mutation.

Governing Hill Equation:
  f(S) = (S^n) / (S^n + Kd^n)
  where n is the Hill cooperativity coefficient (default n = 8.0) and Kd is the activation threshold.

CONSUMER: Water Governor, mutating tool gates, financial/token spend authorizations.
VERIFIER: tests/test_ultrasensitive_gate.py.
HOUSE LAW: Strictly zero unicode em-dashes; zero side effects on failure; pure functions.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


DEFAULT_THRESHOLD_KD = 0.80  # Default activation threshold Kd
DEFAULT_HILL_COEFF_N = 8.0   # High cooperativity for near-vertical step response


@dataclass(frozen=True)
class GateDecision:
    """Crisp, non-dithering binary decision payload."""
    permitted: bool
    force: float              # 0.0 (strictly suppressed) or 1.0 (fully armed)
    continuous_response: float # Raw Hill curve output f(S) in [0.0, 1.0]
    signal_value: float       # Input continuous signal S
    threshold_kd: float       # Threshold Kd
    hill_coeff_n: float       # Cooperativity n
    fol_entailed: bool        # Dual-rail formal logic verification
    verdict: str              # STEP_PERMITTED, SUB_THRESHOLD_SUPPRESSED, or FOL_REFUSED
    reasons: List[str] = field(default_factory=list)


def evaluate_hill_curve(
    signal: float,
    kd: float = DEFAULT_THRESHOLD_KD,
    n: float = DEFAULT_HILL_COEFF_N,
) -> float:
    """Compute the non-linear Hill equation response f(S) = S^n / (S^n + Kd^n)."""
    if signal <= 0.0:
        return 0.0
    if kd <= 0.0:
        return 1.0

    try:
        s_pow = math.pow(signal, n)
        kd_pow = math.pow(kd, n)
        denom = s_pow + kd_pow
        if denom == 0.0:
            return 0.0
        return s_pow / denom
    except OverflowError:
        # For very large exponents, if signal > kd, response is 1.0; else 0.0
        return 1.0 if signal > kd else 0.0


def evaluate_ultrasensitive_gate(
    signal_score: float,
    threshold_kd: float = DEFAULT_THRESHOLD_KD,
    hill_coeff_n: float = DEFAULT_HILL_COEFF_N,
    fol_entailed: bool = True,
    step_cutoff: float = 0.50,
) -> GateDecision:
    """Evaluate whether an action meets the sharp ultrasensitive step-function threshold.
    
    Parameters:
      signal_score: Continuous metric score in [0.0, 1.0] (e.g. test pass rate, semantic match).
      threshold_kd: The critical activation threshold Kd (default 0.80).
      hill_coeff_n: Cooperativity coefficient n (default 8.0).
      fol_entailed: Whether formal First-Order Logic entailment is verified.
      step_cutoff: The decision threshold on the Hill curve response (default 0.50).
    """
    reasons: List[str] = []

    # Rail 1: Formal Logic Gate
    if not fol_entailed:
        reasons.append("FOL proof check failed: Formal invariant not entailed in KB.")
        return GateDecision(
            permitted=False,
            force=0.0,
            continuous_response=0.0,
            signal_value=signal_score,
            threshold_kd=threshold_kd,
            hill_coeff_n=hill_coeff_n,
            fol_entailed=False,
            verdict="FOL_REFUSED",
            reasons=reasons,
        )

    # Rail 2: Non-Linear Ultrasensitive Hill Switch
    hill_val = evaluate_hill_curve(signal_score, kd=threshold_kd, n=hill_coeff_n)

    if hill_val < step_cutoff:
        reasons.append(
            f"Sub-threshold signal {signal_score:.4f} < Kd {threshold_kd:.4f} "
            f"(Hill response {hill_val:.4f} < {step_cutoff:.2f}). Suppressed to zero."
        )
        return GateDecision(
            permitted=False,
            force=0.0,
            continuous_response=round(hill_val, 6),
            signal_value=signal_score,
            threshold_kd=threshold_kd,
            hill_coeff_n=hill_coeff_n,
            fol_entailed=True,
            verdict="SUB_THRESHOLD_SUPPRESSED",
            reasons=reasons,
        )

    # Both rails passed: full force permitted
    reasons.append(
        f"Supra-threshold signal {signal_score:.4f} >= Kd {threshold_kd:.4f} "
        f"(Hill response {hill_val:.4f} >= {step_cutoff:.2f}). Fully armed."
    )
    return GateDecision(
        permitted=True,
        force=1.0,
        continuous_response=round(hill_val, 6),
        signal_value=signal_score,
        threshold_kd=threshold_kd,
        hill_coeff_n=hill_coeff_n,
        fol_entailed=True,
        verdict="STEP_PERMITTED",
        reasons=reasons,
    )


def main() -> int:
    """CLI tester for the Ultrasensitive Step-Function Gate."""
    parser = argparse.ArgumentParser(description="Ultrasensitive Non-Linear Step-Function Gate")
    parser.add_argument("--signal", type=float, required=True, help="Input signal score in [0.0, 1.0]")
    parser.add_argument("--kd", type=float, default=0.80, help="Activation threshold Kd (default: 0.80)")
    parser.add_argument("--n", type=float, default=8.0, help="Hill coefficient n (default: 8.0)")
    parser.add_argument("--fol-fail", action="store_true", help="Simulate FOL proof failure")
    args = parser.parse_args()

    decision = evaluate_ultrasensitive_gate(
        signal_score=args.signal,
        threshold_kd=args.kd,
        hill_coeff_n=args.n,
        fol_entailed=not args.fol_fail,
    )

    print(json.dumps(asdict(decision), indent=2))
    return 0 if decision.permitted else 1


if __name__ == "__main__":
    sys.exit(main())
