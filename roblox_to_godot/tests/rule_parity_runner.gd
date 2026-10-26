extends SceneTree
## rule_parity_runner.gd — the GDScript side of tools/rule_parity.py (V5
## parity harness, 2026-09-30; receipt watch/inbox/last_mile_20260930/
## V5_PARITY.md).
##
## Headless: godot --headless --path roblox_to_godot \
##     --script res://tests/rule_parity_runner.gd -- <inputs.json> <out.jsonl>
##
## Consumes the SAME canonical JSON the Python side consumes (schema
## rule_parity.v1), replays every sequence through systems/water_graph.gd
## under the server receipt law and emits one JSONL row per tick:
## {seq, family, tick, hash, verdicts, state}. hash = SHA-256 over
## the canonical state text, the SAME bytes mag.water_graph hashes —
## tools/rule_parity.py canonical_state_text() is the formatter's twin.
## Node hash fields: elev, kind, sill, volume, steam, rot — the rot
## field is the vortex REGISTER (2026-10-24, mariner cycle 15, THE
## REGISTER ON THE WIRE): this runner installs a spec's initial rot at
## add_node and ends its hash at rot, so register drift reads
## parity-false. Receipt receipt_20261024_mariner.md.
##
## LEGALITY LAW (Q11, 2026-10-01, mountain_climb — was the water subset
## only): the mirror now rejects exactly what the server rejects at
## receipt, mirroring server/server.py _admit_action's ladder verbatim —
## MAC gate (the keyless arms of server/frame_mac.py check/admit: strict
## window bare frame, seq type/monotony, 32-lowercase-hex tag shape; the
## TAG arm needs K, which only SRP6 mints — the GDScript bignum client is
## server/README "What v1 owes", so the corpus never emits a shape-legal
## mac and the unverifiable arm is never reached), then the nonce law
## (STALE_NONCE: replay / unbind / non-int types, the id burns at
## receipt), then world validation (server/world.py
## MountainWorld.validate over the FULL six-verb CHAT_TABLE contract:
## say/whisper BAD_TEXT, whisper UNKNOWN_TARGET, join/boil/tag node
## targets, valve pipe targets, boil/tag DRY_POOL — MAX_SAY arrives in
## the input JSON stamped from server.world.MAX_SAY, never forked), then
## the rate cap (RATE_CAP: one acked action per sid per tick bucket;
## whisper acks direct and still spends the window). Tamper disconnects
## (server.py breaks the read loop): the connection goes DARK and later
## frames emit no verdict, exactly like frames that never arrived.
##
## This runner MEASURES, never patches: water_graph.gd is loaded as-is, so
## any law drift between the engines lands in the hash diff. Exit 0 = ran
## (parity verdict belongs to the comparator), 3 = bad usage/IO.

const WG := preload("res://systems/water_graph.gd")

var verbs: Array = []
var max_say := 240  # server/world.py MAX_SAY, stamped in the input JSON
var roster: Dictionary = {}
var pending: Array = []
# receipt-ladder state (the tools/rule_parity.py HarnessWorld twin):
# nonce high-water marks and spent tick buckets per sid (the
# protocol_table.ReceiptGate law), the armed-MAC window and expected seq
# (the frame_mac law), and the dark-connection bit (tamper = disconnect).
var _nonce_hwm: Dictionary = {}
var _staged_tick: Dictionary = {}
var _arm_at_tick := -1
var _mac_expected := 0
var _conn_dark := false


func _init() -> void:
	var user_args := OS.get_cmdline_user_args()
	if user_args.size() != 2:
		push_error("usage: -- <inputs.json> <out.jsonl>")
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
	if doc == null or not doc.has("sequences"):
		push_error("bad input JSON (need schema rule_parity.v1)")
		quit(3)
		return
	verbs = doc.get("verbs", [])
	max_say = int(doc.get("max_say", 240))
	var fh := FileAccess.open(out_path, FileAccess.WRITE)
	if fh == null:
		push_error("cannot write output: " + out_path)
		quit(3)
		return
	for seq: Dictionary in doc["sequences"]:
		_play_sequence(seq, fh)
	fh.close()
	print("gd runner: wrote %d frames" % _frames_written)
	quit(0)


var _frames_written: int = 0


