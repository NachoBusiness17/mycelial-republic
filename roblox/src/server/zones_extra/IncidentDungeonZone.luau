--!strict
-- IncidentDungeonZone — the maze-arena incident (2026-09-06) as a walkable
-- dungeon, ported from dashboard/static/incident_dungeon.html. One night,
-- four stacked birth defects killed the arena: the seal, the inverted bounce,
-- the unbounded world, the bogus flood. Each room is one defect, the
-- inscription is the buggy line, the right answer opens the way; finish all
-- four and THE RUN opens — a finisher can restate the four defect classes:
-- teaching = the game. All inscriptions, numbers and receipts are the
-- source file's own; nothing here is invented.

local Players = game:GetService("Players")
local ServerScriptService = game:GetService("ServerScriptService")
local ShadowLedger = require((script.Parent:FindFirstChild("ShadowLedger") or script.Parent.Parent:WaitForChild("ShadowLedger")) :: ModuleScript)
-- ledger lookup via the SSS root: resolves whether this module sits in
-- zones_extra or is moved flat by central wiring (init.server owns wiring)

local IncidentDungeonZone = {}
local origin = Vector3.new(220, 8, -220)
local ROOM_W, ROOM_D, WALL_H = 40, 36, 7
local PITCH = ROOM_W + 4
local GOLD = Color3.fromRGB(232, 201, 106) -- solved / the falsifier
local ACCENT = Color3.fromRGB(124, 245, 255) -- the inscriptions' cyan

type Answer = { t: string, ok: boolean }
type RoomSpec = { name: string, insc: string, note: string, answers: { Answer } }

local ROOMS: { RoomSpec } = {
	{ name = "I · THE SEAL",
		insc = "walls: [[0.5,0.5,0.03,1.2]] .map(w=>[w[0]*2, w[1]*2.7, w[2]*2, w[3]*2.7])",
		note = "hh 1.2 × 2.7 = 3.24 > world 2.7 → the wall overflows its own world → FULL SEAL. The spawn chamber could never reach the cheese. The fix: 0.28 × 2.7 = 0.756 — a wall, not a seal.",
		answers = { { t = "CARVE THE GAP (hh 1.2 → 0.28)", ok = true } } },
	{ name = "II · THE INVERTED BOUNCE",
		insc = "if(sdf(nx,ny)<0.012){ move } else { bounce }",
		note = "sdf < 0 means INSIDE a wall. The condition hires the mover only when its next step is stone — they press their faces into the west wall forever. Which predicate lets a mover move?",
		answers = { { t = "sdf(nx,ny) < 0.012", ok = false }, { t = "sdf(nx,ny) >= 0.012", ok = true } } },
	{ name = "III · THE UNBOUNDED WORLD",
		insc = "return d;   // sdf: walls only — no outer term",
		note = "Signed distance of the walls alone; nothing says the world ends. The escaped are still out there: x = -71, -40, -19, -6. An SDF union of primitives is taken with…",
		answers = { { t = "Math.max(d, box)", ok = false }, { t = "Math.min(d, box)", ok = true } } },
	{ name = "IV · THE BOGUS FLOOD",
		insc = "sdf((nx+0.5)/2, (ny+0.5)/2.7)   // neighbors read at wy~25",
		note = "Grid row ny (0..134) divided by the world height 2.7: the flood evaluated its neighbors an entire world above the maze. Which pair of characters was missing from the buggy line?",
		answers = { { t = "GW", ok = false }, { t = "GH", ok = true }, { t = "2.7", ok = false }, { t = "ny", ok = false } } },
}

local solved: { boolean } = {}
local solvedN = 0
local barriers: { BasePart } = {}
-- annotation exactness (t42 triage, lanes/t42.check.txt row 4): glow holds the Instance.new("Part") pedestal orb. Runtime unchanged.
local glow: { { part: Part, room: number } } = {}
local runDoor: BasePart? = nil
local runOpened = false

local function say(player: Player, text: string)
	print(("[IncidentDungeon] %s hears: %s"):format(player.Name, text))
end

local function lbl(parent: Instance, pos: UDim2, size: UDim2, text: string, color: Color3): TextLabel
	local t = Instance.new("TextLabel")
	t.Position = pos; t.Size = size; t.BackgroundTransparency = 1
	t.TextScaled = true; t.TextWrapped = true; t.Font = Enum.Font.Code
	t.TextColor3 = color; t.Text = text; t.Parent = parent
	return t
