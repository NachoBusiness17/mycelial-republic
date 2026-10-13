"""tests/test_b8_v2_preconds.py — B8 (2026-09-30), the reader half of the
VERKLE_V2_DECISION.md §2.2/§4 preconditions for the operator v2 flip.

The decision memo names the rows!=sessions drift family: under chain_mode=v2
(append-leaves) one session spans multiple chain rows and analytics readers
silently change meaning (none fail loudly). These tests pin the minimal
latest-per-session resolution landed in each of the three named readers:

  - mag/cache_map.py        — the time-window join + session counts read the
                              session's LATEST row only; a stale earlier row's
                              window must not shadow it or double-count.
  - mag/gene_pool_feeder.py — the aud_verkles seam resolves the rows-vs-sessions
                              BASIS (distinct_session_ids), flags append_mode,
                              and names both denominators in gene texts.
  - mag/knot_untangle.py    — the near-duplicate scan clusters the LATEST row
                              per session; a session's own seq history must
                              never read as "tangled".

v1 law (unchanged behavior): on chains with one row per session every
resolution is the identity — pinned here too, because the flip has not
happened (configs/mag.yaml chain_mode stays v1 until the operator window).

Spec: watch/inbox/VERKLE_V2_DECISION.md + watch/inbox/last_mile_20260930/B8_V2_PRECONDS.md
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag import cache_map  # noqa: E402
from mag import gene_pool_feeder as gpf  # noqa: E402
from mag import knot_untangle as ku  # noqa: E402


def _usage(ts: str, prompt: int) -> dict:
    return {"ts": ts, "provider": "deepseek", "ok": True,
            "prompt_tokens": prompt, "completion_tokens": 1}


# ── cache_map: window join reads the session's LATEST row ────────────────────

def test_cache_map_resolves_multirow_sessions_to_latest() -> None:
    chain_rows = [
        # session A stale seq-1 row: old theme + old window
        {"session_id": "sess-a", "session_seq": 1, "chain_mode": "v2",
         "start_minute": "2026-09-30T10:00:00Z", "end_minute": "2026-09-30T10:30:00Z",
         "dominant_theme": "old_theme"},
        # session A LATEST seq-2 row: new theme + later window
        {"session_id": "sess-a", "session_seq": 2, "chain_mode": "v2",
         "start_minute": "2026-09-30T11:00:00Z", "end_minute": "2026-09-30T11:30:00Z",
         "dominant_theme": "new_theme"},
        {"session_id": "sess-b", "session_seq": 1, "chain_mode": "v2",
         "start_minute": "2026-09-30T12:00:00Z", "end_minute": "2026-09-30T12:30:00Z",
         "dominant_theme": "theme_b"},
    ]
    usage = [
        # inside session A's STALE window: after resolution that window no
        # longer exists — the call must fall to unmapped, never old_theme
        _usage("2026-09-30T10:10:00Z", 100),
        # inside session A's LATEST window: attributed to new_theme
        _usage("2026-09-30T11:10:00Z", 50),
    ]
    m = cache_map.build_map(usage_rows=usage, chain_rows=chain_rows)
    assert m["verkle"]["n_sessions"] == 2, "sessions, not rows"
    assert m["verkle"]["n_chain_rows"] == 3, "raw rows surfaced as their own denominator"
    themes = {t["theme"]: t for t in m["by_theme"]}
    assert themes["new_theme"]["calls"] == 1
    assert "old_theme" not in themes, "stale row's window must not survive resolution"


def test_cache_map_dedupe_is_identity_on_v1() -> None:
    """One row per session (v1 amend semantics): the resolution is the identity."""
    rows = [{"session_id": f"sess-{i}",
             "start_minute": "2026-09-30T10:00:00Z", "end_minute": "2026-09-30T11:00:00Z",
             "dominant_theme": "t"} for i in range(3)]
    assert cache_map.latest_rows_per_session(rows) is rows


def test_cache_map_latest_row_per_session_order() -> None:
    """The helper keeps the latest occurrence's chain position (recency order),
    passes orphan (no-session) rows through in place."""
    orphan = {"session_id": None, "dominant_theme": "x"}
    stale_a = {"session_id": "a", "v": 1}
    other = {"session_id": "b", "v": 1}
    latest_a = {"session_id": "a", "v": 2}
    out = cache_map.latest_rows_per_session([stale_a, other, orphan, latest_a])
    assert [id(r) for r in out] == [id(other), id(orphan), id(latest_a)], (
        "stale 'a' row dropped; 'b', the orphan, and the LATEST 'a' row survive "
        "in their chain positions")
    assert out[-1]["v"] == 2, "last matching row wins"


# ── gene_pool_feeder: the aud_verkles seam names the session basis ───────────

def test_gene_pool_basis_is_identity_on_v1() -> None:
    v = {"rows": 7197, "session_diversity": {"distinct_session_ids": 7197, "dup_rate": 0}}
    basis = gpf.resolve_verkle_basis(v)
    assert basis["append_mode"] is False
    assert basis["sessions"] == 7197
    # v1 gene text is byte-unchanged (the frozen 2026-09-04 audit reads exactly this)
    assert gpf._knot_theme_text("biography", 1100, v, basis) == (
        "chain theme 'biography': 1100 signed rows in verkle_chain.jsonl "
        "(7197 rows total, dup_rate 0)")


def test_gene_pool_basis_flags_v2_append_mode() -> None:
    """A v2-sourced audit (rows > distinct sessions) must never read rows as
    sessions: both denominators named, dup_rate read as canonical history."""
    v = {"rows": 12, "session_diversity": {"distinct_session_ids": 5, "dup_rate": 0.5833}}
    basis = gpf.resolve_verkle_basis(v)
    assert basis["append_mode"] is True
    assert basis["sessions"] == 5
    assert basis["dup_rate_reading"] == "canonical append-leaves history (AH19 v2), not anomaly"
    text = gpf._knot_theme_text("biography", 9, v, basis)
    assert "12 rows / 5 sessions under v2 append-leaves" in text
    assert "canonical append-leaves history" in text


# ── knot_untangle: cluster the LATEST row per session ────────────────────────

def test_knot_untangle_resolves_multirow_sessions_to_latest(tmp_path, monkeypatch) -> None:
    from mag import chain_query

    rows = [
        # session A seq history: the stale row shares an anchor with the latest
        # row but is NOT a near-duplicate of it (overlap 3/9 = 0.33)
        {"session_id": "sess-a", "session_seq": 1, "chain_mode": "v2",
         "filename": "a.s1.knot.json", "note": "alpha beta gamma delta epsilon zeta"},
        # session A LATEST row: a genuine near-duplicate of session B (6/7)
        {"session_id": "sess-a", "session_seq": 2, "chain_mode": "v2",
         "filename": "a.s2.knot.json", "note": "alpha beta gamma eta theta iota"},
        {"session_id": "sess-b", "session_seq": 1, "chain_mode": "v2",
         "filename": "b.s1.knot.json", "note": "alpha beta gamma eta theta iota kappa"},
    ]
    chain_file = tmp_path / "verkle_chain.jsonl"
    chain_file.write_text("\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
    monkeypatch.setattr(chain_query, "CHAIN_PATH", chain_file)

    scan = ku.scan_chain()
    assert scan["ok"] is True, scan
    assert scan["n_knots"] == 2, "one knot per SESSION (latest row), not per chain row"
    assert scan["n_chain_rows"] == 3
    assert scan["n_tangled_clusters"] == 1, "the real near-duplicate pair (A-latest, B)"
    member_files = {m["filename"] for m in scan["top_tangled"][0]["members"]}
    assert member_files == {"a.s2.knot.json", "b.s1.knot.json"}, (
        "the session's LATEST row represents it; the stale seq row never appears")


def test_knot_untangle_dedupe_is_identity_on_v1() -> None:
    rows = [{"session_id": "a", "filename": "a.knot.json"},
            {"session_id": "b", "filename": "b.knot.json"}]
    assert ku.latest_rows_per_session(rows) is rows
