#!/usr/bin/env python3
"""B2-31 verification: poll/RMW disease tripwire in tools/luau_lint.py.

Proves, against fixtures shaped like the real diseases from the t56/t63/t74
receipts (watch/inbox/gala_20260925/afterparty/lanes/):
  1. t56-style 1s leaderstats poll trips the poll check, reported line matches.
  2. t63-style 10s garden GetPlayers poll (nested for, no closure) trips it.
  3. t74-style GetAsync+SetAsync in one function trips the RMW check.
  4. Cured shapes stay clean: HeadMuseum split flush/restore, TheAnswerBoss
     Touched closure reads (closure depth 1) with task.wait(3)/task.wait(2) at
     loop depth 0, and disease keywords living only in comments/strings.
  5. blank_comments_strings is length- and newline-preserving on the real
     ShadowLedger.luau and finds no live GetAsync/SetAsync there (cure intact).
Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_31_tripwire_verify.py
"""
import importlib.util
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location("luau_lint", ROOT / "tools" / "luau_lint.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)

T56_POLL = """local function attach(player: Player)
	task.spawn(function()
		while player.Parent do
			marks.Value = player:GetAttribute("VirtueMarks") or 0
			rebirths.Value = player:GetAttribute("Rebirths") or 0
			local summitCount = 0
			for name in pairs(player:GetAttributes()) do
				if string.sub(name, 1, 7) == "Summit_" then summitCount += 1 end
			end
			summits.Value = summitCount
			task.wait(1)
		end
	end)
end
"""

T63_POLL = """task.spawn(function()
	while true do
		for _, pl in ipairs(Players:GetPlayers()) do
			for i = 1, 4 do
				local plantedAt = pl:GetAttribute(("Plot%d"):format(i))
				if plantedAt then refresh(pl, i, plantedAt) end
			end
		end
		task.wait(10)
	end
end)
"""

T74_RMW = """local function record(player: Player, room: string, line: string)
	task.spawn(function()
		local key = ("p%s_day%s"):format(player.UserId, os.date("!%Y%m%d"))
		local ok, rows = pcall(function()
			return store:GetAsync(key)
		end)
		if not ok then return end
		rows = (type(rows) == "table") and rows or {}
		table.insert(rows, { room = room, line = line })
		pcall(function()
			store:SetAsync(key, rows)
		end)
	end)
end
"""

CLEAN = """local function flushSoul(id: string, soul: Soul.Soul)
	local ok, err = pcall(function()
		soulStore:SetAsync(soulKey(id), serialize(soul))
	end)
	if not ok then warn(err) end
end

local function restoreSoul(id: string, soul: Soul.Soul)
	local ok, data = pcall(function()
		return soulStore:GetAsync(soulKey(id))
	end)
	if type(data) ~= "table" then return end
	return data
end

local hp = 5
wavePart.Touched:Connect(function(hit)
	local plr = Players:GetPlayerFromCharacter(hit.Parent)
	if plr and plr:GetAttribute("Abil_Redirect") == true then
		hp -= 1
	end
end)
while hp > 0 do
	task.wait(3)
	task.wait(2)
	hp -= 1
end
"""

COMMENTS_ONLY = """-- old poll: while player.Parent do GetAttribute("X") task.wait(1) end (t56 was here)
-- t74 receipt: this was GetAsync + SetAsync, a lost-update race
local s = "store:GetAsync(key) then store:SetAsync(key, rows) after task.wait(1)"
print(s)
"""

failures: list[str] = []


def run(src: str, name: str) -> list[str]:
    findings = lint.poll_disease_findings(lint.blank_comments_strings(src))
    findings += lint.rmw_disease_findings(lint.blank_comments_strings(src))
    return findings


def expect(name: str, cond: bool, detail: str) -> None:
    tag = "PASS" if cond else "FAIL"
    print(f"[{tag}] {name}: {detail}")
    if not cond:
        failures.append(name)


# 1-5 fixture expectations
f56 = run(T56_POLL, "t56")
expect("t56 poll trips", len(f56) == 1 and f56[0].startswith("poll disease (t56/t63)"), f56 or "no finding")
expect("t56 line number", f56 and "line 4" in f56[0], f56[0] if f56 else "")

f63 = run(T63_POLL, "t63")
expect("t63 poll trips", len(f63) == 1 and "task.wait(10s)" in f63[0], f63 or "no finding")
expect("t63 line number", f63 and "line 5" in f63[0], f63[0] if f63 else "")

f74 = run(T74_RMW, "t74")
expect("t74 RMW trips", len(f74) == 1 and f74[0].startswith("RMW disease (t74)"), f74 or "no finding")
expect("t74 lines 5+11", f74 and "line 5" in f74[0] and "line 11" in f74[0], f74[0] if f74 else "")

fclean = run(CLEAN, "clean")
expect("cured shapes clean", not fclean, fclean or "no findings")

fcomm = run(COMMENTS_ONLY, "comments")
expect("comments/strings blanked", not fcomm, fcomm or "no findings")

# real-tree spot checks
sl_path = ROOT / "roblox" / "src" / "server" / "ShadowLedger.luau"
sl_raw = sl_path.read_text(encoding="utf-8")
sl_blank = lint.blank_comments_strings(sl_raw)
expect("blank preserves length", len(sl_blank) == len(sl_raw), f"{len(sl_blank)} == {len(sl_raw)}")
expect("blank preserves newlines", sl_blank.count("\n") == sl_raw.count("\n"), f"{sl_blank.count(chr(10))}")
fsl = lint.rmw_disease_findings(sl_blank)
expect("ShadowLedger cure intact", not fsl, fsl or "no RMW finding (UpdateAsync only)")

ta_path = ROOT / "roblox" / "src" / "server" / "TheAnswerBoss.luau"
ta_blank = lint.blank_comments_strings(ta_path.read_text(encoding="utf-8"))
fta = lint.poll_disease_findings(ta_blank)
expect("TheAnswerBoss Touched reads not flagged", not fta, fta or "no poll finding")

print()
print("RESULT:", "ALL PASS" if not failures else f"FAILURES: {failures}")
raise SystemExit(1 if failures else 0)
