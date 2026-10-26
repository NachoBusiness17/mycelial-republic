#!/usr/bin/env python3
"""fable_room.py - render ONE law as ONE walkable room (the Primer endgame pour).

Rows 1 + 5 of the delta table (research/gaming_corpus/primer_vs_fleet.md): the
fleet enforces its laws but nothing narrates them; this organ renders one law as
a small grid of chambers the reader can walk, fail in safely, and walk out of
understanding. First candidate LAW-061, the hallucinated-map law: the room where
the map lies to you and the floor checks your hash. LAW-061 is deliberately NOT
registered here - memory/law/registry.json promotion is operator-gated (the
operator gate is respected, not self-served, per
watch/inbox/GAME_CORPUS_SELF_STEAL_20261019.md section 4): this room NARRATES the
law, registration stays human.

CONSUMER: the operator (walks the room as a pedagogy exhibit) and the dashboard
room surfaces / THE ROOM exhibit pipeline - render_room() returns a JSON-able
dict a room surface can paint directly (no HTML emitted here, no network, $0).
The per-reader gate file this consults is state/shadow_work/reader_state.json,
sitting beside state/shadow_work/chunk_manifest.json per the same wiring map;
its falsifier is inherited from shadow_walk: a tile with vision_validated:false
must fail to draw even when reader_state demands it.

VERIFIER: tests/test_fable_room.py (exit blocked while the lying tile is
unverified; fog tiles refuse to draw; reader_state precedence cannot override
the vision gate; the room is solvable when every hash checks; renders are
byte-deterministic for identical inputs).

Integration notes: mag/room_state.py is a one-shot generator with no module
registry to join, so no registration touch was made anywhere. Wiring a surface =
import build_law061_room + law061_manifest + render_room / solve_room and paint
the returned dict. Determinism contract: no network, no clock reads, no RNG in
the core logic - every function is a pure function of its arguments; ISO stamps
enter only as the updated_utc argument at the render edge, so the same inputs
always yield the same room bytes. Hash continuity: the tile hash is the estate's
fnv1a32, the same implementation dashboard/static/_build_shadow_walk.py uses to
mint state/shadow_work/chunk_manifest.json (hash_algo "fnv1a32"), so a fable
tile and a shadow_walk chunk verify with one algorithm.
"""
from __future__ import annotations

import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
READER_STATE_PATH = os.path.join(ROOT, "state", "shadow_work", "reader_state.json")

SCHEMA_ROOM = "fable_room.v1"
SCHEMA_MANIFEST = "fable_room_manifest.v1"
SCHEMA_RENDER = "fable_room_render.v1"
READER_STATE_SCHEMA = "reader_state.v1"
HASH_ALGO = "fnv1a32"

VERIFIED = "VERIFIED"   # tile hash checks against the floor; draws and walks
FOG = "FOG"             # floor has no validated hash for the tile; refuses to draw
MAP_LIE = "MAP_LIE"     # the map's hash disagrees with the floor's hash

LAW_ID = "LAW-061"
LAW_NAME = "hallucinated_map"
ROOM_TITLE = "the room where the map lies and the floor checks your hash"
ROOM_LESSON = ("the map can lie; the hash cannot. "
               "fix the map from the floor, never the floor from the map.")
REGISTRATION_NOTE = ("LAW-061 narrated only; not registered in "
                     "memory/law/registry.json - law promotion is operator-gated.")

# (row, col, map_name, claim, floor_claim)
# floor_claim None means map and floor agree: the floor hash is fnv1a32(claim).
# The exit chamber (2,2) is the LAW-061 liar: the map paints gold there, the
# floor reads plain stone, so the two hashes can never agree until the map is
# rewritten from the floor (fix_map_from_floor).
_LAW061_CHAMBERS = (
    (0, 0, "THE HAND-OFF",
     "you are handed a map at the door and told the map is the estate",
     None),
    (0, 1, "THE APPEND-ONLY WALL",
     "the chain never rewrites history; it only appends sealed blocks",
     None),
    (0, 2, "THE UNMAPPED ANNEX",
     "the map draws a pantry here", None),
    (1, 0, "THE SEEN SLAB",
     "what the vision pass validated stays drawn; no hash, no draw",
     None),
    (1, 1, "THE CROSSROADS",
     "four doors, each stamped with a hash you can check by hand",
     None),
    (1, 2, "THE GHOST GALLERY",
     "the map sketches portraits here", None),
    (2, 0, "THE QUIET VAULT",
     "records outlive the seats that wrote them",
     None),
    (2, 1, "THE FLOORBOARDS",
     "under every tile is a hash; the tile can be repainted, the boards cannot",
     None),
    (2, 2, "THE TREASURY DOOR",
     "the map paints gold behind this door and calls it the way out",
     "the floor reads plain stone: this door opens only for a hash that checks"),
)

# Default fog design of the LAW-061 floor: one tile the floor never catalogued
# (fog by absence) and one tile the vision pass has not validated yet (fog by
# the vision gate). Both refuse to draw; both refuse the foot.
FOG_ABSENT = ("chamber_0_2",)
FOG_UNVALIDATED = ("chamber_1_2",)


