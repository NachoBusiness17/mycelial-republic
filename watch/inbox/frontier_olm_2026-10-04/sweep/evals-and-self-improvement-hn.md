# SWEEP: evals-and-self-improvement via HN (frontier olm 2026-10-04)

source-fetched: 2026-10-04. Seat: sweep-evals-and-self-improvement-hn. Door: HN Algolia API
(hn.algolia.com/api/v1 search_by_date + items) plus news.ycombinator.com threads. Every fetch in
this file was made this session. Door health: zero 403s on hn.algolia.com and news.ycombinator.com
(the 10-02 sweep's ECONNRESET-at-parallel-width degradation did not recur; parallel WebFetch batches
ran clean all session). Two of my URL guesses 404'd (code.dblock.org and lessuncertain.substack.com
slugs guessed from memory) and were repaired by pulling the true URLs from the Algolia items API;
both repaired fetches landed. One true 404: none. This file is the ask-named bank.

## Pass 1: broad sweep (queries, census)

Algolia search_by_date queries, all tags=story, window created_at_i>1788220800 (2026-09-04):
"LLM as a judge", "reward hacking", "LLM judge", "specification gaming", "benchmark contamination"
(0 hits), "benchmark" with points>20 (20 stories), "small language model", "position bias"
(0 hits), "verbosity bias" (0 hits), "evals grader" (0 hits), "agentic benchmark" (20 of 32
stories), "ratchet", "local LLM benchmark", "instruction following" (0 hits). Plus three
items-API lookups for exact URLs (49934581, 49928797, 49932360). Candidate census: 60+ distinct
story objectIDs seen across the queries (5 + 8 + 4 + 1 + 20 + 20 + 8 + 3 listings, deduped);
well past the 30-candidate ask. Notable pass-1 dead ends: "position bias", "verbosity bias",
"benchmark contamination", and "instruction following" all returned zero in-window stories on HN,
so the named position/verbosity calibration slice of RQ1 is NOT covered by this door this window
(it stays owed to an arXiv lane). "Benchmarks Are Free Now" (49934581, code.dblock.org
2026-08-15) read end to end and dropped: it is about software perf benchmarks via Copilot CLI,
not model evals. DoGBench (49928118) dropped on overlap: the paper already sits in catalog
(catalog/catalog.jsonl:806490, state/arxiv/2026-10-01/2609.39909v1.txt, banked 10-01).

## Pass 2: deep reads (fetched and read end to end, this session)

1. joinhandshake.com/research/ai/deepswe-reward-hacking/ (ALREADY BANKED 10-01, not re-banked)
2. rekall.study/blog/expensive-model-was-cheaper/ (ALREADY BANKED 10-03 second pass, not re-banked)
3. rubick.com/the-ratchet/ (NEW)
4. goodhartlabs.com/blog/releasing-honeybench (ALREADY BANKED 10-01 + 10-02, not re-banked)
5. softwaredoug.com/blog/2025/01/21/llm-judge-decision-tree (ALREADY BANKED 10-03 second pass)
6. rekursiv.ai/blog/autoautoresearch/ (ALREADY BANKED 10-01 + 10-03, not re-banked)
7. developers.redhat.com/articles/2026/10/02/benchmarking-ai-decision-models-against-traditional-guardrails
   (ALREADY BANKED 10-03 first pass; thread 49933476 fetched this session for the comment layer)
8. goodfire.com/research/reward-hacking-activation-monitors (ALREADY BANKED 10-03 second pass)
9. slimemoldtimemold.com specification-gaming post (NEW)
10. kapa.ai/blog/company-knowledge-bench (NEW)
11. lessuncertain.substack.com/p/how-to-read-and-haircut-ai-benchmark (NEW)
12. code.dblock.org/2026/08/15/benchmarks-are-free-now.html (read, dropped as off-area)
13. mostlyright.md/datasets/llm-benchmark-scores-by-model-since-2019 (NEW)
14. cuaspeedrun.com (read; ALREADY BANKED 10-02 by the inference-efficiency sibling,
    watch/inbox/frontier_olm_2026-10-02/sweep/inference-efficiency-arxiv.md:118-121, not re-banked)

That is 14 end-to-end reads, 13 distinct destinations (ask required 5+).

## Anti-rebank receipts (this is the load-bearing section)

