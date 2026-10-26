--!strict
-- NpcGateway — the bridge between the world and the fleet's brain.
-- NPC = SEAT: every AI head is a persona served by the local mag gateway
-- (tools/roblox_npc_gateway.py), which routes to the free stealth lanes
-- (stealth/space-bunny-alpha on OpenRouter x2 keys + Nous). One ractor,
-- many faces. When the bus is dark, heads fall back to canned first lines
-- and say so honestly (no fabrication law).

local HttpService = game:GetService("HttpService")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Config = require(Shared:WaitForChild("Config"))
local Lore = require(Shared:WaitForChild("Lore"))

local NpcGateway = {}
local lastCallByHead: { [string]: number } = {}
local COOLDOWN = 2 -- seconds per head; protects the free lanes

local function firstLineFor(headId: string): string
	for _, h in ipairs(Lore.Heads) do
		if h.id == headId then return h.firstLine end
	end
	return "..."
end

-- ask(): one turn of one seat. Context = where they stand, what the room asks.
function NpcGateway.ask(headId: string, playerName: string, message: string, roomContext: string, model: string?): (string, boolean)
	local now = os.clock()
	if lastCallByHead[headId] and now - lastCallByHead[headId] < COOLDOWN then
		return "(the head is still thinking about the last question)", false
	end
	lastCallByHead[headId] = now

	local body = HttpService:JSONEncode({
		head = headId,
		player = playerName,
		message = message,
		room = roomContext,
		model = model, -- nil = gateway default; survey passes cross-family slugs (Mooncast law)
	})
	local ok, err = pcall(function()
		local res = HttpService:RequestAsync({
			Url = Config.Gateway.url,
			Method = "POST",
			Headers = { ["Content-Type"] = "application/json" },
			Body = body,
			Timeout = Config.Gateway.timeoutSec,
		})
		if res.Success then
			local decoded = HttpService:JSONDecode(res.Body)
			if decoded.reply and decoded.reply ~= "" then
				return decoded.reply
			end
		end
		return nil
	end)

	if ok and type(err) == "string" and #err > 0 then
		return err, true
	end

	-- offline: honest fallback (never fabricate a live model)
	local fallback = firstLineFor(headId)
	return fallback .. "  (the bus to the fleet is dark; this is a recording)", false
end

return NpcGateway
