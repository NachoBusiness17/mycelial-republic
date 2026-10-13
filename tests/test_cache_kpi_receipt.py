"""Tests for the cache_kpi receipt-verdict parse (ouroboros R3 move 7).

Cause + evidence: tools/cache_kpi.py _receipt did bool(ok) on the receipt
verdict, and a producer stamping the string "false" counted as RECEIPTED
(the truthiness of a non-empty string); the lens probe measured 2 of 3 rows
receipted on false-strings (SYNTHESIS row 7). Contract under test: bool
verdicts unchanged, string "false"/"0"/"no" REFUSED, string "true"/"1"/"yes"
receipted, unparseable strings carry no verdict (nominal only), and
compute() banks receipt tokens from ok verdicts only.
"""
from __future__ import annotations

import tools.cache_kpi as ck


def _row(**over):
    row = {"provider": "deepseek", "ts": "2026-10-05T00:00:00Z",
           "prompt_tokens": 1000, "cached_tokens": 600, "miss_tokens": 400,
           "ok": True}
    row.update(over)
    return row


def test_false_string_refused_not_receipted():
    ok, _ = ck._receipt(_row(receipt_ok="false"))
    assert ok is False
    ok, _ = ck._receipt(_row(cache_receipt={"ok": "False", "verified_tokens": 10}))
    assert ok is False


def test_true_string_and_bool_verdicts_unchanged():
    assert ck._receipt(_row(receipt_ok="true"))[0] is True
    assert ck._receipt(_row(receipt_ok=True))[0] is True
    assert ck._receipt(_row(receipt_ok=False))[0] is False


def test_unparseable_and_absent_carry_no_verdict():
    assert ck._receipt(_row(receipt_ok="maybe")) == (None, None)
    assert ck._receipt(_row())[0] is None


def test_compute_banks_only_true_receipts():
    """The probe shape: rows 1-2 stamped the string "false" (pre-fix both
    counted receipted, 2 of 3); after the fix only the true row banks."""
    rows = [
        _row(receipt_ok="false", receipt_verified_tokens=600),
        _row(cache_receipt={"ok": "false"}),
        _row(receipt_ok=True, receipt_verified_tokens=500),
    ]
    g = ck.compute(rows)["deepseek"]
    assert g["receipt_rows"] == 3
    assert g["receipt_ok_rows"] == 1
    assert g["receipt_tok"] == 500
    # nominal cache math is untouched: 3 rows x 600 cached, 1300 unreceipted
    assert g["cached_tok"] == 1800
    assert g["unreceipted_tok"] == 1300
