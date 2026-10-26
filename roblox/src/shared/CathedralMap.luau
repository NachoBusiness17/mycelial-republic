--!strict
-- CathedralMap  -  candidate TWO of the eigen-map card (ractor panel 2026-09-26,
-- cands/eigenmap-two.md). THE CATHEDRAL as a walkable world map: region
-- positions are the eigen_centroids of the curvature scan, BYTE-COPIED from
-- watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json (ts below), and ONE
-- convention is held everywhere  -  data, minimap, and the world plate agree:
--
--   bearing 0 deg = north = eigen -y, clockwise: atan2(dx, -dy)
--     (same FORMULA as tools/cathedral_eigen_map.py:46, so every number here
--     matches a recompute from the scan JSON)
--   on the minimap, -y is up (north arrow at top)
--   in the world, north = -Z and worldZ = ORIGIN.Z + ey * SCALE, so walking
--     world -Z walks map-up, and the compass you read is the compass you walk
--
-- Fold note (judge ruling 2026-09-27): the sibling build eigenmap-one
-- (roblox/src/shared/EigenMap.luau) used the same bearing formula but
-- flipped its minimap Y (EigenMapHud.client.luau toScale: (py1-ey)/span
-- renders +ey up), so its drawn map and its bearing text disagreed by
-- 180 deg; the judge killed it on the mirrored minimap and this module is
-- the estate's one cathedral map. The killed build's bytes are preserved in
-- watch/inbox/ractor_panel_20260926/cands/killed/.
--
-- The pure-number API (everything above the Roblox adapters line) touches no
-- Roblox globals, so tools/bin/luau/luau.exe can execute it headless;
-- tools/eigenmap_two_check.py diffs this module's output against a Python
-- recompute from the scan JSON, and tools/eigenmap_two_smoke.py executes the
-- plate + HUD scripts themselves under Roblox-API stubs.

local CathedralMap = {}

