"""UF-01 innkeeper tests (LW8, 2026-09-30).

Laws under test (receipt watch/inbox/last_mile_20260930/LW8_INNKEEPER.md):
  - the ike3 seam: the innkeeper is a REAL session - roster row, snapshot
    visible, at the spring - with no socket anywhere
  - greet on join: known players hear exactly
    "Welcome back, <name> - the spring is at <N> units"; first-timers hear
    the no-back variant; known players with a ledger history hear what they
    did ("Last visit you tagged <k> fish, <name>.")
  - water-state comment: crown tiers vs win_crown, e.g. crown 2 of 4 is
    exactly "The crown is half full."; cadence is tick % 8 or any
    water-moving player action, never RNG
  - motion rows: idle mostly, dance only when a player tags a fish at the
    innkeeper's node (honest co-location; the world has no coordinates);
    every emitted row is legal in the X9 MOTION_TABLE dialect
  - the LW6 say law: non-empty str, cap 240, one typed reject BAD_TEXT
  - memories persist across sessions (new world + new actor, same JSON
    file) and the file is fail-closed on corruption
  - decide() is pure: identical inputs give identical rows, inputs are
    never mutated
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from server.innkeeper import (  # noqa: E402
    BAD_TEXT,
    INNKEEPER_NODE,
    INNKEEPER_SID,
    INNKEEPER_USER,
    Innkeeper,
    PlayerMemories,
    crown_tier,
    decide,
    parse_ledger_event,
    say_law,
    say_row,
)
from server.protocol_table import MOTION_DISPATCH  # noqa: E402
from server.world import MountainWorld  # noqa: E402


def said(rows: dict) -> list[str]:
    return [r["text"] for r in rows["say"] if r.get("verb") == "say"]


def motion_verbs(rows: dict) -> list[str]:
    return [r["verb"] for r in rows["motion"] if "verb" in r]


# ------------------------------------------------------------ say law ----

def test_say_law_cap_and_shape():
    ok, why = say_law("x" * 240)
    assert (ok, why) == (True, None)
    for bad in ("x" * 241, "", None, 7, ["hi"]):
        assert say_law(bad) == (False, BAD_TEXT)
    row = say_row(INNKEEPER_SID, "x" * 240)
    assert row == {"verb": "say", "sid": INNKEEPER_SID, "text": "x" * 240}
    rej = say_row(INNKEEPER_SID, "x" * 241)
    assert rej == {"op": "reject", "why": BAD_TEXT, "verb": "say"}


# ------------------------------------------------------ ledger parsing ----

def test_parse_ledger_event_grammar():
    assert parse_ledger_event("ada joins at spring.") == {
        "user": "ada", "verb": "join", "target": "spring"}
    assert parse_ledger_event("ada tags a fish at hollow (score 3).") == {
        "user": "ada", "verb": "tag", "target": "hollow", "score": 3}
    assert parse_ledger_event("boiler boils 1 at spring; it rises.") == {
        "user": "boiler", "verb": "boil", "target": "spring", "rose": True}
    assert parse_ledger_event(
        "boiler boils at spring: pool went dry between ask and tick.") == {
        "user": "boiler", "verb": "boil", "target": "spring", "rose": False}
    assert parse_ledger_event("boiler shuts p_out.") == {
        "user": "boiler", "verb": "valve", "target": "p_out", "open": False}
    assert parse_ledger_event("boiler opens p_bypass.") == {
        "user": "boiler", "verb": "valve", "target": "p_bypass", "open": True}
    # physics lines are not player actions
    assert parse_ledger_event("Steam condenses at crown (+1).") is None
    assert parse_ledger_event("") is None


# ------------------------------------------------------------- brain ----

def _state(tick: int, nodes: dict, events: list[str] | None = None,
           win_crown: int = 4) -> dict:
    return {"tick": tick, "nodes": nodes, "roster": {}, "scores": {},
            "events": events or [], "win_crown": win_crown}


def test_water_state_comment_crown_half_full():
    rows = decide(8, _state(8, {"spring": 6, "crown": 2}), {})
    assert rows["say"] == [
        {"verb": "say", "sid": INNKEEPER_SID, "text": "The crown is half full."}]


def test_water_state_comment_tiers_and_cadence():
    assert crown_tier(4, 4) == "The crown is full."
    assert crown_tier(3, 4) == "The crown is half full."
    assert crown_tier(2, 4) == "The crown is half full."
    assert crown_tier(1, 4) == "The crown is barely wet."
    assert crown_tier(0, 4) == "The crown is dry."
    # off-cadence, no player water action, no joins: the innkeeper is quiet
    rows = decide(3, _state(3, {"spring": 6, "crown": 0}), {})
    assert rows["say"] == [] and rows["memory"] == {}
    # but a player moving water pulls the comment off cadence
    rows = decide(
        3, _state(3, {"spring": 5, "crown": 0},
                  ["boiler shuts p_spring."]), {})
    assert said(rows) == ["The crown is dry."]
    assert rows["memory"] == {"boiler": {"last_action": "shut p_spring"}}


def test_greet_on_join_known_and_first_time():
    mem = {"ada": {"visits": 2, "last_action": "tagged a fish at hollow",
                   "fish_tagged": 3}}
    rows = decide(1, _state(1, {"spring": 6, "crown": 0},
                            ["ada joins at spring."]), mem)
    assert said(rows) == [
        "Welcome back, ada - the spring is at 6 units",
        "Last visit you tagged 3 fish, ada.",
    ]
    assert rows["memory"]["ada"]["visits"] == 1  # delta, not the total
    # first-timer: no back, no ledger gossip
    rows = decide(1, _state(1, {"spring": 4, "crown": 0},
                            ["neo joins at terrace."]), mem)
    assert said(rows) == ["Welcome, neo - the spring is at 4 units"]


def test_motion_idle_mostly_dance_on_nearby_tag():
    idle = decide(2, _state(2, {"spring": 6, "crown": 0}), {})
    assert motion_verbs(idle) == ["idle"]
    assert idle["motion"][0]["dir"] == INNKEEPER_NODE
    # a tag at the innkeeper's node is nearby (co-location, no coordinates)
    dance = decide(2, _state(2, {"spring": 6, "crown": 0},
                             ["ada tags a fish at spring (score 1)."]), {})
    assert motion_verbs(dance) == ["dance"]
    # a tag elsewhere is not nearby
    far = decide(2, _state(2, {"spring": 6, "hollow": 2, "crown": 0},
                           ["ada tags a fish at hollow (score 1)."]), {})
    assert motion_verbs(far) == ["idle"]
    assert far["memory"]["ada"] == {
        "fish_tagged": 1, "last_action": "tagged a fish at hollow"}


def test_decide_is_pure_and_deterministic():
    mem = {"ada": {"visits": 1, "last_action": "joined at spring",
                   "fish_tagged": 2}}
    state = _state(8, {"spring": 6, "crown": 2},
                   ["ada joins at spring.", "ada tags a fish at spring (score 3)."])
    mem_before, state_before = copy.deepcopy(mem), copy.deepcopy(state)
    first = decide(state["tick"], state, mem)
    second = decide(state["tick"], state, mem)
    assert first == second
    assert mem == mem_before and state == state_before  # zero mutation
    # tick drives variety: another tick, another idle intensity
    other = decide(9, _state(9, {"spring": 6, "crown": 2}), {})
    assert other["motion"][0]["intensity_q8"] != first["motion"][0]["intensity_q8"]


# -------------------------------------------------------- memories file ----

def test_player_memories_persist_across_sessions(tmp_path: Path):
    path = tmp_path / "players.json"
    a = PlayerMemories(path)
    a.apply({"ada": {"visits": 1, "fish_tagged": 2,
                     "last_action": "tagged a fish at spring"}})
    a.save()
    b = PlayerMemories(path)  # a whole new session, same file
    assert b.known("ada")
    assert b.get("ada") == {"visits": 1, "fish_tagged": 2,
                            "last_action": "tagged a fish at spring"}
    # sorted+compact bytes: identical memories, identical file bytes
    body = path.read_text(encoding="utf-8")
    assert body.endswith("\n")
    assert body.strip() == json.dumps(
        {"ada": {"fish_tagged": 2, "last_action": "tagged a fish at spring",
                 "visits": 1}},
        sort_keys=True, separators=(",", ":"))


def test_player_memories_fail_closed_on_corruption(tmp_path: Path):
    path = tmp_path / "players.json"
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(ValueError, match="refusing to boot"):
        PlayerMemories(path)


# ------------------------------------------------------ the actor flow ----

def _join_flow(world: MountainWorld, user: str, sid: str,
               keep: Innkeeper, also_tag: str | None = None) -> dict:
    world.register_session(sid, user)
    world.stage(sid, "join", INNKEEPER_NODE)
    if also_tag is not None:
        world.stage(sid, "tag", also_tag)
    return keep.pump(world.tick())


def test_innkeeper_is_a_real_session_at_the_spring():
    world = MountainWorld()
    keep = Innkeeper(world, _tmp_mem())
    row = keep.attach()
    assert row == {"user": INNKEEPER_USER, "at": INNKEEPER_NODE}
    snap = world.snapshot()
    assert snap["roster"][INNKEEPER_SID] == {"user": INNKEEPER_USER,
                                             "at": INNKEEPER_NODE}
    world.close()


def test_full_flow_greet_remember_and_persist(tmp_path: Path):
    """Three worlds, one memory file: visit 1 (stranger), visit 2 (known,
    tags a fish at the spring), visit 3 (greeted BY NAME with the catch)."""
    mem_path = tmp_path / "players.json"

    world1 = MountainWorld()
    keep1 = Innkeeper(world1, mem_path)
    keep1.attach()
    rows1 = _join_flow(world1, "ada", "s1", keep1)
    spring1 = rows_mem_units(rows1)
    assert said(rows1) == [f"Welcome, ada - the spring is at {spring1} units"]
    assert motion_verbs(rows1) == ["idle"]
    world1.close()

    world2 = MountainWorld()  # a whole new server run, same memories
    keep2 = Innkeeper(world2, mem_path)
    keep2.attach()
    rows2 = _join_flow(world2, "ada", "s1", keep2, also_tag=INNKEEPER_NODE)
    spring2 = rows_mem_units(rows2)
    assert said(rows2) == [
        f"Welcome back, ada - the spring is at {spring2} units"]
    assert motion_verbs(rows2) == ["dance"]  # tagged right at the spring

    world3 = MountainWorld()  # and again: now the ledger history speaks
    keep3 = Innkeeper(world3, mem_path)
    keep3.attach()
    rows3 = _join_flow(world3, "ada", "s1", keep3)
    spring3 = rows_mem_units(rows3)
    assert said(rows3) == [
        f"Welcome back, ada - the spring is at {spring3} units",
        "Last visit you tagged 1 fish, ada.",
    ]
    stored = json.loads(mem_path.read_text(encoding="utf-8"))["ada"]
    assert stored == {"visits": 3, "fish_tagged": 1,
                      "last_action": "joined at spring"}
    world2.close()
    world3.close()


def rows_mem_units(rows: dict) -> int:
    """The spring volume the greeting actually quoted (never hardcode it:
    the physics moves water every tick)."""
    for text in said(rows):
        if "the spring is at " in text:
            return int(text.rsplit(" ", 2)[-2])
    raise AssertionError(f"no greeting in {rows}")


def _tmp_mem() -> Path:
    import tempfile
    return Path(tempfile.mkdtemp(prefix="innkeeper_test_")) / "players.json"


def test_emitted_rows_are_legal_in_their_channels(tmp_path: Path):
    world = MountainWorld()
    keep = Innkeeper(world, tmp_path / "players.json")
    keep.attach()
    world.register_session("s1", "ada")
    world.stage("s1", "join", INNKEEPER_NODE)
    world.stage("s1", "tag", INNKEEPER_NODE)
    world.stage("s1", "boil", INNKEEPER_NODE)
    rows = keep.pump(world.tick())
    nodes = frozenset(world.node_volumes())
    for row in rows["motion"]:
        ask = MOTION_DISPATCH.ask(row["verb"], "AUTHED",
                                  args={"intensity_q8": row["intensity_q8"],
                                        "dir": row["dir"]},
                                  targets=nodes)
        assert ask["ok"], ask
    for row in rows["say"]:
        assert say_law(row["text"]) == (True, None)
    # dance beat the idle: the tag at the spring outranks the quiet default
    assert motion_verbs(rows) == ["dance"]
    world.close()


def test_innkeeper_ignores_its_own_rows(tmp_path: Path):
    """No self-greet loop: the actor's user never appears in its memory
    deltas or greetings, even if a row somehow carried its name."""
    world = MountainWorld()
    keep = Innkeeper(world, tmp_path / "players.json")
    keep.attach()
    rows = keep.pump(world.tick())
    assert INNKEEPER_USER not in rows["memory"]
    assert rows["say"] == []  # quiet tick: roster row emits no event
    world.close()
