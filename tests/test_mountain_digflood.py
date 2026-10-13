"""mountain_digflood tests — the DFHack moment on a synthetic dam board.

LM6 (2026-09-30): `dig` is the operator's hand, the water obeys the
physics. Each test pins one law: load builds the River from a
water_graph.v1 board (g{y}x{x} grammar, waste outlets, silt mantle);
dig lowers one cell and spoils it as silt (logged, bounded); the dam
holds WITHOUT the dig (drained == 0) and breaches WITH it (drained > 0,
incision, a growing delta) — the classic moment itself; meters survive
the state round-trip; flood-report prints the dossier honestly; and the
whole session is byte-deterministic (same commands -> same state file).

Board geometry (tuned, cross_section 1000): the reservoir FLOORS slope
to the dam (80/70/62/55) so poured water arrives moving instead of
standing on its spring (a flat floor self-captures: the spring incises
below its outlet — rung 4's documented stall — and the breach never
drains). The dam crest at 72 tops the deep floor (55) by 17 elev units
= 4352 volume units of head: a 1920-unit pour can never overtop it. One
26-deep dig at the crest (72 -> 46, below the 55 floor, above the 35
downstream) breaks it open. The St Helens 64x64 board is exercised in
the receipt (LM6_DIGFLOOD), not here — the suite stays fast.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import tools.mountain_digflood as mdf  # noqa: E402


# ------------------------------------------------------------- boards ----
def ridge_board(h: int = 5, w: int = 9) -> dict:
    """The dam board: sloping reservoir (80/70/62/55) behind a 72 crest
    at col 4, a downstream slope 35/20/10/3, and the sea = east column."""
    nodes = {}
    for y in range(h):
        for x in range(w):
            if x < 4:
                e = (80, 70, 62, 55)[x]
            elif x == 4:
                e = 72                        # the dam crest
            else:
                e = (35, 20, 10, 3)[x - 5]    # the downstream slope
            nodes[f"g{y}x{x}"] = {"elev": e,
                                  "kind": "waste" if x == 8 else "plain",
                                  "sill": 0, "volume": 0}
    return {"schema": "water_graph.v1", "nodes": nodes, "pipes": {},
            "tick": 0,
            "dem_board": {"tile_id": "RIDGEDAM", "shape": [h, w],
                          "board_hash": "a" * 12,
                          "waste_cell": "g2x8"}}


def write_board(tmp_path: Path, board: dict | None = None) -> Path:
    p = tmp_path / "ridge_board.json"
    p.write_text(json.dumps(board if board is not None else ridge_board()),
                 encoding="utf-8")
    return p


def session(tmp_path: Path, dig: tuple[int, int, int] | None = None,
            rate: int = 8, ticks: int = 240, board: Path | None = None,
            tag: str = "s") -> Path:
    """load [dig] pour -> the state path (the full DF moment)."""
    state = tmp_path / f"{tag}.json"
    b = str(board or write_board(tmp_path))
    assert mdf.main(["load", "--board", b, "--state", str(state)]) == 0
    if dig is not None:
        x, y, k = dig
        assert mdf.main(["dig", str(x), str(y), "-k", str(k),
                         "--state", str(state)]) == 0
    assert mdf.main(["pour", "0", "2", "-n", str(rate), "-t", str(ticks),
                     "--state", str(state)]) == 0
    return state


# --------------------------------------------------------------- load ----
def test_load_builds_river_mantle_and_baseline(tmp_path):
    state_path = tmp_path / "s.json"
    assert mdf.main(["load", "--board", str(write_board(tmp_path)),
                     "--state", str(state_path)]) == 0
    state = mdf.read_state(state_path)
    assert state["schema"] == "digflood.v1"
    assert state["board"]["tile_id"] == "RIDGEDAM"
    assert state["board"]["shape"] == [5, 9]
    assert state["board"]["waste"] == [[y, 8] for y in range(5)]
    river = mdf.river_from_state(state)
    assert river.elev[2][0] == 80 and river.elev[2][4] == 72
    assert river.waste == {(y, 8) for y in range(5)}
    # mantle on every land cell (45 - 5 waste), none on the sea
    assert river.total_silt() == 40 * 6
    assert river.silt[2][8] == 0
    assert state["baseline_elev"] == river.elev   # pristine, pre-dig
    assert state["digs"] == [] and state["pours"] == []


# ---------------------------------------------------------------- dig ----
def test_dig_lowers_elev_and_spoils_silt(tmp_path):
    state_path = tmp_path / "s.json"
    assert mdf.main(["load", "--board", str(write_board(tmp_path)),
                     "--state", str(state_path)]) == 0
    assert mdf.main(["dig", "4", "2", "-k", "26",
                     "--state", str(state_path)]) == 0
    state = mdf.read_state(state_path)
    river = mdf.river_from_state(state)
    assert river.elev[2][4] == 46, "the breach: 72 - 26"
    assert river.silt[2][4] == 6 + 26, "mantle + spoil"
    assert state["baseline_elev"][2][4] == 72, "the baseline never moves"
    assert state["digs"] == [{"x": 4, "y": 2, "depth": 26,
                              "before": 72, "after": 46, "tick": 0}]


def test_dig_rejects_bounds_waste_and_bad_depth(tmp_path):
    state_path = tmp_path / "s.json"
    assert mdf.main(["load", "--board", str(write_board(tmp_path)),
                     "--state", str(state_path)]) == 0
    for argv in (["dig", "99", "0", "--state", str(state_path)],
                 ["dig", "0", "99", "--state", str(state_path)],
                 ["dig", "8", "2", "--state", str(state_path)],   # the sea
                 ["dig", "4", "2", "-k", "0", "--state", str(state_path)]):
        assert mdf.main(argv) == 2, f"{argv} must fail cleanly"


# ------------------------------------------------- the DF moment itself ----
def test_without_dig_the_dam_holds(tmp_path):
    state_path = session(tmp_path, dig=None, tag="noleak")
    river = mdf.river_from_state(mdf.read_state(state_path))
    assert river.drained == 0, "no breach, no drainage — the lake pools"
    wet_xs = [x for y in range(5) for x in range(9) if river.vol[y][x] > 0]
    assert wet_xs and max(wet_xs) <= 3, "water stays behind the dam"
    path = mdf.thalweg(river, 2, 3)
    assert path[-1][1] <= 3, "no path through the wall (walk stays behind)"


def test_breach_drains_erodes_and_builds_a_delta(tmp_path):
    state_path = session(tmp_path, dig=(4, 2, 26), tag="breach")
    state = mdf.read_state(state_path)
    river = mdf.river_from_state(state)
    assert river.drained > 0, "the lake must find the dug channel"
    assert any(river.vol[y][x] > 0 for y in range(5) for x in range(5, 8)), \
        "wet cells downstream of the breach"
    assert river.total_eroded > 0, "the channel must incise"
    assert river.elev[2][4] < 46, "the water keeps carving the dug notch"
    grew = river.delta_silt() > 0 or river.elev[2][8] > 3
    assert grew, "the delta must grow at the waste (silt parked or bed raised)"
    # the audits the report makes: silt conserved (vs first-pour total),
    # elev accounted (hand-dug + water-carved - landed)
    assert river.total_silt() == state["silt_at_first_pour"]
    dug = sum(d["depth"] for d in state["digs"])
    e0 = sum(sum(r) for r in state["baseline_elev"])
    assert e0 - river.total_elev() == dug + river.total_eroded \
        - river.total_deposited
    assert river.tick_count == 240


# ---------------------------------------------------------- the report ----
def test_flood_report_prints_the_dossier(tmp_path, capsys):
    state_path = session(tmp_path, dig=(4, 2, 26), tag="rep")
    capsys.readouterr()
    assert mdf.main(["flood-report", "--state", str(state_path)]) == 0
    text = capsys.readouterr().out
    river = mdf.river_from_state(mdf.read_state(state_path))
    for needle in ("flood-report", "wetted cells:", "max flow path",
                   "erosion:", "silt:", "delta:", "audit: silt CONSERVED",
                   "elev accounting"):
        assert needle in text, f"report must carry {needle!r}"
    assert f"wetted cells: {river.wet_cells()} " in text
    assert "RIDGEDAM" in text and "g2x8" in text
    trace = tmp_path / "trace.txt"
    assert mdf.main(["flood-report", "--state", str(state_path),
                     "--trace", str(trace)]) == 0
    assert trace.read_text(encoding="utf-8").startswith("flood-report")


# --------------------------------------------------- determinism + state ----
def test_session_is_byte_deterministic(tmp_path, capsys):
    board = write_board(tmp_path)
    a = session(tmp_path, dig=(4, 2, 26), board=board, tag="a")
    capsys.readouterr()
    b = session(tmp_path, dig=(4, 2, 26), board=board, tag="b")
    capsys.readouterr()
    assert a.read_bytes() == b.read_bytes(), \
        "same command sequence -> byte-identical state"


def test_meters_survive_the_state_round_trip(tmp_path):
    state_path = session(tmp_path, dig=(4, 2, 26), tag="meters")
    river = mdf.river_from_state(mdf.read_state(state_path))
    again = mdf.river_from_state(mdf.read_state(state_path))
    assert again.drained == river.drained > 0
    assert again.total_eroded == river.total_eroded
    assert again.total_deposited == river.total_deposited
    assert again.tick_count == river.tick_count


# -------------------------------------------------------------- thalweg ----
def test_thalweg_walks_the_carved_bed_to_the_sea():
    # dry confined slope: 50/40/30/20/10/0 with walls, sea at (1, 5)
    w = 6
    elev = [[70] * w for _ in range(3)]
    for x in range(w):
        elev[1][x] = 50 - x * 10
    river = mdf.River(elev, waste={(1, 5)},
                      silt=[[0] * w for _ in range(3)])
    path = mdf.thalweg(river, 1, 0)
    assert path == [(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    # a pit stops the walk: carve a hole mid-slope
    river.elev[1][3] = 5
    path2 = mdf.thalweg(river, 1, 0)
    assert path2[-1] == (1, 3) and len(path2) == 4


def test_thalweg_crosses_the_dug_notch_to_the_sea(tmp_path):
    state_path = tmp_path / "s.json"
    assert mdf.main(["load", "--board", str(write_board(tmp_path)),
                     "--state", str(state_path)]) == 0
    assert mdf.main(["dig", "4", "2", "-k", "26",
                     "--state", str(state_path)]) == 0
    river = mdf.river_from_state(mdf.read_state(state_path))
    path = mdf.thalweg(river, 2, 3)          # from the dam face, dry bed
    assert (2, 4) in path, "the walk must cross the dug notch"
    assert path[-1] in river.waste, "and run out to the sea"


# ------------------------------------------------------------ failure ----
def test_load_missing_board_and_missing_state_fail(tmp_path):
    assert mdf.main(["load", "--board", str(tmp_path / "nope.json"),
                     "--state", str(tmp_path / "s.json")]) == 2
    assert mdf.main(["flood-report",
                     "--state", str(tmp_path / "nope.json")]) == 2
