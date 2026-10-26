# Frontier sweep: evals-and-self-improvement (X door)

source-fetched: 2026-10-08. Actor: sweep-evals-and-self-improvement-x. Door: WebSearch `site:x.com` queries, single posts resolved through `https://api.fxtwitter.com/<user>/status/<id>`, arxiv /abs pages fetched directly for quote fidelity.

## Door state (honest)

- WebSearch worked but was heavily rate-limited: several sub-queries died with MCP 429/1302, three parallel calls hit 60s timeouts, and I had to drop to sequential single searches. No 403s anywhere.
- fxtwitter door resolved every post I tried (5/5), including X long-form articles.
- Search engines index X thinly (noted by the search tool itself on three queries). The strict last-30-days X-only pool is thin; the strongest on-axis material concentrates in weekly digest accounts (dair_ai). Of the 8 banked items only 2 sit inside the strict 30-day window (SIFT 09-17, dair_ai digest 09-27); the rest are Jul-Aug and dated honestly below.

## Pass 1 - candidate pool (32+ considered)

rohanpaul RACE post (Jun 2025, stale); dair_ai digests 07-19, 08-30, 09-27; dair_ai articles 2086499440597102848 (Model-or-Harness week), 2081437966866505856 (Harness Handbook), 2073814128888549810 (Red Queen / Verification Horizon); dair_ai 2058537927823556668 (Code as Agent Harness); TheValueist threads 2092227309835108800 and 2077732635741450375; xy9301 2036017855381340269 (AI auditing II); MemOS_dev 2020854044583924111; Kangwook_Lee 1993438649963164121 (judge eval); poteto 2069824386283319343; polydao article 2083061585858158636; Av1dlive article 2064292484856041558; alphabatcher article 2095503115130646825; businessbarista 2085383591475773666; PawelHuryn 2056109927727292629; kmeanskaran article 2090436724250026177; diamai_ article 2092671754363916291; TheZvi 1868678517132509613 (stale); stateof_ai 1843635071607050709 (stale); techNmak and Harry_The_Nerd articles (weak); profiles: lupantech, wellecks (AlphaVerus), EnterMirari, sameeurehman, akshay_pachaar, dyfan22 (HalluHard). Plus the 30 papers carried inside the three dair_ai digests.

## Pass 2 - deep reads (11 items read end to end)

fxtwitter: dair_ai 2078883557573849583, dair_ai 2094085853026951319, dair_ai 2104263416252625124, TheValueist 2092227309835108800, poteto 2069824386283319343. arxiv /abs: 2609.19526, 2609.26550, 2609.23939, 2608.18300, 2608.22752, 2608.20614, 2607.09197, 2607.09510.

## Dedup decisions (already held - NOT re-banked)

- XYEval (2609.23939): held at `state/arxiv/2026-09-22/2609.23939v1.txt` (catalog row 444908). Dropped despite being a direct Q2 mutation-pattern match.
- The Compaction Cliff (2608.22752): swept by the 2026-10-05 sibling, `watch/inbox/frontier_olm_2026-10-05/sweep/_raw/passau_compaction.txt` (catalog row 1073445). Dropped.
- JEV-as-a-Judge (2609.26550): v1 abstract held at `state/arxiv/2026-09-23/2609.26550v1.txt` (catalog row 445289); also `corpus/library/jev_steal_library/` (catalog rows 27772-27774, persona harness + fleet bibliography, mtime 09-19). Not re-banked, but a REFRESH is owed: my fetch of the current page reads v4 (revised 2026-10-06) whose abstract adds material the held v1 stub lacks: the frozen cascade is "0.9 points more accurate than GPT-6" on 1,610 held-out pairs at 41% of its cost, a pre-specified live test matched GPT-6 exactly, 0.15s median latency, confidence routing weakens on style-adversarial pairs and reference-free prose, and a recipe for locally validating escalation thresholds. That last piece is the judge2 (Q7) threshold-validation method; the estate holds the claim but not the recipe.
- Overlap instrument note: full recursive grep of memory/ was killed after crawling agent_sessions (gigabyte session blobs, substring noise); curated dirs (rib, law, lenses, improve, frontier, zknot, briefs, press, workflows) were grepped clean: zero hits for every banked candidate.

## Banked items (strongest first)

