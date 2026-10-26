"""Corpus FTS5 wiring tests (B2-102, 2026-09-26).

Covers the contract the tools/corpus.py module spec states, on synthetic
mini-catalogs (never the 210 MB real one): the index-preferred path (fresh
db answers with engine=fts5, rows in catalog order), the freshness gate in
all its arms (absent db scans and says so; db older than catalog.jsonl is
stale and says so; a meta catalog_bytes mismatch is stale even when the
mtime gate is backdated out of the way, the never-silently-stale law; a
garbage db is stale, not a crash), the mid-token parity honesty pin (scan
finds noblegarden for "garden", fts5 does not, and the fts5 result carries
the parity note naming the 3 measured delta rows), the read-only law (a
search over a fresh index leaves the db bytes and the directory untouched),
and the rebuild entry point bound to the same gate code (single source: the
rebuild tool's _load_corpus is pointed at the test's corpus module).
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ROWS = [
    {"path": "docs/garden.md", "title": "garden notes",
     "zone": "doctrine", "ext": ".md", "mtime": "2026-09-18T00:00:00Z"},
    {"path": "ext/noblegarden.cpp", "title": "noble feast",
     "zone": "ext:games", "ext": ".cpp", "mtime": "2026-09-18T00:00:00Z"},
    {"path": "docs/hermes_queue.md", "title": "queue",
     "zone": "doctrine", "ext": ".md", "mtime": "2026-09-15T00:00:00Z"},
    {"path": "memory/runs/verkle.md", "title": "verkle knot",
     "zone": "runs", "ext": ".md", "mtime": "2026-09-20T00:00:00Z"},
]


def _cid(rel: str) -> str:
    return hashlib.sha256(rel.encode("utf-8")).hexdigest()[:12]


@pytest.fixture()
def fts_env(tmp_path, monkeypatch):
    corpus = _load("corpus_under_test", "tools/corpus.py")
    rebuild = _load("corpus_rebuild_under_test", "tools/corpus_fts_rebuild.py")
    cat = tmp_path / "catalog.jsonl"
    with open(cat, "w", encoding="utf-8") as fh:
        for row in ROWS:
            full = {"id": _cid(row["path"]), "bytes": 100, "age_days": 8, **row}
            fh.write(json.dumps(full) + "\n")
    db = tmp_path / "catalog_fts.sqlite"
    tags = tmp_path / "tags.jsonl"
    monkeypatch.setattr(corpus, "CATALOG", cat)
    monkeypatch.setattr(corpus, "FTS_DB", db)
    monkeypatch.setattr(corpus, "TAGS", tags)
    monkeypatch.setattr(corpus, "REBUILD_CLI", "tools/corpus_fts_rebuild.py")
    return {"corpus": corpus, "rebuild": rebuild,
            "catalog": cat, "db": db, "tags": tags}


def _build(env) -> dict:
    return env["rebuild"].build_index(env["catalog"], env["db"])


def test_fresh_index_preferred(fts_env):
    env = fts_env
    stats = _build(env)
    assert stats["rows_indexed"] == len(ROWS)
    res = env["corpus"].corpus_search(query="garden")
    assert res["ok"] is True
    assert res["engine"] == "fts5"
    assert res["index_state"] == "fresh"
    assert [h["path"] for h in res["hits"]] == ["docs/garden.md"]
    assert "parity_note" in res and "mid-token" in res["parity_note"]
    assert res["law"].startswith("pointers only")


def test_missing_db_scans_and_says_so(fts_env):
    res = fts_env["corpus"].corpus_search(query="garden")
    assert res["engine"] == "scan"
    assert res["index_state"] == "absent"
    assert "tools/corpus_fts_rebuild.py" in res["index_note"]
    assert [h["path"] for h in res["hits"]] == ["docs/garden.md", "ext/noblegarden.cpp"]


def test_db_older_than_catalog_is_stale_and_says_so(fts_env):
    env = fts_env
    _build(env)
    future = time.time() + 120
    os.utime(env["catalog"], (future, future))  # catalog now newer than db
    res = env["corpus"].corpus_search(query="garden")
    assert res["engine"] == "scan"
    assert res["index_state"] == "stale"
    assert "older than catalog.jsonl" in res["index_note"]


def test_bytes_gate_catches_what_mtime_hides(fts_env):
    """The never-silently-stale law's hard case: catalog content changed but
    its mtime backdated below the db. Only the meta catalog_bytes gate sees
    it, and the result must say stale, not pass as fresh."""
    env = fts_env
    _build(env)
    with open(env["catalog"], "a", encoding="utf-8") as fh:
        fh.write(json.dumps({"id": "x" * 12, "path": "docs/late.md",
                             "bytes": 1, "mtime": "2026-09-21T00:00:00Z",
                             "zone": "doctrine", "ext": ".md",
                             "title": "late", "age_days": 5}) + "\n")
    past = env["db"].stat().st_mtime - 60
    os.utime(env["catalog"], (past, past))
    res = env["corpus"].corpus_search(query="garden")
    assert res["engine"] == "scan"
    assert res["index_state"] == "stale"
    assert "catalog bytes" in res["index_note"]


def test_midtoken_parity_disclosed_on_both_engines(fts_env):
    env = fts_env
    scan = env["corpus"].corpus_search(query="garden")
    assert scan["engine"] == "scan"
    assert "ext/noblegarden.cpp" in {h["path"] for h in scan["hits"]}
    _build(env)
    fts = env["corpus"].corpus_search(query="garden")
    assert fts["engine"] == "fts5"
    assert "ext/noblegarden.cpp" not in {h["path"] for h in fts["hits"]}
    note = fts["parity_note"]
    for token in ("hermes 914 to 912", "falsifier 69 to 68", "garden 17 to 14",
                  "B2_22_fts5_spike_20260926.md"):
        assert token in note


def test_search_is_readonly_over_the_index(fts_env):
    env = fts_env
    _build(env)
    sha_before = hashlib.sha256(env["db"].read_bytes()).hexdigest()
    siblings_before = sorted(p.name for p in env["db"].parent.iterdir())
    for q in ("garden", "verkle", "hermes"):
        res = env["corpus"].corpus_search(query=q)
        assert res["engine"] == "fts5"
    assert hashlib.sha256(env["db"].read_bytes()).hexdigest() == sha_before
    assert sorted(p.name for p in env["db"].parent.iterdir()) == siblings_before


def test_fts_filters_zone_ext_since_and_kind(fts_env):
    env = fts_env
    _build(env)
    with open(env["tags"], "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"id": _cid("memory/runs/verkle.md"),
                             "kind": "receipt"}) + "\n")
        fh.write(json.dumps({"id": _cid("docs/hermes_queue.md"),
                             "kind": "code"}) + "\n")
    corpus = env["corpus"]
    assert corpus.corpus_search(query="verkle", zone="doctrine")["hits"] == []
    assert [h["path"] for h in corpus.corpus_search(
        query="verkle", ext=".md")["hits"]] == ["memory/runs/verkle.md"]
    assert corpus.corpus_search(query="verkle", since="2026-09-21")["hits"] == []
    kind_res = corpus.corpus_search(query="verkle", kind="receipt")
    assert kind_res["engine"] == "fts5"
    assert [h["path"] for h in kind_res["hits"]] == ["memory/runs/verkle.md"]
    assert corpus.corpus_search(query="verkle", kind="code")["hits"] == []
    no_tags = corpus.corpus_search(query="verkle", kind="prose")
    assert no_tags["ok"] is False and "tag pass" in no_tags["error"]


def test_termless_query_bypasses_index_disclosed(fts_env):
    env = fts_env
    _build(env)
    res = env["corpus"].corpus_search(query="")
    assert res["engine"] == "scan"
    assert res["index_state"] == "bypassed"
    assert res["hit_count"] == 4  # scan early-breaks far below catalog end


def test_garbage_db_is_stale_not_crash(fts_env):
    env = fts_env
    env["db"].write_bytes(b"this is not sqlite" * 10)
    res = env["corpus"].corpus_search(query="garden")
    assert res["engine"] == "scan"
    assert res["index_state"] == "stale"
    assert "unreadable" in res["index_note"]


def test_rebuild_check_and_deep_bound_to_same_gate(fts_env, monkeypatch):
    env = fts_env
    rebuild = env["rebuild"]
    monkeypatch.setattr(rebuild, "_load_corpus", lambda: env["corpus"])
    _build(env)
    ok = rebuild.check(deep=True)
    assert ok["index_state"] == "fresh"
    assert ok["deep"] == "match"
    assert rebuild.check(deep=False)["index_state"] == "fresh"
    # now break freshness past the mtime gate and read the same gate back
    with open(env["catalog"], "a", encoding="utf-8") as fh:
        fh.write("{}\n")
    past = env["db"].stat().st_mtime - 60
    os.utime(env["catalog"], (past, past))
    bad = rebuild.check(deep=True)
    assert bad["index_state"] == "stale"
    assert "catalog bytes" in bad["note"]


def test_rebuild_main_check_exit_codes(fts_env, monkeypatch, capsys):
    env = fts_env
    rebuild = env["rebuild"]
    monkeypatch.setattr(rebuild, "_load_corpus", lambda: env["corpus"])
    _build(env)
    monkeypatch.setattr(sys, "argv", ["corpus_fts_rebuild.py", "--check"])
    assert rebuild.main() == 0
    env["db"].unlink()
    monkeypatch.setattr(sys, "argv", ["corpus_fts_rebuild.py", "--check"])
    assert rebuild.main() == 2
    capsys.readouterr()
