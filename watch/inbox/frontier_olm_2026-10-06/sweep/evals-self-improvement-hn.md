# Frontier sweep: evals + self-improvement via Hacker News, 2026-10-06

source-fetched: 2026-10-06
Seat: sweep-evals-self-improvement-hn (dynamic workflow actor). Door: HN Algolia API
(hn.algolia.com/api/v1/search + /search_by_date, tags=story, numericFilters=created_at_i>1788652800
= 2026-09-06T00:00Z, i.e. last 30 days), then news.ycombinator.com/item?id=... for threads.
Dedup base read in full first: frontier_olm_2026-10-05/sweep/evals-self-improvement-{hn,arxiv,x,
reddit}.md (the day-5 mine) plus frontier_olm_2026-10-06/lens/{laws,burns}.md, so nothing below
re-banks day-5 work. Helper scripts + raw outputs live beside this file: _evals_confirm_sweep.py,
_evals_confirm_sweep_out.txt, _evals_frag_adjudicate.txt (all run this sitting, exit 0).

## RQ answers (the ask's five research questions)

### RQ1: judge2 mass duel re-judging - NOT RUN, inventory measured instead

Running judge2 over the historical verdict rows requires a paid second-family dispatch (the menu
item prices it at ~300 asks, est $0.3-1.5, RIB_DEEPSEEK_ELDER_SEAT.md:113-119); this sweep seat
ran no paid judges, so the flip fraction is NOT MEASURED, not zero. What I measured this sitting
(`_evals_confirm_sweep.py` section c, output `_evals_confirm_sweep_out.txt`):

- `logs/duel/duels.jsonl`: 80 rows, ALL dated 2026-09-30 (last ts 2026-09-30T23:50:54Z); judge
  histogram: fireworks/ember-1 = 70 rows, z-ai/glm-5.3-prime = 10 rows. Every row is n=1 judge:
  80 single-judge verdicts are the re-judge population, and every judge2 dissent becomes a named
  re-look ticket per the menu item's own yield clause (RIB_DEEPSEEK_ELDER_SEAT.md:117-119).
- The instrument spec is already frozen in the rib (slots labeled, no names, no prices, temp 0.3);
  nothing here substitutes for running it. Owed, priced, ready.

### RQ2: confirm the day-5 evals-self-improvement sweep items - DONE at liveness+quote grade

My census of the day-5 evals files reads 31 named deep-read/banked items (10 HN pass-2 + 9 arxiv
deep-reads + 8 X banked + 4 reddit banked); the day-5 DIGEST's count is "evals-self-improvement
(28)" (DIGEST.md:56-65). I could not reconstruct which 3 items their 28 excludes (the DIGEST does
not enumerate), so both counts stand: mine instrument-tagged to the four files, theirs to
DIGEST.md:57. Confirmation results (all fetches this sitting):

- 10/10 HN threads LIVE via Algolia items API, titles intact (49716123, 49655621, 49742415,
  49796714, 49897103, 49910150, 49911995 at 194 pts, 49916869, 49931859, 49962903).
- 9/9 arXiv IDs LIVE via export.arxiv.org; 6/9 abstracts still carry the day-5 stored fragments
  (2610.02142 "minutes of CPU time", 2610.00025, 2609.34924 "churn decays", 2609.38812 "61.43",
  2609.36556 "refreshable", 2610.02911 "looked consistent"). The 3 fragment-misses (2609.36043
  SAGE, 2609.38652 AgBench, 2609.07370 CPU benchmark) are FULL-TEXT-level quotes per the day-5
  file's method section; abstract refetch cannot see them, so they are UNADJUDICATED here, not
  proven false.
