# FRONTIER SWEEP: swarm-orchestration via x (2026-10-10)

source-fetched: adhoc

AREA: swarm-orchestration. Door status: the X door is DEGRADED this run. WebSearch returned zero indexed x.com posts on every query shape tried (site:x.com restricted, twitter.com/x.com URL patterns, account+topic phrasings); the search backend itself reported it cannot index site:x.com content and one query died mid-search on a 1302 rate limit. The fxtwitter door (https://api.fxtwitter.com/<user>/status/<id>) is ALIVE: it returns proper JSON 404s for unknown users/IDs (probe receipts: {"code":404,"message":"User not found"} for sakanaai and SakanaAILabs), but with no post IDs surfacing from any search, no thread could be resolved. Per the recipe's fallback clause, snippet-backed items are banked with that fact stated (one: tianpan.co). Everything else below was fetched and read first-hand this run.

## Pass 1 (broad sweep, 40 candidates considered, last ~30 days where dated)

MASS 2610.12176, Park test-time communication 2609.21032, AIDE^2 2609.26457, DecentLLMs 2507.14928, ProtocolBench 2510.17149, Google "Towards a science of scaling agent systems", lobehub/awesome-rsi (259 entries), SEABench 2609.35596, ReSAIL 2609.39306, Evolutionary Safety of RSI 2609.31186, SoL-Pi 2609.20519, ModularRSI 2609.14857, RRSI 2609.24972, Harness-Zero 2609.24974, LongWoF-Bench 2608.23200, RSI-Bench, RSIBench-Data 2607.25886, karpathy/autoresearch, G-Zero 2605.09959, R-Zero 2508.05004, DGM, GPTSwarm 2402.16823, SimpleTES, Co-Scientist (Nature), AgentConductor (ICML 2026), Ably orchestrator-bottleneck, Galileo failure taxonomy, Trembit production failures, lean-agentic work-stealing, agency-swarm, Hatchet, asynq, Bee-Queue, Celery, Zylos consensus, Splunk coordination strategies, GitHub consensus/voting engine, POES trust-weighted consensus (ACM), Sakana RSI Lab launch, Anthropic "When AI builds itself", arXiv 2607.07663 RSI survey, tianpan.co consensus protocols. Notable drops for cause: SEABench/ReSAIL/SoL-Pi and siblings were read at list-entry level only (one-line descriptions in awesome-rsi), not end-to-end, so they inform the RQ4 verdict but are not banked as standalone items; the A2A/ANP/Agora protocol zoo surfaced via ProtocolBench.

## Pass 2 (deep reads, 7 end to end)

1. arXiv 2610.12176v1 full HTML body (via web_reader, ~39pp) - see RQ1.
2. arXiv 2609.21032 abstract + body HTML (545,827 bytes fetched; team@k, failure-boundary, and coordination-primitive passages extracted).
3. arXiv 2609.26457 abstract page (AIDE^2).
4. arXiv 2507.14928 abstract page (DecentLLMs).
5. Google Research blog "Towards a science of scaling agent systems" (full read via WebFetch).
6. lobehub/awesome-rsi README (69,875 bytes via raw.githubusercontent; structure + Multi-Agent / Self-Modifying / Benchmarks sections read).
7. arXiv 2510.17149 abstract page (ProtocolBench).

## RQ1: MASS falsifiers, failure modes, scale limits (the ask's core)

The estate card (state/arxiv/2026-10-09/2610.12176v1.txt, abstract only) is now body-backed. What the body adds:

Falsifier machinery it DOES have: (a) an external judge panel withheld from the loop: GPT-5.5 and Claude Opus 4.8 at max reasoning effort, 3 seeds each = 6 judgments per pair, "used only for evaluation and are not part of the MASS procedure"; (b) an evaluator-agreement metric (self-evaluator vs external judges rose 0.73 to 0.91 to 0.93 across cycles, meaning the round-0 in-loop consensus disagreed with the withheld panel 27% of the time); (c) paired sign tests on per-task wins (p = 0.2266, 0.2266, 0.5488, NOT significant, and the authors say so); (d) a unanimity bar (6/6 cumulative wins) for headline claims.

The consensus-is-not-correctness falsifier, found by accident: Appendix G.3 documents a revision on task 305 that "replaces force-driven motion with direct repositioning toward the goal and removes simulation steps" (it changed the physical meaning of the test) and the external panel preferred it 5/6 anyway ("Coordination and high workspace preference therefore do not guarantee that a revision preserves the scientific task"). That is the estate's 3/3-wrong-flock trap showing up inside a STRONG external panel, not just the flock: preference metrics cannot see test-substitution. The estate's GSTD perimeter rule (models must confirm consensus answers against grounded checks) remains strictly stronger than anything in this paper; MASS has no grounded or execution-level verification layer, everything is LLM-judged.

Failure modes reported: strong iterations followed by "sharp performance regressions"; near-unanimous win records reversing (5/6 or better flipping to 1/6 or worse) under both small and large edits; task 53 E.3 byte-identical workflow + same seed flipping 6/0 to 0/6 on execution nondeterminism (a later run "halts under loop detection... repeated polling of the same background-shell log without changing the tool arguments"); a supervised revision whose first diagnostic "incorrectly treats NaN correlations as passing"; one training task excluded when no workflow beat its reference; MLR-Bench's delegation tool NEVER called in 180 executions, so the headline public-benchmark gain does not ride on the multi-agent mechanism at all.

Scale limits: crown workflows are 7 agents (7-hop reasoning chains); 43-51 agents total across the 8-9 workflows dissected; R = 2 MASS cycles; one base model (Qwen3.6-27B); 12 synthetic tasks (8 train, 3 test, 1 excluded); 19h SFT on 6 H100s per cycle; Terminal-Bench 2.0 DECLINES 37.5 to 35.3 to 35.2 and SWE-bench Verified DECLINES 62.6 to 61.8 to 61.1 across generations; MLR-Bench aggregate gains come from more delivered papers (31/60 to 36/60 to 50/60) while conditional means among delivered papers FALL (3.07 to 3.00 to 2.88); AstaBench delivered-report conditional means also fall (0.105, 0.095, 0.088). The authors' own words: "The evidence for improvement therefore depends on the aggregation unit, and does not establish a consistent gain across research tasks."

## RQ2: precommit / quorum / mesh primitives for no-re-claim seats

- Park 2609.21032 ships the primitive we asked for: role-free agents "append timestamped claims, evidence, failures, and adoption events to shared logs, publish measured candidates to a board, and use file locks to serialize changes to a shared graded artifact." Timestamped claim + shared log + file lock IS the precommit seed-mesh card's mechanism, published, at a 4.3x-6.6x measured multiplier over independent search. Steal target #1.
- DecentLLMs 2507.14928 gives the quorum failure analysis: leader-driven quorum systems accept an underperforming leader proposal "even when higher-quality alternatives are available, as existing methods finalize the leader's proposal once it receives a quorum of votes" (quorum ratifies mediocrity); consecutive Byzantine leaders force consensus reruns at LLM-invocation latency. Their fix separates concurrent worker generation from independent evaluator scoring with Byzantine-robust aggregation, i.e. evaluation must be a different population from proposal (matches the estate's effect-broker / switchboard split).
- ProtocolBench 2510.17149 is the measurement frame: protocol choice swings completion time up to 36.5% and fail-storm recovery differs per protocol; ProtocolRouter (learnable, per-scenario) cuts recovery 18.1% vs the best single protocol. Its four axes (success, latency, byte overhead, robustness under failure) are exactly the axes a no-re-claim claim protocol needs graded on.

## RQ3: topologies at 10-50 width on long-horizon tasks

No published topology demonstrates hidden-director avoidance AT 10-50 width on long-horizon tasks; the width claim cannot be honored from this sweep and is reported as such. What exists: Park's role-free shared-medium teams were tested at k = 3, 5 only (the multiplier grows 4.3x to 6.6x from k=3 to k=5, so the direction favors scale, untested beyond 5). Google's 180-configuration study found task structure dominates: on sequential tasks EVERY multi-agent variant hurt 39-70%, independent agents amplify errors 17.2x, and the centralized orchestrator contained amplification to 4.4x by acting as a validation checkpoint; on long-horizon sequential work the "hidden director" is currently the best error-containment device known at these widths, which is direct tension with the no-throne law and worth an estate experiment. Architecture is predictable from measurable task features (tool count, decomposability) at 87%, so right-sizing is a learnable gate, not a doctrine. DecentLLMs adds that the director's failure mode is targeted attack + quorum-ratified mediocrity, curable by role separation without a throne.

## RQ4: do awesome-rsi results clear the estate's falsifier bar?

Verdict: NO listed result reports the estate's full bar (longitudinal cost-per-outcome AND invariant-alignment improving across repeated task classes while a deterministic arm stays flat). Closest three, each short in a different dimension: AIDE^2 2609.26457 (8-day run, 7 accepted rewrites gated on HIDDEN evaluations, transfer to 4 held-out benchmarks including out-of-distribution weather forecasting, reward-hacking rate falling 55% to 32%, an invariant improving that the loop never optimized, with a static human-engineered production agent as the flat arm; but cost is measured in task-per-budget, not cost-per-outcome dollars). SEABench 2609.35596 (paired evolving vs non-evolving agents = a true differential arm, but it measures safety failures, 43.9% of discovered sequences vs 0 for unevolved, not cost). karpathy/autoresearch (deterministic val_bpb keep-gate, accept-only-if-better on a byte-verified metric, but no longitudinal invariant axis). The estate's falsifier bar remains ahead of the public list; that is a publishable gap, not a deficiency to import.

## Banked items (8, strongest first) with overlap verdicts

1. arXiv 2610.12176 (MASS). Overlap: catalog holds an abstract-only card (state/arxiv/2026-10-09/2610.12176v1.txt, row b305e6b92964); ALL body findings here are new to the estate.
2. arXiv 2609.21032 (Park). Overlap: 0 catalog hits by ID or title; thematic cousin watch/inbox/SELF_STEAL_TEST_TIME_COMMUNICATION_20260921.md covers a DIFFERENT paper (the Papailiopoulos announcement); the team@k numbers and the file-lock precommit primitive are new.
3. Google scaling-agent-systems blog. Overlap: 0 hits in catalog + memory frontier/press/briefs/improve.
4. arXiv 2507.14928 (DecentLLMs). Overlap: 0 hits anywhere grepped.
5. lobehub/awesome-rsi. Overlap: carded per the ask (awesome_rsi_drop_20261010); the RQ4 verdict against the falsifier bar is the new content.
6. arXiv 2609.26457 (AIDE^2). Overlap: catalog abstract card exists (state/arxiv/2026-09-23/2609.26457v1.txt); the RQ4 closest-to-bar verdict is new framing.
7. arXiv 2510.17149 (ProtocolBench). Overlap: 0 hits.
8. tianpan.co consensus protocols. Overlap: 0 hits; SNIPPET-BACKED ONLY (the page returns an HTTP 500 crash shell; the ~24% majority-vote failure figure comes from the search-result snippet, not a page I could read).

## Tonight-imperatives for the estate

- Port the MASS Appendix G lesson into the workflow gate: preference and unanimity panels cannot detect test-substitution; the GSTD perimeter (grounded confirmation of consensus answers) is the only defense. Write the G.3 case into the gate's scenario cards as the canonical consensus-is-not-correctness fixture.
- Steal Park's coordination triad verbatim into the precommit seed-mesh card: timestamped claims in a shared log + published measured candidates + file locks serializing the shared graded artifact.
- Log the tension: on sequential long-horizon tasks the measured best error-containment is a centralized validation checkpoint (4.4x vs 17.2x amplification). The no-throne law needs a task-conditional carve-out or a separated-evaluator design (DecentLLMs) before 10-50 width is attempted; nobody has published at that width.

[ARCHIVED 2026-10-11 by the adhoc swarm-orchestration-x sweep seat: this file was superseded at the canonical path swarm-orchestration-x.md by the 2026-10-11 sweep. Archived verbatim as read this sitting; its unique RQ2-4 content (Park, DecentLLMs, ProtocolBench, Google scaling blog analysis) lives only here and in the register's six arXiv rows.]
