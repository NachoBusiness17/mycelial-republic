extends Node2D
## St Helens terrain board loader — Z3 (2026-09-29)
## Mission: the DEM->board bridge (tools/dem_to_board.py, X7) writes
## water_graph.v1 specs like logs/terrain/N46W122_board.json (4096 nodes,
## 64x64 grid "g{row}x{col}", elev 0..255, zero pipes — sheet-flow pipes are
## WF rung 2, not fabricated here). This node makes that board VISIBLE and
## PLAYABLE in the Godot slice:
##   load JSON -> build a systems/water_graph.gd graph (the same from_spec
##   field set mag/water_graph.py reads: elev/kind/sill/volume per node,
##   src/dst/cap/siphon/crest/open per pipe, top-level tick) -> render the
##   grid as a minimap of colored quads (elev ramp 0..255, volume as
##   brightness toward aqua, cold pits tinted slate, the waste outlet marked)
##   while the terrain's own water graph ticks underneath the drawing.
## The full 64x64 map cannot fit the 1152x648 window as 1:1 terrain, so it
## renders as a corner minimap; the Mountain board and its water graph keep
## running underneath (game.gd only toggles this node's visibility on T).
##
## Demo water, honestly labeled: the spec loads verbatim (every volume 0),
## then RAIN_SEED units are deposited once at the highest plain node so the
## volume-brightness path has something to show and click-boils have water
## to lift — steam condenses at the highest cold node (the engine's law),
## visibly teleporting brightness across the map. Deterministic: fixed cell,
## fixed amount, no RNG.

const WaterGraph := preload("res://systems/water_graph.gd")

const DEFAULT_TILE := "N46W122"
const TICK_SECONDS := 0.8   # matches the Mountain board's tick
const CELL := 5.0           # 64 cells * 5 px = 320 px minimap
const MARGIN := 24.0
const BRIGHT_CAP := 4       # volume units that read as full brightness
const RAIN_SEED := 3        # one-time deposit at the highest plain node

const LOWLAND := Color(0.13, 0.16, 0.12)
const FOOTHILL := Color(0.23, 0.33, 0.16)
const UPLAND := Color(0.42, 0.38, 0.24)
const SUBALP := Color(0.52, 0.48, 0.42)
const SNOW := Color(0.95, 0.95, 0.97)
const AQUA := Color(0.45, 0.80, 1.0)
const COLD_TINT := Color(0.20, 0.38, 0.55)
const WASTE_TINT := Color(0.42, 0.12, 0.20)

var graph: Node
var rows: int = 0
var cols: int = 0
var tile_id: String = ""
var board_hash: String = ""
var cold_count: int = 0
var waste_cell: String = ""
var rain_node: String = ""
var last_events: Array[String] = []
var load_error: String = ""
var board_origin: Vector2


func _ready() -> void:
	var path := _board_path()
	if not _load_board(path):
		load_error = "terrain board not found: %s" % path
		return
	_build_and_seed(path)
	board_origin = Vector2(1152.0 - MARGIN - cols * CELL, MARGIN)
	var t := Timer.new()
	t.name = "TerrainTick"
	t.wait_time = TICK_SECONDS
	t.timeout.connect(_on_tick)
	add_child(t)
	t.start()


func toggle() -> void:
	visible = not visible
	var t := get_node_or_null("TerrainTick")
	if t is Timer:
		if visible:
			t.start()
		else:
			t.stop()


func _board_path() -> String:
	# Resolution order: STHELENS_BOARD env override, then the board the DEM
	# bridge lands one level above this project (repo_root/logs/terrain/),
	# then a copy inside the project. globalize_path keeps this honest in
	# headless runs (--path roblox_to_godot from the repo root).
	var env := OS.get_environment("STHELENS_BOARD")
	if env != "" and FileAccess.file_exists(env):
		return env
	var sibling := ProjectSettings.globalize_path("res://").path_join(
		"../logs/terrain/%s_board.json" % DEFAULT_TILE)
	if FileAccess.file_exists(sibling):
		return sibling
	return "res://%s_board.json" % DEFAULT_TILE


func _load_board(path: String) -> bool:
	var f := FileAccess.open(path, FileAccess.READ)
	if f == null:
		return false
	var parsed = JSON.parse_string(f.get_as_text())
	f.close()
	if parsed == null or not (parsed is Dictionary):
		load_error = "terrain board is not JSON: %s" % path
		return false
	var spec: Dictionary = parsed
	if String(spec.get("schema", "")) != "water_graph.v1":
		load_error = "not a water_graph.v1 spec: %s" % path
		return false
	var dem: Dictionary = spec.get("dem_board", {})
	tile_id = String(dem.get("tile_id", DEFAULT_TILE))
	board_hash = String(dem.get("board_hash", ""))
	waste_cell = String(dem.get("waste_cell", ""))
	var shape: Array = dem.get("shape", [0, 0])
	rows = int(shape[0])
	cols = int(shape[1])
	cold_count = (dem.get("cold_cells", []) as Array).size()
	var nodes_spec: Dictionary = spec.get("nodes", {})
	if rows <= 0 or cols <= 0 or rows * cols != nodes_spec.size():
		load_error = "grid shape %s does not match node count in %s" % [str(shape), path]
		return false
	_build_graph(spec)
	return true


