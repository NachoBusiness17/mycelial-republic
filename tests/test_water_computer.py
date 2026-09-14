"""Water-computer keep — engine owns heights. Bucket is a cheat, not a win."""
from __future__ import annotations

from mag.game_campaign import (
    apply_action,
    begin_play,
    load_campaign,
    parse_player_speech,
    resolve_module,
    set_character,
    parse_character,
)
from mag.water_computer import (
    charge_n,
    cheated,
    heights,
    ice_n,
    phase,
    rain_n,
    sight_glass,
    steam_n,
    won,
)


def _boot():
    b = begin_play(module_id="water_computer", voice_session_id="pytest-water", force_new=True)
    cid = str(b.get("campaign_id") or (b.get("campaign") or {}).get("campaign_id") or "")
    if b.get("need_character"):
        set_character(cid, parse_character("I'm Ash a curious engineer"))
    return cid


def _do(cid: str, line: str):
    act = parse_player_speech(line) or {"type": "look"}
    return apply_action(cid, act)


def test_module_resolves():
    m = resolve_module("water one")
    assert m and m.get("module_id") == "water_computer"
    assert "gallery" in (m.get("rooms") or {})


def test_parse_valves():
    assert parse_player_speech("open valve")["type"] == "open"
    assert parse_player_speech("close valve")["type"] == "close"
    assert parse_player_speech("pour bucket")["type"] == "pour"
    assert parse_player_speech("wait")["type"] == "wait"


def test_valve_refused_in_gallery():
    cid = _boot()
    r = _do(cid, "open valve")
    assert r.get("ok") is False
    assert "valve" in str(r.get("error") or "").lower()


def test_gravity_moves_when_open():
    cid = _boot()
    assert _do(cid, "go west").get("ok")
    assert _do(cid, "open valve").get("ok")
    before = heights(load_campaign(cid))
    assert _do(cid, "wait").get("ok")
    after = heights(load_campaign(cid))
    assert after["source"] == before["source"] - 1
    assert after["work"] == before["work"] + 1


def test_bucket_is_cheat_not_win():
    cid = _boot()
    assert _do(cid, "go north").get("ok")
    assert _do(cid, "take bucket").get("ok")
    r = _do(cid, "pour bucket")
    assert r.get("ok")
    camp = load_campaign(cid)
    assert cheated(camp)
    assert not won(camp)
    assert heights(camp)["out"] >= 1
    assert "DISPUTED" in sight_glass(camp)


def test_flow_wins():
    cid = _boot()
    for line in (
        "go west",
        "open valve",
        "wait",
        "wait",
        "go east",
        "go east",
        "open valve",
        "wait",
        "wait",
    ):
        r = _do(cid, line)
        assert r.get("ok"), (line, r.get("error"), r.get("narrate"))
    camp = load_campaign(cid)
    assert not cheated(camp)
    assert won(camp)
    assert heights(camp)["out"] >= 2


def test_cycle_steam_rain_charge_ice_melt():
    cid = _boot()
    assert _do(cid, "go west").get("ok")
    assert _do(cid, "open valve").get("ok")
    assert _do(cid, "wait").get("ok")
    assert _do(cid, "boil").get("ok") or _do(cid, "turn the water into a gas").get("ok")
    camp = load_campaign(cid)
    assert phase(camp) == "gas"
    assert steam_n(camp) >= 1
    while steam_n(load_campaign(cid)) > 0:
        assert _do(cid, "wait").get("ok")
    while rain_n(load_campaign(cid)) > 0:
        assert _do(cid, "wait").get("ok")
    camp = load_campaign(cid)
    assert phase(camp) == "liquid"
    assert heights(camp)["source"] >= 1
    assert charge_n(camp) >= 1
    r = _do(cid, "freeze")
    assert r.get("ok"), r
    camp = load_campaign(cid)
    assert phase(camp) == "ice"
    assert ice_n(camp) >= 1
    while ice_n(load_campaign(cid)) > 0:
        assert _do(cid, "wait").get("ok")
    camp = load_campaign(cid)
    assert phase(camp) == "liquid"
    assert heights(camp)["source"] >= 1
