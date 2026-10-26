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
		-- t74 receipt: this was GetAsync + SetAsync (:43-50 before the fix), a
		-- two-call read-modify-write. Two servers recording the same player+day
		-- both read the same rows and the later SetAsync clobbered the other's
		-- append (lost update); the docs say SetAsync "may cause data
		-- inconsistency if two servers attempt to set the same key"
		-- (create.roblox.com GlobalDataStore, fetched 2026-09-25). Fix per
		-- t63.next_steal: UpdateAsync applies the transform to the latest
		-- stored value, so appends serialize. The transform copies then
		-- appends (no mutation of the passed table, nothing yielded) because
		-- the docs say it "will be called as many times as needed" with prior
		-- results discarded; a mutating transform could double-append on a
		-- retry. Schema unchanged: the value is still an array of entry rows,
		-- so pre-fix saves read back as-is. No batch queue: no caller loops N
		-- same-player records per visit (caller census, t74.check.txt), and
		-- buffering rows would trade durability for size.
		pcall(function()
			store:UpdateAsync(key, function(old)
				local rows = {}
				if type(old) == "table" then
					for i = 1, #old do rows[i] = old[i] end
				end
				rows[#rows + 1] = entry
				return rows
			end)
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
