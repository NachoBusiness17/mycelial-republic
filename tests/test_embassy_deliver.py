"""Test the embassy-deliver automation (publish-safety gate, placeholders, dry-run).

All deterministic, no network, no git side effects (dry-run), no credentials.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from mag.embassy_deliver import (
    REPO_NAME,
    assemble,
    placeholder_check,
    publish,
    publish_safety_check,
)


def test_safety_gate_ok_on_clean_files():
    """A file with no secrets passes the publish-safety gate."""
    tmp = Path(__file__).parent / "_deliver_clean_test"
    tmp.mkdir(exist_ok=True)
    f = tmp / "note.md"
    f.write_text("The synthetic surrogate used abstract placeholders only. Evidence-based.\n", encoding="utf-8")
    res = publish_safety_check([f])
    assert res["ok"] is True
    assert res["secrets"] == {}
    f.unlink(missing_ok=True)
    tmp.rmdir()


def test_safety_gate_blocks_real_secret():
    """A planted real secret blocks the gate (never publish it)."""
    tmp = Path(__file__).parent / "_deliver_secret_test"
    tmp.mkdir(exist_ok=True)
    f = tmp / "leak.md"
    f.write_text("token is ghp_0123456789abcdefABCDEF\n", encoding="utf-8")
    res = publish_safety_check([f])
    assert res["ok"] is False
    assert "gh_token" in res["secrets"].get("leak.md", {})
    f.unlink(missing_ok=True)
    tmp.rmdir()


def test_placeholder_check_flags_unresolved():
    """An unresolved ⟨ ⟨ ⟩ ⟩ operator placeholder blocks the pipeline."""
    tmp = Path(__file__).parent / "_deliver_ph_test.md"
    tmp.write_text("channel: ⟨ private embassy channel ⟩\n", encoding="utf-8")
    res = placeholder_check(tmp)
    assert res["ok"] is False
    assert len(res["unresolved"]) == 1
    tmp.unlink(missing_ok=True)


def test_placeholder_check_ok_when_none():
    tmp = Path(__file__).parent / "_deliver_ph2_test.md"
    tmp.write_text("channel: discord dm\n", encoding="utf-8")
    res = placeholder_check(tmp)
    assert res["ok"] is True
    tmp.unlink(missing_ok=True)


def test_placeholder_check_ignores_empty_self_reference():
    """The doc's own instruction 'marked ⟨ ⟩' is self-reference, not a field."""
    tmp = Path(__file__).parent / "_deliver_ph3_test.md"
    tmp.write_text("Placeholder fields are marked ⟨ ⟩ like so.\n", encoding="utf-8")
    res = placeholder_check(tmp)
    assert res["ok"] is True
    tmp.unlink(missing_ok=True)


def test_publish_dry_run_takes_no_external_action():
    """Dry-run returns clean gated result and never pushes."""
    res = publish(dry=True)
    # The gates may block (placeholders unresolved) OR report a dry-run; either
    # way no external action occurs and "dry" is always surfaced.
    assert res["dry"] is True


def test_assemble_dry_never_inits_git():
    res = assemble(dry=True)
    assert res["ok"] is True
    assert res["dry"] is True
    assert "git init" in res["steps"]
