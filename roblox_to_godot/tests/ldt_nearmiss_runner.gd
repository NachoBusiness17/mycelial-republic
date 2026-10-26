extends SceneTree
## ldt_nearmiss_runner.gd — the GDScript twin of the LDT near-miss scoring
## kernel (Q18 answer, 2026-10-01, mountain_climb lane; the
## rule_parity_runner.gd / flock_parity_runner.gd pattern applied to the
## discrete near-miss verdict).
##
## Headless: tools/godot/Godot_v4.3-stable_win64.exe --headless \
##     --path roblox_to_godot \
##     --script res://tests/ldt_nearmiss_runner.gd -- <corpus.json> <out.jsonl>
##
## WHAT IS PORTED — the SCALAR kernel of the near-miss scoring, i.e. the
## per-row margin/threshold rule around the argmax, mirrored line-for-line
## from tools/ldt_lattice.py evaluate_lattice (:403-417) and the raw arm of
## tools/ldt_nearmiss.py _arm (:224, :227-234):
##
##   raw      pred = argmax(probs) FIRST-MAX tie rule (numpy argmax law);
##            answered = max(probs) >= tau
##   strict   masked argmax (infeasible entries read as -inf), conf = masked
##            max, answered = conf >= tau (empty feasible set -> pred -1,
##            conf 0.0, abstain)
##   renorm   as strict, plus conf = masked_max / max(feasible_mass, 1e-12)
##            when feasible_mass > 0 else 0.0; feasible_mass = sequential
##            float64 sum over the 5 positions in LABELS order (infeasible
##            positions contribute 0.0) — numpy's (probs*mask).sum(axis=1)
##            for a 5-element row is the same sequential sum from 0.0
##
## WHAT IS NOT PORTED (named, never hidden):
##   - the MLP forward pass (tools/ldt_train.py forward: float32 matmuls +
##     softmax). Vector-only numpy over trained weights; the twin receives
##     the softmax probs as INPUTS and never recomputes the network.
##   - the numpy row vectorization itself (axis-1 ops). The RULE is ported
##     as a per-row scalar loop — port the rule, not the vectorization.
##   - the featurizer (vocab/hashing) and the constraint propagator
##     (feasible_set / cascade: the physics oracle that produces the
##     feasible mask and the labels). Python-side inputs, transported.
##   - fleet-level bookkeeping (per-class recall, pair metrics,
##     soundness/coverage rollups): aggregates, not row verdicts.
##
## FLOAT LAW (the Q14 flock lesson): both sides compute in float64 and every
## float crosses the wire as IEEE-754 double BIT PATTERNS in hex — decimal
## JSON parses differently per runtime and Godot Vector paths are float32,
## so bits are the only shared alphabet (flock_parity_runner.gd's codec
## rule, widened to 64). Little-endian pinned by hand (compose the
## PackedByteArray bytes ourselves). tau travels as bits too; the ONLY
## float literals inside this runner are the renorm clamp 1e-12 and the
## loop zero 0.0 — both named divergence axes, deliberately live.
##
## Corpus schema (ldt_nearmiss_parity.v1):
##   {schema, labels[5], tau_hex, rows: [{id, family, probs_hex[5],
##    feasible[5]bool, y}]} — labels order must be tools/ldt_train.py
##   LABELS; y is corpus metadata the twin does not read (the verdict does
##   not consult truth).
##
## Output: one JSONL row per corpus row, verdicts for all three modes:
##   {id, tau_echo_hex, raw/strict/renorm: {pred, answered, conf_hex,
##    pred_is_gain}}. This runner MEASURES, never patches. Exit 0 = ran
## (the parity verdict belongs to the comparator), 3 = usage/IO/schema.


