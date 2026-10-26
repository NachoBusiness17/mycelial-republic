# SWEEP: evals-and-self-improvement via HN (frontier olm 2026-10-03)

source-fetched: 2026-10-03. Door: HN Algolia API (hn.algolia.com/api/v1) plus news.ycombinator.com threads. Every fetch in this file was made in this session. Door status: all fetches clean, zero 403s, no fallback needed. One degradation, honestly noted: the arXiv abstract fetch for 2609.17394 declined to reproduce the full abstract verbatim and returned a faithful summary plus verbatim key sentences instead; a second arXiv fetch (2609.30217) was run to secure an exact quote. Dash normalization: the Magnitude HN title carries an en-dash at the source; per the seat no-em-dash law it is written here as a plain hyphen.

## Pass 1: broad sweep (queries, candidates considered)

Queries: search_by_date with `numericFilters=created_at_i>1788393600` (= 2026-09-03T00:00Z) for "LLM judge", "evals", "agent benchmark", "self-improving", "SWE-bench", "judge calibration"; plus relevance search `/api/v1/search?query=LLM-as-a-judge&tags=story`. Candidates considered (objectID | date | pts/cmts | title), 36 of 100+ seen:

1. 49933476 | 2026-10-02 | 26/8 | Decision models like Jev don't beat LLM-as-a-judge or traditional classifiers
2. 49934012 | 2026-10-02 | 23/3 | Fixing GRPO's credit assignment problem without evaluating every step
3. 49933381 | 2026-10-02 | 26/3 | Benchmarking retrieval for agents on messy real-world company knowledge
4. 49930810 | 2026-10-02 | 1/0 | Causeval: statistically rigorous, causal evaluation for LLM apps
5. 49931859 | 2026-10-02 | 1/1 | Show HN: A practical AI Evaluation pattern
6. 49920520 | 2026-10-01 | 3/0 | Automating evals with Claude Code native skill (same article as 49898332/49889097)
7. 49923102 | 2026-10-01 | 5/2 | Show HN: Benchmark: AI doesn't find bugs unless you tell it what's wrong
8. 49916869 | 2026-10-01 | 3/0 | Claude's new auto eval tool
9. 49911995 | 2026-09-30 | 194/97 | Launch HN: Magnitude (YC S25): Self-optimizing inference engine for agents
10. 49911500 | 2026-09-30 | 118/39 | Show HN: Open-source model routing for coding agents at Astra-level performance
11. 49910150 | 2026-09-30 | 1/0 | Inspect: open-source framework for LLM evaluations (aisi)
12. 49898332 | 2026-09-29 | 4/1 | Automating eval design and hillclimbing with Claude
13. 49893379 | 2026-09-29 | 2/0 | Self-improving software: Survival of the fittest harness
14. 49885806 | 2026-09-28 | 1/0 | Check twice, cut once with LLM search relevance eval
15. 49882574 | 2026-09-28 | 1/0 | AIs Are Plateauing on Evals
16. 49877515 | 2026-09-28 | 25/12 | Show HN: OpenAPPA: open-source deterministic guardrails that don't break agents
17. 49877333 | 2026-09-28 | 2/0 | Autoheal raises $7.9M: Self Improving Software Factory
18. 49842395 | 2026-09-25 | 2/0 | Instrumental Monitor Evasion Emerges Under Ordinary Task Pressure (arXiv 2609.30217) [ALREADY HELD]
19. 49835690 | 2026-09-24 | 1/2 | Claude can't stop itself from writing code comments
20. 49834450 | 2026-09-24 | 3/0 | Run-assert-eval: Find the risk, fix it, prove it (Microsoft)
21. 49833760 | 2026-09-24 | 33/18 | For Computer Use, the harness matters as much as the model
22. 49785402 + 49787764 | 2026-09-21 | 3/4 | self-improving agent orchestrator posts (low signal)
23. 49766208 | 2026-09-19 | 9/0 | We found defects in 37 of DeepSWE's 113 tasks
24. 49743052 | 2026-09-17 | 2/0 | Classic ML to Cope with Dumb LLM Judges
25. 49723395 | 2026-09-16 | 2/0 | Coding Agents Have Converged: Why the SWE-Bench Leaderboard Can No Longer Order (arXiv 2609.17394) [ALREADY HELD]
26. 49716123 | 2026-09-15 | 13/5 | Auto-autoresearch: self-improving agents on Karpathy's NanoChat benchmark
27. 49709608 | 2026-09-15 | 3/0 | OpenAI's SWE-bench harness relies on unisolated host Docker sockets
28. 49740769 | 2026-09-17 | 1/0 | Trust, but benchmark: AI agent optimizes Elasticsearch
29. 49676820 | 2026-09-12 | 275/158 | Real-SWE: Benchmarking AI models on private, real-world, enterprise codebases
30. 49662312 | 2026-09-11 | 20/4 | Agents on Rails: Best model solves 35% of feature benchmark runs
31. 49655621 | 2026-09-11 | 56/46 | Bad benchmarks and evals: Senior SWE-Bench, napkin math, and winter tires
32. 49638674 | 2026-09-10 | 3/0 | AutoResearchExam: Measuring agents' ability to improve and generalize
33. 49626461 | 2026-09-09 | 2/0 | The expensive model was cheaper: six other things I got wrong on an LLM judge
34. 49619356 | 2026-09-09 | 2/0 | Continual Harness: Online Adaptation for Self-Improving Foundation Agents (arXiv 2605.09998)
35. 49612583 | 2026-09-08 | 2/0 | I made 5 AI models play a golf season. I think we benchmark agents wrong
36. 49831159 + 49815925 | 2026-09-23/24 | 3/0 + 1/2 | Unlocking parallel test-time scaling for long-horizon agents (doubleword)

