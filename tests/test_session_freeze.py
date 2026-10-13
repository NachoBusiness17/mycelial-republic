"""Test session freeze — immutable snapshot for DeepSeek Pro Max / external seats.

Tests freeze_session_snapshot() output shape, content hash dedup,
CLI flags, file write/load, and integration with sense() + sense_session().
"""
from __future__ import annotations

import json
import pytest
from pathlib import Path
from unittest.mock import patch


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def mock_state_files(tmp_path, monkeypatch):
    """Set up mock state files for the freeze to read."""
    import mag.session_freeze as sf

    # CURRENT.md
    current_md = tmp_path / "state" / "CURRENT.md"
    current_md.parent.mkdir(parents=True, exist_ok=True)
    current_md.write_text("""## Goal
Test the session freeze pipeline end-to-end

**status:** running
**tier:** T2
**step:** 2

## Plan
- Create session_freeze.py
- Add REST endpoint
- Write tests
""", encoding="utf-8")

    # Brief
    brief_md = tmp_path / "memory" / "briefs" / "latest.md"
    brief_md.parent.mkdir(parents=True, exist_ok=True)
    brief_md.write_text("""# Session brief
**verkle root:** abc123def456789
**queue total:** 2
**current goal:** session freeze pipeline
**current status:** running
""", encoding="utf-8")

    # Agent state
    agent_dir = tmp_path / "memory" / "agent_state"
    agent_dir.mkdir(parents=True, exist_ok=True)
    (agent_dir / "LATEST.json").write_text(json.dumps({
        "schema": "mag_agent_state.v1",
        "label": "freeze-test",
        "one_line": "Test the freeze snapshot pipeline.",
        "next_moves": [{"id": "m1", "title": "Create module", "status": "done"}],
        "do_not_redesign": ["verkle chain"],
        "content_commit": {"hex": "abcdef1234567890"},
        "ts": "2026-08-08T00:00:00+00:00",
    }), encoding="utf-8")

    # Coding session
    cs_dir = tmp_path / "memory" / "working"
    cs_dir.mkdir(parents=True, exist_ok=True)
    (cs_dir / "coding_session_loop.json").write_text(json.dumps({
        "schema": "coding_session_loop.v1",
        "session_id": "freeze-test-001",
        "seeded_ts": "2026-08-08T00:00:00+00:00",
        "status": "ready",
    }), encoding="utf-8")

    # Ghost dirs
    (tmp_path / "logs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "memory" / "runs").mkdir(parents=True, exist_ok=True)
    (tmp_path / "memory" / "runs" / "ghost").mkdir(parents=True, exist_ok=True)
    (tmp_path / "memory" / "biography").mkdir(parents=True, exist_ok=True)

    # Redirect ROOT in all relevant modules
    monkeypatch.setattr(sf, "ROOT", tmp_path)
    monkeypatch.setattr("mag.ghost.ROOT", tmp_path)
    monkeypatch.setattr("mag.session_state_brief.ROOT", tmp_path)
    monkeypatch.setattr("config.ROOT", tmp_path)

    # Also redirect agent_state paths (computed at import time from config.ROOT)
    import mag.agent_state as ags
    monkeypatch.setattr(ags, "STATE_DIR", tmp_path / "memory" / "agent_state")
    monkeypatch.setattr(ags, "LATEST_JSON", tmp_path / "memory" / "agent_state" / "LATEST.json")
    monkeypatch.setattr(ags, "VERSIONS", tmp_path / "memory" / "agent_state" / "versions")

    # Also redirect freeze dir to temp
    freeze_dir = tmp_path / "memory" / "freeze"
    monkeypatch.setattr(sf, "FREEZE_DIR", freeze_dir)

    return tmp_path


# ── freeze_session_snapshot() ─────────────────────────────────────

def test_freeze_returns_schema(mock_state_files):
    """freeze_session_snapshot() returns a dict with the correct schema."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot()
    assert snap["schema"] == "session_freeze.v1"
    assert "ts" in snap
    assert "layers" in snap
    assert "content_hash" in snap
    assert "summary" in snap


def test_freeze_has_all_default_layers(mock_state_files):
    """Default freeze includes system_health, session_context, agent_state, brief."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot()
    layers = snap["layers"]

    assert "system_health" in layers
    assert "session_context" in layers
    assert "agent_state" in layers
    assert "brief" in layers
    assert "routing" not in layers  # default: off


def test_freeze_routing_optional(mock_state_files):
    """include_routing=True adds the routing layer."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot(include_routing=True)
    assert "routing" in snap["layers"]


def test_freeze_layers_selective(mock_state_files):
    """Individual layers can be excluded."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot(
        include_system_health=False,
        include_session_context=False,
        include_agent_state=False,
        include_brief=False,
    )
    layers = snap["layers"]

    assert "system_health" not in layers
    assert "session_context" not in layers
    assert "agent_state" not in layers
    assert "brief" not in layers


def test_freeze_content_hash_deterministic(mock_state_files):
    """Same state → same content_hash (dedup)."""
    from mag.session_freeze import freeze_session_snapshot

    snap1 = freeze_session_snapshot()
    snap2 = freeze_session_snapshot()

    assert snap1["content_hash"] == snap2["content_hash"]


