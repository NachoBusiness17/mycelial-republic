--!strict
-- Monetization — MarketplaceService wiring per ROBLOX_MONETIZATION_PLAN_20260924.md.
-- Pass IDs are filled in Studio after first publish; the table is the source of
-- truth so scripts keep working with id=0 (disabled) until then.

local MarketplaceService = game:GetService("MarketplaceService")
local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Config = require(Shared:WaitForChild("Config"))

local Monetization = {}
local ownedPass: { [string]: { [number]: boolean } } = {}

function Monetization.owns(player: Player, passKey: string): boolean
	local pass = Config.GamePasses[passKey]
	if not pass or not pass.id or pass.id == 0 then return false end -- unpublished SKU = free-disabled
	local cache = ownedPass[passKey]
	if cache and cache[player.UserId] ~= nil then return cache[player.UserId] end
	local ok, owns = pcall(function()
		return MarketplaceService:UserOwnsGamePassAsync(player.UserId, pass.id)
	end)
	if not ok then return false end
	ownedPass[passKey] = ownedPass[passKey] or {}
	ownedPass[passKey][player.UserId] = owns
	return owns
end

function Monetization.invalidate(player: Player, passKey: string)
	if ownedPass[passKey] then ownedPass[passKey][player.UserId] = nil end
end

function Monetization.init()
	MarketplaceService.ProcessReceipt = function(receipt)
		local player = Players:GetPlayerByUserId(receipt.PlayerId)
		if not player then
			-- retry when they rejoin (Roblox will re-deliver)
			return Enum.ProductPurchaseDecision.NotProcessedYet
		end
		for key, prod in pairs(Config.DevProducts) do
			if prod.id ~= 0 and receipt.ProductId == prod.id then
				if key == "ExtraLife" then
					player:SetAttribute("ExtraLives", tonumber((player:GetAttribute("ExtraLives")) or 0) + 1)
				elseif key == "SkipVellum" then
					player:SetAttribute("SkipVellum", true)
				elseif key == "VirtueDoubler" then
					player:SetAttribute("VirtueDoublerUntil", os.time() + 3600)
				end
				return Enum.ProductPurchaseDecision.PurchaseGranted
			end
		end
		return Enum.ProductPurchaseDecision.NotProcessedYet
	end

	Players.PlayerRemoving:Connect(function(player)
		for _, cache in pairs(ownedPass) do cache[player.UserId] = nil end
	end)
end

return Monetization
