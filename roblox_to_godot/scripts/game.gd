extends Node2D
## THE MOUNTAIN — sovereign slice (2026-09-29)
## One loop, two estate systems:
##   flock.gd       — the school: chase until a fish tires, tag it (score).
##                    Z7 2026-09-30: fish_brain.gd decides each fish's motion
##                    as MOTION_TABLE rows; this rig applies them as steering
##                    (the old flock math is the fallback when a row fails).
##   water_graph.gd — the mountain: route water through valves, a siphon,
##                    and an XOR junction. Gravity only flows downhill.
##                    The ONLY way to lift water uphill is the estate's
##                    steam law: boil it anywhere, it condenses at the
##                    highest cold node — the Crown.
## WIN: fill the Crown to 4 units. Total water in the world: 8.
## Every unit you let reach Waste is a unit you must boil twice as hard.
## Dried pools lose the school: the fish gather at the wettest pool.
##
## DUAL MODE (W1 2026-09-29, server/README.md wiring spec): at boot a
## NetClient probes the estate's world server. Welcome within 2s ->
## AUTHORITATIVE: the server's tick broadcast is the only mutator, the
## water Timer below is render-only, SPACE/E become staged action
## proposals, ack/reject feed hint_text, and score comes off the wire.
## Otherwise -> SOVEREIGN: the unchanged local slice.
##
## HEAD LAW (Z10 2026-09-30): H toggles the head law live — boolean verdict
## (water_graph.py) vs graded head (the mag/hydrology.py mirror in
## systems/water_graph.gd: cross_section depth, Q8 head, flow proportional
## to dHead). Same tick structure either way; MAG_HYDROLOGY=1 at boot
## starts in hydrology mode (the headless smoke lane's hook).

const WaterGraph := preload("res://systems/water_graph.gd")
const Flock := preload("res://systems/flock.gd")
const FishBrain := preload("res://systems/fish_brain.gd")  # Z7 2026-09-30: the brain owns the school's policy
const WaterParticles := preload("res://systems/water_particles.gd")
# B3 2026-09-30: netcode v0 - the preload now points at the interpolation
# layer (network/net_client.gd extends the W1 transport scripts/net_client.gd
# verbatim). Same signals, same surface, same dual-mode law; ticked now fires
# per render frame with t-100ms interpolated volumes instead of per server
# tick with raw ones (Gaffer snapshot interpolation; no prediction,
# ROUTE_COUNTER). Receipt: watch/inbox/last_mile_20260930/B3_NETCODE.md
const NetClient := preload("res://network/net_client.gd")
const Title := preload("res://scenes/title.gd")  # B14 2026-09-30: the door's statics (chosen_mode / join_endpoint); scenes/title.gd owns them
const Juice := preload("res://scripts/juice.gd")  # V4 2026-09-30: Z14 juice layer (shake, win flash, synth audio, vignette)
const Hud := preload("res://scripts/hud.gd")  # AA5 2026-09-30: the drawn HUD (water bars + crown ring, school panel, mode strip, tag popups)
# R7 2026-09-30 (Q15/V2ASK3): every constant shared with another script is
# aliased from systems/game_constants.gd — the single source. The BRAIN_*
# block below was a line-by-line mirror of flock.gd's values (Z7) and the
# net/UI twins below that mirrored title.gd/hud.gd; all now read one file,
# guarded by tests/test_game_constants.py against raw literals outside it.
const GC := preload("res://systems/game_constants.gd")

const WIN_CROWN := GC.WIN_CROWN
# Z14 feel pass 2026-09-29: 0.8 -> 0.5. Boiling is the game's only progress
# verb and its feedback is the NEXT tick (steam condenses at the Crown inside
# graph.tick()): measured SPACE->condense dead air 0.59s and 0.80s at the old
# pace (z14 probe, watch/inbox/hydrology/Z14_FEEL_PASS.md). 0.5s halves the
# worst case and lifts the whole-board heartbeat 1.6x while the integer
# graph stays legible at 2 ticks/s. Debt: server/world.py TICK_MS stays 800,
# so authoritative mode keeps the old pace until the server gets its own
# feel pass (out of this lane's file ownership).
const TICK_SECONDS := 0.5
const BOIL_RADIUS := 40.0
const VALVE_RADIUS := 26.0
# Z14 feel pass 2026-09-29: 10 -> 22. Terminal drift under drag 0.985 is
# ~65.7*PULL/60 px/s: at 10 the school migrated a measured 11.0 px/s toward
# the wettest pool (z14 probe, spring->hollow ~540px = 49s to gather — the
# school-follows-water loop is the slice's only systemic feedback and was
# invisible on play timescales). 22 -> ~24 px/s: a 234px spring->gate1
# gather reads in ~10s. Governs BOTH the Z7 brain path (pursue/carry rows)
# and the flock fallback; still a gentle steer vs the cursor, and the
# tired-fish carry stays interceptable for tags.
const POOL_PULL := GC.POOL_PULL   # px/s^2 gentle steer of fish toward wettest pool
const POOL_PREF_DIST := GC.POOL_PREF_DIST

# Z7 2026-09-30: the fish_brain row lane. flock.gd is READ-ONLY now, so its
# step() integration math is ported here with per-constant citations; the brain
# owns policy (which motion), the rig owns motion (how it integrates).
# R7 2026-09-30: every value here is an alias of systems/game_constants.gd
# (which flock.gd itself now reads) — the mirror and the mirrored can no
# longer disagree (V6's FLEE_RADIUS 14-vs-20 day is the receipt).
const BRAIN_FLEE_PUSH := GC.FLEE_PUSH      # flock.gd FLEE_PUSH — flee accel magnitude
const BRAIN_WIGGLE := GC.WIGGLE           # flock.gd WIGGLE — dance amplitude
const BRAIN_FATIGUE_DECAY := GC.FATIGUE_DECAY
const BRAIN_DRAG := GC.DRAG
const BRAIN_COAST_TIME := GC.COAST_TIME
const BRAIN_CATCH_RADIUS := GC.CATCH_RADIUS
const BRAIN_TIRED := GC.TIRED             # the catch window
const BRAIN_TRAIL_DROP := GC.TRAIL_DROP   # pheromone drop threshold
const MOTION_VERBS: Array = ["idle", "flee", "pursue", "carry", "dance"]  # server/protocol_table.py MOTION_VERBS (read, not re-derived)

