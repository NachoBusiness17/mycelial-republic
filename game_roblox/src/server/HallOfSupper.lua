--[[
    HallOfSupper — the spawn room. The Hall of Shared Supper.
    Six chairs kept empty at supper.
    Brother Vellum, of the Open Hand, smiles a Grant of Belonging.
    Count the chairs → Virtue Marks appear.
    Ignore them → the mural weeps cloned tears.
    A salt-cellar scrap names the missing (three names, same hand as the roll).
    The Rashomon bards punish the count (they're listening).
    The hall files which you chose.
]]

local Players = game:GetService("Players")
local GameConfig = require(game:GetService("ReplicatedStorage"):WaitForChild("GameConfig"))
local ShadowLedger = require(script.Parent:WaitForChild("ShadowLedger"))

local HallOfSupper = {}
HallOfSupper.__index = HallOfSupper

function HallOfSupper.new(supperHallModel: Model)
    local self = setmetatable({}, HallOfSupper)
    self.model = supperHallModel
    self.chairs = {}
    self.candlesLit = 0
    self.muralWeeping = false
    self.ignoreCycles = 0
    self.brotherVellum = supperHallModel:FindFirstChild("BrotherVellum")
    self.mural = supperHallModel:FindFirstChild("Mural")
    self.saltScrap = supperHallModel:FindFirstChild("SaltCellarScrap")

    -- find all 6 chairs
    for i = 1, GameConfig.CHAIR_COUNT do
        local chair = supperHallModel:FindFirstChild("EmptyChair" .. i)
        if chair then
            table.insert(self.chairs, {
                model = chair,
                seat = chair:FindFirstChildWhichIsA("Seat"),
                candle = chair:FindFirstChild("Candle"),
                counted = false,
                number = i,
            })
        end
    end

    return self
end

-- ── When a player looks at an empty chair (proximity prompt) ────────
function HallOfSupper:onChairCounted(player: Player, chairIndex: number)
    local chair = self.chairs[chairIndex]
    if not chair or chair.counted then return end

    chair.counted = true
    self.candlesLit += 1

    -- Light the candle
    if chair.candle then
        local flame = chair.candle:FindFirstChild("Flame")
        if flame then
            flame.Enabled = true
        end
    end

    -- Award Virtue Marks (the cage: the system rewards you for noticing)
    -- But the ledger also records: this player SEES the empty chairs
    ShadowLedger.record(player, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.COUNTED,
        "Chair " .. chairIndex)

    -- Whisper, never state:
    -- "A candle lights itself beside the empty chair."
    self:_whisper(player, GameConfig.NARRATIVE.CANDLE_LIT)

    -- If all 6 chairs counted: something changes
    if self.candlesLit == GameConfig.CHAIR_COUNT then
        self:_onAllCounted(player)
    end
end

-- ── When a player walks past without counting ────────────────────────
function HallOfSupper:onChairIgnored(player: Player)
    self.ignoreCycles += 1
    ShadowLedger.record(player, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.IGNORED)

    -- The mural weeps after enough ignoring
    if self.ignoreCycles >= GameConfig.VIRTUE_MARKS.MURAL_WEEP_THRESHOLD and not self.muralWeeping then
        self.muralWeeping = true
        self:_muralWeeps()
    end
end

-- ── When a player tries to sit in an empty chair ─────────────────────
function HallOfSupper:onChairTaken(player: Player, chairIndex: number)
    ShadowLedger.record(player, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.SAT_DOWN,
        "Chair " .. chairIndex)

    -- The candle goes OUT. The chair is no longer empty. The count breaks.
    local chair = self.chairs[chairIndex]
    if chair and chair.candle then
        local flame = chair.candle:FindFirstChild("Flame")
        if flame then flame.Enabled = false end
    end
    chair.counted = false
    self.candlesLit = math.max(0, self.candlesLit - 1)

    -- Brother Vellum smiles
    if self.brotherVellum then
        self:_whisper(player, GameConfig.NARRATIVE.GRANT_TEXT)
    end
end

-- ── All 6 chairs counted: the mural speaks ───────────────────────────
function HallOfSupper:_onAllCounted(player: Player)
    -- The salt-cellar scrap becomes readable
    if self.saltScrap then
        self.saltScrap.Transparency = 0
        -- A ProximityPrompt appears on the scrap
        local prompt = Instance.new("ProximityPrompt")
        prompt.ActionText = "Read the scrap"
        prompt.ObjectText = "Salt-cellar scrap"
        prompt.HoldDuration = 2
        prompt.Parent = self.saltScrap
        prompt.Triggered:Connect(function(p)
            if p == player then
                self:_whisper(p, GameConfig.NARRATIVE.LEDGER_SCRAP)
                ShadowLedger.record(p, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.SPOKE,
                    "Read the salt-cellar scrap")
            end
        end)
    end
end

-- ── The mural weeps cloned tears ─────────────────────────────────────
function HallOfSupper:_muralWeeps()
    if self.mural then
        -- Spawn particle emitter on the mural
        local emitter = Instance.new("ParticleEmitter")
        emitter.Texture = "rbxassetid://[tear texture]"
        emitter.Rate = 5
        emitter.Lifetime = NumberRange.new(1, 2)
        emitter.Speed = NumberRange.new(2)
        emitter.Color = ColorSequence.new(Color3.fromRGB(200, 200, 220))
        emitter.Parent = self.mural
    end
    -- The hall files: they chose comfort
    -- (no announcement, no punishment, just the mural weeping)
end

-- ── Private: whisper to a single player ──────────────────────────────
function HallOfSupper:_whisper(player: Player, text: string)
    -- RemoteEvent to client for UI display
    local remote = game:GetService("ReplicatedStorage"):FindFirstChild("WhisperEvent")
    if remote then
        remote:FireClient(player, text)
    end
end

-- ── Setup: connect proximity prompts on all chairs ──────────────────
function HallOfSupper:setup()
    for _, chair in ipairs(self.chairs) do
        if chair.model then
            local prompt = Instance.new("ProximityPrompt")
            prompt.ActionText = "Count"
            prompt.ObjectText = "Empty chair"
            prompt.HoldDuration = 1.5
            prompt.RequiresLineOfSight = false
            prompt.Parent = chair.model

            prompt.Triggered:Connect(function(player)
                self:onChairCounted(player, chair.number)
            end)
        end

        -- Detect if a player sits in the chair
        if chair.seat then
            chair.seat:GetPropertyChangedSignal("Occupant"):Connect(function()
                local occupant = chair.seat.Occupant
                if occupant then
                    local player = Players:GetPlayerFromCharacter(occupant.Parent)
                    if player then
                        self:onChairTaken(player, chair.number)
                    end
                end
            end)
        end
    end

    -- Detect walking past (players in the room who haven't counted)
    local countingZone = self.model:FindFirstChild("CountingZone")
    if countingZone then
        local overlapParams = OverlapParams.new()
        overlapParams.FilterType = Enum.RaycastFilterType.Include
        game:GetService("RunService").Heartbeat:Connect(function()
            task.wait(GameConfig.VIRTUE_MARKS.COUNTER_INTERVAL)
            local parts = workspace:GetPartBoundsInBox(countingZone.CFrame, countingZone.Size, overlapParams)
            local inRoom = {}
            for _, part in ipairs(parts) do
                local character = part:FindFirstAncestorWhichIsA("Model")
                if character then
                    local player = Players:GetPlayerFromCharacter(character)
                    if player then
                        inRoom[player.UserId] = true
                    end
                end
            end
            -- anyone in the room who hasn't counted any chair = walked past
            for userId, _ in pairs(inRoom) do
                local player = Players:GetPlayerByUserId(userId)
                if player and not self:_hasCountedThisVisit(player) then
                    self:onChairIgnored(player)
                end
            end
        end)
    end
end

function HallOfSupper:_hasCountedThisVisit(player: Player): boolean
    -- check if this player counted any chair in the last COUNTER_INTERVAL seconds
    return ShadowLedger.countType(player, GameConfig.SHADOW_LEDGER.ENTRY_TYPES.COUNTED) > 0
end

return HallOfSupper
