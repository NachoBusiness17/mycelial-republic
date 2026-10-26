--!strict
-- ProceduralBody - DF build_body_from_rcp, folded into wisp shapes.
-- Mined chain (corpus/df_mine/df_procedural.json, assembly_chain_forgotten_beast):
--   a. weighted pick from the 235 RCP profiles -> body base; QUADRUPED has a
--      1-in-20 flip to SIX/EIGHT legs (profiles flagged cannot_have_get_more_legs
--      are exempt, mined law)
--   b. must_have parts are added UNCONDITIONALLY (wings, tails, shell, antennae,
--      horns, mandibles, pincers, claws, mantis arms, flippers, trunk, quills,
--      plates, stinger)
--   c. ONE primary tweak per body -> one attack class; scorpion profiles force
--      TAIL_STINGER, spiders force WEBS, stingers/blood/poison-bite force their
--      respective attacks, and FLAME forces FIRE (mined triggers). Per-class
--      triggers (mouth/beak for fire, evil-gated breath/secretion/blood) are
--      filtered and modeled per DF raws.
--   d. 1-in-20 uniform-material flip: the whole body becomes one matter family
--      (ash, flame, glass, mineral, ...); insubstantial families are tabled.
-- Tables are GENERATED (shared/RcpData.luau); this module owns the assembly.
-- Geometry is blocky Luau primitives welded to the core ball: the wisp stays
-- one physics assembly (chase velocity + Touched unchanged on the core).

local RcpData = require(script.Parent:WaitForChild("RcpData"))

local ProceduralBody = {}

export type Spec = {
	profile: string,
	profileType: string,
	bodyBase: string,
	legs: number,
	parts: { string }, -- mined must_have parts (wing flags resolved to a count)
	attack: string,
	warning: string,
	material: string, -- uniform matter family, "" = flesh
	insubstantial: boolean,
	description: string,
}

-- body base -> leg count (mined body_bases; limbless bases are 0)
local BASE_LEGS: { [string]: number } = {
	AMORPHOUS = 0,
	NO_LIMB = 0,
	WORM = 0,
	SNAKE = 0,
	INSECT_LARVA = 0,
	HUMANOID = 2,
	TWO_LEGS_NO_ARMS = 2,
	TWO_LEGS_NO_ARMS_HUMANOID = 2,
	BIPEDAL_DINOSAUR = 2,
	QUADRUPED = 4,
	QUADRUPED_FRONT_GRASP = 4,
	INSECT = 6,
	SCORPION = 8,
	SPIDER = 8,
	EIGHT_LEGGED = 8,
	EIGHT_LEGGED_LOBSTERFORM = 8,
	TEN_LEGGED = 10,
	TEN_LEGGED_LOBSTERFORM = 10,
}

-- mined flag -> rendered part (must_have_ prefix stripped)
local FLAG_PARTS: { [string]: string } = {
	must_have_insect_wings = "wings",
	must_have_skin_wings = "wings",
	must_have_feather_wings = "wings",
	must_have_tail = "tail",
	must_have_feather_tail = "tail",
	must_have_scorpion_tail = "raised tail",
	must_have_crustacean_tail = "tail",
	must_have_shell = "shell",
	must_have_antennae = "antennae",
	must_have_one_head_horn = "horn",
	must_have_giant_mandibles = "mandibles",
	must_have_pincers = "pincers",
	must_have_grabbing_claws = "claws",
	must_have_mantis_arms = "mantis arms",
	must_have_walrus_flippers = "flippers",
	must_have_elephant_trunk = "trunk",
	must_have_quills = "quills",
	must_have_plates = "plates",
	must_have_insect_stinger = "stinger",
}

