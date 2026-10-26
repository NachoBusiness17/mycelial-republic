# Frontier sweep: swarm-orchestration via reddit - 2026-10-08

source-fetched: 2026-10-08. Area: swarm-orchestration. Doors honestly recorded below.

## Door ledger (degraded primary, two working alternates)

- old.reddit.com/r/*/top.json via WebFetch: page shell only, no JSON. DEGRADED.
- www.reddit.com and api.reddit.com: HTTP 403 Blocked (hosted fetcher AND local curl with browser UA; 189908-byte block page).
- old.reddit.com thread HTML (hosted webReader + WebFetch): login wall / nav chrome only.
- redlib.catsarch.com 429, redlib.perennialte.ch 403, rl.bloat.cat ECONNRESET.
- r.jina.ai proxy of reddit: Reddit-side 403 "You've been blocked by network security".
- Wayback Machine: no snapshots for any target thread (availability API returned empty).
- WORKING DOOR 1: safereddit.com (redlib mirror) via WebFetch: full post bodies + comments. Used for 8 of 9 deep reads.
- WORKING DOOR 2: api.pullpush.io (Reddit archive): byte-exact selftext. Worked for single-ID lookups; the bulk search endpoint 429-stormed after 36 rapid queries (my fault, retired that approach).

## Pass 1 - broad pool

40+ candidates surfaced via WebSearch site:reddit.com fallback across r/LocalLLaMA, r/LocalLLM, r/LLMDevs, r/MachineLearning, r/ClaudeAI, r/ClaudeCode on 7 query shapes (swarm/orchestration, consensus/self-consistency, parallel/429, LLM-as-judge, MoA/groupthink, subagent width, vLLM/SGLang throughput). Fresh-prefix threads (1w/1x, late Sep-Oct 2026) plus older strong-signal threads. 9 threads read end to end in pass 2.

## Pass 2 - deep reads and what they say to our questions

### Q1 - width A/B (workflow max_concurrency 3 vs Task agents 10-12)

- Opencode config for maximum parallelism (r/LocalLLaMA, 2026-03-09, u/HlddenDreck + u/PsychologicalRope850): "Set a hard max parallel subagents so you don't saturate RAM + KV cache bandwidth" and "The big win is role-based concurrency, not pure token throughput on one request." Their measured failure: 3-4 same-role coders on ONE endpoint with huge context produced contention and degraded outputs. Width degrades QUALITY per endpoint before it degrades throughput. Direct A/B design input: our two proven shapes differ in retry shape AND per-child endpoint pressure; record per-endpoint concurrent load as a covariate, not just width.
- PSA: Agent Teams vs Subagents (r/ClaudeAI, 2026-02-05): u/bittabet's team head "spawned almost 90 agents in parallel which of course killed my usage limit in like two minutes" - the vendor-usage-limit twin of our workflow-children 429-storm. Hub-and-spoke vs peer-shared-task-list are two dispatch shapes with different overheads; 53 isolated agents via bash needed separate synthesis prompts (interagent pass-off is load-bearing, matching our gate).
- I'm pretty close to the middle thanks to you all (r/LocalLLaMA, ~2026-10-03, 624 upvotes, FRESH): u/FingerGnumerics boosted "VLLM serve slots from 2 to 8 concurrence" under a big-model-orchestrates-4B split; input:output token ratio fell 75:1 to 10:1; Qwen 4B did ~2/3 of 300k records in 24h. Counterpoint in-thread (u/taytay735): smarter models need fewer tokens/steps, so raw token comparisons mislead - a confound our A/B must pin (same model+version both arms, else the width effect is confounded with step-count effects).
- Agent swarm coordination (r/LocalLLaMA, ~2026-09-30, FRESH): u/devoidfury runs a manager that "coordinates, designs, and calls workflow graphs, spinning up multiple agents, each can use from a defined pool of models" - used qwen3.8-flash-next across 3 systems to review ~100 harnesses. Also the local-worker/cloud-reviewer split (our janitor/specialist shape) endorsed by u/No_Product_5759 with "cap iterations and concurrency; benchmark against a single-model baseline" - the community independently prescribes OUR width A/B including the baseline arm.

The A/B itself cannot be run from a sweep seat; it is an on-box experiment. Reddit contributes the covariates: per-endpoint concurrent load, model-version pinning, step-count confound, baseline arm.

### Q2 - flock decode, consensus-strength as anti-signal

- Markovian RSA with Zaya1-8B (r/LocalLLM, 2026-06-12, u/PatC883): N=8, K=3, T=2 on AIME; pass@1 67.5% vs RSA 5/5, per-trace 67.5% to 82.5%. The Q2 steal is the failure decode: on AIME24 I-2 "the self-consistency 'majority' was literally one ballot (the only extractable answer), so it won by luck". Their recommendation: "run self-consistency (N=8, vote, no aggregation round) as the default". DECODE = count extractable ballots before reading vote strength; a high-strength consensus built on 1/8 ballot participation is luck, not signal. This is exactly a decode that maps consensus onto the actual task output space (ballot-extraction rate), the thing Q10 asks for.
- Agent Zero v1.0 (r/LocalLLaMA, 2026-02-07, u/brownman19): Kuramoto coherence score r in [0,1] with a TWO-SIDED band: below 0.3 triggers intervention, above 0.95 "signals groupthink risk". An external implementation encoding HIGH consensus strength as a failure flag, converging with our 0/3 wrong-at-high-strength finding. Honest caveat: 17% upvoted, 2 comments, skeptical reception - steal the two-sided-band idea, not the validation. Dogfood answer for "next sweep's own review pass": score the review flock's coherence AND flag >0.95 bands as probe-escalation triggers, pairing with ArcticSwarm's 82.6 vs 63.5 counter-evidence.

### Q3 - probe-first verification vs paid judge

- Is LLM-as-a-judge actually reliable? (r/LLMDevs, 2026-07-06, u/larabyeol, 50k outputs/week): "30%+ disagreement rates" when the SAME outputs were scored two weeks apart - caused by a silent GPT-4o update, took 2 months to notice. Position bias (prefers first output), self-preference (GPT-4o grades GPT-4o generously). Fixes: pin judge prompt+model version; run judge twice with swapped positions; u/eddzsh: judge from a different model family than the generator (OP: "cut the gap noticeably") - INDEPENDENT CONVERGENCE with our judge2 second-family law (lens/laws.md Q7). u/Kind-Atmosphere9655's triage shape is literally probe-first: deterministic format/schema/JSON checks in code, judge only for subjective axes, measure false-pass/false-fail at the actual threshold rather than global agreement, route confident to auto and near-threshold to human/judge. Strongest external support for replacing the paid-judge-first pass.
- We Discovered Why Your LLM Judge Results Are Lying (r/learnmachinelearning, 2026-05-26, LayerLens): three-judge panels across 196 models/54 benchmarks: "78% of judgements reach full consensus" / 18% majority 2-of-3 / "4% have no consensus < this is where the ambiguity lives". Byte-exact selftext via pullpush. Judge-model selection matters more than expected (GPT-4 conservative, mistral permissive); disagreement pattern = task-design signal. For our register rows: if probe flags the disagreement minority, judge2 spend concentrates on the ~4-22% ambiguous band, not all rows.

### Q4 - pheromone bus claim atomicity

- Agent swarm coordination comment by u/EnvironmentalLeg8506: "One catch: once the folder syncs between machines, the move isn't atomic anymore." / "Keep the claiming for a given task type on one machine, or live with the occasional duplicate." - a wild-type report of EXACTLY our [a,b,c] vs [a,b,c,c] duplicate-claim falsifier: claim moves that are non-atomic across sync boundaries mint duplicate task assignments. Their mitigations (single-machine claiming; accept occasional duplicates) bracket our MAG_POSITION_BOUND_LEAVES test. u/Salt_Hyena5896: "Also add a max-hop/dead-letter path so a bad tool result can't make the swarm loop forever."
- Considered, NOT banked: "I built a hive mind for Claude Code" (r/LocalLLaMA, 2026-01-26) - SQLite+FTS5 shared memory + message bus; OP admits "Sometimes one agent keeps assigning tasks to itself in an infinite loop" and is fleeing SQLite concurrency for postgres. Relevant self-claim-loop failure mode, but the thread is promo-contaminated (paid-upvote accusations, fork-of-claude-flow allegations) with zero numbers; not banked as a top-8 item, recorded here for the failure-mode ledger.

### Q5 - G2 blind-sweep placement law enforcement cost

No Reddit evidence found either way (searched blind sweep / placement / gate latency shapes). OWED - this question is only answerable by our own two-run scenario-card experiment; no external steal exists.

## Overlap ledger (grep vs holdings)

- Thread IDs 1u3j4id/1toe6ir/1rotukw/1qwwadp/1qnjota/1wu3rio/1up5owd/1wmmdlz/1qy9lzl/1rumv62/1qv7lo6: zero hits in catalog/catalog.jsonl and memory/ (git grep).
- "Kuramoto": 3 catalog hits = our own docs/ref/RESEARCH_NOTE_FLYWHEEL_BUDGET_PROJECTION.md (budgeted Hebbian Kuramoto) + a Kuramoto-Sivashinsky PDE arxiv paper. Conceptual overlap with our own note; the Agent Zero thread is an independent implementation, banked with that caveat.
- "LLM-as-a-judge": 10 catalog hits = openai-cookbook Custom-LLM-as-a-Judge assets + phoenix docs. Tooling docs, not reliability empirics. New.
- "self-consistency": 5 hits = cookbook figures + arxiv perturbation paper + ai-engineering-from-scratch book chapter "Voting, Self-Consistency, and Debate Topology". The RSA thread's ballot-participation decode is adjacent to the chapter but a distinct empirical artifact.
- "Agent Teams": 3 hits = our memory/research_packs/bibverify/dsh-teams.md + arxiv interchangeability paper + book chapter. Neighbor holdings; the PSA thread's 90-agent runaway data point is new.
- Catalog has essentially no reddit-thread holdings (2 rows total mention reddit.com; one is a sesame-ai prompt-leak source). All 8 banked items are new territory.

## Banked items (strongest first, 8 of 9 read)

1. Agent swarm coordination - r/LocalLLaMA - 2026-09-30 - https://www.reddit.com/r/LocalLLaMA/comments/1wu3rio/agent_swarm_coordination/
2. I did the Markovian RSA thing with Zaya1-8B - r/LocalLLM - 2026-06-12 - https://www.reddit.com/r/LocalLLM/comments/1u3j4id/i_did_the_markovian_rsa_thing_with_zaya18b/
3. Agent Zero v1.0 (Kuramoto) - r/LocalLLaMA - 2026-02-07 - https://www.reddit.com/r/LocalLLaMA/comments/1qy9lzl/agent_zero_v10_opensource_multiagent_coordination/
4. Is LLM-as-a-judge actually reliable for grading outputs? - r/LLMDevs - 2026-07-06 - https://www.reddit.com/r/LLMDevs/comments/1up5owd/is_llmasajudge_actually_reliable_for_grading/
5. We Discovered Why Your LLM Judge Results Are Lying - r/learnmachinelearning - 2026-05-26 - https://www.reddit.com/r/learnmachinelearning/comments/1toe6ir/we_discovered_why_your_llm_judge_results_are_lying/
6. Opencode config for maximum parallelism - r/LocalLLaMA - 2026-03-09 - https://www.reddit.com/r/LocalLLaMA/comments/1rotukw/opencode_config_for_maximum_parallelism/
7. PSA: Agent Teams vs Subagents - r/ClaudeAI - 2026-02-05 - https://www.reddit.com/r/ClaudeAI/comments/1qwwadp/psa_agent_teams_subagents_heres_the_actual/
8. I'm pretty close to the middle thanks to you all - r/LocalLLaMA - ~2026-10-03 - https://www.reddit.com/r/LocalLLaMA/comments/1wwbcdt/im_pretty_close_to_the_middle_thanks_to_you_all/

Quote provenance: item 5's quote is byte-exact from pullpush JSON (confidence 0.95). Items 1-2 quotes were extracted in a dedicated verbatim-extraction pass over safereddit (0.8-0.85). Items 3,4,6,7,8 quotes are strings the fetch digest marked as quotations (0.7-0.8) - a digest layer stands between page and quote for those; flagged per the no-fabrication law.
