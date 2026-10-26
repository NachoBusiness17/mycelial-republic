# INTAKE CARD — DIMASHVETS: UZU 105 tok/s ON M5 MAX (founder announcement) (Grok batch 2/10, 2026-09-04)

## ITEM (verbatim root, fxtwitter 200 OK)
@dimashvets (Dima Shvets), Sep 03 2026 15:25Z: "We're releasing speculative decoding in our
inference engine Uzu, starting with Qwen3.6-27B. On Apple M5 Max with 128 GB of unified
memory, our Mirai-M stack reaches 105 output tokens/sec entirely on-device - 2.9x faster
than the fastest MLX speculative-decoding implementation we benchmarked. The result comes
from full-stack co-design: DFlash + our Weaver model, tree-based speculative decoding,
Mirai quantization, our verification algorithm, and Metal kernels optimized for Apple
silicon. ... 105 t/s is the evidence, full-stack integration is the moat. But tokens/sec
are not actually the metric we ultimately care about. More on that soon."
Stats: 126,730 views / 18 replies / 15 RT / 117 likes / 131 bookmarks (bookmarks > likes,
second time on this release — latent demand census repeats).

## INGEST — the chart (image read directly: HRTQ6hAboAA-_5A)
Qwen3.6-27B output tok/s, Apple M5 Max 128 GB: uzu+specdec **105** · MTPLX (MLX specdec)
**55** ("1.9x faster") · llama.cpp+specdec **30** ("3.5x") · MLX plain **26** ("4x").
Vendor-self-published bar chart.

## THREAD (Amendment 2, web_reader through the wall)
- @dimashvets self-reply (9h later, 1.4K likes): "Run the model ... Mirai-M ... 105 tok/s
  specdec on M5 Max — 14.5 GB, 27B parameters. Install with one command."
- @artuskg: "(Q)wen 3.8 27B? Asking for a M4 owner." (578 views) — the M5-gating question,
  asked by the market, UNANSWERED by the vendor. Same open question the uzu card filed.
- No community note.

## MAP
- RE-FIND, filed honestly: this is the SAME release as watch/INTAKE_UZU_SPECDEC_20260903
  (20/25 BUILD NOW → Rocinante prep) — repetition is emphasis, scored as a re-find (N:2).
  What is NEW: the founder pinning a CONCRETE falsifiable number (105 t/s, M5 Max 128GB,
  14.5GB Mirai-M 4-bit) where the uzu card had to work from an implied range (~110-125),
  plus named stack internals (DFlash + Weaver, tree specdec, Mirai quants).
- The chart's MTPLX baseline (55) vs the community's r/LocalLLaMA 63: vendor baseline
  reads low — makes the "2.9x" headline bigger than a 63-baseline would. Noted in attack.
- Lands in ROCINANTE_PREP_20260903.md: probe target sharpens from "beat ~63, approach
  ~110-125" to "beat ~63 community MTPLX; vendor pins 105."

## [SOCRATIC] assumption attacked: "two vendor posts = stronger proof" — attacked by
reading the chart bytes instead of the headlines. Instrument: image read + baseline
cross-check. What survives: a sharper falsifiable target; the proof obligation is
unchanged (still $0 vendor claims until Oct 27).

## ASSERT
Uzu's full-stack co-design (DFlash draft + Weaver + tree specdec + Mirai quants + Metal
kernels) makes on-device Qwen3.6-27B run at 105 output tok/s on M5 Max 128GB — ~2x the
best alternative MLX speculative-decoding stack.

## ATTACK
1. Vendor-measured, vendor-published baselines: chart MTPLX=55 vs community-measured 63
   (r/LocalLLaMA, cited in the uzu card) — baseline selection inflates the multiple;
   against 63 the same absolute number is 1.67x, not 1.9x.
2. No protocol in the post: prompt classes, context length, accept-rate, and quant of the
   MTPLX baseline undisclosed — not replicable from the bytes (metrics page is the
   protocol to replicate, per the uzu card).
3. The M4 question from the thread is unanswered — M5-gating of the spec-decode boost
   remains open, and we cannot buy an M5 Max to disprove it before Oct 27.

## MEASURE ($0, run)
Chart + thread read this turn (image bytes, fxtwitter JSON, web_reader). Probe target
UPDATE filed to Rocinante prep: day-one protocol stays the uzu card's (tok/s, TTFT,
memory, same quant, three prompt classes), target now: beat 63 (community MTPLX), check
against 105 (vendor). Kill condition: our M5 Ultra run < 90 t/s on Mirai-M 4-bit → the
co-design claim is M5-Max-flattered or non-portable; < 63 → dead.

## SCORE — F:4 P:4 C:5 W:3 N:2 = **18/25 → BUILD, WINDOWED** (Rocinante lane)

## TRI-STATE
- Release + 105 t/s claim + stack names — **Supported as the vendor's pinned claim**
  (root + chart + self-reply all consistent, two fetches); **Unproven as performance**
  (no independent M5 number exists; only M4-plain data so far).
- 14.5GB Mirai-M 4-bit memory footprint — **Unproven** (vendor self-reply).
- MTPLX=55 baseline — **Disputed as representative** (community 63 measured independently).
- Bookmarks>likes demand shape — **Supported** (126.7K views, 131 bm / 117 likes).

## VERDICT — **BUILD** (windowed): update the Oct 27 probe card with the pinned targets
(105 vendor / 63 community floor; 14.5GB footprint row) inside ROCINANTE_PREP; nothing
runs before hardware. No new wire — the uzu card's wire already covers this lane.
TWO COUNTERS: FORBIDS quoting "2.9x" without the baseline dispute attached. PAID RENT:
replaced an implied target range with one falsifiable number + a footprint row.

## THE CROP
Qwen3.8-27B and Muse Glimmer support not probed this pass; the metrics-page protocol not
re-fetched (uzu card holds it); the 17 other replies unread. The Economist chair should
price the Mirai-quant lock-in against the GGUF fleet standard before engine selection
freezes.

## FILED — watch/INTAKE_DIMASHVETS_UZU_M5_20260904.md + room thread "intake"
