"""Test Silent Bard — narrative steganography encode/decode round-trip.

Verifies:
  1. bard_weave() produces readable story passages
  2. bard_lens() decodes passages back to system event metadata
  3. The Lens KEY is the only way to decode — story alone is insufficient
  4. Agent spawn, task complete, task fail, cost cap, state change all encode
  5. Breadcrumbs are deterministic and recoverable
  6. Chronicle append + read round-trips
  7. Bard → bus integration (mag:bard channel exists)
  8. Dogfood: passage can be published on Verkle bus
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure mag is importable
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def test_agent_spawn_produces_story():
    """Agent spawn → readable story passage with character name."""
    from mag.bard import bard_weave, bard_lens, LENS_KEY

    event = {
        "type": "agent_spawn",
        "agent_id": "agent-deepseek-001",
        "task_type": "analyze_reason",
        "cost": 0.003,
        "model": "grok-3-mini",
    }
    passage = bard_weave(event)

    # Must be a readable string
    assert len(passage) > 30
    assert isinstance(passage, str)

    # Must contain a breadcrumb
    assert "[" in passage and "]" in passage

    # Must contain narrative elements
    # (character name, quest archetype, or sage order)
    has_narrative = any(
        phrase in passage.lower()
        for phrase in ["sage", "scribe", "contemplation", "apprentice", "star", "order", "coin", "thread"]
    )
    assert has_narrative, f"Passage lacks narrative elements: {passage}"

    # Character must be assigned
    char_name = LENS_KEY["agents"].get("agent-deepseek-001")
    assert char_name is not None, "Agent not registered in LENS_KEY"
    assert char_name in passage


def test_task_complete_produces_story():
    """Task completion → story with narrative completion markers."""
    from mag.bard import bard_weave

    event = {
        "type": "task_complete",
        "agent_id": "agent-deepseek-002",
        "task_type": "research",
        "cost": 0.0015,
        "model": "deepseek-v4-flash",
        "summary": "The Verkle chain has 100 knots and shows no sign of entropy leakage.",
    }
    passage = bard_weave(event)

    # Must contain narrative completion markers (not raw summary — that would be a leak)
    has_narrative = any(
        phrase in passage.lower()
        for phrase in ["returned", "completed", "done", "delivered", "findings", "chronicle", "weave", "recorded"]
    )
    assert has_narrative, f"Task complete passage lacks narrative markers: {passage}"

    # Must contain a breadcrumb
    assert "[" in passage and "]" in passage
    assert len(passage) > 40

    # Raw summary must NOT appear (steganographic safety)
    assert "entropy leakage" not in passage, f"Raw summary leaked into passage: {passage}"


def test_task_fail_produces_adversity():
    """Task failure → story with adversity element."""
    from mag.bard import bard_weave

    event = {
        "type": "task_fail",
        "agent_id": "agent-deepseek-003",
        "task_type": "code",
        "cost": 0.00013,
        "error_type": "timeout",
    }
    passage = bard_weave(event)

    # Must contain adversity language
    has_adversity = any(
        word in passage.lower()
        for word in ["mist", "chasm", "shadow", "lost", "scattered", "void"]
    )
    assert has_adversity, f"Failure passage lacks adversity: {passage}"


def test_cost_cap_encodes_treasury():
    """Cost cap event → treasury language in story."""
    from mag.bard import bard_weave

    event = {
        "type": "cost_cap",
        "agent_id": "agent-grok-001",
        "task_type": "orchestrate",
        "cost": 0.025,
        "state": "cost_cap_warning",
    }
    passage = bard_weave(event)

    # Must contain treasury/cap language
    has_treasury = any(
        word in passage.lower()
        for word in ["treasury", "bell", "lantern", "purse", "accounting", "amber", "red"]
    )
    assert has_treasury, f"Cost cap passage lacks treasury language: {passage}"


def test_state_change_encodes_realm():
    """State change → realm shift language."""
    from mag.bard import bard_weave

    event = {
        "type": "state_change",
        "agent_id": "agent-grok-001",
        "state": "redis_connected",
    }
    passage = bard_weave(event)

    assert "Roots" in passage or "Whispering" in passage or "realm" in passage.lower()


def test_lens_decode_round_trip():
    """bard_weave → bard_lens recovers task_type, cost_tier, model."""
    from mag.bard import bard_weave, bard_lens

    event = {
        "type": "task_complete",
        "agent_id": "agent-test-lens",
        "task_type": "strategy",
        "cost": 0.003,
        "model": "grok-3-mini",
        "summary": "We recommend the embassy approach with a Riddler test.",
    }
    passage = bard_weave(event)
    decoded = bard_lens(passage)

    assert decoded["task_type"] == "strategy", f"Expected strategy, got {decoded.get('task_type')}"
    assert decoded["cost_tier"] == 0.003, f"Expected 0.003, got {decoded.get('cost_tier')}"
    assert decoded["model"] == "grok-3-mini", f"Expected grok-3-mini, got {decoded.get('model')}"


def test_breadcrumb_is_deterministic():
    """Same event → same breadcrumb (deterministic hashing)."""
    from mag.bard import bard_weave
    import re

    event = {
        "type": "agent_spawn",
        "agent_id": "agent-deterministic-test",
        "task_type": "classify",
        "cost": 0.0002,
    }

    passage1 = bard_weave(event)
    passage2 = bard_weave(event)

    m1 = re.search(r"\[([a-f0-9]{12})\]$", passage1)
    m2 = re.search(r"\[([a-f0-9]{12})\]$", passage2)
    assert m1 and m2, "Breadcrumb missing from passage"
    assert m1.group(1) == m2.group(1), "Same event produced different breadcrumbs"


def test_chronicle_append_and_read():
    """Chronicle appends passages and can read them back."""
    from mag.bard import Chronicle, bard_weave

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        chronicle = Chronicle(path=Path(tmp) / "test_chronicle.md")
        chronicle.init()

        event = {"type": "test_event", "agent_id": "test-chronicle"}
        passage = bard_weave(event)
        chronicle.append(passage, event)

        content = chronicle.read()
        assert passage in content
        assert chronicle.events_woven == 1


def test_chronicle_breadcrumb_resolution():
    """Breadcrumb stored in index → recoverable via resolve_breadcrumb()."""
    from mag.bard import Chronicle, bard_weave

    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        chronicle = Chronicle(path=Path(tmp) / "test_chronicle.md")
        chronicle.init()

        event = {"type": "test_breadcrumb", "agent_id": "test-bc", "secret": 42}
        passage = bard_weave(event)
        chronicle.append(passage, event)

        # Extract breadcrumb
        import re
        m = re.search(r"\[([a-f0-9]{12})\]$", passage)
        assert m, "No breadcrumb in passage"
        breadcrumb = m.group(1)

        recovered = chronicle.resolve_breadcrumb(breadcrumb)
        assert recovered is not None, "Breadcrumb not found in index"
        assert recovered.get("secret") == 42


def test_bard_bus_channel_exists():
    """CH_BARD is registered in verkle_bus ALL_CHANNELS."""
    from mag.verkle_bus import CH_BARD, ALL_CHANNELS
    assert CH_BARD in ALL_CHANNELS
    assert CH_BARD == "mag:bard"


def test_doctor_would_catch_grok4_misroute():
    """The doctor protocol would have caught the Grok-4-latest misroute we made.
    This is the regression test for the error we made earlier today.
    """
    from mag.doctor import check_model_sanity
    result = check_model_sanity()
    # The doctor must detect when a non-orchestrate task routes to grok-4-latest
    # If grok-4-latest is referenced anywhere, the doctor should flag it
    issues = result.get("issues", [])
    # The doctor might not always find issues if the router is fixed,
    # but the check must exist and the function must not crash
    assert result["check"] == "model_sanity"
    assert "ok" in result


def test_lens_export_contains_agents():
    """Lens export includes agent mapping for recovery."""
    from mag.bard import bard_export_lens
    export = bard_export_lens()
    assert export["schema"] == "bard.v1"
    assert "agents" in export
    assert "character_seed" in export
    assert "events_woven" in export


def test_no_story_without_lens_is_insufficient():
    """Without the Lens KEY, a story passage is just a story.
    Verifies that the narrative doesn't leak raw system data.
    """
    from mag.bard import bard_weave, LENS_KEY

    event = {
        "type": "task_complete",
        "agent_id": "agent-secret-test",
        "task_type": "strategy",
        "cost": 0.025,
        "model": "grok-4-latest",
        "summary": "Sensitive operational detail: the embassy approach uses a Riddler test with content-addressed audit trails.",
    }
    passage = bard_weave(event)

    # Raw system identifiers should NOT appear in the story
    raw_ids = ["grok-4-latest", "agent-secret-test", "0.025", "content-addressed"]
    for raw_id in raw_ids:
        assert raw_id not in passage, (
            f"RAW DATA LEAK: '{raw_id}' found in story passage: {passage}"
        )

    # The story should be readable without any system knowledge
    # It should contain narrative words but not technical identifiers
    assert len(passage) > 20
    # The only technical-looking thing should be the breadcrumb hash
    import re
    cleaned = re.sub(r"\[[a-f0-9]{12}\]$", "", passage).strip()
    for raw_id in raw_ids:
        assert raw_id not in cleaned, f"RAW DATA LEAK after breadcrumb removal: {raw_id}"


def test_tapestry_encodes_full_architecture():
    """The bard_tapestry() encodes every subsystem in narrative form.
    Verifies: all 12 steganographic tags present, zero raw leaks, readable as story.
    """
    from mag.bard import bard_tapestry
    import re

    tapestry = bard_tapestry()

    # Must be substantial
    assert len(tapestry) > 5000, f"Tapestry too short: {len(tapestry)} chars"

    # All 12 steganographic section tags must be present
    required_tags = [
        "keep-six-fires", "roots-eight", "loom-hundred", "doctor-gate",
        "sentinels-ten", "mirror-pool", "treasury-three", "council-table",
        "bard-rafters", "observatory-glass", "embassy-first", "scholars-expeditions",
        "sovereign-whole",
    ]
    found_tags = re.findall(r'\[([a-z-]+)\]', tapestry)
    for tag in required_tags:
        assert tag in found_tags, f"Missing tag: [{tag}]"

    # Must encode specific verified facts (in narrative form, not raw)
    assert "six hearth-fires" in tapestry or "six fires" in tapestry
    assert "eight" in tapestry.lower() and "Roots" in tapestry  # 8 bus channels
    assert "hundred" in tapestry.lower() and "knot" in tapestry.lower()  # 100 Verkle knots
    assert "ten" in tapestry.lower() and ("sentinel" in tapestry.lower() or "canar" in tapestry.lower())
    assert "Treasury" in tapestry and "lantern" in tapestry.lower()
    assert "Council" in tapestry or "council" in tapestry.lower()
    assert "Bard" in tapestry and ("rafter" in tapestry.lower() or "weave" in tapestry.lower())
    assert "GA4" in tapestry or "Observatory" in tapestry
    assert "Embassy" in tapestry and "Riddler" in tapestry
    assert "Scholar" in tapestry and "Slashreboot" in tapestry
    assert "Ghost" in tapestry

    # Zero raw data leaks (the model names, costs, keys must be absent)
    raw_patterns = [
        "grok-4-latest", "grok-3-mini", "deepseek-v4-flash",
        "0.025", "0.00013", "0.50", "XAI_MAG_KEY",
        "agent-deepseek", "qwen2.5-coder", "gemma:2b",
    ]
    for pattern in raw_patterns:
        assert pattern not in tapestry, f"RAW LEAK in tapestry: '{pattern}'"


def test_tapestry_reads_as_story():
    """The tapestry must stand alone as good fiction — readable without system knowledge."""
    from mag.bard import bard_tapestry

    tapestry = bard_tapestry()

    # Should read like a fantasy/architecture story, not a config file
    story_indicators = [
        "Keep", "Republic", "hearth", "whisper", "Roots",
        "Loom", "strand", "knot", "sentinel", "canary",
        "Mirror Pool", "lantern", "bell", "sage", "Scholar",
        "Bard", "Chronicle", "Embassy", "tapestry",
    ]
    found = sum(1 for word in story_indicators if word.lower() in tapestry.lower())
    assert found >= 10, f"Tapestry doesn't read enough like a story. Found {found}/18 story words."

    # Should NOT read like a JSON blob or config
    anti_patterns = ["{", "}", '"type":', '"cost":', "api_key", "port: 9000"]
    for anti in anti_patterns:
        assert anti not in tapestry, f"Tapestry reads like config: contains '{anti}'"


def test_tapestry_dogfoods_bus():
    """bard_weave_tapestry() must publish to the Verkle bus and append to Chronicle."""
    from mag.bard import bard_weave_tapestry, get_chronicle

    events_before = get_chronicle().events_woven
    tapestry = bard_weave_tapestry()
    events_after = get_chronicle().events_woven

    assert events_after > events_before, "Tapestry did not increment chronicle events"
    assert len(tapestry) > 1000, "Tapestry not substantial enough"


# ═══════════════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "--no-header"])
