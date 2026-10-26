# STEAL CARD: quantization-compression (frontier_olm 2026-10-07, round 2 REVISE applied)

Round 1 carried one false evidence claim and one selective-attribution gap; both re-verified
against bytes THIS sitting and fixed here: (1) the qwen3 8B-instruct manifest pull FAILED
(manifest_qwen3_8b-instruct.json and manifest_qwen3_8b-thinking.json are
{"errors":[{"code":"MANIFEST_UNKNOWN"...}}]} registry error bodies, head-checked this
sitting; the round-1 port cited 8b-instruct as in-hand substrate, false); (2) the 17.5/28.3
screening reversal and the strict-parse flip are LLAMA-under-one-prompt numbers, and the
paper's own datum at the estate's exact model (Qwen, "essentially unchanged" under strict
parsing) is now stated as the prior against probe prediction 2. Minors fixed in the same
pass: sweep re-bank credited, percolator path disambiguated, 09-30 shorthand expanded to
full paths, lanes.yaml scope corrected (worker pin :37; the probe's qwen2.5:7b-instruct is
not pinned in lanes.yaml at all). Card JSON banked beside this md per the 10-03 convention
(watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.json, on disk).

Seat: steal-quantization-compression gopher. Both finds verified against the on-disk
feed-stage abstracts (state/arxiv/2026-10-07/2610.07781v1.txt:6 and
state/arxiv/2026-10-07/2610.08164v1.txt:6, quotes grep-confirmed 1-hit each this sitting);
full-text numbers are carried from the sweep seat's end-to-end HTML read
(sweep/quantization-compression-arxiv.md:26-37, honesty :85), not re-fetched here (OWED).

## Estate overlap (verified this sitting, not taken from the find's word)

- `grep -c "2610.07781" catalog/catalog.jsonl` = 1; `grep -c "2610.08164" catalog/catalog.jsonl` = 1.
  Both hits are raw feed-stage fetch rows only (catalog/catalog.jsonl:1195121 and :1195175,
  each pointing at state/arxiv/2026-10-07/<id>v1.txt, zone lsa).
- `grep -rn` over watch/inbox *.md for both IDs = exactly one prior file: this round's own
  sweep receipt (sweep/quantization-compression-arxiv.md, items 1-2). Zero prior curated
  banks. Unmined before this sweep: CONFIRMED.

---

## Steal 1 (primary): the A/B design rules, not a number (arXiv 2610.07781)

Source: https://arxiv.org/abs/2610.07781 (Yuhe Hu, 2026-10-06, NeurIPS 2026 SLM-Agents
workshop, 7 pages; sweep read abs + full HTML end to end, sweep:27-28).

Verified quote (state/arxiv/2026-10-07/2610.07781v1.txt:6): "The 8-bit-4-bit recovery
comparison changes direction across prompts and evaluation targets."

The mechanism stolen: at exactly the estate's owed pair (Qwen2.5-7B-Instruct served via
llama.cpp at GGUF Q8_0 vs Q4_K_M, naming per the sweep's full-text read at sweep:28; the
abstract alone says only "8-bit and 4-bit variants"), a quant A/B is not a measurement
until four design choices are pinned, because each can flip the verdict alone. Every number
below is tagged with its model:
1. Prompt (QWEN datum): matched-task deltas across the 5 prompts ran +8.3 / -3.3 / -10.0 /
   -50.0 / +35.0 points, and the only two CIs excluding zero favor OPPOSITE precisions
   (sweep:30; series is sweep-carried, the -50.0/+35.0 endpoints abstract-verified).
2. Task screening (LLAMA datum, one prompt): "For Llama under one prompt, scoring each
   variant only on its own clean-passing tasks favors 4-bit by 17.5 points; scoring the
   same tasks for both variants gives no difference, while scoring the full pipeline
   favors 8-bit by 28.3 points" (verbatim, txt:6). The abstract gives no Qwen counterpart
   for the screening swing.
