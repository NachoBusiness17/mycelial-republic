extends Control
## TITLE - B14 2026-09-30 (last-mile wave: "the game boots straight into
## the world; a stranger needs a door"). Receipt:
## watch/inbox/last_mile_20260930/B14_TITLE.md.
##
## The door: game name, one-line tagline, two mode buttons (SOVEREIGN -
## play alone / AUTHORITATIVE - join the server at the host:port field),
## the verbatim control list card, and the "verify everything" one-liner
## pointing at PLAYER_ONE.md. Pure _draw like the HUD law (AA5): one
## Control, every pixel drawn geometry + draw_string, mouse_filter IGNORE,
## zero RNG, no wall clock (the cursor blink keys off this node's own
## accumulated process deltas, the sim_time instrument in title edition;
## nothing samples the OS clock).
##
## V5 feel pass 2026-09-30 (the entrance): a river band FLOWS IN from the
## left behind the name over ENTRANCE_S seconds — the leading edge eases
## out cubic and carries the choppiest wave (a pour reads at the front,
## calm at the back), splash droplets ride the edge while it travels, and
## after the fill the surface keeps lapping forever. Pure geometry: two
## sine terms phased off _time (CLOCK LAW), amplitude ramp keyed on
## x-position — same band every boot, frame-replayable.
##
## KEYBOARD ONLY (the mission's "no mouse dependency"): UP/DOWN move the
## selection, ENTER walks through the door. While the AUTHORITATIVE row is
## selected, printable keys edit the host:port field and BACKSPACE erases
## (navigation and ENTER never type). The mouse does nothing at all.
##
## HANDOFF (statics: this script loads once per process; scenes/title.tscn
## instantiates it, game.gd preloads it and reads the choice):
##   chosen_mode   -1 = no title ran (a direct scenes/main.tscn run keeps
##                  W1's boot-probe auto-join bytes), 0 = sovereign,
##                  1 = authoritative.
##   join_endpoint the field bytes at the AUTHORITATIVE ENTER ("" otherwise
##                  and on sovereign; an emptied field falls back to the
##                  compiled NET_HOST/NET_PORT in game.gd).
##   field_text   persists across ESC returns so an endpoint a stranger
##                  typed survives a walk back out (static, not per-door).
## ESC from the game scene-swaps back here (game.gd KEY_ESCAPE); the swap
## frees the whole Main tree, so walking in again re-inits clean.

# FIX 2026-09-30 (D9 playtest, watch/inbox/last_mile_20260930/D9_PLAYTEST.md):
# born MODE_* (B14); 0b846c01f renamed game.gd's references to
# Title.DOOR_* (see systems/game_constants.gd: "title.gd's DOOR_* are a
# different domain") WITHOUT renaming them here, so scripts/game.gd failed
# to parse ("Cannot find member DOOR_SOVEREIGN") and the committed game
# booted Main as a dead scriptless Node2D — caught live by the D9 fresh
# playtest boot. Renamed here to finish that half-done rename; grep shows
# no other consumer of the old names (tests pin neither).
const DOOR_UNCHOSEN := -1
const DOOR_SOVEREIGN := 0
const DOOR_AUTHORITATIVE := 1

static var chosen_mode := DOOR_UNCHOSEN
static var join_endpoint := ""
static var field_text := ""

const VIEW := Vector2(1152.0, 648.0)  # project.godot viewport (hud.gd idiom)
const GAME_SCENE := "res://scenes/main.tscn"
const DEFAULT_ENDPOINT := "127.0.0.1:8800"  # game.gd NET_HOST/NET_PORT
const FIELD_MAX := 48  # bounded field; typing past it is dropped, not crashed

# Layout (screen space). Two centered door panels, controls card lower-left,
# verify one-liner lower-right.
const BTN0 := Rect2(336.0, 200.0, 480.0, 76.0)
const BTN1 := Rect2(336.0, 292.0, 480.0, 76.0)
const FIELD_SLOT := Rect2(360.0, 342.0, 432.0, 22.0)  # inside BTN1
const CARD_RECT := Rect2(24.0, 436.0, 600.0, 196.0)

