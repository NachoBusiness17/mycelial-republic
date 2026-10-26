# frontier sweep: evals + self-improvement via arXiv - 2026-10-06

source-fetched: 2026-10-06
Area: evals-self-improvement via arxiv. Feeds tools/citation_lint.py, tools/violation_ratchet.py,
the tools/workflow_gate.py scenario cards, memory/percolator/invariants.json, and
memory/burns/LEDGER.jsonl, because verdicts need second judges, rows expire, and spend rows are
the descent protocol's own falsifier.

## Method (what was actually fetched)

Pass 1, broad sweep. Four arXiv Atom API queries via export.arxiv.org (sortBy=submittedDate,
descending), each listing enumerated entry by entry (id, title, date, first author, one verbatim
abstract sentence per entry):

1. `all:"LLM as a judge"` - 30 entries, 2026-09-24 through 2026-10-05
2. `all:"self-improvement" AND all:"language model"` - 25 entries, 2026-09-27 through 2026-10-05
3. `all:"model routing" AND all:"language model"` - 20 entries, 2026-08-09 through 2026-10-03
   (entries dated 2026-08-09 to 08-31 sit outside the 30-day preference and were not banked)
4. `abs:"model collapse" AND abs:"iterative"` - 15 entries, 2026-02-10 through 2026-10-01
   (only the 2026-09-10 to 10-01 rows were in-window candidates)

Candidate pool: 90 enumerated entries considered; 60+ inside the 2026-09-06 to 2026-10-06
window, well past the 30-candidate floor. The listing pages (arxiv.org/list/cs.CL/recent and
/list/cs.LG/recent) were NOT fetched this sitting: the four API queries alone cleared the
candidate floor with tighter relevance than the listing pages gave yesterday's run, and
yesterday's file (frontier_olm_2026-10-05/sweep/evals-self-improvement-arxiv.md:16) already
records that those pages degrade to a partial ~50-entries-per-day view.

Pass 2, deep reads. EIGHT items read end to end on arxiv.org/abs pages (title, authors, dates
and versions, full abstract, quantitative findings, categories, comments field each):

- 2609.32533 (LLMAdBench), 2609.37577 (Pair Difficulty Matters, EMNLP 2026 short),
  2609.31857 (LLM Judge Validation Under Sparse Overlap, NeurIPS 2026),
  2610.05094 (Judge Design Choices), 2609.33955 (Judge Measurement Systems),
  2609.34712 (RSI-Router), 2610.01493 (Text Entropy Rate Filtering, NeurIPS 2026),
  2609.36892 (Harness Evolution as Learning)

## Degradations (honest log)

- No door 403'd or degraded. All four API queries and all eight abs pages returned on first
  fetch; no fallback path was used, and none is claimed.
- Two WebFetch abstract extractions (2609.31857, 2609.33955, 2609.37577, 2610.01493,
  2609.34712) returned faithful paraphrase-plus-snippets rather than the full abstract verbatim;
  the verbatim quotes banked for those items are the short exact snippets the fetch pipeline
  copied from the page, not full-abstract quotes. Items where the full abstract came back
  verbatim (2609.32533, 2609.36892) carry the highest confidence.
- HTML full-texts (arxiv.org/html) were not fetched this sitting; everything below abstract
  depth for these eight items is NOT asserted.

## Overlap vs our holdings (the instrument, this sitting)

Scan: `.venv/Scripts/python.exe -X utf8 C:/Users/foste/AppData/Local/Temp/overlap_check_evals_1006.py`,
exit 0, elapsed 252.8s. catalog.jsonl read line-by-line: 1,130,965 lines, 322,474,755 bytes.
memory/ walked with junction pruning: 545,909 files, 2,881,771,969 bytes. 14 candidate
signatures (IDs, titles, distinctive phrases). Findings:

- 2609.32533 LLMAdBench, 2609.31857 Sparse Overlap, 2610.05094 Judge Design, 2609.34712
  RSI-Router, 2609.36892 Harness Evolution: ZERO hits on ID, title, and phrases. New to
  holdings.
- 2609.37577 Pair Difficulty: abstract snapshot already held (catalog.jsonl:690682,
  state/arxiv/2026-09-30/2609.37577v1.txt, 1,368 B, lsa zone, mtime 2026-09-30T06:31:01Z).
  Banked below as an upgrade with the overlap declared; the EMNLP acceptance, the
  rank-gap-conditional argument, and the proxy-inconsistency diagnosis are the new depth.
