--!strict
-- LeaderstatsHud  -  the Mountain's always-on-screen scorecard page (Q-041
-- 2026-09-28). The server's leaderstats folder (init.server.luau:200-263)
-- already gives the Roblox-standard M-key player list; this page is the
-- visible top-right mirror of the SAME four IntValues (Virtue Marks,
-- Rebirths, Invariants, Summits). Courier law: read-only, no second truth.
-- The IntValues are the single source, so the page reads .Value once at bind
-- then rides each IntValue's Changed signal - no polling (the t56 law that
-- cured the server's leaderstats poll applies here too).
-- Respawn-safe: the folder lives on the Player, not the Character, and the
-- ScreenGui is ResetOnSpawn=false like every HUD in this tree. While the
-- server has not yet attached (or a stat child has not replicated) the row
-- reads "..." - an honest blank, never a fabricated 0.

local Players = game:GetService("Players")

local player = Players.LocalPlayer

local INK = Color3.fromRGB(230, 224, 196)
local PANEL = Color3.fromRGB(20, 18, 26)

-- the four rows, keyed by the leaderstats child name (sole writer:
-- init.server.luau:205-214); label is the display name
local ROWS: { { stat: string, label: string } } = {
	{ stat = "Virtue Marks", label = "VM" },
	{ stat = "Rebirths", label = "Rebirths" },
	{ stat = "Invariants", label = "Invariants" },
	{ stat = "Summits", label = "Summits" },
}

-- ---- panel: top-right, 36px down (clears the Roblox top bar, same offset
-- the cathedral panel uses to clear the sphere chip); the cathedral panel
-- holds the left column, so the right was the one free wall ----
local gui = Instance.new("ScreenGui")
gui.Name = "LeaderstatsHud"
gui.ResetOnSpawn = false
gui.DisplayOrder = 10
gui.Parent = player:WaitForChild("PlayerGui")

local panel = Instance.new("Frame")
panel.AnchorPoint = Vector2.new(1, 0)
panel.Position = UDim2.new(1, -8, 0, 36)
panel.Size = UDim2.new(0, 176, 0, 124)
panel.BackgroundColor3 = PANEL
panel.BackgroundTransparency = 0.35
panel.BorderSizePixel = 0
local panelCorner = Instance.new("UICorner")
panelCorner.CornerRadius = UDim.new(0, 8)
panelCorner.Parent = panel
panel.Parent = gui

local title = Instance.new("TextLabel")
title.Size = UDim2.new(1, -16, 0, 18)
title.Position = UDim2.new(0, 8, 0, 6)
title.BackgroundTransparency = 1
title.Font = Enum.Font.Garamond
title.TextSize = 14
title.TextColor3 = INK
title.TextXAlignment = Enum.TextXAlignment.Left
title.Text = "THE MOUNTAIN · scorecard"
title.Parent = panel

local rowsFrame = Instance.new("Frame")
rowsFrame.Size = UDim2.new(1, -16, 0, #ROWS * 22)
rowsFrame.Position = UDim2.new(0, 8, 0, 28)
rowsFrame.BackgroundTransparency = 1
rowsFrame.BorderSizePixel = 0
local layout = Instance.new("UIListLayout")
layout.FillDirection = Enum.FillDirection.Vertical
layout.SortOrder = Enum.SortOrder.LayoutOrder
layout.Parent = rowsFrame
rowsFrame.Parent = panel

-- ---- wire: one row per leaderstats IntValue ----
local stats = player:WaitForChild("leaderstats")

for i, row in ipairs(ROWS) do
	local holder = Instance.new("Frame")
	holder.Size = UDim2.new(1, 0, 0, 22)
	holder.BackgroundTransparency = 1
	holder.BorderSizePixel = 0
	holder.LayoutOrder = i
	holder.Parent = rowsFrame

	local name = Instance.new("TextLabel")
	name.Size = UDim2.new(1, -52, 1, 0)
	name.BackgroundTransparency = 1
	name.Font = Enum.Font.Garamond
	name.TextSize = 14
	name.TextColor3 = INK
	name.TextXAlignment = Enum.TextXAlignment.Left
	name.Text = row.label
	name.Parent = holder

	local value = Instance.new("TextLabel")
	value.AnchorPoint = Vector2.new(1, 0)
	value.Position = UDim2.new(1, 0, 0, 0)
	value.Size = UDim2.new(0, 48, 1, 0)
	value.BackgroundTransparency = 1
	value.Font = Enum.Font.Code
	value.TextSize = 14
	value.TextColor3 = INK
	value.TextXAlignment = Enum.TextXAlignment.Right
	value.Text = "..." -- pre-replication honest blank
	value.Parent = holder

	local stat = stats:WaitForChild(row.stat) :: IntValue
	local function paint(n: number)
		value.Text = ("%d"):format(n)
	end
	paint(stat.Value)
	stat.Changed:Connect(paint)
end
