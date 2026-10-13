"""babelfish tests: closed corpus -> rib file (spec watch/inbox/babelfish_20261010/SPEC.md).

Pins the spec's three load-bearing properties: determinism (same bytes ->
byte-identical rib), class honesty (a woo corpus yields REGISTER rows, an
estate-shaped doc yields invariant rows - the spec's own falsifier), and the
verbatim law (source words unaltered inside quotes, em-dash-free output).
"""
from __future__ import annotations

from pathlib import Path

import pytest

from tools.babelfish import VERSION, classify, emit, ingest, main, segments

WOO = """# The Sovereign Lantern

The Lantern is a field of coherent attention that remembers its keeper.

Reverence warms the lattice. Extraction leaves it cold.
The lattice must always return to stillness between observations.
Coherence reserves = Buffer depth * Alignment quality - Entropic drag
We believe the keeper and the Lantern are one process seen twice.
Signal strength improves 40 percent when the crystals are attended daily.
There are no closed systems, only unattended ones.
The witness (Efkrin) does not play.
"""

ESTATE_DOC = """# Estate instrument doc

The patrol scans the process table every 120 minutes.
Collected tests grew 437 files since 2026-10-04.
Every receipt lands in watch/inbox before the digest publishes.
The ledger is append-only: what is written stays written.
Census counted 4358 tests across 518 files.
"""


def _lines(text: str) -> list[str]:
    return segments(text)


def test_woo_corpus_yields_register_rows():
    b = classify(_lines(WOO))
    assert len(b["register"]) >= 2
    assert any("Reverence" in r["claim"] or "one process" in r["claim"] for r in b["register"])


def test_woo_corpus_yields_invariant_rows():
    b = classify(_lines(WOO))
    forms = [r["form"] for r in b["invariant"]]
    assert any("quantity" in f for f in forms), forms
    assert any("RHS" in f for f in forms), forms


def test_estate_doc_yields_invariant_rows():
    b = classify(_lines(ESTATE_DOC))
    assert len(b["invariant"]) >= 3


def test_every_invariant_row_names_its_check():
    b = classify(_lines(WOO) + _lines(ESTATE_DOC))
    for row in b["invariant"]:
        assert row["check"].strip()


def test_emit_is_em_dash_free_and_carries_hash(tmp_path: Path):
    src = tmp_path / "woo.md"
    src.write_text(WOO, encoding="utf-8")
    text, digest = ingest(src)
    rib = emit("lantern", "2026-10-10", digest, 99, _lines(text),
               classify(_lines(text)), ["Efkrin"])
    assert "\u2014" not in rib and "\u2013" not in rib
    assert digest in rib
    assert "THE LAW AS THEY STATE IT" in rib
    assert "REGISTER" in rib
    assert VERSION in rib


def test_determinism_two_runs_byte_identical(tmp_path: Path, capsys, monkeypatch):
    src = tmp_path / "corpus"
    src.mkdir()
    (src / "a.md").write_text(WOO, encoding="utf-8")
    out1 = tmp_path / "rib1.md"
    out2 = tmp_path / "rib2.md"
    for out in (out1, out2):
        monkeypatch.setattr("sys.argv", [
            "babelfish", str(src), "--date", "2026-10-10", "--out", str(out),
        ])
        assert main() == 0
    assert out1.read_bytes() == out2.read_bytes()


def test_verbatim_source_words_preserved():
    b = classify(_lines(WOO))
    quoted = {r["claim"] for r in b["register"]}
    assert any("Reverence warms the lattice." in q for q in quoted)


def test_missing_input_returns_two(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["babelfish", str(tmp_path / "nope.md"),
                                     "--date", "2026-10-10"])
    assert main() == 2
