"""tests for republic_wave — the cross-operator engine: N people's corpora deduped into shared
invariants, sovereignty preserved, distributed into the one standing wave.

RIB (frozen spec):
  contribute(operator, invariant) -> fold one citizen's invariant into the shared wave. Content-
      addressed: same invariant from any citizen is ONE knot (deduped). Sovereignty: records who +
      the invariant, NEVER the raw personal record. Idempotent. Pure stdlib, $0.
  dedupe(records) -> collapse N raw records into unique invariants by content anchor. Returns the
      dedupe ratio (volume cheap, diversity is the self).
  wave() -> read back the shared standing wave (deduped invariants + who contributed).
  simulate(n, per) -> prove the billion-scale shape: n contributors -> unique invariants + ratio.

Contract: content-address by invariant (not raw text) = dedupe works at a billion; sovereignty =
who+what, never the raw record; distribution = fold into the shared wave everyone mounts.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import republic_wave  # noqa: E402


def test_contribute_dedupes_across_operators(tmp_path):
    republic_wave.WAVE_DIR = tmp_path
    republic_wave.WAVE = tmp_path / "wave.jsonl"
    republic_wave.WAVE_INDEX = tmp_path / "contributors.json"
    # same invariant from 2 different operators -> ONE knot (deduped)
    a = republic_wave.contribute("citizen-1", "the world is the authority")
    b = republic_wave.contribute("citizen-2", "the world is the authority")
    assert a["added_new"] is True
    assert b["deduped"] is True  # same invariant, second contributor adds no new knot
    assert a["anchor"] == b["anchor"]  # content address is the same
    w = republic_wave.wave()
    assert w["n_shared_invariants"] == 1  # one shared invariant, not two


def test_contribute_requires_both():
    r = republic_wave.contribute("", "")
    assert r["ok"] is False


def test_dedupe_ratio():
    records = [
        {"operator": "a", "invariant": "the world is the authority"},
        {"operator": "b", "invariant": "the world is the authority"},
        {"operator": "c", "invariant": "never capture, willful participation"},
    ]
    d = republic_wave.dedupe(records)
    assert d["n_inputs"] == 3
    assert d["n_unique_invariants"] == 2
    assert d["redundancy_removed"] == 1
    assert d["dedupe_ratio"] == round(1 / 3, 3)


def test_wave_reads_shared_and_contributors(tmp_path):
    republic_wave.WAVE_DIR = tmp_path
    republic_wave.WAVE = tmp_path / "wave.jsonl"
    republic_wave.WAVE_INDEX = tmp_path / "contributors.json"
    republic_wave.contribute("citizen-1", "lesson one")
    republic_wave.contribute("citizen-2", "lesson two")
    w = republic_wave.wave()
    assert w["ok"] is True
    assert w["n_shared_invariants"] == 2
    assert w["n_contributors"] == 2


def test_simulate_proves_dedupe_at_scale(tmp_path):
    republic_wave.WAVE_DIR = tmp_path
    republic_wave.WAVE = tmp_path / "wave.jsonl"
    republic_wave.WAVE_INDEX = tmp_path / "contributors.json"
    s = republic_wave.simulate(n=1000, per_contributor=3)
    assert s["ok"] is True
    assert s["n_inputs"] == 3000
    # shared lessons are deduped to a small set -> unique < inputs (dedupe happens)
    assert s["n_unique_invariants"] < s["n_inputs"]
    assert s["dedupe_ratio"] > 0.25  # redundancy collapses (3000 -> ~2004 unique); invariant remains
    assert s["honesty"]
