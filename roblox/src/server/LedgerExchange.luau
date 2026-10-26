--!strict
-- LedgerExchange — the Steal-a economy, cloned 1:1 onto the estate (numbers
-- and sources in docs/CLONED_MECHANICS.md §3.1). The Marble Run conveyor
-- spawns artifacts; buy with Virtue Marks; slots tick income; steal from an
-- unlocked neighbor's alcove and run it home under the full carry penalty;
-- lock your alcove from the Counting Circle; rebirth at 5,000 VM.
--
--   rarities: common 50 VM / +1 per 10s · rare 200 / +5 · epic 800 / +20 · legendary 3000 / +80
--   slots 4 (+2 per rebirth) · lock 60s (+10s per rebirth) · shield 1 per 5 min
--   carry penalty: speed x0.6, abilities disabled, owner notified, +10s their lock
--   rebirth 5000 VM: slots reset, x1.5 income, pet orb hatched (swarm auto-collect)

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local Shared = ReplicatedStorage:WaitForChild("Modules")
local SeedRng = require(Shared:WaitForChild("SeedRng"))
local ArtifactLore = require(Shared:WaitForChild("ArtifactLore"))
local DfValue = require(Shared:WaitForChild("DfValue"))
local Trove = require(Shared:WaitForChild("Trove"))
local ServerScriptService = game:GetService("ServerScriptService")
local ShadowLedger = require(ServerScriptService:WaitForChild("ShadowLedger"))

local LedgerExchange = {}
local CONVEYOR_Z, RAIL_HALF = 96, 42
local RNG = SeedRng.new(20260924)

local ARTIFACTS = {
	{ name = "Chair Nail",           rarity = "common",    cost = 50,   income = 1,  color = Color3.fromRGB(160, 140, 100) },
	{ name = "Salt Scraps",          rarity = "common",    cost = 50,   income = 1,  color = Color3.fromRGB(220, 220, 210) },
	{ name = "Vellum's Pen",         rarity = "rare",      cost = 200,  income = 5,  color = Color3.fromRGB(200, 180, 90) },
	{ name = "Bard's Lyre",          rarity = "rare",      cost = 200,  income = 5,  color = Color3.fromRGB(140, 170, 220) },
	{ name = "Locked Eye",           rarity = "epic",      cost = 800,  income = 20, color = Color3.fromRGB(170, 60, 200) },
	{ name = "A page of the Answer", rarity = "legendary", cost = 3000, income = 80, color = Color3.fromRGB(240, 240, 250) },
}

local SLOTS_BASE, LOCK_BASE, LOCK_PER_REBIRTH, REBIRTH_AT = 4, 60, 10, 5000
local pads: { [Player]: BasePart } = {}
local lockUntil: { [Player]: number } = {}

local function slots(player: Player): number
	return SLOTS_BASE + 2 * tonumber((player:GetAttribute("Rebirths")) or 0)
end

local function firstFreeSlot(player: Player): number?
	for slot = 1, slots(player) do
		if not player:GetAttribute(("Slot%d"):format(slot)) then return slot end
	end
	return nil
end

local function stashArtifact(player: Player, name: string, income: number, dfValue: number?)
	local slot = firstFreeSlot(player)
	if not slot then return false end
	player:SetAttribute(("Slot%d"):format(slot), income)
	player:SetAttribute(("Slot%dName"):format(slot), name)
	-- the dwarven appraisal rides the slot (DF value law); bought pieces carry
	-- it, run-home steals re-carry it so the appraisal survives resale
	if dfValue then
		player:SetAttribute(("Slot%dDf"):format(slot), dfValue)
	end
	return true
end

