"""dirac bank receipt-binding tests (register row 6, 2026-10-05).

The bank verb is the destructive ledger act on watch/inbox/
DIRAC_BANKED_INVARIANTS.jsonl: a banked invariant ends a gap's status
forever (scan() honors it as closed_solved). Adopting the RECEIPT_BINDINGS
shape from tools/queue_close.py (watch/inbox/QUEUE_CLOSE_VERB_20260927.md),
the proving receipt resolves ONLY from the literal table in mag/dirac_loop.py
and the runtime can never supply a path. These tests pin the refusals:

  - a runtime --receipt path (registered or not) is an unrecognized argument
    and argparse refuses the invocation with exit 2;
  - an edge with no RECEIPT_BINDINGS entry refuses (unbound-edge);
  - a bound receipt that does not byte-exist refuses (receipt-missing);
  - a successful bank resolves the receipt ONLY from the table and refuses
    a second bank of the same invariant (already-banked).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mag.dirac_loop as dl  # noqa: E402

EDGE = "organ:test_a->organ:test_b"


def _synthetic_loops() -> dict:
    return {"loops": [{"edge": EDGE, "labels": ["test_a", "test_b"]}]}


def test_runtime_receipt_path_is_refused_by_argparse(capsys):
    """The headline law: an unregistered path handed to the verb at runtime
    cannot reach bank() at all. There is no --receipt argument; argparse
    treats the path as an unrecognized argument and exits 2."""
    with pytest.raises(SystemExit) as ei:
        dl.main(["bank", "--edge", EDGE,
                 "--receipt", "watch/inbox/UNREGISTERED_EVIDENCE_PATH.md"])
    assert ei.value.code == 2, "a runtime-supplied receipt path must refuse exit 2"
    err = capsys.readouterr().err
    assert "--receipt" in err, "refusal must name the rejected argument"


def test_cli_unbound_edge_refuses_exit_2():
    """An edge with no binding has no evidence; the verb refuses, exit 2,
    nothing appended (the queue_close 'no binding, no close' law)."""
    before = dl.BANKED_FILE.read_text(encoding="utf-8") if dl.BANKED_FILE.is_file() else ""
    rc = dl.main(["bank", "--edge", "organ:never_bound->organ:also_never"])
    assert rc == 2, "unbound edge must exit 2"
    after = dl.BANKED_FILE.read_text(encoding="utf-8") if dl.BANKED_FILE.is_file() else ""
    assert before == after, "a refused bank must not touch the ledger"


def test_bank_unbound_edge_refusal_shape():
    res = dl.bank("organ:never_bound->organ:also_never")
    assert res["ok"] is False
    assert res["refusal"] == "unbound-edge"
    assert "RECEIPT_BINDINGS" in res["error"]


def test_bank_bound_receipt_missing_bytes_refuses(tmp_path, monkeypatch):
    """A registered receipt that does not byte-exist refuses (receipt-missing):
    the binding table names real files only."""
    monkeypatch.setattr(dl, "RECEIPT_BINDINGS",
                        {EDGE: "watch/inbox/__NO_SUCH_EVIDENCE_FILE__.md"})
    monkeypatch.setattr(dl, "BANKED_FILE", tmp_path / "BANKED.jsonl")
    res = dl.bank(EDGE)
    assert res["ok"] is False
    assert res["refusal"] == "receipt-missing"
    assert not (tmp_path / "BANKED.jsonl").exists(), "refused bank writes nothing"


def test_bank_resolves_evidence_only_from_the_table(tmp_path, monkeypatch):
    """Happy path under the binding law: the receipt written into the ledger
    is exactly the literal bound path; no runtime value can inject anything."""
    evidence = tmp_path / "evidence" / "proof.md"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("proof bytes\n", encoding="utf-8")
    rel = "evidence/proof.md"
    monkeypatch.setattr(dl, "ROOT", tmp_path)
    monkeypatch.setattr(dl, "RECEIPT_BINDINGS", {EDGE: rel})
    monkeypatch.setattr(dl, "BANKED_FILE", tmp_path / "BANKED.jsonl")
    monkeypatch.setattr(dl, "fundamental_cycles", _synthetic_loops)

    res = dl.bank(EDGE, seat="lane-e07")
    assert res["ok"] is True
    row = res["banked"]
    assert row["receipt"] == rel, "ledger receipt must be the literal bound path"
    assert row["edge"] == EDGE and row["seat"] == "lane-e07"
    ledger_rows = [json.loads(l) for l in
                   (tmp_path / "BANKED.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(ledger_rows) == 1 and ledger_rows[0]["receipt"] == rel


def test_double_bank_refused(tmp_path, monkeypatch):
    """The queue_close status-guard analog: banking an invariant that is
    already in the ledger refuses (already-banked), never mints a second
    close row from the same evidence."""
    evidence = tmp_path / "evidence" / "proof.md"
    evidence.parent.mkdir(parents=True)
    evidence.write_text("proof bytes\n", encoding="utf-8")
    monkeypatch.setattr(dl, "ROOT", tmp_path)
    monkeypatch.setattr(dl, "RECEIPT_BINDINGS", {EDGE: "evidence/proof.md"})
    monkeypatch.setattr(dl, "BANKED_FILE", tmp_path / "BANKED.jsonl")
    monkeypatch.setattr(dl, "fundamental_cycles", _synthetic_loops)

    first = dl.bank(EDGE)
    assert first["ok"] is True
    second = dl.bank(EDGE)
    assert second["ok"] is False
    assert second["refusal"] == "already-banked"
    ledger_lines = [l for l in
                    (tmp_path / "BANKED.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(ledger_lines) == 1, "the refused second bank appended nothing"


def test_seeded_bindings_byte_exist():
    """The table's seed entries are literal real files on disk (the law the
    verb enforces must hold for the table the verb ships with)."""
    for edge, rel in dl.RECEIPT_BINDINGS.items():
        p = dl.ROOT.joinpath(*rel.split("/"))
        assert p.is_file(), f"seed binding for {edge} does not byte-exist: {p}"
