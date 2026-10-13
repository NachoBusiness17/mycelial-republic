"""Tests for tools.lru_null_arm (G1 gap law null arm, M3 steal).

The G1 gap law (memory/research_polished/kv_cache_compaction.md:13) demands an
LRU null before any eviction/compaction claim is believed. These tests pin the
simulator semantics that the null's number rests on: block-granular radix
prefix sharing, leaf-only LRU eviction (internal prefix blocks survive, evicted
leaves miss), the estate hard-clip shape (mag/context_pack.py:1414-1416), and
replay determinism. The falsifiable claim itself (80%+ hit at the 8k-block
anchor) is a MEASUREMENT over the moving trails tree, not a test assertion -
it lives in the banked curve JSON, not here.

Receipt: watch/inbox/buildall/lru-null-arm.md
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from tools import lru_null_arm as lna  # noqa: E402


def _run_all_checks():
    return lna.self_test()


def test_self_test_battery_green():
    failures, n = _run_all_checks()
    assert failures == []
    assert n >= 11


def test_block_granular_prefix_share():
    sim = lna.RadixLeafLRU(None, 4)
    sim.request("AAAA")
    hit, total, _ = sim.request("AAAAB")
    assert (hit, total) == (4, 5)  # block hit + partial-tail miss


def test_lru_leaf_eviction_sequence():
    sim = lna.RadixLeafLRU(2, 4)
    sim.request("AAAA")
    sim.request("BBBB")
    sim.request("CCCC")            # evicts A (oldest leaf)
    assert sim.n_cached == 2
    hit, _, _ = sim.request("BBBB")
    assert hit == 4                # hit inserts nothing, evicts nothing
    hit, _, _ = sim.request("AAAA")
    assert hit == 0                # evicted leaf misses; insert evicts C
    hit, _, _ = sim.request("BBBB")
    assert hit == 4                # B was more recent than C, survives


def test_internal_block_survives_leaf_eviction():
    sim = lna.RadixLeafLRU(1, 4)
    sim.request("AAAABBBB")        # 2 blocks; eviction takes leaf BBBB only
    hit, total, _ = sim.request("AAAACCCC")
    assert (hit, total) == (4, 8)  # prefix block AAAA still cached
    hit, _, _ = sim.request("BBBBDDDD")
    assert hit == 0                # evicted leaf is gone


def test_append_only_growth_hits():
    sim = lna.RadixLeafLRU(None, 64)
    p1 = "X" * 256
    sim.request(p1)
    hit, total, _ = sim.request(p1 + "Y" * 192)
    assert (hit, total) == (256, 448)


def test_clip_matches_estate_shape():
    clipped = lna._clip_keep_head("Z" * 6000, 4800)
    assert len(clipped) == 4800
    assert clipped.endswith("(pack clipped)")
    assert lna._clip_keep_head("Z" * 100, 4800) == "Z" * 100


def test_replay_deterministic():
    a = lna.replay(["AAAA", "BBBB", "AAAA"], capacity_blocks=2, block_chars=4)
    b = lna.replay(["AAAA", "BBBB", "AAAA"], capacity_blocks=2, block_chars=4)
    assert a == b


def test_sessions_gap_broken():
    from datetime import datetime, timedelta, timezone
    t0 = datetime(2026, 10, 3, 12, 0, tzinfo=timezone.utc)
    rows = [
        {"dt": t0, "ts": "t0", "lane": "l", "line_no": 1, "actor": "a",
         "event": "E", "detail": ""},
        {"dt": t0 + timedelta(minutes=5), "ts": "t5", "lane": "l",
         "line_no": 2, "actor": "a", "event": "E", "detail": ""},
        {"dt": t0 + timedelta(minutes=45), "ts": "t45", "lane": "l",
         "line_no": 3, "actor": "a", "event": "E", "detail": ""},
    ]
    _, n_sessions = lna.assign_sessions(rows, gap_min=30.0)
    assert n_sessions == 2
    assert [r["session"] for r in rows] == [1, 1, 2]


def test_frozen_prefix_stable_across_sessions_and_row_data():
    f1 = lna._frozen_prefix("lane", "actor", 4800, 1024)
    f2 = lna._frozen_prefix("lane", "actor", 4800, 1024)
    assert f1 == f2 and len(f1) == 1024
    other = lna._frozen_prefix("lane2", "actor", 4800, 1024)
    assert other != f1


def test_volatile_arm_prefix_changes_per_row():
    rows = [
        {"dt": None, "ts": f"2026-10-03T12:0{i}:00Z", "lane": "l",
         "line_no": i, "actor": "a", "event": "E", "detail": f"d{i}"}
        for i in range(2)
    ]
    for r in rows:
        r["dt"] = __import__("datetime").datetime(
            2026, 10, 3, 12, 0, r["line_no"], tzinfo=__import__("datetime").timezone.utc)
        r["session"] = 1
    prompts, _ = lna.build_prompt_sets(
        rows, budget=4800, frozen_chars=64, arms=["volatile", "frozen_append"])
    assert prompts["volatile"][0] != prompts["volatile"][1]
    # frozen_append head is byte-stable across turns
    assert prompts["frozen_append"][0].startswith(
        prompts["frozen_append"][1][:64]) or \
        prompts["frozen_append"][1].startswith(
            prompts["frozen_append"][0][:64])
