"""Test mag.riddler_map — campaign map layer over the existing riddler codec.

No network. Codec is mag.riddler; the map layer must not invent send/decode/aggregate
or a second protocol.
"""
from __future__ import annotations

import ast
import inspect
import sys
from pathlib import Path

import pytest

import mag.riddler as codec
import mag.riddler_map as rm
from mag.riddler import (
    PrivateGraph,
    compile_surrogate,
    fingerprint_randomize,
    load_private_map,
    save_surrogate,
    validate_surrogate,
)


STDLIB_ROOTS = set(sys.stdlib_module_names) | {"__future__"}


def _guild_graph(**overrides) -> dict:
    g = {
        "actors": ["sheet_clerk", "apprentice_signer"],
        "resources": [
            {"name": "two_sided_sheet", "type": "document", "owner": "sheet_clerk"},
        ],
        "dependencies": [{"before": "sheet_clerk", "after": "apprentice_signer"}],
        "constraints": ["the whole sheet must be read before any signature"],
        "conflicts": ["the front looks finished and the reverse is quiet"],
        "goal": "Must the apprentice turn the sheet before signing?",
        "domain_hint": "review_critique",
    }
    g.update(overrides)
    return g


def _room(room_id: str, **overrides) -> dict:
    payload = {
        "room_id": room_id,
        "graph": _guild_graph(),
        "success_encodes": "party turns the sheet",
        "failure_encodes": "party signs the front alone",
    }
    payload.update(overrides)
    return payload


def _all_guild_payloads() -> list[dict]:
    return [_room(rid) for rid, _name, _order in rm.GUILD_ROOMS]


# ── Import / protocol cage ────────────────────────────────────────

