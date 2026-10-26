--!strict
-- ShadowLedger — "the room that remembers." The hall files which you chose.
-- Every choice the world observes a player make (or refuse to make) is written
-- here, keyed by k-space address, and is readable back by The Watchful Eye.

local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")

local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local KSpace = _G.KSPACE_UNDER_TEST -- B2-30 harness delta (sole edit; real line 10)

local ShadowLedger = {}
local store = DataStoreService:GetDataStore("ShadowLedger_v1")

export type Entry = {
	player: string,
	kspace: string,       -- zone address
	choice: string,       -- what they did, or pointedly did not do
	noticing: boolean,    -- did they notice the thing (the Vellum mechanic)
	virtueMarks: number,
	ts: number,
}

local sessionLedger: { [string]: { Entry } } = {}

function ShadowLedger.record(player: Player, zone: string, choice: string, noticing: boolean?)
	local addr = KSpace.get(zone)
	local entry: Entry = {
		player = player.UserId and tostring(player.UserId) or player.Name,
		kspace = addr and addr.zone or zone,
		choice = choice,
		noticing = noticing == true,
		virtueMarks = (noticing == true) and 1 or 0,
		ts = os.time(),
	}
	local list = sessionLedger[entry.player]
	if not list then list = {} sessionLedger[entry.player] = list end
	table.insert(list, entry)

	-- durable write; the ledger is the authority (the world is the record)
	task.spawn(function()
		local key = ("p%s_day%s"):format(entry.player, os.date("!%Y%m%d"))
		local ok, existing = pcall(function()
			return store:GetAsync(key)
		end)
		local rows = (ok and type(existing) == "table") and existing or {}
		table.insert(rows, entry)
		pcall(function()
			store:SetAsync(key, rows)
		end)
	end)
end

-- The Watchful Eye (199R pass): read another player's disposition — what the
-- ledger says about them, never raw chat. Disposition = ratio of noticing.
function ShadowLedger.disposition(ofPlayer: Player): string
	local list = sessionLedger[tostring(ofPlayer.UserId)]
	if not list or #list == 0 then return "THE LEDGER IS BLANK. THAT IS ITS OWN VERDICT." end
	local noticed = 0
	for _, e in ipairs(list) do
		if e.noticing then noticed += 1 end
	end
	local r = noticed / #list
	if r > 0.66 then return "SEES WHAT IS THERE. THE CHAIRS RATTLE WHEN THEY WALK PAST." end
	if r > 0.33 then return "GLANCES, SOMETIMES. THE HALL IS PATIENT WITH GLANCERS." end
	return "ATE PAST IT ALL. THE STEW KEEPS ITS RECIPE."
end

function ShadowLedger.onLeaving(player: Player)
	sessionLedger[tostring(player.UserId)] = nil
end

Players.PlayerRemoving:Connect(ShadowLedger.onLeaving)

return ShadowLedger
