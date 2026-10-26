-- judge driver for candidate ONE (eigenmap-one): executes the REAL module
-- roblox/src/shared/EigenMap.luau under the plain luau CLI. Machine-readable
-- rows consumed by checks/eigenmap_judge.py. No mocks, no rewrites.

local EigenMap = require("../../../roblox/src/shared/EigenMap")

print("scanstamp " .. (select(1, EigenMap.scanStamp())) .. " " .. (select(2, EigenMap.scanStamp())))
print("studsperunit " .. tostring(EigenMap.STUDS_PER_UNIT))
print("plaza " .. tostring(EigenMap.PLAZA_X) .. " " .. tostring(EigenMap.PLAZA_Z))

local regs = EigenMap.regions()
for _, r in ipairs(regs) do
	print(("region %s %.10f %.10f %s %s %d"):format(r.name, r.ex, r.ey, r.class, tostring(r.cos), r.hops))
end

for i = 1, #regs do
	for j = 1, #regs do
		if i < j then
			local a, b = regs[i].name, regs[j].name
			print(("pair %s %s %.12f %.8f"):format(a, b, EigenMap.distEigen(a, b), EigenMap.bearingEigen(a, b)))
		end
	end
end

-- walker probes: standing exactly on each beacon, readout to every region
for _, a in ipairs(regs) do
	for _, b in ipairs(regs) do
		print(("probe %s %s %.12f %.8f"):format(a.name, b.name,
			EigenMap.distFromEigen(b.name, a.ex, a.ey), EigenMap.bearingFromEigen(b.name, a.ex, a.ey)))
	end
	local n, d = EigenMap.nearestEigen(a.ex, a.ey)
	print(("nearest %s %s %.12f"):format(a.name, n, d))
end

-- world transform (pure numeric half)
for _, r in ipairs(regs) do
	local wx, wz = EigenMap.worldFromEigen(r.ex, r.ey)
	local bx, bz = EigenMap.eigenFromWorld(wx, wz)
	print(("world %s %.6f %.6f %.12f %.12f"):format(r.name, wx, wz, bx, bz))
end

for _, s in ipairs(EigenMap.chain()) do
	print(("chain %s %s %s"):format(s.a, s.b, s.kind))
end
for _, m in ipairs(EigenMap.offMap()) do
	print("offmap " .. m)
end
local w, t = EigenMap.beta0()
print("beta0 " .. tostring(w) .. " " .. tostring(t))
