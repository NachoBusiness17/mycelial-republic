--!strict
-- RiddleMazeZone — PORT REALITY NOTE: eraser_maze.html has NO riddles. It is THE ERASER MAZE
-- (PURPLE HARVEST B2): a maze lit by a two-layer quantum field — WAVE layer (path-sum fringes
-- in the twin-slit chamber, wall x=44, gaps y=15/25) and MEASUREMENT layer (cells inside sight
-- radius are SEEN: the incoherent sum shows, fringes die). The eraser fires a unitary phase
-- rotation (phi += pi/3): fringes return IN THE NEW BASIS. Win: reach the PRISM after an eraser
-- re-mixed its basis (eraseStamp>0) and no collapse landed on it since — the delayed-choice
-- loop. Observation ledger append-only (SEED/COLLAPSE/ERASE/PRISM rows; tail pruning only
-- windows the live view, rows are never rewritten). Kept source numbers: 61x41 grid, chamber
-- carve 36..56x8..32, SEED_AMP=0.5, k=2, sight r=7, pads r=10/13/10/9 at the exact want list,
-- tile cooldown 30 frames, palette+gamma 0.72, boot seed 20260906. Port gaps (honest): sliders,
-- R-reseed, falsifier grid, sight-ring drawing, dead-end braiding (braid 0.55, corridor
-- topology only — the two tagged slit families are the route families that fringe), the
-- source's own-light family and the carried E-eraser (the four eraser pads deliver the erase);
-- amplitudes keep the EXACT k*d_f phases with uniform magnitude; free movement replaces
-- frame-stepped grid moves (cells map from position).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerScriptService = game:GetService("ServerScriptService")
local SeedRng = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("SeedRng"))
local SectionStream = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("SectionStream"))
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local RiddleMazeZone = {}; local origin = Vector3.new(300, 8, 0) -- clear of every listed zone origin
local GW, GH, CELL, N = 61, 41, 5, 61 * 41 -- exact source numbers
local GX, G1, G2 = 44, 15, 25
local K_WAVE, SIGHT_R, SEED_AMP, ERASER_PHI = 2.0, 7, 0.5, math.pi / 3
local DX, DY = { 1, -1, 0, 0 }, { 0, 0, 1, -1 }
-- Q-043 streamed sections (GnomeCode ep.1 pattern): the wall grid materializes
-- in 8x8-cell chunks around whoever approaches instead of ~1400 wall parts at
-- boot. Everything gameplay-bearing (floor, chamber tiles, prism, pads, the
-- field itself) still builds eagerly; wall parts are anonymous geometry no
-- other system looks up, so deferring them changes nothing observable except
-- WHEN the rock appears.
local CHUNK = 8
local STREAM_RADIUS = 120 -- the RIDDLE MAZE portal lands ~100 studs south; the maze manifests on approach
local STREAM_BUDGET = 4 -- chunks per poll tick: a walking player gets the whole neighborhood in well under a second

type Family = { d: { [number]: number }, sig: number, amp: number }
local fieldOpen: { [number]: number } = {}; local fams: { Family } = {}
local ccos, csin = {}, {} -- cos/sin(k*d): the field's phase basis
local obsStamp, eraseStamp, prism = {}, {}, { x = 52, y = 20 }; local phi, frameN, prismHasFringes = 0, 0, false
local stats = { collapses = 0, erases = 0 }; local ledger: { string } = {}
local chamberTiles: { { part: BasePart, i: number, v: number? } } = {}
local prismPart: BasePart? = nil; local won: { [Player]: boolean } = {}
local wallStreamRef: SectionStream.SectionStream? = nil -- Q-043: the wall-chunk stream, polled from tick

