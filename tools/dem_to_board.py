"""dem_to_board — terrain bridge: SRTM .hgt -> 64x64 water_graph board.

Design: watch/inbox/water_engineering_20260930/GB_TERRAIN_FEED.md (lane 2/6).
The estate's water substrate (mag/water_graph.py, soon mag/hydrology.py
"Watershed" rung 2 heightfield sheet-flow) plays on an integer 64x64 board;
real terrain ships as SRTM .hgt tiles. This tool is the bridge between them.

  1. Reader: .hgt = 1 deg x 1 deg grid of BIG-ENDIAN signed int16 meters
     (SRTM3 1201x1201, SRTM1 3601x3601 — size is derived from file length,
     any square tile parses). Stdlib only: array('h').frombytes() +
     byteswap(). Voids (-32768) map to 0 m.
  2. Converter: integer-partition the tile into 64x64 blocks (block y covers
     rows [y*H//64, (y+1)*H//64) — every cell counted exactly once), block
     mean = sum//count, normalize (h-min)*255//(max-min) to 0-255. Emits
     4096 nodes g{y}x{x} as a water_graph.v1 spec (from_spec loads it
     directly): volume 0, kind plain, auto-tags — the single lowest edge
     cell (tie-break row-major) is `waste` (the outlet), interior closed-
     depression floors (flat regions strictly higher on every side — lake
     surfaces, crater floors) are `cold`.
  3. Board hash: sha256(tile_id + bytes(elev_grid row-major)) — same tile,
     byte-identical board (the determinism law: integers only, no floats,
     no RNG, anywhere in this file).

  --synthetic generates a deterministic St-Helens-flavored fake tile
  (cone + crater + lake basin, pure integer math) so the whole path is
  testable with zero downloads; --download fetches a real tile from a
  public mirror (AWS Open Data terrain-tiles/skadi first, viewfinder
  panoramas fallback).

Outputs land in logs/terrain/ (this tool's durable root). No effects beyond
files; the switchboard is not involved.
"""
from __future__ import annotations

import argparse
import array
import gzip
import hashlib
import io
import json
import math
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TERRAIN_DIR = REPO / "logs" / "terrain"

GRID = 64                       # board edge -> GRID*GRID nodes
VOID = -32768                   # SRTM nodata sentinel
SYNTHETIC_TILE_ID = "SYNTH_STHELENS"

# Public mirrors for unauthenticated .hgt, tried in order (2026-09-29):
#   skadi (AWS Open Data terrain tiles) serves GZIPPED .hgt.gz — the bare
#   .hgt URL 404s; verified by S3 list-API probe of skadi/N46/ before the
#   N46W122 fetch landed. viewfinderpanoramas (1" SRTM, zip) is the
#   fallback. e4ftl01.cr.usgs.gov needs Earthdata auth — not listed.
MIRRORS = (
    "https://elevation-tiles-prod.s3.amazonaws.com/skadi/{folder}/{name}.hgt.gz",
    "https://viewfinderpanoramas.org/dem1/{name}.zip",
)


