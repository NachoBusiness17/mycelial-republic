extends Area3D
## GravityPlane — the CONTROL: Resonant wall-walk steal (AC1 #3, banked for
## the 3D expansion). STANDALONE PROTOTYPE: not referenced by game.gd — the
## Mountain is a 2D water-graph top-down; this is the mechanism, pure math,
## zero GPU cost (no shader, no post — one quaternion slerp per frame).
##
## What this volume does when the player walks into it:
##   1. slerps the player's up-vector onto the plane's normal over 0.4 s,
##   2. reparents the player onto the wall surface (a moving/rotating wall
##      then carries the player, the Resonant room trick),
##   3. slerps the camera pivot by the SAME quaternion, so screen-down
##      always reads as the new down — the brain-breaking part is that the
##      camera never snaps, it leans.
##
## Headless probe (deterministic, no renderer, fixed steps):
##   gp.auto_tick = false
##   gp.shift_to(2)                      # east wall, see NORMAL_TABLE
##   while not gp.probe_state()["settled"]:
##       gp.tick(1.0 / 60.0)             # 24 ticks = 0.4 s (+1 for float tail)
##   var s := gp.probe_state()
##   # assert s["align"] > 0.999 and s["camera_align"] > 0.999 and s["reparented"]

const PLAYER_GROUP := "gravity_player"

## Canonical normals, indexed for shift_to() so the probe (and the demo
## scene's six wall volumes) never hand-build a vector. Index 0 = floor =
## default gravity, so a probe sweep can reset with shift_to(0).
const NORMAL_TABLE := [
    Vector3(0, 1, 0),   # 0 floor  (default gravity)
    Vector3(0, -1, 0),  # 1 ceiling
    Vector3(1, 0, 0),   # 2 east wall
    Vector3(-1, 0, 0),  # 3 west wall
    Vector3(0, 0, 1),   # 4 south wall
    Vector3(0, 0, -1),  # 5 north wall
]

enum Phase { IDLE, SHIFTING, SETTLED }

@export var player: Node3D
## Node the player is reparented onto when a shift begins. Defaults to
## this volume's parent — i.e. the wall body the Area3D is mounted on.
@export var wall_surface: Node3D
## Head/camera pivot (child of the player in the demo scene). Slerped in
## lockstep with the player so screen-down tracks the new down.
@export var camera_pivot: Node3D
## Normal the player's up-vector should land on when the body enters.
## The wall's OUTWARD normal: standing on the east wall means up = +X.
@export var plane_normal := Vector3(1, 0, 0)
## Shift length in seconds. 0.4 reads as supernatural-but-not-nauseating;
## the whole feel of the trick lives in this constant.
@export var shift_duration := 0.4
## When true, _physics_process drives tick() (normal play). The headless
## probe sets this false and calls tick() with fixed steps itself, so the
## result never depends on frame timing.
@export var auto_tick := true

var phase := Phase.IDLE
var target_normal := Vector3.UP

var _t := 0.0
var _player_q_from := Quaternion.IDENTITY
var _player_q_to := Quaternion.IDENTITY
var _pivot_q_from := Quaternion.IDENTITY
var _pivot_q_to := Quaternion.IDENTITY
var _reparented := false


func _ready() -> void:
    if wall_surface == null:
        wall_surface = get_parent() as Node3D
    if player == null:
        player = get_tree().get_first_node_in_group(PLAYER_GROUP) as Node3D
    body_entered.connect(_on_body_entered)


func _physics_process(delta: float) -> void:
    if auto_tick:
        tick(delta)


## Advances the shift state machine by an exact delta. Called from
## _physics_process in play; called directly with fixed steps by the
## headless probe for bit-identical replays.
func tick(delta: float) -> void:
    if phase != Phase.SHIFTING:
        return
    _t = minf(_t + delta, shift_duration)
    var w := _smooth(_t / shift_duration)
    if player != null:
        player.global_transform.basis = Basis(_player_q_from.slerp(_player_q_to, w))
    if camera_pivot != null:
        camera_pivot.global_transform.basis = Basis(_pivot_q_from.slerp(_pivot_q_to, w))
    if _t >= shift_duration:
        phase = Phase.SETTLED


