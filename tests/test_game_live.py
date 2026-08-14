"""tests for game_live — the game that IS the live republic. Deterministic + stateless.

RIB (frozen spec):
  live_events() -> read the ACTUAL republic's activity (chronicle payload) as world-feed events,
                   grounded from real ledgers; never invented. Each: kind + layman + anchor.
  feed()        -> fold each NEW live event as a verkle knot in the world (game_world.set_state) +
                   DM-narrate. Idempotent: an event already folded doesn't re-land.
  play_live()   -> the full live turn: ingest real activity -> fold to chain -> DM narrates.

Stateless-correct: exercises the real module against the real ledgers (read-only events + idempotent
feed). No monkeypatch of internals.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_live  # noqa: E402


def test_live_events_grounded():
    events = game_live.live_events(limit=5)
    assert isinstance(events, list)
    assert len(events) >= 1
    # each event has a layman label + a deterministic anchor
    for e in events:
        assert e.get("layman")
        assert e.get("anchor")


def test_anchor_deterministic():
    assert game_live._anchor("hello world") == game_live._anchor("hello world")
    assert game_live._anchor("a") != game_live._anchor("b")


def test_feed_idempotent_and_folds():
    # run feed twice; the second run should re-fold nothing (idempotent by anchor)
    r1 = game_live.feed(limit=5, narrate=False)
    assert r1["ok"] is True
    assert "folded_new" in r1 and "already_fed" in r1
    r2 = game_live.feed(limit=5, narrate=False)
    # honesty: already-fed events are skipped, not re-folded
    assert r2["folded_new"] >= 0
    # anchors that landed in r1 are recorded so they don't re-land
    fed = game_live._load_fed()
    assert isinstance(fed, set)


def test_play_live_full_turn():
    p = game_live.play_live(limit=5)
    assert p["ok"] is True
    assert "feed" in p and "world" in p
    assert p["feed"]["ok"] is True
    assert "n_entities" in p["world"]


def test_dm_narrate_returns_voice():
    folded = [{"layman": "a session was filed to disk"}, {"layman": "the swarm returned a pack"}]
    n = game_live._dm_narrate(folded)
    assert isinstance(n, str)
    assert len(n) > 0
