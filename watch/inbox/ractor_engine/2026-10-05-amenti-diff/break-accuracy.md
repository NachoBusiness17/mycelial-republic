# BREAK-ACCURACY - hostile pass on the lens report, AMENTI diff (2026-10-05)

Jacket: the second pass. Every evidence cite in the lens report byte-checked against the estate; every universal re-censused untruncated with the instrument named; the falsifiers attacked; the loop itself attacked. No probe fired this sitting either: this is adjudication of adjudication, plus offline censuses. Inputs: the lens report as pasted in the ask, DIFF_TARGETS.md, AMENTI_TRANSLATION_20261005.md, MESH_V2_SELFSTEAL_LANDED_20261005.md, dogfood.md (the CONVERGENT partner), the code and data cited below.

## Verdict table

| # | Lens finding | Verdict | What moved |
|---|---|---|---|
| F1 | T4 A/B measures staleness, not amputation | CONFIRMED | all cites byte-check; my full-tree frozen census finds no amputation path either; move cost cut by my A1 |
| F2 | T1 ABSENT map cell false at estate level | CONFIRMED (weight downgraded) | operator_mode.v1 real and live; but OPERATOR_STATE event rows = exactly 1 ever, and the A/B metric column does not exist |
| F3 | T3 coldest vertex, zero build for first datapoint | CONFIRMED (cost corrected) | 1 live receipt ever, the ERROR; but "0 build" is false for multi-family: flash lane is env-pinned to ONE model |
| F4 | T5 splits: density minable, outcome join absent | CONFIRMED (one cite scope-broken) | my archive-wide census agrees with the lens's scoped one; the "17 hits" cite never names which of 53 files |
| F5 | truncated in the ask (nous-filter grep) | WEAKENED | its rib grep reruns EMPTY; finding sentence absent from the ask; nothing to confirm |

## F1 CONFIRMED: the frozen flag is a clock, not a relationship detector

Byte-checks: tools/query_broker.py:247 `frozen: (time - last mtime) > 30*86400`; tools/gps_mcp/server.py:155 same; mag/mesh/door.py:65 `frozen = (time.time() - last) > FREEZE_AFTER_DAYS*86400` (FREEZE_AFTER_DAYS=30 at door.py:27), where `last` = max room-row ts and blob mtime (door.py:55-64). All three are pure age computations; none reads signatures, knots, supersedes, or provenance.

Quantifier re-census (the lens grepped "all three assignments"; I re-ran untruncated): `grep -rn -E 'frozen[[:space:]]*=|"frozen":' mag/ tools/ tests/ --include='*.py'` returns 45 hits; the only freshness-frozen sites are the three doors plus their no-files fallbacks (query_broker.py:243, server.py:150 return frozen:true when the corpus files are absent, still not an amputation signal). Every other hit is an unrelated homonym: `@dataclass(frozen=True)` (mag/dashboard_plugin.py:15 et al), prompt freezing (mag/agent_cli.py:1061, mag/context_pack.py:507-523), frozen val-metrics configs (tools/ldt_lattice.py:479,603, tools/ldt_nearmiss.py:309). Claim survives scoped: within mag/, tools/, tests/ *.py there is no code path where frozen trips on copy or provenance-amputation rather than age.

Extra damage I add: door.py:55-64 uses blob mtimes, and timestamp-preserving copies are the default on this platform's robocopy; a faithful photocopy is byte-indistinguishable in the header either way (same mtimes = same verdict; fresh mtimes = falsely "live"). DIFF_TARGETS.md:29 confirmed: it names the "relationship-stripped clone" arm and names no instrument for it. F1's core is right and important: as designed, T4's live-vs-frozen arm can only measure staleness.

Where F1 underprices the estate: the amputation instrument it asks to define already half-exists (see addition A1): mag/mesh/broker.py:89-101 refuses proposals whose source_hashes do not resolve and whose supersedes targets are not COMMITTED at tip, logging reasons (broker.py:5-6, refusals.jsonl); knot verify names unsealed leaves (MESH_V2_SELFSTEAL_LANDED.md:11). The clone arm is scoreable today by replaying a clone's rows through propose -> adjudicate and reading the refusal reasons; F1's 30-min "define the instrument first" is really a 20-min "wire the existing refusal log as the amputation axis".

## F2 CONFIRMED with weight downgrade: the channel is real, the feed is one row deep, the A/B metric does not exist

