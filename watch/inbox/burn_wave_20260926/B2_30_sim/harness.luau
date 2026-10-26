-- B2-30 ShadowLedger concurrent-writer SIMULATION (not a live DataStore proof).
-- Runtime: tools/bin/luau/luau.exe. The Luau logic under test is the real repo
-- file (ut_ShadowLedger.luau, one documented line delta) and the real pre-t74
-- file from git 5e291421a (ut_ShadowLedger_old.luau, same sole delta).
-- The DataStore backend is an in-memory stub implementing the documented
-- UpdateAsync/SetAsync contract (sentences quoted in the receipt, fetched from
-- the archived official GlobalDataStore page, snapshot 20260311133112).
-- Concurrency model: task.spawn semantics (run until first yield), yields at
-- DataStore network boundaries only; UpdateAsync read-transform-write contains
-- no yield, which is exactly the serialization the docs sentence claims.

local failures = 0
local function check(name, cond, detail)
	if cond then
		print("PASS  " .. name)
	else
		failures += 1
		print("FAIL  " .. name .. (detail and ("  :: " .. detail) or ""))
	end
end

-- deterministic LCG (Luau CLI has no math.randomseed)
local rngState = 42
local function srand(s) rngState = s % 2147483648 end
local function rnd(n)
	rngState = (1103515245 * rngState + 12345) % 2147483648
	return rngState % n
end

