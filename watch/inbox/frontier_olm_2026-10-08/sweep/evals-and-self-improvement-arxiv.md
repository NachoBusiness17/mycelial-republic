# FRONTIER SWEEP: evals-and-self-improvement via arxiv - 2026-10-08

source-fetched: 2026-10-08. Doors: arXiv Atom API (`export.arxiv.org/api/query`, 5 targeted
queries, all `submittedDate:[202609070000 TO 202610090000]`, sortBy=submittedDate desc:
`all:"LLM-as-judge"` 30 entries; `abs:"benchmark contamination"` 1; `abs:"semantic entropy"` 6;
`abs:"data contamination"+cat:cs.CL` 3; `abs:"contamination"+abs:"language models"` 30;
`abs:"self-improvement"+abs:"language models"` 30; `abs:"judge"+abs:"position bias"` 6) plus
`arxiv.org/abs/` deep reads. Pass 1 considered 106 candidate entries (above the 30 floor).
Pass 2 deep-read 12 papers at abs-page depth: 2610.07354, 2609.33044, 2609.35025, 2610.07570,
2609.27510, 2609.37577, 2609.34017, 2609.33467, 2610.06366, 2610.09229, 2609.38372, 2610.02975.
No door failures: every query returned parseable Atom; every abs fetch succeeded first try.
Tooling degradations, honestly: inline PowerShell lost `$`-variables to the shell layer twice
(parse errors, receipts in-session); all greps were re-run via script files
(`_catalog_grep.ps1`, `_mem_grep.ps1`) and rg. One repo-wide recursive grep was too slow,
killed at 4 min, and replaced with a scoped grep over memory/rib, memory/lenses, memory/press,
memory/improve, and the 10-05..10-08 frontier dirs.

## Grounding read before sweeping (what the ask's citations resolve to)

- The ask's Q7/Q8/Q9 text matches `watch/inbox/frontier_olm_2026-10-07/lens/laws.md:105-107`:
  judge2 owed ("may never be the only judge on a verdict that routes dollars", the mass
  re-judge of the whole duel ledger unbuilt), ask_bank v1 = 20 asks wanting 100+, law census
  unbuilt ("same law filed twice under different names: the one-bug-many-jackets disease").
- The ask's 0.871 number resolves to today's lens
  (`watch/inbox/frontier_olm_2026-10-08/lens/burns.md:91`, `lens/questions.md:221,234,301`)
  and its SOURCE is arXiv 2610.07354 (semantic entropy AUROC 0.871 on GSM8K for
  small-to-large escalation), which the day-7 sweeps ALREADY banked
  (`frontier_olm_2026-10-07/sweep/inference-efficiency-arxiv.md:12-13,46` and
  `open-local-language-models-arxiv.md:9,17,28,43`; day-8 sibling re-bank at
  `frontier_olm_2026-10-08/sweep/open-local-models-arxiv.md:12`). This sweep therefore does
  NOT re-bank it; my own deep read of it this sitting confirmed the number and is logged in
  the considered trail only.

## Overlap policy and what I found (commands actually run)

`powershell -File _catalog_grep.ps1` over catalog/catalog.jsonl (15 fixed-string patterns) and
`powershell -File _mem_grep.ps1` (14 patterns over memory/rib, memory/lenses, memory/press,
memory/improve, watch/inbox/frontier_olm_2026-10-0{5,6,7,8}), plus
`rg -l "2609\.33044|2609\.35025|..." watch/inbox/frontier_olm_2026-10-08/sweep` for same-day
sibling collisions (EXIT-CLEAN, zero hits after substring false-positives like "exercise"
matching bare CISE were excluded). I also READ both area predecessors end to end
(`frontier_olm_2026-10-07/sweep/evals-self-improvement-arxiv.md` full file;
`frontier_olm_2026-10-06/sweep/evals-self-improvement-arxiv.md` method + Q1/Q4 sections) to
draw the known-set line. Findings:

- 2610.07354 (Escalation Signals / 0.871): banked day-7 x2 sweeps + day-8 sibling. DROPPED.
- 2609.33467 (A Cheap Verifier): catalog holds a FULL raw fetch from the 09-28 sweep
  (`frontier_olm_20260928/sweep/_raw/full_2609.33467.txt`, 102,455 bytes). DROPPED.
- 2609.27510 (Uncheatable Eval): banked day-7 item #7 (deep read). DROPPED.
- 2609.37577 (Pair Difficulty): banked day-6 Q1 (`:105-110`) and named in day-7 trail. DROPPED.
- AutoDataBench NAME COLLISION: catalog L806542 holds `state/arxiv/2026-10-01/2609.40097v1.txt`
  titled "AutoDataBench: A Data-centric Testbed for Accelerating Auto Research" (Yuan et al.,
  read this sitting: a data-intelligence testbed, NOT the task-writing benchmark). My banked
  item is the OTHER AutoDataBench, 2609.35025 (Luo et al.). The estate's law census
  (ask Q9) must key on arxiv id, not title, or it will merge two different papers - a live
  specimen of the duplicate-label disease (lens/graph.md:25-30) found inside our own catalog.
