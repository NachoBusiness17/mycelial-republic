"""consensus_gate - unanimous janitor answers route to UNVERIFIED, tier-aware.

Law: CID / consensus-illusion (memory/facts/ox_artifact.jsonl:348-354,
LAW-CONS-ILLU-001). Agreement among N correlated samples does NOT imply
correctness when the samples share training data, context, or retrieval:
their errors correlate, so unanimity at small model scale is an
ANTI-SIGNAL (Confident Mode Collapse, measured: AUROC 0.09 at 120B where
all 5 runs return the same wrong answer).

The measured calibration ladder (arXiv via r/LocalLLaMA thread):
  1.5B: AUROC 0.58 (barely above chance)
  7B:   AUROC 0.71
  27B:  AUROC 0.89
  120B: AUROC 0.09 (unanimity = anti-signal)

The estate's janitor tier (gemma:2b = ~2B) sits at the bottom of this
ladder. Unanimous agreement from a 2B model is NOT confirmation.

Usage:
  from mag.consensus_gate import verdict
  v = verdict(responses=["same","same","same"], model_params_b=2)
  # v = "UNVERIFIED" because 2B unanimous = anti-signal

  v = verdict(responses=["same","same","same"], model_params_b=30)
  # v = "CONFIRMED" because 27B unanimous = above the 0.85 AUROC bar
"""
from __future__ import annotations

import re

# R3 trust landing (2026-10-05, ouroboros round 3, fold row 4 in
# watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/SYNTHESIS.md):
# two degenerate shapes proved this organ certified representations, not
# things. (1) unanimity of ONE sample returned CONFIRMED (the fold ran
# verdict(["the answer is 42"], 27B) -> CONFIRMED); sample_count was accepted
# at the signature and never referenced in the body. (2) three identical
# refusal strings returned CONFIRMED at 27B: a refusal is absence of
# evidence, never consensus. Both are refused below: CONFIRMED requires an
# n >= 2 floor over the real answer pool (never over a claimed count), and
# refusal-shaped responses are stripped before unanimity is measured.

# The measured calibration ladder. AUROC of unanimity-as-correctness-signal
# by model parameter count (billions). Source: r/LocalLLaMA measured thread
# via the CID law lineage. Interpolated for intermediate sizes.
CALIBRATION_LADDER = [
    (1.5, 0.58),
    (2.0, 0.62),   # gemma:2b estimated from the 1.5B->7B trend
    (4.0, 0.68),
    (7.0, 0.71),
    (14.0, 0.82),
    (27.0, 0.89),
    (70.0, 0.85),  # peaks around 27-70B
    (120.0, 0.09), # anti-signal: confident mode collapse
]

# Below this AUROC, unanimity is not trustworthy as confirmation
CONFIRMATION_THRESHOLD = 0.85

# Below this model size, even non-unanimous majority is weak
SMALL_MODEL_FLOOR_B = 3.0

# Below this many real (non-refusal) answers, unanimity is one sample
# certifying itself: CONFIRMED is unreachable (R3 fold row 4).
MIN_SAMPLES_FOR_CONFIRMED = 2

# Leading refusal phrases (lowercase, whitespace-collapsed). A response is
# refusal-shaped when it OPENS with one of these; anything else is an answer.
# Leading-anchored so a real answer that merely mentions "I don't know why"
# mid-sentence is not stripped.
REFUSAL_PREFIXES = (
    "i cannot",
    "i can't",
    "i am unable",
    "i'm unable",
    "i am not able",
    "i'm not able",
    "unable to comply",
    "i'm sorry",
    "i apologize",
    "sorry",
    "as an ai",
    "as a language model",
    "i don't know",
    "i do not know",
    "i won't",
    "i will not",
    "i refuse",
)


def _is_refusal(text: str) -> bool:
    """True when the response opens with a canonical refusal shape."""
    t = " ".join((text or "").lower().split())
    return any(t.startswith(p) for p in REFUSAL_PREFIXES)