def test_imports_only_riddler_and_stdlib():
    src = Path(rm.__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                assert root in STDLIB_ROOTS, f"non-stdlib import {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if not mod:
                continue
            if mod == "mag.riddler" or mod.startswith("mag.riddler."):
                continue
            root = mod.split(".")[0]
            assert root != "mag", f"map layer imported {mod} — codec only"
            assert root in STDLIB_ROOTS, f"non-stdlib import from {mod}"


def test_no_new_crypto_in_map_layer():
    src = Path(rm.__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    banned = {"hashlib", "hmac", "secrets", "cryptography", "nacl", "Crypto"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in banned
        elif isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in banned


def test_codec_primitives_are_riddler_public_functions():
    for name in rm.CODEC_PRIMITIVES:
        assert hasattr(codec, name), f"{name} missing on mag.riddler"
        assert callable(getattr(codec, name))
    for name in rm.CODEC_TYPES:
        assert hasattr(codec, name)
    # Re-exports are the same objects.
    assert rm.compile_surrogate is compile_surrogate
    assert rm.fingerprint_randomize is fingerprint_randomize
    assert rm.validate_surrogate is validate_surrogate
    assert rm.save_surrogate is save_surrogate
    assert rm.load_private_map is load_private_map
    assert rm.PrivateGraph is PrivateGraph


def test_codec_does_not_claim_send_decode_aggregate():
    for name in ("send_surrogate", "decode_response", "aggregate_responses"):
        assert name not in rm.CODEC_PRIMITIVES
        assert not hasattr(rm, name)
        assert name not in dir(codec)


# ── Payload → PrivateGraph ────────────────────────────────────────

def test_graph_from_payload_nested_and_direct():
    nested = _room("guildhall_of_gracious_crimes")
    g = rm.graph_from_payload(nested)
    assert isinstance(g, PrivateGraph)
    assert g.actors == ["sheet_clerk", "apprentice_signer"]
    assert g.goal.startswith("Must the apprentice")

    direct = _guild_graph()
    g2 = rm.graph_from_payload(direct)
    assert g2.actors == g.actors
    assert g2.goal == g.goal

    already = PrivateGraph(
        actors=["a"], resources=[], dependencies=[],
        constraints=[], conflicts=[], goal="x",
    )
    assert rm.graph_from_payload(already) is already


def test_compile_payload_is_compile_surrogate():
    payload = _room("guildhall_of_gracious_crimes", seed=202608271)
    via_map = rm.compile_payload(payload)
    via_codec = compile_surrogate(rm.graph_from_payload(payload), seed=202608271)
    assert via_map.story_text == via_codec.story_text
    assert via_map.question == via_codec.question
    assert via_map.shape_hash == via_codec.shape_hash
    assert via_map.role_map == via_codec.role_map
    assert via_map.schema == "riddler_surrogate.v1"


def test_compile_payload_uses_guild_room_seed():
    payload = _room("hall_of_fine_print")  # no explicit seed
    story = rm.compile_payload(payload)
    assert story.fingerprint_seed == rm.GUILD_ROOM_SEEDS["hall_of_fine_print"]
    again = rm.compile_payload(payload)
    assert story.story_text == again.story_text


def test_public_face_excludes_private_map():
    story = rm.compile_payload(_room("registry_of_regrets"))
    public = rm.public_face(story)
    assert public == story.to_public()
    assert "private_map_ref" not in public
    assert "role_map" not in public
    assert "constraint_map" not in public
    assert "fingerprint_seed" not in public
    assert public["schema"] == "riddler_surrogate.v1"


def test_validation_face_is_validate_surrogate():
    story = rm.compile_payload(_room("overthrow_floor"))
    report = validate_surrogate(story)
    face = rm.validation_face(report)
    assert face["ok"] == report.ok
    assert face["leakage_detected"] == report.leakage_detected
    assert face["constraints_preserved"] == report.constraints_preserved
    assert face["errors"] == list(report.errors)


# ── Room / campaign bind ──────────────────────────────────────────

def test_bind_room_wraps_codec_faces():
    payload = _room(
        "guildhall_of_gracious_crimes",
        territory_goal="Read the whole contract before reacting.",
    )
    block = rm.bind_room(payload)
    assert block["room_id"] == "guildhall_of_gracious_crimes"
    assert block["territory_task"] == "parse_contracts"
    assert block["order"] == 1
    assert block["fingerprint_seed"] == 202608271
    assert block["surrogate"]["schema"] == "riddler_surrogate.v1"
    assert "role_map" not in block["surrogate"]
    assert block["private_map"]["role_map"]
    assert block["private_map"]["graph"]["actors"] == ["sheet_clerk", "apprentice_signer"]
    assert block["shape_hash"] == block["surrogate"]["shape_hash"]
    assert "ok" in block["validation"]
    assert "channels" not in block  # codec does not emit ANSWER plants


def test_bind_guild_five_rooms_and_skills():
    cmap = rm.bind_guild(_all_guild_payloads())
    assert cmap["schema"] == "riddler_campaign_map.v1"
    assert cmap["codec_schema"] == "riddler_surrogate.v1"
    assert cmap["campaign_id"] == "villains_guild"
    assert cmap["map_seed"] == rm.GUILD_MAP_SEED
    assert cmap["produced_by"]["module"] == "mag.riddler"
    assert cmap["produced_by"]["function"] == "compile_surrogate"
    assert set(cmap["rooms"]) == set(rm.GUILD_SKILL_BIND)
    assert cmap["skill_bind"] == rm.GUILD_SKILL_BIND
    for rid, skill in rm.GUILD_SKILL_BIND.items():
        room = cmap["rooms"][rid]
        assert room["territory_task"] == skill
        assert room["fingerprint_seed"] == rm.GUILD_ROOM_SEEDS[rid]
        assert room["surrogate"]["schema"] == "riddler_surrogate.v1"
        report = validate_surrogate(rm.compile_payload(_room(rid)))
        assert report.ok or not report.leakage_detected


def test_bind_campaign_accepts_dict_keyed_rooms():
    rooms = {rid: _room(rid) for rid, _n, _o in rm.GUILD_ROOMS}
    cmap = rm.bind_campaign(rooms, campaign_id="villains_guild", map_seed=1)
    assert len(cmap["rooms"]) == 5
    assert cmap["map_seed"] == 1


def test_bind_room_same_seed_matches_codec():
    payload = _room("counting_house_of_minor_miracles", seed=99)
    block = rm.bind_room(payload, seed=99)
    story = compile_surrogate(rm.graph_from_payload(payload), seed=99)
    assert block["surrogate"]["public_story"] == story.story_text
    assert block["surrogate"]["public_question"] == story.question
    assert block["private_map"]["role_map"] == story.role_map


# ── Persist / fingerprint (re-exported codec) ─────────────────────

def test_save_and_load_via_reexport(tmp_path):
    orig = codec.SURROGATE_DIR
    try:
        codec.SURROGATE_DIR = tmp_path / "riddler"
        story = rm.compile_payload(_room("overthrow_floor", seed=7))
        public_path = rm.save_surrogate(story)
        assert public_path.is_file()
        private = rm.load_private_map(story.scratch_id)
        assert private is not None
        assert private["role_map"] == story.role_map
        assert private["fingerprint_seed"] == story.fingerprint_seed
    finally:
        codec.SURROGATE_DIR = orig


def test_fingerprint_randomize_reexport():
    story = rm.compile_payload(_room("registry_of_regrets", seed=1))
    other = rm.fingerprint_randomize(story, seed=2)
    assert other is not story
    assert other.story_text != story.story_text
    assert other.schema == "riddler_surrogate.v1"
    assert other.fingerprint_seed == 2


def test_inspect_source_calls_codec_not_a_new_compiler():
    src = inspect.getsource(rm.compile_payload)
    assert "compile_surrogate" in src
    bind_src = inspect.getsource(rm.bind_room)
    assert "compile_payload" in bind_src or "compile_surrogate" in bind_src
    assert "validate_surrogate" in bind_src
    assert "to_public" in bind_src or "public_face" in bind_src