# The skyline ridge behind the name: one dim polyline, pure geometry (the
# "elegant without images" law; no sprites, no themes, no styleboxes). A var,
# not a const: the PackedVector2Array() constructor is not a constant
# expression in 4.3 (byte-run parse error; same bytes every instance anyway).
var RIDGE := PackedVector2Array([
	Vector2(0.0, 112.0), Vector2(140.0, 84.0), Vector2(300.0, 118.0),
	Vector2(430.0, 70.0), Vector2(600.0, 124.0), Vector2(760.0, 86.0),
	Vector2(900.0, 120.0), Vector2(1030.0, 68.0), Vector2(1152.0, 104.0),
])

# V5 entrance river (the header's flow-in): surface baseline sits just above
# the name baseline so the glyphs stand IN the water; the band floor keeps it
# a river behind the title, not a flood over the doors.
const WATER_Y := 98.0         # surface baseline (name baseline: 132)
const WATER_FLOOR := 176.0    # band bottom (doors start at y 200)
const ENTRANCE_S := 1.4       # seconds the leading edge takes to cross
const WAVE_BIG := 4.5         # long swell amplitude, px
const WAVE_SMALL := 2.5       # short chop amplitude, px
const WATER_COL := Color(0.30, 0.55, 0.80, 0.42)
const CREST_COL := Color(0.60, 0.82, 0.95, 0.55)

# The control list, verbatim from the game's own card (PLAYER_ONE.md
# section 3 keeps this exact wording; key -> description).
const CONTROLS: Array = [
	["Mouse", "Move the shepherd. Chase a fish until it tires (it turns gold), close in to tag it. Tagged fish are score."],
	["SPACE", "Boil 1 unit at the nearest pool. It rises as steam and lands in the Crown."],
	["E", "Open/shut the nearest valve."],
	["R", "Restart after the win."],
	["H", "(Extra) Swap the water law: strict open/shut flow vs graded depth and head."],
	["T", "(Extra) Toggle the terrain board: a real 64x64 Mount St Helens map; click a wet cell to boil it."],
]
const VERIFY_LINE := "verify everything: check every claim yourself by running the thing. see PLAYER_ONE.md"
const TAGLINE := "a small puzzle world about water"  # PLAYER_ONE.md section 1, verbatim fragment

# Palette (hud.gd grammar: the same panel/edge/text/mode colors).
const BACKDROP := Color(0.035, 0.045, 0.06)
const PANEL_BG := Color(0.04, 0.05, 0.07, 0.62)
const PANEL_EDGE := Color(0.55, 0.62, 0.7, 0.28)
const PANEL_EDGE_LIT := Color(0.55, 0.62, 0.7, 0.8)
const SLOT_BG := Color(0.1, 0.12, 0.16, 0.9)
const SLOT_EDGE := Color(0.5, 0.58, 0.68, 0.35)
const NAME_COL := Color(0.78, 0.9, 1.0)
const TEXT_DIM := Color(0.6, 0.65, 0.7)
const TEXT_MAIN := Color(0.85, 0.88, 0.92)
const GOLD := Color(0.95, 0.8, 0.35)
const SOVEREIGN_COL := Color(0.55, 0.85, 0.8)
const AUTH_COL := Color(0.9, 0.75, 0.4)
const FIELD_CURSOR := Color(0.55, 0.85, 0.95)

var sel := 0      # 0 = SOVEREIGN row, 1 = AUTHORITATIVE row (fresh doors start at 0)
var _time := 0.0  # the door's sim clock: accumulated deltas only (CLOCK LAW)


