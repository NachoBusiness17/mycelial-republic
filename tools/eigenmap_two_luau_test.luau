-- eigenmap_two_luau_test  -  executes the REAL shared module (no mocks) under
-- the plain luau CLI (tools/bin/luau/luau.exe) so the overlay's math is
-- checked as shipped, not as re-typed. Prints machine-readable rows that
-- tools/eigenmap_two_check.py diffs against a Python recompute from
-- watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260927.json.
-- Only the pure-number API runs here (the module's Roblox adapters are
-- guarded by design; its top level touches no Roblox globals).
-- (Relocated 2026-09-27 from cands/eigenmap-two-luau-test.luau; require path
-- updated for the tools/ location. The plate + HUD scripts themselves are
-- executed by tools/eigenmap_two_smoke.luau.)

local CathedralMap = require("../roblox/src/shared/CathedralMap")

print("scan_ts " .. CathedralMap.SCAN_TS)
print("scan_source " .. CathedralMap.SCAN_SOURCE)
print("scale " .. tostring(CathedralMap.SCALE))
print("origin " .. CathedralMap.ORIGIN_X .. " " .. CathedralMap.ORIGIN_Y .. " " .. CathedralMap.ORIGIN_Z)

for _, r in ipairs(CathedralMap.regions()) do
	local c = CathedralMap.centroid(r) or { 0, 0 }
	print(("region %s %.4f %.4f %s %s"):format(r, c[1], c[2], CathedralMap.class(r),
		tostring(CathedralMap.cos(r))))
end

for _, p in ipairs(CathedralMap.pairwise()) do
	print(("pair %s %s %.4f %.1f %.1f"):format(p.a, p.b, p.dist, p.bearing, p.bearingBack))
end

print(("vote %.4f %.4f %s"):format(CathedralMap.chainLen(), CathedralMap.starLen(), CathedralMap.VOTE.shorter))

for _, e in ipairs(CathedralMap.chainEdges()) do
	print(("chaingedge %s %s"):format(e.a, e.b))
end
for _, e in ipairs(CathedralMap.hubEdges()) do
	print(("hubedge %s %s"):format(e.a, e.b))
end

-- walker probes: standing exactly on a beacon must read dist 0 and the
-- position equals the centroid; a synthetic offset must read the same
-- distance/bearing Python computes for the same point.
for _, r in ipairs(CathedralMap.regions()) do
	local c = CathedralMap.centroid(r) or { 0, 0 }
	local n = CathedralMap.nearest(c[1], c[2])
	print(("probe_on_beacon %s %.4f %.1f %s"):format(r, n.dist, n.bearing, n.region))
end
-- probe midpoint between water_computer and audit_dungeon (Python recomputes
-- the same point: average of the two centroids in the 0927 JSON)
local w = CathedralMap.centroid("water_computer") or { 0, 0 }
local a = CathedralMap.centroid("audit_dungeon") or { 0, 0 }
local mx, my = (w[1] + a[1]) / 2, (w[2] + a[2]) / 2
print(("probe_mid %.4f %.4f %s %.4f %.1f"):format(mx, my,
	CathedralMap.nearest(mx, my).region, CathedralMap.nearest(mx, my).dist,
	CathedralMap.nearest(mx, my).bearing))
print(("probe_mid_to_fractal %.4f %.1f"):format(
	CathedralMap.distFrom(mx, my, "fractal_maze"),
	CathedralMap.bearingFrom(mx, my, "fractal_maze")))
