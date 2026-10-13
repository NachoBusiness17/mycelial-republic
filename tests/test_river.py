"""river tests -- Watershed rung 4: erosion/sediment on the integer
substrate (WC's river-bend steal, WF_SYNTHESIS.md 2026-09-30).

Each test pins one law: silt conservation (never created, never
destroyed), the sill law (strict >: erosion above, deposition below),
erosion lowers / deposition raises, a channel carves over 100 ticks on a
slope, determinism (byte-identical specs), and the bridge law that the
water phase is still rung 2's sheet flow exactly (no silt -> identical
to a plain FieldFlow).
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mag.field_flow import FieldFlow  # noqa: E402
from mag.river import River, det_noise, from_spec  # noqa: E402


# ------------------------------------------------------------- boards ----
def _split_board(mantle: int = 10) -> tuple[list[list[int]], list[list[int]]]:
    """3x3: spring A=(1,0) high, twin pits B=(0,1) C=(2,1) low, walls high.
    A's outflow splits across B and C, so A carries flow 8 while B and C
    carry 4 each -- above and below a sill of 6."""
    elev = [[30, 0, 30],
            [20, 30, 30],
            [30, 0, 30]]
    silt = [[mantle] * 3 for _ in range(3)]
    return elev, silt


def _slope_board() -> tuple[list[list[int]], list[list[int]], set]:
    """3x12: a confined channel row stepping down 10/col to a deep sea
    outlet; dry armored walls 20 above the channel on both sides."""
    w = 12
    elev = [[0] * w for _ in range(3)]
    for x in range(11):
        elev[1][x] = 110 - x * 10          # 110 at the spring, 10 at the mouth
        elev[0][x] = elev[2][x] = elev[1][x] + 20
    elev[1][11] = -80                      # the sea
    elev[0][11] = elev[2][11] = 120        # sea walls
    silt = [[0] * w for _ in range(3)]
    for x in range(12):
        silt[1][x] = 50                    # the channel's regolith mantle
    return elev, silt, {(1, 11)}


def _meadow(h: int = 12, w: int = 40, span: int = 3, step: int = 6,
            mantle: int = 6):
    """Noisy sloped plain (deterministic hash noise) draining east to a
    sea column -- the meander board."""
    elev = [[(w - 1 - x) * step + det_noise(y, x, span) for x in range(w)]
            for y in range(h)]
    silt = [[mantle] * w for _ in range(h)]
    waste = {(y, w - 1) for y in range(h)}
    return elev, silt, waste


def _run(r: River, ticks: int, pour_y: int = 6, pour_x: int = 0,
         rate: int = 8) -> None:
    for _ in range(ticks):
        r.add_water(pour_y, pour_x, rate)
        r.tick()


# ------------------------------------------------------ construction ----
def test_construction_rejects_bad_silt():
    try:
        River([[0, 1], [2, 3]], silt=[[1]])
    except ValueError:
        pass
    else:
        raise AssertionError("silt shape mismatch must raise")
    try:
        River([[0, 1]], silt=[[1, -1]])
    except ValueError:
        pass
    else:
        raise AssertionError("negative silt must raise")
    try:
        River([[0, 1]], sill_flow=-1)
    except ValueError:
        pass
    else:
        raise AssertionError("negative sill_flow must raise")


# ------------------------------------------------------- conservation ----
def test_silt_conserved_on_noisy_run():
    elev, silt, waste = _meadow()
    r = River(elev, silt=silt, waste=waste)
    s0, e0 = r.total_silt(), r.total_elev()
    for t in range(1, 401):
        r.add_water(6, 0, 8)
        r.tick()
        if t % 25 == 0:
            assert r.total_silt() == s0, f"tick {t}: silt appeared or vanished"
    assert r.total_eroded > 0, "the run must actually move rock"
    # elev accounting: every carved unit either landed or washed out with
    # the water (the collision rule) -- nothing unaccounted.
    assert e0 - r.total_elev() == r.total_eroded - r.total_deposited


# --------------------------------------------------------- sill law ----
def test_erosion_lowers_deposition_raises():
    elev, silt = _split_board()
    r = River(elev, silt=silt, sill_flow=6)
    r.add_water(1, 0, 8)
    r.tick()
    assert r.elev[1][0] == 19, "the flowing spring must carve (-1 elev)"
    assert r.elev[0][1] == 1, "the quiet pit must gain a bar (+1 elev)"
    assert r.elev[2][1] == 0, "tie-break: first equal-lowest neighbor receives"
    assert r.silt[1][0] == 9 and r.silt[0][1] == 11
    assert r.total_eroded == 1 and r.total_deposited == 1


def test_erosion_and_deposition_continue_over_ticks():
    elev, silt = _split_board()
    r = River(elev, silt=silt, sill_flow=6)
    _run(r, 6, pour_y=1, pour_x=0)
    # A is the only eroder (flow 8 > 6); its 6 carves land on B or C
    assert r.elev[1][0] == 14, "1 carve per tick for 6 ticks"
    assert r.elev[0][1] + r.elev[2][1] == 6, "every unit lands on a quiet pit"
    assert r.total_eroded == 6


def test_sill_is_strictly_greater():
    elev, silt = _split_board()
    at = River(elev, silt=[row[:] for row in silt], sill_flow=8)
    _run(at, 5, pour_y=1, pour_x=0)
    assert at.total_eroded == 0, "flow == sill must NOT erode (strict >)"
    assert at.elev[1][0] == 20 and at.elev[0][1] == 0
    above = River(elev, silt=[row[:] for row in silt], sill_flow=7)
    _run(above, 1, pour_y=1, pour_x=0)
    assert above.total_eroded == 1, "flow 8 > sill 7 must erode"


# ----------------------------------------------------------- carving ----
def test_channel_carves_over_100_ticks_on_slope():
    elev, silt, waste = _slope_board()
    r = River(elev, silt=silt, waste=waste, sill_flow=6)
    s0 = r.total_silt()
    _run(r, 100, pour_y=1, pour_x=0)
    carved = 110 - r.elev[1][0]
    assert carved == 50, (
        f"spring carves 1/tick until its 50-silt mantle armors ({carved})")
    assert r.elev[1][1] < 80, "the channel proper must incise, not just the spring"
    assert all(r.elev[0][x] == elev[0][x] and r.elev[2][x] == elev[2][x]
               for x in range(12)), "dry armored walls never move"
    assert r.elev[1][11] > -80, "the sea outlet must grow a delta"
    assert r.total_silt() == s0
    assert r.total_eroded >= 500, "the whole channel erodes most ticks"


# -------------------------------------------------------- determinism ----
def test_determinism_byte_identical_spec():
    runs = []
    for _ in range(2):
        elev, silt, waste = _meadow()
        r = River(elev, silt=silt, waste=waste)
        _run(r, 300)
        runs.append(r.to_spec())
    assert runs[0] == runs[1], "same inputs must give byte-identical specs"


def test_spec_round_trip():
    elev, silt, waste = _meadow(h=6, w=10)
    r = River(elev, silt=silt, waste=waste, sill_flow=4)
    _run(r, 20, pour_y=3)
    spec = r.to_spec()
    r2 = from_spec(spec)
    assert r2.elev == r.elev and r2.silt == r.silt and r2.vol == r.vol
    assert r2.waste == r.waste and r2.sill_flow == 4 and r2.tick_count == 20


# ------------------------------------------------------ bridge law ----
def test_water_phase_matches_field_flow_with_no_silt():
    """No silt -> no sediment -> the tick IS rung 2's sheet flow exactly
    (volumes, elevations, dirty order). Pins the instrumented copy
    against the parent law."""
    elev = [[(15 - x) * 5 + det_noise(y, x, 2) for x in range(16)]
            for y in range(8)]
    r = River(elev, waste={(y, 15) for y in range(8)})
    f = FieldFlow([row[:] for row in elev], waste={(y, 15) for y in range(8)})
    for t in range(20):
        r.add_water(4, 1, 6)
        f.add_water(4, 1, 6)
        r.tick()
        f.tick()
    assert r.vol == f.vol, "water law must match rung 2"
    assert r.elev == f.elev == elev, "no silt means no bed movement"
    assert list(r.dirty) == list(f.dirty), "dirty-set law must match rung 2"
    assert r.tick_count == f.tick_count == 20
    assert r.total_eroded == 0