3. Parsing policy (LLAMA datum, one prompt): rescoring the SAME logs with strict output
   parsing flips that +28.3 to -15.0, "which 8-bit Llama violates far more often than
   4-bit Llama under that prompt... while leaving Qwen essentially unchanged" (txt:6). So
   the existence proof that the parse channel can reverse a verdict is Llama-side; at the
   estate's exact model the paper's own prior is FLAT.
4. Uncertainty unit: tasks, not injected fault sites (txt:6, closing sentence).
The paper's own conclusion is the steal: "one prompt, one screened task set, and one
scoring policy do not establish a stable conclusion about quantized-agent robustness"
(txt:6).

Organ fed: the QUANTIZER organ's weights side (mag/auto_quantize.py:1-24 is analytics-only,
so the weights-side gate lives in the steal/percolator paper trail) and through it the
GOPHER FLEET local tier, whose model pins sit in configs/lanes.yaml (gemma:2b janitor pins
:31-33, qwen2.5-coder:7b worker pin :37) behind the RX 5600 XT 6GB envelope at
configs/lanes.yaml:28. Scope note (round-2 fix): the probe substrate qwen2.5:7b-instruct is
NOT pinned in lanes.yaml at all (grep this sitting: qwen2.5 appears only as
qwen2.5-coder:7b, lines :29/:37/:67).

Concrete port move: the owed qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B (UN-RUN, this
round's lens/burns.md:97 and :218; instrument spec held at
watch/inbox/frontier_olm_2026-10-03/DIGEST.md:224 and re-owed at :274) must be AMENDED,
not fired as specced: >=5 prompt phrasings per task; the deployment verdict = full-pipeline
success over ALL tasks; matched-task (per-prompt clean-intersection) deltas reported as the
diagnostic, never the headline; strict-parse success banked as its own channel; per-task
spread reported. Plus the same sweep's export-cast rider (item 6, sweep:60, arXiv
2610.07853): hash the exact GGUF artifact and pin the conversion toolchain, or the ladder
measures the exporter. The gate also lands on any future quant drop into the lanes.yaml
model pins (janitors :31-33, worker :37): no single-prompt score promotes a quant (extends
the 10-03 Q4_K_M floor gate,
watch/inbox/frontier_olm_2026-10-03/percolator_candidates.jsonl:3).

## Steal 2: training-free rank-r compensation, the protected-spine alternative at estate scale (arXiv 2610.08164)

Source: https://arxiv.org/abs/2610.08164 (Song, Lee, Lee, Choi, 2026-10-06, 17 pages;
sweep read abs + full HTML end to end, sweep:34-37).

Verified quote (state/arxiv/2026-10-07/2610.08164v1.txt:6): "it recovers 51% and 84% of
the gap to FP16, versus 31% and 63% for the strongest baseline". Same line verifies
the WikiText-2 numbers: 2-bit QuIP# 12.43 -> 10.26 on Qwen3-8B, 21.11 -> 13.22 on
Qwen3-4B.

The mechanism stolen: two closed-form stages, zero training (txt:6). Stage 1 aligns each
layer's output with the FP16 model under a Fisher-weighted ASYMMETRIC objective (symmetric
calibration makes the compensation target inherently high-rank, so the rank budget captures
little); stage 2 re-measures statistics on the compensated model and takes one
rank-constrained natural-gradient step absorbing the first-order signal every prior
compensator drops. Every adapter is one truncated SVD; backward passes only collect
statistics. Stage 2 needs just 8K calibration tokens; overhead is a rank-64 adapter per
linear, 264-349 MB per set on 8B; no code released (all body numbers sweep:37, carried).