- 4/4 reddit posts LIVE via Arctic Shift with dates and scores matching the day-5 file exactly
  (1ws6bmh 57 pts 09-28, 1wtzedu 75 pts 09-30, 1waiu6b 47 pts 09-08, 1wpqbxp 1 pt 09-25). Three
  stored quotes confirmed verbatim in live selftext by direct needle search after my first
  normalizer pass produced false GONEs (the "57 of 60 held-out closed-loop tasks" and "propose,
  measure, reflect, and revise" fragments are byte-present; see _evals_frag_adjudicate.txt).
  1wpqbxp remains title-grade: selftext is 9 bytes, as the day-5 file recorded.
- 8 X items: the day-5 X file recorded handles and dates but NO status IDs, so liveness is not
  refetchable through my allowlisted doors. Recorded UNCONFIRMED (not failed).
- Which become register rows: the 23 mechanically-confirmed items are register-eligible today.
  Strongest register candidates, in order: SAGE 2609.36043 (paired acceptance test for the
  ratchet), 2610.02142 (keyword-harness ladder), 2609.34924 (churn-decay spend-theater meter),
  2609.38812 (61.43/49.36 verify-detect prior), 2610.02911 (probe-the-harness checklist), danluu
  49655621 (grader flips ~23% on rerun), rekursiv 49716123 (evidence ledger with unqualified
  panels kept), doyouok 49796714 (dead-man watchdog shape), reddit 1ws6bmh (the six-part
  admission battery) and 1wtzedu (the missing-base-row falsifier). The 8 X items stay sweep-level
  pending a recorded fetch. Writing register rows is the fold's move; this file supplies the
  verdicts.

### RQ3: the burns ledger is silent day eight - carrier found, reconciliation FAILS

- Confirmed by my tail: `memory/burns/LEDGER.jsonl` holds 693 rows, last ts 2026-09-28T13:45:00Z
  (line 693), matching frontier_olm_2026-10-06/lens/burns.md:36-45 line for line; last git touch
  ecf47999a 2026-09-29 23:01 (TIE-IT-ALL).
- The carrier that kept moving is `memory/runs/hermes_burn/usage.jsonl` (writer
  `tools/hermes_burn.py:66`): 3,010 rows, ALL dated 2026-10-01 through 2026-10-05 (by-day: 10-01
  = 236, 10-02 = 5, 10-03 = 1,034, 10-04 = 1,448, 10-05 = 287), last ts 2026-10-05T07:12:43Z -
  itself now silent over a day as of this sitting. So descent leg 8 spend rows exist for the
  10-01..10-05 window in usage.jsonl, while the burns LEDGER's separate verdict-row stream
  stopped 09-28; the file holds nothing for 09-25..09-30 and is not git-tracked, so whether an
  earlier rotation held those rows cannot be verified from here (OWED).
- Reconciliation with the DIGEST/RECEIPT record: FAILS. usage.jsonl sums to 14.7M tokens
  (11.81M prompt + 2.91M completion over 3,010 rows, my sum this sitting), while commit
  d5f89d97b's message claims "164.5M tokens, largest single run" for the day-5 mine, and the
  string "164.5" appears NOWHERE in frontier_olm_2026-10-05/RECEIPT.md or DIGEST.md (grep, zero
  hits, this sitting). Verdict: the 164.5M headline is phantom-class until a carrier names it -
  either a hand-copied number (the struck 191.8M disease, citation-lint class) or real
  workflow-actor token burn that NO usage-row writer meters (workflow children have no
  tools/hermes_burn.py call path in the evidence I read). Either way leg 8 has a coverage hole:
  "every paid dispatch banks usage" is unenforceable for workflow actors today.
- Which instrument owns the clock: NONE. The LEDGER's writer was the burn-wave driver (closed
  09-28); tools/hermes_burn.py is a passive meter that fires only when a paid dispatch happens -
  it meters spend, it does not own a cadence. The scheduled-task fleet (MagFreeLaneFleet 30 min,
  MagCensusPatrolDaily, MagFtsIndexDaily) each own their own beat but nothing watches either
  ledger's freshness. The cure is the 10-05 sweep's Doyouok shape: store an expected-next-row
  timestamp per ledger, a Task-Scheduler dead-man beat alerts on breach, and the alert triggers
  the census-patrol rebuild-and-verify path. That design is now backed by two measured silences
  (LEDGER day 8, usage.jsonl day 1+).

### RQ4: row expiry under L16 - cadence and priority order

Grounding: RIB_MODEL_GARDEN_ROUTING.md:54-62 (30-day expiry + family events; amend-never-rewrite)
and :202-209 (the fill procedure). Every seeded verdict row carries moment 2026-09-30 or
2026-10-01 (frontier_olm_2026-10-06/lens/laws.md:89, Q4), so the whole battery goes STALE around
2026-10-30 at once - a cliff, not a trickle. Proposed cadence and order, grounded in the fill
procedure plus this sweep's finds:

