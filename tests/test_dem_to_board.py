"""dem_to_board — terrain bridge tests (GB_TERRAIN_FEED lane 2/6).

Covers the three mission asks: the .hgt reader (big-endian parse, void
mapping), converter determinism (same tile -> same board hash, hash law
recomputed independently), and cold/waste auto-tagging (closed-depression
floors only — terrace steps that leak downhill are not lakes) — plus the
water_graph.v1 contract so the Watershed lane can consume the board
blind. The synthetic generator gets small-grid unit tests here; the full
1201x1201 CLI run is exercised in the receipt (X7_STHELENS).
"""
from __future__ import annotations

import array
import hashlib
import json
import sys

import pytest

import tools.dem_to_board as d2b


# ------------------------------------------------------------- fixtures ----
def write_fixture(path, rows):
    """Write an .hgt the way SRTM does: big-endian int16, row-major."""
    buf = array.array("h", [v for row in rows for v in row])
    if sys.byteorder == "little":
        buf.byteswap()
    path.write_bytes(buf.tobytes())
    return path


@pytest.fixture
def small_hgt(tmp_path):
    # 4x4 with values > 127 (a missing byteswap would garble them), a
    # void (-32768), and a hand-checkable layout.
    return write_fixture(tmp_path / "N00E000.hgt", [
        [100, 200, 300, 400],
        [500, 600, -32768, 700],
        [800, 900, 1000, 1100],
        [1200, 1300, 1400, 1500],
    ])


@pytest.fixture
def synth_rows():
    # Small odd-sized synthetic (161x161) — same generator, fast in-suite.
    return d2b.synthetic_rows(161)


# --------------------------------------------------------------- reader ----
def test_reader_parses_fixture_and_maps_void(small_hgt):
    size, rows = d2b.read_hgt(small_hgt)
    assert size == 4
    assert rows == [
        [100, 200, 300, 400],
        [500, 600, 0, 700],          # void -> 0, not -32768
        [800, 900, 1000, 1100],
        [1200, 1300, 1400, 1500],
    ]


def test_reader_big_endian_regardless_of_host(tmp_path):
    # 500 = 0x01F4: read little-endian it decodes to 0xF401 = 62465 —
    # a missing byteswap cannot hide behind small values.
    p = write_fixture(tmp_path / "T.hgt", [[500, 1], [1, 500]])
    _, rows = d2b.read_hgt(p)
    assert rows[0][0] == 500


def test_reader_rejects_non_square(tmp_path):
    p = tmp_path / "T.hgt"
    p.write_bytes(b"\x00" * 12)      # 6 int16s — not a square grid
    with pytest.raises(ValueError, match="not a square"):
        d2b.read_hgt(p)


def test_write_hgt_roundtrips_through_read(tmp_path):
    # no void values: read_hgt maps -32768 to 0 by design, so a pure
    # roundtrip test must stay away from the sentinel.
    rows = [[-100, 0, 2500], [32767, -5, 7], [1, 2, 3]]
    p = tmp_path / "R.hgt"
    d2b.write_hgt(p, rows)
    assert d2b.read_hgt(p) == (3, rows)


# ------------------------------------------------------------- converter ----
def test_block_means_exact_partition():
    # 4x4 -> 2x2 blocks; every cell counted exactly once, sum//count.
    rows = [[1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 12],
            [13, 14, 15, 16]]
    assert d2b.block_means(rows, 2) == [[3, 5], [11, 13]]
    # 5x5 -> 2x2: integer partition gives 2x2 and 3x3 blocks (no floats);
    # means are sum//count over each ragged block.
    rows5 = [[v for v in range(r * 5, r * 5 + 5)] for r in range(5)]
    means = d2b.block_means(rows5, 2)
    assert means == [[3, 5], [15, 18]]


def test_normalize_bounds_and_flat():
    assert d2b.normalize([[0, 500], [1000, 250]]) == [[0, 127], [255, 63]]
    assert d2b.normalize([[7, 7], [7, 7]]) == [[0, 0], [0, 0]]


def test_converter_determinism_same_tile_same_hash(synth_rows, tmp_path):
    b1 = d2b.build_board("T", synth_rows, "synthetic")
    p = tmp_path / "T.hgt"
    d2b.write_hgt(p, synth_rows)     # file round-trip must not drift it
    b2 = d2b.build_board("T", d2b.read_hgt(p)[1], "file")
    assert b1["dem_board"]["board_hash"] == b2["dem_board"]["board_hash"]
    assert b1["nodes"] == b2["nodes"]


def test_different_tile_different_hash(synth_rows):
    b1 = d2b.build_board("T", synth_rows, "synthetic")
    tweaked = [list(r) for r in synth_rows]
    tweaked[80][80] += 1
    # RESOLUTION FLOOR (law, not bug): a 1 m single-cell bump is below the
    # integer block mean (block count >= 4 cells), so the board is
    # byte-identical — the substrate's quantization, never nondeterminism.
    assert d2b.build_board("T", tweaked,
                           "synthetic")["dem_board"]["board_hash"] \
        == b1["dem_board"]["board_hash"]
    tweaked[80][80] += 1000          # +1001 m moves the block mean by >250
    b2 = d2b.build_board("T", tweaked, "synthetic")
    assert b1["dem_board"]["board_hash"] != b2["dem_board"]["board_hash"]


