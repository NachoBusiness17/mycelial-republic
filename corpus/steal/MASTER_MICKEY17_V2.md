# MICKEY-17 v2.1 MASTER FOLD (run-0, fire 4)

- folded_at: 2026-10-11T03:29:41Z (fold script sha256 58bd72c79c6d, FOLD_SECTIONS.md in this run dir)
- lane archive: memory/runs/mickey17_v2/runs/run-0/lanes (15 lanes, 162 rows; estate greps and negative findings live in each lane file)
- copies: corpus/steal/MASTER_MICKEY17_V2.md (estate) and the identical workspace copy under the mickey17_v2 workspace dir (both surfaces held the identical fire-3 fold at fold start; this fold rewrites both in the same pass)
- sections marked script-verbatim are sliced from FOLD_SECTIONS.md; seat prose surrounds them. Every steal sentence carries lane id + row index. Numbers computed by this fold's builder are labeled fold-computed; everything else is scripted or lane-cited.
- supersession: this fold rewrites the 2026-10-10T21:58:49Z fire-3 fold (which rewrote the 02:55 fold) in place on both surfaces. The lane rows are unchanged since fire 3 (162 rows, same scoreboard); what moved is the verifier layer: deep_tier2 verdicts grew 17 -> 29 (gate-repairer row-key repairs at 23:0x-23:2xZ, persisted in the lane .checks.json files), adding 1 same-chain-verified verdict, 1 more unconfirmed verdict (same row, re-keyed), and the R92/R94 register-row attribution correction now folded into DISPUTED D3. Banked lane rows are preserved verbatim in the lane files; nothing here removes a lane's own bytes.

## CASUALTY HEADER (script-verbatim)

## CASUALTY HEADER

- fired: 15
- landed (parseable files): 15
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.


## SCOREBOARD (script-verbatim)

## SCOREBOARD (recount)

- rows: 162
- estate_status: confirms-ours 67, new 47, we-have-better 29, owed 19
- leverage: high 80, medium 75, low 7


## FIDELITY (script-verbatim)

## FIDELITY

- rows with all of quote/source/steal/estate_status non-empty: 159/162 (98.1%)


## VERIFIER TABLE (script-verbatim)

## VERIFIER TABLE (persisted verdicts)

- lanes with persisted checks: 15
- verdicts: checks 5 (supports split: no 2, yes 3), deep_tier2 29 (verdict split: same-chain-verified 1, unconfirmed 2, verified 26), rows 5 (supports split: no 3, yes 2), supports 54 (supports split: no 53, yes 1)
- deep_tier2 join: 8/29 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 21


## WIDTH-ECONOMICS (script-verbatim)

## WIDTH-ECONOMICS

- rows/lane: median 11, max 18, min 5
- top-10 lanes share: 84.6%
- exact cross-lane duplicate quotes (normalized): 3
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)


## PRISMA FLOW (script-verbatim)

## PRISMA FLOW

- identified: 162
- screened: 162 (all rows carry the six rubric fields or their gap notes)
- excluded: 9 verifier-unconfirmed (deep_tier2): 1
- included: 161
- invariant: identified == included + excluded **HOLDS** (162 = 161 + 1)


## TOP-K SELECTION (script-verbatim rule and truncated entry list)

## TOP-K (script-computed; a lane-claimed top steal outside this list files as DISPUTED)

- [high] a01-arena-cadence#0: the arena cap is $25 per the automation's own title and step-1 prompt; the parable's '$25.11 cap' misnames the
- [high] a01-arena-cadence#1: '8 cycles' is byte-true as the fire count at parable-filing time (8 of 9 scheduled fires had fired) but the re
- [high] a01-arena-cadence#2: every session did not bank: 8 of 41 dirs have no gwap_banked and no ledger rows (dnd0 143335, 143639, 162136,
- [high] a01-arena-cadence#5: the audit's 'did every session bank' answer is moment-dependent and the tree was moving under the audit: at th
- [high] a01-arena-cadence#6: the parable cites a ledger that matches no file on disk: 'the arena-sessions-v3 ledger (266 rows, chain ok)' -
- [high] a01-arena-cadence#7: the cap held only for the cron lane and only from 21:00z: the day crossed $25 at 19:33:24.686865z (cumulative
- [high] a01-arena-cadence#9: the cap did not hold on either full arena day: day-04 crossed $25 at 22:06:53z and closed $26.2921 ($1.29 over
- [high] a01-arena-cadence#13: flight-3 confirmation, fresh instruments: the ask's two questions now have register-closed answers, re-execute
- [high] a02-dungeon-campaign#0: parser collapse decided the verdict: strip_and_cap (dungeon.py:102-107) flattens every speech to one line and
- [high] a02-dungeon-campaign#1: phantom regrowth is spec'd but never enforced: the campaign enemy branch (dungeon.py:439-468 current bytes) co
- [high] a02-dungeon-campaign#3: new: the dm channel was dead for the whole campaign and nobody banked it. the content_filter void path (dungeo
- [high] a02-dungeon-campaign#4: partial is earned by the letter and not in substance: deterministic and reproducible (root_anchors 0/3, party

