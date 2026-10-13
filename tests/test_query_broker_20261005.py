"""D11 regression: the three-signal query broker.

The door: FTS + lattice + embedding fusion. The contract: RRF fusion
(k=60) with per-signal ranks visible; the embedding signal is ABSENT
when the embedder is down - the hash-geometric fallback is never
silently claimed as semantic (the door's falsifier); the recall floor
(the catalog census moment) is named in the report, not hidden.
"""
import pytest

import tools.query_broker as qb
from tools.query_broker import ask, embed_signal, fuse, fts_signal, lattice_signal


def _row(key, title="t", origin="fts", text=None):
    return {"key": key, "title": title, "origin": origin, "text": text or key}


# -- fusion ----------------------------------------------------------------


def test_rrf_arithmetic_exact():
    a = [_row("x"), _row("y"), _row("z")]           # ranks 1,2,3
    b = [_row("y"), _row("x")]                       # ranks 1,2
    out = fuse({"fts": a, "lattice": b}, k=3)
    # x: 1/(60+1) + 1/(60+2); y: 1/(60+2) + 1/(60+1); z: 1/(60+3)
    expect_x = 1 / 61 + 1 / 62
    expect_y = 1 / 62 + 1 / 61
    assert out[0]["key"] in ("x", "y")
    # the module rounds rrf to 6 places; tolerance covers that rounding
    assert out[0]["rrf"] == pytest.approx(max(expect_x, expect_y), abs=1e-6)
    by_key = {r["key"]: r for r in out}
    assert by_key["x"]["rrf"] == pytest.approx(expect_x, abs=1e-6)
    assert by_key["y"]["rrf"] == pytest.approx(expect_y, abs=1e-6)
    assert by_key["z"]["rrf"] == pytest.approx(1 / 63, abs=1e-6)
    assert by_key["x"]["ranks"] == {"fts": 1, "lattice": 2}


def test_missing_signal_contributes_nothing():
    out = fuse({"fts": [_row("only")]}, k=5)
    assert len(out) == 1
    assert out[0]["ranks"] == {"fts": 1}


# -- fts signal ------------------------------------------------------------


def test_fts_terms_normalized_and_one_char_dropped(monkeypatch):
    calls = {}

    def fake_corpus_search(query, limit=30):
        calls["query"] = query
        calls["limit"] = limit
        return {"hits": [{"id": "1", "path": "a/passatk.md", "title": "Pass"}],
                "engine": "scan", "index_state": "fresh"}

    monkeypatch.setattr(qb, "corpus_search", fake_corpus_search)
    rows, meta = fts_signal("pass@K coverage!", 8)
    assert calls["query"] == "pass coverage"  # @K split, 1-char dropped
    assert rows[0]["key"] == "a/passatk.md"
    assert meta["engine"] == "scan"


def test_fts_meta_names_the_recall_floor(monkeypatch):
    def fake_corpus_search(query, limit=30):
        return {"hits": [], "engine": "scan", "index_state": "stale",
                "map_asof": "2026-10-04T09:00:00Z", "map_age_hours": 26.0}

    monkeypatch.setattr(qb, "corpus_search", fake_corpus_search)
    _, meta = fts_signal("anything", 8)
    assert meta["map_asof"] == "2026-10-04T09:00:00Z"
    assert meta["map_age_hours"] == 26.0


# -- lattice signal --------------------------------------------------------


def test_lattice_overlap_only_and_deterministic():
    nodes = [
        {"id": "n1", "title": "hydrology wave map", "path": "memory/x.md"},
        {"id": "n2", "title": "unrelated theme", "path": "memory/y.md"},
        {"id": "n3", "title": "water hydrology graph", "path": "memory/z.md"},
    ]
    r1 = lattice_signal("hydrology water", 5, nodes=nodes)
    r2 = lattice_signal("hydrology water", 5, nodes=nodes)
    assert [x["key"] for x in r1] == [x["key"] for x in r2]  # deterministic
    assert r1[0]["key"] == "memory/z.md"  # 2/2 overlap beats 1/2
    assert all("memory/y.md" != x["key"] for x in r1)  # no overlap, no hit


def test_lattice_empty_query_or_nodes():
    assert lattice_signal("", 5, nodes=[]) == []
    assert lattice_signal("hydrology", 5, nodes=[]) == []


# -- embedding signal ------------------------------------------------------


def test_embed_absent_never_fallback(monkeypatch):
    rows, meta = embed_signal("q", [_row("a"), _row("b")], 5,
                              embedder=lambda t: None)
    assert rows == []
    assert meta["source"] == "absent"
    assert "no vector" in meta["note"]


def test_embed_absent_when_recall_empty():
    rows, meta = embed_signal("q", [], 5, embedder=lambda t: [1.0, 0.0])
    # candidates empty -> the only embedded text is the query: honest absent
    assert meta["source"] == "absent"


def test_embed_reranks_by_cosine():
    qv = [1.0, 0.0]
    vecs = {"the cat sat": [1.0, 0.0],        # aligned -> first
            "dogs bark loud": [0.0, 1.0],     # orthogonal -> last
            "cat mat flat": [0.9, 0.1]}       # close -> second

    def embedder(t):
        return vecs.get(t)

    cands = [_row("d1", text="dogs bark loud"), _row("c1", text="the cat sat"),
             _row("c2", text="cat mat flat")]
    rows, meta = embed_signal("the cat sat", cands, 3, embedder=embedder)
    assert [r["text"] for r in rows] == ["the cat sat", "cat mat flat", "dogs bark loud"]
    assert meta["source"].startswith("ollama:") or meta["source"] == "test"


# -- end to end ------------------------------------------------------------


def test_ask_fuses_two_signals_when_embedder_down(monkeypatch):
    monkeypatch.setattr(qb, "corpus_search", lambda q, limit=30: {
        "hits": [{"id": "1", "path": "docs/gwap.md", "title": "gwap"}],
        "engine": "scan", "index_state": "fresh"})
    nodes = [{"id": "n1", "title": "gwap agreement", "path": "docs/gwap.md"}]
    rep = ask("gwap", k=5,
              embedder=lambda t: None)  # ollama down
    assert rep["signals"]["embed"]["source"] == "absent"
    assert rep["signals"]["fts"]["hits"] == 1
    assert rep["rows"], "two-signal fusion must still answer"
    assert set(rep["rows"][0]["ranks"]) <= {"fts", "lattice"}
