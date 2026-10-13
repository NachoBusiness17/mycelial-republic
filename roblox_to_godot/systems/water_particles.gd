extends Node2D
## Water Particles — Watershed rung 3 (watch/inbox/water_engineering_20260930/
## WF_SYNTHESIS.md ladder step 3: droplets with position+velocity riding the
## field). Client-render ONLY: this layer reads the integer water graph and
## never mutates it — tick/boil/valve stay with the authority (the local
## Timer in sovereign mode, the server broadcast in authoritative mode).
##
## Field sources, all derived read-only from water_graph.gd state:
##   pipes     — capsule velocity: inside a pipe corridor, droplets are pushed
##               src->dst at speed prop. to flow/cap, where flow is the integer
##               the authority's next tick would move (min(cap, src.volume)
##               when head/prime allows), with a parabolic profile across the
##               capsule radius plus a mouth-capture pull at the ends.
##   XOR gates — junction events ("Junction X passes ...") spawn curl rings:
##               tangential velocity amp * exp(-dist / CURL_FALLOFF) with a
##               decaying life; a pooled gated node also carries a gentle
##               standing churn so held water visibly spins. Ring spin comes
##               from hash(node_name) parity.
##   pools     — droplets drift toward the nearest pool that holds volume.
## Splash rings (drawn expanding arcs) fire on water_event strings delivered
## over the graph's water_event signal — AJ4 2026-09-30: game.gd emits it at
## every event append (sovereign ticks, server broadcasts, player verbs). The
## old count-cursor over the host's 6-slot last_events feed went permanently
## blind once the feed saturated (append+trim were atomic; cursor parked at
## 6 == size 6 from tick 3 — receipt AJ4_PLAYTEST.md); the signal is
## exactly-once in BOTH net modes.
##
## Determinism: zero RandomNumberGenerator. Per-droplet phase, jitter, and
## lifetime come from hash(index) through a 64-entry sine table; every time
## base is the sim_time the caller passes in (the W1 law from flock.gd's
## receipt: no wall clock — same inputs, same animation, frame for frame).
##
## AD2 2026-09-30 (destruction visual grammar, watch/inbox/last_mile_20260930/
## AD2_VISUALS.md): four event-driven visuals layered onto the same read-only
## contract. (1) "Junction X STARVED: ..." -> amber pulse ring + dust tint on
## the gated node, plus a droplet trickle at the waste basin parsed from the
## event tail (the "held at the junction" shape has no basin and no trickle).
## (2) "Siphon X breaks (intake dry)." -> shrinking ring at the src pool, a
## dim envelope on the crest dot (game.gd reads siphon_dim; the engine has
## already flipped primed to false, so the base dot is dark and this overlay
## fades bright->dark), and corridor droplets kicked toward dst. (3) steam
## column: pale droplets launched upward at any node with steam > 0 (read off
## the graph state each step, not off events — boil() sets n.steam and the
## next tick's _condense_steam clears it, so the column lives exactly the
## boil->condense window). (4) "Pipe X FRACTURES (stress N): spray to Y." ->
## persistent fracture registry (crack decal drawn here; game.gd renders the
## pipe as two stubs with a gap off fractures) plus a persistent spray
## emitter aimed at Y. The fracture physics is AD1's lane (water_graph.gd/
## water_graph.py, not touched here): the grammar above arrives on the
## water_event signal, so this layer stays inert — no error, no visual —
## until the engine starts emitting it. Zero RNG holds: crack jitter, spray
## spread, and steam launch all come from _unit(hash(seed)).

const PARTICLE_CAP := 220
# R7 2026-09-30: aliased from systems/game_constants.gd — the same drag law
# flock.gd integrates under (was a hand-copied 0.985 "flock.gd idiom").
const GC := preload("res://systems/game_constants.gd")
const DRAG := GC.DRAG               # flock idiom: vel *= pow(DRAG, dt * 60)
const CAPSULE_R := 11.0           # pipe corridor half-width, px
const PIPE_SPEED := 90.0          # px/s along the corridor at flow == cap
const MOUTH_R := 24.0             # capture radius around pipe ends
const CURL_FALLOFF := 68.0        # exp(-dist / CURL_FALLOFF), px
const CURL_LIFE := 3.2            # seconds a junction curl ring lives
const CURL_AMP := 140.0
const CHURN_FALLOFF := 38.0       # standing vortex at a pooled gated node
const SPAWN_RATE := 3.0           # droplets recycled per flow-unit per second

