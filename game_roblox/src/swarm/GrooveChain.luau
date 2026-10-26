--[[
    GrooveChain — PRIVLIDGE. The beat IS the ruleset.
    Per-player on-beat chain state: consecutive on-beat actions build a
    Groove (multiplier ladder), off-beat or neglect breaks it.
]]

--!strict
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local BeatClock = require(script.Parent:WaitForChild("BeatClock"))

local GrooveChain = {}
GrooveChain.__index = GrooveChain

-- === CONSTANTS ===
-- Golden-ratio-ish progression: 1, 2, 3, 5, 8, 13
local MULTIPLIERS = { 1, 2, 3, 5, 8, 13 }
local MAX_CHAIN_LEVEL = #MULTIPLIERS

-- === REMOTES ===
local remotesFolder = ReplicatedStorage:FindFirstChild("PRIVLIDGE_Remotes")
if not remotesFolder then
	remotesFolder = Instance.new("Folder")
	remotesFolder.Name = "PRIVLIDGE_Remotes"
	remotesFolder.Parent = ReplicatedStorage
end

local function ensureRemote(name: string): RemoteEvent
	local r = remotesFolder:FindFirstChild(name)
	if not r then
		r = Instance.new("RemoteEvent")
		r.Name = name
		r.Parent = remotesFolder
	end
	return r :: RemoteEvent
end

local grooveStep = ensureRemote("GrooveStep")
local grooveBreak = ensureRemote("GrooveBreak")

-- === STATE (per player) ===
type ChainState = {
	chain: number,
	chainLevel: number,
	lastAction: number,
}

local states: { [Player]: ChainState } = {}

local function computeLevel(newChain: number): number
	-- Level rises every 2 on-beat actions, capped at the ladder top.
	local lvl = math.floor(newChain / 2)
	return math.min(lvl, MAX_CHAIN_LEVEL - 1)
end

-- === PUBLIC API ===

function GrooveChain.Register(player: Player)
	if states[player] then return end
	states[player] = { chain = 0, chainLevel = 0, lastAction = 0 }
end

function GrooveChain.Remove(player: Player)
	states[player] = nil
end

-- On-beat action. Returns the points awarded (basePoints * multiplier).
function GrooveChain.OnBeatAction(player: Player, basePoints: number): number
	local st = states[player]
	if not st then return 0 end

	st.chain += 1
	st.lastAction = os.clock()
	local newLevel = computeLevel(st.chain)
	local leveledUp = newLevel ~= st.chainLevel
	st.chainLevel = newLevel

	local mult = MULTIPLIERS[st.chainLevel + 1]
	local awarded = basePoints * mult

	-- Client owns all sound: it renders rising pitch from chainLevel.
	grooveStep:FireClient(player, st.chain, st.chainLevel, mult, awarded, leveledUp)

	return awarded
end

-- Off-beat action: chain dies.
function GrooveChain.OnOffBeat(player: Player)
	local st = states[player]
	if not st or st.chain == 0 then return end
	local lostChain = st.chain
	st.chain = 0
	st.chainLevel = 0
	grooveBreak:FireClient(player, lostChain)
end

function GrooveChain.GetChain(player: Player): number
	local st = states[player]
	return st and st.chain or 0
end

-- Call ONCE per grid step: a neglected chain dies. Decay window derives
-- from the live clock so SetBPM can't desync it (two bars, wherever the
-- grid currently sits).
function GrooveChain.Tick()
	local decay = BeatClock.GetStepsPerBar() * 2 * BeatClock.GetSecondsPerStep()
	local now = os.clock()
	for player, st in pairs(states) do
		if st.chain > 0 and now - st.lastAction > decay then
			GrooveChain.OnOffBeat(player)
		end
	end
end

function GrooveChain.Reset(player: Player)
	local st = states[player]
	if not st then return end
	st.chain = 0
	st.chainLevel = 0
end

return GrooveChain
