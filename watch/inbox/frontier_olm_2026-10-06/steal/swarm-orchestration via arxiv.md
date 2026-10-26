# Steal card: swarm-orchestration via arxiv (2026-10-06, round 3, count corrected)

Find: arXiv 2609.34432, "Semantics, Workflows, and Infrastructure: Understanding Agent Serving at Production Scale" (v1 submitted 2026-09-28), https://arxiv.org/abs/2609.34432
Sweep row: watch/inbox/frontier_olm_2026-10-06/sweep/swarm-orchestration-arxiv.md:23 (item 4, RQ4 envelope)
Round-2 review approved everything except one byte-contradicted count (card line 12, field-swapped grep -L transcription) and an incomplete trajectory enumeration (line 10). Both are fixed this round with fresh moment-stamped commands; approved-as-written content is carried unchanged in substance.

## Verification log

- Abstract fetched first-hand via WebFetch on the abs page: confirmed verbatim "a two-week trace of 11.7 million requests", "over 10k GPUs", "rare execution overlap among logical sibling requests", "context reuse across task boundaries", "highly skewed request volumes across sessions". [round 1]
- Dedupe, restamped this round: rg over memory/ + catalog/ (gitignore-respecting) for the paper id, "11.7 million", and the title fragment returns no files (ran this round: NO_PRIOR_HOLDINGS_RECONFIRMED). .gitignore:34 excludes memory/trajectory/steps.jsonl from that sweep; targeted reads of that file show the only hits are self-referential trajectory-journal rows from this mine's own run session (session_id sess_dwf-dwfrun-4c984c88-1675-48d6-ba2c-c784fd33d025 with actor suffixes). Enumeration, now complete at this snapshot: row 62537 (2026-10-06T15:37:53.900Z, actor_3_13, contains "11.7 million"; read fresh this round), rows 63323-63328 (17:39-17:40Z [round 2]), rows 64571 and 64575 (23:02Z [round 2]), and rows 64572, 64598, 64600, 64711, 64773, 64796 (read fresh this round: 6x "2609.34432", 3x "11.7 million", actors actor_4_24, actor_5_10, actor_6_10). Rows appended since any snapshot are this run's own commands; the conclusion stands: no prior holdings, only self-referential trajectory-journal rows.
- CORRECTED COUNT (the round-2 blocker). Round-2 card line 12 said "0 missing started_at, 594 missing ended_at"; the raw round-2 output actually had 594 on the started_at line (command order was created, started, ended; outputs 0, 594, 0), and the card transcribed the swap. Census re-run this round in one labeled pass at moment 2026-10-06T23:58:20Z: TOTAL 6,685 rows; grep -L counts: 0 missing created_at, 596 missing started_at, 0 missing ended_at; three-field intersection (comm -12 of created/started/ended possessing lists): 6,089 rows with a complete created_at/started_at/ended_at span. Live-tree note per the B2-216 census-denominator law: the total read 6,682 at the round-2 check, 6,683 then 6,684 at the reviewer's minutes-apart checks, 6,685 at this moment; the hole count moved 594 to 596 for the same reason. Byte evidence for the hole's meaning: memory/runs/orchestrator/tasks/t-fadvice-0c458a03.json (read this round) is status "failed" with 0 started_at hits and 1 ended_at hit, a failed-before-start row. So the ledger's true complete-span denominator is 6,089 at moment 2026-10-06T23:58:20Z, matching the reviewer's independent 6,089.
- AGENTS.md anchors: line 35 fan-out width law (verbatim "the limit is rolling throughput, not width-only"), line 36 max-concurrency standing law, line 37 THE DESCENT PROTOCOL (leg 1 prior-art sweep, leg 8 usage banking). [round 2 read; re-confirmed by round-2 reviewer]
- Instrument census: for WORKFLOW CHILDREN no timing instrument exists (.zcode/workflow-runs/dwfrun-c948c345-3be2-4b40-873f-8ae21837fdac.mjs is a lowered script with zero timing tokens and 3 log( calls [round 1]; workflow max_concurrency declared "3 (fan-out width law default ...)" at .zcode/workflows/olm-mine.dwf.ts:29 [round 2]). For ORCHESTRATOR DISPATCHES the ledger above is the instrument.
- Reviewer-reproduction note, reported faithfully [round 2]: the round-1 review's "zero overlap/sibling/stagger hits" across the three envelope receipts did not fully reproduce: exactly one hit, corpus/steal/TETHERED_LINK_STEAL_20260925.md:54, "owns it (`workflow_run_not_retunable` from a sibling session", where "sibling" means a sibling harness session, unrelated to dispatch overlap. The unmeasured-axis conclusion stands.
- Standing boundary: the paper-side quantities (11.7M requests, 10k+ GPUs, two weeks, overlap rarity) are the authors' abstract claims, cited not reproduced (sweep boundary note, sweep file lines 34-36).

## The steal (mechanism, not a link dump)

Production-scale counter-evidence to sizing dispatch shapes for heavy sibling concurrency: in a two-week 11.7M-request trace on 10k+ GPUs, logical sibling requests rarely overlap in wall-clock execution; demand is dominated by skewed per-session volumes and cross-task context reuse. Reading: sibling width buys latency tolerance and retry surface, not proportional parallel throughput.

Observable mismatch (fix C): the paper measures server-side execution on a 10k-GPU serving cluster; the estate can only log client-side dispatch-to-finish wall-clock (queue time, throttle waits, retries included). Every transfer inference below scopes to our dispatch shape only; nothing here claims to reproduce the paper's serving regime.

## Estate map

Feeds the gopher fleet (dispatch shape). Port move, two legs:

1. Zero-instrument first cut, runnable today (fix D + Descent Protocol leg 1, AGENTS.md:37): read the existing ledger memory/runs/orchestrator/tasks/ and compute the descriptive metric below over temporally co-resident dispatch pairs, using the 6,089 complete-span rows (moment 2026-10-06T23:58:20Z; rows carry no wave id, co-residency is derived from timestamp intersection of started_at/ended_at). Output feeds A/B arm design; it is explicitly not the falsifier.
2. The discriminating leg: a width A/B on the workflow path, where pooled co-resident siblings overlap near-fully by construction (max_concurrency 3 stamp at olm-mine.dwf.ts:29; 10-12-wide clean measurements only on the Task-agent path, AGENTS.md:35). That construction is why an overlap threshold alone can fire or pass structurally (fix B), so the threshold lives on throughput.

Secondary steals parked: (1) "context reuse across task boundaries" backs the byte-identical-ask amend-cache law, corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md:10; (2) "highly skewed request volumes across sessions" is a water-graph per-session budget prior.

## The probe (defined so it can actually fail)

Descriptive metric (fix A): for two siblings i and j of one fan-out, overlap(i,j) = max(0, min(end_i, end_j) - max(start_i, start_j)) divided by min(dur_i, dur_j), dur being the client-side dispatch-to-finish span; denominator is the shorter sibling's span, so 1.0 is full co-residency and 0 is strict serialization; wave statistic is the median over unordered co-resident pairs. Worked example: spans 60s and 30s sharing a 15s window score 15/30 = 0.5.

Falsifiable test (fix B): one gated workflow, same item corpus, two arms on consecutive runs: max_concurrency 5 vs max_concurrency 10. Per arm, measure valid finds/hour (gate-passing items) and 429/1302 first-contact count. Prediction if the paper's regime transfers to our account-backed lane: width 10 yields under 1.25 times the finds/hour of width 5, because rolling account throughput rather than width binds (AGENTS.md:35 states this as a measured conclusion; the A/B makes it decisive at the current mix). Falsified if width 10 yields at least 1.5 times finds/hour at comparable first-contact error rate: width genuinely buys throughput on our lane, the width-cap law keeps its present form, and the paper's overlap regime does not describe our fleet. Both arms bank usage rows per descent leg 8 (AGENTS.md:37).

## Sources

- https://arxiv.org/abs/2609.34432 (abs page fetched via WebFetch; v1 2026-09-28)
- watch/inbox/frontier_olm_2026-10-06/sweep/swarm-orchestration-arxiv.md lines 3, 12-16, 23, 34-36
- AGENTS.md:35, AGENTS.md:36, AGENTS.md:37 (fan-out width law; max-concurrency standing law; Descent Protocol legs 1 and 8)
- .zcode/workflows/olm-mine.dwf.ts:29 (max_concurrency 3 declaration stamp)
- memory/runs/orchestrator/tasks/ (6,685 rows at moment 2026-10-06T23:58:20Z; 6,089 complete spans; hole samples t-fadvice-0c458a03.json; field samples tprobe01.json, ext-0002ae23c5.json)
- memory/trajectory/steps.jsonl rows 62537, 63323-63328, 64571, 64572, 64575, 64598, 64600, 64711, 64773, 64796 (self-referential hits only; appended-since-snapshot clause above) and .gitignore:34 (its exclusion)
- corpus/steal/TETHERED_LINK_STEAL_20260925.md:54 (single incidental regex hit, quoted above)
- corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md:10 (byte-identical ask amend-cache)
- .zcode/workflow-runs/dwfrun-c948c345-3be2-4b40-873f-8ae21837fdac.mjs and memory/workflows/REGISTRY.jsonl (131 rows, run-level ts only) [round 1 checks]

OWED: nothing outstanding beyond the standing paper-claims boundary named above.
