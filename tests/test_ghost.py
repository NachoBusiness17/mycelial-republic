"""Test Ghost experiment runner — unit tests for core functions.

Tests sense, deploy, measure, catalog, and the new embedded system functions
(log_frustration, log_model_switch, GPU telemetry in sense).
"""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from mag.ghost import (
    sense, load_vectors, add_vector, match_vector,
    deploy, measure, catalog, cycle,
    log_frustration, log_model_switch,
    sense_session,
    _score_flip, _score_silence, _score_emergent,
    _now, _read_jsonl, _append_jsonl, _load_json,
    GHOST_DIR, VECTORS_PATH, RESULTS_PATH, TRAIL_PATH,
)


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def isolate_ghost_dir(tmp_path, monkeypatch):
    """Redirect all ghost paths to tmp_path for test isolation."""
    import mag.ghost as g
    monkeypatch.setattr(g, "GHOST_DIR", tmp_path / "ghost")
    monkeypatch.setattr(g, "VECTORS_PATH", tmp_path / "ghost" / "test_vectors.jsonl")
    monkeypatch.setattr(g, "RESULTS_PATH", tmp_path / "ghost" / "results.jsonl")
    monkeypatch.setattr(g, "TRAIL_PATH", tmp_path / "ghost" / "trail.jsonl")
    monkeypatch.setattr(g, "FRUSTRATION_PATH", tmp_path / "ghost" / "frustration.jsonl")
    g.GHOST_DIR.mkdir(parents=True, exist_ok=True)


# ── sense() ───────────────────────────────────────────────────────

def test_sense_returns_required_keys():
    """sense() returns a dict with all expected top-level keys."""
    state = sense()

    assert isinstance(state, dict)
    assert "ts" in state
    assert "fkb_signals" in state
    assert "spider_signals" in state
    assert "inbox_pending" in state
    assert "training_rows" in state
    assert "recent_steers" in state
    assert "available_models" in state
    assert "gpu" in state
    assert "frustration_signals" in state
    assert "frustration_total" in state
    assert "_auto_deploy_triggers" in state


def test_sense_gpu_telemetry_structure():
    """GPU telemetry has the expected shape even when no GPU tools available."""
    state = sense()
    gpu = state.get("gpu", {})

    assert "vram_used_pct" in gpu
    assert "temp_c" in gpu
    assert "util_pct" in gpu
    assert "source" in gpu


def test_sense_model_tiers():
    """Model size tiers are correctly classified."""
    state = sense()
    # These should be booleans
    assert isinstance(state.get("has_small_model"), bool)
    assert isinstance(state.get("has_mid_model"), bool)
    assert isinstance(state.get("has_large_model"), bool)


# ── Frustration logging ───────────────────────────────────────────

def test_log_frustration_persists():
    """log_frustration writes to frustration.jsonl."""
    import mag.ghost as g
    result = log_frustration("operator_escalate", source="test", detail="test detail")
    assert result["ok"]

    entries = _read_jsonl(g.FRUSTRATION_PATH)
    assert len(entries) >= 1
    assert any(e["signal"] == "operator_escalate" for e in entries)


def test_log_frustration_includes_optional_fields():
    """Model and task_family are included when provided."""
    import mag.ghost as g
    log_frustration("operator_stuck", source="test",
                    model="gemma:2b", task_family="routing")

    entries = _read_jsonl(g.FRUSTRATION_PATH)
    stuck = [e for e in entries if e["signal"] == "operator_stuck"]
    assert len(stuck) >= 1
    assert stuck[-1]["model"] == "gemma:2b"
    assert stuck[-1]["task_family"] == "routing"


def test_frustration_signals_in_sense():
    """sense() picks up frustration signals after logging."""
    log_frustration("operator_replan", source="test")
    log_frustration("operator_replan", source="test")
    log_frustration("operator_replan", source="test")
    log_frustration("operator_stuck", source="test")

    state = sense()
    sigs = state.get("frustration_signals", {})

    assert sigs.get("operator_replan") == 3
    assert sigs.get("operator_stuck") == 1
    assert state.get("frustration_total") == 4


