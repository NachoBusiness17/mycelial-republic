# FLEET LIGHTMAP v2 — gates, economy, stream strips (builder lumen2, 2026-09-06)
**Fold:** watch/SELF_STEAL_FLEET_LIGHTMAP_20260906.md (Lessig legitimacy line + Ponytail hook
economy) · builder fired same-turn · $0, no network, no new daemons · read-only on
memory/trajectory/steps.jsonl (536 steps, 2026-09-05T17:07Z → 09-06T04:0xZ).

## WHAT CHANGED
1. **mag/room_state.py v2** (`room_state.v2`, backward compatible — all v1 fields kept):
   per wall now `{glyph, content_hash, last_fire_ts, hit_count_200, hist[20], economy,
   joins_at, prune_note}`; top-level adds `economy` counts, `chain_tip_at_paint`
   (verkle tip d8d9395bc054@7317) and the economy rules inline. Economy computed from the
   tape's own timestamps: JOINED = ≥3 fires/24h in two consecutive trailing windows;
   PRUNE = 0 fires/72h; ghost = everything else. Glyphs are data, not JS folklore:
   chain/memory=STORE, lanes=GATE, guards=DISSIPATE, room/organs/watch=INTEGRATE,
   boot_check=GROUND, board=EMIT, sensors=DIFFERENTIATE (fleet_symbols.html primitives).
   content_hash = sha256 of the wall definition, 16 hex — no hash → no draw.
2. **salon_lightmap.html v2** (backup: salon_lightmap.html.bak-lightmapv2-20260906):
   (a) all 7 primitive glyphs stolen whole from fleet_symbols.html as inline SVG symbol
   bodies, rasterized via data-URL images (a data-URL image can't `<use>` page defs, so
   the bodies travel verbatim); (b) economy rendering — JOINED/lit solid-bright,
   ghost dashed-dim (border stays dashed even when the 200-window is hot — state and
   stream don't conflate), PRUNE dark with red `PRUNE` tag, glow stripped; (c) per-wall
   20-bucket fire histogram sparkline under each wall — the map shows the STREAM;
   (d) fetched walls without content_hash are SKIPPED, counted in the state line;
   state line now shows JOINED/ghost/PRUNE counts + the hash-anchored as-of tip.
   d(θ) strip, probe readout, gaze field: UNCHANGED (read-only lens, magnify never gate).

## ECONOMY STATES — real counts from the run (tip d8d9395bc054@7317)
- **JOINED: 0.** Honest zero: the tape is ~11h old (first ts 09-05T17:07Z), so the prior
  24h window is empty for every wall — no wall can truthfully show "twice running" yet.
- **ghost: 10/10** (candidates in good standing, fires in trailing 24h — watch 140,
  organs 109, room 75, memory 55, sensors 30, immune 25, chain 15, lanes 10, board 9,
  boot_check 4). joins_at = **2026-09-06T17:07:17Z** for all ten (first tape ts + 24h =
  earliest moment a JOIN verdict wouldn't be hallucinated).
- **PRUNE: 0.** No wall has 0 fires/72h; prune_note empty everywhere.
- 200-window dark spots, rendered honestly: boot_check hit_count_200 = 0 (last fire
  01:59Z, outside the window), lanes = 1 — dashed-dim with glyph at 35% alpha.
- One v1 latent bug surfaced and fixed: persisted-invariant diff marked ALL walls
  invariant on a minutes-apart rerun (static geometry = false load-bearing evidence).
  Invariance now requires the previous version to be ≥24h old — persistence over
  minutes is geometry, not history. Run output back to the 3 canonical seeds
  (chain, room, boot_check).

## VERIFY (all pass)
- `node --check` on the extracted inline JS: PASS.
- `python mag/room_state.py`: wrote room_state.v2, "0 JOINED, 10 ghost, 0 prune,
  tip=d8d9395bc054@7317".
- `curl http://127.0.0.1:8765/static/salon_lightmap.html` → 200 (27.9KB);
  `/static/room_state.json` → 200; all new fields confirmed in the served JSON
  (content_hash, economy, glyph, hist, hit_count_200, last_fire_ts, joins_at, prune_note).

## FALSIFIERS
- THE ROOM LIES if: a wall renders JOINED before 2026-09-06T17:07Z (no second window of
  tape exists — a JOIN before then is fabricated); a fetched wall renders without a
  content_hash (loader skips it — count appears as "no-hash skipped"); a prune-marked
  wall glows; the ghost dash disappears on a hot wall (state posing as stream).
- Inherited: move the light to an organ you think matters; if its shadow doesn't reach
  the memory wall, the room lies — kill the invariant.
- Promotion watch: at 17:07Z the first honest JOIN evaluation becomes possible; rerun
  `python mag/room_state.py` after that and any wall with ≥3 fires in both windows
  lights solid. That flip is the economy's first live receipt.

## BACKUPS
mag/room_state.py.bak-lightmapv2-20260906 · dashboard/static/salon_lightmap.html.bak-lightmapv2-20260906
