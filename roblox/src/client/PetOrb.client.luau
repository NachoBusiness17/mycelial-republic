--!strict
-- PetOrb.client - the rebirth pet, made visible (Q-042, 2026-09-28).
-- SPEC (already owned, no behavior invented): docs/CLONED_MECHANICS.md
-- rebirth row "hatch a pet orb (Pet-Sim auto-grind: follows you,
-- auto-collects swarm gems in a 12-stud radius)"; docs/PLAYTEST.md
-- "with the pet orb (after rebirth) gems collect from ~12 studs".
-- The server already owns the grind: LedgerExchange stamps the PetOrb
-- attribute at rebirth and SwarmZone collects gems from 12 studs of the
-- character root while it is set. This script is the BODY of that truth,
-- painted locally off the same replicated attribute (the t46/t59 pattern:
-- server stamps, client paints; deterministic local visuals only):
--   1. the orb model: a gold neon ball (the Counting Circle's gold, the
--      fold it hatched from) with a PointLight and a camera-facing Trail,
--   2. the follower: RenderStepped lerp to a hover point behind the right
--      shoulder (offset magnitude ~3.0 studs of the root, always inside the
--      12-stud collect radius, so what you see floats inside what the
--      server actually collects from),
--   3. the gem-collect visual: when a gem dies inside OUR collect radius
--      the client bursts a ring at the gem's last position and the orb
--      gulps (quick size pulse).
-- No new remotes: gems are found by name among workspace's children, the
-- same folder SwarmZone parents them to. Standalone LocalScript (sibling of
-- init.client/CathedralMapHud) so the pet lives or dies with its own file.

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer

-- palette: orb is the Counting Circle's gold (LedgerExchange rebirth circle),
-- burst is the gem's green (SwarmZone gems). Both constants copied from the
-- server sources they mirror, so the pet reads as part of those systems.
local ORB_COLOR = Color3.fromRGB(230, 200, 60)
local GEM_COLOR = Color3.fromRGB(120, 220, 160)

local ORB_SIZE = Vector3.new(1.1, 1.1, 1.1)
-- behind the right shoulder; magnitude ~3.0 studs, well inside the 12-stud
-- collect radius the server enforces (SwarmZone PetOrb branch)
local HOVER_OFFSET = Vector3.new(0.9, 2.4, 1.7)
local FOLLOW_RATE = 8 -- lerp stiffness per second; higher = tighter follow

-- collect radii, mirroring SwarmZone's own line (PetOrb ? 12 : 3.5)
local GEM_RADIUS_BASE = 3.5
local GEM_RADIUS_PET = 12

-- ---- 1. the orb model ----
local function buildOrb(): Model
	local model = Instance.new("Model")
	model.Name = "PetOrb"

	local core = Instance.new("Part")
	core.Name = "OrbCore"
	core.Shape = Enum.PartType.Ball
	core.Size = ORB_SIZE
	core.Color = ORB_COLOR
	core.Material = Enum.Material.Neon
	core.Anchored = true
	core.CanCollide = false
	core.CanQuery = false
	core.CanTouch = false
	core.CastShadow = false
	core.Parent = model

	local glow = Instance.new("PointLight")
	glow.Name = "OrbGlow"
	glow.Color = ORB_COLOR
	glow.Range = 10
	glow.Brightness = 1.2
	glow.Parent = core

	local top = Instance.new("Attachment")
	top.Name = "TrailTop"
	top.Position = Vector3.new(0, 0.45, 0)
	top.Parent = core
	local bottom = Instance.new("Attachment")
	bottom.Name = "TrailBottom"
	bottom.Position = Vector3.new(0, -0.45, 0)
	bottom.Parent = core

	local trail = Instance.new("Trail")
	trail.Name = "OrbTrail"
	trail.Attachment0 = top
	trail.Attachment1 = bottom
	trail.Lifetime = 0.3
	trail.MinLength = 0.05
	trail.FaceCamera = true
	trail.LightEmission = 1
	trail.Color = ColorSequence.new(ORB_COLOR)
	trail.Transparency = NumberSequence.new({
		NumberSequenceKeypoint.new(0, 0.25),
		NumberSequenceKeypoint.new(1, 1),
	})
	trail.WidthScale = NumberSequence.new({
		NumberSequenceKeypoint.new(0, 1),
		NumberSequenceKeypoint.new(1, 0.1),
	})
	trail.Enabled = false
	trail.Parent = core

	model.PrimaryPart = core
	return model
end

-- ---- orb state ----
local orb: Model? = nil
local orbCore: BasePart? = nil
local orbTrail: Trail? = nil
local pulseTween: Tween? = nil

local function stopPulse()
	if pulseTween then
		pulseTween:Cancel()
		pulseTween = nil
	end
	if orbCore then
		orbCore.Size = ORB_SIZE
	end
