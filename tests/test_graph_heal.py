"""Tests for tools.graph_heal (Mickey17 W3, v0 compaction pass).

Cards per the lane ask: census counts a fixture; heal adds exactly the
expected edges (conservative: exactly-one-module token match, or source-file
rule; ambiguity heals nothing); demote only LISTS (pointer rows, no graph
mutation, nothing deleted); the whole pass is idempotent; --dry writes
nothing; a corrupt graph fails closed (exit 2).

Structural note baked into the assertions: an orphan is degree-0 BY
DEFINITION, so it can never already carry a why_context edge - the
already_healed counter is defense for a future rule change and reads 0 here;
second-pass idempotency rides the degree gate itself.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools import graph_heal as gh


def _node(nid, kind, label, source=""):
    n = {"id": nid, "kind": kind, "label": label}
    if source:
        n["source"] = source
    return n


@pytest.fixture()
def graph(tmp_path: Path) -> dict:
    """Fixture shaped like the real one: has_invariant edges fan out to
    invariant strings that are NOT node ids, so the only degree-giving edges
    are already_inside + one prior why_context.

    Expected plan (hand-derived, asserted downstream):
      HEAL  module:alpha_weaver -> token "alpha" matches only alpha_harvester
      HEAL  steal:beta_notes    -> token "beta" matches only beta_ledger
      HEAL  doctrine:scratch    -> no token match; source file exists and
                                   exactly one module (beta_ledger) owns it
      SKIP  module:beta_ledger  -> orphan module, own file exists but no OTHER
                                   owner: demote (self-heal is forbidden)
      SKIP  doctrine:gamma_probe-> "gamma" matches north AND south: ambiguous
      DEMOTE knot:delta_ghost, case_law "law:" (degenerate kind-word label),
             and the two SKIPs above
      omega_ring is NOT an orphan (prior why_context inbound edge).
    """
    mag = tmp_path / "mag"
    mag.mkdir()
    for name in ("alpha_harvester.py", "beta_ledger.py",
                 "gamma_north.py", "gamma_south.py", "alpha_weaver.py"):
        (mag / name).write_text("# fixture\n", encoding="utf-8")
    return {
        "schema": "knowledge_graph.v2",
        "ts": "2026-09-29T00:00:00Z",
        "nodes": [
            _node("module:alpha_harvester.py", "module", "alpha_harvester",
                  str(mag / "alpha_harvester.py")),
            _node("module:beta_ledger.py", "module", "beta_ledger",
                  str(mag / "beta_ledger.py")),
            _node("module:gamma_north.py", "module", "gamma_north",
                  str(mag / "gamma_north.py")),
            _node("module:gamma_south.py", "module", "gamma_south",
                  str(mag / "gamma_south.py")),
            _node("family:linked", "landscape", "linked"),
            # --- orphans below ---
            _node("module:alpha_weaver.py", "module", "alpha_weaver",
                  str(mag / "alpha_weaver.py")),
            _node("steal:beta_notes", "steal", "beta_notes",
                  str(mag / "beta_notes.md")),  # file absent: token rule only
            _node("doctrine:scratch", "doctrine", "scratch",
                  str(mag / "beta_ledger.py")),  # shares beta_ledger's file
            _node("doctrine:gamma_probe", "doctrine", "gamma_probe"),
            _node("knot:delta_ghost", "knot", "delta_ghost"),
            _node("law:", "case_law", "law"),
            _node("steal:omega_ring", "steal", "omega_ring"),
        ],
        "edges": [
            {"from": "module:alpha_harvester.py",
             "to": "invariant:alpha deterministic v1", "rel": "has_invariant",
             "text": "Schema: alpha.v1"},
            {"from": "module:gamma_north.py", "to": "module:family_linked",
             "rel": "already_inside", "text": "north is inside"},
            {"from": "family:linked", "to": "module:gamma_south.py",
             "rel": "already_inside", "text": "south is inside"},
            {"from": "module:gamma_north.py", "to": "steal:omega_ring",
             "rel": "why_context", "text": "graph_heal v0 why-context: prior"},
        ],
    }


def test_census_counts_fixture(graph, tmp_path):
    c = gh.census(graph)
    assert c["nodes"] == 12
    assert c["edges"] == 4
    # degree-holders: alpha_harvester, gamma_north, gamma_south,
    # family:linked, omega_ring -> 5 linked, 7 orphans of 12.
    assert c["orphans"] == 7
    assert c["orphans_by_kind"] == {"case_law": 1, "doctrine": 2,
                                    "knot": 1, "module": 2, "steal": 1}


def test_heal_adds_exactly_expected_edges(graph, tmp_path):
    plan_ = gh.plan(graph, tmp_path)
    got = {(op["from"], op["to"]) for op in plan_.heal_ops}
    assert got == {("module:alpha_harvester.py", "module:alpha_weaver.py"),
                   ("module:beta_ledger.py", "steal:beta_notes"),
                   ("module:beta_ledger.py", "doctrine:scratch")}
    for op in plan_.heal_ops:
        assert op["rel"] == gh.HEAL_REL
        assert op["heal"] == gh.HEAL_MARKER
    assert plan_.ambiguous == 1          # gamma matches north AND south
    assert plan_.already_healed == 0     # degree-0 nodes cannot hold edges
    assert plan_.demote_count == 4


def test_demote_only_lists_never_deletes(graph, tmp_path):
    plan_ = gh.plan(graph, tmp_path)
    # Every demotion is a pointer row into the quantized_thought archive;
    # no archive file is created by demotion and no graph node is removed.
    assert all(d["event"] == "forget" for d in plan_.demotions)
    assert all(d["pointer"].startswith(gh.GHOST_DIR_REL + "/")
               for d in plan_.demotions)
    names = {d["name"] for d in plan_.demotions}
    assert {"beta_ledger", "gamma_probe", "delta_ghost", "law"} == names
    assert not (tmp_path / gh.GHOST_DIR_REL).exists()
    nodes_before = len(graph["nodes"])
    edges_before = len(graph["edges"])
    gh.apply_heal(graph, plan_.heal_ops)
    assert len(graph["nodes"]) == nodes_before   # heal adds edges only
    assert len(graph["edges"]) == edges_before + 3


def test_idempotent_second_pass_adds_nothing(graph, tmp_path):
    plan_ = gh.plan(graph, tmp_path)
    gh.apply_heal(graph, plan_.heal_ops)
    second = gh.plan(graph, tmp_path)
    assert second.heal_count == 0
    # The anchor cascade: beta_ledger anchored two heals, so it earned
    # out-degree and is no longer an orphan; the three no-signal orphans
    # (gamma_probe still ambiguous, delta_ghost, law:) are what remains.
    assert second.census["orphans"] == 3
    assert second.demote_count == 3
    # forget list bytes are deterministic across passes (no wall-clock keys).
    f1, h1 = gh.forget_rows(graph, second)
    f2, h2 = gh.forget_rows(graph, gh.plan(graph, tmp_path))
    assert f1 == f2 and h1 == h2
    assert len(h1) == 4  # prior omega edge + the three new heals


def test_forget_merge_is_append_only_by_id(tmp_path):
    path = tmp_path / "forget_events.jsonl"
    first = gh.merge_forget(path, [{"id": "a", "name": "A"},
                                   {"id": "b", "name": "B"}])
    gh._write_jsonl(path, first)
    again = gh.merge_forget(path, [{"id": "b", "name": "B"},
                                   {"id": "c", "name": "C"}])
    assert [r["id"] for r in again] == ["a", "b", "c"]  # b not duplicated
    gh._write_jsonl(path, again)
    assert [r["id"] for r in gh.merge_forget(path, again)] == ["a", "b", "c"]


def test_dry_writes_nothing(graph, tmp_path, capsys):
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(graph, ensure_ascii=False),
                          encoding="utf-8")
    rc = gh.main(["--graph", str(graph_path), "--root", str(tmp_path), "--dry"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "RESULT: DRY census=7 orphans heal=3 demote=4" in out
    assert not (tmp_path / gh.FORGET_LIST_REL).exists()
    assert not (tmp_path / gh.HEAL_LOG_REL).exists()
    assert not (tmp_path / gh.FORGET_LIST_REL).parent.exists()
    assert len(json.loads(graph_path.read_text(encoding="utf-8"))["edges"]) == 4


def test_real_pass_writes_graph_and_pointer_list(graph, tmp_path, capsys):
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(graph, ensure_ascii=False),
                          encoding="utf-8")
    rc = gh.main(["--graph", str(graph_path), "--root", str(tmp_path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "RESULT: PASS healed=3 demoted_listed=4 deleted=0 graph_edges=7" in out
    healed = json.loads(graph_path.read_text(encoding="utf-8"))
    assert len(healed["edges"]) == 7
    assert healed["nodes"] == graph["nodes"]  # untouched apart from edges
    forget = [json.loads(x) for x in
              (tmp_path / gh.FORGET_LIST_REL).read_text(encoding="utf-8")
              .splitlines()]
    assert len(forget) == 4
    assert all(r["pointer"].startswith(gh.GHOST_DIR_REL + "/") for r in forget)
    # rerun over the healed graph: idempotent end to end - no new edges and
    # the forget list keeps its 4 recorded events (append-only by id).
    rc2 = gh.main(["--graph", str(graph_path), "--root", str(tmp_path)])
    assert rc2 == 0
    assert "healed=0" in capsys.readouterr().out
    assert len(json.loads(graph_path.read_text(encoding="utf-8"))
               ["edges"]) == 7
    forget_after = [json.loads(x) for x in
                    (tmp_path / gh.FORGET_LIST_REL).read_text(encoding="utf-8")
                    .splitlines()]
    assert len(forget_after) == 4


def test_colliding_labels_get_unique_pointers():
    # distinct ids sharing a label -> hash suffix; the real graph's 300
    # byte-identical "law:" rows -> sequence suffixes beyond that.
    used: set[str] = set()
    p1 = gh.archive_pointer("case_law", "law", "law:a", used)
    p2 = gh.archive_pointer("case_law", "law", "law:b", used)
    p3 = gh.archive_pointer("case_law", "law", "law:", used)
    p4 = gh.archive_pointer("case_law", "law", "law:", used)
    assert len({p1, p2, p3, p4}) == 4
    assert all(p.endswith(".md") for p in (p1, p2, p3, p4))


def test_census_reports_duplicate_ids_and_dedupes_forget(graph, tmp_path):
    # the real-graph defect, reproduced: 300 case_law rows share id "law:".
    graph["nodes"] += [dict(graph["nodes"][-2])] * 3  # extra "law:" rows
    c = gh.census(graph)
    assert c["orphans"] == 10
    assert c["duplicate_node_ids"] == {"law:": 4}
    plan_ = gh.plan(graph, tmp_path)
    forget, _ = gh.forget_rows(graph, plan_)
    merged = gh.merge_forget(tmp_path / "forget_events.jsonl", forget)
    assert len(merged) == len({r["id"] for r in merged})  # one identity once


def test_corrupt_graph_fails_closed(tmp_path, capsys):
    bad = tmp_path / "bad.json"
    bad.write_text("{not json", encoding="utf-8")
    assert gh.main(["--graph", str(bad), "--root", str(tmp_path)]) == 2
    assert "FAIL" in capsys.readouterr().err
    missing = tmp_path / "missing.json"
    assert gh.main(["--graph", str(missing), "--root",
                    str(tmp_path)]) == 2
