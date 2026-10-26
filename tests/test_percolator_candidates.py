"""--candidates ingest (fillball-1001, 2026-10-01) - mine rows reach the review pass.

GAP_REGISTER rank 6 (a02-r2): the olm mine's percolator_candidates.jsonl rows had
ZERO consumers (grep mag/ tools/ tests/ = 0 hits before this file). The read path
added to mag/percolator.py ingests them as CANDIDATES into
memory/percolator/candidates.jsonl with promoted=False.

Laws under test:
  1. a real mine candidate (row bytes from watch/inbox/frontier_olm_2026-10-01/)
     reaches the review pass with its real source_url attached;
  2. THE PROMOTE GATE STAYS ALPHA-BUDGET: ingestion never writes
     invariants.json or explore.jsonl, no matter how signal-heavy the claim;
  3. noise/theater in a claim still strips to the noise file (pipeline shape kept);
  4. a rerun over the same file is idempotent (no duplicate candidate rows);
  5. glob expansion works and a no-match pattern fails honestly (ok=False).

Every test runs against a tmp_path world (registry/seals/noise/explore/candidates/
config all redirected; fact_bus + destructive_receipt stubbed) - the live
memory/percolator tree is never touched, same discipline as test_percolator_z15.py.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from mag import percolator

REAL_MINE_FILE = (percolator.ROOT / "watch" / "inbox" / "frontier_olm_2026-10-01"
                  / "percolator_candidates.jsonl")
SIGNAL_CLAIM = ("the invariant procedure: we built a mechanism that folds the "
                "training signal, the map precedes the territory")
NOISE_CLAIM = "follow me and subscribe, like and share, win a giveaway, click the link"


@pytest.fixture
def world(tmp_path, monkeypatch):
    """Isolated percolator world; restores every patched module path on teardown."""
    monkeypatch.setattr(percolator, "INVARIANT_REGISTRY", tmp_path / "invariants.json")
    monkeypatch.setattr(percolator, "SEALS_DIR", tmp_path / "seals")
    monkeypatch.setattr(percolator, "NOISE_DIR", tmp_path / "noise")
    monkeypatch.setattr(percolator, "EXPLORE_QUEUE", tmp_path / "explore.jsonl")
    monkeypatch.setattr(percolator, "CANDIDATES_REVIEW", tmp_path / "candidates.jsonl")
    monkeypatch.setattr(percolator, "PERCOLATOR_CFG", tmp_path / "percolator.json")
    monkeypatch.setattr(percolator, "_cfg_cache",
                        {"mtime": None, "data": dict(percolator._CFG_DEFAULTS)})
    monkeypatch.setattr("mag.fact_bus.publish_fact",
                        lambda *a, **k: {"ok": True, "stub": True})
    monkeypatch.setattr("mag.destructive_receipt.record",
                        lambda *a, **k: {"ok": True, "stub": True})
    return tmp_path


def _write_mine_file(tmp_path: Path, rows: list[dict]) -> Path:
    p = tmp_path / "percolator_candidates.jsonl"
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows),
                 encoding="utf-8")
    return p


def _read_review(world: Path) -> list[dict]:
    if not percolator.CANDIDATES_REVIEW.is_file():
        return []
    return [json.loads(l) for l in
            percolator.CANDIDATES_REVIEW.read_text(encoding="utf-8").splitlines() if l.strip()]


# ── law 1: a REAL mine candidate reaches the review pass ─────────────────────

@pytest.mark.skipif(not REAL_MINE_FILE.is_file(),
                    reason="real mine file not on disk: watch/inbox/frontier_olm_2026-10-01/")
def test_real_mine_candidate_reaches_review_pass(world, monkeypatch):
    """One real row from the 2026-10-01 olm mine digest lands in the review pass
    with status candidate and its real source_url - and promotes nothing."""
    real_rows = [json.loads(l) for l in
                 REAL_MINE_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert real_rows, "real mine file exists but parsed to zero rows"
    row = real_rows[0]
    rel = str(REAL_MINE_FILE.relative_to(percolator.ROOT)).replace("\\", "/")
    res = percolator.ingest_candidates([str(REAL_MINE_FILE)])
    assert res["ok"] is True
    assert res["n_rows"] == len(real_rows)
    assert res["n_candidate"] >= 1
    assert res["n_promoted"] == 0
    assert "alpha-budget" in res["promote_gate"]
    review = _read_review(world)
    hits = [r for r in review if r["file"] == rel and r["source"] == row["source_url"]]
    assert hits, f"no review row carries the real source_url {row['source_url']!r}"
    top = hits[0]
    assert top["status"] == "candidate"
    assert top["promoted"] is False
    assert top["claim"] == row["claim"][:600]          # the real claim bytes, bounded
    assert top["canonical"] == percolator._canonical_hex(
        [s["sentence"] for s in percolator.partition(row["claim"])["signal"]])


# ── law 2: the promote gate stays alpha-budget (never auto-promote) ──────────

def test_ingest_never_writes_invariants_or_explore(world):
    """A maximally signal-heavy claim still cannot compile an invariant from the
    ingest path: invariants.json and explore.jsonl must not even come to exist."""
    p = _write_mine_file(world, [{"claim": SIGNAL_CLAIM, "source_url": "https://x.test/1",
                                  "estate_map": "mag/percolator.py", "probe": "unit"}])
    res = percolator.ingest_candidates([str(p)])
    assert res["ok"] is True and res["n_candidate"] == 1
    assert res["n_promoted"] == 0
    assert not (world / "invariants.json").exists(), "ingest compiled an invariant"
    assert not (world / "explore.jsonl").exists(), "ingest wrote an explore row"
    assert _read_review(world)[0]["n_signal"] >= 1      # signal WAS detected and filed


# ── law 3: noise still strips to the noise file ──────────────────────────────

def test_noise_claim_strips_and_files_no_signal(world):
    p = _write_mine_file(world, [{"claim": NOISE_CLAIM, "source_url": "https://x.test/2"}])
    res = percolator.ingest_candidates([str(p)])
    assert res["ok"] is True
    assert res["n_stripped_sentences"] >= 1
    assert res["n_candidate"] == 1                       # still reviewable, as a candidate
    review = _read_review(world)
    assert review[0]["n_signal"] == 0 and review[0]["signal"] == ""
    noise_rows = [json.loads(l) for l in
                  (world / "noise" / "frontier_mine.jsonl").read_text(
                      encoding="utf-8").splitlines() if l.strip()]
    assert noise_rows, "stripped noise never reached the noise file"


def test_empty_claim_counts_as_no_signal(world):
    p = _write_mine_file(world, [{"source_url": "https://x.test/3"},
                                 {"claim": "   ", "source_url": "https://x.test/4"}])
    res = percolator.ingest_candidates([str(p)])
    assert res["ok"] is True and res["n_rows"] == 2 and res["n_no_signal"] == 2
    assert res["n_candidate"] == 0
    assert _read_review(world) == []


# ── law 4: rerun idempotence ─────────────────────────────────────────────────

def test_rerun_is_idempotent(world):
    p = _write_mine_file(world, [{"claim": SIGNAL_CLAIM, "source_url": "https://x.test/5",
                                  "area": "ctx", "card_path": "cards/a.md"}])
    first = percolator.ingest_candidates([str(p)])
    assert first["n_candidate"] == 1 and first["n_dupe"] == 0
    second = percolator.ingest_candidates([str(p)])
    assert second["n_candidate"] == 0 and second["n_dupe"] == 1
    assert second["n_stripped_sentences"] == 0           # rerun strips nothing new
    assert len(_read_review(world)) == 1                 # no duplicate row landed
    carried = _read_review(world)[0]
    assert carried["area"] == "ctx" and carried["card_path"] == "cards/a.md"


def test_rerun_does_not_double_strip_noise(world):
    """Caught live (fillball-1001): dedupe ran AFTER append_noise, so an
    idempotence rerun doubled the domain noise file."""
    p = _write_mine_file(world, [{"claim": NOISE_CLAIM, "source_url": "https://x.test/9"}])
    noise_file = world / "noise" / "frontier_mine.jsonl"
    percolator.ingest_candidates([str(p)])
    n_first = len(noise_file.read_text(encoding="utf-8").splitlines())
    assert n_first >= 1
    percolator.ingest_candidates([str(p)])               # pure dedupe pass
    n_after = len(noise_file.read_text(encoding="utf-8").splitlines())
    assert n_after == n_first, f"rerun grew the noise file {n_first} -> {n_after}"


# ── law 5: glob expansion + honest no-match failure ──────────────────────────

def test_glob_expansion_and_unmatched_pattern(world):
    _write_mine_file(world, [{"claim": SIGNAL_CLAIM, "source_url": "https://x.test/6"}])
    (world / "mine_b").mkdir()
    _write_mine_file(world / "mine_b",
                     [{"claim": NOISE_CLAIM, "source_url": "https://x.test/7"}])
    res = percolator.ingest_candidates([str(world / "percolator_candidates.jsonl"),
                                        str(world / "mine_b" / "*.jsonl"),
                                        str(world / "no_such_dir" / "*.jsonl")])
    assert res["ok"] is True and res["n_files"] == 2
    assert res["unmatched"] == [str(world / "no_such_dir" / "*.jsonl")]
    assert res["n_candidate"] == 2


def test_no_match_fails_honestly(world):
    res = percolator.ingest_candidates([str(world / "nothing_here.jsonl")])
    assert res["ok"] is False
    assert "no candidates files matched" in res["error"]
    assert res["unmatched"] == [str(world / "nothing_here.jsonl")]


def test_relative_path_yields_forward_slash_repo_relative_file_field(world):
    """The production CLI shape is a relative glob run from the repo root; the
    review row's 'file' must come out forward-slash repo-relative (the rerun
    dedupe key depends on the exact string; a native-separator leak would
    duplicate every row on rerun)."""
    p = _write_mine_file(world, [{"claim": SIGNAL_CLAIM, "source_url": "https://x.test/8"}])
    rel = str(p.relative_to(percolator.ROOT)).replace("\\", "/")
    res = percolator.ingest_candidates([rel])
    assert res["ok"] is True and res["n_candidate"] == 1
    row = _read_review(world)[0]
    assert row["file"] == rel
    assert "\\" not in row["file"]
