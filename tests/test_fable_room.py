"""Tests for mag/fable_room.py - the LAW-061 fable room (Primer endgame pour).

VERIFIER named by the organ's Consumer Law docstring. Falsifiers covered here:
exit blocked while the lying tile is unverified; fog tiles refuse to draw;
reader_state precedence cannot override vision_validated:false; the room is
solvable when every hash checks; identical inputs yield identical render bytes.
"""
from __future__ import annotations

import json

from mag import fable_room as fr


def _render_bytes(render: dict) -> str:
    return json.dumps(render, sort_keys=True, separators=(",", ":"))


def test_fnv1a32_known_vector():
    # same constant basis as shadow_walk's fnv1a32
    assert fr.fnv1a32("") == "811c9dc5"


def test_exit_blocked_while_liar_unverified():
    room = fr.build_law061_room()
    man = fr.law061_manifest()
    # the map paints the exit as gold; the floor refuses the foot
    walk = fr.walk_chamber(room, man, room["exit"])
    assert walk["ok"] is False
    assert walk["state"] == fr.MAP_LIE
    assert walk["map_hash"] != walk["floor_hash"]
    # and because the exit is the liar, the room cannot be solved as mapped
    solved = fr.solve_room(room, man)
    assert solved["solvable"] is False
    assert solved["blocked_at"] == room["exit"]
    assert solved["blocked_reason"] == fr.MAP_LIE
    render = fr.render_room(room, man, updated_utc="2026-10-19T00:00:00Z")
    assert render["exit_open"] is False


def test_fog_tiles_refuse_to_draw():
    room = fr.build_law061_room()
    man = fr.law061_manifest()
    render = fr.render_room(room, man)
    by_id = {c["id"]: c for c in render["chambers"]}
    # fog by absence: the floor never catalogued the tile
    absent = by_id["chamber_0_2"]
    assert absent["state"] == fr.FOG
    assert absent["drawn"] is False
    assert absent["claim"] is None
    # fog by vision gate: hash present but vision_validated:false
    ghost = by_id["chamber_1_2"]
    assert ghost["state"] == fr.FOG
    assert ghost["drawn"] is False
    assert ghost["claim"] is None
    # fog refuses the foot too
    assert fr.walk_chamber(room, man, "chamber_1_2")["ok"] is False
    assert render["summary"]["fog"] == 2


def test_reader_state_cannot_override_vision():
    room = fr.build_law061_room()
    man = fr.law061_manifest()
    rs = {
        "_schema_version": "reader_state.v1",
        "reader": "operator",
        "updated_utc": "2026-10-19T00:00:00Z",
        "attention_hints": ["chamber_1_2", "chamber_0_1"],
        "laws_in_focus": ["LAW-061"],
        "vision_precedence": True,
    }
    render = fr.render_room(room, man, reader_state=rs)
    by_id = {c["id"]: c for c in render["chambers"]}
    # the reader demanded the ghost gallery; the vision gate refused
    demanded_fog = by_id["chamber_1_2"]
    assert demanded_fog["state"] == fr.FOG
    assert demanded_fog["drawn"] is False
    assert demanded_fog["focus"] is False
    assert "refused" in demanded_fog["reader_refused"]
    # a validated chamber the reader demands does zoom into focus
    honest_focus = by_id["chamber_0_1"]
    assert honest_focus["focus"] is True
    assert honest_focus["drawn"] is True
    assert render["vision_precedence_enforced"] is True
    assert render["reader_state_applied"] is True


def test_law061_solvable_when_every_hash_checks():
    room = fr.build_law061_room()
    man = fr.law061_manifest(fog_absent=(), fog_unvalidated=())
    # the cure: fix the map from the floor (the floor never moved)
    fixed = fr.fix_map_from_floor(room, man)
    assert fixed["map_corrections"], "the liar chamber must be corrected"
    corrected = [c for c in fixed["chambers"] if c["id"] == room["exit"]][0]
    assert corrected["corrected_from_floor"] is True
    assert corrected["map_lie_original_hash"] != corrected["tile_hash"]
    solved = fr.solve_room(fixed, man)
    assert solved["solvable"] is True
    assert solved["path"][0] == room["entrance"]
    assert solved["path"][-1] == room["exit"]
    # and with every hash checking, every chamber walks and the exit opens
    for ch in fixed["chambers"]:
        assert fr.walk_chamber(fixed, man, ch["id"])["ok"] is True
    render = fr.render_room(fixed, man, updated_utc="2026-10-19T00:00:00Z")
    assert render["summary"]["verified"] == 9
    assert render["summary"]["map_lie"] == 0
    assert render["summary"]["fog"] == 0
    assert render["exit_open"] is True


def test_deterministic_output():
    man1 = fr.law061_manifest()
    man2 = fr.law061_manifest()
    rs = {
        "_schema_version": "reader_state.v1",
        "reader": "operator",
        "updated_utc": "2026-10-19T00:00:00Z",
        "attention_hints": [],
        "laws_in_focus": ["LAW-061"],
        "vision_precedence": True,
    }
    r1 = fr.render_room(fr.build_law061_room(), man1, reader_state=rs,
                        updated_utc="2026-10-19T00:00:00Z")
    r2 = fr.render_room(fr.build_law061_room(), man2, reader_state=rs,
                        updated_utc="2026-10-19T00:00:00Z")
    assert _render_bytes(r1) == _render_bytes(r2)


def test_load_reader_state_missing_file_is_empty_gate(tmp_path):
    missing = tmp_path / "nope.json"
    assert fr.load_reader_state(str(missing)) == {}
    p = tmp_path / "rs.json"
    p.write_text(json.dumps({"reader": "operator", "vision_precedence": True}),
                 encoding="utf-8")
    assert fr.load_reader_state(str(p))["reader"] == "operator"
