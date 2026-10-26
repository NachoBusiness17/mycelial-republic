# Sweep: inference-efficiency via HN - 2026-10-10

source-fetched: 2026-10-10. Doors: HN Algolia `search_by_date` + `search` (OK, no 403s);
news.ycombinator.com item pages (OK); one linked page failed - `http://justine.lol/matmul/`
died with CERT_HAS_EXPIRED on direct fetch, the webReader fallback succeeded and revealed the
URL is a Mar-31-2024 post resubmitted to HN on 2026-10-02 (item 49938916). One docs.z.ai
fetch timed out once, retry succeeded. Pass 1: 6 Algolia queries (vLLM, ollama, llama.cpp,
"speculative decoding", "tokens per second", "inference GPU"), 60+ unique story candidates
considered inside the 30-day window (created_at_i>1788998400). Pass 2: 10 items read end to
end (8 banked below, plus justine.lol/matmul and the nexlab orchestrator survey, both folded
in as supporting evidence rather than banked).

## Banked items (strongest first)

1. **Benchmarking Local LLM Servers: Llama.cpp, Llamafile, LM Studio, and Ollama**
   (blog.mozilla.ai, HN 49742415, 2026-09-17). The only instruments-grade outside benchmark
   of the estate's actual stack. Methodology is a twin of our instruments-only law: 15 runs,
   first discarded as warmup, 2 fastest + 2 slowest dropped, middle 10 averaged, cold server
   restarts, interleaved, 1 SD error bars, TTFT explicitly listed as NOT measured. Steals:
   (a) speculative decoding at Ollama's library default draft=4 makes 27B decode WORSE than
   none (~15 vs 23.4 tok/s) - our janitor fleet runs library defaults, so spec-decoding
   settings are an unaudited lane; (b) build flags and shader toolchains move decode/PP by
   4.3-63% - any tok/s baseline must pin toolchain versions or it is not a baseline;
   (c) all four servers share the llama.cpp core and land within a few percent at fixed
   flags: switching server is not a throughput lever, flags and builds are.

2. **New in Llama.cpp: Decision Models** (huggingface.co/blog/ggml-org, HN 49934323,
   2026-10-02; sibling: Ollama 0.35 supports them, HN 49908997/49906337). Decision models
   read input once and score a fixed option set via `/v1/systemone` (CHOICE/SCORE/NOUL),
   six GGUF models (Julia-1 144M through Clef 27B), median latencies 3-43 ms on one RTX PRO
   6000, router mode serves several per server. This is the strongest outside evidence for
   laws-lens q10 (thinking on/off economics): for routing/moderation/verification micro-
   decisions the thinking-token tax is sidestepped entirely, locally, on the existing
   llama.cpp/ollama runtime. Overlap: estate holds the API class via the remote TypeSafe
   oracle (memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:30, CHOICE/SCORE/
   NOUL and /v1/systemone) - the LOCAL-GGUF runtime with measured latencies is the new part.

3. **Launch HN: Magnitude (YC S25) - self-optimizing inference engine** (HN 49911995,
   2026-09-30, 194 pts, 97 comments; thread read). Claims vs llama.cpp: 92% faster decode on
   M4 Pro, 19% on DGX Spark, 27-28% less per-agent memory via 8-bit-key/4-bit-value KV
   quantization. Thread is the real signal: llama.cpp is a weak baseline on Mac (MLX/Rapid-
   MLX beat Magnitude ~2x on M5 Max), and - decisive for us - a commenter reports hardware
   NOT DETECTED on a Win11 Intel + RTX PRO 1000 laptop. Verdict for the Windows janitor
   fleet: not ready on Windows; the steal is the concept pair (KV-cache quantization +
   per-agent memory accounting), not the engine.

4. **Local LLM Inference at Scale with vLLM** (data4sci.com, HN 50032575 - the ask's anchor,
   2026-10-10). Single DGX Spark (GB10, 128 GB unified, 273 GB/s), Qwen3.5-35B-A3B-FP8:
   34 tok/s single-stream, 284 tok/s at batch 256 (~8x), 2,820 tok/s batched prefill over
   1.35M input tokens in ~8 min; KV cache 28.8 GiB ~ 585k tokens. Verbatim: "vLLM was built
   from the ground up for linux systems" - no Windows path, so vLLM-class serving does not
   transplant to the fleet directly. What DOES transfer: (a) batch amortization is the only
   8x-class lever, and it needs queued work, not single-stream janitor calls; (b) the post's
   thinking example - 854 tokens of which ~520 words deliberation vs ~43 words answer - is
   clean outside evidence for the ~12x answer-overhead shape of thinking-on economics (q10).

5. **Faster prompt lookup drafting in llama.cpp** (jadidbourbaki.github.io, HN 49859982,
   2026-09-26, 89 pts). Pure CPU data-structure work (dense segmented maps, sorted vectors,
   Lemire constmap/binary-fuse filters): drafting up to 42x faster, static-cache load 3.76 s
   to 0.23 s, peak memory down up to 2.6x, acceptance rates unchanged, benchmarked with
   llama-lookup-stats on M4 Pro. Reproducible on a consumer Windows host (CPU-only, model-
   agnostic). CAUTION pairing with item 1: if draft acceptance is low (draft=4 default),
   spec decoding can net NEGATIVE - measure acceptance before adopting.

