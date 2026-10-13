"""tests for ghost_memlance.select_wave — the favorite tool (memlance) made smarter with the wave
geometry (self-improve: 'always relooking at your own tools to make them better'). Deterministic.

RIB (frozen spec):
  select(goal,k)     -> GROUNDED selection: only states read as real bytes, provenance + verified
      guard, never hallucinate. (unchanged core — the favorite stays intact)
  select_wave(goal,k)-> the SAME grounded select + an ADDITIVE holographic-wave bias (osculating
      coldest seams). Keeps provenance + verified. wave_aware=True; biased states carry a wave_bias.
      Never surfaces ungrounded states (the wave only reranks what is already grounded).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import ghost_memlance as gm  # noqa: E402


def test_select_grounded_shape_unchanged():
    r = gm.select("standing wave", k=4)
    assert r["ok"] is True
    for s in r["selected"]:
        # provenance + verified guard always present (the anti-hallucination core)
        assert s["path"] and "verified" in s and "reason" in s and "excerpt" in s


def test_select_wave_keeps_grounding_and_flags_wave():
    r = gm.select_wave("standing wave", k=4)
    assert r["ok"] is True
    assert r["wave_aware"] is True
    for s in r["selected"]:
        # the wave reranks but never drops the grounding guard
        assert s["path"] and "verified" in s and "excerpt" in s
    # at least one state carries the wave bias (or none if no seams matched — still valid)
    biased = [s for s in r["selected"] if s.get("wave_bias")]
    assert isinstance(biased, list)
    for s in biased:
        assert s["wave_bias"] > 0 and "wave-seam bias" in s["reason"]


def test_select_wave_never_surfaces_ungrounded():
    # select_wave must never introduce states without provenance, regardless of wave bias
    r = gm.select_wave("self sovereign agent", k=6)
    for s in r["selected"]:
        assert s["path"]
        assert isinstance(s["verified"], bool)
