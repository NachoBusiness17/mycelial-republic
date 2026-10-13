"""B2 event-ring tests: the writer-side half of AJ4's blindness fix.

Laws under test (receipt watch/inbox/last_mile_20260930/B2_EVENT_RING.md):
  - the 6-cap on game.gd's last_events display feed was the writer-side
    starver: a tick carrying more than 6 strings dropped the head before any
    feed-polling reader (hud greeting rescan, events strip) could see it
  - the feed is now a 64-slot drop-oldest RING with an event_dropped tally
    the HUD surfaces ("+N dropped") — a burst of 20 events in ONE tick is
    fully visible to a reader polling after the tick, not just the last 6
  - this is the ephemeral broadcast channel only: the water_event signal
    stays exactly-once and server/world.py's hash-chained replay log is
    untouched (determinism law); the server's tick payload already carries
    the full event list (server.py pump_once broadcasts world.tick() raw,
    no cap anywhere server-side — grep evidence in the receipt)

The estate box idiom (test_motion_rows.py): .gd laws are enforced
structurally over the source; the executed run below additionally drives the
REAL game.gd headless (Godot 4.3 console exe, X8/W3 create-run-delete
harness) whenever tools/godot holds the binary, and skips with a named
reason otherwise.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
GAME_GD = ROOT / "roblox_to_godot" / "scripts" / "game.gd"
HUD_GGD = ROOT / "roblox_to_godot" / "scripts" / "hud.gd"
PROJECT = ROOT / "roblox_to_godot"
GODOT = ROOT / "tools" / "godot" / "Godot_v4.3-stable_win64_console.exe"

RING_CAP = 64

PROBE_GD = """extends Node
func _ready() -> void:
    var fails: Array[String] = []
    var game: Node = load("res://scripts/game.gd").new()
    add_child(game)
    for i in 20:
        game._push_event("burst %d" % i)
    var ring: Array = game.get("last_events")
    if ring.size() != 20:
        fails.append("burst: reader sees %d, want 20" % ring.size())
    if String(ring[0]) != "burst 0" or String(ring[19]) != "burst 19":
        fails.append("burst: order broken")
    if int(game.get("event_dropped")) != 0:
        fails.append("burst: dropped=%d, want 0" % int(game.get("event_dropped")))
    for i in 50:
        game._push_event("more %d" % i)
    ring = game.get("last_events")
    if ring.size() != 64:
        fails.append("overflow: ring holds %d, want 64" % ring.size())
    if int(game.get("event_dropped")) != 6:
        fails.append("overflow: dropped=%d, want 6" % int(game.get("event_dropped")))
    if String(ring[0]) != "burst 6":
        fails.append("overflow: drop-oldest broken, head='%s'" % ring[0])
    if String(ring[ring.size() - 1]) != "more 49":
        fails.append("overflow: newest lost, tail='%s'" % ring[ring.size() - 1])
    if fails.is_empty():
        print("B2_RING_PASS burst20=20/20 ring=64 dropped=6")
    else:
        for f in fails:
            print("B2_RING_FAIL ", f)
"""

PROBE_TSCN = """[gd_scene load_steps=2 format=3]

[ext_resource type="Script" path="res://{probe_name}.gd" id="1"]

[node name="B2EventRingProbe" type="Node"]
script = ExtResource("1")
"""


# --------------------------------------------------------- structural laws ----

def test_ring_capacity_is_64_not_6():
    src = GAME_GD.read_text(encoding="utf-8")
    m = re.search(r"^const EVENT_RING_CAP := (\d+)$", src, re.MULTILINE)
    assert m, "game.gd must declare EVENT_RING_CAP (B2 ring law)"
    assert int(m.group(1)) == RING_CAP


def test_writer_drops_oldest_and_counts_every_drop():
    src = GAME_GD.read_text(encoding="utf-8")
    # the ring law: append, then while over cap pop_front AND count the drop
    # (a pop without the tally, or a tally without the pop, fails this shape)
    m = re.search(
        r"func _on_water_event\(text: String\) -> void:\n"
        r"(?:[^\n]*\n)*?"
        r"[ \t]*last_events\.append\(text\)\n"
        r"[ \t]*while last_events\.size\(\) > EVENT_RING_CAP:\n"
        r"[ \t]*last_events\.pop_front\(\)\n"
        r"[ \t]*event_dropped \+= 1",
        src,
    )
    assert m, "_on_water_event must drop-oldest at EVENT_RING_CAP and tally"


def test_no_six_cap_remains_anywhere_in_game_gd():
    # comments may quote the retired law (fix comments carry the cause), so
    # this scans CODE lines only — a live `size() > 6` trim anywhere is the
    # regression, a cited one inside # comments is the receipt
    src = GAME_GD.read_text(encoding="utf-8")
    code_lines = [
        ln for ln in src.splitlines()
        if not ln.lstrip().startswith("#") and "size() > 6" in ln
    ]
    assert not code_lines, f"the 6-cap starver is back (B2 regression): {code_lines}"


def test_hud_surfaces_the_drop_tally():
    src = HUD_GGD.read_text(encoding="utf-8")
    assert "event_dropped" in src, "hud.gd must read event_dropped (B2 law)"
    assert "+%d dropped" in src, "hud.gd must render the drop tally visibly"


def test_water_event_signal_fanout_still_exact_once():
    # the AJ4 reader fix rides untouched: every append still fans out on the
    # signal BEFORE any ring bounding (emit in _push_event, bound in
    # _on_water_event — the writer's own handler, connected after the others)
    src = GAME_GD.read_text(encoding="utf-8")
    assert "graph.water_event.emit(text)" in src


# ----------------------------------------------------------- executed law ----

@pytest.mark.skipif(not GODOT.exists(), reason="no Godot binary in tools/godot (structural laws still hold)")
def test_burst_of_20_in_one_tick_reader_sees_all_20():
    """Drives the real game.gd headless: 20 _push_event calls in one tick
    (exactly the loop _on_water_tick/_on_net_tick run per tick event), then
    the reader polls the ring the way hud does (host.get("last_events"))."""
    probe_name = "_tmp_b2_event_ring_probe"
    probe_gd = PROJECT / f"{probe_name}.gd"
    probe_tscn = PROJECT / f"{probe_name}.tscn"
    try:
        probe_gd.write_text(PROBE_GD, encoding="utf-8")
        probe_tscn.write_text(PROBE_TSCN.format(probe_name=probe_name), encoding="utf-8")
        proc = subprocess.run(
            [str(GODOT), "--headless", "--path", str(PROJECT),
             f"res://{probe_name}.tscn", "--quit-after", "5"],
            capture_output=True, text=True, timeout=90,
        )
        out = proc.stdout + proc.stderr
    finally:  # X8/W3 create-run-delete idiom: no probe trace survives the run
        probe_gd.unlink(missing_ok=True)
        probe_tscn.unlink(missing_ok=True)
    assert "B2_RING_PASS burst20=20/20 ring=64 dropped=6" in out, out
    assert "B2_RING_FAIL" not in out, out