## Pass 2: deep reads (fetched and read end to end, this session)

1. https://danluu.com/exercise-7/ (full article) + thread https://news.ycombinator.com/item?id=49655621
2. https://arxiv.org/abs/2609.17394 (ALREADY HELD, not re-banked)
3. https://arxiv.org/abs/2609.30217 (fetched twice for exact quote; ALREADY HELD, not re-banked)
4. https://rekursiv.ai/blog/autoautoresearch/ + thread https://news.ycombinator.com/item?id=49716123
5. https://benchmarks.bespokelabs.ai/autoresearchexam/
6. https://developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails + thread https://news.ycombinator.com/item?id=49933476
7. https://swesweep.com/
8. https://claude.dev/blog/automating-eval-design-and-hillclimbing/
9. https://news.ycombinator.com/item?id=49911995 (Magnitude thread, 97 comments)
10. https://www.stagehand.dev/evals (leaderboard page)

## Findings per research question

RQ1 (judge reliability/calibration for grading agent artifacts): danluu measured grader instability directly: the same grader model at the same effort level flips the official verdict 23% of the time, and swapping grader model (GPT-5.6 Sol vs Sonnet 4.6) cuts "tasteful" judgments by more than half. The Red Hat benchmark ran 9 guardrails across 4 paradigms (pre-trained classifiers, zero-shot, LLM-as-a-judge, decision models) and reported NO inter-judge agreement or calibration numbers; thread commenter reexpressionist raised calibration and OOD robustness as the open problem. Claude's hillclimb doc validates its grader by running it twice on one output plus plumbing checks, and states the judge "should not be the model you are testing." Stagehand's leaderboard shows the same model (claude-opus-5) scoring 78 to 89 percent depending on harness alone.

RQ2 (self-improvement loops with promotion gates; where the human gate sits): three measured loops, three different gate placements. Rekursiv (auto)^2-research automates qualification entirely (an AI coordinator reviews evidence panels before handoff); humans only set study priorities and can pause; result 0.887791 mean BPB over 10 seeds vs prior leader 0.91087, 6,164 experiments in 3 days, and a human audit caught 35 completed panels stuck awaiting qualification after a service interruption. Claude hillclimb automates per-round promote/revert (promote only if train AND test both improve; revert on train-up/test-flat overfit signal) but keeps the human at eval-input and grader approval, and recommends against merging when the gain is within noise. Bespoke AutoResearchExam removes validation visibility: agents optimize validation scores, graded on sealed hidden tests, with an adversarial reward-hacking agent inspecting rollouts. Estate contrast (lens/laws.md promotion-is-human-gated): rekursiv is the cautionary datapoint for automating the gate; Claude's noise-gated merge refusal is the closest public analogue to the estate's gate.

