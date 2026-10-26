"""m7-heal-log-drain (2026-10-12, port-debt-20261011; design owner: steal card
watch/inbox/frontier_olm_adhoc/steal/agent-memory-continuity via x.md Find 1).

build() gains a heal-log drain as its LAST step. The wound: build() preserves
only hand-folded nodes, so a rebuild wiped every manual why_context edge
(measured 2026-10-07 on a copy: 117 -> 0, the supersession wire comment in
mag/knowledge_graph.py); the live graph sat at 0 why_context on 2026-10-11
with all 117 edges surviving only in the heal log. The cure re-applies the
newest heal log's edges idempotently by edge id (from/to/text hash) and
dead-letters dangling endpoints instead of letting them vanish.

Cards:
  - a log row whose endpoints exist in the rebuilt node set is restored as a
    why_context edge and PERSISTS to the graph file build() writes;
  - running build() twice adds no duplicate edges: same why_context edge-id
    set both times, no edge growth of any class (idempotent replay);
  - a log row with a dangling endpoint never enters the graph; it
    dead-letters exactly once with the dangling side named, and a second
    build() appends zero rows (append-only merge by edge id);
  - a duplicate row inside one log collapses (the log is derived state a
    later heal pass rewrites from the restored graph, so replaying the same
    edge twice is the normal case);
  - a missing heal log drains zero rows and writes no dead-letter file.
"""
from __future__ import annotations

import json
from pathlib import Path

from mag import knowledge_graph as kg

HEAL_LOG_REL = (Path("memory") / "corpus" / "quantized_thought"
                / "graph_ghosts" / "heal_log.jsonl")
DEAD_REL = (Path("memory") / "corpus" / "quantized_thought"
            / "graph_ghosts" / "heal_drain_dead_letters.jsonl")


def _row(frm: str, to: str, text: str) -> dict:
    return {"log": "heal", "graph_ts": "2026-10-06T18:06:27Z",
            "from": frm, "to": to, "text": text, "heal": "graph_heal.v0"}


def _tmp_root(tmp_path: Path) -> Path:
    mag = tmp_path / "mag"
    mag.mkdir()
    (mag / "alpha.py").write_text('"""Alpha purpose."""\n', encoding="utf-8")
    (mag / "beta.py").write_text('"""Beta purpose."""\n', encoding="utf-8")
    log = tmp_path / HEAL_LOG_REL
    log.parent.mkdir(parents=True)
    rows = [
        _row("module:alpha.py", "module:beta.py",
             "graph_heal v0 why-context: edge one"),
        _row("module:beta.py", "module:alpha.py",
             "graph_heal v0 why-context: edge two"),
        # exact duplicate of row one: a later heal pass rewrites the log from
        # the restored graph, so a double replay is the normal case
        _row("module:alpha.py", "module:beta.py",
             "graph_heal v0 why-context: edge one"),
        # dangling endpoint: doctrine:ghost is no node in the rebuilt set
        _row("module:alpha.py", "doctrine:ghost",
             "graph_heal v0 why-context: dangling"),
    ]
    log.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
    return tmp_path


def _patch(root: Path, monkeypatch) -> None:
    monkeypatch.setattr(kg, "ROOT", root)
    monkeypatch.setattr(kg, "GRAPH_PATH",
                        root / "memory" / "knowledge_graph.json")


def _why(edges: list[dict]) -> list[dict]:
    return [e for e in edges if e.get("rel") == "why_context"]


def test_build_restores_and_persists(tmp_path, monkeypatch):
    root = _tmp_root(tmp_path)
    _patch(root, monkeypatch)
    g = kg.build()
    why = _why(g["edges"])
    assert {(e["from"], e["to"], e["text"]) for e in why} == {
        ("module:alpha.py", "module:beta.py",
         "graph_heal v0 why-context: edge one"),
        ("module:beta.py", "module:alpha.py",
         "graph_heal v0 why-context: edge two")}
    assert all(e["rel"] == kg.HEAL_REL for e in why)
    drain = g["heal_drain"]
    assert (drain["log_rows"], drain["restored"], drain["duplicate_skipped"],
            drain["dead_lettered"], drain["malformed"]) == (4, 2, 1, 1, 0)
    # the restoration persists: the written graph file carries the same edges
    persisted = json.loads(kg.GRAPH_PATH.read_text(encoding="utf-8"))
    assert {(e["from"], e["to"], e["text"])
            for e in _why(persisted["edges"])} == {
        (e["from"], e["to"], e["text"]) for e in why}


def test_build_twice_adds_no_duplicates_and_dangling_dead_letters(tmp_path, monkeypatch):
    root = _tmp_root(tmp_path)
    _patch(root, monkeypatch)
    g1 = kg.build()
    ids1 = {kg.heal_edge_id(e) for e in _why(g1["edges"])}
    n1 = len(g1["edges"])
    # second build: the drain replays the same log onto a freshly regenerated
    # edge set and must land the same edges, never duplicates
    g2 = kg.build()
    ids2 = {kg.heal_edge_id(e) for e in _why(g2["edges"])}
    assert len(_why(g1["edges"])) == len(_why(g2["edges"])) == 2
    assert ids1 == ids2 and len(ids2) == 2
    assert len(g2["edges"]) == n1  # no growth in any edge class
    assert g2["heal_drain"]["restored"] == 2  # replay, not accumulation
    # the dangling row never entered the graph; it dead-lettered exactly once
    dead_rows = [json.loads(l) for l in
                 (root / DEAD_REL).read_text(encoding="utf-8").splitlines()
                 if l.strip()]
    assert len(dead_rows) == 1
    d = dead_rows[0]
    assert (d["from"], d["to"]) == ("module:alpha.py", "doctrine:ghost")
    assert d["dangling"] == "to"
    assert d["edge_id"] == kg.heal_edge_id(
        {"from": d["from"], "to": d["to"], "text": d["text"]})
    assert d["to"] not in {n["id"] for n in g2["nodes"]}
    assert not [e for e in g2["edges"] if e["to"] == "doctrine:ghost"]
    # a third build appends zero dead-letter rows (append-only by edge id)
    g3 = kg.build()
    dead_rows2 = [json.loads(l) for l in
                  (root / DEAD_REL).read_text(encoding="utf-8").splitlines()
                  if l.strip()]
    assert len(dead_rows2) == 1
    assert len(_why(g3["edges"])) == 2


def test_missing_log_is_a_noop_drain(tmp_path, monkeypatch):
    mag = tmp_path / "mag"
    mag.mkdir()
    (mag / "alpha.py").write_text('"""Alpha purpose."""\n', encoding="utf-8")
    _patch(tmp_path, monkeypatch)
    g = kg.build()
    drain = g["heal_drain"]
    assert drain["log_rows"] == 0
    assert drain["restored"] == 0
    assert drain["dead_lettered"] == 0
    assert not (tmp_path / DEAD_REL).exists()
