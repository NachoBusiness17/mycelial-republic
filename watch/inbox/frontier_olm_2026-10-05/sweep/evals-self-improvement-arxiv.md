# frontier sweep: evals + self-improvement via arXiv - 2026-10-05

source-fetched: 2026-10-05
Area: evals-self-improvement via arxiv. Feeds: githooks/pre-push gates (ratchet, citation lint, workflow gate), tools/census_drift_patrol.py, tools/hermes_burn.py, and the Gero-4B admission gate.

## Method (what was actually fetched)

Pass 1, broad sweep. Six arXiv Atom API queries via export.arxiv.org (sortBy=submittedDate, descending), plus the two recent-listing pages:

1. `all:"SWE-bench"` - 25 entries, 2026-09-27 through 2026-10-01
2. `all:"small language model" AND all:"benchmark"` - 25 entries, 2026-08-14 through 2026-10-02 (six entries dated 2026-08-14 to 08-26 sit outside the 30-day preference and were excluded from banking)
3. `all:"self-improving" AND all:"language model"` - 25 entries, 2026-09-27 through 2026-10-02
4. `all:"tool use" AND all:"agent" AND all:"evaluation"` - 25 entries, 2026-09-27 through 2026-10-02
5. `all:"observability" AND all:"language model"` - 15 entries, 2026-10-02
6. `all:"anomaly detection" AND all:"LLM"` - 15 entries, 2026-09-14 through 2026-10-01
7. https://arxiv.org/list/cs.CL/recent and https://arxiv.org/list/cs.LG/recent (2026-10-05 listings; both reported only the first ~50 entries per day - the listing pages degrade to a partial view, noted as such)

Candidate pool: 100+ enumerated entries across the four research questions; well over 30 inside the 2026-09-05 to 2026-10-05 window. Pass-1 candidates include (non-exhaustive, strongest-relevant): 2609.36043, 2610.00025, 2610.02142, 2609.07370, 2609.38652, 2609.34924, 2609.38812, 2609.36556, 2610.02911, 2609.34198, 2609.37315, 2609.35025, 2609.35760, 2609.38670, 2610.03394, 2609.21341, 2610.02206, 2609.35875, 2609.39321, 2609.00665, 2608.17183, 2609.34683, 2609.37834, 2609.37968, 2609.38372, 2609.34975, 2609.33398, 2609.33295, 2610.03002, 2610.03190, 2610.03515, 2610.03226, 2610.01223, 2609.31371, 2609.25261, 2609.20620, 2610.02952.

Pass 2, deep reads (9 items read end to end, not title-banked):
- FULL TEXT (arxiv.org/html): 2609.36043v1 (SAGE), 2610.02142v1 (Keyword Harnesses), 2609.38652v1 (AgBench)
- ABSTRACT PAGE (arxiv.org/abs, detailed extraction): 2610.00025 (Microtask Eligibility Gap), 2609.07370 (CPU Reliability Benchmark), 2609.34924 (Audit the Scaffold), 2609.38812 (Self-Verification), 2609.36556 (MAADBench), 2610.02911 (Probe the Harness)

## Degradations (honest log)

- First attempt at the six remaining HTML full-texts ran in one parallel batch and ALL SIX timed out at the 60s WebFetch cap (AgBench, in the same batch, succeeded). Retried SAGE + Keyword Harnesses sequentially: both succeeded. The other four were read at abstract depth only; anything below abstract for those items is NOT asserted.
- The listing pages self-report showing only ~50 of 113+ entries per day; they are a partial door.
- Overlap greps: the first findstr attempt died on cmd quote-mangling; the first python walk stalled (memory/biography junctions, killed after 10+ min with zero hits printed); the bounded rerun skipped catalog.jsonl (over its 5MB size guard) and capped at 20k memory files - so it also did NOT count as the overlap check; the final run scans catalog.jsonl line-by-line plus the whole memory tree with junction pruning. Overlap fields below cite that final run only.

## Q1: cheap agent evals for 2B-8B local models, CPU-only hosts

