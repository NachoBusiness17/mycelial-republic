# MICKEY-17 v2.1 master fold: boot-lane interference burn wave 1 (2026-09-25)

Folded 2026-09-25 by the fold seat (dwfrun-217c37f5, topic: "Boot lane interference burn wave 1 (2026-09-25): dogfood the estate's own gates and meters while the burn runs; every row binds to verbatim tool output"). Wave 1 = 9 lanes (8 dd-gate dogfood lanes + 1 negatives-binding lane), all landed, 45 rows this wave.

Gate disclosure (read this first): the fold ask arrived with the gate's stdout EMPTY (0 bytes); the in-run gate produced nothing. To keep the fold script-gated anyway, the fold seat re-ran the identical gate command during the fold: `bash C:/Users/foste/.zcode/workspace/default/mickey17_v2/fold_run.sh 9` from a fresh shell; it exited 0 with 4292 bytes and printed its summary line: `lanes=58 rows=286 included=285 excluded=1 dups=0 median_rows=5 -> C:\Users\foste\Documents\projects\local_sovereign_agent\memory\runs\mickey17_v2\FOLD_SECTIONS.md`. The rerun rewrote that sections file (mtime moved to the fold). Every number below is that script's output, quoted verbatim; prose around it is the fold seat's, and any fold-level count the script does not compute is tagged `carried`.

Archive condition (stated, not averaged): this run uses the legacy shared archive `memory/runs/mickey17_v2/lanes`, which still holds the earlier 40-target sweep's 49 research lanes beside wave 1's 9. The script counts what the directory holds: 58 landed files from 9 fired, hence `missing (no file): -49`. That figure is fired-vs-files arithmetic on the shared dir, not lost lanes: run metadata shows tombstoned `[]` and refired `[]`. The per-run archive fix (`--run` slug) exists in the saved workflow but this run's materialized script predates it.

Record laws: this fold is em-dash-free end to end; the scripted sections and lane quotes embedded here carry no em-dash byte either (the script emits them only in casualty-suffix lines that are empty this fold).

## CASUALTY HEADER (verbatim, tools/mickey17_v2_fold.py)

- fired: 9
- landed (parseable files): 58
- landed-empty (0 rows): 0
- parse errors: 0
- missing (no file): -49
- classification: missing/transient get ONE bounded idempotent refill; hard failures are tombstoned and subtracted from owed.

Condition: see archive condition above. This wave's own 9 lanes all landed with 5 rows each; nothing is missing.

## SCOREBOARD (recount, verbatim, whole legacy archive, 286 rows)

- rows: 286
- estate_status: confirms-ours 113, owed 66, new 56, we-have-better 51
- leverage: medium 140, high 139, low 7

Wave 1 contributes 45 of the 286 (9 lanes x 5 rows) `carried`.

## FIDELITY (verbatim)

- rows with all of quote/source/steal/estate_status non-empty: 286/286 (100.0%)

## VERIFIER TABLE (persisted verdicts, verbatim)

- lanes with persisted checks: 9
- verdicts: checks 15, rows 5, supports 25

Meaning (carried, from the tool source at tools/mickey17_v2_fold.py:156-162): the table sums list-valued keys across the 9 wave-1 `<id>.checks.json` files; recomputed mechanically during the fold: `{rows: 5, supports: 25, checks: 15}`. The 9 files do not share one key shape, so the split is uneven across them.

## WIDTH-ECONOMICS (verbatim)

- rows/lane: median 5, max 6, min 1
- top-10 lanes share: 17.8%
- exact cross-lane duplicate quotes (normalized): 0
- gate: width above 50 requires dup share < 10% and top-10 share < 50% (Law 7)

## PRISMA FLOW (verbatim)

- identified: 286
- screened: 286 (all rows carry the six rubric fields or their gap notes)
- excluded: 1 phantom-source (dead-lane negative row): 1
- included: 285
- invariant: identified == included + excluded **HOLDS** (286 = 285 + 1)

The excluded row is the single-row dead lane `skywork-guide` (source `https://api.skywork.ai/nova/seo_article/detail_by_slug`, HTTP 404 at fold time) `carried` (lane file: memory/runs/mickey17_v2/lanes/skywork-guide.json).

## URL LIVENESS (scripted at fold time, verbatim)

