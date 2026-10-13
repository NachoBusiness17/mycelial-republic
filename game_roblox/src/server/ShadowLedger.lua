--[[
    ShadowLedger — the hall's private record of what each player chose
    Append-only. The hall files which you chose.
    Players never see this ledger. They see its consequences.
]]

local Players = game:GetService("Players")
local DataStoreService = game:GetService("DataStoreService")
local GameConfig = require(game:GetService("ReplicatedStorage"):WaitForChild("GameConfig"))

local ShadowLedger = {}
local store = DataStoreService:GetDataStore("ShadowLedger_v1")

-- In-memory ledger for this session
local sessionLedger = {}

-- ── Record a choice ─────────────────────────────────────────────────
function ShadowLedger.record(player: Player, entryType: string, detail: string?)
    local userId = tostring(player.UserId)
    if not sessionLedger[userId] then
        sessionLedger[userId] = {
            name = player.Name,
            joined = os.time(),
            entries = {},
        }
    end

    table.insert(sessionLedger[userId].entries, {
        type = entryType,
        detail = detail,
        ts = os.time(),
    })

    -- async persist (the ledger is append-only; nothing ever gets deleted)
    task.spawn(function()
        local key = "ledger_" .. userId
        local existing = store:GetAsync(key)
        if existing then
            table.insert(existing.entries, sessionLedger[userId].entries[#sessionLedger[userId].entries])
            store:SetAsync(key, existing)
        else
            store:SetAsync(key, sessionLedger[userId])
        end
    end)
end

-- ── Query: how many times has this player counted? ──────────────────
function ShadowLedger.countType(player: Player, entryType: string): number
    local userId = tostring(player.UserId)
    local ledger = sessionLedger[userId]
    if not ledger then return 0 end
    local count = 0
    for _, entry in ipairs(ledger.entries) do
        if entry.type == entryType then count += 1 end
    end
    return count
end

-- ── The hall's disposition of this player ────────────────────────────
-- The system does not require belief in the lie.
-- It only requires that you become too tired to keep pointing at the empty chairs.
function ShadowLedger.getDisposition(player: Player): string
    local counted = ShadowLedger.countType(player, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.COUNTED)
    local ignored = ShadowLedger.countType(player, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.IGNORED)
    local satDown = ShadowLedger.countType(player, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.SAT_DOWN)

    if satDown > 0 then
        return "seated"      -- the player took a chair. The hall approves.
    elseif counted > ignored * 2 then
        return "watchful"    -- the player keeps counting. The hall files this.
    elseif ignored > counted * 2 then
        return "comfortable" -- the player walked past. The hall smiles.
    else
        return "unfiled"     -- not enough data. The hall is patient.
    end
end

-- ── Cleanup on leave ────────────────────────────────────────────────
Players.PlayerRemoving:Connect(function(player)
    -- persist before they leave
    local userId = tostring(player.UserId)
    if sessionLedger[userId] then
        task.spawn(function()
            store:SetAsync("ledger_" .. userId, sessionLedger[userId])
        end)
    end
end)

return ShadowLedger
