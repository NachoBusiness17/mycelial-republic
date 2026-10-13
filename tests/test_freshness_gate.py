"""Freshness-receipts gate tests (MICKEY17 V2 owed item, t11b; hash binding t37).

Covers the three contract cases first (fresh passes, stale fails, missing
stamp fails), then the negative space as first-class cases: future-dated
stamps, unparseable dates, missing files, and the real CLI exit codes
(0 fresh, 2 otherwise) pinned through a subprocess. The t37 layer binds the
stamp to a source hash: `source-fetched: DATE sha256:HEX` plus --source PATH
(hash-match passes, hash-mismatch fails, no-hash behaves exactly as before,
a re-stamp that drops a binding fails, --days stays untouched).
"""
from __future__ import annotations

import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

from tools.freshness_gate import DEFAULT_MAX_AGE_DAYS, gate, gate_file, main, sha256_of_file

TODAY = date(2026, 9, 25)
TOOL = Path(__file__).resolve().parents[1] / "tools" / "freshness_gate.py"
SELF = Path(__file__).resolve() if "__file__" in globals() else TOOL.parents[1] / "tests" / "test_freshness_gate.py"

# HEADLESS law (spawn_sites_no_window, ratcheted by tests/test_headless_law.py):
# every subprocess spawn carries CREATE_NO_WINDOW on win32 so no console window
# pops on the operator's desktop. 0 on platforms without the flag.
HEADLESS = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000) if sys.platform == "win32" else 0


def test_fresh_receipt_passes():
    result = gate("# receipt\nsource-fetched: 2026-09-20\nclaim body\n", TODAY)
    assert result["ok"] is True
    assert result["stamp"] == "2026-09-20"
    assert result["age_days"] == 5


def test_stale_receipt_fails():
    result = gate("source-fetched: 2026-09-01\nclaim body\n", TODAY)
    assert result["ok"] is False
    assert result["age_days"] > DEFAULT_MAX_AGE_DAYS


def test_missing_stamp_fails():
    result = gate("# receipt with no stamp at all\n", TODAY)
    assert result["ok"] is False
    assert "no freshness stamp" in result["reason"]


def test_boundary_age_exactly_at_bar_passes():
    stamp = TODAY.isoformat()
    assert gate(f"source-fetched: {stamp}\n", TODAY, max_age_days=14)["ok"] is True


def test_boundary_age_one_past_bar_fails():
    old = TODAY.isoformat()
    today_plus = date(2026, 10, 10)
    assert gate(f"source-fetched: {old}\n", today_plus, max_age_days=14)["ok"] is False


def test_days_argument_is_honored():
    # 2026-09-15 is exactly 10d old at TODAY.
    text = "source-fetched: 2026-09-15\n"
    assert gate(text, TODAY, max_age_days=9)["ok"] is False
    assert gate(text, TODAY, max_age_days=10)["ok"] is True
    assert gate(text, TODAY, max_age_days=14)["ok"] is True


def test_most_recent_stamp_is_the_evidence():
    text = "source-fetched: 2026-06-01\n...refetch...\nsource-fetched: 2026-09-24\n"
    result = gate(text, TODAY)
    assert result["ok"] is True
    assert result["stamp"] == "2026-09-24"


def test_future_dated_stamp_fails():
    result = gate("source-fetched: 2026-10-01\n", TODAY)
    assert result["ok"] is False
    assert "future-dated" in result["reason"]


def test_malformed_calendar_date_is_not_a_stamp():
    result = gate("source-fetched: 2026-13-40\n", TODAY)
    assert result["ok"] is False
    assert "no freshness stamp" in result["reason"]


def test_label_variants_are_accepted():
    for line in (
        "source_fetched: 2026-09-24",
        "source fetched: 2026-09-24",
        "Source-Fetched: 2026-09-24",
        "fetched: 2026-09-24",
        "observed-at: 2026-09-24",
        "observed_at: 2026-09-24",
        "source-fetched:2026-09-24",
        "source-fetched: 2026-09-24T14:03:00Z",
    ):
        assert gate(line + "\n", TODAY)["ok"] is True, line


def test_unrelated_dates_do_not_count_as_stamps():
    text = "landed 2026-09-25 per ticket #2026-0925, reviewed 2026-09-25\n"
    assert gate(text, TODAY)["ok"] is False


def test_gate_file_missing_receipt_fails_closed(tmp_path):
    result = gate_file(tmp_path / "absent.md", TODAY)
    assert result["ok"] is False
    assert "not found" in result["reason"]


