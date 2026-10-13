"""Tests for the supersession wire (2026-10-07, lane m6-graph-supersession of
morning-block-20261007; R5 next-loop target 2: SUPERSEDED.md entries as graph
edges, superseded_by relation, both node ids, idempotent).

Cards:
  - the REAL register parses to its rows (register is a boot surface; the
    wire binds to its live bytes, not a hand-copied count);
  - every row mints a superseded/superseder node pair + one superseded_by
    edge carrying BOTH node ids and the evidence cell;
  - _edges() regenerates the edge from the dead node's superseded_by field
    (the build() wipe cure: a rebuild dropped all 117 manual why_context
    edges measured on a copy 2026-10-07, so an append-only wire alone would
    not be a durable graph fact);
  - build() end to end on a tmp root: the register facts survive a rebuild
    and a second build adds nothing (idempotent by regeneration);
  - tools/superseded_wire.py: --dry writes nothing; a real pass appends
    exactly the missing pair/edge to a fixture graph; a second pass adds
    zero; a corrupt graph or an unparseable register fails closed (exit 2).
"""
from __future__ import annotations

import json
from pathlib import Path

from mag import knowledge_graph as kg
from tools import superseded_wire as sw

REGISTER_FIXTURE = """# SUPERSEDED - fixture

| # | superseded conclusion | banked (when / where) | superseded by | evidence |
|---|---|---|---|---|
| 1 | the moon is cheese. | 2026-10-01 / fixture.md | 2026-10-02 / probe: it is rock | probe bytes |
| 2 | the well is bottomless. | 2026-10-03 / fixture.md | 2026-10-04 / sounding: it has a floor | sounding bytes |
"""


def test_real_register_parses_to_its_rows():
    rows = kg.superseded_rows()
    assert len(rows) == 6, "the live register held 6 rows at wire time"
    assert [r["n"] for r in rows] == ["1", "2", "3", "4", "5", "6"]
    for r in rows:
        assert r["believed"] and r["banked"] and r["superseding"] and r["evidence"]


def test_mint_pairs_join_both_node_ids():
    nodes, edges = kg._superseded_wire()
    assert len(nodes) == 12 and len(edges) == 6
    ids = {n["id"] for n in nodes}
    for e in edges:
        assert e["rel"] == kg.SUPERSEDED_REL == "superseded_by"
        assert e["from"] in ids and e["to"] in ids  # both endpoints are nodes
        assert e["from"].startswith("superseded:row-")
        assert e["to"] == "superseder:row-" + e["from"].split("row-")[1]
        assert e["text"]
    dead = next(n for n in nodes if n["id"] == "superseded:row-1")
    assert dead["superseded_by"] == "superseder:row-1"
    assert dead["outcome"] == "falsified"
    assert edges[0]["text"] == dead["evidence"][:160]


def test_edges_regenerates_from_the_superseded_by_field():
    # the build() wipe cure: the edge must regenerate from the node field
    # (maps_to precedent), not live as a manual append.
    nodes, _ = kg._superseded_wire()
    edges = kg._edges(nodes)
    sup = [e for e in edges if e["rel"] == "superseded_by"]
    assert len(sup) == 6
    assert {(e["from"], e["to"]) for e in sup} == {
        (f"superseded:row-{i}", f"superseder:row-{i}") for i in range(1, 7)}


def _tmp_root(tmp_path: Path, register_text: str = REGISTER_FIXTURE) -> Path:
    mag = tmp_path / "mag"
    mag.mkdir()
    (mag / "alpha.py").write_text('"""Alpha purpose."""\n', encoding="utf-8")
    reg = tmp_path / "memory" / "fold_history" / "SUPERSEDED.md"
    reg.parent.mkdir(parents=True)
    reg.write_text(register_text, encoding="utf-8")
    return tmp_path