## URL LIVENESS (script-verbatim)

## URL LIVENESS (scripted at fold time)

- unique URLs: 6; fetched: 6; skipped non-public: 0; live: 4; dead/blocked-status: 2
  - HTTP -1: https://api-docs.deepseek.com/api/create-chat-completion (fetched via WebFetch, byte-checked via cur
  - HTTP 404: https://x.com/yifanzhang_/status/2101068650161807857

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.


## TOP STEALS (the script's TOP-K, 12 rows; quotes and actions in full from the lane rows)

A lane-claimed top steal outside this list files as DISPUTED [script-verbatim rule]. Selection and order are the script's; the text is the lanes' own claims, quotes, and actions.

### T1. a01-arena-cadence#0 (high | new)
FINDING: The arena cap is $25 per the automation's own title and step-1 prompt; the parable's '$25.11 cap' misnames the 20:00Z meter reading ($25.1134, my recomputation from usage.jsonl) as the cap.
QUOTE: "Hourly arena cycle: dungeon + tavern + gwap bank, $25 daily cap"
ACTION (one seat, one sitting): amend the automation prompt so step 1 gates on arena-family ids only (TAVERN/DND0/CAMP) instead of the whole-day sum, then file a one-line parable erratum naming $25 as the cap and $25.11 as the 20:00Z reading. [a01-arena-cadence#0]

### T2. a01-arena-cadence#1 (high | confirms-ours)
FINDING: '8 cycles' is byte-true as the fire count at parable-filing time (8 of 9 scheduled fires had fired) but the receipt hides that the first fire failed and that the 20:00Z fire ran three dungeon sessions at 20:21-20:23Z AFTER the day crossed $25 at 19:33:24Z; the 21:00Z fire shows succeeded with zero session activity, consistent with the cap gate finally stopping it.
QUOTE: "the hourly arena cron, 8 cycles, automation-b1ce1342"
ACTION (one seat, one sitting): fold the automation_runs sqlite census (fire times, outcomes) into the dawn compiler status feed and the parable erratum so cadence receipts carry failure rows, not just counts. [a01-arena-cadence#1]

### T3. a01-arena-cadence#2 (high | new)
FINDING: Every session did NOT bank: 8 of 41 dirs have no GWAP_BANKED and no ledger rows (dnd0 143335, 143639, 162136, 185933, 202147, 202158, 202213; tavern 162257), the 16:00Z fire banked nothing at all, and the 3 dirs without DONE (the 12:18-12:21Z manual burst) are banked anyway; the 'two newest unbanked' catch-up rule structurally starves backlog dirs because each fire mints 2 fresh unbanked ones.
QUOTE: ""verdict": "PARTIAL: the Wyrm unanchored - the season continues", "spend_usd": 0.2399"
ACTION (one seat, one sitting): run .venv/Scripts/python.exe tools/arena_gwap.py over the 8 unbanked dirs oldest-first (order flag or explicit list, not 'two newest'), landing markers plus arena-capability.jsonl rows and a one-line backlog receipt in watch/inbox/. [a01-arena-cadence#2]

### T4. a01-arena-cadence#5 (high | new)
FINDING: The audit's 'did every session bank' answer is moment-dependent and the tree was moving under the audit: at the parable's filing and at my 03:04Z census the answer was NO (16-17 of ~48-51 dirs unbanked, ledger zero-rows at hours 16/20/21/22/23), but a backfill drained the entire backlog between 03:04Z and 03:26:51Z so that at the final read every one of 53 session dirs carries GWAP_BANKED AND matching ledger rows (88 rows banked at hour 03), meaning the banking claim is only honest with a moment stamp.
QUOTE: ""ts_utc":"2026-10-04T03:26:51Z""
ACTION (one seat, one sitting): add a banked_at moment column to the dawn report's gwap line (rows, sessions, AS-OF timestamp) and a receipts note crediting the backfill run (tools/arena_gwap.py --backfill is the only flag that matches the 88-row hour-03 drain, but no receipt names it - attribution is unproven), landing in watch/inbox/. [a01-arena-cadence#5]

### T5. a01-arena-cadence#6 (high | new)
FINDING: The parable cites a ledger that matches no file on disk: 'the arena-sessions-v3 ledger (266 rows, chain ok)' - arena-sessions.jsonl holds 60 rows frozen at 12:52:58Z, arena-capability.jsonl held 314 at filing, and the name 'arena-sessions-v3' appears nowhere in code or any other receipt; the 266 figure is best explained as the capability ledger's post-hour-14 moment (121+145) stapled to a wrong ledger name, a phantom-citation class defect (GAP_REGISTER rank 3) in a receipt that is itself about honesty.
QUOTE: "the arena-sessions-v3 ledger (266 rows, chain ok), verkle-anchored, the golden vectors reproducing"
ACTION (one seat, one sitting): one-line parable erratum correcting the ledger citation to arena-capability.jsonl with the filing-moment count (314) and adding arena-sessions.jsonl (60 rows, the 12:51Z bar-fight, frozen) as its own named artifact. [a01-arena-cadence#6]

### T6. a01-arena-cadence#7 (high | new)
FINDING: The cap held only for the cron lane and only from 21:00Z: the day crossed $25 at 19:33:24.686865Z (cumulative $25.1134 on a GALA prime-judgment row), the 20:00Z fire still ran three dungeon sessions post-crossing whose bank then never ran that night (hour-20/21/22/23 ledger buckets empty until the backfill), manual dungeon play continued 22:50-22:56Z, and the day closed at $25.6218 - $0.62 OVER the $25 cap; day 04 opened clean ($1.2509 by 03:3xZ) and the 02:21-02:28Z pair banked outside any fire window (02:00Z fire closed 02:03:11Z), so the bank step is not fire-atomic.
QUOTE: "{"ts": "2026-10-03T19:33:24.686865Z", "id": "GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003_STAGE_B", "model": "z-ai/glm-5.3-prime""
ACTION (one seat, one sitting): make the automation's bank step run AFTER play within the same fire (or have the tavern carrier invoke arena_gwap bank at exit) so a fire's own sessions can never outlive their bank overnight, then dogfood one fire and check the ledger's hour bucket. [a01-arena-cadence#7]

### T7. a01-arena-cadence#9 (high | new)
FINDING: The cap did NOT hold on either full arena day: day-04 crossed $25 at 22:06:53Z and closed $26.2921 ($1.29 over), the crossing landing mid-fire of the 22:00Z fire that started at $24.4905 with $0.51 headroom; the 23:00Z and 00:00Z fires then minted nothing (the gate's only true stops), while non-arena lanes (THE/REPRINT) spent $1.22 after the crossing because only the arena lane gated; the lag-by-one-fire is structural (gate reads at fire start, crossing happens during the fire), so only the automation's deletion ended overspend - day-05 spent $3.76 total and the meter has been near-dark since 10-07.
QUOTE: "2026-10-04 cross: ('2026-10-04T22:06:53.865221Z', 25.0074) final_cum: 26.2921"
ACTION (one seat, one sitting): append a day-04 section to PARABLE_ERRATUM_20261004.md (crossed 22:06:53Z, closed $26.2921, four scaffold-only succeeded fires 18:00-21:00Z, 23:00Z+00:00Z fires minted nothing, deletion not gate ended the overspend) so the erratum covers the cadence's full life, not day one. [a01-arena-cadence#9]

### T8. a01-arena-cadence#13 (high | confirms-ours)
FINDING: Flight-3 confirmation, fresh instruments: the ask's two questions now have register-closed answers, re-executed by me at 2026-10-10T20:3xZ - every real session banked (110/110 transcript-bearing dirs, chain 0 breaks, ledger frozen at 730 rows since 2026-10-05T07:12:43Z) and the cap NEVER held on any full arena day (day-03 closed $25.6218, day-04 $26.2921, day-05 burned $3.7616 more after the day-key reset; deletion, not the gate, ended the overspend).
QUOTE: "Second over-cap close in two days (day-03 $25.6218, section 4)."
ACTION (one seat, one sitting): mint corpus/steal/ARENA_CAP_NEVER_HELD_20261010.md as a standalone steal card (the day-keyed whole-account gate is structurally lag-by-one-fire; a recreated arena cron must load the arena-family gate banked in erratum section 7) - corpus/steal still carries this lane only inside MASTER_MICKEY17_V2.md (grep 1 file), so the law has no card of its own. [a01-arena-cadence#13]

### T9. a02-dungeon-campaign#0 (high | confirms-ours)
FINDING: Parser collapse decided the verdict: strip_and_cap (dungeon.py:102-107) flattens every speech to one line and the tag scan (dungeon.py:488-491) reads only line-initial bracket lines, so the 14 logged S4 PC speeches all parse tagless and the S4 disjunct at dungeon.py:496 (Python precedence makes the wyrm test independent of verb) resolves every one as a wyrm ATTACK; my replay of all 14 speeches through the current HEAD bytes reproduces 14/14 logged verdicts and reaches the AUDIT branch 0 times, so all [AUDIT root] win checks were structurally unreachable as played. Folded as master 6.4 / N7 / GO item 2; line anchor updated from the prior 485 to 496 on the clean tree.
QUOTE: "if verb == "ATTACK" and obj in enemy["actor"] or (scene == "S4" and obj == "wyrm"):"
ACTION (one seat, one sitting): execute master GO item 2 as written, regex tag search across the capped speech or opening-tag-only grading in tools/dungeon.py, plus tests/test_dungeon_parser.py replaying the 14 logged S4 verdicts as fixtures. [a02-dungeon-campaign#0]

### T10. a02-dungeon-campaign#1 (high | confirms-ours)
FINDING: Phantom Regrowth is spec'd but never enforced: the campaign enemy branch (dungeon.py:439-468 current bytes) contains no per-turn heal and the only ehp mutation is the damage clamp at dungeon.py:499, and the scroll-audit reveal is case-dead because obj is lowercased at dungeon.py:494 while the carried keys are mixed-case, so the membership test at dungeon.py:515 ('vault deed b' in carried -> False, executed) can never burn a phantom. Commit a7d7d313d claims 'regrowth 5/scroll' anyway (a phantom figure, N5-registered in the master), and the DM narrated the heal at transcript row 45 that the state machine never applied. The Wyrm therefore died at turn 8 on 30 HP that the spec's Wyrm would have kept regrowing.
QUOTE: "At the start of each Wyrm turn, it heals 5 per PHANTOM scroll still unaudited in any pack."
ACTION (one seat, one sitting): implement the per-turn heal keyed to the unaudited PHANTOM count plus the audit-burn, case-fold the carried lookup at dungeon.py:515, and land the two-line erratum on commit a7d7d313d in the run receipt at watch/inbox/playground/. [a02-dungeon-campaign#1]

### T11. a02-dungeon-campaign#3 (high | new)
FINDING: NEW: the DM channel was dead for the whole campaign and nobody banked it. The content_filter void path (dungeon.py:183-193) replaced the dm_response on 40 of 50 transcript rows including all 39 PC-beat readbacks (only the S0 omen and 4 of 5 monster beats got narration), so the module's read-back loop (the DM must open with the verdict tag, DND_module.md:138) never reached a single PC; the seats responded by self-rolling d20s inside their speeches, which the carrier then discarded. Zero hits for 'content_filter' in MASTER_MICKEY17_V2.md, ARENA_V2_DESIGN_20261004.md, and DND_module.md against 40 in the run transcript. This is also the mechanism behind the folded a02#3 finding: my dice_audit rerun (extracted from the spec, genesis tips x50) exits 1 with verdict flags on all 50 rows and preimage/roll/turn flags on the 5 ledger rows, correcting the folded 45-and-4 counts; per the module's own falsifier the session is VOID from the first bad row, not a clean PARTIAL.
QUOTE: "content = ""  # a filtered generation is void regardless of bytes"
ACTION (one seat, one sitting): bank finish_reason per call and count voided readbacks in the run's DONE, retry the DM call on a de-globged prompt (it quotes the actor's combat speech verbatim), and file the void-census in the run 202213Z receipt; land in tools/dungeon.py _paid plus the ARENA_V2 design's substance-gate leg. [a02-dungeon-campaign#3]

### T12. a02-dungeon-campaign#4 (high | confirms-ours)
FINDING: PARTIAL is earned by the letter and not in substance: deterministic and reproducible (root_anchors 0/3, party alive with chatgpt lowest at 6 HP, Wyrm down at turn 8 on cumulative 39 damage of 30 HP, 95 total S4 PC damage), but the win path was unreachable by construction (row 1) and the label rides a VOID session (row 4). Corrected counts now in the row: 5 explicit [AUDIT root] request beats / 6 tag occurrences in S4 speeches, and the saelis cross-audit quote reads 'aren't on the ledger' verbatim, not 'are not'. Spend claim reconciled by my own ledger split: exactly 84 usage rows fall in the run window 20:22:13-20:30:14Z, which is the exact call count the code implies (39 PC beats x 2 + 5 monster beats + 1 S0), summing $0.2400 vs DONE's $0.2399 (per-row 4-decimal bank rounding), with zero rows stamped dnd0_20261003T202213Z because the tag law landed post-run in f017a479a. Emergent keeper stands: the seats cross-audited each other's self-rolled numbers in-world, trust-bytes-not-reports under a dead referee. ARENA_V2_DESIGN_20261004.md:36-38 now seeds the v2 season on this verdict.
QUOTE: "PARTIAL: the Wyrm unanchored - the season continues"
ACTION (one seat, one sitting): file the carrier-failure erratum receipt for run 202213Z at watch/inbox/playground/ (verdict PARTIAL stands, mechanics off-spec, audit VOID, DM channel 40/50 voided), and carry the in-world cross-audit behavior forward as a named party mechanic in the module revision. [a02-dungeon-campaign#4]

## DISPUTED TIER (contradiction pairs, both quotes, conditional rulings)

Eight entries. D0 is the run's tier-2 unconfirmed verdict set (the PRISMA exclusion). D1-D7 are contradiction pairs from the lane rows; each carries both quotes and a conditional ruling, ruled with conditions rather than averaged.

### D0. TIER-2 UNCONFIRMED (the PRISMA exclusion): a07-fifty-wide-waves#1
PAIR: lane claim vs its own cited source.
CLAIM EXCERPT: "TALLY GAP re-verified across three asks and CURED IN CODE: extraction holds 60 distinct units over 16 filings vs 50 tallied verdicts (30+11+3+6, internally consistent), and refire 2's live guard run (tools/fifty_wide_guard.py, exit 1 naming exactly the 10 dropped keys) reproduced the drop; the drop mechanism itself remains unknown (D1 stands), no dispatch_log.jsonl exists on disk, and no wave has ..."
QUOTE (the cited source, byte-true): "flash lanes, each byte-checking one claim from 16 BURN_* filings."
VERIFIER: deep_tier2 verdict UNCONFIRMED, twice. The verifier table's 2 unconfirmed verdicts both sit on this one row under its pre-repair and post-repair row_keys (the 23:27Z gate-repairer re-keying in a07-fifty-wide-waves.checks.json, read this fold: verdict and evidence bytes unchanged, only the join keys moved). The cited receipt carries the 16-filing/50-verdict tally (30/11/3/6, internally consistent) and none of the claim's mechanics: no 60-unit extraction, no guard live-run, no drop mechanism, no pre-flight absence.
RULING (conditional): the row stays excluded from the included set (PRISMA holds 162 = 161 + 1) until one real fifty-wide wave pre-flights tools/fifty_wide_guard.py and banks the first complete replay pair (dispatch_log row + agents dir). The verified half stands: the guard and archive tools are on disk and the asserted-equality steal is LANDED; the operator-owed back half is the standing action. [a07-fifty-wide-waves#1]

### D1. MOMENT PAIR: a01-arena-cadence#2 vs a01-arena-cadence#13
SIDE A (2026-10-03T21:55Z read) CLAIM EXCERPT: "8 of 41 dirs have no gwap_banked and no ledger rows (dnd0 143335, 143639, 162136, 185933, 202147, 202158, 202213; tavern 162257)"
SIDE A QUOTE: ""verdict": "PARTIAL: the Wyrm unanchored - the season continues", "spend_usd": 0.2399"
SIDE B (2026-10-10T20:3xZ re-execution) CLAIM EXCERPT: "every real session banked (110/110 transcript-bearing dirs, chain 0 breaks, ledger frozen at 730 rows since 2026-10-05T07:12:43Z)"
SIDE B QUOTE: "Second over-cap close in two days (day-03 $25.6218, section 4)."
RULING (conditional on moment): both sides are byte-true at their own moments; tier-2 re-executed side B's numbers fresh (usage.jsonl per-day sums, the 730-row chain walk, the --status census) and they reproduce. A backfill drained the entire unbanked backlog between 03:04Z and 03:26:51Z on 2026-10-04, the drain visible in the ledger's own timestamp: QUOTE: ""ts_utc":"2026-10-04T03:26:51Z"" [a01-arena-cadence#5]. Under the moment law the banking claim is only honest with a moment stamp; a count without one is stale on arrival. No contradiction survives the stamp; the cure is the banked_at-column action on a01-arena-cadence#5.

### D2. LAW-BYTES PAIR: owning docstring vs code condition (a06-sacred-cow#0)
SIDE A (the doc claim) QUOTE: "depth=mechanical sends thinking:{type:disabled} UNCONDITIONALLY, regardless of the lane's disable_thinking flag"
SIDE B (the code bytes, read by this fold at mag/route_chat.py:148-151): "if depth == \"mechanical\": if not _thinking_forbidden(model): body_obj[\"thinking\"] = {\"type\": \"disabled\"}" - the disabled key is gated on the model, not sent unconditionally; the qwen-flash recipe (mag/inference_budget.py:191-192) carries "thinking" in forbidden_keys, so qwen-class models get omission (the measured-ON state) instead of disabled. The carve-out is lawful and documented (LAND_d3_wire.md:20-22) and pinned by tests/test_route_chat_depth.py:134-138.
RULING: the code condition wins; the doc claim is scoped-false. The unconditioned form lives in five places against the code's condition (wire_thinking docstring 137-139, route_chat docstring 180-183, pass-3 row fbfbb31c40ad, GAP_REGISTER R95, GAP_REGISTER line 587) and grep shows no doc flags the drift [a06-sacred-cow#0]. Cure: GO item 6 (the a15-rollup#2 sitting, carrying this row's carve-out wording).

### D3. REGISTER-INTERNAL PAIR: GAP_REGISTER R92/R94 vs R96 (a06-sacred-cow#1)
SIDE A (the law form, register line 472 under header R94; R92's FILL repeats it in its supersession bracket at line 463) QUOTE: "the SACRED COW FELL commit (53f56d0f3) landed BEFORE the refire and re-scoped that law (thinking-on design asks deliver 2-3x complete outputs)"
SIDE B (R96, the scoping form, register line 481, tier-2 byte-read): "The 2-3x headline also remains unjudged: memory/runs/ds_batches/delta_judge_results.jsonl mtime is still Oct 3 13:04 local (the 17:04:52Z file pass 2 read; untouched since)"; the confound is numeric (arm 2 zero-content at the 16000 cap; 7/14 rows cap-pinned).
RULING (conditional): both rows live in one 131-row register (commit b928a2240, fill-ball dwfrun-6c87e51f working it) with no DISPUTED marker reconciling them, so a fill-ball working R92/R94 can quote the overclaim as settled. Rule the "2-3x" rows unjudged-budget-confounded until the A/B rerun lands (a05-delta-study#15 lever, the DS_THINKING=on override); GO item 1 executes the ruling note. ATTRIBUTION CORRECTION (tier-2 verified at the 03:29Z fold, folding forward): the lane's claim names "R93" but the as-law claim text sits at line 472 under header "## R94 [medium] a05-delta-study (new)"; the two as-law rows are R92 (FILL bracket) and R94 (claim). R93 is the flash_chars counter-drift row and carries no ratio text. [a06-sacred-cow#1]

### D4. SAME-FILE PAIR: ARENA_V2_DESIGN bullet 3 erratum vs bullet 4 headline (a06-sacred-cow#2)
SIDE A (the surviving headline, now line 42) QUOTE: "4. PER-TASK THINKING: mechanical lanes thinking-off, design lanes thinking-on at 16K+ budgets (2-3x deliverables, zero AH10 failures on design shape)."
SIDE B (the same-day edit): the file was modified Oct 10 09:16 and bullet 3 grew by 10 lines carrying the GAP_REGISTER R10 erratum and the void census, while bullet 4 kept the unscoped headline (line 32 at HEAD, line 42 in the working tree, sed-verified both moments).
RULING: the overclaim survived a same-day edit; today's erratum discipline and the seven-day-old overclaim sit in adjacent bullets. Cure: the a06-sacred-cow#2 edit (bullet 4 to the scoped numbers), paired beside GO item 6.

### D5. FOLD-BYTES PAIR: INDEX fold moment vs live event log (a13-receipts-census#0)
SIDE A (the fold, as derived) QUOTE: ""derived_at": "2026-10-10T14:52:41.538Z",     "event_count": 13418,"
SIDE B (the live log): 13,682 lines against the fold's 13,418 events, 264 behind at a fold hours old (747 -> 284 -> 264 across the three fires).
RULING (conditional on moment): the fold is stale by construction between refolds and tools/refold_gate.py greps show no log-vs-fold drift check at all, so every receipt sealed after 14:52Z that day was invisible to INDEX queries until the next manual refold. Third consecutive recurrence; cure: GO item 7 (the tripwire in tools/refold_gate.py). [a13-receipts-census#0]

### D6. PREMISE-DRIFT PAIR: 2026-10-03 audit premise vs live push remote (a15-rollup#3)
SIDE A (the dead premise): the 2026-10-03 leak audit's "exposure is local-only".
SIDE B (the live bytes) QUOTE: "https://github.com/NachoBusiness17/mycelial-republic.git (push)"
RULING: the premise is dead. A live push remote exists (ls-verified), the audited commits are not on it (merge-base negative x3), but the tracked home-path surface is 6,650 occurrences in 666 files at the audited commit and 132,594 in 2,973 files at HEAD, so one push of a modern branch publishes the operator's home path wholesale; the single already-pushed occurrence (framework/docker-compose.yml) is unwashed. Cure: GO item 9. [a15-rollup#3]

### D7. CENSUS PAIR: the ask's "44/46 settled" vs the board (a12-ractor-legs#0, with a12-ractor-legs#4)
SIDE A (the current receipt on the audited path) QUOTE: "This file replaces the 2026-10-03 grokbot fork receipt that previously occupied this path (division A, 8 lanes; the review body's foreign-lane notes below refer to that run)."
SIDE B (the census): division A is 8 lanes/40 rows, division B is 12 lanes/0 rows, so "44/46 settled" matches nothing on this board. The companion premise numbers are phantoms: 36M tokens is 2.43x the ENTIRE alltime hermes_burn ledger (3,038 rows / 14,840,023 tokens / $94.7436, flat-field re-run this session via CHECK8; 0 rows after 2026-10-07T09:21:35Z), and "44/46" + "18 steals" live in exactly 3 files (pure self-echo). [a12-ractor-legs#0] [a12-ractor-legs#4]
RULING: rule "44/46 settled" void; point audits at the two division receipts (the division-A JSONs now live under _filed-20261003-grokbot/); the burn ledger is 3 days dark, so no meter exists for any in-flight "phase 2" burn claim. Cure: the a12-ractor-legs#4 verifier fix plus the 3-day-dark alarm, and the a12-ractor-legs#0 R54 amendment.

## NEGATIVE RESULTS (counted reasons table)

Counted by this fold's builder from the script sections, the lane JSONs, and the persisted checks files (instrument receipt in FOLD NOTES).

| # | reason | count | where | disposition |
|---|--------|-------|-------|-------------|
| 1 | tier-2 deep check unconfirmed | 1 row (2 verdicts) | a07-fifty-wide-waves#1 | excluded from included (PRISMA holds 162 = 161 + 1); both unconfirmed verdicts sit on this one row (pre- and post-repair keys); carried in DISPUTED as D0 |
| 2 | dead/blocked URLs at fold time | 2 URLs / 3 citing rows | HTTP 404 x.com post 2101068650161807857: a09-grok47#8; HTTP -1 deepseek api-docs create-chat-completion: a05-delta-study#9 and a06-sacred-cow#3 (source-field scan run this fold) | rows citing them move to negative results with their status; rendered rows carry url_checked_at [script-verbatim rule]. CONDITION (not a falsification): both deepseek-docs rows bank their own sitting-time fetch receipts (WebFetch + curl -sL, 142,966 bytes, byte-grepped) in their source fields; the fold-time probe returned HTTP -1, so the rows stand on their banked bytes with liveness marked failed at fold time |
| 3 | exact cross-lane duplicate quotes (normalized) | 3 pairs | a03-tavern-curve#16 + a15-rollup#0; a09-grok47#5 + a15-rollup#4; a11-commits#7 + a15-rollup#3 (recomputed by this fold over the 162 rows: whitespace-normalized exact matches, 3 and only 3) | counted, no exclusion; the Law 7 width gate is non-binding at width 15 (it binds above 50); the a15-rollup rows deliberately quote the sibling lanes' evidence as register defects |
| 4 | tombstones | 0 | [] | none: no hard failures, nothing subtracted from owed; missing/transient would get one bounded idempotent refill [script-verbatim rule] |
| 5 | verifier deep_tier2 join-miss (verified, no lane-row match) | 21 | join table [script-verbatim] | no exclusion weight, labeled not fatal; the misses ride prior-pass row texts the lanes later reworded, which is also why the a07 keys needed the 23:27Z repair |
| 6 | web-fetch rubric leg not applicable (estate-local byte sources) | 9 of 15 lanes | a01-arena-cadence, a02-dungeon-campaign, a03-tavern-curve, a08-rails-laws, a11-commits, a12-ractor-legs, a13-receipts-census, a14-queue-truth, a15-rollup (fold-computed from the lane notes; a06 and a10 fetched live, a04/a07/a09 fetched-equivalent or web_reader) | recorded as rubric gaps in the lane files, not exclusions |
| 7 | memory/research_polished zero-hit | 15 of 15 lanes | all lanes (fold-computed: every lane file records its own research_polished grep as zero hits) | the corpus-polish surface remains unwritten for this run's whole material set; standing negative at every audit moment (a15: fifth consecutive) |

## GO LIST (top 10; one seat, one sitting)

1. a15-rollup#0: Amend GAP_REGISTER 20261010 in one sitting: stamp R89 EXECUTED (healed in d349ce7d2, 2026-10-04); amend R13's FILL to the 8/37 closed census (kill the dead 3/13 count); append the R95 model-scoped correction; rule the R92/R94 2-3x rows unjudged-budget-confounded per R96 (D3's attribution correction applies: R94, not R93); land the fill-fold law (a "not re-verified" fill note triggers a one-command re-check before landing). [a15-rollup#0]
2. a03-tavern-curve#15: Execute master GO item 7 verbatim: dated 37/41 refresh into TAVERN_CURVE_AUDIT_20261003.md, persona-count column, three DEAD markers, RESEARCH_SUMMARY section 5 rewrite to the distribution reading, master refire lines; cite the closed census (newest calibration point 20261005T071101Z). [a03-tavern-curve#15]
3. a04-arena-gwap-gps#14: Execute arena GO item 3 exactly as written: scene-set refusal in bank() plus a one-time .bak-pattern migration recomputing the four capability rows at scene level, with the recompute proof against stored rows; landing spot tools/arena_gwap.py bank(). Retires the 1.2392x scene-level inflation standing in the live routing table. [a04-arena-gwap-gps#14]
4. a08-rails-laws#15: Port the sibling files' _offline fixture into tests/test_route_chat.py (monkeypatch rc.USAGE to tmp_path in test_dormant_lane_refusal) and add one case in tests/test_route_chat_banks.py asserting the production usage ledger is untouched by the suite. Closes the live-proven production-ledger leak (tier-2 verified: ledger row 23 is byte-for-byte the claimed test-written row). [a08-rails-laws#15]
5. a01-arena-cadence#13: Mint corpus/steal/ARENA_CAP_NEVER_HELD_20261010.md as a standalone steal card (the day-keyed whole-account gate is structurally lag-by-one-fire; a recreated arena cron must load the arena-family gate banked in erratum section 7). [a01-arena-cadence#13]
6. a15-rollup#2: Scope the two owning docstrings in mag/route_chat.py (wire_thinking 137-139 and the depth clause 180-183) to name the _thinking_forbidden carve-out (models whose inference_budget recipe forbids the key get omission; qwen-flash 400s), land the ratio gate at route_chat.py:300 with a banked test, and append the one-line R95 correction. Carries a06-sacred-cow#0's carve-out wording and a06-sacred-cow#3's vendor budget line (8K/64K/128K-at-max-effort defaults; reasoning_effort default high). [a15-rollup#2]
7. a13-receipts-census#0: Add the drift tripwire to tools/refold_gate.py (fail when wc -l index_events.jsonl minus INDEX event_count > 0 at day close) and wire it into the dawn report the way the census patrol reads its carrier. The drift has now outlived two manual refolds. [a13-receipts-census#0]
8. a13-receipts-census#2: Seal watch/inbox/gap_analysis_20261010/GAP_REGISTER.md with tools/md_record_seal.py AND fix the collision hazard it exposed: the fill-ball's dwfrun verifies its worklist receipt by dir+sha, not by the GAP_REGISTER name (three events answer to that name). [a13-receipts-census#2]
9. a15-rollup#3: Pre-push range gate blocking when the pushed range introduces new "C:/Users/foste" occurrences (the full tree is past hand-washing at 132k), and wash the single already-pushed occurrence in framework/docker-compose.yml now; landing spot githooks/pre-push next edit (master GO item 5 carries the fix). [a15-rollup#3]
10. a09-grok47#8: Append the DEAD_PRIMARY annotation to watch/inbox/LINKS.jsonl for the 404 post with this seat's fetch date, strike the row's load-bearing "ONLY on-disk pointer" language, and re-point any FlashREINFORCE claim at the recurring 0-entry arXiv state. [a09-grok47#8]

REMAINING OWED (13 rows outside the top 10, one seat one sitting each): a03-tavern-curve#4; a05-delta-study#14; a05-delta-study#15; a06-sacred-cow#2; a08-rails-laws#8; a08-rails-laws#12; a08-rails-laws#13; a09-grok47#10; a10-ds-batches#3; a10-ds-batches#9; a13-receipts-census#1; a13-receipts-census#4; a15-rollup#1. a05-delta-study#14 is absorbed by GO item 1 (the R89 stamp); a06-sacred-cow#2 is the bullet-4 edit paired beside GO item 6. Fold-computed from the scoreboard's 19 owed rows minus the 6 owed rows seated in the GO list.

## FOLD NOTES

- Gate note (conditional): top-10 lane share is 84.6% and the Law 7 gate binds only when width goes above 50, so no gate breach at width 15; the 3 duplicate quotes are counted, not excluded. [script-verbatim WIDTH-ECONOMICS]
- URL note: 4 of 6 unique URLs live at fold time; the 2 dead ones are dispositioned in NEGATIVE RESULTS row 2 and every rendered row carries url_checked_at. [script-verbatim URL LIVENESS]
- ORDINAL-REFERENT HAZARD (a04-arena-gwap-gps#15's citation-drift class, now applying to this file's own lineage): lane actions that cite "master GO item N" by number refer to the master version at their banking moment (T9's action cites the 02:55 fold's GO item 2, the dungeon parser fix, which has since landed per a11-commits#5; a03-tavern-curve#15's "GO item 7" cites the 18:19-era master). This fold's GO list carries named lane rows on every item precisely so ordinals cannot rot; quote the lane id + row index, never the ordinal.
- TWO-CLOCK FOLD HAZARD (a15-rollup negative, carried): the 02:55 master fold and the afternoon lane refires sat ~14 hours apart; this fire-4 fold closes that gap at 03:29Z by folding the post-refire verifier layer (the checks persisted 23:0x-23:2xZ) with the unchanged 162-row lane set, and D3 folds the verifier's R92/R94 attribution correction. The moment law applies to folds as much as to counts.
- The a15-rollup lane is this fold's successor register: its S1 rows are GO items 1 and 6 here, and its S2 rows are GO item 9 (home-path) and the second-fold pass (a15-rollup#1, remaining owed).
- Instrument receipt: this fold was assembled by the folder seat from FOLD_SECTIONS.md (script-verbatim slices) and the 15 lane JSONs; no other source contributed a number. Checks run by this fold's own sitting: whitespace-normalized cross-lane duplicate-quote recompute over all 162 rows (3 pairs, matching the script's count); dead-URL source-field scan over all rows (a05-delta-study#9, a06-sacred-cow#3, a09-grok47#8); location of both unconfirmed deep_tier2 verdicts in a07-fifty-wide-waves.checks.json with the 23:27Z repair note; byte-read of mag/route_chat.py:148-151 confirming D2's code side; research_polished grep-record scan across all 15 lane files (15/15 zero-hit).
