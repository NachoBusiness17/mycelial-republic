# AC9 — FULL RESMOKE after V5 economy fix + Godot wave (particles, terrain, brain, hydrology, feel, juice)

Date: 2026-09-30 · Lane: AC9 (ZCode) · No commit (per lane law).
File ownership: this receipt only. **Zero game/server files edited — no crash
found, the one-bug-fix budget went unspent.** Throwaway harness
`roblox_to_godot/ac9_harness.gd` created, run, **deleted** (X8/W3 idiom);
`git status roblox_to_godot/` carries no trace of this lane.

## Mission

V5 made waste a basin (STARVED routes, `_move` accumulates) in the Python
engine the server runs; the Godot client gained particles, terrain, brain
wiring, hydrology, feel fixes, juice, and the drawn HUD since W3's smoke.
Re-run the full smoke at intensity and answer: does the V5 engine change
break any existing client assumptions?

## Instrument

- Binary: `tools/godot/Godot_v4.3-stable_win64_console.exe`, `--headless`,
  `--path roblox_to_godot`, from repo root.
- Stages 2-4 harness: `res://ac9_harness.gd` (SceneTree + inner Probe node),
  instantiates the real `scenes/main.tscn`, injects REAL `InputEventKey`s via
  `Input.parse_input_event`, counts frames, hooks NetClient signals, prints
  `AC9SMOKE` telemetry, quits. Env: `SMOKE_FRAMES`, `SMOKE_PRESS="frame:KEY"`,
  `MOUNTAIN_SERVER` (read by net_client.gd, untouched).
- Pipeline verified before scoring: H at frame 30 flipped `hydrology=true`
  headless (`/tmp/ac9_pipeline.log`).

## Results — pass/fail table

| # | Stage | Shape | Exit | ERROR/WARN lines | Evidence | Verdict |
|---|-------|-------|------|------------------|----------|---------|
| 1 | 60 frames | `--quit-after 60` | 0 | 0 | banner only, clean | **PASS** |
| 2 | 300 frames, T@150 | harness `SMOKE_PRESS="150:T"` | 0 | 0 | terrain `N46W122` 64x64 loaded, `load_error=''`, own graph ticked 4x, `visible=true`; Mountain board `waste=8 TOTAL=8`; `brain_fallback_frames=0` | **PASS** |
| 3 | 300 frames, H@100 | harness `SMOKE_PRESS="100:H"` | 0 | 0 | `hydrology=true` at report (flipped live at 100), graded-Q8 law, `TOTAL=8` with `waste=4` HELD, `brain_fallback_frames=0` | **PASS** |
| 4 | Authoritative: bg server + client 900 frames | `python -m server.server` (temp users ada/steam + temp world log, port 8800) + client `MOUNTAIN_SERVER=127.0.0.1:8800` | 0 (client AND server) | 0 (client AND server) | `mode=AUTHORITATIVE`, `welcomes=1`, **8 tick broadcasts** (last `n=35`), `acks=0 rejects=0`; last tick `waste=8 node_sum=8` and the client MIRRORED it (`VOLS waste=8 TOTAL=8`); local `tick_count=0` (server-sole-mutator law HELD); server chain 103 rows, `load_log_rows` own check PASS, seq 1..103 no gaps, waste=8 from tick 8 and never lost | **PASS** |

**4/4 PASS. Zero ERROR/WARNING/SCRIPT ERROR lines across all runs** (sweep
`grep -i "error|warning|crash|leak|assert"` over the five logs, telemetry
lines excluded).

## Key question — does V5 (waste holds volume) break client assumptions?

**No. Nothing broke, and the feared client/server divergence is already gone.**

- The `.gd` mirror **already carries the V5 law**: AC5's port
  (`AC5_GD_MIRROR.md`, uncommitted working tree) landed before this lane's
  scored runs — stage 2 PROVED it live: sovereign board settled `waste=8`
  with `TOTAL=8` (pre-V5 bytes deleted to 0; the old STARVED `node.volume=0`
  is gone from the working tree). Stage 3 proved the hydrology branch holds
  too (`waste=4`, `TOTAL=8`).
- Authoritative mode: the server tick now carries `waste=8`; the client's
  `_on_net_tick`/`_apply_snapshot` mirror plain node volumes, so it rendered
  waste=8 with no parse or range trouble. The HUD waste bar clamps at
  `WORLD_WATER=8` (exactly full, no overflow); `_wettest_pool` skips waste;
  the win law reads crown only — **no assumption anywhere breaks on a
  non-zero waste**.
- Terrain (T@150) loads clean on the current tree — the terrain board runs
  the `.gd` mirror, which now conserves: no `STARVED` deletion events fired
  in any log.
- Fish brain held every stage: `brain_fallback_frames=0` in all scored runs.

## Notes

- Server stage setup (W3 law, no repo files touched): temp
  `AuthStore` `%TEMP%/ac9_users.json` (user ada/steam via `ensure_user`),
  `--log %TEMP%/ac9_world.jsonl`, `--users %TEMP%/ac9_users.json`; port 8800
  confirmed quiet, server stopped after the run (listener gone, only
  TIME_WAIT sockets).
- The harness itself needed one Variant-inference fix (project treats GDScript
  warnings as errors) — an edit to MY throwaway probe file, not a product
  bug-fix; no product file was touched.
- Working-tree drift observed mid-session (not this lane's edits): AC5's
  `water_graph.gd` mirror fix appeared between session start and the scored
  runs; `game.gd` + untracked `hud.gd` (AA5) were present throughout and ran
  clean.
- Receipt law: every number above is from an executed run's captured output
  (`/tmp/ac9_s1_60f.log`, `ac9_pipeline.log`, `ac9_s2_t150.log`,
  `ac9_s3_h100.log`, `ac9_s4_auth.log`; server `%TEMP%/ac9_server.log`,
  `%TEMP%/ac9_world.jsonl`), never estimated.
