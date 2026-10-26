-- == B2-30 scenario driver (composed after the stubs and real module bytes) ==

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
check("S0 store name ShadowLedger_v1", simStore._order():find("ShadowLedger_v1", 1, true) ~= nil, simStore._order())
check("S0 blank disposition line", SL.disposition(mkPlayer(1, "x")) == "THE LEDGER IS BLANK. THAT IS ITS OWN VERDICT.")

print("== S1 key format p<uid>_day<UTC yyyymmdd> ==")
SL.record(mkPlayer(8675309, "solo"), "Basecamp", "keyfmt probe")
step_all()
local k1 = keyOf(8675309)
local r1 = rowsOf(k1)
check("S1 utc day is 20260926", utcday() == "20260926", utcday())
check("S1 key shape", k1 == "p8675309_day20260926", k1)
check("S1 one row at key", #r1 == 1, tostring(#r1))
local e1 = r1[1] or {}
check("S1 entry fields", e1.player == "8675309" and e1.kspace == "Basecamp" and e1.choice == "keyfmt probe" and e1.noticing == false and e1.virtueMarks == 0, tostring(e1.player) .. "," .. tostring(e1.kspace) .. "," .. tostring(e1.choice))
check("S1 ts sane", type(e1.ts) == "number" and os.time() >= e1.ts and os.time() - e1.ts < 5, tostring(e1.ts))

print("== S2 old path (real 5e291421a bytes) same-key worst-case interleave ==")
simStore._reset()
SOLD.record(mkPlayer(4242, "a"), "Basecamp", portalText("SWARM"))
SOLD.record(mkPlayer(4242, "a"), "Basecamp", portalText("SKI"))
step_all()
local r2 = rowsOf(keyOf(4242))
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
__ON_PLAYER_REMOVING(mkPlayer(1001, "c1"))
__ON_PLAYER_REMOVING(mkPlayer(1002, "c2"))
local ra = rowsOf(keyOf(1001))
local rb = rowsOf(keyOf(1002))
check("S4 client 1 row persists", #ra == 1 and ra[1] and ra[1].choice == portalText("SWARM"), tostring(#ra))
check("S4 client 2 row persists", #rb == 1 and rb[1] and rb[1].choice == portalText("SKI"), tostring(#rb))
print("     discriminator probe: same scenario on the OLD module")
simStore._reset()
SOLD.record(mkPlayer(1001, "c1"), "Basecamp", portalText("SWARM"))
SOLD.record(mkPlayer(1002, "c2"), "Basecamp", portalText("SKI"))
step_all()
local raOld = rowsOf(keyOf(1001))
local rbOld = rowsOf(keyOf(1002))
check("S4 old path also passes two-uid crossing (different keys, no race)", #raOld == 1 and #rbOld == 1, tostring(#raOld) .. "/" .. tostring(#rbOld))
print("     => P3 two-client crossing does NOT discriminate t74 fix vs bug")

print("== S4b mixed fleet: unfixed server's late set clobbers the fixed row ==")
simStore._reset()
SOLD.record(mkPlayer(4242, "a"), "Basecamp", portalText("SKI")) -- old server gets first
SL.record(mkPlayer(4242, "a"), "Basecamp", portalText("SWARM")) -- fixed server commits
step_all()
local r4b = rowsOf(keyOf(4242))
check("S4b mixed servers same key: old late set loses the fixed row", #r4b == 1 and r4b[1].choice == portalText("SKI"), tostring(#r4b) .. " rows")
print("     (residual risk while any server runs pre-t74 code; both-fixed is S3)")

print("== S5 retry law: transform called twice, no double-append ==")
simStore._reset()
SL.record(mkPlayer(5555, "r"), "Basecamp", "retry probe")
step_all()
local base1 = rowsOf(keyOf(5555))
check("S5 baseline single append", #base1 == 1, tostring(#base1))
SL.record(mkPlayer(5555, "r"), "Basecamp", "retry probe 2")
-- docs: re-call happens with the key's CURRENT value (baseline rows plus the
-- other server's intervening row), previous result discarded
local cur = rowsOf(keyOf(5555))
cur[#cur + 1] = { player = "5555", choice = "other-server row", noticing = false, virtueMarks = 0, ts = os.time() }
simStore._armRetry("fresh", cur)
step_all()
local r5 = rowsOf(keyOf(5555))
check("S5 retry keeps exactly one append per record", countChoice(r5, "retry probe 2") == 1 and #r5 == 3, "rows=" .. tostring(#r5) .. " probe2=" .. tostring(countChoice(r5, "retry probe 2")))
simStore._armRetry("shared", nil)
SL.record(mkPlayer(5555, "r"), "Basecamp", "retry probe 3")
step_all()
local r5b = rowsOf(keyOf(5555))
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
