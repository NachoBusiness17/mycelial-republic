"""tests/test_veil_evaluator.py - Verification for Automated Veil Evaluator."""
from __future__ import annotations

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.veil_evaluator import (
    ESTATE_INVARIANTS,
    check_identity_leaks,
    check_snapshot_cleanliness,
    compute_veil_metric,
    score_invariant_recovery,
)


def test_invariants_catalog():
    assert len(ESTATE_INVARIANTS) == 10
    assert "INV-01" in ESTATE_INVARIANTS
    assert "INV-04" in ESTATE_INVARIANTS


def test_invariant_recovery():
    sample_text = (
        "The blank space was preserved and not rewritten. "
        "The lying map misled the traveler, but the floor checks the hash. "
        "A receipt was generated before any destructive mutation. "
        "The text does not contain any mention of a gardener."
    )
    res = score_invariant_recovery(sample_text)
    assert res["recovered_count"] >= 4
    assert "INV-01" in res["recovered_ids"]
    assert "INV-04" in res["recovered_ids"]
    assert "INV-05" in res["recovered_ids"]
    assert "INV-06" in res["recovered_ids"]


def test_identity_leak_detection():
    clean_text = "Miriam walked into the archive and inspected the ledger."
    assert len(check_identity_leaks(clean_text)) == 0

    leaked_text = "Miriam opened /mnt/c/Users/foste/Documents/projects/run.py with key sk-abcdef1234567890123456"
    leaks = check_identity_leaks(leaked_text)
    assert len(leaks) >= 2


def test_veil_metric_thresholds():
    # Strong veil: recovers >= 7 invariants, zero leaks
    strong_text = (
        "1. The blank space is preserved; not rewritten. "
        "2. Framework rails enforce safety boundaries. "
        "3. LAW-064 requires grounded evidence and verifiable citations. "
        "4. The lying map trapped him; the floor checks hash. "
        "5. A log entry receipt is emitted before destructive actions. "
        "6. The story has no mention of the porter. "
        "7. Clear boundaries protect public artifacts from private state. "
        "8. Reactive wakeup ensures decoupled execution without busy polling."
    )
    metric_strong = compute_veil_metric(strong_text)
    assert metric_strong["verdict"] == "VEIL_STRONG"
    assert metric_strong["identity_leak_rate"] == 0.0
    assert metric_strong["veil_metric"] >= 0.70

    # Breached veil: even with 10 invariants, if private path leaks -> VEIL_BREACHED
    breached_text = strong_text + " Running on /mnt/c/Users/foste/test"
    metric_breached = compute_veil_metric(breached_text)
    assert metric_breached["verdict"] == "VEIL_BREACHED"
    assert metric_breached["identity_leak_rate"] == 1.0


def test_snapshot_cleanliness():
    safe_paths = [
        "canon/same_book/BOOK_V1.md",
        "tools/veil_evaluator.py",
        "dashboard/static/room.html",
    ]
    res_safe = check_snapshot_cleanliness(safe_paths)
    assert res_safe["clean"] is True

    unsafe_paths = [
        "canon/same_book/BOOK_V1.md",
        ".env",
        "memory/biography/knot_01.json",
    ]
    res_unsafe = check_snapshot_cleanliness(unsafe_paths)
    assert res_unsafe["clean"] is False
    assert len(res_unsafe["violations"]) == 2


def test_em_dash_cleanliness():
    tools_path = os.path.join(ROOT, "tools", "veil_evaluator.py")
    text = open(tools_path, encoding="utf-8").read()
    assert "—" not in text, "Unicode em-dash forbidden in veil_evaluator.py"


if __name__ == "__main__":
    test_invariants_catalog()
    test_invariant_recovery()
    test_identity_leak_detection()
    test_veil_metric_thresholds()
    test_snapshot_cleanliness()
    test_em_dash_cleanliness()
    print("ALL TESTS PASSED in test_veil_evaluator.py")