# Net config (W1): override the endpoint with the MOUNTAIN_SERVER env var
# ("host" or "host:port"); net_client.gd begin() reads it. R7: host/port
# aliased from GC (title.gd's DEFAULT_ENDPOINT is the composed twin).
const NET_HOST := GC.NET_HOST
const NET_PORT := GC.NET_PORT
const NET_USER := "ada"
const NET_PASS := "steam"  # v0 plaintext hello; real auth/TLS is v1 debt (server README)
const NET_CONNECT_TIMEOUT := 2.0  # seconds; a welcome inside this window flips the mode
const NET_HINT_HOLD := 120

enum Mode { PROBING, AUTHORITATIVE, SOVEREIGN }

# name -> [x, elev, start_volume]
const POOL_LAYOUT := {
    "spring":  [130.0, 10, 6],
    "terrace": [430.0, 6, 0],
    "gate1":   [280.0, 5, 0],
    "hollow":  [620.0, 3, 2],
    "waste":   [790.0, 0, 0],
    "crown":   [1010.0, 14, 0],
}

var graph: Node
var flock: Node
var particles: Node2D
var player: Node2D
var pools: Dictionary = {}      # node_name -> Vector2 (board position)
var wettest: String = "spring"
var score: int = 0
var won: bool = false
var mode := Mode.PROBING
var net: NetClient = null
var sim_time := 0.0  # W1: flock wiggle time source; replaces the wall clock (flock.gd step receipt)
var last_events: Array[String] = []
# B2 2026-09-30 (AJ4's writer-side root cause): this feed was capped at 6, so
# any tick carrying more than 6 strings (say/whisper bursts + physics lines)
# dropped the head before a feed-polling reader ever saw it — feed-based
# readers (hud greeting rescan, events strip) were blind to all but the tail
# of every burst. The ring now holds 64 with drop-oldest and counts every
# drop in event_dropped (shown by the HUD's events strip). Ephemeral display
# channel only: the water_event signal stays exactly-once and the server's
# hash-chained replay log is untouched (the determinism law). Receipt:
# watch/inbox/last_mile_20260930/B2_EVENT_RING.md.
const EVENT_RING_CAP := 64
var event_dropped := 0  # events lost to ring overflow; the HUD shows the tally
var hint_text: String = ""
var hint_hold := 0  # frames a failure hint stays pinned before context hints resume
var terrain: Node2D = null  # Z3 2026-09-29: St Helens board minimap, lazy-loaded on T
var staged_motion: Dictionary = {}  # Z7: fish_id -> latest staged MOTION_TABLE row (AUTHORITATIVE only)
var brain_fallback_frames := 0      # Z7: frames the old flock math ran because a row failed the gate

# AJ4 2026-09-30 (playtest fix): valve cycling at shared pipe ends. Pools host
# several pipe ends (three share the gate1 dot) and the old first-in-dict
# tie-break made p_terrace/p_out unreachable at gate1, p_drain unreachable at
# hollow, and the siphon p_bypass — a README-taught mechanic — unreachable
# ANYWHERE (its two ends, spring and terrace, are both owned by an
# earlier-in-dict pipe; playtest bytes: three E presses at spring all picked
# p_spring). Repeated E presses within a short window at one spot now cycle
# the tie set in insertion order, and the hint names the pipe the NEXT E hit
# will toggle (the cycle state advances only on an actual press).
const VALVE_CYCLE_S := 2.0         # window in which a repeated E cycles the tie set
var _valve_last: String = ""       # the pipe the last E actually toggled
var _valve_last_pos := Vector2(1.0e9, 1.0e9)
var _valve_last_t := -99.0

# AA5 2026-09-30: the four basic-text Labels and the win ColorRect/Label are
# gone — scripts/hud.gd draws the whole HUD surface (its header owns the law)
# and hosts the byte-moved win overlay. This handle is the only game.gd state.
var hud: Control = null


func _ready() -> void:
    _build_water()
    # Watershed rung 3: the droplet layer rides the graph read-only (never
    # mutates it; the Timer/server stays the sole authority) and draws over
    # the board, under the HUD CanvasLayer.
    particles = WaterParticles.new()
    particles.bind(graph, pools, self)
    add_child(particles)
    _build_flock()
    _build_player()
    # V4 2026-09-30: the JUICE layer (Z14 feel notes: "no sound, no shake,
    # no win celebration"). Self-driving: its own _process/_draw, reading the
    # graph, pools, last_events feed, and won flag off this host — this hook
    # is the only game.gd touch (scripts/juice.gd owns everything else).
    # Added before the HUD layer so its vignette draws over the board but
    # under the HUD text; its win flash rides its own layer-2 CanvasLayer.
    var juice := Juice.new()
    juice.name = "Juice"
    juice.bind(self)
    add_child(juice)
    _build_hud()
    var t := Timer.new()
    t.wait_time = TICK_SECONDS
    t.timeout.connect(_on_water_tick)
    add_child(t)
    t.start()
    _begin_net_probe()


func _exit_tree() -> void:
    # B14 2026-09-30 (title wiring): teardown hygiene for the ESC-to-title and
    # R-reload scene swaps. NetClient is a child node (freed with us either
    # way), but its StreamPeerTCP is NOT a node: stop() disconnects the
    # socket now, deterministically, instead of at RefCounted drop.
    if net != null:
        net.stop()