-- ---- DATA (byte-faithful from the scan; do not hand-edit) ----
-- source: watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json
-- scan ts: 2026-09-27T01:07:39.278044+00:00
-- adventure_2d6 has NO eigen centroid in any scan (its module_id is
-- adventure_2d6_stub, so curvature_scan's mods.get("adventure_2d6") misses):
-- OFF-MAP BY CONSTRUCTION, recorded, never silently dropped.

CathedralMap.SCAN_SOURCE = "watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json"
CathedralMap.SCAN_TS = "2026-09-27T01:07:39.278044+00:00"
CathedralMap.SPECTRUM_HEAD = { 0.362, 0.317, 0.293, 0.284 }

-- scan JSON eigen_centroids block, verbatim values
local CENTROIDS: { [string]: { number } } = {
	["water_computer"] = { -0.0236, -0.0124 },
	["fractal_maze"] = { -0.0294, -0.0043 },
	["riddler_optics"] = { -0.0162, -0.0080 },
	["riddler_engram"] = { -0.0137, -0.0071 },
	["audit_dungeon"] = { -0.0180, -0.0090 },
}

-- scan JSON regions block (class + cos). riddler_engram cos is null in the
-- scan (DARK): no number invented here.
local CLASS: { [string]: string } = {
	["water_computer"] = "SADDLE",
	["fractal_maze"] = "SADDLE",
	["riddler_optics"] = "SADDLE",
	["riddler_engram"] = "DARK",
	["audit_dungeon"] = "SADDLE",
}
local COS: { [string]: number } = {
	["water_computer"] = 0.358,
	["fractal_maze"] = 0.129,
	["riddler_optics"] = 0.134,
	["audit_dungeon"] = 0.124,
}

-- scan JSON descent_vote (a VOTE, not a verdict): water_first is the
-- OPERATIVE LEAN, the RIB descent-order invariant stays CONTESTED
-- (watch/inbox/REFEREE_VERDICT_20260926.md). chain()/starLen() below must
-- reproduce these two numbers at the scan's 3dp rounding.
CathedralMap.VOTE = { chain_len = 0.031, star_len = 0.036, shorter = "water-first" }

CathedralMap.OFF_MAP = { "adventure_2d6 (module_id adventure_2d6_stub: no eigen centroid in any scan)" }

-- descent order over the MAPPED regions (the operative lean). Edge policy is
-- derived, not stored: see chainEdges()  -  no edge may anchor on the DARK
-- region (referee missing-edge ruling, REFEREE_VERDICT_20260926.md: never
-- canonize a builder's private geometry via the DARK anchor; this build draws
-- NO engram leg at all, not even as debt dashed lines).
CathedralMap.WATER_FIRST = { "water_computer", "fractal_maze", "riddler_optics", "riddler_engram", "audit_dungeon" }

-- ---- world anchor (the one affine map; eigen plane horizontal) ----
CathedralMap.SCALE = 12000 -- studs per eigen unit; centroid cloud spans
-- ~0.0157 x 0.0081 eigen = ~188 x 97 studs. Ground: far SOUTH, clear of every
-- existing zone (checked 2026-09-26: the nearest content south is FRONTIER
-- SOULS' flats at X -400..0, Z -400..0; STEER FIELD at (-400,-110); nothing
-- between Z 300 and Z 600 on X -360..-160).
-- ORIGIN is kept as three NUMBERS (not a Vector3) so this file's top level
-- stays free of Roblox globals and the plain luau CLI can require it; the
-- Vector3 adapter is origin() below.
CathedralMap.ORIGIN_X = 0
CathedralMap.ORIGIN_Y = 8
CathedralMap.ORIGIN_Z = 560 -- eigen (0, 0) lands here
CathedralMap.PLATE_MARGIN = 16 -- studs of floor past each extreme beacon

-- ---- pure math (Luau CLI runnable; no Roblox globals above the adapters) ----

function CathedralMap.regions(): { string }
	local out: { string } = {}
	for r in pairs(CENTROIDS) do
		table.insert(out, r)
	end
	table.sort(out)
	return out
end

function CathedralMap.centroid(region: string): { number }?
	return CENTROIDS[region]
end

function CathedralMap.class(region: string): string
	return CLASS[region] or "?"
end

function CathedralMap.cos(region: string): number?
	return COS[region]
end

local function r4(x: number): number
	return math.round(x * 10000) / 10000
end
local function r1(x: number): number
	return math.round(x * 10) / 10
end

-- Euclidean distance in eigen units, 4dp  -  the scan's own metric.
function CathedralMap.dist(a: string, b: string): number
	local pa, pb = CENTROIDS[a], CENTROIDS[b]
	if not pa or not pb then
		return -1 -- unknown region: a negative is a fact, not a throw
	end
	return r4(math.sqrt((pb[1] - pa[1]) ^ 2 + (pb[2] - pa[2]) ^ 2))
end

-- Bearing a->b, degrees, 0 = north = eigen -y, clockwise (atan2(dx, -dy)):
-- numerically the HTML map's law (tools/cathedral_eigen_map.py:45-47).
-- math.atan2 is the four-quadrant form (Luau/Roblox); math.atan is NOT  - 
-- its second argument is ignored (verified: tools/bin/luau/luau.exe prints
-- atan(1,2)=45 deg, atan(-1,-2)=-45 deg), which silently collapses every
-- bearing toward 0/360. eigenmap-two-check.txt caught exactly that.
function CathedralMap.bearing(a: string, b: string): number
	local pa, pb = CENTROIDS[a], CENTROIDS[b]
	if not pa or not pb then
		return -1
	end
	local deg = math.deg(math.atan2(pb[1] - pa[1], -(pb[2] - pa[2])))
	return r1((deg + 360) % 360)
end

-- Walker readouts from a live eigen position (x, y) toward a region.
-- Position sanity anchor: worldToEigen(toWorld(r)) == centroid of r exactly,
-- so standing ON a beacon makes distFrom(r) read 0.0000.
function CathedralMap.distFrom(x: number, y: number, region: string): number
	local p = CENTROIDS[region]
	if not p then
		return -1
	end
	return r4(math.sqrt((p[1] - x) ^ 2 + (p[2] - y) ^ 2))
end

function CathedralMap.bearingFrom(x: number, y: number, region: string): number
	local p = CENTROIDS[region]
	if not p then
		return -1
	end
	local deg = math.deg(math.atan2(p[1] - x, -(p[2] - y)))
	return r1((deg + 360) % 360)
end

local WINDS = { "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
	"S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW" }
function CathedralMap.compass(deg: number): string
	return WINDS[(math.floor(deg / 22.5 + 0.5) % 16) + 1]
end

export type Near = { region: string, dist: number, bearing: number }
-- Ties break ALPHABETICALLY (eigenmap-two-check probe: the water/audit
-- midpoint is an exact 0.0033 tie; pairs() hash order must never pick the
-- nearest region). Iterates the sorted region list, strict <, name on equal.
function CathedralMap.nearest(x: number, y: number): Near
	local best: Near = { region = "?", dist = -1, bearing = -1 }
	for _, r in ipairs(CathedralMap.regions()) do
		local d = CathedralMap.distFrom(x, y, r)
		if best.dist < 0 or d < best.dist then
			best = { region = r, dist = d, bearing = CathedralMap.bearingFrom(x, y, r) }
		end
	end
	return best
end

-- The frozen pairwise receipt: 10 unordered pairs, both bearings, dist 4dp /
-- bearing 1dp. This is the exact number set eigenmap-two-check.py recomputes
-- from the scan JSON  -  the judge's position/distance/bearing sanity check and
-- this table are the same arithmetic.
export type Pair = { a: string, b: string, dist: number, bearing: number, bearingBack: number }
function CathedralMap.pairwise(): { Pair }
	local regs = CathedralMap.regions()
	local out: { Pair } = {}
	for i = 1, #regs do
		for j = i + 1, #regs do
			local a, b = regs[i], regs[j]
			table.insert(out, {
				a = a,
				b = b,
				dist = CathedralMap.dist(a, b),
				bearing = CathedralMap.bearing(a, b),
				bearingBack = CathedralMap.bearing(b, a),
			})
		end
	end
	return out
end

-- Vote arithmetic in-module (4dp): reproduces the scan's filed
-- water_first_chain_len / hub_first_star_len at 3dp (0.031 / 0.036).
function CathedralMap.chainLen(): number
	local total = 0.0
	for i = 1, #CathedralMap.WATER_FIRST - 1 do
		local pa = CENTROIDS[CathedralMap.WATER_FIRST[i]]
		local pb = CENTROIDS[CathedralMap.WATER_FIRST[i + 1]]
		if pa and pb then
			total += math.sqrt((pb[1] - pa[1]) ^ 2 + (pb[2] - pa[2]) ^ 2)
		end
	end
	return r4(total)
end

function CathedralMap.starLen(): number
	local total = 0.0
	local home = CENTROIDS["water_computer"]
	for _, p in pairs(CENTROIDS) do
		total += math.sqrt((p[1] - home[1]) ^ 2 + (p[2] - home[2]) ^ 2)
	end
	return r4(total)
end

-- Edge policy, DERIVED (server plate and client HUD both consume these  - 
-- single authorship): chain legs of the water_first order where BOTH ends are
-- SADDLE. Legs touching riddler_engram (DARK) are refused outright per the
-- referee ruling; the DARK anchor stands isolated on the map by design.
export type Edge = { a: string, b: string }
function CathedralMap.chainEdges(): { Edge }
	local out: { Edge } = {}
	for i = 1, #CathedralMap.WATER_FIRST - 1 do
		local a, b = CathedralMap.WATER_FIRST[i], CathedralMap.WATER_FIRST[i + 1]
		if CLASS[a] == "SADDLE" and CLASS[b] == "SADDLE" then
			table.insert(out, { a = a, b = b })
		end
	end
	return out
end

function CathedralMap.hubEdges(): { Edge }
	local chain = CathedralMap.chainEdges()
	local function inChain(a: string, b: string): boolean
		for _, e in ipairs(chain) do
			if (e.a == a and e.b == b) or (e.a == b and e.b == a) then
				return true
			end
		end
		return false
	end
	local out: { Edge } = {}
	for r in pairs(CENTROIDS) do
		if r ~= "water_computer" and CLASS[r] == "SADDLE" and not inChain("water_computer", r) then
			table.insert(out, { a = "water_computer", b = r })
		end
	end
	table.sort(out, function(x, y)
		return x.b < y.b
	end)
	return out
end

-- eigen bbox (+ margin in eigen units)  -  the minimap fitting math.
function CathedralMap.mapBounds(marginEigen: number): (number, number, number, number)
	local minX, maxX, minY, maxY = math.huge, -math.huge, math.huge, -math.huge
	for _, p in pairs(CENTROIDS) do
		minX = math.min(minX, p[1])
		maxX = math.max(maxX, p[1])
		minY = math.min(minY, p[2])
		maxY = math.max(maxY, p[2])
	end
	return minX - marginEigen, maxX + marginEigen, minY - marginEigen, maxY + marginEigen
end

-- ---- Roblox adapters (Vector3 only below this line) ----

-- eigen (0, 0) as a world position (adapter for the numeric ORIGIN_* above)
function CathedralMap.origin(): Vector3
	return Vector3.new(CathedralMap.ORIGIN_X, CathedralMap.ORIGIN_Y, CathedralMap.ORIGIN_Z)
end

-- World placement. NORTH = -Z = eigen -y (the bearing law's north), so:
-- worldX = ORIGIN.X + ex * SCALE ; worldZ = ORIGIN.Z + ey * SCALE.
-- Walking world -Z walks map-up; the plate, the minimap and every bearing
-- text share one compass.
function CathedralMap.toWorld(region: string): Vector3
	local c = CENTROIDS[region]
	if not c then
		return CathedralMap.origin()
	end
	return Vector3.new(
		CathedralMap.ORIGIN_X + c[1] * CathedralMap.SCALE,
		CathedralMap.ORIGIN_Y,
		CathedralMap.ORIGIN_Z + c[2] * CathedralMap.SCALE
	)
end

-- Inverse of toWorld; round-trips a beacon to its own centroid.
function CathedralMap.worldToEigen(p: Vector3): (number, number)
	return (p.X - CathedralMap.ORIGIN_X) / CathedralMap.SCALE,
		(p.Z - CathedralMap.ORIGIN_Z) / CathedralMap.SCALE
end

function CathedralMap.plateCenter(): Vector3
	local minX, maxX, minY, maxY = CathedralMap.mapBounds(0)
	return Vector3.new(
		CathedralMap.ORIGIN_X + (minX + maxX) / 2 * CathedralMap.SCALE,
		CathedralMap.ORIGIN_Y,
		CathedralMap.ORIGIN_Z + (minY + maxY) / 2 * CathedralMap.SCALE
	)
end

function CathedralMap.plateSize(): Vector3
	local minX, maxX, minY, maxY = CathedralMap.mapBounds(0)
	return Vector3.new(
		(maxX - minX) * CathedralMap.SCALE + 2 * CathedralMap.PLATE_MARGIN,
		1,
		(maxY - minY) * CathedralMap.SCALE + 2 * CathedralMap.PLATE_MARGIN
	)
end

-- class palette = the HTML map's law (tools/cathedral_eigen_map.py:29):
-- SADDLE amber, DARK violet, HILL green
function CathedralMap.classColor(cls: string): Color3
	if cls == "SADDLE" then
		return Color3.fromRGB(217, 164, 65)
	elseif cls == "DARK" then
		return Color3.fromRGB(91, 75, 138)
	elseif cls == "HILL" then
		return Color3.fromRGB(76, 154, 106)
	end
	return Color3.fromRGB(136, 136, 136)
end

return CathedralMap
