# MASTER FOLD - MICKEY-17 v2.1 READ-THE-ESTATE (run 2026-10-04-0)

**Fold provenance.** 12 lanes fired, 12 landed (casualty header below, script-computed). The fold gate's counting script produced `memory/runs/mickey17_v2/runs/2026-10-04-0/FOLD_SECTIONS.md` from the lane archive at `memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/`; every scripted number in sections 1-5 is verbatim from that file. Lane prose in sections 6-9 is folded from the 12 lane JSON files and their `.checks.json` verdicts in the same archive. Any number the fold seat brings itself is tagged `carried`. Every steal sentence carries lane id + row index. Folded 2026-10-04.

## 0. How to read this fold

- Row addresses: `lane#N` indexes the lane file's `rows` array, 0-based. `r04#1` is the second row of `r04-estate-index-anatomy.json`.
- Tier-1 (persisted lane checks, `.checks.json` per lane): does the row's quote alone entail its claim? The fold-gate payload grades 60 rows: 12 yes / 48 no (`carried`, mirrored in the lane checks files). Per r12's checks census, the no's are overwhelmingly quote-narrower-than-claim (the checker demands the quote alone carry every conjunct; lanes verified extra conjuncts with their own cross_checks), not mass fabrication; exactly ONE true quote-claim contradiction was found estate-wide (r07#1, DISPUTED D2).
- Tier-2 (deep checks, independent instrument re-runs): 12 rows sampled estate-wide, 7 verified / 5 unconfirmed. Unconfirmed rows carry their measured corrections in the DISPUTED tier (D6-D10) and in the Standing Numbers block; the corrections rule, the original counts do not.
- The fold seat read all 12 lane files plus FOLD_SECTIONS.md this sitting; it did not re-run lane instruments. Tier-2 verdicts are carried from the fold-gate payload's deepChecks records.

## 1. CASUALTY HEADER (script, verbatim)

- fired: 12
- landed (parseable files): 12
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): 0
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## 2. SCOREBOARD (script, verbatim)

- rows: 60
- estate_status: new 24, confirms-ours 15, we-have-better 11, owed 8, green-solved 2
- leverage: high 34, medium 24, low 2

## 3. FIDELITY / VERIFIER TABLE / WIDTH-ECONOMICS (script, verbatim)

### FIDELITY

- rows with all of quote/source/steal/estate_status non-empty: 60/60 (100.0%)

### VERIFIER TABLE (persisted verdicts)

- lanes with persisted checks: 12
- verdicts: checks 10, deep_tier2 12, entries 5, supports 45

### WIDTH-ECONOMICS

- rows/lane: median 5, max 5, min 5
- top-10 lanes share: 83.3%
- exact cross-lane duplicate quotes (normalized): 2
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

## 4. PRISMA FLOW (script, verbatim)

- identified: 60
- screened: 60 (all rows carry the six rubric fields or their gap notes)
- excluded: 0
- included: 60
- invariant: identified == included + excluded **HOLDS** (60 = 60 + 0)

## 5. URL LIVENESS (script, verbatim)

- unique URLs: 0; fetched: 0; skipped non-public: 0; live: 0; dead/blocked-status: 0

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

## 6. TOP STEALS (script TOP-K, 12 rows; each with its quote and its one-sitting action)

The script's TOP-K is authoritative; a lane-claimed top steal outside this list files as DISPUTED. Tier-2 verdict lines carry the checker's measured corrections where they exist.

### TS-01. r01#0 [high, new] - The AH14 corr_id join field is a phantom on its primary surface