func _build_water() -> void:
    graph = WaterGraph.new()
    graph.name = "WaterGraph"
    # Z10: MAG_HYDROLOGY=1|true boots in graded-head mode (headless smoke
    # lane); the H key flips it live either way.
    graph.hydrology = OS.get_environment("MAG_HYDROLOGY").to_lower() in ["1", "true"]
    add_child(graph)
    for pool_name: String in POOL_LAYOUT:
        var spec: Array = POOL_LAYOUT[pool_name]
        var kind := "cold" if pool_name == "crown" else ("waste" if pool_name == "waste" else ("xor" if pool_name == "gate1" else "plain"))
        graph.add_node(pool_name, int(spec[1]), kind, 0, int(spec[2]))
        var y := _elev_y(int(spec[1]))
        pools[pool_name] = Vector2(spec[0], y)
    graph.add_pipe("p_spring", "spring", "gate1", 1)
    graph.add_pipe("p_terrace", "terrace", "gate1", 1)
    graph.add_pipe("p_out", "gate1", "hollow", 1)
    graph.add_pipe("p_drain", "hollow", "waste", 1)
    graph.add_pipe("p_bypass", "spring", "terrace", 1, true, 2, false)  # siphon, starts shut
    graph.water_event.connect(_on_water_event)


func _build_flock() -> void:
    flock = Flock.new()
    flock.name = "Flock"
    add_child(flock)
    flock.fish_killed.connect(_on_fish_killed)
    flock.trail_dropped.connect(func(_pos: Vector2, _strength: float) -> void: pass)
    var rng := RandomNumberGenerator.new()
    rng.seed = 20260929  # deterministic slice; the water is deterministic too
    for i in 12:
        var base: Vector2 = pools["spring"]
        var jitter := Vector2(rng.randf_range(-60, 60), rng.randf_range(-50, 50))
        flock.add_fish(base + jitter)


func _build_player() -> void:
    player = preload("res://scripts/player.gd").new()
    player.name = "Player"
    add_child(player)


func _build_hud() -> void:
    # AA5 2026-09-30: the basic-text HUD (four Labels + win ColorRect) moved
    # into scripts/hud.gd — one Control that draws the pool bars, the crown
    # progress ring, the school counter panel, the mode strip, and the tag
    # popups, and hosts the win overlay. Same bind-before-add_child contract
    # as juice/water_particles; the CanvasLayer keeps its name and default
    # layer 1 (under juice's layer-2 win flash — the V4 draw-order law).
    hud = Hud.new()
    hud.name = "Hud"
    hud.bind(self)
    var layer := CanvasLayer.new()
    layer.name = "HUD"
    add_child(layer)
    layer.add_child(hud)


func _elev_y(elev: int) -> float:
    return 600.0 - elev * 36.0


# ------------------------------------------------------------- net mode ----

func _begin_net_probe() -> void:
    # B14 2026-09-30 (title wiring; receipt watch/inbox/last_mile_20260930/
    # B14_TITLE.md): the title door chooses the lane. DOOR_SOVEREIGN (0) =
    # the stranger asked to play alone: no probe, no NetClient, sovereign
    # NOW. chosen_mode -1 (no title ran: a direct scenes/main.tscn run, the
    # headless smoke lane, the AC9 harness) keeps W1's boot-probe auto-join
    # bytes exactly as they were. (R7: title.gd's door lanes renamed
    # DOOR_* — they are not game.gd's Mode enum and must not share its
    # MODE_* names.)
    if Title.chosen_mode == Title.DOOR_SOVEREIGN:
        _fall_sovereign()
        return
    net = NetClient.new()
    net.name = "NetClient"
    add_child(net)
    net.welcomed.connect(_on_net_welcomed)
    net.ticked.connect(_on_net_tick)
    net.acked.connect(_on_net_ack)
    net.rejected.connect(_on_net_reject)
    net.auth_failed.connect(_on_net_auth_failed)
    net.host = NET_HOST
    net.port = NET_PORT
    net.user = NET_USER
    net.password = NET_PASS
    # B14: the title's host:port field overrides the compiled defaults when
    # the AUTHORITATIVE door was taken and the field is non-empty. Precedence
    # stays MOUNTAIN_SERVER env (net_client.gd begin(), the packed-copy law)
    # > the field > NET_HOST/NET_PORT; begin() re-reads the env itself.
    if Title.chosen_mode == Title.DOOR_AUTHORITATIVE and Title.join_endpoint != "":
        if Title.join_endpoint.contains(":"):
            var parts := Title.join_endpoint.split(":")
            net.host = parts[0]
            net.port = int(parts[1])
        else:
            net.host = Title.join_endpoint
    net.begin()
    var deadline := Timer.new()
    deadline.name = "NetProbeDeadline"
    deadline.wait_time = NET_CONNECT_TIMEOUT
    deadline.one_shot = true
    deadline.timeout.connect(_on_probe_deadline)
    add_child(deadline)
    deadline.start()


func _on_probe_deadline() -> void:
    if mode == Mode.PROBING:
        _fall_sovereign()


func _fall_sovereign() -> void:
    mode = Mode.SOVEREIGN
    if net != null:
        net.stop()
        net.queue_free()
        net = null


func _on_net_auth_failed(why: String) -> void:
    if mode != Mode.PROBING:
        return
    hint_text = "server refused login (%s); sovereign mode" % why
    hint_hold = 300
    _fall_sovereign()


func _on_net_welcomed(world: Dictionary) -> void:
    if mode != Mode.PROBING:
        return
    mode = Mode.AUTHORITATIVE
    _apply_snapshot(world)
    hint_text = "authoritative: the mountain lives on the server"
    hint_hold = 180


