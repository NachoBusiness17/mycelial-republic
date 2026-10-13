--!strict
-- GalleryZone — "The Estate Gallery": the operator's static web gallery made
-- physical. One roof, three pedestals:
--   1. Isfahan Lattice — seeded Voronoi glass, ported from
--      dashboard/static/vislab/isfahan_lattice.html (12 named doors, seed
--      salt SEED*7919+104729, anisotropy dy*1.7 "tall panes like the arches").
--   2. Spore Fish — no render source found in-repo; built from the name plus
--      the monetization plan line. All its numbers are -- CLAIMED:.
--   3. Bad Apple Field — 1-bit flip rhythm ported from
--      dashboard/static/bad_apple_field.html (1200f @30fps, 96x72 1-bit).

local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local ledgerParent = script.Parent:FindFirstChild("ShadowLedger") and script.Parent or script.Parent.Parent
local ShadowLedger = require(ledgerParent:WaitForChild("ShadowLedger"))

local GalleryZone = {}
local origin = Vector3.new(0, 8, -260) -- south of Basecamp; ~184 from Ski/Arrakis, 260 from camp

-- the 12 named doors, verbatim from the Isfahan source (name, inscription, seed)
-- luau has no tuple types: rows carry named fields so name/inscription stay
-- string and seed stays number. Fix receipt: the old positional rows
-- {name, inscription, seed} made luau unify the row element to string and flag
-- each numeric seed as TypeError x7 (w2/lanes/a01-mountain.check.txt lines 26-32).
type Door = { name: string, inscription: string, seed: number }
	local DOORS: { Door } = {
	{ name = "the mirror toll", inscription = "your reflection holds the door you cannot wait at", seed = 11 },
	{ name = "two banks", inscription = "two banks of one river, never merged", seed = 7 },
	{ name = "the ninth law", inscription = "the world only moves when you move", seed = 9 },
	{ name = "the passing guard", inscription = "the sentry walks its line; cross behind its back", seed = 13 },
	{ name = "weight and shadow", inscription = "the treasure is load-bearing", seed = 21 },
	{ name = "the looking glass", inscription = "the reversed letter is watching you find it", seed = 3 },
	{ name = "the keeper", inscription = "he calls his own by name", seed = 17 },
	{ name = "the offered weight", inscription = "charcoal is free; nothing else is", seed = 23 },
	{ name = "the closing door", inscription = "the ledger constrains future accounts, not the past", seed = 29 },
	{ name = "the barbed junction", inscription = "speak only on the even breath", seed = 31 },
	{ name = "stroke order", inscription = "first the seal, then the wax, then the hand", seed = 37 },
	{ name = "the seventh watcher", inscription = "the wall was never evidence", seed = 41 },
}

-- annotation exactness (t42 triage, lanes/t42.check.txt row 12; cleared by t72 after t57 cleared rows 1-7 the same way): mk now returns Part, so the fields hold Part exactly; BasePart failed the exact-table literal check at 150,24/171,22/194,24. Runtime unchanged.
type Pane = { part: Part, u: number, v: number, ph: number }
type Fishie = { part: Part, radius: number, speed: number, phase: number, bob: number }
type Tile = { part: Part, phase: number, period: number, col: number, row: number }
local latticePt: { { u: number, v: number, hue: number, ph: number } } = {}

local panes: { Pane } = {}
local fish: { Fishie } = {}
local tiles: { Tile } = {}
local latticeLabel: TextLabel?
local doorIdx, clock, feedUntil = 1, 0, 0
local frameAcc, frame, playing = 0, -1, true
local TILE_ON, TILE_OFF = Color3.fromRGB(238, 240, 236), Color3.fromRGB(12, 12, 15)
local fishCenter = origin + Vector3.new(0, 4.5, 4)

-- annotation exactness (t42 triage, lanes/t42.check.txt row 12; cleared by t72 after t57 cleared rows 1-7 the same way): mk returns Instance.new("Part") (below); Part is what is stored, BasePart failed plaque's : Part return at 82,2. Runtime unchanged.
local function mk(parent: Instance, size: Vector3, pos: Vector3, color: Color3, mat: Enum.Material, collide: boolean?): Part
	local p = Instance.new("Part")
	p.Anchored = true
	p.Size = size
	p.Position = pos
	p.Color = color
	p.Material = mat
	p.CanCollide = collide == true
	p.Parent = parent
	return p
end

