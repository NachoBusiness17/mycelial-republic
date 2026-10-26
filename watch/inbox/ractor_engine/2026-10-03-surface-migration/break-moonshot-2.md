# BREAK PASS: moonshot-2 (surface migration lens), hostile second pass

Filed 2026-10-03 by break-moonshot-2. Moment: driver.beat read cycle=1678 at 2026-10-03T20:32:58Z;
usage.jsonl pinned at 1,236 rows / $64.29; attention.md pinned at 1,178 lines. The estate was live
under this pass; ledgers moved between the lens's reads and mine, so counts are named per moment
(census denominator law). No em-dash bytes. Every claim below was executed or read this sitting.

## VERDICTS

### F1 "The migration's central scoreboard does not exist in bytes" - CONFIRMED

Re-ran every cite, all byte-exact:
- `./.venv/Scripts/python.exe -c "import json; reg=json.load(open('watch/inbox/frontier_delta_register_20261003.json'))"`: 14 rows; key set exactly {contract_parts, flash_chars, flash_cites, flash_unver, frontier_chars, frontier_cites, frontier_unver, id}. No verdict, no cost, no deepseek arm, no win rate. Sample ids: BARFIGHT_spec, DND_module, WIRE_PLAN.
- queue/STANDING_RAILS.md:49-50 verbatim: "The Delta Register judge pass completes (30/50 lanes landed, ~20 killed by the interrupt before the no-cancel law landed; re-fire cheap on GO)."
- `ls watch/inbox/replay_flash | wc -l` = 13. 13 x 582K = 7.57M, so the ask's 9.5M seat-token figure stays OWED.
- configs/providers.yaml:150-168 nous lane models = z-ai/glm-5.3-prime, qwen/qwen3.8-max-prime, fireworks/ember-1 (lines 159-162). No GLM-5.3-max. configs/off_hours.yaml:71 `id: overnight-5.3-max, provider: z_ai, model: glm-5.3`, and the file's own lines 68-69 disclaim it: "a routing hint, not a cost claim. Change it if '5.3 max' means a different provider/model."
- Absence check (instrument and scope named): `grep -l "39 judged|39-lane|8-5 on" watch/inbox/*.md` (top-level inbox md files only) = zero hits. No receipt reproduces the 39-lane/8-5 census in that scope; deeper inbox subdirs not swept.

Sharpening the lens missed: watch/inbox/mag_rails_plugin_spec_20261003.md tool 4 (mag_delta_register) promises "the register rows (three-arm scores, win rates, the frontier-only class)" - fields that exist in no register byte. The scoreboard gap is load-bearing for the plugin surface too, not just the migration verdict.

Nuance the lens overstated: "the model the thesis names is not on the lane it names" is a naming ambiguity the repo itself flags (off_hours.yaml:68-69), not proof the thesis points at a nonexistent model; glm-5.3-prime is the plausible referent. Does not rescue the scoreboard.

### F2 "The estate already built and proved the headless loop; promote it instead of a fifth executor" - CONFIRMED (strengthened)