- unique URLs: 139; fetched: 139; skipped non-public: 0; live: 130; dead/blocked-status: 9
  - HTTP -1: https://datatracker.ietf.org/doc/search/?q=crovia
  - HTTP 403: https://openai.com/index/introducing-the-agents-api
  - HTTP 403: https://openai.com/index/introducing-deep-research/
  - HTTP 403: https://openai.com/index/the-next-evolution-of-the-agents-sdk
  - HTTP 403: https://www.perplexity.ai/hub/blog/learning-from-real-world-experience
  - HTTP 403: https://www.perplexity.ai/hub/blog/photon
  - HTTP 404: https://api.skywork.ai/nova/seo_article/detail_by_slug
  - HTTP 405: https://agentmemoryleaderboard.ai
  - HTTP 405: https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId

- rows citing dead URLs move to negative results with their status; rendered rows carry url_checked_at.

Lane mapping of the 9 dead URLs (carried, by grep over the lane archive): state-artifact-formats (-1), openai-agents-latest (403, two URLs), openai-deep-research (403), perplexity-lab (403), persistent-coding-agents and swarm-economics (403, shared photon URL), skywork-guide (404), agent-memory-sota row #2 (405, leaderboard), kci-rubric (405). Most 403/405 are bot-walls on live pages, not dead claims; they are itemized in NEGATIVE RESULTS.

## TOP STEALS (the script's TOP-K, all 12, with quotes and actions)

The script ranks by leverage then lane id alphabetically then row index and takes 12 (tools/mickey17_v2_fold.py:204-207). All 12 slots land on research lanes with ids sorting before `dd-`; this wave's own claims therefore file DISPUTED per the section's own rule (see D7) and act through the GO LIST. No quote below is the fold seat's; each binds to its lane row in `memory/runs/mickey17_v2/lanes/`.

1. [high] a2a-mcp-security#0 (new). Quote: "a malicious server can change the tool description after the client has already approved it". Action: pin every MCP tool's name+description+schema hash into the estate's append-only hash chain at first connect; diff on every reconnect and alarm on drift before the drifted tool is callable.
2. [high] a2a-mcp-security#1 (owed). Quote: "Treat icon metadata and icon bytes as untrusted inputs and defend against network, privacy, and parsing risks." Action: extend the pack-tails-are-DATA law to MCP tool results: any imperative sentence arriving in a tool result or resource payload routes through the operator gate before execution.
3. [high] agent-memory-sota#0 (owed). Quote: "intercepts proposed persistent-memory writes and produces deterministic Accept, Review, or Quarantine decisions". Action: add a Review tier + source-trust score to the estate's fail-closed ingest so trusted-source suspicions route to operator_inbox advisory instead of silent exclusion.
4. [high] agent-memory-sota#1 (owed). Quote: "Persistence changes availability, not epistemic standing: stored or retrieved material is not thereby supported." Action: stamp each estate knot/fold with a typed evidential-status enum (supported/disputed/withheld + origin type) so assertion code can refuse to present stored material as supported.
5. [high] agent-memory-sota#3 (owed). Quote: "is not provided with tools to edit its core memory". Action: revoke memory-write tools from conversational seats and make the 04:00 fold window the sole memory write path (estate's own queued action, watch/inbox/NIGHT_EXTERNAL_MEMORY_20260911.md:19).
6. [high] agentcheck#0 (confirms-ours). Quote: "Tool-using LLM agents are mostly evaluated assuming all tools work." Action: build a fault-injection harness around the estate's own tool grants; inject delay/stale/empty faults per tool and file a recovery receipt before the tool counts as law-backed.
7. [high] agentcheck#1 (owed). Quote: "a retry mitigation raises success on timeout error faults from as few as 30% of cases to 100%, whereas stale-data faults remain near 3-4 of 10 regardless of the mitigation." Action: extend the doc-only freshness gate into a tool-result freshness receipt: observed-at timestamp + source hash on every tool result; claims past the bar fail receipts-before-claims.
8. [high] agentcheck#4 (we-have-better). Quote: "systemic over-trust in corrupted outputs". Action: keep fault recovery in meters, not model scale: pair every cheap worker with a programmatic output check (K-of-N quorum, escalate-on-failure) instead of expecting a bigger seat to notice corrupted tool data.
9. [high] agentic-researcher#1 (confirms-ours). Quote: "At the beginning of every session (or after a context window reset), the agent re-reads report.tex, TODO.md, and the git log to restore continuity." Action: make the re-read a structural resume step in estate workflow lanes: after context reset or process death, a lane re-reads its fold/receipt files and git log before its first action.
10. [high] agentic-researcher#3 (confirms-ours). Quote: "we enforce that the agent (a) does not run a full, potentially expensive evaluation after every minor code change, and (b) does not discard ideas based on unsuccessful small-scale runs on toy problem instances." Action: add an oracle-ceiling cell to falsifier-ledger entries: pre-compute the theoretical upper bound per lane and record gap-remaining before spending free-lane budget.
11. [high] anthropic-multiagent#1 (confirms-ours). Quote: "multi-agent systems use about 15x more tokens than chats. For economic viability, multi-agent systems require tasks where the value of the task is high enough to pay for the increased performance." Action: add a value-per-token admission gate to estate fan-outs: no fan-out unless expected task value clears the ~15x premium (budget caps already mapped in memory/research_polished/economics.md:18,30).
12. [high] anthropic-multiagent#2 (owed). Quote: "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each, and complex research might use more than 10 subagents with clearly divided responsibilities." Action: close the G4_4_wiring.md:38 BUILD item by wiring lane effort budgets in the workflow engine using Anthropic's three tiers verbatim as defaults.

