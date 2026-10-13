-- eigenmap_two_smoke_env  -  the Roblox-API stub environment for the
-- headless execution smoke (consumed by tools/eigenmap_two_smoke.py, which
-- stages this file as SmokeEnv.luau beside byte-copies of the real scripts).
--
-- WHY a module: the luau CLI gives every file its OWN global environment, so
-- globals defined in a driver never reach a required module. The smoke
-- therefore prepends a two-line prelude to the staged copies of the REAL
-- CathedralPlate/CathedralMapHud scripts that binds this shared environment
-- (game, workspace, Instance, Vector3, ...) as file-local names shadowing the
-- missing globals; require() caches modules, so plate + HUD + driver all see
-- the SAME workspace, players and signals, and the driver can observe every
-- part the build created. The tree files' bytes are unchanged; the prelude
-- exists only inside the staged copies (the Python asserts the staged file
-- ends with the exact tree bytes).
--
-- Fidelity note: this is a behavioral stub of the API surface the two
-- scripts touch (properties, Parent/children bookkeeping, signals, Vector3
-- arithmetic). It proves the code paths run and their numbers are right; it
-- is NOT Roblox Studio (no rendering, no physics, no DataStore).

local SmokeEnv = {}

local function newSignal()
	local sig = { _fns = {} }
	function sig:Connect(fn)
		table.insert(self._fns, fn)
		return { Connected = true, Disconnect = function() end }
	end
	function sig:Once(fn)
		table.insert(self._fns, fn)
	end
	function sig:Fire(...)
		for _, fn in ipairs(self._fns) do
			fn(...)
		end
	end
	return sig
end
SmokeEnv.newSignal = newSignal

local V3 = {}
V3.__index = function(t, k)
	if k == "Magnitude" then
		return math.sqrt(t.X * t.X + t.Y * t.Y + t.Z * t.Z)
	end
	return nil
end
V3.__add = function(a, b) return setmetatable({ X = a.X + b.X, Y = a.Y + b.Y, Z = a.Z + b.Z }, V3) end
V3.__sub = function(a, b) return setmetatable({ X = a.X - b.X, Y = a.Y - b.Y, Z = a.Z - b.Z }, V3) end
V3.__unm = function(a) return setmetatable({ X = -a.X, Y = -a.Y, Z = -a.Z }, V3) end
V3.__div = function(a, s) return setmetatable({ X = a.X / s, Y = a.Y / s, Z = a.Z / s }, V3) end
V3.__eq = function(a, b) return a.X == b.X and a.Y == b.Y and a.Z == b.Z end
V3.__tostring = function(a) return ("%f, %f, %f"):format(a.X, a.Y, a.Z) end
function V3.new(x, y, z) return setmetatable({ X = x or 0, Y = y or 0, Z = z or 0 }, V3) end
SmokeEnv.Vector3 = { new = V3.new, zero = V3.new(0, 0, 0), one = V3.new(1, 1, 1) }

local V2 = {}
V2.__index = V2
function V2.new(x, y) return setmetatable({ X = x or 0, Y = y or 0 }, V2) end
SmokeEnv.Vector2 = { new = V2.new, zero = V2.new(0, 0), one = V2.new(1, 1) }

SmokeEnv.Color3 = {
	new = function(r, g, b) return { R = r, G = g, B = b, _c3 = true } end,
	fromRGB = function(r, g, b) return { R = r, G = g, B = b, _c3 = "rgb" } end,
}

SmokeEnv.UDim2 = {
	new = function(xs, xo, ys, yo)
		return { X = { Scale = xs, Offset = xo }, Y = { Scale = ys, Offset = yo }, _udim2 = "new" }
	end,
	fromScale = function(xs, ys)
		return { X = { Scale = xs, Offset = 0 }, Y = { Scale = ys, Offset = 0 }, _udim2 = "fromScale" }
	end,
	fromOffset = function(x, y)
		return { X = { Scale = 0, Offset = x }, Y = { Scale = 0, Offset = y }, _udim2 = "fromOffset" }
	end,
}
SmokeEnv.UDim = { new = function(s, o) return { Scale = s, Offset = o } end }

local function autoEnum()
	return setmetatable({}, { __index = function(t, k)
		local v = autoEnum()
		rawset(t, k, v)
		return v
	end })
end
SmokeEnv.Enum = autoEnum()