1. Weekly beat (new MagRoutingRefreshWeekly task, census-patrol exit-code shape): re-measure in
   priority order - (a) every WIN/CHAMPION cell first, because only those route dollars (L18);
   (b) contamination-suspect cells (grok-4.7 adversarial-review r1, laws.md:88); (c) UNMEASURED
   cells of the funded set, question-class priority (evidence-readable cheap cells before
   simulation-class premium cells, RIB_MODEL_GARDEN_ROUTING.md:234-242).
2. Family events fire an out-of-band re-measure of that family's whole column immediately
   (fingerprint change, carrier swap, deprecation, price: :54-62) - the Clef/decision-model
   release cycle shows vendor swaps now happen mid-week, not quarterly.
3. Every re-measure appends a new-moment row; stale rows stay as lineage (:61-62). A re-measure
   reuses the 8-item battery at the ECON-documented shape (:203-205) and fills cells FROM the
   receipt the same session (:206).
4. Cheap pre-rank before any full re-run: the BenchPress result (5 benchmarks predict the other
   44 within ~5-7 points median, day-5 X file item 3) says the weekly beat can pre-rank candidates
   with a 5-benchmark panel and spend the full battery only on rank changes - that is the
   re-measurement cadence's cost control.
5. Anti-contamination for the re-seed: pull new hidden asks from the hidden bank (Q8) or build
   them self-bench-style from the estate's own merged work (below), so a re-measured row is
   provably-unseen rather than plain-sight.
Deadline math: 2026-10-30 is 24 days out; at one funded family per weekly beat the battery
re-fills with one beat to spare only if the first beat fires within 7 days.

### RQ5: GROWS pass 3 - designed to fail

Pass 2 proved GROWS-not-fixpoint (R4 double pass, frontier_olm_2026-10-06/lens/burns.md:179-181).
Pass 3 must be able to return the opposite verdict. Design:

- Freeze the banked-set union U = round-1+2 (42 register rows) + day-4 (22 + 10) + day-5 (23 + 8)
  registers + the git-logged drops through 10-06 (the union the burns lenses itemize). Freeze the
  doors (same 8 areas x 4 doors) and a fixed window.
- Run the sweep at the same width. Instrument two rates per area: NEW-row rate (finds not in U at
  title/ID level) and UPGRADE rate (sweep-level rows that confirm into register rows).
- Fixpoint is REFUTED (GROWS again) if either rate is nonzero anywhere - the measured result that
  proves the estate is NOT at fixpoint is any single new find or any single upgrade.
- Fixpoint is PROVEN only if: zero new rows, zero upgrades, AND a second independent window
  replicates the zero, AND the relay leg (R5's next-loop target: a cheap seat boots on the fresh
  law pack) produces boot findings that all match prior registers. A pass-3 window whose findings
  all match prior registers is exactly the fixpoint witness the ask names; anything less is
  sweep-theater, the descent falsifier in miniature.
- Honest caveat: at current frontier velocity (this sweep alone surfaced 5+ new register-grade
  items inside 24h), the prior expectation is that pass 3 REFUTES fixpoint; the design's value is
  that the refutation is now a counted rate, not an impression.

## Pass 1: broad sweep (47 unique candidates, last 30 days)

Nine Algolia queries (search + search_by_date; terms: LLM judge evaluation, eval harness agents,
SWE-bench, self-improving agent, benchmark gaming reward hacking, fine-tuning small model evals,
RL fine-tuning open weights, evals, AI agent benchmark contaminated). Full list with ids, points,
dates, and query attribution in _evals_confirm_sweep_out.txt section b. Day-5 overlap (skipped as
re-banking): danluu 49655621, rekursiv 49716123, Real-SWE 49676820, DeepSWE defects 49766208
(day-5 pass-1 candidate only, never deep-read - upgraded below), SWE-bench docker socket 49709608,
Coding-Agents-Converged 49723395, Swesweep 49923102, OpenAPPA 49877515, Novus 49609555, RPi5
49898897, Autoheal 49877333, AgentOrchestrator 49787764, Continual Harness 49619356, parallel
test-time scaling 49815925, Benzi 49599867, Mozilla 49742415, and the day-5 evals candidates
49965723/49962903/49961283/49956391/49951195/49931859/49930810/49916869/49910385/49940599/
49934012/49796714/49710478 cluster. NEW this window (day-5 files carry none of them): Clef
49923692 (640 pts), vals magnetic semiconductors 49970667 (432 pts), Self-bench 49967408,
self-improving agent loops 49970405, Slowave 49702887 (memory area - sibling's lane, not banked
here), Wayfinder 49585201, Mistral Large 4 Scores 49978033, vals Testing-AI 49970806,
CppDepend parser eval 49963092, p(doom) Ask HN 49953734 (off-area).