- Zero overlap (catalog + scoped memory/watch + today's siblings): 2609.33044, 2609.35025,
  2610.06366, 2610.07570, 2610.09229, 2609.34017, 2610.02975, 2609.38372. These eight bank.

## Banked items (strongest first; all quotes verbatim from arxiv abs pages fetched this sitting)

### 1. Pinned and Still Unstable: Within-Judge Verdict Variance and the Noise Floor of LLM-as-Judge Leaderboards - arXiv 2609.33044 (v1 2026-09-27, v2 2026-09-30) - ZERO overlap

Four frontier judges, one enterprise cloud platform, Arena-Hard/AlpacaEval 2/MT-Bench.
Identical temperature-zero inputs to the SAME judge produce different verdicts across re-runs
("per-item flip rates of roughly 5% on average and about 40% on the close-call items that
decide leaderboard margins"), a 40x per-judge range (0.13% to ~10%); cross-judge agreement
coarse (Kendall's tau 0.42-0.64 Gemini vs Sonnet); of 15 expected head-to-head orderings, 12
survived all re-runs of the main judge but only 8 survived under every judge. v2 is a
claims-provenance correction pass (no new experiments). Protocol it proposes: multiple
re-runs, per-item stability profiles, adjacency intervals, and results under at least two
judges from different families.

Estate fit (Q7): the judge2 re-judge of the ~300-ask duel ledger needs a NOISE FLOOR before a
flip count means anything, and day-6's banked priors (order-swap ~25% floor via LLMAdBench
2609.32533; close-gap dominance via Pair Difficulty) measure flips under CHANGED conditions.
This paper measures flips under NO change at all - pure serving nondeterminism - so it is the
lower bound: any ember-1-vs-judge2 flip rate must be read as (observed - ~5% same-family
resample floor), and the estate's planned second-family judge is literally this paper's
proposed protocol. Its per-item flip-rate metric is directly implementable on the duel ledger
by re-running ember-1 on a stratified sample before paying for judge2.

### 2. AutoDataBench: Can Agents Write the Data That Feeds the Self-Improvement Loop? - arXiv 2609.35025 (2026-09-28) - ZERO overlap (name-collides with catalog's 2609.40097, different paper)

Given an original task and a target model's attempt record, an agent must write a NEW task
meeting acceptance criteria for "validity, novelty, difficulty and behavioural coverage";
industry practice accepts generated data sample-by-sample against such criteria, so the
benchmark scores the writer, not a downstream model. "No agent we evaluate scores above 20
out of 100 at the default time budget" (45 minutes); quadrupling the strongest agent's time
improved its score substantially at almost unchanged cost per usable task. Code:
github.com/StarDewXXX/AutoDataBench.

Estate fit (Q8): the ask-bank grower (20 -> 100+ contamination-safe asks) is exactly this
benchmark's shape, and its headline is the warning label: generated asks are cheap only if
you do not gate them. The steal is the four-axis acceptance gate - the NOVELTY axis is the
duty_fuzz twin-minting gate made an admission criterion rather than a post-hoc patrol, and
the time-budget result says per-ask generation budget (or iteration count) moves quality
more than model choice. Our generator should mint, then be scored on validity/novelty/
difficulty/coverage per ask, with the 20/100 external number as the calibration prior for
what raw generation achieves.

### 3. Correct Verdicts, Flawed Reasoning: Structured Auditing of LLM-based Vulnerability Reasoning - arXiv 2610.06366 (2026-10-05) - ZERO overlap

Manual audit: "approximately 60% of correct vulnerability verdicts are accompanied by
fabricated or unverifiable claims" that free-form CoT hides. VERA makes models emit a
Structured Reasoning Record (tracked pointers, memory operations, state transitions in
machine-readable fields) checked deterministically over eight failure modes; the schema
enables mutation testing of judges at scale without human annotation; reasoning flaws appear
equally in correct and incorrect verdicts, and VERA exposes 87% of reasoning errors that
free-form LLM-as-judge evaluation misses.

Estate fit (Q7/Q5): the duel ledger's verdicts can be dollar-routing-correct for fabricated
reasons - a 60%-class hazard the verdict column cannot see. The SRR pattern (claims as
machine-checkable pointers) is the same instrument class as tools/citation_lint.py extended
to reasoning steps, and the mutation-testing trick (inject known flaws, measure what the
judge catches) is a $0 way to score judge2 candidates on our own ledger before the paid run.

### 4. Unanimously Wrong: Certified Abstention from How Medical LLM Consensus Forms - arXiv 2610.07570 (2026-10-06, GenAI4Health @ NeurIPS 2026) - ZERO overlap

A system "can be unanimously wrong, returning the same incorrect answer on every sample";
13.4% of unanimous votes on MedQA are wrong. ProbeGuard reads consensus FORMATION (agreement
trajectories, minority persistence, retrieval saturation, rationale semantic entropy, active
counter-evidence probes) instead of the final consensus state, lifting unanimous-layer error
discrimination from chance to 0.696 AUROC, with a Learn-then-Test certified rule answering
six in ten unanimous-layer questions at 9.0% observed selective risk.

Estate fit: the estate's own consensus priors (flock consensus 0/3 at strength 0.6-0.67,
lens/laws.md:102; ArcticSwarm premature-consensus, day-7 DIGEST) get their external
mechanism: the signal is in the trajectory, not the vote. For the gauntlet and any pooled
review, sampling the agreement TRAJECTORY (does minority opinion persist across samples?)
is a buildable free-lane feature, and the certified-abstention shape (answer only when the
risk bound holds) is the abstain rung the tier ladder lacks between local and paid.

### 5. Conditional Accuracy Profiles: Diagnosing LLM Judges across Deployment Conditions - arXiv 2610.09229 (2026-10-06) - ZERO overlap

Single-number judge accuracy "hides the deployment conditions under which a judge succeeds or
fails"; CAP is a benchmark-agnostic post-hoc decomposition of pairwise judge accuracy into
eight conditions (content sensitivity, robustness, rationale quality). Seven judges, six
benchmarks: omission sensitivity is not predicted by aggregate accuracy; Position Robustness
has the strongest rank stability (mean Spearman 0.87) yet degrades most under adversarial
stress; profiles offer "a more actionable basis than aggregate accuracy for selecting LLM
judges."

Estate fit (Q7): when judge2 lands, its acceptance row should be a CONDITION PROFILE (what
input perturbations, omission, rationale quality flip it), not one accuracy number - the
same per-condition discipline the estate already applies to routing cells (UNMEASURED grid,
lens/laws.md:104). The eight conditions are a ready-made column set for the judge2
registration row.

### 6. Maat: Independent Deterministic Contract-Based Governance for Multi-Agent LLM Workflows - arXiv 2609.34017 (2026-09-27) - ZERO overlap (only raw forum-JSON name hits)

Runtime governance validating agent handoffs against versioned workflow contracts with "no
language model in the validation or scoring path." Six workflows, 6-15 agents, 522 trials.
Two self-corrections worth stealing whole: (a) a post-publication audit found the benchmark
scorers "credited any early halt as a prevented defect"; corrected gains are +7.7% to +29.1%
in five workflows, flat in one; (b) manual review of 94 halts found 35 false alarms (37%),
and counting them as failures, "the governed arm scores below the ungoverned arm in four of
six workflows."

Estate fit (Q5): the promote-WARN-gate-to-percolator-invariant decision (fix-the-cause law,
lens/laws.md cited in ask) needs exactly Maat's accounting: a gate's value = defects caught -
false alarms caused, and the false-alarm ledger must be MANUALLY REVIEWED, not self-scored
(their scorer artifact = our grader-self-strike pattern). Colon reveal at 25/28 true positives
looks promotable ONLY until its false-positive count is in the same table; Maat's 37% shows a
majority-true gate can still be net-negative. Deterministic no-LLM validation is also the
containment direction the shell-door work already took.

### 7. Reliable Self-Evolution with Imperfect Proxy Rewards (CISE) - arXiv 2610.02975 (2026-10-02) - ZERO overlap

Cheap proxy scores in self-evolving search "may assign high scores to infeasible candidates"
and those false positives "may contaminate both the final output and the feedback used to
guide subsequent generations." CISE builds candidate-specific conformal reward intervals
(conditional conformal inference + iteration-wise online density-ratio estimation) and only
returns candidates whose EVERY property interval fits its feasible region; "all candidates
returned by CISE are true positives under high-fidelity evaluation," at the cost of a
smaller shortlist. Code: github.com/MLAI-Yonsei/CISE.

Estate fit (Q8/Q5): the ask-bank and percolator promotion both currently accept on point
scores; CISE is the published shape for interval-gated acceptance - mint an ask only if its
novelty/contamination interval clears the duty_fuzz delta threshold with margin, promote an
invariant only if its catch-rate interval clears. Their headline hazard (false positives
poisoning the FEEDBACK loop, not just the output) is precisely the twin-contamination risk
in a self-feeding bank: one phrasing twin accepted into the bank teaches the generator that
twinning works.

### 8. Self-Evolving Harness on Multiple Tasks with the Agent as Its Own Optimizer - arXiv 2609.38372 (2026-09-29) - ZERO overlap

A harness is "the code around a language-model agent that organizes prompts, calls tools,
manages context, and controls execution"; here the same frozen model that solves tasks
"directly edits the harness that runs it." From a 49-line seed harness, two-stage training
gains +4.48 in-distribution (surpassing Codex) and +12.64 out-of-distribution across five
OOD benchmarks; continual training lifts Claw-Eval 66.17 -> 68.06. Emergent mechanisms
analyzed: "output truncation, history compaction, and independent review."

Estate fit: day-7's trail explicitly deferred the harness-RSI vein to a future sweep
(frontier_olm_2026-10-07/sweep/evals-self-improvement-arxiv.md:76); this is that vein's
cleanest specimen. The estate IS a self-evolving harness (violation ratchet, citation lint,
percolator, gates); the steals are (a) harness diffs as first-class reviewable artifacts -
every self-edit lands as a diff against the ratchet, (b) keeping dominated historical
harness versions as lineage (day-6's RSI-Router finding, same shape), and (c) the sober note
that "independent review" EMERGED as a mechanism - the harness evolved toward the estate's
own gate architecture unprompted.

## Considered and not banked (Pass 1/2 trail, for the census)

2610.07354 Escalation Signals (banked day-7; my read confirms 0.871 GSM8K semantic-entropy
escalation AUROC, difficulty-only baseline matching it on synthetic data, and a
cached-outcome transfer collapse 0.908 -> 0.518 correctly forecast - all already in estate
files). 2609.33467 Cheap Verifier (banked 09-28 full raw). 2609.27510 Uncheatable (banked
day-7). 2609.37577 Pair Difficulty (banked day-6). 2609.24516 LLJ Cards (judge-eval
reporting guidelines; superseded in coverage by items 1+5's protocols). 2609.38420 Type-6
Logic (verification methods non-interchangeable, kappa ~0.034 vs LINC; thin estate hook).
2609.32622 CoT-Pass@k audit (judges accept corrupted chains; claim class covered by item 3).
2610.01243 VLM position-bias audit (decisions change on 60% of prompts reordering; covered by
day-6's order-swap prior). 2609.31184 bias-corrected sustainable eval (latent-variable bias
correction; adjacent to day-6's banked set). 2610.04370 Boundaries Agree, Labels Do Not
(intra-annotator stability as quality/contamination check - nearest Q9 analog found, not
banked: it addresses human re-annotation, not law-file dedup). 2609.34661 Codoku,
2610.00416 chess prompt-opt benchmark, 2609.25352 SSP-Bench (renewable-benchmark family -
ask-bank-adjacent but generation mechanisms already covered by item 2's acceptance-gate
framing). 2609.35308 session-level contamination (multi-turn false-premise adoption).
2610.05976 Self-Step Rejection (self-verifier acceptance gate). 2609.38516 recursive social
improvement (copying skill files: efficient not effective). 2609.34712 RSI-Router (banked
day-6 Q4).

## Cross-cutting take for the improve loop

Three convergences across independent papers this sitting: (1) every judge-reliability paper
measures a DIFFERENT flip axis - order-swap (~25%, day-6), close-gap dominance (day-6),
within-judge resample (~5% avg / ~40% close-call, item 1) - and the judge2 flip count is
uninterpretable until all three floors are named in the same row; (2) correct-verdict/
wrong-reason (item 3) and unanimous-but-wrong (item 4) both say the verdict column is the
weakest instrument on the ledger - machine-checkable reasoning records and consensus
trajectories are the two published upgrades, both runnable on free lanes before any paid
re-judge; (3) acceptance gates beat generation quality: items 2 and 7 independently conclude
that gating generated items per-axis (novelty intervals, coverage criteria) is where yield
comes from, which is the ask-bank growth plan and the percolator promotion plan in one shape.

## Honest limits

- No dedicated Q9 (law-census) item was found in the 30-day window; the nearest analogs
  (2610.04370 label stability; the catalog's own AutoDataBench title collision, above) are
  noted, not banked as answers. The census remains an estate build.
- No estate instrument was run this sitting: no meter rows, no judge2 run, no ask-bank mint,
  no duty_fuzz pairs - this sweep only mines and dedups external work.
- All 8 banked items were read at abs-page depth (title, authors, dates, abstract,
  comments, links); no full-text HTML/PDF reads this sitting, so theorem/procedure details
  inside the bodies remain unread (same depth the day-7 predecessor used for 2 of its 8).
- Quotes are verbatim from fetched abs pages; where the fetch tool summarized rather than
  quoted, I re-fetched (2609.35025) for exact sentences before quoting.
