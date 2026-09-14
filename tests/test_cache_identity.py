"""tests for mag/cache_identity.py — W3 cache-identity probe (falsifier F-W2).

Offline only: determinism, drift integrity, medians, metrics, tri-state verdict
gates, row schema. No ollama calls — the probe itself is exercised separately
($0-local, host ollama only).
"""
from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import cache_identity as ci  # noqa: E402


def test_body_deterministic_and_ascii():
    b1 = ci.load_body_text(4000)
    b2 = ci.load_body_text(4000)
    assert b1 == b2
    assert len(b1) == 4000
    assert all(32 <= ord(c) < 127 for c in b1)


def test_body_is_real_repo_text_labeled():
    for size in (200, 6000, 16000):  # label chunk is FIRST: every body carries it
        body = ci.load_body_text(size)
        assert "PROXY prefill corpus" in body
        assert "c1/c2" in body


def test_compose_prefix_deterministic_with_sentinel():
    body = ci.load_body_text(3000)
    m = ci.marker_for(ci.DEFAULT_SEED, 1)
    p1 = ci.compose_prefix(m, body)
    p2 = ci.compose_prefix(ci.marker_for(ci.DEFAULT_SEED, 1), body)
    assert p1 == p2
    assert p1.rstrip().endswith(ci.SENTINEL)
    assert m in p1


def test_marker_unique_per_round_deterministic():
    m1 = ci.marker_for(1, 1)
    m2 = ci.marker_for(1, 2)
    m3 = ci.marker_for(2, 1)
    assert m1 != m2 and m1 != m3 and m2 != m3
    assert m1 == ci.marker_for(1, 1)


def test_drift_byte_integrity():
    body = ci.load_body_text(4000)
    base = ci.compose_prefix(ci.marker_for(7, 3), body)
    for frac in (ci.DEFAULT_HEAD_FRAC, ci.DEFAULT_TAIL_FRAC, 0.5):
        d, idx = ci.drift_byte(base, frac)
        assert len(d) == len(base)
        assert sum(1 for a, b in zip(d, base) if a != b) == 1
        assert d[:idx] == base[:idx]
        assert d[idx + 1:] == base[idx + 1:]
        assert d != base
        # drift lands inside the body region, never in header or sentinel
        hdr_end = base.find("\n\n") + 2
        sent_start = base.rfind("\n\n" + ci.SENTINEL)
        assert hdr_end <= idx < sent_start
        # deterministic
        d2, idx2 = ci.drift_byte(base, frac)
        assert (d, idx) == (d2, idx2)


def test_prompt_sha_separates_arms():
    body = ci.load_body_text(2000)
    base = ci.compose_prefix(ci.marker_for(9, 1), body)
    head, _ = ci.drift_byte(base, ci.DEFAULT_HEAD_FRAC)
    tail, _ = ci.drift_byte(base, ci.DEFAULT_TAIL_FRAC)
    user = ci.USER_PROMPT
    sha_base = ci.prompt_sha(base, user)
    assert sha_base == ci.prompt_sha(base, user)          # warm identical
    assert sha_base != ci.prompt_sha(head, user)
    assert sha_base != ci.prompt_sha(tail, user)
    assert ci.prompt_sha(head, user) != ci.prompt_sha(tail, user)


def test_median():
    assert ci.median([1.0, 5.0, 3.0]) == 3.0
    assert ci.median([4.0, 1.0, 2.0, 3.0]) == 2.5
    assert ci.median([]) == 0.0


def _synthetic_meds() -> dict[str, float]:
    return {"cold_prefill_ms": 1000.0, "warm_prefill_ms": 10.0,
            "drift_tail_prefill_ms": 60.0, "drift_head_prefill_ms": 900.0,
            "cold_wall_ms": 2000.0, "warm_wall_ms": 100.0,
            "drift_tail_wall_ms": 120.0, "drift_head_wall_ms": 1800.0}


def test_compute_metrics_formulas():
    met = ci.compute_metrics(_synthetic_meds())
    assert abs(met["speedup_prefill"] - 100.0) < 1e-9
    assert abs(met["hit_ratio_est_prefill"] - 0.99) < 1e-9
    assert abs(met["collapse_ratio_prefill"] - 0.9) < 1e-9
    assert abs(met["drift_vs_warm_prefill"] - 90.0) < 1e-9
    assert abs(met["tail_retention_prefill"] - 0.94) < 1e-9
    assert abs(met["speedup_wall"] - 20.0) < 1e-9


def test_verdict_gates():
    # strong signal -> SUPPORTED
    assert ci.verdict_tri_state(ci.compute_metrics(_synthetic_meds()))["tri_state"] == "SUPPORTED"
    # no re-light -> DISPUTED
    bad = dict(_synthetic_meds(), warm_prefill_ms=900.0, warm_wall_ms=1800.0)
    assert ci.verdict_tri_state(ci.compute_metrics(bad))["tri_state"] == "DISPUTED"
    # fast warm but hit below the 95% bar -> UNPROVEN
    mid = dict(_synthetic_meds(), warm_prefill_ms=100.0)  # hit 0.9
    assert ci.verdict_tri_state(ci.compute_metrics(mid))["tri_state"] == "UNPROVEN"
    # warm fast but drift does NOT collapse (keeps warm speed) -> UNPROVEN (collapse gate)
    noc = dict(_synthetic_meds(), drift_head_prefill_ms=50.0)
    assert ci.verdict_tri_state(ci.compute_metrics(noc))["tri_state"] == "UNPROVEN"


def test_row_schema_carries_honesty():
    # schema fields the probe writes must include the honesty law carriers
    required = {"label", "instrument", "falsifier", "ts", "run_kind", "status",
                "ollama_version", "model", "body_sources", "body_note",
                "drift_head_frac", "drift_tail_frac", "gates", "honesty",
                "rounds_data", "medians_ms", "metrics", "verdict"}
    assert ci.LABEL == "PROXY"
    assert ci.FALSIFIER == "F-W2"
    assert ci.USER_PROMPT == "Repeat the last sentence of the context verbatim."
    # gates documented as constants
    assert ci.GATE_SPEEDUP == 2.0 and ci.GATE_HIT == 0.95
    assert ci.GATE_COLLAPSE_LO <= 1.0 <= ci.GATE_COLLAPSE_HI
    # sha helper matches contract
    assert len(ci.prompt_sha("a", "b")) == 16
    assert ci.prompt_sha("a", "b") == hashlib.sha256(b"a\x00b").hexdigest()[:16]
    assert required  # schema documented above