- 2609.07370 "Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B Small Language Models for Edge Deployment" (2026-09-07): platform-agnostic CPU baseline, five sub-2B open-weight models (Phi-1.5, Pythia-1.4B, TinyLlama-1.1B-Chat, Qwen2.5-0.5B/1.5B), 100 MCP-style tool-calling prompts, metrics parseability/tool-name/argument-completeness/value-agreement; CPU resource probe (7,960 MiB and 30.78s mean latency for Qwen2.5-1.5B; 3,637 MiB and 10.63s for 0.5B). Only 5 of 1,000 raw responses were directly parseable JSON - near-total dependence on output-recovery parsing; greedy vs sampling swings Qwen2.5-0.5B from 72% to 32%. This is the nearest published template for a CPU-only grading harness. Explicit non-claim: no named boards tested, no full MCP implementation.
- 2610.02142 "Keyword Harnesses Fail Open" (2026-10-01): the ladder (lenient keyword harness, then fixed-prompt battery, then verbatim reproduction + novel-prompt generalization, then mechanism probes: first-token probability, embedding drift) runs in "minutes on CPU per checkpoint" and catches a false-positive tool-use claim (B4=0.650 lenient score on a model that passes 0/6 verbatim reproduction checks and has 10^-4 to 10^-5 prior on its own trigger token). Quote: "The ladder costs minutes of CPU time, and we argue it should gate tool-use claims on small models."
- 2609.38652 "AgBench" (2026-09-29): 60 tasks x 32 configs (2 devices x 4 architectures x 4 concurrency levels) = 1,920 executions, ~440 device-hours per full matrix; per-task verifiers hidden from the agent; measures success, completion time, goodput, API cost, sensitive-data exposure. Local-only on RTX 5090 drops 35/60 to 12/60 under concurrency; failed hybrid runs can cost MORE than cloud-only ($2.57 vs $0.72 at C=8). Local models graded on real devices, not leaderboards.
- 2610.00025 (also Q4): 4 agent microtasks x Qwen3 0.6/1.7/4/8B = 16 configs, CI-backed eligibility thresholds anchored to a cheap non-LLM baseline; 0/16 eligible, 4-bit quantization moves none into eligibility, replicates 12/12 ineligible on Llama-3.x.
- Also noted (not deep-read): 2610.03394 EdgeAgent (on-device multi-agent on Apple M4 unified memory, 1.77x speedup), 2609.21341 (8,199-run production study of an SLM database agent: 75.7% of failures involve tool calls, many server-side, not model-side).

Estate takeaway for the Gero-4B and CPU doors: a defensible CPU-only battery already exists in pieces - the 100-prompt MCP-style suite (2609.07370) + the 4-level ladder (2610.02142) + CI-anchored eligibility thresholds (2610.00025) + resource probe numbers. None alone is the Gero-4B gate; composed, they are.

## Q2: self-improvement loops with gates and ledgers vs mere claims; published falsifiers

- 2609.36043 "SAGE: A Statistical Acceptance Gate for Self-Evolving Agents" (2026-09-28) is the direct literature twin of our ratchet. Mechanism: incumbent vs candidate run on the SAME validation items; wins/regressions ledgered as discordant pairs; one-sided exact conditional binomial test (reduces to one-sided exact McNemar at lambda=1); commit only if discounted net gain > 0 AND p < alpha AND regression fraction <= tau; abstain otherwise (m=0 means p=1 means abstain). Results: regression rate lowered in 19/20 settings (36.5% to 0% on LiveMath, 42.8% to 0% on OfficeQA with DeepSeek-V4) and highest final score in all 20, equal-budget. Ablation honesty: paired comparison alone gives +6.20, the statistical test adds +2.53. Explicit non-claims: no trajectory-level error control (validation set reused), thresholds manually tuned, binary verifier only, no multi-agent claim. Our ratchet (violation_baseline accept-by-name) is stricter about debt naming; SAGE adds the math we do not have: a per-edit paired significance test before accepting a change.
- 2609.34924 "Audit the Scaffold, Not the Checkpoint" (2026-09-28): stationarity dichotomy - a fixed reachable edit set makes diminishing returns structural; escape only by expanding the edit set. Published falsifiers: per-round improvement decays toward zero on SWE-bench; churn decays geometrically over 401 production sessions; 30 same-family workers fail weighted-vote (23 of 55 tasks, 42%). This is the descent-protocol spend-theater falsifier in academic form: if the loop's edit set is fixed, ledger growth is churn, not improvement.
- 2609.38812 (2026-09-30): agents "verify often but detect little" - only 61.43% of incorrect candidates detected, only 49.36% of detected errors repaired; SCVD distillation lifts TerminalBench2.1 Pass@1 by 9.74 to 16.85 points. Direct falsifier for any "the model checked it" claim in our self-verification lanes.
- 2610.02911 "Probe the Harness" (2026-10-02): four harness details (PPO ratio source, seed propagation, replay-queue reuse across 33 updates, loss normalizers) reversed a published RL comparison; "with the harness checked, TIS matches SAN on verl"; in each flawed case "the logged quantity looked consistent with a working setup." That last sentence is the census-drift disease in RL form.
- Also noted (title/abstract level only): 2609.34198 Frozen Judges (version-dependent judge error, paired audits over judge-only release decisions), 2609.37315 executable-contract audit of agent benchmarks (7 tool defects + 1 evaluator flaw across four benchmarks), 2609.35025 AutoDataBench (agents cannot write data meeting acceptance criteria: none over 20/100 in 45 min).