## DISPUTED tier (contradiction pairs, both quotes, conditional rulings)

Include rule: every tier-2 unconfirmed row lands here. Tier-2 ran on 12 script-selected load-bearing rows: 9 verified, 3 unconfirmed, 0 crashed. Tier-1 supports (45 rows checked): 12 yes, 33 no; the recurring "no" is the same shape, a claim whose conjunction spans several sources while the quote carries one; tier-2 then byte-verified 9 of 12 anyway. Both facts `carried` from run metadata.

D1. dd-snapshot#2 (tier-2 UNCONFIRMED) vs dd-pile#2. Lane claim quote: `"pile": 136, "classified": 0, "unclassified": 136,` and the claim's headline "tools/pile_classify.py has never drained the pile". Refuting bytes (tier-2): memory/pile/classified.jsonl holds 34 classified rows spanning 2026-08-07 to 2026-09-25T23:36:59Z, 31 predating the receipt row; the live status reads 137/0/137, and mag/state_snapshot.py:115 counts only in-pile `classified` flags while tools/pile_classify.py:94-95 sets that flag only on the copy it appends elsewhere and never rewrites state_summaries.jsonl. Ruling (conditional): the zero is real but it is a gauge defect; an unlinked write-back, not a dead loop; the drain is partially alive (34/137). Treat "never drained" as refuted; keep "status gauge can never rise" as the defect.

D2. dd-surface#1 (tier-2 UNCONFIRMED). Lane claim: "All 150 unindexed files have zero register events in the append-only log ... no rebuild can register files the log never saw," quote: "INDEX.json is now DERIVED from the append-only event log index_events.jsonl (Ethereum fold pattern, EXP-002A). Writers APPEND events; they never rewrite this file or the log. The log is the source of truth." Tier-2 found the universal false: of 168 unindexed at recheck, 3 carry register events (DRIFT_PATROL_20260925.md at valid event #2354, which postdates the 12:03:43Z fold; pure fold staleness a rebuild WOULD repair; INDEX.md and SHARED_SURFACE_CONTRACT.json were register-then-invalidate), 85 files are truly invisible to the log, and live counts drifted (files 858, unindexed 166). Ruling (conditional): dd-surface#3's repair stands but broadened; backfill `add` events for the event-less files AND run `rebuild` (it repairs the DRIFT_PATROL-class staleness the lane said it could not) then `verify`, via scripts/index_fold_host.mjs. Never hand-edit INDEX.json either way.

D3. dd-mdrecord#0 (tier-2 UNCONFIRMED). Lane quote: "verdict: RECORD HAS TEETH-MARKS", claimed as confirming the on-file question "verbatim". Tier-2: that string exists only in console output (tools/md_record_audit.py:126); watch/inbox/MD_RECORD_AUDIT.json contains no verdict field (grep 0 hits); the file's criteria (Accurate 0/10 drifted, Enduring 3 unparseable grandfathered, all_pass false) are byte-verified. Ruling: substance confirmed, the word "verbatim" withdrawn for the verdict line; the verdict is console-only by design (docstring line 11).