func _init() -> void:
	var user_args := OS.get_cmdline_user_args()
	if user_args.size() != 2:
		push_error("usage: -- <corpus.json> <out.jsonl>")
		quit(3)
		return
	var in_path := String(user_args[0])
	var out_path := String(user_args[1])
	var raw := FileAccess.get_file_as_string(in_path)
	if raw.is_empty():
		push_error("cannot read corpus: " + in_path)
		quit(3)
		return
	var doc: Dictionary = JSON.parse_string(raw)
	if doc == null or not doc.has("rows") or not doc.has("tau_hex"):
		push_error("bad corpus JSON (need schema ldt_nearmiss_parity.v1)")
		quit(3)
		return
	if String(doc.get("schema", "")) != "ldt_nearmiss_parity.v1":
		push_error("unknown schema: " + String(doc.get("schema", "")))
		quit(3)
		return
	var labels: Array = doc["labels"]
	var gain_idx := labels.find("legal_gain")
	if labels.size() != 5 or gain_idx < 0:
		push_error("corpus labels are not the 5-way LDT label set")
		quit(3)
		return
	var tau := _hex_f64(String(doc["tau_hex"]))
	var fh := FileAccess.open(out_path, FileAccess.WRITE)
	if fh == null:
		push_error("cannot write output: " + out_path)
		quit(3)
		return
	var n := 0
	for row: Dictionary in doc["rows"]:
		var probs := PackedFloat64Array()
		for h in row["probs_hex"]:
			probs.append(_hex_f64(String(h)))
		var feasible: Array = row["feasible"]
		fh.store_line(JSON.stringify({
			"id": String(row["id"]),
			"tau_echo_hex": _f64_hex(tau),
			"raw": _verdict(probs, feasible, tau, "raw", gain_idx),
			"strict": _verdict(probs, feasible, tau, "strict", gain_idx),
			"renorm": _verdict(probs, feasible, tau, "renorm", gain_idx),
		}))
		n += 1
	fh.close()
	print("ldt_nearmiss gd runner: %d rows x 3 modes" % n)
	quit(0)


## The scalar kernel — tools/ldt_lattice.py evaluate_lattice + the raw arm
## of tools/ldt_nearmiss.py _arm, mirrored. First-max tie rule throughout
## (strict `>` keeps the FIRST maximum, numpy argmax's law).
func _verdict(probs: PackedFloat64Array, feasible: Array, tau: float,
		mode: String, gain_idx: int) -> Dictionary:
	if mode == "raw":
		var rbest := 0
		for j in range(1, probs.size()):
			if probs[j] > probs[rbest]:
				rbest = j
		var rconf := probs[rbest]
		return {"pred": rbest, "answered": rconf >= tau,
			"conf_hex": _f64_hex(rconf), "pred_is_gain": rbest == gain_idx}
	# strict / renorm: the masked projection
	var any_feasible := false
	for j in range(feasible.size()):
		if bool(feasible[j]):
			any_feasible = true
			break
	if not any_feasible:
		return {"pred": -1, "answered": false, "conf_hex": _f64_hex(0.0),
			"pred_is_gain": false}
	var best := -1
	for j in range(probs.size()):
		if bool(feasible[j]) and (best < 0 or probs[j] > probs[best]):
			best = j
	var conf := probs[best]
	if mode == "renorm":
		var mass := 0.0
		for j in range(probs.size()):
			mass += (probs[j] if bool(feasible[j]) else 0.0)
		if mass > 0.0:
			conf = conf / max(mass, 1e-12)
		else:
			conf = 0.0
	return {"pred": best, "answered": conf >= tau, "conf_hex": _f64_hex(conf),
		"pred_is_gain": best == gain_idx}


# ---- float64 hex codec: the flock_parity_runner.gd convention at 64 bits.
# The hex string is the u64 BIT PATTERN as integer digits (python:
# "%016x" % struct.unpack("<Q", struct.pack("<d", v))[0]); the bytes are
# decomposed/composed little-endian by hand so encode/decode endianness can
# never silently flip the transport.

func _f64_hex(v: float) -> String:
	var b := PackedByteArray()
	b.resize(8)
	b.encode_double(0, v)
	var parts := PackedStringArray()
	for k in range(7, -1, -1):          # byte 7 first = big-endian digits
		parts.append("%02x" % b[k])
	return "0x" + "".join(parts)


func _hex_f64(s: String) -> float:
	var t := s.trim_prefix("0x").to_lower()
	if t.length() != 16:
		push_error("bad hex64: " + s)
		return 0.0
	var bits := 0
	for i in range(16):
		var d := "0123456789abcdef".find(t[i])
		if d < 0:
			push_error("bad hex64 nibble: " + s)
			return 0.0
		bits = (bits << 4) | d
	var b := PackedByteArray()
	b.resize(8)
	for k in range(8):                  # integer -> little-endian bytes
		b[k] = (bits >> (8 * k)) & 0xFF
	return b.decode_double(0)
