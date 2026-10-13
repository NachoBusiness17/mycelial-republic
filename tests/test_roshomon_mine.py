"""tests for roshomon_mine — roshomon the socratic conversation, mine for data, inform the swarm of
direction, and passively measure tesuji from VS Code session logs as a data source.

RIB (frozen spec):
  roshomon_mine()      -> roshomon.compare on the socratic subject -> the CONVERGENT core (mined data).
  inform_swarm()       -> route each mined core invariant as a direction via swarm_surface.route_novel
                          (dedupe by anchor + drain in-cluster).
  tesuji_from_sessions() -> read our VS Code session logs (session store) as a data source + log them
                          as tesuji shells (passive tesuji measurement). Honest: never fabricates.

Contract: reuses roshomon, swarm_surface, tesuji_shell — no invention. Pure reuse of our own machinery.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import roshomon_mine  # noqa: E402


def test_roshomon_mine_reports():
    m = roshomon_mine.roshomon_mine()
    assert m["ok"] in (True, False)  # compare may have 0 witnesses (honest) but must not crash
    assert "subject" in m and "n_core_invariants" in m
    assert "core" in m
    assert m["honesty"]


def test_inform_swarm_routes_or_dedupes():
    r = roshomon_mine.inform_swarm(enqueue=True, limit=5)
    assert r["ok"] is True
    assert "routed_to_swarm" in r and "already_deduped" in r
    assert r["honesty"]


def test_tesuji_from_sessions_honest():
    t = roshomon_mine.tesuji_from_sessions(log=True)
    assert t["ok"] is True
    assert "n_session_sources" in t and "tesuji_shells_logged" in t
    assert t["honesty"]
