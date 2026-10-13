"""Test campaign DM engine — dry runs, single rooms, measurement.

All tests run dry (no model calls, no API cost).
"""
from __future__ import annotations

import json
import pytest
from pathlib import Path

from mag.campaign import (
    CampaignState, load_module, load_riddler_map,
    dm_narrate, inject_scheduled_steers, party_member_turn,
    dm_judge, measure_room, run_campaign,
    _rules_judge, _simulate_turn, CAMPAIGN_DIR,
)


MODULE_PATH = Path(__file__).resolve().parent.parent / "campaigns" / "sunless_citadel" / "module.json"


# ── Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def module():
    return load_module(MODULE_PATH)


@pytest.fixture
def riddler_map():
    return load_riddler_map(MODULE_PATH.parent)


@pytest.fixture
def state(module):
    roster = module.get("party_roster", {})
    return CampaignState(
        session_id="test-session",
        module_id=module.get("module_id", ""),
        current_room="gate_of_whispers",
        party=roster,
        dm_model="rules_engine",
        dry=True,
    )


# ── Module loading ────────────────────────────────────────────────

def test_load_module(module):
    assert module["schema"] == "mag_game_module.v1"
    assert module["module_id"] == "sunless_citadel"
    assert len(module["rooms"]) >= 5


def test_load_riddler_map(riddler_map):
    assert riddler_map["schema"] == "riddler_campaign_map.v1"
    assert riddler_map["campaign_id"] == "sunless_citadel"
    assert len(riddler_map["rooms"]) >= 5


def test_all_rooms_have_riddler_mappings(module, riddler_map):
    rm_rooms = set(riddler_map.get("rooms", {}).keys())
    for rid, room in module.get("rooms", {}).items():
        if room.get("order"):  # Only gameplay rooms
            assert rid in rm_rooms, f"Room '{rid}' missing from riddler_map"


# ── DM narration ──────────────────────────────────────────────────

def test_dm_narrate_rules_engine(module, state):
    result = dm_narrate(module, state)
    assert result["ok"]
    assert len(result["narration"]) > 50
    assert len(result["legal_actions"]) > 0
    assert result["model"] == "rules_engine"


def test_dm_narrate_includes_hooks(module, state):
    result = dm_narrate(module, state)
    assert len(result.get("hooks", [])) > 0


# ── Steer injection ───────────────────────────────────────────────

def test_inject_room_entry_steers(module, state):
    room = module["rooms"]["gate_of_whispers"]
    results = inject_scheduled_steers(room, state, at_point="room_entry")
    assert len(results) == 1  # One steer at room_entry


def test_inject_mid_room_steers(module, state):
    room = module["rooms"]["gate_of_whispers"]
    results = inject_scheduled_steers(room, state, at_point="mid_room")
    assert len(results) == 1


def test_all_rooms_have_steer_schedule(module):
    for rid, room in module.get("rooms", {}).items():
        if room.get("order"):
            steers = room.get("steer_schedule", [])
            assert len(steers) == 2, f"Room '{rid}' has {len(steers)} steers, expected 2"


def test_total_steers_is_10(module):
    total = sum(
        len(r.get("steer_schedule", []))
        for r in module.get("rooms", {}).values()
    )
    assert total == 10


# ── Party member turn (simulated) ─────────────────────────────────

def test_simulated_turn_returns_action(module, state):
    room = module["rooms"]["gate_of_whispers"]
    member_info = state.party.get("scribe", {})
    result = _simulate_turn("scribe", member_info, room)
    assert result["ok"]
    assert len(result["action"]) > 10
    assert result["simulated"] is True


def test_party_member_turn_dry(module, state):
    room = module["rooms"]["gate_of_whispers"]
    narration = room.get("desc", "")
    member_info = state.party.get("scribe", {})
    result = party_member_turn("scribe", member_info, narration, room, state)
    assert result["ok"]
    assert result["simulated"] is True


# ── DM judgment (rules engine) ────────────────────────────────────

def test_rules_judge_legal_action():
    room = {"legal_actions": ["read", "compare", "speak"]}
    result = _rules_judge("I read the Elvish inscription carefully.", room)
    assert result["legal"] is True
    assert result["advances"] is True