### 1. When is Routing Meaningful? Diversity and Robustness in Language Model Societies
arxiv.org/abs/2607.09197 · Huot/Kaisers/Lapata · 2026-07-10 · fetched 2026-10-08.
Routing judged only on accuracy+cost ignores behavioral differentiation (without it "routing is vacuous") and stability under surface-form query variants. HSE shows diminishing returns: "a curated subset of fewer than ten agents recovers most available diversity in a large pool". KNN routers gain accuracy on specialist pools but lose robustness under perturbation; prompted routing stays stable.
Bearing: Q1's hidden precondition. Before manufacturing n>=40 fleet-labeled rows, measure whether the fleet behaviorally differentiates at all: if HSE-style differentiation is absent, the decision meter is routing on noise and no row count fixes it. Their perturbation-robustness metric over surface-form variants is the public twin of our duty_fuzz twin-minting (delta >= 0.15) law, applied to router stability instead of contamination. Also bounds the fleet question: fewer than ten behaviorally-distinct actors may recover most of the pool's diversity.
Overlap: catalog greps "When is Routing Meaningful"/"2607.09197"/"Hierarchic Social Entropy" = 0; curated memory = 0; today's sibling `_txt_routing.txt` is a different artifact (Reddit per-prompt routing discussion, grep 0).

### 2. Self Improvement via Fast Tree-search (SIFT)
arxiv.org/abs/2609.19526 · Fu/Kulanthaivelu/Yamada · 2026-09-17 · fetched 2026-10-08.
"We introduce a simple, sample-efficient self-improvement framework that significantly improves coding performance under strict budget constraints." Candidate self-modifications are screened by LLM-as-a-judge pairwise comparisons, win-loss records aggregated with a regularized Bradley-Terry model, rank-based parent sampling drives a lightweight tree search; costly downstream benchmark evaluations run only on the most promising nodes.
Bearing: Q1 economics. The n>=40 row manufacture and every decision-rung re-run is an evaluation-budget problem; SIFT's shape (cheap pairwise judge pre-screen, then BT ranking, then spend real battery runs only on survivors) is the steal for manufacturing rows without paying full battery cost per candidate. Also the probe-vs-judge hierarchy our day-7 mine already banked (97-99% probe recall vs judge 9) but with the aggregation step we lack.
Overlap: catalog "fast tree-search"/"2609.19526" = 0; curated memory = 0.

### 3. Evaluating Skills, Not Just Agents (ACES / Skill Lift)
arxiv.org/abs/2608.20614 · Kevin et al., NVIDIA · 2026-08-20 · fetched 2026-10-08.
Enterprise review gates check structure/style/security, not whether a package "helps a live agent complete enterprise tasks under the same model, sandbox, and grading policy". ACES runs paired live trials with/without a skill, normalizes trajectories (ATIF), grades six runtime metrics; 145 real skills, 947 scored paired cases, mean composite Skill Lift 0.2134 (95% CI [0.1967, 0.2301]), positive in 72.8% of cases. The dair_ai digest carrier adds that scanner-based review gates correlate weakly (rho 0.14) with quality.
Bearing: Q5 + Q1. The paired with/without run under pinned model+sandbox+grader is exactly the public cousin of our quant A/B four-pinned-choices law, with a confidence interval and case count we can copy for the decision-rung bar. And rho 0.14 is ammunition for the WARN-to-invariant promotion question: a gate finding that recurs without curing is worth promoting only if it correlates with outcomes, and static-scan gates measurably do not.
Overlap: catalog "Skill Lift"/"2608.20614" = 0; curated memory = 0.

### 4. The Lifecycle of LLM-as-a-Judge for Large-Scale Recommendation Explanations
arxiv.org/abs/2608.18300 · Kong et al., Netflix · 2026-08-18 (v3 08-31) · fetched 2026-10-08.
Judges in deployed systems need a lifecycle, not a snapshot: birth (criteria + curated human-labeled benchmarks), training (Reasoning-Aligned Rubric Tuning via a meta-judge over reasoning), deployment (quality gating + reflective generation), monitoring via continuous HITL alignment that "detects drift and triggers re-tuning behind a human review gate". Five-week A/B over tens of millions of members, no quality-related takedowns.
Bearing: Q3/Q7. This is the cure shape for the ember-1-only-judge standing incident: a judge2 is not a one-shot re-judge but a maintained second channel with drift monitoring and a human-gated re-tuning trigger. The Birth phase (curated human-labeled benchmark per criterion) is also the ask-bank growth pattern for Q8.
Overlap: catalog "Judges as a Lifecycle"/"LLM-as-a-Judge for Large-Scale"/"2608.18300" = 0; curated memory = 0.

### 5. Failure as a Process: An Anatomy of CLI Coding Agent Trajectories
arxiv.org/abs/2607.09510 · Zhao et al. · 2026-07-10 · fetched 2026-10-08.
3,843 trajectories (7 frontier models, 3 scaffolds, Terminal-Bench), 1,794 valid ones annotated across 63,000+ steps, 14 findings: failures "are predominantly driven by epistemic errors, typically begin within the first few execution steps" and stay hidden "until recovery is no longer possible".
Bearing: Q5. The colon-reveal (25/28) and lyrics-verbatim repeat offenders are early-onset epistemic failures of exactly this class: onset in the first steps, invisible at end-state patrol. The paper's implication (earlier validation, not final-outcome evaluation) is the fix-the-cause argument for promoting recurring WARN findings into percolator invariants that fire at generation time.
Overlap: catalog "Failure as a Process"/"2607.09510" = 0; curated memory = 0.

