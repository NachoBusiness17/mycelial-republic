--!strict
-- MudBasecamp — the Roshomon MUD as a place. Rooms = fleet systems (game_mud.v2),
-- exits = portal pads, and the two mechanics that make it ours:
--   survey — the party of AI heads witnesses the same scene; >=2 agree = CORE = loot
--   claim  — fold the room's core as an invariant (attribute + ledger row)
-- Plus the Hall of Shared Supper: Vellum's grant, the six chairs, the counting.
-- The hall files which you chose (ShadowLedger). Death speaks in CAPS.

local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Lore = require(Shared:WaitForChild("Lore"))
local Trove = require(Shared:WaitForChild("Trove"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))
local NpcGateway = require(script.Parent:WaitForChild("NpcGateway"))
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Worldgen = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("Worldgen"))
local SeedRng = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("SeedRng"))
local ProceduralBody = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("ProceduralBody"))
local Temptation = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("Temptation"))

local MudBasecamp = {}
local origin = Vector3.new(0, 8, 0)
local roomPlots: { [string]: Vector3 } = {}
local CENTER = "the World-Memory"

-- chat relay (Q-037, the client remotes pass): say() rides the Chat remote to
-- the speaking player's HUD. Bound by init.server after the Remotes folder is
-- built; unbound say() keeps the Studio print so nothing depends on call order
-- (build() runs before the remotes exist at init).
local chatRelay: RemoteEvent? = nil

function MudBasecamp.bindChat(remote: RemoteEvent)
	chatRelay = remote
end

local function say(player: Player, text: string)
	print(("[Basecamp] %s hears: %s"):format(player.Name, text))
	local relay = chatRelay
	if relay then
		relay:FireClient(player, text)
	end
end

local function portalPad(fromRoom: string, toRoom: string, pos: Vector3): Part
	local pad = Instance.new("Part")
	pad.Anchored = true
	pad.Size = Vector3.new(6, 0.4, 6)
	pad.Position = pos
	pad.Color = Color3.fromRGB(90, 80, 140)
	pad.Material = Enum.Material.Neon
	pad.Name = ("To_%s"):format(toRoom)
	pad.Parent = workspace

	pad.Touched:Connect(function(hit)
		local char = hit.Parent
		local player = char and Players:GetPlayerFromCharacter(char)
		if player and char then
			local dest = roomPlots[toRoom]
			if dest then
				(char :: Model):PivotTo(CFrame.new(dest + Vector3.new(0, 4, 0)))
				ShadowLedger.record(player, "Basecamp", ("walked %s -> %s"):format(fromRoom, toRoom))
			end
		end
	end)
	return pad
end

local function buildRoom(name: string, pos: Vector3): Part
	local spec = Lore.Rooms[name]
	local floor = Instance.new("Part")
	floor.Anchored = true
	floor.Size = Vector3.new(44, 1, 44)
	floor.Position = pos
	floor.Color = (name == "the Hall of Shared Supper") and Color3.fromRGB(64, 50, 40) or Color3.fromRGB(28, 27, 34)
	floor.Material = Enum.Material.Slate
	floor.Name = ("Room_%s"):format(name)
	floor.Parent = workspace

	local plaque = Instance.new("Part")
	plaque.Anchored = true
	plaque.Size = Vector3.new(14, 5, 0.5)
	plaque.Position = pos + Vector3.new(0, 6, -21)
	plaque.Color = Color3.fromRGB(18, 17, 22)
	plaque.Parent = floor.Parent
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Back
	gui.PixelsPerStud = 12
	local t1 = Instance.new("TextLabel")
	t1.Size = UDim2.new(1, 0, 0.4, 0)
	t1.BackgroundTransparency = 1
	t1.Text = name:upper()
	t1.TextColor3 = Color3.fromRGB(226, 219, 190)
	t1.Font = Enum.Font.Garamond
	t1.TextSize = 28
	t1.Parent = gui
	local t2 = Instance.new("TextLabel")
	t2.Position = UDim2.fromScale(0, 0.4)
	t2.Size = UDim2.new(1, 0, 0.6, 0)
	t2.BackgroundTransparency = 1
	t2.TextWrapped = true
	t2.Text = (spec.role .. "  ·  SURVEY: ") .. spec.question
	t2.TextColor3 = Color3.fromRGB(190, 184, 164)
	t2.Font = Enum.Font.Garamond
	t2.TextSize = 12
	t2.Parent = gui
	gui.Parent = plaque
	plaque.Parent = workspace

	local surveyPrompt = Instance.new("ProximityPrompt")
	surveyPrompt.ActionText = "Survey"
	surveyPrompt.ObjectText = "witness this scene"
	surveyPrompt.HoldDuration = 2
	surveyPrompt.MaxActivationDistance = 10
	surveyPrompt.Parent = plaque
	surveyPrompt.Triggered:Connect(function(player: Player)
		MudBasecamp.survey(player, name)
	end)

	return floor
