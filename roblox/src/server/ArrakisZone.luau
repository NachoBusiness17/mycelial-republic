--!strict
-- ArrakisZone — the riding sim. Translated from arrakis.html laws:
-- "speed is score · spice chains are the line · crests are arcs · the Maker
-- hunts the fast · E drops a thumper (3) · the slow are safe and the safe are poor"
-- Touch a gate to bank everything. Spice chained without stopping = LINE xN.

local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Config = require(Shared:WaitForChild("Config"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))

local ArrakisZone = {}
local origin = Vector3.new(120, 8, -120)
local SIZE = 220

local spawners: { () -> () } = {}

local function spawnSpice()
	local s = Instance.new("Part")
	s.Shape = Enum.PartType.Ball
	s.Size = Vector3.new(2.5, 2.5, 2.5)
	s.Color = Color3.fromRGB(200, 120, 60)
	s.Material = Enum.Material.Neon
	s.Position = origin + Vector3.new(math.random(-SIZE/2, SIZE/2), 4, math.random(-SIZE/2, SIZE/2))
	s.Name = "Spice"
	s.Parent = workspace
	s.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if player then
			-- chain: picking spice without banking keeps the LINE growing
			player:SetAttribute("SpiceChain", tonumber((player:GetAttribute("SpiceChain")) or 0) + 1)
			s:Destroy()
		end
	end)
	task.delay(45, function() if s.Parent then s:Destroy() end end)
end

local function spawnGate()
	local g = Instance.new("Part")
	g.Anchored = true
	g.Size = Vector3.new(4, 14, 2)
	g.Color = Color3.fromRGB(90, 200, 140)
	g.Material = Enum.Material.Neon
	g.Position = origin + Vector3.new(math.random(-SIZE/2 + 20, SIZE/2 - 20), 8, math.random(-SIZE/2 + 20, SIZE/2 - 20))
	g.Name = "BankGate"
	g.Parent = workspace
	g.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if not player then return end
		local chain = tonumber(player:GetAttribute("SpiceChain")) or 0
		if chain > 0 then
			-- bank: LINE xN (chain is the multiplier); speed-driven score banks here
			local speed = tonumber(player:GetAttribute("TopSpeed")) or 0
			local banked = math.floor(chain * 25 + speed * 5)
			player:SetAttribute("ArrakisBanked", tonumber((player:GetAttribute("ArrakisBanked")) or 0) + banked)
			ShadowLedger.record(player, "Arrakis", string.format("banked LINE x%d at a gate (%d)", chain, banked), true)
			player:SetAttribute("SpiceChain", 0)
		end
	end)
	task.delay(60, function() if g.Parent then g:Destroy() end end)
end

function ArrakisZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "Arrakis"

	-- dune sea
	local sand = Instance.new("Part")
	sand.Anchored = true
	sand.Size = Vector3.new(SIZE, 1, SIZE)
	sand.Position = Vector3.new(origin.X, origin.Y - 1, origin.Z)
	sand.Color = Color3.fromRGB(196, 156, 96)
	sand.Material = Enum.Material.Sand
	sand.Parent = model

	-- crest ramps: cross them fast and you FLY
	for i = 1, 5 do
		local crest = Instance.new("Part")
		crest.Anchored = true
		crest.Size = Vector3.new(20, 1, 12)
		crest.CFrame = CFrame.new(origin + Vector3.new(math.random(-80, 80), 2, math.random(-80, 80)))
			* CFrame.Angles(math.rad(-18), math.rad(math.random(0, 360)), 0)
		crest.Color = Color3.fromRGB(170, 130, 80)
		crest.Material = Enum.Material.Sand
		crest.Parent = model
	end

	-- the board: a VehicleSeat sled
	local board = Instance.new("Part")
	board.Anchored = false
	board.Size = Vector3.new(4, 0.6, 8)
	board.Color = Color3.fromRGB(60, 60, 70)
	board.Position = origin + Vector3.new(0, 2, 0)
	board.Name = "RiderBoard"
	local seat = Instance.new("VehicleSeat")
	seat.Size = Vector3.new(2, 0.4, 2)
	seat.Position = Vector3.new(0, 0.6, 0)
	seat.MaxSpeed = 60
	seat.Parent = board
	local force = Instance.new("VectorForce")
	force.Attachment0 = Instance.new("Attachment", board)
	force.Force = Vector3.new(0, workspace.Gravity * 0.92, 0) -- near-hover: speed is score
	force.Parent = board
	board.Parent = model

	-- thumper station: E-equivalent prompt, 3 charges, sends the Maker elsewhere
	local station = Instance.new("Part")
	station.Anchored = true
	station.Size = Vector3.new(6, 6, 6)
	station.Position = origin + Vector3.new(0, 4, -30)
	station.Color = Color3.fromRGB(120, 90, 60)
	station.Parent = model
	local thumper = Instance.new("ProximityPrompt")
	thumper.ActionText = "Drop a thumper (3)"
	thumper.ObjectText = "thumper station"
	thumper.HoldDuration = 0.5
	thumper.Parent = station
	thumper.Triggered:Connect(function(player: Player)
		local charges = tonumber(player:GetAttribute("Thumpers")) or Config.Arrakis.thumperCharges
		if charges <= 0 then return end
		player:SetAttribute("Thumpers", charges - 1)
		local t = Instance.new("Part")
		t.Anchored = true
		t.Size = Vector3.new(2, 4, 2)
		t.Color = Color3.fromRGB(230, 90, 50)
		t.Material = Enum.Material.Neon
		t.Position = origin + Vector3.new(math.random(-90, 90), 3, math.random(-90, 90))
		t.Name = "Thumper"
		t.Parent = workspace
		ArrakisZone.retargetMaker(t.Position)
		task.delay(20, function() if t.Parent then t:Destroy() end end)
	end)

	table.insert(spawners, spawnSpice)
	model.Parent = workspace
	return model
