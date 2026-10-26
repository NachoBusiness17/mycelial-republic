-- Q-043 executable check: SectionStream ordering/budget/one-shot/radius
-- semantics, run on tools/bin/luau/luau.exe against the REAL module source
-- (loaded below), with a minimal Vector3 stub (the module only needs
-- .new/.Magnitude and vector sub; the game's Vector3 is the Roblox runtime's).
local function v3new(x, y, z)
	local t = { X = x, Y = y, Z = z }
	t.Magnitude = math.sqrt(x * x + y * y + z * z)
	return setmetatable(t, {
		__sub = function(a, b) return v3new(a.X - b.X, a.Y - b.Y, a.Z - b.Z) end,
		__add = function(a, b) return v3new(a.X + b.X, a.Y + b.Y, a.Z + b.Z) end,
	})
end
Vector3 = { new = v3new }

local SectionStream = (function()
--!strict
-- SectionStream — the GnomeCode ep.1 streamed-sections pattern (Doors: the
-- world materializes ahead of the walker instead of all at boot; ADOPT move 1
-- of docs/ARCHITECTURE_NEXT.md). A stream holds sections, each a one-shot
-- build closure plus a center; poll(positions) builds every unbuilt section
-- whose center sits within `radius` of any position, at most `budget` builds
-- per poll so a neighborhood manifests across frames instead of spiking one.
--
-- ordered = true builds STRICTLY in insertion order: a section never builds
-- before its predecessors even when its own radius trips first. Maze builds
-- whose closures draw from one shared SeedRng stream must use this mode —
-- insertion order then equals rng draw order, so a streamed world is
-- byte-identical to the eager one, only later in time (the Ossuary floors
-- ride one SeedRng(20261031); the per-floor draw counts are unchanged, so
-- every corridor, sentinel, lever and brazier lands where it always did).
--
-- Consumed by OssuaryZone (stacked floors, ordered) and RiddleMazeZone (wall
-- chunks, proximity). Judged too small to stream: SpectralMazeZone (7 doors,
-- 1 hall part) and MazeArenaZone (10 fixed walls) build in microseconds.

export type Section = {
	center: Vector3,
	build: () -> (),
	done: boolean,
}

export type SectionStream = {
	add: (self: SectionStream, center: Vector3, build: () -> ()) -> (),
	poll: (self: SectionStream, positions: { Vector3 }) -> number,
	pending: (self: SectionStream) -> number,
}

export type StreamConfig = {
	radius: number,
	budget: number?,
	ordered: boolean?,
}

local SectionStream = {}
SectionStream.__index = SectionStream

-- ordered-mode gate: a section may build only once every earlier-registered
-- section has built (insertion order = rng draw order for seeded builds)
local function predecessorsDone(sections: { Section }, sec: Section): boolean
	for _, other in ipairs(sections) do
		if other == sec then
			return true -- walked insertion order up to sec: everything before is done
		end
		if not other.done then
			return false
		end
	end
	return true
end

function SectionStream.new(cfg: StreamConfig): SectionStream
	local self = setmetatable({
		_radius = cfg.radius,
		_budget = cfg.budget or math.huge,
		_ordered = cfg.ordered == true,
		_sections = {} :: { Section },
	}, SectionStream)
	return (self :: any) :: SectionStream
end

function SectionStream:add(center: Vector3, build: () -> ())
	table.insert(self._sections :: { Section }, { center = center, build = build, done = false })
end

function SectionStream:poll(positions: { Vector3 }): number
	local sections = self._sections :: { Section }
	local budget = self._budget :: number
	local radius = self._radius :: number
	local built = 0
	for _, sec in ipairs(sections) do
		if built >= budget then
			break
		end
		if not sec.done and (not self._ordered or predecessorsDone(sections, sec)) then
			for _, pos in ipairs(positions) do
				if (pos - sec.center).Magnitude <= radius then
					sec.done = true
					sec.build()
					built += 1
					break
				end
			end
		end
	end
	return built
end

function SectionStream:pending(): number
	local n = 0
	for _, sec in ipairs(self._sections :: { Section }) do
		if not sec.done then
			n += 1
		end
	end
	return n
end

return SectionStream
end)()

local failures = 0
local function check(name, cond)
	if cond then
		print("PASS " .. name)
	else
		failures += 1
		print("FAIL " .. name)
	end
end

-- 1. ordered mode: insertion order wins even when the poll stands on the
-- LAST section's center (the Ossuary claim: rng draw order preserved)
local order = {}
local names = { "A", "B", "C" }
local s1 = SectionStream.new({ radius = 100, budget = 1, ordered = true })
for i, name in ipairs(names) do
	s1:add(Vector3.new(i * 10, 0, 0), function() table.insert(order, name) end)
end
check("ordered: nothing builds far away", s1:poll({ Vector3.new(1000, 0, 0) }) == 0)
check("ordered: standing on C builds A first", s1:poll({ Vector3.new(30, 0, 0) }) == 1 and order[1] == "A")
check("ordered: second poll builds B", s1:poll({ Vector3.new(30, 0, 0) }) == 1 and order[2] == "B")
check("ordered: third poll builds C", s1:poll({ Vector3.new(30, 0, 0) }) == 1 and order[3] == "C")
check("ordered: draw order == insertion order", table.concat(order, ",") == "A,B,C")
check("ordered: sections are one-shot", s1:poll({ Vector3.new(30, 0, 0) }) == 0 and #order == 3)
check("pending drains to zero", s1:pending() == 0)

-- 2. budget caps builds per poll
local built2 = 0
local s2 = SectionStream.new({ radius = 100, budget = 2, ordered = false })
for i = 1, 4 do
	s2:add(Vector3.new(i, 0, 0), function() built2 += 1 end)
end
check("budget: first poll builds exactly 2", s2:poll({ Vector3.new(2, 0, 0) }) == 2)
check("budget: second poll builds the rest", s2:poll({ Vector3.new(2, 0, 0) }) == 2 and built2 == 4)

-- 3. radius gates a section entirely
local hit = false
local s3 = SectionStream.new({ radius = 50, ordered = false })
s3:add(Vector3.new(200, 0, 0), function() hit = true end)
check("radius: out-of-range section never builds", s3:poll({ Vector3.new(0, 0, 0) }) == 0 and not hit)

-- 4. unordered mode builds the in-range section regardless of predecessors
-- (the RiddleMaze mode: wall chunks carry no rng order)
local hits = {}
local s4 = SectionStream.new({ radius = 100, ordered = false })
s4:add(Vector3.new(0, 0, 0), function() table.insert(hits, "A") end)
s4:add(Vector3.new(5, 0, 0), function() table.insert(hits, "B") end)
s4:add(Vector3.new(1000, 0, 0), function() table.insert(hits, "C") end)
s4:poll({ Vector3.new(5, 0, 0) })
check("unordered: in-range build, out-of-range skipped", hits[1] == "A" and hits[2] == "B" and #hits == 2)

-- 5. multiple poll positions (several players) all count
local got = false
local s5 = SectionStream.new({ radius = 10, ordered = false })
s5:add(Vector3.new(100, 0, 0), function() got = true end)
check("multi-position: second player's position triggers", s5:poll({ Vector3.new(0, 0, 0), Vector3.new(95, 0, 0) }) == 1 and got)

if failures == 0 then
	print("ALL CHECKS PASS")
else
	print(("FAILURES: %d"):format(failures))
	error("check failed")
end
