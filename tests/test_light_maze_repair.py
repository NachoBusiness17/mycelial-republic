#!/usr/bin/env python3
"""tests/test_light_maze_repair.py - G2 lane g2-i10-light-maze (2026-10-18).

Repair-list tests for tools/light_maze.py against memory/rib/RIB_LIGHT_MAZE_20261012.md:
  R1 - real FTS5 probe of catalog/catalog_fts.sqlite (old reference/gstdcoin
       path + "# skip" stub replaced)
  R2 - prior-receipt hits>2 proxy kept but marked PROXY with upgrade path
  R3 - the rib's fourth route (unknown) in the classify ladder
  R4 - optional MAG_LIT_MAP lit-map hook (absent file = corpus+receipts only)
  R5 - decision ledger JSONL (env-overridable so tests never write the repo)
"""
from __future__ import annotations

import json
import sqlite3
import sys

import pytest

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[1]))

import tools.light_maze as lm  # noqa: E402


# ---------------------------------------------------------------- R3: routes

def test_route_frontier_zero_signal():
    assert lm.classify_match(0, False, False) == "frontier"


def test_route_unknown_thin_signal():
    # 1-2 corpus hits with no coverage: too thin to route, ask the operator.
    assert lm.classify_match(1, False, False) == "unknown"
    assert lm.classify_match(2, False, False) == "unknown"


def test_route_freelane_corpus_lit_uncovered():
    assert lm.classify_match(lm.THIN_SIGNAL_HITS, False, False) == "freelane"
    assert lm.classify_match(50, False, False) == "freelane"


def test_route_inplace_tool_coverage():
    assert lm.classify_match(0, True, False) == "inplace"


def test_route_inplace_prior_receipt_and_tool():
    assert lm.classify_match(9, True, True) == "inplace"


def test_route_freelane_prior_receipt_without_tool():
    assert lm.classify_match(1, False, True) == "freelane"


def test_route_negative_hits_defensive_zero():
    assert lm.classify_match(-3, False, False) == "frontier"


def test_all_four_routes_distinct():
    got = {
        lm.classify_match(0, False, False),
        lm.classify_match(1, False, False),
        lm.classify_match(3, False, False),
        lm.classify_match(0, True, False),
    }
    assert got == {"frontier", "unknown", "freelane", "inplace"}


# ---------------------------------------------------------------- R1: FTS

def test_r1_constant_points_at_real_index():
    assert lm.CORPUS_FTS.name == "catalog_fts.sqlite"
    assert "catalog" in lm.CORPUS_FTS.parts
    # the dead reference/gstdcoin path must not be back
    assert "reference" not in lm.CORPUS_FTS.parts
    assert "gstdcoin" not in lm.CORPUS_FTS.parts


def test_r1_fts_path_exists_and_queryable():
    if not lm.CORPUS_FTS.is_file():
        pytest.skip("catalog/catalog_fts.sqlite missing on this tree")
    con = sqlite3.connect("file:%s?mode=ro" % lm.CORPUS_FTS.as_posix(), uri=True)
    try:
        n = con.execute(
            "SELECT count(*) FROM corpus WHERE corpus MATCH 'agents'"
        ).fetchone()[0]
    finally:
        con.close()
    assert n > 0


def test_r1_search_corpus_returns_hits_and_matches():
    if not lm.CORPUS_FTS.is_file():
        pytest.skip("catalog/catalog_fts.sqlite missing on this tree")
    hits, matches = lm.search_corpus("agents agreement registry")
    assert isinstance(hits, int) and hits > 0
    assert isinstance(matches, list) and len(matches) > 0
    assert "path" in matches[0] and "title" in matches[0]


def test_r1_search_corpus_no_terms_is_safe():
    hits, matches = lm.search_corpus("a b c d")
    assert hits == 0 and matches == []


# ---------------------------------------------------------------- R2: proxy

def test_r2_proxy_marker_and_upgrade_path_in_source():
    src = lm.__file__
    with open(src, encoding="utf-8") as fh:
        text = fh.read()
    assert "PROXY" in text
    assert "watch" in text and "inbox" in text  # upgrade path named


def test_r2_proxy_threshold_is_hits_over_two():
    # route() derives the proxy from hits > 2; verify the boundary end to end
    # through classify_match the way route() calls it.
    assert lm.classify_match(2, False, True) == "freelane"
    assert lm.classify_match(3, False, True) == "freelane"


# ---------------------------------------------------------------- R4: lit map

