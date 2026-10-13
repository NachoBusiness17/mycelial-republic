--!strict
-- HeadMuseum — the museum of the fleet's minds. One building at Basecamp,
-- one pedestal per persona, one head each. Talking to a head = one turn of
-- one seat over the NpcGateway (which rides the free stealth lanes).
-- The estate's first interactive exhibit of itself: the static gallery
-- (viz, particles, lattice) becomes rooms later; the heads come first.

local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Lore = require(Shared:WaitForChild("Lore"))
local Trove = require(Shared:WaitForChild("Trove"))
local NpcGateway = require(script.Parent:WaitForChild("NpcGateway"))
local Soul = require(Shared:WaitForChild("Soul")) -- was a second full service chain; Shared resolves the module type
local DataStoreService = game:GetService("DataStoreService")

local HeadMuseum = {}
local origin = Vector3.new(60, 4, 0) -- east of Basecamp center
local souls: { [string]: Soul.Soul } = {}

-- ---- soul persistence (the owed Soul.luau wiring) ----
-- DF two-stage law holds in the store: only LEDGER ROWS (emotions naming
-- their cause) and needs persist; stress and mood derive at read time and
-- are never stored as truth. One DataStore key per head.
local SOUL_STORE = "HeadMuseumSouls_v1"
local SOUL_ROWS_MAX = 60 -- the ledger keeps its most recent rows
local FLUSH_PERIOD = 30
local soulStore = DataStoreService:GetDataStore(SOUL_STORE)
-- History (receipts, negative first-class): the souls table (line 16) was
-- always Soul.Soul; the "Unknown type 'Soul.Soul'" at 16,26 was the gate's
-- repo-root analyze phantom (module files unloadable from the wrong cwd),
-- root-caused by t1d and fixed in the gate by t24 (runs 1-4, repo-root 4
-- errors vs exit 0 from roblox/; receipt:
-- watch/inbox/gala_20260925/afterparty/lanes/t1d.check.txt). That phantom was
-- the only reason these were any; with the cwd fix landed, t30 pays the owed
-- tightening (dirty table + soul params -> Soul.Soul), verified exit 0 by
-- module analyze of this file from roblox/ 2026-09-26.
local dirty: { [string]: Soul.Soul } = {}

local function soulKey(id: string): string
	return ("soul_%s"):format(id)
end

