"""tests for deep_research_moonshot — the DEEP-RESEARCH MOONSHOT (self-stolen internal synthesis).
Deterministic + stateless + $0 core.

RIB (frozen spec):
  synthesize(question) -> internal-corpus synthesis: PRIOR (research_lens) + WITNESS (roshomon) +
      SHADOW (shadow_work) + KNOT (lens_chain) folded into THE MARRIAGE (stochastic+deterministic+
      corpus -> one chain link). Always ok:True with a non-empty invariant + shadow edge. Per-stage
      honest ok flags (model tier down / swarm undrained are honest, not fatal).
  moonshot(question)  -> synthesize + ROUTE the novel seam to the swarm via swarm_surface.route_novel
      (the one primitive). Returns {ok, synthesis, routed} — routed is deduped-or-enqueued, never fatal.
  cadence(limit)      -> bounded sweep of the standing-wave RIBs -> moonshot each.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import deep_research_moonshot as drm  # noqa: E402


def test_synthesize_ok_and_marriage_shape():
    s = drm.synthesize("what is the one seam the standing wave has not yet shaded toward the frontier")
    assert s["ok"] is True
    m = s["marriage"]
    # the marriage has all three halves: stochastic + deterministic + corpus
    assert "stochastic" in m and "deterministic" in m and "corpus" in m
    # the invariant + shadow edge are always non-empty (the moonshot never returns a blank link)
    assert m["invariant"]
    assert m["shadow_edge"]
    # stages present, each honest (ok is a bool)
    assert isinstance(s["stages"], list) and s["stages"]


def test_synthesize_empty_question_honest_error():
    s = drm.synthesize("   ")
    assert s["ok"] is False
    assert "error" in s


def test_moonshot_routes_novel_and_never_fatal():
    mo = drm.moonshot("what is the one mechanism by which a swarm becomes smarter than its parts",
                      route=True)
    assert mo["ok"] is True
    assert "synthesis" in mo and "routed" in mo
    # routed is either enqueued (task_id) or deduped (already sent) or honest error — never fatal
    r = mo["routed"]
    assert r.get("ok") in (True, False)
    assert any(k in r for k in ("task_id", "deduped", "error"))
    # the goal handed to the swarm is grounded in the synthesized invariant
    assert mo["synthesis"]["invariant"]


def test_cadence_bounded_and_returns_moonshots():
    c = drm.cadence(limit=2, route=False)
    assert c["ok"] is True
    assert c["n_moonshots"] <= 2
    assert len(c["questions"]) <= 2
    assert "routed" in c


def test_status_contract():
    st = drm.status()
    assert st["ok"] is True
    assert st["schema"] == "deep_research_moonshot.v1"
    assert "synthesize" in st["contract"] and "moonshot" in st["contract"]
    # reuses our own machinery (self-steal), never external
    assert "swarm_surface" in st["reuses"]