func _ready() -> void:
	mouse_filter = Control.MOUSE_FILTER_IGNORE  # keyboard-only door; never eats the mouse
	size = VIEW
	if field_text == "":
		# First door this process. net_client.gd begin() env grammar:
		# MOUNTAIN_SERVER ("host" or "host:port") outranks the compiled
		# default, so show the stranger the endpoint a packed copy would
		# actually use. begin() re-reads the env at connect time and still
		# wins (the packed-copy law; this screen only seeds the field).
		var env := OS.get_environment("MOUNTAIN_SERVER")
		field_text = env if env != "" else DEFAULT_ENDPOINT


func _process(delta: float) -> void:
	_time += delta
	queue_redraw()


func _unhandled_key_input(event: InputEvent) -> void:
	if event is InputEventKey and event.pressed and not event.echo:
		match event.keycode:
			KEY_UP, KEY_DOWN:
				sel = 1 - sel  # two doors: either key wraps to the other row
				queue_redraw()
			KEY_ENTER, KEY_KP_ENTER:
				_activate()
			KEY_BACKSPACE:
				if sel == DOOR_AUTHORITATIVE:
					field_text = field_text.substr(0, field_text.length() - 1)
					queue_redraw()
			_:
				# Printable keys edit the field only while the AUTHORITATIVE
				# row is selected. unicode >= 33 skips spaces (a host:port
				# has none) and every control code; ENTER matched above, so
				# starting never types.
				var u: int = event.unicode
				if sel == DOOR_AUTHORITATIVE and u >= 33 and field_text.length() < FIELD_MAX:
					field_text += char(u)
					queue_redraw()


func _activate() -> void:
	# ENTER on the selected door. change_scene_to_file defers the swap to
	# the end of the frame (the same family as the existing R-key
	# reload_current_scene in game.gd), so this is safe from an input
	# callback; the whole Main tree is freed by the swap, which IS the
	# clean re-init.
	chosen_mode = sel
	join_endpoint = field_text if sel == DOOR_AUTHORITATIVE else ""
	get_tree().change_scene_to_file(GAME_SCENE)


# -------------------------------------------------------------------- draw ----

func _draw_entrance_water() -> void:
	# V5 entrance river (header law). Leading edge x crosses the view on a
	# cubic ease-out; the wave amplitude ramps up toward the leading edge
	# (churn at the pour, calm at the back); three splash droplets ride the
	# edge while it travels, on sine phases of _time (zero RNG, no hash
	# needed — continuous functions of the door's own clock).
	var et: float = clampf(_time / ENTRANCE_S, 0.0, 1.0)
	var edge: float = VIEW.x * (1.0 - pow(1.0 - et, 3.0))
	if edge <= 1.0:
		return
	var steps := 40
	var surf := PackedVector2Array()
	for k in steps + 1:
		var x: float = edge * float(k) / float(steps)
		var churn: float = 0.35 + 0.65 * (x / edge)
		var y: float = WATER_Y + churn * (WAVE_BIG * sin(x * 0.021 - _time * 2.6) + WAVE_SMALL * sin(x * 0.047 + _time * 1.8))
		surf.append(Vector2(x, y))
	var poly := PackedVector2Array()
	poly.append_array(surf)
	poly.append(Vector2(edge, WATER_FLOOR))
	poly.append(Vector2(0.0, WATER_FLOOR))
	draw_colored_polygon(poly, WATER_COL)
	draw_polyline(surf, CREST_COL, 1.5, false)
	if et < 1.0:
		# Splash droplets ahead of the leading edge: deterministic sine
		# phases per droplet, dying the frame the edge settles.
		for k in 3:
			var bob: float = absf(sin(_time * 6.0 + float(k) * 2.1))
			var dp := Vector2(edge - 8.0 - 9.0 * float(k), WATER_Y - 8.0 - 16.0 * bob)
			draw_circle(dp, 1.6, Color(0.7, 0.85, 0.95, 0.6))