local function logRow(kind: string, detail: string) -- the append-only observation ledger
	table.insert(ledger, ("#%04d %s f%d · %s"):format(#ledger, kind, frameN, detail)); if #ledger > 30 then table.remove(ledger, 1) end -- tail windowed; rows never rewritten
end

local function nb(x: number, y: number): number return (x >= 0 and y >= 0 and x < GW and y < GH) and y * GW + x or -1 end

-- BFS over open cells (mask-limited); unreachable cells read as -1
local function bfs(sx: number, sy: number, mask: { [number]: number }?): { [number]: number }
	local dist, q, qh, qt = {}, {}, 1, 1
	dist[sy * GW + sx], q[1] = 0, sy * GW + sx
	while qh <= qt do
		local c = q[qh]; qh += 1
		for dd = 1, 4 do
			local p = nb(c % GW + DX[dd], math.floor(c / GW) + DY[dd])
			if p >= 0 and fieldOpen[p] == 1 and dist[p] == nil and (mask == nil or mask[p] == 1) then dist[p], qt, q[qt + 1] = dist[c] + 1, qt + 1, p end
		end
	end
	for i = 0, N - 1 do if dist[i] == nil then dist[i] = -1 end end
	return dist
end

local function genMaze(rng) -- recursive backtracker on odd cells (source's braid pass not ported)
	local open = fieldOpen
	for y = 1, GH - 2 do for x = 1, GW - 2 do if x % 2 == 1 and y % 2 == 1 then open[y * GW + x] = 1 end end end
	local seen, stack = { [GW + 1] = true }, { GW + 1 }
	while #stack > 0 do
		local cur = stack[#stack]
		local cx, cy = cur % GW, math.floor(cur / GW)
		local opts = {}
		for dd = 1, 4 do
			local nx, ny = cx + DX[dd] * 2, cy + DY[dd] * 2
			if nx > 0 and ny > 0 and nx < GW - 1 and ny < GH - 1 and not seen[ny * GW + nx] then table.insert(opts, dd) end
		end
		if #opts == 0 then table.remove(stack) else
			local dd = opts[rng:int(1, #opts)]
			local ty, tx = cy + DY[dd] * 2, cx + DX[dd] * 2
			open[(cy + DY[dd]) * GW + cx + DX[dd]], open[ty * GW + tx], seen[ty * GW + tx] = 1, 1, true
			table.insert(stack, ty * GW + tx)
		end
	end
end

-- display intensity: observed (which-path known) -> sum |A_f|^2 (flat); else coherent |sum A_f e^{i phi sigma_f}|^2
local function intensityAt(i: number, incoherent: boolean): number
	if incoherent then -- observed: which-path known -> the tagged sum, washed flat
		local s = 0; for _, fm in ipairs(fams) do if fm.d[i] >= 0 then s += fm.amp * fm.amp end end; return s
	end
	local cs, sn, cr, ci = math.cos(phi), math.sin(phi), 0, 0
	for _, fm in ipairs(fams) do
		local di = fm.d[i]
		if di >= 0 then
			local re, im, sg = fm.amp * ccos[di], fm.amp * csin[di], fm.sig
			cr += re * cs - im * sg * sn; ci += re * sg * sn + im * cs
		end
	end
	return cr * cr + ci * ci
end

local function blast(cx: number, cy: number, r: number, label: string, erasing: boolean)
	local n = 0; if erasing then phi += ERASER_PHI end -- unitary on the tags, never a deletion
	for dy = -r, r do for dx = -r, r do
		local i = (dx * dx + dy * dy <= r * r) and nb(cx + dx, cy + dy) or -1
		if i >= 0 and fieldOpen[i] == 1 then
			n += 1
			if erasing then eraseStamp[i] = frameN else obsStamp[i] = frameN end
		end
	end end
	if erasing then stats.erases += 1 else stats.collapses += 1 end
	logRow(erasing and "ERASE" or "COLLAPSE", ("%s r=%d @%d,%d · +%d cells%s · total %d"):format(label, r, cx, cy, n,
		erasing and (" · basis now %d°"):format(math.floor(math.deg(phi)) % 360) or "", erasing and stats.erases or stats.collapses))
end

local function stampSight(px: number, py: number) -- seeing collapses the light
	for dy = -SIGHT_R, SIGHT_R do for dx = -SIGHT_R, SIGHT_R do
		local x, y = px + dx, py + dy
		local i = (dx * dx + dy * dy <= SIGHT_R * SIGHT_R) and nb(x, y) or -1
		if i >= 0 and fieldOpen[i] == 1 and not (x == prism.x and y == prism.y) then obsStamp[i] = frameN end -- the prism reads without recording
	end end
end

local function snapOpen(x: number, y: number): (number, number)
	if fieldOpen[y * GW + x] == 1 then return x, y end
	for r = 1, 14 do for dy = -r, r do for dx = -r, r do
		local nx, ny = x + dx, y + dy
		if nx >= 1 and ny >= 1 and nx < GW - 1 and ny < GH - 1 and fieldOpen[ny * GW + nx] == 1 then return nx, ny end
	end end end
	return 1, 1
end

local function worldXZ(x: number, y: number): Vector3 return origin + Vector3.new((x - (GW - 1) / 2) * CELL, 0, (y - (GH - 1) / 2) * CELL) end
local function cellOf(pos: Vector3): (number, number) return math.floor((pos.X - origin.X) / CELL + 0.5) + 30, math.floor((pos.Z - origin.Z) / CELL + 0.5) + 20 end
local function inBounds(pos: Vector3): boolean return math.abs(pos.X - origin.X) <= GW * CELL / 2 + 10 and math.abs(pos.Z - origin.Z) <= GH * CELL / 2 + 10 and math.abs(pos.Y - origin.Y) < 30 end

local function part(model: Model, name: string, size: Vector3, pos: Vector3, color: Color3, mat: Enum.Material): BasePart
	local p = Instance.new("Part"); p.Anchored, p.Name, p.Size, p.Position, p.Color, p.Material, p.Parent = true, name, size, pos, color, mat, model; return p
end

function RiddleMazeZone.build(): Model
	local model = Instance.new("Model"); model.Name = "EraserMaze"; local rng = SeedRng.new(20260906) -- the source boot seed
	table.clear(fieldOpen); table.clear(fams); genMaze(rng)
	for y = 8, 32 do for x = 36, 56 do fieldOpen[y * GW + x] = 1 end end -- carve the chamber hall
	for y = 8, 32 do if y ~= G1 and y ~= G2 then fieldOpen[y * GW + GX] = 0 end end -- full-height twin-slit wall
	for i = 0, N do ccos[i], csin[i] = math.cos(K_WAVE * i), math.sin(K_WAVE * i) end
	local mask1 = {} -- the tagged slit families live only on the dark side of the slit wall
	for i = 0, N - 1 do
		local x, y = i % GW, math.floor(i / GW)
		if fieldOpen[i] == 1 and x >= GX and y >= 8 and y <= 32 then mask1[i] = 1 end
	end
	fams[1], fams[2] = { d = bfs(GX, G1, mask1), sig = 1, amp = SEED_AMP }, { d = bfs(GX, G2, mask1), sig = -1, amp = SEED_AMP } -- slits y=15 / y=25
	prism.x, prism.y = snapOpen(prism.x, prism.y)
	prismHasFringes = fams[1].d[prism.y * GW + prism.x] >= 0 and fams[2].d[prism.y * GW + prism.x] >= 0 -- true two-path light or the win is fake
	table.clear(obsStamp); table.clear(eraseStamp); table.clear(ledger); table.clear(chamberTiles)
	frameN, phi, stats.collapses, stats.erases = 0, 0, 0, 0
	part(model, "MazeFloor", Vector3.new(GW * CELL, 1, GH * CELL), origin + Vector3.new(0, -0.5, 0), Color3.fromRGB(6, 10, 9), Enum.Material.Slate)
	-- Q-043: walls stream in 8x8-cell chunks (same per-cell part call as the
	-- old eager loop, same look). genMaze ran above, so fieldOpen is final;
	-- each chunk closure reads the cells it owns. No SeedRng in the build
	-- pass (the source fixes every wall), so unordered proximity streaming
	-- cannot reorder anything.
	local wallStream = SectionStream.new({ radius = STREAM_RADIUS, budget = STREAM_BUDGET })
	for cy = 0, GH - 1, CHUNK do
		for cx = 0, GW - 1, CHUNK do
			local x0, y0 = cx, cy
			local x1, y1 = math.min(cx + CHUNK - 1, GW - 1), math.min(cy + CHUNK - 1, GH - 1)
			local center = worldXZ((x0 + x1) / 2, (y0 + y1) / 2) + Vector3.new(0, 5, 0)
			wallStream:add(center, function()
				for y = y0, y1 do for x = x0, x1 do -- walls where the field is closed
					if fieldOpen[y * GW + x] ~= 1 then part(model, "Wall", Vector3.new(CELL, 10, CELL), worldXZ(x, y) + Vector3.new(0, 5, 0), Color3.fromRGB(18, 24, 22), Enum.Material.Slate) end
				end end
			end)
		end
	end
	wallStreamRef = wallStream
	for y = 8, 32 do for x = 36, 56 do -- chamber floor tiles carry the fringe palette
		local i = y * GW + x
		if fieldOpen[i] == 1 then table.insert(chamberTiles, { part = part(model, "FringeTile", Vector3.new(CELL, 0.3, CELL), worldXZ(x, y) + Vector3.new(0, 0.15, 0), Color3.fromRGB(10, 12, 16), Enum.Material.Neon), i = i }) end
	end end
	prismPart = part(model, "Prism", Vector3.new(4.5, 4.5, 4.5), worldXZ(prism.x, prism.y) + Vector3.new(0, 2.5, 0), Color3.fromRGB(255, 124, 224), Enum.Material.Neon)
	local pl = Instance.new("PointLight"); pl.Color, pl.Range, pl.Brightness, pl.Parent = Color3.fromRGB(255, 124, 224), 16, 1.5, prismPart
	-- eraser + detector pads at the source's exact want list, snapped to open cells
	local want: { { any } } = { { 40, 12, "eraser", 0 }, { 48, 20, "eraser", 0 }, { 12, 6, "eraser", 0 }, { 38, 28, "eraser", 0 }, { 46, 20, "detector", 13 }, { 36, 20, "detector", 10 }, { 20, 34, "detector", 9 } }
	for _, wd in ipairs(want) do
		local t = { x = wd[1], y = wd[2], kind = wd[3], r = wd[4], cool = 0 }
		t.x, t.y = snapOpen(t.x, t.y)
		local pad = part(model, t.kind .. "Pad", Vector3.new(CELL, 0.4, CELL), worldXZ(t.x, t.y) + Vector3.new(0, 0.25, 0), t.kind == "eraser" and Color3.fromRGB(180, 140, 255) or Color3.fromRGB(255, 106, 77), Enum.Material.Neon)
		pad.Touched:Connect(function(hit)
			local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
			if plr and frameN >= t.cool then -- source tile cooldown: 30 frames
				t.cool = frameN + 30
				blast(t.x, t.y, t.kind == "eraser" and 10 or t.r, t.kind == "eraser" and "eraser tile" or "DETECTOR tile", t.kind == "eraser")
			end
		end)
	end
	logRow("SEED", "maze seed 20260906 · ledger opened (append-only) · prism two-path: " .. (prismHasFringes and "YES" or "NO"))
	model.Parent = workspace
	return model
end

function RiddleMazeZone.tick(_dt: number)
	frameN += 1; local pi0 = prism.y * GW + prism.x
	-- Q-043: manifest wall chunks around anyone whose position is near the
	-- maze (all players poll, not just inBounds ones: the approach counts)
	local stream = wallStreamRef
	if stream then
		local roots: { Vector3 } = {}
		for _, plr in ipairs(Players:GetPlayers()) do
			local root = plr.Character and plr.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then table.insert(roots, root.Position) end
		end
		if #roots > 0 then stream:poll(roots) end
	end
	for _, plr in ipairs(Players:GetPlayers()) do
		local root = plr.Character and plr.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if root and inBounds(root.Position) then
			local cx, cy = cellOf(root.Position)
			stampSight(cx, cy) -- seeing collapses the light
			-- LIT only if an eraser re-mixed the basis and no collapse landed since: delayed choice
			if not won[plr] and prismHasFringes and math.abs(cx - prism.x) + math.abs(cy - prism.y) <= 2 and (eraseStamp[pi0] or 0) > 0 and (obsStamp[pi0] or 0) <= eraseStamp[pi0] then
				won[plr] = true
				plr:SetAttribute("VirtueMarks", (plr:GetAttribute("VirtueMarks") or 0) + 50)
				logRow("PRISM", ("LIT — prism read in the eraser basis @%d,%d · delayed choice honored"):format(prism.x, prism.y))
				ShadowLedger.record(plr, "RiddleMaze", "lit the prism in the eraser basis (delayed choice)", true)
			end
		end
	end
	local max = 0 -- display: the source normalizes by the frame's max display value
	for _, t in ipairs(chamberTiles) do
		t.v = intensityAt(t.i, (obsStamp[t.i] or 0) > (eraseStamp[t.i] or 0))
		if (t.v :: number) > max then max = t.v :: number end
	end
	if max <= 0 then max = 1 end
	for _, t in ipairs(chamberTiles) do -- observed -> washed flat slate; else coherent violet band (source palette + gamma 0.72)
		local seen = (obsStamp[t.i] or 0) > (eraseStamp[t.i] or 0)
		local tt = math.clamp((t.v :: number) / max, 0, 1) ^ 0.72
		if seen then t.part.Color = Color3.fromRGB(26 + 70 * tt, 30 + 66 * tt, 52 + 80 * tt)
		else t.part.Color = Color3.fromRGB(36 + 219 * tt, 22 + 98 * tt * tt, 70 + 185 * tt) end
	end
	local pp = prismPart
	if pp then -- white + pulse while the prism still fringes in the current basis (source stroke)
		local lit = prismHasFringes and (obsStamp[pi0] or 0) <= (eraseStamp[pi0] or 0)
		pp.Color = lit and Color3.fromRGB(255, 255, 255) or Color3.fromRGB(255, 124, 224)
		local light = pp:FindFirstChildOfClass("PointLight"); if light then light.Brightness = lit and 2 + math.sin(frameN * 0.2) or 1.5 end
		pp:SetAttribute("LedgerRows", #ledger); pp:SetAttribute("BasisDeg", math.floor(math.deg(phi)) % 360)
	end
end

Players.PlayerRemoving:Connect(function(p) won[p] = nil end)

return RiddleMazeZone
