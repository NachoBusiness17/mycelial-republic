--!strict
-- PlayerFeel — the universal movement polish layer (Blox Fruits / RIVALS standard):
-- sprint x1.5 on Shift, Q dash (60 studs, 3s cooldown), one double jump.
-- Input arrives from the client (finit.client.luau) over the Movement remote;
-- the server validates and applies. No stamina in v1. Per-player FOV kick is
-- a client pass (v1.1); the dash itself is server-authoritative.

local Players = game:GetService("Players")

local PlayerFeel = {}
local BASE_WALK = 16
local SPRINT_MULT = 1.5
local DASH_STUDS = 60
local DASH_COOLDOWN = 3

local lastDash: { [Player]: number } = {}
local sprinting: { [Player]: boolean } = {}
local airJumps: { [Player]: number } = {}

local function applySpeed(player: Player, char: Model?)
	local hum = char and char:FindFirstChild("Humanoid") :: Humanoid?
	if not hum then return end
	local carry = player:GetAttribute("Carrying") == true
	local mult = (sprinting[player] and SPRINT_MULT or 1) * (carry and 0.6 or 1)
	hum.WalkSpeed = BASE_WALK * mult
end

function PlayerFeel.bind(remote: RemoteEvent)
	remote.OnServerEvent:Connect(function(player: Player, action: string, sprintOn: boolean?)
		local char = player.Character
		local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?

		if action == "sprint" then
			sprinting[player] = sprintOn == true
			applySpeed(player, char)
		elseif action == "dash" and root then
			local now = os.clock()
			if now - (lastDash[player] or 0) < DASH_COOLDOWN then return end
			lastDash[player] = now
			local hum = char and char:FindFirstChild("Humanoid") :: Humanoid?
			local dir = hum and hum.MoveDirection or Vector3.zero
			if dir.Magnitude < 0.1 then
				dir = root.CFrame.LookVector
			end
			root.AssemblyLinearVelocity = dir.Unit * DASH_STUDS
			player:SetAttribute("DashAt", now)
		elseif action == "airjump" then
			local hum = char and char:FindFirstChild("Humanoid") :: Humanoid?
			if hum and hum:GetState() ~= Enum.HumanoidStateType.Landed
				and (airJumps[player] or 0) < 1 and root then
				airJumps[player] = (airJumps[player] or 0) + 1
				root.AssemblyLinearVelocity = Vector3.new(
					root.AssemblyLinearVelocity.X, 45, root.AssemblyLinearVelocity.Z)
			end
		end
	end)
end

function PlayerFeel.init()
	Players.PlayerAdded:Connect(function(player: Player)
		lastDash[player] = 0
		airJumps[player] = 0
		player.CharacterAdded:Connect(function(char)
			applySpeed(player, char)
			local hum = char:WaitForChild("Humanoid") :: Humanoid
			hum.StateChanged:Connect(function(_, new)
				if new == Enum.HumanoidStateType.Landed then
					airJumps[player] = 0 -- double jump resets on landing
				end
			end)
		end)
	end)
	Players.PlayerRemoving:Connect(function(player)
		lastDash[player] = nil
		sprinting[player] = nil
		airJumps[player] = nil
	end)
	-- Tower-of-Hell law: falls cost seconds, not sessions
	Players.RespawnTime = 1
end

return PlayerFeel
