extends RefCounted
## FishBrain — the flock policy as a pure decide() (X9, 2026-09-30).
## Port of systems/flock.gd step() into the protocol table's motion
## dialect: idle/flee/pursue/carry/dance rows, each emitted as
##   {"verb": String, "intensity_q8": int 0..255, "dir": pool node name}.
## A row is legal iff it passes MOTION_TABLE.ask(verb, "AUTHED", row,
## pool_names) in server/protocol_table.py — this file never re-implements
## validation, it only emits; the rig (game.gd) applies, never re-derives.
## The boid math becomes policy: what flock.gd computed as steering
## accelerations, decide() classifies into ONE named motion per fish per
## tick, so the same row can drive local steering AND a server proposal.
##
## DETERMINISM LAW (the W1 leak lesson, flock.gd:32 receipt): decide() is a
## PURE function of (fish_id, tick, snapshot). No RNG, no wall clock, no
## scene tree, no state, no mutation of the snapshot — same inputs in,
## same row bytes out, every call. The estate box has no Godot binary
## (watch/inbox/GODOT_SLICE_20260929.md:37), so purity is enforced by
## construction and by tests/test_motion_rows.py structural laws; the
## first executed determinism run lands when a binary does.
##
## SNAPSHOT CONTRACT (game.gd builds it per frame; nothing here writes it):
##   {
##     "fish": [{"pos": Vector2, "vel": Vector2, "fatigue": float,
##               "alive": bool}, ...],        # flock.fish, order-stable
##     "player_pos": Vector2,                 # player.global_position
##     "pools": {String: Vector2},            # node name -> board position
##     "wettest": String,                     # game.gd _wettest_pool()
##   }

# R7 2026-09-30 (Q15/V2ASK3): these six were hand-copied mirrors of
# flock.gd / game.gd values — and FLEE_RADIUS had already drifted (this
# file kept the pre-V6 14 while flock.gd moved to 20; V6_FISH_FLEE.md's
# named handoff). All are aliased from systems/game_constants.gd now, the
# single source both lanes read; tests/test_game_constants.py guards the
# registered names against raw literals outside that file.
const GC := preload("res://systems/game_constants.gd")
const FLEE_RADIUS := GC.FLEE_RADIUS     # threat distance (V6/Z14 tuning: 20 — this file's stale 14 trued up)
const CATCH_RADIUS := GC.CATCH_RADIUS   # the tired window is catchable (the player's verb, cited)
const SCHOOL_RADIUS := GC.SCHOOL_RADIUS # dance needs schoolmates
const TRAIL_RADIUS := GC.TRAIL_RADIUS   # pursue urgency normalizer
const TIRED := GC.TIRED                 # catch window / trail-drop threshold
const POOL_PREF_DIST := GC.POOL_PREF_DIST  # pursue fires beyond the prefer ring


static func _q8(x: float) -> int:
	return int(round(clampf(x, 0.0, 1.0) * 255.0))


static func _nearest_pool(pos: Vector2, pools: Dictionary) -> String:
	var best_name := ""
	var best_d := INF
	var names_: Array = pools.keys()
	names_.sort()
	for p: String in names_:
		var d: float = pos.distance_to(pools[p])
		if d < best_d:
			best_d = d
			best_name = p
	return best_name


static func _farthest_pool(pos: Vector2, pools: Dictionary) -> String:
	var best_name := ""
	var best_d := -1.0
	var names_: Array = pools.keys()
	names_.sort()
	for p: String in names_:
		var d: float = pos.distance_to(pools[p])
		if d > best_d:
			best_d = d
			best_name = p
	return best_name


## The policy: one motion row per fish per tick. Branch order mirrors
## flock.gd step()'s own evaluation order (threat -> tire/catch window ->
## school/pool pull -> wiggle), so the port is a classification of the
## boid math, not a new opinion.
static func decide(fish_id: int, tick: int, snapshot: Dictionary) -> Dictionary:
	var fish: Array = snapshot.get("fish", [])
	var pools: Dictionary = snapshot.get("pools", {})
	var wettest: String = snapshot.get("wettest", "")
	if fish_id < 0 or fish_id >= fish.size() or pools.is_empty():
		return {"verb": "idle", "intensity_q8": 0, "dir": wettest}
	var f: Dictionary = fish[fish_id]
	if not bool(f.get("alive", false)):
		return {"verb": "idle", "intensity_q8": 0, "dir": wettest}

	var pos: Vector2 = f["pos"]
	var fatigue: float = float(f.get("fatigue", 0.0))
	# No player in the snapshot = no threat (parked far outside FLEE_RADIUS).
	var player: Vector2 = snapshot.get("player_pos", pos + Vector2(FLEE_RADIUS * 4.0, 0.0))
	var threat_d: float = pos.distance_to(player)

	# 1) FLEE (flock.gd:48-50): threat inside FLEE_RADIUS and not spent.
	#    Urgency = proximity (closer player, harder flee); the escape target
	#    is the pool farthest from the player, ties broken by name.
	if threat_d < FLEE_RADIUS and fatigue < 1.0:
		return {"verb": "flee",
				"intensity_q8": _q8(1.0 - threat_d / FLEE_RADIUS),
				"dir": _farthest_pool(player, pools)}

	# 2) CARRY (flock.gd:77,85 + game.gd POOL_PULL): the tired window —
	#    drag owns the fish and the school's pull toward water carries it.
	#    Intensity = fatigue itself, q8.
	if fatigue >= TIRED:
		return {"verb": "carry", "intensity_q8": _q8(fatigue), "dir": wettest}

	# 3) PURSUE (game.gd _pull_fish_to_water): a fresh fish beyond the
	#    prefer ring steers to the wettest pool; urgency = distance
	#    normalized by the trail radius.
	if wettest != "" and pools.has(wettest):
		var d_home: float = pos.distance_to(pools[wettest])
		if d_home > POOL_PREF_DIST:
			return {"verb": "pursue",
					"intensity_q8": _q8(d_home / TRAIL_RADIUS),
					"dir": wettest}

	# 4) DANCE vs IDLE (flock.gd:74 wiggle + the tire/rest else-branch):
	#    with schoolmates inside SCHOOL_RADIUS the wiggle is the swim —
	#    dance, its intensity the pure tick-driven wiggle phase; alone and
	#    fresh the fish rests — idle, its intensity how much rest remains.
	#    Schoolmate identity is the INDEX (Dictionary == is by value;
	#    flock.gd:64's `other == f` skips value-twins, the index does not).
	var schoolmates := 0
	for i in fish.size():
		if i == fish_id:
			continue
		var other: Dictionary = fish[i]
		if not bool(other.get("alive", false)):
			continue
		if pos.distance_to(other["pos"]) < SCHOOL_RADIUS:
			schoolmates += 1
	if schoolmates > 0:
		return {"verb": "dance",
				"intensity_q8": _q8((sin(float(tick) * 0.7 + pos.x * 0.05) + 1.0) / 2.0),
				"dir": _nearest_pool(pos, pools)}
	return {"verb": "idle",
			"intensity_q8": _q8(1.0 - fatigue),
			"dir": _nearest_pool(pos, pools)}