SmokeEnv.CFrame = {
	new = function(...) return { _kind = "new", args = { ... } } end,
	lookAt = function(from, to) return { _kind = "lookAt", from = from, to = to } end,
}

-- the canvas default every Frame reports as AbsoluteSize (the smoke's Python
-- mirrors these numbers when it recomputes the HUD render equation)
SmokeEnv.CANVAS_W, SmokeEnv.CANVAS_H = 280, 176

-- Instances are PROXIES over a backing store: every property write passes
-- through __newindex (a plain table would let the SECOND `inst.Parent = x`
-- assignment bypass the metamethod once the key exists, silently dropping
-- re-parent tracking; caught by the youMarker case, fixed 2026-09-27).
SmokeEnv.Instance = {
	new = function(className)
		local store = { ClassName = className, _kids = {} }
		-- forward-declared: `local proxy = setmetatable(...)` would NOT put the
		-- local in scope inside its own initializer (the closures would capture
		-- a nil outer `proxy`; caught by the youMarker/workspace repro, 2026-09-27)
		local proxy
		proxy = setmetatable({}, {
			__index = function(_, k)
				if k == "Touched" then
					if store.Touched == nil then
						store.Touched = newSignal()
					end
					return store.Touched
				elseif k == "GetPropertyChangedSignal" then
					return function(_s, _prop) return newSignal() end
				elseif k == "ClearAllChildren" then
					return function(_s)
						for i in pairs(store._kids) do
							store._kids[i] = nil
						end
					end
				elseif k == "GetChildren" then
					return function(_s)
						local out = {}
						for _, c in ipairs(store._kids) do
							table.insert(out, c)
						end
						return out
					end
				elseif k == "AbsoluteSize" and store.AbsoluteSize == nil then
					return V2.new(SmokeEnv.CANVAS_W, SmokeEnv.CANVAS_H)
				end
				return store[k]
			end,
			__newindex = function(_, k, v)
				if k == "Parent" and v ~= nil and type(v) == "table" then
					store.Parent = v
					local pkids = v._kids -- recurses through the child proxy's __index
					if pkids ~= nil then
						table.insert(pkids, proxy)
					end
					return
				end
				store[k] = v
			end,
		})
		return proxy
	end,
}

SmokeEnv.workspace = SmokeEnv.Instance.new("Workspace")

-- the one fake player both scripts see
SmokeEnv.state = { fakeCharacter = nil }
local playerGui = SmokeEnv.Instance.new("PlayerGui")
SmokeEnv.playerStub = {
	UserId = 4242,
	Character = nil, -- the driver sets this before firing the HUD heartbeat
	WaitForChild = function(_, n)
		if n == "PlayerGui" then
			return playerGui
		end
		error("smoke stub: unexpected WaitForChild " .. tostring(n))
	end,
}
SmokeEnv.playerGui = playerGui
local PlayersService = {
	LocalPlayer = SmokeEnv.playerStub,
	GetPlayerFromCharacter = function(_, char)
		if char == SmokeEnv.state.fakeCharacter then
			return SmokeEnv.playerStub
		end
		return nil
	end,
}
local ModulesNode = {
	WaitForChild = function(_, n)
		if n == "CathedralMap" then
			return "./CathedralMap" -- string require: resolves in the staged dir
		end
		error("smoke stub: unexpected module WaitForChild " .. tostring(n))
	end,
}
local ReplicatedStorageService = {
	WaitForChild = function(_, n)
		if n == "Modules" then
			return ModulesNode
		end
		error("smoke stub: unexpected WaitForChild " .. tostring(n))
	end,
}
SmokeEnv.runService = { Heartbeat = newSignal(), RenderStepped = newSignal() }
local services = {
	Players = PlayersService,
	ReplicatedStorage = ReplicatedStorageService,
	RunService = SmokeEnv.runService,
}
SmokeEnv.game = {
	GetService = function(_, name)
		return services[name] or error("smoke stub: unexpected service " .. tostring(name))
	end,
}
SmokeEnv.script = {
	Parent = {
		WaitForChild = function(_, n)
			if n == "ShadowLedger" then
				return "./ShadowLedgerStub"
			end
			error("smoke stub: unexpected script.Parent WaitForChild " .. tostring(n))
		end,
	},
}

function SmokeEnv.kidsOf(inst)
	return inst._kids or {} -- through the proxy __index (no rawget: proxies carry no keys)
end

return SmokeEnv