-- ---- the Marble Run ----
local function spawnOnConveyor()
	local spec = ARTIFACTS[RNG:int(1, #ARTIFACTS)]
	local a = Instance.new("Part")
	a.Size = Vector3.new(2.4, 2.4, 2.4)
	a.Color = spec.color
	a.Material = (spec.rarity == "legendary") and Enum.Material.Neon or Enum.Material.SmoothPlastic
	a.Position = Vector3.new(-RAIL_HALF, 5, CONVEYOR_Z)
	a.Name = "Artifact"
	a:SetAttribute("ArtifactName", spec.name)
	a:SetAttribute("ArtifactCost", spec.cost)
	a:SetAttribute("ArtifactIncome", spec.income)

	-- dwarven lore (DF wiki mine, LINKS-341): every artifact carries a real
	-- dwarven compound name and a strange-mood history line
	local dwName = ArtifactLore.name(RNG)
	local moodLine = ArtifactLore.moodLine(RNG, "the hall", spec.name)
	a:SetAttribute("ArtifactDwarven", dwName)

	-- DF value law (WORLDGEN_MINE.md #8): the dwarven appraisal rides every
	-- piece; the cloned VM cost above is untouched by it
	local appraisal = DfValue.appraise(RNG)
	a:SetAttribute("ArtifactDfValue", appraisal.value)
	a:SetAttribute("ArtifactDfText", appraisal.text)

	local bill = Instance.new("BillboardGui")
	bill.Size = UDim2.new(0, 150, 0, 66)
	bill.StudsOffset = Vector3.new(0, 2, 0)
	local t = Instance.new("TextLabel")
	t.Size = UDim2.fromScale(1, 1)
	t.BackgroundTransparency = 1
	t.TextWrapped = true
	t.Text = ("%s\n%s\n%d VM · +%d/10s\n%s"):format(spec.name, dwName, spec.cost, spec.income, appraisal.text)
	t.TextColor3 = spec.color
	t.Font = Enum.Font.Garamond
	t.TextSize = 11
	t.Parent = bill
	bill.Parent = a

	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = ("Buy (%d VM)"):format(spec.cost)
	prompt.ObjectText = spec.name
	prompt.HoldDuration = 0.5
	prompt.Parent = a
	prompt.Triggered:Connect(function(player: Player)
		if a.Parent == nil then return end
		local vm = tonumber(player:GetAttribute("VirtueMarks")) or 0
		if vm < spec.cost then return end
		if not stashArtifact(player, spec.name, spec.income, appraisal.value) then return end -- alcove full
		player:SetAttribute("VirtueMarks", vm - spec.cost)
		a:Destroy()
		ShadowLedger.record(player, "Basecamp", ("bought %s — %s. %s"):format(spec.name, dwName, moodLine), true)
	end)

	a.Parent = workspace
	-- Q-043 Trove pass: the conveyor slide is owned by the artifact's lifetime
	-- (AttachToInstance -> Destroying -> Clean). The body ends the thread
	-- itself with a false return (past the rail, or the artifact bought and
	-- destroyed under it); a Clean cancel landing on this running thread is a
	-- pcall'd no-op, so the false return is always the real exit — nothing
	-- spins and nothing dies by age.
	local trove = Trove.new()
	trove:AttachToInstance(a)
	trove:Loop(0.1, function()
		if not a.Parent then return false end
		a.Position += Vector3.new(2, 0, 0)
		if a.Position.X > RAIL_HALF then
			a:Destroy()
			return false
		end
		return true
	end)
end

-- ---- alcoves ----
local function notify(player: Player, text: string)
	local pad = pads[player]
	if not pad then return end
	local old = pad:FindFirstChild("Notify")
	if old then old:Destroy() end
	local bill = Instance.new("BillboardGui")
	bill.Name = "Notify"
	bill.Size = UDim2.new(0, 220, 0, 34)
	bill.StudsOffset = Vector3.new(0, 8, 0)
	bill.AlwaysOnTop = true
	local t = Instance.new("TextLabel")
	t.Size = UDim2.fromScale(1, 1)
	t.BackgroundTransparency = 1
	t.Text = text
	t.TextColor3 = Color3.fromRGB(240, 120, 120)
	t.Font = Enum.Font.Garamond
	t.TextSize = 14
	t.Parent = bill
	bill.Parent = pad
	task.delay(5, function() if bill.Parent then bill:Destroy() end end)
end

local function buildAlcove(player: Player, index: number)
	local pos = Vector3.new((index - 5) * 24, 8, 40)

	local pad = Instance.new("Part")
	pad.Anchored = true
	pad.Size = Vector3.new(16, 0.5, 16)
	pad.Position = pos
	pad.Color = Color3.fromRGB(46, 42, 52)
	pad.Material = Enum.Material.Slate
	pad.Name = player.Name .. "_Alcove"
	pad:SetAttribute("Owner", player.Name)
	pad.Parent = workspace
	pads[player] = pad

	local circle = Instance.new("Part")
	circle.Anchored = true
	circle.Shape = Enum.PartType.Cylinder
	circle.Size = Vector3.new(0.4, 6, 6)
	circle.CFrame = CFrame.new(pos + Vector3.new(0, 0.6, 10)) * CFrame.Angles(0, 0, math.rad(90))
	circle.Color = Color3.fromRGB(230, 200, 60)
	circle.Material = Enum.Material.Neon
	circle.Parent = workspace

	local lock = Instance.new("ProximityPrompt")
	lock.ActionText = "Lock the alcove"
	lock.ObjectText = "the Counting Circle"
	lock.HoldDuration = 0.5
	lock.Parent = circle
	lock.Triggered:Connect(function(p: Player)
		if p ~= player then return end -- only the owner locks their own circle
		lockUntil[player] = os.clock() + LOCK_BASE + LOCK_PER_REBIRTH * tonumber((player:GetAttribute("Rebirths")) or 0)
	end)

	local rebirth = Instance.new("ProximityPrompt")
	rebirth.ActionText = ("REBIRTH (%d VM)"):format(REBIRTH_AT)
	rebirth.ObjectText = "fold your ledger"
	rebirth.HoldDuration = 3
	rebirth.Parent = circle

	rebirth.Triggered:Connect(function(p: Player)
		if p ~= player then return end
		if tonumber((p:GetAttribute("VirtueMarks")) or 0) < REBIRTH_AT then return end
		p:SetAttribute("VirtueMarks", tonumber((p:GetAttribute("VirtueMarks")) or 0) - REBIRTH_AT)
		p:SetAttribute("Rebirths", tonumber((p:GetAttribute("Rebirths")) or 0) + 1)
		p:SetAttribute("PetOrb", true) -- Pet-Sim wheel: the orb auto-grinds for you
		for slot = 1, 32 do
			p:SetAttribute(("Slot%d"):format(slot), nil)
		end
		ShadowLedger.record(p, "Basecamp", "rebirthed: the ledger folds, the alcove empties, an orb hatches", true)
		notify(p, "THE LEDGER FOLDS. SOMETHING SMALL HATCHES AND FOLLOWS YOU.")
	end)

	-- steal: take from an unlocked neighbor's pad
	local steal = Instance.new("ProximityPrompt")
	steal.ActionText = "Borrow (steal)"
	steal.ObjectText = player.Name .. "'s alcove"
	steal.HoldDuration = 1
	steal.MaxActivationDistance = 12
	steal.Parent = pad
	steal.Triggered:Connect(function(thief: Player)
		if thief == player then return end
		if (lockUntil[player] or 0) > os.clock() then return end -- locked: immune
		-- take the highest-income filled slot
		local bestSlot, bestIncome = nil, -1
		for slot = 1, slots(player) do
			-- type pin t66 (receipt: watch/inbox/gala_20260925/afterparty/lanes/t58.check.txt, LedgerExchange 217,13 + 217,62): GetAttribute reads unknown, stashArtifact writes income: number, tonumber is identity on a stored number. Runtime unchanged.
			local v = tonumber(player:GetAttribute(("Slot%d"):format(slot)))
			if v and v > bestIncome then bestSlot, bestIncome = slot, v end
		end
		if not bestSlot then return end -- nothing worth taking
		-- type pin t66 (receipt: t58.check.txt, LedgerExchange 228,86 + 229,73): Slot%dName is written as name: string, tostring is identity on a stored string, and the nil case already fell to "loot". Runtime unchanged.
		local name = tostring(player:GetAttribute(("Slot%dName"):format(bestSlot)) or "loot")
		local carriedDf = tonumber((player:GetAttribute(("Slot%dDf"):format(bestSlot)))) -- appraisal travels with the piece
		player:SetAttribute(("Slot%d"):format(bestSlot), nil)
		player:SetAttribute(("Slot%dDf"):format(bestSlot), nil)
		thief:SetAttribute("Carrying", true) -- speed x0.6 + abilities disabled (PlayerFeel/AbilitySlots read this)
		thief:SetAttribute("CarryingName", name)
		thief:SetAttribute("CarryingFrom", player.Name)
		thief:SetAttribute("CarryingDf", carriedDf)
		notify(player, ("THE %s TAKES YOUR %s. RUN THEM DOWN."):format(thief.Name:upper(), name:upper()))
		ShadowLedger.record(thief, "Basecamp", ("borrowed %s from %s"):format(name, player.Name))
	end)

	-- deposit / defense: touching your own pad drops the carrier
	pad.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if not plr then return end
		if plr == player and plr:GetAttribute("Carrying") then
			local name = plr:GetAttribute("CarryingName") or "loot"
			-- the run-home income is the dwarven appraisal, banded 1..80
			-- (DfValue.vmIncome; a carry without an appraisal lands at the floor)
			local dfValue = tonumber((plr:GetAttribute("CarryingDf"))) or 0
			if stashArtifact(plr, name, DfValue.vmIncome(dfValue), dfValue > 0 and dfValue or nil) then
				plr:SetAttribute("Carrying", nil)
				plr:SetAttribute("CarryingName", nil)
				local victimName = plr:GetAttribute("CarryingFrom")
				local victim = victimName and Players:FindFirstChild(victimName)
				if victim then
					lockUntil[victim] = math.max(lockUntil[victim] or 0, os.clock()) + 10
					notify(victim, "YOUR LOCK TIME GREW WHILE THEY RAN.")
				end
				ShadowLedger.record(plr, "Basecamp", ("stashed %s at the alcove"):format(name), true)
			end
		end
	end)
end

-- ---- tick: conveyor + income ----
local tickAcc, spawnAcc = 0, 0

function LedgerExchange.tick(dt: number)
	spawnAcc += dt
	if spawnAcc >= 8 then
		spawnAcc = 0
		spawnOnConveyor()
	end
	tickAcc += dt
	if tickAcc >= 10 then
		tickAcc = 0
		for _, player in ipairs(Players:GetPlayers()) do
			local income = 0
			for slot = 1, slots(player) do
				local v = player:GetAttribute(("Slot%d"):format(slot))
				if v then income += v end
			end
			income = math.floor(income * (1.5 ^ tonumber((player:GetAttribute("Rebirths")) or 0)))
			player:SetAttribute("VirtueMarks", tonumber((player:GetAttribute("VirtueMarks")) or 0) + income)
			player:SetAttribute("ExchangeIncome", income)
		end
	end
end

function LedgerExchange.init()
	Players.PlayerAdded:Connect(function(player: Player)
		player:SetAttribute("VirtueMarks", 100) -- the tutorial's 100 cash, skinned
		buildAlcove(player, math.clamp(#Players:GetPlayers(), 1, 8))
	end)
	for _ = 1, 4 do
		spawnOnConveyor()
	end

	-- the Marble Run rail
	local rail = Instance.new("Part")
	rail.Anchored = true
	rail.Size = Vector3.new(RAIL_HALF * 2, 1, 4)
	rail.Position = Vector3.new(0, 3.5, CONVEYOR_Z)
	rail.Color = Color3.fromRGB(40, 36, 46)
	rail.Material = Enum.Material.DiamondPlate
	rail.Name = "TheMarbleRun"
	rail.Parent = workspace
end

return LedgerExchange