## Deterministic test hook for the headless probe: shift the player's
## up-vector onto NORMAL_TABLE[normal_idx]. Returns 0 on accept, -1 bad
## index, -2 no player wired. Physics body entry goes through the same
## _begin_shift, so the probe exercises the real path, not a mock.
func shift_to(normal_idx: int) -> int:
    if normal_idx < 0 or normal_idx >= NORMAL_TABLE.size():
        push_error("shift_to: index %d outside NORMAL_TABLE (0..%d)" % [normal_idx, NORMAL_TABLE.size() - 1])
        return -1
    if player == null:
        push_error("shift_to: no player wired")
        return -2
    return _begin_shift(NORMAL_TABLE[normal_idx].normalized())


## Snapshot for the headless probe: phase, up-vector alignment for player
## AND camera pivot, reparent state, current parent — everything an
## assertion needs, without the renderer.
func probe_state() -> Dictionary:
    var player_up := Vector3.ZERO
    var camera_up := Vector3.ZERO
    var parent_name := ""
    if player != null:
        player_up = player.global_transform.basis.y
        if player.get_parent() != null:
            parent_name = player.get_parent().name
    if camera_pivot != null:
        camera_up = camera_pivot.global_transform.basis.y
    return {
        "phase": phase,
        "settled": phase == Phase.SETTLED,
        "t": _t,
        "target": target_normal,
        "player_up": player_up,
        "align": player_up.dot(target_normal),
        "camera_up": camera_up,
        "camera_align": camera_up.dot(target_normal),
        "reparented": _reparented,
        "player_parent": parent_name,
    }


func _on_body_entered(body: Node3D) -> void:
    if body != player:
        return
    _begin_shift(plane_normal.normalized())


## Starts (or re-targets — re-entry mid-shift is allowed and recomputes
## from the CURRENT orientation, so chained volumes blend instead of
## snapping) a shift from the player's live up-vector onto `normal`.
func _begin_shift(normal: Vector3) -> int:
    var current_up := player.global_transform.basis.y
    _reparent_player()
    if current_up.distance_to(normal) < 0.00001:
        phase = Phase.SETTLED
        return 0
    target_normal = normal
    var delta_q := _shortest_arc(current_up, normal)
    _player_q_from = Quaternion(player.global_transform.basis)
    _player_q_to = delta_q * _player_q_from
    if camera_pivot != null:
        _pivot_q_from = Quaternion(camera_pivot.global_transform.basis)
    else:
        _pivot_q_from = Quaternion.IDENTITY
    _pivot_q_to = delta_q * _pivot_q_from
    _t = 0.0
    phase = Phase.SHIFTING
    return 0


## Hand the player to the wall surface, keeping world transform: from now
## on the wall's own motion (rotating room, sliding plate) carries the
## player for free — that is the whole reason for the reparent.
func _reparent_player() -> void:
    if wall_surface == null:
        return
    if player.get_parent() == wall_surface:
        _reparented = true
        return
    player.reparent(wall_surface, true)
    _reparented = true


## Shortest-arc rotation taking unit vector `from` onto unit vector `to`.
## Antiparallel (floor <-> ceiling) has NO unique shortest arc, so we pin
## a stable fallback axis — without this the ceiling shift would be
## nondeterministic across platforms and the probe would flake.
static func _shortest_arc(from: Vector3, to: Vector3) -> Quaternion:
    var d := from.dot(to)
    if d > 0.999999:
        return Quaternion.IDENTITY
    if d < -0.999999:
        var pin := from.cross(Vector3.FORWARD)
        if pin.length_squared() < 0.000001:
            pin = from.cross(Vector3.RIGHT)
        return Quaternion(pin.normalized(), PI)
    var axis := from.cross(to).normalized()
    return Quaternion(axis, from.angle_to(to))


## Smoothstep: 0 at 0, exactly 1 at 1 — the shift lands precisely on the
## target basis, never a hair off it.
static func _smooth(t: float) -> float:
    return t * t * (3.0 - 2.0 * t)