end

-- the Maker hunts the fast — but NEVER without a telegraph (the Doors law:
-- Rush does not hit before the lights die). 2s of rumble column, then breach.
local maker: BasePart? = nil
local makerTarget: Vector3? = nil
local telegraphPart: BasePart? = nil
local telegraphUntil = 0

function ArrakisZone.retargetMaker(pos: Vector3)
	makerTarget = pos
end

local function beginTelegraph(pos: Vector3)
	if telegraphPart and telegraphPart.Parent then telegraphPart:Destroy() end
	local col = Instance.new("Part")
	col.Anchored = true
	col.Size = Vector3.new(6, 60, 6)
	col.Position = pos + Vector3.new(0, 30, 0)
	col.Color = Color3.fromRGB(200, 60, 40)
	col.Material = Enum.Material.Neon
	col.Transparency = 0.55
	col.CanCollide = false
	col.Name = "MakerTelegraph"
	col.Parent = workspace
	telegraphPart = col
	telegraphUntil = os.clock() + 2
	makerTarget = nil
end

function ArrakisZone.tick(dt: number)
	for _, f in ipairs(spawners) do
		if math.random() < dt * 0.5 then f() end
	end
	if math.random() < dt * 0.08 then spawnGate() end

	if not maker then
		local m = Instance.new("Part")
		m.Shape = Enum.PartType.Ball
		m.Size = Vector3.new(14, 14, 14)
		m.Color = Color3.fromRGB(150, 90, 50)
		m.Material = Enum.Material.Sand
		m.Position = origin + Vector3.new(0, -6, -100)
		m.Name = "THE MAKER"
		m.Parent = workspace
		maker = m
	end

	-- X ability: ThumperToss drops a thumper at the thrower's feet
	for _, p in ipairs(Players:GetPlayers()) do
		if p:GetAttribute("Abil_Thumper") then
			local root = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
			if root then
				local t = Instance.new("Part")
				t.Anchored = true
				t.Size = Vector3.new(2, 4, 2)
				t.Color = Color3.fromRGB(230, 90, 50)
				t.Material = Enum.Material.Neon
				t.Position = root.Position + Vector3.new(0, 1, 0)
				t.Name = "Thumper"
				t.Parent = workspace
				ArrakisZone.retargetMaker(t.Position)
				task.delay(20, function() if t.Parent then t:Destroy() end end)
			end
		end
	end

	if maker then
		-- breach cycle: telegraph 2s, then lunge
		if telegraphUntil > 0 then
			if os.clock() >= telegraphUntil then
				-- THE BREACH: lunge to the marked point, knock up anyone near it
				local breachPos = telegraphPart and telegraphPart.Position - Vector3.new(0, 30, 0)
				if breachPos and maker then
					maker.Position = breachPos - Vector3.new(0, 4, 0)
				end
				for _, p in ipairs(Players:GetPlayers()) do
					local root = p.Character and p.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
					if root and breachPos and (root.Position - breachPos).Magnitude < 14 then
						root.AssemblyLinearVelocity = Vector3.new(0, 70, 0) -- the arc of the breach
					end
				end
				if telegraphPart and telegraphPart.Parent then telegraphPart:Destroy() end
				telegraphPart = nil
				telegraphUntil = 0
			end
		else
		local fastest, speed = nil, 20 -- below 20 the slow are safe
		for _, p in ipairs(Players:GetPlayers()) do
			local s = tonumber(p:GetAttribute("TopSpeed")) or 0
			if s > speed then fastest, speed = p, s end
		end
		local goal = makerTarget or (fastest and fastest.Character
			and fastest.Character:FindFirstChild("HumanoidRootPart") and (fastest.Character:FindFirstChild("HumanoidRootPart") :: BasePart).Position)
			or origin
			if makerTarget then
				makerTarget = nil
			elseif fastest and math.random() < dt * 0.1 then
				beginTelegraph(goal) -- fair horror: you get two seconds of red column
			end
			local dir = (goal - maker.Position)
			if dir.Magnitude > 4 then
				maker.AssemblyLinearVelocity = dir.Unit * 18
			end
		end
	end
end

return ArrakisZone