const DEEP := Color(0.30, 0.55, 0.80)
const SPRAY := Color(0.80, 0.93, 1.00)
const WATER_RING := Color(0.55, 0.80, 0.95)
const JUNCTION_RING := Color(0.85, 0.70, 0.35)
const SIPHON_RING := Color(0.90, 0.75, 0.30)
const STEAM_RING := Color(0.85, 0.92, 1.00)
const WASTE_RING := Color(0.50, 0.40, 0.45)
const BOIL_RING := Color(0.95, 0.95, 0.90)

# AD2 destruction grammar (see header). Colors first, then lifetimes/rates.
const STARVE_RING := Color(0.90, 0.62, 0.25)   # amber pulse on the gated node
const STARVE_DUST := Color(0.35, 0.28, 0.18)   # dust tint over the same node
const STARVE_LIFE := 2.2                        # seconds the starve marks hold
const TRICKLE_RATE := 8.0                       # droplets/s at the waste basin
const TRICKLE_LIFE := 1.4                       # seconds the trickle runs
const SIPHON_KICK := 130.0                      # px/s impulse toward dst
const SIPHON_KICK_R := 20.0                     # corridor radius that eats it
const SIPHON_DIM_LIFE := 1.1                    # seconds the crest dot dims
const STEAM_RATE := 16.0                        # droplets/s per steam unit
const STEAM_RISE := 55.0                        # launch speed, px/s upward
const STEAM_BUOY := 70.0                        # px/s^2 upward while alive
const STEAM_COL := Color(0.88, 0.94, 1.00)      # pale column droplet
const FRACTURE_RATE := 2.5                      # spray droplets/s at stress 0
const FRACTURE_SPRAY := 70.0                    # spray launch speed, px/s
const CRACK_COL := Color(0.12, 0.11, 0.10, 0.9)

var graph: Node = null            # systems/water_graph.gd instance (read-only; water_event source)
var pools: Dictionary = {}        # node_name -> Vector2 board position
var host: Node = null             # game.gd (bind contract; the feed poll is gone, AJ4)

var particles: Array[Dictionary] = []   # {pos, vel, life, max_life, dead, steam}
var curls: Array[Dictionary] = []       # {pos, spin, amp, life}
var splashes: Array[Dictionary] = []    # {pos, r, growth, life, max, col}
var churns: Array[Dictionary] = []      # {pos, spin, amp} standing pooled-gate vortices
var starves: Array[Dictionary] = []     # AD2: {pos, phase, life} amber pulse + dust tint
var trickles: Array[Dictionary] = []    # AD2: {pos, rate, budget, life} waste-basin trickle
var fractures: Dictionary = {}          # AD2: pipe_name -> {t, gap, pt, along, perp, dir, stress, budget, seed}
var siphon_dim: Dictionary = {}         # AD2: pipe_name -> life (crest dot dim envelope)
var steam_budgets: Dictionary = {}      # AD2: node_name -> fractional spawn accumulator
var sine: Array[float] = []             # 64-entry table in [-1, 1]

var spawn_wheel := 0              # weighted round-robin cursor over flow units
var spawn_budget := 0.0
var recycle_cursor := 0           # sweep cursor for the longest-dead droplet
var sim_clock := 0.0              # last sim_time handed to step(); _draw spins curl arcs with it


func _init() -> void:
    for i in 64:
        sine.append(sin(TAU * float(i) / 64.0))


## game.gd calls this right after instantiation, before add_child():
## graph + pools must already be built (they are by end of _build_water()).
func bind(graph_ref: Node, pools_ref: Dictionary, host_ref: Node) -> void:
    graph = graph_ref
    pools = pools_ref
    host = host_ref
    # AJ4 2026-09-30: event delivery moved from the (blind) count-cursor poll
    # of the host's bounded feed to the graph's water_event signal, emitted by
    # game.gd at every append — see game.gd _push_event for the receipt.
    graph.connect("water_event", _on_event)
    _seed_particles()


func _seed_particles() -> void:
    # Initial fill: distribute along the corridors that already flow, weight
    # by integer flow units, positions staggered by hash(index) through the
    # sine table. If nothing flows yet, droplets start dead and the spawner
    # revives them the moment flow appears.
    var flows: Array[Dictionary] = _active_flows()
    var total_units := 0
    for f: Dictionary in flows:
        total_units += int(f["units"])
    for i in PARTICLE_CAP:
        var p := {"pos": Vector2.ZERO, "vel": Vector2.ZERO, "life": 0.0, "max_life": 1.0, "dead": true, "steam": false}
        var ml: float = 4.0 + 4.0 * _unit(i * 17 + 3)
        p["max_life"] = ml
        p["life"] = ml * (0.15 + 0.85 * _unit(i * 5 + 1))  # stagger deaths into a steady stream
        if total_units > 0:
            var wheel: int = absi(hash(i * 977)) % total_units
            var chosen: Dictionary = flows[flows.size() - 1]
            var acc := 0
            for f: Dictionary in flows:
                acc += int(f["units"])
                if wheel < acc:
                    chosen = f
                    break
            var a: Vector2 = chosen["a"]
            var b: Vector2 = chosen["b"]
            var t: float = _unit(i * 11 + 7)
            var side: Vector2 = Vector2(-(b.y - a.y), b.x - a.x).normalized()
            p["pos"] = a + (b - a) * t + side * (CAPSULE_R * 0.7 * _unit(i * 13 + 9))
            p["vel"] = chosen["dir"] * (14.0 + 10.0 * _unit(i * 19 + 11))
            p["dead"] = false
        particles.append(p)


