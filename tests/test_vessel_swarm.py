"""tests for vessel_swarm — the naval architecture: k8s ships over the verkle seabed, k3 liquid
swarms that envelop knots, sonar (lensing) for direction; + Risk of Rain / Deep Rock Galactic / EVE
Online mapped to our systems.

RIB (frozen spec):
  sonar(ping)     -> take direction by lensing the structure (lens_chain.resolve), $0.
  launch_swarm()  -> release k3 liquid swarms (the quantized wave lent to workers) to envelop a knot,
                     folded as a world event.
  naval_map()     -> k8s=ships, verkle=seabed, k3 liquid swarms, envelop, sonar=lensing.
  game_map()      -> Risk of Rain / DRG / EVE mapped to our systems (steal the mechanism).

Contract: reuses game_world + lens_chain; the naval image is the republic-as-fleet-at-sea.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import vessel_swarm  # noqa: E402


def test_sonar_takes_direction():
    s = vessel_swarm.sonar(ping="what surrounds this knot")
    assert s["ok"] is True
    assert "direction" in s or "sonar_error" in s


def test_launch_swarm_envelops_knot(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    l = vessel_swarm.launch_swarm(target="a knot", n=3)
    assert l["ok"] is True
    assert l["n_workers"] == 3
    assert "envelop" in l["liquid_swarm"]  # the swarm envelops the knot


def test_naval_map_layers():
    m = vessel_swarm.naval_map()
    assert m["ok"] is True
    layers = [x["layer"] for x in m["naval_map"]]
    assert "k8s ships" in layers and "verkle seabed" in layers and "sonar = lensing" in layers


def test_game_map_three_games():
    m = vessel_swarm.game_map()
    assert m["ok"] is True
    games = [x["game"] for x in m["game_map"]]
    assert "Risk of Rain" in games and "Deep Rock Galactic" in games and "EVE Online" in games
    # each maps to our systems (the mechanism is steal-able)
    assert "republic" in " ".join(x["maps_to"] for x in m["game_map"]).lower()


def test_chain_of_command_captain_is_operator():
    c = vessel_swarm.chain_of_command()
    assert c["ok"] is True
    ranks = [x["rank"] for x in c["chain_of_command"]]
    assert "Captain" in ranks and "Admiral (coordinator)" in ranks
    captain = next(x for x in c["chain_of_command"] if x["rank"] == "Captain")
    assert "OPERATOR" in captain["who"].upper()  # the operator is the captain


def test_fleet_tactics_coordinated(tmp_path):
    from mag import game_world
    game_world.WORLD = tmp_path / "world_state.json"
    game_world.WORLD_DIR = tmp_path
    t = vessel_swarm.fleet_tactics(objective="the wave", ships=3)
    assert t["ok"] is True
    assert t["n_ships"] == 3
    assert len(t["ships"]) == 3  # each ship runs its operation
    assert t["captain"]  # the captain commands