func _apply_snapshot(world: Dictionary) -> void:
    # world = MountainWorld.snapshot(): to_spec() + winner/win_crown/tick_ms/
    # roster/scores (server/world.py). Board geometry stays POOL_LAYOUT
    # (the server builds the same board verbatim); only state mirrors in.
    var nodes_spec: Dictionary = world.get("nodes", {})
    for node_name: String in nodes_spec:
        if graph.nodes.has(node_name):
            var spec: Dictionary = nodes_spec[node_name]
            graph.nodes[node_name].volume = int(spec.get("volume", 0))
    var pipes_spec: Dictionary = world.get("pipes", {})
    for pipe_name: String in pipes_spec:
        if graph.pipes.has(pipe_name):
            var pspec: Dictionary = pipes_spec[pipe_name]
            if pspec.has("open"):
                graph.pipes[pipe_name].open = bool(pspec["open"])
            if pspec.has("primed"):
                graph.pipes[pipe_name].primed = bool(pspec["primed"])
    var scores: Dictionary = world.get("scores", {})
    if scores.has(net.user):
        score = int(scores[net.user])
    wettest = _wettest_pool()


func _on_net_tick(_n: int, nodes: Dictionary, events: Array, winner: bool) -> void:
    if mode != Mode.AUTHORITATIVE or net == null:
        return
    # Render-only apply: full node volumes overwrite the mirror, so any
    # probe-time local drift is erased here and the local graph.tick()
    # never runs in this mode (the server is the sole mutator).
    for node_name: String in nodes:
        if graph.nodes.has(node_name):
            graph.nodes[node_name].volume = int(nodes[node_name])
    var trimmed: Array[String] = []
    for e: String in events:
        trimmed.append(e)
        if e.begins_with(net.user + " tags a fish"):
            var s := _score_from_event(e)
            if s >= 0:
                score = s  # score from the server; the v0 tick payload has no scores field
    for e: String in trimmed:
        _push_event(e)
    wettest = _wettest_pool()
    if winner or graph.volume("crown") >= WIN_CROWN:
        _crown_filled()


func _on_net_ack(verb: String, target: String, applies_at_tick: int) -> void:
    if mode != Mode.AUTHORITATIVE:
        return
    hint_text = "staged: %s %s (applies at tick %d)" % [verb, target, applies_at_tick]
    hint_hold = 60
    if verb == "valve" and graph.pipes.has(target):
        # Render-only mirror of our own toggle so the draw tracks the proposal
        # until the next broadcast. Debt: the v0 tick payload carries node
        # volumes only, so other clients' valve moves never reach the mirror
        # (v1: pipes in the tick payload, or a snapshot re-request op).
        if graph.pipes[target].open:
            graph.close_pipe(target)
        else:
            graph.open_pipe(target)


func _on_net_reject(why: String, verb: String, target: String) -> void:
    if mode != Mode.AUTHORITATIVE:
        return
    hint_text = _reject_hint(why, verb, target)
    hint_hold = NET_HINT_HOLD


func _reject_hint(why: String, verb: String, target: String) -> String:
    # Mappings per server/README.md wiring #3; unknown codes pass through raw.
    # Q11 (2026-10-01): the chat/anti-cheat/MAC classes joined the table so
    # every typed reject the server can emit has a client-side twin (the
    # legality mirror itself lives in tests/rule_parity_runner.gd).
    match why:
        "DRY_POOL":
            return "the pool is dry"
        "UNKNOWN_TARGET":
            return "no valve within reach" if verb == "valve" else "the server does not know %s" % target
        "UNKNOWN_VERB":
            return "the server refuses that verb"
        "UNKNOWN_SID":
            return "session lost on the server; reconnect"
        "BAD_TEXT":
            return "chat refused: empty or over 240 chars"
        "RATE_CAP":
            return "one action per tick; wait for the next tick"
        "STALE_NONCE":
            return "replayed action id; ids must climb"
        "BAD_MAC":
            return "frame failed the integrity check; the server disconnected us"
        "BAD_AUTH", "UNKNOWN_OP":
            return "protocol error (%s)" % why
        _:
            return "refused: %s" % why


func _score_from_event(ev: String) -> int:
    # Parses "<user> tags a fish at <pool> (score N)." (server/world.py _apply).
    var idx := ev.find("(score ")
    if idx < 0:
        return -1
    var tail: String = ev.substr(idx + 7).split(")")[0]
    return tail.to_int() if tail.is_valid_int() else -1


func _process(delta: float) -> void:
    if won:
        return
    sim_time += delta
    # Z7 2026-09-30: the brain path owns the school — one decide() row per
    # alive fish, applied as steering. Any illegal row fails the whole frame
    # closed and the OLD flock math (flock.step + pool pull) runs instead.
    if not _step_brain(delta):
        brain_fallback_frames += 1
        flock.step(player.global_position, delta, sim_time)
        _pull_fish_to_water(delta)
    particles.step(delta, sim_time)
    _update_hints()
    queue_redraw()


# ------------------------------------------ Z7 2026-09-30: fish_brain wiring ----
# X9's integration note landed: game.gd is a motion-row consumer. Per frame it
# builds the snapshot fish_brain.gd documents (fish/player_pos/pools/wettest),
# calls decide() per alive fish, applies each row with the X9 formula
# accel * (intensity_q8 / 255.0) * delta, and in AUTHORITATIVE mode stages the
# same rows as MOTION_TABLE proposals. flock.gd keeps storage + the fallback.

func _step_brain(delta: float) -> bool:
    # Returns false when any row is illegal (brain failed) so the caller
    # reruns the old flock math for that frame. Tick is the W1 sim_time
    # counter (never the wall clock — the flock.gd:32 leak law).
    var tick := int(sim_time * 60.0)
    var snapshot := {
        "fish": flock.fish,
        "player_pos": player.global_position,
        "pools": pools,
        "wettest": _wettest_pool(),
    }
    var rows: Array = []  # [fish_id, row] in decide order
    for i in flock.fish.size():
        if not bool(flock.fish[i].get("alive", false)):
            continue
        var row: Variant = FishBrain.decide(i, tick, snapshot)
        if not _motion_row_legal(row):
            return false
        rows.append([i, row])
    if mode == Mode.AUTHORITATIVE:
        # Staged MOTION_TABLE proposals: each row already passed the payload
        # law below, so what lands here is the motion dialect's shape
        # (server/protocol_table.py MOTION_SPEC: {intensity_q8: u8,
        # dir: target}, handlers rig_*). The v0 wire does not carry motion
        # verbs yet (server adopts them in a later lane per protocol_table's
        # X9 note), so staging means parking the latest row per fish —
        # bounded by the school size, never sent, ready for that lane.
        for pair in rows:
            var r: Dictionary = pair[1]
            staged_motion[int(pair[0])] = {
                "tick": tick,
                "verb": String(r["verb"]),
                "intensity_q8": int(r["intensity_q8"]),
                "dir": String(r["dir"]),
            }
    if not _brain_trail_ok():
        return false  # inherited trail is malformed: brain lane unhealthy, fall back
    for pair in rows:
        _apply_motion_row(int(pair[0]), pair[1], delta)
    _brain_trail(delta)
    return true


