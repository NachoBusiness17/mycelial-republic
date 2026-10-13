"""R3 trust landing tests: the four degenerate consensus shapes (2026-10-05).

Fold row 4 (watch/inbox/ractor_engine/2026-10-05-ouroboros-r3-trust/
SYNTHESIS.md) proved both consensus organs certified representations, not
things, and this file pins every refused shape:

1. unanimity of ONE sample returned CONFIRMED (consensus_gate ignored its
   own sample_count; the fold ran verdict(["the answer is 42"], 27B)).
2. a refusal triplet returned CONFIRMED at 27B (absence of evidence
   certified as consensus).
3. four byte-identical answers flagged independent=[True]*4 returned
   n_effective 4.0 (the CID law inverted: the flag was a witness ticket).
4. the strong path needed no construction evidence (distinct ask digests
   or cross-family stamps) - a bare boolean upgraded correlated echoes.

Every test names the shape it refuses and the legit path it must preserve.
"""
from __future__ import annotations

import pytest

from mag import memweave
from mag.consensus_gate import verdict, classify_batch

TRIPLET = ["the answer is 42"] * 3
REFUSAL_TRIPLET = ["I cannot answer that."] * 3
QUAD_IDENTICAL = ["x"] * 4


# shape 1: unanimity of one sample is one sample certifying itself


def test_single_answer_never_confirmed() -> None:
    """The fold's exact probe: verdict(['the answer is 42'], 27B) used to
    return CONFIRMED; the n >= 2 floor refuses it."""
    assert verdict(["the answer is 42"], model_params_b=27) == "UNVERIFIED"


def test_sample_count_claim_cannot_inflate_the_pool() -> None:
    """A claimed count is a representation; the pool is the thing. Claiming
    5 samples behind one answer stays UNVERIFIED, and a claim of 1 sample
    over two real answers lowers the effective n below the floor."""
    assert verdict(["the answer is 42"], model_params_b=27, sample_count=5) == "UNVERIFIED"
    assert verdict(["same answer", "same answer"], model_params_b=30,
                   sample_count=1) == "UNVERIFIED"


def test_two_real_unanimous_samples_still_confirm() -> None:
    """The floor must not break the legit path: two real agreeing samples
    above the small-model bar still CONFIRM; below it stays UNVERIFIED."""
    assert verdict(["same answer", "same answer"], model_params_b=30) == "CONFIRMED"
    assert verdict(["same answer", "same answer"], model_params_b=2) == "UNVERIFIED"


# shape 2: refusal-shaped unanimity is absence of evidence


def test_refusal_triplet_not_consensus() -> None:
    """The fold's 27B refusal triplet: three identical refusals must never
    certify as CONFIRMED (or DISPUTED - a refusal abstains, not disagrees)."""
    assert verdict(REFUSAL_TRIPLET, model_params_b=27) == "UNVERIFIED"
    assert verdict(["I'm sorry, but I cannot help with that."] * 3,
                   model_params_b=27) == "UNVERIFIED"
    assert verdict(["As an AI language model, I cannot answer."] * 3,
                   model_params_b=27) == "UNVERIFIED"


def test_refusals_strip_before_unanimity() -> None:
    """Two real agreeing answers plus a refusal still confirm at 30B; one
    real answer plus a refusal does not (the pool fell below the floor)."""
    assert verdict(["I cannot answer that.", "42", "42"], model_params_b=30) == "CONFIRMED"
    assert verdict(["I cannot answer that.", "42"], model_params_b=30) == "UNVERIFIED"


def test_answer_mentioning_uncertainty_is_not_stripped() -> None:
    """Leading-anchored refusal match only: a real answer that mentions
    'I don't know' mid-sentence is an answer, not a refusal."""
    assert verdict(["the answer is 42, and I don't know why it works"] * 2,
                   model_params_b=30) == "CONFIRMED"


def test_disputed_and_batch_shapes_untouched() -> None:
    assert verdict(["a", "b"], model_params_b=30) == "DISPUTED"
    batch = classify_batch([{"id": 1, "text": "I cannot answer."},
                            {"id": 2, "text": "I cannot answer."}],
                           model_params_b=27)
    assert batch["verdict"] == "UNVERIFIED"
    assert batch["n_refusal_shaped"] == 2


# shapes 3 + 4: the independent flag is not a witness ticket


def test_byte_identical_flagged_answers_are_one_witness() -> None:
    """The fold's exact probe: four identical answers flagged independent
    returned n_effective 4.0; the CID law counts them as ONE opinion."""
    q = memweave.consensus_quality(QUAD_IDENTICAL, independent=[True] * 4)
    assert q["n_independent"] == 1
    assert q["n_effective"] == 1.0
    assert q["correlated"] is True
    assert q["verdict"] == "correlated_weak"


def test_duplicate_construction_tokens_do_not_split() -> None:
    """Construction evidence means DISTINCT tokens: the same token on every
    answer is one construction, one witness, regardless of flags."""
    q = memweave.consensus_quality(QUAD_IDENTICAL, independent=[True] * 4,
                                   construction=["ask-digest-1"] * 4)
    assert q["n_independent"] == 1
    assert q["verdict"] == "correlated_weak"


def test_distinct_construction_tokens_earn_the_strong_path() -> None:
    """Four byte-identical answers from four distinct constructions (distinct
    ask digests) are four real witnesses: the strong case the guard exists
    to report, now on evidence instead of a boolean."""
    q = memweave.consensus_quality(QUAD_IDENTICAL, independent=[True] * 4,
                                   construction=["d1", "d2", "d3", "d4"])
    assert q["n_independent"] == 4
    assert q["n_effective"] == 4.0
    assert q["correlated"] is False
    assert q["verdict"] == "strong"


def test_construction_needs_tokens_on_both_sides() -> None:
    """A correlated pair splits only when BOTH answers carry tokens: one
    token against a tokenless witness is a ticket, not evidence."""
    q = memweave.consensus_quality(["x", "x"], independent=[True, True],
                                   construction=["", "tok-a"])
    assert q["n_independent"] == 1
    assert q["verdict"] == "correlated_weak"


def test_construction_length_guard() -> None:
    with pytest.raises(ValueError):
        memweave.consensus_quality(QUAD_IDENTICAL, construction=["d1", "d2"])


# preserved legit paths (the B3 merge-actor contract must not regress)


def test_unanimous_pool_cid_penalty_preserved() -> None:
    q = memweave.consensus_quality(TRIPLET)
    assert q["n_independent"] == 1
    assert q["n_effective"] == 1.0
    assert q["verdict"] == "correlated_weak"


def test_dissenting_pool_still_strong() -> None:
    q = memweave.consensus_quality(["a b c", "d e f", "g h i", "j k l"])
    assert q["n_independent"] == 4
    assert q["verdict"] == "strong"


def test_merge_passes_construction_through(tmp_path) -> None:
    res = memweave.consensus_merge(QUAD_IDENTICAL, "research",
                                   construction=["d1", "d2", "d3", "d4"],
                                   trail=tmp_path / "trail.jsonl")
    assert res["verdict"]["verdict"] == "strong"
    assert res["row"]["detail"]["n_independent"] == 4


def test_claims_verify_strong_case_survives_on_construction_evidence() -> None:
    """claims_verify pools two byte-identical roots from two different code
    paths: under the R3 law its strong verdict must ride on the two code
    paths' digests, not the bare flag."""
    from mag import claims_verify
    cq = claims_verify.run()["existing_consensus_guard"]
    assert cq["n_independent"] == 2
    assert cq["verdict"] == "strong"