6. **Mercury 2.5 LLM hits 770 tokens per second** (HN 49823348, 2026-09-23, 151 pts, 92
   comments; thread read). Diffusion LLM, API-side number from artificialanalysis.ai; no
   commenter reproduces anything like it locally (nearest local datapoint in thread: ~100
   tok/s on a Mac Studio, different model). Thread verdict: quality "on par with any 14B
   model at max", speed advantage erodes at batch because diffusion requests share hardware
   poorly. For the instruments-only law this is the canonical regrade case: headline tok/s
   without architecture + serving condition + locality is not a claim we can bank.

7. **GLM-5.3-FlashX docs - "thinking.type only supports enabled; thinking cannot be
   disabled"** (docs.z.ai, HN 49757191, 2026-09-18). Closes an estate debt rather than
   re-firing it: FLASHX_PROBE_20260927.md:44-47 owes a flip condition "if flashx fired with
   reasoning disabled beats flash first-content TTFT by 2x" - the docs now prove that
   configuration cannot exist, so the DECLINED verdict is final and the owed probe is
   dead-on-arrival (a paper closure, no spend). Also restates 200 tok/s with no conditions
   and "not yet available on the plan". Per the ask's guard: EMPTY_REASONING stays terminal,
   and the banked quant A/B tie at ceiling is NOT re-run by anything here.

8. **AI Development on Windows: From PyTorch and Llama.cpp to Windows ML**
   (devblogs.microsoft.com/foundry-on-windows, HN 49997807/50002660, 2026-10-07/08).
   Experimental llama.cpp/GGUF support inside Windows ML: `WinMLServer.exe model.gguf
   --target gpu --port 8080` exposing an OpenAI-compatible /v1 endpoint, engine selection
   automatic, MS contributing CUDA kernels/spec-decoding/multi-GPU upstream. Zero benchmark
   numbers in the post - under the instruments-only law this banks as a watch item only:
   the Windows-native serving door now exists, unmeasured.

## Exclusions and negatives (so nobody re-chases them)

- **justine.lol/matmul (HN 49938916, "LLaMA Now Goes Faster on CPUs")** - 2026-10-02 HN
  resubmission of Mar-2024 content (verified in fetched page text: "Mar 31st, 2024"). The
  84 matmul kernels are long upstreamed into llama.cpp, i.e. already inside the estate's
  ollama stack. Already-absorbed prior art; not banked.
- **nexlab self-hosted orchestrators compared (HN 49778078)** - read end to end; it is a
  desk survey of docs, zero benchmarks run. Useful only as RQ4 evidence: it endorses Ollama
  for one machine ("It is the right answer for a laptop or one desktop") and NO tool in the
  13-tool survey discusses disk/memory footprint - the GB/day question outside surveys do
  not ask.
- Ask-HN threads with 0 comments (50033571 coding-agent speed, 50016644 subscribed-vs-local)
  were considered and skipped: no thread, no signal beyond the question.

## Research-question answers

- **RQ1 (serving advances vs Windows ollama fleet):** Nothing vLLM-class runs on Windows
  (vLLM is Linux-first per item 4; Magnitude's Windows path fails hardware detection per
  item 3). The transferable levers are batch amortization (8x, needs queueing), toolchain/
  build pinning (4-63% swing, item 1), and spec-decoding settings audits (can be negative,
  item 1). Windows ML (item 8) is the future Windows-native door, unmeasured. The banked
  quant A/B tie at ceiling is NOT re-run; any follow-up would be a NEW instrument scoped to
  spec-decoding flags, which is exactly the kind of settings audit item 1 motivates.
- **RQ2 (thinking on/off economics, q10):** Three outside datapoints: FlashX cannot run
  thinking-off at all (item 7 - and our own diagnostic already showed 133/138 tokens were
  reasoning, FLASHX_PROBE_20260927.md:26-28); the data4sci example shows ~12x answer
  overhead in a thinking block (item 4); decision models remove the tax for structured
  micro-decisions entirely (item 2). This is enough to regrade q10's suspect rows toward
  "thinking-off wins on latency lanes; decision-model wins on routing lanes", without
  refiring any burn.
- **RQ3 (instruments-only law):** Surviving locally-reproducible claims: Mozilla's relative
  server parity at fixed flags, spec-decode draft-4 regression, toolchain deltas (item 1);
  prompt-lookup 42x drafting (item 5, CPU, llama-lookup-stats instrument). Non-surviving:
  Mercury 770 tok/s (API, diffusion, quality-capped, item 6), FlashX 200 tok/s (no
  conditions stated, item 7).
- **RQ4 (standing-wave GB/day):** Serving adds three growth classes the ledger must see:
  KV cache (28.8 GiB ~ 585k tokens on one box, item 4), n-gram static caches sized by
  corpus (0-541 MB in item 5's benchmarks), and model-weight churn. The existing law shape
  absorbs them WITHOUT a new budget class IF each serving artifact registers as a declared
  burn (RIB_STANDING_WAVE_BUDGET_20261009.md:16 law 1 tokens-are-disk, :23 law 3 burns-
  declare-exhaust); the exhaust declaration should gain a cache-artifact kind. Smith's DISK
  ETA alert class needs no change - weights+cache are ordinary GB/day rows once declared.
  EMPTY_REASONING remains terminal per RIB_INFERENCE_BUDGET_20261001.md:54-62; nothing here
  refires it.

## Estate hooks

Feeds RIB_INFERENCE_BUDGET_20261001 (spec-decoding settings audit as a follow-on
instrument), RIB_STANDING_WAVE_BUDGET_20261009 (cache-artifact exhaust kind), the hermes
burn bank and 247 driver log (batch amortization only matters if lanes queue), smith DISK
ETA (no change), driving ladder local rung (decision models as the new local micro-rung).
