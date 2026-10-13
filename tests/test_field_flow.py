"""field_flow -- Watershed rung 2 tests (Z5: DF dirty-block sheet flow).

Covers the four mission asks: a puddle spreads and settles on flat ground;
the dirty-block tick processes at most (and provably exactly matches) what
a full scan would; volume is conserved on closed boards and against the
drained counter on outlet boards; and runs are byte-deterministic
(snapshots, wetted-meter history, dirty insertion order). The dem_to_board
bridge is exercised against the real synthetic tile, and the perf sanity
(64x64, 1000 drip ticks) runs as a report-only test with a conservation
assert -- timing lands in the receipt, never a CI gate.
"""
from __future__ import annotations

import math
import time

import pytest

from mag.field_flow import (
    DEFAULT_CONDUCTANCE,
    HEAD_SCALE,
    FieldFlow,
)

import tools.dem_to_board as d2b


# ----------------------------------------------------------- puddle law ----
def test_puddle_spreads_and_settles():
    # Flat 9x9, one pour: the depth head must push water outward until
    # every adjacent depth difference sits below the integer flow floor.
    flow = FieldFlow([[5] * 9 for _ in range(9)])
    flow.add_water(4, 4, 600)
    ran = flow.run(5000)
    assert flow.settled()
    assert 0 < ran < 5000                       # it settled, not timed out
    snap = flow.snapshot()
    wet = [v for row in snap for v in row if v > 0]
    assert len(wet) >= 9                        # spread past the source cell
    assert snap[4][4] < 600                     # the source gave water up
    assert max(wet) - min(wet) <= 160           # near-level surface (adjacent
    # diffs round to zero below 256//conductance = 32 head units = 32
    # volume units at cross_section 1000; 160 bounds a 5-cell gradient)
    assert flow.total_volume() == 600


def test_settled_board_ticks_at_zero_cost():
    flow = FieldFlow([[2] * 5 for _ in range(5)])
    flow.add_water(2, 2, 100)
    flow.run(5000)
    assert flow.settled()
    before = flow.snapshot()
    processed, moved = flow.tick()
    assert processed == 0 and moved == 0        # quiescent water costs zero
    assert flow.snapshot() == before


def test_single_unit_droplet_is_retained():
    # The integer surface-tension floor: 1 unit on flat ground has dHead
    # that rounds to zero flow, so a droplet never evaporates by rounding.
    flow = FieldFlow([[4] * 3 for _ in range(3)])
    flow.add_water(1, 1, 1)
    flow.run(100)
    assert flow.snapshot()[1][1] == 1
    assert flow.wet_cells() == 1


def test_water_flows_downhill_never_uphill():
    down = FieldFlow([[10, 0]])                 # one row, high -> low
    down.add_water(0, 0, 50)
    processed, moved = down.tick()
    assert moved > 0 and down.snapshot()[0][1] > 0
    up = FieldFlow([[0, 10]])                   # water already at the low end
    up.add_water(0, 0, 50)
    processed, moved = up.tick()
    assert moved == 0 and up.snapshot()[0][0] == 50


# ------------------------------------------------------- dirty-block law ----
def test_dirty_block_matches_full_scan_exactly_and_costs_less():
    # The load-bearing claim: the dirty tick lands the byte-identical
    # state a naive full scan would, while examining fewer cells.
    terr = [[(x * 13 + y * 7) % 23 for x in range(12)] for y in range(12)]
    a = FieldFlow(terr)
    b = FieldFlow(terr)
    for flow in (a, b):
        flow.add_water(6, 6, 400)
        flow.add_water(2, 9, 250)
    a_processed = []
    for _ in range(60):
        pa, ma = a.tick()
        pb, mb = b.tick(full=True)
        a_processed.append(pa)
        assert a.snapshot() == b.snapshot()     # exactness, step by step
        assert ma == mb
        assert pa <= pb                         # dirty never costs more
        assert pb == 12 * 12                    # full scan pays the board
    assert min(a_processed) < 12 * 12           # and at least one tick
    # genuinely skipped work (settling tail)
    assert sorted(a.dirty) == sorted(b.dirty)   # same active set, same law
    assert a.total_volume() == b.total_volume() == 650


def test_dirty_set_is_exactly_moved_cells_plus_neighbors():
    # Law shape check on a hand-checkable board: 1D slope, water at the
    # top. After one tick the moved cells are the sender and the one
    # downhill neighbor; the dirty set is those plus their neighbors.
    flow = FieldFlow([[30, 20, 10, 0]])
    flow.add_water(0, 0, 40)
    flow.tick()
    assert sorted(flow.dirty) == [(0, 0), (0, 1), (0, 2)]


# ---------------------------------------------------------- conservation ----
def test_conservation_closed_board_every_tick():
    terr = [[(x * 5 + y * 3) % 11 for x in range(8)] for y in range(8)]
    flow = FieldFlow(terr)
    flow.add_water(3, 3, 300)
    flow.add_water(6, 1, 120)
    for _ in range(80):
        flow.tick()
        assert flow.total_volume() == 420
        assert all(v >= 0 for row in flow.snapshot() for v in row)