Organ fed: the QUANTIZER weights side again, but by a different axis than the estate's
protected-spine law: the 09-30 bank holds "protection budgets beat uniform at extreme
bits" (VeriLoop IQ1_M protected spine,
watch/inbox/frontier_olm_2026-09-30/sweep/quantization-compression-hn.md:43; RQ2 consensus
this round at sweep:71). Round-2 credit fix: the sweep ALREADY lists "closed-form adapter
compensation (Align-Then-Correct, no code)" in the RQ2 consensus (sweep:71) and already
carries the 51%/84% vs 31%/63% datum (sweep:36); this card's increment is ONLY the
protected-spine-ALTERNATIVE framing: instead of spending PRECISION on protected tensors,
spend RANK beside all frozen tensors, a second measured candidate for the estate's
extreme-bits question at its own 4B-8B scale. And the SOVEREIGN MIRROR's persistence lane
already states this paper's law in weight space: mag/lora_pipeline.py:19-21 ("the adapter
is the increment, the base model is the state, and QLoRA 4-bit is the quantized base state
under a low-rank delta"); LQEC is the training-free closed-form realization of that exact
delta (the estate trains it with gradients at mag/lora_pipeline.py:25-27; no ghost-adapter
artifact exists yet, memory/training/lora/ holds only formatted_data.jsonl +
train_ghost.py, checked this sitting).

Concrete port move: (a) bank ONLY the framing delta above into the RQ2 row (the listing
and datum stay credited to sweep:36/:71); (b) arm the WATCH TRIGGER pattern the pipeline
already has (mag/lora_pipeline.py:15-17 arms on HF appearance): watch for an
Align-Then-Correct code release (none today, sweep:37); on release, the replication
substrate status is, head-checked this sitting: Qwen3-4B manifests REAL (base, instruct,
thinking: manifest_qwen3_4b.json, manifest_qwen3_4b-instruct.json,
manifest_qwen3_4b-thinking.json, all docker v2), Qwen3-8B BASE manifest REAL
(manifest_qwen3_8b.json), Qwen3-8B-INSTRUCT NOT IN HAND (manifest_qwen3_8b-instruct.json
and manifest_qwen3_8b-thinking.json are MANIFEST_UNKNOWN error bodies; the 8B-instruct tag
is unresolved, a failed pull, not an uninspected rung). Stage-2 calibration (8K tokens)
fits estate usage ledgers by orders of magnitude. Until code exists, replication is a
port-of-math project, not an install; nothing is asserted servable.

---

## Falsifiable probes (cheap, this week; both specced, NOT run)

THE probe (Steal 1; the standing debt fired with the stolen design rules): run the owed
A/B with the amended instrument. Arms: on-box qwen2.5:7b (Q4_K_M, digest 845dbda0ea48,
watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.md:11) vs
qwen2.5:7b-instruct-q8_0 (library-verified 8.1 GB pull,
watch/inbox/frontier_olm_2026-10-03/percolator_candidates.jsonl:3). Shape: 10
deterministic tool-failure-recovery tasks x 5 prompt phrasings via /api/generate,
temperature 0, identical caps; score full-pipeline success (deployment number),
matched-task deltas (diagnostic), strict-parse violations (own channel), per-task spread.
PREDICTIONS: (1) the pooled verdict sign flips across at least 2 of 5 prompts or the
matched-task range exceeds 20 points (QWEN-side paper datum at this exact model+quant
pair: -50.0 to +35.0, sweep:30; endpoints abstract-verified); (2) strict-parse violation
rates differ between arms. Prediction 2 is stated with its honest prior: the paper's
existence proof for a parse-channel verdict flip is LLAMA-side (8-bit Llama violated far
more often, +28.3 to -15.0, txt:6) while at QWEN, the estate's exact model, strict parsing
left results "essentially unchanged" (txt:6), so the expected case per the paper is FLAT
and the channel is banked as a rider unless it fires. FALSIFIERS: (1) all 5 prompts agree
in sign with per-task spread under 20 points, which kills the multi-prompt rule as dead
weight at janitor scale on our task mix and banks the first stability datum AT ODDS with
the paper; (2) parse rates equal (the paper-expected Qwen outcome), demoting the pinned
parsing channel to a logged rider. Either way the four-lane-re-owed debt (10-03
DIGEST.md:224, :274) discharges with an instrument that cannot manufacture a verdict by
design. Cost: $0 plus one 8.1 GB pull, one afternoon, 50 runs per arm, hardware already on
box.

