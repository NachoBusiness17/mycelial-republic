-- eigenmap_two_smoke  -  the DRIVER of the headless execution smoke for the
-- eigen-map card's surviving build (card eigenmap, ractor panel 2026-09-26;
-- landed by the revise-eigenmap pass 2026-09-27). The only supported entry
-- point is: .venv/Scripts/python.exe tools/eigenmap_two_smoke.py
--
-- It stages byte-copies of the REAL scripts beside tools/eigenmap_two_smoke_env.luau
-- (the Roblox-API stub environment; see that file's header for why the env is
-- a module) and runs this driver as main.luau under tools/bin/luau/luau.exe:
--   1. requires the REAL CathedralPlate module, calls build() (the same call
--      init.server.luau makes), reads entry(), ticks 50 frames, fires two
--      beacon Touched events with a walker standing on water_computer's
--      world anchor, and dumps every created part from the shared workspace.
--   2. requires the REAL CathedralMapHud.client script (its entire top level
--      executes: panel build, static map draw, Heartbeat connect), fires the
--      heartbeat with the character in place, and dumps the readout.
-- Every machine row printed here is diffed against an independent Python
-- recompute from the scan JSON by tools/eigenmap_two_smoke.py.

local E = require("./SmokeEnv")
local CathedralMap = require("./CathedralMap")
local CathedralPlate = require("./CathedralPlate")
local LedgerStub = require("./ShadowLedgerStub")

CathedralPlate.build()

local entry = CathedralPlate.entry()
print(("entry %.6f %.6f %.6f"):format(entry.X, entry.Y, entry.Z))

local beaconNames = {}
for _, p in ipairs(E.kidsOf(E.workspace)) do
	local nm = p.Name or ""
	if string.sub(nm, 1, 16) == "CathedralBeacon_" then
		table.insert(beaconNames, string.sub(nm, 17))
	end
end
table.sort(beaconNames)
print(("beacons %d %s"):format(#beaconNames, table.concat(beaconNames, ",")))

local stripIdx = 0
for _, p in ipairs(E.kidsOf(E.workspace)) do
	local cf = p.CFrame
	if cf ~= nil and type(cf) == "table" and cf._kind == "lookAt" then
		local sz = p.Size
		stripIdx += 1
		print(("strip %d %.2f %.6f %.6f %.6f %.6f"):format(stripIdx, sz.X,
			cf.from.X, cf.from.Z, cf.to.X, cf.to.Z))
	end
end

-- the chain must breathe: tick 50 frames, report chain-strip transparencies
local function chainTransparencies()
	local out = {}
	for _, p in ipairs(E.kidsOf(E.workspace)) do
		local cf = p.CFrame
		local sz = p.Size
		if cf ~= nil and type(cf) == "table" and cf._kind == "lookAt" and sz.X == 1.4 then
			table.insert(out, p.Transparency or -1)
		end
	end
	return out
end
local tBefore = chainTransparencies()
for _ = 1, 50 do
	CathedralPlate.tick(1 / 30)
end
local tAfter = chainTransparencies()
print(("chaintrans before %s"):format(table.concat(tBefore, " ")))
print(("chaintrans after %s"):format(table.concat(tAfter, " ")))

-- beacon Touched -> ShadowLedger row carrying the walker's live readout.
-- Walker stands exactly ON water_computer's world anchor, touches its beacon
-- (the on-beacon zero case), then also touches audit_dungeon's beacon from
-- that same spot (the nonzero distance/bearing case).
local wcWorld = CathedralMap.toWorld("water_computer")
local hrp = { Position = { X = wcWorld.X, Y = wcWorld.Y, Z = wcWorld.Z } }
local fakeCharacter = {
	FindFirstChild = function(_, n)
		if n == "HumanoidRootPart" then
			return hrp
		end
		return nil
	end,
}
E.state.fakeCharacter = fakeCharacter
E.playerStub.Character = fakeCharacter
local function touchBeacon(region)
	for _, p in ipairs(E.kidsOf(E.workspace)) do
		if p.Name == "CathedralBeacon_" .. region then
			p.Touched:Fire({ Parent = fakeCharacter })
			return true
		end
	end
	return false
end
touchBeacon("water_computer")
touchBeacon("audit_dungeon")
print(("ledger_rows %d"):format(#LedgerStub.rows))
for i, row in ipairs(LedgerStub.rows) do
	print(("ledger %d where=%s player=%d %s"):format(i, tostring(row.where), row.player.UserId, row.line))
end

-- the REAL client HUD: its whole top level executes at require time
require("./CathedralMapHud")

local function descendants(inst)
	local out = {}
	local function walk(node)
		for _, c in ipairs(E.kidsOf(node)) do
			table.insert(out, c)
			walk(c)
		end
	end
	walk(inst)
	return out
end

-- the static minimap: labels carry their pixel positions (drawn at require)
for _, gui in ipairs(E.kidsOf(E.playerGui)) do
	for _, child in ipairs(descendants(gui)) do
		if child.ClassName == "Frame" and child.ClipsDescendants == true then
			for _, sub in ipairs(descendants(child)) do
				if sub.ClassName == "TextLabel" and sub.Text then
					local pos = sub.Position
					if pos and pos._udim2 then
						print(("maplabel %s %.10f %.10f %.10f %.10f"):format(sub.Text,
							pos.X.Scale, pos.X.Offset, pos.Y.Scale, pos.Y.Offset))
					end
				end
			end
			local frames = 0
			for _, sub in ipairs(descendants(child)) do
				if sub.ClassName == "Frame" then
					frames += 1
				end
			end
			print(("mapframe_frames %d"):format(frames))
		end
	end
end

-- fire the HUD heartbeat with the walker standing on water_computer
E.runService.Heartbeat:Fire()
for _, gui in ipairs(E.kidsOf(E.playerGui)) do
	for _, child in ipairs(descendants(gui)) do
		if child.ClassName == "TextLabel" then
			local txt = child.Text or ""
			if string.sub(txt, 1, 10) == "POS eigen " then
				for line in string.gmatch(txt .. "\n", "(.-)\n") do
					print(("readout %s"):format(line))
				end
			end
		end
	end
end

print("smoke_done")