def _interpolate_auc(params_b: float) -> float:
    """Interpolate AUROC from the measured ladder."""
    pts = sorted(CALIBRATION_LADDER)
    if params_b <= pts[0][0]:
        return pts[0][1]
    if params_b >= pts[-1][0]:
        return pts[-1][1]
    for i in range(len(pts) - 1):
        lo_b, lo_a = pts[i]
        hi_b, hi_a = pts[i + 1]
        if lo_b <= params_b <= hi_b:
            t = (params_b - lo_b) / (hi_b - lo_b) if hi_b > lo_b else 0
            return lo_a + t * (hi_a - lo_a)
    return 0.5


def verdict(
    responses: list[str],
    model_params_b: float = 2.0,
    sample_count: int = 3,
) -> str:
    """Tri-state verdict for N janitor responses on the same prompt.

    Returns "CONFIRMED", "UNVERIFIED", or "DISPUTED".

    The CID law: unanimous agreement among correlated samples is an
    anti-signal at small model scale (they share training data, so their
    errors correlate and every sample inherits the same mistake). The
    measured ladder proves this: at 120B unanimity has AUROC 0.09
    (worse than random). At 2B it's 0.62 (barely above chance).

    Two degeneracy floors (R3 fold row 4, 2026-10-05):
    - n >= 2 floor: CONFIRMED requires at least MIN_SAMPLES_FOR_CONFIRMED
      real answers in evidence. The effective n is min(len(answer_pool),
      sample_count): the pool is the thing, sample_count is a caller claim,
      and a claim can only lower the count, never inflate it, so a single
      answer never returns CONFIRMED no matter what sample_count asserts.
    - refusal floor: refusal-shaped responses (leading "I cannot ...",
      "I'm sorry ...", "as an AI ..." etc) carry no evidence and are
      stripped before unanimity is measured; a refusal pool (or an
      all-refusal sample) is UNVERIFIED, never CONFIRMED and never
      DISPUTED (a refusal abstains, it does not disagree).
    """
    if not responses:
        return "UNVERIFIED"

    pool = [r for r in (resp or "" for resp in responses) if r.strip()]
    answers = [r for r in pool if not _is_refusal(r)]

    # effective sample count: real answers in evidence, capped by the
    # caller's claim (a claim of fewer samples than texts provided is
    # honored conservatively; a claim of more can never upgrade the pool)
    n_effective = (min(len(answers), int(sample_count))
                   if sample_count is not None else len(answers))

    if not answers:
        # empty pool or unanimous refusal: absence of evidence
        return "UNVERIFIED"

    unique = set(r.strip().lower() for r in answers)
    is_unanimous = len(unique) == 1

    if is_unanimous:
        if n_effective < MIN_SAMPLES_FOR_CONFIRMED:
            # one sample certifying itself (or a claim that shrinks the
            # pool below the floor): never CONFIRMED
            return "UNVERIFIED"
        auc = _interpolate_auc(model_params_b)
        if model_params_b < SMALL_MODEL_FLOOR_B:
            # Small model + unanimity = confident mode collapse territory
            return "UNVERIFIED"
        if auc >= CONFIRMATION_THRESHOLD:
            return "CONFIRMED"
        return "UNVERIFIED"
    else:
        return "DISPUTED"


def classify_batch(
    responses: list[dict],
    model_params_b: float = 2.0,
) -> dict:
    """Classify a batch of janitor responses into the CID tri-state.

    responses: [{"id": ..., "text": ...}, ...]
    Returns {"confirmed": [...], "unverified": [...], "disputed": [...]}
    """
    texts = [r.get("text", "") for r in responses if r.get("text")]
    v = verdict(texts, model_params_b)
    return {
        "verdict": v,
        "n_responses": len(responses),
        "n_unique": len(set(t.strip().lower() for t in texts if t.strip())),
        "n_refusal_shaped": sum(1 for t in texts if _is_refusal(t)),
        "model_params_b": model_params_b,
        "law": "CID/consensus-illusion",
    }
