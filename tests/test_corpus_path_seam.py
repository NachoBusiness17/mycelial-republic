"""Corpus search/get path-seam regression tests (B2-184, 2026-09-26).

Seam: mag/catalog_scan.py walks the PROJECTS dir (ROOT = projects, line 83),
so catalog rows and corpus_search hits carry the "local_sovereign_agent/"
prefix, while tools/corpus.py serves repo-relative only. Before the fix,
corpus_get(a search hit path) resolved a nonexistent nested path and refused.
The fix strips that exact prefix in _confine (both forms accepted, ids and
search output unchanged -- the catalog-id law derives ids from the STORED
relative path, so normalizing search output would break re-verification).

Falsifier under test: corpus_get(corpus_search hit path) returns ok:true.
"""
from __future__ import annotations

import json

from tools.corpus import _catalog_id, _confine, corpus_get, corpus_search

REPO_PREFIX = "local_sovereign_agent/"


def _first_real_hit_path():
    """A path exactly as corpus_search emits it, backed by a real file."""
    res = corpus_search("catalog")
    assert res["ok"], res
    for hit in res["hits"]:
        p = str(hit.get("path", ""))
        if p.startswith(REPO_PREFIX):
            return p
    # fall back to the map itself: first LSA-prefixed row with a live file
    with open("catalog/catalog.jsonl", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            if not line.strip():
                continue
            row = json.loads(line)
            p = str(row.get("path", ""))
            if p.startswith(REPO_PREFIX) and p.endswith(".py"):
                return p
    raise AssertionError("no LSA-prefixed catalog path with a live file found")


def test_confine_accepts_both_forms_to_same_file():
    a = _confine("tools/corpus.py")
    b = _confine(REPO_PREFIX + "tools/corpus.py")
    assert a is not None and b is not None
    assert a == b


def test_confine_still_refuses_escapes_and_absolutes():
    assert _confine("") is None
    assert _confine("C:\\Windows\\system32\\drivers\\etc\\hosts") is None
    assert _confine("../outside.txt") is None
    assert _confine(REPO_PREFIX) is None  # bare prefix strips to nothing
    # the escape check that matters: the parent traversal must not resolve
    # outside REPO after the strip
    assert _confine(REPO_PREFIX + "../../outside.txt") is None


def test_corpus_get_of_search_hit_path_returns_ok_true():
    hit_path = _first_real_hit_path()
    got = corpus_get(hit_path)
    assert got["ok"], got
    assert got["path"] == hit_path[len(REPO_PREFIX):]
    # self-consistency: the id is derived from the SERVED repo-relative path
    # (pre-existing corpus_get convention; NOTE it diverges from the scanner's
    # projects-relative id for the same file -- observed, not fixed here,
    # outside the B2-184 path seam)
    assert got["catalog_id"] == _catalog_id(got["path"])


def test_search_hit_end_to_end_roundtrip():
    res = corpus_search("catalog_scan")
    assert res["ok"], res
    hit = next((h for h in res["hits"]
                if str(h.get("path", "")).startswith(REPO_PREFIX)), None)
    if hit is None:
        import pytest
        pytest.skip("no LSA-prefixed hit for this query in the current map")
    got = corpus_get(hit["path"])
    assert got["ok"], got
    assert got["bytes_served"] > 0