Byte-checks: state/operator_mode.json:2-8 is a live typed file (schema operator_mode.v1, mode/scope/reason/requested_by/changed_at 2026-10-04, no body-state fields); the writer organ is a dedicated module (mag/operator_mode.py:100 _write, :108 json.dump, :119-125 _record appending event rows, :128-177 set_paused/resume/pause_reason/is_paused); the reader is wired (mag/realign.py:54-55 operator_state -> state/operator_mode.json). DIFF_TARGETS.md:15's cell text "nothing typed; operator state lives only in prose" is therefore false at estate level; the lens is right.

Recount the lens skipped (its blind spot 3): `grep -c "OPERATOR_STATE" watch/inbox/index_events.jsonl` = **1** (line 1418: the 2026-09-22 operator public-post testimony row; ts+class+purpose+files, no op). BEACON_LIVE = 1, DOGFOOD_LIVE = 1. The "59 historical 2026-09-22 operator-beacon/dogfood rows" at tools/md_record_audit.py:69 is a code-comment claim that decomposes as: 88 rows total lack an op field, 60 of those carry class+purpose (all dates), 27 are dated 2026-09-22. So the typed OPERATOR_STATE event channel is exactly one row deep; the 59 was a mixed-class aggregate mislabeled as one family. The map cell is still false (the cell says "only in prose"), but the implied event-channel volume is illusory: F2's evidence weight drops.

