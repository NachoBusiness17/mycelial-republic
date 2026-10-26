# B2-110 MudBasecamp wisp TypeError triage (2026-09-26)

## Verdict

LANDED via type narrow, not noise registration. The finding was real: the wisp chase loop declared `hum` from `FindFirstChild("HumanoidRootPart")`, which luau-lsp types `Instance?`, and then read `hum.Position` at (220,19), so every mountain_check run printed "Key 'Position' not found in external type 'Instance'" as a surviving TypeError while the gate (parse-only) passed. Fixed by casting the declaration to `BasePart?` (the file's own established pattern; line 431 casts `WaitForChild("Humanoid") :: Humanoid`), which narrows under the `if hum then` truthiness check and restores `Position` to a known key. The brief's alternative arm (register in the accepted-noise header) was rejected: Position on a HumanoidRootPart is a true invariant, so silencing it would have buried a class of real errors. Verified: single-file analyze shows zero (220,19) findings post-fix, full-tree analyze (src/shared src/server src/server/zones_extra src/client) shows parse_fails=0 and zero occurrences of 220,19, and the remaining MudBasecamp findings are all documented accepted-noise classes (number?/unknown on GetAttribute reads). Runtime behavior unchanged: the cast is compile-time only; the nil-check and chase math are byte-identical logic.

## Evidence

- roblox/src/server/MudBasecamp.luau:218 pre-fix `local hum = target.Character and target.Character:FindFirstChild("HumanoidRootPart")` typed Instance?, :220 `local dir = (hum.Position - wisp.Position)` the read that tripped
- Pre-fix reproduction, luau-lsp analyze single file: `MudBasecamp.luau [game/ServerScriptService/MudBasecamp](220,19): TypeError: Key 'Position' not found in external type 'Instance'` (measured 2026-09-26 this lane)
- Post-fix: roblox/src/server/MudBasecamp.luau:218-221 comment block + `local hum = target.Character and target.Character:FindFirstChild("HumanoidRootPart") :: BasePart?`; full-tree rerun parse_fails=0, grep -c '220,19' = 0
- tools/mountain_check:5-9 accepted-noise header (the classes the surviving findings fall into: "number | unknown"/"number?" on GetAttribute reads); tools/mountain_check noise-filter grep chain unchanged by this lane
- Existing in-file cast precedent: roblox/src/server/MudBasecamp.luau:431 `local hum = char:WaitForChild("Humanoid") :: Humanoid`

## Work done

Reproduced the finding with the repo's own analyzer before touching bytes (single-file analyze, finding text byte-matched the brief). Applied the type narrow with a cause-carrying comment naming the brief, the pre-fix line, and the error text. Re-ran the analyzer twice: single file (0 hits on 220,19) and the exact mountain_check full-tree invocation (parse_fails=0, 0 hits on 220,19). Checked the noise-header alternative and filed the rejection reason in Verdict. Receipt filed at watch/inbox/burn_wave_20260926/B2_110_mudbasecamp_wisp_20260926.md; LEDGER row appended via .venv/Scripts/python.exe json.dumps; queue row (sat pre-checked [x] with no receipt, the B2-238 disease) annotated with this landing note, the check now earned.

## Falsifier

From repo root: `cd roblox && ../tools/bin/luaulsp/luau-lsp.exe analyze --definitions="../tools/bin/globalTypes.d.luau" --sourcemap="sourcemap.json" src/shared src/server src/server/zones_extra src/client 2>&1 | grep -c "220,19"` must print 0; if it prints 1 or more, the cast was reverted or the sourcemap drifted and the finding is back. Conversely `grep -n "BasePart?" roblox/src/server/MudBasecamp.luau` must hit line 221; run `bash tools/mountain_check` and the string "MudBasecamp.luau(220" must not appear in the findings stream while the gate still exits 0. If a future edit removes the `if hum then` guard, the cast stops narrowing and the analyzer will fire again at that line: that is the tripwire working, not a regression of this fix.

## Bibliography closed

roblox/src/server/MudBasecamp.luau (read 200-240 and 425-435, edited 218-221); tools/mountain_check (read in full, unchanged, noise classes verified); tools/bin/luaulsp/luau-lsp.exe + tools/bin/globalTypes.d.luau + roblox/sourcemap.json (probe harness, unchanged); QUEUE.md B2-110 row (annotated); memory/burns/LEDGER.jsonl (appended).