def test_gate_file_reads_utf8_receipt(tmp_path):
    receipt = tmp_path / "r.md"
    receipt.write_text("source-fetched: 2026-09-24\n", encoding="utf-8")
    assert gate_file(receipt, TODAY)["ok"] is True


@pytest.mark.parametrize(
    "offset_days,want_exit",
    [
        (-1, 0),    # stamped yesterday: fresh under the default 14d bar
        (-30, 2),   # stamped a month ago: stale under any bar here
    ],
)
def test_cli_exit_codes(tmp_path, offset_days, want_exit):
    # R4b note (2026-10-06): these run the REAL CLI, so the wall clock is live --
    # the old hard-coded 2026-09-xx stamps went time-bomb red on 2026-10-04 and
    # broke test_cli_hash_match_exit0_mismatch_exit2 the same way. Dates are now
    # derived from today; the in-process gates above keep their pinned TODAY.
    text = f"source-fetched: {(date.today() + timedelta(days=offset_days)).isoformat()}\n"
    receipt = tmp_path / "receipt.md"
    receipt.write_text(text, encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(receipt)],
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=HEADLESS,
    )
    assert proc.returncode == want_exit, proc.stdout + proc.stderr


def test_cli_no_stamp_exits_two(tmp_path):
    receipt = tmp_path / "receipt.md"
    receipt.write_text("no stamp here\n", encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, str(TOOL), str(receipt)],
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=HEADLESS,
    )
    assert proc.returncode == 2, proc.stdout + proc.stderr


def test_self_test_exits_zero():
    proc = subprocess.run(
        [sys.executable, str(TOOL), "--self-test"],
        capture_output=True,
        text=True,
        timeout=60,
        creationflags=HEADLESS,
    )
    assert proc.returncode == 0
    assert proc.stdout.count("PASS") == 6


def test_main_returns_int_directly(tmp_path):
    fresh = tmp_path / "fresh.md"
    fresh.write_text("source-fetched: 2026-09-25\n", encoding="utf-8")
    assert main([str(fresh), "--days", "14"]) == 0
    assert main([str(tmp_path / "nope.md")]) == 2


# --- t37: source-hash binding -------------------------------------------------


def _bound_receipt(tmp_path, content: bytes, stamp_date: str = "2026-09-20"):
    """Write a source file plus a receipt whose stamp binds its real sha256."""
    src = tmp_path / "source.txt"
    src.write_bytes(content)
    digest = sha256_of_file(src)
    receipt = tmp_path / "receipt.md"
    receipt.write_text(f"source-fetched: {stamp_date} sha256:{digest}\n", encoding="utf-8")
    return receipt, src, digest


def test_stamp_with_matching_hash_passes(tmp_path):
    receipt, src, digest = _bound_receipt(tmp_path, b"claim v1\n")
    result = gate_file(receipt, TODAY, source=src)
    assert result["ok"] is True
    assert result["hash"] == digest
    assert result["hash_ok"] is True
    assert "verified" in result["reason"]


def test_stamp_with_mismatched_hash_fails(tmp_path):
    receipt, src, digest = _bound_receipt(tmp_path, b"claim v1\n")
    src.write_bytes(b"claim v2 changed\n")  # source moved under the old binding
    result = gate_file(receipt, TODAY, source=src)
    assert result["ok"] is False
    assert result["hash_ok"] is False
    assert "mismatch" in result["reason"]
    assert digest in result["reason"]


def test_no_hash_behaves_as_before(tmp_path):
    text = "source-fetched: 2026-09-20\nclaim body\n"
    result = gate(text, TODAY)
    assert result["ok"] is True
    assert result["stamp"] == "2026-09-20"
    assert result["age_days"] == 5
    assert result["hash"] is None
    assert result["hash_ok"] is None
    assert "sha256" not in result["reason"]


def test_bound_source_missing_fails(tmp_path):
    receipt, _src, _digest = _bound_receipt(tmp_path, b"claim v1\n")
    result = gate_file(receipt, TODAY, source=tmp_path / "gone.txt")
    assert result["ok"] is False
    assert "bound source file not found" in result["reason"]


def test_hash_without_source_is_stamped_but_unverified(tmp_path):
    receipt, _src, digest = _bound_receipt(tmp_path, b"claim v1\n")
    result = gate_file(receipt, TODAY)
    assert result["ok"] is True
    assert result["hash"] == digest
    assert result["hash_ok"] is None
    assert "unverified" in result["reason"]


