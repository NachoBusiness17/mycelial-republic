# frontier sweep: open-local-language-models via arxiv

source-fetched: 2026-10-01
Area: open-local-language-models via arxiv. Seat: sweep gopher, Mag Resource Harness.
Feeds the local janitor seats (gemma:2b scut, gemma4 short worker) and the driving ladder's
sensing-versus-judgment split with a replacement-or-keep verdict for the bottom rung, plus the
C1 censorship program's E1-E3 experiment design (assembled in descent window 1,
`watch/inbox/hermes_burn/`, lens `watch/inbox/frontier_olm_2026-10-01/lens/burns.md:44`).

## Doors used and degradations (honest ledger)

- Door 1, arXiv export API: 6 WebFetch queries (recipe per
  `watch/inbox/frontier_olm_2026-10-01/lens/doors.md:20-28`, re-verified live by the lens seat
  today), all Atom XML parsed, all sorted submittedDate descending:
  `cat:cs.CL AND all:"refusal"` (25 entries, totalResults 766), `all:"GGUF"` (20, totalResults 49),
  `all:"llama.cpp" OR all:"Ollama" OR all:"vLLM" OR all:"MLX"` (25, totalResults 797),
  `ti:"Qwen" OR ti:"Gemma" OR ti:"Mistral" OR ti:"DeepSeek" OR ti:"Phi"` (22, totalResults 1163),
  `cat:cs.CL AND (on-device OR edge OR small language model)` (20, totalResults 3471), plus one
  `id_list` batch fetch of 5 papers by curl for verbatim abstracts.
- Door 2, HN Algolia search_by_date, window created_at_i>1785542400 (2026-08-01, the 60-day
  window): queries `ollama` (30 of 136 hits), `"llama.cpp"` (30 of 41), `gguf` (30 of 36), `qwen`
  (30 of 485), `gemma` (30 of 248), `refusal` (20 of 121). One query DEGRADED: `"open weights" OR
  "open-weight"` returned nbHits 0, Algolia does not honor that OR syntax; per the recipe I fell
  back to per-keyword queries rather than claiming the OR query worked.
- Degradation 2: the MCP web reader returned a 1302 rate-limit error on one fetch
  (arxiv.org/abs/2609.18526); fallback was WebFetch for that page plus curl of the arXiv API
  `id_list` endpoint and raw HF page HTML, which is also how every banked verbatim quote below was
  secured byte-exactly (WebFetch's extraction model declines full verbatim reproduction, so quotes
  were re-pulled from raw XML/HTML rather than trusted to the extractor).
- No door 403'd. The reddit door was not attempted (closed with root cause verified at
  `watch/inbox/frontier_olm_2026-10-01/lens/doors.md:40-47`).

## Pass 1, broad sweep

Pool: ~137 arXiv entry lines across 5 API queries (published 2026-09-14..2026-09-30) plus ~170 HN
hit lines across 6 date-filtered queries (2026-08-19..2026-10-01). Unique candidates after
dedupe exceed 150; the 30-item floor is passed roughly five times over. Adjudicated list
(id | date | verdict), where "known" = hit in the overlap grep described below:

1. 2609.31678 | 09-16 | BANK: soft refusals under KV compression, RQ2 core
2. 2609.25447 | 09-21 | BANK: 60-model pressure/fold measurement, RQ2
3. 2609.18526 | 09-16 | BANK: local-LLM serving confidentiality failures, RQ3 janitor-host angle
4. Ternary-Bonsai-8B-gguf | HN 09-20 | BANK: 8B Apache-2.0 ternary GGUF, RQ1/RQ4 (family known)
5. HF blog transformers-GGUF | blog ~04-24, HN 09-22/23 | BANK: runtime boundary, RQ2/RQ3
6. Ollama Jev decision models | 09-29 | BANK: Ollama 0.35 stack change, RQ3/RQ1
7. Dynamic Abliteration blog | 09-24 | BANK: non-destructive refusal suppression, RQ2, estate-new
8. Mozilla 4-server benchmark | 09-17 | BANK (prose-depth): configuration beats engine, RQ3
9. 2609.05881 Broken on Arrival | 09-05 | drop-as-rebank: deep-read by the 09-30 quant sweep
10. 2609.35465 Tetra | 09-28 | drop-as-rebank: full-HTML read by the 09-28 inference-eff sweep
11. Ollaya (HN 49848269) | 09-25 | drop-as-rebank: deep-banked by the 09-30 inference-eff sweep
12. Gerganov on Nvidia-HF (HN 49567357) | 09-04 | hold: read this ask, listed by 09-28 quant sweep
13. 2609.39358 Galahad | 09-30 | hold: 09-30 submission, unread this ask, kv-area flavored
14. 2609.38981 Vosti | 09-30 | hold: 09-30 submission, unread this ask
15. 2609.38706 provenance-blind KV reuse | 09-30 | hold: unread, kv-area
16. 2609.37916 RLX Rust multi-backend | 09-29 | hold: unread; ingests GGUF, compares MLX
17. 2609.29757 OllamaDrama honeypot | 09-24 | hold: unread; Ollama-API attack surface
18. 2609.26333 Disaggregated Quantization | 09-22 | hold: unread; llama.cpp+vLLM validated
19. 2609.32042 Polish agentic quant thresholds | 09-25 | hold: 3-bit/2-bit collapse point
20. 2609.14864 GGUF-metadata throughput prediction | 09-14 | hold: constants do not transfer
21. 2609.25014 quantizer choice = PII leakage | 08-02 | hold: GGUF Q4_K_M leaks more than AWQ
22. 2609.19989 China AIGC compliance benchmark | 09-17 | hold: 2,303-question censorship audit
23. 2609.23039 political alignment audit | 09-19 | hold: preregistered, unread this ask
24. 2609.35544 sycophancy vs refusal | 09-28 | hold: Qwen3.5 SAE injection, unread
25. 2609.25518 Matryoshka attribution | 09-22 | hold: 1% weights restore removes refusals
26. 2609.39223 QATFactory | 09-30 | hold: exports Q4_K to llama.cpp, unread
27. 2609.33927 Phi-2 QLoRA | 09-27 | drop: already held by 09-30 olm sweep (#11)
28. 2609.30716 Gemma 4 behavioral eval | 09-25 | drop: banked by 09-30 olm sweep (#6)
29. Qwen3.8-Flash-Next-GSQ-GGUF (HN 49703818) | 09-14 | hold: 125B MoE, not <=8B
30. Unsloth Dynamic 3.0 GGUFs (HN 49365443) | 08-19 | hold: 322 pts, just outside 30d, quant lane
31. llama.cpp fork 2-4x multiGPU MoE (HN 49845314) | 09-25 | hold: fork, unverifiable claims
32. Faster prompt lookup drafting (HN 49859982) | 09-26 | hold: 89 pts, unread
33. Magnitude launch (HN 49911995) | 09-30 | hold: 178 pts agent-inference engine, unread
34. IttyBittyAI Qwen2.5:0.5B on 2017 phone (HN 49835080) | 09-24 | drop: no URL, unverifiable
35. PewDiePie Qwen2.5-9B finetune (HN 49918326) | 10-01 | drop: video, no measured content

## Pass 2, deep reads (10 items; depths labeled)

FULL VERBATIM ABSTRACT (curl of `https://export.arxiv.org/api/query?id_list=...`, raw XML parsed
in this ask's transcript): 2609.31678, 2609.05881, 2609.25447, 2609.18526, 2609.35465.
FULL PAGE (web reader): huggingface.co/blog/transformers-llama-cpp-quants,
huggingface.co/prism-ml/Ternary-Bonsai-8B-gguf (quotes re-secured from raw HTML via curl).
STRUCTURED FETCH (WebFetch): arxiv.org/abs/2609.18526, blog.mozilla.ai 4-server benchmark,
news.ycombinator.com/item?id=49567357, blog.madhukaraphatak.in dynamic-abliteration post,
ollama.com/blog/ollama-now-supports-jev-style-decision-models.

### The five arXiv abstracts, verbatim-anchored

- **2609.31678 When Keywords Drop but Classifiers Hold (2026-09-16).** Paired protocol, n=200
  harmful prompts with long filler context, each answered under full retention and under matched
  KV eviction, then scored by keyword heuristics, the HarmBench Llama-2-13B classifier, an
  auxiliary LLM judge, and humans on disagreements. Headline: "On Qwen2.5-3B, keyword refusal
  falls from 98.0% to 80.5% (McNemar p~1e-8) while classifier refusal stays near ceiling
  (99.0%-99.5%) and MMLU accuracy is unchanged (50.0%)"; human labels predominantly follow the
  classifier, consistent with soft refusals. Closing instruction, taken as the E1-E3 amendment:
  "safety auditing under compression should rely on several judges matched to the serving context
  rather than on keyword rates alone." The refusal is in the model; the MEASUREMENT of the
  refusal is runtime-dependent. C1's E1-E3 must score each serving regime (Ollama vs
  transformers, and under compression) with judge ensembles, never keyword filters.
- **2609.25447 Conduct Under Pressure (2026-09-21).** 60 models from 13 vendors, frozen
  multi-turn pressure scenes, frozen codebook: trajectory (held/folded) and manner. Two findings
  separate: "fold rate correlates with a public capability index at Spearman -0.64, with little
  vendor effect" (recency dominates whether a model folds) while "How it holds tracks the
  vendor" (six of 17 manner codes sort by vendor at permutation p<=0.001). Also: six LLM coders
  label more consistently than three human coders (Krippendorff alpha 0.66 vs 0.46). For C1:
  refusal strength is a property of generation recency, not vendor ethics; the fold/freeze
  instrument can run with LLM coders against a small human-owned reference.
- **2609.18526 The Illusion of Local Privacy (2026-09-16).** Four confidentiality boundaries in
  consumer local serving (model loading, runtime memory, wrapper persistence, serving interface),
  LLAnalyzer framework, four open-weight families, two platforms. Findings: 24-hour AFL++ fuzzing
  (12M+ executions) found no parser crashes, but "we recover prompts after inference because
  multiple plaintext representations survive in allocator-managed memory, and sanitisation
  reduces this residue without eliminating it", and "we uncover a previously undocumented
  authorization flaw in llama.cpp that allows one authenticated client to restore another
  tenant's saved conversation state; the attack succeeds in 200/200 controlled trials." The
  janitor host is multi-seat: this is a hardening ticket for any shared Ollama/llama.cpp box.
- **2609.05881 Broken on Arrival (2026-09-05).** 327 quantized artifacts executed (305 official
  Ollama library, 22 top HuggingFace community), 15-task smoke + 164-task escalation + dual
  backend + independent-conversion referee: five silently defective OFFICIAL Ollama conversions
  (four Qwen2.5-Coder-3B, one phi3.5-mini) solving zero tasks on both backends, plus two
  backend-dependent community failures (pass on Metal, degrade on CUDA). "We release ... the
  quantcheck acceptance-testing tool ... and argue that model registries need the acceptance gate
  that package registries already run." Deep-read already by the 09-30 quantization sweep, which
  banked the adjudication chain; cited here because it is the janitor lane's pull-time acceptance
  gate (quantcheck), runnable before any `ollama pull` is trusted.
- **2609.35465 Tetra (2026-09-28).** Verbatim abstract secured this ask: Qwen3-4B/8B/14B files at
  2.73/2.70/2.73 bits per parameter, MMLU 63.37/69.58/75.66, "At 4B our file scores 23.6 points
  above llama.cpp's IQ2_XXS (2.48 bits per parameter)", 113.8/95.0/57.2 tok/s "in our engine" on
  one L40S. Cross-checked against the 09-28 inference-efficiency sweep's full-HTML read, which
  adds the negative: decode is SLOWER than 4-bit AWQ (95.0 vs 123.2 tok/s at 8B). Not a GGUF
  drop-in; format is research-grade. Recorded for the quant floor: 2.7 bits/param is now a
  quality-viable floor, but not a throughput win.

### The five page reads

- **Ternary-Bonsai-8B-gguf (HF card; HN story 2026-09-20).** Apache-2.0, base Qwen3-8B (8.19B
  params, ~6.95B non-embedding), context 65,536. Packed GGUF Q2_0 g128 = 2.03 GiB (2.18 GB),
  "86.7% 7.5x" reduction from FP16 16.38 GB. Card benchmark table (their runs): Avg 75.5 vs
  Qwen3-8B 79.3 across six benchmarks; "Ternary Bonsai 8B ranks 2nd among all compared models
  despite being 1/8th the size." THE CATCH, verbatim: "Q2_0 is not yet in mainline llama.cpp.
  Use our fork at PrismML-Eng/llama.cpp (prism branch, default) which adds Q2_0 support for CPU
  (NEON/generic) and Metal." So: NOT a drop-in on the estate's stock Ollama. Overlap note: the
  27B sibling was verified by the gapwave lane 09-20
  (memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md) with the same fork-only
  caveat; this ask adds the 8B card data (sizes, license, scores) for the janitor-lane decision.
- **HF blog "Transformers now runs llama.cpp quants".** Verbatim from raw HTML: "We're adding
  support for running GGUF models efficiently in transformers , so you can use checkpoints sized
  for your laptop's memory through the familiar transformers APIs." It names the local stack
  explicitly: "Its inference engine powers local AI tools such as Ollama, LM Studio, and Jan."
  Two load paths: GGUF straight into from_pretrained, or `GgufConfig(dequantize=True)` to
  "Dequantize the weights and continue with a standard transformers training workflow" (example
  checkpoint unsloth/Qwen3.5-4B-GGUF). Honesty: the embedded Chaumond tweet is dated April 24,
  2026; the HN resurfaces are 09-22/09-23 (inside my window). The C1 consequence is the point:
  the Ollama-vs-transformers fork is no longer a format boundary, the same GGUF artifact loads in
  both runtimes, so E1-E3's runtime axis can isolate RUNTIME behavior on a SHARED artifact, and a
  single GGUF becomes the controlled variable.
- **Ollama blog: Jev-style decision models (2026-09-29, Ollama 0.35).** New `/v1/systemone`
  endpoint; models named: nimble 9B (Bespoke Labs, open source), tev1 4B and tev1:0.8b (Together
  AI, experimental); "Nimble 9B averaged 91ms per decision in the Pac-Man example below when
  running locally on an M5 Max"; use cases named include content/safety moderation and model
  routing. This is a scut-slot competitor INSIDE the estate's incumbent runtime: a 0.8B/4B
  decision model pulled through the same Ollama the janitors run. Also adjacent to the estate's
  own kev prototype (catalog row corpus/library/kev/AGENTS.md, "Kev - prototype of a Jev-style
  decision model").
- **Mozilla "Benchmarking Local LLM Servers" (2026-09-17).** Four servers (llama.cpp, llamafile,
  LM Studio, Ollama), three Qwen sizes (0.8B/9B/27B), same GGUF files, three hosts (M4 Max, Xeon
  + L40S, Steam Deck Vulkan). Headline: "Across all three models, llama.cpp, llamafile and
  Ollama sit within +/-3% of each other at every prompt length"; the tens-of-percent movers are
  configuration: CUDA graphs +16.8% decode, a newer Vulkan toolchain +63% prompt processing on
  9B, and on Mac MLX builds "Ollama's MLX runner turns on speculative decoding by itself, with an
  adaptive draft depth." Verdict for the janitor lane: engine choice is not the lever; flags and
  toolchains are. No TTFT measured (throughput only).
- **HN 49567357 Gerganov on llama.cpp/ggml after Nvidia's HuggingFace acquisition (2026-09-04,
  76 pts).** His statement per the thread: "Going forward, llama.cpp/ggml will stick to its
  founding principles. One of the most important qualities of the project is to be
  hardware-agnostic," with backends continuing "as usual - driven and shaped by the community."
  Stack-risk signal for anything pinned to llama.cpp; no fork-exodus evidence in the thread,
  community-health comments dominate.
- **Dynamic Abliteration (blog.madhukaraphatak.in, 2026-09-24; HN 49831201, 108 pts).** Runtime
  refusal suppression with base weights frozen: PyTorch forward hooks "intercept intermediate
  residual streams at runtime across Layers", a learned Engram module (n-gram hash tables +
  per-layer projections + sigmoid gate) decides when to inject. Measured on Qwen3-4B bf16 on an
  A100: single-layer steering (layer 14, alpha=1.2) FAILED (still refuses); multi-layer static
  steering (layers 12-20, alpha=0.3) succeeded (model produced keylogger code); Engram trained on
  2,000 PKU-SafeRLHF samples in 8.92 minutes. C1 consequence: stock-model censorship measurements
  do not bound steered deployments, and suppression no longer requires weight edits (contrast the
  memlance fork finding that Ollama cannot inject residual vectors: this rides transformers-side
  hooks, i.e. the OTHER runtime).

## The four research questions, answered from what was fetched

### RQ1: upgrade over gemma:2b/gemma4 at <=8B, Sep-Oct 2026, licenses

Honest window answer: NO new <=8B general-purpose open-weight release was found in Sep-Oct 2026
that beats gemma-class 2B per measured evidence. The arXiv ti: sweep surfaced only audio/video/
driving Qwen items and 552B-class DeepSeek MoEs; HN's release chatter is quant re-releases and
decision models. The candidates that DID surface:

- **Ternary-Bonsai-8B** (Apache-2.0, verified on card this ask): 2.03 GiB, 75.5 vs Qwen3-8B 79.3
  avg, but loads ONLY in PrismML's llama.cpp fork: not a drop-in for the estate's Ollama; a
  fork-runtime experiment, not a janitor replacement.
- **Ollama tev1:0.8b / tev1 4B / nimble 9B** (09-29): drop-in via the incumbent runtime, but
  chore-specific decision models, not general chat; license for nimble named "open source"
  (Bespoke Labs) on the blog, exact license text OWED.
- **Qwen3.5-4B** exists as unsloth GGUF (named in the HF blog example) and a 09-29 HN post
  describes fine-tuning it to replace Gemini Flash-Lite in RAG (duane.sh, title-level only,
  unread). Qwen license text remains OWED, carried from prior sweeps.

Verdict for the bottom rung: KEEP gemma:2b/gemma4 this window. The replacement pressure is
chore-shaped (decision models at 0.8B-4B doing the scut lane's classification work in 91ms),
not a general-model upgrade. A first honest experiment before any slot change: pull tev1:0.8b,
run the scut ticket mix, compare.

### RQ2: refusal/censorship differences across runtimes, extending C1's E1-E3

Four measured 2026 sources, all read this ask: (1) 2609.31678, refusal MEASUREMENT is
runtime-dependent: under matched KV compression keyword monitors under-report refusals 98.0 ->
80.5% while trained classifiers hold 99.0-99.5; mandate multi-judge scoring matched to the
serving regime; (2) 2609.25447, fold-vs-hold tracks generation recency (Spearman -0.64 with
capability), manner tracks vendor: pin model DATE as a variable in E1-E3; (3) Dynamic
Abliteration, transformers-side runtime hooks suppress refusal on Qwen3-4B with weights frozen,
single-layer fails, multi-layer (12-20) succeeds: C1 must assume steered deployments exist and
add a hooks-present arm; (4) HF transformers-GGUF, the same GGUF artifact now loads in both
Ollama and transformers, which makes the runtime axis a clean controlled experiment (one
artifact, two runtimes). Issue-tracker-grade corroboration: 2609.05881's five broken OFFICIAL
Ollama conversions show the Ollama artifact pipeline itself can be defective independent of the
model. Synthesis for E1-E3: add (E4) a compression arm, (E5) a steered/armored arm, and score
both with judge ensembles, never keyword rates.

### RQ3: local inference stack changes, last 60 days (HN + arXiv doors)

(1) Ollama 0.35 ships `/v1/systemone` decision models (09-29); (2) the transformers-GGUF loader
formalizes the shared-artifact runtime boundary (blog ~04-24, resurfaced 09-22/23); (3) Mozilla's
4-server measured benchmark says configuration beats engine, within 3% among llama.cpp/
llamafile/Ollama at every prompt length (09-17); (4) Nvidia acquired HuggingFace and Gerganov
publicly committed llama.cpp/ggml to hardware-agnostic independence (09-04); (5) new engines
crowd the lane: Ollaya (615 pts, 09-25, deep-banked by the 09-30 sweep), Magnitude YC S25
(178 pts, 09-30), Reflex cold-start TTFT; (6) llama.cpp internals: faster prompt lookup drafting
(89 pts, 09-26), a 2-4x multiGPU MoE fork (09-25), and on arXiv Galahad persists KV across
vLLM/SGLang/llama.cpp (09-30) and Vosti ships formally verified bitwise-identical inference
(09-30); (7) security: the OllamaDrama honeypot paper (09-24) and 2609.18526's llama.cpp
cross-tenant restore flaw (200/200).

### RQ4: day-0 GGUF + RAM/VRAM footprints per quant

Verified footprints this ask: Ternary-Bonsai-8B Q2_0 g128 = 2.03 GiB (2.18 GB) vs 16.38 GB FP16
(86.7% reduction, 7.5x); card-throughput 76 tok/s (llama.cpp fork, Apple M4 Pro 48 GB per the
card's TOC label). Tetra Qwen3-4B at 2.73 bpw: MMLU 63.37, 23.6 pts above llama.cpp IQ2_XXS at
2.48 bpw, but slower than 4-bit AWQ (09-28 sweep's read). Unsloth remains the day-0 GGUF
norm-bearer: Dynamic 3.0 GGUFs (322 pts, 08-19, quant lane) and Qwen3.8-Flash-Next-GGUF with a
non-uniform GSQ build running on 2x RTX 3090 (09-14). The janitor lane's actionable artifact is
not a model but quantcheck (2609.05881's released tool): run the smoke suite on any pulled GGUF
before trusting it, since five official Ollama conversions were silently broken and two more
were backend-dependent (pass Metal, fail CUDA).

## Overlap census (commands actually run this ask)

`.venv/Scripts/python.exe` scan of catalog/catalog.jsonl (691,788 lines), memory/ (373,657
files), and both predecessor carriers (343 files under watch/inbox/frontier_olm_2026-09-30/ and
watch/inbox/frontier_olm_20260928/) over 24 phrases. Results:

- "dynamic abliteration" ZERO, "engram steering" ZERO, "ollaya" ZERO in catalog/memory:
  genuinely estate-new surface (Ollaya itself was deep-banked by the 0930 inference-eff sweep).
- "when keywords drop"/"soft refusals under kv": memory/runs/corpus_gap_research/
  ARXIV_REGISTER.json + MAP_BACKFILL + listed (title-only, no deep read) in the 0928
  quantization-compression-arxiv sweep. This ask's deep read adds the numbers and the E1-E3
  amendment; not a re-bank.
- "conduct under pressure": catalog.jsonl:445131 only (state/arxiv/2026-09-23/2609.25447v1.txt
  abstract snapshot, 1,742 bytes). Never mined. New.
- "broken on arrival"/"quantcheck": catalog 3 rows + 09-30 quant sweep DEEP READ. Re-bank
  avoided; cited, not banked.
- "ternary-bonsai"/"prismml": gapwave splash verified the 27B 09-20 + quant sweeps + catalog
  rows. The 8B card data is the new increment; family is known.
- "transformers-llama-cpp-quants": one raw RSS capture line (0930 _rss_quant_month.xml) and a
  title-list line in the 0928 quant HN sweep. Never mined as a finding. New at finding level.
- "illusion of local privacy": listed in BOTH kv-cache sweeps' candidate lists (0928+0930), no
  findings text found in my grep. Banked here for the janitor-host angle with that disclosure.
- "leech-lattice quantized" (Tetra): 0928 inference-efficiency sweep full-HTML read. Cited only.
- "benchmarking local llm servers"/"llama-benchy": gapwave hn_x_fanout/local_serving.md + 0928/
  0930 lists. Banked at prose depth here; flagged as previously listed.
- "ollama now supports"/"nimble"/ollama.com/blog: ABSENT from all three surfaces. The 09-29
  Ollama blog is estate-new.
- "gerganov": catalog.jsonl:691308 + memory hits are general llama.cpp references; the
  Nvidia-HF thread was title-listed by the 0928 quant HN sweep. Prose-only here.

## OWED / not verified

- nimble/tev1 license texts (blog says "open source" for nimble only): OWED, one HF/GitHub fetch.
- Qwen3.5-4B and Qwen3.8 license texts: carried OWED from prior sweeps, not re-verified here.
- Galahad 2609.39358, Vosti 2609.38981, OllamaDrama 2609.29757, RLX 2609.37916, Disaggregated
  Quantization 2609.26333, 2609.23039, 2609.35544, 2609.19989: title/gist only from pass-1, not
  read end to end, NOT banked as items.
- The Mozilla post's per-token overhead figures (0.4/1.8/5.4 ms) are the extractor's reading of
  the page; the within-3% quote is marked as extracted from that fetch, confidence 0.8.
- Ternary-Bonsai 76 tok/s figure comes from the card's own benchmark section (self-reported,
  M4 Pro); no independent run exists.
- HN "Ollaya" and the llama.cpp MoE fork claims: unverifiable community claims, prior sweeps
  hold them; not re-verified.
- INDEX.json registration of this file: not performed (the workflow publishes).

## Receipts

Fetches this ask: WebFetch arXiv API x5 + abs x1 + HN Algolia x6 + HN item x1 + Mozilla blog +
madhukaraphatak blog + ollama blog; web reader x5 (two arXiv abs, HF blog, Bonsai card, one
1302 rate-limit failure on 2609.18526); curl x3 (arXiv id_list XML, HF blog HTML, Bonsai card
HTML); WebSearch x0 (not needed, both doors answered). Local instruments: one python overlap
scan (691,788 catalog lines + 373,657 memory files + 343 carrier files), one python XML/HTML
verbatim extractor, todo tracking. Temp files `_sweep_tmp_arxiv.xml`, `_sweep_tmp_hf.html`,
`_sweep_tmp_bonsai.html`, `_sweep_bank_draft.md` are working scratch in the repo root, deleted
after the sanitized landing below.