Secondary probe (Steal 2, minutes, $0): extend mag/gguf_cartography.py's census (pure-
stdlib GGUF parser, mag/gguf_cartography.py:1-8) over the on-box qwen2.5:7b blob to
compute exact rank-r adapter byte cost (r = 8/16/64) across parsed linear tensors, and
check it against the configs/lanes.yaml:28 envelope minus Q4_K_M weights (4.7 GB) minus
8k f16 KV (KV bytes computed from blob metadata: n_layers, n_kv_heads, head_dim; not
asserted here). PREDICTION, parameterized: the paper's rank-64 set (264-349 MB at 8B,
sweep:37; proportionally less at 7B) still fits the 6GB envelope at CONTEXT=8k, so the
paper's exact operating point is servable on the estate box. FALSIFIER: over envelope, in
which case the adapter rung ships at rank <= 16 or moves to the 4B substrate (manifests
real, above), and whether gains survive at reduced rank is OWED (no code, no rank
ablation banked anywhere).

## OWED / not verified

- This seat verified the two abstracts on disk (both txt:6) only. The full-text numbers
  (per-prompt series +8.3/-3.3/-10.0/-50.0/+35.0 with its CIs, screened rates 43.3 vs
  90.9, FP16 9.73 / 13.64, rank-64 264-349 MB, 8K calibration tokens, the no-code
  verdict, and the llama.cpp/Q8_0/Q4_K_M GGUF naming) are carried from the sweep seat's
  end-to-end HTML read (sweep:28-37 with honesty :85), not re-fetched by this seat.
- Both probes are specced, NOT run this session; the burns ledger owns firing.
- No trained LoRA adapter exists (memory/training/lora/ holds data + script only), so the
  lora_pipeline tie is law-text-level, not artifact-level.
- Qwen3-8B-instruct manifest: FAILED PULL (MANIFEST_UNKNOWN), tag unresolved; re-pull or
  tag correction owed before any 8B-instruct-scale replication claim. The four real
  manifests' quant rungs were not inspected.
- Align-Then-Correct ships no code; any estate replication is a from-paper port of the
  closed-form math, and nothing about its servability is asserted.

## Receipts (commands this seat ran, round 2 sitting)

- Manifest truth: head -c 120 over all six manifest_qwen3_*.json in this dir; 8b-instruct
  and 8b-thinking return {"errors":[{"code":"MANIFEST_UNKNOWN"...}]}, the other four
  return docker v2 schemaVersion 2 manifests.
- Quote re-verification: grep 1-hit each for both steal quotes in their txt:6 files, plus
  the verbatim "For Llama under one prompt..." screening sentence and 1-hit
  "while leaving Qwen essentially unchanged" (attribution fix 2).
- lanes.yaml scope: sed -n '34,40p' + grep -n "qwen2.5" (worker pin :37; qwen2.5:7b-
  instruct absent; matches :29/:37/:67 all qwen2.5-coder:7b).
- JSON convention: Read watch/inbox/frontier_olm_2026-10-03/steal/quantization-and-compression.json
  (fields area/steal/source_url/estate_map/probe/chars); this card's JSON banked beside
  the md in the same shape.
- Round-1 receipts still stand: catalog greps (1 and 1, rows :1195121/:1195175), watch/
  inbox *.md grep (one prior file, the sweep receipt), organ reads (mag/auto_quantize.py:1-24,
  mag/lora_pipeline.py:1-27, configs/lanes.yaml:28-34, AGENTS.md:30, lens/burns.md:97/:218,
  ls memory/training/lora/), prior-art reads
  (watch/inbox/frontier_olm_2026-09-30/steal/quantization-compression.md:36-73,
  10-03 steal card :11/:55/:65, 10-03 DIGEST.md:49/:224/:270/:274,
  watch/inbox/frontier_olm_2026-10-03/percolator_candidates.jsonl:3,
  this round's sweep receipt in full).