func _motion_row_legal(row: Variant) -> bool:
    # The MOTION_TABLE payload law mirrored rig-side (server/protocol_table.py
    # _check_args): exact key set, u8 intensity (a bool is a verdict, not an
    # intensity), dir a node name the board knows. The Python table stays the
    # contract owner; this is the same law so nothing illegal is staged or
    # applied, and any violation means the brain failed -> flock fallback.
    if typeof(row) != TYPE_DICTIONARY:
        return false  # not a row at all (decide() broke)
    var r: Dictionary = row
    var keys: Array = r.keys()
    keys.sort()
    if keys != ["dir", "intensity_q8", "verb"]:
        return false  # BAD_ARGS: exact key set, no more, no less
    var verb: Variant = r["verb"]
    if not (verb is String) or not MOTION_VERBS.has(verb):
        return false  # UNKNOWN_VERB
    var q8: Variant = r["intensity_q8"]
    if q8 is bool or not (q8 is int) or q8 < 0 or q8 > 255:
        return false  # BAD_INTENSITY: the u8 law
    var dir_name: Variant = r["dir"]
    if not (dir_name is String) or not pools.has(dir_name):
        return false  # UNKNOWN_TARGET: dir is a node NAME, never a Vector2
    return true


func _apply_motion_row(fish_id: int, row: Dictionary, delta: float) -> void:
    # One motion row as steering (X9 formula): accel * (intensity_q8 / 255).
    # Fatigue/drag/catch/move are the flock.gd step() port (read-only file);
    # every line cites its source. Fish identity is the INDEX (Dictionary ==
    # is by value; the X9 law), so fish_killed emits fish_id directly —
    # flock.gd:79's fish.find(f) could mis-twin on value-identical dicts.
    var f: Dictionary = flock.fish[fish_id]
    var inten: float = float(row["intensity_q8"]) / 255.0
    var pos: Vector2 = f["pos"]
    var vel: Vector2 = f["vel"]
    var fatigue: float = f["fatigue"]

    match String(row["verb"]):
        "flee":
            # flock.gd:48-50: away from the player, toward the far pool
            var away: Vector2 = (pos - player.global_position).normalized()
            var to_pool: Vector2 = (pools[row["dir"]] - pos).normalized()
            vel += (away + to_pool).normalized() * BRAIN_FLEE_PUSH * inten * delta
            fatigue = minf(fatigue + delta / BRAIN_COAST_TIME, 1.0)  # flock.gd:50 tire
        "pursue", "carry":
            # game.gd _pull_fish_to_water port: steer toward pools[dir]
            var d: Vector2 = pools[row["dir"]] - pos
            if d.length() > 0.0:
                vel += d.normalized() * POOL_PULL * inten * delta
            fatigue = maxf(fatigue - delta * BRAIN_FATIGUE_DECAY / BRAIN_COAST_TIME, 0.0)  # flock.gd:53 rest
        "dance":
            # flock.gd:74 wiggle, intensity-modulated (the brain's own phase)
            vel += Vector2(sin(sim_time * 7.0 + pos.x * 0.05), cos(sim_time * 7.0 + pos.y * 0.05)) * BRAIN_WIGGLE * inten * delta
            fatigue = maxf(fatigue - delta * BRAIN_FATIGUE_DECAY / BRAIN_COAST_TIME, 0.0)  # flock.gd:53 rest
        "idle":
            # rest depth damps the coast (X9 idle row: intensity = 1 - fatigue)
            vel *= pow(1.0 - 0.05 * inten, delta * 60.0)
            fatigue = maxf(fatigue - delta * BRAIN_FATIGUE_DECAY / BRAIN_COAST_TIME, 0.0)  # flock.gd:53 rest

    vel *= pow(BRAIN_DRAG, delta * 60.0)  # flock.gd:56 drag
    f["fatigue"] = fatigue
    f["vel"] = vel
    # flock.gd:77-79 catch: the player's verb on a tired fish, before the move
    if pos.distance_to(player.global_position) < BRAIN_CATCH_RADIUS and fatigue > BRAIN_TIRED:
        f["alive"] = false
        flock.fish_killed.emit(fish_id)
        return
    f["pos"] = pos + vel * delta  # flock.gd:81 move


func _brain_trail_ok() -> bool:
    # Fail-closed precheck of the inherited trail (written by either lane),
    # run BEFORE any row applies so a fallback frame never double-steps.
    for t in flock.trail:
        if not (t is Dictionary) or not (t.has("pos") and t.has("life") and t.has("strength")):
            return false
    return true


func _brain_trail(delta: float) -> void:
    # flock.gd:84-95 pheromone trail port (flock.gd keeps the storage).
    var trail: Array[Dictionary] = flock.trail
    for f in flock.fish:
        if bool(f.get("alive", false)) and float(f["fatigue"]) > BRAIN_TRAIL_DROP:
            trail.append({"pos": f["pos"], "strength": float(f["fatigue"]), "life": float(f["fatigue"]) * 5.0})
    var alive_trail: Array[Dictionary] = []
    for t in trail:
        t["life"] = float(t["life"]) - delta
        if float(t["life"]) > 0.0:
            alive_trail.append(t)
    flock.trail = alive_trail
    if flock.trail.size() > int(flock.trail_cap):
        flock.trail = flock.trail.slice(flock.trail.size() - int(flock.trail_cap))


