# W3 — FULL-STACK SMOKE: everything landed, run it at intensity

Date: 2026-09-30 · Lane: W3 (ZCode) · Commit: NONE (per lane law)
File ownership: this receipt only. **Zero game/server files edited — zero
bugs found, so the one-bug-fix-per-file budget was never spent.**

## Mission

Everything has landed in the Godot client (hydrology mode, water particles,
terrain loader, fish brain wiring, feel fixes, flee tuning, motion rows,
dual-mode net_client). Run the headless engine at increasing intensity and
report pass/fail per stage. Any ERROR line = a bug: fix small, file big.

## Instrument

- Binary: `tools/godot/Godot_v4.3-stable_win64_console.exe` (4.3 stable),
  `--headless`, from repo root, `--path roblox_to_godot`.
- Stages 1-2: canonical `--quit-after {60,300}` (README/Z3 idiom).
- Stages 3-5: throwaway SceneTree harness `res://w3_smoke_harness.gd`
  (X8 run-then-delete idiom; created, run, **deleted after the last run** —
  `git status roblox_to_godot/` clean of it). It instantiates the real
  `scenes/main.tscn`, injects REAL `InputEventKey`s through
  `Input.parse_input_event` (the true input pipeline — verified delivering
  headless before the scored runs: H at frame 30 flipped `graph.hydrology`
  true), counts frames, hooks net signals, prints W3SMOKE telemetry, quits.
- Headless runs uncapped (~130 fps solo, ~75 fps with the 4096-node terrain
  board live); Timer/server cadences are wall-clock, so tick counts below are
  real-time-derived, not frame-derived.

## Results — full pass/fail table

| # | Stage | Command shape (env) | Exit | ERROR lines | Evidence | Verdict |
|---|-------|---------------------|------|-------------|----------|---------|
| 1 | 60 frames (baseline) | `--quit-after 60` | 0 | 0 | banner only, 1.4 s | **PASS** |
| 2 | 300 frames (feel-pass duration) | `--quit-after 300` | 0 | 0 | banner only, 3.2 s | **PASS** |
| 3 | 900 frames, **T at 300** (load) **+ T at 600** (unload) | harness, `SMOKE_PRESS="300:T,600:T"` | 0 | 0 | terrain loaded `N46W122` 4096 nodes, rain 3 at g9x15, own graph ticked 9x, `visible=false` after second T, `load_error=""`; Mountain board kept running below (24 water ticks, spring 6->0, no-input drain to waste is correct physics); `brain_fallback_frames=0` | **PASS** |
| 4 | 300 frames, **H at 100** (hydrology toggle mid-run) | harness, `SMOKE_PRESS="100:H"` | 0 | 0 | `hydrology=true` at report (flipped live from boolean verdict), 4 water ticks under the graded-Q8 head law, mode fell SOVEREIGN after the 2 s probe deadline, `brain_fallback_frames=0` | **PASS** |
| 5 | **Authoritative mode**: `python -m server.server` (background) + client via net_client | harness, `MOUNTAIN_SERVER=127.0.0.1:8800`, 900 frames, net signals hooked | 0 | 0 (client AND server) | `mode=AUTHORITATIVE`, `welcomes=1`, **7 tick broadcasts received** (last `n=38`; server up ~30 s at 800 ms/tick — consistent), `acks=0 rejects=0`; local graph `tick_count=0` (the render-only law HELD: server is the sole mutator); server hash-chained log 61 ticks, `waste=8` settle state (untended board drains — correct), no server exceptions | **PASS** |

**5/5 PASS. Zero ERROR lines, zero WARNING lines, zero SCRIPT ERRORs across
all runs** (sweep: `grep -i "error|warning|crash|leak|assert"` over all six
logs — the sixth being the pre-stage pipeline-verification run).

## Stage-5 setup notes (why, so it reproduces)

- `server/users.json` is EMPTY (`{"users": {}}`) — hello as ada/steam would
  take BAD_AUTH and fall sovereign. The server's `--users` flag pointed at a
  temp store (`%TEMP%/w3_users.json`, user `ada`/`steam` via AuthStore) and
  `--log` at `%TEMP%/w3_world_smoke.jsonl`, so no repo file was touched for
  auth. Port 8800 confirmed quiet before bind; server stopped after the run.
- The Godot client needed no changes: `game.gd` already probes 127.0.0.1:8800
  at boot (`MOUNTAIN_SERVER` env honored) and flips AUTHORITATIVE on welcome.

## Findings

- **Bugs found: none.** No bug-fix edits were made to any file; the budget
  went unspent. The everything-landed tree executes clean at all five
  intensities, both head laws, both net modes, terrain load AND unload.
- Fish brain (Z7 motion rows) held the whole run in every stage:
  `brain_fallback_frames=0` everywhere — zero illegal rows, zero fallbacks.
- Working-tree note (NOT this lane's edit): `roblox_to_godot/v4_probe.gd`
  shows deleted in `git status`. It was itself a "run-then-delete" throwaway
  probe (V4 lane's own header says so) that got swept into mega-commit
  f6af8bf1d; its disappearance is probe cleanup catching up, pre-existing at
  receipt time. Left untouched.
- Receipt law kept: every number above is from an executed run's captured
  output (`/tmp/w3_s1_60f.log`, `w3_s2_300f`, `w3_s3_t300`, `w3_s4_h100`,
  `w3_s5_auth`, `w3_pipeline_test`), never estimated.
