--!strict
-- RuinsGoZone — the grid puzzle climb. Capture tiles by walking; capture a
-- connected chain to claim the group (RUINS GO: zones on the board, moves as
-- tools). Extra Life dev product = one rescue when the group is taken.

local Players = game:GetService("Players")
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))

local RuinsGoZone = {}
local origin = Vector3.new(120, 8, 120)
local N = 9
local cellByTile: { [BasePart]: { player: string?, group: number? } } = {}

function RuinsGoZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "RuinsGo"

	for gx = 1, N do
		for gz = 1, N do
			local tile = Instance.new("Part")
			tile.Anchored = true
			tile.Size = Vector3.new(8, 0.6, 8)
			tile.Position = origin + Vector3.new((gx - (N + 1) / 2) * 8.4, 0, (gz - (N + 1) / 2) * 8.4)
			tile.Color = Color3.fromRGB(52, 48, 40)
			tile.Material = Enum.Material.WoodPlanks
			tile.Name = ("Tile_%d_%d"):format(gx, gz)
			tile.Parent = model
			cellByTile[tile] = { player = nil, group = nil }

			tile.Touched:Connect(function(hit)
				local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
				if not player then return end
				local cell = cellByTile[tile]
				if not cell then return end
				local owner = tostring(player.UserId)
				if cell.player == owner then return end
				-- capture overwrites neutrals; contest = the other player's group thins
				cell.player = owner
				tile.Color = tonumber((player:GetAttribute("Invariants")) or 0) > 0
					and Color3.fromRGB(110, 150, 90)
					or Color3.fromRGB(150, 130, 80)
				player:SetAttribute("RuinsScore", tonumber((player:GetAttribute("RuinsScore")) or 0) + 1)
			end)
		end
	end

	model.Parent = workspace
	return model
end

return RuinsGoZone
