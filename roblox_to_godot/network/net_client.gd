extends "res://scripts/net_client.gd"
## NetClient - netcode v0: Gaffer snapshot interpolation on the W1 wire (B3).
##
## AN EXTENSION OF THE EXISTING CLIENT, NOT A PARALLEL ONE: this class
## extends the-mountain transport verbatim (roblox_to_godot/scripts/
## net_client.gd, byte-identical to the-mountain/game/scripts/
## net_client.gd at HEAD 7d5dbe2, ROUTE_COUNTER source ledger). The
## transport keeps owning everything it already covered: connect, hello,
## sid bookkeeping, line framing, MOUNTAIN_SERVER retarget, ack/reject
## passthrough, render-only mirror philosophy. This layer adds exactly
## one thing the transport lacked: TIME - when the client renders server
## truth.
##
## WHAT IT ADDS (Gaffer, "Snapshot Interpolation", gafferongames.com):
##   - every tick payload is buffered (SnapshotBuffer, last N stamps)
##     instead of applied the instant it lands;
##   - the world is rendered as it was INTERP_DELAY_MS ago, linearly
##     interpolated between the two bracketing snapshots, on the render
##     clock (every _process frame), never extrapolated: a starving
##     buffer freezes on the newest sample rather than guessing;
##   - events and winner deliver exactly once, when the render clock
##     crosses the snapshot that carried them.
##
## WHAT IT DELIBERATELY DOES NOT ADD (ROUTE_COUNTER 2026-09-30,
## watch/inbox/mountain_climb/ROUTE_COUNTER.md): client-side input
## prediction. The mountain is whole-unit, no-randomness, human-paced;
## the wire is server-authoritative and the client owns no state.
## "Prediction is polish, not existence" - it is v1 debt, re-priced
## against a stranger's missing-list. send_action stays the inherited
## passthrough; nothing here predicts, stages, or swallows.
##
## THE SWITCH (mission #3): "tick" lines never reach the transport's
## direct-apply path (no super call), and the inherited `ticked` signal
## is re-emitted per render frame with interpolated volumes - same
## signal shape, same consumers. game.gd's dual-mode law is untouched:
## its PROBING -> AUTHORITATIVE switch rides the welcome, SOVEREIGN is
## the 2s probe deadline fallback, and its AUTHORITATIVE handler stays
## byte-identical while rendering a 100ms-behind, smooth world.
##
## Clock law: _clock accumulates _process deltas (the flock.gd sim_time
## law: never the wall clock), stamps arrivals, and drives sampling.
##
## Verification: the estate box has no Godot binary
## (watch/inbox/GODOT_SLICE_20260929.md); tests/test_netcode_v0.py runs
## these laws as a byte-mirrored Python client against a LIVE WorldServer
## and pins these bytes structurally. LANDED-as-code,
## PLAYED-by-no-one-yet. Receipt:
## watch/inbox/last_mile_20260930/B3_NETCODE.md.

const SnapshotBuffer := preload("res://network/snapshot_buffer.gd")

const INTERP_DELAY_MS := 100  # the Gaffer render delay: t - 100ms
const INTERP_DELAY_S := INTERP_DELAY_MS / 1000.0
const RUBBER_EPS := 1.0e-6   # float dust tolerance of the envelope law

var _clock := 0.0            # delta-accumulated render clock (never the wall clock)
var _snap_buf := SnapshotBuffer.new()  # renamed: parent declares _buf as the wire PackedByteArray; redeclaring broke parse (B14 blocked checks)
var _events_cursor_n := 0    # exactly-once side-channel cursor
var _winner_emitted := false # winner fires once per connection, not per frame

# Law counters (tests/test_netcode_v0.py mirrors these byte-for-byte;
# a future HUD/debug lane may read stats()).
var render_frames := 0       # frames an interpolated world was emitted
var rubber_band_frames := 0  # frames rendered OUTSIDE the bracket envelope (law: 0)
var max_truth_error := 0.0   # worst |rendered - bracket-truth corridor| exit (law: 0.0)


func _process(delta: float) -> void:
	if _down:
		return  # socket gone: hold the last applied world, same silence law as the transport
	_clock += delta
	super._process(delta)  # transport polls + drains; tick lines detour into the buffer below
	_render_tick()


func _handle_line(text: String) -> void:
	# The one interception point: "tick" feeds the buffer (and never
	# reaches the transport's direct apply); every other op passes
	# through unchanged, so welcome/ack/reject/auth_failed keep firing
	# on the base signals exactly as game.gd already consumes them.
	var parsed: Variant = JSON.parse_string(text.strip_edges())
	if typeof(parsed) != TYPE_DICTIONARY:
		return  # same drop law as the transport's handler
	var msg: Dictionary = parsed
	if String(msg.get("op", "")) == "tick":
		_snap_buf.push(
			int(msg.get("n", 0)),
			_clock,
			msg.get("nodes", {}),
			msg.get("events", []),
			bool(msg.get("winner", false))
		)
		return
	super._handle_line(text)


func _render_tick() -> void:
	# The render clock: sample the world as it was INTERP_DELAY_S ago,
	# clamp inside the buffered window (freeze, never extrapolate), and
	# re-emit the inherited ticked signal with the interpolated volumes.
	if not welcomed_flag:
		return
	var rt := _clock - INTERP_DELAY_S
	var frame: Dictionary = _snap_buf.sample(rt)
	if frame.is_empty():
		return  # fewer than two snapshots: game.gd keeps the welcome-seeded world
	var nodes: Dictionary = frame["nodes"]
	# Rubber-band law: an interpolated value must sit inside the truth
	# corridor of its own brackets, always - PER NODE min/max, because a
	# draining node moves DOWNWARD between brackets (fix receipt: the
	# first live 300-tick run counted 10 phantom violations exactly on
	# decreasing nodes mid-segment; the corridor is the bracket pair's
	# min/max, not lower-snapshot/upper-snapshot). Any frame outside is
	# a pathology (stale dedupe failure, bracket bug), counted, never
	# rendered silently.
	var lo: Dictionary = frame["lo_nodes"]
	var hi: Dictionary = frame["hi_nodes"]
	for key in nodes:
		var name := String(key)
		var v := float(nodes[name])
		var va := float(lo.get(name, 0))
		var vb := float(hi.get(name, 0))
		var floor_v := minf(va, vb)
		var ceil_v := maxf(va, vb)
		if v < floor_v - RUBBER_EPS or v > ceil_v + RUBBER_EPS:
			rubber_band_frames += 1
			max_truth_error = maxf(max_truth_error, maxf(floor_v - v, v - ceil_v))
	# Side channels exactly once, when the render clock crosses the
	# snapshot that carried them; winner fires once per connection.
	var crossed: Dictionary = _snap_buf.crossed(rt, _events_cursor_n)
	_events_cursor_n = int(crossed["n"])
	var winner := false
	if bool(crossed["winner"]) and not _winner_emitted:
		_winner_emitted = true
		winner = true
	render_frames += 1
	ticked.emit(int(frame["n"]), nodes, crossed["events"], winner)


func stats() -> Dictionary:
	# Read-only law surface for tests/debug: buffer occupancy, render
	# cadence, and the two zero-laws (envelope exits, truth error).
	return {
		"buffered": _snap_buf.size(),
		"capacity": SnapshotBuffer.CAPACITY,
		"newest_n": _snap_buf.newest_n(),
		"events_cursor_n": _events_cursor_n,
		"interp_delay_ms": INTERP_DELAY_MS,
		"render_frames": render_frames,
		"rubber_band_frames": rubber_band_frames,
		"max_truth_error": max_truth_error,
	}