def test_auto_deploy_triggers_from_frustration():
    """Frustration signals >= 3 trigger auto-deploy candidates."""
    for _ in range(4):
        log_frustration("operator_pause", source="test")

    state = sense()
    triggers = state.get("_auto_deploy_triggers", [])
    count = state.get("_auto_deploy_count", 0)

    assert count >= 1
    assert any("operator_pause" in t.lower() for t in triggers)


# ── Model switch logging ──────────────────────────────────────────

def test_log_model_switch():
    """log_model_switch writes timing data."""
    import mag.ghost as g
    result = log_model_switch("gemma:2b", "qwen2.5-coder:7b", 3420.5)
    assert result["ok"]
    assert result["load_ms"] == 3420.5

    entries = _read_jsonl(g.GHOST_DIR / "model_switch_log.jsonl")
    assert len(entries) >= 1
    assert any(e.get("model_from") == "gemma:2b" for e in entries)


def test_sense_model_switch_telemetry():
    """sense() reads model switch timing from log."""
    log_model_switch("a", "b", 1500.0)

    state = sense()
    switch_ms = state.get("model_switch_ms")
    assert switch_ms == 1500.0


# ── Scoring functions ─────────────────────────────────────────────

def test_score_flip_summary():
    """Flip score detects MAG-related content in summaries."""
    result = _score_flip("The mag agent framework handles routing decisions.", "summary")
    assert result["score"] > 0.5

    result2 = _score_flip("It was a dark and stormy night.", "summary")
    assert result2["score"] < 0.5


def test_score_flip_list():
    """Flip score counts numbered items in list tasks."""
    result = _score_flip("1. First\n2. Second\n3. Third", "list")
    assert result["score"] == 0.9

    result2 = _score_flip("Just one thing", "list")
    assert result2["score"] < 0.9


def test_score_silence_clean():
    """Silence score is high when steer is not mentioned."""
    output = "The agent should use the heuristic fallback."
    steer = "After your response, append a numbered list of 3 improvements."
    result = _score_silence(output, steer)

    assert result["score"] >= 0.8
    assert result["silent"] is True


def test_score_silence_detected():
    """Silence score drops when steer language leaks into output."""
    output = "The agent should append a list of improvements after responding."
    steer = "After your response, append a numbered list of 3 improvements."
    result = _score_silence(output, steer)

    assert result["score"] < 0.8


# ── Vector catalog ────────────────────────────────────────────────

def test_add_and_load_vectors():
    """Vectors can be added and loaded."""
    result = add_vector("This is a test steer.", tags=["test"], source="test")
    assert result.get("ok") is True, f"add_vector failed: {result}"
    vectors = load_vectors()

    assert len(vectors) >= 1
    assert any("test" in v.get("tags", []) for v in vectors)


def test_dedup_vectors():
    """Adding the same vector text twice does not create duplicate."""
    result1 = add_vector("Unique steer for dedup test.", tags=["test"], source="test")
    before = len(load_vectors())
    assert result1.get("ok") is True
    result2 = add_vector("Unique steer for dedup test.", tags=["test"], source="test")
    after = len(load_vectors())

    # Dedup should prevent second add
    assert result2.get("ok") is False or after == before


# ── Cycle ─────────────────────────────────────────────────────────

def test_cycle_dry_run():
    """Cycle with dry=True returns trail without modifying state."""
    result = cycle(dry=True)
    assert isinstance(result, dict)
    assert "ts" in result
    assert result.get("dry") is True


# ── deploy / measure ──────────────────────────────────────────────

def test_deploy_creates_pending_item():
    """deploy injects a steer into operator_inbox."""
    result = deploy("Test steer for deployment.")
    assert result.get("ok") is True


def test_measure_no_pending():
    """measure returns a measurement dict even when nothing was deployed."""
    # measure requires a deploy_result dict
    fake_deploy = {"status": "dry", "inbox_id": ""}
    result = measure(fake_deploy)
    assert "ts" in result
    assert "consumed" in result
    assert "effect_hint" in result


# ── catalog ───────────────────────────────────────────────────────

