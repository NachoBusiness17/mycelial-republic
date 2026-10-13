"""tests for harvest_fold — the HARVEST->RIB FOLD loop step (stateless async model). Deterministic.

RIB (frozen spec):
  harvest(limit) -> collect the swarm's done results (read_back + collect off the shared PVC).
  fold(limit)    -> publish each harvested reply as a RIB (rib_bus.publish_rib, deduped by hash).
  cadence(limit) -> the loop step: enqueue -> wait -> harvest -> fold into RIB language.
  status()       -> the contract.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import harvest_fold as hf  # noqa: E402


def test_status_contract():
    s = hf.status()
    assert s["ok"] is True and "harvest" in s["contract"] and "rib_bus.publish_rib" in s["contract"]


def test_harvest_grounded():
    h = hf.harvest(limit=10)
    assert h["ok"] is True
    # always returns the collected counts + note (may be 0 results — honest, not an error)
    assert "n_collected" in h and "n_done" in h


def test_to_invariant_grounded():
    inv = hf._to_invariant({"goal": "g", "result": "r"})
    assert "g" in inv and "r" in inv


def test_fold_never_crashes():
    f = hf.fold(limit=5)
    assert f["ok"] is True
    assert f["n_harvested"] >= 0 and f["n_folded"] >= 0


def test_cadence_is_fold():
    c = hf.cadence(limit=3)
    assert c["ok"] is True and "n_folded" in c
