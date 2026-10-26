# SWEEP: quantization-and-compression via X (2026-10-03)

Seat: sweep gopher, area quantization-and-compression-x. Window: 2026-09-03 to 2026-10-03 (30 days).
Feeds: percolator auto_quantize invariants (memory/percolator/invariants.json, existence-checked this session),
deliberate-ask quantize-target field, model-garden inference-budget tests (tests/test_inference_budget.py, existence-checked).

## Doors used and their condition

- fxtwitter door (https://api.fxtwitter.com/<user>/status/<id>): WORKED, zero 403s. 6 X posts resolved to full text.
- site:x.com WebSearch: degraded. The index surfaces x.com posts but truncates the link to bare "https://x.com" with no status ID,
  so most X hits could not be resolved to fxtwitter. Workaround: harvested real status URLs from AINews aggregator pages
  (news.smol.ai issues + latent.space issues) which cite the original posts, then resolved those through fxtwitter.
- news.smol.ai: readable via curl; its /issues/ index ends at 26-09-10, so late-September discovery rode the
  latent.space sitemap instead. Reddit: HARD BLOCKED on every door tried (curl UA, WebFetch, web_reader, old.reddit .json).
  Reddit-sourced items below are banked with the AINews page URL I actually read, Reddit thread named in the note.

## Pass 1 pool (considered, 30+)

In-window kept: llamAmpere v0.4 README + KV doc; stochasticchasm 2098154481750020375; nrehiew_ 2098170450526543892,
2098170409686647263, 2098170443660402942; ArtificialAnlys 2098148674203488422; vllm_project 2097397769338282222;
latent.space reality-checks (2026-09-17), deepseek-v41-flash (2026-09-12), aef-1 (2026-09-15); smol.ai issues
26-09-08 (TAK task-aware quant), 26-09-09 (MLX mixed 4/8-bit + 8-bit KV), 26-09-10 (V4.1 Flash 890 B/token, MXFP4 vLLM Radiance build).
Considered and rejected as OUT OF WINDOW: latent.space "10% worse 100x cheaper" Qwen3.8-27B Q4_K_S agency issue
(datePublished 2026-08-22, read anyway for context), Unsloth Dynamic V3 accuracy claims (Aug 19 smol issue), Together AI KV
compression (Jun 2), Bonsai 27B 1.7-bit tool-calling coverage (Jul), Dynamic Mixed-Precision Routing arxiv (May), Qwen3.8-Flash
KV-to-BF16 stability reports (Aug 24). Considered, URL UNRESOLVED (OWED, never asserted): SPHQuant extreme low-bit weight
quantization (search gave Sep 21, 2026 date and bare arxiv.org link only; arxiv API query returned empty); pinggy.io Sep 8
"do not go below 4-bit" hardware guide (slug guesses 404, not indexed); the "How to hit 262K context and 95+ TPS with
Qwen3.8-27B" x.com post (Sep 3, search snippet only, no status ID; its content was independently captured by reading the
llamAmpere README it announces).

## Pass 2 deep reads (end to end, 10)

1. llamAmpere v0.4 README (raw.githubusercontent.com/JakeATX/llamAmpere/v0.4 = main README, 20,174 bytes) + docs/KV-cache-quantization.md (5,176 bytes).
2. fxtwitter full text: stochasticchasm/status/2098154481750020375.
3. fxtwitter full text: nrehiew_/status/2098170450526543892.
4. fxtwitter full text: nrehiew_/status/2098170409686647263.
5. fxtwitter full text: nrehiew_/status/2098170443660402942.
6. fxtwitter full text: ArtificialAnlys/status/2098148674203488422.
7. fxtwitter full text: vllm_project/status/2097397769338282222.
8. latent.space/p/ainews-reality-checks-on-ai-news (Voodoo + FP8/Q4 sections).
9. latent.space/p/ainews-deepseek-v41-flash-763b-p8b (NVFP4 + KV sections).
10. news.smol.ai/issues/26-09-08 + 26-09-09 + 26-09-10 (TAK, MLX mixed quant, KV passages).

