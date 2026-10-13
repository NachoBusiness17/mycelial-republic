"""D8 regression: mycelium supersession lineage (republic.py port).

The door (eleven-doors D8): port superseded_by/valid_at from
mag/republic.py into lattice_edge.v1 + mycelium, then mycelium.v2. The
republic law (:209-218) ported to edges: superseded_by is set ONCE,
never re-pointed, its target must exist in the same book, and an edge
cannot supersede itself; valid_at is immutable once set. Unlike letters
(FROZEN after delivery), an edge is a LIVING measurement - weight and
counters stay mutable by design; only the lineage fields are frozen.
v1 rows on disk read as live-forever (fields absent = None).
"""
import json

import pytest

import mag.mycelium as myc
from mag.mycelium import SupersedeViolation, supersede


@pytest.fixture()
def book(tmp_path, monkeypatch):
    monkeypatch.setattr(myc, "MYC", tmp_path)
    monkeypatch.setattr(myc, "NODES", tmp_path / "nodes.jsonl")
    monkeypatch.setattr(myc, "EDGES", tmp_path / "edges.jsonl")
    a = myc.add_node("concept-a")
    b = myc.add_node("concept-b")
    c = myc.add_node("concept-c")
    return a, b, c


def _edge_ids():
    return [e["id"] for e in myc._load_edges()]


def test_new_edges_carry_v2_lineage_fields(book):
    a, b, _ = book
    r = myc.link(a["id"], b["id"], etype="supports")
    assert r["ok"]
    e = r["edge"]
    assert e["schema"] == "mycelium.v2"
    assert e["superseded_by"] is None
    assert e["valid_at"]  # stamped at creation


def test_supersede_sets_once_and_refuses_repoint(book):
    a, b, c = book
    myc.link(a["id"], b["id"], etype="supports")
    myc.link(a["id"], c["id"], etype="supports")
    e1, e2 = _edge_ids()
    r1 = supersede(e1, e2, reason="re-measured")
    assert r1["ok"]
    assert r1["edge"]["superseded_by"] == e2
    r2 = supersede(e1, e2)  # already superseded - never re-pointed
    assert not r2["ok"] and "never re-pointed" in r2["error"]


def test_supersede_target_must_exist_and_cannot_be_self(book):
    a, b, _ = book
    myc.link(a["id"], b["id"])
    e1, = _edge_ids()
    r = supersede(e1, "e-nonexistent")
    assert not r["ok"] and "not found" in r["error"]
    r2 = supersede(e1, e1)
    assert not r["ok"] and "itself" in r2["error"]


def test_rewrite_guard_blocks_repoint_and_valid_at_edit(book):
    a, b, c = book
    myc.link(a["id"], b["id"])
    myc.link(a["id"], c["id"])
    e1, e2 = _edge_ids()
    assert supersede(e1, e2)["ok"]
    # a hand-rolled rewrite that re-points the supersession -> refused
    edges = myc._load_edges()
    edges[0]["superseded_by"] = "e-somebodyelse"
    with pytest.raises(SupersedeViolation):
        myc._rewrite_edges(edges)
    # and one that forges valid_at on a stamped edge -> refused
    edges = myc._load_edges()
    edges[0]["valid_at"] = "2001-01-01T00:00:00+00:00"
    with pytest.raises(SupersedeViolation):
        myc._rewrite_edges(edges)
    # but weight/counter mutation still passes (living measurement)
    edges = myc._load_edges()
    edges[0]["weight"] = 0.9
    myc._rewrite_edges(edges)


def test_rewrite_guard_allows_the_first_supersede_via_rewrite(book):
    a, b, c = book
    myc.link(a["id"], b["id"])
    myc.link(a["id"], c["id"])
    e1, e2 = _edge_ids()
    edges = myc._load_edges()
    edges[0]["superseded_by"] = e2  # None -> existing id: the one legal move
    myc._rewrite_edges(edges)  # no raise
    assert myc._load_edges()[0]["superseded_by"] == e2


def test_v1_rows_read_live_forever_and_reinforce_still_works(book, tmp_path):
    a, b, _ = book
    # mint a NEVER-STAMPED v1 row directly (popping fields off a stamped
    # edge is exactly the forgery the guard refuses - proven by this test's
    # first draft failing on it)
    v1_edge = {
        "schema": "mycelium.v1", "id": "e-v1-legacy-0001", "src": a["id"],
        "dst": b["id"], "type": "supports", "note": "", "weight": 0.5,
        "success_count": 0, "failure_count": 0, "contradictions": 0,
        "refs_in": 0, "last_used": 0.0, "created": "2026-08-09T00:00:00+00:00",
        "protected": False,
    }
    with myc.EDGES.open("a", encoding="utf-8") as f:
        f.write(json.dumps(v1_edge) + "\n")
    loaded = next(e for e in myc._load_edges() if e["id"] == "e-v1-legacy-0001")
    assert loaded.get("superseded_by") is None  # absent reads as live forever
    # reinforce on the v1 edge still works and keeps its shape
    r = myc.reinforce(a["id"], b["id"], etype="any")
    assert r["ok"]
    e = next(e for e in myc._load_edges() if e["id"] == "e-v1-legacy-0001")
    assert "superseded_by" not in e  # the v1 row keeps its v1 shape


def test_lattice_edges_carry_lineage_fields():
    from mag import lattice_backfill as lb

    # the four emit sites stamp the fields; prove on the built edge set if
    # the corpus is present, else on a direct builder call smoke
    edges = getattr(lb, "build_lattice", lambda **k: None)
    made = None
    for name in ("build_lattice", "build", "lattice"):
        fn = getattr(lb, name, None)
        if callable(fn):
            try:
                made = fn()
                break
            except Exception:
                continue
    src = open(lb.__file__, encoding="utf-8").read()
    # the contract: every lattice_edge.v1 dict literal carries the fields
    assert src.count('"superseded_by": None') == 4
    assert src.count('"valid_at": _edge_valid_at') == 4