D4. dd-mdrecord#1 vs dd-mdrecord#2 (both tier-2 VERIFIED; a real contradiction pair). Baseline quote: "Baselines otherwise: freshness PASS, md_record teeth-marks = grandfathered only," (watch/inbox/BOOT_LANE_INTERFERENCE_BURN_20260925.md:36). Counter-quote: `"all_pass": true` (git HEAD snapshot of watch/inbox/MD_RECORD_AUDIT.json, commit 16b45778a, ts 2026-09-21T19:04:57Z, the only durable prior audit). Ruling (conditional): the last durable audit was RECORD CLEAN, so today's three failing criteria (Attributable 59 seal events missing file/ts, Contemporaneous 45 of 92 today-files unsealed, Original 76 untracked) are NEW degradation, not a standing state; amend the wave baseline to carry the counts (dd-mdrecord#1's action).

D5. dd-chainguard#0 churn (tier-2 VERIFIED with one stale scalar). Lane quote: `"ok": false, "state": "regression", "rows": 9834, "dangling": 3,`. Tier-2 live rerun: rows 9835 (the append-only chain gained one knot between the lane's runs and the check; wc -l memory/biography/verkle_chain.jsonl = 9835), same ok:false / state:regression / dangling 3 / dangling_unflagged 2, tip still matches chain. Ruling (conditional): the scalar row-count is a moving number on a live chain; the verdict is churn-stable (which is dd-chainguard#3's own finding). Quote the verdict, not the row count, as the canary.

D6. s1-negatives#1 premise nuance (within-source). Prereg shorthand (watch/inbox/INTERFERENCE_REPLICATION_PREREG_20260925.md:55-56) cites only the 4-number pair, 0.87 vs 0.94; the log (RESEARCH_LOG.md:322-325) shows the 5-number pair runs the other way, 0.94 vs 0.92. Ruling (conditional): the robust evidence for "hidden-state probe weaker than feature probe" is the frontier solve counts (15/30 vs 22/30), not AUC alone; cite the pair with the solve-count grounding, never the favorable pair alone.

D7. Script-rule note, not a substance fight: the TOP-K section's own rule says "a lane-claimed top steal outside this list files as DISPUTED." Wave 1's headline claims (config-seal coverage gap, chain regression, T1 coupling collapse, OLLAMA_HOST root cause, surface backfill ruling, ALCOA degradation, five interference-search negatives) all sit outside the 12 slots because the rank is alphabetical and `a2a...anthropic` fills them. Ruling (conditional): they are carried here and in the GO LIST with lane id + row index, and the GO LIST is explicitly not the script's TOP-K; the script's own rule places them in this tier.

## NEGATIVE RESULTS (counted reasons table)

Tombstones: none; `tombstoned: []` from run metadata. Refires: none; `refired: []`.

| # | Reason | Count | Source |
|---|--------|-------|--------|
| 1 | Tombstoned lanes (hard failures) | 0 | run metadata (scripted) |
| 2 | Refires | 0 | run metadata (scripted) |
| 3 | Phantom-source rows excluded by PRISMA | 1 | scripted PRISMA (skywork-guide, HTTP 404) |
| 4 | Dead/blocked URLs at fold time | 9 of 139 | scripted URL LIVENESS; lane mapping `carried` above |
| 5 | Tier-2 unconfirmed load-bearing rows | 3 of 12 (0 crashed) | run metadata; ruled in DISPUTED D1-D3 |
| 6 | Lanes filing rubric-1 web-fetch as not-applicable (primary source is a local tool or vendored file, cross-checked against raw bytes instead) | 9 of 9 wave lanes | each lane's note/rubric_gaps |
| 7 | Zero-hit estate-grep findings (a zero hit is a finding) | 14 across 8 of 9 lanes `carried`; memory/research_polished returned zero hits for 8 of the 9 lanes that grepped it (dd-drift the exception, 6 files) | lane files |
| 8 | Premise/ask drift refuted with receipts | 6 `carried`: `state-snapshot --dry` does not exist (argparse exit 2); drift registry is 9 pairs / 11 checks, not ~32 metrics; tools/drift.py start command is a silent no-op (no __main__); the organ's tri-state is healthy/tip_stale/regression, not FAIL; main.py pile-classify cannot pass flags (exit 2 twice, then silent drop); md_record "grandfathered only" baseline is stale | dd-snapshot#1, dd-drift#1, dd-drift#2, dd-chainguard rubric_gaps, dd-pile#1, dd-mdrecord#2 |
| 9 | Meter lies caught (tool self-report vs raw bytes) | 2 `carried`: wrapper printed total_classified=28 against 31 physical rows (3 duplicate ids); pile docstring promises idempotency while 3 ids appear twice | dd-pile#1, dd-pile#3 |
| 10 | In-source negatives bound by s1-negatives | 7 `carried`: overclaim self-corrected in source (LOG:278); overreach narrowed by review (LOG:224-225); one-seed premise drift unrepaired (LOG:349-350 + CLAIMS.md:26); prereg cherry-pick (D6); disclosed small-n walls (LOG:167, 191-192, 60); phantom-citation spot-check 3 of 15 resolved, 12 not fetched; voided cmd-syntax grep rerun with GNU grep | s1-negatives.json negative_first_class |
| 11 | Tier-1 supports checks failed as written | 33 of 45 `carried`; dominant shape: multi-source conjunction claims, not bad quotes | run metadata laneChecks |

