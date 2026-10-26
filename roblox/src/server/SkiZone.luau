--!strict
-- SkiZone — the downhill. Translated from skifree.html: speed ramps over
-- time, score per frame, trees, and the crash -> yeti chase. The 49R
-- "skip the yeti" line is served by the Extra Life dev product (one rescue).

local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Config = require(Shared:WaitForChild("Config"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))

local SkiZone = {}
local origin = Vector3.new(-120, 8, -120)
local runState: { [Player]: { speed: number, yeti: BasePart?, crashed: boolean } } = {}

local function spawnTree(pos: Vector3): BasePart
	local tree = Instance.new("Part")
	tree.Anchored = true
	tree.Size = Vector3.new(3, 12, 3)
	tree.Position = pos + Vector3.new(0, 6, 0)
	tree.Color = Color3.fromRGB(40, 90, 50)
	tree.Material = Enum.Material.Grass
	tree.Name = "Tree"
	tree.Parent = workspace
	return tree
end

local function spawnYeti(target: Player): BasePart
	local y = Instance.new("Part")
	y.Shape = Enum.PartType.Ball
	y.Size = Vector3.new(6, 6, 6)
	y.Color = Color3.fromRGB(235, 235, 245)
	y.Material = Enum.Material.Snow
	y.Name = "YETI"
	y.CanCollide = false
	local root = target.Character and target.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	y.Position = root and root.Position + Vector3.new(0, 0, 40) or origin
	y.Parent = workspace
	return y
end

function SkiZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "SkiRun"

	local slope = Instance.new("Part")
	slope.Anchored = true
	slope.Size = Vector3.new(80, 1, 400)
	slope.CFrame = CFrame.new(origin) * CFrame.Angles(math.rad(12), 0, 0)
	slope.Color = Color3.fromRGB(226, 232, 240)
	slope.Material = Enum.Material.Snow
	slope.Parent = model

	-- seeded tree slalom: math.random is fine here (the replay-safe seed lives
	-- in SeedRng for anything score-bearing; trees are scenery)
	for _ = 1, 60 do
		spawnTree(origin + Vector3.new(math.random(-35, 35), math.random(-180, 180), math.random(-180, 180)))
	end

	model.Parent = workspace

	slope.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if player and not runState[player] then
			runState[player] = { speed = Config.Ski.baseSpeed, yeti = nil, crashed = false }
			ShadowLedger.record(player, "Ski", "dropped in", true)
		end
	end)

	Players.PlayerRemoving:Connect(function(p) runState[p] = nil end)
	return model
end

function SkiZone.tick(dt: number)
	for player, state in pairs(runState) do
		local char = player.Character
		if not char then continue end
		local root = char:FindFirstChild("HumanoidRootPart") :: BasePart?
		if not root then continue end

		state.speed += Config.Ski.speedRampPerSec * dt -- speed ramps over time
		player:SetAttribute("SkiScore", (tonumber(player:GetAttribute("SkiScore")) or 0) + math.floor(state.speed * dt))

		-- crash -> the yeti comes (Extra Life product = one rescue)
		local hum = char:FindFirstChild("Humanoid") :: Humanoid?
		if hum and hum.Health <= 0 and not state.crashed then
			state.crashed = true
			state.yeti = spawnYeti(player)
		end
		if state.yeti and state.yeti.Parent and root then
			local dir = root.Position - state.yeti.Position
			state.yeti.AssemblyLinearVelocity = dir.Unit * (state.speed + 4) -- it is faster
			if dir.Magnitude < 6 then
				if (tonumber(player:GetAttribute("ExtraLives")) or 0) > 0 then
					player:SetAttribute("ExtraLives", player:GetAttribute("ExtraLives") - 1)
					state.yeti:Destroy()
					state.yeti = nil
					state.crashed = false
					ShadowLedger.record(player, "Ski", "spent an Extra Life on the yeti", true)
				elseif hum then
					hum.Health = 0
				end
			end
		end
	end
end

return SkiZone