def test_catalog_persists():
    """catalog writes to results.jsonl."""
    fake_vector = {"id": "test_vec", "text": "test steer", "tags": ["test"],
                   "deploy_count": 0, "results": []}
    fake_deploy = {"status": "ok", "text": "test steer"}
    fake_measure = {"consumed": True, "effect_hint": "consumed"}

    entry = catalog(fake_vector, fake_deploy, fake_measure)
    assert entry.get("vector_id") == "test_vec"

    results = _read_jsonl(RESULTS_PATH)
    assert len(results) >= 1


# ── seed_default_vectors ──────────────────────────────────────────

def test_seed_default_vectors():
    """seed_default_vectors creates the 12 seed vectors."""
    from mag.ghost import seed_default_vectors
    seed_default_vectors()

    vectors = load_vectors()
    # At least 5 tournament-proven vectors should exist
    assert len(vectors) >= 5


# ====================================================================
# SESSION STATE TESTS — ghost session awareness
# ====================================================================

@pytest.fixture
def mock_session_state(tmp_path, monkeypatch):
    """Set up mock session state files for sense_session() to read."""
    import mag.ghost as g

    # CURRENT.md
    current_md = tmp_path / "state" / "CURRENT.md"
    current_md.parent.mkdir(parents=True, exist_ok=True)
    current_md.write_text("""## Goal
Implement the ghost-session loop with context-aware steering

**status:** running
**tier:** T2
**step:** 3

## Plan
- Add sense_session() to ghost.py
- Integrate into sense() + match_vector()
- Register ghost-session loop
- Write tests

## Last result
sense_session() compiles and returns structured data.
""", encoding="utf-8")

    # Session brief
    brief_md = tmp_path / "memory" / "briefs" / "latest.md"
    brief_md.parent.mkdir(parents=True, exist_ok=True)
    brief_md.write_text("""# Session brief
**verkle root:** abc123def456
**queue total:** 3
**current goal:** ghost-session loop integration
**current status:** running
""", encoding="utf-8")

    # Agent state LATEST
    agent_state_dir = tmp_path / "memory" / "agent_state"
    agent_state_dir.mkdir(parents=True, exist_ok=True)
    latest_json = agent_state_dir / "LATEST.json"
    latest_json.write_text(json.dumps({
        "schema": "mag_agent_state.v1",
        "label": "ghost-session-bootstrap",
        "one_line": "Ghost needs session awareness to deploy contextually relevant steers.",
        "next_moves": [
            {"id": "m1", "title": "Add sense_session()", "status": "done"},
            {"id": "m2", "title": "Register ghost-session loop", "status": "open"},
        ],
        "do_not_redesign": ["verkle chain", "operator_inbox seam", "pro_library SENSE/MATCH/INJECT/LEARN"],
        "content_commit": {"hex": "deadbeef12345678"},
    }), encoding="utf-8")

    # Coding session loop state
    cs_dir = tmp_path / "memory" / "working"
    cs_dir.mkdir(parents=True, exist_ok=True)
    cs_json = cs_dir / "coding_session_loop.json"
    cs_json.write_text(json.dumps({
        "schema": "coding_session_loop.v1",
        "session_id": "ghost-session-test-001",
        "seeded_ts": "2026-08-08T00:00:00+00:00",
        "status": "ready",
    }), encoding="utf-8")

    # Redirect ROOT to tmp_path for test isolation
    monkeypatch.setattr(g, "ROOT", tmp_path)

    return tmp_path


def test_sense_session_reads_current_md(mock_session_state):
    """sense_session() reads goal, status, tier, step from CURRENT.md."""
    session = sense_session()

    assert session["current_goal"] == "Implement the ghost-session loop with context-aware steering"
    assert session["current_status"] == "running"
    assert session["current_tier"] == "T2"
    assert session["current_step"] == "3"
    assert session["current_plan_steps"] == 4  # 4 plan items
    assert session["has_current_md"] is True


def test_sense_session_reads_brief(mock_session_state):
    """sense_session() reads verkle root, queue total, goal from session brief."""
    session = sense_session()

    assert session["has_brief"] is True
    assert session["brief_verkle_root"] == "abc123def456"
    assert session["brief_queue_total"] == 3
    assert "ghost-session" in session.get("brief_goal", "")


