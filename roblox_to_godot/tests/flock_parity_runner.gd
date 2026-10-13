extends SceneTree
## flock_parity_runner.gd — the GDScript side of tools/flock_parity.py
## (R4 2026-09-30, Q14/V2ASK3 pair 1: GDScript <-> Python, the estate's
## proven rule_parity_runner.gd pattern applied to the FLOAT engine).
## Receipt: watch/inbox/last_mile_20260930/R4_FLOCK_PARITY.md.
##
## Headless: tools/godot/Godot_v4.3-stable_win64.exe --headless \
##     --path roblox_to_godot \
##     --script res://tests/flock_parity_runner.gd -- <in.json> <out.jsonl>
##
## Three doc schemas (twins of tools/flock_parity.py):
##   flockframe/1  teacher-forced frames: each tick is a PURE map
##                 input state -> systems/flock.gd step() -> output state.
##                 The driver feeds the reference's float32-quantized output
##                 as the next tick's input, so per-tick error never
##                 compounds (V2ASK3's teacher-forcing law — free-running
##                 boid trajectories are chaotic and would false-fail).
##   flockfree/1   free-run smoke: one initial state, N self-fed ticks,
##                 flock-level statistics only (the V2ASK3 smoke lane).
##   flockcodec/1  float32 codec corpus echo — proves the hex-bits transport
##                 is lossless through the real Godot process.
##
## All floats travel as float32 bit patterns in hex strings ("0x%08x"):
## Godot Vector2 is float32, Python floats are float64, and decimal JSON
## parses differently per runtime — the bits are the only shared alphabet
## (V2ASK3 Q14 codec rule). Byte order is pinned little-endian by hand
## (compose/decompose the PackedByteArray bytes ourselves), verified
## end-to-end by the flockcodec echo.
##
## CONSTANTS GUARD (the Q15 link): the frame carries constants_hash =
## sha256 over "NAME=<float32 bits hex>" lines of game_constants.gd's flock
## family. A runner whose compiled-in constants differ exits 3 and produces
## NO output rows — constant drift is a harness error, never a mysterious
## position diff (V2ASK3: "A runner whose compiled-in constants hash differs
## refuses to run with exit code 3").
##
## This runner MEASURES, never patches: systems/flock.gd is stepped AS-IS.
## Exit 0 = ran (the parity verdict belongs to the comparator), 3 = usage /
## IO / constants guard, 2 = unknown schema.

const Flock := preload("res://systems/flock.gd")
const GC := preload("res://systems/game_constants.gd")

# tools/flock_parity.py CONST_NAMES twin (sorted; the hash text is
# "NAME=bits\n" per line — both sides must byte-match).
const CONST_NAMES := [
	"CATCH_RADIUS", "COAST_TIME", "DRAG", "FATIGUE_DECAY", "FLEE_PUSH",
	"FLEE_RADIUS", "POOL_PREF_DIST", "POOL_PULL", "SCHOOL_RADIUS", "TIRED",
	"TRAIL_DROP", "TRAIL_RADIUS", "WIGGLE",
]

var _rows: int = 0


func _init() -> void:
	var user_args := OS.get_cmdline_user_args()
	if user_args.size() != 2:
		push_error("usage: -- <in.json> <out.jsonl>")
		quit(3)
		return
	var in_path := String(user_args[0])
	var out_path := String(user_args[1])
	var raw := FileAccess.get_file_as_string(in_path)
	if raw.is_empty():
		push_error("cannot read input: " + in_path)
		quit(3)
		return
	var doc: Dictionary = JSON.parse_string(raw)
	if doc == null or not doc.has("schema"):
		push_error("bad input JSON: " + in_path)
		quit(3)
		return
	var expected := _constants_hash()
	if String(doc.get("constants_hash", "")) != expected:
		push_error("constants_hash mismatch: doc=" + String(doc.get("constants_hash", ""))
			+ " game_constants.gd=" + expected
			+ " | gd canonical body:\n" + _constants_body()
			+ " — regenerate the frames (Q15 guard, V2ASK3 Q14/Q15 link)")
		quit(3)
		return
	var fh := FileAccess.open(out_path, FileAccess.WRITE)
	if fh == null:
		push_error("cannot write output: " + out_path)
		quit(3)
		return
	var schema := String(doc["schema"])
	if schema == "flockframe/1":
		_run_teacher(doc, fh)
	elif schema == "flockfree/1":
		_run_free(doc, fh)
	elif schema == "flockcodec/1":
		_run_codec(doc, fh)
	else:
		fh.close()
		push_error("unknown schema: " + schema)
		quit(2)
		return
	fh.close()
	print("gd flock runner: wrote %d rows" % _rows)
	quit(0)


