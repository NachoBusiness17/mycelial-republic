extends Node
## BOOT INTEGRITY - R6 2026-09-30 (last-mile Q09: the artifact gets an ID).
##
## The build pipeline (scripts/build_game.ps1) stamps the exported exe with
## an appended trailer: JSON payload, then 8-byte magic "MAGSTMP1", then a
## little-endian u32 payload length as the FINAL 4 bytes of the file:
##
##   [ exe bytes ][ payload JSON ][ MAGSTMP1 ][ u32 len(payload) ]
##
## payload = {"v":1,"git":<source sha>,"pck_sha256":<hex>,"built":<utc>,
##            "source":"estate-twin"|"the-mountain"}
##
## At boot this autoload reads the stamp off the exe, hashes the .pck that
## sits beside it, and prints the artifact's identity to stderr:
##
##   ARTIFACT_ID git=<sha> pck=ok ...      stamp matches the pck
##   ARTIFACT_ID git=<sha> pck=FAIL ...    pck swapped/missing -> quit(1)
##   ARTIFACT_ID editor ...                run from source (F5/--path), no
##                                         stamp expected, game continues
##   ARTIFACT_ID UNSTAMPED ...             exported without the pipeline;
##                                         loud warning, game continues
##
## WHY THE STAMP LIVES IN THE EXE, NOT THE PCK: any check shipped inside
## the pck swaps with it. The exe is the half of the pair a pck-swap
## leaves behind, so it is the only place a pinned expectation can sit
## (Q09's named threat: "the .pck sits beside the exe and can be swapped").
## The appended trailer is a PE overlay: the loader ignores it, and its
## final 4 bytes are a <4KB length, so it can never collide with Godot's
## embedded-pck "GDPC" end-magic scan.
##
## Stranger's verification (no Godot needed), next to the exe:
##   TheMountain.exe --headless --quit-after 2    -> "ARTIFACT_ID ... pck=ok"
## A swapped pck exits non-zero instead. Full offline command in the build
## receipt: watch/inbox/last_mile_20260930/R6_ARTIFACT_ID.md.

const MAGIC := "MAGSTMP1"
const TRAILER_TAIL := 12   # 8 magic + 4 little-endian payload length
const PAYLOAD_MAX := 4096  # the stamp is a one-line JSON; a huge "length" is corruption, not a stamp

func _ready() -> void:
	var line := _boot_line()
	printerr(line)
	if line.find(" pck=FAIL") != -1:
		# Fail closed: identity broken -> refuse to run. Exit 1 is the
		# machine-checkable signal (tests + the stranger's command key
		# off it); the stderr line is the human-readable one.
		push_error(line)
		get_tree().quit(1)

func _boot_line() -> String:
	if OS.has_feature("editor"):
		# Source lane: godot --path <project> or F5. get_executable_path()
		# is the editor binary; there is no stamped export to check.
		return "ARTIFACT_ID editor source-run (stamps live in pipeline exports)"
	var exe_path := OS.get_executable_path()
	var f := FileAccess.open(exe_path, FileAccess.READ)
	if f == null:
		return "ARTIFACT_ID FAIL exe unreadable: " + exe_path
	var size := f.get_length()
	if size < TRAILER_TAIL + 8:
		return "ARTIFACT_ID FAIL exe trivial: " + str(size) + " bytes"
	f.seek(size - 4)
	var plen := f.get_32()
	f.seek(size - TRAILER_TAIL)
	var magic := f.get_buffer(8).get_string_from_ascii()
	if magic != MAGIC:
		return "ARTIFACT_ID UNSTAMPED exe (built without scripts/build_game.ps1; pck not verifiable)"
	if plen <= 2 or plen > PAYLOAD_MAX or size < TRAILER_TAIL + plen:
		return "ARTIFACT_ID FAIL stamp payload size out of range: " + str(plen)
	f.seek(size - TRAILER_TAIL - plen)
	var payload := f.get_buffer(plen).get_string_from_utf8()
	var stamp: Variant = JSON.parse_string(payload)
	if not (stamp is Dictionary) or not stamp.has("git") or not stamp.has("pck_sha256"):
		return "ARTIFACT_ID FAIL stamp payload is not a v1 stamp: " + payload.substr(0, 80)
	var git_sha := String(stamp["git"])
	var want := String(stamp["pck_sha256"]).to_lower()
	var pck_path := exe_path.get_basename() + ".pck"
	# Reachable when Godot is booted with --main-pack <other.pck>: the game
	# runs from the substituted pack while the exe's own pck is gone. With no
	# pack at all Godot's loader fires before any GDScript runs (engine
	# prints "Is the .pck file missing?" and hangs - 4.3 defect, named in
	# the R6 tests).
	if not FileAccess.file_exists(pck_path):
		return "ARTIFACT_ID git=%s pck=FAIL pck missing beside exe (%s)" % [git_sha, pck_path]
	var digest := _sha256_file(pck_path)
	if digest == "":
		return "ARTIFACT_ID git=%s pck=FAIL pck unreadable (%s)" % [git_sha, pck_path]
	if digest != want:
		return "ARTIFACT_ID git=%s pck=FAIL pck sha256 %s != stamped %s (SWAPPED PCK)" % [git_sha, digest, want]
	return "ARTIFACT_ID git=%s pck=ok sha256=%s source=%s" % [git_sha, digest, String(stamp.get("source", "?"))]

## Streamed SHA-256 (HashingContext, 1 MiB chunks): the pck is ~95 KB today
## but this stays correct if art ever fattens it past any naive floor.
func _sha256_file(path: String) -> String:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return ""
	var h := HashingContext.new()
	var err := h.start(HashingContext.HASH_SHA256)
	if err != OK:
		return ""
	var remaining := f.get_length()
	while remaining > 0:
		var chunk := f.get_buffer(mini(remaining, 1 << 20))
		if chunk.is_empty():
			return ""
		h.update(chunk)
		remaining -= chunk.size()
	return h.finish().hex_encode()