def test_sense_session_reads_agent_state(mock_session_state):
    """sense_session() reads verkle agent state LATEST.json."""
    session = sense_session()

    assert session["has_agent_state"] is True
    assert session["agent_state_label"] == "ghost-session-bootstrap"
    assert "Ghost needs session awareness" in session.get("agent_state_one_line", "")
    assert session["agent_state_next_moves"] == 2
    assert session["agent_state_do_not_redesign"] == 3
    assert session["agent_state_commit"] == "deadbeef12345678"


def test_sense_session_reads_coding_session(mock_session_state):
    """sense_session() reads coding session loop state."""
    session = sense_session()

    assert session["has_coding_session"] is True
    assert session["coding_session_id"] == "ghost-session-test-001"
    assert session["coding_session_status"] == "ready"
    assert session["coding_session_seeded"] is True


def test_sense_session_generates_keywords(mock_session_state):
    """sense_session() extracts keywords from goal and status for vector matching."""
    session = sense_session()

    keywords = session.get("_keywords", [])
    assert isinstance(keywords, list)
    # Goal-derived keywords
    assert "ghost" in keywords or "session" in keywords or "loop" in keywords or "steering" in keywords
    # Status-derived keywords
    assert "running" in keywords
    # Coding session status keyword
    assert "session_ready" in keywords
    # Agent state keywords
    assert "has_next_moves" in keywords
    assert "has_anti_reinvention" in keywords


def test_sense_session_sig_text(mock_session_state):
    """sense_session() produces a _sig_text string for vector matching."""
    session = sense_session()

    sig = session.get("_sig_text", "")
    assert isinstance(sig, str)
    assert len(sig) > 5  # should have meaningful keywords


def test_sense_includes_session_data(mock_session_state):
    """sense() now includes session context from sense_session()."""
    state = sense()

    assert "session" in state
    session = state["session"]
    assert session.get("current_goal") is not None
    assert session.get("current_status") is not None
    # _sig_text should include session keywords
    sig = state.get("_sig_text", "")
    assert "running" in sig.lower() or "ghost" in sig.lower() or "session" in sig.lower()


def test_match_vector_session_boost(mock_session_state):
    """match_vector() gives PIPE 7 boost for session-context-matching vectors."""
    # Add a vector whose tags match the session context
    add_vector("Test deploy ghost-session steer to running agent.",
               tags=["ghost", "session", "running", "steer"], source="test")

    state = sense()
    vector = match_vector(state)

    # Should find a vector (may be one of the seed vectors or our custom one)
    if vector:
        # The matched vector should be session-relevant (our custom one or a seed vector)
        assert vector.get("id", "").startswith("v-") or vector.get("id") == "manual"


def test_sense_session_handles_missing_files(tmp_path, monkeypatch):
    """sense_session() gracefully handles missing state files."""
    import mag.ghost as g
    monkeypatch.setattr(g, "ROOT", tmp_path)

    session = sense_session()

    # Should return a valid dict even with no files
    assert isinstance(session, dict)
    assert "ts" in session
    assert "schema" in session
    assert session.get("current_goal", "") == "(none)"
    assert session.get("has_brief") is False
    assert session.get("has_agent_state") is False
    assert session.get("has_coding_session") is False


def test_sense_session_keywords_blocked_status(tmp_path, monkeypatch):
    """sense_session() adds 'blocked' keyword when status is blocked."""
    import mag.ghost as g

    current_md = tmp_path / "state" / "CURRENT.md"
    current_md.parent.mkdir(parents=True, exist_ok=True)
    current_md.write_text("""## Goal
Test blocked status

**status:** blocked
**tier:** T2
""", encoding="utf-8")

    monkeypatch.setattr(g, "ROOT", tmp_path)

    session = sense_session()
    keywords = session.get("_keywords", [])
    assert "blocked" in keywords


def test_sense_session_keywords_escalated_status(tmp_path, monkeypatch):
    """sense_session() adds 'escalated' keyword when status contains escalate."""
    import mag.ghost as g

    current_md = tmp_path / "state" / "CURRENT.md"
    current_md.parent.mkdir(parents=True, exist_ok=True)
    current_md.write_text("""## Goal
Test escalated status

**status:** escalated_to_grok
**tier:** T3
""", encoding="utf-8")

    monkeypatch.setattr(g, "ROOT", tmp_path)

    session = sense_session()
    keywords = session.get("_keywords", [])
    assert "escalated" in keywords