## Q3: keeping burn/usage ledgers from going dark; auto-revive

Honest verdict: thin. No paper found on ledger-silence detection or auto-revival of burn ledgers as such. Nearest analogs, all read at abstract depth at most:
- 2609.36556 "MAADBench" (2026-09-29): the "refreshable paradigm" is the transferable idea - labels regenerated deterministically at zero cost per refresh, tasks drawn from a ~10^37 task space to defeat memorization; 5,200 step-labeled traces, 25 methods, 5 backbones; current anomaly-detection methods are supervision-hungry and not robust across backbones. For our burns ledger: the day-7 silence (693 rows, last ts 2026-09-28T13:45Z) is exactly the anomaly class MAADBench says current detectors miss. The estate's own cure is the scheduled-task pattern (MagFtsIndexDaily-style: detect exit 2, attempt sanctioned rebuild, alert only if silence survives the rebuild); MAADBench's refreshability argues the same design law: make a ledger's expected-next-row time a first-class stored field, not an emergent property.
- 2609.35760 TokenCast (2026-09-29, title/abstract level): forecasting token consumption during agent execution (21.3% savings under budget-control replay) - nearest thing to proactive burn accounting.
- 2609.31371 log-anomaly-detection empirical study (2026-09-25, title/abstract level): adaptation strategy, scale, quantization vs accuracy/cost/noise-robustness for LLM log monitoring.
- 2610.01223 (title/abstract level): LLM-written NumPy anomaly detectors that are GPU-free - a CPU-runnable silence detector is buildable in this style.

Falsifier for this area stands: literature gives no off-the-shelf ledger-liveness design; the estate's own scheduled-task + freshness-check pattern (B2-465 FTS daily, census patrol) is ahead of what arXiv publishes here.

## Q4: minimum viable battery before tier admission (the Gero-4B gate, repeatable)

Composed from deep reads, in order:
1. Mechanism probes first (2610.02142 level 4): first-token probability on the trigger/tool tokens and embedding-drift check vs the warm-start parent - minutes on CPU, no generation, kills "fluent but fake" admits before any suite runs.
2. Verbatim-reproduction + novel-prompt generalization (2610.02142 level 3): can it emit well-formed calls with non-identical sensible arguments on unseen entities; suppression prompt over-trigger rate reported alongside (0.087 and 0.174 in their two models).
3. 100-prompt CPU tool-calling battery with recovery-parser scoring (2609.07370): parseability, tool-name, argument completeness, value agreement; greedy AND sampled decoding (their 72% to 32% greedy/sampling cliff is the reason), plus the resource probe row (MiB, mean latency) for the tier's hardware.
4. Microtask eligibility with CI-anchored thresholds (2610.00025): 4 microtasks x the model at 2-3 precisions; pass requires the confidence bound clearing tau anchored to a non-LLM baseline; publish the raw count (they banked "0 of 16" as the headline - a negative result is a valid gate outcome, which is the whole point).
5. Budget-matched baseline comparison before any ensemble/agent-harness claim (2609.35875: across 23 SLMs and 5,500+ runs, debate ties or loses to budget-matched self-consistency - any "it works better in our harness" claim must be budget-matched).

## Overlap vs our holdings

