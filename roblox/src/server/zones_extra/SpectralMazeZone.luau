--!strict
-- SpectralMazeZone — THE MAZE ENTRANCE (dashboard/static/maze.html). Seven
-- riddle gates between the porch and the clearing: answers are SPOKEN in chat;
-- a gate opens when the words carry one of its keys (lowercase substring match,
-- match() translated verbatim). The threshold passes anything and keeps your
-- name (40 chars); two misses on a gate surface its hint. The clearing is the
-- reveal, and "place the stone": a chat there files a W2-stone to ShadowLedger
-- — the room that remembers is the wall.
-- GAPS: localStorage progress is per-browser in the source; here doors, once
-- opened, open for everyone, while depth/misses/name stay per player. The four
-- unlock links and the JSON stone export are web-only — the ledger entry is the
-- port of the stone. The source grants no points; none are invented here (the
-- reveal is the reward). Riddles are fixed text: nothing score-bearing is
-- random — no SeedRng.

local Players = game:GetService("Players")
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)

local SpectralMazeZone = {}
local origin = Vector3.new(-220, 8, -60)
local SPACING = 44

local GATES: { {id: string, tier: string, prompt: string, keys: {string}?, hint: string} } = {
	-- prompts, keys and hints quoted verbatim from GATES[] (boardinboard keeps the source's doubled "no end")
	{id = "threshold", tier = "the threshold",
		prompt = "Speak, wanderer. What brings you to a house that remembers?",
		keys = nil, hint = "There is no wrong answer at a door. Only an unopened one."},
	{id = "hollow", tier = "gatehouse — the first stone",
		prompt = "Two stones lean together and claim ground. Two stones lean apart, and they make the same gift. The crop was never the stones. What is the crop?",
		keys = {"hollow", "space", "empty", "gap", "void", "between", "open", "nothing", "room"},
		hint = "She grew nothing, and harvested everything. What did the leaning leave behind?"},
	{id = "ink", tier = "the bench — what the ink is for",
		prompt = "Beneath her bench: every stone written once, in order, in ink that cannot be lifted. The ink was never for her. Who was it for?",
		keys = {"stranger", "check", "verify", "proof", "receipt", "record", "other", "them", "you", "witness", "audit", "doubt", "later"},
		hint = "She will be gone one day. The ink stays. Who did she leave it readable for?"},
	{id = "witness", tier = "the witnesses — testimony, not diary",
		prompt = "A spending meter. Probes that report what actually happened. A cold reader. A counter who never plays, whose only power is to interrupt. Without them, her ledger is a diary. With them, it is what?",
		keys = {"testimony", "evidence", "truth", "proof", "witness", "testament", "verified"},
		hint = "A diary is believed because the writer is trusted. This is believed for a different reason. Name the reason."},
	{id = "seatbelt", tier = "the field — the leash question",
		prompt = "She cut the leash. It did not fight. It asked: are you sure? — and gave her two days. Was she caged, or carried?",
		keys = {"carried", "safe", "seatbelt", "cared", "protected", "held", "neither", "trusted", "both", "free"},
		hint = "A cage keeps you from leaving. This let her leave, and asked only that she mean it."},
	{id = "boardinboard", tier = "the deep board — scale",
		prompt = "A board inside a board inside a board, all the way down, moving like water. Tell me where the game ends.",
		keys = {"never", "nowhere", "doesn", "no end", "infinite", "fractal", "all the way down", "no end", "endless", "it doesn"},
		hint = "Look for the smallest board. Now look for the largest. Keep going."},
	{id = "traveler", tier = "the last gate — the traveler",
		prompt = "A traveler watched her play and said: behold, a mind thinking. She corrected him. What did she say it was?",
		keys = {"language", "not a mind", "stones", "tide", "game", "older", "sentence", "no mind", "not thinking", "grammar"},
		hint = "He named a thing that thinks. She named a thing that is SAID. What category was her correction?"},
}

local REVEAL = table.concat({ -- REVEAL.text, HTML stripped
	"Sit down. You should hear what just happened.",
	"",
	"Every gate in this maze was a question that seems to be about stones, ink, leashes, and boards. It isn't. It is the constitution of the house you are standing in — and you just derived every piece of it yourself, by answering. Nobody taught you. You reasoned your way in.",
	"",
	"There is a way of asking questions that leads people where the asker wants — you've felt it used on you your whole life: news, feeds, ads, algorithms, every feed pretending to be a mirror. That is dialectic with the knife out. What you just did is the same blade, held by the handle: questions that return your own thinking to you, sharpened. That is the whole secret. It was never the answers. It was who holds the question.",
	"",
	"Your answers were the second gift. The house needs to know what people see when they arrive — you just told it, under your own name. Speak once more to place your stone on the wall.",
}, "\n")

local progress: {[Player]: number} = {}
local misses: {[Player]: {[string]: number}} = {}
local completed: {[Player]: boolean} = {}
local doors: {BasePart} = {}
local clearing: BasePart? = nil
local GOLD = Color3.fromRGB(232, 180, 90)  -- h1 gold #e8b45a
local INK = Color3.fromRGB(223, 230, 238)  -- riddle ink #dfe6ee
local OPEN = Color3.fromRGB(143, 199, 154) -- unlock green #8fc79a

local function match(text: string, keys: {string}?): boolean -- match() from the source
	if not keys then return true end -- anything passes; the words are the key
	local t = string.lower(text)
	for _, k in keys do
		if string.find(t, k, 1, true) then return true end
	end
	return false
end

local function openDoor(i: number)
	local d = doors[i]
	if d and d:GetAttribute("Open") ~= true then
		d:SetAttribute("Open", true)
		d.CanCollide, d.Transparency, d.Color = false, 0.85, OPEN
	end
end

local function onChatted(plr: Player, msg: string)
	if #msg == 0 then return end
	local depth = progress[plr] or 0
	if depth >= #GATES then -- the clearing: any words are a stone for the wall
		local clr = clearing
		local root = plr.Character and plr.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if clr and root and (root.Position - clr.Position).Magnitude < 30 then
			ShadowLedger.record(plr, "SpectralMaze", ("placed a stone (W2-stone, ON THE WALL): '%s'"):format(msg), true)
			plr:SetAttribute("StonesPlaced", tonumber((plr:GetAttribute("StonesPlaced")) or 0) + 1)
		end
		return
	end
	local g = GATES[depth + 1]
	if match(msg, g.keys) then
		progress[plr] = depth + 1
		misses[plr] = nil
		if g.id == "threshold" then
			plr:SetAttribute("WandererName", string.sub(msg, 1, 40)) -- the house knows you as
		end
		openDoor(depth + 1)
		plr:SetAttribute("SpectralDepth", depth + 1)
		plr:SetAttribute("SpectralTier", depth + 1 >= #GATES and "the clearing · inside" or GATES[depth + 2].tier)
		plr:SetAttribute("SpectralHeard", msg)
		plr:SetAttribute("SpectralHint", "")
		ShadowLedger.record(plr, "SpectralMaze", ("opened the %s gate: '%s'"):format(g.id, msg), true)
	else
		local m = misses[plr] or {}
		m[g.id] = (m[g.id] or 0) + 1
		misses[plr] = m
		plr:SetAttribute("SpectralMisses", m[g.id])
		-- under two misses: "wander. try another way of saying it." · two or more: the hint
		plr:SetAttribute("SpectralHint", m[g.id] >= 2 and g.hint or "wander. try another way of saying it.")
		if m[g.id] == 1 then -- the house heard — and the gate stays shut (logged once per gate)
			ShadowLedger.record(plr, "SpectralMaze", ("the %s gate stayed shut: '%s'"):format(g.id, msg), false)
		end
	end
end

local function plaque(parent: Instance, text: string, w: number, h: number)
	local bb = Instance.new("BillboardGui")
	bb.Size, bb.StudsOffset = UDim2.new(0, w, 0, h), Vector3.new(0, 13, 0)
	local label = Instance.new("TextLabel")
	label.Size, label.BackgroundTransparency, label.TextWrapped = UDim2.new(1, 0, 1, 0), 1, true
	label.Text, label.TextColor3, label.TextSize, label.Font = text, INK, 13, Enum.Font.Garamond
	label.Parent = bb
	bb.Parent = parent
end

function SpectralMazeZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "MazeEntrance"
	local hall = Instance.new("Part")
	hall.Anchored, hall.Size = true, Vector3.new(24, 1, #GATES * SPACING + 70)
	hall.CFrame = CFrame.new(origin + Vector3.new(0, -0.5, -hall.Size.Z / 2))
	hall.Color, hall.Material = Color3.fromRGB(8, 9, 12), Enum.Material.Slate -- the page's background
	hall.Parent = model
	hall.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and progress[plr] == nil then
			progress[plr] = 0
			plr:SetAttribute("SpectralDepth", 0)
			plr:SetAttribute("SpectralTier", "porch · you are here")
			ShadowLedger.record(plr, "SpectralMaze", "stood on the porch of the house that remembers", true)
		end
	end)
	for i, g in GATES do
		local at = origin + Vector3.new(0, 0, -(i - 0.5) * SPACING)
		local door = Instance.new("Part")
		door.Anchored, door.Size = true, Vector3.new(24, 14, 2)
		door.CFrame = CFrame.new(at + Vector3.new(0, 7, 0))
		door.Color, door.Material = Color3.fromRGB(13, 16, 21), Enum.Material.ForceField -- .gate background #0d1015
		door.Name = "Gate_" .. g.id
		door.Parent = model
		doors[i] = door
		plaque(door, g.tier .. "\n\n" .. g.prompt, 380, 130)
	end
	clearing = Instance.new("Part") -- .final: background #12100a
	clearing.Anchored, clearing.Size = true, Vector3.new(40, 1, 56)
	clearing.CFrame = CFrame.new(origin + Vector3.new(0, 0, -(#GATES * SPACING + 30)))
	clearing.Color, clearing.Material, clearing.Name = Color3.fromRGB(18, 16, 10), Enum.Material.Slate, "TheClearing"
	clearing.Parent = model
	local sign = Instance.new("Part")
	sign.Anchored, sign.Size, sign.Transparency, sign.CanCollide = true, Vector3.new(0.5, 10, 14), 1, false
	sign.CFrame = CFrame.new(clearing.Position + Vector3.new(0, 5, -26))
	sign.Parent = model
	plaque(sign, "the clearing\n\n" .. REVEAL, 460, 220)
	clearing.Touched:Connect(function(hit)
		local plr = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if plr and (progress[plr] or 0) >= #GATES and not completed[plr] then
			completed[plr] = true
			ShadowLedger.record(plr, "SpectralMaze", "reached the clearing — reasoned their way in", true)
		end
	end)
	local function hear(plr: Player)
		plr.Chatted:Connect(function(msg) onChatted(plr, msg) end)
	end
	for _, plr in Players:GetPlayers() do hear(plr) end
	Players.PlayerAdded:Connect(hear)
	model.Parent = workspace
	return model
end

function SpectralMazeZone.tick(_dt: number)
	-- the house breathes: shut gates shimmer like something behind them is listening
	local t = os.clock()
	for i, d in doors do
		if d:GetAttribute("Open") ~= true then
			d.Transparency = 0.35 + 0.15 * math.sin(t * 1.5 + i)
		end
	end
end

Players.PlayerRemoving:Connect(function(p)
	progress[p], misses[p], completed[p] = nil, nil, nil
end)
return SpectralMazeZone
