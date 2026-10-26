# W1 NET CLIENT - 2026-09-29

Mickey17 Wave 1 lane: Godot client wiring for the estate world server v0.
Owner seat: zcode (GLM-5.3). No git commit (lane order).

## Files

- `roblox_to_godot/scripts/net_client.gd` (NEW, 160 lines): transport
  half of wire v0 (server/protocol.py). StreamPeerTCP to configurable
  host:port; fields + `MOUNTAIN_SERVER` env override ("host" or
  "host:port", read in begin()); hello with user/pass on connect; keeps
  `sid` from welcome; LF-framed JSON line buffer (MAX_LINE 65536,
  mirrors protocol.py); signals: welcomed(world), ticked(n, nodes,
  events, winner), acked(verb, target, applies_at_tick), rejected(why,
  verb, target), auth_failed(why). No world state, no prediction.
- `roblox_to_godot/scripts/game.gd` (edited): dual mode.
- `roblox_to_godot/systems/flock.gd` (edited): wall-clock fix only.

## Dual-mode decision points (game.gd)

1. Probe: `_begin_net_probe()` in `_ready`; welcome inside
   NET_CONNECT_TIMEOUT 2.0s flips mode to AUTHORITATIVE
   (`_on_net_welcomed`); the one-shot NetProbeDeadline Timer (or an
   auth_failed) falls to SOVEREIGN (`_fall_sovereign`: net.stop() +
   free). PROBING plays sovereign until resolved.
2. `_on_water_tick` (~:375): AUTHORITATIVE branch makes the water Timer
   render-only (refresh wettest, no graph.tick()); the server tick
   broadcast `_on_net_tick` applies full node volumes + events to the
   mirror graph (probe-time drift erased; server is sole mutator).
3. `_try_boil` / `_try_valve`: AUTHORITATIVE branches send staged
   proposals via net.send_action (client dry pre-check is UX only; the
   server's DRY_POOL is the real gate); ack and reject feed hint_text
   (`_reject_hint` maps DRY_POOL -> "the pool is dry",
   UNKNOWN_TARGET -> "no valve within reach" per README wiring #3).
   Score: welcome `scores` seeds it, tag events parsed from tick
   broadcasts ("<user> tags a fish at <pool> (score N)"); local catch
   proposes a server `tag` at the nearest wet pool (flock stays
   sensing-only, README wiring #4).

## flock.gd wall-clock fix (wave finding, line 67)

step() now takes `sim_time` (tick counter accumulated in game.gd
_process); the wiggle read Time.get_ticks_msec() before, so runs never
matched and pauses distorted the school. Receipt comment in file.

## Verification (all 2026-09-29, byte-real commands)

- Mandated: `"tools/godot/Godot_v4.3-stable_win64_console.exe"
  --headless --path roblox_to_godot --quit-after 60` -> only the engine
  banner, exit 0, zero errors (parse preserved).
- Extended: same with `--quit-after 300` (crosses the 2s probe deadline;
  connection-refused -> sovereign fallback exercised) -> zero errors,
  exit 0.
- LIVE smoke against the real server (temp users file + temp log under
  ~/.w1smoke, port 8899, MOUNTAIN_SERVER override; temp SceneTree script
  driving net_client.gd, deleted after):
  `SMOKE welcomed sid=0a5094f8 nodes=[crown,gate1,hollow,spring,terrace,waste]`
  `SMOKE sent boil spring ok=true`
  `SMOKE reject DRY_POOL boil spring` (correct: spring had drained on
  the idle server by tick 16; typed reject path proven)
  `SMOKE tick 16..18 nodes={...} winner=false` (broadcasts parsed)
  exit 0. Server stopped, temp files removed.

## Laws

- Em-dash 0 in authored text. One nuance: the win-label string (the one
  ending "R, em-dash, climb again.") is pre-existing text moved verbatim
  from _on_water_tick into the shared `_crown_filled()` helper so the
  authoritative path reuses it; moved not authored, file count drops
  from 2 copies to 1.
- Fix comments carry receipts (flock.gd wall-clock, _crown_filled move,
  net_client framing guard).
- Not committed, per lane order.

## Debt noticed (v1, not lane scope)

- Tick payload carries node volumes only: other clients' valve toggles
  never reach the mirror (own toggles are mirrored on ack, render-only).
- No mid-session loss signal after welcome (net goes dark silently).
- Plaintext password in hello (server README already owns this).