local function plaque(parent: Instance, text: string, pos: Vector3): Part
	local p = mk(parent, Vector3.new(5, 1.6, 0.3), pos, Color3.fromRGB(24, 22, 30), Enum.Material.Slate, true)
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Front
	gui.PixelsPerStud = 24
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.fromScale(1, 1)
	lbl.BackgroundTransparency = 1
	lbl.TextWrapped = true
	lbl.TextColor3 = Color3.fromRGB(220, 214, 190)
	lbl.Font = Enum.Font.Garamond
	lbl.TextSize = 12
	lbl.Text = text
	lbl.Parent = gui
	gui.Parent = p
	return p
end

local function banner(parent: Instance): TextLabel
	local gui = Instance.new("BillboardGui")
	gui.Size = UDim2.new(0, 260, 0, 64)
	gui.StudsOffset = Vector3.new(0, 3, 0)
	gui.AlwaysOnTop = true
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.fromScale(1, 1)
	lbl.BackgroundTransparency = 1
	lbl.TextWrapped = true
	lbl.TextColor3 = Color3.fromRGB(217, 164, 65) -- the source's inscription gold
	lbl.Font = Enum.Font.Garamond
	lbl.TextSize = 13
	lbl.Parent = gui
	gui.Parent = parent
	return lbl
end

local function prompt(parent: Instance, action: string, title: string, fn: (Player) -> ())
	local pr = Instance.new("ProximityPrompt")
	pr.ActionText = action
	pr.ObjectText = title
	pr.HoldDuration = 0.3
	pr.MaxActivationDistance = 10
	pr.Parent = parent
	pr.Triggered:Connect(fn)
end

-- re-seed the lattice from a named door and repaint every pane by Voronoi cell
local function seedDoor(idx: number)
	doorIdx = idx
	local door = DOORS[idx]
	local rng = SeedRng.new(door.seed * 7919 + 104729) -- same salt as the source
	latticePt = {}
	for _ = 1, 26 do -- 26 seeded points, as in the source
		table.insert(latticePt, { u = rng:next(), v = rng:next(), hue = rng:next(), ph = rng:next() * 6 })
	end
	for _, pane in ipairs(panes) do
		local best, bd = 1, math.huge
		for i, pt in ipairs(latticePt) do
			local dx, dy = pane.u - pt.u, pane.v - pt.v
			local d = dx * dx + dy * dy * 1.7 -- tall arches, per the source
			if d < bd then
				bd, best = d, i
			end
		end
		local pt = latticePt[best]
		local hue = Color3.fromHSV(pt.hue, 0.65 + 0.2 * pt.hue, 0.5 + 0.2 * pt.hue)
		pane.part.Color = hue
		pane.ph = pt.ph
	end
	if latticeLabel then
		latticeLabel.Text = string.format('ISFAHAN LATTICE — seed %d · "%s"\n"%s"', door.seed, door.name, door.inscription)
	end
end