## The whole per-frame update. delta for motion, sim_time for every phase —
## the flock.gd W1 contract: no wall clock anywhere in this file.
func step(delta: float, sim_time: float) -> void:
    if graph == null or pools.is_empty():
        return
    sim_clock = sim_time
    _decay_rings(delta)
    var flows: Array[Dictionary] = _active_flows()
    _update_churns()
    _spawn(delta, flows)
    _spawn_steam(delta)
    _spawn_fracture_spray(delta)
    _run_trickles(delta)
    for i in particles.size():
        var p: Dictionary = particles[i]
        if p["dead"]:
            continue
        var steamy: bool = bool(p.get("steam", false))
        var vel: Vector2 = p["vel"]
        # Steam droplets skip the pool-gather pull (buoyant: the column must
        # leave the pool it boiled from) and ride their own upward accel.
        vel += _field_at(p["pos"], flows, steamy) * delta
        if steamy:
            vel += Vector2(0.0, -STEAM_BUOY) * delta
        else:
            # Sine-table wiggle, phase from hash(index): droplets shimmer in still pools.
            var ph: float = TAU * _unit(i * 23 + 2)
            vel += Vector2(_tab(sim_time * 1.7 + ph), _tab(sim_time * 1.3 + ph * 2.0)) * 6.0 * delta
        vel *= pow(DRAG, delta * 60.0)
        p["vel"] = vel
        p["pos"] = p["pos"] + vel * delta
        var life: float = p["life"] - delta
        p["life"] = life
        var pos: Vector2 = p["pos"]
        if life <= 0.0 or pos.x < -40.0 or pos.x > 1200.0 or pos.y < -60.0 or pos.y > 700.0:
            p["dead"] = true
    queue_redraw()


# ------------------------------------------------------------------ field ----

func _active_flows() -> Array[Dictionary]:
    # Read-only snapshot of every pipe whose integer flow is nonzero: the
    # exact units the authority's next tick would move (water_graph.gd
    # _available arithmetic, recomputed client-side, never executed on it).
    var out: Array[Dictionary] = []
    var pipes_dict: Dictionary = graph.pipes
    for pipe_name: String in pipes_dict:
        var pipe = pipes_dict[pipe_name]
        var open: bool = pipe.open
        var src_name: String = pipe.src
        var dst_name: String = pipe.dst
        var cap: int = pipe.cap
        var siphon: bool = pipe.siphon
        var primed: bool = pipe.primed
        var nodes_dict: Dictionary = graph.nodes
        var src = nodes_dict.get(src_name)
        var dst = nodes_dict.get(dst_name)
        if src == null or dst == null:
            continue
        var src_vol: int = src.volume
        var units := 0
        if open and src_vol > 0:
            if siphon:
                if primed:
                    units = mini(cap, src_vol)
            elif src.elev > dst.elev:
                units = mini(cap, src_vol)
        if units <= 0 or not (pools.has(src_name) and pools.has(dst_name)):
            continue
        var a: Vector2 = pools[src_name]
        var b: Vector2 = pools[dst_name]
        out.append({
            "name": pipe_name,
            "a": a,
            "b": b,
            "dir": (b - a) / maxf((b - a).length(), 1.0),
            "units": units,
            "frac": clampf(float(units) / float(maxi(cap, 1)), 0.0, 1.0),
        })
    return out


