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
