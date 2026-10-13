extends Node
## Flock — ported from dashboard/static/games/swarm.html + roblox/src/shared/Flock.luau
## Boids: flee/tire/rest, school cohesion+separation+wiggle, pheromone trail.
## Scale law: speeds x0.08, lengths flee 20 / catch 3.5 / school 20 / sep 3 / trail 38.
##
## POSITIVE MODE (LM9 2026-09-30, operator law: reward beats threat): with
## `positive = true` and food on the board, the food gradient ATTRACTS —
## fish seek food, gain satiation, and satiation modulates explore-vs-exploit
## (hungry exploit the gradient, fed fish mill on the patch). No flee accrual,
## no fatigue, no catch window: the panic state cannot exist. The threat path
## (positive = false, the default) is byte-identical to V6's tuning.

signal fish_killed(fish_id: int)
signal trail_dropped(pos: Vector2, strength: float)

# R7 2026-09-30 (Q15/V2ASK3): every constant shared with another script is
# aliased from systems/game_constants.gd — the single source. tests/
# test_game_constants.py fails on any raw literal of a registered name
# outside that file, so a retune can never land on one twin only (the V6
# lesson: Z14 moved FLEE_RADIUS here and fish_brain.gd kept 14 for a day).
const GC := preload("res://systems/game_constants.gd")

# Z14 2026-09-30: 14 -> 20. At the old push the flee terminal speed was
# 2.5 / (60 * (1 - 0.985)) = ~2.8 px/s, so 14px bought ~5s of threat room.
# The push is now 6.0 (~6.7 px/s terminal), so 14px shrank the reaction
# window proportionally; 20 keeps the cursor-warning time in the same
# ballpark. R7 trued fish_brain.gd's stale 14 mirror up (V6_FISH_FLEE.md
# handoff) — both lanes now read one value.
const FLEE_RADIUS := GC.FLEE_RADIUS
const CATCH_RADIUS := GC.CATCH_RADIUS
const SCHOOL_RADIUS := GC.SCHOOL_RADIUS
const SEP_RADIUS := 3.0
const TRAIL_RADIUS := GC.TRAIL_RADIUS
const FATIGUE_DECAY := GC.FATIGUE_DECAY
const DRAG := GC.DRAG
const COAST_TIME := GC.COAST_TIME
const POP_CAP := 45
# R7: these were INLINE literals at the call sites until game.gd's BRAIN_*
# block grew into a line-by-line mirror of them — named + shared now so the
# mirror cannot drift from the math it mirrors.
const FLEE_PUSH := GC.FLEE_PUSH       # the flee accel magnitude (V6/Z14: 2.5 -> 6.0)
const WIGGLE := GC.WIGGLE             # dance amplitude
const TIRED := GC.TIRED               # the catch window opens above this fatigue
const TRAIL_DROP := GC.TRAIL_DROP     # pheromone drop threshold

# LM9 2026-09-30: positive-mode constants. FOOD_PULL is the game's own
# gentle steer (GC.POOL_PULL — no secret force advantage); FOOD_PREF_DIST
# rides the same prefer ring. The rest are the food/satiation law mirrored
# byte-for-byte in mag/flock_positive.py (the A/B harness instrument,
# value-pinned by tests/test_game_constants.py — flock-local, one .gd file).
const FOOD_PREF_DIST := GC.POOL_PREF_DIST  # stop pulling when near the patch (game.gd POOL_PREF_DIST shape)
const FOOD_PULL := GC.POOL_PULL            # px/s^2 attractor, scaled by hunger
const EAT_RADIUS := 10.0      # bite range at the patch
const EAT_RATE := 2.0         # food units per second while grazing
const SATIATION_GAIN := 0.15  # satiation per food unit eaten
const DIGEST_RATE := 0.04     # satiation per second spent not feeding
const EXPLORE_BASE := 0.4     # wiggle amplitude floor (hungry = focused)
const EXPLORE_SAT := 1.2      # extra wiggle amplitude at full satiation

var fish: Array[Dictionary] = []  # {pos, vel, fatigue, satiation, alive}
var trail: Array[Dictionary] = []  # {pos: Vector2, strength: float, life: float}
var trail_cap: int = 140
var rng := RandomNumberGenerator.new()
# LM9: positive mode (reward gradients) vs threat mode (flee/tire, default).
var positive := false
var food: Array[Dictionary] = []  # {pos: Vector2, amount: float}


func add_food(pos: Vector2, amount: float) -> void:
    food.append({"pos": pos, "amount": amount})


func add_fish(pos: Vector2) -> int:
    if fish.size() >= POP_CAP:
        return -1
    fish.append({"pos": pos, "vel": Vector2.ZERO, "fatigue": 0.0,
            "satiation": 0.0, "alive": true})
    return fish.size() - 1