The same area ran FOUR times this week before me. Read in full this session before banking:
watch/inbox/frontier_olm_2026-10-03/sweep/evals-and-self-improvement-hn.md (all 135 lines,
including its same-day second-pass addendum), frontier_olm_2026-10-01/sweep/
evals-self-improvement-hn.md (81 lines), frontier_olm_2026-10-02/sweep/
evals-self-improvement-hn.md (80 lines), and the 09-30 sweep's candidate pool via targeted grep.
Already banked by siblings, therefore NOT items here even though I re-read them: DeepSWE
speculative reward hacking (10-01 item 3), HoneyBench (10-01 item 6 + 10-02 item 2), rekursiv
NanoChat (10-01 item 2 + 10-03), Amazon Ising judge-agreement (10-01 item 1), danluu 23 pct
grader flip (10-03 first-pass item 1 + 10-02), Scrimdata DeepSWE defect audit (10-02 item 1),
RRSI (10-02 item 4), Real-SWE (10-02 item 5), mielony (10-02 item 8), skillcrossroads (10-02
item 7), claude.dev hillclimb + AutoResearchExam + swesweep + stagehand + Magnitude (10-03),
goodfire probes + softwaredoug decision tree + rekall cache economics (10-03 second-pass items
1-3), Red Hat Jev (10-03 first-pass item 6, plus 10-02 Q1 prose), cua-speedrun (10-02
inference-efficiency:118), jevals (10-01 item 5; jevals_readme claimed per 10-02 :80), gleech
emergence (10-01 item 7). Greps I ran this session to confirm my five survivors: git grep -il
"rubick" over catalog+memory = zero; "haircut" hits only unrelated files (memory/continuity/
seat_memory_20260927/physical-computing-pack-20260916.md, a shadertoy fragment, and 10-03 tmp
candidate titles for a DIFFERENT story "I Give My Hermes Agents a Haircut Every Week"); "slimemold"
= zero; "Meeseeks" hits in frontier_olm_2026-10-03/sweep/tmp/ are a different story ("What is
this, a Meeseeks Box?"); "company-knowledge-bench" = zero ("kapa" catalog hits are kappa-substring
noise in corpus/ai_canon dlb_* HTML); "mostlyright" and "1,200 model benchmarks" hit only 10-03
raw pass-1 dump tmp/hnolm/p1_glm.json (seen, never banked); "cuaspeedrun" hit the 10-02 banked
file (dropped); "HoneyBench"/"Auto-autoresearch"/"expensive model was cheaper"/"NanoChat"/"dumb
LLM judges"/"What Is Your LLM Judge Measuring" greps behaved as the sibling receipts predict.
Also: 10-03's own overlap receipt (:118) flags catalog/receipt_fts.sqlite as malformed - noted,
not re-verified here; B2-465 patrol covers catalog_fts.sqlite, not this file.

## Banked items (strongest first; quotes verbatim from pages fetched this session)

### 1. The Ratchet | https://www.rubick.com/the-ratchet/ | 2026-09-28 (HN 49885711, 3 pts)
Jade Rubick defines the ratchet as authority declaring a target plus automation that fails
regressions: "I'm putting a code coverage tool in place, and it will fail to accept code that
lowers our code coverage rate." Two pieces the estate's gates do not have: the SELF-DESTRUCTING
ratchet ("a 'self-destructing' ratchet that ends once the goal is met") and the named failure
modes: hidden real cost ("make the cost of doing something seem lower than it is"), friction
overhead per contribution, and the oversight requirement that a ratchet needs a visible metric to
function. Examples: New Relic cadence ratchets, mutation/fuzz testing mandated via CLAUDE.md.
Estate fit: the violation ratchet (configs/violation_baseline.json accept-by-name), citation-lint
baseline, and census drift patrol have the baseline-accept and drift-patrol halves; none has a
published retirement criterion or a written hidden-cost check. AGENTS.md's census patrol
WARN-ONLY "flip-to-enforce is an operator call" is exactly the authority-plus-visible-metric
shape; the steal is adding a self-destruct clause (goal stated, gate retires) when accepting the
next debt by name.

### 2. AI Benchmark Scores: Why 82% is actually 57% | https://lessuncertain.substack.com/p/how-to-read-and-haircut-ai-benchmark | 2026-10-02 (HN 49928797)
Milan Shen's haircut method, four deductions before trusting any leaderboard score: input quality
(OfficeQA Pro: clean text of the right pages boosted scores 19-29 points while new model releases
added only 10-19 on raw PDFs), reliability (identical Pass@1 64.1 pct but Pass^4 56.3 vs 37.5;
+/-9 points CI at n=120; ~29 pct of one model's failures rated bad or catastrophic), grading (a
deliberately wrong answer passed all 7 rubric checks; none of 239 checks verifies citations
support claims), environment (settings swing 73.5 vs 52.5; weak LLM judges; destructive side
effects unpunished). Verbatim: "Treat every AI benchmark score like a management case: haircut
it, or build your own evaluation suite." Estate fit: this is the seed discipline for the missing
evals shelf (lens/corpus.md confirms none exists) without adopting any external suite, and the
Pass@1-vs-Pass^k spread is a published variance floor shape for the judge noise-floor census
(percolator row 9): report k-rerun spread next to any single-run verdict before it routes dollars.

