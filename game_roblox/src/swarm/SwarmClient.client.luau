--[[
    SwarmClient — PRIVLIDGE. The beat IS the ruleset.
    Input, camera, HUD, juice. Keyboard: A/D strafe, Space jump, R restart.
]]

--!strict
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local camera = workspace.CurrentCamera

local Juice = require(script.Parent:WaitForChild("Juice"))

-- No default character (CharacterAutoLoads=false): take the camera so
-- our follow rig owns CFrame writes.
camera.CameraType = Enum.CameraType.Scriptable

local Remotes = ReplicatedStorage:WaitForChild("Remotes")
local RemoteStateUpdate = Remotes:WaitForChild("StateUpdate")
local RemoteJuice = Remotes:WaitForChild("Juice")
local RemoteDeath = Remotes:WaitForChild("Death")
local RemoteScore = Remotes:WaitForChild("ScoreUpdate")
local RemoteInput = Remotes:WaitForChild("Input")
local RemoteRestart = Remotes:WaitForChild("Restart")
local RemoteShop = Remotes:WaitForChild("Shop")

local PRIVRemotes = ReplicatedStorage:WaitForChild("PRIVLIDGE_Remotes")
local BeatPulse = PRIVRemotes:WaitForChild("BeatPulse")
local GrooveStep = PRIVRemotes:WaitForChild("GrooveStep")
local GrooveBreak = PRIVRemotes:WaitForChild("GrooveBreak")
local RiserRemote = PRIVRemotes:WaitForChild("Riser")

-- ============================================================
-- SFX — engine built-in sounds (ship with Roblox, no uploads).
-- Rising pitch with the chain is rendered here, from chainLevel.
-- ============================================================
local SoundService = game:GetService("SoundService")

local PITCH_OFFSETS = { 0, 2, 4, 7, 9, 12 } -- semitones per chain level

local SFX_DEFS = {
	jump = { id = "rbxasset://sounds/swoosh.wav", volume = 0.35 },
	land = { id = "rbxasset://sounds/impact_water.mp3", volume = 0.3 },
	collect = { id = "rbxasset://sounds/electronicpingshort.wav", volume = 0.45 },
	levelup = { id = "rbxasset://sounds/victory.wav", volume = 0.45 },
	miss = { id = "rbxasset://sounds/button.wav", volume = 0.4 },
	death = { id = "rbxasset://sounds/uuhhh.mp3", volume = 0.7 },
	tick = { id = "rbxasset://sounds/electronicpingshort.wav", volume = 0.12 },
}

local sfxPool: { [string]: Sound } = {}

function playSfx(name: string, playbackSpeed: number?)
	local def = SFX_DEFS[name]
	if not def then return end
	local s = sfxPool[name]
	if not s then
		s = Instance.new("Sound")
		s.SoundId = def.id
		s.Volume = def.volume
		s.Parent = SoundService
		sfxPool[name] = s
	end
	s.PlaybackSpeed = playbackSpeed or 1
	s.TimePosition = 0
	s:Play()
end