## Pass 2: deep reads (fetched end to end this session)

1. https://blog.cloudflare.com/clef-decision-models/ + thread 49923692 (640 pts)
2. https://www.vals.ai/blogs/room-temperature-magnetic-semiconductors + thread 49970667 (432 pts)
3. https://github.com/mupt-ai/self-bench (+ HN 49967408)
4. https://www.scrimdata.com/blog/deep-swe-benchmark-defects-ambiguities (+ HN 49766208; the
   thread page fetched with zero visible comments - noted, the blog is the banked source)
5. https://blog.oodle.ai/self-improving-agent-loops/ (+ HN 49970405)
Plus the confirm-pass refetches (Algolia x10, arXiv API batch, Arctic Shift x4) and the day-5
file reads that opened the run.

## New items banked (strongest first)

### 1. DeepSWE defect audit: 37 of 113 tasks defective or ambiguous (scrimdata, HN 49766208, 2026-09-15)

Methodology is the transferable part: all 372 recorded failures reviewed, AI first pass, "a human
expert reviewed the 180 flagged cases", then fixes validated by rerunning ARCHIVED submissions
against corrected evaluators (no new code), turning 67 failures into passes (+4.22 to 6.19
percentage points). Quote: "Optimize against such scores without reading the failures, and you
train models to satisfy the evaluator rather than solve the problem." Second quote: "Before
counting another percentage point as progress, we should check what the point was awarded for."
Estate map: this is citation_lint + the ratchet's argument in benchmark form, and the
rerun-archived-submissions-against-corrected-evaluator move is exactly how judge2 re-judging
should bank its flips (replay, do not re-ask). Why: feeds githooks/pre-push gates and the duel
re-judge design. Overlap: "scrimdata" 0 catalog.jsonl / 0 memory (rg, this sitting); day-5 HN file
listed the thread id in its pass-1 candidate line only (evals-self-improvement-hn.md:12), never
deep-read. Confidence 0.95.

### 2. Clef: open-weight decision models + RL fine-tuning platform (Cloudflare blog, HN 49923692, 2026-10-01, 640 pts)

Jev-API-compatible classifiers on frozen Qwen3.8-27B / Qwen3.5-9B with rank-256 LoRA, prefill-only
inference, trained with label-smoothed CE + Brier + RLCD; BANKING77 macro-F1 94.20 vs Jev 79.74.
Quote (from the post, via the thread): "We currently use Qwen as the base model and post-trained
it to suit decision model use cases." The thread supplies the falsifiers the day-5 decision-model
wave (pending confirmation, DIGEST.md:71-81) needs: dgacmu's hands-on test had Clef vision at
~41% on a coin task losing to local gemma4:27b (53%, 4x faster); wongarsu: only median latency is
reported, fine-tuned LLM latency degrades with input size where Jev stays flat; agrippanux and
andrewingram: real-world tests found Clef 2-3x slower and worse than Jev; meander_water: the
"deterministic" claim is misleading on repeated calls. Why: advances the estate's pending
decision-model headline from sweep-level toward adjudication with named public counter-evidence;
the "rung under gemma:2b" claim must survive exactly these tests. Overlap: catalog 0 for
"clef-decision-models" and "49923692"; sibling finetuning-adaptation seat confirmed thread
liveness TODAY (their finetuning-adaptation-arxiv.md:72, raw/conf_hn_49923692.json); this bank
adds the thread falsifiers, which their confirm pass did not extract. Confidence 0.9.

### 3. Self-bench: private coding-agent benchmarks from your own merged PRs (mupt-ai/self-bench, HN 49967408, 2026-10-05)

