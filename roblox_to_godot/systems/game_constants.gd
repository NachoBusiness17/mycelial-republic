extends RefCounted
## GameConstants — the single source of truth for every constant shared by
## two or more scripts (Q15 / V2ASK3, R7 2026-09-30).
##
## LAW (the drift this file kills): before R7 the same gameplay value lived
## in up to four places — flock.gd FLEE_RADIUS 20 (Z14/V6 tuning) vs
## fish_brain.gd 14 (the stale pre-V6 mirror, V6_FISH_FLEE.md's named
## handoff) vs tools/mountain_units.py 14 (rode fish_brain) vs
## mag/flock_positive.py 20 (rode flock) — and game.gd's BRAIN_* block
## mirrored flock.gd's INLINE literals line-by-line. Every retune had to be
## hand-copied to each twin; V6 proved the failure mode (one twin missed,
## the brain path triggered flee at 14px while the fallback used 20). Now
## every consumer preloads this file and aliases
## (`const FLEE_RADIUS := GC.FLEE_RADIUS`), and
## tests/test_game_constants.py fails on any raw literal const of a
## registered name outside this file — the drift can never recur silently.
##
## FORM (V2ASK3 verdict, watch/inbox/frontier_asks/volley2/results/V2ASK3.md
## Q15): a const leaf — NOT an autoload. Autoloads are runtime nodes for
## mutable state; invariants belong in consts usable inside const
## expressions. The judgment's class_name form is narrowed to preload here:
## this estate runs the headless binary with no editor pass, so the global
## script-class cache would never regenerate — a preload path resolves at
## parse time with zero cache dependency. This file depends on nothing (a
## leaf cannot cycle).
##
## OWNERSHIP OF VALUES: each block cites the receipt that last moved it.
## Changing a value here retunes every consumer in the same parse — one
## edit, one truth. tests/test_game_constants.py pins the current values;
## a deliberate retune updates the pin in the same commit (receipt law).

# --- the flock/fish family ---------------------------------------------------
# Consumers: systems/flock.gd (steering), systems/fish_brain.gd (policy),
# scripts/game.gd (the Z7 rig's BRAIN_* mirrors), systems/water_particles.gd
# (DRAG). The Python twins (mag/flock_positive.py, tools/mountain_units.py)
# are pinned to these values by tests/test_game_constants.py (parsed, not
# imported — no runtime coupling).
const FLEE_RADIUS := 20.0      # V6/Z14 2026-09-30: 14 -> 20 — at flee push 6.0 (~6.7 px/s terminal) 14px shrank the cursor-warning window; 20 restores it. fish_brain.gd rode the stale 14 until R7 trued it up (V6_FISH_FLEE.md handoff).
const CATCH_RADIUS := 3.5      # the tired window is catchable — the player's verb
const SCHOOL_RADIUS := 20.0    # dance needs schoolmates
const TRAIL_RADIUS := 38.0     # pursue urgency normalizer
const TIRED := 0.7             # fatigue >= this: the catch window opens / carried
const TRAIL_DROP := 0.5        # fatigue > this: a pheromone trail entry drops
const FLEE_PUSH := 6.0         # V6/Z14: 2.5 -> 6.0 — flee accel magnitude; terminal ~6.7 px/s under DRAG
const WIGGLE := 0.05           # dance amplitude (the constant law; positive mode scales it)
const FATIGUE_DECAY := 0.4     # rest rate
const DRAG := 0.985            # vel *= pow(DRAG, dt * 60) — the flock + water_particles idiom
const COAST_TIME := 0.8        # ~0.8s of cumulative fleeing spends the fish
const POOL_PREF_DIST := 30.0   # the pursue/pull ring around its target (pool, or food patch — LM9: same value, no secret force advantage)
const POOL_PULL := 22.0        # Z14: 10 -> 22 — gentle steer accel toward the wettest pool (~24 px/s terminal drift)

# --- the win/mode family (scripts/game.gd, scripts/hud.gd) --------------------
const WIN_CROWN := 4           # crowns to win; hud.gd CROWN_GOAL is this same denominator
const MODE_PROBING := 0        # game.gd `enum Mode { PROBING, AUTHORITATIVE,
const MODE_AUTHORITATIVE := 1  # SOVEREIGN }` — the guard test pins the enum
const MODE_SOVEREIGN := 2      # order to these values. title.gd's DOOR_* are a different domain (door lanes, not game modes).

# --- the net family (scripts/game.gd, scenes/title.gd) ------------------------
const NET_HOST := "127.0.0.1"
const NET_PORT := 8800
const NET_DEFAULT_ENDPOINT := "127.0.0.1:8800"  # == NET_HOST:NET_PORT (guard-pinned; title.gd DEFAULT_ENDPOINT aliases this)

# --- the UI family (scripts/hud.gd, scenes/title.gd, scripts/juice.gd) --------
const VIEW := Vector2(1152.0, 648.0)  # project.godot viewport (window/size)
const PANEL_BG := Color(0.04, 0.05, 0.07, 0.62)
const PANEL_EDGE := Color(0.55, 0.62, 0.7, 0.28)
const TEXT_DIM := Color(0.6, 0.65, 0.7)
const TEXT_MAIN := Color(0.85, 0.88, 0.92)
const GOLD := Color(0.95, 0.8, 0.35)
const SOVEREIGN_COL := Color(0.55, 0.85, 0.8)
const AUTH_COL := Color(0.9, 0.75, 0.4)
