"""REPRINT tests (W3D, 2026-09-29) — death as interagent hand-off.

Ledger return 11/24 improvement: a defeated campaign folds its death as a
verkle knot, harvests salvage (honest temple:/slain:/door_open: flags +
inventory kept, cheat:/nuke: dropped), re-seats the named actor from CHAR_DIR
with hp restored + reprint_n+1, and leaves receipt rows via the live
party_subchain + training_events patterns.

Isolation: CAMP_DIR/CHAR_DIR are monkeypatched to tmp_path and the three
receipt sinks (party_subchain.append, training_events.emit,
rib_bus.publish_rib) are monkeypatched to recorders — the shared verkle
chain, events file and rib store stay byte-still (conftest B2-336 law).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import mag.game_campaign as gc  # noqa: E402
from mag.game_campaign import reprint  # noqa: E402


@pytest.fixture
def lanes(tmp_path, monkeypatch):
    """Isolated campaign + character dirs, and recorders on the receipt sinks."""
    camps = tmp_path / "campaigns"
    chars = tmp_path / "chars"
    monkeypatch.setattr(gc, "CAMP_DIR", camps)
    monkeypatch.setattr(gc, "CHAR_DIR", chars)

    calls: dict[str, list] = {"party": [], "events": [], "ribs": []}

    import mag.party_subchain as ps
    import mag.training_events as te
    import mag.rib_bus as rb

    monkeypatch.setattr(
        ps, "append", lambda **kw: calls["party"].append(kw) or {"ok": True}
    )
    monkeypatch.setattr(
        te, "emit", lambda pattern, **kw: calls["events"].append({"pattern": pattern, **kw}) or {"ok": True}
    )
    monkeypatch.setattr(
        rb, "publish_rib", lambda *a, **kw: calls["ribs"].append({"args": a, **kw}) or {"ok": True}
    )
    return calls


def _campaign(cid: str, status: str, *, flags=None, inventory=None, name="Ash", reprint_n=0,
              module_id="classic", module_title="Classic Stub") -> dict:
    return {
        "schema": gc.SCHEMA,
        "campaign_id": cid,
        "ts": gc._utc(),
        "voice_session_id": "pytest-reprint",
        "module_id": module_id,
        "module_title": module_title,
        "status": status,
        "room_id": "start",
        "player": {
            "name": name,
            "archetype": "fighter",
            "hp": 0 if status == "defeated" else 12,
            "hp_max": 12,
            "ac": 14,
            "attack_bonus": 4,
            "damage": "1d8+2",
            "traits": ["brave"],
            "inventory": list(inventory if inventory is not None else ["torch", "rations", "gem"]),
        },
        "encounter": None,
        "flags": list(flags if flags is not None else []),
        "reprint_n": reprint_n,
        "log": [],
        "module_snapshot": {"rooms": {}, "event_tables": {}, "player_start": {}},
    }


def _seat(cid: str, status: str, **kw) -> str:
    gc.save_campaign(_campaign(cid, status, **kw))
    return cid


def _sheet(name: str = "Ash", *, campaign_id: str, hp_max: int = 12) -> None:
    gc.CHAR_DIR.mkdir(parents=True, exist_ok=True)
    sp = gc._char_sheet_path(name)
    sp.write_text(
        json.dumps(
            {
                "player": {
                    "name": name,
                    "archetype": "fighter",
                    "hp": hp_max,
                    "hp_max": hp_max,
                    "ac": 14,
                    "attack_bonus": 4,
                    "damage": "1d8+2",
                    "traits": ["brave"],
                    "inventory": ["torch", "rations"],
                },
                "campaign_id": campaign_id,
                "ts": gc._utc(),
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_defeated_reprints_flags_honored_and_actor_reseated(lanes):
    """The corpse reprints: honest flags carried, module flags folded into the
    knot (not carried), inventory kept, CHAR_DIR actor re-seated with hp
    restored, receipt rows fired."""
    cid = _seat(
        "gc-dead01",
        "defeated",
        flags=["temple:r1", "slain:goblin-pit", "door_open:crypt", "water:phase"],
    )
    _sheet("Ash", campaign_id=cid, hp_max=20)  # sheet outranks the corpse: hp_max 20 vs 12

    out = reprint(cid)
    assert out["ok"] is True
    assert out["kept_flags"] == ["temple:r1", "slain:goblin-pit", "door_open:crypt"]
    assert out["folded_flags"] == ["water:phase"]  # honest but module-scoped: knotted, not carried
    assert out["dropped_flags"] == []

    new = gc.load_campaign(out["campaign_id"])
    assert new is not None
    assert new["status"] == "active"
    assert new["flags"] == ["temple:r1", "slain:goblin-pit", "door_open:crypt"]
    assert new["player"]["inventory"] == ["torch", "rations", "gem"]
    assert new["player"]["hp"] == 20 and new["player"]["hp_max"] == 20  # re-seated from CHAR_DIR sheet
    assert new["reprint_of"] == cid

    # corpse is filed, not deleted: status reprinted + pointer to the clone
    old = gc.load_campaign(cid)
    assert old["status"] == "reprinted"
    assert old["reprinted_to"] == out["campaign_id"]

    # receipt rows: one party_subchain row + one training_events row
    assert len(lanes["party"]) == 1
    assert lanes["party"][0]["kind"] == "reprint"
    assert cid in lanes["party"][0]["move"]
    assert len(lanes["events"]) == 1
    assert lanes["events"][0]["pattern"] == "game_turn"
    assert lanes["events"][0]["join"]["kind"] == "reprint"
    # the death folded as a knot (rib_bus idiom)
    assert len(lanes["ribs"]) == 1
    assert lanes["ribs"][0]["source"] == "game_campaign.reprint"


def test_cheat_flags_dropped(lanes):
    """cheat:/nuke: never ride the clone — the exact water_computer cheat
    vocabulary is stripped while honest flags survive."""
    cid = _seat(
        "gc-cheat01",
        "defeated",
        flags=["temple:r2", "cheat:bucket", "nuke:fireball", "door_open:vault"],
    )
    out = reprint(cid)
    assert out["ok"] is True
    assert out["kept_flags"] == ["temple:r2", "door_open:vault"]
    assert sorted(out["dropped_flags"]) == ["cheat:bucket", "nuke:fireball"]
    new = gc.load_campaign(out["campaign_id"])
    assert new["flags"] == ["temple:r2", "door_open:vault"]
    # dropped flags are named in the knot row, not silently lost
    knot_text = " ".join(str(a) for a in lanes["ribs"][0]["args"])
    assert "cheat:bucket" in knot_text and "nuke:fireball" in knot_text


def test_counter_increments_across_generations(lanes):
    """reprint_n climbs with each death: 0 -> 1 -> 2, and the character sheet
    advances with the clone."""
    cid = _seat("gc-gen0", "defeated")
    _sheet("Ash", campaign_id=cid)

    first = reprint(cid)
    assert first["ok"] is True and first["reprint_n"] == 1

    # the clone dies too; its reprint continues the lineage
    clone = gc.load_campaign(first["campaign_id"])
    clone["status"] = "defeated"
    clone["player"]["hp"] = 0
    gc.save_campaign(clone)

    second = reprint(first["campaign_id"])
    assert second["ok"] is True and second["reprint_n"] == 2
    assert second["reprint_of"] == first["campaign_id"]

    sheet = json.loads(gc._char_sheet_path("Ash").read_text(encoding="utf-8"))
    assert sheet["reprint_n"] == 2
    assert sheet["campaign_id"] == second["campaign_id"]


def test_live_campaign_refused(lanes):
    """Only the dead reprint: an active campaign is refused untouched — no
    clone, no receipts, no knot, no sheet advance."""
    cid = _seat("gc-alive", "active")
    _sheet("Ash", campaign_id=cid)

    out = reprint(cid)
    assert out["ok"] is False
    assert out.get("refused") is True
    assert "not defeated" in out["error"]

    camp = gc.load_campaign(cid)
    assert camp["status"] == "active"  # untouched
    assert "reprinted_to" not in camp
    # nothing fired: no receipts, no knot, no new campaign files
    assert lanes["party"] == [] and lanes["events"] == [] and lanes["ribs"] == []
    assert list(gc.CAMP_DIR.glob("gc-*.json")) == [gc.CAMP_DIR / "gc-alive.json"]
    sheet = json.loads(gc._char_sheet_path("Ash").read_text(encoding="utf-8"))
    assert sheet["campaign_id"] == cid  # sheet untouched


def test_missing_campaign_refused(lanes):
    assert reprint("gc-ghost")["ok"] is False


def test_cli_verb(lanes, capsys):
    """python -m mag.game_campaign reprint <cid>: exit 0 on reprint, 2 on
    refusal; JSON verdict on stdout."""
    cid = _seat("gc-cli1", "defeated")
    _sheet("Ash", campaign_id=cid)

    assert gc._cli(["reprint", cid]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["ok"] is True and out["reprint_n"] == 1

    assert gc._cli(["reprint", cid]) == 2  # already reprinted: refused now
    out2 = json.loads(capsys.readouterr().out)
    assert out2["ok"] is False and out2.get("refused") is True

    assert gc._cli([]) == 2  # usage line
    assert "usage:" in capsys.readouterr().out


# ── X3 water weld (2026-09-29, receipt watch/inbox/hydrology/X3_WATER_WELD.md) ─
# W3D's honest seam: the water module's reprint pass-off no-oped because
# water_computer wasn't in that lane's file set. Now handle(atype="reprint")
# salvages the water state from the corpse (camp["reprint_of"]) onto the
# clone — node volumes / tank heights carry across death. The water remembers.


def _graph_flag(spec) -> str:
    from mag.water_computer import GRAPH_FLAG

    return GRAPH_FLAG + "=" + json.dumps(spec, sort_keys=True, separators=(",", ":"))


def test_water_campaign_reprints_with_volumes_carried(lanes):
    """A defeated graph-mode water campaign reprints with node volumes
    carried: the module speaks in the pass-off (carries its own namespace),
    the engine still folds the module flag into the knot — its law,
    unchanged. water:anchored never rides the clone."""
    from mag.water_computer import default_graph_spec, graph_spec
    from mag.water_graph import from_spec

    spec = default_graph_spec()
    spec["nodes"]["source"]["volume"] = 4  # two marks flowed before death
    spec["nodes"]["out"]["volume"] = 1
    cid = _seat(
        "wc-dead01",
        "defeated",
        module_id="water_computer",
        module_title="Water Computer",
        flags=[_graph_flag(spec), "water:anchored=deadbeefcafe0123", "temple:r1"],
    )
    _sheet("Ash", campaign_id=cid, hp_max=20)

    out = reprint(cid)
    assert out["ok"] is True
    # the pass-off is handled now — the W3D seam is welded
    assert out["pass_off"]["handled"] is True
    assert out["pass_off"]["water_salvage"]["mode"] == "graph"
    assert out["pass_off"]["water_salvage"]["dishonest"] is False

    # the engine folded the module flags into the knot (never carried by the engine)...
    assert any(str(f).startswith("water:graph=") for f in out["folded_flags"])
    assert any(str(f).startswith("water:anchored=") for f in out["folded_flags"])
    # ...while the module carried the graph onto the clone through the pass-off
    new = gc.load_campaign(out["campaign_id"])
    got = graph_spec(new)
    assert got is not None, "the clone must ride the corpse's graph mode"
    g = from_spec(got)
    assert g.nodes["source"].volume == 4
    assert g.nodes["out"].volume == 1
    assert g.nodes["reservoir"].volume == 2
    # honest engine-kept flag + module namespace coexist on the clone
    assert "temple:r1" in new["flags"]
    fmap = {f.split("=", 1)[0]: f.split("=", 1)[1] for f in new["flags"] if "=" in f}
    assert "water:anchored" not in fmap, "proof dedupe is per-campaign"
    # the module event rode the clone's log
    assert any("water remembers" in str(row.get("text")) for row in new["log"])


def test_water_reprint_legacy_heights_carried(lanes):
    """Legacy 3-tank corpse: heights + phase ledger + charge carry as-died."""
    from mag.water_computer import charge_n, heights, phase

    cid = _seat(
        "wc-dead02",
        "defeated",
        module_id="water_computer",
        module_title="Water Computer",
        flags=["water:source=1", "water:work=1", "water:out=1",
               "water:phase=liquid", "charge=2"],
    )
    _sheet("Ash", campaign_id=cid)

    out = reprint(cid)
    assert out["pass_off"]["handled"] is True
    assert out["pass_off"]["water_salvage"]["mode"] == "legacy"
    new = gc.load_campaign(out["campaign_id"])
    assert heights(new) == {"source": 1, "work": 1, "out": 1}
    assert phase(new) == "liquid"
    assert charge_n(new) == 2


def test_water_reprint_cheat_death_carries_no_water(lanes):
    """A cheat death carries no water memory: graph topology stands drained
    and shut, the bucket's fake OUT height does not ride the clone."""
    from mag.water_computer import default_graph_spec, graph_spec, heights
    from mag.water_graph import from_spec

    spec = default_graph_spec()
    spec["nodes"]["source"]["volume"] = 5
    spec["nodes"]["out"]["volume"] = 2
    g_cid = _seat(
        "wc-nuke01",
        "defeated",
        module_id="water_computer",
        module_title="Water Computer",
        flags=[_graph_flag(spec), "nuke:fireball", "scorched"],
    )
    _sheet("Ash", campaign_id=g_cid)
    out = reprint(g_cid)
    assert out["pass_off"]["water_salvage"]["dishonest"] is True
    assert sorted(out["dropped_flags"]) == ["nuke:fireball", "scorched"]
    new = gc.load_campaign(out["campaign_id"])
    got = graph_spec(new)
    assert got is not None, "the mode carries even across a cheat death"
    g = from_spec(got)
    assert all(n.volume == 0 for n in g.nodes.values())
    assert all(not p.open for p in g.pipes.values())

    # legacy corpse that bucket-cheated: the fake OUT height must not carry
    l_cid = _seat(
        "wc-bucket01",
        "defeated",
        module_id="water_computer",
        module_title="Water Computer",
        flags=["water:source=0", "water:out=3", "cheat:bucket"],
    )
    _sheet("Ash", campaign_id=l_cid)
    new2 = gc.load_campaign(reprint(l_cid)["campaign_id"])
    assert heights(new2) == {"source": 3, "work": 0, "out": 0}, "fresh seed, no lie"
    assert "cheat:bucket" not in new2["flags"]
