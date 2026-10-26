"""tests/test_contract_widening.py - Unit tests for Organ 4 Contract Widening."""
from __future__ import annotations

import json
from pathlib import Path
import pytest

from mag import contract_widening as cw


def test_check_extended_surfaces(tmp_path: Path):
    errors: list[str] = []
    warnings: list[str] = []

    # Missing surfaces
    res = cw.check_extended_surfaces(tmp_path, errors, warnings)
    assert not res["queue_ok"]
    assert not res["bridge_ok"]
    assert len(errors) == 2

    # Populate surfaces
    errors.clear()
    warnings.clear()
    queue_dir = tmp_path / "queue"
    bridge_dir = tmp_path / "bridge"
    for s in ["handoff", "lanes", "results"]:
        (queue_dir / s).mkdir(parents=True)
    for s in ["inbox", "outboxes"]:
        (bridge_dir / s).mkdir(parents=True)

    res = cw.check_extended_surfaces(tmp_path, errors, warnings)
    assert res["queue_ok"]
    assert res["bridge_ok"]
    assert len(res["missing_subdirs"]) == 0
    assert len(errors) == 0
    assert len(warnings) == 0


def test_check_handoff_integrity(tmp_path: Path):
    errors: list[str] = []
    warnings: list[str] = []
    queue_handoff = tmp_path / "queue" / "handoff"
    queue_handoff.mkdir(parents=True)

    # Legacy handoff (grandfathered)
    legacy = {
        "schema": "handoff.v1",
        "ts": "2026-09-01T00:00:00Z",
        "goal": "legacy task",
    }
    (queue_handoff / "HANDOFF-legacy.json").write_text(json.dumps(legacy), encoding="utf-8")

    # New compliant handoff
    compliant = {
        "schema": "handoff.v2",
        "ts": "2026-10-18T12:00:00Z",
        "sha256": "abcdef123456",
        "receipt": "watch/inbox/test_receipt.md",
    }
    (queue_handoff / "HANDOFF-compliant.json").write_text(json.dumps(compliant), encoding="utf-8")

    # New non-compliant handoff (violates F4)
    non_compliant = {
        "schema": "handoff.v2",
        "ts": "2026-10-18T12:01:00Z",
        "goal": "hashless handoff",
    }
    (queue_handoff / "HANDOFF-bad.json").write_text(json.dumps(non_compliant), encoding="utf-8")

    res = cw.check_handoff_integrity(tmp_path, errors, warnings)
    assert res["grandfathered"] == 1
    assert res["compliant"] == 1
    assert len(res["violations"]) == 1
    assert len(errors) == 1
    assert "HANDOFF-bad.json" in errors[0]


def test_check_subdirectory_orphans(tmp_path: Path):
    warnings: list[str] = []
    inbox = tmp_path / "inbox"
    nested = inbox / "subdir" / "deep"
    nested.mkdir(parents=True)

    # Create files
    (inbox / "indexed_top.md").write_text("top", encoding="utf-8")
    (nested / "indexed_deep.md").write_text("deep", encoding="utf-8")
    (nested / "orphan_deep.md").write_text("orphan", encoding="utf-8")

    index = {
        "schema": "index.v1",
        "root": "/board/inbox",
        "items": [
            {"path": "indexed_top.md"},
            {"path": "subdir/deep/indexed_deep.md"},
        ],
    }
    (inbox / "INDEX.json").write_text(json.dumps(index), encoding="utf-8")

    report = cw.check_subdirectory_orphans(inbox, index, warnings)
    assert report["orphans_total"] == 1
    assert "subdir/deep/orphan_deep.md" in report["orphans"]
    assert len(warnings) == 1
    assert "1 orphans across subdirectories" in warnings[0]


def test_check_promotion_ledger(tmp_path: Path):
    errors: list[str] = []
    warnings: list[str] = []
    inbox = tmp_path / "inbox"
    inbox.mkdir(parents=True)

    # Missing ledger
    res = cw.check_promotion_ledger(inbox, errors, warnings)
    assert res["ok"] is False
    assert len(errors) == 1

    # Valid ledger
    errors.clear()
    valid_row = {
        "schema": "promotion.v1",
        "ts": "2026-10-18T10:00:00Z",
        "source_path": "watch/inbox/test.md",
        "sha256": "123456",
        "dest_path": "tools/test.py",
        "promoted_by": "test-agent",
        "receipt_path": "watch/inbox/receipt.md",
    }
    ledger = inbox / "PROMOTION_LEDGER.jsonl"
    ledger.write_text(json.dumps(valid_row) + "\n", encoding="utf-8")

    res = cw.check_promotion_ledger(inbox, errors, warnings)
    assert res["ok"] is True
    assert res["count"] == 1
    assert len(errors) == 0
