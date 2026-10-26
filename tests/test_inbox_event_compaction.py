"""tests/test_inbox_event_compaction.py - Verification for inbox event compactor."""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.inbox_event_compaction import (
    compute_state_hash,
    generate_compaction_plan,
    profile_events,
)


def test_profiling_logic():
    dummy_events = [
        {"seq": 1, "op": "register", "file": "file_a.md", "sha256": "1111", "ts": "2026-10-01T00:00:00Z"},
        {"seq": 2, "op": "register", "file": "file_b.md", "sha256": "2222", "ts": "2026-10-01T00:01:00Z"},
        {"seq": 3, "op": "autoseal", "file": "file_a.md", "sha256": "3333", "ts": "2026-10-01T00:02:00Z"}, # updates file_a
        {"seq": 4, "op": "invalidate", "file": "file_b.md", "ts": "2026-10-01T00:03:00Z"}, # removes file_b
        {"seq": 5, "op": "register", "file": "file_c.md", "sha256": "4444", "ts": "2026-10-01T00:04:00Z"},
    ]
    prof = profile_events(dummy_events)
    assert prof["total_events"] == 5
    assert prof["active_items"] == 2  # file_a and file_c
    assert "file_a.md" in prof["active_files"]
    assert prof["active_files"]["file_a.md"]["sha256"] == "3333"
    assert "file_b.md" not in prof["active_files"]
    assert "file_c.md" in prof["active_files"]
    assert prof["redundant_events"] == 3
    assert prof["compaction_ratio"] == 0.60


def test_state_hash_determinism():
    state1 = {"a.txt": {"sha256": "123"}, "b.txt": {"sha256": "456"}}
    state2 = {"b.txt": {"sha256": "456"}, "a.txt": {"sha256": "123"}} # different insertion order
    h1 = compute_state_hash(state1)
    h2 = compute_state_hash(state2)
    assert h1 == h2
    assert len(h1) == 64


def test_plan_generation_tmp(tmp_path=None):
    dummy_events = [
        {"seq": 1, "op": "register", "file": "test.md", "sha256": "aaa", "ts": "2026-10-01T00:00:00Z"}
    ]
    test_log = os.path.join(ROOT, "watch", "inbox", "tmp_test_events.jsonl")
    with open(test_log, "w", encoding="utf-8") as fp:
        for ev in dummy_events:
            fp.write(json.dumps(ev) + "\n")

    plan_file = os.path.join(ROOT, "watch", "inbox", "tmp_test_plan.md")
    saved_plan = generate_compaction_plan(test_log, plan_file)
    assert os.path.exists(saved_plan)
    with open(saved_plan, "r", encoding="utf-8") as fp:
        txt = fp.read()
    assert "Total Logged Events: **1**" in txt
    assert "Active Retained Items: **1**" in txt

    # Clean up temp files
    if os.path.exists(test_log):
        os.remove(test_log)
    if os.path.exists(plan_file):
        os.remove(plan_file)


def test_em_dash_cleanliness():
    tool_file = os.path.join(ROOT, "tools", "inbox_event_compaction.py")
    content = open(tool_file, "r", encoding="utf-8").read()
    assert "—" not in content, "Forbidden unicode em-dash found in inbox_event_compaction.py"


if __name__ == "__main__":
    test_profiling_logic()
    test_state_hash_determinism()
    test_plan_generation_tmp()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_inbox_event_compaction.py")