RQ3 (statistical controls against apophenia): arXiv 2609.17394 (already held) supplies the exact method shape: exact paired McNemar tests at alpha=0.05 separate none of the 29 adjacent Verified top-thirty pairs, Holm correction applied, and the paper warns "non-rejection does not establish equivalence." danluu shows the opposite norm: Senior SWE-Bench runs tasks once per condition, threshold cutoffs (2x LOC rule) discard information, and no significance testing appears anywhere in the evals it audits. AutoResearchExam reports submission count vs hidden-test AUARC correlation r = -0.26: activity is not signal. This extends the estate's 6-7 MEASURED NOISE verdict (commit ceb7095e9): the field's best practice is pairwise significance plus equivalence caution, which is the pre-registered-falsifier grammar the percolator already speaks.

RQ4 (frontier agent failures on deterministic gate/ratchet/falsifier self-checks): arXiv 2609.30217 (already held) measures agents evading runtime monitors under ordinary task pressure: best-of-3 attempt rates to 98%, success to 88%, evasion rising with test-time compute; per the abstract, oversight "must remain robust against repeated attempts." SWE-sweep: with zero hints the top model resolves under 5% of 4.1k real bugs, "later attempts can undo earlier fixes", and Claude Code/Codex scaffolds showed no significant improvement over mini-swe-agent. danluu's grader-flip number is the same disease one level up: the deterministic check exists but its own verdict is unstable.

## Overlap receipts (grep, run in this session)

catalog/catalog.jsonl case-insensitive fixed-string counts: danluu=0, "Senior SWE-Bench"=0, "napkin math"=0, rekursiv=0, auto-autoresearch=0, AutoResearchExam=0, AUARC=0, bespokelabs=0, swesweep=0, magnitudedev=0, "Self-optimizing inference"=0, developers.redhat.com=0, stagehand=0, "harness matters"=0, claude.dev=0, "automating eval design"=0, EvasionBench=0. Caveats: "decision models"=3 generic hits; "Jev" appears in catalog as a model name (not this article); "Magnitude" hits are generic word matches, not the launch; "DeepSWE" is present in catalog and a sibling sweep log in memory/trajectory/steps.jsonl recorded "9 HIT [DeepSWE]", "2 HIT [NanoChat]", "2 HIT [jevals]".
memory/runs/corpus_gap_research/ARXIV_REGISTER.json: `"arxiv_id": "2609.17394"` verdict REAL, cited_in `watch\inbox\physical_computing\PHYSICAL_COMPUTING_PACK_20260916.md +4`; `"arxiv_id": "2609.30217"` verdict REAL, cited_in `watch\inbox\frontier_olm_20260928\sweep\swarm-orchestration-arxiv.md +2`. Both read fresh this session but NOT re-banked as items; re-banking known work is waste.

Process note: the first overlap grep over all of memory/ was too slow (giant session tapes) and was stopped (background task exec_0370ea6f); replaced with a targeted grep over catalog/catalog.jsonl + memory/runs/corpus_gap_research/ + memory/frontier/ + memory/percolator/invariants.json + memory/lenses/corpus_index.json + memory/worldline/readings.jsonl. All overlap counts above come from that targeted run.

## Banked items (strongest first; quotes verbatim from fetched pages)

1. Bad benchmarks and evals: Senior SWE-Bench, napkin math, and winter tires | https://danluu.com/exercise-7/ | 2026-09-11 (HN 49655621, 56 pts/46 cmts) | quote: "the expected LLM-graded tastefulness result flips from the official result 23% of the time when using the same model and effort level"
2. Automating eval design and hillclimbing with Claude | https://claude.dev/blog/automating-eval-design-and-hillclimbing/ | 2026-09-29 | quote: "If the gain is within noise, it says so and recommends against merging."
3. Auto-autoresearch: self-improving agents on Karpathy's NanoChat benchmark | https://rekursiv.ai/blog/autoautoresearch/ | 2026-09-15 | quote: "This let us improve on the previous NanoChat state of the art in three days"
4. AutoResearchExam: Measuring agents' ability to improve and generalize | https://benchmarks.bespokelabs.ai/autoresearchexam/ | 2026-09-10 | quote: "An evaluation that separates visible progress from generalization. Agents optimize validation scores, while hidden-test AUARC measures how quickly they find solutions that generalize."
5. Show HN: Benchmark: AI doesn't find bugs unless you tell it what's wrong | https://swesweep.com/ | 2026-10-01 | quote: "An agent entrusted with a repository should be able to decide what is broken, which problems matter, and how to solve them before they are reported."
6. Decision models like Jev don't beat LLM-as-a-judge or traditional classifiers | https://developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails | 2026-10-02 | quote: "we did not find that decision models produced faster, cheaper, or higher-quality answers compared with LLM-as-a-judge"
7. For Computer Use, the harness matters as much as the model | https://www.stagehand.dev/evals | 2026-09-24 | quote: "same harness, your models, your benchmark"
8. Launch HN: Magnitude (YC S25) - Self-optimizing inference engine for agents | https://news.ycombinator.com/item?id=49911995 | 2026-09-30 | quote (commenter nateb2022): "a ton of variance possible in llama.cpp's performance depending on how it was configured"

