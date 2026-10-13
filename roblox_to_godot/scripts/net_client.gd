extends Node
## NetClient - the Godot half of the estate's world-server wire v0
## (server/protocol.py: line-delimited JSON over TCP; ops out: hello/action,
## ops in: welcome/tick/ack/reject).
##
## Owns exactly the transport: connect, hello, sid bookkeeping, line
## framing, op dispatch to signals. Owns no world state and predicts
## nothing; game.gd's mirror graph stays render-only and every mutation
## authority stays server-side (W1 2026-09-29, game_platform_basecamp).
##
## Config: set host/port/user/password fields (game.gd does), then begin().
## The MOUNTAIN_SERVER env var ("host" or "host:port") overrides the
## endpoint at begin() time so a packed client can be retargeted without
## a rebuild. v0 sends the password in plaintext inside hello; killing
## that is v1 debt (server README "What v1 owes").
##
## Debt (v1): no reconnect and no mid-session loss signal. Before the
## welcome, game.gd's 2s probe deadline falls back to sovereign mode on
## its own; after the welcome a dead socket just stops the broadcasts.

signal welcomed(world: Dictionary)
signal ticked(n: int, nodes: Dictionary, events: Array, winner: bool)
signal acked(verb: String, target: String, applies_at_tick: int)
signal rejected(why: String, verb: String, target: String)
signal auth_failed(why: String)

const MAX_LINE := 65536  # mirrors server/protocol.py MAX_LINE; a longer line is a framing fault

var host := "127.0.0.1"
var port := 8800
var user := "ada"
var password := "steam"

var peer := StreamPeerTCP.new()
var sid := ""
var welcomed_flag := false

var _hello_sent := false
var _buf := PackedByteArray()
var _down := false


func begin() -> void:
	var env := OS.get_environment("MOUNTAIN_SERVER")
	if env != "":
		if env.contains(":"):
			var parts := env.split(":")
			host = parts[0]
			port = int(parts[1])
		else:
			host = env
	peer.connect_to_host(host, port)


func is_live() -> bool:
	return welcomed_flag and peer.get_status() == StreamPeerTCP.STATUS_CONNECTED


func send_action(verb: String, target: String) -> bool:
	if sid == "" or peer.get_status() != StreamPeerTCP.STATUS_CONNECTED:
		return false
	_send({"op": "action", "sid": sid, "verb": verb, "target": target})
	return true


func stop() -> void:
	_down = true
	if peer.get_status() != StreamPeerTCP.STATUS_NONE:
		peer.disconnect_from_host()


func _process(_delta: float) -> void:
	if _down:
		return
	peer.poll()
	var status := peer.get_status()
	if status == StreamPeerTCP.STATUS_ERROR or status == StreamPeerTCP.STATUS_NONE:
		# Socket died (refused, reset, closed). No signal here by design
		# (see Debt above): pre-welcome, game.gd's 2s probe deadline is the
		# fallback path; post-welcome, silence in the broadcasts is the
		# operator's cue.
		_down = true
		return
	if status == StreamPeerTCP.STATUS_CONNECTED and not _hello_sent:
		_hello_sent = true
		_send({"op": "hello", "user": user, "pass": password})
	if status != StreamPeerTCP.STATUS_CONNECTED:
		return
	while true:
		var avail := peer.get_available_bytes()
		if avail <= 0:
			break
		var chunk: Array = peer.get_partial_data(avail)
		var err: int = chunk[0]
		if err != OK:
			break
		var bytes: PackedByteArray = chunk[1]
		_buf.append_array(bytes)
		_drain_lines()


func _send(msg: Dictionary) -> void:
	peer.put_data((JSON.stringify(msg) + "\n").to_utf8_buffer())


func _drain_lines() -> void:
	while true:
		var nl := _buf.find(10)  # LF; the wire is \n-terminated UTF-8 JSON lines
		if nl < 0:
			if _buf.size() > MAX_LINE:
				# Runaway line with no terminator: drop the buffer, keep the
				# socket (protocol.py would refuse the oversized line anyway).
				_buf.clear()
			return
		var line := _buf.slice(0, nl)
		_buf = _buf.slice(nl + 1)
		if line.size() <= MAX_LINE:
			_handle_line(line.get_string_from_utf8())


func _handle_line(text: String) -> void:
	var parsed: Variant = JSON.parse_string(text.strip_edges())
	if typeof(parsed) != TYPE_DICTIONARY:
		return  # not a JSON object; the server would answer BAD_JSON, client-side we just drop it
	var msg: Dictionary = parsed
	match String(msg.get("op", "")):
		"welcome":
			sid = String(msg.get("sid", ""))
			welcomed_flag = true
			var world: Dictionary = msg.get("world", {})
			welcomed.emit(world)
		"tick":
			var n: int = int(msg.get("n", 0))
			var nodes: Dictionary = msg.get("nodes", {})
			var events: Array = msg.get("events", [])
			var winner: bool = bool(msg.get("winner", false))
			ticked.emit(n, nodes, events, winner)
		"ack":
			acked.emit(String(msg.get("verb", "")), String(msg.get("target", "")), int(msg.get("applies_at_tick", 0)))
		"reject":
			var why := String(msg.get("why", ""))
			if why == "BAD_AUTH" or why == "UNKNOWN_OP":
				auth_failed.emit(why)
			rejected.emit(why, String(msg.get("verb", "")), String(msg.get("target", "")))
		_:
			pass