func _draw() -> void:
	var font := ThemeDB.fallback_font
	draw_rect(Rect2(Vector2.ZERO, VIEW), BACKDROP)
	draw_polyline(RIDGE, Color(0.5, 0.62, 0.72, 0.16), 2.0)

	# V5 entrance: the river flows in BEHIND the name, so it draws before the
	# glyphs. _draw_entrance_water is pure geometry keyed on _time.
	_draw_entrance_water()

	# Name + tagline (the tagline is PLAYER_ONE.md section 1 wording).
	var name_str := "THE MOUNTAIN"
	var nw: float = font.get_string_size(name_str, HORIZONTAL_ALIGNMENT_LEFT, -1, 44).x
	draw_string(font, Vector2((VIEW.x - nw) * 0.5, 132.0), name_str, HORIZONTAL_ALIGNMENT_LEFT, -1, 44, NAME_COL)
	var tw: float = font.get_string_size(TAGLINE, HORIZONTAL_ALIGNMENT_LEFT, -1, 15).x
	draw_string(font, Vector2((VIEW.x - tw) * 0.5, 162.0), TAGLINE, HORIZONTAL_ALIGNMENT_LEFT, -1, 15, TEXT_DIM)

	_door(BTN0, 0, "SOVEREIGN", "play alone", SOVEREIGN_COL)
	_door(BTN1, 1, "AUTHORITATIVE", "join the server at", AUTH_COL)

	# Field slot (inside the AUTHORITATIVE door): the endpoint bytes plus a
	# blinking block cursor while that row is selected. The blink phase is a
	# pure function of _time (CLOCK LAW; no wall clock, frame-replayable).
	var lit: bool = sel == 1
	draw_rect(FIELD_SLOT, SLOT_BG, true)
	draw_rect(FIELD_SLOT, SLOT_EDGE if not lit else PANEL_EDGE_LIT, false, 1.0)
	var shown := _fit_tail(font, field_text, 12, FIELD_SLOT.size.x - 14.0)
	draw_string(font, FIELD_SLOT.position + Vector2(7.0, 15.0), shown, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, TEXT_MAIN if lit else TEXT_DIM)
	if lit and int(_time * 2.0) % 2 == 0:
		var cw: float = font.get_string_size(shown, HORIZONTAL_ALIGNMENT_LEFT, -1, 12).x
		draw_rect(Rect2(FIELD_SLOT.position + Vector2(7.0 + cw + 1.0, 4.0), Vector2(7.0, 14.0)), FIELD_CURSOR)

	# Nav line under the doors.
	var nav := "UP/DOWN choose. ENTER starts."
	if lit:
		nav += "  type to edit host:port, BACKSPACE erases."
	var nw2: float = font.get_string_size(nav, HORIZONTAL_ALIGNMENT_LEFT, -1, 13).x
	draw_string(font, Vector2((VIEW.x - nw2) * 0.5, 398.0), nav, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color(0.55, 0.6, 0.66, 0.85))

	_controls_card(font)
	draw_string(font, Vector2(648.0, 626.0), VERIFY_LINE, HORIZONTAL_ALIGNMENT_LEFT, -1, 10, Color(0.85, 0.72, 0.4, 0.9))


func _door(rect: Rect2, idx: int, label: String, sub: String, col: Color) -> void:
	# One mode button: chamfered plate (hud.gd _panel idiom), label in the
	# mode strip's color grammar, sub in dim, and on the selected row a
	# brighter edge plus a drawn chevron marker.
	var font := ThemeDB.fallback_font
	var lit: bool = sel == idx
	_panel(rect, PANEL_EDGE_LIT if lit else PANEL_EDGE)
	var text_col: Color = col if lit else Color(col.r, col.g, col.b, 0.55)
	# Baselines +26/+44 (byte-run geometry fix: the first draft sat the sub at
	# +52, colliding with BTN1's field slot at +50..+72 — the slot's opaque
	# fill drew over the "join the server at" glyphs' lower half).
	draw_string(font, rect.position + Vector2(24.0, 26.0), label, HORIZONTAL_ALIGNMENT_LEFT, -1, 20, text_col)
	draw_string(font, rect.position + Vector2(24.0, 44.0), sub, HORIZONTAL_ALIGNMENT_LEFT, -1, 11, TEXT_DIM if lit else Color(0.6, 0.65, 0.7, 0.55))
	if lit:
		var my: float = rect.position.y + rect.size.y * 0.5
		var mx: float = rect.position.x + 10.0
		draw_colored_polygon(PackedVector2Array([
			Vector2(mx, my - 6.0), Vector2(mx + 8.0, my), Vector2(mx, my + 6.0),
		]), col)


