"""D6 regression: monoculture agreement-rate proxy adapter.

The door (eleven-doors D6): import the roshomon primitives + reimplement
the grouping loop; NEVER compare() (k8s-welded). The falsifier made law:
at 0.55 the long-form chapters can group all-or-nothing, killing the
estimate - so the adapter sweeps thresholds and reports UNMEASURABLE
honestly when degenerate. These tests pin: the mass case, the disjoint
case, the measurable middle, the grouping semantics, and the
attention-alert contract on core-size drop.
"""
import json

import pytest

import tools.monoculture_proxy as mp
from tools.monoculture_proxy import measure, record


def test_identical_witnesses_are_unmeasurable_mass():
    text = ("The verkle tip anchors every proof. Receipts land before claims. "
            "Trust bytes, not reports. The chain verifies the file.") * 3
    report = measure({"a": text, "b": text, "c": text})
    assert report["n_statements"] >= 10
    assert report["measurable"] is False
    assert report["unmeasurable_reason"] == "single-group dominance at every threshold"


def test_disjoint_witnesses_are_unmeasurable_zero_core():
    # no statement recurs across witnesses at any threshold
    a = " ".join(f"alpha topic {i} entirely distinct content {i}." for i in range(12))
    b = " ".join(f"beta theme {i} wholly other material {i}." for i in range(12))
    c = " ".join(f"gamma thread {i} separate again {i}." for i in range(12))
    report = measure({"a": a, "b": b, "c": c})
    assert report["measurable"] is False
    assert report["unmeasurable_reason"] == "zero-core at every threshold"


def test_partial_overlap_is_measurable_with_core():
    shared = ("The chain tip anchors the proof bytes. Receipts land before any claim is made. "
              "The verkle knot compacts history without losing lineage.")
    a = shared + (" Lane alpha also reports its own distinct finding here today. "
                  "Alpha keeps a private ledger row for its second observation. "
                  "A third alpha-only note closes the surface.")
    b = shared + (" Lane beta separately notes an unrelated second observation. "
                  "Beta writes its own material only for this line. "
                  "Another beta private note lands now.")
    c = ("Lane gamma only reports its own private material with no overlap at all. "
         "Gamma second statement stays fully distinct. Third gamma line diverges. "
         "Fourth gamma statement also unique. Fifth gamma statement ends it.")
    report = measure({"a": a, "b": b, "c": c})
    assert report["n_statements"] >= 10
    assert report["measurable"] is True
    t055 = report["per_threshold"]["0.55"]
    assert t055["core_groups"] >= 1
    assert 0.0 < t055["agreement_proxy"] < 1.0


def test_grouping_joins_on_overlap_not_identity():
    # the reimplemented loop matches the roshomon semantics: a statement
    # joins the first group whose representative overlaps >= threshold
    stmts = [["the verkle tip anchors proofs"], ["the verkle tip anchors the proof"]]
    groups = mp._group_witness_statements(stmts, 0.55)
    assert len(groups) == 1
    assert groups[0][1] == {0, 1}  # both witnesses in one core group


def test_record_appends_history_and_alerts_on_drop(tmp_path, monkeypatch):
    hist = tmp_path / "history.jsonl"
    att = tmp_path / "attention.md"
    monkeypatch.setattr(mp, "HISTORY", hist)
    monkeypatch.setattr(mp, "ATTENTION", att)
    shared = "The chain tip anchors the proof bytes. Receipts land before any claim is made."
    r1 = measure({"a": shared + " extra one.", "b": shared + " extra two.",
                  "c": "private material only, entirely other."})
    row1 = record(r1, label="test", alert=True)
    assert row1["prev_core_statements_055"] is None
    assert row1["alerted_attention"] is False  # first row: baseline, no alert
    assert not att.exists()
    # a corpus with a smaller core next run -> alert fires
    thin = "Barely any shared statement now at all. Only one line overlaps prior text."
    r2 = measure({"a": thin, "b": thin + " extra.", "c": "all different words here today."})
    row2 = record(r2, label="test", alert=True)
    assert row2["alerted_attention"] == (row2["core_statements_055"] < row1["core_statements_055"])
    if row2["alerted_attention"]:
        assert "core-size drop" in att.read_text(encoding="utf-8")
    # history has both rows
    rows = [json.loads(l) for l in hist.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert [r["label"] for r in rows] == ["test", "test"]


def test_record_no_alert_on_rise_or_equal(tmp_path, monkeypatch):
    hist = tmp_path / "history.jsonl"
    att = tmp_path / "attention.md"
    monkeypatch.setattr(mp, "HISTORY", hist)
    monkeypatch.setattr(mp, "ATTENTION", att)
    thin = "One shared line only today. Everything else diverges completely here."
    rich = ("The chain tip anchors the proof bytes. Receipts land before any claim. "
            "Trust bytes not reports. The sweep reads sensitivity honestly. "
            "Another recurring line across witnesses. And one more for the core.")
    r1 = measure({"a": thin, "b": thin + " x.", "c": "unrelated words entirely."})
    record(r1, label="rise", alert=True)
    r2 = measure({"a": rich, "b": rich + " y.", "c": rich + " z."})
    row2 = record(r2, label="rise", alert=True)
    assert row2["alerted_attention"] is False  # core grew
    assert not att.exists()
