--!strict
-- SteerFieldZone — translated from dashboard/static/steer_field.html ("THE FILM").
-- The film's truth is a summed radial falloff per light: v = (1-d/rad)^1.6 * I,
-- rad = 170*I + 40, in the lane color. Six dumb sagents (walkers) sample 8
-- directions each 66 ms step (wobble sin(t+i)*0.3, step 3.2 px) and climb the
-- intensity gradient, bouncing off the four failure pillars. You write on the
-- film by carrying a lamp (source law: "steer the interior by writing on the
-- film"): raise it at the dimmer and walkers steer toward YOU; a walker that
-- reaches your lamp banks credit and re-seats on the rim.
local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local SteerFieldZone = {}
local origin = Vector3.new(-400, 8, -110)
local STUD = 0.25 -- source film is 960x600 px -> 240x150 studs
local T_STEP = 0.066 -- source draw/step interval
local BANK_DIST, BANK_PAY = 20, 25 -- CLAIMED: lamp reach px + payout (port mechanic)
local simT, stepAcc, tileClock = 0, 0, 0

local LIGHTS = { -- { x, y, intensity, r, g, b } — the 7 contracted engines, exact
	{ 140, 90, 0.10, 255, 179, 71 }, { 420, 80, 0.43, 255, 179, 71 }, -- eng_A.1 TURN-FAIL, eng_A.2 glm-flash-free
	{ 700, 90, 0.43, 125, 255, 168 }, -- eng_E.1 openclaw
	{ 180, 330, 0.51, 111, 216, 255 }, { 430, 460, 0.59, 111, 216, 255 }, -- eng_Z.1, eng_Z.2 zai-opencode
	{ 760, 380, 0.51, 111, 216, 255 }, { 870, 200, 0.43, 111, 216, 255 }, -- eng_Z.3, eng_Z.4
}
local PILLARS = { -- occluders: { x, y, w, h } — exact
	{ 200, 130, 44, 150 }, { 460, 330, 44, 170 }, { 700, 110, 44, 150 }, { 620, 430, 44, 120 },
}
local SEATS = { { 40, 300 }, { 70, 300 }, { 100, 300 }, { 40, 420 }, { 70, 420 }, { 100, 420 } }
local LAMP_STEPS = { 0.10, 0.43, 0.51, 0.59 } -- the engines' own intensities
local LAMP_RGB = { 255, 224, 102 } -- #ffe066, the operator lane from the source legend

local lampI: { [Player]: number } = {}
-- annotation exactness (t42 triage, lanes/t42.check.txt row 1): walkers hold Instance.new("Part") (line 148); Part is what is stored, BasePart failed the exact-table literal check. Runtime unchanged.
local walkers: { { x: number, y: number, part: Part } } = {}
local tiles: { BasePart } = {}
local rng = SeedRng.new(20260903) -- field ts 2026-09-03

local function inOcc(x: number, y: number): boolean
	for _, o in ipairs(PILLARS) do
		if x >= o[1] and x <= o[1] + o[3] and y >= o[2] and y <= o[2] + o[4] then return true end
	end
	return false
end

-- the film's truth: summed radial falloff per light; a raised lamp writes too
local function field(x: number, y: number): (number, number, number, number)
	local v, r, g, b = 0, 0, 0, 0
	for _, L in ipairs(LIGHTS) do
		local rad = 170 * L[3] + 40
		local d = math.sqrt((x - L[1]) ^ 2 + (y - L[2]) ^ 2)
		if d < rad then
			local w = (1 - d / rad) ^ 1.6 * L[3]
			r += w * L[4] ; g += w * L[5] ; b += w * L[6] ; v += w
		end
	end
	for p, I in pairs(lampI) do
		local root = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if root then
			local rel = root.Position - origin
			local rad, d = 170 * I + 40, math.sqrt((rel.X / STUD - x) ^ 2 + (rel.Z / STUD - y) ^ 2)
			if d < rad then
				local w = (1 - d / rad) ^ 1.6 * I
				r += w * LAMP_RGB[1] ; g += w * LAMP_RGB[2] ; b += w * LAMP_RGB[3] ; v += w
			end
		end
	end
	return v, r, g, b
end

local function lampPos(p: Player): (number?, number?)
	local root = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return nil, nil end
	local rel = root.Position - origin
	return rel.X / STUD, rel.Z / STUD
end

-- L2: dumb sagents — walk up the intensity gradient, bounce off occluders
local function stepWalkers()
	for i, w in ipairs(walkers) do
		local bx, by, bv = w.x, w.y, field(w.x, w.y)
		for a = 0, 7 do
			local th = a * math.pi / 4 + math.sin(simT + i) * 0.3
			local nx, ny = w.x + math.cos(th) * 3.2, w.y + math.sin(th) * 3.2
			if nx > 8 and ny > 8 and nx < 952 and ny < 592 and not inOcc(nx, ny) then
				local v = field(nx, ny)
				if v > bv then bx, by, bv = nx, ny, v end
			end
		end
		if bx == w.x and by == w.y then
			local th = math.sin(simT * 1.7 + i * 2.1) * math.pi * 2
			local nx, ny = w.x + math.cos(th) * 3.2, w.y + math.sin(th) * 3.2
			if nx > 8 and ny > 8 and nx < 952 and ny < 592 and not inOcc(nx, ny) then w.x, w.y = nx, ny end
		else
			w.x, w.y = bx, by
		end
		for p, I in pairs(lampI) do -- a walker that reaches your lamp banks
			local px, py = lampPos(p)
			if px and I > 0 and math.sqrt((w.x - px) ^ 2 + (w.y - (py :: number)) ^ 2) < BANK_DIST then
				p:SetAttribute("SteerBanked", (tonumber(p:GetAttribute("SteerBanked")) or 0) + BANK_PAY)
				ShadowLedger.record(p, "SteerField", ("steered a walker to the lamp (+%d)"):format(BANK_PAY), true)
				local s = SEATS[rng:int(1, #SEATS)] ; w.x, w.y = s[1], s[2]
				break
			end
		end
	end
end

local function refreshTiles()
	for tz = 0, 14 do
		for tx = 0, 23 do
			local t = tiles[tz * 24 + tx + 1]
			local _, r, g, b = field(tx * 40 + 20, tz * 40 + 20)
			t.Color = Color3.fromRGB(math.min(255, r) * 0.9 + 7, math.min(255, g) * 0.9 + 8, math.min(255, b) * 0.9 + 12)
		end
	end
end

function SteerFieldZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "SteerField"
	for _ = 1, 24 * 15 do -- the film floor: 24x15 tiles of 10 studs
		local t = Instance.new("Part")
		t.Anchored = true ; t.Size = Vector3.new(10, 1, 10)
		t.Position = origin + Vector3.new((#tiles % 24) * 10 + 5, 0, math.floor(#tiles / 24) * 10 + 5)
		t.Color = Color3.fromRGB(7, 8, 12) ; t.Parent = model ; table.insert(tiles, t)
	end
	refreshTiles()
	for _, L in ipairs(LIGHTS) do -- engines: ring + orb in lane color
		local ring = Instance.new("Part")
		ring.Shape = Enum.PartType.Cylinder ; ring.Anchored = true ; ring.Size = Vector3.new(0.4, 8, 8)
		ring.CFrame = CFrame.new(origin + Vector3.new(L[1] * STUD, 0.8, L[2] * STUD)) * CFrame.Angles(0, 0, math.rad(90))
		ring.Color = Color3.fromRGB(L[4], L[5], L[6]) ; ring.Material = Enum.Material.Neon ; ring.Parent = model
		local orb = Instance.new("Part")
		orb.Shape = Enum.PartType.Ball ; orb.Anchored = true ; orb.Size = Vector3.new(2, 2, 2)
		orb.Position = origin + Vector3.new(L[1] * STUD, 4, L[2] * STUD)
		orb.Color = ring.Color ; orb.Material = Enum.Material.Neon ; orb.Parent = model
		orb.Name = L[3] >= 0.51 and "EngineBright" or "Engine"
	end
	for _, o in ipairs(PILLARS) do -- failure pillars block walkers and players
		local wall = Instance.new("Part")
		wall.Anchored = true ; wall.Size = Vector3.new(o[3] * STUD, 10, o[4] * STUD)
		wall.Position = origin + Vector3.new((o[1] + o[3] / 2) * STUD, 5, (o[2] + o[4] / 2) * STUD)
		wall.Color = Color3.fromRGB(16, 19, 25) ; wall.Name = "Pillar" ; wall.Parent = model
	end
	for i, s in ipairs(SEATS) do
		local w = Instance.new("Part")
		w.Shape = Enum.PartType.Ball ; w.Anchored = true ; w.Size = Vector3.new(1, 1, 1)
		w.Color = Color3.fromRGB(232, 236, 245) ; w.Material = Enum.Material.Neon
		w.Name = "Walker" .. i ; w.Position = origin + Vector3.new(s[1] * STUD, 1.5, s[2] * STUD) ; w.Parent = model
		table.insert(walkers, { x = s[1], y = s[2], part = w })
	end
	local dimmer = Instance.new("Part") -- the dimmer station: raise your lamp
	dimmer.Anchored = true ; dimmer.Size = Vector3.new(6, 6, 6)
	dimmer.Color = Color3.fromRGB(LAMP_RGB[1], LAMP_RGB[2], LAMP_RGB[3]) ; dimmer.Material = Enum.Material.Neon
	dimmer.Position = origin + Vector3.new(-15, 4, 40) ; dimmer.Name = "Dimmer" ; dimmer.Parent = model
	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = "Turn your lamp up (off at max)"
	prompt.ObjectText = "dimmer station" ; prompt.HoldDuration = 0.25 ; prompt.Parent = dimmer
	prompt.Triggered:Connect(function(player: Player)
		local cur = lampI[player] or 0
		local nextI: number? = nil
		for _, step in ipairs(LAMP_STEPS) do
			if step > cur then nextI = step ; break end
		end
		if nextI then
			lampI[player] = nextI
			ShadowLedger.record(player, "SteerField", ("raised the lamp to I=%.2f"):format(nextI), true)
		else
			ShadowLedger.record(player, "SteerField", "dimmed the lamp off", true)
		end
	end)
	model.Parent = workspace
	Players.PlayerRemoving:Connect(function(p) lampI[p] = nil end)
	return model
end

function SteerFieldZone.tick(dt: number)
	stepAcc += dt
	while stepAcc >= T_STEP do -- source: step + draw every 66 ms
		stepAcc -= T_STEP
		simT += 0.05
		stepWalkers()
	end
	for _, w in ipairs(walkers) do
		w.part.Position = origin + Vector3.new(w.x * STUD, 1.5, w.y * STUD)
	end
	tileClock += dt
	if tileClock >= 0.25 then tileClock = 0 ; refreshTiles() end
end

return SteerFieldZone