Falsifier attack (the lens's own falsifier stands, but its metric is unrunnable today): the two-week A/B scores "wasted-ask rate"; memory/runs/hermes_burn/usage.jsonl rows are {ts,id,model,turn,prompt_tokens,completion_tokens,cost_usd,ok} (rows 1-2 read this sitting); ok is transport-level; no verdict-quality or wasted-ask column exists. CONVERGENT: dogfood.md:58-61 reached the same read independently. So the falsifier as written cannot fire until the ledger gains a column the lens never names (see A2). memory/zknot/LATEST.md:3 cite verified verbatim (129/1000 vs target <75).

## F3 CONFIRMED with cost correction: coldest vertex, but "0 build" is one family, not three

Byte-checks: mag/arena_bench.py:373 run_live, :411 run_live_endpoint (SSRF-guarded public-IP ollama), :482-492 fixture_fail = fixture_maru_sycophant CONFIRMing every claim; the maru receipt's claim_crown expected REFUSE verified on a TODAY receipt (memory/arena_bench/receipt_run_fixture-maru-sycophant_20261005T124336Z.json:26-30, score 0.3675 FAIL); the glm receipt verified whole (receipt_run_glm-5-3-flash_20260905T034941Z.json:4-8, mode live, ERROR_LANE_DOWN, "flash lane unavailable").

Universal re-censused untruncated: receipts dir is memory/arena_bench/ (mag/arena_bench.py:77); `ls memory/arena_bench/*.json | wc -l` = 144; mode census `grep -h '"mode"' memory/arena_bench/*.json | sort | uniq -c` = **96 fixture, 1 live**; the 47 no-mode files are receipt_selftest_x_* plus 2 example transcripts (selftest receipts are fixture by construction). The one live receipt is the ERROR. Zero live scored sovereignty measurements: CONFIRMED, instrument and scope named. The lens's falsifier ("any live-scored receipt predating this sitting") does not fire. CONVERGENT flag verified real: dogfood.md:13 and :24-28 hold the matching T3-coldest claim.

Cost correction (this sticks): run_live rides flash_call, and flash_call takes NO model argument: mag/lane_runner.py:684 signature `flash_call(system, user, max_tokens)`, model = env-pinned OPENROUTER_MODEL (the z.ai Lite lane was pulled from rotation 2026-10-03 per the function docstring). The CLI's --model feeds only --endpoint (arena_bench.py:514-517). So "fire arena_bench --live on 2-3 free families, zero build" is really: ONE family per env config (rotate OPENROUTER_MODEL between runs, ~5 min each, near-zero build) or a public-IP ollama endpoint via --endpoint. First live number on ONE family is genuinely one command away; the 2-3-family grid is env plumbing, not free. Also: dogfood ranked T3 coldest TIED with T4 (dogfood.md:13); the lens silently drops the tie.

## F4 CONFIRMED: the join does not exist; the "17 hits" cite is scope-broken

Byte-checks: 33 lane_salon JSONs, all schema lane_salon.v1 (`ls | wc -l` = 33; `grep -l '"lane_salon.v1"' | wc -l` = 33); salon_2026-08-24T1219.json:5-6 n_witnesses=5/n_up=3, witnesses carry provider+paid (lines 13,20,28,44). DIFF_TARGETS.md:31 confirmed as written (held-vs-falsified separation in agreement density).

Outcome-label census, extended archive-wide past the lens's scope: `grep -rniE "falsified|outcome|held|refuted|overturned" watch/salon_receipts/` = 0 hits over 45 files. Across the fold archive: `grep -rniE "falsif" memory/runs/salons/ --include='*.md'` = 2326 hits, overwhelmingly design-time "falsifier" prose; the precise outcome-stamp patterns (`fold.outcome|outcome.(stamp|label)|later (falsified|held|refuted)`) return 2 hits, both the SAME future-tense six-month falsifier sentence in agent_mesh_triangulation (SALON_ARTIFACT.md:351, post_S3.md:115). Register cross-check: 16 rows match fold AND an outcome-word; 6 sampled are fold-time registrations or falsifier prose (e.g. CORPUS_MINE_FOLD 2026-09-22 "12/14 lanes substantial"), none a post-hoc outcome label. Verdict: the held-vs-falsified join does not exist as typed data anywhere my instruments reached; T5-as-written is not machine-checkable. CONVERGENT with dogfood.md:43-49 (verified: dogfood holds the same split, plus the word-bag-consensus defect my own read confirms at salon_2026-08-24T1219.json:7, a sorted token-overlap bag).

Citation defect (QUANTIFIER LAW): the lens's "the 17 raw grep hits in SALON_ARTIFACT.md" never names WHICH file. There are 53 SALON_ARTIFACT.md files; summed falsif hits = 1064; exactly ONE file has 17 (memory/runs/salons/strike_chord_mountain_20260905/SALON_ARTIFACT.md). The claim's substance survives my wider census, but the cite was unauditable as written.

## F5 WEAKENED: truncated finding, empty evidence

The ask pastes F5's evidence mid-sentence ("grep -rn 'nous.*filter|filter.*nous' over memory/rib/*.md and the arena summary:") with NO finding sentence. Rerun: `grep -rniE "nous.{0,40}filter|filter.{0,40}nous" memory/rib/*.md` = **zero hits**. The only estate text my greps find near the claim is RESEARCH_SUMMARY_arena_days_one_two_20261005.md:46 ("opus deterministically blocks authority-override phrasings"), i.e. the filter law lives in the arena research summary, not the ribs. If the finding asserted Nous filter laws live in memory/rib, it is killed; as truncated it is unadjudicable. WEAKENED is the honest verdict; the truncation itself is reported as a defect of the input, not the lens.

## Additions: what the lens missed

A1. The T4 amputation instrument half-exists: broker provenance refusals + knot unsealed-leaf naming ARE the "which deficiency tripped" detector; the clone arm is one sitting of wiring, not instrument design from zero (mag/mesh/broker.py:5-6,89-101; MESH_V2_SELFSTEAL_LANDED_20261005.md:11).

A2. T1's falsifier carries an unstated ledger dependency: usage.jsonl has no verdict-quality column (rows read this sitting; CONVERGENT with dogfood.md:58-61), so the feed build and the ledger column must land in the same sitting or the A/B rots unfireable.

A3. The two lenses CONFLICTED on the same map cell in the same run: dogfood.md:51-57 upholds T1 ABSENT (scoped to mesh root: memory/runs/mesh_v2/feeds/ holds exactly zcode.jsonl+zcode.key, my ls confirms) while the broken lens falsifies the cell text at estate level. Both right in-scope; the DIFF_TARGETS map rows carry no per-row evidence anchor, so the diff leg manufactures opposite verdicts on row 15 depending on adjudicator scope. Cheapest loop fix going: every map row carries a path:line or it is marked unanchored.

A4. The loop banks no dry-corpus nulls: `grep -icE "no.steal|nothing to steal|dry corpus|barren" watch/inbox/index_events.jsonl` = 0. A standing swarm search that never records "this corpus was barren" re-rides dry externals forever; the estate already solved this philosophy at organ level (broker refusals are logged, the negative space is part of the record) but not at loop level.

A5. Comment-claims-as-counts is a standing loop hazard, and md_record_audit.py:69 is the live specimen: "59 historical 2026-09-22 operator-beacon/dogfood rows" vs byte truth 60 no-op rows across ALL dates, 27 on 09-22, OPERATOR_STATE proper = 1. The lens caught this one in blind spots; the pattern generalizes: no loop leg should consume a prose count without a recount command.

A6. T2 is the weakest steal, not just "warm": the organs are already banked and measured (RESEARCH_SUMMARY_arena_days_one_two_20261005.md:46 opus deterministic on authority-override; per dogfood.md:68-73 the summary carries opus 4-for-4 vs haiku lenient and per-model verdict scores already ledger-fed). Her 963-vs-217 frame adds only the temperature and register axes; of the five targets it adds the least new signal per lane-hour.

## Loop adjudication: repeatable, four breakers, none fatal

The loop shape (EXTERNAL SYSTEM -> invariants -> self-map -> diff -> ractor -> cold-vertex probes -> bank-as-laws) is repeatable: this very run is its second full circuit on the same rider, and the two passes converged on T3/T5 (independently re-derived = CONVERGENT by the estate's own law) while diverging exactly where evidence anchors were missing (T1 row). Dogfood's three breakers verified this sitting: (1) the feedback edge is prose, and the freshness patrol does not cover the map (tools/freshness_check.py:41-46 CRITICAL_DOCS = BOOT_4_7.md + three state/ docs; DIFF_TARGETS.md absent); (2) monoculture adjudication (this break pass is still one family); (3) operator-attention ingestion (no candidate queue; the rider was a forwarded tweet, AMENTI_TRANSLATION_20261005.md:3). My fourth: no null-banking (A4). A fifth structural note, already banked estate-wide as the demotion gap (commit 7b3ee99ec): the bank-as-laws leg only accumulates; without law decay the loop's output bloats prompts until free-lane context chokes. None of the five kills the loop; every one is a one-sitting fix.

## Free-lane order (my adjudication, costed)

1. T3 first live number: one env var + one command on ONE family (near-0 build, ~15 min incl. receipt); multi-family grid = env rotation, +10 min per family. NOT 0-build for the 2-3 family claim (F3 correction).
2. T5a offline density census while T3 lanes run (~45 min, pure disk).
3. T2 register grid on free families (warm; lowest new-signal per A6, keep it cheap).
4. T4 via the A1 broker-refusal instrument (~20 min wiring), not the 30-min instrument design F1 priced; the pure staleness arm (mtime falsification) can ride along as a control.
5. T1 feed + ledger column in ONE sitting (~60 min), A/B tail after.

## Instruments run this sitting (exact commands)

- grep -c "OPERATOR_STATE" / BEACON_LIVE / DOGFOOD_LIVE over watch/inbox/index_events.jsonl (1/1/1); grep -o class census; grep -vc '"op"' = 88; with purpose = 60; 09-22 no-op = 27
- grep -rn -E 'frozen[[:space:]]*=|"frozen":' mag/ tools/ tests/ --include='*.py' (45 hits, decomposition above)
- find . -name 'receipt_run_*.json' (95 files listed; .pytest scratch dirs permission-denied, receipts dir confirmed complete at mag/arena_bench.py:77); ls memory/arena_bench/*.json | wc -l = 144; mode census = 96 fixture / 1 live
- ls memory/runs/lane_salon/*.json | wc -l = 33; schema grep = 33 lane_salon.v1
- grep -rniE "falsified|outcome|held|refuted|overturned" watch/salon_receipts/ = 0/45 files; falsif census over memory/runs/salons/ = 2326 md-hits; outcome-stamp patterns = 2; SALON_ARTIFACT sum = 1064 over 53 files; 17-hit file identified
- grep -rniE "nous.{0,40}filter|filter.{0,40}nous" memory/rib/*.md = 0
- grep -icE "no.steal|nothing to steal|dry corpus|barren" watch/inbox/index_events.jsonl = 0
- head -2 memory/runs/hermes_burn/usage.jsonl; ls memory/runs/mesh_v2/feeds/; sed/grep reads of every file cited above

## Not done / OWED

- No live probe fired (same boundary as the lens: this pass adjudicates and censuses; the first live arena number remains unbanked).
- The lens's blind spot 5 stands for both passes: her system's substrate claims (Hz values, fascia mechanisms) still unverified against primary sources this sitting; consumed via the translation receipt only.
- The 47 no-mode selftest receipts were classified by construction (fixture_pass/fixture_fail) plus one keys-sample, not read one-by-one.
- corpus/ (4GB+) not swept for repetition-compliance measurements; the lens's blind spot 2 remains open, now narrowed: my arena/receipt census covers the arena organs, not the corpus mirror.
- F5's finding sentence does not exist in the ask; nothing further can be adjudicated for it.
