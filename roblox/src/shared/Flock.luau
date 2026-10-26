--!strict
-- Flock — the living-crop boids engine ported from dashboard/static/games/swarm.html
-- (Q-032). The source's own thesis: "the crop is ALIVE — XP is a spore fish, and it
-- flees ... the header catches the tired ones" (swarm.html:949-950). Three laws,
-- each carried from its exact source lines:
--
--   1. FLEE / TIRE / REST  (swarm.html:951-968) — an airborne fish flees the player
--      inside the flee radius, accelerating away at max(minSpeed, baseSpeed −
--      fatigue·slope), the same speed scalar pushed ×6 on the plane and ×4 on the
--      height axis; it accumulates `flee` fatigue, then when the player is out of
--      range it coasts (fleeT lingers 0.8s with drag but no gravity), then it TIRES:
--      fatigue decays by 0.4^dt and gravity pulls it down. Floor contact flips it
--      to rest. Drag 0.985 per source frame, frame-normalized as 0.985^(60·dt).
--      Arena walls bounce at half restitution (the source's x-walls at 8 / WW−8,
--      generalized to the port's two horizontal axes).
--   2. SCHOOL (swarm.html:970-981, the boids core) — a RESTING fish is steered by
--      direct position nudges only, never velocity: cohesion toward the centroid of
--      neighbors inside the school radius (rate 0.9 on the plane, 0.55 on height),
--      separation from neighbors inside the separation radius (rate 0.6 / 0.35),
--      plus the identity wiggle sin(t·7 + x·0.05)·amp·dt along world X, then the
--      floor clamp. The source's floor clamp `g.y > floor → g.y = floor` grows on a
--      down-positive canvas axis; here Y is up, so the clamp is `Y < floorY`.
--   3. PHEROMONE TRAIL (steering law swarm.html:842-851, drop law :1113-1121) — the
--      horde steers at the freshest trail point whose score life·(1 − manhattan/
--      radius) beats the floor 1.2, else straight at the player. Walking drops
--      points with life 2.5; the loud action (source: the harvest header; port: the
--      Fire pellet) drops life 5. Cap 140 points, drop interval 0.15s.
--
-- Scale law (the one port mapping, recorded in roblox/docs/CLONED_MECHANICS.md
-- §3.7): the source runs on a 2400-wide canvas with a 200-unit/s skater; this port
-- has a 90-stud arena and a 16 studs/s walk. Speeds scale ×0.08 (the player ratio;
-- gravity and the toss inherit it). Lengths are tuned inside that envelope to stay
-- playable: flee 95→14, catch 15→3.5 (the port's existing touch-collect radius),
-- school 155→20, separation 15→3, trail radius 300→38, wiggle amp 6→1.5. Rates,
-- thresholds, lives, the 1.2 score floor, the drag, and the 0.4^dt fatigue decay
-- carry over verbatim. NOT cloned here: the harvest-header row, the county-line
-- survey, and THE FISH boss duel (45 stays a population cap, not a spawn trigger) —
-- separate mechanics, open moves.
--
-- Pure module: no Instances, no services. A host with only a Vector3 stub (`.new`,
-- `+ - * /`, `Magnitude`, `Unit`) can execute every function, which is what the
-- banked check script does.

local Flock = {}

-- scale factors (see header)
local SPEED_SCALE = 0.08 -- the source skater 200 u/s -> the port walk 16 studs/s

-- flee / tire / rest (swarm.html:951-968; orig values in comments)
local FLEE_RADIUS = 14 -- orig 95
local FLEE_RADIUS_RAIN = 10 -- orig 68 (braver in rain); keeps the 68/95 ratio
local FLEE_SPEED = 26 -- orig 320 x SPEED_SCALE
local FLEE_SPEED_MIN = 11 -- orig 140 x SPEED_SCALE
local FLEE_FATIGUE_SLOPE = 160 * SPEED_SCALE -- orig 160
local FLEE_PLANE_PUSH = 6 -- verbatim: horizontal share of the speed scalar
local FLEE_HEIGHT_PUSH = 4 -- verbatim: vertical share
local FLEE_COAST = 0.8 -- verbatim: fleeT linger before the tire branch
local FATIGUE_DECAY = 0.4 -- verbatim: fatigue *= 0.4^dt while tiring
local GRAVITY = 140 * SPEED_SCALE -- orig 140 (tire branch only)
local DRAG = 0.985 -- verbatim, per 1/60s source frame
local WALL_BOUNCE = 0.5 -- verbatim

-- school (swarm.html:970-981)
local SCHOOL_RADIUS = 20 -- orig 155 (24025 = 155^2)
local COHESION_PLANE = 0.9 -- verbatim
local COHESION_HEIGHT = 0.55 -- verbatim
local SEPARATION_RADIUS = 3 -- orig 15 (225 = 15^2)
local SEPARATION_PLANE = 0.6 -- verbatim
local SEPARATION_HEIGHT = 0.35 -- verbatim
local WIGGLE_FREQ = 7 -- verbatim
local WIGGLE_SPACE = 0.05 -- verbatim
local WIGGLE_AMP = 1.5 -- orig 6

-- pheromone trail (swarm.html:842-851 + :1113-1121)
local TRAIL_RADIUS = 38 -- orig 300 (manhattan)
local TRAIL_SCORE_FLOOR = 1.2 -- verbatim
local TRAIL_LIFE_WALK = 2.5 -- verbatim
local TRAIL_LIFE_LOUD = 5 -- verbatim (source: harvest; port: Fire pellet)
local TRAIL_DROP_INTERVAL = 0.15 -- verbatim
local TRAIL_CAP = 140 -- verbatim

-- crop loop (swarm.html:631 toss, :1074 stir warn, :1091 gem ceiling)
local TOSS_SPEED = 46 * SPEED_SCALE -- orig rnd(-46, 46) horizontal
local TOSS_UP_MIN = 10 * SPEED_SCALE -- orig rnd(-90, -10) upward
local TOSS_UP_MAX = 90 * SPEED_SCALE
local STIR_AT = 30 -- verbatim warn threshold
local POP_CAP = 45 -- orig 200 ceiling; here the pre-boss population law
local CATCH_RADIUS = 3.5 -- orig 15 -> the port's existing touch-collect radius

export type Fish = {
	pos: Vector3,
	vel: Vector3,
	rest: boolean,
	flee: number,
	fleeT: number,
}

export type Bounds = {
	minX: number,
	maxX: number,
	minZ: number,
	maxZ: number,
	floorY: number,
}

export type TrailPoint = {
	pos: Vector3,
	life: number,
}

export type Trail = {
	points: { TrailPoint },
	cap: number,
}

function Flock.newFish(pos: Vector3, toss: Vector3?): Fish
	if toss then
		return { pos = pos, vel = toss, rest = false, flee = 0, fleeT = 0 }
	end
	return { pos = pos, vel = Vector3.zero, rest = true, flee = 0, fleeT = 0 }
end

-- the kill-drop toss (swarm.html:631 `vx:rnd(-46,46), vy:rnd(-90,-10)`), scaled;
-- the source tosses on one horizontal axis, the port across the full plane
function Flock.toss(rng: (() -> number)?): Vector3
	-- branch instead of `rng or math.random`: calling a union of function
	-- types is a TypeError under the strict analyzer
	local function draw(): number
		if rng then
			return rng()
		end
		return math.random()
	end
	local ang = draw() * math.pi * 2
	local mag = draw() * TOSS_SPEED
	local up = TOSS_UP_MIN + draw() * (TOSS_UP_MAX - TOSS_UP_MIN)
	return Vector3.new(math.cos(ang) * mag, up, math.sin(ang) * mag)
end

-- flee / tire / rest for one airborne fish (swarm.html:951-968). Mutates `f`.
-- `raining` keeps the source's braver-in-rain radius (the port passes false;
-- the zone has no weather yet — the parameter keeps the law in the module).
function Flock.fleeStep(f: Fish, playerPos: Vector3, dt: number, raining: boolean, bounds: Bounds)
	local delta = f.pos - playerPos
	local d = delta.Magnitude
	local fleeR = if raining then FLEE_RADIUS_RAIN else FLEE_RADIUS
	if d < fleeR and d > 0.01 then
		-- the fish darts (braver in rain)
		f.flee += dt
		f.fleeT = FLEE_COAST
		local sp = math.max(FLEE_SPEED_MIN, FLEE_SPEED - f.flee * FLEE_FATIGUE_SLOPE)
		local away = delta / d
		f.vel += Vector3.new(
			away.X * sp * FLEE_PLANE_PUSH * dt,
			away.Y * sp * FLEE_HEIGHT_PUSH * dt,
			away.Z * sp * FLEE_PLANE_PUSH * dt
		)
	elseif f.fleeT > 0 then
		f.fleeT -= dt
	else
		-- it tires
		f.flee *= FATIGUE_DECAY ^ dt
		f.vel -= Vector3.new(0, GRAVITY * dt, 0)
	end
	-- drag (source 0.985/frame; frame-normalized), integrate
	local drag = DRAG ^ (dt * 60)
	f.vel *= drag
	f.pos += f.vel * dt
	-- arena walls bounce at half restitution (source x-walls generalized to Z)
	if f.pos.X < bounds.minX then
		f.pos = Vector3.new(bounds.minX, f.pos.Y, f.pos.Z)
		f.vel = Vector3.new(math.abs(f.vel.X) * WALL_BOUNCE, f.vel.Y, f.vel.Z)
	elseif f.pos.X > bounds.maxX then
		f.pos = Vector3.new(bounds.maxX, f.pos.Y, f.pos.Z)
		f.vel = Vector3.new(-math.abs(f.vel.X) * WALL_BOUNCE, f.vel.Y, f.vel.Z)
	end
	if f.pos.Z < bounds.minZ then
		f.pos = Vector3.new(f.pos.X, f.pos.Y, bounds.minZ)
		f.vel = Vector3.new(f.vel.X, f.vel.Y, math.abs(f.vel.Z) * WALL_BOUNCE)
	elseif f.pos.Z > bounds.maxZ then
		f.pos = Vector3.new(f.pos.X, f.pos.Y, bounds.maxZ)
		f.vel = Vector3.new(f.vel.X, f.vel.Y, -math.abs(f.vel.Z) * WALL_BOUNCE)
	end
	-- floor contact -> rest (source: vx *= 0.6 damp, vy = 0, rest)
	if f.pos.Y <= bounds.floorY then
		f.pos = Vector3.new(f.pos.X, bounds.floorY, f.pos.Z)
		f.vel = Vector3.new(f.vel.X * 0.6, 0, f.vel.Z * 0.6)
		f.rest = true
	end
end

-- the boids school for one RESTED fish (swarm.html:970-981). Position nudges only;
-- neighbors include airborne fish, exactly like the source's global gems loop.
-- `t` is zone time (source T), `floorY` the rest height (source gyAt(x) − 6).
function Flock.schoolStep(f: Fish, school: { Fish }, t: number, dt: number, floorY: number)
	local cx, cy, cz, cn = 0, 0, 0, 0
	for _, o in school do
		if o == f then
			continue
		end
		local delta = o.pos - f.pos
		local d2 = delta.X * delta.X + delta.Y * delta.Y + delta.Z * delta.Z
		if d2 < SCHOOL_RADIUS * SCHOOL_RADIUS then
			cx += o.pos.X
			cy += o.pos.Y
			cz += o.pos.Z
			cn += 1
			if d2 < SEPARATION_RADIUS * SEPARATION_RADIUS then
				f.pos -= Vector3.new(
					delta.X * SEPARATION_PLANE * dt,
					delta.Y * SEPARATION_HEIGHT * dt,
					delta.Z * SEPARATION_PLANE * dt
				)
			end
		end
	end
	if cn > 0 then
		f.pos += Vector3.new(
			(cx / cn - f.pos.X) * COHESION_PLANE * dt,
			(cy / cn - f.pos.Y) * COHESION_HEIGHT * dt,
			(cz / cn - f.pos.Z) * COHESION_PLANE * dt
		)
	end
	-- the identity wiggle, along world X like the source's only horizontal axis
	f.pos += Vector3.new(math.sin(t * WIGGLE_FREQ + f.pos.X * WIGGLE_SPACE) * WIGGLE_AMP * dt, 0, 0)
	-- floor clamp (canvas-y down in the source, Y up here: the comparison flips)
	if f.pos.Y < floorY then
		f.pos = Vector3.new(f.pos.X, floorY, f.pos.Z)
	end
end

-- the source's catch law for airborne fish (swarm.html:968 `if(d0<15)`); the zone
-- applies its own collect radii on top (touch 3.5, pet orb 12)
function Flock.caught(f: Fish, playerPos: Vector3): boolean
	return (f.pos - playerPos).Magnitude < CATCH_RADIUS
end

function Flock.loudTrailLife(loud: boolean): number
	return if loud then TRAIL_LIFE_LOUD else TRAIL_LIFE_WALK
end

Flock.TRAIL_DROP_INTERVAL = TRAIL_DROP_INTERVAL
Flock.TRAIL_CAP = TRAIL_CAP
Flock.STIR_AT = STIR_AT
Flock.POP_CAP = POP_CAP

-- ---- the pheromone trail (plain-table state + free functions: strict-clean
-- without metatable typing, and executable against a bare Vector3 stub) ----

function Flock.trailNew(cap: number?): Trail
	return { points = {}, cap = cap or TRAIL_CAP }
end

-- drop one point (source: push + shift past the cap, swarm.html:1115-1118)
function Flock.trailDrop(trail: Trail, pos: Vector3, life: number)
	table.insert(trail.points, { pos = pos, life = life })
	while #trail.points > trail.cap do
		table.remove(trail.points, 1)
	end
end

-- age the trail (source: life -= dt, filter at 0, swarm.html:1120-1121)
function Flock.trailStep(trail: Trail, dt: number)
	local alive: { TrailPoint } = {}
	for _, p in trail.points do
		p.life -= dt
		if p.life > 0 then
			table.insert(alive, p)
		end
	end
	trail.points = alive
end

-- best fresh score at a position (swarm.html:845-850: manhattan radius, score
-- life·(1 − d/radius)); returns the score and the point, or nil
function Flock.trailBest(trail: Trail, pos: Vector3): (number, TrailPoint?)
	local bestScore, bestPoint = 0, nil :: TrailPoint?
	for _, p in trail.points do
		local d = math.abs(p.pos.X - pos.X) + math.abs(p.pos.Y - pos.Y) + math.abs(p.pos.Z - pos.Z)
		if d < TRAIL_RADIUS then
			local s = p.life * (1 - d / TRAIL_RADIUS)
			if s > bestScore then
				bestScore = s
				bestPoint = p
			end
		end
	end
	return bestScore, bestPoint
end

-- the steering law (swarm.html:842-851): the trail pulls when it is fresher than
-- the score floor, else the horde walks straight at the player. Returns a unit
-- direction, or the zero vector when both targets coincide with the asker.
function Flock.trailSteer(trail: Trail, pos: Vector3, playerPos: Vector3): Vector3
	local score, point = Flock.trailBest(trail, pos)
	local target = if score > TRAIL_SCORE_FLOOR and point then point.pos else playerPos
	local delta = target - pos
	if delta.Magnitude < 1e-4 then
		return Vector3.zero
	end
	return delta.Unit
end

return Flock