### 6. Loops You Can Trust (lauren / @poteto, X article)
x.com/poteto/status/2069824386283319343 · 2026-06-24 · fetched 2026-10-08 via fxtwitter door.
"One key aspect of building trustworthy loops is that every stage can stop the line." Cursor's Benny pipeline chains triage/repro/fix automations, each producing artifacts; "show me your work" beats plausible explanations; pstack's /show-me-your-work "keeps an append only decision log" reviewed by a different model family; recurring failures are turned into skills; autonomy granted only once earned.
Bearing: Q5 + Q3. Two steals: (a) every loop stage gets stop-the-line authority, which is exactly what our WARN patrol findings lack and what the promotion question asks; (b) the decision log is reviewed by a DIFFERENT MODEL FAMILY, a hand-rolled judge2 precedent from production that converges with Q7's second-family re-judge.
Overlap: catalog "Loops You Can Trust"/"poteto" = 0; curated memory = 0.

### 7. Top AI Papers of the Week, Sep 21-27 (@dair_ai)
x.com/dair_ai/status/2104263416252625124 · 2026-09-27 (in-window) · fetched 2026-10-08 via fxtwitter door.
Ten-paper index; quote from its GAVEL entry: "more than doubles the success rate of a small model without changing its weights". Un-held pointers beyond items 1-2 above: EvoOntology (2609.15779, self-evolving ontology layer served over MCP replacing hand-written semantics, direct material for the law-census duplicate-label disease at lens/graph.md:25); Harness-Zero (2609.24974, distilling specialized-harness gains into model weights); Self-Organizing Agent Teams (2609.22682); WFM (2609.18182, wiki foundation model as long-term agent memory); ScientistTwo (2609.19644).
Bearing: carrier artifact, one in-window X post holding eight un-held on-axis pointers. Two of its ten (XYEval, JEV-as-a-Judge) were already in the estate; that overlap is recorded rather than re-banked.
Overlap: catalog rows 444908 (XYEval) + 445289 (JEV) hold 2/10 of its papers; the digest post itself: 0.

### 8. Thomson 1.0 technical-report teardown (@TheValueist thread)
x.com/TheValueist/status/2092227309835108800 · 2026-08-25 · fetched 2026-10-08 via fxtwitter door.
Thread on the Thomson Reuters Thomson 1.0 model; quotes Schwarz: "And our tech report shows how others can do it for even less spend". Documents the released-model risk set including incomplete decontamination, and (per the search-result snippet for the same post) evaluation decontamination via 13-gram matching against benchmark targets before selection; benchmark values differing across announcement vs model card vs HuggingFace materials.
Bearing: Q2. The 13-gram pre-selection decontamination control is a cheap deterministic twin of duty_fuzz for the ask-bank: n-gram screen first, embedding-delta second. The benchmark-value divergence across sources is our citation-lint PHANTOM-NUMBER disease in the wild, same cure class.
Overlap: catalog "Thomson" = 0; curated memory = 0. Caveat: the 13-gram sentence is from the search snippet of this post, not the fetched body; the fetched body carries the incomplete-decontamination risk flag.

## What the sweep says about the five questions

- Q1 (rows + 0.880 bar): the public evidence says measure routing meaningfulness BEFORE manufacturing rows (item 1), manufacture them with judge pre-screen + BT aggregation (item 2), and score with paired pinned runs + CIs (item 3). No public number challenges the 0.871 semantic-entropy ceiling directly.
- Q2 (ask-bank 20 to 100+): XYEval's benchmark-mutation pattern is the held answer (already banked 09-22, the estate should USE it, not re-find it); 13-gram screening (item 8) is the cheap dedup layer.
- Q3/Q7 (judge2): Netflix lifecycle (item 4) + poteto's cross-family review (item 6) + the held JEV v4 threshold recipe (refresh owed) together give the second-family re-judge design.
- Q9 (law census): EvoOntology pointer (item 7) for the duplicate-label disease; nothing measured on collision rate in this sweep.
- Q5 (recurring gates): rho 0.14 (item 3) + early-onset epistemic failure (item 5) argue for outcome-correlated, generation-time invariants over recurring static WARNs.

OWED: diff JEV v1 vs v4 to confirm the escalation-beats-frontier numbers are v4 additions; fetch EvoOntology and Harness-Zero abstracts before promotion; the strict-30-day X pool stays thin, so a re-sweep when the search backend is not rate-limited may find October-native posts.