Task from each merged PR (pre-commit state + PR description as instruction + authoring agent
writes hidden tests and a reference solution), Harbor-format output, scored accuracy-vs-cost with
a Pareto frontier. Quote: "A task is accepted only if the tests fail without a solution, pass with
the original implementation, pass again on a rerun, and survive an independent review." Live
leaderboards for next.js, supabase, sentry, posthog. Why: this is the ask_bank hidden-half design
(Q8, RIB_DEEPSEEK_ELDER_SEAT.md:114-123) already built by someone else - hidden tests unseen by
any judged family, drawn from real work - and it doubles as the Gero-4B admission gate's task
source and the GROWS-pass-3 re-seed source. Overlap: "self-bench"/"selfbench"/"mupt-ai" 0 catalog,
0 memory/inbox (rg). Confidence 0.85.

### 4. Opus 5.5 agents surface two magnetic semiconductor candidates - computational validation only (vals.ai, HN 49970667, 2026-10-05, 432 pts)

Agents ran DFT (PBE+U and HSE06) via Quantum ESPRESSO, designed one compound and flagged one
known one; the post's own falsifier discipline: "Neither the band gap nor the spin sorting has
been measured yet", plus input files, raw outputs, and a one-command public checker. Thread's
sharpest line (atq2119): "A lot of the public successes with agents is really LLM-driven local
search against an objective function that is evaluated in more traditional ways." Also a live
title-rot demo: HN's editorialized title dropped "Antiferromagnetic" and misreadings followed.
Why: the descent protocol's legs 6-7 (reasoning returned to instruments, verification by
instrument not narrative) in one public artifact; the checker + raw-outputs pattern is the shape
for the estate's own self-improvement claims. Overlap: "magnetic semiconductor" 0 catalog, 0
memory outside this session's own outputs. Confidence 0.9.

### 5. Building self-improving agent loops (oodle blog, HN 49970405, 2026-10-05)

Support agent on Temporal; traces analyzed, an LLM drafts a candidate prompt, a code-based eval
(no LLM-as-judge) runs over a golden dataset of prior tickets via experiment webhooks, and
promotion to production is a human approval through a Temporal signal. Quote: "Errors go back to
the model as tool output, not as exceptions, so it gets a chance to correct its own arguments."
Why: an outside replica of the estate's own law stack (promotion is human-gated, RIB_allseat
L25; deterministic grammar stays deterministic) - thin as a source, but it shows the loop shape
is converging industry-wide, which is convergence evidence for the percolator. Overlap: "oodle"
0 catalog; only this session's outputs in memory. Confidence 0.8.

## Overlap ledger (what I ran, this sitting)

- catalog/catalog.jsonl: grep -c per pattern - 49923692 = 0, clef-decision-models = 0, magnetic
  semiconductor = 0, self-bench/selfbench = 0, scrimdata = 0, oodle = 0, atq2119 = 0.
- memory/ + watch/inbox/frontier_olm_2026-10-06 (rg -l, trajectory/logs excluded): all candidate
  patterns hit ONLY this session's own output files, except 49923692/clef-decision-models which
  also hit the sibling finetuning seat's confirm files (declared in item 2) - no pre-existing
  holding carries any banked item.
- Day-5 dedup: every pass-1 candidate appearing in frontier_olm_2026-10-05/sweep/
  evals-self-improvement-*.md was skipped as re-banking (list in Pass 1 section).

## Caveats and not-run

- judge2 re-judging NOT RUN (needs a funded second-family dispatch; inventory and spec measured
  and named in RQ1). The flip fraction is unknown, not zero.
- Register rows not written by this seat; RQ2 supplies confirmation verdicts only.
- The 3 arXiv full-text-level quote fragments (SAGE, AgBench, CPU benchmark) are UNADJUDICATED,
  not disproven; the 8 X items are UNCONFIRMED (no status ids recorded by the day-5 file).
- usage.jsonl holds no 09-25..09-30 rows and is untracked, so pre-10-01 leg-8 reconciliation is
  OWED (rotation unknown).
- Thread 49766208 fetched with no visible comments (degraded render); banked source is the blog.
- Article quotes came through the WebFetch reader, one step removed from raw HTML.
- The 164.5M reconciliation verdict rests on: my token sum over the current file, my grep of
  RECEIPT.md/DIGEST.md, and the commit message d5f89d97b; if a second token carrier exists
  outside memory/runs/hermes_burn/, this verdict must be re-run against it (search was scoped to
  the path the descent rib names).