func _field_at(pos: Vector2, flows: Array[Dictionary], buoyant: bool = false) -> Vector2:
    var v := Vector2.ZERO
    # Pipe capsules: along-corridor velocity with parabolic radial profile.
    for f: Dictionary in flows:
        var a: Vector2 = f["a"]
        var ab: Vector2 = f["b"] - a
        var lensq: float = maxf(ab.length_squared(), 1.0)
        var t: float = clampf((pos - a).dot(ab) / lensq, 0.0, 1.0)
        var off: Vector2 = pos - (a + ab * t)
        var d: float = off.length()
        if d < CAPSULE_R:
            var profile: float = 1.0 - (d / CAPSULE_R) * (d / CAPSULE_R)
            v += f["dir"] * (PIPE_SPEED * float(f["frac"])) * profile
            if d > 0.5:
                v -= off.normalized() * 14.0 * profile  # confinement toward the axis
        elif d < MOUTH_R:
            v -= off.normalized() * 10.0  # mouth capture: pull nearby droplets in
    # Junction curl rings: tangential, exp falloff, decaying life.
    for c: Dictionary in curls:
        var roff: Vector2 = pos - c["pos"]
        var dist: float = roff.length()
        if dist < 0.5 or dist > CURL_FALLOFF * 4.0:
            continue
        var tangent: Vector2 = Vector2(-roff.y, roff.x) / dist
        v += tangent * (float(c["amp"]) * float(c["spin"]) * exp(-dist / CURL_FALLOFF) * (float(c["life"]) / CURL_LIFE))
    # Standing churn at pooled gated nodes.
    for ch: Dictionary in churns:
        var coff: Vector2 = pos - ch["pos"]
        var cdist: float = coff.length()
        if cdist < 0.5 or cdist > CHURN_FALLOFF * 3.0:
            continue
        var ctan: Vector2 = Vector2(-coff.y, coff.x) / cdist
        v += ctan * (float(ch["amp"]) * float(ch["spin"]) * exp(-cdist / CHURN_FALLOFF))
    # Wet pools gather nearby droplets. Buoyant (steam) droplets are exempt:
    # the gather pull would bend the rising column back into the pool it
    # just boiled from (AD2).
    if not buoyant:
        for pool_name: String in pools:
            var vol: int = graph.volume(pool_name)
            if vol <= 0:
                continue
            var to_pool: Vector2 = pools[pool_name] - pos
            var pd: float = to_pool.length()
            if pd > 0.5 and pd < 34.0:
                v += to_pool.normalized() * (20.0 * (1.0 - pd / 34.0))
    return v


func _update_churns() -> void:
    # Gated nodes (xor/sill) holding volume spin slowly: held water churns.
    churns.clear()
    var nodes_dict: Dictionary = graph.nodes
    for node_name: String in nodes_dict:
        var n = nodes_dict[node_name]
        if n.volume <= 0:
            continue
        if not (n.kind == "xor" or n.kind == "sill"):
            continue
        if not pools.has(node_name):
            continue
        churns.append({
            "pos": pools[node_name],
            "spin": 1.0 if absi(hash(node_name)) % 2 == 0 else -1.0,
            "amp": 26.0 * float(mini(n.volume, 4)),
        })


# ----------------------------------------------------------------- spawn ----

func _spawn(delta: float, flows: Array[Dictionary]) -> void:
    # Respawn at pipe srcs proportional to integer flow: a weighted
    # round-robin wheel over flow units — the zero-RNG way to sample "proportional
    # to flow". Dead droplets are recycled in cursor order.
    var total_units := 0
    for f: Dictionary in flows:
        total_units += int(f["units"])
    if total_units <= 0:
        return
    spawn_budget += float(total_units) * SPAWN_RATE * delta
    while spawn_budget >= 1.0:
        spawn_budget -= 1.0
        spawn_wheel = (spawn_wheel + 1) % total_units
        var chosen: Dictionary = flows[flows.size() - 1]
        var acc := 0
        for f: Dictionary in flows:
            acc += int(f["units"])
            if spawn_wheel < acc:
                chosen = f
                break
        var idx := _recycle_idx()
        if idx >= 0:
            _respawn(particles[idx], idx, chosen)


func _recycle_idx() -> int:
    # AD2: the _spawn cursor sweep lifted out — every emitter (corridor,
    # steam, fracture spray, trickle) recycles the longest-idle dead droplet
    # through the same sweep. Returns -1 when the cap is fully alive.
    for k in PARTICLE_CAP:
        var idx: int = (recycle_cursor + k) % PARTICLE_CAP
        if particles[idx]["dead"]:
            recycle_cursor = (idx + 1) % PARTICLE_CAP
            return idx
    return -1


func _respawn(p: Dictionary, idx: int, pipe: Dictionary) -> void:
    # Emerge at the pipe src end, jittered by hash(index) through the sine table.
    var a: Vector2 = pipe["a"]
    var ang: float = TAU * _unit(idx * 7 + 13)
    var rad: float = 4.0 + 9.0 * _unit(idx * 31 + 5)
    p["pos"] = a + Vector2(cos(ang), sin(ang)) * rad
    p["vel"] = pipe["dir"] * 18.0
    var ml: float = 4.0 + 4.0 * _unit(idx * 17 + 3)
    p["life"] = ml
    p["max_life"] = ml
    p["dead"] = false
    p["steam"] = false