## Answers to the four research questions

### RQ1: 2-4 bit quality retention on 2-8B models, agentic tasks not perplexity

The estate's exact size class (2-8B) is under-covered by what surfaced; the loud 2026 evidence is at 27B (Qwen3.8-27B as the
local-agent workhorse) and the finding shape is consistent: Q4 retains tool-calling when the model is QAT'd or dynamic-quantized,
but base PTQ at Q4 measurably worsens loop/tool-call stability, and FP8/Q8 is the stability floor for long agentic sessions.
Evidence read this session: latent.space reality-checks (2026-09-17) carries a user report of "several million tokens" on
Qwen3.8 27B at FP8 up to ~262k context with "no issues with tool calls" and the claim that "Q4 quantization likely worsens
looping"; Voodoo Dynamic Quant (same page) is a per-tensor gate optimizer against KLD, competitive at aggressive low-size
levels while Unsloth Dynamic 3.0 stays better at mid/high levels. TAK (smol 26-09-08) claims 99% of BF16 reasoning
performance at 15% of size on a 27B using a task-specific imatrix, i.e. retention is being bought by specialization.
For OUR 2-8B lanes: no paper surfaced that directly measures 2-8B agentic retention; nearest datapoints are the llamAmpere
EXL3 curve (82 tok/s at 4.0 bpw, parity 81-82 tok/s down to 3.0 bpw = speed flat but that is a throughput not quality claim)
and the already-banked Bonsai-2 ternary 98.2% retention at 1.72 bpw (memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md).
OWED: a dedicated 2-8B agentic eval of low-bit quants; nothing bankable surfaced in-window.

### RQ2: formats/tooling best supported on consumer Windows hardware, measured tok/s and memory

llamAmpere v0.4 is the strongest measured source found: one RTX 3090/3090 Ti (24 GB), Qwen3.8-27B, GGUF with GGUF-native
EXL3 types (SM86 kernel), MTP drafter on by default, 104.28 tok/s ship-corpus decode, 262,144-token context under a 23 GB cap,
67.8 tok/s after a 250,000-token prompt. Build states "Needs Linux" for v0.4; Windows support is not claimed in what I read,
so treat it as CUDA-consumer not Windows-native. Format ranking implied by the read: GGUF is the universal interchange
(every item in the pool ships GGUF first), EXL3 now rides GGUF-native types in forks, MLX mixed 4/8-bit is the Apple lane
(ddalcu pack: dense 8-bit, experts 4-bit, 8-bit KV, 1M ctx, ~117 GB peak, 40 tok/s prose / 75 tok/s coding on M5 Max 128GB),
MXFP4 has a vLLM build (codeberg ggz14/radiance-vllm-mxfp4, claimed faster than Q8 for the 27B, feasibility-disputed in comments).
AWQ/GPTQ: nothing new surfaced in-window; the pool has moved to GGUF/EXL3/MLX/MXFP4/NVFP4 vocabulary.

### RQ3: is KV quantization co-designed with weight quantization in shipped stacks, and the joint cost?

YES, twice over, at opposite ends of the market. (a) Frontier: DeepSeek V4.1 Flash ships KV compression as architecture
(nrehiew_: "890 bytes/token KV size for these benchmark score is just nuts"; estate LANE4 already banked the 1/8-of-V4-Flash
footprint), and stochasticchasm's read of the tech report is "QAT for the kv cache as well. no wonder it performs better than
other models at fp4 kv cache" - i.e. the KV cache is quantization-aware TRAINED, not post-hoc quantized, and that is offered as
the mechanism for FP4-KV quality. (b) Consumer: llamAmpere v0.4 ships turbo KV types (turbo2-turbo6, 2.125-6.125 bits/value,
Walsh-Hadamard rotation, layer-adaptive and GQA-aware asymmetric defaults, MTP drafter cache follows the trunk types by default)
with measured joint cost: turbo5/turbo4 at 9.25 bits/K+V element shows KL 0.00155-0.00241 vs f16-close 0.00362-0.00455, and on
GPQA + LiveCodeBench (2,400 answers) neither turbo5/turbo4 (+1.2 [-2.6,+5.2]) nor q8_0/turbo3 (-1.0 [-4.8,+2.8]) differs from
q8_0/q8_0 at 95% confidence, with ZERO measured speed cost (85.8 vs 85.9 tok/s). Same doc warns the coupling is model-sensitive:
GPT-OSS attention sinks make even q8_0 K change the output distribution; f16 K mandated there, and short fluent samples are
declared an insufficient quality check (use KL divergence). That warning is directly load-bearing for our constrained-logprob
scorer lanes (the same caveat the Bonsai digest ruled on).