local function buildLattice(model: Instance)
	local wall = mk(model, Vector3.new(0.6, 12.4, 20.4), origin + Vector3.new(-22, 6.2, -6), Color3.fromRGB(20, 18, 24), Enum.Material.Marble, true)
	plaque(model, "Isfahan Lattice", origin + Vector3.new(-22, 0.4, 6.4))
	latticeLabel = banner(wall)
	local cols, rows = 9, 6
	for c = 1, cols do
		for r = 1, rows do
			local pane = mk(model, Vector3.new(1.9, 1.9, 0.25), Vector3.zero, Color3.new(1, 1, 1), Enum.Material.Glass, false)
			pane.Transparency = 0.35
			table.insert(panes, {
				part = pane,
				ph = 0,
				u = (c - 0.5) / cols,
				v = (r - 0.5) / rows,
			})
		end
	end
	seedDoor(1)
	prompt(wall, "Walk the doors", "Isfahan Lattice", function(player: Player)
		seedDoor(doorIdx % #DOORS + 1)
		ShadowLedger.record(player, "Gallery", "walked a lattice door", true)
	end)
end

local function buildFish(model: Instance)
	local basin = mk(model, Vector3.new(14, 1, 14), origin + Vector3.new(0, 0.5, 4), Color3.fromRGB(24, 34, 40), Enum.Material.Glass, true)
	mk(model, Vector3.new(2, 2, 2), origin + Vector3.new(0, 1.5, 4), Color3.fromRGB(38, 34, 46), Enum.Material.Marble, true) -- pedestal
	local rng = SeedRng.new(20260924)
	for _ = 1, 13 do -- CLAIMED: school of 13 spore-fish
		local f = mk(model, Vector3.new(1.1, 1.1, 1.1), fishCenter, Color3.fromHSV(rng:next() * 0.25 + 0.35, 0.7, 0.85), Enum.Material.Neon, false)
		table.insert(fish, {
			part = f,
			radius = 3 + rng:next() * 4.5, -- CLAIMED: orbit radii 3–7.5 studs
			speed = 0.5 + rng:next() * 0.9, -- CLAIMED: angular speed rad/s
			phase = rng:next() * math.pi * 2,
			bob = 0.4 + rng:next() * 0.8, -- CLAIMED: bob amplitude
		})
	end
	local label = banner(basin)
	label.Text = "SPORE FISH\nthey keep the circle; feeding scatters it"
	prompt(basin, "Feed", "Spore Fish", function(player: Player)
		feedUntil = clock + 4 -- CLAIMED: frenzy lasts 4s
		ShadowLedger.record(player, "Gallery", "fed the spore fish", true)
	end)
end

local function buildBadApple(model: Instance)
	local screen = mk(model, Vector3.new(22.4, 16.4, 0.6), origin + Vector3.new(22, 8.2, -6), Color3.fromRGB(18, 16, 20), Enum.Material.Metal, true)
	local rng = SeedRng.new(41800)
	local cols, rows = 12, 8 -- 96 tiles standing in for the 96x72 1-bit source
	for c = 1, cols do
		for r = 1, rows do
			local t = mk(model, Vector3.new(1.5, 1.5, 0.2), Vector3.zero, TILE_OFF, Enum.Material.SmoothPlastic, false)
			table.insert(tiles, {
				part = t,
				phase = rng:int(0, 1),
				period = 2 + rng:int(0, 3), -- CLAIMED: per-tile flip cadence 2–5 frames
				col = (c - 0.5) / cols,
				row = (r - 0.5) / rows,
			})
		end
	end
	local label = banner(screen)
	label.Text = "BAD APPLE FIELD\nthe field flips in rhythm; pause to hold a frame"
	prompt(screen, "Pause / resume", "Bad Apple Field", function(player: Player)
		playing = not playing
		ShadowLedger.record(player, "Gallery", playing and "resumed the field" or "held a frame", true)
	end)
end

function GalleryZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "EstateGallery"

	mk(model, Vector3.new(72, 1, 30), origin + Vector3.new(0, -0.5, 0), Color3.fromRGB(30, 28, 36), Enum.Material.Marble, true) -- floor
	mk(model, Vector3.new(72, 18, 1), origin + Vector3.new(0, 9, -16.5), Color3.fromRGB(34, 31, 40), Enum.Material.Marble, true) -- back wall
	mk(model, Vector3.new(72, 0.6, 30), origin + Vector3.new(0, 13, 0), Color3.fromRGB(26, 24, 32), Enum.Material.Slate, false) -- roof
	plaque(model, "THE ESTATE GALLERY\nthe static gallery, made physical — FIND · FILE · LOAD", origin + Vector3.new(0, 0.4, 13.6))

	buildLattice(model)
	buildFish(model)
	buildBadApple(model)

	model.Parent = workspace

	for _, p in ipairs(panes) do -- lay the glass grid onto its wall
		p.part.Position = origin + Vector3.new(-22 + (p.u - 0.5) * 18, 2.6 + p.v * 11, -5.55)
	end
	for _, t in ipairs(tiles) do -- lay the field onto its screen
		t.part.Position = origin + Vector3.new(22 + (t.col - 0.5) * 18, 2.6 + t.row * 13, -5.55)
	end
	return model
end

function GalleryZone.tick(dt: number)
	clock += dt
	-- Isfahan: the sun sweeps and the light through the law moves with it
	local a = clock * 0.12
	for _, pane in ipairs(panes) do
		pane.part.Transparency = 0.18 + 0.44 * (0.5 + 0.5 * math.sin(a + pane.ph))
	end
	-- Spore Fish: keep the circle; the feed scatters it wide and fast
	local fed = clock < feedUntil
	local spread, rush = fed and 1.8 or 1, fed and 1.6 or 1 -- CLAIMED: scatter x1.8, frenzy speed x1.6
	for _, f in ipairs(fish) do
		local ang = clock * f.speed * rush + f.phase
		local r = f.radius * spread
		f.part.Position = fishCenter + Vector3.new(math.cos(ang) * r, math.sin(clock * 2 + f.phase) * f.bob, math.sin(ang) * r * 0.6)
	end
	-- Bad Apple: the field flips at 30fps like the source's 1200f @30fps
	if playing then
		frameAcc += dt * 30
		local nf = math.floor(frameAcc)
		if nf ~= frame then
			frame = nf
			for _, t in ipairs(tiles) do
				local on = (math.floor(frame / t.period) + t.phase) % 2 == 0
				t.part.Color = on and TILE_ON or TILE_OFF
				t.part.Material = on and Enum.Material.Neon or Enum.Material.SmoothPlastic
			end
		end
	end
end

return GalleryZone
