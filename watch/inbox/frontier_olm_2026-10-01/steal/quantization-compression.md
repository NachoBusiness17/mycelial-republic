# STEAL CARD: quantization-compression (round 2, critique applied)

Round 2. Date: 2026-10-01. The round-1 critique's five fixes are all applied; every fix
was re-verified against the tree THIS ask (section 1). Round-1 items the critique marked
sound are kept (catalog greps re-run again; organ cites unchanged). Sources: the same 8
confirmed finds from the ask (6 Reddit via PullPush, 2 X via fxtwitter), now cross-checked
against the same run's banked sweep records under
watch/inbox/frontier_olm_2026-10-01/sweep/.

## 1. Checks run THIS ask (round 2)

1. Catalog overlap greps re-run (rg 15.2.0): llama-manager 0, kvarn|anbeeld 0,
   exl3|exllamav3 0, atomic dynamic 0 (each exit 1, echo'd label). catalog/catalog.jsonl
   present. Matches the critique's "keep as-is" verdict.
2. `ollama list` run this ask: gemma:2b b50d6c999e59 1.7 GB present (matches the 09-30
   card receipt at frontier_olm_2026-09-30/steal/quantization-compression.md:11), plus
   qwen2.5:3b-instruct 1.9 GB and deepseek-r1:1.5b 1.1 GB. The primary probe substrate
   is on the box.
3. Fix 1 verified: sweep/_fx/ contains superalesha_status_2090318708283502972.json with
   tweet id "2090318708283502972" and the verbatim five-stack lineup text ("FP8 baseline
   on vllm, 2x3090 NVFP4 W4A16 on vllm, 2x3090 AWQ INT4 on vllm, 2x3090 GGUF Q4_K_M on
   llama.cpp, 2x3090 NInfer on a single 3090 ... 40 arms total"). NO _fx artifact exists
   for the ask-carried id 2090318712515481653. The banked receipt is the result post of
   the bake-off thread (replying_to root 2090318703992717486).
4. Line numbers checked: "the specific post did not resolve" sits at
   sweep/quantization-compression-x.md:22 exactly as the critique cited. The banked
   find-1 verdict wording "KV quantization is the LAST resort" sits at
   sweep/quantization-compression-reddit.md:51, NOT :56 as the critique cited (the :56
   line is the anbeeld precision-tail section heading; wording verified at :51). The
   verbatim line "I can't stand kv cache quantization" is NOT in the banked reddit sweep
   (rg, 0 hits), confirming critique fix 5.
5. Fix 3 verified: mag/vast_launcher.py:444 (serve steps) and :457 (launch_command) both
   carry `-ngl 999 -c 262144 --flash-attn on --cache-type-k q8_0 --cache-type-v q8_0`
   for the SAELIS lane; :436 prices the trade ("48GB ... for Q8_0; 24GB only fits Q4
   (~18GB, quality drop)").
6. Fix 4 verified: mag/auto_quantize.py:55-57, `class Quantum`, docstring "An aggregated
   analytics bucket. Replaces N individual events with 1 summary", `level` comment at
   :60 "0=raw, 1=hourly, 2=daily, 3=weekly, 4=monthly". Analytics downsampling, not
   model or KV quantization. mag/state_quantizer.py is likewise state-side.
7. Find-8 receipt spot-check: rg -c "14/22" sweep/_fx/outsource__status_2088743329760469374.json
   -> 1 hit; the receipt is in sweep/_fx/ (ls this ask).

## 2. The steal (one mechanism, not a link dump)

Across all eight finds the same mechanism repeats: inside one model family, the measured
quality delta between quantization choices is SMALLER than the quality/perf deltas
available from cheaper adjacent levers (KV cache policy, context length, reasoning
preset, runtime choice, distill-target choice). Therefore run quantization as a
DEGRADATION LADDER with a measured stop, not as a static quant pick.

(a) Ladder order for llama.cpp-class serving (find 1, 2026-09-11, wadeAlexC's
llama-manager): speculative decoding off first, then mmproj (vision tower) to CPU, then
KV q8_0, then KV q4_0, preserving the KV cache across hot reconfigs. The banked sweep
carries the ladder's measured shape on a 32 GB GPU with Qwen3.8-27B-UD-Q4_K_XL: f16-KV
baseline 167,680 tokens, +33,280 from disable-spec, +17,920 from mmproj-to-cpu,
+43,264 from quantize-kv-q8, reaching 262,144 (sweep/quantization-compression-reddit.md:51).
The author's banked verdict: "KV quantization is the LAST resort" (same line). The
punchier ask-carried quote ("I can't stand kv cache quantization. Even at q8_0, I can
feel the difference.") is NOT in the banked sweep record; it is labeled ask-carried
only and used as the hypothesis to test, not as evidence.
(b) The quant pick inside one family is nearly free at 4-bit class (find 7, bake-off
thread, banked id 2090318708283502972): the lineup text is byte-backed by the _fx
receipt (5 production stacks, 150 agentic/coding plus 90 reasoning tasks per mode, 40
arms); the pass@1 outcome is banked at sweep/quantization-compression-x.md:22 (AWQ INT4
90.0 / NVFP4 89.3 / GGUF Q4_K_M 89.3 / FP8 88.7 / NInfer 88.0, McNemar a statistical
tie; "the gap between quants is smaller than the gap between reasoning presets"). The
ask-carried quote and the ask-carried URL for this find are NOT byte-backed (no _fx
artifact for 2090318712515481653; the numbers come from the sweep lane's own read).
(c) Conditioned counterweights: find 8 (banked receipt
sweep/_fx/outsource__status_2088743329760469374.json, spot-checked this ask): Q4 14/22
vs Q5 15/22 with Q4 buying speed and context headroom; find 4 (sweep reddit item 6, :66):
task-conditioned Q4-vs-Q8 delta (AD-Q4_K_M 95.6% top-1 / KLD 0.0113 / 67 tok/s vs Q8_0
98.9% / 0.0006 / 50 tok/s, voxel task, RTX PRO 6000), authors "sometimes preferred the
Q4 output overall".
(d) Selection metric: KLD per GB, gated by a task eval (find 2, sweep item 2 :54: ~36
quants of a 4B model on Lunar Lake iGPU; Bartowski Q5_K_S best KLD/GB 0.00778 / 2.91 GB
vs Q4_K_M 0.0216-0.0250; the author's reruns showed KLD "jumping up-and-down full grid
lines" run to run). The estate's own bench shows the same disease:
memory/improve/sources/ponytail-2026-08-03/benchmarks/results/2026-06-15-llama3.2-local.md
lines 34-39 (n=5 median +26%, n=3 median -17%, sign flips on sample size).
(e) Capacity law bounds the distill target (find 5, sweep item 7 :69: Allen-Zhu & Li ~2
bits/param; Q1 garbage at 30B, usable at 1T-3T; a 2-4B janitor holds procedure, not
world knowledge).
(f) Distill recipe shape (find 6, sweep item 8 :72): bucket failure types BEFORE
training (wrong tactic / bad formalization / missing lemma search / proof-state
misunderstanding), then logit distillation from public scripts over a few-GB trace set;
maps 1:1 onto seat tapes (code-agent-data skill). The sibling X lane partially fills the
reddit lane's frontier-distill coverage gap with the Qwen3.8-2B-Distill recipe
(sweep/quantization-compression-x.md:25); the reddit-door gap itself stands as OWED.
(g) Runtime challenger on record (find 3, sweep item 4 :60): ExLlamaV3, quality claims
self-labeled folklore ("these are not benchmarks"), comments carry numbers (~65 to ~80
tok/s on Qwen3.8-27B 8-bit at 256k, 5090+4090; exl3-SC-6bpw ~10% faster tg, 10% less
VRAM, 20% more context vs Unsloth q6_KL) plus the mul1-vs-mcg codebook caveat.
(h) Ladder refinements banked alongside find 1 (sweep :51, :56-57): the precision tail
(anbeeld/BeeLlama: keep the newest 128-2048 KV tokens full precision; q4_0 + 1024-token
tail beat q5_0 no-tail on BOTH quality and memory) and the community reports that KV
FP16-vs-Q8_0 was invisible in heavy coding tasks while Q4-vs-Q5 MODEL quant was visible
(Itsluc). These slot a quality-recovery rung between KV q8_0 and full f16.

## 3. Estate map (organ per steal; round-1 collision fixed)

- janitor serving config (the REAL landing spot; the estate has no model-quantization
  organ): port (a) as a KV ladder in the config of the daemon serving gemma:2b scut and
  gemma4. This EXTENDS an existing unmeasured bet: the estate already serves the
  specialist lane with the exact q8_0 KV rung, mag/vast_launcher.py:444 and :457
  (`--cache-type-k q8_0 --cache-type-v q8_0 --flash-attn on -c 262144`, SAELIS). The
  probe in section 4 finally measures the rung the estate already runs.
- context pack (mag/context_pack.py:35 `_emit_pack_offload`): takes (a)'s offload-first
  ordering and, from find 8, long-context decode decay (48 tok/s at 131K down to 4.1 at
  262K) as a pack-sizing input; cap packs at the measured decode knee.
- percolator (mag/percolator.py:76) plus the code-agent-data skill: port (e) as the rule
  that distilled seats encode procedure, not world knowledge, and (f) as a pre-training
  gate: failure-type buckets over seat tapes must exist and cluster before any QLoRA run.
- sovereign mirror (docs/DOCTRINE_MAP.md:78): port (g) as the adoption gate for any
  27B-class local mirror: exl3 must beat the llama.cpp baseline head-to-head (tg, VRAM,
  context) and the codebook (mul1 vs mcg) must match the downloaded build.
- ANALOGY ONLY, labeled as such: mag/auto_quantize.py:56 `class Quantum` (analytics
  downsampling bucket, "Replaces N individual events with 1 summary", levels 0=raw
  through 4=monthly at :60) and mag/state_quantizer.py (state-side summaries) are NOT
  model or KV quantization organs. Any port of (b)/(d) onto them is by analogy, same
  convention as frontier_olm_2026-09-30/steal/quantization-compression.md:46.
- Continuity cite: watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md
  (09-30 round 1) is a DIFFERENT mechanism (capability-stratified quant damage +
  agreement counterfeiting, arXiv 2609.* finds) with complementary probes (induction /
  retrieval battery, collision rate, evidence-field gate). Fold both cards without
  double-counting the janitor-quant lane in percolator_candidates.jsonl.
- water graph (hydrology organ: mag/field_flow.py; tests/test_hydrology.py,
  test_k8s_water.py, test_river.py) and gopher fleet (docs/FRAMEWORK_LOAD.md gopher
  lanes): NO find feeds either. Recorded as no-feed rather than stretched.

## 4. Probes (falsifiable, cheap; round-1 threshold fixed to flip counts)

PRIMARY (carried in the StealCard JSON): on gemma:2b (b50d6c999e59, 1.7 GB, confirmed by
`ollama list` this ask), run a 20-prompt needle bank pinned near the model's served
context ceiling: each prompt carries deterministic filler padding to roughly 8K tokens
(ceiling confirmed at probe time; it is the runner's gemma:2b limit) plus one
exact-match needle task (repeat-this-nonce-string / recall-this-fact). Three arms at
identical seed and temperature, changing only KV cache type: f16, q8_0, q4_0.
Falsifiable prediction in FLIP COUNTS (a 20-prompt bank moves in 5-point steps, so
round 1's percentage framing was innumerate): q8_0 flips 0 of 20 needle answers versus
f16 (at most 1 of 60 pooled across three repeats) while `ollama ps` shows a measurable
VRAM drop at the pinned context. Falsifier: q8_0 flips 2 or more of 20 in any repeat,
which confirms find 1's author on OUR stack, stops the ladder at mmproj-offload for
janitors, and files a review ticket against the unmeasured SAELIS q8_0 KV default
(mag/vast_launcher.py:444,457); or q4_0 flips 0 of 20, which extends the ladder one
rung down (next rung: the precision tail of (h), anbeeld-style, before any deeper KV
quant). Context is pinned deliberately: KV bytes and the KV-quant delta scale with
context, and at short prompts the delta on a 1.7 GB model sits inside VRAM noise.
Step 1 of the probe verifies the Ollama-side KV knob; if the daemon does not expose it,
fall back to raw llama-server, whose --cache-type-k/--cache-type-v q8_0 flags ARE
estate-verified (mag/vast_launcher.py:444,457). Cost: 60 local inferences plus one
filler builder, $0, one afternoon. This also executes the sibling X lane's own open
follow-up ("rerun the suite shape on gemma:2b", sweep/quantization-compression-x.md:23).

Per-find probes:
- find 2: re-run the estate's llama3.2 Q4_K_M bench (path in 2(d)) against Q5_K_S on the
  same 5 tasks; falsifier: Q5_K_S fails to beat Q4_K_M on quality per GB.
- find 3: hardware-feasibility check FIRST (OWED: exl3 needs exllamav3 plus CUDA; this
  host's GPU not verified this ask), then a 30-minute head-to-head vs q6_KL.
- find 4: adopt the conditioned reporting template (task, hardware, metric, tok/s, KLD,
  top-1) as the acceptance bar for any estate quant bench; a bench that cannot state
  conditions is not evidence.
- find 5: quiz a 2-4B seat on procedure versus world-knowledge items from its own
  fine-tune set; prediction: procedure retention exceeds fact retention.
- find 6: bucket 100 seat-tape failure rows before any training; falsifier: no bucket
  holds 60%+ of failures, so no distill signal and the QLoRA lane stays closed.
- find 7: A/B two reasoning presets on the SAME Q4 model over 50 bank asks; prediction:
  the preset gap exceeds the quant gap.
- find 8: measure janitor tok/s at 2K versus 16K context; set the context-pack cap at
  the measured knee.

## 5. Overlap and novelty (re-verified this ask, round 2)

rg 15.2.0 over catalog/catalog.jsonl (present): llama-manager 0 hits, kvarn|anbeeld 0,
exl3|exllamav3 0, atomic dynamic 0. Matches the finds' claims and the critique's
keep-as-is verdict. Nearest estate holding (complementary): the llama3.2:latest 3.2B
Q4_K_M Ollama bench (section 2(d) path).

## 6. OWED / honesty ledger (updated by the critique)

- Find 7: the ask-carried URL (x.com/superalesha/status/2090318712515481653) and quote
  are NOT byte-backed; the banked artifact is the result post, status id
  2090318708283502972, receipt sweep/_fx/superalesha_status_2090318708283502972.json
  (lineup text), with the pass@1 numbers banked at
  sweep/quantization-compression-x.md:22. Used with that provenance.
- Find 1: the "I can't stand kv cache quantization" line is ask-carried only (rg 0 hits
  in the banked sweep this ask); the banked verdict wording is "KV quantization is the
  LAST resort" (sweep/quantization-compression-reddit.md:51; the critique's :56 cite
  was off, verified at :51).
- Ollama-side KV-quant knob for the primary probe: not verified this ask (step 1 of the
  probe). llama-server flags are estate-verified in-repo (mag/vast_launcher.py:444,457),
  which retires round 1's blanket knob OWED.
- gemma:2b 8K context ceiling: general knowledge, confirm at probe time.
- exl3 hardware feasibility on this host: OWED before any find-3 probe.
- X-thread numbers (finds 7, 8): single-author measurements, not replicated by us.
- Reddit-door frontier-distill coverage gap (find 6): stands; the sibling X lane's
  Qwen3.8-2B-Distill recipe (sweep/quantization-compression-x.md:25) partially fills it.

## 7. Source URLs and receipts

1. https://www.reddit.com/r/LocalLLaMA/comments/1wdqit1/running_qwen3827bq4_at_max_context_on_a_32_gb_gpu/ (2026-09-11, conf 1; banked sweep/quantization-compression-reddit.md:51)
2. https://www.reddit.com/r/LocalLLaMA/comments/1sdqn13/qwen354b_gguf_quants_comparison_kld_vs_speed/ (2026-04-06, conf 1; banked sweep :53-54)
3. https://www.reddit.com/r/LocalLLaMA/comments/1wa36d1/exllamav3_is_underrated/ (2026-09-07, conf 1; banked sweep :59-60)
4. https://www.reddit.com/r/LocalLLaMA/comments/1vwh3u7/we_quantized_qwen_38_27b_and_compared_the_quants/ (2026-08-23, conf 1; banked sweep :65-66)
5. https://www.reddit.com/r/LocalLLaMA/comments/1vcwl43/is_there_a_point_where_models_just_cannot_get_any/ (2026-08-01, conf 1; banked sweep :68-69)
6. https://www.reddit.com/r/LocalLLaMA/comments/1ugo5nw/how_to_distill_my_own_models/ (2026-06-27, conf 1; banked sweep :71-72)
7. BAKE-OFF, CORRECTED CITATION: banked status id 2090318708283502972, receipt
   sweep/_fx/superalesha_status_2090318708283502972.json (2026-08-20, conf 0.97; numbers
   banked sweep/quantization-compression-x.md:22). The ask-carried id 2090318712515481653
   has no _fx artifact and is not banked.
8. https://x.com/outsource_/status/2088743329760469374 (2026-08-15, conf 0.97; receipt
   sweep/_fx/outsource__status_2088743329760469374.json, spot-checked this ask)