def test_conservation_with_waste_outlet():
    # dem_to_board tags the lowest edge cell `waste` (the tile outlet):
    # water reaching it leaves the board and must land in `drained`.
    elev = [[(2 - y) * 8 + (2 - x) for x in range(3)] for y in range(3)]
    flow = FieldFlow(elev, waste={(2, 2)})
    flow.add_water(0, 0, 200)
    flow.run(3000)
    assert flow.drained > 0                     # water actually left
    assert flow.total_volume() + flow.drained == 200
    assert flow.settled()


# ----------------------------------------------------------- determinism ----
def test_determinism_identical_runs():
    terr = [[(x * 7 + y * 11) % 19 for x in range(10)] for y in range(10)]

    def scenario(flow):
        hist = []
        flow.add_water(5, 5, 500)
        for _ in range(10):
            hist.append(flow.tick())
        flow.add_water(1, 8, 90)
        for _ in range(40):
            hist.append(flow.tick())
        return flow, hist

    a, hist_a = scenario(FieldFlow(terr))
    b, hist_b = scenario(FieldFlow(terr))
    assert a.snapshot() == b.snapshot()
    assert hist_a == hist_b                     # wetted meter deterministic
    assert list(a.dirty) == list(b.dirty)       # insertion order identical
    assert a.drained == b.drained and a.total_moved == b.total_moved


def test_q8_flow_matches_hand_computation():
    # One pour, one neighbor pair: raw = dHead * conductance >> 8 with
    # depth = volume at cross_section 1000. Elevs differ by 1 (256 head
    # units), source holds 50 -> dHead 306 -> raw 9 (hand-checkable).
    flow = FieldFlow([[6, 5]])
    flow.add_water(0, 0, 50)
    d_head = (6 - 5) * HEAD_SCALE + 50
    want = (d_head * DEFAULT_CONDUCTANCE) >> 8
    assert want == 9
    processed, moved = flow.tick()
    assert moved == want
    assert flow.snapshot() == [[50 - want, want]]


# ------------------------------------------------------------- the bridge ----
def test_from_board_loads_dem_to_board_output():
    board = d2b.build_board("S", d2b.synthetic_rows(161), "synthetic")
    flow = FieldFlow.from_board(board)
    assert (flow.h, flow.w) == (64, 64)
    grid = [[board["nodes"][f"g{y}x{x}"]["elev"] for x in range(64)]
            for y in range(64)]
    assert flow.elev == grid
    wy, wx = _coords(board["dem_board"]["waste_cell"])
    assert flow.waste == {(wy, wx)}
    assert flow.total_volume() == 0 and flow.settled()


def test_from_board_pour_in_the_crater_is_deterministic():
    board = d2b.build_board("S", d2b.synthetic_rows(161), "synthetic")
    runs = []
    for _ in range(2):
        flow = FieldFlow.from_board(board)
        flow.add_water(32, 32, 800)             # the cone peak / crater rim
        for _ in range(300):
            flow.tick()
        assert flow.total_volume() == 800       # closed board: nothing lost
        runs.append(flow.snapshot())
    assert runs[0] == runs[1]


def test_from_board_rejects_malformed_nodes():
    with pytest.raises(ValueError, match="no nodes"):
        FieldFlow.from_board({"schema": "water_graph.v1"})
    with pytest.raises(ValueError, match="want g"):
        FieldFlow.from_board({"nodes": {"bogus": {"elev": 1}}})


def test_constructor_validation():
    with pytest.raises(ValueError, match="non-empty"):
        FieldFlow([])
    with pytest.raises(ValueError, match="rectangular"):
        FieldFlow([[1, 2], [3]])
    with pytest.raises(ValueError, match="waste cell"):
        FieldFlow([[1, 2]], waste={(0, 5)})
    with pytest.raises(ValueError, match="cross_section"):
        FieldFlow([[1]], cross_section=0)
    with pytest.raises(ValueError, match="amount"):
        FieldFlow([[1]]).add_water(0, 0, 0)
    with pytest.raises(ValueError, match="outside the grid"):
        FieldFlow([[1]]).add_water(1, 0, 5)


# -------------------------------------------------------------- perf sanity ----
def test_perf_64x64_1000_ticks_report_only():
    # Deterministic integer cone (cratered like the synthetic tile), a
    # constant drip on the upper flank, 1000 ticks. No timing assert (CI
    # machines differ); the measured ms lands in the Z5 receipt.
    n, c = 64, 32
    elev = []
    for y in range(n):
        row = []
        for x in range(n):
            d = math.isqrt((y - c) * (y - c) + (x - c) * (x - c))
            e = 120 - 3 * d if d < 40 else 0
            if d < 6:                           # crater bowl inside the cone
                e = 60 - 6 * d
            row.append(max(e, 0))
        elev.append(row)
    flow = FieldFlow(elev)
    t0 = time.perf_counter()
    for _ in range(1000):
        flow.add_water(c, c - 8, 6)             # drip onto the north flank
        flow.tick()
    ms = (time.perf_counter() - t0) * 1000
    assert flow.total_volume() == 1000 * 6      # every drop accounted for
    assert all(v >= 0 for row in flow.snapshot() for v in row)
    print(f"\n[perf] 64x64, 1000 drip ticks: {ms:.1f} ms "
          f"(total_processed={flow.total_processed} cells, "
          f"moved={flow.total_moved} units)")


def _coords(name: str) -> tuple[int, int]:
    idx = name.index("x", 1)
    return int(name[1:idx]), int(name[idx + 1:])