func _controls_card(font: Font) -> void:
	_panel(CARD_RECT, PANEL_EDGE)
	var px: float = CARD_RECT.position.x
	var py: float = CARD_RECT.position.y
	draw_string(font, Vector2(px + 14.0, py + 22.0), "CONTROLS", HORIZONTAL_ALIGNMENT_LEFT, -1, 12, GOLD)
	draw_line(Vector2(px + 12.0, py + 32.0), Vector2(CARD_RECT.end.x - 12.0, py + 32.0), PANEL_EDGE, 1.0)
	var y: float = py + 50.0
	for row: Array in CONTROLS:
		var key_name: String = row[0]
		var desc: String = row[1]
		draw_string(font, Vector2(px + 14.0, y), key_name, HORIZONTAL_ALIGNMENT_LEFT, -1, 11, GOLD)
		var lines := _wrap_px(desc, font, 11, CARD_RECT.size.x - 100.0 - 12.0)
		for i in lines.size():
			draw_string(font, Vector2(px + 100.0, y + float(i) * 13.0), lines[i], HORIZONTAL_ALIGNMENT_LEFT, -1, 11, TEXT_MAIN)
		y += float(lines.size()) * 13.0 + 6.0


# ----------------------------------------------------------------- helpers ----

func _panel(rect: Rect2, edge: Color) -> void:
	# Chamfered dark plate: octagon fill + thin outline (hud.gd _panel,
	# pure _draw geometry).
	var c := 7.0
	var pts := PackedVector2Array([
		Vector2(rect.position.x + c, rect.position.y),
		Vector2(rect.end.x - c, rect.position.y),
		Vector2(rect.end.x, rect.position.y + c),
		Vector2(rect.end.x, rect.end.y - c),
		Vector2(rect.end.x - c, rect.end.y),
		Vector2(rect.position.x + c, rect.end.y),
		Vector2(rect.position.x, rect.end.y - c),
		Vector2(rect.position.x, rect.position.y + c),
	])
	draw_colored_polygon(pts, PANEL_BG)
	var outline := PackedVector2Array()
	for p: Vector2 in pts:
		outline.append(p)
	outline.append(pts[0])
	draw_polyline(outline, edge, 1.0, false)


func _wrap_px(text: String, font: Font, size: int, max_w: float) -> Array[String]:
	# Deterministic greedy word wrap measured in pixels (hud.gd _wrap2's
	# greedy law, unbounded lines). Same bytes in, same lines out; no RNG,
	# no clock.
	var words: PackedStringArray = text.split(" ")
	var lines: Array[String] = []
	var line := ""
	for w in words:
		var cand: String = w if line == "" else line + " " + w
		if font.get_string_size(cand, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x <= max_w or line == "":
			line = cand  # a single over-long word still lands (never dropped)
			continue
		lines.append(line)
		line = w
	if line != "":
		lines.append(line)
	return lines


func _fit_tail(font: Font, text: String, size: int, max_w: float) -> String:
	# Field display: if the endpoint outgrows the slot, show the TAIL (what
	# you are typing stays visible). Deterministic front-trim.
	var t := text
	while t.length() > 1 and font.get_string_size(t, HORIZONTAL_ALIGNMENT_LEFT, -1, size).x > max_w:
		t = t.substr(1)
	return t
