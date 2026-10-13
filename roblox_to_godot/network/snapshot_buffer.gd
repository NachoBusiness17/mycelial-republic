extends RefCounted
## SnapshotBuffer - the Gaffer-on-Games snapshot interpolation core (B3).
##
## Pure time-domain buffer: authoritative tick payloads are pushed with a
## LOCAL monotonic clock stamp, and the world is sampled as it was
## RENDER_T seconds ago, interpolated between the two snapshots that
## bracket that instant. Owns no transport, no actions, no world state -
## network/net_client.gd (this file's only consumer) owns those.
##
## Laws (Gaffer, "Snapshot Interpolation", gafferongames.com; receipt
## watch/inbox/last_mile_20260930/B3_NETCODE.md):
##   1. RING: the last CAPACITY snapshots, ascending by stamp. A tick
##      number that does not advance the newest (n <= newest_n) never
##      enters: TCP cannot reorder the wire, so a replayed or duplicated
##      line must not rewind the render.
##   2. INTERPOLATE, NEVER GUESS: sample(render_t) linearly interpolates
##      node volumes between the bracketing snapshots. Entity state
##      between two truths is the segment joining them, never a value
##      beyond either endpoint.
##   3. NO EXTRAPOLATION: render_t clamps into [oldest_t, newest_t]. A
##      starved buffer FREEZES on the newest sample; stale beats a guess
##      the server never sent (the rubber-band disease).
##   4. SIDE CHANNELS ARE NOT INTERPOLATED: events and winner ride their
##      snapshot exactly once, delivered by crossed() when the render
##      clock passes that snapshot's stamp. A cursor remembers what has
##      shipped; nothing renders twice.
##
## Scope (ROUTE_COUNTER 2026-09-30, watch/inbox/mountain_climb/): the
## mountain is whole-unit, no-randomness, human-paced; the client
## predicts NOTHING by design. This buffer closes the real gap - smooth
## rendering from server ticks - and nothing more.
##
## Volumes are integers on the wire and floats in a sample; the integer
## law belongs to the server (server/world.py), the client renders the
## interpolated float and truncates at apply time (game.gd
## _on_net_tick's int()).
##
## Verification: the estate box has no Godot binary
## (watch/inbox/GODOT_SLICE_20260929.md); tests/test_netcode_v0.py runs
## these laws as a byte-mirrored Python buffer and pins this file's
## constants structurally. LANDED-as-code, PLAYED-by-no-one-yet.

const CAPACITY := 32  # snapshots; ~26s of 800ms server ticks, bounded memory

# Ascending by stamp: [{n: int, t: float, nodes: Dictionary,
#                       events: Array, winner: bool}]
var _snaps: Array = []


func push(n: int, t: float, nodes: Dictionary, events: Array, winner: bool) -> bool:
	# Law 1: the ring only moves forward. Duplicate/stale tick numbers
	# are refused (returns false) so the render timeline stays monotone.
	if not _snaps.is_empty() and n <= int(_snaps[_snaps.size() - 1]["n"]):
		return false
	_snaps.append({
		"n": n,
		"t": t,
		"nodes": nodes.duplicate(),
		"events": events.duplicate(),
		"winner": winner,
	})
	if _snaps.size() > CAPACITY:
		_snaps.pop_front()
	return true


func size() -> int:
	return _snaps.size()


func newest_n() -> int:
	# The newest buffered tick number; 0 when nothing has landed yet.
	if _snaps.is_empty():
		return 0
	return int(_snaps[_snaps.size() - 1]["n"])


func sample(render_t: float) -> Dictionary:
	# Law 2 + 3. Returns {} until two snapshots exist, else:
	#   {n: lower bracket tick, hi_n: upper bracket tick, frac: 0..1,
	#    nodes: {name: float}, lo_nodes/hi_nodes: the bracket truths}
	# The bracket truths ride along so the caller can enforce the
	# rubber-band envelope (rendered stays between the brackets).
	if _snaps.size() < 2:
		return {}
	var rt := clampf(render_t, float(_snaps[0]["t"]), float(_snaps[_snaps.size() - 1]["t"]))
	var hi := 1
	while hi < _snaps.size() and float(_snaps[hi]["t"]) < rt:
		hi += 1
	if hi >= _snaps.size():
		hi = _snaps.size() - 1
	var a: Dictionary = _snaps[hi - 1]
	var b: Dictionary = _snaps[hi]
	var span := float(b["t"]) - float(a["t"])
	var frac := 0.0 if span <= 0.0 else (rt - float(a["t"])) / span
	var nodes := {}
	for key in b["nodes"]:
		var name := String(key)
		var va := float(a["nodes"].get(name, 0))
		var vb := float(b["nodes"].get(name, 0))
		nodes[name] = va + (vb - va) * frac
	return {
		"n": int(a["n"]),
		"hi_n": int(b["n"]),
		"frac": frac,
		"nodes": nodes,
		"lo_nodes": a["nodes"],
		"hi_nodes": b["nodes"],
	}


func crossed(render_t: float, cursor_n: int) -> Dictionary:
	# Law 4: everything the render clock has passed since cursor_n.
	# Returns {n: the new cursor, events: exactly-once concatenation,
	# winner: any crossed snapshot won}. Uses the UNCLAMPED render_t: a
	# starving render freezes volumes (sample clamps) but side channels
	# catch up rather than stalling a tick behind forever.
	var events: Array = []
	var winner := false
	var high := cursor_n
	for s in _snaps:
		var snap: Dictionary = s
		if int(snap["n"]) > cursor_n and float(snap["t"]) <= render_t:
			events.append_array(snap["events"])
			winner = winner or bool(snap["winner"])
			high = maxi(high, int(snap["n"]))
	return {"n": high, "events": events, "winner": winner}