func _pull_fish_to_water(delta: float) -> void:
    var target := _wettest_pool()
    if target == "":
        return
    var center: Vector2 = pools[target]
    for f in flock.fish:
        if not f.alive:
            continue
        var d: Vector2 = center - f.pos
        if d.length() > POOL_PREF_DIST:
            f.vel += d.normalized() * POOL_PULL * delta


func _wettest_pool() -> String:
    var best := ""
    var best_v := 0
    for pool_name: String in pools:
        if pool_name == "waste":
            continue
        var v: int = graph.volume(pool_name)
        if v > best_v:
            best_v = v
            best = pool_name
    return best


func _unhandled_key_input(event: InputEvent) -> void:
    if event is InputEventKey and event.pressed and not event.echo:
        match event.keycode:
            KEY_ESCAPE:
                # B14 2026-09-30 (title wiring): ESC walks back out the door.
                # The scene swap frees this whole Main tree (graph, flock,
                # particles, net, timers), so walking in again re-inits clean;
                # _exit_tree above closes the socket first. Not won-gated:
                # ESC also escapes the win panel (R keeps its restart role).
                get_tree().change_scene_to_file("res://scenes/title.tscn")
            KEY_SPACE:
                _try_boil()
            KEY_E:
                _try_valve()
            KEY_H:
                _toggle_head_law()
            KEY_R:
                if won:
                    get_tree().reload_current_scene()
            KEY_T:
                # Z3 2026-09-29: toggle the St Helens terrain board
                # (scripts/terrain_loader.gd loads the water_graph.v1 spec,
                # renders the 64x64 grid as a minimap, runs its own water
                # graph underneath; the Mountain board keeps running below).
                if terrain == null:
                    terrain = preload("res://scripts/terrain_loader.gd").new()
                    terrain.name = "TerrainLoader"
                    add_child(terrain)
                else:
                    terrain.toggle()


func _toggle_head_law() -> void:
    # Z10 2026-09-30: H flips the head law mid-run (boolean verdict <->
    # graded Q8 head, the mag/hydrology.py mirror in systems/water_graph.gd).
    # Both modes tick the same graph; only _available/_move flow arithmetic
    # changes, and the event grammar is identical.
    if won:
        return
    graph.hydrology = not graph.hydrology
    hint_text = "head law: %s (H to toggle)" % ("graded Q8 hydrology" if graph.hydrology else "boolean verdict")
    hint_hold = 120


func _try_boil() -> void:
    if won:
        return
    var pool_name := _nearest_pool(player.global_position, BOIL_RADIUS)
    if pool_name == "":
        hint_text = "stand closer to water to boil it"
        hint_hold = 120
        return
    if graph.volume(pool_name) <= 0:
        hint_text = "%s is dry — nothing to boil" % pool_name
        hint_hold = 120
        return
    if mode == Mode.AUTHORITATIVE:
        # Proposal, not mutation: the server validates and stages it and the
        # apply lands in a later tick broadcast (server README wiring #3).
        # The dry pre-check above is UX on a mirror that can lag one tick;
        # the server's DRY_POOL reject is the real gate.
        if net.send_action("boil", pool_name):
            hint_text = "proposing: boil 1 at %s" % pool_name
            hint_hold = 45
        else:
            hint_text = "server link down; boil not sent"
            hint_hold = NET_HINT_HOLD
        return
    var lifted: int = graph.boil(pool_name, 1) # B1.0 fix 2026-09-29: boil() via Node handle returns Variant; := cannot infer
    _push_event("You boil 1 unit at %s; it rises." % pool_name)
    if lifted == 0:
        hint_text = "the boil failed — pool dry"


func _try_valve() -> void:
    if won:
        return
    var pipe_name := _valve_pick(player.global_position)
    if pipe_name == "":
        hint_text = "no valve within reach"
        hint_hold = 120
        return
    if mode == Mode.AUTHORITATIVE:
        # Proposal, not mutation: the server owns the toggle (README wiring #3).
        if net.send_action("valve", pipe_name):
            hint_text = "proposing: valve %s" % pipe_name
            hint_hold = 45
            _valve_advance(pipe_name)
        else:
            hint_text = "server link down; valve not sent"
            hint_hold = NET_HINT_HOLD
        return
    var p: Dictionary = graph.to_dict()["pipes"][pipe_name]
    if p["open"]:
        graph.close_pipe(pipe_name)
        _push_event("You shut %s." % pipe_name)
    else:
        # D9 playtest fix 2026-09-30 (receipt watch/inbox/last_mile_20260930/
        # D9_PLAYTEST.md): on a FRACTURED pipe open_pipe() refuses by engine
        # law (AC2: burst is forever) but the old bytes still claimed
        # "You open %s." — the feed asserted an action that never happened
        # (D9 phase C: E on the burst p_out emitted "You open p_out." while
        # the pipe stayed shut). The feed now states the refusal.
        if p["fractured"]:
            _push_event("You try %s: it FRACTURED — it stays shut forever." % pipe_name)
            hint_text = "%s is fractured; it never reopens" % pipe_name
            hint_hold = 120
            _valve_advance(pipe_name)
            return
        graph.open_pipe(pipe_name)
        _push_event("You open %s." % pipe_name)
    _valve_advance(pipe_name)


