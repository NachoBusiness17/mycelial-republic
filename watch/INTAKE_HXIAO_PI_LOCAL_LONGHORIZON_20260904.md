# INTAKE CARD — HXIAO: 16-HOUR ZERO-STEERING LOCAL AGENT LOOP (Grok batch 3/10, 2026-09-04)

## ITEM (verbatim root — fxtwitter 200 OK, note tweet, 3,979 chars)
@hxiao (Han Xiao), Sep 03 2026 20:25Z: "Sharing two long-horizon sessions on pi +
self-hosted models. first: 16 hours long, zero steering, 99 laps. I used pi + local models
to port our upcoming Jina model from bf16 PyTorch into MLX+MTP quants (model J in the
sequel). The local model is qwen3.8-flash-next-omlx-q4 from @jundotkim, running at the full
262K context window. I have only 2 plugins on pi: no /goal command — the first user msg is
the goal; pi-vcc for context compaction (drop-in replacement, vcc_search/vcc_recall as
memory recall tool); web read/search via jina-mcp; search_corpus vector search on a local
data room ... The whole setup runs on an M3 Ultra 512G ... peak memory ~150GB ... they
rarely compete at the flops level ... Takes: first lap 3.6h fully autonomous ... '2026
open-weight models are seriously trained for long-horizon tasks, not just a marketing
term' ... bash dominated every other tool — qwen3.8 does everything via bash including
edit/search/read/write ... web search was almost never called, despite every nudge."
Stats: 788 views / 2 replies / 8 likes / 10 bookmarks (bm > likes on a small post =
practitioner demand, same shape as the uzu census).

## THREAD (Amendment 2)
2 replies (unread — thin thread, root is the full artifact; noted in crop). No community
note. The author is Jina AI's founder — the post is also a product-adjacent demo, which is
the bias to price in.

## MAP
- ROCINANTE PREP (watch/ROCINANTE_PREP_20260903.md): M3 Ultra 512G is one generation off
  the 4x M5 Ultra buy. Peak ~150GB with two local models resident + "they rarely compete"
  is a memory-bandwidth/flops interleaving datum for day-one sizing. MLX+MTP quant porting
  pattern = the horse's first-job candidate list (uzu lane, QLoRA Stage 5).
- RIB_COMPACTION_DOC_20260831: pi-vcc IS our compaction doctrine independently re-found —
  algorithmic compaction + search/recall = the RIB fold + memory recall pair. Two lanes,
  same organ: signal.
- Long-horizon loop shape (first-msg-is-goal, nudge cadence, swimlane telemetry) maps onto
  overnight_churn / night cadence lanes.

## [SOCRATIC] assumption attacked: "vendor CEO demo = marketing inflation" — attacked by
probing the named tooling instead of the narrative. Instrument: $0 GitHub/registry probes.
What survives: tooling real, claim still self-reported.

## ASSERT
A minimal-toolset local agent loop (one goal message, algorithmic context compaction with
search/recall, bash-dominant tool use) sustains 16-hour autonomous sessions at 262K
context on a 512G Mac — long-horizon reliability is now a local-substrate property, not a
cloud property.

## ATTACK
1. Self-reported single-case: one task (bf16→MLX+MTP port), one operator, screenshots not
   logs — the 16h/99-lap number has no artifact (evidence: root only).
2. Survivor/selection bias: he shares the session that worked; a 9h lap on "another task"
   is mentioned in passing — base rate invisible.
3. "Zero steering" is softened by his own text: a "do better" nudge fired after every lap —
   the loop was nudged 98 times; zero-steering is framing.
4. Vendor interest: the ported model is Jina's own upcoming release — demo serves launch.

## MEASURE ($0, run)
- pi-vcc exists: **Supported** — sting8k/pi-vcc, npm @sting8k/pi-vcc, "algorithmic
  conversation compactor for Pi. No LLM calls", inspired by lllyasviel's VCC; ecosystem
  exists (pi-blackhole, pi-context-tools, r/PiCodingAgent comparisons). Probed this turn.
- pi agent exists: badlogic/pi-mono resolves (301→repo). Han Xiao's GitHub: 200.
- Kill condition for the long-horizon claim: run our own overnight_churn with
  first-msg-goal + no mid-loop steering for one night window; if the loop stalls without
  per-lap nudges, the "no /goal plugin needed" reading is dead on our stack.

## SCORE — F:5 P:4 C:5 W:3 N:4 = **21/25 → BUILD NOW**

## TRI-STATE
- pi + pi-vcc tooling real and public — **Supported** (GitHub/npm probes, this turn).
- 16h/99-lap session happened as described — **Unproven** (self-reported, no logs).
- qwen3.8-flash-next long-horizon capability claim — **Unproven** (single case, vendor-
  adjacent author), directional.
- M-series Ultra concurrency datum (two local models, ~150GB, no flops contention) —
  **Unproven**, falsifiable day one on Rocinante.
- Algorithmic-compaction organ converges with RIB doctrine — **Supported** (both docs).

## VERDICT — **BUILD** (small, $0)
File as a Rocinante day-one pattern: minimal plugins, pi-vcc-style ALGORITHMIC compaction
+ search/recall as the recall organ, bash-dominance as a steering/measurement expectation,
swimlane-style telemetry. Add one convergence line to RIB_COMPACTION_DOC citing the
independent re-find (VCC lineage). No new code; pattern rows only.
TWO COUNTERS: FORBIDS importing "zero steering" as a fleet claim — our loops keep the
nudge cadence until the kill-condition test says otherwise. PAID RENT: one Rocinante
pattern row + one RIB convergence receipt, both pinned to named files.

## THE CROP
The second session ("model J sequel") not ingested; 2 replies unread; the swimlane image
not analyzed; jundotkim's qwen3.8-flash-next-omlx-q4 weights not probed. Different-mind
contest: the maze-keeper chair should judge whether VCC-style algorithmic compaction fits
the Stage 5 brain's context diet.

## FILED — watch/INTAKE_HXIAO_PI_LOCAL_LONGHORIZON_20260904.md + room thread "intake"
