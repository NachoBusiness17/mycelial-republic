# BURN build-fold-verify 20260926 b (the owed t67/t63 grep pair)

## Verdict
steal

## Evidence
1. Charge (B2_10_playtest_prereg_20260926.md): the shipped rbxlx "provably lacks four landed fixes: t74 ShadowLedger UpdateAsync, t67 derived join, t63 garden signals, t72 GalleryZone annotations." B2-29 cleared t74/t72 only; LEDGER row build-fold-verify: "one grep pair owed before Sep-29".
2. Marker definitions located: t67.check.txt says the stale build "still bakes the old no-arg ZoneGate.init() and the authored literal (3 ZONE_REGION mentions)"; the fix bakes `zoneRegions[z.name] = z.region` (:72), `ZoneGate.init(zoneRegions)` (:74), WaveZone `region: string` (:42), leaving "zero ZONE_REGION code references in src (one comment citation ... init.server.luau:40)". t63.check.txt says the 10s poll was removed ("grep task.wait(10) over file: 0 matches") and replaced by `prompt.PromptButtonHoldBegan:Connect` (:385) and `GetAttributeChangedSignal(("Plot%d"))` (:388), with PromptButtonHoldBegan having "no prior usage" in src.
3. Greps on the shipped rbxlx (roblox/the_mountain.rbxlx, 383,204 bytes, mtime Sep 26 15:38, before this lane's rebuild): ZONE_REGION 1, "region: string" 2, "zoneRegions[z.name] = z.region" 1, "ZoneGate.init(zoneRegions)" 1, PromptButtonHoldBegan 2, GetAttributeChangedSignal 11, onPlotChanged 2, "task.wait(10)" 0. b2-29 baselines held: UpdateAsync 2, "GetAsync(key)" 0, "annotation exactness" 8.
4. Check script: `bash tools/mountain_check` printed "checked 43 files, 0 with findings", "parse-level failures: 0", "unique findings: 8" (all LocalUnused), "Built project to the_mountain.rbxlx", "== GATE PASS: the_mountain.rbxlx rebuilt ==". Re-grepped all 11 markers on the rebuilt bytes (383,431 bytes, mtime 17:18): identical counts, no regression.

## Steal or Vacuous
- t67 derived join: CLOSED on build bytes. Exactly 1 ZONE_REGION hit (the intentional t64 comment citation; the stale build baked 3 from the authored literal), the derive loop and single ZoneGate.init(zoneRegions) caller are present, and the required region field rides the WaveZone type.
- t63 garden signals: CLOSED on build bytes. The garden poll is absent (task.wait(10) = 0) and both replacement bindings are baked: PromptButtonHoldBegan 2 (its only two src occurrences) and GetAttributeChangedSignal with onPlotChanged.
- b2-10 red finding: fully closed. All four named fixes are grep-proven on build bytes; B2-29's t74/t72 counts reproduce exactly.
- mountain_check: GATE PASS. One delta vs b2-29: 8 findings now vs 9 then; the "1 external-type TypeError MudBasecamp(220,19)" b2-29 recorded is gone, consistent with src edits after 08:28 (shipped mtime was already 15:38 before this run, size then 383,204 vs b2-29's 383,204 byte claim, now 383,431 after rebuild).
- Residual unchanged from b2-29's own falsifier: t74 stays "NOT verified against a live DataStore"; playtest P3 owns that runtime check at Sep-29.

## Falsifier
none proposed

## Bibliography (closed)
watch/inbox/BURN_build-fold-verify_20260926.md · memory/burns/LEDGER.jsonl (rows b2-10, b2-29, build-fold-verify) · watch/inbox/burn_wave_20260926/{B2_10_playtest_prereg,B2_29_rbxlx_rebuild}_20260926.md · watch/inbox/gala_20260925/afterparty/lanes/{t63,t67}.check.txt · roblox/the_mountain.rbxlx (pre + post rebuild) · roblox/src/server/{MudBasecamp,init.server,ZoneGate}.luau · tools/mountain_check · roblox/docs/PLAYTEST.md
