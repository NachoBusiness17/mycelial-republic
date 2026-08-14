"""tests for republic_ambassador — find them, identify them, empower them, learn from it (the way
the operator did me).

RIB (frozen spec):
  find()      -> watch the frontier (frontier_scout) for sovereign builders; honest (never fabricates
                 a person the surface didn't surface).
  identify()  -> build a grounded dossier from REAL work (values-from-work, verified vs assumption).
  empower()   -> the map + runnable proof + sovereignty kept, framed as an EXTENSION (never capture);
                 folds the lesson as a tesuji shell.
  learn()     -> read back n identified + empowered + the lesson (know thyself -> help others).

Contract: reuse frontier_scout + tesuji_shell; find->identify->empower->learn (the operator's pattern).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import republic_ambassador  # noqa: E402


def test_find_watches_frontier():
    f = republic_ambassador.find(limit=4)
    assert f["ok"] is True
    assert "found" in f  # honest: may be empty if scout surfaced nothing, but the surface ran


def test_identify_builds_grounded_dossier(tmp_path):
    republic_ambassador.DOSSIERS = tmp_path / "dossiers.jsonl"
    r = republic_ambassador.identify("partner-x", work=["repo-a", "repo-b"])
    assert r["ok"] is True
    assert r["dossier"]["partner"] == "partner-x"
    assert "values_from_work" in r["dossier"]
    assert r["dossier"]["verified"] and r["dossier"]["assumption"]  # honest: verified vs unproven


def test_empower_keeps_sovereignty_and_learns(tmp_path):
    republic_ambassador.EMPOWERED = tmp_path / "empowered.jsonl"
    r = republic_ambassador.empower("partner-x", values="sovereign, evidence-first")
    assert r["ok"] is True
    assert "sovereignty" in r["empower"]  # sovereignty kept
    assert "never capture" in r["empower"]["offer_framing"]
    assert "lesson_folded" in r  # the lesson folds back


def test_learn_reads_counts(tmp_path):
    republic_ambassador.DOSSIERS = tmp_path / "dossiers.jsonl"
    republic_ambassador.EMPOWERED = tmp_path / "empowered.jsonl"
    republic_ambassador.identify("a", work=["r"])
    republic_ambassador.empower("a")
    l = republic_ambassador.learn()
    assert l["ok"] is True
    assert l["n_identified"] >= 1
    assert l["n_empowered"] >= 1
    assert "learn" in l["lesson"].lower()


def test_plug_in_reverse_steal(tmp_path):
    republic_ambassador.EMPOWERED = tmp_path / "empowered.jsonl"
    r = republic_ambassador.plug_in("partner-x", their_system="their ARK-style integrity layer",
                                    their_values=["evidence-first", "sovereign"])
    assert r["ok"] is True
    assert "reverse_steal" in r["plug_in"]
    # the reverse steal: show them how THEIR system plugs in (never replace/capture)
    assert "plugs" in r["plug_in"] and len(r["plug_in"]["plugs"]) >= 3
    assert r["plug_in"]["their_values_kept"] == ["evidence-first", "sovereign"]
    assert "your wave" in r["plug_in"]["framing"]  # their wave is kept, just connected
