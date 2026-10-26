--!strict
-- EigenMapZone -- the cathedral eigen-map built as a walkable plaza east of
-- the mountain. The world map IS the data: beacons stand at the scan's
-- eigen_centroids under the EigenMap transform (shared/EigenMap.luau, the
-- single authorship site for data + math), the water_first chain (operative
-- lean, watch/inbox/REFEREE_VERDICT_20260926.md) is drawn on the floor as
-- solid beams where the wired graph has the edge and dotted stones where it
-- does not (missing stitches = metered build debt, never narrated away), and
-- the off-map regions + the beta0 3-islands finding are carved on plaques
-- because a negative is a fact. The walker-view overlay itself is client
-- side (client/EigenMapHud.client.luau) and reads the same shared module.

local Players = game:GetService("Players")

local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local EigenMap = require(Shared:WaitForChild("EigenMap"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))

local EigenMapZone = {}

-- ledger debounce: one row per player+region per visit burst
local lastSeen: { [number]: { [string]: number } } = {}
local DEBOUNCE = 10

local FLOOR_MARGIN = 40

local function tag(parent: Instance, text: string, color: Color3, size: number)
	local bb = Instance.new("BillboardGui")
	bb.Size = UDim2.new(0, 320, 0, size * 14 + 8)
	bb.StudsOffset = Vector3.new(0, 6, 0)
	bb.MaxDistance = 220
	bb.AlwaysOnTop = false
	local label = Instance.new("TextLabel")
	label.Size = UDim2.fromScale(1, 1)
	label.BackgroundTransparency = 1
	label.Font = Enum.Font.Garamond
	label.TextSize = size
	label.TextColor3 = color
	label.Text = text
	label.Parent = bb
	bb.Parent = parent
	return bb
end

local function beacon(model: Model, name: string, wx: number, wz: number)
	local row = EigenMap.region(name)
	if not row then return end
	local pillar = Instance.new("Part")
	pillar.Anchored = true
	pillar.Size = Vector3.new(2.5, 9, 2.5)
	-- base on the floor top (FLOOR_Y), center up half the height
	pillar.Position = Vector3.new(wx, EigenMap.FLOOR_Y + 4.5, wz)
	pillar.Color = EigenMap.classColor(row.class)
	pillar.Material = Enum.Material.Neon
	pillar.Name = ("Beacon_%s"):format(name)
	pillar.Parent = model

	local classLine = row.cos and ("%s cos %.3f"):format(row.class, row.cos)
		or ("%s (off-manifold, no cosine)"):format(row.class)
	local eigenLine = ("eigen (%.4f, %.4f) · %d studs / milli-eigen")
		:format(row.ex, row.ey, EigenMap.studsPerMilli())
	tag(pillar, ("%s\n%s\n%d hop%s from water_computer\n%s")
		:format(name, classLine, row.hops, row.hops == 1 and "" or "s", eigenLine),
		Color3.fromRGB(230, 224, 196), 14)

	pillar.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if not player then return end
		local now = os.clock()
		local perPlayer = lastSeen[player.UserId]
		if perPlayer and perPlayer[name] and now - perPlayer[name] < DEBOUNCE then return end
		if not perPlayer then
			perPlayer = {}
			lastSeen[player.UserId] = perPlayer
		end
		perPlayer[name] = now
		ShadowLedger.record(player, "EigenMap",
			("walked the eigen-map: reached the %s beacon (%s, %d hops from water)")
				:format(name, classLine, row.hops))
	end)
end

local function chainBeam(model: Model, ax: number, az: number, bx: number, bz: number, kind: string)
	local y = EigenMap.FLOOR_Y + 0.12
	local a = Vector3.new(ax, y, az)
	local b = Vector3.new(bx, y, bz)
	local len = (b - a).Magnitude
	if kind == "wired" then
		local beam = Instance.new("Part")
		beam.Anchored = true
		beam.CanCollide = false
		beam.Size = Vector3.new(1.2, 0.12, len)
		beam.CFrame = CFrame.lookAt((a + b) / 2, b)
		beam.Color = Color3.fromRGB(179, 86, 44) -- the HTML map's rust chain color
		beam.Material = Enum.Material.Neon
		beam.Transparency = 0.15
		beam.Name = "Chain_wired"
		beam.Parent = model
		return
	end
	-- missing stitch / via: dotted stones so the gap reads as a gap
	local stones = math.max(3, math.floor(len / 10))
	for i = 0, stones do
		local t = i / stones
		local stone = Instance.new("Part")
		stone.Anchored = true
		stone.CanCollide = false
		stone.Size = Vector3.new(1.1, 0.3, 1.1)
		stone.Position = a:Lerp(b, t)
		stone.Color = Color3.fromRGB(96, 60, 40)
		stone.Material = Enum.Material.Slate
		stone.Name = ("Chain_%s_dot"):format(kind)
		stone.Parent = model
	end
end

function EigenMapZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "EigenMap"

	-- floor over the beacon bounding box + margin
	local ex0, ex1, ey0, ey1 = EigenMap.span()
	local fx0, fz0 = EigenMap.worldFromEigen(ex0, ey1)
	local fx1, fz1 = EigenMap.worldFromEigen(ex1, ey0)
	local floor = Instance.new("Part")
	floor.Anchored = true
	floor.Size = Vector3.new(fx1 - fx0 + 2 * FLOOR_MARGIN, 1, fz1 - fz0 + 2 * FLOOR_MARGIN)
	floor.Position = Vector3.new(
		(fx0 + fx1) / 2,
		EigenMap.FLOOR_Y - 0.5,
		(fz0 + fz1) / 2
	)
	floor.Color = Color3.fromRGB(26, 24, 32)
	floor.Material = Enum.Material.Slate
	floor.Name = "EigenMap_floor"
	floor.Parent = model

	-- north needle: eigen -ey = world -Z; bearing 0 = N, clockwise
	local cx, cz = EigenMap.center()
	local cwx, cwz = EigenMap.worldFromEigen(cx, cz)
	local needleLen = (fz1 - fz0) / 2 + FLOOR_MARGIN - 8
	local needle = Instance.new("Part")
	needle.Anchored = true
	needle.CanCollide = false
	needle.Size = Vector3.new(0.4, 0.12, needleLen)
	needle.CFrame = CFrame.lookAt(Vector3.new(cwx, EigenMap.FLOOR_Y + 0.1, cwz),
		Vector3.new(cwx, EigenMap.FLOOR_Y + 0.1, cwz - needleLen))
	needle.Color = Color3.fromRGB(220, 216, 235)
	needle.Material = Enum.Material.Neon
	needle.Transparency = 0.35
	needle.Name = "North_needle"
	needle.Parent = model
	local nPost = Instance.new("Part")
	nPost.Anchored = true
	nPost.Size = Vector3.new(1.4, 5, 1.4)
	nPost.Position = Vector3.new(cwx, EigenMap.FLOOR_Y + 2.5, cwz - needleLen - 4)
	nPost.Color = Color3.fromRGB(220, 216, 235)
	nPost.Material = Enum.Material.Marble
	nPost.Name = "North_post"
	nPost.Parent = model
	tag(nPost, "N\nnorth = -Z · bearing 0 = N, clockwise", Color3.fromRGB(230, 224, 196), 13)

	-- beacons at their eigen centroids
	local pos: { [string]: Vector3 } = {}
	for _, r in ipairs(EigenMap.regions()) do
		local p = EigenMap.worldPos(r.name)
		pos[r.name] = p
		beacon(model, r.name, p.X, p.Z)
	end

	-- the water_first chain, stamped by the wired graph
	for _, seg in ipairs(EigenMap.chain()) do
		local a, b = pos[seg.a], pos[seg.b]
		if a and b then
			chainBeam(model, a.X, a.Z, b.X, b.Z, seg.kind)
			if seg.kind ~= "wired" then
				-- name the debt at the segment midpoint, not in a caption
				local mid = (a + b) / 2
				local debt = Instance.new("Part")
				debt.Anchored = true
				debt.CanCollide = false
				debt.Size = Vector3.new(2, 2, 2)
				debt.Position = Vector3.new(mid.X, EigenMap.FLOOR_Y + 0.8, mid.Z)
				debt.Transparency = 1
				debt.Name = ("Chain_missing_%s_%s"):format(seg.a, seg.b)
				debt.Parent = model
				tag(debt, ("%s -> %s\nmissing stitch: no wired edge\nbuild debt, metered")
					:format(seg.a, seg.b), Color3.fromRGB(235, 120, 90), 12)
			end
		end
	end

	-- the plaques: what the map is, what it honestly lacks
	local southZ = fz1 + FLOOR_MARGIN - 10
	local plaques: { { title: string, body: string, dx: number } } = {
		{ dx = -70, title = "THE MAP",
			body = "regions at their eigen_centroids\ntop-2 singular directions, doctrine corpus\nscan %s\nsha256 %s\n%d studs per eigen unit · north = -Z",
		},
		{ dx = 0, title = "WHAT IT LACKS",
			body = "off-map, no eigen centroid:\n%s\nwired beta0 %d vs intended %d:\n3 islands until the river-ford loop\nis hand-wired (scan finding)",
		},
		{ dx = 70, title = "THE LEAN",
			body = "water_first is the operative lean\nreferee 0.6: a LEAN, not a proof\nRIB descent order stays CONTESTED\nwatch/inbox/REFEREE_VERDICT_20260926.md",
		},
	}
	local ts, sha = EigenMap.scanStamp()
	local wired, intended = EigenMap.beta0()
	local offList = table.concat(EigenMap.offMap(), ", ")
	for _, pl in ipairs(plaques) do
		local stone = Instance.new("Part")
		stone.Anchored = true
		stone.Size = Vector3.new(56, 7, 1.2)
		stone.Position = Vector3.new(cwx + pl.dx, EigenMap.FLOOR_Y + 3.5, southZ)
		stone.Color = Color3.fromRGB(40, 37, 48)
		stone.Material = Enum.Material.Slate
		stone.Name = ("Plaque_%s"):format((pl.title:gsub("%W", "_")))
		stone.Parent = model
		local body = pl.body
		if pl.title == "THE MAP" then
			body = body:format(ts:sub(1, 10), sha:sub(1, 12), EigenMap.STUDS_PER_UNIT)
		elseif pl.title == "WHAT IT LACKS" then
			body = body:format(offList, wired, intended)
		end
		tag(stone, ("%s\n%s"):format(pl.title, body), Color3.fromRGB(217, 200, 150), 13)
	end

	model.Parent = workspace
	return model
end

return EigenMapZone
