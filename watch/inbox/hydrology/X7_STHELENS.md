# X7 - TERRAIN BRIDGE LANDED (2026-09-29)

Design: `watch/inbox/water_engineering_20260930/GB_TERRAIN_FEED.md` (lane 2/6).
Deliverable: `tools/dem_to_board.py` + `tests/test_dem_to_board.py`, outputs in
`logs/terrain/`. Stdlib only, integers only, no RNG, no floats — the
determinism law holds end to end. No commit (operator's push).

## What landed

1. **Reader** `read_hgt`: `array('h').frombytes` + `byteswap` on little-endian
   hosts, voids (-32768) -> 0 m, square-size derived from byte length (SRTM3
   1201 and SRTM1 3601 both parse; non-square rejects). `write_hgt` is the
   exact inverse so `--synthetic` rides the same reader path as a download.
2. **Converter** `build_board`: integer-partition 64x64 blocks (block y covers
   rows `[y*H//64, (y+1)*H//64)` — full coverage, zero overlap), block mean
   `sum//count`, normalize `(h-min)*255//(max-min)`, 4096 nodes `g{y}x{x}`,
   volume 0, kind plain; emits a `water_graph.v1` spec that
   `mag.water_graph.from_spec` loads verbatim (the Watershed lane consumes it
   blind — tested). Board hash `sha256(tile_id + bytes(elev_grid))`.
3. **Auto-tags**: `waste` = single lowest edge cell, row-major tie-break (the
   outlet). `cold` = interior CLOSED-DEPRESSION FLOORS: 4-connected flat
   regions strictly higher on every boundary side (board edge counts as
   draining). Real water surfaces and crater floors are flat and rimmed, so
   they tag; terrain that leaks downhill does not.
4. **`--synthetic`**: deterministic fake tile (2400 m cone + 400 m crater +
   Spirit-Lake-style basin NE of it with a 1150 m floor clamp + 1 m/8-row
   tilt), geometry proportional to grid size (1201 = reference).
5. **`--download NAME`**: unauthenticated mirrors — AWS Open Data skadi
   (`.hgt.gz`, gunzipped) then viewfinderpanoramas dem1 (zip). Failure exits 3
   and names the tile OWED; it never fabricates.

## Real runs (2026-09-29, Mag venv)

- `--synthetic` (twice, byte-identical): `logs/terrain/SYNTH_STHELENS.hgt`
  2,884,802 bytes; 1201x1201 -> 64x64, 530..2029 m; hash
  `7b1401a8986b5796d7703ab40a06c108faf99fa32f59d752a40bc8ca87f710da` (both
  runs); waste `g61x0`; cold 6 cells — lake floor `g27x37`, crater floor
  cluster `g33x29..g35x30`.
- `--download N46W122`: LANDED, not owed — 25,934,402 bytes SRTM1 3601x3601
  from `elevation-tiles-prod.s3.amazonaws.com/skadi/N46/N46W122.hgt.gz`;
  267..4193 m (Rainier owns the tile max, so the design's "crater rim ~255" is
  tile-relative — St Helens rim lands ~148); hash
  `25e926f09e3b65d219edd7c5fc545ca3698cad80708e41e25eaf167265e7d84c`;
  re-converting the on-disk tile reproduces the same hash. waste `g30x0`
  (west edge, ~46.5N — Toutle drainage side). cold 238 cells = every closed
  basin at 1.7 km block resolution (what WF rung 2 sheet-flow will pool
  anyway), including crater/blast-zone `g50x12`, `g52x9` and Spirit Lake
  `g45x9`, `g45x12`.
- `pytest tests/test_dem_to_board.py -q`: **18 passed in 0.94s** (first run
  of the fresh file: 4 failed -> 12 passed after test-side fixes; see
  corrections). Re-ran green after every code edit.
- Full-suite `pytest -q`: NOT COMPLETED — two background attempts both
  aborted mid-run with no summary line (first at 38%, second at 59%
  progress, `exit=1` written by the wrapper, log
  `logs/terrain/full_suite_20260929.log`); death points differ, so it is
  not a fixed killer test, and the bridge's 18 tests pass at the head of
  the run. No full-suite pass/fail count is claimed here because none was
  byte-produced; the operator owes the suite a clean foreground run if a
  number is needed.

## Corrections made mid-build (cause + evidence)

- **Tagging rule replaced.** First cut tagged per-cell local minima; the
  synthetic's 1 m/8-row tilt terraces read as lakes — 931/4096 cold cells
  (rows g1x1-g1x8). Closed-depression floors are the physical definition:
  re-run tags 6 synthetic / 238 real, all rimmed flats. Regression test
  `test_terraces_that_leak_downhill_are_not_lakes` pins it.
- **Synthetic geometry was absolute, not proportional** — cone center (row
  640) sat outside a 161x161 test tile, so small-grid tests passed vacuously
  on an empty plain. Geometry now scales with n; tests see real terrain.
- **Skadi URL is `.hgt.gz`, not `.hgt`** — bare URL 404s; S3 list-API probe of
  `skadi/N46/` showed all keys gzipped. Mirror fixed + gunzip added.
- **Resolution floor pinned as law**: a +1 m single-cell bump is below the
  integer block mean (>= 4 cells/block) and legitimately yields a
  byte-identical board — quantization, not nondeterminism; +1001 m moves the
  hash. Test documents both directions.

## Owed / next

- None owed on this lane's contract. Natural next: Watershed rung 2 consumes
  `*_board.json` (elev grid + waste outlet + cold floors are already in the
  spec's node kinds, so sheet-flow needs zero terrain-side changes).
