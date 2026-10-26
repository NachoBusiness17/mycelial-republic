--[[
    ServerMain — the boot sequence. Everything connects here.
    The estate runs. The hall files. The Answer waits.
]]

local ServerScriptService = game:GetService("ServerScriptService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Players = game:GetService("Players")

-- Load shared config
local GameConfig = require(ReplicatedStorage:WaitForChild("GameConfig"))

-- Load modules
local ShadowLedger = require(ServerScriptService:WaitForChild("ShadowLedger"))
local TheAnswer = require(ServerScriptService:WaitForChild("TheAnswer"))
local HallOfSupper = require(ServerScriptService:WaitForChild("HallOfSupper"))

-- ── Create the shared whisper event ─────────────────────────────────
local whisperEvent = Instance.new("RemoteEvent")
whisperEvent.Name = "WhisperEvent"
whisperEvent.Parent = ReplicatedStorage

-- ── Boot the hall ───────────────────────────────────────────────────
local supperHall = workspace:WaitForChild("SupperHall")
local hall = HallOfSupper.new(supperHall)
hall:setup()

print("[LedgerOfEmptyChairs] Hall of Shared Supper online. " ..
      #hall.chairs .. " chairs empty. The hall files which you chose.")

-- ── Spawn The Answer (dormant, waiting) ──────────────────────────────
local answer = TheAnswer.new(GameConfig.BOSS)
-- The Answer is not spawned yet. It spawns when a player has:
--   1. Counted all 6 chairs (the hall noticed)
--   2. Read the salt-cellar scrap (the player connected)
--   3. Spoken the count aloud (the player chose)
-- Then The Answer appears. Not as a boss. As a Helpful Stranger.
-- With warm eyes. Offering a grant. Smiling.

-- ── Player joined: initialize their ledger ──────────────────────────
Players.PlayerAdded:Connect(function(player)
    ShadowLedger.record(player, "joined", "Player entered the hall")

    -- Give them nothing. Let them explore.
    -- The system does not require belief in the lie.
    -- It only requires that you become too tired to keep pointing.
end)

print("[LedgerOfEmptyChairs] v" .. GameConfig.VERSION .. " online. The ledger is not a diary.")