def test_source_demanded_but_receipt_has_no_binding_fails(tmp_path):
    src = tmp_path / "source.txt"
    src.write_bytes(b"claim v1\n")
    receipt = tmp_path / "receipt.md"
    receipt.write_text("source-fetched: 2026-09-20\n", encoding="utf-8")
    result = gate_file(receipt, TODAY, source=src)
    assert result["ok"] is False
    assert "no sha256 binding" in result["reason"]


def test_restamp_dropping_binding_fails():
    old_bound = "source-fetched: 2026-06-01 sha256:" + "a" * 64 + "\n"
    fresh_bare = "source-fetched: 2026-09-20\n"
    result = gate(old_bound + fresh_bare, TODAY)
    assert result["ok"] is False
    assert "re-stamp smell" in result["reason"]


def test_restamp_with_new_binding_passes():
    old_bound = "source-fetched: 2026-06-01 sha256:" + "a" * 64 + "\n"
    fresh_bound = "source-fetched: 2026-09-20 sha256:" + "b" * 64 + "\n"
    result = gate(old_bound + fresh_bound, TODAY)
    assert result["ok"] is True
    assert result["hash"] == "b" * 64


def test_hash_comparison_is_case_insensitive(tmp_path):
    src = tmp_path / "source.txt"
    src.write_bytes(b"claim v1\n")
    receipt = tmp_path / "receipt.md"
    receipt.write_text(f"source-fetched: 2026-09-20 sha256:{sha256_of_file(src).upper()}\n", encoding="utf-8")
    result = gate_file(receipt, TODAY, source=src)
    assert result["ok"] is True
    assert result["hash"] == sha256_of_file(src)


def test_days_bar_still_applies_to_bound_stamp(tmp_path):
    receipt, src, _digest = _bound_receipt(tmp_path, b"claim v1\n", stamp_date="2026-09-01")
    stale = gate_file(receipt, TODAY, max_age_days=14, source=src)
    assert stale["ok"] is False  # hash matches but the date bar is untouched
    assert "old; bar is" in stale["reason"]
    widened = gate_file(receipt, TODAY, max_age_days=30, source=src)
    assert widened["ok"] is True  # --days override still honored with a binding
    assert widened["hash_ok"] is True


def test_malformed_binding_is_not_a_stamp():
    overlong = "source-fetched: 2026-09-20 sha256:" + "a" * 65 + "\n"
    result = gate(overlong, TODAY)
    assert result["ok"] is False
    assert "no freshness stamp" in result["reason"]
    short = "source-fetched: 2026-09-20 sha256:" + "a" * 63 + "\n"
    result = gate(short, TODAY)
    assert result["ok"] is False
    assert "no freshness stamp" in result["reason"]
    nonhex = "source-fetched: 2026-09-20 sha256:" + "z" * 64 + "\n"
    result = gate(nonhex, TODAY)
    assert result["ok"] is False
    assert "no freshness stamp" in result["reason"]


def test_cli_hash_match_exit0_mismatch_exit2(tmp_path):
    # R4b (2026-10-06): stamp is today-5 (was hard-coded 2026-09-20) because this
    # test drives the real CLI under the live clock -- the pinned date turned the
    # expected-exit-0 leg red on 2026-10-04 with "16d old; bar is 14d".
    stamp = (date.today() - timedelta(days=5)).isoformat()
    receipt, src, _digest = _bound_receipt(tmp_path, b"claim v1\n", stamp_date=stamp)
    match = subprocess.run(
        [sys.executable, str(TOOL), str(receipt), "--source", str(src)],
        capture_output=True, text=True, timeout=60, creationflags=HEADLESS,
    )
    assert match.returncode == 0, match.stdout + match.stderr
    src.write_bytes(b"claim v2 changed\n")
    mismatch = subprocess.run(
        [sys.executable, str(TOOL), str(receipt), "--source", str(src)],
        capture_output=True, text=True, timeout=60, creationflags=HEADLESS,
    )
    assert mismatch.returncode == 2, mismatch.stdout + mismatch.stderr


def test_module_has_no_em_dash_in_filed_text():
    tool_src = TOOL.read_text(encoding="utf-8")
    test_src = SELF.read_text(encoding="utf-8")
    assert "\u2014" not in tool_src
    assert "\u2013" not in tool_src
    assert "\u2014" not in test_src
    assert "\u2013" not in test_src