func _play_sequence(seq: Dictionary, fh: FileAccess) -> void:
	var wg: Node = WG.new()
	roster = {}
	pending = []
	_nonce_hwm = {}
	_staged_tick = {}
	_arm_at_tick = int(seq.get("arm_at_tick", -1))
	_mac_expected = 0
	_conn_dark = false
	for n: Dictionary in seq["nodes"]:
		wg.add_node(String(n["name"]), int(n.get("elev", 0)),
			String(n.get("kind", "plain")), int(n.get("sill", 0)),
			int(n.get("volume", 0)),
			int(n.get("cross_section", WG.DEFAULT_CROSS_SECTION)),
			int(n.get("rot", 0)))
	for p: Dictionary in seq["pipes"]:
		wg.add_pipe(String(p["name"]), String(p["src"]), String(p["dst"]),
			int(p.get("cap", 1)), bool(p.get("siphon", false)),
			int(p.get("crest", 2)), bool(p.get("open", true)))
	for sid: String in seq["sids"]:
		roster[sid] = {"user": "user_" + sid}
	var tick_no: int = 0
	for frame: Array in seq["frames"]:
		tick_no += 1
		var verdicts: Array = []
		for act: Dictionary in frame:
			var v := _admit_action(wg, act, tick_no)
			if not v.is_empty():
				verdicts.append(v)  # dark frames emit no verdict (never arrived)
		for act: Dictionary in pending:
			_apply(wg, act)
		pending = []
		wg.tick()
		fh.store_line(JSON.stringify({
			"seq": seq["id"], "family": seq["family"], "tick": tick_no,
			"hash": _state_hash(wg), "verdicts": verdicts,
			"state": _state_fields(wg),
		}))
		_frames_written += 1


# --- receipt ladder: server/server.py _admit_action (:489-521) mirror ---

func _admit_action(wg: Node, act: Dictionary, tick_no: int) -> String:
	# MAC gate -> nonce law -> world validation -> rate cap -> stage ->
	# commit on ack. Returns "ack", "reject:<code>", or "" when the
	# connection is dark (tamper disconnected it) — the caller emits no
	# verdict, exactly like a frame that never reached the server.
	if _conn_dark:
		return ""
	var sid := String(act["sid"])
	var verb := String(act["verb"])
	var target := String(act["target"])
	var mac_why := _mac_admit(act, tick_no)
	if not mac_why.is_empty():
		_conn_dark = true  # server.py: break — tamper, never resync
		return "reject:" + mac_why
	# 'n' ABSENT is the NO_NONCE state (the unbind law below); 'n': null is
	# a VALUE whose type is not int -> STALE_NONCE, the python twin's
	# `type(nonce) is not int` — the two must never collapse.
	var nonce_why := _admit_nonce(sid, act["n"] if act.has("n") else null, act.has("n"))
	if not nonce_why.is_empty():
		return "reject:" + nonce_why
	var why := _validate(wg, sid, verb, target)
	if not why.is_empty():
		return "reject:" + why
	var applies_at := int(wg.tick_count) + 1
	if int(_staged_tick.get(sid, -1)) == applies_at:
		return "reject:RATE_CAP"
	# stage (server/world.py stage): whisper is the one receipt-time verb —
	# it acks direct and never pends (LW6).
	if verb != "whisper":
		pending.append({"sid": sid, "verb": verb, "target": target})
	_staged_tick[sid] = applies_at  # commit: an ack is an ack (whisper too)
	return "ack"


func _admit_nonce(sid: String, raw: Variant, has_n: bool) -> String:
	# protocol_table.ReceiptGate.admit_nonce twin: no 'n' on a bound session
	# is the unbind trick (STALE_NONCE); a bool is a verdict, null and
	# strings are not ids (the X9 u8 law); JSON numbers arrive float64
	# here, so an integral float IS the python side's int (never a fork),
	# a fractional one is the python float -> STALE_NONCE. Burns at receipt.
	if not has_n:
		if _nonce_hwm.has(sid):
			return "STALE_NONCE"
		return ""
	if raw == null or typeof(raw) == TYPE_BOOL or not (typeof(raw) == TYPE_INT or typeof(raw) == TYPE_FLOAT):
		return "STALE_NONCE"
	if typeof(raw) == TYPE_FLOAT and float(raw) != float(int(raw)):
		return "STALE_NONCE"
	var n := int(raw)
	if _nonce_hwm.has(sid) and n <= int(_nonce_hwm[sid]):
		return "STALE_NONCE"
	_nonce_hwm[sid] = n
	return ""


func _mac_admit(act: Dictionary, tick_no: int) -> String:
	# server/frame_mac.py FrameMacState.admit/check twin, KEYLESS arms only,
	# in check()'s exact order (:215-231): bare frame in the strict window,
	# seq type/range (SHAPE), seq != expected (SEQ — never resync), tag
	# shape (SHAPE, 32 lowercase hex). The TAG arm (HMAC under k_c2s) needs
	# K, which only SRP6 mints; the corpus never emits a shape-legal mac,
	# so the unverifiable arm is never reached. arm_at_tick models
	# "srp_proof armed this connection just before tick N" with
	# require_frame_mac=True (the closed window); before it the gate is
	# skipped entirely (server.py only admits armed sessions).
	if _arm_at_tick < 0 or tick_no < _arm_at_tick:
		return ""
	if not act.has("mac"):
		return "BAD_MAC"
	var seq_v: Variant = act.get("seq")
	if typeof(seq_v) == TYPE_BOOL or not (typeof(seq_v) == TYPE_INT or typeof(seq_v) == TYPE_FLOAT) or int(seq_v) < 0:
		return "BAD_MAC"  # SHAPE
	var seq := int(seq_v)
	if seq != _mac_expected:
		return "BAD_MAC"  # SEQ: gap or replay
	var tag: Variant = act.get("mac")
	if typeof(tag) != TYPE_STRING or String(tag).length() != 32:
		return "BAD_MAC"  # SHAPE
	var t := String(tag)
	for i in t.length():
		var c := t.unicode_at(i)
		if not ((c >= 48 and c <= 57) or (c >= 97 and c <= 102)):
			return "BAD_MAC"  # SHAPE: lowercase hex only
	_mac_expected += 1
	return ""


