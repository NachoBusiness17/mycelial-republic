# Sweep: quantization-compression via X - 2026-10-01

Lane: quantization-compression-x (frontier olm daily). Window: 2026-09-01 .. 2026-10-01.
Doors: WebSearch (site:x.com queries) for pass 1; fxtwitter JSON door (`https://api.fxtwitter.com/<user>/status/<id>`) for pass 2. All quotes below are verbatim from fetched fxtwitter JSON (cached under `sweep/_fx/*.json` in this directory as receipts).

## Doors, honestly

- fxtwitter resolves single status posts clean (full text, date, metrics). It 404s on EVERY X long-form article path: tested `i/article/2102796817201029123`, `i/article/2096546474255372288`, `i/article/2095646450138874095`, and the `_avichawla/article/2096491130489872479` variant, all HTTP 404 (verified with `curl -o /dev/null -w "%{http_code}"`). Three of the strongest leads (a KLD-reading essay, a GLM-5.3-Flash prune log, a 240K-context llama.cpp build guide) point INTO articles that cannot be read through this door. Per recipe those bank as resolved tweet text + search snippet with the degradation named, never as an article read.
- WebSearch hit 1302/429 rate limits twice mid-run (the Q4-vs-Q8 query and one distillation query); both were retried with reworded queries and succeeded on retry. No search result was invented from a failed call.
- One fetch-loop bug of my own: fxtwitter needs the `/status/` path segment; a first batch without it 404'd wholesale and was rerun correctly. The 404s were the URL shape, not door degradation, and are not reported as such.

## Pass 1 - candidates (broad)

~55 candidate posts surfaced from 9 WebSearch queries (GGUF k-quants, AWQ/GPTQ/EXL2/EXL3, Q4-vs-Q8, KV-cache quantization 2026, KV eviction, attention sinks, distillation x2, September quant news, bartowski/KLD). Date triage via snowflake IDs plus fxtwitter `created_at` on every post I resolved: only a minority of search hits are inside the 30-day window. The strongest measured material on these exact research questions clusters 2026-08-15..08-26 (just outside window); the strongest in-window material is 2026-09-06..09-24. Both are banked below with true dates; window status is marked per item.

## Pass 2 - deep reads (14 posts fetched end to end)

superalesha bake-off root + result (08-20), superalesha GLM-5.3 Flash (09-07), outsource_ Qwen3.8-27B home runbook (08-15), TeksEdge Xing4.0 (09-17), TeksEdge MiniCPM5-2B (09-07), TeksEdge Qwen3.8-27B game build (09-06), 0x0SojalSec (08-21), Oluwaphilemon1 (08-26), Mayhem4Markets DeepSeek-V4.1 KV (09-10), Mayhem4Markets EXL3 (07-29), BrandonMusicKy KLD (09-24), _avichawla article pin (09-06). Estate pre-reads for overlap: `corpus/library/lmcache-src/docs/design/v1/distributed/serde/turboquant.md` (LMCache TurboQuant is a storage-layer serde for KV tensors at L2, NOT the Google TurboQuant KV algorithm the May feeds hype: different components, so Google-side KV quant news is not a duplicate) and `memory/research_polished/kv_cache_compaction.md` (estate already holds the H2O/SnapKV/StreamingLLM eviction line and prefix-cache economics).

## Answers sketch (per research question)