func _build_graph(spec: Dictionary) -> void:
	# Field-for-field port of mag/water_graph.py from_spec(): elev/kind/sill/
	# volume per node (the spec's steam field is all 0 and python from_spec
	# ignores it too — parity), then pipes, then tick_count.
	graph = WaterGraph.new()
	graph.name = "TerrainWaterGraph"
	add_child(graph)
	var nodes_spec: Dictionary = spec.get("nodes", {})
	for node_name in nodes_spec:
		var n: Dictionary = nodes_spec[node_name]
		graph.add_node(String(node_name), int(n.get("elev", 0)),
			String(n.get("kind", "plain")), int(n.get("sill", 0)),
			int(n.get("volume", 0)))
	var pipes_spec: Dictionary = spec.get("pipes", {})
	for pipe_name in pipes_spec:
		var p: Dictionary = pipes_spec[pipe_name]
		graph.add_pipe(String(pipe_name), String(p.get("src", "")),
			String(p.get("dst", "")), int(p.get("cap", 1)),
			bool(p.get("siphon", false)), int(p.get("crest", 2)),
			bool(p.get("open", true)))
	graph.tick_count = int(spec.get("tick", 0))


func _build_and_seed(path: String) -> void:
	# The demo deposit: pick the highest plain (non-cold, non-waste) node;
	# file order breaks elev ties, so the pick is deterministic per board.
	var best_elev := -1
	for n in graph.nodes.values():
		if n.kind == "plain" and n.elev > best_elev:
			best_elev = n.elev
			rain_node = n.name
	if rain_node != "":
		graph.nodes[rain_node].volume += RAIN_SEED
	last_events.append("Board %s loaded (%s); rain deposits %d at %s." % [
		tile_id, path.get_file(), RAIN_SEED, rain_node])


func _on_tick() -> void:
	var events: Array[String] = graph.tick()
	if events.size() > 2:
		events = events.slice(events.size() - 2)
	last_events.append_array(events)
	while last_events.size() > 4:
		last_events.pop_front()


func _process(_delta: float) -> void:
	if visible:
		queue_redraw()


func _unhandled_input(event: InputEvent) -> void:
	# Click a minimap cell to boil 1 unit: the volume dims there and the
	# steam condenses at the highest cold node (water_graph.gd steam law).
	if not visible or load_error != "" or not (event is InputEventMouseButton):
		return
	var mb := event as InputEventMouseButton
	if mb.pressed and mb.button_index == MOUSE_BUTTON_LEFT:
		var local := mb.position - board_origin
		if local.x < 0 or local.y < 0 or local.x >= cols * CELL or local.y >= rows * CELL:
			return
		var cell_name := "g%dx%d" % [int(local.y / CELL), int(local.x / CELL)]
		if graph.volume(cell_name) > 0:
			graph.boil(cell_name, 1)
			last_events.append("You boil 1 at %s; it rises." % cell_name)
		else:
			last_events.append("%s is dry — nothing to boil." % cell_name)
		while last_events.size() > 4:
			last_events.pop_front()


func _elev_color(e: int) -> Color:
	var t := clampf(e / 255.0, 0.0, 1.0)
	if t < 0.33:
		return LOWLAND.lerp(FOOTHILL, t / 0.33)
	elif t < 0.5:
		return FOOTHILL.lerp(UPLAND, (t - 0.33) / 0.17)
	elif t < 0.75:
		return UPLAND.lerp(SUBALP, (t - 0.5) / 0.25)
	return SUBALP.lerp(SNOW, (t - 0.75) / 0.25)


func _draw() -> void:
	if load_error != "":
		draw_string(ThemeDB.fallback_font, Vector2(560, 300), load_error,
			HORIZONTAL_ALIGNMENT_LEFT, -1, 15, Color(0.9, 0.3, 0.3))
		draw_string(ThemeDB.fallback_font, Vector2(560, 324),
			"(run tools/dem_to_board.py --download to land the tile)",
			HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.6, 0.6, 0.6))
		return
	# Grid quads: elevation ramp, kind tints, volume as brightness.
	for node_name in graph.nodes:
		var parts := String(node_name).substr(1).split("x")
		if parts.size() != 2:
			continue
		var n = graph.nodes[node_name]
		var col := _elev_color(int(n.elev))
		if n.kind == "cold":
			col = col.lerp(COLD_TINT, 0.45)
		elif n.kind == "waste":
			col = col.lerp(WASTE_TINT, 0.6)
		if int(n.volume) > 0:
			var frac := clampf(float(n.volume) / float(BRIGHT_CAP), 0.0, 1.0)
			col = col.lerp(AQUA, 0.2 + 0.8 * frac)
		var rect := Rect2(board_origin + Vector2(int(parts[1]) * CELL, int(parts[0]) * CELL),
			Vector2(CELL, CELL))
		draw_rect(rect, col)  # filled quad, no outline
		if int(n.steam) > 0:
			draw_circle(rect.get_center(), 1.5, Color(0.95, 0.95, 0.9))
	draw_rect(Rect2(board_origin - Vector2(1, 1), Vector2(cols * CELL + 2, rows * CELL + 2)),
		Color(0.7, 0.7, 0.65), false, 1.5)
	# Header / footer.
	var hash8 := board_hash.substr(0, 8)
	draw_string(ThemeDB.fallback_font, board_origin + Vector2(0, -8),
		"%s  %dx%d  %d nodes  cold %d  waste %s  hash %s  tick %d" % [
			tile_id, rows, cols, graph.nodes.size(), cold_count, waste_cell,
			hash8, graph.tick_count],
		HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.8, 0.85, 0.8))
	draw_string(ThemeDB.fallback_font, board_origin + Vector2(0, rows * CELL + 16),
		"click a bright cell to boil — steam condenses at the highest cold pit",
		HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color(0.55, 0.7, 0.75))
	if last_events.size() > 0:
		draw_string(ThemeDB.fallback_font, board_origin + Vector2(0, rows * CELL + 32),
			" · ".join(last_events.slice(maxi(0, last_events.size() - 2))),
			HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color(0.6, 0.65, 0.7))
