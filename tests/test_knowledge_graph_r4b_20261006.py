"""R4b cures (2026-10-06, ouroboros R4 memory fold S5, lane R4b; receipt
watch/inbox/ouroboros_20261005/r4b_land_graph_genome.md):

1. _edges() no longer mints already_inside edges from prose we_have entries:
   only a leading *.py token whose module node exists may mint. All 29 dangling
   edges in the 2026-10-06T09:20Z census were already_inside mints aimed at
   module ids nothing materializes ("stateless-ghost-swarm / cheap_swarm ..."
   style prose).
2. fold() stamps an outcome held/falsified/pending so a superseded conclusion
   is representable (the fold-rot mask of the no-demotion disease); an invalid
   outcome raises BEFORE any write.
"""
from __future__ import annotations

import json

import pytest

from mag import knowledge_graph as kg


def _mod(nid: str) -> dict:
    return {"id": nid, "kind": "module", "label": nid,
            "purpose": "", "invariants": [], "source": ""}


def test_prose_we_have_mints_no_edge():
    fam = {"id": "family:prose", "kind": "landscape", "label": "prose",
           "we_have": ["stateless-ghost-swarm / cheap_swarm (stateless doctrine)",
                       "routing.md - human oversight exceptional"], "delta": ""}
    edges = kg._edges([_mod("module:real_thing.py"), fam])
    assert [e for e in edges if e["rel"] == "already_inside"] == []


def test_py_shaped_we_have_mints_only_what_exists():
    fam = {"id": "family:py", "kind": "landscape", "label": "py",
           "we_have": ["mag/real_thing.py (the one that exists as a node)",
                       "mag/ghost_mod.py (py-shaped but no node)"], "delta": ""}
    edges = kg._edges([_mod("module:real_thing.py"), fam])
    inside = [e for e in edges if e["rel"] == "already_inside"]
    assert [(e["from"], e["to"]) for e in inside] == [("family:py", "module:real_thing.py")]


def test_fold_stamps_pending_by_default(tmp_path, monkeypatch):
    monkeypatch.setattr(kg, "GRAPH_PATH", tmp_path / "kg.json")
    r = kg.fold("held claim", "doctrine", "note")
    assert r["outcome"] == "pending"
    g = json.loads((tmp_path / "kg.json").read_text(encoding="utf-8"))
    assert g["nodes"][0]["outcome"] == "pending"


@pytest.mark.parametrize("outcome", ["held", "falsified"])
def test_fold_accepts_the_verdict_stamps(tmp_path, monkeypatch, outcome):
    monkeypatch.setattr(kg, "GRAPH_PATH", tmp_path / "kg.json")
    assert kg.fold(f"{outcome} claim", "doctrine", "n", outcome=outcome)["outcome"] == outcome


def test_fold_rejects_unknown_outcome_before_writing(tmp_path, monkeypatch):
    monkeypatch.setattr(kg, "GRAPH_PATH", tmp_path / "kg.json")
    with pytest.raises(ValueError):
        kg.fold("bogus", "doctrine", "n", outcome="bogus")
    assert not (tmp_path / "kg.json").exists()


def test_fold_same_id_is_amend_not_erase(tmp_path, monkeypatch):
    monkeypatch.setattr(kg, "GRAPH_PATH", tmp_path / "kg.json")
    kg.fold("twin", "doctrine", "first", outcome="falsified")
    again = kg.fold("twin", "doctrine", "second", outcome="held")
    assert again["already_present"] is True
    g = json.loads((tmp_path / "kg.json").read_text(encoding="utf-8"))
    assert len([n for n in g["nodes"] if n["id"].endswith("twin")]) == 1
    assert g["nodes"][0]["outcome"] == "falsified"