def test_board_hash_law_is_sha256_of_tile_id_plus_elev_bytes(synth_rows):
    board = d2b.build_board("N46W122", synth_rows, "synthetic")
    grid = [[board["nodes"][f"g{y}x{x}"]["elev"] for x in range(64)]
            for y in range(64)]
    expect = hashlib.sha256(
        b"N46W122" + bytes(v for row in grid for v in row)).hexdigest()
    assert board["dem_board"]["board_hash"] == expect


# ------------------------------------------------------------------ tags ----
def test_cold_tags_closed_depression_floor():
    grid = [[5] * 5 for _ in range(5)]
    grid[2][2] = 1                  # interior pit -> lake
    cold, waste = d2b.tag_cells(grid)
    assert cold == [(2, 2)]
    assert waste == (0, 0)          # flat edge ties break row-major


def test_flat_board_tags_no_cold():
    cold, _ = d2b.tag_cells([[3] * 6 for _ in range(6)])
    assert cold == []


def test_terraces_that_leak_downhill_are_not_lakes():
    # Regression for the first cut (2026-09-29): per-cell local minima read
    # every 1-unit terrace step as a lake and tagged 931/4096 cells on the
    # synthetic. A flat band with a LOWER neighbor leaks — not a lake.
    grid = [[5] * 6 for _ in range(2)] + [[4] * 6 for _ in range(4)]
    cold, _ = d2b.tag_cells(grid)
    assert cold == []


def test_waste_is_lowest_edge_cell():
    grid = [[9, 9, 9, 9],
            [9, 1, 2, 9],
            [9, 3, 4, 0],           # 0 on the edge beats the interior pit
            [9, 9, 2, 9]]
    cold, waste = d2b.tag_cells(grid)
    assert waste == (2, 3)
    assert cold == [(1, 1)]


def test_flat_floor_patch_tags_all_its_cells():
    # A flat basin floor (how real water surfaces and carved lake beds
    # look after block means) is one connected cold patch, not one cell.
    grid = [[9] * 6 for _ in range(6)]
    for y in (2, 3):
        for x in (2, 3):
            grid[y][x] = 4
    cold, _ = d2b.tag_cells(grid)
    assert cold == [(2, 2), (2, 3), (3, 2), (3, 3)]


def test_synthetic_tags_crater_and_lake_cold(synth_rows):
    board = d2b.build_board("S", synth_rows, "synthetic")
    hdr = board["dem_board"]
    kinds = {n: v["kind"] for n, v in board["nodes"].items()}
    colds = hdr["cold_cells"]
    # Spirit-Lake-style flat floor -> a plural patch, crater floor -> more.
    assert len(colds) >= 2
    elev = {n: v["elev"] for n, v in board["nodes"].items()}
    assert all(elev[c] < 255 for c in colds)          # basins, not the rim
    # waste is a single edge cell at the lowest edge elevation.
    n = 64
    edge = [elev[f"g{y}x{x}"] for y in range(n) for x in range(n)
            if y in (0, n - 1) or x in (0, n - 1)]
    assert elev[hdr["waste_cell"]] == min(edge)
    assert list(kinds.values()).count("waste") == 1
    # cold cells are interior and their nodes carry the tag.
    for c in colds:
        y, x = int(c[1:c.index("x")]), int(c[c.index("x") + 1:])
        assert 0 < y < n - 1 and 0 < x < n - 1
        assert kinds[c] == "cold"


def test_synthetic_generator_is_deterministic():
    assert (d2b.synthetic_rows(101) == d2b.synthetic_rows(101)
            and d2b.synthetic_rows(101)[0][0] != 0)


# --------------------------------------------------- water_graph v1 feed ----
def test_board_is_water_graph_v1_loadable(synth_rows, tmp_path):
    board = d2b.build_board("S", synth_rows, "synthetic")
    p = tmp_path / "b.json"
    p.write_text(json.dumps(board), encoding="utf-8")
    spec = json.loads(p.read_text(encoding="utf-8"))
    assert spec["schema"] == "water_graph.v1"

    from mag.water_graph import from_spec
    g = from_spec(spec)
    assert len(g.nodes) == 64 * 64
    assert g.pipes == {}
    for name, node in g.nodes.items():
        y, x = name[1:name.index("x")], name[name.index("x") + 1:]
        assert name == f"g{y}x{x}"
        assert 0 <= node.elev <= 255 and node.volume == 0 and node.steam == 0
        assert node.kind in ("plain", "cold", "waste")


def test_download_tile_name_validation():
    with pytest.raises(ValueError, match="bad tile name"):
        d2b.download_tile("garbage")