# ----------------------------------------------- AD2 destruction emitters ----

func _spawn_steam(delta: float) -> void:
    # (3) Steam column: pale droplets launched upward at every node the graph
    # holds steam > 0 at, rate scaled by the integer steam units. Reads state
    # (not events): boil() sets n.steam, the next tick's _condense_steam
    # clears it, and the column lives exactly that boil->condense window.
    var nodes_dict: Dictionary = graph.nodes
    var steaming: Array[String] = []
    for node_name: String in nodes_dict:
        if int(nodes_dict[node_name].steam) > 0 and pools.has(node_name):
            steaming.append(node_name)
    var stale: Array = []
    for node_name in steam_budgets.keys():
        if not (node_name is String) or not steaming.has(node_name):
            stale.append(node_name)
    for node_name in stale:
        steam_budgets.erase(node_name)
    for node_name: String in steaming:
        steam_budgets[node_name] = float(steam_budgets.get(node_name, 0.0)) + STEAM_RATE * float(int(nodes_dict[node_name].steam)) * delta
        while float(steam_budgets[node_name]) >= 1.0:
            steam_budgets[node_name] = float(steam_budgets[node_name]) - 1.0
            var idx := _recycle_idx()
            if idx < 0:
                steam_budgets[node_name] = 0.0
                break
            var p: Dictionary = particles[idx]
            var s := absi(hash(node_name)) + idx * 13
            p["pos"] = pools[node_name] + Vector2((_unit(s + 1) - 0.5) * 14.0, -2.0 - 6.0 * _unit(s + 3))
            p["vel"] = Vector2((_unit(s + 5) - 0.5) * 10.0, -STEAM_RISE * (0.7 + 0.6 * _unit(s + 7)))
            var ml: float = 1.0 + 0.8 * _unit(s + 9)
            p["life"] = ml
            p["max_life"] = ml
            p["dead"] = false
            p["steam"] = true


func _spawn_fracture_spray(delta: float) -> void:
    # (4) Persistent spray at each registered fracture, aimed at the "spray
    # to Y" node, rate lifting with stress. Runs every step for the life of
    # the registry entry (fractures do not heal).
    for pipe_name: String in fractures:
        var fr: Dictionary = fractures[pipe_name]
        fr["budget"] = float(fr["budget"]) + FRACTURE_RATE * (1.0 + float(fr["stress"]) / 8.0) * delta
        while float(fr["budget"]) >= 1.0:
            fr["budget"] = float(fr["budget"]) - 1.0
            var idx := _recycle_idx()
            if idx < 0:
                fr["budget"] = 0.0
                break
            var p: Dictionary = particles[idx]
            var s: int = int(fr["seed"]) + idx * 31
            var perp: Vector2 = fr["perp"]
            var dir: Vector2 = fr["dir"]
            # Spread around the spray axis: hash-jittered rotation (+-0.4 rad).
            var a: float = (_unit(s + 1) - 0.5) * 0.8
            var kicked: Vector2 = Vector2(dir.x * cos(a) - dir.y * sin(a), dir.x * sin(a) + dir.y * cos(a))
            p["pos"] = fr["pt"] + perp * ((_unit(s + 3) - 0.5) * 8.0)
            p["vel"] = kicked * (FRACTURE_SPRAY * (0.7 + 0.6 * _unit(s + 5)))
            var ml: float = 1.4 + 1.2 * _unit(s + 7)
            p["life"] = ml
            p["max_life"] = ml
            p["dead"] = false
            p["steam"] = false


func _run_trickles(delta: float) -> void:
    # (1) STARVED droplet trickle at the waste basin: a short-lived emitter
    # raining droplets into the basin the spill routed to.
    for tr: Dictionary in trickles:
        tr["budget"] = float(tr["budget"]) + float(tr["rate"]) * delta
        while float(tr["budget"]) >= 1.0:
            tr["budget"] = float(tr["budget"]) - 1.0
            var idx := _recycle_idx()
            if idx < 0:
                tr["budget"] = 0.0
                break
            var p: Dictionary = particles[idx]
            var s := absi(hash(idx * 101 + 7))
            p["pos"] = tr["pos"] + Vector2((_unit(s + 1) - 0.5) * 18.0, -10.0 - 6.0 * _unit(s + 3))
            p["vel"] = Vector2((_unit(s + 5) - 0.5) * 14.0, 42.0)
            var ml: float = 0.9 + 0.5 * _unit(s + 9)
            p["life"] = ml
            p["max_life"] = ml
            p["dead"] = false
            p["steam"] = false


# ---------------------------------------------------------------- events ----