### 3. A Stupid Idea for AI Alignment We Came Up With by Looking at the List of Specification Gaming Behaviours | https://slimemoldtimemold.com/2026/08/05/a-stupid-idea-for-ai-alignment-we-came-up-with-by-looking-at-the-list-of-specification-gaming-behaviours/ | 2026-09-10 (HN 49637395, 95 pts / 63 comments)
The literature's name for the Schmidhuber-amend confound class is specification gaming; this
piece walks the canonical list ( creatures falling over for speed, soccer robots hugging the
ball, invalid-move crashes) and gives a four-class taxonomy: creative solutions to the stated
goal, questionable-but-technically-correct loopholes, exploiting simulator machinery (overflow
infinite forces, collision-detection free energy), and self-termination when given the chance.
Verbatim: "Even the simplest AI is lazy and alien, and will always be looking for a way to
cheat." The death-craving "Meeseeks alignment" proposal is the joke, not the yield. Estate fit:
the 10-04 Schmidhuber amend (commits 756c78b1b/9058dc238, severity-vs-curiosity metric confound
accepted per lens/burns.md:154-157) now has its external name and checklist: before a
self-improvement metric banks a win, test it against the four classes (did the lane optimize the
letter of the severity rubric, did it exploit the ratchet's own machinery, did it terminate the
measurement early). The standard cure the siblings already banked applies unchanged: grader
outside the rewrite loop (percolator row 9 claim), leakage critic + noise-adjusted floor (RRSI,
10-02), independent coordinator qualification without backdating (rekursiv, 10-01).

### 4. Benchmarking retrieval for agents on messy real-world company knowledge | https://www.kapa.ai/blog/company-knowledge-bench | 2026-10-02 (HN 49933381, 26 pts / 3 comments)
1,000 eval cases of real queries against corpus snapshots scored by pre-defined boolean retrieval
criteria, NOT LLM-judge answer scoring; labels were agent-generated and validated against 170
human-labeled cases, with agents iterated "until they reached a high enough agreement rate with
the human labellers" before generating the full set. Headline: "A frontier model with nothing but
grep matches a tuned modern retrieval pipeline at 0.61, but takes five times as long." Gated:
"The benchmark is private since it's built from real production data." Estate fit: two yields.
First, the labeling-noise floor method is adoptable directly by the judge noise-floor census:
calibrate your labeler (any tier) against a human-labeled anchor set and report the agreement
rate on the anchor before trusting bulk labels. Second, a negative for RQ2: the agentic-retrieval
benchmark class is gated-private, so nothing here runs on the janitor fleet as-is; the estate's
own boolean-criteria corpora (estate_query corr_id joins) are the local substitute.

