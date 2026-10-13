--!strict
-- TheAnswerBoss — the summit. 5 phases, the 15-degree lean before the strike
-- in phase 3 (the tell), Calabi-Yau deflection (jump the fold) and the
-- Wing Chun redirect (turn the centerline, give it back).
-- The Answer's Weakness pass (499R) highlights the tell in phase 3.

local Players = game:GetService("Players")
local Shared = game:GetService("ReplicatedStorage"):WaitForChild("Modules")
local Lore = require(Shared:WaitForChild("Lore"))
local Trove = require(Shared:WaitForChild("Trove"))
local Monetization = require(script.Parent:WaitForChild("Monetization"))

local TheAnswerBoss = {}
local arena = Vector3.new(0, 8 + 30 * 6, -0) -- summit: depth 6 * 30 studs up
local running = false

local function telegraph(boss: Part, strikePos: Vector3, showTell: boolean)
	-- the lean: 15 degrees off true before it strikes (Lore.TheAnswer.tellDegrees)
	local lean = showTell and Lore.TheAnswer.tellDegrees or 0
	boss.CFrame = CFrame.new(boss.Position)
		* CFrame.Angles(math.rad(lean), 0, math.rad(lean))
	local conn
	conn = boss.Touched:Connect(function(hit)
		local player = hit.Parent and Players:GetPlayerFromCharacter(hit.Parent)
		if player and player.Character then
			player.Character:BreakJoints() -- the strike lands unless deflected/redirected
			conn:Disconnect()
		end
	end)
	task.delay(0.9, function()
		conn:Disconnect()
		boss.CFrame = CFrame.new(strikePos)
	end)
end

function TheAnswerBoss.build(): Model
	local model = Instance.new("Model")
	model.Name = "TheAnswerArena"

	local platform = Instance.new("Part")
	platform.Anchored = true
	platform.Size = Vector3.new(90, 2, 90)
	platform.Position = Vector3.new(0, arena.Y - 1, 0)
	platform.Color = Color3.fromRGB(14, 12, 20)
	platform.Material = Enum.Material.Slate
	platform.Parent = model

	local boss = Instance.new("Part")
	boss.Anchored = true
	boss.Shape = Enum.PartType.Ball
	boss.Size = Vector3.new(10, 10, 10)
	boss.Position = arena + Vector3.new(0, 7, -24)
	boss.Color = Color3.fromRGB(200, 196, 210)
	boss.Material = Enum.Material.ForceField
	boss.Name = "THE ANSWER"
	boss.Parent = model

	local tag = Instance.new("BillboardGui")
	tag.Size = UDim2.new(0, 300, 0, 40)
	tag.StudsOffset = Vector3.new(0, 7, 0)
	tag.AlwaysOnTop = true
	local lbl = Instance.new("TextLabel")
	lbl.Size = UDim2.fromScale(1, 1)
	lbl.BackgroundTransparency = 1
	lbl.Text = Lore.TheAnswer.name .. " · " .. Lore.TheAnswer.prose[1]
	lbl.TextColor3 = Color3.fromRGB(235, 230, 210)
	lbl.Font = Enum.Font.Garamond
	lbl.TextSize = 18
	lbl.Parent = tag
	tag.Parent = boss

	local start = Instance.new("ProximityPrompt")
	start.ActionText = "Ask it anything"
	start.ObjectText = "THE ANSWER"
	start.HoldDuration = 2
	start.Parent = boss

	start.Triggered:Connect(function(player: Player)
		if running then return end
		running = true
		-- Q-043 Trove pass: the fight loop is OWNED by the boss's lifetime
		-- (AttachToInstance -> Destroying -> Clean cancels the thread). A boss
		-- destroyed mid-fight now ends the encounter instead of leaving a
		-- loop spawning fold-waves at a corpse (the old task.spawn died by
		-- error, unowned). The normal path is byte-identical: hp drains to 0,
		-- the thread finishes, running drops. Raw tracked thread, not
		-- trove:Loop — a phase paces itself with two different waits (3s
		-- telegraph, 2s strike) that a fixed-interval Loop cannot express.
		local fightTrove = Trove.new()
		fightTrove:AttachToInstance(boss)
		fightTrove:Add(task.spawn(function()
			local hp = 5 -- five phases; each landed redirect costs it a phase
			while hp > 0 do
				local phase = Lore.TheAnswer.phases - hp + 1
				lbl.Text = ("PHASE %d · %s"):format(phase, Lore.TheAnswer.prose[phase])

				-- the fold wave: jump it (Calabi-Yau deflection)
				local wave = Instance.new("Part")
				wave.Anchored = false
				wave.Size = Vector3.new(90, 1, 4)
				wave.CFrame = CFrame.new(boss.Position + Vector3.new(0, 1, 10))
				wave.Color = Color3.fromRGB(120, 110, 220)
				wave.Material = Enum.Material.Neon
				wave.CanCollide = false
				wave.Parent = model
				wave.AssemblyLinearVelocity = Vector3.new(0, 0, 30)
				local hitOnce = false
				wave.Touched:Connect(function(hit)
					if hitOnce then return end
					local charModel = hit.Parent :: Model?
					local plr = charModel and Players:GetPlayerFromCharacter(charModel)
					if plr and charModel then
						local root = charModel:FindFirstChild("HumanoidRootPart") :: BasePart?
						-- WING CHUN REDIRECT (C, 1.5s window): do not meet the mass;
						-- turn the centerline and give it back — a redirected wave
						-- costs THE ANSWER a phase (the only way to hurt it).
						if plr:GetAttribute("Abil_Redirect") == true then
							hitOnce = true
							plr:SetAttribute("RedirectedWave", tonumber((plr:GetAttribute("RedirectedWave")) or 0) + 1)
							hp -= 1
							lbl.Text = "THE WAVE TURNS AROUND. IT ANSWERS ITSELF."
							if wave.Parent then wave:Destroy() end
							return
						end
						-- Calabi-Yau deflection: airborne players fold over it untouched
						-- fix 2026-09-25 (t1a): 'char' was an undefined global here
						-- (luau-lsp TypeError at 115,25); root from line 102 is the
						-- same lookup, so the shadowed re-declaration was removed.
						if root and root.AssemblyLinearVelocity.Y > 4 then return end
						hitOnce = true
						charModel:BreakJoints()
					end
				end)
				task.delay(4, function() if wave.Parent then wave:Destroy() end end)

				-- the strike: telegraphed lean (visible tell if pass owned or late phases)
				task.wait(3)
				local showTell = phase >= Lore.TheAnswer.tellPhase + 1
					or Monetization.owns(player, "AnswersWeakness")
				telegraph(boss, boss.Position, showTell)
				task.wait(2)

				hp -= 1
			end
			lbl.Text = "IT ANSWERED ITSELF. THE CHAIRS AT BASECAMP ARE SIX AGAIN."
			running = false
		end))
	end)

	model.Parent = workspace
	return model
end

return TheAnswerBoss