end

local function tag(part: BasePart, text: string)
	local gui = Instance.new("BillboardGui")
	gui.Size = UDim2.fromScale(10, 1.6); gui.StudsOffset = Vector3.new(0, 3, 0); gui.AlwaysOnTop = true
	lbl(gui, UDim2.new(), UDim2.fromScale(1, 1), text, Color3.fromRGB(200, 230, 217))
	gui.Parent = part
end

-- the wall is the bug: room title, the buggy line carved, the diagnosis note
local function inscription(parent: Instance, pos: Vector3, face: Enum.NormalId, title: string, note: string, mono: string)
	local p = Instance.new("Part")
	p.Anchored = true; p.Size = Vector3.new(24, 9, 0.5); p.Position = pos
	p.Color = Color3.fromRGB(10, 18, 16); p.Parent = parent
	local gui = Instance.new("SurfaceGui")
	gui.Face = face; gui.PixelsPerStud = 5
	lbl(gui, UDim2.new(), UDim2.fromScale(1, 0.18), title, ACCENT)
	lbl(gui, UDim2.fromScale(0, 0.18), UDim2.fromScale(1, 0.26), mono, ACCENT)
	lbl(gui, UDim2.fromScale(0, 0.44), UDim2.fromScale(1, 0.56), note, Color3.fromRGB(200, 230, 217))
	gui.Parent = p
end

local function pedestal(parent: Model, pos: Vector3, roomIdx: number, room: RoomSpec, ans: Answer)
	local p = Instance.new("Part")
	p.Shape = Enum.PartType.Ball
	p.Anchored = true; p.Size = Vector3.new(3, 3, 3); p.Position = pos
	p.Color = GOLD; p.Material = Enum.Material.Neon; p.Parent = parent
	table.insert(glow, { part = p, room = roomIdx })
	local prompt = Instance.new("ProximityPrompt")
	prompt.ActionText = ans.t; prompt.ObjectText = room.name .. " · diagnose"
	prompt.HoldDuration = 1; prompt.MaxActivationDistance = 10; prompt.Parent = p
	prompt.Triggered:Connect(function(player: Player)
		if solved[roomIdx] then return say(player, "the way here is already open.") end
		if not ans.ok then
			ShadowLedger.record(player, "IncidentDungeon", ("the defect disagrees with '%s' — read the inscription again"):format(ans.t), false)
			return say(player, "the defect disagrees — read the inscription again.")
		end
		solved[roomIdx] = true; solvedN += 1
		local gate = barriers[roomIdx]
		if gate then gate.CanCollide = false; gate.Color = GOLD; gate.Transparency = 0.5 end
		ShadowLedger.record(player, "IncidentDungeon", ("room %s diagnosed — '%s' stands; the way opens"):format(room.name, ans.t), true)
		say(player, ("ROOM %s SOLVED — the way opens."):format(room.name))
		if solvedN >= #ROOMS and runDoor and not runOpened then
			runOpened = true; runDoor.CanCollide = false; runDoor.Transparency = 0.6; runDoor.Color = GOLD
			say(player, "THE RUN is open — the falsifier waits beyond it.")
		end
	end)
end

