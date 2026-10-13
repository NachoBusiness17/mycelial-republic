"""Strict-prefix receipt law tests (build wave B2, 2026-10-05).

Law source: arXiv 2609.15030 steal card
watch/inbox/frontier_olm_2026-10-04/steal/kv-cache-and-context-engineering.md
(token-prefix validity != state validity). Two proofs the lane contract
demands:
  1. a mismatched receipt forces recompute (config-generation tag or
     prefix divergence - never a skip on unproven state);
  2. the cache_kpi tok_hit split counts nominal vs receipt-verified hits
     correctly, so cache economics measure usable, not claimed, cache.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mag.context_checkpoint import (  # noqa: E402
    CheckpointEngine,
    freeze_receipt,
    gate_skip_recompute,
)
from tools.cache_kpi import compute  # noqa: E402

# ASCII so byte offsets are char offsets; block size is 64 bytes
FULL = "\n".join("frozen history line %03d: the quick brown fox" % i for i in range(40))


def test_mismatched_receipt_forces_recompute(tmp_path):
    engine = CheckpointEngine()
    engine.checkpoint_dir = tmp_path / "checkpoints"
    session = "receipt-mismatch-001"
    cp = engine.checkpoint(session_id=session, full_context=FULL,
                           model_used="gen-a-model", config_generation="gen-A")
    assert cp.prefix_receipt["schema"] == "prefix_receipt.v1"
    assert cp.prefix_receipt["config_generation"] == "gen-A"

    # 1. matching generation + intact prefix -> the only skip allowed
    ok_gate = engine.reuse_prefix(session, FULL, config_generation="gen-A")
    assert ok_gate["skip_recompute"] is True, ok_gate
    assert ok_gate["verified_bytes"] == len(FULL.encode())
    assert ok_gate["reason"] == "ok"

    # a longer candidate (prefix + fresh tail) still proves the frozen prefix;
    # the tail is new work, never cached
    tail_gate = engine.reuse_prefix(session, FULL + "\nfresh tail",
                                    config_generation="gen-A")
    assert tail_gate["skip_recompute"] is True, tail_gate
    assert tail_gate["verified_bytes"] == len(FULL.encode())

    # 2. config-generation mismatch: identical bytes, different state
    # producer -> recompute, zero verified bytes
    stale = engine.reuse_prefix(session, FULL, config_generation="gen-B")
    assert stale["skip_recompute"] is False, stale
    assert stale["verified_bytes"] == 0
    assert stale["reason"] == "config-generation-mismatch"

    # 3. tampered prefix: diverges inside block 1 -> partial verify, no skip
    tampered = FULL[:80] + "X" + FULL[81:]
    diverged = engine.reuse_prefix(session, tampered, config_generation="gen-A")
    assert diverged["skip_recompute"] is False, diverged
    assert diverged["reason"] == "prefix-divergence"
    assert 0 < diverged["verified_bytes"] < len(FULL.encode())
    assert diverged["verified_bytes"] == 64  # block 0 intact, block 1 diverged

    # 4. pre-law rows carry no receipt: unreceipted reuse costs as a miss
    bare = gate_skip_recompute(FULL, {}, "gen-A")
    assert bare["skip_recompute"] is False
    assert bare["reason"] == "no-receipt"


def test_receipt_survives_disk_roundtrip(tmp_path):
    """A fresh engine (cold cache) reloads the receipt and gates on it."""
    writer = CheckpointEngine()
    writer.checkpoint_dir = tmp_path / "checkpoints"
    session = "receipt-roundtrip-002"
    writer.checkpoint(session_id=session, full_context=FULL,
                      model_used="gen-a-model", config_generation="gen-R")

    reader = CheckpointEngine()
    reader.checkpoint_dir = tmp_path / "checkpoints"
    gate = reader.reuse_prefix(session, FULL, config_generation="gen-R")
    assert gate["skip_recompute"] is True, gate
    stale = reader.reuse_prefix(session, FULL, config_generation="gen-S")
    assert stale["skip_recompute"] is False
    assert stale["reason"] == "config-generation-mismatch"


def test_freeze_receipt_binds_generation_tag():
    """Same bytes, two generations -> two distinct receipts, cross-refused."""
    r1 = freeze_receipt(FULL, "gen-1")
    r2 = freeze_receipt(FULL, "gen-2")
    assert r1["prefix_sha256"] == r2["prefix_sha256"]
    assert r1["config_generation"] != r2["config_generation"]
    assert gate_skip_recompute(FULL, r1, "gen-1")["skip_recompute"] is True
    assert gate_skip_recompute(FULL, r2, "gen-1")["skip_recompute"] is False


def test_kpi_split_counts_nominal_vs_receipt_verified():
    rows = [
        # receipt-verified hit: 100 cached, all 100 state-proven
        {"ts": "2026-10-05T01", "provider": "deepseek", "prompt_tokens": 200,
         "cache_hit_tokens": 100, "cache_miss_tokens": 100, "ok": True,
         "cache_receipt": {"ok": True, "verified_tokens": 100}},
        # nominal hit, no receipt verdict: claimed but unproven
        {"ts": "2026-10-05T02", "provider": "deepseek", "prompt_tokens": 200,
         "cache_hit_tokens": 80, "cache_miss_tokens": 120, "ok": True},
        # receipt present and REFUSED: nominal hit, zero usable tokens
        {"ts": "2026-10-05T03", "provider": "deepseek", "prompt_tokens": 100,
         "cache_hit_tokens": 60, "cache_miss_tokens": 40, "ok": True,
         "cache_receipt": {"ok": False}},
        # error row: counted as err, excluded from every rate
        {"ts": "2026-10-05T04", "provider": "deepseek", "prompt_tokens": 50,
         "cache_hit_tokens": 50, "cache_miss_tokens": 0, "ok": False,
         "cache_receipt": {"ok": True, "verified_tokens": 50}},
        # flat-field twin shape, with an inflated verified count that must
        # clamp to the row's own claimed cache
        {"ts": "2026-10-05T05", "provider": "deepseek", "prompt_tokens": 100,
         "cache_hit_tokens": 50, "cache_miss_tokens": 50, "ok": True,
         "receipt_ok": True, "receipt_verified_tokens": 999},
    ]
    g = compute(rows)["deepseek"]
    assert g["cached_tok"] == 290                    # 100+80+60+50 (err excluded)
    assert g["receipt_tok"] == 150                   # 100 + clamped 50
    assert g["unreceipted_tok"] == 140               # claimed but not state-proven
    assert g["denom_tok"] == 600                     # 200+200+100+100
    assert g["tok_hit_rate"] == round(290 / 600, 4)  # nominal
    assert g["tok_hit_receipted_rate"] == round(150 / 600, 4)  # usable
    assert g["receipt_rows"] == 3                    # ok rows carrying a verdict
    assert g["receipt_ok_rows"] == 2                 # verified + clamped-flat row
    assert g["rows"] == 5 and g["err"] == 1
