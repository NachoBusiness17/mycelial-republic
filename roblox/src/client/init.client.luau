--!strict
-- finit.client — the one client script: keys in, remotes out, feel out.
-- SPEC t46: portal pads tint by the server-stamped Gate_<zone> attribute
-- (ZoneGate.allianceFor): allied leans green, opposed leans red,
-- independent tints nothing; deterministic local visuals only.
-- SPEC t59: a corner chip echoes the server-stamped Sphere attribute
-- ("Sphere: <name>", ZoneGate.ensureSphere, replicated) with the soul's
-- aggregate Gate_ verdict word tinted per ALLIANCE_TINT; allianceFor's
-- third word is "independent", not "neutral" (never fabricated), and it
-- tints nothing (a negative is a fact).
-- Shift sprint (hold), Q dash, Space double jump, Z/X/C/V abilities,
-- dash FOV kick, ability cooldown chips. Q-040 (cloned-mechanics §2/§3.3):
-- the same inputs bind as ContextActionService touch buttons on touch
-- devices, the cooldown chips move over those buttons, and the mobile jump
-- button (JumpRequest, not a Space InputBegan) feeds the double jump.
-- The server owns validation and cooldowns; this file is a courier with
-- good manners, not a brain.

local Players = game:GetService("Players")
local UserInputService = game:GetService("UserInputService")
local ContextActionService = game:GetService("ContextActionService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local TweenService = game:GetService("TweenService")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer
local remotes = ReplicatedStorage:WaitForChild("Remotes")
local movement = remotes:WaitForChild("Movement") :: RemoteEvent
local ability = remotes:WaitForChild("Ability") :: RemoteEvent
local chat = remotes:WaitForChild("Chat") :: RemoteEvent -- server world-voice (MudBasecamp.say)

local airJumps = 0

-- ability display table (mirrors server REGISTRY; server still owns the truth).
-- `fire` is the server-side ability name from AbilitySlots.REGISTRY that both
-- the keyboard path and the touch buttons send; the server name is the only
-- string it accepts (AbilitySlots.bind matches by name).
local ABILITIES = {
	{ name = "Fire",     key = Enum.KeyCode.Z, attribute = "Abil_Fire",     cd = 0.25, fire = "Fire" },
	{ name = "Thumper",  key = Enum.KeyCode.X, attribute = "Abil_Thumper",  cd = 10,   fire = "ThumperToss" },
	{ name = "Redirect", key = Enum.KeyCode.C, attribute = "Abil_Redirect", cd = 8,    fire = "WingChunRedirect" },
	{ name = "Count",    key = Enum.KeyCode.V, attribute = "Abil_Count",    cd = 20,   fire = "Count" },
}

-- ---- cooldown chips: 4 skill slots, bottom-right cluster ----
-- Q-043 UI pass: each chip is now a panel with a key/name label, a cooldown
-- fill bar that drains across the mirrored cd, an active-window stroke glow
-- (attribute still true = the ability is LIVE), and a cluster-wide dim while
-- the server disables every slot (Carrying = the Steal-a penalty; the server
-- reads the same attribute to refuse each fire, we only paint it). Courier
-- law unchanged: the server owns validation and the cooldown clock; the chip
-- clock starts at the replicated attribute flip, the drain is local math.
local gui = Instance.new("ScreenGui")
gui.Name = "AbilityChips"
gui.ResetOnSpawn = false
gui.Parent = player:WaitForChild("PlayerGui")

local CHIP_BG = Color3.fromRGB(20, 18, 26)
local CHIP_INK = Color3.fromRGB(230, 224, 196)
local CHIP_READY = Color3.fromRGB(143, 199, 154)
local CHIP_FILL = Color3.fromRGB(232, 180, 90)
local CHIP_GLOW = Color3.fromRGB(255, 220, 150)

local chips: { { label: TextLabel, fill: Frame, stroke: UIStroke, last: number, ab: typeof(ABILITIES[1]) } } = {}
for i, ab in ipairs(ABILITIES) do
	local chip = Instance.new("Frame")
	chip.Size = UDim2.new(0, 64, 0, 46)
	chip.Position = UDim2.new(1, -80 * (5 - i), 1, -130)
	chip.BackgroundColor3 = CHIP_BG
	chip.BackgroundTransparency = 0.35
	chip.BorderSizePixel = 0
	chip.Parent = gui
	local corner = Instance.new("UICorner")
	corner.CornerRadius = UDim.new(0, 6)
	corner.Parent = chip
	local stroke = Instance.new("UIStroke")
	stroke.Color = CHIP_GLOW
	stroke.Transparency = 1 -- a ready chip has no border; the active window lights it
	stroke.Parent = chip

	local label = Instance.new("TextLabel")
	label.Size = UDim2.new(1, 0, 1, -6)
	label.BackgroundTransparency = 1
	label.TextColor3 = CHIP_READY
	label.Font = Enum.Font.Garamond
	label.TextSize = 14
	label.Text = ab.key.Name .. "\n" .. ab.name
	label.Parent = chip

	local fill = Instance.new("Frame")
	fill.AnchorPoint = Vector2.new(0, 1)
	fill.Position = UDim2.new(0, 0, 1, 0)
	fill.Size = UDim2.new(0, 0, 0, 3)
	fill.BorderSizePixel = 0
	fill.BackgroundColor3 = CHIP_FILL
	fill.Parent = chip

	table.insert(chips, { label = label, fill = fill, stroke = stroke, last = -math.huge, ab = ab })

	-- server flips the attribute true at fire time; that is our clock start
	player:GetAttributeChangedSignal(ab.attribute):Connect(function()
		if player:GetAttribute(ab.attribute) == true then
			for _, c in ipairs(chips) do
				if c.ab.name == ab.name then c.last = os.clock() end
			end
		end
	end)
end

RunService.RenderStepped:Connect(function()
	local now = os.clock()
	local carrying = player:GetAttribute("Carrying") == true
	for _, c in ipairs(chips) do
		local remain = c.ab.cd - (now - c.last)
		local active = player:GetAttribute(c.ab.attribute) == true
		if remain > 0 then
			c.label.Text = ("%s\n%.1f"):format(c.ab.key.Name, remain)
			c.label.TextColor3 = CHIP_INK
			c.label.TextTransparency = carrying and 0.55 or 0.4
			c.fill.Size = UDim2.new(math.clamp(remain / c.ab.cd, 0, 1), 0, 0, 3)
			c.fill.BackgroundTransparency = carrying and 0.7 or 0
			c.stroke.Transparency = 1
		else
			c.label.Text = c.ab.key.Name .. "\n" .. c.ab.name
			c.label.TextColor3 = active and CHIP_GLOW or CHIP_READY
			c.label.TextTransparency = carrying and 0.55 or 0
			c.fill.Size = UDim2.new(0, 0, 0, 3)
			c.stroke.Transparency = active and 0 or 1
		end
	end
end)

-- ---- dash FOV kick: 70 -> 82 -> 70 on every DashAt bump ----
-- FIX: camera resolved per kick, not captured once. Cause: this script runs
-- once per session and outlives respawns (gui.ResetOnSpawn = false above),
-- but workspace.CurrentCamera is nullable and can be replaced across respawn
-- flows, so a captured reference goes stale and the kick silently dies after
-- a swap. Evidence: same-file respawn-surviving design (ResetOnSpawn false,
-- CharacterAdded re-watch) against the nullable CurrentCamera contract.
player:GetAttributeChangedSignal("DashAt"):Connect(function()
	local cam = workspace.CurrentCamera
	if not cam then return end
	local out = TweenService:Create(cam, TweenInfo.new(0.12, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { FieldOfView = 82 })
	out:Play()
	out.Completed:Once(function()
		local back = workspace.CurrentCamera
		if not back then return end
		TweenService:Create(back, TweenInfo.new(0.3, Enum.EasingStyle.Quad, Enum.EasingDirection.Out), { FieldOfView = 70 }):Play()
	end)
end)

-- ---- portal ring tint: gate verdict (t46), attribute pattern ----
-- The server stamps ZoneGate.allianceFor per wave zone once at join as
-- Gate_<zone> attributes (zone names sanitized to underscores, the same
-- gsub the Portal_ pad suffix is read with, see server ZoneGate.gateAttr).
-- This block only paints: fixed colors, one lerp, no loop. Independent
-- tints nothing (a negative is a fact); opposed is reachable only if the
-- mine ever grows an aligned region row (ZoneGate header seam) and the
-- tint renders it rather than leaving a dead branch. Climb portals carry
-- no Gate_ attribute, so they stay untouched.
local ALLIANCE_TINT: { [string]: Color3 } = {
	allied = Color3.fromRGB(90, 230, 130),
	opposed = Color3.fromRGB(235, 60, 60),
}

local function bindPad(pad: Instance)
	local zone = pad.Name:match("^Portal_(.+)$")
	if not zone then return end
	local key = ("Gate_%s"):format((zone:gsub("%W", "_")))
	local apply = function()
		local part = pad :: BasePart
		if not part:IsA("BasePart") then return end
		local verdict = player:GetAttribute(key)
		if typeof(verdict) ~= "string" then return end
		local tint = ALLIANCE_TINT[verdict :: string]
		if not tint then return end
		part.Color = part.Color:Lerp(tint, 0.45)
	end
	apply()
	player:GetAttributeChangedSignal(key):Connect(apply)
end

for _, pad in ipairs(workspace:GetChildren()) do
	bindPad(pad)
end
workspace.ChildAdded:Connect(bindPad)

-- ---- soul chip: the player's replicated Sphere attribute (t59) ----
-- ZoneGate.ensureSphere stamps "Sphere" on the player server-side, so it
-- replicates and this block only paints (no server change, no client
-- re-derivation of the draw). The word after the name is the soul's
-- aggregate over the same stamped Gate_<zone> verdicts the pads tint, with
-- allianceFor's own precedence (opposition outranks kinship): any opposed
-- decides, else any allied, else independent. Independent tints nothing (a
-- negative is a fact); the chip speaks allianceFor's real verdict words.
local SOUL_TEXT = Color3.fromRGB(230, 224, 196)
local sphereChip = Instance.new("TextLabel")
sphereChip.Size = UDim2.new(0, 170, 0, 22)
sphereChip.Position = UDim2.new(0, 8, 0, 8)
sphereChip.BackgroundColor3 = Color3.fromRGB(20, 18, 26)
sphereChip.BackgroundTransparency = 0.35
sphereChip.TextColor3 = SOUL_TEXT
sphereChip.Font = Enum.Font.Garamond
sphereChip.TextSize = 14
sphereChip.TextXAlignment = Enum.TextXAlignment.Left
sphereChip.Parent = gui

local function refreshSoulChip()
	local sphere = player:GetAttribute("Sphere")
	if typeof(sphere) ~= "string" then
		sphereChip.Text = "Sphere: (unset)" -- attribute not replicated yet
		return
	end
	local verdict = "independent"
	for attr, value in pairs(player:GetAttributes()) do
		if attr:sub(1, 5) == "Gate_" and typeof(value) == "string" then
			if value == "opposed" then
				verdict = "opposed"
			elseif value == "allied" and verdict ~= "opposed" then
				verdict = "allied"
			end
		end
	end
	sphereChip.Text = ("Sphere: %s (%s)"):format(sphere, verdict)
	sphereChip.TextColor3 = ALLIANCE_TINT[verdict] or SOUL_TEXT
end

refreshSoulChip()
player:GetAttributeChangedSignal("Sphere"):Connect(refreshSoulChip)
-- the Gate_ names are the server's sanitized zone list (ZoneGate.gateAttr);
-- the client never re-authors it, so the same signal pattern widens to a
-- prefix filter over AttributeChanged
player.AttributeChanged:Connect(function(attr)
	if attr:sub(1, 5) == "Gate_" then refreshSoulChip() end
end)

-- ---- chat relay log: the server's world-voice lands here (Q-037) ----
-- One FireClient per MudBasecamp.say(): stack the last few lines bottom-left
-- (below the ability chips' mirror, clear of the cathedral panel), fade each
-- out and retire it. Courier law holds: display only, no filtering, no
-- commands — the server already wrote the words it chose to say.
local CHAT_MAX = 7
local chatLog = Instance.new("Frame")
chatLog.Name = "ChatLog"
chatLog.AnchorPoint = Vector2.new(0, 1)
chatLog.Position = UDim2.new(0, 8, 1, -8)
chatLog.Size = UDim2.new(0, 430, 0, 150)
chatLog.BackgroundTransparency = 1
chatLog.Parent = gui
local chatLayout = Instance.new("UIListLayout")
chatLayout.FillDirection = Enum.FillDirection.Vertical
chatLayout.VerticalAlignment = Enum.VerticalAlignment.Bottom
chatLayout.SortOrder = Enum.SortOrder.LayoutOrder
chatLayout.Padding = UDim.new(0, 2)
chatLayout.Parent = chatLog

chat.OnClientEvent:Connect(function(text: unknown)
	if typeof(text) ~= "string" then return end -- not our server's shape
	local line = Instance.new("TextLabel")
	line.Name = "ChatLine"
	line.AutomaticSize = Enum.AutomaticSize.Y
	line.Size = UDim2.new(1, 0, 0, 0)
	line.BackgroundTransparency = 1
	line.Font = Enum.Font.Garamond
	line.TextSize = 14
	line.TextColor3 = SOUL_TEXT
	line.TextXAlignment = Enum.TextXAlignment.Left
	line.TextWrapped = true
	line.Text = text
	line.LayoutOrder = math.huge -- newest paints last; orders below retire age
	line.Parent = chatLog
	-- bounded log: retire the oldest line once past the cap
	local lines: { TextLabel } = {}
	for _, c in ipairs(chatLog:GetChildren()) do
		if c:IsA("TextLabel") then table.insert(lines, c :: TextLabel) end
	end
	if #lines > CHAT_MAX then
		table.sort(lines, function(a, b) return a.LayoutOrder < b.LayoutOrder end)
		lines[1]:Destroy()
	end
	-- relabel LayoutOrder by arrival rank so "oldest" stays well-defined
	for rank, l in ipairs(lines) do
		l.LayoutOrder = rank
	end
	task.delay(6, function()
		local fade = TweenService:Create(line, TweenInfo.new(2, Enum.EasingStyle.Quad, Enum.EasingDirection.In), { TextTransparency = 1, BackgroundTransparency = 1 })
		fade:Play()
		fade.Completed:Once(function() line:Destroy() end)
	end)
end)

local function character(): Model?
	return player.Character
end

local function charHum(): Humanoid?
	local c = character()
	return c and c:FindFirstChildOfClass("Humanoid")
end

-- track grounded-ness client-side for the double jump allowance
local function watch(char: Model)
	local hum = char:WaitForChild("Humanoid") :: Humanoid
	airJumps = 0
	hum.StateChanged:Connect(function(_, new)
		if new == Enum.HumanoidStateType.Landed then
			airJumps = 0
		end
	end)
end

if player.Character then watch(player.Character) end
player.CharacterAdded:Connect(watch)

-- one airjump guard, two entry points: the Space key (keyboard) and
-- JumpRequest (the mobile jump button raises JumpRequest, never a Space
-- InputBegan). The guard is idempotent across both entries because airJumps
-- increments synchronously before the second caller checks it, so a desktop
-- press that raises both events still sends at most one airjump.
local function tryAirJump()
	local hum = charHum()
	if hum and hum:GetState() ~= Enum.HumanoidStateType.Landed
		and hum:GetState() ~= Enum.HumanoidStateType.Jumping
		and airJumps < 1 then
		airJumps += 1
		movement:FireServer("airjump")
	end
end

UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end
	if input.KeyCode == Enum.KeyCode.LeftShift or input.KeyCode == Enum.KeyCode.RightShift then
		movement:FireServer("sprint", true)
	elseif input.KeyCode == Enum.KeyCode.Q then
		movement:FireServer("dash")
	elseif input.KeyCode == Enum.KeyCode.Space then
		tryAirJump()
	else
		for _, ab in ipairs(ABILITIES) do
			if input.KeyCode == ab.key then
				ability:FireServer(ab.fire)
				break
			end
		end
	end
end)

UserInputService.InputEnded:Connect(function(input)
	if input.KeyCode == Enum.KeyCode.LeftShift or input.KeyCode == Enum.KeyCode.RightShift then
		movement:FireServer("sprint", false)
	end
end)

UserInputService.JumpRequest:Connect(tryAirJump)

-- ---- mobile bindings (Q-040): ContextActionService touch buttons ----
-- Spec: cloned-mechanics §2 "Mobile | thumbstick + jump + ContextActionService
-- buttons | ability + dash + interact buttons" and §3.3 "cooldown chips and
-- mobile ContextActionService buttons". Interact is already engine
-- (ProximityPrompt shows its own touch button), so this block covers sprint
-- (hold), dash and the four ability slots. Keycodes are deliberately NOT
-- bound here: the keyboard path above already owns those keys, and a second
-- CAS keycode binding would double-fire every keyboard press. CAS touch
-- buttons render only on touch devices; the TouchEnabled gate keeps the
-- verified desktop path untouched. Button positions are thumb-reach
-- constants, not verified visuals: a live touch playtest stays owed.
if UserInputService.TouchEnabled then
	local function bindTouch(name: string, position: UDim2, onPress: (on: boolean) -> ())
		ContextActionService:BindAction(name, function(_, state)
			onPress(state == Enum.UserInputState.Begin)
			return Enum.ContextActionResult.Sink
		end, true)
		ContextActionService:SetPosition(name, position)
	end

	bindTouch("Sprint", UDim2.new(0, 8, 1, -78), function(on)
		movement:FireServer("sprint", on)
	end)
	bindTouch("Dash", UDim2.new(1, -70, 1, -170), function(on)
		if on then movement:FireServer("dash") end
	end)

	local touchSpots: { [string]: UDim2 } = {
		Fire     = UDim2.new(1, -70, 1, -80),
		Thumper  = UDim2.new(1, -160, 1, -40),
		Redirect = UDim2.new(1, -160, 1, -120),
		Count    = UDim2.new(1, -250, 1, -40),
	}
	for i, ab in ipairs(ABILITIES) do
		local actionName = "Ability_" .. ab.name
		bindTouch(actionName, touchSpots[ab.name], function(on)
			if on then ability:FireServer(ab.fire) end
		end)
		-- cooldown chip OVER the ability button: move the chip into the CAS
		-- button so the countdown paints on top of it. GetButton can return
		-- nil until the engine builds the touch GUI, so the move polls for a
		-- bounded 10s and otherwise leaves the chip as the free-floating
		-- legend it already is (no unbounded wait, no missing-UI crash).
		local chip = chips[i].label
		task.spawn(function()
			for _ = 1, 100 do
				local btn = ContextActionService:GetButton(actionName)
				if btn then
					chip.BackgroundTransparency = 1
					chip.Size = UDim2.fromScale(1, 1)
					chip.Position = UDim2.fromScale(0, 0)
					chip.Parent = btn
					return
				end
				task.wait(0.1)
			end
		end)
	end
end