function IncidentDungeonZone.build(): Model
	local model = Instance.new("Model")
	model.Name = "IncidentDungeon"

	local hallLen = (#ROOMS - 1) * PITCH + ROOM_W + 4
	local midX = origin.X - ROOM_W / 2 - 2 + hallLen / 2
	for _, zs in ipairs({ -1, 1 }) do
		local wall = Instance.new("Part")
		wall.Anchored = true; wall.Size = Vector3.new(hallLen, WALL_H, 1)
		wall.Position = Vector3.new(midX, origin.Y + WALL_H / 2, origin.Z + zs * (ROOM_D / 2 + 0.5))
		wall.Color = Color3.fromRGB(16, 27, 24); wall.Parent = model
	end

	for i, room in ipairs(ROOMS) do
		local cx = origin.X + (i - 1) * PITCH
		table.insert(solved, false)

		local floor = Instance.new("Part")
		floor.Anchored = true; floor.Size = Vector3.new(ROOM_W, 1, ROOM_D)
		floor.Position = Vector3.new(cx, origin.Y - 0.5, origin.Z)
		floor.Color = (i % 2 == 0) and Color3.fromRGB(12, 18, 16) or Color3.fromRGB(10, 14, 12)
		floor.Material = Enum.Material.Slate; floor.Parent = model

		inscription(model, Vector3.new(cx, origin.Y + 5.5, origin.Z - ROOM_D / 2 + 0.4), Enum.NormalId.Back,
			room.name, room.note, room.insc)

		local n = #room.answers
		for j, ans in ipairs(room.answers) do
			local px = if n > 1 then cx - 12 + (j - 1) * (24 / (n - 1)) else cx
			pedestal(model, Vector3.new(px, origin.Y + 1.5, origin.Z + 10), i, room, ans)
		end

		if i < #ROOMS then
			local bx = cx + PITCH / 2
			local gate = Instance.new("Part")
			gate.Anchored = true; gate.Size = Vector3.new(1, WALL_H, 10)
			gate.Position = Vector3.new(bx, origin.Y + WALL_H / 2, origin.Z)
			gate.Color = Color3.fromRGB(92, 16, 16); gate.Material = Enum.Material.Neon
			gate.Name = "Barrier_" .. i; gate.Parent = model
			barriers[i] = gate
			for _, zs in ipairs({ -1, 1 }) do
				local flank = Instance.new("Part")
				flank.Anchored = true; flank.Size = Vector3.new(1, WALL_H, (ROOM_D - 10) / 2)
				flank.Position = Vector3.new(bx, origin.Y + WALL_H / 2, origin.Z + zs * (5 + (ROOM_D - 10) / 4))
				flank.Color = Color3.fromRGB(16, 27, 24); flank.Parent = model
			end
		end
	end

	local endX = origin.X + (#ROOMS - 1) * PITCH + ROOM_W / 2 + 2
	for _, zs in ipairs({ -1, 1 }) do
		local seg = Instance.new("Part")
		seg.Anchored = true; seg.Size = Vector3.new(1, WALL_H, (ROOM_D - 12) / 2)
		seg.Position = Vector3.new(endX, origin.Y + WALL_H / 2, origin.Z + zs * (6 + (ROOM_D - 12) / 4))
		seg.Color = Color3.fromRGB(16, 27, 24); seg.Parent = model
	end
	local door = Instance.new("Part")
	door.Anchored = true; door.Size = Vector3.new(1, WALL_H, 12)
	door.Position = Vector3.new(endX, origin.Y + WALL_H / 2, origin.Z)
	door.Color = Color3.fromRGB(16, 27, 24); door.Name = "TheRun"; door.Parent = model
	runDoor = door
	tag(door, "THE RUN · sealed by the boss")
	door.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if not player or not runOpened then return end
		if player:GetAttribute("IncidentRestated") then return end
		player:SetAttribute("IncidentRestated", true)
		ShadowLedger.record(player, "IncidentDungeon",
			"finished the dungeon — restates the four defect classes: SCALE-PAST-WORLD · INVERTED-PREDICATE · UNBOUNDED-DOMAIN · WRONG-TRANSFORM; deepest lesson kept DISPUTED-AND-KEPT: bogus fields look alive (LAW-061)", true)
	end)

	inscription(model, Vector3.new(endX + 0.6, origin.Y + 5.5, origin.Z), Enum.NormalId.Left,
		"THE RUN · THE FALSIFIER",
		"RECEIPTS: queue/handoff/zcode/CONVO.md row 09-06 ~03:0xZ · dashboard/static/maze_arena.html (the FIXED form) · state/_maze_sim_test.js (headless harness, kept) · watch/inbox/MAZE_ARENA_B1_20260906.md · LAW-061: bogus fields look alive — validate the field.",
		"a player who finishes can restate the four defect classes — teaching = the game")

	model.Parent = workspace
	return model
end

function IncidentDungeonZone.tick(_dt: number)
	local t = os.clock()
	for i, gate in ipairs(barriers) do
		if not solved[i] then gate.Transparency = 0.18 + 0.1 * math.sin(t * 4) end
	end
	for _, g in ipairs(glow) do
		g.part.Transparency = solved[g.room] and 0.6 or 0.05 + 0.2 * math.abs(math.sin(t * 2 + g.room))
	end
	if runDoor and not runOpened then runDoor.Transparency = 0.15 + 0.1 * math.sin(t * 2) end
end

return IncidentDungeonZone
