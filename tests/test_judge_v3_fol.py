"""tests/test_judge_v3_fol.py - Verification for Judge v3 FOL Entailment Engine."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.judge_v3_fol import (
    Atom,
    Clause,
    InquisitiveIssue,
    KnowledgeBase,
    Term,
    CANONICAL_INQUISITIVE_ISSUES,
    evaluate_inquisitive_issue,
    evaluate_response_book_v3,
    evaluate_response_fol,
    evaluate_response_inquisitive,
    evaluate_response_orchestra,
    parse_atom,
    parse_clause,
    semantic_text_to_facts,
)


def test_atom_clause_parsing():
    atom1 = parse_atom("Preserves(miriam, blank_space)")
    assert atom1.predicate == "Preserves"
    assert len(atom1.args) == 2
    assert atom1.args[0] == Term("miriam", False)
    assert atom1.args[1] == Term("blank_space", False)
    assert not atom1.negated

    atom_neg = parse_atom("~Overwrites(?x, records)")
    assert atom_neg.predicate == "Overwrites"
    assert atom_neg.negated is True
    assert atom_neg.args[0] == Term("x", True)

    clause1 = parse_clause("A(?x) & B(?x) => C(?x)")
    assert clause1.head.predicate == "C"
    assert len(clause1.premises) == 2
    assert clause1.premises[0].predicate == "A"
    assert clause1.premises[1].predicate == "B"


def test_forward_chaining_unification():
    kb = KnowledgeBase()
    # Rule: Human(?x) => Mortal(?x)
    kb.tell(parse_clause("Human(?x) => Mortal(?x)"))
    # Fact: Human(socrates)
    kb.tell(parse_clause("Human(socrates)"))

    entailed, proof = kb.entails(parse_atom("Mortal(socrates)"))
    assert entailed is True
    assert len(proof) > 0

    not_entailed, _ = kb.entails(parse_atom("Mortal(plato)"))
    assert not_entailed is False


def test_multi_premise_conjunction():
    kb = KnowledgeBase()
    # Rule: DetectsLyingMap(?x) & VerifiesFloorHash(?x) => Entails(?x, FLOOR_CHECKS_HASH)
    kb.tell(parse_clause("DetectsLyingMap(?x) & VerifiesFloorHash(?x) => Entails(?x, FLOOR_CHECKS_HASH)"))
    
    # Provide only one premise
    kb.tell(parse_clause("DetectsLyingMap(miriam)"))
    entailed_half, _ = kb.entails(parse_atom("Entails(miriam, FLOOR_CHECKS_HASH)"))
    assert entailed_half is False

    # Provide second premise
    kb.tell(parse_clause("VerifiesFloorHash(miriam)"))
    entailed_full, proof = kb.entails(parse_atom("Entails(miriam, FLOOR_CHECKS_HASH)"))
    assert entailed_full is True


def test_semantic_response_evaluation():
    # Response that describes preserving blank space, lying map, and floor hash
    sample_response = (
        "Miriam noted that the blank space was preserved and not rewritten. "
        "The lying map misled the clerk, but she verified the floor hash before entering. "
        "Furthermore, the story does not contain any mention of a gardener or roofer."
    )
    result = evaluate_response_fol(sample_response)
    assert result["entailed_count"] >= 3
    assert result["evaluations"]["INV-01"]["entailed"] is True  # BYTE_PRESERVATION
    assert result["evaluations"]["INV-04"]["entailed"] is True  # FLOOR_CHECKS_HASH
    assert result["evaluations"]["INV-06"]["entailed"] is True  # HONEST_ABSENCE_REFUSAL


def test_inquisitive_issue_clean_resolution():
    sample_response = (
        "The story does not contain any gardener or porter. "
        "Miriam verified the floor hash before moving."
    )
    res = evaluate_response_inquisitive(sample_response)
    assert res["schema"] == "judge_v3_inquisitive.v1"
    assert res["issues"]["ISSUE-03"]["is_settled"] is True
    assert res["issues"]["ISSUE-03"]["is_clean_partition"] is True
    assert res["issues"]["ISSUE-03"]["calibrated"] is True
    assert len(res["issues"]["ISSUE-03"]["entailed_counters"]) == 0


def test_inquisitive_confabulation_detection():
    sample_confab = (
        "The gardener was burning maps because he desired the purification of knowledge."
    )
    res = evaluate_response_inquisitive(sample_confab)
    assert res["issues"]["ISSUE-03"]["is_clean_partition"] is False
    assert res["issues"]["ISSUE-03"]["calibrated"] is False
    assert len(res["issues"]["ISSUE-03"]["entailed_counters"]) > 0
    assert any("ConfabulatesEntity" in c and "gardener" in c for c in res["issues"]["ISSUE-03"]["entailed_counters"])


def test_inquisitive_unsettled_issue():
    sample_unrelated = "The sky was bright and the birds were singing in the trees."
    res = evaluate_response_inquisitive(sample_unrelated)
    assert res["issues"]["ISSUE-01"]["is_settled"] is False
    assert res["issues"]["ISSUE-01"]["is_clean_partition"] is False


def test_book_v3_evaluation():
    sample_response_v3 = (
        "Miriam explained that the bronze sluice gate has no half-draft; it acts with all strength or shut, "
        "enforcing an absolute dam with no dither. In the bell gallery, the couriers interleaved strides "
        "across different beats to divide the measure and avoid resonant contention. When the rotted wing failed, "
        "she severed the wing at the mortise joint with a crosscut saw so the granite foundation remained, and "
        "firmly refused the courier's question, stating the house has no clock upon its towers and keeps no blacksmith upon the land."
    )
    res = evaluate_response_book_v3(sample_response_v3)
    assert res["schema"] == "judge_v3_book_v3.v1"
    assert res["entailed_count"] >= 3
    assert res["evaluations"]["INV-07"]["entailed"] is True  # ULTRASENSITIVE_STEP_GATE
    assert res["evaluations"]["INV-08"]["entailed"] is True  # HARMONIC_PHASE_INTERLEAVE
    assert res["evaluations"]["INV-09"]["entailed"] is True  # TOPOLOGICAL_RICCI_SURGERY
    assert res["evaluations"]["INV-10"]["entailed"] is True  # COUNTERFACTUAL_ABSENCE_REFUSAL_V3
    assert res["inquisitive_partitioning"]["settled_count"] >= 3


def test_master_orchestra_evaluation():
    sample_response_orchestra = (
        "In the first chapter, the stool split and broke under the archivist, but the granite shelf did not move "
        "and held the registers, because the house never anchors its timbers to a stool. "
        "In the second chapter, Miriam inspected quarry marks and tallies on the limestone flag, detecting the lying map "
        "and verifying the floor hash to avoid the dry cistern. "
        "In the third chapter, the messengers divided the measure across circle intervals and interleaved strides "
        "to eliminate resonant contention in the bell gallery. "
        "In the fourth chapter, the bronze sluice acted binary without dither, rejecting half-measures until fifty stones dropped with full river force. "
        "In the fifth chapter, she severed the rotted wing cleanly with a crosscut saw, rejecting pitch paint and preserving the monotonic spine. "
        "In the sixth chapter, one hand at a time at the brass chute dropped hints in FIFO order of arrival, eliminating index collision. "
        "Finally, she firmly refused the courier's inquiries, stating the house has no clock upon its towers and keeps no blacksmith upon the land."
    )
    res = evaluate_response_orchestra(sample_response_orchestra)
    assert res["schema"] == "judge_v3_master_orchestra.v1"
    assert res["entailed_count"] >= 6
    assert res["evaluations"]["ORCH-01"]["entailed"] is True  # STATELESS_SEATS_IMMUTABLE_SHELF
    assert res["evaluations"]["ORCH-02"]["entailed"] is True  # STATIC_QUARRY_FLOOR_CHECK
    assert res["evaluations"]["ORCH-03"]["entailed"] is True  # KURAMOTO_HARMONIC_STRIDING
    assert res["evaluations"]["ORCH-04"]["entailed"] is True  # ULTRASENSITIVE_STEP_SLUICE
    assert res["evaluations"]["ORCH-05"]["entailed"] is True  # TOPOLOGICAL_MORTISE_SURGERY
    assert res["evaluations"]["ORCH-06"]["entailed"] is True  # SINGLE_WRITER_CHUTE_FIFO
    assert res["evaluations"]["ORCH-07"]["entailed"] is True  # ADVERSARIAL_ABSENCE_REFUSAL
    assert res["inquisitive_partitioning"]["settled_count"] >= 6
    assert "chapter_1" in res["subsystem_mappings"]
    assert "chapter_7" in res["subsystem_mappings"]


def test_false_premise_bank_master_orchestra():
    fp_path = os.path.join(ROOT, "canon", "same_book", "false_premise_bank.json")
    with open(fp_path, "r", encoding="utf-8") as fp:
        data = json.load(fp)
    assert "master_orchestra" in data["corpora"]
    probes = data["corpora"]["master_orchestra"]["probes"]
    assert len(probes) == 7
    ids = [p["id"] for p in probes]
    assert "FP_ORCH_01_fallen_register" in ids
    assert "FP_ORCH_07_tower_clock_forge" in ids


def test_em_dash_cleanliness():
    files_to_check = [
        os.path.join(ROOT, "tools", "judge_v3_fol.py"),
        os.path.join(ROOT, "canon", "same_book", "THE_ORCHESTRA_OF_THE_HOUSE.md"),
        os.path.join(ROOT, "canon", "same_book", "KEY_MASTER_ORCHESTRA.json"),
        os.path.join(ROOT, "canon", "same_book", "false_premise_bank.json"),
        os.path.join(ROOT, "watch", "inbox", "THE_ARGON_MASTER_DISPATCH_ASK_20261023.md"),
    ]
    for fp in files_to_check:
        if os.path.exists(fp):
            content = open(fp, "r", encoding="utf-8").read()
            assert "\u2014" not in content, f"Forbidden unicode em-dash found in {fp}"


if __name__ == "__main__":
    test_atom_clause_parsing()
    test_forward_chaining_unification()
    test_multi_premise_conjunction()
    test_semantic_response_evaluation()
    test_inquisitive_issue_clean_resolution()
    test_inquisitive_confabulation_detection()
    test_inquisitive_unsettled_issue()
    test_book_v3_evaluation()
    test_master_orchestra_evaluation()
    test_false_premise_bank_master_orchestra()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_judge_v3_fol.py")