Final scan: `.venv/Scripts/python.exe -X utf8 C:/Users/foste/AppData/Local/Temp/overlap_check3.py`, exit 0. catalog.jsonl (312,694,731 bytes) read line-by-line: 9 matching lines. memory/ walk with junction pruning: 502,760 files scanned, 79 matching lines (most are the estate's own prior-sweep grep commands recorded in trajectory logs). Verdicts:

- 2609.07370 CPU Reliability Benchmark: ALREADY HELD, not re-banked. catalog.jsonl:674049/674061/674062 (intake zone, frontier_olm_20260928 sweep: abs html 43,082 B + full html 169,792 B + full txt 48,765 B, mtime 2026-09-29), mirrored at catalog.jsonl:1082613/1082683/1082684 (ext:lsa_reboot_staging); memory/runs/corpus_gap_research/ARXIV_REGISTER.json:4514; memory/runs/corpus_gap_research/MAP_BACKFILL.md:744; battery repo already registered (memory/runs/ds_batches/cow2_items.jsonl:1, github.com/Abrar051/sml_mcp_benchmark); a prior seat read it intro through conclusion (memory/trajectory/steps.jsonl:36738).
- 2610.02142 Keyword Harnesses: abstract snapshot held (catalog.jsonl:870443, state/arxiv/2026-10-02/2610.02142v1.txt, 1,954 B); prior seats overlap-grepped it (memory/trajectory/steps.jsonl:45478 through 47171, 59486 through 59490). The full-text 4-level ladder, suppression numbers, and non-claims here are new depth; banked as an upgrade with overlap declared.
- 2610.02911 Probe the Harness: abstract snapshot held as of today (catalog.jsonl:1038306, state/arxiv/2026-10-05/2610.02911v1.txt, 1,341 B, mtime 2026-10-05T06:30:43Z); one coincidental pre-paper phrase hit (memory/runs/matthew480_20260913/hermes_out/smoke_harness__attack_anthropic__claude-haiku-4.5.md:103). Checklist content new.
- 2609.36043 SAGE: no catalog entry; a single trajectory mention as a candidate ID in a prior sweep command (memory/trajectory/steps.jsonl:37769). New to holdings.
- 2610.00025: no catalog entry; prior sweep candidate-ID lists and the prior seats' own overlap-grep commands only (memory/trajectory/steps.jsonl:58958, 58982, 59074, 59112, 59143). New to holdings as a banked item.
- 2609.34924: no catalog entry; prior-sweep grep commands only (memory/trajectory/steps.jsonl:50640, 50641, 50648, 50649, 50697, 50751, 50757, 50763). New to holdings.
- 2609.38812: zero hits on the ID, "SCVD", and "trust their own verification". New.
- 2609.38652 AgBench: zero hits. New.
- 2609.36556 MAADBench: zero hits. New.
- TokenCast (2609.35760): already cataloged (catalog.jsonl:671422, lsa zone, age_days 0); not resubmitted.

## Steal list (concrete)

1. SAGE's paired acceptance test (one-sided exact binomial on discordant pairs, lambda discount, regression-fraction cap, abstain on m=0) into the percolator/ratchet accept path - accepts become ledger facts with a p-value, matching the descent protocol's falsifier leg.
2. The churn-decay measurement (2609.34924): instrument descent weeks with per-round improvement + churn decay curves; a flat improvement curve over a growing ledger IS the spend-theater verdict, computed not argued.
3. The 61.43%/49.36% detection/repair rates (2609.38812) as the prior for any self-verification lane: "verified by the same model" is evidence of roughly half the errors at best.
4. The PTH checklist idea (2610.02911): before any A/B our lanes run, probe the harness details (seed propagation, queue reuse, normalizers) and log that the probe ran - the logged quantity looking consistent is not evidence.
5. The CPU battery composition in Q4 as the Gero-4B admission spec, with a publishable negative outcome allowed.
6. MAADBench's zero-cost deterministic label refresh as the design law for ledger liveness: store the expected-next-row timestamp and alarm on its breach (the burns day-7 silence cure, built from a published benchmark principle).

## Receipt

Doors: 6 arXiv API queries + 2 listing pages (pass 1); 3 HTML full-texts + 6 abs pages + 2 quote-recheck refetches (pass 2). Overlap scan: `.venv/Scripts/python.exe -X utf8 C:/Users/foste/AppData/Local/Temp/overlap_check3.py` (catalog.jsonl line-by-line + memory/ walk with junction pruning). All quotes above were copied by the fetch pipeline from the exact URLs named per item; two (2610.00025, 2609.38812) required a second targeted fetch because the first came back truncated, and carry lower confidence in the JSON result.