-- uniform matter family -> color / Roblox material / transparency ("" family
-- = the wisp's flesh look, kept from the old ball)
export type MatterLook = { color: Color3, material: Enum.Material, alpha: number }

local MATTER_LOOK: { [string]: MatterLook } = {
	[""] = { color = Color3.fromRGB(140, 60, 200), material = Enum.Material.Neon, alpha = 0 },
	ASH = { color = Color3.fromRGB(90, 85, 82), material = Enum.Material.Slate, alpha = 0 },
	MUD = { color = Color3.fromRGB(95, 75, 55), material = Enum.Material.Mud, alpha = 0 },
	VOMIT = { color = Color3.fromRGB(120, 150, 60), material = Enum.Material.SmoothPlastic, alpha = 0 },
	SALT_POWDER = { color = Color3.fromRGB(225, 220, 205), material = Enum.Material.Salt, alpha = 0.3 },
	GRIME = { color = Color3.fromRGB(70, 65, 60), material = Enum.Material.Slate, alpha = 0 },
	SNOW = { color = Color3.fromRGB(235, 240, 250), material = Enum.Material.Snow, alpha = 0 },
	WATER = { color = Color3.fromRGB(120, 170, 220), material = Enum.Material.Glass, alpha = 0.4 },
	STEAM = { color = Color3.fromRGB(210, 215, 225), material = Enum.Material.Neon, alpha = 0.5 },
	FLAME = { color = Color3.fromRGB(255, 140, 40), material = Enum.Material.Neon, alpha = 0 },
	AMBER = { color = Color3.fromRGB(215, 150, 40), material = Enum.Material.SmoothPlastic, alpha = 0 },
		-- Coral exists at runtime but the gate definitions (tools/bin/globalTypes.d.luau) predate it: SmoothPlastic stands in
	CORAL = { color = Color3.fromRGB(220, 110, 110), material = Enum.Material.SmoothPlastic, alpha = 0 },
	GLASS_GREEN = { color = Color3.fromRGB(110, 200, 140), material = Enum.Material.Glass, alpha = 0.35 },
	GLASS_CLEAR = { color = Color3.fromRGB(200, 220, 235), material = Enum.Material.Glass, alpha = 0.35 },
	GLASS_CRYSTAL = { color = Color3.fromRGB(170, 190, 255), material = Enum.Material.Glass, alpha = 0.3 },
	CHARCOAL = { color = Color3.fromRGB(45, 42, 40), material = Enum.Material.Slate, alpha = 0 },
	COKE = { color = Color3.fromRGB(35, 32, 30), material = Enum.Material.Slate, alpha = 0 },
	SALT_SOLID = { color = Color3.fromRGB(230, 228, 215), material = Enum.Material.Salt, alpha = 0 },
	ICE = { color = Color3.fromRGB(170, 215, 240), material = Enum.Material.Ice, alpha = 0.15 },
}

local function hasFlag(flags: { string }, name: string): boolean
	for _, f in ipairs(flags) do
		if f == name then return true end
	end
	return false
end

-- a. weighted pick across the 235 mined profiles
local function pickProfile(rng: any)
	local total = 0
	for _, p in ipairs(RcpData.PROFILES) do
		total += p.weight
	end
	local roll = rng:next() * total
	for _, p in ipairs(RcpData.PROFILES) do
		roll -= p.weight
		if roll < 0 then
			return p
		end
	end
	return RcpData.PROFILES[#RcpData.PROFILES]
end

export type AssembleOpts = {
	isEvil: boolean?,
	material: string?,
}

local function hasMouthOrBeak(p: any, flags: { string }): boolean
	if p.class == "AVIAN" or hasFlag(flags, "must_have_beak") then
		return true
	end
	if p.class == "MAMMAL" or p.class == "REPTILE" or p.class == "REPTILE_FEATHERED" or p.class == "AMPHIBIAN" then
		return true
	end
	if p.bodyBase == "QUADRUPED" or p.bodyBase == "HUMANOID" or p.bodyBase == "BIPEDAL_DINOSAUR" or p.bodyBase == "SNAKE" then
		return true
	end
	if hasFlag(flags, "must_have_giant_mandibles") or hasFlag(flags, "must_have_poison_bite") then
		return true
	end
	return false
end

local function pickAttack(rng: any, p: any, flags: { string }, material: string, isEvil: boolean): string
	-- 1. Uniform FLAME material unconditionally forces FIRE (mined DF law)
	if material == "FLAME" then
		return "FIRE"
	end

	-- 2. Forced triggers from mined profile flags (mined DF laws)
	if hasFlag(flags, "must_have_scorpion_tail") then
		return "TAIL_STINGER"
	end
	if hasFlag(flags, "must_have_insect_stinger") then
		return "INSECT_STINGER"
	end
	if hasFlag(flags, "must_have_webs") then
		return "WEBS"
	end
	if hasFlag(flags, "must_have_poison_bite") then
		return "POISON_BITE"
	end
	if hasFlag(flags, "suck_blood_through_proboscis") or hasFlag(flags, "suck_blood_through_mouth") then
		return "PROBOSCIS_BLOOD"
	end

	-- 3. Anatomical and alignment candidate filtering per DF raws
	local candidates: { string } = {}

	-- FIRE: requires mouth or beak (avian, reptile, quadruped, humanoid, etc.)
	if hasMouthOrBeak(p, flags) then
		table.insert(candidates, "FIRE")
	end

	-- BREATHE_TRAILING_FLOW / BREATHE_UNDIRECTED: evil-only breath attacks
	if isEvil then
		table.insert(candidates, "BREATHE_TRAILING_FLOW")
		table.insert(candidates, "BREATHE_UNDIRECTED")
	end

	-- BREATHE_GLOB: deadly spittle, requires head/mouth (non-amorphous)
	if hasMouthOrBeak(p, flags) or p.bodyBase ~= "AMORPHOUS" then
		table.insert(candidates, "BREATHE_GLOB")
	end

	-- POISON_BLOOD: evil + creature has blood/ichor/goo (vertebrate or fleshy)
	if isEvil and (p.class == "FLESHY" or p.class == "MAMMAL" or p.class == "REPTILE" or p.class == "REPTILE_FEATHERED" or p.class == "AMPHIBIAN" or p.class == "AVIAN") then
		table.insert(candidates, "POISON_BLOOD")
	end

	-- SECRETION: evil + solid surface body (chitin, reptile, plates, shell)
	if isEvil and (p.class == "CHITIN_EXO" or p.class == "REPTILE" or hasFlag(flags, "must_have_plates") or hasFlag(flags, "must_have_shell")) then
		table.insert(candidates, "SECRETION")
	end

	-- TAIL_STINGER: 1-in-20 if creature has a tail
	if (hasFlag(flags, "must_have_tail") or hasFlag(flags, "must_have_crustacean_tail") or hasFlag(flags, "must_have_feather_tail")) and rng:next() < 0.05 then
		table.insert(candidates, "TAIL_STINGER")
	end

	-- INSECT_STINGER: 1-in-20 if insect/chitin
	if p.class == "CHITIN_EXO" and rng:next() < 0.05 then
		table.insert(candidates, "INSECT_STINGER")
	end

	-- POISON_BITE: bite injection if mouth/teeth present
	if hasMouthOrBeak(p, flags) then
		table.insert(candidates, "POISON_BITE")
	end

	-- PROBOSCIS_BLOOD: blood hunger
	if p.bodyBase == "INSECT" or p.bodyBase == "WORM" or p.class == "CHITIN_EXO" then
		table.insert(candidates, "PROBOSCIS_BLOOD")
	end

	-- WEBS: spinnerets (arachnid or insect)
	if p.bodyBase == "SPIDER" or p.class == "CHITIN_EXO" then
		table.insert(candidates, "WEBS")
	end

	-- If candidates pool is empty, fallback to all ATTACKS
	if #candidates == 0 then
		for name in pairs(RcpData.ATTACKS) do
			table.insert(candidates, name)
		end
	end

	table.sort(candidates) -- deterministic under SeedRng replay
	return candidates[rng:int(1, #candidates)]
end

function ProceduralBody.assemble(rng: any, maybeOpts: AssembleOpts?): Spec
	local p = pickProfile(rng)
	local flags: { string } = {}
	for f in string.gmatch(p.flags, "[^;]+") do
		table.insert(flags, f)
	end
	local isEvil = if maybeOpts and maybeOpts.isEvil ~= nil then maybeOpts.isEvil else true

	-- a. legs: base count + the QUADRUPED 1-in-20 leg flip (exempt flag honored)
	local legs = BASE_LEGS[p.bodyBase] or 4
	if p.bodyBase == "QUADRUPED" and not hasFlag(flags, "cannot_have_get_more_legs") and rng:next() < 1 / 20 then
		legs = rng:int(6, 8) -- mined: grows SIX_LEGGED or EIGHT_LEGGED
	end

	-- b. must_have parts, unconditional
	local parts: { string } = {}
	for _, f in ipairs(flags) do
		local part = FLAG_PARTS[f]
		if part and part ~= "wings" then
			table.insert(parts, part)
		elseif part == "wings" then
			table.insert(parts, "wings") -- one wings entry regardless of which flag
		end
	end

	-- c. uniform matter family: 1-in-20 uniform-material flip (or forced by options)
	local material = (maybeOpts and maybeOpts.material) or ""
	if material == "" and rng:next() < 1 / 20 then
		material = RcpData.MATTER[rng:int(1, #RcpData.MATTER)]
	end
	local insubstantial = false
	for _, m in ipairs(RcpData.INSUBSTANTIAL) do
		if m == material then
			insubstantial = true
			break
		end
	end

	-- d. primary tweak -> attack class per DF triggers + warning line
	local attack = pickAttack(rng, p, flags, material, isEvil)
	local warning = RcpData.ATTACKS[attack].warning

	local piece = #parts > 0 and (" " .. table.concat(parts, ", ")) or ""
	local description = ("%s (%s, %d legs%s)%s"):format(
		p.name, p.bodyBase, legs, piece,
		material ~= "" and (" composed of " .. string.lower(material)) or ""
	)

	return {
		profile = p.name,
		profileType = p.type,
		bodyBase = p.bodyBase,
		legs = legs,
		parts = parts,
		attack = attack,
		warning = warning,
		material = material,
		insubstantial = insubstantial,
		description = description,
	}
end

-- ---- rendering: welded primitive parts around the core ball ----

local function lookFor(spec: Spec): MatterLook
	return MATTER_LOOK[spec.material] or MATTER_LOOK[""]
end

local function part(model: Model, name: string, size: Vector3, cframe: CFrame, color: Color3, material: Enum.Material, transparency: number, core: BasePart)
	local p = Instance.new("Part")
	p.Name = name
	p.Size = size
	p.CFrame = cframe
	p.Color = color
	p.Material = material
	p.Transparency = transparency
	p.CanCollide = false
	p.Massless = true -- the core keeps the whole assembly's physics
	p.Parent = model
	local weld = Instance.new("WeldConstraint")
	weld.Part0 = core
	weld.Part1 = p
	weld.Parent = p
	return p
end

-- attach the mined body plan to a core ball; returns the Model wrapper
function ProceduralBody.build(spec: Spec, core: BasePart): Model
	local model = Instance.new("Model")
	model.Name = "ForgottenWisp"
	local look = lookFor(spec)
	local function add(name: string, size: Vector3, cframe: CFrame)
		part(model, name, size, cframe, look.color, look.material, look.alpha, core)
	end
	local at = core.CFrame

	-- legs (QUADRUPED law: the flip decides 4/6/8; insect bases carry their own)
	for i = 1, spec.legs do
		local side = (i % 2 == 0) and 1 or -1
		local row = math.floor((i - 1) / 2)
		local spread = math.min(row + 1, 3)
		add("Leg", Vector3.new(0.5, 2, 0.5),
			at * CFrame.new(side * 1.4, -0.8, spread * 1.2 - 1.2) * CFrame.Angles(0, 0, math.rad(side * 25)))
	end

	for _, partName in ipairs(spec.parts) do
		if partName == "wings" then
			for _, s in ipairs({ -1, 1 }) do
				add("Wing", Vector3.new(4, 0.2, 1.6),
					at * CFrame.new(s * 2.8, 1.1, -0.3) * CFrame.Angles(0, 0, math.rad(s * -18)))
			end
		elseif partName == "tail" or partName == "raised tail" then
			local lift = (partName == "raised tail") and 1.6 or 0
			add("Tail", Vector3.new(0.8, 0.8, 3), at * CFrame.new(0, lift, -2.4) * CFrame.Angles(math.rad(-15), 0, 0))
		elseif partName == "shell" then
			local shell = Instance.new("Part")
			shell.Name = "Shell"
			shell.Shape = Enum.PartType.Ball
			shell.Size = Vector3.new(3.4, 2.6, 3.4)
			shell.CFrame = at * CFrame.new(0, 1.1, 0)
			shell.Color = look.color
			shell.Material = look.material
			shell.Transparency = look.alpha
			shell.CanCollide = false
			shell.Massless = true
			shell.Parent = model
			local weld = Instance.new("WeldConstraint")
			weld.Part0 = core
			weld.Part1 = shell
			weld.Parent = shell
		elseif partName == "antennae" then
			for _, s in ipairs({ -1, 1 }) do
				add("Antenna", Vector3.new(0.15, 1.6, 0.15),
					at * CFrame.new(s * 0.5, 1.8, 0.6) * CFrame.Angles(math.rad(20), 0, math.rad(s * 15)))
			end
		elseif partName == "horn" then
			add("Horn", Vector3.new(0.4, 1.4, 0.4), at * CFrame.new(0, 1.9, 0.8) * CFrame.Angles(math.rad(-20), 0, 0))
		elseif partName == "mandibles" then
			for _, s in ipairs({ -1, 1 }) do
				add("Mandible", Vector3.new(0.4, 0.4, 1.8),
					at * CFrame.new(s * 0.9, 0.2, 1.8) * CFrame.Angles(0, math.rad(s * 25), 0))
			end
		elseif partName == "pincers" or partName == "claws" or partName == "mantis arms" then
			for _, s in ipairs({ -1, 1 }) do
				add(partName, Vector3.new(0.5, 0.5, 2),
					at * CFrame.new(s * 1.6, 0.3, 1.4) * CFrame.Angles(0, math.rad(s * 15), 0))
			end
		elseif partName == "flippers" then
			for _, s in ipairs({ -1, 1 }) do
				add("Flipper", Vector3.new(1.8, 0.3, 1.2), at * CFrame.new(s * 2, -0.5, 0))
			end
		elseif partName == "trunk" then
			add("Trunk", Vector3.new(0.5, 2.2, 0.5), at * CFrame.new(0, -0.6, 2) * CFrame.Angles(math.rad(30), 0, 0))
		elseif partName == "quills" then
			for i = 1, 4 do
				add("Quill", Vector3.new(0.15, 1.8, 0.15),
					at * CFrame.new((i - 2.5) * 0.6, 1.6, -0.4) * CFrame.Angles(math.rad(-20), 0, 0))
			end
		elseif partName == "plates" then
			for i = 1, 3 do
				add("Plate", Vector3.new(1.8, 0.3, 1), at * CFrame.new(0, 1.5, (i - 2) * 1.1))
			end
		elseif partName == "stinger" then
			add("Stinger", Vector3.new(0.4, 1.4, 0.4), at * CFrame.new(0, 0.6, -2.2) * CFrame.Angles(math.rad(40), 0, 0))
		end
	end

	model.PrimaryPart = core
	return model
end

return ProceduralBody