-- scheduler: coroutines yielded at store boundaries
local ready = {}
local order = {}
local function log(s) order[#order + 1] = s end

local function step_all()
	while #ready > 0 do
		local c = table.remove(ready, 1)
		local ok, e = coroutine.resume(c)
		if not ok then error("writer fault: " .. tostring(e)) end
	end
end

local function step_all_shuffled()
	while #ready > 0 do
		local c = table.remove(ready, rnd(#ready) + 1)
		local ok, e = coroutine.resume(c)
		if not ok then error("writer fault: " .. tostring(e)) end
	end
end

task = {}
task.spawn = function(f)
	local c = coroutine.create(f)
	local ok, e = coroutine.resume(c)
	if not ok then error("spawn fault: " .. tostring(e)) end
	if coroutine.status(c) == "suspended" then ready[#ready + 1] = c end
	return c
end

-- in-memory store stub; values deep-copied across the network boundary
local data = {}
local retryMode = nil -- nil | "fresh" | "shared"
local retrySeed = nil

local function deepcopy(v)
	if type(v) ~= "table" then return v end
	local r = {}
	for k, x in pairs(v) do r[k] = deepcopy(x) end
	return r
end

local simStore
simStore = {
	GetAsync = function(_, key)
		coroutine.yield("get")
		log("get " .. key)
		local v = data[key]
		return v and deepcopy(v) or nil
	end,
	SetAsync = function(_, key, value)
		coroutine.yield("set")
		log("set " .. key)
		data[key] = deepcopy(value)
	end,
	UpdateAsync = function(_, key, transform)
		coroutine.yield("ua")
		log("ua " .. key)
		local old = data[key]
		local buf = old and deepcopy(old) or nil
		local rows
		if retryMode == "fresh" then
			transform(buf) -- first result discarded per the docs sentence
			rows = transform(retrySeed and deepcopy(retrySeed) or (buf and deepcopy(buf) or nil))
		elseif retryMode == "shared" then
			rows = transform(buf) -- same buffer handed to the transform twice
			rows = transform(buf)
		else
			rows = transform(buf)
		end
		if rows == nil then
			log("ua-cancel " .. key)
			return nil
		end
		data[key] = deepcopy(rows)
		return rows
	end,
	_reset = function() data = {} retryMode = nil retrySeed = nil ready = {} order = {} end,
	_peek = function(key) return data[key] and deepcopy(data[key]) or nil end,
	_seed = function(key, v) data[key] = deepcopy(v) end,
	_armRetry = function(mode, seed) retryMode = mode; retrySeed = seed end,
	_order = function() return table.concat(order, " | ") end,
}

Players = {
	PlayerRemoving = {
		Connect = function(_, fn)
			_G._onPlayerRemoving = fn
			return { Disconnect = function() end }
		end,
	},
}

local DataStoreService = {
	GetDataStore = function(_, name)
		log("GetDataStore " .. name)
		return simStore
	end,
}

game = {
	GetService = function(_, name)
		if name == "DataStoreService" then return DataStoreService end
		if name == "Players" then return Players end
		if name == "ReplicatedStorage" then
			return { WaitForChild = function() return { WaitForChild = function() return {} end } end }
		end
		error("unexpected service " .. name)
	end,
}

_G.KSPACE_UNDER_TEST = require("./ut_KSpace")
local SL = require("./ut_ShadowLedger")
local SOLD = require("./ut_ShadowLedger_old")

local function mkPlayer(uid, name) return { UserId = uid, Name = name } end
local function utcday() return os.date("!%Y%m%d") end
local function keyOf(uid) return ("p%d_day%s"):format(uid, utcday()) end
local function rowsOf(key) return simStore._peek(key) or {} end
local function countChoice(rows, text)
	local n = 0
	for _, e in ipairs(rows) do if e.choice == text then n += 1 end end
	return n
end
local function portalText(to) return ("took the portal to %s"):format(to) end

print("== S0 sanity ==")
check("S0 store name ShadowLedger_v1", simStore._order():find("ShadowLedger_v1", 1, true) ~= nil)
check("S0 blank disposition line", SL.disposition(mkPlayer(1, "x")) == "THE LEDGER IS BLANK. THAT IS ITS OWN VERDICT.")

print("== S1 key format p<uid>_day<UTC yyyymmdd> ==")
SL.record(mkPlayer(8675309, "solo"), "Basecamp", "keyfmt probe")
step_all()
local k1 = keyOf(8675309)
local r1 = rowsOf(k1)
check("S1 utc day is 20260926", utcday() == "20260926", utcday())
check("S1 key shape", k1 == ("p8675309_day20260926"), k1)
check("S1 one row at key", #r1 == 1, tostring(#r1))
local e1 = r1[1] or {}
check("S1 entry fields", e1.player == "8675309" and e1.kspace == "Basecamp" and e1.choice == "keyfmt probe" and e1.noticing == false and e1.virtueMarks == 0, tostring(e1.player) .. "," .. tostring(e1.kspace) .. "," .. tostring(e1.choice))
check("S1 ts sane", type(e1.ts) == "number" and os.time() >= e1.ts and os.time() - e1.ts < 5, tostring(e1.ts))

print("== S2 old path (real 5e291421a bytes) same-key worst-case interleave ==")
simStore._reset()
SOLD.record(mkPlayer(4242, "a"), "Basecamp", portalText("SWARM"))
SOLD.record(mkPlayer(4242, "a"), "Basecamp", portalText("SKI"))
step_all()
local k2 = keyOf(4242)
local r2 = rowsOf(k2)
print("     op order: " .. simStore._order())
check("S2 lost update reproduced (1 row, one portal line gone)", #r2 == 1 and (countChoice(r2, portalText("SWARM")) + countChoice(r2, portalText("SKI"))) == 1, tostring(#r2))

print("== S2b old path, serialized single writer (no race baseline) ==")
simStore._reset()
SOLD.record(mkPlayer(4243, "a"), "Basecamp", portalText("SWARM"))
step_all()
SOLD.record(mkPlayer(4243, "a"), "Basecamp", portalText("SKI"))
step_all()
check("S2b both rows persist without interleave", #rowsOf(keyOf(4243)) == 2, tostring(#rowsOf(keyOf(4243))))

print("== S3 new path (real HEAD bytes) same-key worst-case interleave ==")
simStore._reset()
SL.record(mkPlayer(4242, "a"), "Basecamp", portalText("SWARM"))
SL.record(mkPlayer(4242, "a"), "Basecamp", portalText("SKI"))
step_all()
local r3 = rowsOf(keyOf(4242))
print("     op order: " .. simStore._order())
check("S3 no lost update (2 rows)", #r3 == 2, tostring(#r3))
check("S3 both portal rows present", countChoice(r3, portalText("SWARM")) == 1 and countChoice(r3, portalText("SKI")) == 1, "swarm=" .. tostring(countChoice(r3, portalText("SWARM"))) .. " ski=" .. tostring(countChoice(r3, portalText("SKI"))))

print("== S4 P3 shape: two clients cross, stop (onLeaving), rows persist ==")
simStore._reset()
SL.record(mkPlayer(1001, "c1"), "Basecamp", portalText("SWARM"))
SL.record(mkPlayer(1002, "c2"), "Basecamp", portalText("SKI"))
step_all()
_G._onPlayerRemoving(mkPlayer(1001, "c1"))
_G._onPlayerRemoving(mkPlayer(1002, "c2"))
local ra = rowsOf(keyOf(1001))
local rb = rowsOf(keyOf(1002))
check("S4 client 1 row persists", #ra == 1 and ra[1] and ra[1].choice == portalText("SWARM"), tostring(#ra))
check("S4 client 2 row persists", #rb == 1 and rb[1] and rb[1].choice == portalText("SKI"), tostring(#rb))
print("     discriminator note: rerunning this exact scenario on the OLD module")
simStore._reset()
SOLD.record(mkPlayer(1001, "c1"), "Basecamp", portalText("SWARM"))
SOLD.record(mkPlayer(1002, "c2"), "Basecamp", portalText("SKI"))
step_all()
local raOld = rowsOf(keyOf(1001))
local rbOld = rowsOf(keyOf(1002))
check("S4 old path also passes two-uid crossing (different keys, no race)", #raOld == 1 and #rbOld == 1, tostring(#raOld) .. "/" .. tostring(#rbOld))
print("     => P3 two-client crossing does NOT discriminate t74 fix vs bug;")

print("== S4b the discriminating probe: same uid, same day, two servers ==")
simStore._reset()
SL.record(mkPlayer(4242, "a"), "Basecamp", portalText("SWARM")) -- server A write
SOLD.record(mkPlayer(4242, "a"), "Basecamp", portalText("SKI")) -- server B write, old code
step_all()
local r4b = rowsOf(keyOf(4242))
check("S4b mixed old/new servers same key: new survives, old row lost", #r4b == 1 and r4b[1].choice == portalText("SWARM"), tostring(#r4b) .. " rows")
print("     (models rejoin inside the same UTC day landing on an unfixed server)")

print("== S5 retry law: transform called twice, no double-append ==")
simStore._reset()
SL.record(mkPlayer(5555, "r"), "Basecamp", "retry probe")
step_all()
local k5 = keyOf(5555)
local base1 = rowsOf(k5)
check("S5 baseline single append", #base1 == 1, tostring(#base1))
SL.record(mkPlayer(5555, "r"), "Basecamp", "retry probe 2")
simStore._armRetry("fresh", {{ player = "5555", choice = "other-server row", noticing = false, virtueMarks = 0, ts = os.time() }})
step_all()
local r5 = rowsOf(k5)
check("S5 retry keeps exactly one append per record", countChoice(r5, "retry probe 2") == 1 and #r5 == 3, "rows=" .. tostring(#r5) .. " probe2=" .. tostring(countChoice(r5, "retry probe 2")))
simStore._armRetry("shared", nil)
SL.record(mkPlayer(5555, "r"), "Basecamp", "retry probe 3")
step_all()
local r5b = rowsOf(k5)
check("S5 shared-buffer double call still one append (copy-then-append)", countChoice(r5b, "retry probe 3") == 1, "probe3=" .. tostring(countChoice(r5b, "retry probe 3")))
local mutant = { player = "5555", choice = "mutant probe", noticing = false, virtueMarks = 0, ts = os.time() }
local buf = {{ player = "5555", choice = "seed row", noticing = false, virtueMarks = 0, ts = os.time() }}
local function mutatingTransform(old) -- control: old GetAsync+SetAsync style mutation
	old = old or {}
	old[#old + 1] = mutant
	return old
end
mutatingTransform(buf)
mutatingTransform(buf)
check("S5 control: mutating transform under double call double-appends", countChoice(buf, "mutant probe") == 2, "mutant=" .. tostring(countChoice(buf, "mutant probe")))

print("== S6 schema compatibility: pre-law array passes through ==")
simStore._reset()
local legacy = {
	{ player = "6666", choice = "legacy-a", noticing = true, virtueMarks = 1, ts = 1 },
	{ player = "6666", choice = "legacy-b", noticing = false, virtueMarks = 0, ts = 2 },
}
simStore._seed(keyOf(6666), legacy)
SL.record(mkPlayer(6666, "z"), "Basecamp", "post-law row")
step_all()
local r6 = rowsOf(keyOf(6666))
check("S6 legacy rows intact, one appended", #r6 == 3 and r6[1].choice == "legacy-a" and r6[2].choice == "legacy-b" and r6[3].choice == "post-law row", tostring(#r6))

print("== S7 fuzz: shuffled schedules, 2-4 writers, same key ==")
local oldLost, newLost, trials = 0, 0, 0
for _, writers in ipairs({ 2, 3, 4 }) do
	for seed = 1, 60 do
		trials += 1
		simStore._reset()
		srand(seed * 100 + writers)
		for w = 1, writers do
			SOLD.record(mkPlayer(777, "f"), "Basecamp", ("old-w%d"):format(w))
		end
		step_all_shuffled()
		oldLost += (writers - #rowsOf(keyOf(777)))
		simStore._reset()
		srand(seed * 100 + writers)
		for w = 1, writers do
			SL.record(mkPlayer(777, "f"), "Basecamp", ("new-w%d"):format(w))
		end
		step_all_shuffled()
		newLost += (writers - #rowsOf(keyOf(777)))
	end
end
print(("     old path lost rows: %d over %d trials; new path lost rows: %d"):format(oldLost, trials, newLost))
check("S7 old path demonstrably loses rows under interleave", oldLost > 0, tostring(oldLost))
check("S7 new path loses zero rows in every schedule", newLost == 0, tostring(newLost))

print(("== RESULT: %d failures =="):format(failures))
if failures > 0 then error("HARNESS FAILURES: " .. failures) end
