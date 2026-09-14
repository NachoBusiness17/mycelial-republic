# LANE 4/8 — V4.1 Flash SPEED + CACHE PROFILE

Date: 2026-09-10. Seat: zcode (Sancho), triparty lane 4. One file, no keys echoed.
Model string in our logs: `deepseek-v4-flash`. Primary source on disk:
`docs/report_v1/sources/DeepSeek_V41_Flash_tech_report.pdf` (51 pp, HF mirror confirms same text).

## THE POINT

The fleet has been running V4.1-Flash since 2026-08-02 — 46,666 logged calls across 598
sessions, ending seconds before this card was written. Our own cache share (0.964 recent-7d,
0.968 all-time) lands within a point of the claimed 97%, which makes the 97% claim
**plausible and already half-measured by us**. The speed claims (295/390 tok/s) we can NOT
yet confirm from our logs, because our `latency_ms` is a non-streaming round trip — our
68.6 tok/s per-call mean is an undercount artifact, not a contradiction. The P3 bench's
first job is streaming decode measurement; everything else is secondary.

Tri-state summary: 890 B/token SUPPORTED (primary). 1/8 persistent KV SUPPORTED (primary +
two independent echoes). 97% cache hit SUPPORTED-ADJACENT (our 0.964-0.968 measured; public
echo is 99.93% on V4-Flash, not V4.1). 295/390 tok/s UNPROVEN publicly, UNMEASURED by us in
streaming terms. 96M/$1.30 UNPROVEN (no public trace; arithmetic plausible, see table).

## CLAIMS TABLE

| # | Metric | Claimed | Observed by whom | Tri-state | Our measured (logs/provider_usage.jsonl) |
|---|--------|---------|------------------|-----------|------------------------------------------|
| 1 | Decode speed, agent run | 295 tok/s | Operator-reported ego_agent run (no public trace found) | UNPROVEN | Not yet measurable — our latency is round-trip. Wall-clock per-call: mean 68.6, median 68.7, p90 94.9, max 197.8 tok/s (undercount: includes TTFT + network + non-streaming) |
| 2 | Decode speed, API | ~390 tok/s | No public source found today | UNPROVEN | Aggregate wall-clock 162.5 tok/s all-time, 75.7 recent-7d — same undercount caveat |
| 3 | Cache hit rate | 97% (96M-token trial, $1.30) | No public trace of this exact trial; BigGo documents 99.93% hit on ~1B input tokens for $2.65 on **V4-Flash** (prior model) | DISPUTED-lean-SUPPORTED: number is realistic, sourcing is wrong model | **0.964 recent-7d (13,485 calls); 0.9681 all-time (hit 588,777,984 / (hit+miss) 608,222,520 tok)** |
| 4 | Fleet-wide cache share | 0.9437 | Our own frozen 7-day snapshot, `watch/astra_hold0/INSTANCE_I4_20260911.md:421` = 4,012,328,067/4,251,900,260, denominator `tok_in_stepfinish`, reaudit-confirmed | SUPPORTED (internal, fleet-wide all models — not v4-flash-specific; v4-flash-specific is higher, see #3) | Confirmed against row-level logs |
| 5 | Global KV footprint | 890 B/token (HBM), ~1/4 of V4-Flash, 437x vs V1 | Tech report Fig 1(b) + abstract; echoed by Sina Finance release coverage (437x), Wall St. Engine (~75% HBM cut) | SUPPORTED (primary on disk) | Not measurable from API — provider-side |
| 6 | Persistent KV footprint | ~1/8 of V4-Flash (SSD/host); SWA KV dropped from persistent cache, moved to 10%-of-host-DRAM pool, minutes TTL; global KV retained >=72h | Tech report §3.2.1 (primary); Wall St. Engine "87.5% persistent SSD cut"; The Neuron "cuts AI memory 8x" | SUPPORTED (primary + 2 independent echoes) | Not directly measurable; the >=72h global-KV retention IS testable via our hit-rate-vs-age curve (see checklist) |
| 7 | "~8x persistent KV reduction, SemiAnalysis" | Same as #6, attributed to SemiAnalysis | SemiAnalysis covers the V4 family (50x KV reduction at 1M ctx for V4-1.6T via CSA+HCA; InferenceX on V4 Pro) but I found no SemiAnalysis page stating exactly "8x persistent" for V4.1-Flash | PARTIAL: 8x is REAL but primary attribution is the tech report, not SemiAnalysis | n/a |
| 8 | Active params | 8B/token prefill, 16B/token decode (CED); 552B backbone MoE; 1M ctx | Tech report abstract | SUPPORTED (primary) | n/a |
| 9 | Blended cost | $1.30 per 96M input tokens = ~$0.0135/M | Unproven; arithmetic check: at ~97% hit, plausible if hit-price ~= $0.01/M and miss-price ~= $0.11/M. BigGo's $2.65/~1B tok (=$0.00265/M, hit-dominated) sits in the same band | UNPROVEN (needs today's pricing page in P3) | Our log has tokens but no price fields for this model — cannot self-check yet |
| 10 | Release status | V4.1-Flash live today (2026-09-10), V4 Pro phased out, API price cut | Sina Finance | SUPPORTED (public) | Fleet traffic predates today's announcement — we were on it 5 weeks early (pre-release endpoint under the same model string) |