# --------------------------------------------------------------- reader ----
def read_hgt(path: str | Path) -> tuple[int, list[list[int]]]:
    """Parse one .hgt tile -> (size, rows of meters). Big-endian int16,
    voids -> 0. Size is derived from the byte length (1201 SRTM3, 3601
    SRTM1, or any square)."""
    data = Path(path).read_bytes()
    if not data or len(data) % 2:
        raise ValueError(f"{path}: .hgt byte length {len(data)} is empty or odd")
    n = math.isqrt(len(data) // 2)
    if n * n * 2 != len(data):
        raise ValueError(f"{path}: {len(data)} bytes is not a square int16 grid")
    buf = array.array("h")
    buf.frombytes(data)
    if sys.byteorder == "little":
        buf.byteswap()                      # .hgt is big-endian, always
    rows = [[0 if v == VOID else v for v in buf[r * n:(r + 1) * n]]
            for r in range(n)]
    return n, rows


def write_hgt(path: str | Path, rows: list[list[int]]) -> None:
    """Inverse of read_hgt (used by --synthetic so the fake tile rides the
    exact same reader path as a real download)."""
    buf = array.array("h", [v for row in rows for v in row])
    if sys.byteorder == "little":
        buf.byteswap()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(buf.tobytes())


# ------------------------------------------------------------ converter ----
def block_means(rows: list[list[int]], n: int = GRID) -> list[list[int]]:
    """64x64 block means via sum//count. Integer partition: block y covers
    source rows [y*H//n, (y+1)*H//n) — full coverage, no overlap, no
    floats, deterministic for any tile size >= n."""
    h = len(rows)
    if h < n:
        raise ValueError(f"tile edge {h} < block edge {n}")
    means = [[0] * n for _ in range(n)]
    for by in range(n):
        r0, r1 = by * h // n, (by + 1) * h // n
        for bx in range(n):
            c0, c1 = bx * h // n, (bx + 1) * h // n
            s = 0
            for r in range(r0, r1):
                s += sum(rows[r][c0:c1])
            means[by][bx] = s // ((r1 - r0) * (c1 - c0))
    return means


def normalize(means: list[list[int]]) -> list[list[int]]:
    """(h-min)*255//(max-min) to 0-255. Flat tile (max==min) -> all 0."""
    flat = [v for row in means for v in row]
    lo, hi = min(flat), max(flat)
    if hi == lo:
        return [[0] * len(means) for _ in means]
    span = hi - lo
    return [[(v - lo) * 255 // span for v in row] for row in means]


def tag_cells(grid: list[list[int]]) -> tuple[list[tuple[int, int]], tuple[int, int]]:
    """Auto-tags on the normalized 64x64 grid.
    waste = the single lowest EDGE cell (the outlet — Toutle River for St
    Helens); ties break row-major (y, then x), deterministic.
    cold = interior CLOSED-DEPRESSION FLOORS (lake surfaces, crater
    floors — Spirit Lake): 4-connected flat regions whose every boundary
    neighbor is strictly higher (the board edge counts as draining, so a
    flat that leaks downhill or touches the edge is not a lake). The first
    cut used per-cell local minima and read every 1-unit terrain terrace
    as a lake (931/4096 cold cells on the synthetic, 2026-09-29); closed
    basins are the physical definition and tag only real water floors."""
    n = len(grid)
    waste = min(((grid[y][x], y, x) for y in range(n) for x in range(n)
                 if y == 0 or y == n - 1 or x == 0 or x == n - 1))[1:]
    cold: list[tuple[int, int]] = []
    seen = [[False] * n for _ in range(n)]
    for y0 in range(n):
        for x0 in range(n):
            if seen[y0][x0]:
                continue
            e = grid[y0][x0]
            comp: list[tuple[int, int]] = []
            closed = True
            stack = [(y0, x0)]
            seen[y0][x0] = True
            while stack:
                y, x = stack.pop()
                comp.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if not (0 <= ny < n and 0 <= nx < n):
                        closed = False               # edge drains: not a lake
                        continue
                    v = grid[ny][nx]
                    if v == e:
                        if not seen[ny][nx]:
                            seen[ny][nx] = True
                            stack.append((ny, nx))
                    elif v < e:
                        closed = False               # leaks downhill
            if closed:
                cold.extend(comp)
    cold.sort()
    return cold, waste


def board_hash(tile_id: str, grid: list[list[int]]) -> str:
    """sha256(tile_id + bytes(elev_grid row-major)) — the spec's determinism
    seal: same tile bytes -> same board -> same hash."""
    h = hashlib.sha256()
    h.update(tile_id.encode("utf-8"))
    h.update(bytes(v for row in grid for v in row))
    return h.hexdigest()


def build_board(tile_id: str, rows: list[list[int]], source: str,
                n: int = GRID) -> dict:
    """Full bridge: hgt rows -> water_graph.v1 board spec (from_spec loads
    it verbatim; the dem_board header carries what the Watershed lane
    needs to know about its terrain)."""
    means = block_means(rows, n)
    meters_min = min(v for row in means for v in row)
    meters_max = max(v for row in means for v in row)
    grid = normalize(means)
    cold, waste = tag_cells(grid)
    nodes: dict[str, dict] = {}
    for y in range(n):
        for x in range(n):
            kind = "plain"
            if (y, x) == waste:
                kind = "waste"
            elif (y, x) in cold:
                kind = "cold"
            nodes[f"g{y}x{x}"] = {"elev": grid[y][x], "kind": kind,
                                  "sill": 0, "volume": 0, "steam": 0}
    return {
        "schema": "water_graph.v1",
        "dem_board": {
            "tile_id": tile_id,
            "source": source,
            "shape": [n, n],
            "board_hash": board_hash(tile_id, grid),
            "meters_min": meters_min,
            "meters_max": meters_max,
            "cold_cells": [f"g{y}x{x}" for y, x in cold],
            "waste_cell": f"g{waste[0]}x{waste[1]}",
        },
        "tick": 0,
        "nodes": nodes,
        "pipes": {},
    }


# ------------------------------------------------------------ synthetic ----
def synthetic_rows(n: int = 1201) -> list[list[int]]:
    """Deterministic fake tile (cone + crater + lake basin, St-Helens
    flavor) in integer meters — no floats, no RNG, so the file is
    byte-identical on every run and every platform. Geometry is
    proportional to n (1201 = the real SRTM3 reference; smaller n keeps
    the same terrain for fast tests):

      - cone: peak 2400 m at 53%/47% of the tile, base 600 m at 36% radius
      - regional tilt: +1 m per 8 rows northward (breaks symmetry so block
        means are not degenerate; its terraces must NOT read as lakes)
      - crater: 400 m deep bowl (7.5% radius) inside the cone — rim ~255
        after normalize, floor a cold basin
      - lake basin: Spirit-Lake-style bowl NE of the crater (40% row, 58%
        col, 5.8% radius, 480 m carve, flat 1150 m floor clamp) — the
        `cold` cells
    """
    peak, base = 2400, 600
    cy, cx = n * 640 // 1201, n * 560 // 1201
    cone_r = n * 430 // 1201
    crater_r, crater_d = n * 90 // 1201, 400
    ly, lx = n * 520 // 1201, n * 700 // 1201
    lake_r, lake_d, lake_floor = n * 70 // 1201, 480, 1150
    rows: list[list[int]] = []
    for y in range(n):
        dy = y - cy
        dly = y - ly
        row: list[int] = []
        for x in range(n):
            dx = x - cx
            d = math.isqrt(dx * dx + dy * dy)
            h = peak - (peak - base) * d // cone_r if d < cone_r else base
            h += (cy - y) // 8                       # tilt northward
            if d < crater_r:
                h -= crater_d * (crater_r - d) // crater_r
            dlx = x - lx
            d2 = math.isqrt(dlx * dlx + dly * dly)
            if d2 < lake_r:
                h = max(h - lake_d * (lake_r - d2) // lake_r, lake_floor)
            row.append(h)
        rows.append(row)
    return rows


# ------------------------------------------------------------ download ----
def download_tile(name: str = "N46W122",
                  dest_dir: Path = TERRAIN_DIR) -> Path:
    """Fetch one real .hgt from a public mirror (no auth). Raises
    RuntimeError naming what was tried on failure — the caller reports the
    tile as owed, never fabricates one."""
    if len(name) != 7 or name[0] not in "NS" or name[3] not in "WE" \
            or not name[1:3].isdigit() or not name[4:].isdigit():
        raise ValueError(f"bad tile name {name!r} (want e.g. N46W122)")
    dest_dir.mkdir(parents=True, exist_ok=True)
    folder = name[:3]                              # skadi two-degree folder
    errors: list[str] = []
    for template in MIRRORS:
        url = template.format(name=name, folder=folder)
        try:
            with urllib.request.urlopen(url, timeout=90) as resp:
                payload = resp.read()
            if url.endswith(".gz"):                 # skadi ships .hgt.gz
                payload = gzip.decompress(payload)
            elif url.endswith(".zip"):
                zf = zipfile.ZipFile(io.BytesIO(payload))
                inner = [i for i in zf.infolist()
                         if i.filename.endswith(".hgt")][0]
                payload = zf.read(inner)
            if len(payload) < 2:
                raise ValueError(f"payload {len(payload)} bytes")
            out = dest_dir / f"{name}.hgt"
            out.write_bytes(payload)
            return out
        except Exception as exc:                   # noqa: BLE001 — report all
            errors.append(f"{url}: {exc}")
    raise RuntimeError("all mirrors failed: " + " | ".join(errors))


# ------------------------------------------------------------------ cli ----
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("tile", nargs="?", help=".hgt path to convert")
    ap.add_argument("--synthetic", action="store_true",
                    help="generate the deterministic fake tile (cone + "
                         "crater + lake basin), write logs/terrain/"
                         f"{SYNTHETIC_TILE_ID}.hgt, convert it")
    ap.add_argument("--download", nargs="?", const="N46W122", metavar="NAME",
                    help="download a real tile (default N46W122) then convert")
    ap.add_argument("-o", "--out", metavar="JSON",
                    help="board output path (default logs/terrain/<tile>_board.json)")
    args = ap.parse_args(argv)

    if not (args.synthetic or args.download or args.tile):
        ap.error("give a tile path, or --synthetic, or --download [NAME]")

    if args.synthetic:
        hgt_path = TERRAIN_DIR / f"{SYNTHETIC_TILE_ID}.hgt"
        write_hgt(hgt_path, synthetic_rows())
        print(f"[synthetic] wrote {hgt_path.name} "
              f"({hgt_path.stat().st_size} bytes, deterministic)")
    elif args.download:
        try:
            hgt_path = download_tile(args.download)
        except RuntimeError as exc:
            print(f"[download] FAILED — real tile OWED: {exc}", file=sys.stderr)
            return 3
        print(f"[download] {hgt_path.stat().st_size} bytes -> {hgt_path}")

    tile_path = Path(args.tile) if args.tile else hgt_path
    size, rows = read_hgt(tile_path)
    tile_id = tile_path.stem.upper()
    source = ("synthetic (cone+crater+lake, GB_TERRAIN_FEED design)" if args.synthetic
              else f"file:{tile_path}")
    board = build_board(tile_id, rows, source)
    hdr = board["dem_board"]

    out = Path(args.out) if args.out else TERRAIN_DIR / f"{tile_id}_board.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(board, indent=1), encoding="utf-8")

    print(f"[board] {tile_id}: {size}x{size} hgt -> {GRID}x{GRID} nodes "
          f"({meters_range(hdr)})")
    print(f"[board] hash {hdr['board_hash']}")
    print(f"[board] waste (outlet) {hdr['waste_cell']}  "
          f"cold (lake/crater) {len(hdr['cold_cells'])} cells: "
          f"{', '.join(hdr['cold_cells'][:8])}"
          f"{' ...' if len(hdr['cold_cells']) > 8 else ''}")
    print(f"[board] wrote {out} ({out.stat().st_size} bytes)")
    return 0


def meters_range(hdr: dict) -> str:
    return f"{hdr['meters_min']}..{hdr['meters_max']} m"


if __name__ == "__main__":
    raise SystemExit(main())