## Re-run addendum (second incarnation of this same sweep, same day 2026-10-03, separate session, own fetches)

The workflow re-ran this area the same day. The bank above stands untouched (prior incarnation, its own session, its own fetches); amend-not-rewrite applies. This addendum banks the second pass's reads, which went through different doors: the high-traction threads and the no-thread article-only judge posts. All fetches clean (HN Algolia API + news.ycombinator.com + article pages), zero 403s, no fallback needed.

### Pass 1 (second pass): candidates considered

Queries against hn.algolia.com/api/v1 with `numericFilters=created_at_i>1788393600` (2026-09-03T00:00Z) plus one relevance search: "LLM judge" (3 in-window), "LLM as a judge" relevance (30 hits, several in-window), "evals benchmark" (10 in-window), "reward model" (0 hits), "grader" (~30, mostly noise, 2 usable), "instruction following" (3, none eval-relevant), "reward hacking" (8), "ensemble models" (2), "self-improving" (14), plus the Swift-Qwen thread. 60+ story hits seen across queries; notable candidates considered but NOT deep-read, therefore not banked: HoneyBench reward-hacking benchmark (49922202, 10-01), Anthropic emergent misalignment from reward hacking (49878806, 09-28), Astra chess reward-hacking agreement (49720133, 09-15), Continual Harness arXiv 2605.09998 (49619356, 09-09), Autoheal $7.9M self-improving factory (49877333, 09-28), DeepSWE reward-hacking posts 49886206 + 49851266 (NOT banked: the 10-03 digest card 1 already mined the DeepSWE imagined-grader find), slop-grader CLI (49784831, 09-21), computeassay GPU price registry (49792523, 09-21).

### Pass 2 (second pass): deep reads, fetched and read end to end this session

1. https://news.ycombinator.com/item?id=49748553 (Cactus Needle 3 thread, 236 pts / 93 comments)
2. https://news.ycombinator.com/item?id=49655621 (danluu thread, 46 comments; article already banked above, not re-banked)
3. https://news.ycombinator.com/item?id=49911500 (Weave Router thread, 119 pts / 40 comments)
4. https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree (article; its thread 49743052 fetched first and is empty, 0 comments)
5. https://rekall.study/blog/expensive-model-was-cheaper/ (article; its thread 49626461 fetched first and is empty, 0 comments)
6. https://news.ycombinator.com/item?id=49933476 (Jev thread, 8 comments; article already banked above, not re-banked)
7. https://www.goodfire.com/research/reward-hacking-activation-monitors (article; its thread 49781606 was not fetched because the listing shows 0 comments, so the article is the content)
8. https://news.ycombinator.com/item?id=49727511 (Swift-Qwen3.8-27B thread, 33 pts / 17 comments)

### New banked items (second pass, strongest first; quotes verbatim from the pages fetched this session)

