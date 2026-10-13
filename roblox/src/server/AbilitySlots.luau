--!strict
-- AbilitySlots — Blox Fruits pattern: four abilities on Z / X / C / V with
-- server-validated cooldowns, active windows as player attributes that zones
-- read (Fire pellets, Thumper tosses, Wing Chun parry, Count reveals).
-- Input arrives from the client over the Ability remote; carrying stolen
-- goods (Steal-a penalty) disables every slot.

local Players = game:GetService("Players")

local AbilitySlots = {}

export type Ability = {
	name: string,
	attribute: string,
	window: number,
	cooldown: number,
}

local REGISTRY: { Ability } = {
	{ name = "Fire",             attribute = "Abil_Fire",     window = 0.15, cooldown = 0.25 },
	{ name = "ThumperToss",      attribute = "Abil_Thumper",  window = 0.15, cooldown = 10 },
	{ name = "WingChunRedirect", attribute = "Abil_Redirect", window = 1.5,  cooldown = 8 },
	{ name = "Count",            attribute = "Abil_Count",    window = 3,    cooldown = 20 },
}

local lastUse: { [Player]: { [string]: number } } = {}

function AbilitySlots.registry(): { Ability }
	return REGISTRY
end

function AbilitySlots.bind(remote: RemoteEvent)
	remote.OnServerEvent:Connect(function(player: Player, name: string)
		local ab: Ability? = nil
		for _, a in ipairs(REGISTRY) do
			if a.name == name then ab = a end
		end
		if not ab then return end
		if player:GetAttribute("Carrying") == true then
			return -- gear disabled while carrying stolen goods
		end
		local now = os.clock()
		local t = (lastUse[player] and lastUse[player][ab.name]) or -math.huge
		if now - t < ab.cooldown then return end -- server owns the cooldown clock
		lastUse[player] = lastUse[player] or {}
		lastUse[player][ab.name] = now
		player:SetAttribute(ab.attribute, true)
		task.delay(ab.window, function()
			if player.Parent then
				player:SetAttribute(ab.attribute, false)
			end
		end)
	end)
end

function AbilitySlots.init()
	Players.PlayerAdded:Connect(function(player: Player)
		lastUse[player] = {}
	end)
	Players.PlayerRemoving:Connect(function(player)
		lastUse[player] = nil
	end)
end

return AbilitySlots
