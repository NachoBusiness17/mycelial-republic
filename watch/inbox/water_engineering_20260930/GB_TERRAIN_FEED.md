# GB - TERRAIN -> WATERSHED FEED (lane 2/6, 2026-09-30)

## The bridge

1. **Format + reader.** SRTM tiles ship as `.hgt`: 1 deg x 1 deg, 1201x1201 big-endian signed-int16 meters (voids = -32768). Stdlib-only reader: `array.array('h').frombytes(...)` + `byteswap()` - no pip dep.
2. **Converter** (`dem_to_board`, feeds `mag/hydrology.py`): stride-sample to 64x64 blocks, block mean via `sum//count` (integers only); normalize `elev = (h-min)*255//(max-min)`; emit 4096 nodes `g{y}x{x}`, elev 0-255, volume 0, kind plain (auto-tag: lowest edge cell `waste`, lake cells `cold`); board hash = `sha256(tile_id + bytes(elev_grid))` in the spec - same tile, byte-identical board.
3. **Payoff.** Mt St Helens quad, tile `N46W122.hgt` (free 30m SRTM): crater rim ~255, lava dome peak, Spirit Lake as `cold`, Toutle River outlet as `waste` - the 1980 blast zone playable on the estate's integer substrate.

Substrate: mag/water_graph.py Node (name, elev:int, kind, sill, volume, steam); target: WF rung 2 (heightfield sheet-flow); determinism law: integers only, no RNG.