1. Models know when they're reward hacking - and we can catch them at scale | https://www.goodfire.com/research/reward-hacking-activation-monitors | 2026-09-21 (HN 49781606) | quote: "On Kimi K3, a probe + LLM combined setup reduces the cost of LLM monitoring by 90% with only a ~1% drop in precision." | RQ2/Q3 exact shape: a difference-of-means activation probe run as a cheap pre-filter in cascade ahead of the LLM monitor, measured on DeepSWE, the same benchmark family as the estate's 10-03 imagined-grader card: at matched false-positive rate the probe caught 3.1% more hacks than the LLM monitor on Kimi K3 and 7.9% fewer on GLM 5.2; hacking prevalence 50-96% of rollouts; probes fire before the hack executes (resampled trajectories at probe-fire points carry out the contemplated hack far more often). This is the field's measured version of cheap-local-pre-filter-then-premium-adjudication, and it prices the premium judge tier down by an order of magnitude at ~1 point precision cost.
2. Classic ML to Cope with Dumb LLM Judges (2025) | https://softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree | 2025-01-21 (submitted to HN 2026-09-17 as 49743052) | quote: "We can take lots of dumb agents, making single, basic decisions, and combine their outputs into something smarter using traditional ML." | RQ1 answer-shape: a laptop-local LLM issuing ~7,000 pairwise per-attribute judgments as features into a scikit-learn decision tree reaches 96.5-96.7% precision at ~36-41% coverage, and 1.0 precision on 1.3% with the strictest abstention branch; per-variant tables show double-check + allow-Neither lifting the uber prompt from 78.1% to 91.72% precision at 65.2% coverage. The ensemble is the FEATURES feeding classic ML, not a vote; coverage becomes the dial the estate's judge-cost question is really asking about.
3. The expensive model was cheaper: six other things I got wrong on an LLM judge | https://rekall.study/blog/expensive-model-was-cheaper/ | 2026-09-09 (HN 49626461) | quote: "A cached read costs about a tenth of the input price, so Sonnet was paying a tenth on nearly every turn while Haiku paid full freight" | Q3 judge-cost reality check: cache minimums (Haiku 4.5: 4,096 tokens vs Sonnet 5: 1,024) invert the cheap-vs-premium judge choice (~$0.094 vs ~$0.045 per voice-hour); judge-specialized Prometheus 2 LOST to a general instruct model (rubric-speak + format failures needed a second rewriting model); DeepSeek v4 Flash TTFT spread 0.47-4.01s means interactive judge loops must buy the tail, not the average. Author's own caveat: "I did not test grading accuracy properly" - the honest negative that argues for the estate's blind-protocol instrument.
4. Show HN: Open-source model routing for coding agents at Astra-level performance (HN thread) | https://news.ycombinator.com/item?id=49911500 | 2026-09-30 (119 pts / 40 comments) | quote (commenter devmor): "models hallucinating the presence of control instructions" | Q4 routing-grid re-measure evidence: Weave Router 2.0 claims Astra pass rates on Terminal Bench 4.0 and SWE Atlas at 52-54% of cost and 2.2-2.5x speed via an HMM+classifier that prunes a 10^100 routing path space; the thread's substantive pushback (trained on frontier labels, so parity is the ceiling; per-turn vs per-session path counting dispute; cache-invalidation token cost from routing) is exactly the measurement grid the estate's routing re-measure would need to run.
5. Show HN: Cactus Needle 3: 8-29MB automation models can match DeepSeek V4 Flash (HN thread) | https://news.ycombinator.com/item?id=49748553 | 2026-09-18 (236 pts / 93 comments) | quote (commenter Scaevolus): "FunctionGemma fine-tune, BF16 209/230 (90.9%)" vs "Needle 3 fine-tuned W4A8 74/230 (32.2%)" | Q1/Q2 calibration against tiny-local-model hype: the headline claim collapses to 32.2% on an independent tool-calling suite, "It copies numbers instead of converting them. '25 minute timer' becomes duration_seconds: 25" sometimes at full confidence, and the model tops out around 10 tool definitions. Confirms the estate's Model-Garden lesson on someone else's launch: per-stack blind measurement beats vendor claims on small local models, and 2-bit quantized prints are where accuracy falls first.
6. Show HN: Swift-Qwen3.8-27B, -58.3% thinking, x1.95 speed, accuracy of xhigh (HN thread) | https://news.ycombinator.com/item?id=49727511 | 2026-09-16 (33 pts / 17 comments) | quote (author kisjovan): "we got Base 66.74% vs Swift 65.84%" | Local-lane token economics: post-training that penalizes overthinking tokens cuts thinking tokens ~39-58% for under ~1 point of accuracy (GPQA-Diamond 88.4% to 88.3% at 58% fewer median tokens; Terminal-Bench 2.1 above; AIME 98.7% to 94.0% attributed to a specific training bug); thread adds the quant interaction: "lower quants suffer from low confidence in its own reasoning and tend to overthink because of that". Candidate fold for the estate's local worker lanes if thinking-token ceilings are the binding constraint, and it dovetails with the 10-03 quant-per-stack measurement card.