func _valve_pick(pos: Vector2) -> String:
    # AJ4: the valve chooser. Nearest pipe end wins; among TRUE ties (ends
    # within 0.5 px of the best distance — pools host several pipe ends on
    # the same dot) the pick cycles in dict insertion order when E is pressed
    # repeatedly at one spot inside the cycle window. _update_hints calls
    # this too, so the hint always names the pipe the next E will hit.
    var dump: Dictionary = graph.to_dict()["pipes"]
    var best_d := VALVE_RADIUS
    for pipe_name: String in dump:
        var p: Dictionary = dump[pipe_name]
        for end_name: String in [p["src"], p["dst"]]:
            var d: float = pos.distance_to(pools[end_name])
            if d < best_d:
                best_d = d
    if best_d >= VALVE_RADIUS:
        return ""
    var tied: Array[String] = []
    for pipe_name: String in dump:
        var p: Dictionary = dump[pipe_name]
        var md := VALVE_RADIUS + 1.0
        for end_name: String in [p["src"], p["dst"]]:
            md = minf(md, pos.distance_to(pools[end_name]))
        if md <= best_d + 0.5:
            tied.append(pipe_name)
    if tied.size() == 1:
        return tied[0]
    if _valve_last != "" and tied.has(_valve_last) and sim_time - _valve_last_t <= VALVE_CYCLE_S and _valve_last_pos.distance_to(pos) < 24.0:
        return tied[(tied.find(_valve_last) + 1) % tied.size()]
    return tied[0]


func _valve_advance(pipe_name: String) -> void:
    _valve_last = pipe_name
    _valve_last_pos = player.global_position
    _valve_last_t = sim_time


func _nearest_pool(pos: Vector2, radius: float) -> String:
    var best := ""
    var best_d := radius
    for pool_name: String in pools:
        var d: float = pos.distance_to(pools[pool_name])
        if d < best_d:
            best_d = d
            best = pool_name
    return best


# AJ4 2026-09-30 (playtest fix; receipt watch/inbox/last_mile_20260930/
# AJ4_PLAYTEST.md): every event string now fans out through graph.water_event
# — the signal water_graph.gd has declared since the original port and, until
# this fix, nothing ever emitted. Cause being fixed: consumers (water_particles
# splash/fracture parsing, hud popups, juice shake) read count-cursors over
# last_events, but the host appends AND trims the feed atomically, so once the
# feed saturated a cursor parked at the cap saw the same size forever and every
# event-driven visual went blind. Playtest evidence: 55 ticks ran with the
# fracture physics live (p_drain burst at stress 283) and zero fracture
# visuals fired — the last parsed event anywhere was tick 2's. The signal is
# exactly-once; last_events stays as the bounded display feed.
# B2 2026-09-30: the display bound itself grew 6 -> 64 (drop-oldest ring +
# event_dropped tally) so feed-based readers also survive bursts; see the
# EVENT_RING_CAP block above.
func _push_event(text: String) -> void:
    graph.water_event.emit(text)


func _on_water_event(text: String) -> void:
    # B2 2026-09-30: the old `while size() > 6: pop_front()` here was the
    # writer-side starver — a 20-event tick left only the last 6 in the ring
    # for every feed-polling reader (hud._scan_greeting/_draw_events). Now:
    # drop-OLDEST at 64, and every drop is counted (not silently lost) so the
    # HUD can show the tally. Probe evidence: burst of 20 in one tick ->
    # reader sees all 20; 70 pushed -> ring holds 64, dropped 6, newest kept.
    last_events.append(text)
    while last_events.size() > EVENT_RING_CAP:
        last_events.pop_front()
        event_dropped += 1


func _on_water_tick() -> void:
    if won:
        return
    if mode == Mode.AUTHORITATIVE:
        # Authoritative mode: this Timer is render-only. The server's tick
        # broadcast (_on_net_tick) is the sole mutator; between broadcasts
        # we merely refresh derived render state.
        wettest = _wettest_pool()
        return
    var events: Array[String] = graph.tick() # B1.0 fix 2026-09-29: tick() via Node handle returns Variant; := cannot infer
    # AJ4 continuation of the channel fix: NO slice-to-3 here anymore. The old
    # slice was a display-feed bound, but after the water_event fan-out it also
    # gated the SIGNAL — playtest run 3: the siphon-break tick carried 4
    # events, the break string was sliced away first, and the visual (AD2's
    # dim envelope + corridor kick) never fired though the engine had unlatched
    # primed. Bounding belongs to the display ring alone (_on_water_event,
    # 64-slot drop-oldest since B2).
    for e: String in events:
        _push_event(e)
    wettest = _wettest_pool()
    if graph.volume("crown") >= WIN_CROWN:
        _crown_filled()


func _crown_filled() -> void:
    # W1 2026-09-29: win block lifted verbatim from _on_water_tick so the
    # authoritative path (_on_net_tick) shares it. AA5 2026-09-30: the cover
    # + label moved into the HUD (scripts/hud.gd show_win); the string is
    # pre-existing text moved, not rewritten (em-dash law: nothing authored).
    won = true
    hud.show_win(score)


func _update_hints() -> void:
    if hint_hold > 0:
        hint_hold -= 1
        return
    var pool_name := _nearest_pool(player.global_position, BOIL_RADIUS)
    if pool_name != "" and graph.volume(pool_name) > 0:
        hint_text = "SPACE — boil 1 unit at %s (it will condense at the Crown)" % pool_name
        return
    var pipe_name := _valve_pick(player.global_position)
    if pipe_name != "":
        var p: Dictionary = graph.to_dict()["pipes"][pipe_name]
        hint_text = "E — %s %s" % ["shut" if p["open"] else "open", pipe_name]
        return
    # AJ4 polish 3 (playtest 5-second test): standing mid-board the hint
    # channel used to go EMPTY — context hints only fire near a pool or a
    # valve — so a new player saw the goal (the HUD's CROWN ring) but never
    # the verb. Guide them to the nearest pool that still holds water.
    var guide := _nearest_wet_pool(player.global_position)
    if guide != "":
        hint_text = "walk to %s — SPACE boils it up to the Crown" % guide


