"""tests for socratic_research — the 5-turn Socratic deep-research ask on the 1000-vibecoder dedupe +
wave distribution, framed by our own lensing + 5 W's, routed to the swarm for direction.

RIB (frozen spec):
  frame() -> self-steal tool_5ws.ask + lens_shader.program to frame the subject (5-W + lens steer).
  ask()   -> route each Socratic turn's direction question to the swarm via swarm_surface.route_novel
             (dedupe by anchor + drain in-cluster). Deterministic + $0; the swarm answers.
  status()-> subject + turn count + surface.

Contract: reuses tool_5ws, lens_shader, swarm_surface — no invention. Turns are sharp direction
questions, not vague prompts.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import socratic_research  # noqa: E402


def test_subject_and_five_turns():
    assert len(socratic_research.SOCRATIC_TURNS) == 5
    assert "dedup" in socratic_research.SUBJECT.lower() or "vibecoder" in socratic_research.SUBJECT.lower()


def test_frame_self_steals_5ws_and_lens():
    f = socratic_research.frame()
    assert f["ok"] is True
    assert "five_ws" in f or "five_ws_error" in f
    assert "lens_frame" in f or "lens_error" in f


def test_ask_routes_to_swarm_or_dedupes():
    r = socratic_research.ask(enqueue=True, limit=5)
    assert r["ok"] is True
    assert "routed_to_swarm" in r and "already_deduped" in r
    assert r["n_turns"] == 5
    # each turn routed (or deduped) via the one primitive; honesty: not fabricated here
    assert r["routed_to_swarm"] + r["already_deduped"] == 5
    assert r["honesty"]


def test_status_reports_surface():
    s = socratic_research.status()
    assert s["ok"] is True
    assert s["n_turns"] == 5
    assert s["surface"] == socratic_research.SURFACE