# ---- the estate hash (same impl as dashboard/static/_build_shadow_walk.py) ----
def fnv1a32(text: str) -> str:
    """fnv1a32 hex string over utf-8 bytes; fnv1a32("") == "811c9dc5"."""
    h = 0x811C9DC5
    for b in text.encode("utf-8"):
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return "%08x" % h


# ---- builders (pure: fresh dicts every call, no module state mutated) ----
def build_law061_room() -> dict:
    """The LAW-061 room definition: a 3x3 grid of claim-tiles with one designed
    liar at the exit. Pure data; the lie lives in tile_hash vs the manifest."""
    chambers = []
    for row, col, name, claim, floor_claim in _LAW061_CHAMBERS:
        ch = {
            "id": "chamber_%d_%d" % (row, col),
            "row": row,
            "col": col,
            "tile_id": "tile_%d_%d" % (row, col),
            "map_name": name,
            "claim": claim,
            "tile_hash": fnv1a32(claim),
        }
        if floor_claim is not None:
            ch["floor_claim"] = floor_claim
            ch["map_note"] = ("the map paints this tile as the way out; "
                              "the floor disagrees")
        chambers.append(ch)
    return {
        "schema": SCHEMA_ROOM,
        "law_id": LAW_ID,
        "law_name": LAW_NAME,
        "title": ROOM_TITLE,
        "lesson": ROOM_LESSON,
        "registration_note": REGISTRATION_NOTE,
        "grid": {"rows": 3, "cols": 3},
        "entrance": "chamber_0_0",
        "exit": "chamber_2_2",
        "chambers": chambers,
    }


def law061_manifest(room: dict | None = None,
                    fog_absent=FOG_ABSENT,
                    fog_unvalidated=FOG_UNVALIDATED) -> dict:
    """The floor: the manifest the room's hashes verify against. Same shape
    family as state/shadow_work/chunk_manifest.json (content_hash +
    vision_validated per tile). Pass empty tuples for the all-hashes-check
    variant the solvability falsifier walks."""
    if room is None:
        room = build_law061_room()
    tiles = {}
    for ch in room["chambers"]:
        if ch["id"] in set(fog_absent):
            continue  # fog by absence: the floor never catalogued this tile
        text = ch.get("floor_claim", ch["claim"])
        entry = {
            "content_hash": fnv1a32(text),
            "vision_validated": ch["id"] not in set(fog_unvalidated),
        }
        tiles[ch["tile_id"]] = entry
    return {"schema": SCHEMA_MANIFEST, "hash_algo": HASH_ALGO, "tiles": tiles}


# ---- the walk (core logic: pure functions of arguments) ----
def _tile_verdict(chamber: dict, manifest: dict):
    """-> (state, reason) with state in {VERIFIED, FOG, MAP_LIE}."""
    tile = manifest.get("tiles", {}).get(chamber["tile_id"])
    if tile is None:
        return FOG, ("no hash in the floor manifest; "
                     "fog until the floor catalogues this tile")
    if not tile.get("vision_validated", False):
        return FOG, ("vision_validated:false; ghost until the vision pass "
                     "validates (no hash, no draw)")
    if chamber.get("tile_hash") != tile.get("content_hash"):
        return MAP_LIE, ("the map's hash does not match the floor's hash; "
                         "the floor never moved")
    return VERIFIED, "tile hash checks against the floor"


def _chamber_by_id(room: dict, chamber_id: str):
    for ch in room["chambers"]:
        if ch["id"] == chamber_id:
            return ch
    return None


def walk_chamber(room: dict, manifest: dict, chamber_id: str) -> dict:
    """Try to stand on one chamber. The floor checks the tile's hash against
    the manifest; fog refuses the foot; a lying tile refuses the foot."""
    ch = _chamber_by_id(room, chamber_id)
    if ch is None:
        return {"chamber": chamber_id, "ok": False,
                "state": None, "reason": "no such chamber in this room"}
    state, reason = _tile_verdict(ch, manifest)
    out = {"chamber": chamber_id, "tile_id": ch["tile_id"],
           "state": state, "reason": reason, "ok": state == VERIFIED}
    if state == MAP_LIE:
        tile = manifest["tiles"][ch["tile_id"]]
        out["map_hash"] = ch.get("tile_hash")
        out["floor_hash"] = tile.get("content_hash")
    return out


