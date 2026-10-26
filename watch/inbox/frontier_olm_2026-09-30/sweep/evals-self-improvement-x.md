# sweep: evals-self-improvement via x

source-fetched: 2026-09-30. Banked 2026-09-30 by the sweep-evals-self-improvement-x gopher of frontier_olm_2026-09-30. Two passes per ask: Pass 1 broad sweep (34 candidates considered, section C), Pass 2 deep read (9 items fetched and read end to end: AgentChaos abs + X post, REUSE abs, When Self-Consistency Backfires abs + export-API record, SkillsBench abs, ACES abs, WebAgents long-context abs, CheckIfExist abs twice, Nautilus Compass abs; plus 3 failed fetch attempts on the walled OpenReview consensus paper). X door exercised first per recipe; non-X doors used as the documented fallback.

## A. Door status (what worked, what degraded - no fallback success faked)

- **fxtwitter door WORKS for plain posts (1 of 1 attempted):** `https://api.fxtwitter.com/ComputerPapers/status/2086746783653196285` returned full JSON: author "Software Engineering Papers (@ComputerPapers)", date August 10, 2026, tweet text naming "AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection" + https://arxiv.org/abs/2608.06790 + "Accepted at the 41st IEEE/ACM International Conference on Automated Software Engineering (ASE 2026)", plus an image whose alt text describes runtime non-intrusive fault injection at the shared HTTP layer covering "crash, omission, and value faults" on content and tool call fields.
- **site:x.com WebSearch degrades, same as the 20260928 cycle:** the Z.ai web_search_prime backend treats `site:` filters loosely (falls through to general web), X content is barely indexed, and `MCP error -429 1302 Rate limit reached` fired on roughly a third of queries (observed on the multi-agent-debate, judge-calibration, chaos, and benchmark-integrity batches); two query batches timed out at the 60s tool limit. Every X-adjacent URL below without a status id is a search-result snippet banked as such.
- **X discovery pattern that held:** @ComputerPapers (arXiv-announcement bot) is the reliable status-id source; search snippets surface its post ids, fxtwitter resolves them. Only one id surfaced for this area's questions this session; the rest of the strong material was read at arXiv directly.
- **OpenReview is walled this session:** both `https://openreview.net/forum?id=lWCLnGrHhH` and `https://openreview.net/pdf?id=lWCLnGrHhH` (and forum `VL3GsIpCF7`) returned browser-verification interstitials, not paper content.
- **Semantic Scholar API 429; OpenAlex API 429 with Retry-After 15459s** (about 4.3 hours, effectively blocked for the day). So the "When Consensus Is Not Correctness" body is OWED; it is banked from the search-result snippet only, per the recipe's fallback.
- **arXiv abs pages and the export API were LIVE today** (unlike 20260928, when export API 429'd): two export-API queries returned clean records (2608.11403, 2602.15871).
- **Estate-side reads grounding the comparison (this session):** `watch/inbox/frontier_olm_2026-09-30/lens/laws.md` (cited lines below) and `watch/inbox/frontier_olm_2026-09-30/lens/burns.md:86-89`.

## B. Estate ground truth the sweep is measured against

- Consensus-illusion result: agreement 0/3 at 0.60-0.67 strength while single-local was correct 3/3; decode maps to a surrogate-action vocabulary orthogonal to task correctness (`lens/laws.md:33`); the redesign demand ("a real redesign, not a patch") is `lens/laws.md:58`.
- Adversarial battery gap: fixed battery of real workloads (multi-hop, tool use, long context) + deliberate RIB poisoning + pod-failure injection, but n=3 workloads (`lens/laws.md:59`).
- Emergence boundary: five axes (invariant alignment gate, cost, quality, variance, generalization) with longitudinal compounding as the sharpest test (`lens/laws.md:34`); the skill_ledger holding that boundary is specified but not shown (`lens/laws.md:60`).
- De-echoed frequency instrument: every quantized-thought row is "inflated echo - provenance only"; the missing instrument measures first-seen / last-seen / distinct-source (`lens/laws.md:73`).
- Certified-decision path: `lens/burns.md:86-89` already names REUSE (arXiv 2609.33180) as the upgrade over the bare counter (`mag/percolator.py:264-272`) while the paired-blind gate sits unwired (`mag/seed_percolator.py:6-16`).
- B2-215 disease: the hand-copied "1,341 tests / 264 files" headline rode 12 days stale with 31 files grown; the census carrier tripwire (`tools/census_drift_patrol.py`, parse_carrier fail-close) is the estate's own answer for one carrier.

### Overlap checks actually run this session

- `rg -il` over `catalog/catalog.jsonl` + `memory/` for 14 candidate phrases (AgentChaos, Consensus Is Not Correctness, Self-Consistency Backfires, SkillsBench, Skill Lift, 2609.33180, CheckIfExist, Nautilus Compass, and the five arXiv ids): only `catalog/catalog.jsonl` matched, on `LongMemEval`/`longmemeval` (11 hits - the corpus holds LongMemEval rows, relevant to Nautilus Compass) and on two adjacent majority-vote titles already in the corpus: "Beyond Majority Vote: Multi-Perspective Adjudication for Medical Hallucination Detection" (arXiv 2609.03953, catalog mtime 2026-09-06) and "On the disintegration of the stochastic majority vote" (catalog mtime 2026-09-16). No banked candidate title/id is in catalog.
- The same phrases appear in `memory/trajectory/steps.jsonl` only as this session's own trajectory echo (that file is gitignored, which is why rg skipped it and a plain-grep pass surfaced it; it is not a holding).
- Prior cycle dedupe: `watch/inbox/frontier_olm_20260928/sweep/evals-self-improvement-x.md` (read in full) banked AgentX, AI4AI-Bench, DiagEvo, A/B Agent, Zvi postmortem, tianpan self-grading, ReqToCode, Latent.Space. None of today's items duplicate those; the only true estate-known item is REUSE, named at `lens/burns.md:89`, banked below with that overlap stated.

## C. Pass 1: candidates considered (34)

1. When Consensus Is Not Correctness: Diversity Collapse and Manufactured Overconfidence in Multi-Agent LLM Debate (OpenReview lWCLnGrHhH, KDD Eval Workshop 2026) - snippet only (OpenReview/SS/OpenAlex walls) - BANKED as item 4
2. When Consensus Is Not Correctness, v2 (OpenReview VL3GsIpCF7) - snippet: inter-agent correlation rises toward one as agents read one another, a single correlation governs the outcome
3. Diversity Collapse and Confidence Inflation in Multi-Agent LLM Debate (OpenReview scW4xmPtlm) - snippet: error correction vs confidence inflation race, "Calibrated Multi-Agent" methods
4. Debate or Vote: Which Yields Better Decisions in Multi-Agent Collaboration? (OpenReview iUjGNJzrF1) - snippet: debate is a martingale over beliefs, correctness does not improve with debate alone (118 citations)
5. The Cost of Consensus: Isolated Self-Correction Prevails (ACM DL 10.1145/3786335.3813137) - snippet: unguided debate produces "modal sycophancy"
6. When Self-Consistency Backfires: Majority Vote Hurts the Majority of Hard Science Problems for Small LLMs (arXiv 2608.11403, v1 2026-08-11, COLM 2026 Efficient Reasoning workshop) - DEEP READ - BANKED as item 1
7. Wisdom of the LLM Crowd: A Large Scale Benchmark (arXiv, Feb 2026) - snippet: majority voting aligns with human consensus only for clearly defined categories
8. Limits of Self-Correction in LLMs: An Information-Theoretic Analysis (preprints.org) - snippet: agreement is non-identifying when generator and evaluator err on the same inputs
9. AURA-Eval: Evaluation Framework for Acting Under Risk (arXiv, 2026-09-06) - snippet: safety evals reduce behavior to agreement-style metrics
10. SAJA: A Simple Approach to Judge Alignment for LLM-as-a-Judge (OpenReview) - snippet: 99.6% on 44% of judgments vs 78% raw judges
11. How to Correctly Report LLM-as-a-Judge Evaluations (ICML 2026 poster 63607) - snippet: CIs with calibration data
12. CalibJudge: Calibrated LLM-as-a-Judge for Multilingual Evaluation (preprints 2026-03.1324) - snippet
13. Linear Probes for Fast and Reliable Uncertainty Estimation (arXiv 2512.22245) - snippet
14. Whether LLMs Can Navigate Beliefs and Facts (arXiv, 2026-09-01) - snippet: fact-checking CoT accuracy collapses on false claims
15. Ranked Voting based Self-Consistency of LLMs (ACL 2025) - snippet; >1y old, dropped as item, kept as decode-redesign adjacent
16. Towards Reliable LLM Grading Through Self-Consistency (preprints, 2025-12) - snippet
17. AgentChaos: Chaos Engineering for Agent Systems via Programmatic Fault Injection (arXiv 2608.06790, ASE 2026; X post 2086746783653196285) - DEEP READ + fxtwitter - BANKED as item 2
18. Khaos SDK (brainbyteslab.org) - snippet: LLM API failure simulation, injection resistance
19. Chaos Engineering for AI Agents (tianpan.co) + "ReliabilityBench" - snippet, vendor overview
20. Evaluating Long-Context Reasoning in LLM-Based WebAgents (arXiv 2512.04307, NeurIPS 2025 LAW) - DEEP READ - BANKED as item 7 (date outside the 30-day window, stated)
21. BRIDGE: multi-hop reasoning over long scientific papers (arXiv 2603.07931) - snippet
22. Oolong: long-context reasoning benchmark (HF papers 2511.02817) - snippet
23. Benchmarking Collaboration of Asynchronous Multi-Agent Systems in Software Engineering (@ComputerPapers profile snippet) - snippet
24. SWE Context Bench (x.com/ComputerPapers/status/2021236736433483847) - snippet, id captured, coding-context benchmark, off-question, not resolved
25. OSS-Bench (x.com/ComputerPapers/status/1924842802174714145) - snippet, old, dropped
26. SkillsBench: Benchmarking How Well Agent Skills Work Across Diverse Tasks (arXiv 2602.12670) - DEEP READ - BANKED as item 6
27. ACES: Evaluating Skills, Not Just Agents (arXiv 2608.20614) - DEEP READ - BANKED as item 3
28. A Framework for Evaluating Agentic Skills at Scale (arXiv 2606.17819) - snippet
29. Agent Skills for LLMs: Architecture (arXiv 2602.12430) - snippet
30. Configuring Agentic AI Coding Tools: An Exploratory Study (arXiv 2602.14690) - snippet
31. Which Self-Improvements Should We Trust? Reliable Self-Improvement When Agents Reuse Their Benchmarks / REUSE (arXiv 2609.33180) - DEEP READ - BANKED as item 5 with overlap note
32. CheckIfExist: Detecting Citation Hallucinations in the Era of AI-Generated Content (arXiv 2602.15871) - DEEP READ - BANKED as item 8
33. Nautilus Compass: Black-box Persona Drift Detection for Production LLM Agents (arXiv 2605.09863) - DEEP READ, kept in section D Q4, not an item (LongMemEval surface already in catalog)
34. James (@jamescardona11_) deterministic regex knowledge-graph post - snippet, off-instrument, dropped

## D. Pass 2: deep reads, mapped to the five research questions

### Q1 - consensus/agreement as a calibrated property decoupled from correctness

**When Self-Consistency Backfires (arXiv 2608.11403, read end to end via abs page + export API).** Self-consistency via majority vote REDUCES per-problem accuracy on most GPQA Diamond problems for small instruction-tuned models: it hurts 56.6% of problems for Qwen2.5-7B and 65.7% for Llama-3-8B. The mechanism finding is the sharp one for `laws.md:33`: on 198 problems x 64 samples, a sample contradicting its problem's plurality still emits that answer with a median margin of 20.52 nats (75.7% above 10 nats); pooled across the benchmark the margin separates correct from incorrect (+0.0604, CI excluding zero) but per-problem paired it does not (-0.0168, CI crossing zero). Verdict: "a signal with across-question discrimination is nearly useless for the within-question decision a router faces." The plurality-agreement gate's failure is left as an open problem; the study is pre-registered, tested once on 69 untouched problems, and honestly reports a failed second-model replication and three unevaluable reasoning-native models. This VALIDATES the rib's measured result (agreement strength decoupled from correctness) with a much larger n and adds the exact axis of the decoupling: population-level agreement statistics do not certify instance-level correctness. Direct input to the `laws.md:58` consensus-decode redesign: any decode that consumes pooled agreement (plurality, mean logit margin) inherits the failure; per-instance verification or an output-space-mapped decode is the surviving direction, and the catalog's own 2609.03953 (multi-perspective adjudication) is an adjacent decode family.

**When Consensus Is Not Correctness (OpenReview lWCLnGrHhH, SNIPPET ONLY - walled).** The snippet names the mechanism the rib inferred from one run: debate drives agents to converge on shared answers, destroying the independence assumption that makes agreement evidence; v2 (VL3GsIpCF7) states inter-agent correlation rises toward one and "this single correlation governs the outcome"; a sibling (scW4xmPtlm) frames benign-vs-harmful debate as a race between error correction and confidence inflation and proposes Calibrated Multi-Agent methods; and Debate or Vote (iUjGNJzrF1, 118 citations) proves debate is a martingale over beliefs, so correctness does not improve with debate alone. All four independently support the rib's narrowing of the flock's role (divergent sampling + explicit check, not consensus verdicts). Body text OWED behind the verification wall.

### Q2 - scaling the adversarial battery from n=3 to a real instrument

**AgentChaos (arXiv 2608.06790, ASE 2026; X announcement resolved through fxtwitter, abs page read end to end).** This is the pod-failure-injection leg of the `laws.md:59` battery, published: runtime, non-intrusive fault injection at the shared LLM HTTP layer (no source modification), with a fault taxonomy of crash / omission / value faults on content fields and tool-call fields, plus per-fault trigger verification so untriggered tasks are filtered instead of diluting the measurement. Results: 65 fault configurations, all systems degrade, pass@1 drops by up to 50 percentage points; robustness ranking is consistent across models ("robustness depends on system implementation rather than model capability"); existing fault diagnosis achieves below 53% accuracy on fault type and below 56% on fault step. Steal-shape for the estate battery: fixed workloads + fault grid + trigger verification + diagnosis benchmark, all composable with the existing rib-poisoning injection (which passed once, `laws.md` Q10 note).

**Evaluating Long-Context Reasoning in LLM-Based WebAgents (arXiv 2512.04307, read end to end).** The long-context leg: sequentially dependent subtasks with irrelevant trajectories injected between them, contexts 25k-150k tokens, four models (Claude-3.7, GPT-4.1, Llama 4, o4-mini), success falls from 40-50% baseline to under 10%; failure modes are loops and losing the original objective; implicit RAG (task-relevant summaries) only partially rescues. Date is outside this sweep's 30-day window (2025-12-03) - banked for the instrument shape, not freshness. Multi-hop leg (BRIDGE, 2603.07931) stayed a snippet this pass.

### Q3 - does any published skill/A-B ledger learn the emergence boundary longitudinally?

**ACES (arXiv 2608.20614, read end to end).** The closest published thing to the `laws.md:60` skill_ledger: repository-native paired live trials with and without a skill, trajectories normalized to a common format (ATIF), six runtime metrics, and a per-skill number ("Skill Lift": the skill's added value for a fixed task, harness, workspace, scorer). On 145 real skills and 947 scored paired cases across 4 harnesses: mean composite Skill Lift 0.2134 (95% CI [0.1967, 0.2301]), positive in 72.8% of paired cases; and the number that justifies the whole design: scan-only structural gates vs LLM-judge correlate at Spearman rho = 0.14, i.e. reviewing skill packages by prose is nearly uncorrelated with their measured live value. That is evidence-earned promotion for skills, exactly the certified-decision shape. What ACES does NOT do: no longitudinal axis - it measures per-skill lift in paired cases, not the compounding signal of an emergent arm improving across repeated task-classes while deterministic stays flat (`laws.md:34`'s sharpest test). The paired-case ledger is the substrate that axis would accumulate on; the rib's five-axis ledger remains unserved in the published corpus.

**SkillsBench (arXiv 2602.12670, read end to end).** The measurement standard for the skill side: 87 tasks, 8 domains, 18 model-harness configurations, deterministic verifiers, curated skills lift average pass rate 33.9% -> 50.5% (+16.6pp), configuration-level gains range +4.1 to +25.7pp, and focused skills (at most three modules) beat exhaustive bundles - a direct calibration for the estate's skill-card granularity.

### Q4 - gates that replace bare-counter promotion; the B2-215 eval

**REUSE (arXiv 2609.33180, v1 2026-09-27, read end to end).** OVERLAP: already named at `lens/burns.md:89` as the upgrade path; this pass verified the paper exists and banked its actual mechanism and numbers. When agents reuse a fixed benchmark to decide which self-modifications to keep, "the search trajectory can adaptively overfit and empirical improvement may not reflect genuine population improvement"; existing multiple-comparison corrections fail because candidates are adaptive to the eval set. REUSE's gate guarantees, at user-set error alpha, that every promoted modification is a genuine population improvement, by strictly limiting what feedback returns to the search and budgeting for all possible promotion histories. Measured effect: false promotions drop from up to 20.7% to 0% while matching baseline performance. This is the published certified-decision gate for exactly the promote step the estate's bare counter (`mag/percolator.py:264-272`) performs.

**Nautilus Compass (arXiv 2605.09863, read end to end, not an item).** The B2-215-shaped instrument: black-box drift detection for production LLM agents via cosine similarity between live behavior and behavioral anchors (weighted top-k mean over BGE-m3 embeddings), mapped to a three-band gating output, ROC AUC 0.83, with a Merkle-chained audit log and $3.50 reproduction cost. Honest weaknesses, stated by the paper itself: 56.6% on LongMemEval-S (about 30 points under white-box leaders, attributed to the no-extraction design) and 44.4% on EverMemBench-Dynamic. The transferable shape for the census disease: anchors + similarity score + banded gate + hash-chained log, i.e. what `tools/census_drift_patrol.py` already does for one carrier, generalized to any carried claim. The direct B2-215 question ("what eval would have caught the 1,341 headline") is answered by the estate's own existing machine plus this paper's banding: a claim whose instrument (census date, counts) is stale relative to tree state fails closed - which is what the patrol now enforces.

### Q5 - the de-echoed frequency instrument (first-seen / last-seen / distinct-source)

**CheckIfExist (arXiv 2602.15871, read end to end twice).** The published distinct-source-count instrument, one domain over: open-source verification of bibliographic references by cascading multi-source validation against CrossRef, Semantic Scholar, and OpenAlex with string-similarity confidence scores, batch BibTeX support. The design maps 1:1 onto a law-currency instrument: a compiled law's weight = distinct independent sources confirming it (estate analog: rib + two independent session transcripts + external corroboration), with cascade order and match confidence instead of raw echo counts. NOT FOUND anywhere in this pass: a published instrument that tracks first-seen / last-seen / distinct-source for compiled doctrine or law claims specifically. The estate's invariants.json already carries count/first_seen/last_seen per the prior cycle's ground truth (C-section of the 20260928 file); the distinct-source dimension is the missing axis and remains novel territory - no published prior art surfaced, which raises rather than lowers confidence that building it is worth the spend.

## E. Banked items (8, strongest first; also the submit_result payload)

1. When Self-Consistency Backfires (arXiv 2608.11403) - Q1 validation at scale
2. AgentChaos (arXiv 2608.06790) - Q2 fault-injection battery leg; X door resolved
3. ACES (arXiv 2608.20614) - Q3 paired skill A/B ledger, evidence-earned lift
4. When Consensus Is Not Correctness (OpenReview lWCLnGrHhH) - Q1 mechanism naming; SNIPPET-ONLY (walls), degraded door stated
5. REUSE (arXiv 2609.33180) - Q4 certified promotion gate; overlap: estate already names it at burns.md:89; numbers + mechanism banked new
6. SkillsBench (arXiv 2602.12670) - Q3 skill measurement standard
7. Evaluating Long-Context Reasoning in LLM-Based WebAgents (arXiv 2512.04307) - Q2 long-context leg; date outside window, stated
8. CheckIfExist (arXiv 2602.15871) - Q5 distinct-source instrument analog

## F. OWED / not run

- "When Consensus Is Not Correctness" full body: OpenReview forum + pdf, Semantic Scholar API, and OpenAlex API all walled or 429 on 2026-09-30 (SS 429; OpenAlex 429 Retry-After 15459s). Banked from the search-result snippet only, per the recipe. OWED via a logged-in door or a later non-throttled window.
- Debate or Vote (iUjGNJzrF1), the scW4xmPtlm and VL3GsIpCF7 variants, Wisdom of the LLM Crowd, SAJA, AURA-Eval, the ICML judge-reporting poster, BRIDGE, Khaos SDK, tianpan chaos overview, async multi-agent collaboration benchmark: snippet only, not deep-read, not banked as items.
- fxtwitter resolution count: 1 of 1 attempted. No status ids surfaced by search for the SkillsBench/ACES announcements; their arXiv pages were read directly instead.
- No estate code was modified and no tests were run (research sweep). Executed checks this session, quoted above: the fxtwitter fetch, arXiv abs/export fetches, the 14-phrase rg overlap pass over catalog + memory, the gitignore-aware re-grep of memory/trajectory/steps.jsonl, and the catalog majority-vote row extraction.
