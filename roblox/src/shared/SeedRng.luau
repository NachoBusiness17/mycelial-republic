--!strict
-- SeedRng — xorshift32, replay-safe: same seed, same mountain, bit-exact rerun.
-- (mulberry32 needs 32-bit multiply wraparound, which Luau doubles lose above
-- 2^53; xorshift32 uses only xor/shift so it is exact. The fleet's Python
-- mulberry32 seeds map 1:1 — same seed integer, deterministic both sides.)

local SeedRng = {}

export type Rng = {
	next: (self: Rng) -> number,
	int: (self: Rng, lo: number, hi: number) -> number,
	pick: (self: Rng, list: { string }) -> string,
	seed: number,
}

function SeedRng.new(seed: number): Rng
	local self = setmetatable({ seed = seed % 2147483647 }, { __index = SeedRng })
	if self.seed == 0 then self.seed = 1 end -- xorshift32 must not start at zero
	return (self :: any)
end

function SeedRng:next(): number
	local s = self.seed
	s = bit32.bxor(s, bit32.lshift(s, 13))
	s = bit32.bxor(s, bit32.rshift(s, 17))
	s = bit32.bxor(s, bit32.lshift(s, 5))
	self.seed = s
	return s / 4294967296
end

function SeedRng:int(lo: number, hi: number): number
	local n: number = self:next()
	return lo + math.floor(n * (hi - lo + 1))
end

function SeedRng:pick(list: { string }): string
	return list[self:int(1, #list)]
end

return SeedRng