- 2610.01493 Entropy Rate: abstract snapshot already held (catalog.jsonl:870276,
  state/arxiv/2026-10-02/2610.01493v1.txt, 1,574 B, mtime 2026-10-02T06:30:25Z). Banked below
  as an upgrade; the quantitative results (null logprob filter, +42% unique trigrams, the
  collapse-detector correlation) are new depth.
- 2609.33955 Judge Measurement Systems: known-by-ID only
  (memory/runs/corpus_gap_research/ARXIV_REGISTER.json:5600-5603, verdict REAL, cited_in the
  frontier_olm_20260928 sweep's open-and-local file). Never deep-read by any prior seat; the
  abs read here is the first. Declared, not silently re-confirmed.
- Dropped from banking as already held: 2609.11149 (catalog.jsonl:443767,
  state/arxiv/2026-09-11/2609.11149v1.txt, held as "A Fragility Spectrum for Recursive
  Language-Model Training" since 09-11), 2609.31184 (catalog.jsonl:581019) and 2609.31215
  (catalog.jsonl:581026), both held since 09-28.
- 2609.35025 AutoDataBench was in yesterday's candidate pool at title/abstract level
  (frontier_olm_2026-10-05/sweep/evals-self-improvement-arxiv.md:18,46) and a same-name
  collision exists (catalog.jsonl:806542 is 2609.40097, a DIFFERENT paper sharing the
  AutoDataBench name prefix). Not banked; excluded by the anti-rebank rule.
- Yesterday's nine deep-read items (SAGE 2609.36043, Audit the Scaffold 2609.34924, and the
  rest per frontier_olm_2026-10-05/sweep/evals-self-improvement-arxiv.md:20-22, 67-80) do not
  intersect this sitting's bank; no re-banking.

## Q1: judge2 mass duel re-judging - what the literature says about flip fractions

The ask's Q1 (run judge2 over historical verdict rows; what fraction of single-judge verdicts
flip) is an estate-instrument run that THIS SEAT DID NOT RUN; no judge2 process was executed
here. What the sweep banks is the measured prior and the sampling design the run needs:

- 2609.32533 LLMAdBench (cs.AI, 2026-09-26, 18,000+ human judgments, 8 frontier judges):
  "Even the most stable models reverse roughly one quarter of their decisions when the
  presentation order is swapped, agreement across models is low", and a fine-tuned Qwen3-8B
  outperforms all zero-shot frontier judges on held-out prediction. Read: a single-judge flip
  fraction has a noise floor near 25% from presentation order alone; any judge2 flip count
  below that floor measures order bias, not verdict error. The fine-tuned-cheap-judge result is
  the second-judge economics the elder-seat law wants: a small trained judge can beat expensive
  zero-shot ones.
- 2609.31857 LLM Judge Validation Under Sparse Overlap (NeurIPS 2026; v2 2026-09-29; 10 judges,
  4 evaluation matrices): at 5% pairwise overlap, wrong-decision rates reach 25% and the
  probability of selecting the wrong best judge among ten is 65%; the proven minimum-overlap
  result is rho >= 0.25 for non-borderline judges; stratified allocation halves false-rejection
  rates vs random sampling. Read: this is the design law for WHICH historical duel rows get the
  judge2 re-look: sample overlap by stratum, not at random, and treat borderline judges as the
  hard case the formula does not save.
- 2609.37577 Pair Difficulty Matters (EMNLP 2026 short): "Under the Bradley--Terry geometry
  underlying pairwise aggregation, each proxy is dominated by close-rank-gap pairs"; far-gap
  pairs carry the ranking signal but barely move the proxies. Read: predicts WHERE duel
  dissents concentrate: in close pairs, exactly where a flip matters least for rankings. The
  judge2 re-look queue should weight far-gap dissents as the loud signal and report
  rank-gap-conditional flip rates, not one global fraction.
- 2610.05094 Judge Design Choices (2026-10-04, 10 reasoning models): "changing the rating
  scale alone can shift measured bias by up to 0.93 points (rating task)"; model identity is
  the dominant variance source (leniency shifts up to 56.1 percentage points across models;
  28.9pp leniency drop from detailed prompts; reasoning-effort reduction moved nothing).
  Read: judge2 is a config change, not a rerun. Pin its prompt, scale, and model per the
  L28 per-animal harness law BEFORE reading flip fractions, or the flips measure the new
  harness, not the verdicts.
