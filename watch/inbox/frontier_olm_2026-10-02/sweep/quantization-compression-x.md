# Sweep: quantization-compression via X (frontier_olm_2026-10-02)

source-fetched: 2026-10-02. ASCII only, no em or en dashes. Every quote below came
from a page or API response fetched this sitting. Sweep gopher seat
(sweep-quantization-compression-x), one ask: two passes, bank only items read here.

## Doors used and their condition

- X door: WebSearch with site:x.com queries (11 queries run). Two mid-sweep 429/1302
  rate-limit bursts hit and self-recovered; no query was lost. Matches the estate's own
  fan-out envelope law receipts.
- fxtwitter door: https://api.fxtwitter.com/<user>/status/<id> resolved every single
  status cleanly (code 200, verbatim text + created_at + likes). X long-form article
  BODIES (x.com/i/article/...) are NOT retrievable through it: RampLabs article
  2104601238738210816 and The Inference Gap 2101034933284417614 both degraded to their
  tweet shells. Per recipe, no fallback success is fabricated.
- Non-X primaries reached and read end to end: labs.ramp.com/research/latent-briefing-kv-cache
  (WebFetch) and huggingface.co/blog/transformers-llama-cpp-quants (WebFetch).

## Estate grounding and dedupe (done this sitting, exact greps)

- Prior same-area sweeps read or outlined: 09-30 quantization-compression-x.md
  (outline: 8 banked incl. JakeKAllDay 2095646450138874095 and the arXiv cliff papers),
  10-01 open-local-language-models-x.md (banked the HF blog four ways), and this fold's
  sibling kv-cache-context-engineering-x.md (banked _avichawla's article
  2096491130489872479 and RampLabs article 2042660310851449223, the April one).
- Overlap baseline from memory/percolator/candidates.jsonl:15-16: the estate already
  holds the Qwen3.8-27B quant-floor evidence (quesma benchmark + arXiv 2609.32042,
  3-bit/2-bit cliff, Q2_K ban for tool roles). Those are held anchors, NOT re-banked.
- Distinctive-phrase greps run against catalog/catalog.jsonl (871,790 rows),
  watch/inbox/, and memory/percolator: "42 Different Outcomes", "12 KV cache
  reduction", "openai endpoint in a single command", "20K+ prompts", "Event-Centric
  Multimodal Memory", "reducing KV cache size by 80", "small piece of the attention
  equation" all returned zero. "run-to-run standard deviation" hits only
  watch/inbox/frontier_olm_20260928/sweep/_raw/q_d_openweight.xml, a raw discovery XML,
  not a banked write-up. "transformers-llama-cpp-quants" hits the 10-01 percolator row
  (already held). "KVzip" hits only the sibling reddit sweep line 37 as bare post IDs.

## Answers to the four research questions

### RQ1. Agentic/task-metric quantization results post-2026-10-01 vs the three banked laws

The three laws (never below 3 bits for agentic work, Q2_K never, perplexity alone never
gates) SURVIVE this sweep: no in-window X item reports an agentic win below 3 bits, and
no item gates a quant on perplexity. The new datum is bnjmn_marie (Sep 14): at 4-bit,
single-run agentic scores are NOT stable instruments. Same harness, same model: AWQ run
1 scored 38.94 vs run 2 at 31.86 on DeepSWE 1.1, with 32 of 113 task outcomes flipped;
NVFP4 posted the identical 31.86 aggregate with 42 of 113 outcomes flipped and only 15
of 36 solved tasks in common; BF16 anchor 43.36. That does not overturn the 3-bit
floor, it adds a variance floor ON TOP: any single-run agentic cell in the model
garden grid measured within roughly 7 points of a neighbor is one sample, not a
ranking. Oluwaphilemon1 (Sep 10) adds a second instrument requirement: concurrency
gating (a quant that holds single-stream can collapse under parallel load). Q2_K
specifically: nothing new in-window on X; the estate's quesma/2609.32042 evidence base
remains the law's support.

### RQ2. Joint weight+KV quantization and the bytes-per-token math

No in-window item does joint weight+KV quantization. What the frontier actually shipped
is KV-token COMPRESSION at the representation level: RampLabs (Sep 28) scaled KVzip +
Attention Matching to GLM 5.3, 80 percent KV cache reduction retaining over 90 percent
of full-context accuracy on QuALITY. That attacks the same bytes-per-token budget the
estate's llama.cpp --cache-type-k/v flags attack, but by eviction rather than by
bit-width, and it is evaluated on long-context accuracy, not agentic tool work. The
labs.ramp.com background writeup (April, Qwen3-14B, read end to end) confirms the
mechanism is attention-scored token eviction with a shared per-layer mask, not
quantization. For the llama.cpp/Ollama serving stack the practical read stands: KV
bit-width flags remain the estate-side lever; eviction-style compaction exists upstream
but is not served by any GGUF artifact.

### RQ3. One artifact across llama.cpp + Ollama + vLLM now transformers runs GGUF natively

