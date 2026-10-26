# TICKET LEDGER - the redemption denominator, row zero (2026-10-01)

The elder-lens question (DAY1_SKILLS_DOGFOOD.md section 3): across the waves, how many
tickets were ISSUED, how many were RUN, and where is the count of the DROPPED ones? Nothing
owned that count. This file is the instrument's first row. Scope of row zero: today's three
named sources only (T1W1_RACTOR.md TICKETS + TO-VERIFY sections, DAY1_SKILLS_DOGFOOD.md owed
lists, LAST_MILE_AIM.md remainder). Wider waves (T1-T6 dig tickets, V1-V5 of other files,
DUEL lanes, WINDOW1 owed items) are out of scope for row zero and named as the widening step.

## THE PROBE (re-runnable)

Instrument: literal Read of the three source files plus grep id-sweeps, this sitting.
Moment: 2026-10-01T21:2xZ. The tree is MOVING (the descent driver is live; four of the RUN
rows below land in this very sitting), so any recount will drift: per the census denominator
law (B2-216), name instrument, moment, and delta before comparing two counts. Commands:

    grep -n "^### L\|^- V\|EASY -\|CLIMB -" watch/inbox/hermes_burn/T1W1_RACTOR.md
    grep -n "LANDED\|PROMOTED\|untouched" watch/inbox/hermes_burn/T1W1_RACTOR.md
    grep -c "^| V" watch/inbox/hermes_burn/T1W1_TOVERIFY_VERDICTS.md
    grep -n "Owed from this dogfood" -A 8 watch/inbox/hermes_burn/DAY1_SKILLS_DOGFOOD.md
    grep -n "WHAT REMAINS" -A 10 watch/inbox/hermes_burn/LAST_MILE_AIM.md

## FIRST CENSUS

| Source (block) | Issued | Run | Parked/open | Dropped | Notes |
|---|---|---|---|---|---|
| T1W1_RACTOR.md TICKETS (numbered) | 14 (9 EASY + 5 CLIMB) | 8 LANDED (2,3,4,7,8,9,11,12) | 6 (5 CLIMB untouched as ordered + 1 promoted-to-CLIMB pending policy call) | 0 | BUILD REPORT section is the run receipt; #1 was triaged, not run |
| T1W1_RACTOR.md TO-VERIFY (V1-V16) | 16 | 16 (5 settled in-file: V1 CONTRADICTED, V2-V5 RESOLVED TRUE; 11 by the verify lane: 8 VERIFIED / 2 REFUTED / 1 UNDECIDABLE) | 0 | 0 | T1W1_TOVERIFY_VERDICTS.md is the run receipt |
| T1W1_RACTOR.md carrier-patch rows (C1-C3) | 3 | 3 LANDED same sitting | 0 | 0 | Minted inside the BUILD REPORT, not the TICKETS section; 21 tests |
| DAY1_SKILLS_DOGFOOD.md owed list | 5 | 4 (items 1-4: bibliography row, skill ledger v1.3, board runway, this denominator probe; all land this sitting ~21:2xZ) | 1 (item 5: refire 6 empty-evidence duels) | 0 | Items 1-4 are the four one-sitting items this lane executes |
| LAST_MILE_AIM.md remainder (unique items) | 11 | 1 (driver heartbeat W2-L5, lands this sitting) | 10 (DG1 ractor turn; T1W2 evidence attach + refire; coordinator commit; standing owed 7: 4 v4 fixtures, memlance witness, quant tag, V12 .bak cleanup, V15 sid design, Godot precompile) | 0 | DG1 ASK itself landed (DG1_moe_mating_door.md exists) and DAY1_CROSS_RACTOR banked a law row on it; the dedicated ractor turn is the open part |
| DEDUP: cross-source repeats excluded | 5 excluded | (counted once above) | | | The 4 one-sitting items appear in BOTH DAY1 (items 1-4) and LAST_MILE ("one-sitting owed"); the 6 duel refires appear in BOTH DAY1 item 5 and the LAST_MILE remainder |
| TOTALS (unique) | 49 | 32 (65.3 percent) | 17 | 0 | 32 + 17 = 49 reconciles |

## HONEST CAVEATS

