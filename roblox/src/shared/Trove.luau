--!strict
-- Trove — scoped cleanup, the Sleitnick/RbxUtil Trove pattern (the ADOPT row
-- of docs/ARCHITECTURE_NEXT.md: "every portal ring, NPC loop and sentinel
-- gets Trove-scoped teardown"). A trove tracks instances, connections,
-- threads, functions and cleanup tables; one Clean() tears them all down, so
-- a hand-rolled task.spawn loop dies by OWNERSHIP instead of polling .Parent
-- or waiting out a task.delay age (ARCHITECTURE_NEXT move 3: "six loops in
-- zones currently die by task.delay age, not ownership" — Q-043 landed the
-- conversions; see each zone's fix receipt).
--
-- Minimal in-repo implementation: the full RbxUtil package is not vendored
-- (no Packages tree in this repo), so this file keeps the upstream SHAPE —
-- Add / Connect / AttachToInstance / Clean / Destroy with the same cleanup
-- dispatch (Instance Destroy, connection Disconnect, thread cancel, function
-- call, table method) — plus one local extension, Loop(interval, fn), which
-- spawns a repeating thread the trove owns. Loop contract:
--   - the body runs immediately, then every `interval` seconds (the shape
--     every converted loop already had: check, act, task.wait);
--   - returning exactly `false` from the body ends the thread (a loop that
--     destroys its own subject returns false; the thread exits on its own);
--     any other return (including none) keeps the loop running;
--   - Clean() task.cancels the thread (safe no-op if it already ended, and
--     safe if it is the thread currently running the body: the Destroying
--     handler fires synchronously from Destroy inside the body, the pcall'd
--     cancel is a no-op on a running thread, and the false return then ends
--     it naturally — both paths terminate, nothing spins).

export type Trove = {
	Add: (self: Trove, object: any, cleanupMethod: string?) -> any,
	Connect: (self: Trove, signal: RBXScriptSignal, fn: (...any) -> (...any)) -> RBXScriptConnection,
	AttachToInstance: (self: Trove, instance: Instance) -> RBXScriptConnection,
	Loop: (self: Trove, interval: number, fn: () -> ...any) -> thread,
	Clean: (self: Trove) -> (),
	Destroy: (self: Trove) -> (),
}

local Trove = {}
Trove.__index = Trove

local function cleanupEntry(entry: { any })
	local object, method = entry[1], entry[2]
	local kind = typeof(object)
	if kind == "Instance" then
		(object :: Instance):Destroy()
	elseif kind == "RBXScriptConnection" then
		(object :: RBXScriptConnection):Disconnect()
	elseif kind == "thread" then
		pcall(task.cancel, object :: thread) -- a dead or running thread just refuses; that is fine
	elseif kind == "function" then
		(object :: () -> ())()
	elseif kind == "table" then
		local tbl = object :: { [string]: any }
		local name = method
			or (typeof(tbl.Destroy) == "function" and "Destroy" or nil)
			or (typeof(tbl.Disconnect) == "function" and "Disconnect" or nil)
			or (typeof(tbl.Clean) == "function" and "Clean" or nil)
		if name then
			tbl[name](tbl)
		end
	end
end

function Trove.new(): Trove
	local self = setmetatable({
		_entries = {} :: { { any } },
		_locked = false,
		_cleaning = false,
	}, Trove)
	return (self :: any) :: Trove
end

function Trove:Add(object: any, cleanupMethod: string?): any
	if self._locked then
		error("Trove is locked (Destroy was called)", 2)
	end
	table.insert(self._entries, { object, cleanupMethod })
	return object
end

function Trove:Connect(signal: RBXScriptSignal, fn: (...any) -> (...any)): RBXScriptConnection
	return self:Add(signal:Connect(fn)) :: RBXScriptConnection
end

function Trove:AttachToInstance(instance: Instance): RBXScriptConnection
	return self:Connect(instance.Destroying, function()
		self:Clean()
	end)
end

function Trove:Loop(interval: number, fn: () -> ...any): thread
	local thread: thread
	thread = task.spawn(function()
		while true do
			if fn() == false then
				break
			end
			task.wait(interval)
		end
	end)
	return self:Add(thread) :: thread
end

function Trove:Clean()
	if self._cleaning then
		return -- re-entrant: a Destroy inside the sweep re-fired Destroying
	end
	self._cleaning = true
	local entries = self._entries
	self._entries = {}
	for i = #entries, 1, -1 do -- LIFO: last-added torn down first
		cleanupEntry(entries[i])
	end
	self._cleaning = false
	self._locked = false
end

function Trove:Destroy()
	self:Clean()
	self._locked = true
end

return Trove
