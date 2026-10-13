extends Node3D
## GravityPlaneDemo boot (AH15). Builds, in _ready, the demo scene AD7
## described in watch/inbox/last_mile_20260930/AD7_GRAVITY.md "Demo scene
## wiring": a floor, two wall planes (east +X / west -X) each carrying a
## GravityPlane volume (scripts/gravity_plane.gd), a player placeholder on
## group "gravity_player", and a Label3D showing the current plane index.
## Code-built nodes are this project's pattern: main.tscn is a bare root +
## script and owns no other nodes, so the demo matches it (bare root +
## this boot script).
##
## NOT wired into the 2D game: project.godot's main_scene stays main.tscn,
## and game.gd never references this scene or gravity_plane.gd.
##
## Headless verify (self-contained: the boot probes itself and quits):
##   tools/godot/Godot_v4.3-stable_win64_console.exe --headless \
##       --path roblox_to_godot res://scenes/gravity_demo.tscn
##   Runs probe_settle(2) and probe_settle(3); quits 0 only when both come
##   back with align > 0.999 AND camera_align > 0.999 AND reparented.

const GravityPlaneScript := preload("res://scripts/gravity_plane.gd")

const PLANE_NAMES := {
    0: "floor", 1: "ceiling", 2: "east", 3: "west", 4: "south", 5: "north",
}

var player: CharacterBody3D
var camera_pivot: Node3D
var label: Label3D
var current_plane_idx := 0

# normal_idx -> Area3D running gravity_plane.gd (this demo wires 2 and 3)
var _volumes := {}


func _ready() -> void:
    _build()
    if DisplayServer.get_name() == "headless":
        _run_headless_probe()


## Probe hook, callable headless: route NORMAL_TABLE[idx] to the wired
## volume for that plane and shift through the REAL _begin_shift path.
## This demo carries two volumes, so planes 2 (east) and 3 (west) are
## wired; other indexes are this map's own -1 (gravity_plane.gd's full
## six-entry table is exercised in its own lane, not re-implemented here).
## On success the label updates to the new plane index.
func shift_to(plane_idx: int) -> int:
    var volume = _volumes.get(plane_idx)
    if volume == null:
        push_error("demo shift_to: plane %d not wired (demo carries 2=east, 3=west)" % plane_idx)
        return -1
    var rc: int = volume.shift_to(plane_idx)
    if rc == 0:
        current_plane_idx = plane_idx
        _update_label()
    return rc


## Deterministic settle for the headless verify: freezes auto_tick on every
## volume, shift_to(idx), then fixed-step ticks (1/60 s) until settled
## (+1 tick for the float tail). Returns the volume's probe_state() with a
## "ticks" count added. No renderer, no frame-timing dependence.
func probe_settle(plane_idx: int) -> Dictionary:
    for volume in _volumes.values():
        volume.set("auto_tick", false)
    var volume = _volumes.get(plane_idx)
    if volume == null:
        return {"error": -1}
    var rc := shift_to(plane_idx)
    if rc != 0:
        return {"error": rc}
    var ticks := 0
    while not volume.probe_state()["settled"] and ticks < 240:
        volume.tick(1.0 / 60.0)
        ticks += 1
    volume.tick(1.0 / 60.0)
    var state: Dictionary = volume.probe_state()
    state["ticks"] = ticks
    return state


func _build() -> void:
    var floor_body := StaticBody3D.new()
    floor_body.name = "Floor"
    floor_body.collision_layer = 1
    floor_body.position = Vector3(0, -0.25, 0)
    add_child(floor_body)
    _add_box(floor_body, Vector3(20, 0.5, 20), Color(0.16, 0.17, 0.19))

    _make_player()

    # Two wall planes carrying GravityPlane volumes: the area box (1.0 x 6 x
    # 18) overlaps the space the player walks through just inside each wall
    # (world x in [9, 10] for east, [-10, -9] for west).
    _make_wall(2, "EastWall", Vector3(10.25, 3, 0), Vector3(-0.75, 0, 0), Vector3(1, 0, 0), Color(0.24, 0.21, 0.17))
    _make_wall(3, "WestWall", Vector3(-10.25, 3, 0), Vector3(0.75, 0, 0), Vector3(-1, 0, 0), Color(0.17, 0.21, 0.24))

    label = Label3D.new()
    label.name = "PlaneLabel"
    label.position = Vector3(0, 2.6, -9.4)
    label.billboard = BaseMaterial3D.BILLBOARD_ENABLED
    label.pixel_size = 0.01
    label.modulate = Color(0.85, 0.95, 1.0)
    add_child(label)

    var sun := DirectionalLight3D.new()
    sun.rotation_degrees = Vector3(-55, -30, 0)
    add_child(sun)

    _update_label()