1. **Best quality-per-byte format on llama.cpp/Ollama:** the only full-format bake-off found (superalesha, 08-20, 5 production stacks, 40 arms, 2.5 days) put AWQ INT4 90.0 / NVFP4 89.3 / GGUF Q4_K_M 89.3 / FP8 88.7 / NInfer 88.0 pass@1, McNemar a statistical tie, and concluded the gap between quants is smaller than the gap between reasoning presets. GGUF Q4_K_M on llama.cpp tied the best vLLM stack: the janitor seats lose nothing measurable at Q4_K_M. Bartowski/ubergarm PPL-KLD tables remain the per-model reference (profile-level only this window; the specific post did not resolve).
2. **Measured Q4 vs Q8 delta with conditions:** outsource_ (08-15, M2 Max 96GB + RTX 4090 24GB, BF16 reference) measured best Q4 at 14/22 on their extended quality suite vs 15/22 for Q5, with better speed and context headroom; the superalesha run found Q4 vs FP8 inside noise at xhigh reasoning (3 tasks of 150). Both state hardware, engine, and task mix. Nothing supported the folklore that Q4 costs quality worth paying Q8 memory for on 27B-class; the honest conditions are "measured on 27B at reasoning presets xhigh/medium", not yet on the estate's 2B janitors (open follow-up: rerun the suite shape on gemma:2b / MiniCPM5-2B).
3. **KV-cache / context compression for a local harness:** TeksEdge's 09-06 build already banked yesterday by the inference-efficiency lane (Q3_K_XL + MTP + compressed KV in 16GB at 96K context, "do not fear aggressive KV quant vs CPU offload"). New this window: DeepSeek-V4.1 Flash doing QAT directly on the KV cache (May 09-10 post; the paper line is already in `memory/runs/corpus_gap_research/ARXIV_REGISTER.json`, so only the adoption signal is new), and the KLD-reading essay lead (unreadable article, OWED). Google's TurboQuant KV algorithm (6x memory, up to 8x speedup claims riding the May feeds) is distinct from our LMCache TurboQuant serde and is NOT yet registered estate-side: candidate for ARXIV_REGISTER.
4. **Frontier distill recipes reproducible without datacenter:** Qwen3.8-2B-Distill (from a 2.4T teacher's reasoning traces, full-parameter SFT, same curriculum as the 4B/9B, Q4_K_M ~1.3GB, MMLU CoT 28.3 to 54.8, GSM8K 33 to 64) is the frontier-published recipe shape, and it exactly fills the gap today's sibling reddit lane registered ("frontier-lab-official distillation recipes did NOT surface as readable reddit threads"). MiniCPM5-2B ships its training data + a speculative-decode model: the trace-derived-dataset + failure-bucket-eval recipe maps 1:1 onto the estate's seat tapes (code-agent-data skill).

## Overlap ledger (greps run 2026-10-01)

14 distinctive-phrase greps over `catalog/catalog.jsonl` + `memory/` + `watch/inbox/` + `corpus/steal/`. Findings: Xing4.0-29B-A4B model is already held via r/LocalLLaMA pulls in the 09-28 and 09-30 sweeps (`watch/inbox/frontier_olm_20260928/sweep/_raw/pull2_LocalLLaMA_multi-agent.json`, `watch/inbox/frontier_olm_2026-09-30/sweep/_raw/p30_seen.json`); the TeksEdge Q3_K_XL game post is already banked in `watch/inbox/frontier_olm_2026-09-30/sweep/inference-efficiency-x.md` (line 26) so it is NOT re-banked here; superalesha's GitHub 4x3090 benchmarks repo is held by yesterday's lane but his bake-off posts are not (post IDs grep 0); MiniCPM5 exists as a name-only mention in an OWED link batch (`memory/runs/mickey17/digest_inbox_09.jsonl`), benchmark bytes new; DeepSeek-V4.1-Flash KV is in ARXIV_REGISTER so its hype post is not banked; NInfer (45 catalog hits) and NVFP4 are known estate terms. Contamination caveat: `memory/trajectory/steps.jsonl` matches several phrases only because it is THIS session's own trajectory log (mtime 2026-10-01T15:16Z); those hits are not prior knowledge. Kvarn/beellama also appear in today's sibling lane `quantization-compression-reddit.md` (parallel lane, different door, complementary items).

## Banked items (strongest first)

1. superalesha 08-20 bake-off result (OUT of window by 12 days, strongest measurement found; conditions complete: 5 stacks, 150 agentic/coding + 90 reasoning tasks, 4 reasoning modes, 40 arms).
2. outsource_ 08-15 Qwen3.8-27B home runbook (OUT of window by 17 days; Q4 14/22 vs Q5 15/22 vs BF16, KV Full/Q8/Q4/FP8 variants, MTP depth sweep, 262K context decay measured).
3. TeksEdge 09-17 Xing4.0-29B-A4B (IN window; IQ4_NL ~19GiB on one 24GB card, llama.cpp PR 151.7 tok/s gen with hardware honestly unattributed).
4. Oluwaphilemon1 08-26 Qwen3.8-2B-Distill recipe (OUT of window by 6 days; fills the reddit lane's frontier-distill gap).
5. TeksEdge 09-07 MiniCPM5-2B (IN window; 1.56GB Q4_K_M at 9B-tier AA index; janitor-class).
6. superalesha 09-07 GLM-5.3 Flash prune verdict (IN window; "ran, did not trust it with real work", linked article unreadable through the door: degraded).
7. 0x0SojalSec 08-21 Qwen3.8-2B-Distill numbers (OUT of window by 11 days; the MMLU/GSM8K deltas).
8. BrandonMusicKy 09-24 KLD-nats reading essay pointer (IN window; tweet resolved, essay 404s through the door: degraded, OWED read via another door).

Dropped on overlap: TeksEdge Q3_K_XL game post (yesterday's X lane), Mayhem DeepSeek-V4.1 KV post (ARXIV_REGISTER), avichawla KV-engineering article (unresolvable pin-to-pin link, zero readable content), Mayhem EXL3 (July 29, thin).

Raw receipts: `sweep/_fx/*.json` (fetched post JSON, this directory).