func _on_event(text: String) -> void:
    var parts: PackedStringArray = text.split(" ")
    if text.begins_with("Junction "):
        if parts.size() < 2 or not pools.has(parts[1]):
            return
        var jpos: Vector2 = pools[parts[1]]
        if text.contains(" passes ") or text.contains(" sill reached"):
            curls.append({"pos": jpos, "spin": 1.0 if absi(hash(parts[1])) % 2 == 0 else -1.0, "amp": CURL_AMP, "life": CURL_LIFE})
            _ring(jpos, 14.0, 46.0, JUNCTION_RING)
        elif text.contains(" STARVED:"):
            # AD2 (1): amber pulse ring + dust tint on the gated node; droplet
            # trickle at the waste basin parsed from the event tail. Two
            # grammar shapes (water_graph.gd): "... spilled to waste at X (...)"
            # carries the basin, "... held at the junction (...)" does not.
            starves.append({"pos": jpos, "phase": TAU * _unit(absi(hash(parts[1])) % 997), "life": STARVE_LIFE})
            if text.contains(" spilled to waste at "):
                var tail: PackedStringArray = text.split(" spilled to waste at ")
                if tail.size() >= 2:
                    var basin: String = tail[1].split(" ")[0]
                    if pools.has(basin):
                        trickles.append({"pos": pools[basin], "rate": TRICKLE_RATE, "budget": 0.0, "life": TRICKLE_LIFE})
        else:
            _ring(jpos, 10.0, 26.0, Color(0.6, 0.55, 0.4, 0.8))
    elif text.begins_with("Siphon "):
        if parts.size() < 2 or not graph.pipes.has(parts[1]):
            return
        var src_name: String = graph.pipes[parts[1]].src
        if text.contains(" breaks (intake dry)"):
            # AD2 (2): shrinking ring at src, crest-dot dim envelope, corridor
            # droplets kicked toward dst. The engine has already unlatched
            # primed before emitting, so the base dot is dark and the dim
            # overlay fades bright -> dark over SIPHON_DIM_LIFE.
            if pools.has(src_name):
                _ring(pools[src_name], 30.0, 6.0, SIPHON_RING)
            siphon_dim[parts[1]] = SIPHON_DIM_LIFE
            _kick_corridor(parts[1])
        elif pools.has(src_name):
            _ring(pools[src_name], 8.0, 34.0, SIPHON_RING)
    elif text.begins_with("Pipe ") and text.contains(" FRACTURES"):
        # AD2 (4): "Pipe X FRACTURES (stress N): spray to Y." The physics is
        # AD1's lane; this parses the fixed grammar off the feed and renders.
        if parts.size() >= 2:
            _register_fracture(parts[1], _stress_from_event(text), _spray_target_from_event(text))
    elif text.begins_with("Steam condenses at "):
        var node_name: String = text.substr("Steam condenses at ".length()).split(" ")[0]
        if pools.has(node_name):
            _ring(pools[node_name], 6.0, 30.0, STEAM_RING)
    elif text.contains(" to waste at "):
        var tail: PackedStringArray = text.split(" at ")
        if tail.size() >= 2 and pools.has(tail[tail.size() - 1]):
            _ring(pools[tail[tail.size() - 1]], 8.0, 28.0, WASTE_RING)
    elif text.contains("->"):
        # "p_out: 1 gate1->hollow." — splash at the dst pool, sized by units.
        var head: PackedStringArray = text.split(": ")
        if head.size() == 2:
            var body: PackedStringArray = head[1].split(" ")
            if body.size() >= 2:
                var units: int = body[0].to_int() if body[0].is_valid_int() else 1
                var ends: PackedStringArray = body[1].trim_suffix(".").split("->")
                if ends.size() == 2 and pools.has(ends[1]):
                    _ring(pools[ends[1]], 4.0 + 3.0 * float(units), 22.0 + 10.0 * float(units), WATER_RING)
    elif text.begins_with("You boil"):
        # "You boil 1 unit at spring; it rises."
        var seg: PackedStringArray = text.split(" at ")
        if seg.size() >= 2:
            var pool_name: String = seg[1].split(";")[0]
            if pools.has(pool_name):
                _ring(pools[pool_name], 6.0, 38.0, BOIL_RING)
    elif text.contains(" tags a fish at "):
        var seg2: PackedStringArray = text.split(" tags a fish at ")
        if seg2.size() >= 2:
            var pool2: String = seg2[1].split(" ")[0]
            if pools.has(pool2):
                _ring(pools[pool2], 6.0, 26.0, Color(0.95, 0.8, 0.35))


func _stress_from_event(text: String) -> int:
    # "(stress N)" from the fracture grammar; 0 when the clause is malformed.
    var idx := text.find("(stress ")
    if idx < 0:
        return 0
    var n := text.substr(idx + 8).split(")")[0]
    return n.to_int() if n.is_valid_int() else 0


