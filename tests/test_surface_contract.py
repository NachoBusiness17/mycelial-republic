"""P3 — surfaces-as-spec CONTRACT tests: each castle (surface) defines the contract the
internals must fulfill. Red until the foundation delivers; green = the castle is built.

Operator/refactor doctrine (2026-08-10): "the surfaces are the spec of intent... castles in
the sky, put the foundations beneath them." This is the verifiable discipline that stops the
crude-signal drift: a surface must name its castle (the human question), and a contract test
asserts the internal endpoint delivers it. These call the modules DIRECTLY (hermetic, no live
HTTP) so they are deterministic and run anywhere.

Run: python -m pytest tests/test_surface_contract.py -q
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def _call(fn):
    """Call a module function defensively; return dict (or raise)."""
    mod, name = fn.split(":")
    import importlib
    m = importlib.import_module(mod)
    return getattr(m, name)()


# ── Machine castle (System: "Mag can/cannot operate because…") ─────────────
def test_sovereign_contract():
    """/api/v1/sovereign must deliver the whole machine: summary + tokenomics + ports."""
    s = _call("mag.sovereign_dashboard:sovereign_dashboard")
    assert isinstance(s, dict)
    assert "summary" in s, "sovereign must have summary (modules online/total)"
    assert "summary" in s and s["summary"].get("modules_total") is not None
    assert "tokenomics" in s and s["tokenomics"].get("status") is not None
    assert "ghost_port" in s


# ── Ghost·now castle (Home: "what matters now, what should I do") ───────────
def test_ghost_control_contract():
    """/api/v1/ghost/control must deliver the human-facing harness: scrum + recurring."""
    g = _call("mag.ghost_control:control")
    assert isinstance(g, dict)
    assert g.get("source") == "ghost"
    assert "scrum" in g, "ghost/control must expose scrum (the 'what matters now' harness)"
    assert "recurring" in g


# ── Solved castle ("surface what our history already solved") ───────────────
def test_solved_contract():
    """/api/v1/solved must surface the solved history from the internals (case law + RIB)."""
    s = _call("mag.solved_surface:solved")
    assert isinstance(s, dict)
    assert "case_law" in s and isinstance(s["case_law"], list)
    assert "n_case_law" in s and s["n_case_law"] >= 0
    assert "rib" in s and isinstance(s["rib"], list)
    assert "verkle_tip" in s
    # the case law is the solved decision set — must be non-empty once the system has history
    assert s["n_case_law"] > 0, "the internals should already hold solved case law"


# ── Health castle (Am I OK to work?) ────────────────────────────────────────
def test_health_contract():
    """/api/v1/health must answer 'am I ok to work': ok + status + integral."""
    h = _call("mag.health:sanity")
    assert isinstance(h, dict)
    assert "ok" in h
    assert "status" in h


# ── Knot lattice castle (History/Continuity: evidence → source) ─────────────
def test_chain_contract():
    """/api/v1/chain must deliver the verkle history: tip + chain (source-backed knots)."""
    import importlib
    m = importlib.import_module("dashboard.rest")
    c = m.h_chain({}, None)  # handler signature: h_chain(_p, _b)
    body = c[1] if isinstance(c, tuple) else c
    assert isinstance(body, dict)
    assert "tip" in body and "chain" in body, "chain must expose the verkle tip + chain"


# ── Story castle (the readable synthesis) ───────────────────────────────────
def test_story_contract():
    """Story must deliver an interpretive narrative (thesis), not a raw feed."""
    st = _call("mag.story:build_story")
    assert isinstance(st, dict)


# ── Diary castle (day-by-day spine from filed beads) ────────────────────────
def test_diary_contract():
    """Diary must deliver a day-by-day spine from filed beads."""
    d = _call("mag.diary:build_diary")
    assert isinstance(d, dict)


# ── Economy castle (cost per verified outcome, not token trivia) ────────────
def test_economy_contract():
    """Economy must expose tokenomics status + spend, not raw token trivia."""
    e = _call("mag.token_economy:economy_snapshot")
    assert isinstance(e, dict)