1. What counts as ISSUED differs by source. T1W1 tickets carry stable ids (numbers, V-ids);
   the DAY1 and LAST_MILE owed items are prose bullets without ids. Prose bullets are the
   weak denominator: a recount cannot grep them reliably and drift is invisible. Widening
   step: assign ids at mint time (the EASY/CLIMB and W2-L patterns already do).
2. Double-counting is real and handled only by hand here: 5 cross-source repeats excluded
   (the 4 one-sitting items, the duel refires). Further overlap axes NOT deduped because
   they name different actions on the same defect: V15 sid-binding (LAST_MILE standing owed)
   vs T1W1 CLIMB ticket 13 (same defect, build ticket vs design note); V12 .bak cleanup vs
   law L9 rotation debt (cleanup vs rotation); Godot precompile also appears as WINDOW2
   door 5 (outside the three sources, not counted here at all).
3. Parked is not DROPPED. The 5 CLIMB tickets are deliberately deferred ("untouched, as
   ordered"); counting deferral as loss would fabricate a leak. A true DROPPED count needs a
   graveyard convention: a ticket declared dead WITH a receipt naming why. Row zero found
   zero explicit drops in scope; the honest statement is "dropped-count unknown, no drop
   receipts exist to count", which is itself the instrument's finding. DG1's kill verdict
   (naive mating-to-MoE DEAD) is a landing, not a drop.
4. RUN means a completion receipt exists in bytes (a LANDED row, a verdict-table row, or
   this sitting's file edits). Four of the 32 RUN rows are landing concurrently with this
   census; a later recount sees run-count rise and parked-count fall as normal drift, not
   error. (Also: run does not imply independently verified, except the V-rows where a second
   instrument verdicted them.)
5. Out of scope for row zero, deliberately: WINDOW2_RACTOR DOORS (6 open doors, one of which
   IS the heartbeat landed here), MOVEMENT2_CHEAP_ANSWERS tickets (dogfood says 2 of 3
   settled), D1/D2/D3 dig tickets (the T1-T6 class), DUEL verdict tickets, WINDOW1_STATE
   owed items. A full-widening census greps for the id families across watch/inbox/.
6. Falsifier of this instrument (inherited from elder-lens): if a receipt already counting
   ticket redemption across waves exists, this ledger retires. The dogfood's grep and this
   pass found none in scope.

## ROW ZERO VERDICT

Issued 49 / Run 32 / Parked 17 / Dropped 0-known. Redemption rate 65.3 percent on day one,
with the parked tail dominated by deliberate CLIMB deferrals and standing (cross-day) owed
items, not by silent loss. The number to watch is not today's rate but whether PARKED rows
across future rows convert or silently age: the aging view (parked rows by mint date) is the
next column this instrument needs, and it only exists if future waves append rows here.

Append convention for future rows: one table row per wave/sitting, same five columns, moment
named, repeats deduped by id where ids exist.

---

## REDEMPTION RUN (2026-10-01, redemption lane, ~22:0xZ)

Mission: actually RUN un-run EASY tickets from T1W1_RACTOR BUILD REPORT, DAY1_SKILLS_DOGFOOD
owed lists, and LAST_MILE_AIM remainder. T1W2 evidence attaches and the 6 paid duel refires
are other lanes' (skipped as ordered; the duel refire is also a spend, not a one-sitting edit).

Tickets executed one at a time, each probed with the narrowest pytest before the next
(instrument: .venv/Scripts/python.exe -m pytest <file> -q -p no:cacheprovider).

| # | Ticket | Source receipt | Verdict |
|---|---|---|---|
| R1 | test_grounding_wave_v4.py test_full_ladder_in_view + shared _corroborated_row helper upgraded to lineage-prefix seats (alpha/a author, beta/b + gamma/c hands, zeta/z voider) | LAST_MILE standing owed "4 v4 fixtures"; ebe4e147b commit owed line | LANDED-with-test: 1 passed narrow, file-wide 26 passed |
| R2 | test_corroboration_needs_two_distinct_non_author_seats upgraded to lineage semantics: same-lineage two-instance pair (beta/b1 + beta/b2) stays RECORDED, second lineage (gamma/c) corroborates | same | LANDED-with-test: 1 passed narrow |
| R3 | test_verify_reports_admission_summary ("1 corroborated" summary) | same | LANDED-with-test (rode the R1 helper): 1 passed |
| R4 | test_false_premise_void_propagates_chain_visible premise/descendant alpha/f, witnesses beta/b + gamma/c, void zeta/z cross-signed beta/b | same | LANDED-with-test: 1 passed narrow |
| R5 | NEW, minted in-sitting: test_corroboration_blocked_by_failing_warrant was passing VACUOUSLY after the lineage law (unprefixed seats can never corroborate, so the warrant gate was untested); upgraded to alpha/a + beta/b + gamma/c so it exercises the warrant block | discovered during R1-R4 (same defect class as the owed fixtures) | LANDED-with-test: asserts RECORDED under two distinct lineages with warrant exit 1 |
| R6 | Arditi et al. 2024 row onto docs/ref/BIBLIOGRAPHY_MAP.md | DAY1 owed item 1 (law 18 teeth) | ALREADY-LANDED by a concurrent lane, verified at bytes this sitting (BIBLIOGRAPHY_MAP.md:134 carries the full row citing C1_censorship_ASSEMBLED.md and this owed item); no duplicate written |

Concurrent-landing verifications (row zero claimed these as RUN at ~21:2xZ; this lane
confirmed each in bytes, no recount change): Arditi row (R6 above), ractor-essay SKILL.md
v1.3 ledger amendment (.agents/skills/ractor-essay/SKILL.md:24 and the version ledger:55),
WAVE24_BOARD HONEST-RUNWAY section (WAVE24_BOARD.md:80, naming owed row 3), and this ledger
itself (denominator probe, owed item 4). Not re-verified by this lane: the driver heartbeat
W2-L5 (row zero's RUN claim; no direct grep hit in scripts/descent_driver.sh, out of this
lane's scope, flagged here rather than silently trusted).

Test evidence (moment ~21:5x-22:0xZ): tests/test_grounding_wave_v4.py 26 passed (was 22
passed / 4 failed at sitting open; the 4 failures were bisected to HEAD bytes by the T1W1
build lane, i.e. the lineage law ebe4e147b landed without its owed fixtures). Regression:
test_grounding_witness_binding + test_grounding_wave_presence 21 passed; broad grounding
family + test_t1w1_ractor_fixes 71 passed. Em-dash check: git diff on the test file adds
zero U+2014 (the file's 7 pre-existing ones untouched).

### Count update (row one)

Row zero: issued 49 / run 32 / parked 17 / dropped 0-known.
This sitting: 4 parked v4-fixture tickets converted to run; 1 new ticket (R5) minted and
run in-sitting (enters both columns); R6 verified already-run (no change, already counted).
Row one: issued 50 / run 37 / parked 13 / dropped 0-known. Reconciles: 37 + 13 = 50.
Redemption rate 74.0 percent (was 65.3). Remaining parked in this ledger's scope: 5 T1W1
CLIMB tickets (deliberate), memlance witness (waits on next-window boots), quant tag
research, V12 .bak cleanup (operator), V15 sid design (CLIMB), Godot precompile (CLIMB),
and the 6 duel refires (paid, another lane). No new drops; no promotions to CLIMB (no
executed ticket hid a design question).

## REDEMPTION RUN 2 (2026-10-02, night lane, ~05:3xZ)

Mission (night orders): next EASY tranche = SW1 tickets (SWARM_1.md minted
table) + the SELFSTEAL_53_ERA five one-sitting upgrades. All code landed with
tests; instrument: tests/test_sw1_tickets.py 17 passed; regression sweeps
- k "code_swarm or swarm" 53 passed, - k touched-module keywords 23 passed.

| # | Ticket | Source receipt | Verdict |
|---|---|---|---|
| SW1-01 | ocean_v2_pilot COST_CAP enforcement (cap_ok gate + aborted_at_cap receipt flag) | SWARM_1.md row 1 | LANDED-with-test |
| SW1-02 | roblox_npc_gateway DNS-rebind TOCTOU (validated-IP pin, SNI/Host/cert on hostname) | SWARM_1.md row 2 | LANDED-with-test |
| SW1-03 | reverse_map stable key rotation (sha256 sid:attempt) | SWARM_1.md row 3 | LANDED-with-test |
| SW1-04 | preload_selector suffix-aware pick_model + refuse fallthrough | SWARM_1.md row 4 | LANDED-with-test |
| SW1-05 | desk_model_probe FROM-verification fail-closed (first half, suffix _has_model, was pre-landed; pinned by test) | SWARM_1.md row 5 | LANDED-with-test |
| SW1-06 | handoff watcher canonical seen format, no 200-id truncation | SWARM_1.md row 6 | LANDED-with-test |
| SW1-07 | tier_probe warm-up tokens counted (row.warm) | SWARM_1.md row 7 | LANDED-with-test |
| SW1-08 | task_wall lane contract settled + run-window done count | SWARM_1.md row 8 | LANDED-with-test |
| SW1-09 | gpu_ghost shared telemetry_allows_local policy (None no longer blocks local) | SWARM_1.md row 9 | LANDED-with-test |
| SW1-10 | gopher_lite guarded choices parse + sized est_tokens + loop-cycle guard | SWARM_1.md row 10 | LANDED-with-test |
| SS53-5 | code_swarm family_behavior_fold at rollup close (family_behavior.v1 ledger + unique-share economics; 429/token/cost legs NAMED not-wired) | SELFSTEAL_53_ERA top-5 #5 | LANDED-with-test |
| SS53-1 | tier-2 auto-adjudication in rollup | SELFSTEAL_53_ERA top-5 #1 | PROMOTED: fires paid blind asks, not a night-lane one-sitting |
| SS53-2 | self-fed staging + ticket promotion | SELFSTEAL_53_ERA top-5 #2 | PROMOTED: touches the ask pipeline the descent driver is actively firing |
| SS53-3 | revision turn-2 heal | SELFSTEAL_53_ERA top-5 #3 | PROMOTED: same ask-pipeline contact |
| SS53-4 | per-family width lanes + burst decay | SELFSTEAL_53_ERA top-5 #4 | PROMOTED: ~60-line concurrency rewrite, not a one-sitting |

### Count update (row two)

Row one: issued 50 / run 37 / parked 13 / dropped 0-known.
This sitting: 10 SW1 tickets + 1 SELFSTEAL upgrade converted to run; 4
SELFSTEAL upgrades PROMOTED (counted parked, with promotion receipts above;
they are CLIMB-class by evidence, not silently aged). New denominator rows
enter both columns: SW1 x10 and SS53 x5 were minted by earlier receipts but
are NEW to this ledger's denominator (row zero scoped only three sources).
Row two: issued 65 / run 48 / parked 17 / dropped 0-known. Reconciles:
48 + 17 = 65. Redemption rate 73.8 percent (row one 74.0; the fall is the
four promotions, not losses). No new drops. Line-ending note: five tool
files were normalized back to their HEAD endings after edit-tool CRLF churn
(reverse_map restored to its native CRLF); diffs are content-only.

## ROW THREE (2026-10-02, boot seat, the dogfood-48h moves)

| # | Ticket | Source receipt | Verdict |
|---|---|---|---|
| DF48-1 | atomic per-ask O_EXCL claim + doubled-key ingest alarm | watch/inbox/ractor_engine/2026-10-02-dogfood-48h/SYNTHESIS.md move 1 | LANDED-with-test (tests/test_instance_guard.py 9 passed; receipt watch/inbox/instance_guard_20261002.md) |
| DF48-4 | instance guard swept to 5 surfaces + 2 stale pidfiles purged | same, move 4 | LANDED-with-test (same battery; ratchet PASS after 3 except-pass fixes + 1 named acceptance) |
| DF48-2 | descent driver bounce under guarded script | same, move 2 | EXECUTED (44072 exited via DRIVER_STOP ~48s; relaunch pid 86854, pidfile written, second launch refused exit 3, beat cycle 1 at 12:50:05Z) |
| DF48-CQ | the commit-queue law named OWED in commit 2093ca518's message but ticketed nowhere | lineage finding, dogfood-48h run | TICKETED HERE (the law itself stays prose-owed until an owner words it; this row ends the ticketed-nowhere half) |

Row three notes: the 12:47Z syntax-error launch in driver.log (a torn read of
descent_driver.sh mid-03:28-edit, source launch unattributed) joins the
standing unattributed-launch OWED class from the ractor run. The relaunched
driver (86854) is session-parented via nohup: money-safe by the guard + ask
claims, liveness tied to the boot seat's session; next boot-lane start owns
it properly.
