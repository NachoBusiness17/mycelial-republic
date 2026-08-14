"""tests for game_environment — the WORLD ENVIRONMENT, self-stolen from the scifi corpus.
Deterministic + $0.

RIB (frozen spec):
  explore(region) -> enter a region of the environment (its scifi invariant, grounded).
  render()        -> the base region map with every region's glyph placed.
  status()        -> the map of the world = the map of our corpus.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_environment as ge  # noqa: E402


def test_status():
    s = ge.status()
    assert s["ok"] is True and s["n_regions"] >= 8


def test_explore_athena():
    r = ge.explore("the_athena_archive")
    assert r["ok"] is True and r["region"] == "The Athena Archive"
    assert "Saelis" in r["invariant"] or "Athena" in r["invariant"]


def test_explore_every_region():
    for key in ge.REGION_KEYS:
        r = ge.explore(key)
        assert r["ok"] is True, key
        assert r["scifi"]  # every region is a real scifi steal


def test_render_places_all():
    r = ge.render()
    assert r["ok"] is True and r["n_regions"] == len(ge.REGIONS)
    assert len(r["placed"]) == len(ge.REGIONS)