## W1 fix 2026-09-29: step() leaked wall-clock time (the wiggle read
## Time.get_ticks_msec() at line 67), so two runs of the same inputs never
## matched and every paused frame distorted the school; the water graph is
## deterministic but the fish were not. sim_time is now a tick counter the
## caller accumulates (game.gd _process: sim_time += delta), making the
## wiggle a pure function of simulated time. Evidence: headless run after
## the fix parses clean and the wave's leak report names this exact line.
func step(player_pos: Vector2, delta: float, sim_time: float) -> void:
    var dt := delta
    for f in fish:
        if not f.alive:
            continue
        var to_player: Vector2 = player_pos - f.pos # B1.0 fix 2026-09-29: f.pos is Variant from Dictionary; := cannot infer
        var dist: float = to_player.length()

        # Steering: POSITIVE (LM9, food attracts) or THREAT (flee/tire).
        # The threat branch order is V6's, untouched.
        if positive and food.size() > 0:
            _step_food(f, dt)
        elif dist < FLEE_RADIUS and f.fatigue < 1.0:
            # Flee when close and not tired
            # Z14 2026-09-30: 2.5 -> 6.0 (GC.FLEE_PUSH). The old push reached
            # a terminal flee speed of only ~2.8 px/s under drag 0.985
            # (2.5 / (60 * 0.015)) — slower than a mouse cursor's slowest
            # approach, so there was zero chase tension (Z14 probe: "fish
            # flee at 2.7 px/s"). 6.0 terminals at ~6.7 px/s (~2.4x): fish
            # now actually escape a lazy cursor. Fatigue is untouched (still
            # dt/COAST_TIME), so the tire law holds: ~0.8s of cumulative
            # fleeing spends the fish and it coasts, catchable inside
            # CATCH_RADIUS once fatigue > TIRED (0.7).
            f.vel += -to_player.normalized() * FLEE_PUSH * dt
            f.fatigue = minf(f.fatigue + dt / COAST_TIME, 1.0)
        else:
            # Tire
            f.fatigue = maxf(f.fatigue - dt * FATIGUE_DECAY / COAST_TIME, 0.0)

        # Drag
        f.vel *= pow(DRAG, dt * 60.0)

        # School: cohesion + separation + wiggle
        var cohesion := Vector2.ZERO
        var separation := Vector2.ZERO
        var count := 0
        for other in fish:
            if other == f or not other.alive:
                continue
            var d: Vector2 = other.pos - f.pos
            var dl := d.length()
            if dl < SCHOOL_RADIUS:
                cohesion += d * 0.9
                if dl < SEP_RADIUS:
                    separation -= d.normalized() * 0.6 / maxf(dl, 0.1)
                count += 1
        if count > 0:
            f.vel += (cohesion / count * 0.55 + separation * 0.35) * dt
        # Wiggle: satiation-modulated in positive mode (LM9 explore-vs-exploit —
        # hungry fish exploit the gradient quietly, fed fish explore the patch),
        # the constant 0.05 law otherwise.
        var wiggle_amp := WIGGLE
        if positive and food.size() > 0:
            wiggle_amp = WIGGLE * (EXPLORE_BASE + EXPLORE_SAT * float(f.get("satiation", 0.0)))
        f.vel += Vector2(sin(sim_time * 7.0 + f.pos.x * 0.05), cos(sim_time * 7.0 + f.pos.y * 0.05)) * wiggle_amp * dt

        # Catch: player catches tired fish (the threat verb — no catch window
        # exists in positive mode: fatigue rests to 0 with nothing to spend it).
        if not positive and dist < CATCH_RADIUS and f.fatigue > TIRED:
            f.alive = false
            fish_killed.emit(fish.find(f))

        f.pos += f.vel * dt

    # Pheromone trail
    for f in fish:
        if f.alive and f.fatigue > TRAIL_DROP:
            trail.append({"pos": f.pos, "strength": f.fatigue, "life": f.fatigue * 5.0})
    # Decay and cap
    var alive_trail: Array[Dictionary] = []
    for t in trail:
        t.life -= dt
        if t.life > 0:
            alive_trail.append(t)
    trail = alive_trail
    if trail.size() > trail_cap:
        trail = trail.slice(trail.size() - trail_cap)


## LM9 2026-09-30: the positive steering branch — food ATTRACTS (reward, not
## threat). Mirror of mag/flock_positive.py step_positive() (the instrument):
## nearest active source; pull while beyond FOOD_PREF_DIST scaled by hunger
## (1 - satiation — EXPLOIT when hungry); bite inside EAT_RADIUS only while
## not full (a full fish does not bite: grazing cycles, not suction); digest
## otherwise; fatigue rests to 0 (nothing spends it — no panic state exists).
## Dictionaries are references: the bite decrements the source in `food`.
func _step_food(f: Dictionary, dt: float) -> void:
    var best := {}
    var best_d := INF
    for src in food:
        if float(src["amount"]) <= 0.0:
            continue
        var d: float = f.pos.distance_to(src["pos"])
        if d < best_d:
            best_d = d
            best = src
    var fed := false
    var sat := float(f.get("satiation", 0.0))
    if not best.is_empty():
        if best_d > FOOD_PREF_DIST:
            var hunger := 1.0 - sat
            var to_src: Vector2 = best["pos"] - f.pos
            if to_src.length() > 0.0:
                f.vel += to_src.normalized() * FOOD_PULL * hunger * dt
        elif best_d < EAT_RADIUS and sat < 1.0:
            var bite: float = minf(float(best["amount"]), EAT_RATE * dt)
            best["amount"] = float(best["amount"]) - bite
            f["satiation"] = minf(sat + bite * SATIATION_GAIN, 1.0)
            fed = bite > 0.0
    if not fed:
        f["satiation"] = maxf(float(f.get("satiation", 0.0)) - dt * DIGEST_RATE, 0.0)
    f.fatigue = maxf(f.fatigue - dt * FATIGUE_DECAY / COAST_TIME, 0.0)


func trail_steer(pos: Vector2) -> Vector2:
    var best_score := 1.2
    var best_dir := Vector2.ZERO
    for t in trail:
        var d: Vector2 = t.pos - pos
        var dist := d.length()
        if dist < TRAIL_RADIUS:
            var score: float = t.strength * (1.0 - dist / TRAIL_RADIUS)
            if score > best_score:
                best_score = score
                best_dir = d.normalized()
    return best_dir
