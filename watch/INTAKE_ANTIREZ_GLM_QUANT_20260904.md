# INTAKE CARD — ANTIREZ: GLM 5.3 vs DeepSeek v4 Flash LOCAL QUANT BENCHMARK (Grok batch 10/10, 2026-09-04)

## ITEM (verbatim root, fetched via fxtwitter 200 OK)
@antirez, Sep 03 2026 22:11Z, note-length: "I ran an extensive benchmark against DeepSeek
v4 Flash and GLM 5.3 Flash Q2, Q4 and mixed quants. Those are the results obtained. Mix of
(hard-ish) benchmarks on cybersecurity, math, QA, ..."
Stats: 8,286 views / 12 replies / 6 RT / 104 likes / 22 bookmarks.

## INGEST — the benchmark table (image read directly: HRUxWFPbIAApoLU, terminal screenshot)
| model | 4K greedy baseline | combined after reruns |
|---|---|---|
| DeepSeek 0731 Q2 | 7/12 | 10/12 strict, 11/12 semantically |
| DeepSeek 0731 mixed Q2/Q4 | 7/12 | 8/12 |
| Vision Experimental Q2 | 6/12 | 9/12 |
| Vision Experimental mixed Q2/Q4 | 7/12 | 10/12 |
| GLM 5.3 Q2 | 8/12 | 9/12 |
| GLM 5.3 Q4, two-Mac TP | 8/12 | 10/12 |
His caption: recovery totals (winning 4K cases not rerun); overall completion 43/72 →
56/72 strict, 57/72 counting DeepSeek Q2's mathematically-right/wrongly-formatted answer;
"GLM Q2's greedy 16K run scored 10/12 versus 9/12 using normal sampling"; remaining
failures = "long Olympiad proofs that identify promising or correct results but never
emit a final answer."

## THREAD (Amendment 2, web_reader through the wall)
- @XadenRyan: evals nice, but "how much did it stay on task — smaller models spray crap
  all over the codebase" → the missing axis is out-of-answer damage. (379 views)
- @ivanfioravanti: "I bet Qwen 3.8 Flash Next will be lower." (744 views)
- No community note. Author's second sentence is in the image caption itself (greedy vs
  sampling tradeoff) — he attacks his own numbers before the thread does.

## MAP
- ROCINANTE DOCK (watch/ROCINANTE_PREP_20260903.md): "GLM 5.3 Q4, two-Mac TP" is a named
  person already running the fleet's future substrate class (Mac cluster, tensor parallel)
  on the fleet's workhorse model family. Day-one receipt, not speculation.
- GLM53FLASH_RESEARCH_20260901 + ECONOMIST_53FLASH_HOSTING_VERDICT_20260901 (antirez
  already cited once in corpus — author known, this content new). Quant-sizing data feeds
  the local-quant decision table (Q2 usable-at-9/12 vs Q4 10/12 on 512G-class memory).
- Converges with SWARM_SCALE_PLAN's output-envelope discipline: his "never emits a final
  answer" failure mode and Ryan's "spray" complaint are the completeness/discipline axes
  the flight recorder already encodes.

## [SOCRATIC] assumption attacked: "a 12-task self-run table is just vibes" — attacked by
reading the image (methodology is unusually honest: reruns, strict/semantic split, greedy
vs sampling disclosed, failure modes named). Instrument: image read + thread fetch.
What survives: directional quant-ranking value, not a general leaderboard.

## ASSERT (steel-man)
Locally quantized GLM 5.3 and DeepSeek v4 Flash are both usable on hard mixed benchmarks
at Q2–Q4, with GLM 5.3 Q4 (two-Mac tensor parallel) at 10/12 and DeepSeek Q2 the semantic
leader at 11/12 — long proofs fail by non-termination, not by wrong direction.

## ATTACK
1. n=12, self-curated tasks, no latency/tok-s, "recovery totals" mix runs across settings
   — ranking noise is high (evidence: his own 8/12→10/12 swings from reruns alone).
2. Quant-conditional and hardware-conditional (two-Mac TP config not fully specified in
   root) — not replicable from the post alone (image lacks mem/context-length rows).
3. Ryan's reply names the missing axis: no out-of-answer damage metric (spray/task-hygiene).
Survives as directional because the author is high-signal, methodology-transparent, and
self-attacking — but "GLM beats/loses to DeepSeek" as a general claim stays out of reach.

## MEASURE ($0, run)
Table read directly from the image bytes; thread fetched; author existence/credibility
cross-checked (ECONOMIST_53FLASH_HOSTING_VERDICT already cites him). Kill condition for
the directional claim: our Oct 27 probe runs a 12-task hard mix, GLM 5.3 Q4 TP vs Q2
single-Mac; if Q2-single ≥ Q4-TP score, the "two-Mac TP matters" reading is dead.

## SCORE — F:5 P:4 C:5 W:4 N:4 = **22/25 → BUILD NOW**

## TRI-STATE
- The table is antirez's honest self-run result — **Supported** (image read; methodology
  disclosed; author credibility on file).
- GLM 5.3 Q4 two-Mac TP 10/12 / DeepSeek 0731 Q2 10/12 strict 11/12 semantic —
  **Supported as his numbers**, **Unproven** as general ranking (n=12, self-curated).
- Greedy 16K beats sampling for GLM Q2 — **Unproven** (single setting, no variance).
- Quantized-frontier-on-Mac-cluster is practically usable — **Supported-directional**
  (his completion rates + the fleet's own weights plan), falsifiable Oct 27.

## VERDICT — **BUILD** (small, $0, today)
File the table into the GLM/Rocinante corpus as probe-target evidence; add the two-Mac TP
receipt to ROCINANTE_PREP; add "out-of-answer damage / stays-on-task" as a scored axis in
the next gauntlet design (Ryan's reply is the receipt the axis is externally demanded).
TWO COUNTERS: FORBIDS citing "GLM 5.3 Q4 > DeepSeek v4" as settled model selection from
this table. PAID RENT: one day-one probe protocol + one gauntlet axis, both pinned.

## THE CROP
Latency and tok/s were not benchmarked (completeness only); the exact TP topology and
memory footprint sit below the fold; a different-mind contest (Economist chair) should
re-derive what n=12 can and cannot support before this enters any LOCKED order.

## FILED — watch/INTAKE_ANTIREZ_GLM_QUANT_20260904.md + room thread "intake"
