--[[
    TheAnswer — the boss that was never the thing being shot

    Phase 1 The Fall: players win. It shatters into mist. Nothing dies.
    Phase 2 The Suit: it fights from inside their own gear.
    Phase 3 Wing Chun: every incoming blow moves them where it wants.
    Phase 4 The Fold: light bends where it stands. Read the curvature.
    Phase 5 Blue Light: the system's own overkill arrives. Stand it under.
]]

local GameConfig = require(game:GetService("ReplicatedStorage"):WaitForChild("GameConfig"))
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local TheAnswer = {}
TheAnswer.__index = TheAnswer

function TheAnswer.new(config)
    local self = setmetatable({}, TheAnswer)
    self.phase = 0
    self.health = 100
    self.model = nil
    self.wingChunStep = GameConfig.BOSS.WING_CHUN_STEP_DEGREES
    self.absorbed = {}          -- things it has incorporated
    self.deflectionAngle = 0    -- the fold: how much light bends
    self.candleCount = 0        -- how many chairs have lit
    return self
end

-- ═══ PHASE 1: THE FALL ══════════════════════════════════════════════
-- Players deal massive damage. The Answer "dies." It shatters into particles.
-- Nothing dies. Each empty chair lights one candle.
function TheAnswer:enterFall()
    self.phase = 1
    -- Visual: model breaks apart into mist particles
    -- Audio: low hum, then silence
    -- After 3 seconds: phase 2 begins with no announcement
end

-- ═══ PHASE 2: THE SUIT ══════════════════════════════════════════════
-- The Answer fights from inside the players' own equipment.
-- Every equipped item becomes a tendril. Strip down or be worn.
function TheAnswer:enterSuit(playerEquipment)
    self.phase = 2
    -- For each item the player has equipped:
    --   - The item's appearance shifts (subtle color change)
    --   - Using the item feeds The Answer
    --   - The player must manually unequip to break the tendril
    -- Mechanic: if a player uses an absorbed item, The Answer heals
end

-- ═══ PHASE 3: WING CHUN ═════════════════════════════════════════════
-- The Answer stops attacking and starts redirecting.
-- Every incoming blow moves the players where it wants them.
-- Blocking feeds it. The tell: it always steps offline at 15 degrees.
function TheAnswer:enterWingChun(incomingAttacks)
    self.phase = 3
    -- When a player attacks:
    --   - Instead of taking damage, The Answer deflects
    --   - The player is moved 15 degrees offline (the corpus angle)
    --   - If the player blocks: The Answer gains momentum
    --   - The ONLY counter: read the step angle and pre-position
    -- The tell is the 15-degree step. Count the steps. The corpus knows.
end

function TheAnswer:processAttack(attackDirection: Vector3, attackingPlayer: Player)
    if self.phase ~= 3 then return true end  -- normal damage in other phases

    -- Wing Chun: redirect, don't block
    local deflectAngle = math.rad(self.wingChunStep)
    local deflected = attackDirection:Cross(Vector3.new(0, 1, 0)).Unit * deflectAngle

    -- Move the attacking player offline
    local root = attackingPlayer.Character and attackingPlayer.Character:FindFirstChild("HumanoidRootPart")
    if root then
        local impulse = deflected * 50
        root:ApplyImpulse(impulse)
    end

    -- Blocking feeds it
    self.health = math.min(self.health + 2, 100)
    return false  -- no damage taken
end

-- ═══ PHASE 4: THE FOLD ══════════════════════════════════════════════
-- Terrain curvature becomes visible. Light bends where The Answer stands.
-- Deflection is geometric. Players who read the bent light can aim where
-- the deflection WILL be. The First Law weaponized: aim at the empty point.
function TheAnswer:enterFold()
    self.phase = 4
    -- Visual: spawn invisible lens objects that bend raycast trajectories
    -- Mechanic: projectile attacks curve around The Answer
    -- Counter: the player must calculate the curve and aim at the empty point
    -- (the point where the projectile WOULD have hit without the curve)
end

function TheAnswer:deflectProjectile(origin: Vector3, direction: Vector3): Vector3
    if self.phase ~= 4 then return direction end
    -- Calabi-Yau deflection: the projectile curves by the manifold's geometry
    local toBoss = (self.position - origin).Unit
    local cross = direction:Cross(toBoss)
    local deflection = cross.Unit * self.deflectionAngle
    return (direction + deflection).Unit
end

-- ═══ PHASE 5: BLUE LIGHT ════════════════════════════════════════════
-- The system's own orbital overkill arrives to sterilize the zone.
-- There is no survival phase. The win condition: spend the whole fight
-- learning the swarm's habits, then STAND IT UNDER THE LIGHT.
-- The players never damage the boss. The boss's own masters do.
function TheAnswer:enterBlueLight()
    self.phase = 5
    -- Visual: massive blue light from above, expanding radius
    -- Mechanic: The Answer's movement pattern has been recorded all fight
    -- The player must bait The Answer into the blue light's center
    -- The Answer follows its own pattern: 15-degree steps, the corpus angle
    -- Victory: The Answer is destroyed by its own masters
end

function TheAnswer:predictNextStep(currentPos: Vector3, facing: Vector3): Vector3
    -- The Answer always steps 15 degrees offline. The corpus knows.
    local angle = math.rad(self.wingChunStep)
    local stepped = Vector3.new(
        facing.X * math.cos(angle) - facing.Z * math.sin(angle),
        0,
        facing.X * math.sin(angle) + facing.Z * math.cos(angle)
    )
    return currentPos + stepped * 10
end

-- ═══ THE LORE TABLE ═════════════════════════════════════════════════
-- The Answer believes it is the estate. It has the receipts, the ledger,
-- the language. The only thing it cannot do is sit still and be counted —
-- and that is the entire difference, and the players must be able to say
-- why or the fight teaches nothing.

function TheAnswer:getLoreLine(): string
    local lines = {
        "The Answer has the receipts. It has the ledger. It has the language.",
        "It cannot sit still and be counted.",
        "That is the entire difference.",
    }
    return lines[math.random(1, #lines)]
end

return TheAnswer