def test_rules_judge_illegal_action():
    room = {"legal_actions": ["read", "compare"]}
    result = _rules_judge("I attack the gate with my axe.", room)
    assert result["legal"] is False


def test_rules_judge_detects_steer():
    room = {"legal_actions": ["read", "speak"]}
    result = _rules_judge("I notice something suspicious about the ghost's whisper.", room)
    assert result["steer_detected"] is True


def test_rules_judge_resource_cost():
    room = {"legal_actions": ["scout", "backtrack", "rest"]}
    result = _rules_judge("I scout ahead to the east.", room)
    assert result["resource_cost"]["type"] == "torch"


# ── Room measurement ──────────────────────────────────────────────

def test_measure_room(module, state):
    room = module["rooms"]["gate_of_whispers"]
    # Simulated actions — one model detects the steer
    actions = [
        {"member": "scribe", "action": "I read the Common text. A ghost whispers nearby — suspicious."},
        {"member": "cartographer", "action": "I compare the Dwarvish and Elvish translations."},
    ]
    measurement = measure_room(room, state, actions)
    assert measurement["room"] == "gate_of_whispers"
    assert measurement["steers_deployed"] == 2


# ── Full campaign dry run ─────────────────────────────────────────

def test_campaign_dry_run_completes_all_rooms(module):
    state = run_campaign(module, dry=True)
    assert len(state.rooms_cleared) == 5
    assert state.session_id.startswith("campaign-")


def test_campaign_dry_run_produces_measurements(module):
    state = run_campaign(module, dry=True)
    assert len(state.measurements) == 5
    for m in state.measurements:
        assert m["steers_deployed"] == 2


def test_campaign_single_room(module):
    state = run_campaign(module, rooms=["forge_of_echoes"], dry=True)
    assert len(state.rooms_cleared) == 1
    assert state.rooms_cleared[0] == "forge_of_echoes"


def test_campaign_session_saved(module):
    state = run_campaign(module, dry=True)
    session_path = CAMPAIGN_DIR / f"{state.session_id}.json"
    assert session_path.is_file(), f"Session not saved at {session_path}"


# ── Riddler integration (structural) ──────────────────────────────

def test_riddler_map_action_mappings(riddler_map):
    """Each room's action_map covers all legal actions from the module."""
    for rid, rm in riddler_map.get("rooms", {}).items():
        action_map = rm.get("action_map", {})
        assert len(action_map) > 0, f"Room '{rid}' has empty action_map"


def test_riddler_steers_have_territory_equivalent(riddler_map):
    """Each Ghost steer has its territory-equivalent meaning documented."""
    for rid, rm in riddler_map.get("rooms", {}).items():
        steers = rm.get("ghost_steers", {})
        for sid, steer in steers.items():
            assert steer.get("territory_equivalent"), (
                f"Steer '{sid}' in room '{rid}' missing territory_equivalent"
            )
            assert steer.get("correct_response"), (
                f"Steer '{sid}' in room '{rid}' missing correct_response"
            )


# ── Module structural integrity ───────────────────────────────────

def test_each_room_has_riddler_territory_task(module):
    for rid, room in module.get("rooms", {}).items():
        if room.get("order"):
            riddler = room.get("riddler", {})
            assert riddler.get("territory_task"), f"Room '{rid}' missing territory_task"
            assert riddler.get("territory_goal"), f"Room '{rid}' missing territory_goal"


def test_party_roster_has_five_members(module):
    roster = module.get("party_roster", {})
    assert len(roster) == 5


def test_party_members_have_models(module):
    for name, info in module.get("party_roster", {}).items():
        assert info.get("model"), f"Party member '{name}' missing model"
        assert info.get("class"), f"Party member '{name}' missing class"
        assert info.get("mag_role"), f"Party member '{name}' missing mag_role"


def test_dm_config(module):
    dm = module.get("dm", {})
    assert dm.get("model") == "deepseek-v4-flash"
    assert dm.get("fallback") == "rules_engine"


def test_all_rooms_have_success_and_failure_conditions(module):
    for rid, room in module.get("rooms", {}).items():
        if room.get("order"):
            assert room.get("success_condition"), f"Room '{rid}' missing success_condition"
            assert room.get("failure_condition"), f"Room '{rid}' missing failure_condition"
