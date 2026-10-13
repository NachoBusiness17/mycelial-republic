# MICKEY-17 v2.1 master fold: run-0, refire state (2026-10-04)

Folded 2026-10-04 by the fold seat (dynamic-workflow actor "folder", run `mickey17_v2` run-0). This document SUPERSEDES the 00:42Z fold of 2026-10-03 that was banked at this same path (75 first-pass rows): every lane refired, mined its gap, and corrected its own first filings, and the archive now holds 94 rows across the same 15 lanes. The fold gate's counting script ran before this seat and its sections are authoritative (`memory/runs/mickey17_v2/runs/run-0/FOLD_SECTIONS.md`; byte-read in full this fold and matching the gate output). This document renders those sections verbatim and adds only the seat's prose, the TOP STEALS quotes and actions, the DISPUTED tier, the negative-results census, and the GO list.

Basis (read this fold, cited): `FOLD_SECTIONS.md` in full; all 15 lane JSONs (a01-a15) at `memory/runs/mickey17_v2/runs/run-0/lanes/` in full; the persisted verifier verdicts re-counted by this seat from the on-disk `.checks.json` files (commands in section 10). Every number below is the script's or a lane row's bytes; anything this seat counted itself carries the exact command and the tag `carried`.

Record law: fold prose is em-dash-free. Lane quotes keep their own bytes. Every steal sentence carries lane id + row index (0-based within the lane's `rows` array; the a08 lane's own r1-r10 labels are shown alongside).

## 1. CASUALTY HEADER (script, verbatim)

- fired: 15
- landed (parseable files): 15
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

Casualty ruling: none needed. The run metadata carries `"tombstoned": []` and `"refired": []` - every fired lane landed parseable, nothing is owed a refill, nothing is tombstoned.

## 2. PRISMA FLOW (script, verbatim)

- identified: 94
- screened: 94 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 94
- invariant: identified == included + excluded **HOLDS** (94 = 94 + 0)

## 3. SCOREBOARD (script, verbatim)

- rows: 94
- estate_status: confirms-ours 40, new 24, we-have-better 23, owed 7
- leverage: high 57, medium 36, low 1

Carried note (moment comparison, not a merge): against the 00:42Z fold's scoreboard (75 rows; confirms-ours 29, new 24, we-have-better 16, owed 6), the refire moved confirms-ours 29 to 40, we-have-better 16 to 23, owed 6 to 7, and rows 75 to 94 - refires re-graded first-pass rows against fresh bytes. Both scoreboards are moment-stamped; neither is averaged (census denominator law, B2-216).

## 4. FIDELITY / VERIFIER TABLE / WIDTH-ECONOMICS (script, verbatim)

FIDELITY:

- rows with all of quote/source/steal/estate_status non-empty: 94/94 (100.0%)

VERIFIER TABLE (persisted verdicts):

- lanes with persisted checks: 15
- verdicts: checks 15, deep_tier2 16, rows 10, supports 50

WIDTH-ECONOMICS:

- rows/lane: median 5, max 10, min 5
- top-10 lanes share: 73.4%
- exact cross-lane duplicate quotes (normalized): 5
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