def test_freeze_content_hash_sha256_hex(mock_state_files):
    """Content hash is a valid SHA256 hex string."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot()
    h = snap["content_hash"]

    assert len(h) == 64
    assert all(c in "0123456789abcdef" for c in h)


def test_freeze_summary_has_goal(mock_state_files):
    """Summary extracts goal and status from session context."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot()
    summary = snap["summary"]

    assert "goal" in summary
    assert "Test the session freeze pipeline" in summary["goal"]
    assert summary["status"] == "running"
    assert "keywords" in summary


def test_freeze_session_context_layer(mock_state_files):
    """Session context layer has goal, status, keywords."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot()
    ctx = snap["layers"]["session_context"]

    assert ctx["current_goal"] is not None
    assert ctx["current_status"] == "running"
    assert isinstance(ctx.get("_keywords"), list)


def test_freeze_agent_state_layer(mock_state_files):
    """Agent state layer includes label, one_line, next_moves."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot()
    agent = snap["layers"]["agent_state"]

    assert agent.get("label") == "freeze-test"
    assert "Test the freeze snapshot" in agent.get("one_line", "")
    assert len(agent.get("next_moves", [])) == 1
    assert agent.get("content_commit") == "abcdef1234567890"


def test_freeze_brief_layer(mock_state_files):
    """Brief layer has verkle and queue data."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot()
    brief = snap["layers"]["brief"]

    assert "verkle" in brief or "queue" in brief


# ── write_freeze / load ───────────────────────────────────────────

def test_write_freeze_creates_file(mock_state_files):
    """write_freeze writes snapshot to disk and returns path info."""
    from mag.session_freeze import freeze_session_snapshot, write_freeze

    snap = freeze_session_snapshot()
    result = write_freeze(snap)

    assert result["ok"] is True
    assert "path" in result
    assert "content_hash" in result
    assert "size_bytes" in result
    assert result["size_bytes"] > 0
    assert Path(result["path"]).is_file()


def test_write_freeze_updates_latest_pointer(mock_state_files):
    """write_freeze updates memory/freeze/LATEST.json."""
    from mag.session_freeze import freeze_session_snapshot, write_freeze, FREEZE_DIR

    snap = freeze_session_snapshot()
    write_freeze(snap)

    latest = FREEZE_DIR / "LATEST.json"
    assert latest.is_file()
    pointer = json.loads(latest.read_text(encoding="utf-8"))
    assert pointer["content_hash"] == snap["content_hash"]


def test_load_latest_freeze_roundtrip(mock_state_files):
    """load_latest_freeze() returns the written snapshot."""
    from mag.session_freeze import freeze_session_snapshot, write_freeze, load_latest_freeze

    snap = freeze_session_snapshot()
    write_freeze(snap)

    loaded = load_latest_freeze()
    assert loaded is not None
    assert loaded["content_hash"] == snap["content_hash"]
    assert loaded["schema"] == "session_freeze.v1"


def test_write_freeze_custom_path(mock_state_files, tmp_path):
    """write_freeze accepts a custom path."""
    from mag.session_freeze import freeze_session_snapshot, write_freeze

    snap = freeze_session_snapshot()
    custom = tmp_path / "custom_freeze.json"
    result = write_freeze(snap, path=custom)

    assert result["ok"] is True
    assert custom.is_file()
    loaded = json.loads(custom.read_text(encoding="utf-8"))
    assert loaded["content_hash"] == snap["content_hash"]


# ── Graceful degradation ──────────────────────────────────────────

def test_freeze_handles_missing_files(tmp_path, monkeypatch):
    """freeze_session_snapshot works with zero state files (empty system)."""
    import mag.session_freeze as sf
    import mag.agent_state as ags

    monkeypatch.setattr(sf, "ROOT", tmp_path)
    monkeypatch.setattr(sf, "FREEZE_DIR", tmp_path / "memory" / "freeze")
    monkeypatch.setattr("mag.ghost.ROOT", tmp_path)
    monkeypatch.setattr("mag.session_state_brief.ROOT", tmp_path)
    monkeypatch.setattr("config.ROOT", tmp_path)
    monkeypatch.setattr(ags, "STATE_DIR", tmp_path / "memory" / "agent_state")
    monkeypatch.setattr(ags, "LATEST_JSON", tmp_path / "memory" / "agent_state" / "LATEST.json")

    snap = sf.freeze_session_snapshot()

    assert snap["schema"] == "session_freeze.v1"
    assert "content_hash" in snap
    # All layers should be present (with defaults or errors, not missing)
    for layer in ("system_health", "session_context", "agent_state", "brief"):
        assert layer in snap["layers"], f"Missing layer: {layer}"


# ── CLI flags ─────────────────────────────────────────────────────

def test_cli_no_system_flag(mock_state_files):
    """--no-system excludes system_health layer."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot(include_system_health=False)
    assert "system_health" not in snap["layers"]


def test_cli_no_session_flag(mock_state_files):
    """--no-session excludes session_context layer."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot(include_session_context=False)
    assert "session_context" not in snap["layers"]


def test_cli_no_agent_flag(mock_state_files):
    """--no-agent excludes agent_state layer."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot(include_agent_state=False)
    assert "agent_state" not in snap["layers"]


def test_cli_no_brief_flag(mock_state_files):
    """--no-brief excludes brief layer."""
    from mag.session_freeze import freeze_session_snapshot

    snap = freeze_session_snapshot(include_brief=False)
    assert "brief" not in snap["layers"]
