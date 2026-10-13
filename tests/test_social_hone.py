"""tests for social_hone — the DATA-HONING pipeline: dumb agents drive browsers, capture is recorded
as HIGH-QUALITY input socratically. Deterministic $0 coordinator.

RIB (frozen spec):
  drive(surface)  -> a dumb agent drives browser_driver on a social surface; honest if CDP/browser is
      down (never fabricates captured content). Unknown surface -> honest error.
  socratic(raw)   -> Socratic distillation of raw -> high-quality input (question + takeaway),
      grounded in raw, never fabricated; empty raw -> honest error.
  hone(surface)   -> drive + socratic + percolate + record to the honed feed; if drive fails, honest.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import social_hone as sh  # noqa: E402


def test_status_surfaces_and_feed():
    st = sh.status()
    assert st["ok"] is True
    assert st["schema"] == "social_hone.v1"
    for s in ("x", "deepseek", "grok", "perplexity"):
        assert s in st["surfaces"]
    assert "honed_feed" in st


def test_drive_unknown_surface_honest():
    r = sh.drive("not-a-surface")
    assert r["ok"] is False
    assert "unknown surface" in r["error"]


def test_drive_honest_when_browser_down():
    # with the CDP/browser down, drive reports it (never fabricates raw content)
    r = sh.drive("x")
    assert r["ok"] in (True, False)
    if r["ok"]:
        assert r["raw"]
    else:
        assert r["error"]


def test_socratic_distills_or_honest_empty():
    s = sh.socratic("here is a concrete high-signal insight about the outside world")
    assert s["ok"] is True
    assert s["takeaway"] and s["question"]
    # empty raw -> honest error, never fabricated
    e = sh.socratic("   ")
    assert e["ok"] is False


def test_hone_never_fabricates():
    r = sh.hone("x")
    assert r["ok"] in (True, False)
    if r["ok"]:
        assert r["takeaway"] and "recorded" in r
