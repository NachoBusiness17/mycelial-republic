from __future__ import annotations


def test_q_context_requires_verified_root_anchored_proof():
    from mag.holographic_q import QKnot, decipher_q_context

    knot = QKnot(
        session_id="q-knot-test",
        q_session="q-test",
        q_sequence=0,
        intent_hash="intent",
        context_hash="context",
        steer_vector="steer",
        measurement_axes=["silence"],
        previous_q_knot="",
        ttl_knots=0,
        agent_assignments=[],
        verkle_root="root-1",
        ts="2026-09-01T00:00:00Z",
        status="active",
    )

    assert not decipher_q_context(knot, "root-1")["ok"]
    assert not decipher_q_context(knot, {"verified": True, "root": "other"})["ok"]
    out = decipher_q_context(knot, {"verified": True, "root": "root-1"})
    assert out["ok"] and out["proof_verified"]