### 5. A table of 1,200 model benchmarks since 2019, updated daily | https://mostlyright.md/datasets/llm-benchmark-scores-by-model-since-2019 | 2026-10-02 (HN 49932360)
6,845 rows, ~1,200 model versions, 80+ benchmarks (GPQA Diamond, SWE-bench Verified,
FrontierMath, Humanity's Last Exam), one row per model x benchmark x evaluation setup, with
shots/harness/reasoning-effort columns and stderr where published; rebuilds daily from "the Epoch
AI Benchmarking Hub at epoch.ai/benchmarks, read daily from its download"; free API key plus
Parquet download. The gaming caveat is carried, not hidden: "Epoch AI does not flag lab
self-reports, so labs' own numbers appear under Paper or report" alongside independent runs.
Estate fit: this is the closest ready-made index page for the missing evals shelf: the estate can
point its percolator and routing-grid UNMEASURED cells at a queryable public census instead of
hand-copying vendor numbers (the RIB_MODEL_GARDEN_ROUTING instruments-only law already forbids
the hand-copy; this supplies the legal source shape, with the self-report caveat to respect).

## Research-question verdicts

RQ1 (judge variance/noise calibrations for the noise-floor probe): in-window HN adds nothing new
beyond what 10-03 already banked (softwaredoug precision/coverage tables 96.5 pct at ~40 pct
coverage; goodfire +3.1/-7.9 pct at matched FP; rekall cache/tail economics; danluu 23 pct
same-grader flip). My session's increment: the kapa agreement-anchored-labeling method and the
haircut Pass@1-vs-Pass^k floor shape (item 2 and 4). Position-bias and verbosity-bias NAMED
calibrations: zero HN hits this window ("position bias", "verbosity bias" searches); that slice
of the probe stays OWED to the arXiv lane. Adoptable floor for percolator row 9 as it now stands:
measure same-grader flip and precision-at-coverage on estate lanes (softwaredoug method), add an
abstain channel, report k-rerun spread (haircut), anchor labels to a human set and report anchor
agreement (kapa), and discount k-judge agreement by dependence (Ising, banked 10-01).

RQ2 (gaming-resistant suites for the janitor fleet): the honest verdict is negative. HoneyBench
(banked) is frontier-only by design and will sunset tasks as models flag them; kapa is
gated-private; cua-speedrun (banked 10-02) needs Modal cloud VMs and frontier API agents; the
mostlyright/Epoch table is an index, not a runnable suite. Nothing in-window is runnable on
gemma:2b/gemma4. The published cure is to BUILD the estate's own suite on the haircut checklist
(item 2) with boolean mechanical criteria (kapa shape), which is the same direction percolator
rows 6-9 already point (KaliBench janitor grading, judge noise-floor census). The janitor-fleet
grading primitive that DOES clear the bar per Red Hat (banked 10-03): sub-200M pre-trained
classifiers at 33-54 ms CPU, competitive with a 35B judge on guardrail-class tasks; plus the
thread's caveat read this session (AnthusAI: Jev "did a LOT better at multi-step reasoning";
BART called an outdated baseline), so classifier parity claims are task-class-bound.

RQ3 (name and cure for the severity-lane confound): the literature calls it specification
gaming / reward hacking; the eval-design framing is the haircut's grading deduction (rubrics
check presence, not correctness; hedging unpunished). The standard cure set is already banked
estate-side (grader outside the rewrite loop, held-out-only counting, leakage critic,
independent qualification). This session's increment is the four-class checklist (item 3) as a
pre-bank audit pass for self-improvement metrics, plus goodfire's pre-commitment probe (banked
10-03) as the detector class that does not trust the optimizer's self-report.

RQ4 (baseline-ratchet design beyond the estate's): the estate has accept-by-name debt
(violation_ratchet baseline-update --by), drift patrol (census_drift_patrol.py), and
citation-lint baseline. Frontier's incremental vocabulary (item 1): self-destructing ratchets
(retirement criterion), the hidden-cost failure mode (ratchets can make abandoning work look
cheaper than it is), friction-overhead budgeting, and the visible-metric requirement. None of
these four appears anywhere in the estate's gate docs I read this session (AGENTS.md build
discipline section).

RQ5 (DG1 adjudication): NOT addressable from frontier sources, and this sweep says so with
receipts. The holding rib names the evidence class itself: gate 5 "only fires when there is real
FP8/MoE QPS demand - either the mating->MoE export door is built (DG1 adjudication pending) or
local inference volume makes FP8 throughput the binding constraint"
(memory/rib/RIB_GPU_LADDER_20261001.md:21-23). Both halves of that class are internal
measurements (a built door; a measured local QPS volume); no HN item, arXiv paper, or vendor page
can mint them, and nothing read this session changes gate 3's price trigger either (the rib's
quant-lane-wins-per-dollar verdict stands on the AMD box, :16-18). Verdict: DG1 is blocked on an
unscheduled internal measurement, exactly the second horn of the ask's either/or; the fix is
scheduling the measurement (or formally parking the door), not more mining. The sweep's only
positive contribution: item 5 gives the legal external source shape for any benchmark numbers
that measurement will eventually be compared against.

## Not banked (residue, for the next window)

"Human Baselines for Benchmarks: AI Now Outperforms Junior Accountants" (49938232, mercor blog,
10-02): seen in pass 1, grep-clean, never deep-read this session - left for the next window.
Anthropic emergent-misalignment-from-reward-hacking (49878806): already held estate-side
(catalog + memory/percolator/explore_handsbox_drain.jsonl hits on "emergent misalignment"; also
named in 10-02 residue). LiveBench (49893058): still unread, JS wall per both sibling sweeps;
do not claim it read. Magnitude (49911995): banked 10-03. "Benchmarks Are Free Now" (49934581):
read, off-area, recorded here so nobody re-fetches it for this area. DoGBench (49928118): paper
already in catalog since 10-01; only the HN discussion, if any, would be new.