# ---------------------------------------------------------- float32 codec ----
# Little-endian pinned by hand so encode_float/decode_float endianness can
# never silently flip the transport (flockcodec echo proves it end-to-end).

func _f32_to_bits(v: float) -> int:
	var b := PackedByteArray()
	b.resize(4)
	b.encode_float(0, v)
	return int(b[0]) | (int(b[1]) << 8) | (int(b[2]) << 16) | (int(b[3]) << 24)


func _bits_to_f32(bits: int) -> float:
	var b := PackedByteArray()
	b.resize(4)
	b[0] = bits & 0xFF
	b[1] = (bits >> 8) & 0xFF
	b[2] = (bits >> 16) & 0xFF
	b[3] = (bits >> 24) & 0xFF
	return b.decode_float(0)


func _hex32(v: float) -> String:
	return "0x%08x" % _f32_to_bits(v)


func _unhex32(s: String) -> float:
	# Manual nibble parse — GDScript has no int(String, base) constructor
	# and String.hex_to_int availability varies; this cannot.
	var t := s.trim_prefix("0x").to_lower()
	var bits := 0
	for i: int in t.length():
		var d := "0123456789abcdef".find(t[i])
		if d < 0:
			push_error("bad hex32: " + s)
			return 0.0
		bits = (bits << 4) | d
	return _bits_to_f32(bits)


func _vec2(hexpair: Array) -> Vector2:
	return Vector2(_unhex32(String(hexpair[0])), _unhex32(String(hexpair[1])))


# ------------------------------------------------------ constants (Q15) ----

func _constants_hash_text() -> String:
	# Explicit const lookup: script constants are const-expression members,
	# not runtime properties — a hand-built table is the guaranteed accessor.
	# tools/flock_parity.py consts_hash() hashes the byte-identical text.
	var vals := {
		"CATCH_RADIUS": GC.CATCH_RADIUS, "COAST_TIME": GC.COAST_TIME,
		"DRAG": GC.DRAG, "FATIGUE_DECAY": GC.FATIGUE_DECAY,
		"FLEE_PUSH": GC.FLEE_PUSH, "FLEE_RADIUS": GC.FLEE_RADIUS,
		"POOL_PREF_DIST": GC.POOL_PREF_DIST, "POOL_PULL": GC.POOL_PULL,
		"SCHOOL_RADIUS": GC.SCHOOL_RADIUS, "TIRED": GC.TIRED,
		"TRAIL_DROP": GC.TRAIL_DROP, "TRAIL_RADIUS": GC.TRAIL_RADIUS,
		"WIGGLE": GC.WIGGLE,
	}
	var parts: Array[String] = []
	for name: String in CONST_NAMES:
		parts.append(name + "=" + _hex32(float(vals[name])))
	return "\n".join(parts) + "\n"


func _constants_hash() -> String:
	return _constants_hash_text().sha256_text()


func _constants_body() -> String:
	# The hash's preimage (drift debugging: diff against the driver's)
	return _constants_hash_text()


# ------------------------------------------------------- teacher forcing ----

func _decode_fish(raw_fish: Array) -> Array[Dictionary]:
	var out: Array[Dictionary] = []
	for rf: Dictionary in raw_fish:
		out.append({
			"pos": _vec2(rf["pos"]),
			"vel": _vec2(rf["vel"]),
			"fatigue": _unhex32(String(rf["fatigue"])),
			"satiation": _unhex32(String(rf["satiation"])),
			"alive": bool(rf["alive"]),
		})
	return out


