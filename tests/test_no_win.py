"""tests for no_win — the Kobayashi Maru primitive. Impossible constraints are won by changing the
conditions of the test, not by more force. Deterministic + $0.

RIB (frozen spec):
  frame(constraint)     -> name the frame before you decide how to beat it.
  reframe(c,i,f)        -> keep the invariant, repurpose the force, change the test. Never refuse.
  play(action)          -> the loop's entry; with no constraint it confirms the overlay stays overtop.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import no_win as nw  # noqa: E402


def test_frame_names_the_test():
    f = nw.frame("we don't have enough compute to win")
    assert f["ok"] is True and f["frame"] == "not_enough"
    assert nw.frame("no one will ever play this")["frame"] == "no_adoption"


def test_reframe_keeps_invariant_changes_conditions():
    r = nw.reframe("this can't be verified deterministically", invariant="the game is the work",
                   force="the DFHack overlay")
    assert r["ok"] is True
    assert r["invariant"] == "the game is the work"   # the bones survive
    assert r["force"] == "the DFHack overlay"          # the flesh adapts
    assert r["win"] is True
    assert "REFRAME" in r["move"]


def test_reframe_never_refuses():
    # every classified frame produces a play, never a refusal
    for c in ["no money", "can't prove it", "no users", "too expensive", "no path"]:
        assert nw.reframe(c, "invariant", "force")["win"] is True


def test_play_default_stands_over_above():
    p = nw.play()
    assert p["ok"] is True and "overtop" in p["play"]