local function chainPitch(chainLevel: number): number
	local semis = PITCH_OFFSETS[math.clamp(chainLevel + 1, 1, #PITCH_OFFSETS)]
	return 2 ^ (semis / 12)
end

local currentChainLevel = 0

-- ============================================================
-- HUD
-- ============================================================
local gui = Instance.new("ScreenGui")
gui.Name = "PRIVLIDGE_HUD"
gui.ResetOnSpawn = false
gui.IgnoreGuiInset = true
gui.Parent = player:WaitForChild("PlayerGui")

local function label(name: string, size: number, pos: UDim2, align: Enum.TextXAlignment, color: Color3): TextLabel
	local l = Instance.new("TextLabel")
	l.Name = name
	l.BackgroundTransparency = 1
	l.Size = UDim2.fromScale(1, 0)
	l.Position = pos
	l.Font = Enum.Font.Code
	l.TextSize = size
	l.TextXAlignment = align
	l.TextColor3 = color
	l.TextStrokeTransparency = 0.6
	l.Text = ""
	l.Parent = gui
	return l
end

local ScoreLabel = label("Score", 34, UDim2.new(0, 0, 0, 24), Enum.TextXAlignment.Center, Color3.fromRGB(255, 240, 120))
ScoreLabel.Text = "RUN 0"

local BankLabel = label("Bank", 16, UDim2.new(0, 0, 0, 62), Enum.TextXAlignment.Center, Color3.fromRGB(160, 160, 190))

local MultLabel = label("Mult", 22, UDim2.new(0, 24, 0, 24), Enum.TextXAlignment.Left, Color3.fromRGB(0, 255, 180))
MultLabel.Text = "x1"

local DeathOverlay: Frame = Instance.new("Frame")
DeathOverlay.Name = "DeathOverlay"
DeathOverlay.Size = UDim2.fromScale(1, 1)
DeathOverlay.BackgroundColor3 = Color3.fromRGB(4, 0, 10)
DeathOverlay.BackgroundTransparency = 1
DeathOverlay.BorderSizePixel = 0
DeathOverlay.Visible = false
DeathOverlay.Parent = gui

local DeathTitle = Instance.new("TextLabel")
DeathTitle.BackgroundTransparency = 1
DeathTitle.Size = UDim2.fromScale(1, 0.2)
DeathTitle.Position = UDim2.fromScale(0, 0.32)
DeathTitle.Font = Enum.Font.Code
DeathTitle.TextSize = 52
DeathTitle.TextColor3 = Color3.fromRGB(255, 80, 80)
DeathTitle.Text = "RUN OVER"
DeathTitle.Parent = DeathOverlay

local DeathStats = Instance.new("TextLabel")
DeathStats.BackgroundTransparency = 1
DeathStats.Size = UDim2.fromScale(0.9, 0.1)
DeathStats.Position = UDim2.fromScale(0.05, 0.55)
DeathStats.Font = Enum.Font.Code
DeathStats.TextSize = 22
DeathStats.TextScaled = true
DeathStats.TextWrapped = true
DeathStats.TextColor3 = Color3.fromRGB(220, 220, 240)
DeathStats.Text = ""
DeathStats.Parent = DeathOverlay

local DeathHint = Instance.new("TextLabel")
DeathHint.BackgroundTransparency = 1
DeathHint.Size = UDim2.fromScale(1, 0.05)
DeathHint.Position = UDim2.fromScale(0, 0.63)
DeathHint.Font = Enum.Font.Code
DeathHint.TextSize = 20
DeathHint.TextColor3 = Color3.fromRGB(255, 240, 120)
DeathHint.Text = "PRESS R / RETRY TO RUN AGAIN"
DeathHint.Parent = DeathOverlay

-- Touch path for restart: a real button so phones are never softlocked.
local RestartButton = Instance.new("TextButton")
RestartButton.Size = UDim2.fromScale(0.34, 0.075)
RestartButton.Position = UDim2.fromScale(0.33, 0.80)
RestartButton.Font = Enum.Font.Code
RestartButton.TextSize = 26
RestartButton.Text = "RUN AGAIN"
RestartButton.BackgroundColor3 = Color3.fromRGB(255, 60, 200)
RestartButton.TextColor3 = Color3.new(0, 0, 0)
RestartButton.BorderSizePixel = 0
RestartButton.Parent = DeathOverlay
RestartButton.Activated:Connect(function()
	RemoteRestart:FireServer()
end)

-- ============================================================
-- SHOP — the bank becomes gear between runs. Server validates.
-- ============================================================
local UPGRADE_MAX = 5

local currentBanked = 0
local currentUpgrades = { speed = 0, jump = 0 }

local shopButtons: { [string]: TextButton } = {}

local function makeShopButton(key: string, xPos: number): TextButton
	local b = Instance.new("TextButton")
	b.Name = "Shop_" .. key
	b.Size = UDim2.fromScale(0.38, 0.075)
	b.Position = UDim2.fromScale(xPos, 0.72)
	b.Font = Enum.Font.Code
	b.TextSize = 19
	b.Text = ""
	b.BackgroundColor3 = Color3.fromRGB(90, 90, 110)
	b.TextColor3 = Color3.new(0, 0, 0)
	b.BorderSizePixel = 0
	b.Parent = DeathOverlay
	b.Activated:Connect(function()
		RemoteShop:FireServer(key)
	end)
	shopButtons[key] = b
	return b
end

makeShopButton("speed", 0.08)
makeShopButton("jump", 0.54)

local function refreshShop()
	for key, btn in pairs(shopButtons) do
		local lvl = currentUpgrades[key] or 0
		if lvl >= UPGRADE_MAX then
			btn.Text = (key:upper()) .. " MAX"
			btn.BackgroundColor3 = Color3.fromRGB(70, 70, 90)
			btn.TextColor3 = Color3.fromRGB(200, 200, 220)
		else
			local cost = 150 * (2 ^ lvl)
			btn.Text = ("+%s LV%d — %d"):format(key:upper(), lvl + 1, cost)
			local affordable = currentBanked >= cost
			btn.BackgroundColor3 = affordable and Color3.fromRGB(0, 255, 180) or Color3.fromRGB(90, 90, 110)
			btn.TextColor3 = Color3.new(0, 0, 0)
		end
	end
end

RemoteShop.OnClientEvent:Connect(function(reply)
	if reply.key == "speed" or reply.key == "jump" then
		currentUpgrades[reply.key] = reply.level
	end
	currentBanked = reply.banked
	refreshShop()
	playSfx(reply.ok and "collect" or "miss", reply.ok and 0.6 or 0.5)
end)

-- Center status flash ("SPEED UP x1.3")
local StatusLabel = Instance.new("TextLabel")
StatusLabel.Size = UDim2.fromScale(1, 0.1)
StatusLabel.Position = UDim2.fromScale(0, 0.2)
StatusLabel.BackgroundTransparency = 1
StatusLabel.Font = Enum.Font.Code
StatusLabel.TextSize = 40
StatusLabel.TextColor3 = Color3.fromRGB(255, 200, 0)
StatusLabel.TextStrokeTransparency = 0.5
StatusLabel.TextTransparency = 1
StatusLabel.Text = ""
StatusLabel.Parent = gui

-- Beat bar: bottom center, flashes on the downbeat
local BeatBar = Instance.new("Frame")
BeatBar.Name = "BeatBar"
BeatBar.AnchorPoint = Vector2.new(0.5, 1)
BeatBar.Position = UDim2.new(0.5, 0, 1, -18)
BeatBar.Size = UDim2.new(0, 220, 0, 5)
BeatBar.BackgroundColor3 = Color3.fromRGB(0, 200, 255)
BeatBar.BorderSizePixel = 0
BeatBar.Parent = gui

-- ============================================================
-- INPUT — ContextActionService: one bind covers keyboard, gamepad and
-- touch (touch buttons render only on touch devices; no more R-key
-- softlock on mobile).
-- ============================================================
local CAS = game:GetService("ContextActionService")

local function actionHandler(actionName: string, inputState: Enum.UserInputState)
	local pressed = inputState == Enum.UserInputState.Begin
	if actionName == "PRIV_Restart" then
		if pressed then
			RemoteRestart:FireServer()
			playSfx("miss", 1.2)
		end
		return Enum.ContextActionResult.Sink
	end
	local action = actionName == "PRIV_Left" and "Left"
		or actionName == "PRIV_Right" and "Right"
		or "Jump"
	RemoteInput:FireServer(action, pressed)
	if action == "Jump" and pressed then
		playSfx("jump")
	end
	return Enum.ContextActionResult.Sink
end

CAS:BindAction("PRIV_Left", actionHandler, true, Enum.KeyCode.A, Enum.KeyCode.Left)
CAS:BindAction("PRIV_Right", actionHandler, true, Enum.KeyCode.D, Enum.KeyCode.Right)
CAS:BindAction("PRIV_Jump", actionHandler, true, Enum.KeyCode.Space, Enum.KeyCode.ButtonA)
CAS:BindAction("PRIV_Restart", actionHandler, true, Enum.KeyCode.R, Enum.KeyCode.ButtonB)

CAS:SetPosition("PRIV_Left", UDim2.new(0.06, 0, 0.62, 0))
CAS:SetPosition("PRIV_Right", UDim2.new(0.24, 0, 0.62, 0))
CAS:SetPosition("PRIV_Jump", UDim2.new(0.82, 0, 0.5, 0))
CAS:SetPosition("PRIV_Restart", UDim2.new(0.82, 0, 0.74, 0))
CAS:SetTitle("PRIV_Left", "◀")
CAS:SetTitle("PRIV_Right", "▶")
CAS:SetTitle("PRIV_Jump", "JUMP")
CAS:SetTitle("PRIV_Restart", "RETRY")

-- ============================================================
-- AUDIO CHANNEL (client leg): the manifest carries the track's measured
-- energy per 8th-note step. The predicted-beat loop indexes it, so bar
-- brightness, bar width and the FOV kick breathe with the actual song.
-- ============================================================
local manifestOk, manifest = pcall(function()
	return require(ReplicatedStorage:WaitForChild("AudioManifest"))
end)
if not manifestOk or typeof(manifest) ~= "table" then
	manifest = {}
end

local stepSeconds = 60 / 122 / 2 -- placeholder until the server speaks
local trackIndex = 0
local lastStep, lastStepAt = 0, os.clock()
local lastBarIndex = 0

local function trackEnergy(): { number }
	local t = trackIndex > 0 and manifest[trackIndex] or nil
	if t and typeof(t.energy) == "table" and #t.energy > 0 then
		return t.energy
	end
	return {}
end

RunService.RenderStepped:Connect(function(dt)
	camera = workspace.CurrentCamera -- Roblox can recreate it; never cache-and-trust
	if not camera then return end
	if camera.CameraType ~= Enum.CameraType.Scriptable then
		camera.CameraType = Enum.CameraType.Scriptable
	end

	-- Predicted continuous step from the last authoritative pulse
	local predicted = lastStep + (os.clock() - lastStepAt) / stepSeconds

	-- Song energy at this step (manifest curve): visuals breathe with the mix
	local energy = trackEnergy()
	local e = 0.5
	if #energy > 0 then
		local i = (math.floor(predicted) % #energy) + 1
		e = math.clamp(energy[i] / 255, 0.15, 1)
	end

	local barIndex = math.floor(predicted / 8)
	if barIndex ~= lastBarIndex then
		lastBarIndex = barIndex
		-- Downbeat: bar flash + FOV kick scaled by the song's own energy
		BeatBar.BackgroundColor3 = Color3.fromRGB(255, 0, 180)
		BeatBar.Size = UDim2.new(0, 220 + math.floor(160 * e), 0, 5 + math.floor(4 * e))
		task.delay(0.12, function()
			BeatBar.BackgroundColor3 = Color3.fromRGB(0, 200, 255)
		end)
		camera.FieldOfView = 72 - 6 * e
		TweenService:Create(camera, TweenInfo.new(0.22, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { FieldOfView = 72 }):Play()
	end
	-- Step phase dims the bar between beats: continuous, not event-driven
	local stepPhase = predicted % 1
	BeatBar.BackgroundTransparency = (1 - e) * 0.5 + 0.3 * stepPhase

	local skater = workspace:FindFirstChild(player.Name .. "_Skater")
	local root = skater and skater:FindFirstChild("Root")
	if not root or not root:IsA("BasePart") then return end

	local target = CFrame.new(root.Position + Vector3.new(0, 7, 13), root.Position + Vector3.new(0, 1, -10))
	local alpha = math.clamp(dt * 6, 0, 1)
	camera.CFrame = camera.CFrame:Lerp(target, alpha) * CFrame.new(Juice.GetShakeOffset())
end)

-- ============================================================
-- EVENTS
-- ============================================================
RemoteScore.OnClientEvent:Connect(function(banked: number, best: number, runScore: number)
	ScoreLabel.Text = "RUN " .. tostring(runScore)
	BankLabel.Text = ("BANK %d  ·  BEST %d"):format(banked, best)
end)

RemoteStateUpdate.OnClientEvent:Connect(function(state)
	if state.alive then
		DeathOverlay.Visible = false
	end
	if state.banked then
		currentBanked = state.banked
	end
	if state.upgrades then
		currentUpgrades = state.upgrades
	end
	if state.stepSeconds and state.stepSeconds > 0 then
		stepSeconds = state.stepSeconds
	end
	if state.trackIndex and typeof(state.trackIndex) == "number" then
		trackIndex = state.trackIndex
	end
	refreshShop()
end)

RemoteDeath.OnClientEvent:Connect(function(reason: string, runScore: number, banked: number, best: number, upgrades)
	currentBanked = banked
	if upgrades then
		currentUpgrades = upgrades
	end
	refreshShop()
	DeathStats.Text = ("%s GOT YOU  ·  RUN %d  ·  BANK %d  ·  BEST %d"):format(
		string.upper(reason), runScore, banked, best)
	DeathOverlay.Visible = true
	DeathOverlay.BackgroundTransparency = 1
	TweenService:Create(DeathOverlay, TweenInfo.new(0.4), { BackgroundTransparency = 0.25 }):Play()
end)

RemoteJuice.OnClientEvent:Connect(function(eventType: string, data)
	if eventType == "trickPerfect" then
		playSfx("collect", chainPitch(currentChainLevel) * 2) -- octave up: perfect
		local intensity = math.clamp(1.2 + (data.chain or 0) / 10, 1.2, 2.5)
		Juice.Fire("bigTrick", nil, intensity)
	elseif eventType == "trickOnBeat" then
		playSfx("collect", chainPitch(currentChainLevel))
		local intensity = math.clamp(1 + (data.chain or 0) / 12, 1, 2.2)
		Juice.Fire("bigTrick", nil, intensity)
	elseif eventType == "miss" then
		playSfx("miss", 0.7)
		Juice.Fire("graze", nil, 0.6)
	elseif eventType == "collect" then
		if data.onBeat then
			playSfx("collect", chainPitch(currentChainLevel))
		else
			playSfx("collect", 0.8) -- flat, dull: off-beat pickup
		end
		Juice.Fire("collect", nil, data.onBeat and 1.2 or 0.7)
	elseif eventType == "graze" then
		Juice.Fire("graze", nil, 0.6)
	elseif eventType == "land" then
		playSfx("land")
		Juice.Fire("land", nil, 0.8)
	elseif eventType == "death" then
		playSfx("death")
		Juice.Fire("death", nil, 1.4)
	elseif eventType == "rampup" then
		-- Legible difficulty: announce every ramp
		playSfx("levelup", 0.8)
		StatusLabel.Text = ("SPEED UP  x%.1f"):format(data.scale or 1)
		StatusLabel.TextTransparency = 0
		TweenService:Create(StatusLabel, TweenInfo.new(1.2, Enum.EasingStyle.Quad, Enum.EasingDirection.In), { TextTransparency = 1 }):Play()
	end
end)

GrooveStep.OnClientEvent:Connect(function(chain: number, chainLevel: number, mult: number, _awarded: number, leveledUp: boolean)
	currentChainLevel = chainLevel
	MultLabel.Text = "x" .. tostring(mult) .. "  ·  " .. tostring(chain)
	if leveledUp then
		playSfx("levelup", 1 + 0.1 * chainLevel)
		MultLabel.TextColor3 = Color3.fromRGB(255, 240, 120)
		task.delay(0.2, function()
			MultLabel.TextColor3 = Color3.fromRGB(0, 255, 180)
		end)
	end
end)

GrooveBreak.OnClientEvent:Connect(function(_lostChain: number, _lostLevel: number)
	currentChainLevel = 0
	MultLabel.Text = "x1  ·  0"
	playSfx("miss", 0.5)
	Juice.Fire("graze", nil, 0.5)
end)

-- Riser: the beat clock warns one bar before the next speed ramp
RiserRemote.OnClientEvent:Connect(function(_leadSteps: number)
	StatusLabel.Text = "SPEED UP INCOMING…"
	StatusLabel.TextTransparency = 0.2
	task.delay(0.9, function()
		StatusLabel.TextTransparency = 1
	end)
end)

BeatPulse.OnClientEvent:Connect(function(step: number, stepInBar: number, stepInBeat: number)
	-- Anchor the predicted-beat loop to the authoritative pulse
	lastStep, lastStepAt = step, os.clock()

	-- Audible metronome on every beat: the player can entrain to the grid
	-- even before a music asset is wired in. Downbeats tick higher.
	if stepInBeat == 0 then
		playSfx("tick", stepInBar == 0 and 1.5 or 1)
	end
end)
