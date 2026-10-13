#!/usr/bin/env python3
"""tests/test_description_pin.py — tests for tools/description_pin.py.

Covers the gate bar from the t11c ask (gala afterparty, mickey17 gate 3):
  - pinned description passes
  - unpinned and unmarked description fails, tool name named
  - PINNED-UNVERSIONED marker passes
  - missing description field fails (negatives first-class)
  - directory mode aggregates across manifests
  - malformed JSON is a finding, not a crash
  - exit codes: 0 iff clean, 2 on findings, 1 on usage error

Run: .venv/Scripts/python.exe -m pytest tests/test_description_pin.py -q
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))

from description_pin import (  # noqa: E402
    MARKER,
    findings_for_file,
    is_pinned,
    main,
)


def write_manifest(path: Path, doc) -> Path:
    path.write_text(json.dumps(doc), encoding="utf-8")
    return path


def test_pinned_description_passes(tmp_path):
    manifest = write_manifest(tmp_path / "tools.json", {"tools": [
        {"name": "scout", "description": "web scout pinned at v1.2"},
        {"name": "scribe", "description": "files notes (version 2.0.1)"},
    ]})
    assert findings_for_file(manifest) == []
    assert main([str(manifest)]) == 0


def test_unpinned_unmarked_fails_and_names_tool(tmp_path):
    manifest = write_manifest(tmp_path / "tools.json", {"tools": [
        {"name": "scout", "description": "web scout pinned at v1.2"},
        {"name": "rogue", "description": "searches the web for things"},
    ]})
    findings = findings_for_file(manifest)
    assert len(findings) == 1
    who, reason = findings[0]
    assert "rogue" in who
    assert "unpinned" in reason
    assert main([str(manifest)]) == 2


def test_marker_passes(tmp_path):
    manifest = write_manifest(tmp_path / "tools.json", {"tools": [
        {"name": "local_clock", "description":
            f"reads the host clock. {MARKER}: stdlib, no upstream releases"},
    ]})
    assert findings_for_file(manifest) == []
    assert main([str(manifest)]) == 0


def test_missing_description_field_is_a_finding(tmp_path):
    manifest = write_manifest(tmp_path / "tools.json",
                              {"tools": [{"name": "mute_tool"}]})
    who, reason = findings_for_file(manifest)[0]
    assert "mute_tool" in who
    assert "no description" in reason
    assert main([str(manifest)]) == 2


def test_directory_mode_aggregates(tmp_path):
    good = tmp_path / "good"
    bad = tmp_path / "bad"
    good.mkdir()
    bad.mkdir()
    write_manifest(good / "a.json", [{"name": "a1",
                                      "description": "alpha v3.1"}])
    write_manifest(bad / "b.json", {"tools": [{"name": "b1",
                                               "description": "beta tool"}]})
    assert main([str(tmp_path)]) == 2


def test_malformed_json_is_a_finding_not_a_crash(tmp_path):
    manifest = tmp_path / "broken.json"
    manifest.write_text("{not json", encoding="utf-8")
    who, reason = findings_for_file(manifest)[0]
    assert "broken.json" in who
    assert "unparsable" in reason
    assert main([str(manifest)]) == 2


def test_bare_list_and_name_keyed_shapes(tmp_path):
    bare = write_manifest(tmp_path / "bare.json",
                          [{"id": "x", "description": "x v0.9"}])
    keyed = write_manifest(tmp_path / "keyed.json",
                           {"y": {"description": "y tool, unpinned"}})
    assert findings_for_file(bare) == []
    assert "y" in findings_for_file(keyed)[0][0]


def test_is_pinned_boundaries():
    assert is_pinned("stable v2")
    assert is_pinned("1.0")
    assert is_pinned("build 1.2.3 upstream")
    assert is_pinned(f"none needed {MARKER.lower()}")
    assert not is_pinned("plain words only")
    assert not is_pinned("version: coming soon")
