--!strict
-- ErosionFieldZone — translated from dashboard/static/erosion_field.html (B1 v1).
-- Technique family credited to Rune Skovbo Johansen (runevision, Shadertoy
-- sf23W1): talus-limited slide + slope creep, 2 ping-pong erode passes, 7
-- engines upwell, the rim drains to sea, 6 marbles roll under -grad(h) and
-- abrade. Paint raise/carve under your feet; grain carved off your stroke banks.
local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local ErosionFieldZone = {}
local origin = Vector3.new(0, 8, -420)
local GW, GH, CELL = 120, 80, 4 -- source was 240x150 cells; half res, same operator
local STUD, HEIGHT = 0.5, 12 -- 480x320 field-px; HEIGHT CLAIMED: studs per unit h
local TALUS, KF, CREEP, DRAIN = 0.010, 0.125, 0.045, 0.985
local H: { number } = table.create(GW * GH, 0)
local H2: { number } = table.create(GW * GH, 0)
local paintedBy: { [number]: Player? } = {}
local tiles: { BasePart } = {}
-- annotation exactness (t42 triage, lanes/t42.check.txt row 7): marbles hold Instance.new("Part") (line 168); stepMarble below takes the same entries. Runtime unchanged.
local marbles: { { x: number, y: number, vx: number, vy: number, part: Part } } = {}
local brush: { [Player]: number } = {} -- +1 raise, -1 carve (source L / R-drag)
local nextPaint: { [Player]: number } = {}
local bankedOnce: { [Player]: boolean } = {}
local erodeAcc, tileClock = 0, 0
local rng = SeedRng.new(20260903) -- field ts 2026-09-03

local ENGINES = { -- source lights, halved px: { x, y, intensity }
	{ 70, 45, 0.10 }, { 210, 40, 0.43 }, { 350, 45, 0.43 }, { 90, 165, 0.51 },
	{ 215, 230, 0.59 }, { 380, 190, 0.51 }, { 435, 100, 0.43 },
}
local MESAS = { -- source occluders, halved px: { x, y, w, h }
	{ 100, 65, 22, 75 }, { 230, 165, 22, 85 }, { 350, 55, 22, 75 }, { 310, 215, 22, 60 },
}
local SEATS = { { 20, 150 }, { 35, 150 }, { 50, 150 }, { 20, 210 }, { 35, 210 }, { 50, 210 } }
local BRUSHES: { { name: string, mode: number, color: Color3 } } = {
	{ name = "raise", mode = 1, color = Color3.fromRGB(232, 236, 245) },
	{ name = "carve", mode = -1, color = Color3.fromRGB(255, 107, 107) },
}
local STOPS = { -- hypsometric palette (sea below 0.205), exact from source
	{ 0.00, 10, 24, 46 }, { 0.12, 18, 44, 78 }, { 0.20, 40, 78, 110 },
	{ 0.24, 126, 116, 82 }, { 0.32, 56, 82, 50 }, { 0.52, 76, 106, 62 },
	{ 0.70, 104, 99, 90 }, { 0.88, 128, 123, 113 }, { 1.05, 226, 232, 240 },
}