## Player placeholder: no controller (that is the future 3D controller's
## lane, per AD7's boundary note). The GravityPlane volume slerps THIS
## node's basis, so the lean is visible even on a dumb body.
func _make_player() -> void:
    player = CharacterBody3D.new()
    player.name = "Player3D"
    player.collision_layer = 1
    player.collision_mask = 1
    player.add_to_group("gravity_player")
    add_child(player)

    var capsule := CapsuleShape3D.new()
    capsule.radius = 0.3
    capsule.height = 1.6
    var body_shape := CollisionShape3D.new()
    body_shape.shape = capsule
    body_shape.position = Vector3(0, 0.8, 0)
    player.add_child(body_shape)

    var capsule_mesh := CapsuleMesh.new()
    capsule_mesh.radius = 0.3
    capsule_mesh.height = 1.6
    var body_mesh := MeshInstance3D.new()
    body_mesh.mesh = capsule_mesh
    body_mesh.position = Vector3(0, 0.8, 0)
    player.add_child(body_mesh)

    camera_pivot = Node3D.new()
    camera_pivot.name = "CameraPivot"
    camera_pivot.position = Vector3(0, 1.2, 0)
    player.add_child(camera_pivot)

    var cam := Camera3D.new()
    cam.position = Vector3(0, 0, 3.5)
    cam.rotation_degrees = Vector3(-15, 0, 0)
    camera_pivot.add_child(cam)


## Wall plane: StaticBody3D (the reparent target / wall surface) carrying a
## GravityPlane Area3D whose box overlaps the walk-through space just
## inside the wall, with plane_normal = the wall's OUTWARD normal.
func _make_wall(plane_idx: int, wall_name: String, wall_pos: Vector3, area_offset: Vector3, normal: Vector3, color: Color) -> void:
    var wall := StaticBody3D.new()
    wall.name = wall_name
    wall.collision_layer = 1
    wall.position = wall_pos
    add_child(wall)
    _add_box(wall, Vector3(0.5, 6, 20), color)

    var volume := Area3D.new()
    volume.name = "GravityPlane" + PLANE_NAMES[plane_idx].capitalize()
    volume.script = GravityPlaneScript
    volume.position = area_offset
    volume.monitoring = true
    volume.collision_mask = 1
    wall.add_child(volume)

    var area_shape := CollisionShape3D.new()
    var box := BoxShape3D.new()
    box.size = Vector3(1.0, 6, 18)
    area_shape.shape = box
    volume.add_child(area_shape)

    # Exports set after the script lands, before _ready runs on tree entry:
    # player/camera_pivot already exist because _make_player ran first.
    volume.set("plane_normal", normal)
    volume.set("wall_surface", wall)
    volume.set("player", player)
    volume.set("camera_pivot", camera_pivot)
    _volumes[plane_idx] = volume


## Mesh + collision pair, one BoxMesh/BoxShape3D of the same size: the
## demo is meant to be looked at, so every collision body is visible.
func _add_box(parent: Node3D, size: Vector3, color: Color) -> void:
    var mesh := BoxMesh.new()
    mesh.size = size
    var material := StandardMaterial3D.new()
    material.albedo_color = color
    mesh.material = material
    var mesh_instance := MeshInstance3D.new()
    mesh_instance.mesh = mesh
    parent.add_child(mesh_instance)

    var shape := BoxShape3D.new()
    shape.size = size
    var collision := CollisionShape3D.new()
    collision.shape = shape
    parent.add_child(collision)


func _update_label() -> void:
    var normal: Vector3 = GravityPlaneScript.NORMAL_TABLE[current_plane_idx]
    label.text = "gravity plane %d: %s   up = (%.1f, %.1f, %.1f)" % [
        current_plane_idx,
        PLANE_NAMES[current_plane_idx],
        normal.x, normal.y, normal.z,
    ]


## Headless gate: exercise both wired planes through probe_settle and quit
## with the verdict. One print line per plane so the run log proves the
## probe executed (not a vacuous quit 0).
func _run_headless_probe() -> void:
    var failures := 0
    for plane_idx in [2, 3]:
        var state := probe_settle(plane_idx)
        var ok: bool = (state.get("align", 0.0) > 0.999
                and state.get("camera_align", 0.0) > 0.999
                and state.get("reparented", false))
        print("AH15 probe plane %d -> %s (%s)" % [plane_idx, "OK" if ok else "FAIL", state])
        if not ok:
            push_error("AH15 probe plane %d failed: %s" % [plane_idx, state])
            failures += 1
    get_tree().quit(1 if failures > 0 else 0)
