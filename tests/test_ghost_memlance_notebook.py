"""Stateless tests for ghost_memlance notebook indexing — memlance can lance Jupyter notebooks.

No monkeypatch (operator correction): uses a synthetic .ipynb written to tmp_path (pytest fixture)
and asserts the pure index function produces a grounded, deterministic memory state.
"""
from __future__ import annotations

import json

from mag.ghost_memlance import _index_notebook, index


def _make_nb(path, title_md: str, code: str, output: str) -> None:
    nb = {"cells": [
        {"cell_type": "markdown", "source": [title_md]},
        {"cell_type": "code", "source": [code], "outputs": [{"text": [output]}]},
    ]}
    path.write_text(json.dumps(nb), encoding="utf-8")


def test_index_notebook_produces_state(tmp_path):
    p = tmp_path / "lanced.ipynb"
    _make_nb(p, "# Lanced Water Notebook\\n\\nthe swarm is water", "x = 1", "WATER-OK")
    st = _index_notebook(p)
    assert st is not None
    assert st["kind"] == "notebook"
    assert "Lanced Water Notebook" in st["title"]
    assert st["n_chars"] > 0
    assert "WATER-OK" in st["excerpt"]  # output is part of the lanced memory


def test_index_notebook_deterministic(tmp_path):
    p = tmp_path / "det.ipynb"
    _make_nb(p, "# Deterministic", "a = 1", "D1")
    assert _index_notebook(p)["title"] == _index_notebook(p)["title"]
    assert _index_notebook(p)["n_chars"] == _index_notebook(p)["n_chars"]


def test_index_includes_notebooks():
    """index() surfaces notebook memory states alongside the disk roots (deterministic)."""
    states = index(refresh=True)
    kinds = {s["kind"] for s in states}
    assert "notebook" in kinds
