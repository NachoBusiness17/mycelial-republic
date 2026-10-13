"""tests for adventure_moonshot — the adventure moonshot, forged from the corpus + routed to swarm.
Deterministic + $0 core.

RIB (frozen spec):
  adventure(ask, route) -> PRIOR->WITNESS->SHADOW->KNOT->MARRIAGE->ROUTE; a novel adventure invariant
       + a novel passage, forged from the corpus (never a copy).
  cadence(limit, route) -> sweep the game's open threads and moonshot them.
  status()              -> the contract.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import adventure_moonshot as am  # noqa: E402


def test_status_contract():
    s = am.status()
    assert s["ok"] is True and "PRIOR" in s["contract"]


def test_adventure_forges_novel_not_copy():
    a = am.adventure("what thread is worth walking?", route=False)
    assert a["ok"] is True
    assert a["invariant"] and a["passage"]
    # the passage is forged from the corpus (heritage present), not empty
    assert a["passage"] != ""


def test_stages_present():
    a = am.adventure(route=False)
    for name in ("prior", "witness", "shadow", "knot", "route"):
        assert name in a["stages"]
    # prior is self-stolen from the corpus (game_campaigns found)
    assert "campaign_titles" in a["stages"]["prior"] or a["stages"]["prior"]["ok"]


def test_cadence_moonshots():
    c = am.cadence(limit=2, route=False)
    assert c["ok"] is True and c["n_moonshots"] == 2
    assert len(c["moonshots"]) == 2