def solve_room(room: dict, manifest: dict) -> dict:
    """BFS from entrance over VERIFIED chambers (4-adjacency) to the exit.
    The exit itself must be VERIFIED: fog cannot be an exit, a lie cannot be
    an exit."""
    entrance, exit_id = room["entrance"], room["exit"]
    states = {ch["id"]: _tile_verdict(ch, manifest)[0] for ch in room["chambers"]}
    rows, cols = room["grid"]["rows"], room["grid"]["cols"]
    coords = {ch["id"]: (ch["row"], ch["col"]) for ch in room["chambers"]}
    by_coord = {(ch["row"], ch["col"]): ch["id"] for ch in room["chambers"]}

    if states.get(exit_id) != VERIFIED:
        return {"law_id": room.get("law_id"), "solvable": False, "path": [],
                "blocked_at": exit_id, "blocked_reason": states.get(exit_id),
                "entrance": entrance, "exit": exit_id}

    # BFS over walkable chambers
    came = {entrance: None}
    frontier = [entrance]
    while frontier:
        cur = frontier.pop(0)
        if cur == exit_id:
            break
        r, c = coords[cur]
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nid = by_coord.get((r + dr, c + dc))
            if nid and nid not in came and states.get(nid) == VERIFIED:
                came[nid] = cur
                frontier.append(nid)

    if exit_id not in came:
        return {"law_id": room.get("law_id"), "solvable": False, "path": [],
                "blocked_at": exit_id, "blocked_reason": "NO_VERIFIED_PATH",
                "entrance": entrance, "exit": exit_id}

    path, node = [], exit_id
    while node is not None:
        path.append(node)
        node = came[node]
    path.reverse()
    return {"law_id": room.get("law_id"), "solvable": True, "path": path,
            "blocked_at": None, "blocked_reason": None,
            "entrance": entrance, "exit": exit_id}


def fix_map_from_floor(room: dict, manifest: dict) -> dict:
    """The LAW-061 cure: rewrite the map from the floor, never the floor from
    the map. Lying tile hashes are corrected to the manifest hash and the
    original lie is kept on the chamber (append-only spirit: record, do not
    erase). Fog is left fog - the cure for fog is validation, not rewriting."""
    fixed = json.loads(json.dumps(room))
    corrections = []
    for ch in fixed["chambers"]:
        tile = manifest.get("tiles", {}).get(ch["tile_id"])
        if tile is None:
            continue
        if ch.get("tile_hash") != tile.get("content_hash"):
            corrections.append({"chamber": ch["id"],
                                "map_hash_was": ch.get("tile_hash"),
                                "floor_hash": tile.get("content_hash")})
            ch["map_lie_original_hash"] = ch.get("tile_hash")
            ch["tile_hash"] = tile.get("content_hash")
            ch["corrected_from_floor"] = True
    fixed["map_corrections"] = corrections
    return fixed


# ---- the render edge (the only place a stamp enters, passed in) ----
def render_room(room: dict, manifest: dict, reader_state: dict | None = None,
                updated_utc: str | None = None) -> dict:
    """Paint the room: one dict a dashboard room surface can draw. Fog chambers
    refuse to draw (claim hidden, drawn False) no matter what reader_state
    demands; vision validity outranks reader state, always."""
    hints = list((reader_state or {}).get("attention_hints", []))
    precedence_demanded = bool((reader_state or {}).get("vision_precedence"))

    chamber_renders = []
    counts = {VERIFIED: 0, FOG: 0, MAP_LIE: 0}
    for ch in room["chambers"]:
        state, reason = _tile_verdict(ch, manifest)
        counts[state] += 1
        entry = {
            "id": ch["id"],
            "row": ch["row"],
            "col": ch["col"],
            "map_name": ch["map_name"],
            "state": state,
            "drawn": state == VERIFIED,
            "claim": ch["claim"] if state != FOG else None,
            "verdict": reason,
        }
        if state == MAP_LIE:
            tile = manifest["tiles"][ch["tile_id"]]
            entry["map_hash"] = ch.get("tile_hash")
            entry["floor_hash"] = tile.get("content_hash")
        if ch["id"] in hints:
            if state == VERIFIED:
                entry["focus"] = True
            else:
                entry["focus"] = False
                entry["reader_refused"] = (
                    "reader_state demanded this chamber; the vision gate "
                    "refused (%s)" % state)
        chamber_renders.append(entry)

    walk = solve_room(room, manifest)
    return {
        "schema": SCHEMA_RENDER,
        "law_id": room.get("law_id"),
        "law_name": room.get("law_name"),
        "title": room.get("title"),
        "lesson": room.get("lesson"),
        "registration_note": room.get("registration_note"),
        "updated_utc": updated_utc,
        "reader": (reader_state or {}).get("reader"),
        "reader_state_applied": bool(reader_state),
        "vision_precedence_enforced": precedence_demanded,
        "attention_hints": hints,
        "grid": room["grid"],
        "entrance": room["entrance"],
        "exit": room["exit"],
        "exit_open": bool(walk["solvable"]),
        "chambers": chamber_renders,
        "summary": {"verified": counts[VERIFIED], "fog": counts[FOG],
                    "map_lie": counts[MAP_LIE]},
        "walk": walk,
    }


# ---- file edge (IO only; no clock, no network) ----
def load_reader_state(path: str | None = None) -> dict:
    """Load the per-reader gate file (state/shadow_work/reader_state.json).
    Missing file reads as an empty gate: {} - vision validity still gates."""
    p = path or READER_STATE_PATH
    if not os.path.exists(p):
        return {}
    with open(p, encoding="utf-8") as f:
        return json.load(f)