## OUR-LOG FINDINGS (detail)

Source: `logs/provider_usage.jsonl` (18 MB), filter `model == "deepseek-v4-flash"`.

- All-time: 46,666 rows (46,277 ok), first 2026-08-02T22:57Z, last 2026-09-10T15:21Z,
  598 sessions. Prompt 1,642,878,446 tok; cache_hit 588,777,984; cache_miss 19,444,536;
  completion 10,981,579 tok.
- CAVEAT for historians: hit+miss (608M) does NOT sum to prompt (1,643M) all-time — early
  rows carry prompt_tokens without a full cache breakdown. The stable metric is
  hit/(hit+miss) = 0.9681. Recent-7d (2026-09-03 onward, 13,485 rows) is clean and gives
  0.964 by both denominators.
- Shape of a call: mean latency 1,448 ms, mean completion 235 tok, mean per-call miss tail
  ~460 tok (matches the report's CED story: input-heavy agentic workload, long cached
  prefix + small uncached suffix).
- kpi.jsonl: zero `deepseek-v4-flash` rows — model-level metering lives only in
  provider_usage.jsonl. P3 should keep it that way (one meter, one seat).
- No ego_agent artifact found in watch/ or memory/runs/ carrying the 295 tok/s or the
  96M/$1.30 trial — if the operator has that run's receipt, it should be filed next to
  this card (v41_paces/ is the shelf).

## P3 BENCH — MEASURE FIRST (ordered)

1. **Streaming decode tok/s, cold vs warm cache.** The only honest test of 295/390. Measure
   TTFT separately from inter-token rate; our non-streaming `latency_ms` cannot separate
   them and never will. Target: >=295 tok/s warm, and a number for cold.
2. **Cache hit share over a 24h agentic session-shaped replay** (our own session mix is
   the fixture — 598 sessions exist). Validates 97% on OUR workload, not a synthetic one.
   Provider-reported cache_hit_tokens is already the meter; zero new plumbing.
3. **Hit rate vs hours-since-last-touch.** The report guarantees global KV resident >=72h.
   Our replay can plot hit share against inter-call gap; the curve's knee is the real
   retention number. This tests claim #6 end-to-end from the outside.
4. **Pricing page capture + blended-cost arithmetic.** Pin today's hit/miss prices, then
   re-derive the $1.30/96M claim (#9). One screenshot-equivalent receipt closes it.
5. **TTFT vs context length** (1k/64k/512k/1M). CED claims prefill halved and near-flat
   decode FLOPs 4k->1M (+1/4). TTFT-vs-ctx slope is the outside-visible signature.
6. **Effective tok/s vs context length** — the DSpark speculative-decoding claim surfaces
   only as effective rate; if effective rate holds at 1M ctx while competitors fall off,
   that's the spec-dec fingerprint without provider internals.

## SOURCES

- Primary (on disk): `docs/report_v1/sources/DeepSeek_V41_Flash_tech_report.pdf`
  (HF mirror: [DeepSeek-V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/resolve/main/DeepSeek_V41_Tech_Report.pdf))
- [SemiAnalysis — DeepSeekV4 1.6T Day 0 to Day 43](https://newsletter.semianalysis.com/p/deepseekv4-16t-day-0-to-day-43-performance) (family-level 50x KV @ 1M ctx; no "8x persistent" line found)
- [Wall St. Engine on X — V4.1-Flash launch](https://x.com/wallstengine/status/2098021690349584587) (~75% HBM, 87.5% persistent cut)
- [Sina Finance — release day coverage](https://finance.sina.com.cn/tech/roll/2026-09-10/doc-inirinuw2931115.shtml) (live today, V4 Pro phased out, 437x)
- [BigGo Finance — cache-hit economics](https://finance.biggo.com/news/b76ddf18-0edf-4cc1-a004-fee5f869a86d) (99.93% hit, ~1B tok for $2.65 — on V4-Flash)
- [r/LocalLLaMA on V4 Flash cost](https://www.reddit.com/r/LocalLLaMA/comments/1uoq1wi/is_deepseek_v4_flash_really_extremely_cheap_to/), [Morph model page](https://www.morphllm.com/deepseek-v4-flash), [MindStudio local benchmarks](https://www.mindstudio.ai/blog/deepseek-v4-flash-local-benchmarks), [CLS.cn cost study](https://www.cls.cn/detail/2444045)
- Internal: `watch/astra_hold0/INSTANCE_I4_20260911.md:421` (0.9437), `watch/inbox/ASTRA_REAUDIT_V3_20260911.md`, `docs/ref/FRONTIER_PROMPT_V1.md:79`