The estate already holds the HF blog (banked 2026-10-01 four ways). New fragmentation
evidence from this sweep: the Sep 22 announcement itself is narrow (Qwen3.5/Qwen3.8
architectures only, packed kernels MPS-only, everything else falls back to
dequantization), and the practitioner stack still splits the artifact by engine:
sudoingX (Sep 23) runs llama.cpp for one card and vLLM for multi-card in the same
stack. vLLM still does not serve GGUF as a first-class artifact. Verdict: GGUF is now
one artifact for llama.cpp + Ollama + transformers (on Apple Silicon, Qwen-family
first), and the re-quantization wall that remains is vLLM and non-Qwen architectures.

### RQ4. Agent memory estate compression as a first-class problem

No in-window item compresses a text behavior-row estate (hundreds of thousands of
rows) the way the estate holds its biography mass. Closest in-window: EM2Mem (Sep 3,
zxlzr/ZJU) makes long-horizon agent memory a first-class ORGANIZATION problem, binding
heterogeneous evidence into event-anchored memory cells with an episodic graph plus a
semantic graph, but it targets multimodal video/audio streams, not filed text rows.
Out-of-window but directly on-point for a future fold: MemTrapBench/AdaptiveMem
(Aug 21, same author, huggingface.co/papers/2608.20202) shows correct, relevant memory
can DEGRADE a model by 10+ points, a caution the estate's own corpus-weighted recall
should carry. Neither is claimed as in-window bank evidence.

## Deep reads this sitting (8 fetches, every quote from these)

1. api.fxtwitter.com/bnjmn_marie/status/2099579957207048696 (full text, created_at
   2026-09-14T19:24:04Z, 161 likes)
2. api.fxtwitter.com/Oluwaphilemon1/status/2097901400797651334 (full text, 2026-09-10)
3. api.fxtwitter.com/RampLabs/status/2104636107174334612 (full text, 2026-09-28) +
   api.fxtwitter.com/samzliu/status/2104655203563913364 (commentary, 2026-09-28)
4. labs.ramp.com/research/latent-briefing-kv-cache (WebFetch, end to end; April 10 2026
   background for item 3)
5. api.fxtwitter.com/sudoingX/status/2102548750996582762 (full text, 2026-09-23)
6. api.fxtwitter.com/zxlzr/status/2095315379136708857 (full text, 2026-09-03)
7. api.fxtwitter.com/techNmak/status/2103488645642793165 (full text, 2026-09-25)
8. huggingface.co/blog/transformers-llama-cpp-quants (WebFetch, end to end; HELD anchor
   from 2026-10-01, used for RQ3, not re-banked)

## Pass-1 candidate ledger (considered this sitting, 40+ surfaced; snowflake/fxtwitter dates)

IN window and banked above: bnjmn_marie (Sep 14), RampLabs (Sep 28) + samzliu (Sep 28),
sudoingX (Sep 23), Oluwaphilemon1 (Sep 10), zxlzr EM2Mem (Sep 3), techNmak (Sep 25).
IN window, ceded to sibling sweeps: _avichawla Sep 11 thread 2098314413128446113 (the
sibling kv-cache-context-engineering-x.md already holds the same author's article
2096491130489872479 with the same 12-technique material), HF blog (held, 10-01).
IN window, article-body unresolvable, not banked: RampLabs article shell
2104601238738210816, The Inference Gap 2101034933284417614, vicky_grok Sep 11 (article
link only), QuantumindSSI field guide (Jul 6, out), Naveen Saradhi 2-bit/AA mention
(profile-level, no status ID to resolve).
Considered and OUT of the 30-day window (verified by fxtwitter created_at or snowflake
decode, none banked): outsource_ Qwen3.8 UNLEASHED (Aug 29), Akashi203 lossless
inference (Aug 3), danielhanchen Inkling 1-bit 74.2 percent (Jul 15), zxlzr
AdaptiveMem/MemTrapBench (Aug 21), cedricclyburn FP8 vs FP16 (Aug 3), analogalok KV
quant flags (Jul 12), Unsloth TurboQuant wave (Mar), mem0ai ICLR memory digest
(Apr 24), AlphaSignalAI ToolCall-15 (Apr), TeksEdge vLLM no-GGUF (Apr 29), Mayhem
GGUF explainer (Aug), GeekyDamian phone GGUF (Aug 25), TheValueist KV math (Dec 2025),
Andrew Ng serving course (Jun), beamnxw context vs memory (Aug), TheZvi Astra (off
topic), mztacat GLM-5.2 (Jun), hrswatigupta memory types (Sep 27, in window but
promo-weighted educational, below the bank line), Brian Roemmele KIMI K3 quant (Aug),
0xSero GLM at home (Jul).

## Honesty block

- Every quote in the banked items is verbatim from the fetched JSON or page listed
  under deep reads. The RampLabs item is banked on its status text (read in full); the
  X article BODY behind it was not retrievable, and the numbers cited (80 percent,
  over 90 percent, QuALITY, GLM 5.3) are exactly the status text's own numbers.
- No check of estate serving binaries was run; this is a public-source sweep only.
- The web_search backend's intermittent 429/1302 bursts were observed twice and
  recovered; no candidate list was truncated by them that I can detect.
