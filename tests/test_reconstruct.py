"""tests for reconstruct — deterministic tracking by RECONSTRUCTION on query, never held state.

RIB (frozen spec):
  state(surface) -> RECONSTRUCT the tracked surface on query (game-world / rib / corpus) from
                    content-addressed source, never a held snapshot. Each carries provenance.
  wave()         -> reconstruct the shared standing wave from the republic_wave ledgers.
  rederive()     -> the grounding check: query twice, confirm byte-stable (re-derivable, no drift).
  status()       -> the reconstruct-don't-hold contract.

Contract: reuses world_rib rederive + game_world + rib_bus + agent_corpus + republic_wave — no
invention. Query = re-derive from source bytes; nothing held that can drift.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import reconstruct  # noqa: E402


def test_state_reconstructs_game_world():
    s = reconstruct.state("game-world")
    assert s["ok"] is True
    assert "state" in s and "provenance" in s
    assert "reconstructed" in s["note"]


def test_state_handles_unknown_surface():
    s = reconstruct.state("anything-else")
    assert s["ok"] is True
    assert "state" in s  # falls back to corpus reconstruction, never errors


def test_wave_reconstructs_standing_wave(tmp_path):
    from mag import republic_wave
    republic_wave.WAVE_DIR = tmp_path
    republic_wave.WAVE = tmp_path / "wave.jsonl"
    republic_wave.WAVE_INDEX = tmp_path / "contributors.json"
    republic_wave.contribute("citizen-1", "the shared wave lesson")
    w = reconstruct.wave()
    assert w["ok"] is True
    assert "state" in w and "provenance" in w
    assert w["state"]["n_shared_invariants"] >= 1


def test_rederive_byte_stable():
    r = reconstruct.rederive("game-world")
    assert r["ok"] is True
    assert "re_derivable" in r
    # reconstructing twice gives the same state (no held drift)
    assert r["first"] == r["second"]


def test_status_contract():
    s = reconstruct.status()
    assert s["ok"] is True
    assert "reconstruct" in s["contract"] and "rederive" in s["contract"]
    assert "reconstruct, don't hold" in s["principle"]


def test_fold_doctrine():
    r = reconstruct.fold_doctrine()
    assert r["ok"] is True
    assert r["domain"] == "reconstruct"
    assert "key" in r