- 2609.33955 Judge Measurement Systems (2026-09-27): production judging needs "a maintained
  measurement system": modular atomic judges over versioned evidence, human-in-the-loop
  governance, and every audit-surfaced disagreement routed to label correction, guideline
  revision, or judge improvement. Read: the re-look ticket is not a one-off mass run, it is the
  disagreement-routing half of a standing system; the paper's own honesty note (studies
  observational, the human reference itself required revision) matches our L24 law that
  consensus strength is not correctness.

## Q2: the 28 evals-self-improvement items - status

Per this morning's burns lens (watch/inbox/frontier_olm_2026-10-06/lens/burns.md:96-99):
evals-self-improvement (28 items), finetuning-adaptation (28), and inference-efficiency (32)
have sweep write-ups but ZERO confirmed register rows; "re-sweeping those three areas is waste;
confirming from the existing sweep files is the owed move." THIS SEAT DID NOT RUN the
confirmation pass (and today's sweep dir already carries sibling _confirm_28.py artifacts,
so a sibling may own it). This sweep adds 8 new deep-read candidates to the same pending
confirmation queue; it does not confirm yesterday's 28.

## Q3: the silent burns ledger - carrier, per the morning lens

Also answered by bytes read this sitting (via watch/inbox/frontier_olm_2026-10-06/lens/burns.md,
which read the ledger this morning): memory/burns/LEDGER.jsonl holds 693 rows, min ts
2026-09-25T10:05:50Z, max ts 2026-09-28T13:45:00Z, file untouched since 2026-09-28 13:15:27
local, day eight of no appends (burns.md:34-45). The carrier holding descent-leg-8 spend rows
is "the DIGEST/RECEIPT pairs, the ouroboros landing receipts, and git log" until the ledger
resumes (burns.md:43-45), and rule 4 of the anti-rebank list orders future windows to treat
DIGEST/RECEIPT plus a git commit as the record, never to assume a ledger row exists
(burns.md:212-213). Which instrument owns the clock is an estate design decision this sweep
did not make; the literature nearest to it (yesterday's MAADBench row, and this sitting's
2609.33955 audit-renewal cadence) both point the same way: expected-next-row time as a stored,
alarmed field.

## Q4: row expiry (L16, STALE ~2026-10-30) - refill cadence and priority

laws.md:89 records the open question: every seeded verdict row carries moment 2026-09-30 or
2026-10-01 and goes STALE 30 days later or on any family event. The sweep's transferable
designs:

- 2609.34712 RSI-Router (2026-09-28): "RSI-router establishes a stronger performance--cost
  Pareto frontier than 9 routing methods" by iterating four stages (subtask mining, routing
  strategy evolution, model-specific skill evolution, Pareto-optimal router selection) and
  KEEPING dominated historical routers as visible experience; it beats a DeepSeek-only
  baseline at 48.3% of the cost across five agentic benchmarks, cutting cost 74.7-82.2% on
  ALFWorld/ScienceWorld/WebShop. Read: the refill shape for our seeded rows is a Pareto
  population re-scored against fresh trajectories, supersede-by-append with the old row kept
  as lineage, which is exactly L16's "supersede by appending a new-moment row, keep the old
  row visible" (laws.md:37) with a mechanism attached. Priority order: re-measure rows that
  route dollars first (per L16), and within them the borderline cells, per 2609.31857's
  finding that borderline cases are where sparse-overlap validation fails.
- Also seen, not banked: 2609.32917 Planner-as-Router (fold routing into planning) and
  2609.34736 SeLMRoute (separate candidate-independent semantic evidence from the learned
  router) - both pass-1 entries read at title/abstract-snippet depth only.

## Q5: GROWS pass 3 - designing the third proof so it can fail

Context from bytes read this sitting: the morning lens states "GROWS not fixpoint is proven,
not open" for passes 1-2 (R1 fleet 79 findings, R2 gaps 89, R3 trust 76, R4 memory 95, R5
relay/meta; watch/inbox/frontier_olm_2026-10-06/lens/burns.md:180-182). Pass 3 needs a
falsifiable fixpoint criterion. Two steals:

- 2610.01493 Text Entropy Rate Filtering (NeurIPS 2026, sole author Lewis Mitchell): a
  non-parametric Kontoyiannis entropy-rate estimator h_k computed from raw text alone (no
  model logprobs, no oracle, no human data) works as a collapse detector (rho = +0.454,
  p < 0.0001) and its filtering beat logprob-based filtering, which showed NO significant
  benefit on any metric (p > 0.23): h_k-filtering gave +42% unique trigrams, +30% vocabulary,
  -19% repetition (all p < 0.0001) over six QLoRA generations on Llama-3.1-8B. Quote: "output
  diversity narrows as rare patterns are progressively lost". Read: run h_k per window over
  the append-only register/findings stream. Fixpoint becomes a measured curve: if new-window
  findings text collapses toward prior-register text (h_k falling, repetition rising toward
  the prior rows), the loop is at fixpoint or collapsing, and "every finding matches a prior
  register" is the zero-entropy endpoint. That is a number that can fail, computed from bytes
  we already produce.
- 2609.36892 Harness Evolution as Learning (2026-09-29): "we formulate harness evolution as a
  learning problem and explain these phenomena through approximation, generalization, and
  optimization errors", analyzing reachable policies, capacity under finite interaction
  evidence, and biased update dynamics. Read: the theory predicts a fixpoint is REACHABLE
  (bounded approximation/generalization/optimization error) and what it looks like: remaining
  improvements confined to the direction the biased update dynamic favors. Pass-3's design:
  pre-register the h_k fixpoint threshold and the expected direction of any residual finding;
  a window whose findings all match prior registers WITH the pre-registered entropy curve flat
  is the proof the estate reached fixpoint after all; findings still appearing is its failure,
  which is the point.

## Steal list (concrete)

1. The order-swap floor (2609.32533): before reading any judge2 flip fraction, run the
   presentation-order A/B on a judge2 sample; flips below the ~25% floor are order bias, and
   the mass-duel receipt must state the floor next to the fraction.
2. The stratified-overlap sampling law (2609.31857): judge2 re-look tickets are drawn by
   stratum with rho >= 0.25 pairwise overlap as the proven minimum for non-borderline judges;
   borderline judges get enlarged samples because the formula does not save them.
3. Rank-gap-conditional flip reporting (2609.37577): the judge2 receipt reports flip rate
   conditioned on rank gap; far-gap dissents are the loud signal, close-gap flips are expected
   noise.
4. Judge2 config pin (2610.05094 + L28): the second judge's prompt, rating scale, and model
   identity are frozen and recorded before the mass run; the 56.1pp model-identity leniency
   swing is why.
5. The Pareto-lineage refill (2609.34712 into L16): routing rows are refreshed by re-scoring
   the whole population against fresh trajectories, appending the new-moment row and keeping
   the dominated row visible; dollars never route on a row past its moment until re-scored.
6. The h_k fixpoint instrument (2610.01493 into GROWS pass 3): a model-free entropy-rate curve
   over the registers stream, threshold pre-registered, flat-curve-plus-matching-findings as
   the fixpoint proof.
7. Disagreement routing as a standing process (2609.33955): every judge2 dissent routes to one
   of label correction, guideline revision, or judge improvement, with the routing decision
   recorded; the audit renews the reference set on a cadence, matching the burns-ledger cure
   (store expected-next-row time, alarm on breach).

## Receipt

Doors this sitting: 4 export.arxiv.org Atom API queries (pass 1, 90 entries enumerated) + 8
arxiv.org/abs pages (pass 2, end to end). No 403s, no degraded doors, no fallbacks used. Local
reads: watch/inbox/frontier_olm_2026-10-06/lens/burns.md (217 lines, full),
watch/inbox/frontier_olm_2026-10-06/lens/laws.md (116 lines, full),
watch/inbox/frontier_olm_2026-10-05/sweep/evals-self-improvement-arxiv.md (94 lines, full),
catalog.jsonl rows 443767, 581019, 581026, 690682, 806542, 870276 (extracted by line number),
memory/runs/corpus_gap_research/ARXIV_REGISTER.json lines 5594-5607. Overlap scan:
`.venv/Scripts/python.exe -X utf8 C:/Users/foste/AppData/Local/Temp/overlap_check_evals_1006.py`
exit 0, 252.8s (catalog 1,130,965 lines line-by-line + memory walk 545,909 files with junction
pruning). Estate checks named in the research questions that were NOT run here: judge2 mass
duel re-judging (no run), the 28-item confirmation pass (sibling artifacts present), any
LEDGER.jsonl append or resume. All quotes are verbatim from the fetched pages named per item.