local function serialize(soul: Soul.Soul)
	local rows = {}
	local first = math.max(1, #soul.emotions - SOUL_ROWS_MAX + 1)
	for i = first, #soul.emotions do
		table.insert(rows, soul.emotions[i])
	end
	return { emotions = rows, needs = soul.needs }
end

local function flushSoul(id: string, soul: Soul.Soul)
	local ok, err = pcall(function()
		soulStore:SetAsync(soulKey(id), serialize(soul))
	end)
	if not ok then
		warn(("[HeadMuseum] soul flush failed for %s: %s"):format(id, tostring(err)))
	end
end

local function restoreSoul(id: string, soul: Soul.Soul)
	local ok, data = pcall(function()
		return soulStore:GetAsync(soulKey(id))
	end)
	if not ok then
		-- no saved ledger reachable (Studio without API access, throttle):
		-- the head starts with an empty ledger and says so; rows are never faked
		warn(("[HeadMuseum] soul load failed for %s: %s"):format(id, tostring(data)))
		return
	end
	if type(data) ~= "table" then return end -- a first-visit head: empty ledger is honest
	for _, row in ipairs(data.emotions or {}) do
		if type(row) == "table" and type(row.thought) == "string" then
			table.insert(soul.emotions, {
				thought = row.thought,
				emotion = tostring(row.emotion),
				strength = tonumber(row.strength) or 0,
				year = tonumber(row.year) or 0,
				synthetic = row.synthetic == true,
			})
		end
	end
	for _, need in ipairs(data.needs or {}) do
		if type(need) == "table" and type(need.id) == "string" then
			Soul.addNeed(soul, need.id)
			for _, n in ipairs(soul.needs) do
				if n.id == need.id then
					n.focus = math.clamp(tonumber(need.focus) or 0, -10000, 400)
				end
			end
		end
	end
end

local function plaque(text: string, pos: Vector3): Part
	local p = Instance.new("Part")
	p.Anchored = true
	p.Size = Vector3.new(6, 2, 0.4)
	p.Position = pos
	p.Color = Color3.fromRGB(24, 22, 30)
	p.Material = Enum.Material.Slate
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Front
	gui.PixelsPerStud = 24
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.fromScale(1, 1)
	lbl.BackgroundTransparency = 1
	lbl.TextWrapped = true
	lbl.TextColor3 = Color3.fromRGB(220, 214, 190)
	lbl.Font = Enum.Font.Garamond
	lbl.TextSize = 14
	lbl.Text = text
	lbl.Parent = gui
	gui.Parent = p
	return p
end

function HeadMuseum.build(): Model
	local museum = Instance.new("Model")
	museum.Name = "HeadMuseum"

	local floor = Instance.new("Part")
	floor.Anchored = true
	floor.Size = Vector3.new(60, 1, 40)
	floor.Position = origin + Vector3.new(0, -0.5, 0)
	floor.Color = Color3.fromRGB(30, 28, 36)
	floor.Material = Enum.Material.Marble
	floor.Parent = museum

	for i, spec in ipairs(Lore.Heads) do
		local angle = (i / #Lore.Heads) * math.pi * 2
		local pos = origin + Vector3.new(math.cos(angle) * 20, 2, math.sin(angle) * 12)

		local pedestal = Instance.new("Part")
		pedestal.Anchored = true
		pedestal.Size = Vector3.new(3, 3, 3)
		pedestal.Position = pos
		pedestal.Color = Color3.fromRGB(38, 34, 46)
		pedestal.Material = Enum.Material.Marble
		pedestal.Parent = museum

		local skull = Instance.new("Part")
		skull.Anchored = true
		skull.Shape = Enum.PartType.Ball
		skull.Size = Vector3.new(2.4, 2.4, 2.4)
		skull.Position = pos + Vector3.new(0, 2.7, 0)
		skull.Color = Color3.fromRGB(206, 198, 178)
		skull.Material = Enum.Material.SmoothPlastic
		skull.Parent = museum

		local billboard = Instance.new("BillboardGui")
		billboard.Size = UDim2.new(0, 240, 0, 56)
		billboard.StudsOffset = Vector3.new(0, 2.4, 0)
		billboard.AlwaysOnTop = true
		local lbl = Instance.new("TextLabel")
		lbl.Size = UDim2.fromScale(1, 1)
		lbl.BackgroundTransparency = 1
		lbl.TextWrapped = true
		lbl.Text = spec.name
		lbl.TextColor3 = Color3.fromRGB(230, 224, 196)
		lbl.Font = Enum.Font.Garamond
		lbl.TextSize = 16
		lbl.Parent = billboard
		billboard.Parent = skull

		plaque(spec.seat, pos + Vector3.new(0, -1.2, 2.4)).Parent = museum

		local prompt = Instance.new("ProximityPrompt")
		prompt.ActionText = "Speak"
		prompt.ObjectText = spec.name
		prompt.HoldDuration = 0.3
		prompt.MaxActivationDistance = 10
		prompt.Parent = skull

		-- each head carries a unit_soul: visits are emotion rows naming their
		-- cause; the ledger persists to the DataStore (loaded async below)
		souls[spec.id] = souls[spec.id] or Soul.new()
		Soul.addNeed(souls[spec.id], "witnesses")
		task.spawn(restoreSoul, spec.id, souls[spec.id])

		prompt.Triggered:Connect(function(player: Player)
			local soul = souls[spec.id]
			Soul.record(soul, player.Name .. " came to listen", "gratitude", 120, os.time())
			Soul.decayNeeds(soul, 30)
			dirty[spec.id] = soul -- flushed on the period below (and at close)
			local reply, isLive = NpcGateway.ask(spec.id, player.Name, "(approach)", "the Head Museum")
			lbl.Text = reply
			if isLive then
				-- give the answer time to be read, then return to the nameplate
				task.delay(14, function()
					lbl.Text = spec.name
				end)
			end
		end)
	end

	museum.Parent = workspace

	-- flush dirty ledgers on a slow clock, and once more at server close.
	-- Q-043 Trove pass: the loop is OWNED by the museum's lifetime
	-- (AttachToInstance -> Destroying -> Clean cancels the thread) instead of
	-- polling museum.Parent. Cadence is identical: dirty starts empty, so the
	-- Loop body's immediate first run flushes nothing, exactly like the old
	-- wait-first first cycle.
	local trove = Trove.new()
	trove:AttachToInstance(museum)
	trove:Loop(FLUSH_PERIOD, function()
		for id, soul in pairs(dirty) do
			dirty[id] = nil
			flushSoul(id, soul)
		end
	end)
	game:BindToClose(function()
		for id, soul in pairs(dirty) do
			dirty[id] = nil
			flushSoul(id, soul)
		end
	end)

	return museum
end

return HeadMuseum
