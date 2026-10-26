-- judge driver for candidate TWO (eigenmap-two): executes the REAL module
-- roblox/src/shared/CathedralMap.luau under the plain luau CLI.
-- Machine-readable rows consumed by checks/eigenmap_judge.py.

local CathedralMap = require("../../../roblox/src/shared/CathedralMap")

print("scan_ts " .. CathedralMap.SCAN_TS)
print("scale " .. tostring(CathedralMap.SCALE))
print("origin " .. tostring(CathedralMap.ORIGIN_X) .. " " .. tostring(CathedralMap.ORIGIN_Y) .. " " .. tostring(CathedralMap.ORIGIN_Z))

local regs = CathedralMap.regions()
for _, r in ipairs(regs) do
	local c = CathedralMap.centroid(r) or { 0, 0 }
	print(("region %s %.10f %.10f %s %s"):format(r, c[1], c[2], CathedralMap.class(r), tostring(CathedralMap.cos(r))))
end

for _, p in ipairs(CathedralMap.pairwise()) do
	print(("pair %s %s %.6f %.4f %.4f"):format(p.a, p.b, p.dist, p.bearing, p.bearingBack))
end

print(("vote %.6f %.6f %s"):format(CathedralMap.chainLen(), CathedralMap.starLen(), CathedralMap.VOTE.shorter))

for _, e in ipairs(CathedralMap.chainEdges()) do
	print(("chainedge %s %s"):format(e.a, e.b))
end
for _, e in ipairs(CathedralMap.hubEdges()) do
	print(("hubedge %s %s"):format(e.a, e.b))
end

-- walker probes: on each beacon and at the water/audit midpoint
for _, r in ipairs(regs) do
	local c = CathedralMap.centroid(r) or { 0, 0 }
	local n = CathedralMap.nearest(c[1], c[2])
	print(("probe_on %s %.6f %.4f %s"):format(r, n.dist, n.bearing, n.region))
end
local w = CathedralMap.centroid("water_computer") or { 0, 0 }
local a = CathedralMap.centroid("audit_dungeon") or { 0, 0 }
local mx, my = (w[1] + a[1]) / 2, (w[2] + a[2]) / 2
local n = CathedralMap.nearest(mx, my)
print(("probe_mid %.10f %.10f %s %.6f %.4f"):format(mx, my, n.region, n.dist, n.bearing))
print(("probe_mid_to_fractal %.6f %.4f"):format(
	CathedralMap.distFrom(mx, my, "fractal_maze"), CathedralMap.bearingFrom(mx, my, "fractal_maze")))
