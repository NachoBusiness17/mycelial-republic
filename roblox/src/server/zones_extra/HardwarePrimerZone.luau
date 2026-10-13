--!strict
-- HardwarePrimerZone — Room 1 of the electronics dungeon, ported from
-- dashboard/static/hardware_primer.html; every constant is that file's own
-- (β=100 per hand, toll 0.7V×2, gates 18/2600 µA, brightness law
-- log10(1+β²·w)·22 cap 100, verdict tolerance ±12, whisper 0-60 µA).
-- PREDICT before you MEASURE — no prediction, no verdict. Educational zone:
-- earns credibility, not revenue — no currency changes hands here.

local Players = game:GetService("Players")
local ServerScriptService = game:GetService("ServerScriptService")
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)
-- ledger lookup via the SSS root: resolves whether this module sits in
-- zones_extra or is moved flat by central wiring (init.server owns wiring)

local HardwarePrimerZone = {}
local origin = Vector3.new(220, 8, 220)
local INK = Color3.fromRGB(110, 198, 181) -- the primer's --ink
local TXT = Color3.fromRGB(207, 232, 226)
local GOLD = Color3.fromRGB(255, 215, 106)

-- the law, executable (verbatim from the primer)
local BETA = 100 -- each hand multiplies 100x
local GATE1_UA = 18 -- first hand opens when whisper*BETA >= 18 µA
local GATE2_UA = 2600 -- second hand when whisper*BETA*BETA >= 2600 µA
local STANDS = 12 -- a prediction stands within ±12 of the measurement

local whisper = 0
local calls: { [number]: number } = {} -- UserId -> predicted brightness
local gates: { BasePart } = {}
local beacon: BasePart? = nil
local beaconLight: PointLight? = nil
local hud: TextLabel? = nil

local function brightness(w: number): number
	if w <= 0 then return 0 end
	return math.min(100, math.round(math.log10(1 + BETA * BETA * w) * 22))
end

local function say(player: Player, text: string)
	print(("[HardwarePrimer] %s hears: %s"):format(player.Name, text))
end

local function lbl(parent: Instance, pos: UDim2, size: UDim2, text: string, color: Color3, wrap: boolean): TextLabel
	local t = Instance.new("TextLabel")
	t.Position = pos; t.Size = size; t.BackgroundTransparency = 1
	t.TextScaled = true; t.TextWrapped = wrap; t.Font = Enum.Font.Code
	t.TextColor3 = color; t.Text = text; t.Parent = parent
	return t
end

local function tag(part: BasePart, text: string): TextLabel
	local gui = Instance.new("BillboardGui")
	gui.Size = UDim2.fromScale(10, 1.6); gui.StudsOffset = Vector3.new(0, 3, 0); gui.AlwaysOnTop = true
	local t = lbl(gui, UDim2.new(), UDim2.fromScale(1, 1), text, TXT, false)
	gui.Parent = part
	return t
end

local function plaque(parent: Instance, pos: Vector3, title: string, body: string)
	local p = Instance.new("Part")
	p.Anchored = true; p.Size = Vector3.new(24, 8, 0.5); p.Position = pos
	p.Color = Color3.fromRGB(10, 16, 14); p.Parent = parent
	local gui = Instance.new("SurfaceGui")
	gui.Face = Enum.NormalId.Back; gui.PixelsPerStud = 5
	lbl(gui, UDim2.new(), UDim2.fromScale(1, 0.22), title, INK, false)
	lbl(gui, UDim2.fromScale(0, 0.22), UDim2.fromScale(1, 0.78), body, TXT, true)
	gui.Parent = p
end

local function pad(parent: Model, pos: Vector3, action: string, object: string, hold: number, fn: (Player) -> ())
	local p = Instance.new("Part")
	p.Anchored = true; p.Size = Vector3.new(4, 0.4, 4); p.Position = pos
	p.Color = Color3.fromRGB(13, 21, 18); p.Material = Enum.Material.Neon; p.Parent = parent
	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = action; prompt.ObjectText = object; prompt.HoldDuration = hold
	prompt.MaxActivationDistance = 8; prompt.Parent = p
	prompt.Triggered:Connect(fn)
end

function HardwarePrimerZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "HardwarePrimer"

	local floor = Instance.new("Part")
	floor.Anchored = true; floor.Size = Vector3.new(64, 1, 88)
	floor.Position = origin - Vector3.new(0, 0.5, 0)
	floor.Color = Color3.fromRGB(6, 10, 9); floor.Material = Enum.Material.Slate; floor.Parent = model

	plaque(model, origin + Vector3.new(0, 6, -42), "THE HARDWARE PRIMER — ROOM 1 · THE DARLINGTON PAIR",
		"THE LAW: a small signal, passed hand to hand, moves great currents — but every hand takes its toll of 0.7 volts before the gate opens. Nothing is free; the amplification is bought with the toll. STATBLOCK: AC 100kΩ input impedance · GAIN β≈10,000 — the whisper becomes a shout · THE TOLL 1.4V (two hands, 0.7 each) · WEAKNESS slow to let go (saturation lingers) · ALIGNMENT Lawful — it multiplies exactly, without opinion.")

	local console = Instance.new("Part")
	console.Anchored = true; console.Size = Vector3.new(12, 3, 4)
	console.Position = origin + Vector3.new(-20, 1.5, -24)
	console.Color = Color3.fromRGB(13, 21, 18); console.Parent = model
	tag(console, "the whisper console (µA)")

	pad(model, origin + Vector3.new(-24, 0.2, -18), "+ whisper", "whisper console (µA)", 0.3, function(_player)
		whisper = math.min(60, whisper + (whisper >= 40 and 10 or 5))
	end)
	pad(model, origin + Vector3.new(-20, 0.2, -18), "- whisper", "whisper console (µA)", 0.3, function(_player)
		whisper = math.max(0, whisper - (whisper > 40 and 10 or 5))
	end)
	pad(model, origin + Vector3.new(-16, 0.2, -18), "silence the whisper", "whisper console (µA)", 0.3, function(_player)
		whisper = 0
	end)

	for i = 1, 2 do
		local g = Instance.new("Part")
		g.Anchored = true; g.CanCollide = false; g.Size = Vector3.new(10, 8, 0.8)
		g.Position = origin + Vector3.new(0, 4, i * 14 - 4)
		g.Color = Color3.fromRGB(51, 63, 68)
		g.Name = i == 1 and "FirstHand" or "SecondHand"; g.Parent = model
		tag(g, (i == 1 and "FIRST HAND" or "SECOND HAND") .. " · toll 0.7V")
		gates[i] = g
	end

	local b = Instance.new("Part")
	b.Shape = Enum.PartType.Ball; b.Anchored = true; b.Size = Vector3.new(4, 4, 4)
	b.Position = origin + Vector3.new(0, 5, 36)
	b.Color = GOLD; b.Material = Enum.Material.Neon; b.Name = "Beacon"; b.Parent = model
	beacon = b
	local light = Instance.new("PointLight")
	light.Range = 48; light.Color = GOLD; light.Parent = b
	beaconLight = light

	local board = Instance.new("Part")
	board.Anchored = true; board.CanCollide = false; board.Transparency = 1; board.Size = Vector3.new(1, 1, 1)
	board.Position = origin + Vector3.new(0, 12, 8); board.Parent = model
	hud = tag(board, "whisper: 0 µA · beacon: 0/100")

	plaque(model, origin + Vector3.new(24, 5, 0), "THE PROOF — predict before you measure",
		"Set the whisper at the console. PREDICT the beacon's brightness (0-100) by the law — brightness is bought with β² × the whisper, and the toll must be paid first. Then MEASURE. A call within ±12 stands; a hit unlocks the restatement. No prediction, no verdict.")

	pad(model, origin + Vector3.new(20, 0.2, -4), "PREDICT: lock the call", "the proof", 0.5, function(player)
		local cur = calls[player.UserId] or -10
		calls[player.UserId] = (cur + 10) % 110 -- cycles 0..100 by 10
		say(player, ("call locked: %d/100"):format(calls[player.UserId]))
	end)
	pad(model, origin + Vector3.new(28, 0.2, -4), "MEASURE IT", "the proof", 1, function(player)
		local call = calls[player.UserId]
		if call == nil then return say(player, "no prediction, no verdict — lock a call first.") end
		local actual = brightness(whisper)
		if math.abs(actual - call) <= STANDS then
			player:SetAttribute("HardwareProof", true)
			ShadowLedger.record(player, "HardwarePrimer", ("called %d, measured %d/100 — lawful amplification, tolls paid"):format(call, actual), true)
			say(player, ("MEASURED: %d/100 — your call stood. Seal the restatement at the wall."):format(actual))
		else
			ShadowLedger.record(player, "HardwarePrimer", ("called %d, measured %d/100 — the law multiplies exactly; re-read the toll"):format(call, actual), false)
			say(player, ("MEASURED: %d/100 — you called %d. The law multiplies exactly; re-read the toll."):format(actual, call))
		end
	end)
	pad(model, origin + Vector3.new(24, 0.2, 12), "SEAL IT", "the restatement", 1.5, function(player)
		if not player:GetAttribute("HardwareProof") then
			return say(player, "the wall asks only those who measured — predict, then measure.")
		end
		player:SetAttribute("HardwareSealed", true)
		ShadowLedger.record(player, "HardwarePrimer", "sealed the restatement: the beacon waits for 1.4V because two hands each take 0.7V before the gate opens (retelling recorded, not graded)", true)
		say(player, "sealed. the primer is a seed: copy it, plant it anywhere, it grows rooms.")
	end)

	Players.PlayerRemoving:Connect(function(player)
		calls[player.UserId] = nil
	end)

	model.Parent = workspace
	return model
end

function HardwarePrimerZone.tick(_dt: number)
	local dark = Color3.fromRGB(51, 63, 68)
	local paid1 = whisper * BETA >= GATE1_UA
	local paid2 = whisper * BETA * BETA >= GATE2_UA
	for i, g in ipairs(gates) do
		local paid = if i == 1 then paid1 else paid2
		g.Color = paid and INK or dark
		g.Material = paid and Enum.Material.Neon or Enum.Material.SmoothPlastic
	end
	local b = brightness(whisper)
	if beacon then
		local s = 4 + b * 0.09
		beacon.Size = Vector3.new(s, s, s)
		beacon.Transparency = 0.95 - b * 0.009
	end
	if beaconLight then beaconLight.Brightness = 0.2 + b * 0.03 end
	if hud then
		hud.Text = ("whisper: %d µA · after hand 1 (β=100): %d µA · after hand 2: %d µA · beacon: %d/100")
			:format(whisper, whisper * BETA, whisper * BETA * BETA, b)
	end
end

return HardwarePrimerZone