end

-- The Hall: six chairs, Vellum, the choice.
local function buildHall(parent: Model, pos: Vector3)
	for i = 1, 6 do
		local chair = Instance.new("Part")
		chair.Anchored = true
		chair.Size = Vector3.new(2, 4, 2)
		chair.Position = pos + Vector3.new(-10 + (i - 1) * 4, 3, -6)
		chair.Color = Color3.fromRGB(70, 56, 44)
		chair.Material = Enum.Material.Wood
		chair.Name = ("EmptyChair_%d"):format(i)
		chair.Parent = parent
	end

	local vellum = Instance.new("Part")
	vellum.Anchored = true
	vellum.Shape = Enum.PartType.Ball
	vellum.Size = Vector3.new(3, 3, 3)
	vellum.Position = pos + Vector3.new(0, 3.5, 6)
	vellum.Color = Color3.fromRGB(214, 204, 176)
	vellum.Material = Enum.Material.SmoothPlastic
	vellum.Name = "BrotherVellum"
	vellum.Parent = parent

	local grant = Instance.new("ProximityPrompt")
	grant.ActionText = "Sign the Grant"
	grant.ObjectText = "Brother Vellum, of the Open Hand"
	grant.HoldDuration = 1
	grant.Parent = vellum
	grant.Triggered:Connect(function(player: Player)
		if player:GetAttribute("SkipVellum") then
			say(player, "You have already bought your way past the waiting. The counting is handled.")
			return
		end
		if player:GetAttribute("SignedGrant") then
			say(player, "Your name is already on the Grant. It does not need you twice.")
			return
		end
		-- DF villain law (WORLDGEN_MINE.md #5): the grant is a plot template and
		-- signing is a temptation roll against the player's values; the counted
		-- chairs are the spine. Failure to resist becomes ongoing corruption.
		local rng = SeedRng.new(os.clock() * 1000 // 1)
		local succumbed, roll, threshold = Temptation.roll(rng, "grant_of_belonging", Temptation.profile(player))
		if succumbed then
			player:SetAttribute("SignedGrant", true)
			player:SetAttribute("Corrupted", true)
			ShadowLedger.record(player, "Basecamp",
				("succumbed to the Grant (temptation %d vs resolve %d): the Open Hand holds a finger")
					:format(roll, threshold), false)
			say(player, Lore.Vellum.grantOffer)
		else
			ShadowLedger.record(player, "Basecamp",
				("felt the pull of the Grant and resisted it (temptation %d vs resolve %d)")
					:format(roll, threshold), true)
			say(player, ("The Open Hand opens and you step back from it. The chairs stay counted. (temptation %d vs resolve %d)"):format(roll, threshold))
		end
	end)

	local count = Instance.new("ProximityPrompt")
	count.ActionText = "Count the empty chairs"
	count.ObjectText = "the long supper table"
	count.HoldDuration = 1.5
	count.Parent = vellum
	count.Triggered:Connect(function(player: Player)
		local marks = tonumber((player:GetAttribute("VirtueMarks")) or 0) + 1
		local dbl = player:GetAttribute("VirtueDoublerUntil")
		if dbl and os.time() < dbl then marks += 1 end
		player:SetAttribute("VirtueMarks", marks)
		player:SetAttribute("CountedChairs", true)
		ShadowLedger.record(player, "Basecamp", "counted the six empty chairs and refused to sign", true)
		say(player, Lore.Vellum.ifCounted .. ("  Virtue Marks: %d. Now they come."):format(marks))
		MudBasecamp.summonWisps(pos, player)
	end)
end

-- "Speak the count aloud and they come."
function MudBasecamp.summonWisps(pos: Vector3, target: Player)
	local rng = SeedRng.new(os.clock() * 1000 // 1)
	for i = 1, 3 do
		-- forgotten-beast law: the world pauses when one is first seen
		-- (announcement carries the DF attack warning), and the body is
		-- ASSEMBLED per the mined RCP chain, never a plain ball anymore
		local bodySpec = ProceduralBody.assemble(rng)
		-- kinship law (WORLDGEN_MINE.md #4): the beast's sphere decides which
		-- zones ally with it and which oppose it, from the generated graph
		local beast = Worldgen.forgottenBeast(rng)
		print(("[FORGOTTEN] %s has come: a %s. It is drawn by wealth and noise. %s %s")
			:format(beast.name, bodySpec.description, bodySpec.warning, Worldgen.kinshipLine(beast)))
		local wisp = Instance.new("Part")
		wisp.Anchored = false
		wisp.Shape = Enum.PartType.Ball
		wisp.Size = Vector3.new(1.4, 1.4, 1.4)
		wisp.Material = Enum.Material.Neon
		wisp.Color = Color3.fromRGB(140, 60, 200)
		wisp.Position = pos + Vector3.new(math.cos(i * 2.1) * 30, 10, math.sin(i * 2.1) * 30)
		local body = ProceduralBody.build(bodySpec, wisp) -- welded limbs, massless: one assembly
		wisp.Parent = body
		body.Parent = workspace
		local touchConn
		touchConn = wisp.Touched:Connect(function(hit)
			local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
			if player and player.Character then
				player.Character:BreakJoints()
				touchConn:Disconnect()
				body:Destroy()
			end
		end)
		-- Q-043 Trove pass: the hunt is OWNED by the terror's body
		-- (AttachToInstance -> Destroying -> Clean cancels the thread), not by
		-- its 30s age. The 30s cap stays as game behavior but enforces itself
		-- by destroying the body (the false return ends the thread); an early
		-- destroy (the Touched kill above) cancels the hunt immediately
		-- instead of leaving it polling body.Parent for up to 30s.
		local t0 = os.clock()
		local trove = Trove.new()
		trove:AttachToInstance(body)
		trove:Loop(0.1, function()
			if not body.Parent then return false end
			if os.clock() - t0 >= 30 then
				body:Destroy()
				return false
			end
			-- B2-110 (2026-09-26): FindFirstChild types Instance?; cast narrows to
			-- BasePart? so hum.Position below stops tripping luau-lsp
			-- "Key 'Position' not found in external type 'Instance'" at (220,19).
			local hum = target.Character and target.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if hum then
				local dir = (hum.Position - wisp.Position)
				if dir.Magnitude > 2 then
					wisp.AssemblyLinearVelocity = dir.Unit * 14
				end
			end
			return true
		end)
	end
end

-- survey: the party witnesses the same scene; converge = core, diverge = swarm log
function MudBasecamp.survey(player: Player, room: string)
	local spec = Lore.Rooms[room]
	if not spec then return end
	ShadowLedger.record(player, "Basecamp", ("surveyed %s"):format(room), true)

	-- Mooncast law (LINKS-335): same-model councils agree too cheaply. The three
	-- witnesses run on THREE DIFFERENT families (stealth + inclusionai + poolside),
	-- all $0, so ROSHOMON CORE (>=2 agree) measures convergence, not consistency.
	local WITNESS_MODELS = {
		"stealth/space-bunny-alpha",
		"inclusionai/ling-3.0-flash-sante:free",
		"poolside/laguna-s-2.1:free",
	}
	local answers: { string } = {}
	for i, h in ipairs(Lore.Heads) do
		if i > 3 then break end -- three seats per survey; free lanes, paced
		local reply, isLive = NpcGateway.ask(h.id, player.Name,
			("Describe this scene and answer: %s"):format(spec.question), room, WITNESS_MODELS[i])
		if isLive then table.insert(answers, reply) end
	end

	local core: { string } = {}
	if #answers >= 2 then
		-- token overlap: content words shared by >=2 witnesses
		local tokens: { [string]: number } = {}
		for _, a in ipairs(answers) do
			local seen: { [string]: boolean } = {}
			for word in string.gmatch(string.lower(a), "%a+") do
				if #word > 4 and not seen[word] then
					seen[word] = true
					tokens[word] = (tokens[word] or 0) + 1
				end
			end
		end
		for word, n in pairs(tokens) do
			if n >= 2 then table.insert(core, word) end
		end
	end

	if #core > 0 then
		local invariants = tonumber((player:GetAttribute("Invariants")) or 0) + #core
		player:SetAttribute("Invariants", invariants)
		say(player, string.format("ROSHOMON CORE (%d witnesses agree): {%s}  -> folded. Invariants: %d",
			#core, table.concat(core, ", "), invariants))
	else
		say(player, "No core. The accounts diverge — routed to the swarm. The room keeps its question.")
		ShadowLedger.record(player, "Basecamp", ("novel-divergence in %s routed to swarm"):format(room))
	end
end

-- Grow-a-Garden wheel: one plot per player at the Warm Springs. Growth runs
-- on server timestamps, so it ripens while you are offline (docs §3.6):
-- 30 min → Spring Herb (5 VM), 8 h → Moon Bloom (25 VM).
local HERB_MIN, BLOOM_H = 30, 8

local function buildGarden(model: Model)
	local springs = roomPlots["the Warm Springs"]
	if not springs then return end

	for i = 1, 4 do
		local plot = Instance.new("Part")
		plot.Anchored = true
		plot.Size = Vector3.new(8, 0.4, 8)
		plot.Position = springs + Vector3.new(-12 + (i - 1) * 8, 0.7, 16)
		plot.Color = Color3.fromRGB(70, 90, 60)
		plot.Material = Enum.Material.Grass
		plot.Name = ("Plot_%d"):format(i)
		plot.Parent = model

		local prompt = Instance.new("ProximityPrompt")
		prompt.ObjectText = "garden plot"
		prompt.HoldDuration = 0.5
		prompt.Parent = plot

		local function refresh(pl: Player)
			local plantedAt = pl:GetAttribute(("Plot%d"):format(i))
			if not plantedAt then
				prompt.ActionText = "Plant a Virtue Seed"
			else
				local elapsedMin = (os.time() - plantedAt) / 60
				if elapsedMin >= BLOOM_H * 60 then
					prompt.ActionText = "Harvest the Moon Bloom (25 VM)"
				elseif elapsedMin >= HERB_MIN then
					prompt.ActionText = "Harvest the Spring Herb (5 VM)"
				else
					prompt.ActionText = ("growing... %d min left"):format(math.ceil(HERB_MIN - elapsedMin))
				end
			end
		end

		prompt.Triggered:Connect(function(pl: Player)
			local plantedAt = pl:GetAttribute(("Plot%d"):format(i))
			if not plantedAt then
				pl:SetAttribute(("Plot%d"):format(i), os.time())
				ShadowLedger.record(pl, "Basecamp", "planted a Virtue Seed at the Warm Springs", true)
			else
				local elapsedMin = (os.time() - plantedAt) / 60
				if elapsedMin >= BLOOM_H * 60 then
					pl:SetAttribute("VirtueMarks", tonumber((pl:GetAttribute("VirtueMarks")) or 0) + 25)
					pl:SetAttribute(("Plot%d"):format(i), nil)
				elseif elapsedMin >= HERB_MIN then
					pl:SetAttribute("VirtueMarks", tonumber((pl:GetAttribute("VirtueMarks")) or 0) + 5)
					pl:SetAttribute(("Plot%d"):format(i), nil)
				else
					return -- not ready; the plot teaches patience
				end
			end
			refresh(pl)
		end)

		-- t63 2026-09-25: the 10s GetPlayers poll is gone, cured like t56's
		-- leaderstats poll (init.server.luau:184-196). The label data rides the
		-- player's Plot<i> attribute; sole writer is this prompt's own Triggered
		-- handler (:326 set, :332/:335 removal) and every one of those paths
		-- already refreshes at :340, so GetAttributeChangedSignal("Plot"..i)
		-- exists to bind future or external writers. First-add firing per the
		-- official attributes doc example ("Fires Changed, AttributeChanged, and
		-- GetAttributeChangedSignal()", fetched 2026-09-25); removal firing is
		-- not doc-stated but is not load-bearing because :340 covers this
		-- file's own writes. Negative, first-class: the "growing... min left"
		-- countdown and the HERB_MIN/BLOOM_H label flips derive from wall-clock
		-- time, which fires no signal. Instead of ticking every plot every 10s
		-- forever, the plant write schedules two one-shot wakeups at exactly
		-- those deadlines (wake at the deadline, not polling); a stale wakeup
		-- after harvest or replant is dropped by the plantedAt guard. The
		-- minute count is only refreshed at the write events and on prompt
		-- engagement (PromptButtonHoldBegan), not continuously; that cosmetic
		-- staleness is accepted in exchange for zero standing timers. Seed at
		-- attach paints the initial label the poll used to cover in 10s.
		local function onPlotChanged(pl: Player)
			refresh(pl)
			local plantedAt = pl:GetAttribute(("Plot%d"):format(i))
			if plantedAt then
				local age = os.time() - plantedAt
				for _, thresholdSec in ipairs({ HERB_MIN * 60, BLOOM_H * 3600 }) do
					local wakeIn = thresholdSec - age
					if wakeIn > 0 then
						task.delay(wakeIn, function()
							if pl.Parent and pl:GetAttribute(("Plot%d"):format(i)) == plantedAt then
								refresh(pl)
							end
						end)
					end
				end
			end
		end

		local function attach(pl: Player)
			refresh(pl)
			prompt.PromptButtonHoldBegan:Connect(function()
				refresh(pl)
			end)
			pl:GetAttributeChangedSignal(("Plot%d"):format(i)):Connect(onPlotChanged)
		end
		Players.PlayerAdded:Connect(attach)
		for _, p in ipairs(Players:GetPlayers()) do
			attach(p)
		end
	end
end

function MudBasecamp.build(): Model
	local model = Instance.new("Model")
	model.Name = "MudBasecamp"

	-- ring layout: rooms on a circle around the Hall
	local names = {}
	for name in pairs(Lore.Rooms) do table.insert(names, name) end
	table.sort(names)
	for i, name in ipairs(names) do
		local angle = ((i - 1) / #names) * math.pi * 2
		local pos = origin + Vector3.new(math.cos(angle) * 130, 8, math.sin(angle) * 130)
		roomPlots[name] = pos
		buildRoom(name, pos).Parent = model
	end
	roomPlots[CENTER] = origin -- World-Memory at the center

	-- exits -> portal pads (graph from Lore)
	for name, spec in pairs(Lore.Rooms) do
		local from = roomPlots[name]
		local seen: { [string]: boolean } = {}
		for _, dest in pairs(spec.exits) do
			if not seen[dest] and roomPlots[dest] then
				seen[dest] = true
				portalPad(name, dest, from + Vector3.new(0, 0.7, 16)).Parent = model
			end
		end
	end

	buildHall(model, origin)
	buildGarden(model)

	-- Death speaks in CAPS (the Pratchett crosswalk)
	Players.PlayerAdded:Connect(function(player)
		player.CharacterAdded:Connect(function(char)
			local hum = char:WaitForChild("Humanoid") :: Humanoid
			hum.Died:Connect(function()
				print(("[DEATH] %s. %s"):format(Lore.Death.format(player.Name, "THE MOUNTAIN"), Lore.Death.opening))
			end)
		end)
	end)

	model.Parent = workspace
	return model
end

return MudBasecamp