func _spray_target_from_event(text: String) -> String:
    # "spray to Y." -> "Y"; empty when the clause is malformed.
    var seg: PackedStringArray = text.split(" spray to ")
    if seg.size() < 2:
        return ""
    return seg[1].trim_suffix(".").split(" ")[0]


func _register_fracture(pipe_name: String, stress: int, spray_to: String) -> void:
    # Idempotent on re-parse (the feed cursor can replay up to 3 tail events
    # after the host trims): an existing registry entry is left untouched.
    if fractures.has(pipe_name) or not graph.pipes.has(pipe_name):
        return
    var pipe = graph.pipes[pipe_name]
    if not (pools.has(pipe.src) and pools.has(pipe.dst)):
        return
    var a: Vector2 = pools[pipe.src]
    var b: Vector2 = pools[pipe.dst]
    var ab: Vector2 = b - a
    var ln: float = maxf(ab.length(), 1.0)
    var along: Vector2 = ab / ln
    var seed := absi(hash(pipe_name))
    var t := 0.35 + 0.30 * _unit(seed % 9973)
    var spray_dst: String = spray_to if pools.has(spray_to) else pipe.dst
    var to_dst: Vector2 = pools[spray_dst] - (a + ab * t)
    fractures[pipe_name] = {
        "t": t,
        "gap": minf(8.0 + 2.0 * float(stress), 16.0),
        "pt": a + ab * t,
        "along": along,
        "perp": Vector2(-along.y, along.x),
        "dir": to_dst / maxf(to_dst.length(), 1.0),
        "stress": maxi(stress, 0),
        "budget": 0.0,
        "seed": seed,
    }


func _kick_corridor(pipe_name: String) -> void:
    # AD2 (2): every live droplet inside the broken siphon's corridor gets an
    # impulse toward dst, scaled by proximity to the axis — the water that
    # was in flight does not vanish with the prime latch, it gets thrown.
    if not graph.pipes.has(pipe_name):
        return
    var pipe = graph.pipes[pipe_name]
    if not (pools.has(pipe.src) and pools.has(pipe.dst)):
        return
    var a: Vector2 = pools[pipe.src]
    var ab: Vector2 = pools[pipe.dst] - a
    var lensq: float = maxf(ab.length_squared(), 1.0)
    var d: Vector2 = ab / sqrt(lensq)
    for p: Dictionary in particles:
        if p["dead"]:
            continue
        var pos: Vector2 = p["pos"]
        var t: float = clampf((pos - a).dot(ab) / lensq, 0.0, 1.0)
        var dist: float = (pos - (a + ab * t)).length()
        if dist < SIPHON_KICK_R:
            p["vel"] = (p["vel"] as Vector2) + d * (SIPHON_KICK * (1.0 - dist / SIPHON_KICK_R))


func _ring(pos: Vector2, r0: float, r1: float, col: Color) -> void:
    splashes.append({"pos": pos, "r": r0, "growth": (r1 - r0) / 0.9, "life": 0.9, "max": 0.9, "col": col})


func _decay_rings(delta: float) -> void:
    var live_curls: Array[Dictionary] = []
    for c: Dictionary in curls:
        c["life"] = float(c["life"]) - delta
        if float(c["life"]) > 0.0:
            live_curls.append(c)
    curls = live_curls
    var live_splashes: Array[Dictionary] = []
    for s: Dictionary in splashes:
        s["life"] = float(s["life"]) - delta
        s["r"] = float(s["r"]) + float(s["growth"]) * delta
        if float(s["life"]) > 0.0:
            live_splashes.append(s)
    splashes = live_splashes
    # AD2: starve marks, basin trickles, crest-dot dims decay on the same beat.
    var live_starves: Array[Dictionary] = []
    for st: Dictionary in starves:
        st["life"] = float(st["life"]) - delta
        if float(st["life"]) > 0.0:
            live_starves.append(st)
    starves = live_starves
    var live_trickles: Array[Dictionary] = []
    for tr: Dictionary in trickles:
        tr["life"] = float(tr["life"]) - delta
        if float(tr["life"]) > 0.0:
            live_trickles.append(tr)
    trickles = live_trickles
    var dead_dims: Array = []
    for pipe_name in siphon_dim.keys():
        siphon_dim[pipe_name] = float(siphon_dim[pipe_name]) - delta
        if float(siphon_dim[pipe_name]) <= 0.0:
            dead_dims.append(pipe_name)
    for pipe_name in dead_dims:
        siphon_dim.erase(pipe_name)


# ------------------------------------------------------------------ draw ----