- tools/overmind_loop.py docstring lines 1-22 verbatim: $1 hard cap (line 5), the ONE glm-flash loop-hour falsifier (lines 4-5), SENSE->DECIDE->GATE (fail-closed verb table)->EXECUTE->VERIFY->LEDGER hash-chained append (lines 11-17).
- memory/runs/overmind/ledger.jsonl parsed: 45 rows; verbs 35 STAGE_ASK + 10 NOOP; cumulative_usd 0.0072; first ts 2026-10-02T00:58:17Z, last ts 2026-10-02T01:58:35Z (exactly the one-hour falsifier window, then dark; nothing since).
- LIVE CHECK the lens did not run: `./.venv/Scripts/python.exe tools/overmind_loop.py verify` returned `{"ok": true, "rows": 45}`. The chain seal is execution-verified, not docstring-claimed.
- Rivals real: scripts/descent_driver.sh:32 writes the beat; `tail memory/runs/hermes_burn/driver.beat` = cycle 1676 at 2026-10-03T19:30:08Z (byte-exact vs the lens) and now 1678 at 20:32:58Z (still alive). mag/afk_orchestrator.py and mag/desk_orchestrator.py exist (ls). Arena automation in-repo: watch/inbox/parable_day_one_20261003.md:9 "the hourly arena cron, 8 cycles, automation-b1ce1342" (matches the ask's 8 cycles byte-for-byte).
- New facts for the move: `grep -rln overmind scripts/` = only an unrelated tmp pilot file, so no scheduled task registers the loop today; and tools/model_garden.py:172-176 shows the DECIDE ask rides model_garden's own urllib door, not mag.route_chat. The lens's 90-minute move is actually two migrations (repoint the door, register the cron) plus the 24h falsifier.

### F3 "The alarm channel is 71 percent false alarms from the tavern run-id drop" - CONFIRMED (figures moved; one correction to the falsifier)

- My moment: `grep -c 'INSTANCE-GUARD doubled-key' memory/attention.md` = 850; `wc -l < memory/attention.md` = 1,178; 72.2 percent. Lens moment: 809 / 1,137 = 71.1 percent. Same shape, file live (+41 alarm lines between reads).
- Mechanism byte-verified: tools/tavern.py:157 emits `f"TAVERN_r{rnd}_{p['name']}"` while docstring line 10 promises `TAVERN_<run>_r<round>_<actor>`. The dungeon twin verified too: tools/dungeon.py:197 `f"DND0_beat{self.turn}_dm"`, :271 `f"DND0_beat{self.turn}_{actor}"`, :320 hardcoded `"DND0_S0_dm"` - all run-invariant.
- Distribution parse of the 850 alarm lines: 88 distinct ids, every one alarmed 14-17 times, every turn=1; groups split ~TAVERN r{round}_{actor} pairs and DND0 beat ids. Consistent with the hourly cron (STANDING_RAILS.md:32) re-colliding on unchanged tags each hour.
- The receipt the lens cited reads verbatim: watch/inbox/dd_dogfood/hermes-economics.md:96-104 names the defect, "809 of 1,150 ledger rows carry doubled_key: true and 809 false INSTANCE-GUARD alarms", and the ingest tripwire at tools/instance_guard.py:191.
- Alarm writer verified: tools/instance_guard.py:191-209 (doubled_key_check writes the attention.md line; docstring lines 194-195 call attention.md "the estate alarm surface (the FTS-law channel)"). The lens's "only alarm channel" phrasing is the organ's own claim; I did not census other channels (logs/, per-run receipts exist), so that word stays attributed, not proven.
- Correction: the lens's falsifier ("fix the tag at tavern.py:157... if alarms still fire, diagnosis wrong") is half-blind: fixing only tavern.py leaves the DND0 family, roughly 30 percent of the alarms by my id-group parse, still firing. The fix must cover both tag sites, which the move's second clause already names.

### F4 "The meters invert the migration thesis" - CONFIRMED with a dropped condition (finding text received truncated; evidence block fully checked)

- Per-id figures byte-exact: BARFIGHT_spec 37,475 tok / $0.59; THE_ROOM_REMEMBERS 71,015 tok / $0.78; PARTYCHAT_spec 71,671 tok / $0.69 (prompt+completion re-summed from memory/runs/hermes_burn/usage.jsonl).
- Moving-ledger deltas: my re-sum 1,236 rows / $64.29 lifetime / 10-03 $25.35 vs the lens's 1,152 / $64.05 / $25.11. Day splits 10-01 $37.76 and 10-02 $1.17 identical. +84 rows / +$0.24 landed between the two reads (the play hour was firing: 995 rows today).
- Waste split exact at watch/inbox/dd_dogfood/hermes-economics.md:13-22: $25.9998 of $63.5824 = 40.9 percent; $0.4929 gross / $0.2913 productive per usable finding (129 units).
- watch/inbox/burn_claims_50wide_20261003.md:40 verbatim: "Cost: ~1.5M subagent tokens, $0 cash (seat tier)."
- The lens's "arena memory note" cite resolves to hermes-economics.md:28: 10-03 $24.6494 (909 rows, the ARENA DAY playground arc).
- DROPPED CONDITION the verdict must carry: the 40.9 percent is LIFETIME and dominated by the A1 stale-force-flag hole ($21.0932, 81 percent of waste) that CARRIER-PATCH 1 already closed; "post-patch days (10-02, 10-03) show zero non-playground re-fire waste" (hermes-economics.md:110-111), and the playground collision repeats (665 fires / $14.9034) were explicitly ruled PRODUCTIVE spend, "ledger-blind" not waste (hermes-economics.md:59-64). Reading 40.9 percent as the Nous lane's standing waste rate overstates present burn by design; the standing defect on this ledger is integrity (the tag collision), a one-line fix, not cash. The honest productive baseline the migration economics should use is $0.29 per usable finding.
- Seat-side metering: confirmed absent in the lens's scope plus mine. `grep -rln "seat_tokens|window_tokens|seat window"` over tools/, memory/runs/, watch/inbox/ returned no z.ai seat-window ledger (hits were unrelated: compaction_eval, ghost, mickey17 files). The 9.5M figure stays OWED and unmeterable until seat tokens bank at landing.

### Blind spots - all stand; two upgraded

1. No provider-side probe this pass either; $220 armed remains prose. Stands.
2. The 9.5M OWED is now verified-absent-with-scope (see F4). Upgraded.
3. No opencode source read by the lens or by me; the second-unobserved-key-process claim stays inference-from-shape. Stands.
4. The 39/8-5 headline verified unreceipted in top-level watch/inbox/*.md (scope named in F1). Stands, slightly strengthened.
5. No pytest or gate run this pass; instruments were python parses, greps, one live verify (overmind), file reads. Stands.

## ADDITIONS (what the lens missed)

A1 (CONVERGENT with the same-day hermes-economics lane): the waste figure the migration economics consumes is lifetime, patch-dominated, and partially ruled productive. Evidence: watch/inbox/dd_dogfood/hermes-economics.md:41-45 (A1 $21.0932, 81 percent), :110-111 (post-patch zero non-playground re-fire waste), :59-64 (collision repeats productive). Falsifier: a fresh parse showing non-playground re-fire waste on post-patch days kills the "closed" reading. Move: 10 min, carry the three conditions into register v2 before the migration verdict eats the number.

A2: the plugin spec promises a scoreboard the register cannot serve. Evidence: watch/inbox/mag_rails_plugin_spec_20261003.md tool 4 vs the register parse (14 rows, 8 metric keys, no verdict/cost/deepseek). Falsifier: any register row carrying a verdict column today (none in this parse). Move: 30 min, mint register v2 (verdict + cost_usd + deepseek arm) before shipping mag_delta_register; one artifact feeds both the migration verdict and the native handle.

A3: the loop the lens wants promoted has no runner and a bespoke door. Evidence: `grep -rln overmind scripts/` = no task registration; tools/model_garden.py:172-176 urllib self-call vs the rails front door (queue/STANDING_RAILS.md:10-12). Falsifier: a scheduled task or cron entry for overmind_loop outside scripts/ kills it. Move: 45 min, register a MagOvermindDaily-shaped task (pattern: scripts/register_fts_index_task.ps1) with the DECIDE door repointed through route_chat, then start the 24h falsifier.

A4: seat-window tokens are unmetered anywhere in-repo, so the seat arm of the economics can never settle. Evidence: scoped grep named in F4; watch/inbox/burn_claims_50wide_20261003.md:40 banks cost only ($0 cash), never tokens. Falsifier: a repo ledger carrying z.ai seat window tokens per deliverable kills it. Move: 20 min, add a seat_tokens field to the flash-arm landing receipts so the next economics pass can difference the arms.

A5: the scoreboard gap and the alarm flood share one root cause the lens priced separately. Evidence: queue/STANDING_RAILS.md:17-18 (law 3, interrupts never cancel) plus :49-50 (the ~20 judge lanes died before the law landed) plus the 850-alarm parse (both wolf families are re-fire/collision artifacts of headless-unaware tagging). Falsifier: re-fire the judge lanes background-executed per law 3; if any lane still dies to an interrupt, the law's coverage is wrong. Move: fold into the F1 move: re-fire the ~20 lanes through the rails' background rule (Task agents or the descent driver), not the interactive seat, so the re-run is itself the migration's first dogfood. Cost: inside the lens's 45-minute estimate.

## OWED (asserted, not verified by this pass)

- The nul-file trap: the ask names it; my scoped greps (tools/, docs/, watch/inbox/, queue/ for nul.file|nul trap|NUL file) found only tools/violation_ratchet.py:19 "sha256(rule NUL file NUL detail)", which is a fingerprint separator, not the trap. Bytes not located; left OWED.
- The $220 armed balance, the opencode source, the 39-lane/8-5 census, the 9.5M seat-token total: all unprobed or unreceipted here; OWED per the lens's own blind spots, now with the absence scopes named above.
- No pytest run, no citation_lint run, no ratchet run this sitting.
