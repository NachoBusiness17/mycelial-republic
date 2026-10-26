# B2-30 harness builder (run with .venv/Scripts/python.exe).
# Composes combined_sim.luau: stub environment + the REAL ShadowLedger.luau
# bytes (current HEAD and pre-t74 git 5e291421a) + the scenario driver, all in
# one Luau chunk so the plain luau.exe runtime (which isolates per-module
# environments) can share the stub globals with the module under test.
# Sole delta per module copy: line 10's instance-based require becomes a
# __KSPACE_UNDER_TEST global handoff. Everything else is the real bytes.
import hashlib
import pathlib
import subprocess

REPO = pathlib.Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")
OUT = pathlib.Path(__file__).parent
DELTA_OLD = 'local KSpace = require(Shared:WaitForChild("KSpace"))'
DELTA_NEW = 'local KSpace = __KSPACE_UNDER_TEST -- B2-30 harness delta (sole edit; real line 10)'

STUBS = """\
-- B2-30 ShadowLedger concurrent-writer SIMULATION (not a live DataStore proof).
-- Composed by make_under_test.py; do not edit generated output.
-- The DataStore backend is an in-memory stub implementing the documented
-- UpdateAsync/SetAsync contract (sentences quoted in the receipt, archived
-- official GlobalDataStore page, snapshot 20260311133112). Concurrency model:
-- task.spawn semantics (run until first yield); yields only at DataStore
-- network boundaries; UpdateAsync read-transform-write has no yield, which is
-- exactly the serialization the docs sentence claims.

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
		if coroutine.status(c) == "suspended" then ready[#ready + 1] = c end
	end
end

local function step_all_shuffled()
	while #ready > 0 do
		local c = table.remove(ready, rnd(#ready) + 1)
		local ok, e = coroutine.resume(c)
		if not ok then error("writer fault: " .. tostring(e)) end
		if coroutine.status(c) == "suspended" then ready[#ready + 1] = c end
	end
end

-- module-visible stubs must be true globals (single chunk, shared env)
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
	_reset = function()
		data = {}
		retryMode = nil
		retrySeed = nil
		ready = {}
		order = {}
	end,
	_peek = function(key) return data[key] and deepcopy(data[key]) or nil end,
	_seed = function(key, v) data[key] = deepcopy(v) end,
	_armRetry = function(mode, seed) retryMode = mode; retrySeed = seed end,
	_order = function() return table.concat(order, " | ") end,
}
__SIM_STORE = simStore

Players = {
	PlayerRemoving = {
		Connect = function(_, fn)
			__ON_PLAYER_REMOVING = fn
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
"""


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def patched(raw: bytes) -> bytes:
    text = raw.decode("utf-8")
    count = text.count(DELTA_OLD)
    assert count == 1, f"require needle count {count} != 1"
    return text.replace(DELTA_OLD, DELTA_NEW).encode("utf-8")


def main() -> None:
    cur = (REPO / "roblox/src/server/ShadowLedger.luau").read_bytes()
    old = subprocess.run(
        ["git", "show", "5e291421a:roblox/src/server/ShadowLedger.luau"],
        cwd=REPO, capture_output=True, check=True,
    ).stdout
    kspace = (REPO / "roblox/src/shared/KSpace.luau").read_bytes()
    driver = (OUT / "driver.luau").read_bytes()

    ut_new = patched(cur)
    ut_old = patched(old)
    kspace_fn = kspace.decode("utf-8")

    combined = "\n".join([
        STUBS,
        "-- == real KSpace.luau (byte-identical, wrapped) ==",
        "__KSPACE_UNDER_TEST = (function()", kspace_fn, "end)()",
        "-- == real ShadowLedger.luau, HEAD (one-line harness delta) ==",
        "local SL = (function()", ut_new.decode("utf-8"), "end)()",
        "-- == real ShadowLedger.luau, pre-t74 5e291421a (one-line harness delta) ==",
        "local SOLD = (function()", ut_old.decode("utf-8"), "end)()",
        driver.decode("utf-8"),
    ])

    out = OUT / "combined_sim.luau"
    out.write_text(combined, encoding="utf-8", newline="\n")

    print("src ShadowLedger.luau (HEAD)      sha256", sha(cur))
    print("src ShadowLedger.luau (5e291421a) sha256", sha(old))
    print("src KSpace.luau                   sha256", sha(kspace))
    print("ut  ut_ShadowLedger (HEAD)        sha256", sha(ut_new))
    print("ut  ut_ShadowLedger (5e291421a)   sha256", sha(ut_old))
    print("out combined_sim.luau             sha256", sha(out.read_bytes()))
    print("sole delta:", DELTA_NEW.strip())


if __name__ == "__main__":
    main()