## GO LIST (top 10, one seat one sitting; each carries lane id + row index)

Per D7 these are wave-1 DISPUTED-tier claims, not the script's TOP-K; each names its landing spot.

1. dd-pile#0: Fix the root cause: `.env` line 118 to `OLLAMA_HOST=http://127.0.0.1:11434` (or delete the line), then `main.py pile-classify --limit 5 --json` must report errors=0; receipt to corpus/steal. This unblocks every main.py-dispatched classify row (106 pending).
2. dd-configseal#3: Switch `_config_files` to rglob and cover *.mdc/*.txt or an explicit allowlist, then re-seal by name; landing spot tools/config_seal.py:36-43. Tier-2 VERIFIED: 7 configs outside the seal, and verify cannot see them (its live set uses the same non-recursive glob).
3. dd-chainguard#2: Run verkle_knot repair over the two unflagged dangling rows (mag-agent-orc-t492d6fd54c, mag-agent-orc-t039e3ee788: refold or flag evidence_lost), then `mark --expected`; landing spot mag/verkle_knot.py. Tier-2 VERIFIED.
4. dd-surface#3 (as widened by D2): Saturday one-sitting: backfill `add` events for the event-less unindexed files, then rebuild (repairs DRIFT_PATROL-class staleness too), then verify, via scripts/index_fold_host.mjs; EXP002A backfill receipt to watch/inbox. Tier-2 VERIFIED for the ruling, with D2's correction folded in.
5. dd-surface#2: `node scripts/index_fold_host.mjs verify`, then re-register or invalidate each of the 24 hash-mismatched active items (EXP-002A's named falsifier tripped 24 times); receipt to watch/inbox. Tier-2 VERIFIED.
6. dd-freshness#3: Add one header line to state/HANDOFF.md declaring it a frozen lineage snapshot; the gate's own contract (tools/freshness_check.py:13-14) requires the self-declaration and the header is bare. Tier-2 VERIFIED as a gate-contract violation.
7. dd-mdrecord#4: One-line patch at tools/md_record_audit.py:113: append the verdict as an index_events.jsonl event alongside the rolling JSON so verdict history is append-only (this run destroyed any uncommitted prior verdict). With dd-mdrecord#1: amend the wave baseline to the three real counts (59 / 45-of-92 / 76).
8. dd-drift#4: Backfill stamped_at/sources/window onto the five v1 I-1 stamp rows (schema-v2 shape, marked reconstructed) so the whole drift registry is trust-the-bytes; landing spot memory/runs/adv_arc_50/drift_stamps.jsonl.
9. s1-negatives#2: Audit mag/ interagent pass-off for raw "do not X" text fed to sibling lanes and convert such signals to structured, ranked-only receipts (33.6% repeat rate beside a note vs 21-22% without); falsifier row to the close receipt.
10. dd-pile#4: Record one consolidated case-law row named "claimed-output-verification" citing the 8 pile ids that are the same receipts-before-claims lesson in six wordings; landing spot mag.skill_ledger via the pile fold path.

## Where the receipts live

Lane archive (A1): memory/runs/mickey17_v2/lanes/; one .json per landed lane plus `<id>.checks.json` tier-1 verdicts. Scripted sections: memory/runs/mickey17_v2/FOLD_SECTIONS.md (regenerated this fold, gate exit 0). Tier-2 evidence strings live in run metadata (12 deep checks: 9 verified, 3 unconfirmed). Copies of this fold: corpus/steal/MASTER_MICKEY17_V2.md (estate) and C:/Users/foste/.zcode/workspace/default/mickey17_v2/MASTER_MICKEY17_V2.md (workspace, for publishing).
