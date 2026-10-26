# MASTER FOLD - dogfood-100m-20261006 (MICKEY-17 v2.1)

- folded_at: 2026-10-06T22:05:09Z (script sha256 76bb8ea7620d), per FOLD_SECTIONS.md
- writer: the folder seat. Every number is the script's or a lane row's; anything the folder brings itself is tagged `carried`.
- lane archive: memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes (cited below by bare filename; row indices are 0-based positions in each file's rows array)
- law: every steal sentence carries lane id + row index. Verbatim script sections keep the script's own punctuation; the folder's prose adds none.
- top steals: 12 (the script's TOP-K). disputed: 0. `carried`: no lane row claims a top steal outside the list - no row carries such a field, and a grep of the archive for top-steal and disputed claims returned nothing.

## COUNT BASIS (`carried`)

- 87 rows in the 16 lane json files plus 8 rows in d14_sweep_summary.json = the script's 95. The four evidence reports (d07_hyperthink_quantizer_report.json, d10_gps_metabolism_report.json, d10_ledger_audit.json, d13_selfplay_evidence.json) carry no lane-shaped rows. Byte probe at this revision: the `rows` field is absent in d07_hyperthink_quantizer_report.json, d10_gps_metabolism_report.json and d13_selfplay_evidence.json, and is the scalar integer 703 in d10_ledger_audit.json - an audit count over tools/gps_mcp/gps_ledger.db3 (the file's own fields read agreed 209 + mismatch 0 + unresolved 494 = 703), not a lane-row list - which the lane parser skips (non-list rows coerce to [] at tools/mickey17_v2_fold.py:81-83). That skip is why the script's casualty header prints these four as landed-empty (0 rows): the header counts a file landed-empty when its post-coercion rows list is empty (tools/mickey17_v2_fold.py:252-253), so it stays verbatim and true for lane rows; the scalar is not a row entry and is not part of the 95.
- the casualty header's "missing (no file): -5" is arithmetic, not absence: 16 fired vs 21 parseable files landed, per the verbatim CASUALTY HEADER below, so the count is negative surplus. Nothing is missing; nothing is queued for refill.
- mechanism, `carried`: the script computes missing as fired minus landed files (tools/mickey17_v2_fold.py); the minus sign is the file surplus, not absence.

## CASUALTY HEADER (verbatim from the script)

- fired: 16
- landed (parseable files): 21
- landed-empty (0 rows): 4 — d07_hyperthink_quantizer_report, d10_gps_metabolism_report, d10_ledger_audit, d13_selfplay_evidence
- parse errors: 0
- missing (no file): -5
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

## SCOREBOARD (verbatim from the script)

- rows: 95
- estate_status: executed 70, executed-with-deviation 12, ? 11, owed 1, confirms-ours 1
- leverage: high 49, medium 35, ? 8, low 3

## PRISMA FLOW (verbatim from the script)

- identified: 95
- screened: 95 (all rows carry the six rubric fields or their gap notes)
- excluded: 9 verifier-unconfirmed (deep_tier2): 1
- included: 94
- invariant: identified == included + excluded **HOLDS** (95 = 94 + 1)

- `carried`: the single excluded row is d02-stash-seam#5, the deep_tier2 verdict "unconfirmed" (d02-stash-seam.checks.json). Its subject survives with one correction: only stash@{1} and stash@{2} captured the index deletion, not stash@{0} and stash@{1} as the row claimed; the deep check's name-status listing of stash@{0} shows sixty paths, none of them the index file, which is absent from the tree. The script's TOP-K still carries the row; read it with the correction.

## EXECUTIONS (the script's TOP-K, all 12, with proof quotes)

Claim text is the lane row's own wording; the folder added two count attributions ("counts per") where the citation lint demanded a byte carrier, and anchor-corrected the BLOCKED unblock where a cited line had ceased to exist.

### E1. [high] d01-seat-boot-pack#0 - the seat-boot falsifier executed live

```
CLAIM: Executed the seat-boot falsifier live this sitting: mag.rib_boot mounted 7/7 law ribs (marathon seventh) with 5 amendments and a present SUPERSEDED register; mag.cmd context-pack rendered mode=full at 7200 chars and repersisted memory/context_pack_latest.md; schtasks verifies MagLawPackDaily Ready with Last Run 10/6 9:30:01 AM (13:30Z, the armed first fire), Last Result 0, Next Run 10/7 9:30 AM.
QUOTE: VAULT: 53 .md ribs censused 2026-10-06T18:22:52.568527+00:00; 7/7 law ribs mounted; 5 amendments riding after the heads
STEAL (d01-seat-boot-pack#0): done
```

Verifier: tier-1 no (the quote proves the boot leg only); deep_tier2 verified - legs byte-proven via PACK_OFFLOAD.jsonl rows and compile_report.json fields; the schtasks leg rides the receipt's prose and was not independently re-run.

### E2. [high] d01-seat-boot-pack#1 - the law rides the file and sheds at inhalation

```
CLAIM: The deepseek thinking MEASURED ON law rides the fresh flash pack file x2 (frontier fields of rib1 MODEL_GATES#2 + rib2 INFERENCE_BUDGET#1) and the L0d vault body (verified True in a direct build_context_pack), but the default 7200-char render SHEDS the L0d carrier at stage 3 and the 1200-char L0b slice truncates the flash fields at 220 chars before any mechanism byte, so fresh-seat inhalation of the law is 0 bytes (0 hits in the printed pack and in context_pack_latest.md). The R5 close claim 'flash pack carries MEASURED ON x2' is file-level true, inhalation-level false; the loop falsifier is not closed at seat inhalation.
QUOTE: "shed_sections": ["L0d rib vault amendments"], "stage": 3
STEAL (d01-seat-boot-pack#1): Residual: rebalance the flash tier (shorten the 5 vault-amendment flash fields in tools/thought_quantizer.py or raise max_laws in mag/constants.py) so the mechanism bytes ride the default slice; the red test_quantized_laws_section_renders_in_default_budget is the acceptance gate.
```

Verifier: tier-1 no; deep_tier2 verified - the x2 MEASURED ON rides the flash file's frontier fields only (rib1 MODEL_GATES#2 + rib2 INFERENCE_BUDGET#1), flash fields truncate at 220 chars, the persisted pack carries 0 hits, and the R5 close claim (commit d5f89d97b) is file-level true and inhalation-level false. The falsifier stays open at seat inhalation.

### E3. [high] d01-seat-boot-pack#2 - the dispatch and convergence laws inhale zero bytes

```
CLAIM: max_concurrency, convergence, and Sybil laws inhale ZERO bytes at fresh-seat boot: 0 hits across instructions_flash.jsonl, memory/rib_boot.json, the printed pack, and context_pack_latest.md. The convergence/Sybil clause's home RIB_MOSAIC_SEED_20260921.md is NOT in VAULT_RIBS (mag/rib_boot.py:90-98) so it never mounts or feeds the quantizer; SUPERSEDED.md row 1 carries the law bytes but rides the pack only as a pointer line inside the shed block.
QUOTE: The convergence clause now carries a Sybil-form exception: the evidence bar is independence of authorship.
STEAL (d01-seat-boot-pack#2): Residual: add RIB_MOSAIC_SEED_20260921.md to VAULT_RIBS (mag/rib_boot.py:90-98) so the convergence/Sybil POST-DATUM amendment mounts and feeds the quantizer; mint a width/max_concurrency law rib only if the operator wants that boot-carried.
```

Verifier: tier-1 no; deep_tier2 verified - 0-hit greps across the four boot surfaces, the mosaic rib absent from VAULT_RIBS, the clause bytes present in memory/fold_history/SUPERSEDED.md row 1, and the pack-carry path read from code. The live stdout print was not re-executed (it would overwrite estate files); verified via the persisted render plus the shed ledger, as the checker disclosed.

### E4. [high] d01-seat-boot-pack#4 - the adjacent suite is red on exactly this invariant

```
CLAIM: Adjacent suite run (pytest -q on test_context_pack_quantized_laws, test_rib_boot_amendments, test_boot_regen, test_thought_quantizer) = 1 failed, 41 passed: test_quantized_laws_section_renders_in_default_budget fails at the fresh 18:26:38Z compile because five ~220-char amendment headers crowd the 1200-char L0b slice and cut the imperative tail rows ('Verify with git diff', 'Elevate with a deliberate ask'). Red is the tripwire working; also verified the 4200-char L0d body cap cuts the BEHAVIOR_CARDS card index entirely even pre-shed (RIB_BEHAVIOR_CARDS and FUNDING-STATEMENT absent from body).
QUOTE: 1 failed, 41 passed in 9.94s
STEAL (d01-seat-boot-pack#4): Residual: the same flash-tier rebalance as the MEASURED ON row turns the red test green; separately widen or reprioritize the 4200-char L0d body cap so the behavior-cards index survives fat packs.
```

Verifier: tier-1 yes (the pytest line is the run's own output and matches the counts).

### E5. [high] d02-stash-seam#0 - the mid-flight sweep censused, hold-reconcile

```
CLAIM: stash@{0} ref 8b45fe9722fd8a2e2647c4880883267f9fcae445, created 2026-10-05T19:00:20-0400 on HEAD ebcd2583d, is the R5-named mid-flight sweep: 58 files (622692 insertions) spanning the R3-L1 executor surfaces (tools/citation_lint*.py, mickey17_v2_fold.py, prepush_credential_shape.py, cache_kpi.py, workflow_gate.py + 4 test files), sibling lane runners (builder, day_work, research, bard_ledger), and estate ledgers (FIRE_LEDGER + REGISTRY, law registry, percolator invariants, catalog). Sweeper seat unnamed in the witness. Disposition: HOLD-RECONCILE, never drop; may carry duplicate first-pass copies of the R3-L1 eleven files plus mag/claims_verify.py and training/events.jsonl snapshots (r3_land_gate.md:32).
QUOTE: At 2026-10-05 19:00:39 EDT a git stash (not this lane) captured ALL working-tree modifications on HEAD ebcd2583d
STEAL (d02-stash-seam#0): none filed on the row (census row; the disposition is HOLD-RECONCILE)
```

Verifier: tier-1 no; deep_tier2 verified - git rev-parse reads stash@{0} = 8b45fe9722fd8a2e2647c4880883267f9fcae445, created 2026-10-05T19:00:20-0400 on HEAD ebcd2583d, 58 files changed with 622692 insertions, span check matches the R3-L1 surfaces. Caveat banked by the checker: the labels HOLD-RECONCILE and never-drop live only in this lane's own files; the estate's banked guidance is reconcile-before-pop.

### E6. [high] d02-stash-seam#3 - the sweep detector landed

```
CLAIM: Landed tools/stash_sweep_watch.py (284 lines): check mode flags a NEW stash push (ref unseen in state/stash_sweep_watch_state.json) whose captured paths intersect the recent-write window (tree mtime within window_seconds of now, or absent-from-tree for captured deletions) and appends one deduped alert line per ref to memory/attention.md (instance_guard doubled_key dedup law); census mode prints per-stash disposition rows; the tool carries NO drop or pop verb by design. Window membership is evaluated by targeted stat of the stash's own paths, not a full-tree walk, because the tree holds ~680k files outside .git (memory/ alone 550k, measured by find|wc -l this sitting). Exit contract: 0 quiet, 1 alert, 2 error.
QUOTE: Dedup law (mirrors tools/instance_guard.py doubled_key_check): one alert line per stash ref, ever; repeat sightings stamp state only.
STEAL (d02-stash-seam#3): residual: wire check mode onto a patrol cadence (schtasks or the governor loop) so a future sibling sweep is caught inside the 900s window instead of at the next manual run
```

Verifier: tier-1 no; deep_tier2 verified - 284 lines confirmed, check-mode semantics read from the code (unseen-ref skip, targeted stat window, absent-from-tree deletion flag), census mode executed live printing 3 disposition rows, no drop or pop verb exists, exit contract verified from code plus a live error probe on a non-repo root. The exit-1 fired path is verified from code bytes only, disclosed.

### E7. [high] d02-stash-seam#4 - the detector's two proofs landed

```
CLAIM: Landed tests/test_stash_sweep_watch.py (86 lines, 2 tests) on real temp git repos: test_detection_fires_on_new_sweep_of_recent_writes proves a new stash push of an in-flight edit fires the verdict and appends exactly one STASH-SWEEP-WATCH alert naming the path and ref; test_quiet_window_stays_quiet proves a new stash whose writes aged out of the window appends nothing and a second pass stays quiet even with fresh live writes elsewhere (state dedup). Run via .venv/Scripts/python.exe -m pytest: 2 passed in 1.83s after the final code state.
QUOTE: assert verdict["fired"] is True
STEAL (d02-stash-seam#4): done
```

Verifier: tier-1 no; deep_tier2 verified - the test file read in full (87 lines on disk against the claim's 86), both named proofs present, suite re-run green (2 passed; timing varies run to run). The file is untracked on disk: landed means written at the estate path, not committed.

### E8. [high] d02-stash-seam#5 - the detector fired on the live estate (read with the correction)

```
CLAIM: Dogfooded the detector on the live estate: first check pass fired on all three stashes (exit 1), appending one alert row per ref at memory/attention.md:684-686 and recording all three refs in the state file. Live find the alert surfaces: stash@{0} and stash@{1} both captured dashboard/data/ESTATE_INDEX.jsonl, which is now ABSENT from the tree (deletion captured; the working tree replaced it with ESTATE_INDEX.pointer.json), and both stashes intersect live lane surfaces (queue/lanes/*/trail.jsonl, training/events.jsonl, watch/monitor_lane.state) that sibling lanes are actively rewriting.
QUOTE: - [x] STASH-SWEEP-WATCH alert 2026-10-06T19:14:11Z: new git stash 8b45fe9722fd8a2e2647c4880883267f9fcae445 (stash@{0}, created 2026-10-05T23:00:20Z) captures 8 path(s) in the recent-write window
STEAL (d02-stash-seam#5): residual: the absent ESTATE_INDEX.jsonl means stash@{0}/stash@{1} hold the last full-index copies; the pointer-file owner should reconcile before any pop
```

Verifier: tier-1 yes; deep_tier2 UNCONFIRMED - the run's single PRISMA exclusion. The alert rows, state-file refs, tree absence and lane-surface intersection all verified, but the row's pairing is contradicted by the bytes: only stash@{1} and stash@{2} captured the index file (stash@{0} lists sixty paths, none of them it). Read the steal with the corrected pairing.

### E9. [high] d03-stopcert-rows#0 - 20 status rows minted into the registry

```
CLAIM: Minted 20 status rows (verdict STATUS-ROW, shape per tools/workflow_gate.py:654-667 json.dumps append) for the 20 saved .zcode/workflows/*.dwf.ts scripts, appending REGISTRY.jsonl lines 111-130; status derived from byte-truth only (sha256[:12] of current bytes vs latest saved-path registry row digest, FIRE_LEDGER.jsonl rows for the saved path, boundary-aware RETIRED.md membership): 5 active (current digest == latest row digest AND a fire row exists), 15 unknown, 0 retired. This loads the R5 'armed but unloaded' stop-cert with per-script status while retiring nothing. Classification rule pinned in each row's status_basis; the positive vocabulary word 'active' is this mint's choice (the task sanctioned only 'unknown' and forbade retirement) and is fully re-derivable from the basis.
QUOTE: appended 20 rows at ts=2026-10-06T18:53:21Z / lines: 110 -> 130 / prefix byte-identity (first 110 lines): OK / status tally: {"retired": 0, "active": 5, "unknown": 15}
STEAL (d03-stopcert-rows#0): Residual: 15 unknown statuses are standing fleet questions - classify each script at its next gate check or fire; the 5 game-dig veins (game-dig-coop-social, -creature-farming, -horror-maze, -liveops-seasonal, -roguelike-runs) have zero registry rows and have never been gate-checked.
```

Verifier: tier-1 yes (the receipt-shaped quote matches the claim's counts and append proofs).

### E10. [high] d03-stopcert-rows#1 - the drifted gate script caught

```
CLAIM: Negative first-class finding: .zcode/workflows/ractor-engine.dwf.ts carries a PASS fire and a PASS registry row at digest d8d63f619ab9 (2026-10-06T00:53:10Z) but its current bytes hash 403c5076482f, so its last gate verdict does not describe its live bytes; the digest-vs-row input caught the drift and the row is status unknown, never invented active.
QUOTE: "latest_registry_row_digest": "d8d63f619ab9", "latest_registry_row_verdict": "PASS", "digest_matches_latest_row": false, "fire_count": 1
STEAL (d03-stopcert-rows#1): Residual: run .venv/Scripts/python.exe tools/workflow_gate.py check --script .zcode/workflows/ractor-engine.dwf.ts to re-certify the drifted bytes (amend-not-rewrite if it FAILs).
```

Verifier: tier-1 yes (the status_basis fragment proves the drift-catch fields as written).

### E11. [high] d04-graph-orphan#0 - live orphan census

```
CLAIM: Live knowledge-graph orphan census executed read-only at 2026-10-06T18:41Z (pre-heal, graph ts 2026-10-06T18:06:27.608164Z): nodes 2926 / edges 1133 / orphans 1205 (doctrine 217 / knot 400 / landscape 2 / module 446 / steal 140) / dangling 0. vs R4 S5 recount (nodes 2921, edges 1144, orphans 1204, dangling 29 at watch/inbox/ractor_engine/2026-10-05-ouroboros-r4-memory/SYNTHESIS.md:29): orphans +1, dangling 29->0 holding since R4b; vs R4b AFTER census (2924/1133/1203/0 at watch/inbox/ouroboros_20261005/r4b_land_graph_genome.md:34-36): edges and dangling identical, nodes +2 / orphans +2 attributed to tree movement between moments (census denominator law).
QUOTE: nodes: 2926 edges: 1133 | orphans: 1205 by_kind: {'doctrine': 217, 'knot': 400, 'landscape': 2, 'module': 446, 'steal': 140} | dangling: 0 (counts per memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/d04-graph-orphan.json row 0).
STEAL (d04-graph-orphan#0): done: census is one command away for the next seat - json.load(memory/knowledge_graph.json), degree-map edges, orphans = degree-0 nodes, dangling = endpoint not in node ids
```

Verifier: tier-1 yes (the census line is the run's own output; every number in it matches the claim and sums).

### E12. [high] d04-graph-orphan#2 - the heal ran the proven path

```
CLAIM: Heal executed through the estate's proven heal path tools/graph_heal.py (Mickey17 W3 v0, suite tests/test_graph_heal.py): dry plan 117 heal / 846 ambiguous / 1088 demote-listed, then real pass RESULT PASS healed=117 demoted_listed=1088 deleted=0 graph_edges=1250. Post-heal census: orphans 1205 -> 1066 (117 healed + 22 orphan-anchors linked as heal sources), edges 1133 -> 1250 (117 why_context, all heal-marked), dangling still 0; the forget-events ledger merged to 1492 ids (counts per memory/runs/mickey17_v2/runs/dogfood-100m-20261006/lanes/d04-graph-orphan.json row 2). Idempotence proven: dry re-run add_edges=0.
QUOTE: RESULT: PASS healed=117 demoted_listed=1088 deleted=0 graph_edges=1250
STEAL (d04-graph-orphan#2): done: rerun is safe anytime (add_edges=0); next seat should NOT run kg.build() without re-healing after
```

Verifier: tier-1 yes (the RESULT line is the heal pass's own output; the arithmetic checks).

## BLOCKED TIER

- owed (1): d06-canon-adjudication#4 - the only row the scoreboard carries as owed; tombstones are zero.

```
REASON: AGENTS.md load-order row 0a names receipt watch/inbox/ouroboros_20261005/r5_land_close.md, which does not exist on disk.
QUOTE: ls: cannot access 'watch/inbox/ouroboros_20261005/r5_land_close.md': No such file or directory
UNBLOCK (the row's own steal, anchor-corrected): One sitting: land the missing watch/inbox/ouroboros_20261005/r5_land_close.md or correct the AGENTS.md row 0a receipt path. Separately, the sibling that touched the zknot module must accept or fix its NEW ratchet debt by name before push (folder note: the row's line anchor on that file predates the d05 module split, which cured that half the same sitting).
```

- status of that unblock, `carried`: the file-too-long half was cured the same sitting by d05-meter-alarm (the zknot_alarm.py module split; d05's row 4 records RATCHET PASS with NEW=0), so the open half is the receipt path only.
- tombstones: 0 - [] (the script computed none; no hard failures to subtract from owed).
- refill: nothing to refill (see COUNT BASIS: the minus is surplus files, not absence).

## NEGATIVE RESULTS (counted reasons table; tombstones included)

| n | reason | count | rows (lane#row) |
|---|--------|-------|-----------------|
| 1 | deep_tier2 verdict unconfirmed; the one PRISMA exclusion (stash pairing corrected) | 1 | d02#5 |
| 2 | trust-teeth bypasses proven against today's bytes (8 probe shapes; the lane's own tally: 6 holes, 3 controls survived, no instrument weakened) | 5 | d15#0, d15#1, d15#2, d15#3, d15#4 |
| 3 | deviation disclosed and cured in-session | 12 | d01#1, d01#2, d01#3, d02#7, d04#1, d05#4, d10#3, d12#2, d13#0, d13#3, d15#6, d16#3 |
| 4 | hypothesis refuted live, banked as executed refutation (watch-blindness) | 1 | d09#1 |
| 5 | surface mismatch: two censuses compared across different instruments (morning ORPHAN_CENSUS.json is the inbox registration census, no kg numbers) | 1 | d04#1 |
| 6 | demand-data selection bias: needle-driven sweeps; 14 of 17 new quota_wall rows are infra noise | 1 | d12#2 |
| 7 | reproduction over an unchanged chain, not new evidence (zero new arena runs since the 10-05 bank) | 1 | d11#2, d11#3 |
| 8 | boundary condition: strong HyperThink claim untestable on current labels (domain field 611/620 behavioral); measured effect weak (NMI 5-11%) | 1 | d07#3 |
| 9 | pre-existing sibling-owned debt observed, not fixed (7 blocking citation rows in sibling files; 2 card PHANTOM-NUMBERs pinned to lines; 1 stale AGENTS.md:5 line-cite WARN) | 3 | d02#8, d05#4, d13#3 |
| 10 | production infrastructure dead or drifted (gate script digest drift; two OpenRouter lanes dead since 10-05; ESTATE_INDEX.jsonl absent from tree) | 4 | d03#1, d14#1, d02#5 |
| 11 | landed code that had never executed its main path (four spawn defects + PIPE deadlock in the bridge, all fixed in-sitting) | 1 | d13#1 |
| 12 | red suite observed and attributed (one kept as tripwire, one cured at the premise) | 2 | d01#4, d13#2 |
| 13 | instrument with zero test coverage (free_lane_fleet has no test file) | 1 | d14#4 |
| - | tombstones (hard failures) | 0 | [] |

## NEXT REGISTER (top 12 residuals; one seat, one sitting each)

### R1. d04-graph-orphan#5 - the supersession wire, spec-first

```
Two edits, one file, build-persistent by construction: fold() grows kwarg supersedes (resolve old_id, fold the old node absent with outcome=falsified, write supersedes on the new node); _edges() grows one branch minting the superseded_by edge. One SUPERSEDED.md row = fold(old, doctrine, falsified) + fold(new, doctrine, held, supersedes=old). Spec in the docstring before the code, per build discipline. Falsifier: a quarter where SUPERSEDED.md gains rows but the graph gains no superseded_by edges.
```

### R2. d01-seat-boot-pack#1 - the flash-tier rebalance that closes the R5 seat-boot falsifier

```
Rebalance the flash tier (shorten the 5 vault-amendment flash fields in tools/thought_quantizer.py or raise max_laws in mag/constants.py) so the mechanism bytes ride the default slice; the red test_quantized_laws_section_renders_in_default_budget is the acceptance gate.
```

### R3. d15-trust-teeth-retest#0 and #1 - the two gate parse fixes

```
Strip unquoted // suffixes (string-literal aware) before the G1-G7 lambdas (the #0 residual); make parse_declared_args indent-tolerant (detect the first arg header's indent, the move-7 fix shape in tools/prepush_workflow_metadata.py) so fired_args, declared_arg_widths and the ledger join see four-space blocks (the #1 residual). One sitting: the two parse fixes only.
```

### R4. d15-trust-teeth-retest#1 and #0 - the probes as gate tests, then the forged-payload cards

```
Add the probes as gate tests (the #1 residual); mint the dated forged-payload scenario cards from these probes once the gate rejects them (LAW-12 FORGED-CARD clause; never weaken the cards - the #0 residual). One sitting, riding after R3 (d15#6 banks the same sequencing): the cards exist only once the fixed gate rejects the probes.
```

### R5. d03-stopcert-rows#1 - re-certify the drifted script

```
Run tools/workflow_gate.py check --script .zcode/workflows/ractor-engine.dwf.ts to re-certify the drifted bytes (amend-not-rewrite if it FAILs).
```

### R6. d03-stopcert-rows#0 - classify the 15 unknowns, then gate-check the 5 game-dig veins

```
One sitting: classify all 15 unknown-status scripts in one active pass now (re-derive each status from its pinned status_basis byte-truth and update the registry rows) instead of waiting for each script's next gate check or fire - this row pulls that standing deferral into one bounded sitting; then gate-check the 5 game-dig veins (game-dig-coop-social, -creature-farming, -horror-maze, -liveops-seasonal, -roguelike-runs) that have zero registry rows and have never been gate-checked.
```

### R7. d09-nha-tiering#4 - the temperature-query door

```
Add a temp column to the crows schema in tools/corpus_fts_rebuild.py, rebuild once through the sanctioned writer, and thread a --temp filter through corpus_search so warm-door terms and cold-tier temperature answer in one query. 933,956 COLD-or-FROZEN spine rows are classifiable but unqueryable today.
```

### R8. d10-gps-metabolism#3 and #4 - close the namespace double-bank door, mark the poison file

```
Make task_shape a required argument (or refuse shapes not already present in the ledger's capability table) in mag/gwap_to_gps feed_session so the next caller cannot double-bank a whole namespace; rename memory/runs/gwap/arena-sessions.jsonl to a .superseded-20261003 suffix (or drop a DO-NOT-FEED marker beside it) so no future feeder or backfill counts it as owed.
```

### R9. d06-canon-adjudication#4 - the owed receipt (the BLOCKED row's unblock)

```
Land the missing watch/inbox/ouroboros_20261005/r5_land_close.md or correct the AGENTS.md row 0a receipt path.
```

### R10. d08-reflux-delta#0 - adopt the delta chain beside the snapshot writer

```
Adopt the chain in mag/lane_runner.py _save_state: append a delta row beside the snapshot rewrite (one sitting); world_state changes[] extraction and warm_state boot rows are the follow-on conversions.
```

### R11. d13-selfplay-run#4 - the intrinsic-reward wire and the actor-side meter

```
Wire the intrinsic-reward forecaster onto the per_problem partial-state rows (one sitting: few-shot or train on memory/runs/*/lanes/ outcomes per MIRA S1), and make generate_move return the llama_cpp usage dict so actor tokens join the meter.
```

### R12. d14-freelfleet-verify#4 (with #2) - give the fleet its first tests, then recover the dead lanes

```
Add tests/test_free_lane_fleet.py covering the dead-provider skip (tools/free_lane_fleet.py:306-308) and the liveness exit contract; no test exists today. Recovery of the two dead OpenRouter lanes (model swap for the 429'd model id plus a health reset) files to the fleet owner lane.
```

- residual pool beyond the twelve (same one-sitting shape, one line each): d01#2 mount RIB_MOSAIC_SEED_20260921.md in VAULT_RIBS; d01#3 give the marathon rib a feed-readable amendment or render law_head digests; d02#3 wire the stash watch onto a patrol cadence; d02#5 pointer-file owner reconciles the stashes before any pop; d05#4 operator: fix the two card PHANTOM-NUMBERs and the stale AGENTS.md:5 line-cite before the next push; d07#3 fine-grained domain tag in the percolator feed, then rerun the probe unchanged; d12#2 tighten the quota_wall needle or add an infra subclass plus one neutral query; d14#0 boot-trigger for the fleet task; d14#3 carry provider usage tokens into ledger rows; d15#6 re-attack census patrol and gwap; d16#0 wire publish_recheck into githooks/pre-push (operator call); d16#3 re-read the three ROT-RECHECK cites before anyone re-consumes the dawn page.

## APPENDIX - remaining script sections (verbatim)

### FIDELITY

- rows with all of quote/source/steal/estate_status non-empty: 84/95 (88.4%)

### VERIFIER TABLE (persisted verdicts)

- lanes with persisted checks: 16
- verdicts: checks 6 (<no-value-field> split: <dict> 6), commands 5 (<no-value-field> split: <dict> 5), deep_tier2 12 (verdict split: same-chain-verified 1, unconfirmed 1, verified 10), deviations 1 (<no-value-field> split: <dict> 1), supports 83 (supports split: no 22, yes 61)
- deep_tier2 join: 11/12 row_keys match a lane row; join-miss (verified, no exclusion weight, labeled not fatal): 1

### WIDTH-ECONOMICS

- rows/lane: median 5, max 9, min 0
- top-10 lanes share: 63.2%
- exact cross-lane duplicate quotes (normalized): 1
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

### URL LIVENESS (scripted at fold time)

- unique URLs: 0; fetched: 0; skipped non-public: 0; live: 0; dead/blocked-status: 0

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

### carried notes on the appendix

- the URL liveness section found 0 unique URLs because every row source is an estate path; there are no dead-URL demotions this fold.
- the TOP-K takes the first 12 rows sorted by leverage then lane id (FOLD_SECTIONS.md); the first 12 high-leverage rows all sit in d01, d02, d03 and d04, so the list is those lanes' high rows.
- the width gate (Law 7) bites only above 50 width; this run fired 16 (FOLD_SECTIONS.md), so it does not bite.
- the verifier table's join-miss is d15#1 (the four-space args bypass): its deep verdict is same-chain-verified, re-proven by the checker's own re-run of the digest-identical probe bytes through the same gate and join code, and its row_key shape does not join a lane row, so it carries no exclusion weight. Its tier-1 quote was not landed bytes at the proof path; the substance was re-proven live by the checker.
- deep-verdict map, `carried` from the checks files: the 12 deep_tier2 verdicts are 10 verified, 1 same-chain-verified (d15#1), 1 unconfirmed (d02#5); the d02 verdict is byte-present at d02-stash-seam.checks.json and the d15 verdict at d15-trust-teeth-retest.checks.json.
- gate record for this master, `carried`: the fold script's A14 unbound-aggregate gate reads OK on both copies, and citation_lint reads ok with blocking=0 and two standing warns on the E2 block (that block's render-config numbers name context_pack_latest.md, which does not carry them as bytes; the deep check verified them via the code constants instead).