# --- world validation: server/world.py MountainWorld.validate mirror ---

func _validate(wg: Node, sid: String, verb: String, target: String) -> String:
	# The FULL six-verb CHAT_TABLE contract, order verbatim (world.py
	# :188-219): sid, verb, say, whisper, valve, generic node target,
	# boil/tag dry check.
	if not roster.has(sid):
		return "UNKNOWN_SID"
	if not verbs.has(verb):
		return "UNKNOWN_VERB"
	if verb == "say":
		# LW6: target IS the text — free-form, never a node name
		if target.is_empty() or target.length() > max_say:
			return "BAD_TEXT"
		return ""
	if verb == "whisper":
		# LW6: target is 'user|text' (first '|' splits; the text may
		# contain more). Malformed or over-length -> BAD_TEXT, a user
		# with no registered session -> UNKNOWN_TARGET.
		var sep := target.find("|")
		if sep < 0:
			return "BAD_TEXT"
		var to_user := target.substr(0, sep)
		var text := target.substr(sep + 1)
		if to_user.is_empty() or text.is_empty() or text.length() > max_say:
			return "BAD_TEXT"
		for sid_key in roster:
			if String(roster[sid_key]["user"]) == to_user:
				return ""
		return "UNKNOWN_TARGET"
	if verb == "valve":
		if not wg.pipes.has(target):
			return "UNKNOWN_TARGET"
		return ""
	if not wg.nodes.has(target):
		return "UNKNOWN_TARGET"  # boil/join/tag: a node name
	if (verb == "boil" or verb == "tag") and wg.nodes[target].volume <= 0:
		return "DRY_POOL"
	return ""


func _apply(wg: Node, act: Dictionary) -> void:
	var verb := String(act["verb"])
	var target := String(act["target"])
	if verb == "boil":
		wg.boil(target, 1)
	elif verb == "valve":
		var pipe = wg.pipes[target]
		if pipe.open:
			wg.close_pipe(target)
		else:
			wg.open_pipe(target)  # refuses a fractured pipe (AC2 law)
	elif verb == "join":
		# roster position only — never enters the state hash (the
		# tools/rule_parity.py HarnessWorld.apply_pending twin)
		roster[String(act["sid"])]["at"] = target
	# say/whisper/tag mutate no graph state (say is a tick event, whisper
	# rides the direct outbox, tag scores server-side).


# --- canonical state hash: tools/rule_parity.py canonical_state_text twin ---

func _state_hash(wg: Node) -> String:
	var node_names: Array = wg.nodes.keys()
	node_names.sort()
	var pipe_names: Array = wg.pipes.keys()
	pipe_names.sort()
	var parts: Array[String] = ["t=%d" % wg.tick_count]
	for name: String in node_names:
		var n = wg.nodes[name]
		parts.append("N|%s|%d|%s|%d|%d|%d|%d" % [name, n.elev, n.kind, n.sill, n.volume, n.steam, n.rot])
	for name: String in pipe_names:
		var p = wg.pipes[name]
		parts.append("P|%s|%s|%s|%d|%d|%d|%d|%d|%d|%d" % [
			name, p.src, p.dst, p.cap, int(p.siphon), p.crest,
			int(p.primed), int(p.open), p.stress, int(p.fractured)])
	return "\n".join(parts).sha256_text()


func _state_fields(wg: Node) -> Dictionary:
	var nodes_out: Dictionary = {}
	for name: String in wg.nodes.keys():
		var n = wg.nodes[name]
		nodes_out[name] = {"elev": n.elev, "kind": n.kind, "sill": n.sill,
			"volume": n.volume, "steam": n.steam}
	var pipes_out: Dictionary = {}
	for name: String in wg.pipes.keys():
		var p = wg.pipes[name]
		pipes_out[name] = {"src": p.src, "dst": p.dst, "cap": p.cap,
			"siphon": p.siphon, "crest": p.crest, "primed": p.primed,
			"open": p.open, "stress": p.stress, "fractured": p.fractured}
	return {"tick": wg.tick_count, "nodes": nodes_out, "pipes": pipes_out}
