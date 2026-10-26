"""tests for game_world_render OPTICS — the stolen concept (measure_plan + mathemetica, 2026-09-14).

RIB (frozen spec):
  dense medium (bright field) bends the lantern ray — temperature is the refractive index.
  void field: straight rays, landed == aimed (backward contract with stone 3).
  enough leaves in a region -> the tree grows an internal node (the grok knot, ▲).
  same steer -> same landing, always (deterministic, content-addressed).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag import game_world_render as gwr  # noqa: E402


def _dense(region):
    return [[0.9 for _ in range(gwr.GRID_W)] for _ in range(gwr.GRID_H)]


def _void(region):
    return [[0.0 for _ in range(gwr.GRID_W)] for _ in range(gwr.GRID_H)]


def test_ray_bends_in_dense_medium(monkeypatch):
    monkeypatch.setattr(gwr, "_field", _dense)
    a = gwr.reveal(player="optic-1", direction="north", region="optics-test")
    b = gwr.reveal(player="optic-1", direction="north", region="optics-test")
    assert a["ok"] is True
    # the ray bent: landed off the aimed cell, with the refraction law on record
    assert a["bent"] is True and (a["x"], a["y"]) != tuple(a["aimed"])
    assert "refracted_at" in a and "temperature" in a["law"]
    # same steer -> same landing (deterministic, content-addressed)
    assert (a["x"], a["y"], a["building"]) == (b["x"], b["y"], b["building"])


def test_ray_straight_in_void(monkeypatch):
    monkeypatch.setattr(gwr, "_field", _void)
    a = gwr.reveal(player="optic-2", direction="north", region="optics-test")
    assert a["bent"] is False
    assert (a["x"], a["y"]) == tuple(a["aimed"])


def test_internal_node_grows_after_enough_leaves(monkeypatch):
    import os
    import time
    monkeypatch.setattr(gwr, "_field", _void)
    # the world is persistent (verkle knots survive runs) — every run needs a virgin grove
    region = f"grove-test-{os.getpid()}-{time.time_ns()}"
    dirs = ["north", "south", "east", "west", "up", "down", "left", "right"]
    saw_grok = None
    # Fix 2026-10-01: 8 steers are NOT 8 leaves — steers content-address into 40x16 cells and
    # two can land on one cell (measured 4.3% of virgin groves; the standing fullsuite RED of
    # 2026-09-29). The contract is LEAVES, not steers: keep steering until the grove really
    # holds GROK_THRESHOLD distinct leaves; the reveal that crosses the threshold grows the knot.
    for i in range(40):
        r = gwr.reveal(player=f"grokker-{i}", direction=dirs[i % len(dirs)], region=region)
        if r.get("grok"):
            saw_grok = r["grok"]
        if gwr._leaf_count(region) >= gwr.GROK_THRESHOLD:
            break
    assert gwr._leaf_count(region) >= gwr.GROK_THRESHOLD  # the grove truly has enough leaves
    # once it does, the tree has grown its internal node
    assert saw_grok is not None
    assert saw_grok["glyph"] == "▲" and "internal node" in saw_grok["name"].lower()
    # exactly once: the knot persists, a second pass grows nothing new
    r = gwr.reveal(player="grokker-once-more", direction="north", region=region)
    assert r.get("grok") is None


def test_old_contract_still_holds(monkeypatch):
    monkeypatch.setattr(gwr, "_field", _void)
    a = gwr.reveal(player="compat", direction="north", region="optics-test")
    b = gwr.reveal(player="compat", direction="north", region="optics-test")
    assert a["x"] == b["x"] and a["y"] == b["y"] and a["building"] == b["building"]
    w = gwr.walk(player="compat", direction="west", region="optics-test")
    assert w["ok"] is True and w["reveal"]["ok"] is True and w["render"]["ok"] is True