local function pal(h: number): Color3
	if h <= STOPS[1][1] then return Color3.fromRGB(STOPS[1][2], STOPS[1][3], STOPS[1][4]) end
	for s = 1, #STOPS - 1 do
		local a, b = STOPS[s], STOPS[s + 1]
		if h <= b[1] then
			local t = (h - a[1]) / (b[1] - a[1])
			return Color3.fromRGB(a[2] + (b[2] - a[2]) * t, a[3] + (b[3] - a[3]) * t, a[4] + (b[4] - a[4]) * t)
		end
	end
	local top = STOPS[#STOPS] ; return Color3.fromRGB(top[2], top[3], top[4])
end

-- one quadratic splat serves PASS 0 paint, PASS 1b upwell, and mesa seeding
local function splat(px: number, py: number, radCells: number, amp: number, who: Player?)
	local cx, cy = px / CELL, py / CELL
	for j = math.max(1, math.floor(cy - radCells)), math.min(GH - 2, math.ceil(cy + radCells)) do
		for i = math.max(1, math.floor(cx - radCells)), math.min(GW - 2, math.ceil(cx + radCells)) do
			local q = 1 - ((i - cx) ^ 2 + (j - cy) ^ 2) / (radCells * radCells)
			if q > 0 then
				local k = j * GW + i
				H[k] += amp * q * q ; if who then paintedBy[k] = who end
			end
		end
	end
end

local function seedField()
	for j = 0, GH - 1 do
		for i = 0, GW - 1 do
			local x, y = i / GW, j / GH -- det spine: sine relief, no RNG
			local h = 0.30 + 0.10 * math.sin(x * 7.3 + y * 3.1) + 0.07 * math.sin(x * 13.7 - y * 9.2 + 1.7)
				+ 0.05 * math.sin(x * 23 + y * 31 + 4.1)
			H[j * GW + i] = math.max(0.02, h)
		end
	end
	for _, o in ipairs(MESAS) do -- occluders stand as high ground (mesa + skirt)
		local cx, cy = (o[1] + o[3] / 2) / CELL, (o[2] + o[4] / 2) / CELL
		local rw, rh = o[3] / (2 * CELL), o[4] / (2 * CELL)
		for j = math.max(1, math.floor(cy - rh - 8)), math.min(GH - 2, math.ceil(cy + rh + 8)) do
			for i = math.max(1, math.floor(cx - rw - 8)), math.min(GW - 2, math.ceil(cx + rw + 8)) do
				local dx, dy = math.max(math.abs(i - cx) - rw, 0), math.max(math.abs(j - cy) - rh, 0)
				local w = math.max(0, 1 - math.sqrt(dx * dx + dy * dy) / 8) ; H[j * GW + i] += w * w * 0.85
			end
		end
	end
	for _, L in ipairs(ENGINES) do -- lights become hills: q^2 falloff, hh = 0.2+0.8I
		splat(L[1], L[2], (40 + 130 * L[3]) / CELL, 0.2 + 0.8 * L[3], nil)
	end
end

-- PASS 1 — gather-form, order-free per-cell operator (the source's fragment
-- shader body): spill past the talus angle, creep below it, drain the rim.
local function erodePass(src: { number }, dst: { number })
	for j = 0, GH - 1 do
		for i = 0, GW - 1 do
			local k, h = j * GW + i, src[j * GW + i]
			local hL = i > 0 and src[k - 1] or h ; local hR = i < GW - 1 and src[k + 1] or h
			local hU = j > 0 and src[k - GW] or h ; local hD = j < GH - 1 and src[k + GW] or h
			local fin, fout = 0, 0
			local d = hL - h ; if d > TALUS then fin += d - TALUS elseif d < -TALUS then fout += -d - TALUS end
			d = hR - h ; if d > TALUS then fin += d - TALUS elseif d < -TALUS then fout += -d - TALUS end
			d = hU - h ; if d > TALUS then fin += d - TALUS elseif d < -TALUS then fout += -d - TALUS end
			d = hD - h ; if d > TALUS then fin += d - TALUS elseif d < -TALUS then fout += -d - TALUS end
			local nh = h + (fin - fout) * KF
			nh += ((hL + hR + hU + hD) * 0.25 - h) * CREEP -- sub-talus creep
			if i == 0 or j == 0 or i == GW - 1 or j == GH - 1 then nh *= DRAIN end -- rim drain
			dst[k] = nh
		end
	end
end

local function sampleH(px: number, py: number): number
	local gx, gy = math.clamp(px / CELL - 0.5, 0, GW - 1.001), math.clamp(py / CELL - 0.5, 0, GH - 1.001)
	local i, j = math.floor(gx), math.floor(gy)
	local u, v, k = gx - i, gy - j, j * GW + i
	return H[k] * (1 - u) * (1 - v) + H[k + 1] * u * (1 - v) + H[k + GW] * (1 - u) * v + H[k + GW + 1] * u * v
end

-- PASS 2 — marbles: gravity along -grad(h) with momentum; the roll abrades
-- same entry type as the marbles table (t42 triage, lanes/t42.check.txt row 7), annotation only
local function stepMarble(m: { x: number, y: number, vx: number, vy: number, part: Part })
	local gx = sampleH(m.x + 2.5, m.y) - sampleH(m.x - 2.5, m.y)
	local gy = sampleH(m.x, m.y + 2.5) - sampleH(m.x, m.y - 2.5)
	m.vx -= gx * 2.8 ; m.vy -= gy * 2.8
	m.vx = m.vx * 0.986 + (rng:next() - 0.5) * 0.05 -- stochastic flesh: jitter
	m.vy = m.vy * 0.986 + (rng:next() - 0.5) * 0.05
	local sp = math.sqrt(m.vx * m.vx + m.vy * m.vy)
	if sp > 6 then m.vx *= 6 / sp ; m.vy *= 6 / sp end
	m.x += m.vx ; m.y += m.vy
	if m.x < 6 then m.x = 6 ; m.vx *= -0.5 end ; if m.x > 474 then m.x = 474 ; m.vx *= -0.5 end
	if m.y < 6 then m.y = 6 ; m.vy *= -0.5 end ; if m.y > 314 then m.y = 314 ; m.vy *= -0.5 end
	local k = math.clamp(math.floor(m.y / CELL), 0, GH - 1) * GW + math.clamp(math.floor(m.x / CELL), 0, GW - 1)
	H[k] -= 0.0025 ; if H[k] < 0.02 then H[k] = 0.02 end -- abrasion: dust leaves
	local p = paintedBy[k]
	if p and p.Parent then -- grain carved off your stroke = credit
		p:SetAttribute("ErosionBanked", (tonumber(p:GetAttribute("ErosionBanked")) or 0) + 1)
		if not bankedOnce[p] then
			bankedOnce[p] = true
			ShadowLedger.record(p, "ErosionField", "first grain banked - the marbles carve where you wrote", true)
		end
	end
	m.part.Position = origin + Vector3.new(m.x * STUD, sampleH(m.x, m.y) * HEIGHT + 1.3, m.y * STUD)
end

local function refreshTiles()
	for tz = 0, 19 do
		for tx = 0, 29 do
			local h, t = H[(tz * 4 + 2) * GW + (tx * 4 + 2)], tiles[tz * 30 + tx + 1]
			t.Position = origin + Vector3.new(tx * 8 + 4, h * HEIGHT, tz * 8 + 4) ; t.Color = pal(h)
		end
	end
end

function ErosionFieldZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "ErosionField"
	seedField()
	for _ = 1, 30 * 20 do -- terrain: 30x20 slabs of 8x8 studs (4x4 cells each)
		local t = Instance.new("Part")
		t.Anchored = true ; t.Size = Vector3.new(8, 1, 8) ; t.Parent = model ; table.insert(tiles, t)
	end
	refreshTiles()
	for i, w in ipairs(SEATS) do -- six marbles from the source walkers
		local m = Instance.new("Part")
		m.Shape = Enum.PartType.Ball ; m.Size = Vector3.new(1.6, 1.6, 1.6)
		m.Color = Color3.fromRGB(238, 242, 248) ; m.Material = Enum.Material.SmoothPlastic
		m.Name = "Marble" .. i ; m.Parent = model
		table.insert(marbles, { x = w[1], y = w[2], vx = 0, vy = 0, part = m })
	end
	for bi, def in ipairs(BRUSHES) do -- the film writes back under your feet
		local s = Instance.new("Part")
		s.Anchored = true ; s.Size = Vector3.new(6, 4, 6) ; s.Color = def.color
		s.Material = Enum.Material.Neon ; s.Position = origin + Vector3.new(-20, 3, bi * 14 - 7)
		s.Name = def.name .. "Brush" ; s.Parent = model
		local prompt = Instance.new("ProximityPrompt")
		prompt.ActionText = "Take the " .. def.name .. " brush"
		prompt.ObjectText = "erosion field" ; prompt.HoldDuration = 0.25 ; prompt.Parent = s
		prompt.Triggered:Connect(function(player: Player)
			brush[player] = def.mode
			ShadowLedger.record(player, "ErosionField", "took the " .. def.name .. " brush", true)
		end)
	end
	model.Parent = workspace
	Players.PlayerRemoving:Connect(function(p)
		brush[p] = nil ; nextPaint[p] = nil ; bankedOnce[p] = nil
		for k, who in pairs(paintedBy) do if who == p then paintedBy[k] = nil end end
	end)
	return model
end

function ErosionFieldZone.tick(dt: number)
	erodeAcc += dt
	if erodeAcc >= 0.125 then -- source frame: 2 ping-pong passes, then upwell
		erodeAcc = 0
		for _ = 1, 2 do erodePass(H, H2) ; local tmp = H ; H = H2 ; H2 = tmp end
		for _, L in ipairs(ENGINES) do splat(L[1], L[2], 3.5, 0.00007 * L[3], nil) end
	end
	for _, p in ipairs(Players:GetPlayers()) do
		local mode = brush[p]
		local root = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if mode and root and os.clock() >= (nextPaint[p] or 0) then
			local rel = root.Position - origin
			local px, py = rel.X / STUD, rel.Z / STUD
			if px > 6 and px < 474 and py > 6 and py < 314 then
				nextPaint[p] = os.clock() + 0.15
				splat(px, py, 9, mode * 0.06, p) -- strokes are steering packets
			end
		end
	end
	for _, m in ipairs(marbles) do stepMarble(m) end
	tileClock += dt
	if tileClock >= 0.3 then tileClock = 0 ; refreshTiles() end
end

return ErosionFieldZone