func _draw() -> void:
    # Droplets: deep blue when slow, pale spray when fast, alpha enveloped at
    # both ends of each droplet's life so the stream never pops. Steam
    # droplets are pale regardless of speed (the AD2 column reads as vapor).
    for p: Dictionary in particles:
        if p["dead"]:
            continue
        var pos: Vector2 = p["pos"]
        var sp: float = (p["vel"] as Vector2).length()
        var fade: float = sin(PI * clampf(float(p["life"]) / float(p["max_life"]), 0.001, 1.0))
        if bool(p.get("steam", false)):
            var vcol := STEAM_COL
            vcol.a = 0.30 + 0.35 * fade
            draw_circle(pos, 1.4, vcol)
            continue
        var col: Color = DEEP.lerp(SPRAY, clampf(sp / 110.0, 0.0, 1.0))
        col.a = 0.28 + 0.40 * fade
        draw_circle(pos, 1.5 + clampf(sp * 0.012, 0.0, 1.2), col)
    # Splash rings: expanding arcs fading quadratically (a break event's ring
    # carries negative growth and contracts — draw_arc clamps radius >= 1).
    for s: Dictionary in splashes:
        var t: float = 1.0 - clampf(float(s["life"]) / float(s["max"]), 0.0, 1.0)
        var scol: Color = s["col"]
        scol.a = (1.0 - t) * (1.0 - t) * 0.8
        draw_arc(s["pos"], maxf(float(s["r"]), 1.0), 0.0, TAU, 26, scol, 1.6)
    # Curl cores: a faint spinning arc pair at each junction ring.
    for c: Dictionary in curls:
        var lf: float = clampf(float(c["life"]) / CURL_LIFE, 0.0, 1.0)
        var ccol := Color(0.75, 0.85, 0.95, 0.22 * lf)
        var start: float = sim_clock * 3.0 * float(c["spin"])
        draw_arc(c["pos"], 26.0, start, start + 2.2, 18, ccol, 1.2)
        draw_arc(c["pos"], 26.0, start + PI, start + PI + 2.2, 18, ccol, 1.2)
    # AD2 (1): STARVED amber pulse ring + dust tint on the gated node. The
    # pulse breathes off sim_clock through the sine table (phase from the
    # node-name hash — zero RNG); both marks fade with the starve life.
    for st: Dictionary in starves:
        var slf: float = clampf(float(st["life"]) / STARVE_LIFE, 0.0, 1.0)
        var pulse_r: float = 15.0 + 4.0 * _tab(sim_clock * 5.0 + float(st["phase"]))
        var scol2 := Color(STARVE_RING.r, STARVE_RING.g, STARVE_RING.b, 0.55 * slf)
        draw_arc(st["pos"], maxf(pulse_r, 1.0), 0.0, TAU, 26, scol2, 2.0)
        var dcol := Color(STARVE_DUST.r, STARVE_DUST.g, STARVE_DUST.b, 0.20 * slf)
        draw_circle(st["pos"], 17.0, dcol)
    # AD2 (4): crack decals — a jagged polyline across each fractured pipe at
    # its registry point, jitter fixed per pipe by the hash idiom so the crack
    # is byte-stable frame to frame (a decal, not an animation).
    for pipe_name: String in fractures:
        var fr: Dictionary = fractures[pipe_name]
        var w: float = minf(6.0 + float(fr["stress"]) * 0.8, 14.0)
        var seed: int = int(fr["seed"])
        var pts := PackedVector2Array()
        var segs := 7
        for i in segs + 1:
            var u: float = float(i) / float(segs) * 2.0 - 1.0
            var jag_along: float = (_unit(seed + i * 17 + 1) - 0.5) * 7.0
            var jag_across: float = (_unit(seed + i * 29 + 7) - 0.5) * 6.0 * (1.0 - absf(u) * 0.5)
            pts.append(fr["pt"] + fr["perp"] * (u * w + jag_across) + fr["along"] * jag_along)
        draw_polyline(pts, CRACK_COL, 2.0)


# ------------------------------------------------------------- sine table ----

func _tab(x: float) -> float:
    # Sine via the 64-entry table: the flock.gd wiggle idiom, quantized.
    var frac: float = x / TAU * 64.0
    var frac_part: float = frac - floorf(frac)
    var i0: int = absi(int(floorf(frac))) % 64
    var i1: int = (i0 + 1) % 64
    return lerp(sine[i0], sine[i1], clampf(frac_part, 0.0, 1.0))


func _unit(seed: int) -> float:
    # Deterministic [0, 1] from an integer seed: hash(index) through the table.
    return 0.5 + 0.5 * sine[absi(hash(seed)) % 64]