func _nearest_wet_pool(pos: Vector2) -> String:
    # AJ4 polish 3: the idle-hint guide target — nearest pool holding volume.
    # The crown is excluded (boiling the summit itself is a no-op); waste is
    # included (V5 law: waste is a boilable recovery basin).
    var best := ""
    var best_d := 1.0e9
    for pool_name: String in pools:
        if pool_name == "crown":
            continue
        if graph.volume(pool_name) <= 0:
            continue
        var d: float = pos.distance_to(pools[pool_name])
        if d < best_d:
            best_d = d
            best = pool_name
    return best


func _on_fish_killed(_fish_id: int) -> void:
    if mode == Mode.AUTHORITATIVE:
        # Sensing-only school (server README wiring #4): the local catch
        # proposes a server tag at the nearest wet pool; the score returns
        # in the tick events ("<user> tags a fish at <pool> (score N)").
        var pool_name := _nearest_pool(player.global_position, BOIL_RADIUS)
        if pool_name == "" or graph.volume(pool_name) <= 0:
            pool_name = wettest
        if pool_name == "" or graph.volume(pool_name) <= 0:
            hint_text = "no wet pool: the school holds no fish to tag"
            hint_hold = NET_HINT_HOLD
            return
        if not net.send_action("tag", pool_name):
            hint_text = "server link down; tag not sent"
            hint_hold = NET_HINT_HOLD
        return
    score += 1


func _draw() -> void:
    # Pipes. AD2 2026-09-30: a pipe registered in the droplet layer's
    # fracture registry (parsed off "Pipe X FRACTURES (stress N): spray to
    # Y." events) renders BROKEN — two stubs with a gap at the hash-fixed
    # fracture point, in cold dead steel instead of the live line color.
    # The registry (point t, gap half-width) lives in water_particles.gd so
    # the crack decal, the spray emitter, and these stubs share one source.
    var fx: WaterParticles = particles as WaterParticles
    var dump: Dictionary = graph.to_dict()["pipes"]
    for pipe_name: String in dump:
        var p: Dictionary = dump[pipe_name]
        var a: Vector2 = pools[p["src"]]
        var b: Vector2 = pools[p["dst"]]
        var col := Color(0.45, 0.62, 0.85) if p["open"] else Color(0.3, 0.3, 0.32, 0.5)
        var fr: Dictionary = fx.fractures.get(pipe_name, {})
        if not fr.is_empty():
            var ab := b - a
            var ln := maxf(ab.length(), 1.0)
            var d := ab / ln
            var cut := float(fr["t"]) * ln
            var gap := float(fr["gap"])
            var broke := Color(0.35, 0.42, 0.50, 0.9)
            draw_line(a, a + d * maxf(cut - gap, 2.0), broke, 3.0)
            draw_line(a + d * minf(cut + gap, ln - 2.0), b, broke, 3.0)
        else:
            draw_line(a, b, col, 3.0 if p["open"] else 1.5)
        if p["siphon"]:
            var mid := (a + b) * 0.5
            draw_circle(mid + Vector2(0, -10), 3.0, Color(0.9, 0.75, 0.3) if p["primed"] else Color(0.4, 0.38, 0.3))
            # AD2 (2): crest dot dims on "Siphon X breaks (intake dry)." — the
            # engine unlatches primed before emitting, so the base dot above is
            # already dark; this overlay starts bright and fades out over the
            # dim window, making the dim a visible transition, not a pop.
            var dim: float = float(fx.siphon_dim.get(pipe_name, 0.0))
            if dim > 0.0:
                draw_circle(mid + Vector2(0, -10), 3.0, Color(0.9, 0.75, 0.3, dim / fx.SIPHON_DIM_LIFE))
    # Pools
    for pool_name: String in pools:
        var pos: Vector2 = pools[pool_name]
        var v: int = graph.volume(pool_name)
        match pool_name:
            "waste":
                draw_rect(Rect2(pos - Vector2(22, 10), Vector2(44, 20)), Color(0.12, 0.1, 0.12))
                draw_string(ThemeDB.fallback_font, pos + Vector2(-18, -16), "WASTE", HORIZONTAL_ALIGNMENT_LEFT, -1, 11, Color(0.5, 0.4, 0.45))
            "gate1":
                draw_circle(pos, 15.0, Color(0.5, 0.45, 0.3, 0.9))
                draw_arc(pos, 20.0, 0, TAU, 24, Color(0.7, 0.6, 0.35), 1.5)
            "crown":
                var frac: float = clampf(float(v) / float(WIN_CROWN), 0.0, 1.0)
                draw_arc(pos, 30.0, -PI / 2, -PI / 2 + TAU * frac, 40, Color(0.55, 0.85, 0.95), 5.0)
                draw_arc(pos, 30.0, 0, TAU, 40, Color(0.25, 0.3, 0.38, 0.6), 1.0)
                draw_string(ThemeDB.fallback_font, pos + Vector2(-20, -40), "CROWN %d/%d" % [v, WIN_CROWN], HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color(0.7, 0.9, 1.0))
            _:
                draw_circle(pos, 24.0, Color(0.16, 0.2, 0.26))
                if v > 0:
                    draw_circle(pos, 8.0 + 3.5 * sqrt(float(v)), Color(0.3, 0.55, 0.8))
                draw_string(ThemeDB.fallback_font, pos + Vector2(-20, -30), pool_name, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.6, 0.65, 0.7))
    # Trail
    for t in flock.trail:
        var a: float = clampf(t["life"] / 5.0, 0.0, 1.0) * 0.5
        draw_circle(t["pos"], 2.0, Color(0.5, 0.7, 0.6, a))
    # Fish
    for f in flock.fish:
        if not f.alive:
            continue
        var tired: float = f["fatigue"]
        var col := Color(0.95, 0.8, 0.35) if tired > 0.7 else Color(0.65, 0.8, 0.9).lerp(Color(0.5, 0.45, 0.65), tired)
        draw_circle(f["pos"], 3.2, col)
    # Player crosshair
    draw_arc(player.global_position, 10.0, 0, TAU, 24, Color(0.95, 0.95, 0.9), 1.5)
    draw_circle(player.global_position, 2.0, Color(0.95, 0.95, 0.9))