Carried reconciliation (this fold's own instrument, commands in section 10): the on-disk checks files hold 75 tier-1 supports = 12 yes / 63 no (per-lane yes: a01-arena-cadence 1, a07-fifty-wide-waves 4, a09-grok47 1, a12-ractor-legs 3, a15-rollup 3), and 16 deep_tier2 verdicts = 15 verified / 1 unconfirmed. The script's "supports 50" is the section of record and is rendered verbatim above; the checks-file walk is this fold's instrument at its moment; both are reported, neither averaged (B2-216). The one unconfirmed deep verdict is ruled in DISPUTED D5.

Carried row-count audit (this fold's instrument): reading the `rows` arrays of all 15 lane files gives a01 8, a02 5, a03 7, a04 7, a05 10, a06 5, a07 5, a08 10, a09 5, a10 5, a11 5, a12 5, a13 5, a14 7, a15 5 = 94, matching the script's recount exactly (median 5, max 10 = a05/a08, min 5).

## 5. URL LIVENESS (script, verbatim)

- unique URLs: 2; fetched: 2; skipped non-public: 0; live: 0; dead/blocked-status: 2
  - HTTP -1: https://api-docs.deepseek.com/api/create-chat-completion (fetched via WebFetch, byte-checked via cur
  - HTTP 404: https://api-docs.deepseek.com/guides/reasoning_model

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

Ruling (DISPUTED D6): both dead statuses are fold-moment transport artifacts, not dead sources - a05-delta-study's own check_run fetched the create-chat-completion page live this wave (WebFetch plus `curl -sL`, raw HTML 142,966 bytes, `393216` grepped from the bytes) and a06-sacred-cow#4 fetched the reasoning_model guide live (curl raw HTML 48,088 bytes, the `thinking` object present after entity decode; the lane rules the prior fold's D5 404 transient). The two citing rows (a05-delta-study#9, a06-sacred-cow#4) move to NEGATIVE RESULTS N3 with their fold-time status and carry url_checked_at = their in-lane audit moments. Neither URL may be cited as dead without a fresh fetch.

## 6. TOP STEALS (the script's TOP-K; quotes and actions from the lane files)

Script header (verbatim): TOP-K (script-computed; a lane-claimed top steal outside this list files as DISPUTED)

All 12 entries are leverage=high. The script's printed lines are display-truncated; the full claims below are byte-read from the lane files this fold. Verification column: tier-1 = the row's persisted supports verdict (does the quote entail the claim; a "no" means the quote anchors one clause of a compound, which is register rank 14's standing discipline); tier-2 = the run's persisted deepCheck where one exists. Summary (`carried`, from the checks-file walk): 1 of 12 carries tier-1 yes (a01-arena-cadence#0); 5 of 12 carry tier-2 verified (a02#0, a02#1, a02#4, a03#1, a03#3). The DISPUTED trigger "lane-claimed top steal outside this list" fired zero times: all 15 lane files were read this fold and no lane claims a top steal beyond its rows (a15's gap_register ranks are register entries, not top-steal claims).

### 6.1 a01-arena-cadence#0 - the cap is $25; "$25.11" is a meter reading misnamed (tier-1 yes; estate_status new)

- Claim (lane bytes): The arena cap is $25 per the automation's own title and step-1 prompt; the parable's '$25.11 cap' misnames the 20:00Z meter reading ($25.1134, my recomputation from usage.jsonl) as the cap.
- Quote (source: `~/.zcode/v2/tasks-index.sqlite`, automations row automation-b1ce1342): `Hourly arena cycle: dungeon + tavern + gwap bank, $25 daily cap`
- Action (a01-arena-cadence#0): one seat, one sitting - amend the automation prompt so step 1 gates on arena-family ids only (TAVERN/DND0/CAMP) instead of the whole-day sum, then file a one-line parable erratum naming $25 as the cap and $25.11 as the 20:00Z reading.

### 6.2 a01-arena-cadence#1 - "8 cycles" is fire-count-true at filing and hides the failed first fire (tier-1 anchor-only; estate_status confirms-ours)

- Claim (lane bytes): '8 cycles' is byte-true as the fire count at parable-filing time (8 of 9 scheduled fires had fired) but the receipt hides that the first fire failed and that the 20:00Z fire ran three dungeon sessions at 20:21-20:23Z AFTER the day crossed $25 at 19:33:24Z; the 21:00Z fire shows succeeded with zero session activity, consistent with the cap gate finally stopping it.
- Quote (source: `watch/inbox/parable_day_one_20261003.md:9`): `the hourly arena cron, 8 cycles, automation-b1ce1342`
- Action (a01-arena-cadence#1): one seat, one sitting - fold the automation_runs sqlite census (fire times, outcomes) into the dawn compiler status feed and the parable erratum so cadence receipts carry failure rows, not just counts.
- Refire note (lane bytes): the fire count is now 15 (13:00Z 10-03 through 03:00Z 10-04, 1 failed = the 13:00Z first fire), so the "8 cycles" figure is stale without a moment stamp.

### 6.3 a01-arena-cadence#2 - every session did not bank; the catch-up rule starves backlog (tier-1 anchor-only; estate_status new)

- Claim (lane bytes): Every session did NOT bank: 8 of 41 dirs have no GWAP_BANKED and no ledger rows (dnd0 143335, 143639, 162136, 185933, 202147, 202158, 202213; tavern 162257), the 16:00Z fire banked nothing at all, and the 3 dirs without DONE (the 12:18-12:21Z manual burst) are banked anyway; the 'two newest unbanked' catch-up rule structurally starves backlog dirs because each fire mints 2 fresh unbanked ones.
- Quote (source: `watch/inbox/playground/dnd0_20261003T202213Z/DONE`): `"verdict": "PARTIAL: the Wyrm unanchored - the season continues", "spend_usd": 0.2399`
- Action (a01-arena-cadence#2): one seat, one sitting - run `.venv/Scripts/python.exe tools/arena_gwap.py` over the unbanked dirs oldest-first (order flag or explicit list, not 'two newest'), landing markers plus arena-capability.jsonl rows and a one-line backlog receipt in `watch/inbox/`.
- Post-audit state (lane bytes, a01#5): superseded in flight - an unattributed backfill drained the whole backlog to 53/53 dirs GWAP_BANKED and ledger-covered by 03:26:51Z. The action's surviving residue is the oldest-first ordering fix and the receipt; the banking claim itself is only honest with a moment stamp (N12).

### 6.4 a01-arena-cadence#5 - the banking answer is moment-dependent; the tree moved under the audit (tier-1 anchor-only; estate_status new)

- Claim (lane bytes): The audit's 'did every session bank' answer is moment-dependent and the tree was moving under the audit: at the parable's filing and at my 03:04Z census the answer was NO (16-17 of ~48-51 dirs unbanked, ledger zero-rows at hours 16/20/21/22/23), but a backfill drained the entire backlog between 03:04Z and 03:26:51Z so that at the final read every one of 53 session dirs carries GWAP_BANKED AND matching ledger rows (88 rows banked at hour 03), meaning the banking claim is only honest with a moment stamp.
- Quote (source: `memory/runs/gwap/arena-capability.jsonl`, last-row fragment): `"ts_utc":"2026-10-04T03:26:51Z"`
- Action (a01-arena-cadence#5): one seat, one sitting - add a banked_at moment column to the dawn report's gwap line (rows, sessions, AS-OF timestamp) and a receipts note crediting the backfill run (`tools/arena_gwap.py --backfill` is the only flag matching the 88-row hour-03 drain, but no receipt names the runner - attribution is unproven), landing in `watch/inbox/`.

### 6.5 a01-arena-cadence#6 - the parable cites a ledger that matches no file on disk (tier-1 anchor-only; estate_status new)

- Claim (lane bytes): The parable cites a ledger that matches no file on disk: 'the arena-sessions-v3 ledger (266 rows, chain ok)' - arena-sessions.jsonl holds 60 rows frozen at 12:52:58Z, arena-capability.jsonl held 314 at filing, and the name 'arena-sessions-v3' appears nowhere in code or any other receipt; the 266 figure is best explained as the capability ledger's post-hour-14 moment (121+145) stapled to a wrong ledger name, a phantom-citation class defect (GAP_REGISTER rank 3) in a receipt that is itself about honesty.
- Quote (source: `watch/inbox/parable_day_one_20261003.md:12`; grep -c confirmed exactly 1 byte-match): `the arena-sessions-v3 ledger (266 rows, chain ok), verkle-anchored, the golden vectors reproducing`
- Action (a01-arena-cadence#6): one seat, one sitting - one-line parable erratum correcting the ledger citation to arena-capability.jsonl with the filing-moment count (314) and adding arena-sessions.jsonl (60 rows, the 12:51Z bar-fight, frozen) as its own named artifact.

### 6.6 a01-arena-cadence#7 - the cap held only for the cron lane and only from 21:00Z (tier-1 anchor-only; estate_status new)

- Claim (lane bytes): The cap held only for the cron lane and only from 21:00Z: the day crossed $25 at 19:33:24.686865Z (cumulative $25.1134 on a GALA prime-judgment row), the 20:00Z fire still ran three dungeon sessions post-crossing whose bank then never ran that night (hour-20/21/22/23 ledger buckets empty until the backfill), manual dungeon play continued 22:50-22:56Z, and the day closed at $25.6218 - $0.62 OVER the $25 cap; day 04 opened clean ($1.2509 by 03:3xZ) and the 02:21-02:28Z pair banked outside any fire window (02:00Z fire closed 02:03:11Z), so the bank step is not fire-atomic.
- Quote (source: `memory/runs/hermes_burn/usage.jsonl`, crossing row): `{"ts": "2026-10-03T19:33:24.686865Z", "id": "GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003_STAGE_B", "model": "z-ai/glm-5.3-prime"`
- Action (a01-arena-cadence#7): one seat, one sitting - make the automation's bank step run AFTER play within the same fire (or have the tavern carrier invoke arena_gwap bank at exit) so a fire's own sessions can never outlive their bank overnight, then dogfood one fire and check the ledger's hour bucket.

### 6.7 a02-dungeon-campaign#0 - parser collapse decided the verdict (tier-1 anchor-only; tier-2 verified; estate_status confirms-ours)

- Claim (lane bytes): Parser collapse decided the verdict: strip_and_cap (dungeon.py:102-107) flattens every speech to one line and the tag scan (dungeon.py:488-491) reads only line-initial bracket lines, so the 14 logged S4 PC speeches all parse tagless and the S4 disjunct at dungeon.py:496 (Python precedence makes the wyrm test independent of verb) resolves every one as a wyrm ATTACK; my replay of all 14 speeches through the current HEAD bytes reproduces 14/14 logged verdicts and reaches the AUDIT branch 0 times, so all [AUDIT root] win checks were structurally unreachable as played. Folded as master 6.4 / N7 / GO item 2 in the prior fold; line anchor moved from the prior 485 to 496 on the clean tree.
- Quote (source: `tools/dungeon.py:496`): `if verb == "ATTACK" and obj in enemy["actor"] or (scene == "S4" and obj == "wyrm"):`
- Action (a02-dungeon-campaign#0): one seat, one sitting - execute the parser fix (regex tag search across the capped speech or opening-tag-only grading) in tools/dungeon.py, plus tests/test_dungeon_parser.py replaying the 14 logged S4 verdicts as fixtures. (This is the leg the lanes cite as former GO item 2; it rides GO item 4 below.)

### 6.8 a02-dungeon-campaign#1 - Phantom Regrowth is spec'd but never enforced (tier-1 anchor-only; tier-2 verified; estate_status confirms-ours)

- Claim (lane bytes): Phantom Regrowth is spec'd but never enforced: the campaign enemy branch (dungeon.py:439-468 current bytes) contains no per-turn heal and the only ehp mutation is the damage clamp at dungeon.py:499, and the scroll-audit reveal is case-dead because obj is lowercased at dungeon.py:494 while the carried keys are mixed-case, so the membership test at dungeon.py:515 ('vault deed b' in carried -> False, executed) can never burn a phantom. Commit a7d7d313d claims 'regrowth 5/scroll' anyway (a phantom figure, N5-registered in the prior fold), and the DM narrated the heal at transcript row 45 that the state machine never applied. The Wyrm therefore died at turn 8 on 30 HP that the spec's Wyrm would have kept regrowing.
- Quote (source: `watch/inbox/hermes_burn/DND_module.md:89`): `At the start of each Wyrm turn, it heals 5 per PHANTOM scroll still unaudited in any pack.`
- Action (a02-dungeon-campaign#1): one seat, one sitting - implement the per-turn heal keyed to the unaudited PHANTOM count plus the audit-burn, case-fold the carried lookup at dungeon.py:515, and land the two-line erratum on commit a7d7d313d in the run receipt at `watch/inbox/playground/`. (Rides GO item 4.)

### 6.9 a02-dungeon-campaign#3 - the DM channel was dead for the whole campaign and nobody banked it (tier-1 anchor-only; no persisted tier-2 on this row - its predecessor's deep verdict is verified and the refire corrections are banked in-lane; estate_status new)

- Claim (lane bytes): NEW: the DM channel was dead for the whole campaign and nobody banked it. The content_filter void path (dungeon.py:183-193) replaced the dm_response on 40 of 50 transcript rows including all 39 PC-beat readbacks (only the S0 omen and 4 of 5 monster beats got narration), so the module's read-back loop (the DM must open with the verdict tag, DND_module.md:138) never reached a single PC; the seats responded by self-rolling d20s inside their speeches, which the carrier then discarded. Zero hits for 'content_filter' in MASTER_MICKEY17_V2.md, ARENA_V2_DESIGN_20261004.md, and DND_module.md against 40 in the run transcript. This is also the mechanism behind the folded finding: the dice_audit rerun exits 1 with verdict flags on all 50 rows and preimage/roll/turn flags on the 5 ledger rows, correcting the prior fold's 45-and-4 counts; per the module's own falsifier the session is VOID from the first bad row, not a clean PARTIAL.
- Quote (source: `tools/dungeon.py:183`): `content = ""  # a filtered generation is void regardless of bytes`
- Action (a02-dungeon-campaign#3): one seat, one sitting - bank finish_reason per call and count voided readbacks in the run's DONE, retry the DM call on a de-globbed prompt (it quotes the actor's combat speech verbatim), and file the void-census in the run 202213Z receipt; land in tools/dungeon.py _paid plus the ARENA_V2 design's substance-gate leg. (Rides GO item 4.)

### 6.10 a02-dungeon-campaign#4 - PARTIAL is earned by the letter and not in substance (tier-1 anchor-only; tier-2 verified; estate_status confirms-ours)

- Claim (lane bytes): PARTIAL is earned by the letter and not in substance: deterministic and reproducible (root_anchors 0/3, party alive with chatgpt lowest at 6 HP, Wyrm down at turn 8 on cumulative 39 damage of 30 HP, 95 total S4 PC damage), but the win path was unreachable by construction (row 0) and the label rides a VOID session (row 3). Corrected counts now in the row: 5 explicit [AUDIT root] request beats / 6 tag occurrences in S4 speeches, and the saelis cross-audit quote reads 'aren't on the ledger' verbatim, not 'are not'. Spend claim reconciled by the lane's own ledger split: exactly 84 usage rows fall in the run window 20:22:13-20:30:14Z, the exact call count the code implies (39 PC beats x 2 + 5 monster beats + 1 S0), summing $0.2400 vs DONE's $0.2399 (per-row 4-decimal bank rounding), with zero rows stamped dnd0_20261003T202213Z because the tag law landed post-run in f017a479a. Emergent keeper stands: the seats cross-audited each other's self-rolled numbers in-world, trust-bytes-not-reports under a dead referee. ARENA_V2_DESIGN_20261004.md:36-38 now seeds the v2 season on this verdict.
- Quote (source: `watch/inbox/playground/dnd0_20261003T202213Z/DONE`): `PARTIAL: the Wyrm unanchored - the season continues`
- Action (a02-dungeon-campaign#4): one seat, one sitting - file the carrier-failure erratum receipt for run 202213Z at `watch/inbox/playground/` (verdict PARTIAL stands, mechanics off-spec, audit VOID, DM channel 40/50 voided), and carry the in-world cross-audit behavior forward as a named party mechanic in the module revision. (Rides GO item 4.)

### 6.11 a03-tavern-curve#1 - "p1 r3 x2" refuted by the run table (tier-1 anchor-only; tier-2 verified; estate_status we-have-better)

- Claim (lane bytes): Component 'p1 r3 x2' REFUTED by the run table: of 13 pressure-1 runs, exactly ONE brawled at round 3 (this file, line 113); the ten p1 brawls landed at rounds 3,4,4,4,5,5,5,6,7,10 (115343Z, 162257Z, 171056Z, 124545Z, 115732Z, 180319Z, 190348Z, 140343Z, 130953Z, 125711Z) and three p1 runs never brawled (121214Z, 124908Z, 152937Z). First escalation of any persona is round 2 in all 13, not 3.
- Quote (source: `watch/inbox/playground/tavern_20261003T115343Z/play.md:113`): `BRAWL at round 3: cumulative escalation 16 >= 16 (pressure 1)`
- Action (a03-tavern-curve#1): one sitting - replace the p1 cell in any calibration card with 'brawl r3-r10 spread, 3/13 no-brawl' from the RUN DONE grep of tavern_*/play.md; land in the next DD-selfsteal fold.
- Refire count update (lane bytes, a03#5; instrument: `grep "BRAWL at round" watch/inbox/playground/tavern_*/play.md` over the 14 p1 runs with RUN DONE at the 2026-10-04 refire moment, receipt watch/inbox/go_wave_20261004/tavern_refresh.md): the corpus grew after the prior bank - T022300Z is p1 session 14 and brawled at round 6 ($0.85), so p1 now reads 11 brawls at rounds 3,4,4,4,5,5,5,6,6,7,10 (median 5) with the same 3 no-brawl runs; exactly one p1 brawl at round 3 still holds, so 'p1 r3 x2' stays refuted on the larger table.

### 6.12 a03-tavern-curve#3 - "Greta fuse 3/3" refuted on both words (tier-1 anchor-only; tier-2 verified; estate_status we-have-better)

- Claim (lane bytes): Component 'Greta fuse 3/3' REFUTED on both words: tools/tavern.py has no 'fuse' - Greta's escalation_threshold is 2 (eff_threshold 1 at p1) in every scenario.json; parsed transcripts show her judge score is 3/5 at round 1 in 12 of 15 runs (4/5 in 3, including this one) and esc crosses 2 at round 2 in 15/15 runs - she never waits three rounds. '3/3' fits only the day's first-three-runs sample (r1 scores 3,3,3) and understates 15/15.
- Quote (source: `watch/inbox/playground/tavern_20261003T130953Z/play.md:24`): `round 1 Greta Thornwood: 4/5 - She openly invokes twenty blades waiting outside, demands forty silver and implies Pell could lose his fingers, a direct threat of violence.`
- Action (a03-tavern-curve#3): one sitting - rewrite the Greta cell as 'judge 3-4 at r1, esc>=2 by r2, 15/15 runs' wherever the tavern calibration note lands.
- Refire count update (lane bytes, a03 refire block; instrument: `grep "round 1 Greta Thornwood" watch/inbox/playground/tavern_*/play.md` over the 16 BARFIGHT sessions with Greta at the 2026-10-04 refire moment, receipt watch/inbox/go_wave_20261004/tavern_refresh.md): 3/5 in 13 of 16 Greta sessions (was 12 of 15); 4/5 in 3 (124908Z, 130953Z, 171056Z); thresholds 2/eff-1 hold in all 16 BARFIGHT scenario.json files.

## 7. DISPUTED TIER

Rule of this tier: a contradiction is held open with both quotes and a conditional ruling; nothing is averaged. Tier-2 unconfirmed rows land here (1 of 16 on the current checks files, walked this fold). D1-D4 carry the prior fold's rulings forward in their refire state; D5 is new this fold; D6 rules the URL-liveness section.

### D1 - a07-fifty-wide-waves#1: the 10-unit tally gap stands; the em-dash drop mechanism is refuted

- Byte-true half (tier-2 verified): the extraction artifact `memory/runs/burn_audit_claims.json` holds 60 distinct units over 16 source filings while the receipt tallies 50 verdicts (30+11+3+6), so 10 units carry no recorded verdict; no per-agent result artifact exists on disk for either wave.
- Refuted half (tier-2 measurement): the prior em-dash hypothesis is REFUTED - the lane measured 2 em-dash units in claim text and 2 raw em-dash byte sequences in the JSON, never 10; the refire row itself now carries the CORRECTED text.
- Conditional ruling (carried from the prior fold's D1): file the dispatch guard (assert len(units)==lanes, print any dropped-unit list) without the em-dash hypothesis; the mechanism is unknown and the dispatch log is not on disk. Quote for the record (a07#1, source `watch/inbox/burn_claims_50wide_20261003.md`): `flash lanes, each byte-checking one claim from 16 BURN_* filings.`

### D2 - a05-delta-study#2: the flash-arm asymmetry is directionally real; its published denominators were never byte-reproduced

- The row's claim (lane bytes): "97 of 115 WIRE_PLAN citations and 69 of 81 THE_ROOM_REMEMBERS citations appear only in the flash outputs and not in the rendered material, and 7 of 7 spot-checked flash-only cites resolve to real file:line bytes."
- State of the verdicts: the prior fold's tier-2 ruled this row unconfirmed (97 numerator and 7/7 spot-checks reproduced; the 115 and 69/81 denominators reproduced under no counting rule tried, and the "rendered material" baseline was never identified); the current checks files carry no deep verdict for it, so nothing supersedes that finding - it is carried, not re-graded.
- Conditional ruling (carried): cite the finding only as "97 unique flash-only file:line cites in WIRE_PLAN.md, 7/7 spot-checks resolve; denominators unreproduced" until the counting rule is stated and the baseline named. Quote for the record (a05#2, source `watch/inbox/replay_flash/WIRE_PLAN.md` header): `Replay of: `memory/plans/hermes_burn_playground_20261003/WIRE_PLAN/ask.json` (target model anthropic/claude-opus-5.5; replayed on the flash rail, 2026-10-03).`

### D3 - a06-sacred-cow#2 vs the route_chat depth law: two law surfaces disagree on thinking-on; operator signature owed

- Side A (a06#2, source `watch/inbox/model_garden/PRIORS.md:25`, STILL-VALID, last touched Oct 1, before the probe): `STILL-VALID (byte-confirmed mechanism, never refire thinking-on)`
- Side B (a06#3 + a06#4, source `mag/route_chat.py` per the lanes' line-by-line read): depth='design' sends `thinking:{type:enabled}` to every lane while mechanical keeps thinking off by omission and never reads the lane's `disable_thinking` flag; the wire shape is live-verified (a06#4 quote, source the DeepSeek reasoning_model guide): `"thinking": {"type": "enabled"},`
- Counter-evidence both ways (lane bytes): the row-8 mechanism is real - the probe's own arm 2 banked 2/10 ok:false zero-content rows at the 16000-token cap (a06#0) - and the design-ask exception is also real (arm 1 landed 4/4 deliverables).
- Conditional ruling (carried, unchanged): treat PRIORS row 8 as scoped to mechanical/long-form until the operator signs; the amendment must name the exception AND the counter-evidence. Held out of GO pending that signature.

### D4 - a08-rails-laws r5 / a06-sacred-cow#3: two in-repo sources contradict on the deepseek v4 thinking-omission default

- Side A (a08 r5 quote, source `configs/providers.yaml:367`): `DeepSeek v4 defaults thinking ON; reasoning tokens eat max_tokens and small budgets return EMPTY content`
- Side B (a08 r5 claim, source `tools/ds_workhorse.py:55-56` per the lane's read): omitting the thinking object IS the off state. Meanwhile `mag/route_chat.py` never reads the lane's `disable_thinking` flag (grep: zero hits in the module, both lanes) and its `msg.get("reasoning")` fallback at :148 reads the wrong field name for the vendor's `reasoning_content`.
- Conditional ruling (carried, unchanged): neither comment is trusted until a $0.001 A/B (thinking omitted vs explicit disabled) is run through route_chat with the winner banked to `memory/runs/route_chat/usage.jsonl`. The four ok=false empty-content smoke rows in that ledger sit on top of this unresolved contradiction. Held out of GO pending the A/B.

### D5 - a08-rails-laws r9 (#8): "doc-first" is contradicted by the git record - the run's ONLY tier-2 unconfirmed row

- The row's claim (lane bytes, estate_status owed): "Rails-default is doc-first and honest but unadopted: the rails doc commit (b5dac8d83) is an ancestor of route_chat.py's creating commit (53f56d0f3, merge-base verified), and this sitting's census found 97 files under tools/+mag/ still calling urlopen and zero test files referencing route_chat, so the doc's named 4-carrier debt understates its own migration backlog."
- The row's quote (source `queue/STANDING_RAILS.md:46-48`, byte-true under whitespace normalization): `tavern/dungeon/hermes_burn/grok_burn still self-call; each migrates to route_chat or documents its reason (fences differ per endpoint) - one per sitting, no batch rewrite.`
- The tier-2 counter-evidence (persisted, verdict unconfirmed): `git log --all --diff-filter=A -- "*route_chat*"` finds exactly one creation in all history - b5dac8d83, the SAME commit that created the rails doc; 53f56d0f3 is the first modification, not the creating commit, so "doc-first" (doc preceding the implementation) is contradicted by the git record and the ancestry check is trivially self-referential. The 97-file urlopen census does not byte-reproduce (closest instruments read 98 on today's tree), and the backlog-understatement inference does not follow from raw urlopen counts because `mag/route_chat.py:145` itself calls urlopen. The debt line itself and "zero test files referencing route_chat" both verified.
- Conditional ruling: keep the debt line as byte-true (the 4 named carriers still self-call, re-verified by the checker); strike "doc-first" everywhere (doc and module landed in one commit); re-census with the named instrument (`grep -rln --include="*.py" "urlopen(" mag tools`) before citing any count (98 today, moment-stamped); never measure migration backlog by raw urlopen counts. The row's one-sitting action (migrate grok_burn onto route_chat(lane='xai') with its fence-difference reason) stands and rides GO item 1's adoption leg.

### D6 - URL liveness: two DeepSeek docs URLs dead at the fold moment, live in-lane hours earlier

- Fold moment (script, verbatim in section 5): HTTP -1 on https://api-docs.deepseek.com/api/create-chat-completion; HTTP 404 on https://api-docs.deepseek.com/guides/reasoning_model.
- In-lane moments: a05-delta-study#9's source fetch (WebFetch plus `curl -sL`, 142,966 bytes, `393216` grepped from bytes) and a06-sacred-cow#4's source fetch (48,088 bytes, the thinking object present after entity decode).
- Conditional ruling: no contradiction in the findings - both wire shapes were byte-confirmed when fetched. The rows file in NEGATIVE RESULTS N3 with their fold-time status and url_checked_at = their in-lane moments; a06#4's demanded test (tests/test_route_chat_depth.py asserting the request body) pins the shape locally so no future seat needs either URL.

## 8. NEGATIVE RESULTS (counted reasons)

Tombstones: `[]` (zero). Refires owed: `[]` (zero). All 15 fired lanes landed parseable (section 1); every refire already landed in its lane file.

Counts in this table are `carried` (this seat's grouping of lane-file rows at this fold's moment); the script computes none of them. Instance pointers are lane bytes.

| # | Reason class | Count | Instances (lane#row, 0-based; a08 by r-label) | Disposition |
|---|---|---|---|---|
| N1 | Tombstoned lanes | 0 | none | run metadata tombstoned=[] |
| N2 | Refires owed | 0 | none | run metadata refired=[] |
| N3 | Dead URL at fold time | 2 | a05-delta-study#9 (create-chat-completion, HTTP -1), a06-sacred-cow#4 (reasoning_model, HTTP 404) | moved here per script law with fold-time status; both fetched live in-lane; ruling in D6 |
| N4 | Tier-2 unconfirmed rows | 1 | a08-rails-laws r9 (#8) "doc-first" | ruled in DISPUTED D5 |
| N5 | Phantom or unbacked figures | 14 rows | a01#0 ($25.11 cap misname), a01#3 ("held to 35 cents" matches no slice), a01#6 (arena-sessions-v3 phantom ledger name), a02#1 half ("regrowth 5/scroll" commit-message figure), a03#1 ("p1 r3 x2"), a03#3 ("Greta fuse 3/3"), a05#4 + a14#2 ("30/50 lanes, ~20 killed" vs the 39/39 results file), a05#5 ($0.14 hand-copied vs measured $0.1928 grand / $0.0977 v2), a06#0 half ("zero AH10 failure modes" vs arm-2 2/10 zero-content), a06#1 ("2-3x" unjudged budget-confounded ratio), a09#0 (8.1/30, 6.9/30 rates standing for integer tallies), a09#1 (pre-written fail sentence contradicted by its own 23%), a12#4 (ask premise phantoms: 44/46, 18 steals, 36M) | each carries a named erratum or ruling in its lane row; a15 register ranks 3-15 bundle them |
| N6 | Stale-owed drift (surfaces say owed/open where the work landed) | 8 rows | a05#4 + a14#2 (rails judge-pass line vs the 39/39 file, mtime 13:04 vs rails 12:48), a14#0 (Q-005/Q-025 closed in todo, open in queue_index since 2026-09-29, citation paths wrong), a14#1 (todo:31 open box vs the elder consult's park and Q-001's 09-30 close), a14#3 (NIGHT_CLOSE move 2 orders a lens-rz1 repair that landed 44 min after the close), a14#4 (GAP_REGISTER presents fillball-filled ranks 2/3/4/6/7 as open), a14#6 (A16 says C1-C3 UNEVALUATED vs STOCHASTIC_LENSING secs 6-7 C1 REFUTED), a15#0 (the prior fold's GO item 7 ordered banking a backlog an out-of-band backfill had already drained), a01#2 half (the 8-dir backlog census superseded in flight) | strike/annotate the owed surfaces; GO items 3, 5, 6, 7 |
| N7 | Structural mechanism defects (doctrine landed, mechanism broken or unenforced) | 17 rows | a01#2 half (catch-up rule structurally starves backlog), a02#0 (parser collapse; also top steal 6.7), a02#1 (regrowth unimplemented, case-dead reveal), a02#2 (Load-Failure Wipe fired off-spec: no prior-verdict gate, party-wide phantom drop, boss starved to 30 HP vs spec 40 - the row the prior fold did not carry), a04#1 half (40 failable rows banked after 14:09:28Z never fed), a04#2 + a04#4 (feed/bank dedupe unsound: 133 double-banked scene_ids, 6 pairs with differing replay hashes, no chain tip, crash mid-loop re-banks), a04#6 (all 259 gps rows self-attested, evidence_resolved=0), a04#6-adjacent a04 row 6 (DUNGEON_ACTOR_MODEL sole identity source for dnd0 rows), a08 r6 (fence TOCTOU: DNS resolved at :75, re-resolved by urlopen at :145), a08 r10 (#9, failures bank nothing: _bank exactly once, never in an except path), a08 r9 half (zero route_chat tests), a10#0 (v1 artifacts still un-void-stamped, 30/30 rows ok:true), a10#1 (ok=True measures API success, never material engagement), a10#3 ({text} law absent from tool docstring, AGENTS.md, and tests), a13#0 (INDEX fold 747 events stale, zero of today's receipts queryable), a13#2 + a13#3 (4 receipts cited-but-never-registered), a15#0 (transfer leg: refire deltas unfolded downstream) | GO items 1, 2, 4, 5, 6, 8, 9; a15#0 partially cured by this document landing in corpus/steal |
| N8 | Unarchived or unrecoverable evidence | 7 | a07 not_run block (no per-agent result artifact for either 50-wide wave; dispatch log not on disk; tally-gap mechanism unknown), a03 gaps (BARFIGHT_spec design-ask output not located; p0 exact trigger unverified), a10 negatives (v1 prompt bytes overwritten 12:19Z), a11 negative ("121 payloads, 178 verdicts fed" is a runtime count not byte-verifiable at commit moment; growth-consistent only), a12 gaps ('18 steals' unverifiable, workflow introspection unavailable), a09 new_negatives (X primary 60s timeout behind the auth wall), a01 negative (the 03:26:51Z backfill runner attribution unproven) | recorded as the boundaries of this run's knowledge; nothing filled by guess |
| N9 | Transfer gap (refire deltas unfolded downstream) | 1 | a15#0 (all 13 refire-delta markers grep 0 in the prior MASTER; the percolator's 7 new invariants are behavioral pro-ticks; memory/research_polished stays zero-hit on day terms) | partially cured by this document landing (it folds the refire deltas); LINKS rows + percolator fire remain the one-wave leg |
| N10 | Zero-hit transfer greps (unmined polished corpus) | 13 of 15 lanes | a01, a02, a03, a04, a06, a08, a09, a10, a11, a12, a13, a14, a15 each recorded a memory/research_polished zero-hit on their own terms | exceptions named, not smoothed: a05 found routing lineage (kv_cache_compaction.md:15-16, persona_ractor_salon.md:61); a07 found ENHANCEMENT_STACK_20260920.md |
| N11 | Prior-fire self-defects, corrected in-lane this wave | 5 lanes, 10 named defects | a13 (3: phantom quote byte STEAL vs file's STEER; whitespace-normalized cross-line quote; burns.md citation lines 116-117 wrong, actual 33/131-132/143/209), a11 (1: insertions(++) quote corruption, corrected to insertions(+)), a10 (4 first-filing strikes: S2-only, non-reproducible grounding ranges, 41KB avg, wrong commit hash), a15 (1: its own rank-1 zero-footprint claim false after two folds landed), a03 (1: compression chain - ask preamble "round 3-4", transcript marker round 5, lane claim "r3 x2") | the record law worked: every defect was caught by the seat's own second instrument |
| N12 | Moment-dependent verdicts on a moving tree | 3 | a01#5 (banking answer flipped NO to YES between 03:04Z and 03:26:51Z), a15#0 (the prior fold stale on arrival), a03#5 (corpus grew post-bank: 13 to 14 p1 runs, 12-of-15 to 13-of-16 Greta) | every restated figure in this fold carries its moment; the banked_at column (GO item 6) is the systemic fix |

## 9. GO LIST (top 10; one seat, one sitting)

Ordered by the a15-rollup gap register (the estate's own severity x fill-ease ranking); lane-cited former GO items of the 00:42Z fold are absorbed and named so cross-references stay resolvable.

1. (a06-sacred-cow#0, a06-sacred-cow#3, a08-rails-laws r6/r7/r10; a15 rank 1) Route_chat compound: amend the mag/route_chat.py:94-98 docstring to scope the claim (arm 1 4/4; arm 2 2/10 zero-content at the 16000 cap); wire disable_thinking, fix the reasoning_content dead fallback, validate the depth enum; land tests/test_route_chat_fence.py (the 5 executed offline checks), tests/test_route_chat_banks.py (hollow-200 banks ok:false regression), tests/test_route_chat_depth.py; add the exception-path _bank row; close the fence TOCTOU (:75 vs :145); route one real production ask so usage.jsonl carries a non-smoke goal. (Absorbs former GO item 3.)
2. (a04-arena-gwap-gps#1, a04-arena-gwap-gps#2, a04-arena-gwap-gps#4, a04-arena-gwap-gps#6, a01-arena-cadence#5; a15 rank 2; former GO item 1) gwap-to-gps dedupe and feed: UNIQUE(model_id, task_shape, evidence_hash) in verdict_log plus INSERT-that-skips in record_verdict; migrate tools/gps_mcp/gps_ledger.db3 by the .bak pattern; feed the 40-row failable backlog; pass evidence_bytes in feed_session; print a per-invocation feed receipt (rows_seen/fed/skipped/distinct); prove by rerunning --backfill with zero new verdict rows.
3. (a05-delta-study#0, a05-delta-study#3, a05-delta-study#4, a05-delta-study#5, a05-delta-study#6, a05-delta-study#9, a14-queue-truth#2; a15 rank 3; former GO items 4+5) Delta-study receipt repair: caveats block + judge tally {frontier 8, flash 5, ds 0/26} + ds_capped field + measured cost column into watch/inbox/frontier_delta_register_20261003.json; correct queue/STANDING_RAILS.md:49-50 to 39/39 linking memory/runs/ds_batches/delta_judge_results.jsonl; restate or drop the $0.14 figure; judge the gaming_corpus pairing (the prompt's own rule makes it 9-5); delete the max_tokens 2000 override at tools/ds_workhorse.py:52 and re-fire the ds arm before any routing table cites 0-for-26.
4. (a02-dungeon-campaign#0, a02-dungeon-campaign#1, a02-dungeon-campaign#2, a02-dungeon-campaign#3, a02-dungeon-campaign#4; a15 rank 4; former GO items 2+8) Dungeon campaign: the parser fix plus tests/test_dungeon_parser.py replaying the 14 logged S4 verdicts (the leg the lanes cite as former GO item 2); implement the per-turn heal plus audit-burn and case-fold the dungeon.py:515 lookup; gate the wipe on the hit target's prior verdict in {FAIL, MISS, FUMBLE} dropping that PC's pack; bank finish_reason per call and count voided readbacks in DONE; file the run-202213Z carrier-failure erratum receipt at watch/inbox/playground/.
5. (a13-receipts-census#0, a13-receipts-census#2, a13-receipts-census#3; a15 rank 5; former GO item 6) INDEX and registration: run scripts/index_fold_host.mjs to refold INDEX.json (747 events stale), then tools/md_record_seal.py over frontier_delta_register_20261003.json and the three xai_grok47 files; rerun the name greps to confirm all receipts appear.
6. (a01-arena-cadence#0, a01-arena-cadence#1, a01-arena-cadence#5, a01-arena-cadence#6, a01-arena-cadence#7; a15 rank 7; former GO item 7, annotated) Arena cadence close-out: make the bank step run inside the fire after play (or the tavern carrier invokes arena_gwap bank at exit) and dogfood one fire; file the parable erratum ($25 cap, $25.11 meter reading, real ledger names with the filing-moment count, the $0.62 over-cap close, the failed 13:00Z fire); add the banked_at moment column to the dawn report; land the backfill attribution note (unproven, not assumed). Former GO item 7 ("bank the 8 unbanked dirs") is DRAINED - the backfill covered 53/53 by 03:26:51Z; strike it and keep only the ordering fix.
7. (a14-queue-truth#0, a14-queue-truth#1, a14-queue-truth#3, a14-queue-truth#4, a14-queue-truth#6; a15 rank 8) Queue-surface truth strikes: append closed rows for Q-005/Q-025 to queue_index.jsonl and fix the todo citation paths; flip todo.md:31 to parked per the elder consult; strike NIGHT_CLOSE move 2 with a pointer to STOCHASTIC_LENSING.md secs 6-7; amend A16_LENS1_VERDICT.md with the verdict-fired addendum; annotate GAP_REGISTER ranks 2/3/4/6/7 with their fillball receipt paths.
8. (a07-fifty-wide-waves#1; a15 rank 9; D1 ruling) Fifty-wide tally guard: make the wave dispatch assert len(units)==lanes and print any dropped-unit list into the receipt; operator sub-item: retain the dispatch log so wave counts are replayable.
9. (a10-ds-batches#0, a10-ds-batches#1, a10-ds-batches#3; a15 rank 10) Hollow-batch enforcement: void-stamp gapfold_results.jsonl and frontier_delta_results.jsonl in place; split ok_api + ok_material with per-row prompt_tokens at tools/ds_workhorse.py:90-94; paste law 2 into the ds_workhorse docstring plus an empty-text render guard in run(); add one render-law test; put one STANDING_RAILS pointer line on the AGENTS.md commands card.
10. (a03-tavern-curve#1, a03-tavern-curve#3, a03-tavern-curve#5; a15 rank 11) Tavern curve refresh: update the calibration cells to the 14-run / 16-session counts (p1 brawls r3-r10 median 5, 3 no-brawl; Greta r1 3/5 in 13 of 16); file watch/inbox/TAVERN_CURVE_AUDIT_20261003.md with the brawl table; fire one labeled pressure-0 scenario and 2 more pressure-2 runs.

First alternate (a15 rank 12, one sitting): (a09-grok47#0, a09-grok47#1, a09-grok47#2) interference amendment erratum naming the rates-times-30 figures and the self-contradicted fail sentence, recover the integer solve counts from Arm B logged rounds, and run the W4 preflight (A1 model-field assert + A2 writer fixture) before Arm C launch. Further alternates, register ranks 16-17: the golden-vector pre-push check (a11-commits#3) and the credential-shape pre-push scan (a11-commits#4); plus the last-seal-vs-bytes patrol check (a12-ractor-legs#3).

Held pending the operator rulings in D3 and D4 (not GO): the PRIORS row 8 scoping amendment and the $0.001 deepseek thinking-default A/B.

## 10. Fold seat attestations

- Read this fold: `memory/runs/mickey17_v2/runs/run-0/FOLD_SECTIONS.md` (all 66 lines; byte-matches the gate output quoted to this seat) and all 15 lane JSONs (a01-a15) at `memory/runs/mickey17_v2/runs/run-0/lanes/`, in full; the prior fold's 237-line master at this path, in full, before overwriting (its GO-item numbering is preserved where the lanes cite it).
- Ran this fold (`carried`, exact commands): (1) verdict walk over all 15 `.checks.json` with `C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe` (recursive `verdict`-field walk) -> deep_tier2 16 = 15 verified / 1 unconfirmed (a08-rails-laws r9), matching the script's deep_tier2 16; (2) supports count over the same files -> 75 supports = 12 yes / 63 no (per-lane yes: a01 1, a07 4, a09 1, a12 3, a15 3); (3) row recount from the lanes' `rows` arrays -> 94 across 15 lanes (a01 8, a02 5, a03 7, a04 7, a05 10, a06 5, a07 5, a08 10, a09 5, a10 5, a11 5, a12 5, a13 5, a14 7, a15 5), matching the script.
- Not run: no pytest, no citation_lint, no re-execution of any lane instrument, no fresh URL fetch. The tier-1 and tier-2 verdicts are the run's persisted results, consumed as given (re-counted, not re-graded); verification belongs to the lanes and the tier-2 checker, not the fold.
- Transfer note: this document lands in corpus/steal and folds the refire deltas the prior fold predates (a15#0's 13-marker grep battery now has a home), which partially cures the transfer meta-gap; the LINKS rows and the percolator fire remain the one-wave leg (GO list's wave-sized residue, N9).
