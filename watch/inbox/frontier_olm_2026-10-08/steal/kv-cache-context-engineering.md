# STEAL CARD: kv-cache-context-engineering (frontier OLM 2026-10-08) - REV 2

Round 2 draft, amended from round 1 per critique. Round 1 passed the substance gate (real
mechanisms, no link dump) but carried three citation defects and one probe-design gap; all four
are fixed here and each fix was re-verified against current bytes THIS SITTING before amending
(see Amendments below). Both confirmed finds were already banked ABS-level by today's own sweep
(watch/inbox/frontier_olm_2026-10-08/sweep/kv-cache-context-engineering-arxiv.md: PatchKV item 1
at :28-29, Dual-QK item 4 at :37-38), so per the BreadthKV precedent ("this card banks the PORT,
not the find", watch/inbox/frontier_olm_2026-10-06/steal/quantization-compression via x.md:8) this
card banks ports and probes, not discoveries. Both arxiv abs pages were re-fetched live in round 1
and corroborate the sweep's quotes and add abs-level mechanism detail. The PatchKV html full text
remains unread; on the timeout count the sweep contradicts itself (see Amendments, M2), and the
depth caveat stands either way. The durable StealCard JSON is now banked beside this file
(kv-cache-context-engineering.json) so future rounds can read it without the run host.

## Amendments (round 2; every re-verification command quoted)

- FIX 1 (wrong-file law cite, blocks): round 1 cited the Q5 instrument law to
  watch/inbox/frontier_olm_2026-10-07/sweep/kv-cache-context-engineering-arxiv.md:57. Wrong file
  and wrong content: that line is a different Q5 (guide-style abstraction, MII numbers). Re-verified
  this sitting: `grep -c -i -e "task-level" -e "perplexity"` over the 10-07 file returned 0
  (EXIT=1), and the law lives at watch/inbox/frontier_olm_2026-10-06/sweep/kv-context-engineering-arxiv.md:57
  (filename has NO "cache"): "any probe scored by offline PPL can pass while task accuracy fails,
  so the A/B must score task-level probes end-to-end". Both cites (probe 2 body and citation list)
  now point at the 10-06 file.
- FIX 2 (false import mechanism, blocks): round 1 claimed the prefix simulator IMPORTS the pack's
  clip shape from mag/context_pack.py:1416. False on current bytes: tools/prefix_cache_sim.py:25 is
  `from __future__ import annotations`, and `git grep -n "context_pack" -- tools/prefix_cache_sim.py`
  returns no import, only comment/string references (:36 the copied constant CLIP_SUFFIX with its
  provenance comment, :128 a law tag, :140 the docstring "Estate hard clip, mag/context_pack.py:1414-1416
  shape"). The coupling is a COPIED CONSTANT, not an import: CLIP_SUFFIX = "\n...(pack clipped)" at
  tools/prefix_cache_sim.py:36, while the executable clip line is mag/context_pack.py:1970
  (`text = text[: max_chars - 20] + "\n...(pack clipped)"`, read this sitting) and :1416 is only the
  schema line. Restated below; consequence flagged: probe 1's rendered packs can silently drift from
  real pack clips if either side edits its copy, so probe 1 step 0 re-diffs the two strings.
- FIX 3 (stale inherited cite, blocks): freeze_system_prompt is mag/context_pack.py:948
  (`grep -n "def freeze_system_prompt"` returned :948, read this sitting), not :467-526; that range
  holds pack config keys ("include_skills" et al, :467-469) and _normalize_mode (:524-526). Round 1
  inherited :467-526 from the tools/lru_null_arm.py:29 header without re-verifying. Card fixed;
  the tool header is flagged STALE here and in the citation list (its :29 provenance comment points
  at the wrong range; the function it names is at :948).
- FIX 4 (probe 2 serving path, blocks): run_ab.py is Ollama /api/generate ONLY: OLLAMA =
  "http://127.0.0.1:11434" and NUM_CTX = 8192 at run_ab.py:34-36, the request posts to /api/generate
  at :227, and a grep for llama_cpp/import llama over the file returns nothing else. Round 1's
  declared fallback (in-process llama_cpp type_k/type_v) is a DIFFERENT serving path whose decode
  t/s and pass rates are not comparable to the quant_ab RECEIPT baseline or the burns.md:59 prior.
  Probe 2 is rewritten below: step 0 pins ONE serving path by name, and cross-path numbers are
  declared non-poolable.
- M1 (gray band, minor): round 1's prediction (<10 percent) and falsifier (>=20 percent of resume
  points with >=50 percent of tokens) left 10-19 percent undispositioned. Disposition now stated in
  probe 1: that band is INCONCLUSIVE, triggers no port decision either way, and requires a
  source-attributed re-run (which ask-path surface mutated) before any claim.
- M2 (timeout count, minor): round 1 said the PatchKV html "timed out twice" citing sweep:8 and
  :67. sweep:8 records ONE timeout event for 2609.26219v1 (the "2 timed out" are two papers,
  2610.02766v1 and 2609.26219v1), while sweep:29's item text says "html timed out twice". The two
  sweep lines disagree on the count; this card claims only what both support: the html full text is
  unread, abs-only.
- M3 (moving-tree catalog cites, minor): catalog line numbers are coordinates on a moving tree.
  All three catalog rows are now cited with id + path alongside the line number (see citations).

## Find 1 (headline): PatchKV - the arithmetic under the byte-identical prefix law, and the price tag on the day the law breaks

- URL: https://arxiv.org/abs/2609.26219 (Yang, Guo, He, Chen, Hu, Li, 2026-08-18; abs page re-fetched round 1, corroborated by the round-1 critique this sitting).
- Quote (ask, confirmed verbatim on the live abs page): "altered causal histories and rotary positions prevent exact reuse of their offloaded key-value (KV) states".
- Mechanism (abs page): decompose adjacent context versions into an exact prefix, an updated span,
  and an aligned suffix; an offline drift model predicts the edit-local dirty region; sparse
  nonlocal blocks are recovered from stored attention; the surviving suffix is restored from CPU
  memory using per-block precision tags through a fused dequantization + RoPE-correction +
  KV-placement path. Numbers: "2.51-3.85x speedup in mean resume time-to-first-token over full
  suffix recomputation" and 1.26-2.06x over CacheBlend, F1 matching or exceeding CacheBlend in six
  of nine settings (remaining within 1.36 points), across three models and three long-context QA
  workloads.
- What is actually new vs estate holdings: the estate holds the prefix-break as LAW (byte-identical
  asks; measured 97.3% cache hit rate with "prefix-breaking rewrites reprice the wave at fresh
  rates", watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md:17) and as vendor grammar
  (xAI edit/remove/reorder breaks the shared prefix, sweep:29). PatchKV is the arithmetic UNDER the
  law: the break is causal-history + RoPE-position math, not a vendor policy choice, so no provider
  knob escapes it, and the repair has a measured price (2.5-3.9x cheaper than cold suffix
  recompute). The estate already holds two of the three pieces: mutations move off the ask path
  (SmoothAgent lookahead transformation, sweep:34-35) and folds stay reversible (ReFold P5 sheds,
  commit 6685db6bc: "sha-addressed stubs + restore door proved 4290 chars"). PatchKV supplies the
  missing third piece: the cost model for the day a mutation happens anyway.
- Organ map: CONTEXT PACK organ, engine side. The pack machinery already journals WHAT changed and
  WHERE: _shed_fold_marker (mag/context_pack.py:69), _shed_recipe_render (mag/context_pack.py:108),
  restore_shed_section (mag/context_pack.py:225), list_shed_stubs (mag/context_pack.py:326), and
  freeze_system_prompt is at mag/context_pack.py:948 (FIX 3). The pack's clip shape reaches the
  prefix simulator as a COPIED CONSTANT, not an import (FIX 2): CLIP_SUFFIX at
  tools/prefix_cache_sim.py:36 mirrors the executable clip at mag/context_pack.py:1970. A shed
  recipe is structurally PatchKV's drift-model OUTPUT (which span went dirty) in ledger form; the
  port would add the KV-side actuator that consumes it.
- Port boundary, honest: both local serving lanes run SHORT context by law. ollama_context is 8192
  (configs/lanes.yaml:63, cap rationale in the comment at :30: "CONTEXT=8k (not 65k)"; the same
  envelope is hard-coded into run_ab.py:36 with the lanes.yaml cite) and the llama.cpp bridge still
  spawns hard-coded "--n_ctx 2048" (mag/llama_cpp_bridge.py:127-128, with the 0.3.36 flags
  fix-comment at :110-115). At 2-8K, the suffix PatchKV saves is a few hundred ms; the paper's
  economics live at 65K+, which this estate deliberately does not run. So the port is conditional
  on probe 1 below: price the surface first, and only if the estate ever lifts the context cap does
  the shed journal become an engine patch queue. Until then this is a grammar row with a measured
  constant attached.

## Find 2: Dual-QK - the 2-bit survival recipe, pointed at the BreadthKV collapse floor the estate already measured

- URL: https://arxiv.org/abs/2610.09827 (Whang et al., 2026-10-07; abs page re-fetched round 1, corroborated by the round-1 critique this sitting).
- Quote (ask, confirmed on the live abs page): "Dual-QK provides 6.8x KV-cache compression and an
  estimated 8.3x reduction in KV read volume relative to unpruned BF16".
- Mechanism (abs page): paired NON-orthogonal query and key transforms (partial key whitening
  combined with a query-aligned basis from calibrated statistics) enable INT2 key quantization plus
  dynamic query-channel pruning; channel-0 protection and bucket-relative RoPE hold long-context
  accuracy. Numbers: 6.8x KV compression at 128K, ~8.3x KV read-volume reduction, up to 3.75x
  decode throughput vs unpruned BF16 in their SGLang implementation, beating OSCAR on most tasks at
  40 percent query-channel sparsity across four models.
- What is actually new vs estate holdings: BreadthKV (banked 10-06; steal card
  watch/inbox/frontier_olm_2026-10-06/steal/quantization-compression via x.md, catalog row
  catalog/catalog.jsonl:1195479, id a65c50a1a541) measured the collapse floor: 1.25-bit KV
  collapses to 0-12% calibration accuracy (same card, :27, quoting the 10-06 KV lane read).
  Dual-QK is the "how to survive 2 bits" answer: the paired transform + channel-0 protection +
  bucket-relative RoPE recipe is what separates survivable INT2 from the naive rotation that floor
  killed. It also opens a third axis the estate's breadth mode lacks: query-channel pruning cuts
  KV READ volume (decode-time bandwidth), not just stored bytes. The sweep's own fit note says the
  same ("Dual-QK spends the budget on precision-and-channel shape instead of token count", sweep:38).
- Organ map: QUANTIZER organ. The port shape is already installed by the BreadthKV card
  (mag/state_quantizer.py:249-273 quantize_state breadth mode; bridge context knobs; card :39-40).
  The weight-side A/B harness ran TODAY on the Ollama path
  (watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md:1-5: qwen2.5:7b Q4_K_M vs q8_0,
  50 paired runs per arm, num_ctx 8192, on watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md),
  but per FIX 4 that harness cannot express a KV-precision arm without a knob byte-prove; probe 2
  below states the reachable paths honestly.
- Port boundary, honest, sharper than the sweep's: the sweep verdict "CUDA/SGLang only: not a
  local steal, a grammar row" (sweep:38) is right about the KERNEL (paired transforms need custom
  kernel support; llama_cpp 0.3.36 exposes only stock GGML KV types, re-verified round 1 and by the
  critique this sitting: type_k and type_v parameters present, enums GGML_TYPE_F16, GGML_TYPE_Q8_0,
  GGML_TYPE_Q4_0 available). And the box-side offload half is already double-sourced non-steal (no
  Vulkan/Windows KV offload in the literature sweep, sweep:60; llama.cpp b11465-b11475 deltas
  Metal-specific, watch/inbox/frontier_olm_2026-10-08/lens/burns.md:93-94). But the PREMISE
  underneath is locally testable and untested: is KV read volume even a bottleneck at the 8192
  envelope? The banked prior says maybe: B4 measured q8_0 decode 100.8 vs f16 55.9 t/s on this
  estate (watch/inbox/frontier_olm_2026-10-06/lens/burns.md:59), but that was a one-off sweep
  number, never re-run with task-level scoring, and the Q5 instrument law
  (watch/inbox/frontier_olm_2026-10-06/sweep/kv-context-engineering-arxiv.md:57, FIX 1) forbids
  accepting it without end-to-end task probes.

## Overlap receipt (commands run round 1, re-run clean by the critique this sitting)

- `git grep -n -e "2609.26219" -e "2610.09827" -- catalog/catalog.jsonl` returned EXIT=1, zero rows
  (round 1 run; critique re-run this sitting, same result): neither paper is in the catalog; both
  live only in today's sweep card. Consistent with both finds' overlap notes.
- The same-nickname collision is real and stays named: catalog/catalog.jsonl:1073131 (id
  0a2ff2bf37b5, .../frontier_olm_2026-10-03/sweep/_raw/2609.39329v1.html) and :1073132 (id
  50607bdce433, same dir 2609.39329v1.txt, title "PatchKV: Weight-Space Compensation of KV
  Cache"), raw-held 10-03. Different paper, different arXiv ID.
- The "xAI prefix-break grammar" phrase originates in today's sweep :29 ("the grammar the estate
  holds from xAI's vendor docs") and lens/questions.md:300; it is ask-and-sweep vocabulary, not a
  separate banked holding.
- BreadthKV positioning: catalog/catalog.jsonl:1195479 (id a65c50a1a541) is the 10-06 BreadthKV
  steal card row. Dual-QK sits BESIDE that axis (precision-and-channel shape vs token count), not
  over it.

## Probes

Probe 1 (the card probe; discharges the sweep's own OWED row "per-ask token measurement of the
estate's own injection paths is a repo audit this sweep could not run from the outside", sweep:69;
zero GPU cost, rides instruments that exist):

- Instrument: tools/prefix_cache_sim.py (365 lines; radix-leaf LRU simulator, RadixAttention
  lineage semantics per its docstring :1-13, G1 law anchored at memory/research_polished/kv_cache_compaction.md:13)
  driven by tools/lru_null_arm.py (265 lines), whose serving model renders estate-style packs
  (frozen prefix via freeze_system_prompt, mag/context_pack.py:948 per FIX 3 - the tool's own :29
  header says :467-526 and is STALE, flagged above - plus an append-only tail) over real trail
  tapes: 12 lanes on disk under dashboard/static/trails/ (counted this sitting, `ls | wc -l`).
  Drift guard (FIX 2 consequence): probe step 0 re-diffs the copied CLIP_SUFFIX constant
  (tools/prefix_cache_sim.py:36) against the live executable clip (mag/context_pack.py:1970) and
  aborts the probe on mismatch, so rendered packs cannot silently diverge from real pack clips.
- Measurement: over one week of trail tapes, diff each rendered session prompt against its
  predecessor and classify every resume point as (a) clean append (first divergence at the tail) or
  (b) mid-pack mutation (first divergence before the last-appended row: a re-render, a shed fold or
  restore, a world_state/warm_state injection change). Report the share of resume points in class b
  and the recomputed-token fraction they carry.
- Prediction (pinned, falsifiable): under the byte-identical law plus P5 reversible sheds, mid-pack
  mutations are rare and shallow: under 10 percent of resume points, under 10 percent of replayed
  prefill tokens. Falsifier: 20 percent or more of resume points carry mid-pack divergence covering
  half or more of the session's tokens. M1 disposition for the gray band: 10-19 percent of resume
  points is INCONCLUSIVE - no port decision either way; the probe then re-runs with per-mutation
  source attribution (which ask-path surface mutated: world_state, warm_state, brief, shed) before
  any claim is filed. If the falsifier fires, PatchKV has real estate surface and the shed recipe
  journal becomes its drift model for free; if the prediction holds, find 1 stays a grammar row
  with a measured constant (2.51-3.85x) attached for the day the context cap lifts, and the
  estate's discipline laws are vindicated with its own numbers. Either outcome banks.

Probe 2 (Dual-QK premise at the envelope; one evening of model runs; serving path pinned per FIX 4):

- Step 0, pin ONE serving path by name: byte-prove whether the installed Ollama exposes a
  KV-cache-type knob for /api/generate (env or request field; version + observed behavior, not
  docs-memory). IF the knob byte-proves, the probe rides run_ab.py's own path (Ollama, num_ctx
  8192, same 50 paired tasks) and its numbers pool with the RECEIPT baseline and burns.md:59. IF it
  does not, the probe runs ENTIRELY in-process on llama_cpp 0.3.36 (type_k/type_v; enum support
  verified round 1 and by the critique: F16/Q8_0/Q4_0 present) as a SELF-CONTAINED A/B with its own
  f16 baseline measured in the same sitting on the same path, and its numbers are declared
  NON-POOLABLE with the RECEIPT baseline, burns.md:59, and any Ollama-path row - different serving
  path, different kernels, different overheads. No arm ever mixes paths.
- Arms (whichever path step 0 pins): f16 vs q8_0 vs q4_0 KV cache, identical prompts, temperature
  0.0, paired seeds, num_ctx 8192. Readouts per the Q5 instrument law
  (watch/inbox/frontier_olm_2026-10-06/sweep/kv-context-engineering-arxiv.md:57, FIX 1):
  task-level completion, never perplexity, plus decode t/s per arm.
- Prediction: q8_0 KV reproduces the burns.md:59 direction (decode t/s above f16) at the 8192
  envelope with no task-level degradation; q4_0 shows where the BreadthKV collapse floor begins on
  this fleet. Falsifier: KV precision does not move decode t/s at 8192 (KV not the bottleneck at
  estate context lengths), or q4_0 completion collapses. Either way the Dual-QK port is priced: the
  first outcome makes the 2-bit cliff measurement the owed next step, the second confirms the
  sweep's grammar-row verdict with local bytes instead of a literature argument.

## OWED (stated, not filled)

- PatchKV full text unread (sweep:8 records the 60s html timeout for 2609.26219v1; sweep:29 says
  "twice" - M2: the sweep's own lines disagree on the count; unread either way). All PatchKV
  mechanism detail here is abs-page depth; the 1.26-2.06x CacheBlend comparison and the
  drift-model/precision-tag internals are abs-level claims, not full-text reads.
- Whether the installed Ollama exposes a KV-cache-type knob: unverified; probe 2 step 0 byte-proves
  it and the step's outcome selects the serving path.
- Dual-QK kernel port on Vulkan/llama.cpp: unknown, not asserted impossible; the non-steal verdict
  covers the offload stack, and the paired-transform kernel has no local implementation path today.
- Neither probe has been run yet; all numbers above are predictions or cited measurements, never
  run results.

## Citations

- https://arxiv.org/abs/2609.26219 and https://arxiv.org/abs/2610.09827 (abs pages fetched live round 1; titles, authors, dates, quotes corroborated by the round-1 critique this sitting)
- watch/inbox/frontier_olm_2026-10-08/sweep/kv-cache-context-engineering-arxiv.md:8, :28-29, :29, :34-35, :37-38, :38, :60, :67, :69 (all line cites verified by the round-1 critique this sitting)
- watch/inbox/frontier_olm_2026-10-08/lens/questions.md:300; watch/inbox/frontier_olm_2026-10-08/lens/burns.md:73-74, :93-94; watch/inbox/frontier_olm_2026-10-08/lens/laws.md:75-77
- watch/inbox/frontier_olm_2026-10-06/sweep/kv-context-engineering-arxiv.md:57 (Q5 instrument law, FIX 1)
- watch/inbox/frontier_olm_2026-10-06/steal/quantization-compression via x.md:8, :27, :39-40, :42, :55; watch/inbox/frontier_olm_2026-10-06/lens/burns.md:59
- watch/inbox/frontier_olm_2026-10-08/sweep/quant_ab/RECEIPT.md:1-5; watch/inbox/port_wave_20261007/QUANT_AB_SPEC_AMEND.md (existence verified); run_ab.py:34-36, :227 (Ollama-only path, FIX 4)
- catalog/catalog.jsonl:1073131 id 0a2ff2bf37b5 (sibling PatchKV 2609.39329 html), :1073132 id 50607bdce433 (same paper txt), :1195479 id a65c50a1a541 (BreadthKV steal card), :1071100 id 41f4600481f5 (BreadthKV abstract snapshot) (M3: id + path carried alongside moving-tree line numbers)
- watch/inbox/burn_wave_20260926/DOGFLOOD_METERS_20260926.md:17
- configs/lanes.yaml:30, :63; mag/llama_cpp_bridge.py:110-115, :127-128
- mag/context_pack.py:69, :108, :225, :326, :948 (freeze_system_prompt, FIX 3), :1970 (executable clip, FIX 2), :1416 (schema line only, FIX 2)
- tools/prefix_cache_sim.py:25 (from __future__ import, FIX 2), :36 (copied CLIP_SUFFIX constant), :128, :140 (provenance comments), :1-13 (docstring); tools/lru_null_arm.py:29 (STALE header, FIX 3), :1-35 (serving model); memory/research_polished/kv_cache_compaction.md:13 (per simulator docstring)
- commit 6685db6bc (P5 ReFold reversible sheds, P6 quant A/B spec, verified via git show round 1, confirmed by critique)
- Ran this sitting (FIX verification batch): sed/grep outputs quoted in Amendments; round 1's llama_cpp introspection (0.3.36, type_k True, type_v True, [GGML_TYPE_F16, GGML_TYPE_Q4_0, GGML_TYPE_Q8_0]) re-run clean by the critique
