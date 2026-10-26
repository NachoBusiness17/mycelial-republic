# B3 NETCODE - snapshot interpolation v0 on the mountain wire (2026-09-30)

Mission: build netcode v0 in GDScript per Gaffer-on-Games in the empty
`network/` dir. MID-FLIGHT CORRECTION applied (counter-route lane,
`watch/inbox/mountain_climb/ROUTE_COUNTER.md`): the-mountain's client
already exists and predicts nothing; prediction was DROPPED, and the
build became an extension of the existing client, not a parallel one.

## What the existing client already covered (NOT rebuilt)

`roblox_to_godot/scripts/net_client.gd`, byte-identical to
`the-mountain/game/scripts/net_client.gd` (diff exit 0 this session,
HEAD 7d5dbe2 per ROUTE_COUNTER's ledger): connect, hello/sid, line
framing (`\n` JSON, MAX_LINE), op dispatch to signals (welcome/tick/
ack/reject), MOUNTAIN_SERVER env retarget, render-only mirror
philosophy, no prediction by design. Every one of those bytes is
untouched; `network/net_client.gd` EXTENDS this file.

## What landed (the ~2 files + wiring + tests)

| File | Owns |
|---|---|
| `roblox_to_godot/network/snapshot_buffer.gd` | Gaffer ring buffer: last 32 snapshots stamped with a local monotonic clock; `sample(render_t)` linearly interpolates node volumes between the two bracketing snapshots, clamped into the window (starved render FREEZES on the newest truth, never extrapolates); `crossed()` delivers events/winner exactly once when the render clock passes their snapshot; stale tick numbers (n <= newest) never enter |
| `roblox_to_godot/network/net_client.gd` | The interpolation layer: `extends "res://scripts/net_client.gd"`; intercepts ONLY the `tick` op (never reaches the transport's direct apply), re-emits the inherited `ticked` signal per render frame with t-100ms interpolated volumes (INTERP_DELAY_MS := 100); every other op passes through `super._handle_line` unchanged, so game.gd's dual-mode switch (PROBING -> AUTHORITATIVE on welcome, SOVEREIGN on the 2s probe deadline) is byte-identical; law counters (`rubber_band_frames`, `max_truth_error`) + `stats()` |
| `roblox_to_godot/scripts/game.gd` | ONE preload line swapped to `res://network/net_client.gd` (receipted in-file). Same signals, same surface; `_on_net_tick` now receives interpolated floats (its `int()` truncation is the integer-law apply). Rest of the file untouched (sibling lanes own the rest of its working-tree diffs) |
| `tests/test_netcode_v0.py` | 5 tests: .gd byte pins (extends path, constants, tick interception, NO prediction: no `func send_action`/`acked.emit`/`_pred`, no wall clock, 0 em-dashes, game.gd wiring), mirror unit laws (dedupe, capacity, clamp, endpoint identity, exactly-once cursor, draining-node corridor), and the LIVE run |

Dropped per ROUTE_COUNTER and STAYED dropped: client input prediction
("prediction is polish, not existence"; whole-unit, no-randomness,
human-paced game). The prediction design sketches from the first half
of this lane were discarded before landing; nothing predicts, stages,
or swallows acks.

## Verification (real numbers, trust bytes)

- `./.venv/Scripts/python.exe -m pytest tests/test_netcode_v0.py -q`:
  5 passed in 11.30s. Live law: 300 ticks against an in-process
  WorldServer (ephemeral port, 20ms cadence, real TCP), buffer reached
  and held CAPACITY 32, render ran ~280+ frames, `rubber_band_frames`
  0, `max_truth_error` 0.0, endpoint identity (sampling AT a tick's
  stamp == its exact volumes) 0.0 error across all ticks, events/winner
  cursor == never-trimmed ledger oracle every frame (winner fired
  exactly once, sticky), DRY_POOL + RATE_CAP rejects and 12+ acks rode
  the passthrough lanes, p_bypass really opened server-side.
- Neighbors stay green: test_flock_positive, test_motion_rows,
  test_mountain_units, test_water_graph, test_server_v0:
  125 passed in 13.82s.
- The estate box still has NO Godot binary
  (watch/inbox/GODOT_SLICE_20260929.md): the .gd bytes are
  LANDED-as-code, PLAYED-by-no-one-yet; the laws ran on the byte-mirror
  Python client (AC5 mirror pattern) with structural pins against drift.
- Fix receipt (build discipline): the first live 300-tick run counted 10
  phantom rubber-band violations, all on DRAINING nodes mid-segment;
  cause: the envelope read lower-snapshot/upper-snapshot instead of the
  per-node min/max truth corridor; fixed in both .gd and mirror, pinned
  by `test_draining_node_renders_inside_its_corridor`. The live run
  earning its keep.

## Honest scope notes

- The mission's path `roblox_to_godot/game/network/` never existed
  (bytes); the empty netcode dir MC3/ROUTE_COUNTER meant is
  `roblox_to_godot/network/` (README: "core/, network/, water/ are
  empty placeholders"). Landed there. The README line is now stale for
  network/ - README.md is outside this lane's file ownership, left for
  its owner.
- Water law shapes the action policy: 8 units total, waste terminal, so
  boils go quiet once the mountain drains; valves never dry out and
  carry the 300-tick wire. The static settled tail is the game's own
  determinism, not a test dodge.
- Interpolation renders volumes as floats between integer truths;
  game.gd truncates at apply (int law stays server-side).

## v1 debt (named, not hidden)

Extrapolation on starvation (v0 freezes); pipes in the tick payload so
other clients' valve moves reach the mirror (v0 wire debt, already
receipted in game.gd's ack handler); input prediction if a stranger's
missing-list ever prices it (ROUTE_COUNTER's own gate); reconnect /
mid-session loss signal (inherited transport debt); server tick feel
pass (800ms vs local 500ms).

Filing: this file is the receipt. No commit (mission law). Em-dash
count: 0. Census note: tests/ gained test_netcode_v0.py (+1 file, +5
collected) after the 2026-09-27 census; within the 7-day window, no
patrol trip.