- Claim (r01-steps-jsonl#0): 18,546 steps rows carry the key since onset 2026-09-30T12:06:08Z and every one is null (writer reads env MAG_CORR_ID only, mag/trajectory_step.py:71-73); FLOW_LEDGER.jsonl is 0/205 non-null while logs/duel/duels.jsonl is 19/80 non-null: the join works on one of three surfaces and joins to nothing. Mechanism labeled inference: the hook runs in the harness process env so a lane-shell export never reaches it.
- Quote: "corr_id, a uuid4 hex8 minted at lane start and carried in the MAG_CORR_ID env var. Seats/lanes that export the var join automatically; unset -> null."
- Action (r01#0): One sitting: locate the dwf actor spawner (rg 'SEED.json' mag tools), inject MAG_CORR_ID=<run-uuid> into the child env at spawn, re-census the null rate on next run, land receipt in watch/inbox/.
- Verdict: tier-1 no (the quote carries the mechanism clause only; the counts live in the lane's own instrument runs); tier-2 not sampled.

### TS-02. r01#3 [high, new] - A working join into the giant already exists and has never been computed

- Claim (r01-steps-jsonl#3): 2,107 worldline actor dirs across 98 runs key on the exact steps.jsonl session_id minus its 'sess_' prefix (SEED.json carries session_id + sha256 slab manifests of the genome the actor was seeded with), while REGISTRY.jsonl (85 rows) joins to ZERO of the 113 distinct dwf-dwfrun uuids the stream records.
- Quote: `"session_id": "dwf-dwfrun-038cd25b-98de-47fd-b600-3102622adcae-actor_1_11",`
- Action (r01#3): One sitting: pick one dwfrun uuid, join its steps.jsonl rows (strip 'sess_') to its worldline SEED.json slabs, diff intended-vs-executed commands, land a fidelity receipt under memory/worldline/ or watch/inbox/.
- Verdict: tier-2 VERIFIED, two named deviations: the live stream recorded 114 distinct dwf-dwfrun uuids at the checker's moment (claim's 113 is plausibly its claim-time count); 'never been computed' is a negative the checker bounded but could not exhaustively prove. Join semantics, 2,107 dirs / 98 runs, SEED slab manifests, and the zero REGISTRY join all byte-verified.

### TS-03. r02#0 [high, green-solved] - The queue drain verb landed and its adoption clause actually executed

- Claim (r02-nightburn-unread#0): the index this receipt left at 3 closed now reads 39 closed / 3 open / 8 superseded, with Q-005 and Q-025 closed today 2026-10-04T08:30:26Z citing receipts verified on disk.
- Quote: "39 open / 8 superseded / 3 closed of 50. The drain now exists; the triage half (roam verdicts) and the drain half (this verb) complete the LINKS-328 pattern."
- Action (r02#0): Adopt the RECEIPT_BINDINGS literal-table shape (close evidence resolves only from a hardcoded row-to-path table, so runtime cannot point the verb at unregistered files) for the next destructive ledger verb; landing spot: tools/ queue-adjacent verbs, one seat one sitting.
- Verdict: tier-2 VERIFIED (quote byte-exact at watch/inbox/QUEUE_CLOSE_VERB_20260927.md:14; tools/queue_close.py exists, 18,029 B; live index reads exactly 39/3/8 of 50; Q-005/Q-025 closed_ts 2026-10-04T08:30:26Z with receipts on disk and zero missing close_receipt paths across all 39 closed rows).

### TS-04. r03#0 [high, new] - Playbook law 14 (fifty-wide wave archive) landed as two real tools, convention-enforced only

- Claim (r03-corpus-founding#0): tools/fifty_wide_archive.py and tools/fifty_wide_guard.py plus smoke dir smoke_20261004_archive_convention exist, but workflow_gate.py carries zero 'fifty' references, and the replay pair's first half memory/runs/fifty_wide/dispatch_log.jsonl does not exist on disk, so no production wave has ever banked a guard row.
- Quote: "The replay pair is the guard's `dispatch_log.jsonl` row (pre-flight, `tools/fifty_wide_guard.py`) plus the agents dir (post-wave); either half alone cannot explain a count gap, and the 2026-10-03 burn wave lost 10 units with neither half on disk"
- Action (r03#0): On the next real width>=5 wave, run tools/fifty_wide_guard.py pre-flight and tools/fifty_wide_archive.py post-wave so dispatch_log.jsonl gets its first production row; landing spot memory/runs/fifty_wide/dispatch_log.jsonl.
- Verdict: tier-2 VERIFIED in all parts (tools exist with Oct 4 mtimes, smoke dir real, workflow_gate.py zero 'fifty' hits, dispatch_log.jsonl absent estate-wide except pytest fixtures).

### TS-05. r03#1 [high, new] - All five TETHERED_LINK 'Laws adopted' (width, off-peak, owner, tether, retry) are prose-only with zero code enforcement

- Claim (r03-corpus-founding#1): zero 'max_concurrency' hits in tools/*.py and mag/*.py, zero 'tether' and zero 'off-peak' hits across the rib vault, zero 'Tether law' hits in watch/inbox; the law survives only in AGENTS.md bullets plus corpus receipts.
- Quote: "**Width law:** on the coding-plan account, dispatch fan-outs at `max_concurrency` 3 or less. 50-wide is an off-peak, dedicated-account luxury."
- Action (r03#1): One seat, one sitting: add a workflow-child dispatch-shape card (max_concurrency <= 3) to tools/workflow_gate.py plus its scenario card in configs/workflow_gate_scenarios, converting the width law from AGENTS.md prose to a submit-time gate.
- Verdict: tier-2 VERIFIED with errata the fold adopts as the standing numbers: '11 days after filing' is 9 days (receipt dated 2026-09-25, file mtime Sep 26); the rib dir holds 57 files (52 .md + 4 .json + 1 .jsonl), not 55, zero-hits holding across all 57; the prose-carrier enumeration is under-inclusive (several more prose receipts carry the width law, all prose/receipt, none harness code); mag/offpeak.py implements an off-peak defer for the DeepSeek pricing law, not the TETHERED_LINK law. Prose-only, zero code enforcement: stands.

### TS-06. r04#0 [high, new] - Fresh full-census cross-check: the index is 4,150,418,528 bytes / 10,661,260 rows, one keyset, snapshot-rewrite writer

- Claim (r04-estate-index-anatomy#0): exactly ONE keyset of 9 fields, 0 bad rows, 0 empty lines, max line 510 B, avg 389.3 B; grew +1,857,661 rows from the sibling's same-day 8,803,599-row pass; the writer is a snapshot rewrite (projects_index.py:107 mode 'w', :103 mtime-desc sort), so growth is walk-scope growth, not append.
- Quote: `"ts": "2026-10-04T18:28:51Z",\r\n "total_files": 10661260,`
- Action (r04#0): Run the sibling-specified tools/estate_index_compact.py --check today while the file is 4.15GB and land its measured projection table in watch/inbox before the next 09:00 scheduled walk re-fattens both copies.
- Verdict: tier-2 VERIFIED (the checker re-ran the full 4.15 GB streaming parse in 96.5s, byte-exact on every number; writer snapshot-rewrite read in code at tools/index/projects_index.py:107/:103/:138; delta proven from git HEAD's prior run record). Caveat adopted: the two runs are 28h29m apart, so 'one day' is approximate.

### TS-07. r04#1 [high, confirms-ours] - The skip list is arithmetic, not judgment (tier-2 unconfirmed: carry the corrected arithmetic)

- Claim (r04-estate-index-anatomy#1): 9,524,538 of 10,661,260 rows carry ext ".source"; one excluded root retires ~89% of the artifact.
- Quote: `{"path": "local_sovereign_agent\\.mimosa\\hook-state\\sess_dwf-dwfrun-1759540b-18c1-4904-ae1d-e1c81a940895-actor_4_21.musnghar-37692-177332149b.baseline\\355add8b5ec7a8eb102fe124e26498f70715b64b185f9837c68f6026c100f80f.source", "proj": "local_sovereign_agent", "rel": "body file", "mtime": "2026-10-01T09:09:34Z"` (byte-exact prefix of the full row)
- Action (r04#1, conditioned per DISPUTED D10): Make the operator decision (sibling design decision point 1) that the .mimosa hook-state subtrees, including the '_mimosa' sibling lane, enter the walk exclusion list, and land it in the same commit as the sqlite spine in tools/index/projects_index.py, never as a follow-up. A single-root exclusion retires 86.01%, not ~89%.
- Verdict: tier-2 UNCONFIRMED (D10): hard counts exact (10,661,260 rows, .source 9,524,538, 4,150,418,528 bytes, peak days 2026-08-05 = 2,933,239 and 2026-09-05 = 1,967,164, median 5,000 files per session dir); the row's load-bearing universal 'ALL of them resolve under local_sovereign_agent\.mimosa\hook-state\' is contradicted (96.27% named root, 3.68% proj '_mimosa', 0.06% other nested copies), and 89.4% mis-rounds its own fraction (89.3378% -> 89.3%).

### TS-08. r04#2 [high, confirms-ours] - The 09-30 mirror pointer dedup is dead again: two independent 4.15GB files, 8.3GB live duplication

- Claim (r04-estate-index-anatomy#2): fsutil hardlink list on each ESTATE_INDEX path returned only that path itself; mtimes 18:28:25Z master / 18:29:05Z dashboard copy, one writer run ~40s apart; both git-tracked at the same 2,523,006,985-byte blob cb136109; the receipt's section-5 prediction byte-proven a second time: any mirror cure not shipped inside the writer is scheduled litter.
- Quote: "producer writes BOTH the dashboard copy and the watch mirror. If its next run re-materializes"
- Action (r04#2): Amend tools/index/projects_index.py:138 to stop the full shutil.copyfile (write the dashboard side as a pointer or drop it) in the same sitting that lands estate_index_compact.py --apply, then rerun tools/estate_index_dedup.py --check the next morning as the tripwire.
- Verdict: tier-2 not separately sampled; CONFIRMED by the r12 rollup's independent fsutil re-run (each path lists only itself, both 4,150,418,528 bytes), recorded in r12-rollup.json greps_run_this_lane.

### TS-09. r04#4 [high, confirms-ours] - Migration verdict: adopt option D (sqlite spine + skip list); relieve the worst reader first

- Claim (r04-estate-index-anatomy#4): full DDL, incremental upsert path, backfill with row-parity gate and sha256 bank, and the reader cutover in cost order, R2 worst first: the_index.html:118 fetch() downloads the whole 4.15GB through the raw server.py:624 /data door.
- Quote: `fetch("/data/ESTATE_INDEX.jsonl", { cache: "no-store" })`
- Action (r04#4): Build /api/v1/estate/query in dashboard/server.py (LIMIT-capped SQL over the new sqlite, ?proj=&rel=&temp=&limit=) and repoint the_index.html:118 to it in one sitting; it needs no writer change and relieves the worst reader immediately.
- Verdict: tier-1 no (the quote is the door line only); tier-2 not sampled.

### TS-10. r05#0 [high, we-have-better] - The largest recorded failure in the trail corpus is one uncured exception family (tier-2 unconfirmed: use 910, not 917)

- Claim (r05-trails-deep#0): one uncured OSError Errno 22 family across the trails, named by day_work TESUJI drops on Sep 14-16 and still failing today (96 builder fails on Oct 4 alone).
- Quote: "EXC OSError: [Errno 22] Invalid argument: '/app/queue/lanes/builder/runner_state.json'"
- Action (r05#0): One seat, one sitting: diff the cage lane_runner's runner_state write against BOARD_REPAIR_INCIDENT_20260926's concurrent-writer diagnosis (same errno class, ruled a two-writer artifact there), single-writer-guard or path-fix it once; land the cure receipt in watch/inbox/ beside BURNDOWN_20261004.md.
- Verdict: tier-2 UNCONFIRMED (D6): quote byte-exact 370x in builder.jsonl (first 2026-09-14T13:53:07Z, last 2026-10-04T12:05:48Z); the qualitative core verified (910 of 939 EXC rows across 12 trails are OSError; TESUJI naming Sep 14-16 verified; 96 builder fails on Oct 4 exact); the stated quantities struck: 917 is 910 (builder 370, research 513, night 26, prose 1, day_work 0, its OSError lines being TESUJI prose relays), and the rows are identical only within each trail (4 distinct target paths). HEAD equals the working tree, so this is not drift.

### TS-11. r05#1 [high, new] - The elder lens was 429-dead 14 consecutive daily cycles; a literal CR in the Bearer header traced to a CRLF .env (tier-2 unconfirmed: spine verified, two specifics struck)

- Claim (r05-trails-deep#1): recovered 2026-10-04T08:20Z after the CR-header failure; the same CRLF disease makes the queue-side trail mirrors byte-diverge.
- Quote: "lane-down: Invalid header value b'Bearer sk-or-v1-41679b3f[REDACTED]\\r'"
- Action (r05#1): One sitting: strip CR at key load (value.rstrip('\r\n') or newline='' on the .env open) in the cage elder runner and normalize trail appends to one EOL; land in the cage runner script plus an incident note next to BURNDOWN_20261004.md.
- Verdict: tier-2 UNCONFIRMED (D7): spine verified byte-exact (14 consecutive daily 429 CYCLE_FAIL rows 2026-09-20T12:00:15Z to 2026-10-03T12:00:10Z with no successful CYCLE between; recovery CYCLE 2026-10-04T08:20:40Z, one minute after the quoted failure; CR-in-Bearer root cause documented at watch/inbox/go_wave_20261004/CSV_VERDICT_20261004.md:33-38; queue-side mirror CR-byte deltas match size deltas on 4 lanes). Struck: '137/137 CRLF-terminated .env' (the root-cause receipt states 136 lines, 0 CRs post-fix; the current .env measures 137 lines with 0 CRLF; no source carries 137/137) and 'only the trail noticing' (seat-salvage-fillball-1001 executed the elder-lens salvage clause 2026-10-02T04:09:37Z, mid-streak). Elder's own mirror is byte-identical; the CRLF divergence afflicts the other four lanes.

### TS-12. r05#2 [high, confirms-ours] - The night march leg failed rc=1 for a month while the monitor leg passed; today's run names the cause for the first time (tier-2 unconfirmed: 28 composites, not 30 consecutive)

- Claim (r05-trails-deep#2): today's run names the cause for the first time (rc=2, .env unmounted by compose, no sanctioned env door), a month-old failure only this trail ever diagnosed.
- Quote: "MARCH SKIP rc=2: no key - /app/.env absent or carries no ZAI_API_KEY_Pro/ZAI_API_KEY (cage: .env unmounted by compose; no env door sanctioned)"
- Action (r05#2): One sitting: mount .env read-only into the cage compose or pass the two ZAI keys through the sanctioned env door, rerun the march leg, and bank the rc=0 receipt in queue/lanes/night/surface.md.
- Verdict: tier-2 UNCONFIRMED (D8): quote byte-exact at night.jsonl line 57 (2026-10-04T08:50:01Z); confirmed: the 22-row crash loop Sep 29 (23:01:11Z-23:51:01Z, all errno-22 on the night runner_state), today's first cause-naming anywhere (rc flips 1->2 at row 57; first cause-bearing scheduler line at logs/lane_scheduler.log:9941, 08:50:08Z), month-old (first failure Sep 4). Struck: '30 consecutive nightly composites' (28 composite rows say 'monitor rc=0; march rc=1' spanning 2026-09-05 to 2026-10-03, with a Sep 22 gap; '30' matches only the raw scheduler-log grep, which double-counts 2 truncated tesuji cross-reference lines).

## 7. DISPUTED TIER (10 entries: contradiction pairs, both quotes, conditional rulings; includes all 5 tier-2 unconfirmed rows)

### D1. Hardlink contradiction: LINKS SCHMIDHUBER-REVIEW-AMENDMENT vs current bytes (r04#3; re-confirmed by r12)

- Claim A quote (watch/inbox/LINKS.jsonl, ts 2026-10-04T14:25:24Z): "fsutil hardlink list proves dashboard/data/ESTATE_INDEX.jsonl and watch/ESTATE_INDEX/ESTATE_INDEX.jsonl are hardlinks to ONE physical 3.4GB file"
- Claim B quote (r04#2's counter-evidence, watch/inbox/W3R_EID_DEDUP.md): "producer writes BOTH the dashboard copy and the watch mirror. If its next run re-materializes"
- Ruling (conditional): two independent fsutil runs this sitting (r04 ~18:40-19:20Z; r12 later) each returned only the path itself; both copies measure 4,150,418,528 bytes at mtimes 18:28:25Z / 18:29:05Z. Either Claim A was wrong at write time (14:25:24Z predates the 18:28:51Z writer run) or a later full rewrite broke the link; the break mechanism is not determined and no verdict is offered on intent. Current bytes contradict Claim A's no-duplication conclusion. Action (r04#3): append a dated correction row to watch/inbox/LINKS.jsonl citing the fsutil output and both sizes/mtimes, and fold a hardlink re-verify into estate_index_compact.py --check so dedup arithmetic never trusts a morning's link state.

### D2. Internal quote-claim contradiction: r07#1's 'migrated' conjunct (the run's one true tier-1 contradiction, found by r12's checks census)

- Claim (r07-links-register#1): "a 2026-09-26 schema split made it links-only with 51 event rows migrated to watch/inbox/EVENTS.jsonl."
- Quote (r07#1's own quote): "SCHEMA SPLIT 2026-09-26: LINKS.jsonl is link rows only going forward; the 51 event rows (lines 275-305 scout/seat events, lines 312-331 endpoint-news events) stay in place per the append-only law"
- Ruling: the quote contradicts the 'migrated' conjunct. watch/inbox/EVENTS.jsonl exists (52,596 B, mtime 2026-09-29 06:21, verified by r12) but no byte shows the 51 rows moved; treat 'migrated' as unsupported. Standing condition for readers: cite the split as 'links-only going forward, event rows retained in place per the append-only law'. The row's 422-row count (vs the ask's ~700 premise) is byte-true.

### D3. OPEN: RIB_FREE_USAGE_POLICY_20260823 vs banked instrument rows (r06#2, DISPUTED-tier open 4 days)

- Claim A quote (memory/rib/RIB_FREE_USAGE_POLICY_20260823.md): "Free seats are an OPPORTUNISTIC sensing surface, never a forced workhorse. Use them when they're cool; the moment you try to force them, they throttle into empty (429)"
- Claim B quote (RIB_MODEL_GARDEN_ROUTING.md:192, banked 2026-09-30): "stealth free lanes (as a class) | 459 rows, ZERO 429, 69h+ sustained forced mining | CONTRADICTION OPEN vs RIB_FREE_USAGE_POLICY_20260823 (which says forcing them throttles); resolve with instruments, not by editing either rib silently"
- Ruling (conditional): the policy's throttle mechanism holds only under whatever conditions produced its original evidence; the 459-row instrument class measured zero 429 under 69h+ of sustained forced mining. The routing rib's own resolution order has sat unexecuted for 4 days. Action (r06#2): One sitting: fire the resolving instrument (a forced-width cool/heat re-probe of the stealth lanes), append the verdict row to both ribs and a watch/inbox receipt per the 'resolve with instruments' clause; no silent edit of either rib before the verdict.

### D4. STALE: RIB_INFERENCE_BUDGET_20261001 vs the d4 probe (r06#0; code cured same day, rib unamended)

- Claim A quote (memory/rib/RIB_INFERENCE_BUDGET_20261001.md): "tools/ds_workhorse.py: thinking-off by construction (the harvested seed) and retry-once on empty, but a thinking-on relapse there would re-fire blind: it needs the classifier at minimum."
- Claim B instrument (watch/inbox/go_wave_20261004/d4_thinking_probe.md, 2026-10-04): omitted thinking key = 70 reasoning chars / 18 reasoning tokens on a one-word ask; only explicit thinking:{type:disabled} is off.
- Ruling: the rib row is stale-in-bytes; the law is now 'omission is a MEASURED ON state'. Code cured 2026-10-04 (tools/ds_workhorse.py:88-104 dated erratum + explicit off; mag/inference_budget.py FAMILY_TABLE row 'CORRECTED 2026-10-04'). Action (r06#0): One seat, one sitting: append the POST-DATUM 2026-10-04 amendment block to the rib naming d4_thinking_probe.md + the two cured code sites, per the amend-never-rewrite law the rib itself ships.

### D5. STALE: RIB_MODEL_GATES_20261001 deepseek rail mandates OFF but not HOW (r06#1; second-order conditions-suspect pair rides with it)

- Claim A quote (memory/rib/RIB_MODEL_GATES_20261001.md): "RAIL: THINKING OFF. MANDATORY. Thinking-on: burns entire budget on hidden reasoning, DNFs, socket hangs, word-salad degeneration (AH10 byte-confirmed)."
- Claim B instrument (d4 settlement, banked as POST-DATUM at watch/inbox/model_garden/PRIORS.md row 8 and watch/inbox/ractor_engine/2026-10-04-parked-decisions/operations.md D3): omission is the ON state; the off-switch must be SENT explicitly via lane config; scoped exception: thinking-on only at depth=design, 32K+ max_tokens, substance-gated.
- Ruling: the mandate stands, the mechanism is now known; the amendment lives outside the rib. Second-order (r06 stale_ribs): RIB_DEEPSEEK_SHOULDERS_20261001 and RIB_DEEPSEEK_ELDER_SEAT both cite 'thinking OFF (row 8, byte-confirmed)' while ds_workhorse ask() omitted the thinking key, so shoulders-era receipts measured through an unmeasured ON default until the 2026-10-04 erratum: conditions-suspect, not struck. Action (r06#1): One sitting: append the D3 scoped ruling to the rib's DEEPSEEK row so the boot-time distillation and the amendment stop living in different files.

### D6. Tier-2 unconfirmed: r05#0 quantity corrections (full record)

- Quote verified byte-exact 370x (builder.jsonl, rows ts 2026-09-14T13:53:07Z to 2026-10-04T12:05:48Z). Measured census: EXC OSError 910 (builder 370, research 513, night 26, prose 1, day_work 0; day_work's 4 OSError lines are TESUJI_DROP prose relays, not failure rows), EXC HTTPError 12, EXC FileNotFoundError 1, over 939 EXC rows on 12 trails. Four distinct target paths, identical only within each trail. HEAD counts equal working-tree counts (git show byte scans), runner-side mirrors match exactly, no 376 state ever present in trail history. Ruling: the row files as 'largest recorded failure family, uncured' with 910/370; 917/376 and 'identical across four trails' are struck. Cure action stands (TS-10).

### D7. Tier-2 unconfirmed: r05#1 two specifics struck, spine stands

- Verified: 14 consecutive daily 429 CYCLE_FAIL rows (2026-09-20T12:00:15Z to 2026-10-03T12:00:10Z, one per day, no CYCLE between; last pre-streak success 2026-09-19T12:00:27Z); recovery CYCLE 2026-10-04T08:20:40Z ('lens on 1 cards'); CR-in-Bearer root cause at watch/inbox/go_wave_20261004/CSV_VERDICT_20261004.md:33-38; queue-side mirror divergence measured as exact CR-byte deltas (bard_ledger 11, day_work 1565, research 2129, builder 1075; dashboard copies 0 CR bytes); elder's mirror byte-identical (0 CR both sides). Struck: '137/137 CRLF-terminated .env' (receipt states 136 lines, 0 CRs post-fix; current .env 137 lines, 0 CRLF; 137/137 appears in no source) and 'only the trail noticing' (line 35 records seat-salvage-fillball-1001 executing the salvage clause and banking a lens 2026-10-02T04:09:37Z mid-streak). Ruling: cure action stands (TS-11); quote the spine numbers above.

### D8. Tier-2 unconfirmed: r05#2 count clause struck, diagnosis narrative stands

- Verified: 29 composite rows in night.jsonl, 28 saying 'monitor rc=0; march rc=1' (2026-09-05 to 2026-10-03), monitor rc=0 on all composites; Sep 22 absent from both the trail and logs/lane_scheduler.log (other lanes ran that day). '30' matches only the raw grep of the scheduler log, which double-counts 2 truncated tesuji cross-reference lines (Sep 7, Sep 15); git versions of the trail hold 28/28/26, never 30. Confirmed: 22-row crash loop Sep 29 23:01:11Z-23:51:01Z (all errno-22 night runner_state) followed by a march rc=1 composite at 23:53:23Z; row 57 is the only cause-naming row (march rc 1->2); first cause-bearing scheduler line 9941 at 2026-10-04T08:50:08Z; month-old (first failure Sep 4, first march rc=1 Sep 5). Ruling: file as '28 composites over Sep 5 to Oct 3 with a Sep 22 gap'; '30 consecutive' is struck; the env-door cure stands (TS-12).

### D9. Tier-2 unconfirmed: r05#3 the 160-char clip constant is a cross-lane transposition (row not in TOP-K, filed here)

- Claim (r05-trails-deep#3): the research trail is 84 percent MONITOR spool rows (3030 of 3610) since its narrative stopped Sep 19; intake_card/self_steal last fired Sep 6; zero recorded downstream consumption; detail fields clip mid-word at 160 chars.
- Quote: "monitor_lane rc=0: 32 new items across 4/7 terms (hn=7, arxiv=0, openalex=25); spool watch/scout/MONITOR_LANE_2026-09-04.md"
- Measured: five of six components byte-verified. 3030/3610 was byte-true at an earlier moment the same evening (the checker measured 3037/3618 minutes later on the live file; the 7 newest rows are all MONITOR; ratio rounds to 84% either way). Narrative stop Sep 19 (last GATE_VERDICT 2026-09-19T00:24:58Z); intake_card n=6 last fired 2026-09-06T02:02:32Z, self_steal n=5 last 2026-09-06T05:52:47Z; 60-61 rotation-epoch MONITOR rows (epochs 8->180, all 2026-10-04); zero recorded downstream consumption (caveat: proves the trail never RECORDS one, not that none happened outside the file). Struck: '160 chars' (0 research details are exactly 160 chars; 1,447 MONITOR details embed exactly 250-char windows; the writer is f"monitor_lane rc={rc}: {out[-250:]}" at mag/lane_runner.py:755; 160 is the economist lane's window, mag/lane_runner.py:749). Ruling: the feed-or-kill action stands with the 250 constant: run the owed consumption query over the corpus FTS index, write the rate onto queue/lanes/research/surface.md, feed or kill the lane on the answer.

### D10. Tier-2 unconfirmed: r04#1 universal and percentage corrections (feeds TS-07)

- Verified exactly: 10,661,260 rows, 9,524,538 with ext '.source', 4,150,418,528 bytes, peak days 2026-08-05 (2,933,239 rows) and 2026-09-05 (1,967,164), 191 distinct mtime days, ~5,000 files per session dir (median exactly 5,000, max 5,005, 2,028 session dirs). Contradicted: 'ALL of them resolve under local_sovereign_agent\.mimosa\hook-state\' is false for 355,798 of 9,524,538 .source rows: 9,168,740 (96.27%) under the named root, 350,503 (3.68%) store '.mimosa\hook-state\...' with proj '_mimosa' and rel 'lane (sibling project)', 5,295 (0.06%) under other nested .mimosa copies (watch\ 1,550, _archaeology_out 846, mag\ 846, and smaller). Mis-round: 9,524,538/10,661,260 = 89.3378% -> 89.3%, not 89.4%; one excluded root retires 86.01%; named root + _mimosa 89.29%; all hook-state subtrees 89.34%. Not re-measurable: the historical growth series (590,246,188 B -> 1,945,896,570 B -> 3,409,161,472 B / 8.8M rows), provenance-corroborated only. Ruling: the skip-list thesis stands at ~89% only when the skip covers all hook-state subtrees including the '_mimosa' lane; a single-root exclusion retires 86.01%; quote the corrected arithmetic (conditions carried into TS-07's action).

## 8. NEGATIVE RESULTS (counted reasons table; tombstones: none)

| # | Reason | Count | Where (lane ids) |
|---|--------|-------|------------------|
| 1 | Zero-hit transfer greps: the steal corpus and the rib vault have never ingested the surface | 27-29 zero-hit terms across 12/12 lanes by the Where itemization (29 if r05's trail.jsonl/TESUJI/Errno22 count as three terms, 27 as one probe cluster; r09's five and r08's one are greps by their lanes' own notes, which label them 'Zero-hit greps' and 'ESTATE GREPS'); the prior '21 grep families' headline did not reconcile with its own itemization and is struck | r01 (rib: steps.jsonl, corr_id), r02 (2: queue_close, burn_reset_20260927), r03 (4: rib off-peak/tether, inbox Tether law, code max_concurrency, gate fifty), r04 (2: estate_index in steal and rib), r05 (steal: trail.jsonl/TESUJI/Errno22), r06 (steal cites ribs ~never), r07 (2: all register themes 0 in steal and rib), r08 (curriculum 0/0), r09 (5 graph terms 0/0), r10 (3: card ids, seat_move, evidence ids), r11 (rib: 191.8, attention_feedback), r12 (2: schmidhuber, CURIOSITY_REGISTER) |
| 2 | Ask-premise drift retired by bytes | 6 | r01 (~37k rows stale, live 55,571+), r03 ('7.5 percent cited' unlocatable), r04 (3.4GB stale, actual 4.15GB), r07 (~700 rows, actual 422), r09 (2: '3,804 nodes' splices F13's 09-30 rib_fork census onto the walk file's 713 edges; flash50's byte-size citation rotted +295% in 7 days) |
| 3 | Tier-2 deep checks returned unconfirmed | 5 | r05#0, r05#1, r05#2, r05#3, r04#1 (all carried with measured corrections in DISPUTED D6-D10) |
| 4 | Tier-1 quote-claim contradictions | 1 | r07#1 'migrated' conjunct (D2) |
| 5 | Stale or contradicted law in the rib vault | 4 | r06: FREE_USAGE_POLICY (DISPUTED, open 4 days), INFERENCE_BUDGET (stale, code cured), MODEL_GATES (stale enforcement shape), DEEPSEEK_SHOULDERS + ELDER_SEAT (conditions-suspect, second-order) |
| 6 | Mechanically-alive, output-dead lanes discovered | 6 | r05 extra_findings: economist (sweep pointer frozen 25 days), forge (forged=0 on all 30 daily cycles), harvest (hits=0 for 18 days), bard (39 duplicate appends Sep 29), jev (orphan 6-row ledger, operator adjudication owed), prose (down since 2026-10-04T06:25Z on errno 22) |
| 7 | Phantom or drifted references | 4 | r06: RIB_FRONTIER_ASK_20260929 designed and cited, never minted, no file anywhere; 4 shorthand census strings resolve to SEED_*/DAY1_* receipts, not ribs; rib scatter (4 ribs in memory/runs/ribs/, tools/ouroboros.py points at nonexistent memory/ribs/). r01: duels.jsonl does not exist at the paths the AH14 docstring implies (actual: logs/duel/duels.jsonl) |
| 8 | Tombstones | 0 | fold gate: tombstoned = [] |
| 9 | Coverage bounds honestly stated in lane notes | 12/12 lanes | r02 (2 of ~180 BURN_* files; 1 of 43 B2 receipts), r05 (three big trails read by structure, not line-by-line; night Sep 22 gap unexplained), r08 (1,160-hour and star counters not re-verified), r10 (3,962-line canon sampled; one whole-repo grep stopped early), r06 (citation counts are substring counts), r11 (F6 not ruled, UTF-16 log broke the grep), r07 (no live HTTP fetch), r09 (no browser render), r01 (corr_id mechanism labeled inference), r03 (gates verified by reading the hook, not executing them), r12 (tier-2 limited to 10 spot-verifications), r04 (14:25Z link state not re-verifiable) |
| 10 | Test suites executed by any lane this run | 0 | every lane's notes say pytest was not asked and not run; no lane executed the suite (per lane archive notes) |
| 11 | URLs fetched | 0 | script URL LIVENESS block (unique 0, fetched 0) |

Additional negative findings banked in lane files, not counted above: r06 vault count drift (r06 read 53 .md at ~18:30Z; r12's two instruments read 52 at ~22:5xZ with dir mtime predating r06's read; miscount unresolved, recorded over either single number; rib_boot's '51 frozen ribs' is stale under both counts); r05's .env '137/137' struck (D7); r01's 5 ts_non_monotonic descents + 66-67 raw-newline split rows (concurrent-writer scars); r04's unscheduled extra index run (last_run.json 18:28:51Z vs scheduled task's 9:00:01 AM fire, runner unrecorded); r09's phantom backbone (188 id-only X-status nodes, one at degree 34); r10's provenance gap (sampled card evidence ids grep zero under corpus/canon, card ids propagate nowhere outside memory/rib); r11's unbanked falsifier firings (next.md F2 and F3 falsified by bytes, no receipt anywhere; F5 late and renamed).

## 9. CURIOSITY REGISTER (top 10, ranked by carried-history retired + verbs minted; unit discipline: rows 3-6 and 8-10 are one seat, one sitting; rows 1, 2 and 7 are packs whose stated one-sitting unit count is binding, each unit its own sitting, never averaged into one)

Metric per r12's grounding: primary = carried-history retired (bytes) + verbs minted (laws/instruments landed), secondary = defects found/fixed/verified, kill only on losing both over 5 waves (memory/percolator/candidates.jsonl row 19; theory origin watch/inbox/LINKS.jsonl rows 371 + 421, arXiv 0812.4360, interestingness as the first derivative of compressibility).

1. **The ESTATE_INDEX compaction pack** (r04#0, r04#1, r04#2, r04#4; r12 rank 1): retires ~7.4 GB of .mimosa litter per copy across two independently-maintained 4.15 GB copies (8.3 GB live duplication, fsutil-proven twice) and stops the writer re-fattening both every walk; mints 3 verbs (estate_index_compact.py --check/--apply, the skip list inside tools/index/projects_index.py's write path, /api/v1/estate/query in dashboard/server.py repointing the_index.html:118). Pack of two one-sitting units, not one sitting: unit 1 lands the check + skip list in the same commit (r04#0 plus r04#1's same-commit clause, with r04#2's :138 copyfile stop in the same sitting per its lane row); unit 2 is the query door (r04#4, its own 'one sitting' in the lane row).
2. **The rib vault boot mount and amendment pack** (r06#0, r06#1, r06#2, r06#3, r06#4; r12 rank 2): retires carried false law from the boot path itself (50 of 53 ribs carry law content in no boot surface; mag/rib_boot.py mounts the bus, never the vault, while indicting the gap in its own docstring); mints 5 verbs (vault mount, 2 POST-DATUM amendments, dup mark on 050639, '51 frozen ribs' count fix, the FREE_USAGE resolving re-probe). Pack of five one-sitting units, one per r06 row, not one sitting: r06#0, r06#1 and r06#2 are the standalone one-sitting actions D4, D5 and D3 carry; r06#3 and r06#4 each carry theirs too (r06#3 bundles the vault mount and the '51' count fix into its single sitting).
3. **The dispatch-shape gate card** (r03#1, conditioned by the tier-2 errata; r12 rank 3): converts the width law (11-day prose, per the claim, actually 9 days) from AGENTS.md bullets into a submit-time instrument; every prevented 429-storm is a window not retired. One sitting: max_concurrency <= 3 card in tools/workflow_gate.py + scenario card in configs/workflow_gate_scenarios, then rerun the LAW-12 scenario suite.
4. **The transfer-debt payoff** (r07#4; r12 rank 4): the meta-gap itself. The master percolator store holds 19 rows with only 2 LINKS-sourced candidates while r07's top-10 deserving list (fungal-compute canon cluster of 26 rows first, then the Jev router capability flag at L263, Strata, OKF, the memory pyramid) stays unfiled, and the bytes-to-verbs metric minted 2026-10-04 is consumed nowhere. One sitting: file the top-10 through the sanctioned percolator writer, then append one estate-index fold and one schmidhuber-metric fold to corpus/steal so the steal map carries its own estate.
5. **The seed-vs-execution fidelity audit** (r01#3, tier-2 VERIFIED; r12 rank 5): one join compresses the 55k-row unread steps stream plus 2,107 worldline actor dirs into per-actor fidelity verdicts the estate has recorded inputs for without ever reading. One sitting: pick one dwfrun uuid, join its steps rows (strip 'sess_') to its SEED.json slabs, diff intended-vs-executed, land the fidelity receipt.
6. **RECEIPT_BINDINGS adoption** (r02#0, tier-2 VERIFIED green-solved): the queue drain verb's adoption clause actually executed (index 3 -> 39 closed, Q-005/Q-025 closed 2026-10-04T08:30:26Z, receipts verified on disk, zero missing close_receipt paths); the reusable shape is that destructive evidence resolves only from a hardcoded row-to-path table. One sitting: adopt it for the next destructive ledger verb.
7. **The trail cure pack** (r05#0, r05#1, r05#2, tier-2 unconfirmed with corrections): the largest uncured operational defect family; a pack of three one-sitting cures, one sitting each (r05#0, r05#1, r05#2; each lane row carries its own 'One sitting' action), not one sitting: (1) single-writer-guard or path-fix the errno-22 runner_state write (910 rows, use the corrected counts); (2) strip CR at key load and normalize trail EOL (14-cycle outage, CR-byte mirror deltas measured); (3) open the sanctioned env door for the night march (28 composites, first cause-naming today). Land each receipt beside watch/inbox/BURNDOWN_20261004.md.
8. **The catalog rescan cure** (r08#2): the librarian D1 disease recurring live: a 5,401-row holding (ai-engineering-from-scratch, clone landed 11:57:53Z after the 07:59:54Z snapshot) reads as a confident zero in catalog.jsonl, tags.jsonl and FTS until the next 03:30 rescan, proven by the map's own walker probe. One sitting: run .venv\Scripts\python.exe -m mag.catalog_rescan incremental (the sanctioned writer), then grep-count the holding to non-zero; also run r08#1's corollary: every corpus consumer emits map_asof/map_stale beside hit counts.
9. **The research lane consumption verdict** (r05#3, tier-2 unconfirmed with the 250-clip correction): an 84%-spooler lane whose monitor output has zero recorded downstream consumption since intake_card/self_steal last fired Sep 6. One sitting: run the owed FTS query (which spooled MONITOR_LANE items ever surface in later watch/inbox cards), write the rate onto queue/lanes/research/surface.md, feed or kill the lane on the answer.
10. **The falsification receipt plus the unbound-aggregate gate** (r11#0, r11#1): next.md's forecast battery F2 (no S2 probe receipt anywhere) and F3 (attention_feedback.jsonl holds exactly 2 rows, mtime Sep 29) are falsified by bytes with no falsification receipt banked, so next.md's own halt rule (re-grade the mine before find four) stands triggered but unfiled; and the 191.8M phantom (ERRATA 001, tier-1 verified) argues the fold gate should fail any master-prose number whose named source file does not carry it. One sitting: file the two-line falsification receipt naming the halt-rule trigger, and add the unbound-aggregate check to the fold gate.

Just missed the cut (`carried`, fold seat's ranking): r09#1 + r09#2 (census printout in _build_estate_walk.py plus seat->produced edges: two verbs retiring the never-recorded 85.6%-islands and zero-seats-in-giant findings) and r10#0 (read the 25 seat_move lines, paste 3 into the next steering block: the cheapest verb-mint on the board).

## 10. Standing numbers (conditions, never averages)

Downstream readers use these; the struck values do not get averaged back in:

- Trail errno-22 family: 910 rows (builder 370, research 513, night 26, prose 1, day_work 0), identical only within each trail. Not 917/376. (D6)
- Night march: 28 composites over Sep 5 to Oct 3 with a Sep 22 gap, monitor rc=0 throughout. Not 30 consecutive. (D8)
- Research clip constant: 250 chars (mag/lane_runner.py:755); 160 is the economist lane (mag/lane_runner.py:749). (D9)
- Skip-list arithmetic: .source 9,524,538 = 89.3% of 10,661,260; single-root exclusion retires 86.01%; all hook-state subtrees (including '_mimosa') 89.34%. Not 89.4%-with-'ALL'. (D10)
- TETHERED_LINK prose-only age: 9 days from the 2026-09-25 receipt; rib vault holds 57 files. Not 11 days / 55 files; the prose-only zero-code-enforcement verdict stands. (TS-05)
- Worldline join: 2,107 actor dirs / 98 runs verified; the stream's dwf uuid count is a live number (114 at the checker's moment, claim said 113). (TS-02)
- LINKS register: 422 rows (wc -l), 55 writers. Not ~700. (r07#1, D2)
- ESTATE_INDEX: 4,150,418,528 bytes / 10,661,260 rows per copy, two independent copies (fsutil, twice). Not 3.4GB, not hardlinks. (TS-06, D1)
- Elder outage: 14 consecutive daily 429 cycles (Sep 20 to Oct 3), recovery 2026-10-04T08:20:40Z. '137/137' struck; 'only the trail noticing' struck. (D7)
- Rib vault size: 52 or 53 .md depending on instrument and moment (r12 vs r06, unresolved, dir mtime predates r06's read); rib_boot's '51 frozen ribs' is stale under both. (Negatives 8)

## 11. Provenance

- Lane archive (12 lane JSON + 12 .checks.json files, read in full this sitting): `C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/mickey17_v2/runs/2026-10-04-0/lanes/`
- Scripted sections: `C:/Users/foste/Documents/projects/local_sovereign_agent/memory/runs/mickey17_v2/runs/2026-10-04-0/FOLD_SECTIONS.md` (fold gate script output; sections 1-5 verbatim from it)
- Tier-1 grades and tier-2 deep-check records: the fold-gate payload (laneChecks 12 yes / 48 no `carried`; deepChecks 7 verified / 5 unconfirmed), mirrored in the per-lane `.checks.json` files
- Not done in this fold: no lane instruments re-run; no pytest; no live URL fetches (script: 0 unique URLs); the fold seat's own additions are the DISPUTED rulings' phrasing, the counted-reasons table, the register ranking beyond r12's five, and this section, all tagged where they carry numbers
- Revised 2026-10-04 on the fresh-reader pass: register rows 1, 2 and 7 relabeled from 'one seat, one sitting' to explicit pack unit counts (CHECK 5 fail: the pack rows overclaimed one sitting), and negatives row 1's unreconcilable '21 grep families' headline struck for the itemized 27-29 term count (CHECK 3 nit); relabels grounded in the lane rows' own 'One sitting' steal sentences (r04#0-#4, r05#0-#2, r06#0-#4); CHECK 1, 2, 4 bound everything else unchanged
- Workspace copy of this fold: `C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_READ_ESTATE.md`