end

local function destroyOrb()
	stopPulse()
	if orb then
		orb:Destroy()
	end
	orb = nil
	orbCore = nil
	orbTrail = nil
end

local function hatchOrb()
	if orb then return end
	local model = buildOrb()
	local core = model.PrimaryPart :: BasePart
	orb = model
	orbCore = core
	orbTrail = core:FindFirstChildOfClass("Trail")
	-- hatch at the shoulder, not at the world origin flying in
	local char = player.Character
	local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if root then
		core.CFrame = root.CFrame * CFrame.new(HOVER_OFFSET)
	end
	model.Parent = workspace
end

-- ---- 2. the follower (and the attribute wiring) ----
-- PetOrb is stamped true by LedgerExchange at rebirth and never cleared by
-- any server path, but the handler still handles a clear: the orb despawns
-- the moment the attribute says so, whatever the future does.
local function syncOrb()
	if player:GetAttribute("PetOrb") == true then
		hatchOrb()
	else
		destroyOrb()
	end
end
player:GetAttributeChangedSignal("PetOrb"):Connect(syncOrb)
syncOrb()

RunService.RenderStepped:Connect(function(dt: number)
	local core = orbCore
	if not core then return end
	local char = player.Character
	local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then
		-- between lives the pet waits, unseen (a pet with no one to follow)
		core.Transparency = 1
		if orbTrail then orbTrail.Enabled = false end
		return
	end
	core.Transparency = 0
	if orbTrail then orbTrail.Enabled = true end
	local bob = math.sin(os.clock() * 2.4) * 0.18
	local target = root.CFrame * CFrame.new(HOVER_OFFSET + Vector3.new(0, bob, 0))
	local alpha = math.clamp(dt * FOLLOW_RATE, 0, 1)
	core.CFrame = core.CFrame:Lerp(target, alpha)
end)

-- ---- 3. the gem-collect visual ----
-- Gems are plain workspace children named "Gem" (SwarmZone parents them at
-- the workspace root). A gem dies exactly two ways: the server's collect
-- loop (it sat inside someone's collect radius; that loop runs every
-- Heartbeat, init.server.luau) or its 30s TTL (it never got near anyone).
-- So a gem that dies inside OUR radius is our collection, touch or orb:
-- the burst fires at the gem's last position and the orb gulps. The radius
-- mirrors the server's own branch so the visual and the grind stay one shape.
local watching: { [BasePart]: boolean } = {}

local function watchGem(inst: Instance)
	local part = inst :: BasePart
	if not part:IsA("BasePart") then return end
	if part.Name ~= "Gem" then return end
	watching[part] = true
end

for _, inst in ipairs(workspace:GetChildren()) do
	watchGem(inst)
end
workspace.ChildAdded:Connect(watchGem)

local function burst(at: Vector3)
	local ring = Instance.new("Part")
	ring.Name = "GemCollectBurst"
	ring.Shape = Enum.PartType.Ball
	ring.Size = Vector3.new(1.7, 1.7, 1.7)
	ring.Color = GEM_COLOR
	ring.Material = Enum.Material.Neon
	ring.Anchored = true
	ring.CanCollide = false
	ring.CanQuery = false
	ring.CanTouch = false
	ring.CastShadow = false
	ring.Transparency = 0.2
	ring.CFrame = CFrame.new(at)
	ring.Parent = workspace
	local out = TweenService:Create(ring, TweenInfo.new(0.35, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
		Size = Vector3.new(4.8, 4.8, 4.8),
		Transparency = 1,
	})
	out.Completed:Once(function()
		ring:Destroy()
	end)
	out:Play()
end

local function gulp()
	local core = orbCore
	if not core then return end
	stopPulse()
	core.Size = ORB_SIZE
	local up = TweenService:Create(core, TweenInfo.new(0.12, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
		Size = ORB_SIZE * 1.35,
	})
	up.Completed:Once(function()
		if orbCore ~= core then return end -- the orb was destroyed mid-gulp
		local back = TweenService:Create(core, TweenInfo.new(0.22, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), {
			Size = ORB_SIZE,
		})
		pulseTween = back
		back:Play()
	end)
	pulseTween = up
	up:Play()
end

local function collectRadius(): number
	return (player:GetAttribute("PetOrb") == true) and GEM_RADIUS_PET or GEM_RADIUS_BASE
end

workspace.ChildRemoved:Connect(function(inst)
	local part = inst :: BasePart
	if not part:IsA("BasePart") then return end
	if not watching[part] then return end
	watching[part] = nil
	local char = player.Character
	local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end
	if (part.Position - root.Position).Magnitude > collectRadius() then return end
	burst(part.Position)
	gulp()
end)
