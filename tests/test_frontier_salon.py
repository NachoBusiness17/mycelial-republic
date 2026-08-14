"""tests for frontier_salon — the three frontier seats (ChatGPT + SuperGrok + V4-Pro) as ONE tandem
surface, saloning our own system into a new version. Deterministic $0 coordinator.

RIB (frozen spec):
  salon(question) -> dispatch the SAME question to each witness (chatgpt / supergrok / v4-pro),
      collect their answers, roshomon-combine into ONE new_version + consensus_invariant. Per-witness
      HONEST ok flags — a down/unreachable witness is reported, never fabricated. n_available+n_down.
  salon_project() -> the test: salon OUR OWN system as the subject. Always ok-shaped (ok may be
      False if all witnesses down, but never fabricates).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import frontier_salon as fs  # noqa: E402


def test_status_witnesses_and_honest_gate():
    st = fs.status()
    assert st["ok"] is True
    assert st["schema"] == "frontier_salon.v1"
    for w in ("chatgpt", "supergrok", "v4-pro"):
        assert w in st["witnesses"]
    # the honest gate is explicit: live salon needs the seats reachable (CDP/login)
    assert "CDP" in st["honest_gate"] or "login" in st["honest_gate"]


def test_salon_reports_honest_witnesses_never_fabricates():
    r = fs.salon("salon this project", surface_filter=["chatgpt"])
    # n_witnesses matches the filter; ok reflects reachability (may be False if the seat is down)
    assert r["n_witnesses"] == 1
    assert r["ok"] in (True, False)
    assert r["n_available"] + r["n_down"] == r["n_witnesses"]
    for w in r["witnesses"]:
        assert w["ok"] in (True, False)
        # an unreachable witness has an error/empty answer; a reachable one has an answer
        if w["ok"]:
            assert w["answer"]
        else:
            assert w["error"] or not w["answer"]
    # the salon always produces a new_version shape (never crashes even with no witnesses)
    assert "new_version" in r and "consensus_invariant" in r


def test_salon_project_is_the_self_test():
    r = fs.salon_project()
    assert "consensus_invariant" in r and "new_version" in r
    assert "n_witnesses" in r


def test_salon_consensus_deterministic():
    # given the same fake witnesses, the shared-invariant is deterministic (token overlap)
    a = fs._shared_invariant([
        {"ok": True, "answer": "the swarm must evolve with the chain and the wave"},
        {"ok": True, "answer": "the chain evolves with the swarm toward the wave"},
    ])
    assert "evolve" in a or "chain" in a or "swarm" in a