### RQ4: does quantization move free-lane token economics enough to shift the cheap-first threshold?

The frontier moved the curve with ARCHITECTURE, not quantization: ArtificialAnlys on V4.1 Flash (552B-A5x/16B active causal
encoder-decoder): "it outperforms the Pro (1.6T) model while costing ~4x less per token". Estate lanes already live on that
curve (watch/inbox/last_mile_20260930/V3_DEEPSEEK_TEST.md banks V4.1 Flash as bulk workhorse; G4_7 cost deep-dive 2026-09-10).
The 890-bytes/token KV plus persistent-KV-across-checkpoints (nrehiew_ RL-infra post) is what makes long agentic sessions cheap
server-side; locally, quantization's economics showed up as context-per-VRAM (262K under 23 GB; 1M-token MLX at ~117 GB) rather
than tok/s-per-dollar. Verdict for the spend laws: cheap-first threshold is NOT moved by quantization this month; it is moved by
frontier serving economics already in the ribs. The quantization lever that IS actionable: the llamAmpere KV result says we can
quantize KV on our local 27B/9B lanes to near-zero quality cost IF we validate with KL divergence per model, which directly
extends the inference-budget tests and the auto_quantize invariants (KV-aware) rather than the spend laws.

## Overlap ledger (grep evidence)

- catalog/catalog.jsonl: llamAmpere 0 hits; Voodoo 0; mlx-serve 0; nrehiew_/stochasticchasm 0; "task-aware quant" 0;
  HiSparse 0. TurboQuant 15 hits (LMCache serde corpus, corpus/library/lmcache-src/.../turboquant/, mtime 2026-09-22;
  same quantization lineage as llamAmpere's llama.cpp TurboQuant types, different layer: serde vs KV cache).
  Bonsai: already verified estate-side, memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md
  (98.2% retention at 1.72 bpw, fork-only loader, logprob-calibration caveat). The llamAmpere item ADDS: MTP-drafted
  throughput (105 tok/s at 2.125 bpw) and the turbo KV family, not the Bonsai quality claim.
  "V4.1 Flash" 4 hits (watch/inbox/mickey/G4_7_cost_analysis.md, v41_paces LANE3+LANE4, last_mile_20260930/V3_DEEPSEEK_TEST.md):
  cost/speed/cache-ratio already banked; the QAT-for-KV hypothesis and the 890-bytes/token figure were NOT found in estate files
  (grep for "890 bytes|QAT.*KV|FP4 KV" over watch/inbox + memory matched only unrelated files).

## Honest gaps

- No 2026 paper measuring 2-8B agentic retention was bankable in-window (OWED above).
- Reddit r/LocalLLaMA / r/LocalLLM threads (30-day UD-Q4_K_XL field test with 845.1 tok/s PP / 73.8 tok/s gen / MTP
  acceptance 0.481; Voodoo announcement; TAK post) could not be read directly: reddit blocked curl, WebFetch, web_reader
  and old.reddit. Their numbers above are quoted from the AINews pages that summarized them, and are labeled as such.
- pinggy.io and SPHQuant URLs unresolved (details in Pass 1 pool).
- MLPerf Inference v6.1 (Sep 16, StorageReview: first agentic inference workload, GGUF under llama.cpp in the reference)
  was considered; not deep-read, not banked.