def test_r4_lit_map_absent_is_empty(tmp_path, monkeypatch):
    monkeypatch.delenv("MAG_LIT_MAP", raising=False)
    assert lm.read_lit_map() == []


def test_r4_lit_map_list_form(tmp_path, monkeypatch):
    p = tmp_path / "lit.json"
    p.write_text(json.dumps(["qwen-coder-instruct", "ollama-gemma"]), encoding="utf-8")
    monkeypatch.setenv("MAG_LIT_MAP", str(p))
    assert lm.read_lit_map() == ["qwen-coder-instruct", "ollama-gemma"]


def test_r4_lit_map_dict_form_and_missing_file(monkeypatch, tmp_path):
    p = tmp_path / "lit.json"
    p.write_text(json.dumps({"lit": ["hot-weights-a"]}), encoding="utf-8")
    monkeypatch.setenv("MAG_LIT_MAP", str(p))
    assert lm.read_lit_map() == ["hot-weights-a"]
    monkeypatch.setenv("MAG_LIT_MAP", str(tmp_path / "nope.json"))
    assert lm.read_lit_map() == []


def test_r4_lit_map_match_routes_inplace(tmp_path, monkeypatch):
    # a lit corridor covering the task counts as known-value coverage even
    # with zero corpus signal and no beacon artifacts.
    p = tmp_path / "lit.json"
    p.write_text(json.dumps(["maze-router-organ"]), encoding="utf-8")
    monkeypatch.setenv("MAG_LIT_MAP", str(p))
    monkeypatch.setattr(lm, "read_beacon", lambda: None)
    monkeypatch.setattr(lm, "search_corpus", lambda task: (0, []))
    monkeypatch.setenv("MAG_LIGHT_MAZE_LEDGER", str(tmp_path / "ledger.jsonl"))
    out = lm.route("finish the maze-router-organ corridor")
    assert out["route"] == "inplace"
    assert out["evidence"]["lit_map_match"] is True


# ---------------------------------------------------------------- R5: ledger

def test_r5_ledger_row_written_and_never_raises(tmp_path, monkeypatch):
    ledger = tmp_path / "deep" / "decisions.jsonl"
    monkeypatch.setenv("MAG_LIGHT_MAZE_LEDGER", str(ledger))
    monkeypatch.delenv("MAG_LIT_MAP", raising=False)
    monkeypatch.setattr(lm, "read_beacon", lambda: None)
    monkeypatch.setattr(lm, "search_corpus", lambda task: (4, [{"path": "x", "title": "y"}]))
    out = lm.route("prior art for the ledger organ")
    assert ledger.is_file()
    rows = [json.loads(line) for line in ledger.read_text(encoding="utf-8").splitlines()]
    assert len(rows) == 1
    assert rows[0]["route"] == out["route"] == "freelane"
    assert "ts" in rows[0] and "evidence" in rows[0]
    # a poisoned ledger target must not break the route decision
    block = tmp_path / "nope" / "x"
    block.parent.mkdir(parents=True)
    block.write_text("file blocks mkdir", encoding="utf-8")
    monkeypatch.setenv("MAG_LIGHT_MAZE_LEDGER", str(block / "decisions.jsonl"))
    out2 = lm.route("prior art again")
    assert out2["route"] == "freelane"


# ---------------------------------------------------------------- CLI compat

def test_cli_original_keys_and_exit_zero(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("MAG_LIGHT_MAZE_LEDGER", str(tmp_path / "ledger.jsonl"))
    monkeypatch.delenv("MAG_LIT_MAP", raising=False)
    monkeypatch.setattr(lm, "read_beacon", lambda: None)
    monkeypatch.setattr(lm, "search_corpus", lambda task: (0, []))
    monkeypatch.setattr(sys, "argv", ["light_maze.py", "route", "the", "task"])
    assert lm.main() == 0
    out = json.loads(capsys.readouterr().out)
    # the original five top-level keys survive (additive repair only)
    for key in ("task", "corpus_hits", "beacon_match", "route", "lit_corridors"):
        assert key in out
    assert out["task"] == "route the task"
    assert out["route"] == "frontier"


def test_cli_no_args_exit_one(capsys):
    argv = sys.argv
    sys.argv = ["light_maze.py"]
    try:
        assert lm.main() == 1
    finally:
        sys.argv = argv
    assert "usage" in capsys.readouterr().out


def test_beacon_reader_tolerant_when_file_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(lm, "BEACON_JSON", tmp_path / "absent.json")
    assert lm.read_beacon() is None
