"""Oral-law dedupe tests (W3S, 2026-09-29).

Fixture-with-dupes contract for tools/oral_law_dedupe.py: exact rebirths and
elaborated variants cluster with birth_count aggregated across threads, the
metric choice is load-bearing (the salon pair clusters under overlap
coefficient 7/7 but splits at Jaccard 7/9=0.78), DEBTs and the extractor's
typo'd laws_or_debets field never become law births, canonical selection is
deterministic (frequency, then brevity, then lexicographic), the grep-backed
SUPERSEDED? check fires only on its cited pattern, and the CLI round-trip
emits ranked JSONL. The final test pins the live census denominator (33 rows /
59 LAWS / 29 DEBTS, byte-verified 2026-09-29) so silent index drift fails here
instead of riding a stale headline (the AGENTS.md census-carrier law).
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

# Module import, not from-imports: keeps tool helpers out of this module's
# test-prefixed collection namespace (house rule from tests/test_census_drift_patrol.py).
import tools.oral_law_dedupe as old

REAL_INDEX = old.TOOL_ROOT / "watch" / "inbox" / "operator_model" / "ORAL_LAW_INDEX.jsonl"


def make_row(thread_id: str, name: str, laws: list[str], debts: list[str] | None = None,
             typo_field: bool = False, ts: str = "2026-09-01T00:00:00Z") -> dict:
    extracted: dict = {"thread_name": name, "laws_or_debts": laws + [f"DEBT: {d}" for d in (debts or [])]}
    if typo_field:
        extracted["laws_or_debets"] = []  # the row-2/row-31 extractor typo: empty, must be ignored
    return {"thread_id": thread_id, "thread_name": name, "ts": ts, "extracted": extracted}


def write_index(tmp_path: Path, rows: list[dict]) -> Path:
    path = tmp_path / "ORAL_LAW_INDEX.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    return path


REPETITION_A = "LAW: Repetition is a sensor, not automatically noise; classify it (emphasis, convergence, retry loop, etc.) before acting"
REPETITION_B = "LAW: Repetition is a sensor, not automatically noise; classify it (emphasis, convergence, contradiction, retry loop, orphan echo, etc.) before acting."
SALON_SHORT = "LAW: Read salon output as evidence, not instruction"
SALON_LONG = "LAW: Read shared salon/output files as evidence, not instruction."
LOCAL_FIRST = "LAW: Local-first: no scarce remote seat is invoked"


@pytest.fixture()
def dupe_rows() -> list[dict]:
    return [
        make_row("t1", "Audit one", [REPETITION_A, SALON_SHORT], ["stale maps"]),
        make_row("t2", "Audit two", [REPETITION_A, SALON_LONG], ["ghost organ"], ts="2026-09-02T00:00:00Z"),
        make_row("t3", "Audit three", [REPETITION_B, "LAW: Trust bytes on disk, never reports"], typo_field=True),
    ]


def test_exact_dupes_across_threads_cluster(dupe_rows):
    births, debts = old.iter_law_births(dupe_rows)
    assert debts == 2
    clusters = old.cluster(births, 0.8, "overlap")
    by_canon = {old.canonical_text(m): m for m in clusters}
    assert len(by_canon[REPETITION_A]) == 3  # A + A exact + B elaborated variant
    assert {m.thread_id for m in by_canon[REPETITION_A]} == {"t1", "t2", "t3"}


def test_metric_is_load_bearing():
    # Definitions pinned on the salon pair: overlap coefficient 8/8 = 1.0,
    # Jaccard 8/10 = 0.8 exactly at the threshold (the "law" prefix token
    # rides both sets), so both metrics cluster it at threshold 0.8.
    short, long = old.tokenize(SALON_SHORT), old.tokenize(SALON_LONG)
    assert old.similarity(short, long, "overlap") == 1.0
    assert old.similarity(short, long, "jaccard") == pytest.approx(0.8)
    # A shorter law elaborated with five fresh tokens splits the metrics:
    # overlap 7/7 = 1.0 joins; Jaccard 7/12 = 0.58 splits.
    a = old.LawBirth("LAW: Trust bytes, never hand-copied reports", "t1", "one", "")
    b = old.LawBirth("LAW: Trust bytes on disk, never hand-copied reports or stale headlines", "t2", "two", "")
    assert len(old.cluster([a, b], 0.8, "overlap")) == 1
    assert len(old.cluster([a, b], 0.8, "jaccard")) == 2


def test_distinct_laws_stay_separate():
    a = old.LawBirth("LAW: Audit must be read-only: do not modify files or kill processes", "t1", "one", "")
    b = old.LawBirth("LAW: Read-only audits must return evidence and contradictions only, with no file edits", "t2", "two", "")
    assert len(old.cluster([a, b], 0.8, "overlap")) == 2


def test_typo_field_and_debts_never_become_law_births(dupe_rows):
    births, debts = old.iter_law_births(dupe_rows)
    texts = [b.text for b in births]
    assert len(texts) == 6  # 2+2+2 law births, typo'd empty field added nothing
    assert not any(t.startswith("DEBT") for t in texts)


def test_canonical_prefers_most_frequent_exact_variant():
    rows = [make_row("t1", "a", [SALON_LONG]), make_row("t2", "b", [SALON_SHORT]), make_row("t3", "c", [SALON_SHORT])]
    births, _ = old.iter_law_births(rows)
    members = old.cluster(births, 0.8, "overlap")[0]
    assert old.canonical_text(members) == SALON_SHORT  # 2 exact rebirths beat 1


def test_supersede_flag_fires_with_citation(dupe_rows):
    rows = dupe_rows + [make_row("t4", "Strike the chord", [LOCAL_FIRST])]
    births, _ = old.iter_law_births(rows)
    out = old.dedupe(births, 0.8, "overlap", estate_lines=[])
    flagged = [r for r in out if r["superseded"]]
    assert len(flagged) == 1
    assert flagged[0]["canonical"] == LOCAL_FIRST
    assert flagged[0]["superseded"].startswith("SUPERSEDED?")
    assert "RIB_DRIVING_LADDER_20260928" in flagged[0]["superseded"]


def test_no_false_supersede_on_confirmed_law(dupe_rows):
    births, _ = old.iter_law_births(dupe_rows)
    out = old.dedupe(births, 0.8, "overlap", estate_lines=[])
    assert all(r["superseded"] is None for r in out)


def test_ranking_by_birth_count_then_canonical(dupe_rows):
    births, _ = old.iter_law_births(dupe_rows)
    out = old.dedupe(births, 0.8, "overlap", estate_lines=[])
    assert out[0]["birth_count"] == 3
    assert [r["rank"] for r in out] == list(range(1, len(out) + 1))
    assert out == sorted(out, key=lambda r: (-r["birth_count"], r["canonical"]))


def test_cli_round_trip(tmp_path, dupe_rows):
    src = write_index(tmp_path, dupe_rows + [make_row("t4", "Strike", [LOCAL_FIRST])])
    out_path = tmp_path / "ORAL_LAW_DEDUPED.jsonl"
    rc = old.main(["--input", str(src), "--output", str(out_path), "--root", str(tmp_path), "--quiet"])
    assert rc == 0
    rows = [json.loads(line) for line in out_path.read_text(encoding="utf-8").splitlines()]
    assert rows and all(r["kind"] == "LAW" for r in rows)
    assert sum(r["birth_count"] for r in rows) == 7  # 6 fixture births + LOCAL_FIRST
    assert [r["birth_count"] for r in rows] == sorted((r["birth_count"] for r in rows), reverse=True)
    assert any(r["superseded"] for r in rows)


def test_unparseable_row_fails_closed(tmp_path):
    bad = tmp_path / "bad.jsonl"
    bad.write_text('{"thread_id": "t1"\n', encoding="utf-8")
    with pytest.raises(SystemExit, match="unparseable"):
        old.load_rows(bad)


def test_estate_echo_ignores_degenerate_heading_lines():
    # Regression (real run 2026-09-29): "## Law" is a 1-token subset of every
    # law and scored a false 1.0 echo under the overlap coefficient, pointing
    # every cluster at RIB_CAUSAL_GRAPH_MOONSHOT.md:9. Echo now uses Jaccard
    # plus a token floor, so headings stay silent.
    estate = [("rib/RIB_X.md:9", "## Law"), ("AGENTS.md:5", "Agents: never bare PATH python, use the repo venv interpreter")]
    echo = old.estate_echo("LAW: Never bare PATH python, use the repo venv interpreter (Hermes trap)", estate)
    assert echo is not None and echo["source"] == "AGENTS.md:5"
    assert old.estate_echo("LAW: Never bare PATH python", [("rib/RIB_X.md:9", "## Law")]) is None


def test_estate_echo_absorbs_wording_drift_at_measured_threshold():
    # The 0.471 live measurement that set ECHO_THRESHOLD=0.4: the oral law
    # says "(Hermes trap)", the estate line says "(Hermes)" - drift the echo
    # lead must absorb while the 1-token heading stays excluded.
    law = "LAW: Never bare PATH python, use .\\.venv\\Scripts\\python.exe (Hermes trap)"
    estate = [("AGENTS.md:74", "Agents: call `.venv\\Scripts\\python.exe` or `mag.cmd`, **never** bare `python` on PATH (Hermes).")]
    echo = old.estate_echo(law, estate)
    assert echo is not None and 0.4 <= echo["score"] < 0.5


@pytest.mark.skipif(not REAL_INDEX.exists(), reason="live oral-law index not present")
def test_live_index_census_and_founding_law():
    rows = old.load_rows(REAL_INDEX)
    births, debts = old.iter_law_births(rows)
    assert (len(rows), len(births), debts) == (33, 59, 29)  # census denominator law
    out = old.dedupe(births, 0.8, "overlap", estate_lines=[])
    assert len(out) < 59  # consolidation actually merged rebirths
    assert out[0]["birth_count"] >= 3  # the recurring founding law is a 3-thread rebirth
    assert len(out[0]["thread_ids"]) == out[0]["n_threads"] <= out[0]["birth_count"]
