"""tests for game_entry — STONE 2 (the entry surface): the "walk forward and a building appears" gate.
Deterministic + stateless + $0.

RIB (frozen spec):
  gate(player, region, archetype) -> the entry: Watcher greeting + persona-recall recount + scene.
      Deterministic; always ok:True; watcher + scene present; recount is grounded (or honest error).
  reveal(region, x, y, direction) -> INTENT-GATED: content-addressed building (same steer -> same
      building), perceptual culling (revealed=True, culled=True). Deterministic + replayable.
  walk() -> gate + reveal in one step (the vertical trigger in miniature).
  svg()  -> bare-metal SVG string (zero deps), contains the building glyph + region label.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_entry  # noqa: E402


def test_gate_ok_watcher_and_scene():
    g = game_entry.gate(player="beta-tester", region="mycelial-republic")
    assert g["ok"] is True
    assert g["watcher"]                      # the Watcher/GM greeting
    assert g["scene"]                        # the entry scene ("walk forward and a building appears")
    assert g["region"] == "mycelial-republic"
    # deterministic: same entry -> same watcher + scene
    g2 = game_entry.gate(player="beta-tester", region="mycelial-republic")
    assert g2["watcher"] == g["watcher"]
    assert g2["scene"] == g["scene"]


def test_reveal_deterministic_content_addressed():
    r1 = game_entry.reveal(region="mycelial-republic", x=4, y=4, direction="forward")
    r2 = game_entry.reveal(region="mycelial-republic", x=4, y=4, direction="forward")
    assert r1["ok"] is True
    assert r1["building"]["key"] == r2["building"]["key"]      # same steer -> same building
    assert r1["seed"] == r2["seed"]
    assert r1["revealed"] is True and r1["culled"] is True     # perceptual culling on
    # a different steer -> different building (not always, but seed must differ)
    r3 = game_entry.reveal(region="mycelial-republic", x=7, y=2, direction="west")
    assert r3["seed"] != r1["seed"]


def test_reveal_region_is_part_of_the_address():
    # the region is part of the content address: same coords, different region -> different building
    a = game_entry.reveal(region="mycelial-republic", x=3, y=3, direction="north")
    b = game_entry.reveal(region="another-world", x=3, y=3, direction="north")
    assert a["seed"] != b["seed"]


def test_walk_combines_gate_and_reveal():
    w = game_entry.walk(player="beta-tester", x=2, y=2, direction="forward")
    assert w["ok"] is True
    assert w["watcher"] and w["recount"] is not None           # the recount beat
    assert w["building"]["name"]                               # the reveal beat
    assert "building appears" in w["scene"]


def test_svg_bare_metal_and_contains_building():
    s = game_entry.svg(region="mycelial-republic", x=4, y=4, direction="forward")
    assert s.startswith("<svg") and s.endswith("</svg>")       # bare-metal SVG, no deps
    # the revealed building's glyph + name are in the markup
    r = game_entry.reveal(region="mycelial-republic", x=4, y=4, direction="forward")
    assert r["building"]["glyph"] in s
    assert "region: mycelial-republic" in s


def test_buildings_catalog_mapped():
    # the world's buildings are grounded archetypes (mapped to real content), all addressable
    assert len(game_entry.BUILDINGS) >= 5
    for k in game_entry.BUILDING_KEYS:
        b = game_entry.BUILDINGS[k]
        assert b["glyph"] and b["name"] and b["color"] and b["line"]
