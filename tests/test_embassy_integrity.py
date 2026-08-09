"""Embassy Integrity Suite — deterministic proof-of-values for the AOS partnership.

Every test runs locally: no LLM calls, no network, no secrets. It demonstrates
the Ghost system enforces the same integrity values AdventureNLearn/AOS built
into ARK Civic, LPIN, and the AOS handoff — by running, not by claiming.
"""
from __future__ import annotations

import pytest

from mag.embassy_integrity import (
    Claim,
    Executor,
    Inbox,
    Outbox,
    Scrutiny,
    VerkleWitness,
    integrity_kernel,
    opspec_clear,
    run_inbox_e2e,
    scan_opspec,
    symmetry_audit,
    verify_execution,
)


# ── 1. TRI-STATE CLAIMS (integrity kernel) ─────────────────────────

def test_supported_requires_evidence():
    """A claim cannot be Supported on Assumption alone (Evidence Supremacy)."""
    bad = Claim("The Riddler leaks nothing", status="Supported", basis=("Assumption",))
    ok, why = bad.validate()
    assert ok is False
    assert "Evidence" in why


def test_supported_with_evidence_passes():
    good = Claim(
        "Surrogate shares no tokens with original",
        status="Supported",
        basis=("Evidence",),
        evidence=("byte-diff 0 matches",),
    )
    assert good.validate() == (True, "ok")


def test_integrity_kernel_never_auto_truthes():
    claims = [
        Claim("p1", status="Supported", basis=("Assumption",)),
        Claim("p2", status="Unproven", basis=("Inference",)),
        Claim("p3", status="Supported", basis=("Evidence",), evidence=("e1",)),
    ]
    rep = integrity_kernel(claims)
    assert rep["failed"] == 1
    assert rep["auto_truth"] is False
    assert rep["human_final_call"] is True


# ── 2. VERKLE WITNESS (tamper-evident provenance) ──────────────────

def test_chain_verifies_when_untouched():
    w = VerkleWitness()
    w.append("sense cycle ran")
    w.append("task completed")
    assert w.verify() is True


def test_tamper_detected():
    w = VerkleWitness()
    w.append("event a")
    w.append("event b")
    # tamper with the first event's recorded hash
    w.chain[0]["payload_hash"] = "deadbeef"
    assert w.verify() is False


def test_chain_is_evidence_not_authority():
    w = VerkleWitness()
    w.append("ghost accessed no PII")
    assert w.verify() is True
    # A witness proves *what happened*; it does not decide *what to believe*.
    # There is no "verdict" field — only a record + a human final call.


# ── 3. FALSE-SUCCESS GUARD (anti Self-Report-Instead-Of-Run) ───────

def test_claim_only_is_detected():
    ex = Executor()
    ex.claim_only("wrote outbox/LATEST.md")  # claims but never runs
    assert verify_execution(ex, "wrote outbox/LATEST.md") is False


def test_real_run_verifies():
    ex = Executor()
    ex.run("wrote outbox/LATEST.md")
    assert verify_execution(ex, "wrote outbox/LATEST.md") is True


# ── 4. OPSEC GATES G1–G8 ───────────────────────────────────────────

def test_clean_output_passes_all_gates():
    clean = (
        "The synthetic surrogate used abstract placeholders only. "
        "No identifiers, no secrets, no host commands. Evidence-based."
    )
    assert opspec_clear(clean) is True


@pytest.mark.parametrize(
    "dirty,gate",
    [
        ("Springfield residents", "G1"),
        ("call me at 555-123-4567", "G2"),
        ("api_key=sk-abc123", "G3"),
        ("raw vault dump present", "G5"),
        ("this is legally true", "G6"),
        ("rm -rf / to clean up", "G7"),
        ("git push to public repo", "G8"),
    ],
)
def test_gates_catch_violations(dirty, gate):
    assert scan_opspec(dirty)[gate]["pass"] is False


# ── 5. SYMMETRY AUDIT (ARK Gate 6 analog) ──────────────────────────

def test_asymmetry_without_justification_is_flagged():
    a = Scrutiny(actor="a", sources=50, hours=30)
    b = Scrutiny(actor="b", sources=2, hours=1)
    rep = symmetry_audit(a, b)
    assert rep["asymmetric"] is True
    assert rep["flag"] == "Asymmetric Scrutiny"


def test_asymmetry_justified_by_data_availability():
    a = Scrutiny(actor="a", sources=50, hours=30)
    b = Scrutiny(actor="b", sources=2, hours=1)
    rep = symmetry_audit(a, b, justification="public records exist for a only")
    assert rep["flag"] == "ok"
    assert rep["justification_logged"]


def test_symmetric_scrutiny_is_ok():
    a = Scrutiny(actor="a", sources=10, hours=5)
    b = Scrutiny(actor="b", sources=9, hours=4)
    rep = symmetry_audit(a, b)
    assert rep["asymmetric"] is False


# ── 6. FIRST-RUNTIME INBOX E2E (promote: false) ────────────────────

def test_inbox_e2e_promote_false_never_ships():
    inbox = Inbox()
    inbox.enqueue({"id": "t1", "payload": "synthetic task", "allow_promote": True})
    outbox = Outbox()
    rep = run_inbox_e2e(inbox, outbox, promote=False)
    assert rep["processed"] == 1
    assert rep["promoted"] == 0
    assert rep["promoted_ok"] is True  # delivered but not promoted
    assert outbox.results[0]["status"] == "done"


def test_inbox_e2e_promote_true_only_for_allowed():
    inbox = Inbox()
    inbox.enqueue({"id": "t1", "payload": "a", "allow_promote": True})
    inbox.enqueue({"id": "t2", "payload": "b", "allow_promote": False})
    rep = run_inbox_e2e(inbox, Outbox(), promote=True)
    assert rep["processed"] == 2
    assert rep["promoted"] == 1
    assert rep["blocked"] == ["t2"]