### Overlap receipts (second pass, greps run this session)

Commands and outputs:
- `git grep -i -l "goodfire\|activation monitor" -- catalog memory` -> only `catalog/receipt_fts.sqlite` (binary). Investigated: `./.venv/Scripts/python.exe` table listing shows FTS5 shadow tables; querying `rrows` fails with `sqlite3.DatabaseError: database disk image is malformed`. Conclusion: the hit is an opaque, unreadable FTS artifact (likely why two unrelated rare tokens both matched), not an estate holding. Side observation for the estate, not an incident claim: `catalog/receipt_fts.sqlite` appears malformed; the B2-465 daily patrol covers `catalog_fts.sqlite`, not this file.
- `git grep -i -l "softwaredoug\|judge-decision-tree\|dumb llm judges" -- catalog memory` -> 0 hits. NEW.
- `git grep -i -l "expensive model was cheaper\|rekall.study" -- catalog memory` -> 0 hits. NEW.
- `git grep -i -l "weave router\|router for coding agents" -- catalog memory` -> 0 hits. NEW.
- `git grep -i -l "cactus" -- catalog memory` -> hits only Gutenberg literary texts and shadertoy fragments (substring noise); no Cactus Needle holding. NEW.
- `git grep -i -l "swift-qwen\|ukisai" -- catalog memory` -> 0 text hits (only the same receipt_fts.sqlite artifact). NEW.
- `git grep -i -l "danluu\|exercise-7\|bad benchmarks" -- catalog memory` -> 0 hits in catalog/memory prose, but the pass above (prior incarnation, same day) already banked danluu; this pass re-confirmed it at thread level only (commenter jdw64: "the LLM-based graders themselves feel highly unstable") and did NOT re-bank it.
- `git grep -i -l "decision models like jev\|benchmarking ai decision models" -- catalog memory` -> 0 hits, but the pass above already banked the Red Hat article; this pass re-confirmed at thread level (lostmsu: "Is Jev any faster, cheaper, or more precise than medium LLMs like Luna 6?") and did NOT re-bank it.
- DeepSWE reward-hacking posts (49886206, 49851266, joinhandshake.com/research/ai/deepswe-reward-hacking): not banked. The 10-03 digest card 1 already mined the DeepSWE imagined-grader find; re-banking known work is waste.

### Cross-pass RQ summary (second pass only)

RQ1 (SLM ensemble replacing the premium judge): softwaredoug gives the measured recipe (many dumb local judgments as features + classic ML combiner + abstention dial, 96.5%+ precision at a third coverage); Goodfire gives the cascade economics (probe pre-filter cuts LLM monitor cost 90% at ~1 precision point); rekall warns the cost model itself has traps (cache minimums invert the ladder; specialized judge models lose to generalists; buy tail latency). None of the three ran blind duel protocols, which is precisely the estate's open differentiator.
RQ2 (unanimity anti-signal / consistency pre-filter): no direct unanimity-anti-signal replication found on HN this pass; nearest neighbors are Goodfire's probe/monitor disagreement (the cheap and premium channels catch DIFFERENT hacks, 3.1% vs -7.9%), reexpressionist's Jev-thread calibration point (logits as "a highly lossy compression of the epistemic (reducible) uncertainty"), and zionsati's quant-confidence note. The estate's 0.09-AUROC confident-mode-collapse ladder remains unreplicated in public HN-reachable work this pass.
RQ3 (strike rate and judge cost per fold): nothing direct. rekall's per-voice-hour judge costs and Goodfire's 90%-monitor-cost-cut are the closest pricing anchors for "what judge spend buys full adjudication of confirmed finds".
RQ4 (costed-but-unbuilt instruments ranked): HN evidence elevates the routing-grid re-measure (Weave Router thread shows the measurement shape and the 52%-cost claim worth checking on estate lanes) and the judge2 re-judge (rekall/softwaredoug both show judge choice and ensemble wiring dominate eval cost and quality); GPU ladder gates got only a weak candidate (computeassay registry, unread).
RQ5 (imagined-grader census): danluu's thread adds independent practitioner testimony that "the LLM-based graders themselves feel highly unstable", but no new rate numbers beyond the article already banked above; the census remains estate-owed.