def test_build_regenerates_the_register_facts(tmp_path, monkeypatch):
    root = _tmp_root(tmp_path)
    monkeypatch.setattr(kg, "ROOT", root)
    monkeypatch.setattr(kg, "GRAPH_PATH",
                        root / "memory" / "knowledge_graph.json")
    g = kg.build()
    sup = [e for e in g["edges"] if e["rel"] == "superseded_by"]
    assert {(e["from"], e["to"]) for e in sup} == {
        ("superseded:row-1", "superseder:row-1"),
        ("superseded:row-2", "superseder:row-2")}
    ids = {n["id"] for n in g["nodes"]}
    assert {"superseded:row-1", "superseder:row-1",
            "superseded:row-2", "superseder:row-2"} <= ids
    n_nodes, n_edges = len(g["nodes"]), len(g["edges"])
    # second build: regenerated from the same register bytes -> no growth
    g2 = kg.build()
    assert (len(g2["nodes"]), len(g2["edges"])) == (n_nodes, n_edges)
    assert len([e for e in g2["edges"]
                if e["rel"] == "superseded_by"]) == 2


def _fixture_graph() -> dict:
    return {"schema": "knowledge_graph.v2", "ts": "2026-10-07T00:00:00Z",
            "nodes": [{"id": "module:alpha.py", "kind": "module",
                       "label": "alpha"}],
            "edges": [{"from": "module:alpha.py", "to": "invariant:x",
                       "rel": "has_invariant", "text": "x"}]}


def test_wire_dry_writes_nothing(tmp_path, capsys):
    reg = tmp_path / "SUPERSEDED.md"
    reg.write_text(REGISTER_FIXTURE, encoding="utf-8")
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(_fixture_graph()), encoding="utf-8")
    rc = sw.main(["--graph", str(graph_path), "--register", str(reg),
                  "--root", str(tmp_path), "--dry"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "RESULT: DRY rows=2 add_nodes=4 add_edges=2" in out
    assert len(json.loads(
        graph_path.read_text(encoding="utf-8"))["edges"]) == 1


def test_wire_pass_then_idempotent_rerun(tmp_path, capsys):
    reg = tmp_path / "SUPERSEDED.md"
    reg.write_text(REGISTER_FIXTURE, encoding="utf-8")
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(_fixture_graph()), encoding="utf-8")
    rc = sw.main(["--graph", str(graph_path), "--register", str(reg),
                  "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "RESULT: PASS wired_edges=2 add_nodes=4" in out
    g = json.loads(graph_path.read_text(encoding="utf-8"))
    assert len(g["nodes"]) == 5 and len(g["edges"]) == 3
    sup = [e for e in g["edges"] if e["rel"] == "superseded_by"]
    assert {(e["from"], e["to"]) for e in sup} == {
        ("superseded:row-1", "superseder:row-1"),
        ("superseded:row-2", "superseder:row-2")}
    # rerun: zero growth
    rc2 = sw.main(["--graph", str(graph_path), "--register", str(reg),
                   "--root", str(tmp_path)])
    out2 = capsys.readouterr().out
    assert rc2 == 0
    assert "wired_edges=0 add_nodes=0" in out2
    g2 = json.loads(graph_path.read_text(encoding="utf-8"))
    assert (len(g2["nodes"]), len(g2["edges"])) == (5, 3)


def test_wire_fails_closed(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    reg = tmp_path / "SUPERSEDED.md"
    reg.write_text(REGISTER_FIXTURE, encoding="utf-8")
    assert sw.main(["--graph", str(bad), "--register", str(reg),
                    "--root", str(tmp_path)]) == 2
    assert "FAIL" in capsys.readouterr().err
    # a graph but an unparseable register is equally unverifiable
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(_fixture_graph()), encoding="utf-8")
    empty = tmp_path / "EMPTY.md"
    empty.write_text("no table here\n", encoding="utf-8")
    assert sw.main(["--graph", str(graph_path), "--register", str(empty),
                    "--root", str(tmp_path)]) == 2
    assert "zero rows" in capsys.readouterr().err
    assert len(json.loads(
        graph_path.read_text(encoding="utf-8"))["edges"]) == 1