## Neighbour ids (sorted) with dist < SCHOOL_RADIUS, alive only — the exact
## Tier-D membership flock.gd's school loop uses, computed on the INPUT
## state so both sides classify the same tick (float32 here, float64 in the
## driver: the comparator's threshold band absorbs the ulp difference).
func _neighbors_of(raw_fish: Array) -> Array:
	var posn: Array[Vector2] = []
	var alive: Array = []
	for rf: Dictionary in raw_fish:
		posn.append(_vec2(rf["pos"]))
		alive.append(bool(rf["alive"]))
	var out: Array = []
	for i: int in raw_fish.size():
		var ids: Array = []
		for j: int in raw_fish.size():
			if j == i or not alive[j]:
				continue
			if (posn[j] - posn[i]).length() < GC.SCHOOL_RADIUS:
				ids.append(int(raw_fish[j]["id"]))
		ids.sort()
		out.append(ids)
	return out


func _run_teacher(doc: Dictionary, fh: FileAccess) -> void:
	var dt := _unhex32(String(doc["dt"]))
	for seq: Dictionary in doc["sequences"]:
		for frame: Dictionary in seq["frames"]:
			var player := _vec2(frame["player"])
			var sim_time := _unhex32(String(frame["sim_time"]))
			var flock: Node = Flock.new()
			flock.fish = _decode_fish(frame["fish"])
			flock.step(player, dt, sim_time)
			var neighbors := _neighbors_of(frame["fish"])
			var fish_out: Array = []
			for i: int in flock.fish.size():
				var f: Dictionary = flock.fish[i]
				var rf: Dictionary = frame["fish"][i]
				var in_alive := bool(rf["alive"])
				var fleeing := in_alive \
					and (player - _vec2(rf["pos"])).length() < GC.FLEE_RADIUS \
					and _unhex32(String(rf["fatigue"])) < 1.0
				fish_out.append({
					"id": int(rf["id"]), "alive": bool(f["alive"]),
					"caught": in_alive and not bool(f["alive"]),
					"fleeing": fleeing, "neighbors": neighbors[i],
					"pos": [_hex32(f["pos"].x), _hex32(f["pos"].y)],
					"vel": [_hex32(f["vel"].x), _hex32(f["vel"].y)],
					"fatigue": _hex32(f["fatigue"]),
					"satiation": _hex32(f["satiation"]),
				})
			fh.store_line(JSON.stringify({
				"seq": seq["id"], "family": seq["family"],
				"tick": int(frame["tick"]), "fish": fish_out,
			}))
			_rows += 1
			flock.free()


# ------------------------------------------------------------ free smoke ----

func _run_free(doc: Dictionary, fh: FileAccess) -> void:
	var dt := _unhex32(String(doc["dt"]))
	var player := _vec2(doc["player"])
	var flock: Node = Flock.new()
	flock.fish = _decode_fish(doc["fish0"])
	for t: int in int(doc["ticks"]):
		var sim_time := _unhex32(_hex32(float(t + 1) * dt))
		flock.step(player, dt, sim_time)
		var fish_out: Array = []
		for i: int in flock.fish.size():
			var f: Dictionary = flock.fish[i]
			fish_out.append({
				"id": int(doc["fish0"][i]["id"]), "alive": bool(f["alive"]),
				"pos": [_hex32(f["pos"].x), _hex32(f["pos"].y)],
			})
		fh.store_line(JSON.stringify({
			"seq": String(doc.get("id", "free")), "family": "free_smoke",
			"tick": t + 1, "fish": fish_out,
		}))
		_rows += 1
	flock.free()


# -------------------------------------------------------------- codec ----

func _run_codec(doc: Dictionary, fh: FileAccess) -> void:
	var echoed: Array = []
	for v: String in doc["values"]:
		echoed.append(_hex32(_unhex32(v)))
	fh.store_line(JSON.stringify({
		"schema": "flockcodec/1", "values": echoed,
		"sha256": _constants_hash(),
	}))
	_rows += 1
