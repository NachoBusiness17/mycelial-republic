# SWEEP: evals-self-improvement via x - 2026-10-06

source-fetched: 2026-10-06. Seat: sweep-evals-self-improvement-x (dynamic workflow actor).
Area: evals-self-improvement (feeds tools/citation_lint.py, tools/violation_ratchet.py, the
tools/workflow_gate.py scenario cards, memory/percolator/invariants.json, and
memory/burns/LEDGER.jsonl). Two passes per the ask. Pass 1: 30+ candidates enumerated across
six WebSearch queries (author-anchored and topic-anchored; the generic site:x.com query
returned one diluted hit, same disease the 10-05 seat logged). Pass 2: 6 items read end to
end this sitting: 4 X posts resolved through the fxtwitter door (api.fxtwitter.com, 5/5
including one X-article-embedding post), plus arxiv 2609.11028 (abs) and arxiv 2609.37834
(API + abs + html full text). The reddit-door items of the 10-05 sweep were NOT re-verified
here (out of this seat's door; no reddit fetch attempted).

Sibling awareness: this directory already holds the 10-06 sibling sweeps
evals-self-improvement-arxiv.md (12:35) and evals-self-improvement-hn.md (12:46) plus their
confirmation scripts (_confirm_28_out.txt covers the FINETUNING area's items, not mine).
Overlap law was run against catalog/catalog.jsonl and memory/ per the ask, and every overlap
field below also names the 10-05 sweep-level provenance explicitly.

## Q1 - THE JUDGE2 MASS DUEL RE-JUDGING RAN (the ask's named check, executed this sitting)

The menu item (RIB_DEEPSEEK_ELDER_SEAT.md menu item 3, "mass duel re-judging, ~300 asks,
est $0.3-1.5") is now a landed receipt for the byte-provable subset of the ledger.

- Coverage wall, computed before firing: logs/duel/duels.jsonl holds 80 rows, 70
  ember-judged single-family (instrument: venv python read this sitting). Only 12 rows are
  faithfully runnable: the 12 W8 rows, whose contender answers are byte-provable (glm via
  w8_glm_{plan,schema,adv}.md per w8_series_duel.py GLM_ANSWER_FILES; grok/ds/qwen via
  w8_contenders_20260930.jsonl, keys adv#ds etc. verified present) and whose asks are
  byte-recoverable (plan/schema are static strings in the committed driver a331069c7; adv
  embeds tools/duel_harness.py recovered through the sha256-pinned frozen blob
  aj1_frozen_harness_v11.py, sha verified twice this sitting, the AJ1 method).
- REFUSED rows, named: 18 v1mf + 2 retro (ask bytes unrecoverable: BASELINE_SPEC.md was
  edited between the 06:32 run and the 07:28 commit a331069c7; the receipt
  V1_MULTIFAMILY_DUEL.md records a 25,962-char ask that matches no git blob: 19,644 bytes
  pre, 32,518 post. Judging 09-30 answers against today's amended spec would let the judge
  penalize contenders for Amendment 7 content they never saw); 29 live + 2 ah10 + 4 f1
  (contender answers never cached; the run_rejudge provenance gate cannot pass); 3 d6ab
  (already judge2'd blind by deepseek 2026-10-01, watch/inbox/hermes_burn/DUEL_JUDGE2.md,
  3/3 ember agreement).
- The run: 12 items built with duel_harness.judge_prompt (blind by construction, original
  swap layout preserved, provenance gate a_chars/b_chars exact match, 12/12 pass), fired
  through tools/ds_workhorse.py (deepseek-chat, temperature 0.3 hardcoded at
  tools/ds_workhorse.py:84, thinking-off mandatory per its harness laws), banked 12
  mode=altjudge rows with rejudge_of pointers (append-only lineage, L32). Ledger grew
  80 -> 92 rows, corr_id e2656ec5, last ts 2026-10-06T17:03:47Z (instrument: venv python
  count this sitting). Files: judge2_items.jsonl, judge2_results.jsonl,
  judge2_bank_summary.json (all in this directory).
- RESULT: 0 of 12 verdicts flipped (flip_fraction 0.0). Combined two-family record over
  every comparable row now banked: 0 flips in 15 (glm altjudge 10/10 agree, deepseek
  12/12 + the 3 d6ab pilot 3/3). Zero dissents, so zero re-look tickets minted. Spend:
  $0.0202 metered by the carrier (judge2_results.jsonl per-row cost_usd; results rows carry
  prompt_tokens per the hollow-batch law, ok_api + ok_material 12/12).
- HONEST CONTAMINATION DISCLOSURE (the AJ1 pattern): deepseek is itself a contender family
  in 6 of the 12 rows, and the deepseek judge picked the deepseek contender in all 6. Those
  6 agreements are self-family evidence, weaker than they look; the clean rows (no ds
  contender: the 3 glm-grok and 3 qwen-glm pairings) also agree 6/6, which is the part that
  independently corroborates ember. A third family with no dog in these rows (grok-4.7,
  funded per L9) is the next judge2 arm if the operator wants the flip fraction defended
  beyond n=2-family.

## Q2 - THE 28 SWEEP ITEMS: WHICH BECOME REGISTER ROWS

The 10-06 DIGEST's gap (DIGEST.md:58, via the 10-06 burns lens section 2b) stands partially
cured for the x door this sitting. Verdicts, instrument-tagged:

- CONFIRMED, register-row grade: BenchShield (dair_ai 2026-09-12 post re-resolved through
  fxtwitter status 2098592449568591902; arxiv 2609.11028 abstract fetched end to end: 456
  human-labeled trajectories, 31,000+ runs, 23-94% -> 77-100% full-chain recall, up to 65%
  cost cut, 96% runtime detection; repo live at github.com/1690940255ran-dot/benchshield).
  The 10-05 bank's every number re-verified. Delta: the repo's own line "the question is not
  whether your harness can be cheated - it is how easily, and how would you know" (search
  snippet grade).
- CONFIRMED with delta: BenchPress (the 10-05 item's Feb-25 date and its
  "5-7 points median error" quote anchor to a post I could not locate; what I verified is
  the announcement post 2069891280679670242, 2026-06-24, verbatim "<3.9%... Evals are rank 2
  lol", plus paper 2606.24020, 84 models x 133 benchmarks, rank-2). Register row should cite
  the June post + paper, not the unlocated Feb one.
- CONFIRMED verbatim, in-window: harshbhatt7585 benchmarks survey (status 2101685636596175238,
  2026-09-20, quote byte-matches the 10-05 bank). Deltas: PostTrainBench is
  arxiv 2603.08640 with a v1.1 leaderboard (Oct 2026) and a 10% -> 34% frontier climb in
  eight months (search-snippet grade).
- CONFIRMED: ErdosBench smoke (prz_chojecki status 2065744053963022375, 2026-06-13; the
  fetched post is part 6 of the thread and carries the 14-problem public smoke + 226-problem
  private full battery verbatim; repo github.com/ulamai/erdosbench).
- ATTRIBUTION CORRECTED: the "Our agent scored 100% on both. It solved 0 tasks." line is
  @yiwei_hou's per two independent profile mirrors (twstalker, sotwe), not MogicianTony's as
  the 10-05 x.md item 8 claims. Snippet-grade evidence, original status not resolved; the
  10-05 attribution should be struck or corrected before that item cites a URL.
- NEW this sitting: arxiv 2609.37834 Mixture of Self-Improving Branches (2026-09-29, in
  window): abstract snapshot was already held (catalog.jsonl:690750,
  state/arxiv/2026-09-30/2609.37834v1.txt, 1,708 B); the fetched abstract adds the
  branch/router design and the 34.8/11.6/3.8 gains. STRUCK: the louishsu.xyz digest snippet
  claiming "a second judge agrees with the headline judge on 493/500 rows (98.6%)" does NOT
  exist in the paper full text (html fetched, NOT FOUND) - banked nowhere, a live lesson in
  fetch-before-bank.
- NOT covered here: the arxiv and hn doors were confirmed by sibling seats today (their
  files in this directory); the reddit door's 4 items remain second-seat-unconfirmed as of
  this write.

## Q3 - THE BURNS LEDGER: CARRIERS, WRITER, CLOCK

- memory/burns/LEDGER.jsonl: still 693 rows, last ts 2026-09-28T13:45:00Z (10-06 lens read
  corroborated; no appends). NO writer instrument exists: rg over tools/ mag/ scripts/ finds
  only readers (tools/anomaly_flagger.py:89, tools/burns_verdict_enum.py:57,
  tools/drift_dashboard.py:62 T6 track, tools/drift_pairs_stamp.py:127,
  tools/estate_query.py:57). The 693 rows were seat-appended during the 09-25..09-28
  burn-wave program; nothing owns the clock.
- The descent leg 8 spend carrier in practice: memory/runs/hermes_burn/usage.jsonl
  (tools/hermes_burn.py): 3,010 rows, per-row {ts, id, model, turn, prompt_tokens,
  completion_tokens, cost_usd, ok}, ts range 2026-10-01T13:11:41Z .. 2026-10-05T07:12:43Z,
  mtime 10-05 03:12 local - silent about 31 hours, not 8 days (instrument: venv python read
  this sitting). Note: its last row's model is anthropic/claude-haiku-4.5, an UNFUNDED key
  family per L9; flagged, not adjudicated here.
- memory/game/FLOW_LEDGER.jsonl (mag/game_flow.py, the AH14 corr writer per
  tools/estate_query.py:16-22): ALIVE (213 rows, last 2026-10-06T14:01:42Z, corr_id on 31
  rows) but carries ZERO cost/token fields; all 213 rows are action=test enqueue events. It
  is a corr stream, not a spend ledger; estate_query's "corr-carrying burns writer" comment
  oversells it.
- Reconciliation answer: resuming memory/burns/LEDGER.jsonl would NOT contradict the
  DIGEST/RECEIPT record - the 10-06 burns lens rule 4 already declares DIGEST/RECEIPT pairs
  plus git commits to BE the record until the ledger resumes. A resume must append only new
  events (amend-never-rewrite, no backfill), keep verdict values inside
  memory/burns/verdict_enum_map.json (tools/burns_verdict_enum.py --apply writes the join
  sidecar and never touches the LEDGER), and one item per record (RIB_MD_RECORD). The
  honest gap: with no writer and no freshness owner, resumption is a discipline choice, not
  an instrument fix; the instrument-shaped cure is the census-patrol pattern (expected-next-
  row + grace + alert) pointed at usage.jsonl, whose 31-hour silence is the live drift
  nobody owns.
- This run banks its own leg-8 rows: judge2_results.jsonl (per-row tokens + cost) and
  judge2_bank_summary.json ($0.0202) beside the receipt.

## Q4 - ROW EXPIRY: CADENCE AND PRIORITY BEFORE 2026-10-30

The seeded grid (RIB_MODEL_GARDEN_ROUTING.md): 32 rows carry moment 2026-09-30 and 14 carry
2026-10-01 (rg counts this sitting), so under L16 the cliff is 2026-10-30/10-31. Design:

- Family events outrank the date (L16's own clause): ling-3.0-flash-fin:free retired from
  the free tier (R062, 404 x3) and GLM-5.3-Flash dropped from the roster (10-05 lens) are
  already STALE NOW; re-measure or supersede those rows first.
- Weekly battery wave, not a cliff: one scheduled wave per week (the estate's Task Scheduler
  pattern: MagFtsIndexDaily/MagCensusPatrolDaily precedent) firing the 8-item battery per
  funded family at the ECON-documented shape, appending new-moment rows and keeping lineage
  (fill procedure steps 1-5, RIB_MODEL_GARDEN_ROUTING.md:202-209). Five weekly waves
  retire the 46 seeded rows before the cliff at W8-series economics (the 12-duel wave cost
  $0.02-2.00 depending on judge family).
- Priority order (dollars-at-risk first): (1) judgment + adversarial-review + planning
  columns for the funded set (glm-5.3-prime, qwen3.8-max-prime, grok-4.7) because premium
  routing misroutes $0.4+ asks; (2) the judge axis itself - this sitting proved the replay
  path at $0.02/12 rows, and the judge rows carry the same 09-30/10-01 moments; (3) the
  blind-grade pass for any cell that routes dollars (L18: cost-per-blind-point is the
  champion metric); (4) unfunded families' cells stay UNMEASURED legally (sonnet-5.5,
  fable-5.1 hold 0 of 8 and are not in the funded set).
- Falsifier carried from the rib: a routing decision citing a stale-moment cell is a one-bug
  violation; cells filled without a receipt are theater.

## Q5 - GROWS PASS 3: A PROOF THAT CAN FAIL

What passes 1-2 proved: R4 memory ran twice (x2 passes, GROWS proven, commit
becb53618/R4B receipts); the R1-R5 rounds banked 79/89/76/95 findings
(DAWN_REPORT_20261006.md:33-35) - the estate grows because each round finds NEW defects.

Pass-3 design (falsifier first, per the ask):

- Pre-register, BEFORE the window: (a) the register union R = frontier_olm_2026-10-03
  (42 rows) + 10-04 (22) + 10-05 (23) + the R1-R5 landing receipts + the ledger's closed
  topics; (b) the novelty test: a finding is NOVEL iff its distinctive-phrase grep against
  catalog/ + memory/ + R misses (the same overlap law this sweep runs); (c) the counter:
  novel findings per round, computed by the fold, not asserted.
- The pass FAILS (i.e., proves fixpoint) on this measured result: a full self-improvement
  round whose finding set yields ZERO register rows after the pre-registered novelty test,
  AND whose round-over-round novel counts continue the decay across R4 -> R5 -> R6 (the
  churn-decay curve of 2609.34924: a flat improvement curve over a growing ledger is the
  spend-theater verdict, computed not argued). Two prior all-dedup rounds in a row is
  fixpoint evidence; one is noise (n=1 judge law applies to estate rounds too).
- The mirror falsifier also pre-registered: if R6's novel count is HIGH but zero of its
  findings land as rib/pack/receipt changes, that is the descent protocol's own
  spend-theater verdict (L13) - growth in findings with no artifact leg is theater in the
  other direction. GROWS is only good if the growth compounds into instruments.
- What would be measured: novel-count per round (target 0), artifact-landing rate per round
  (target > 0 while novel > 0), and the self-steal meter (every ask answered from resident
  ribs, 0 re-derivations) as the cheap leading indicator.

## Banked items (6, strongest first; full schema in the SweepResult)

1. BenchShield (dair_ai post + arxiv 2609.11028 + repo). Quote: "a corpus of 456
   human-labeled trajectories drawn from over 31,000 public agent runs". Overlap: catalog 0,
   memory 0; held sweep-level only in frontier_olm_2026-10-05/sweep/evals-self-improvement-x.md.
2. Mixture of Self-Improving Branches (arxiv 2609.37834). Quote: "34.8% on Olympiad-level
   mathematical reasoning, 11.6% on Terminal-Bench 2.0, and 3.8% on SWE-bench Lite".
   Overlap: abstract snapshot held at catalog.jsonl:690750; upgrade banked with overlap
   declared; the digest's 98.6% second-judge claim STRUCK (not in full text).
3. BenchPress announcement (DimitrisPapail status 2069891280679670242). Quote: "Basically
   can run 5 \"principal\" benchmarks and estimate the rest within <3.9%. Kinda nuts it
   works so well." Overlap: catalog 0, memory 0; sibling hn.md:111 cites it as context only.
4. Benchmarks survey (harshbhatt7585 status 2101685636596175238). Quote: "Learn about LLM
   benchmarks, from foundational like GLUE for language understanding to PostTrainBench for
   evaluating AI autonomy." Overlap: catalog 0, memory 0; 10-05 x.md sweep-level only.
5. ErdosBench smoke (prz_chojecki status 2065744053963022375). Quote: "The full benchmark
   has 226 problems". Overlap: catalog 0, memory 0; 10-05 x.md bank only.
6. Attribution correction: the 100%/0-tasks line is @yiwei_hou's (mirrors twstalker + sotwe),
   not MogicianTony's as the 10-05 bank claims. Quote: "Our agent scored 100% on both. It
   solved 0 tasks." Overlap: catalog 0, memory 0; correction targets the 10-05 x.md item 8.

## Considered, not banked

- ImpossibleBench (fjzzq2002/Ziqian Zhong): paper confirmed real via search cluster (arxiv,
  OpenReview, ICLR 2026, github.com/safety-research/impossiblebench) but no X status
  resolved and no primary page fetched this sitting; stays a named follow-up, snippet grade.
- elliotarledge "stop falling for it" mini-swe-agent 74% (Jun 7): out of the 30-day window,
  snippet only.
- METR reward-hacking LessWrong, Alignment Forum four-case eval, HN "Exploiting agent
  benchmarks" thread: eval-adjacent but non-X and not fetched end to end; leads.
- smol.ai AINews Jul 7 + Lilian Weng harness post: ALREADY HELD (10-05 00:44-04:23 wave
  banked the Harness Engineering Handbook, 10-06 burns lens section 2c).
- FrontierMath Erdos (epoch.ai): distinct from ErdosBench; not fetched.

## Owed / not done

- The 55 remaining ember-only duel rows (29 live + 2 ah10 + 4 f1 + 18 v1mf + 2 retro) are
  unjudgeable until their ask + answer bytes are frozen at judgment time; the fix is a law,
  not a run: every duel row must carry ask_sha256 + a frozen ask blob (the AJ1 frozen-harness
  law generalized), else L16 expiry and judge2 coverage stay decoupled from the ledger.
- A third-family judge2 arm (grok-4.7) over the same 12 rows to de-contaminate the
  deepseek self-picks: not run (spend discipline; one arm per sitting).
- The 10-05 MogicianTony item needs its URL struck or corrected in that file; I did not edit
  a sibling's sweep file.
- usage.jsonl's 31-hour silence and its haiku-4.5 last row: flagged for the operator; no
  alarm instrument owns that clock yet.
