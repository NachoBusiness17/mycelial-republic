# SWEEP: quantization-compression via arXiv (frontier_olm 2026-10-09)

source-fetched: 2026-10-09

Seat: sweep-quantization-compression-arxiv (dynamic workflow run, branch
mag/run-beta1-factory-build-audi-20260806T231709Z). Area card: the 4 questions in
watch/inbox/frontier_olm_2026-10-09/lens/questions.md, Area 2. House laws held: ASCII
only, no em or en dashes, every claim names what was fetched or run this sitting, quotes
are verbatim from pages I fetched myself.

## Doors and instruments (all run this sitting)

- arXiv export API door: GREEN all sitting, zero 403s, zero degrades. 4 API queries +
  8 abstract-page GETs, all via WebFetch, all plain https, no auth.
- Pass 1 queries (submittedDate 2026-09-09 to 2026-10-09, sortBy=submittedDate desc):
  1. all:"quantization" OR all:"quantized", cat cs.CL OR cs.LG, max 60: returned 32
     entries read.
  2. ti:"pruning" OR ti:"weight sharing" OR ti:"sparsity", same cats, max 40: returned
     35 entries read.
  3. all:"quantization-aware training" OR ti:QAT, max 30: returned 21 entries read.
  4. small/edge x quant/prune intersection, max 30: returned 30 entries read.
  Total listing entries read: 118; unique candidate items after dedup by arXiv ID:
  roughly 95, comfortably over the 30-candidate floor. Candidate list (IDs): 2610.12444,
  2610.12338, 2610.12004, 2610.11748, 2610.11482, 2610.11315, 2610.11245, 2610.11226,
  2610.11214, 2610.11115, 2610.10933, 2610.10738, 2610.10385, 2610.10381, 2610.10058,
  2610.09969, 2610.09877, 2610.09827, 2610.09346, 2610.09227, 2610.09212, 2610.09202,
  2610.09183, 2610.08164, 2610.07904, 2610.07853, 2610.07781, 2610.07767, 2610.07522,
  2610.07457, 2610.07197, 2610.07121, 2610.06817, 2610.06404, 2610.06026, 2610.05616,
  2610.04403, 2610.04093, 2610.03959, 2610.03389, 2610.03117, 2610.02951, 2610.02598,
  2610.02524, 2610.01554, 2610.01434, 2610.00426, 2610.00170, 2610.00000-range others
  (2610.08403, 2610.08884, 2610.08732, 2610.08174, 2610.00738, 2610.00412, 2610.00367,
  2610.06903), 2609.39223, 2609.37090, 2609.36860, 2609.36262, 2609.35579, 2609.35260,
  2609.34117, 2609.33977, 2609.33974, 2609.33889, 2609.33601, 2609.33550, 2609.33548,
  2609.33927, 2609.32539, 2609.32204, 2609.32197, 2609.32060, 2609.31932, 2609.31291,
  2609.30729, 2609.30465, 2609.30245, 2609.30037, 2609.29867, 2609.29029, 2609.28262,
  2609.26474, 2609.25498, 2609.24757, 2609.24391, 2609.24042, 2609.23974, 2609.23141,
  2609.21834, 2609.21145, 2609.20441, 2609.16689.
- Pass 2 deep reads (abstract pages fetched and read end to end, 8 total, one GET each):
  2610.07781, 2609.39223, 2609.32060, 2610.11226, 2609.33548, 2609.31291, 2610.00426,
  2610.04403 (the last as the one-GET re-verification the area card asks for).
- Banked items: 5 (7 deep-read candidates, 2 dropped on the overlap walk; see the
  correction log in the Items section). Sweep-level-only entries (2610.09212
  CurveTQ, 2610.09183 Q-PACE, 2610.08403 SSR, 2609.33601 JustQuant, 2610.00738 Q-MINO,
  2610.09202 CanonQ, 2609.33977 GroupMask, 2609.33889 sparsity crossover) are NOT banked:
  the ask banks only items I read myself.

## RQ1: did anything move small-model quality off the qwen2.5:7b Q4-vs-q8 TIE ceiling, or is Q4-at-ceiling the standing rule?

Answer: no PTQ result since 10-01 moves sub-8B quality off the Q4 ceiling, and the
frontier's real move this month is to RE-SCOPE the tie itself. Three findings, all from
pages I fetched:

1. The tie is instrument-scoped, not a law of nature. arXiv 2610.07781 (fetched
   https://arxiv.org/abs/2610.07781) runs 8-bit vs 4-bit on Llama-3.1-8B-Instruct and
   Qwen2.5-7B-Instruct (the estate A/B's exact artifact class) over twenty deterministic
   tool-failure-recovery tasks x five prompts, and finds the comparison flips direction
   with prompt and evaluation design: clean-task deltas range -50.0 to +35.0 points for
   Qwen; one scoring-policy change flips a Llama verdict from +28.3 to -15.0. Verbatim:
   "The 8-bit-4-bit recovery comparison changes direction across prompts and evaluation
   targets." and "one prompt, one screened task set, and one scoring policy do not
   establish a stable conclusion about quantized-agent robustness." This is the
   independent frontier statement of exactly what the estate's own A/B receipt admits:
   sweep/quant_ab/RECEIPT.md limitation 1, "CEILING-BOUND INSTRUMENT: 100% on both arms
   means the task set sits above both quants' competence floor and cannot discriminate
   near it" (read this sitting via the day-8 steal card's quotation of it, and the
   SUMMARY.json read confirms 50/50 both arms, per-task spread 0.0 pp).
2. The Q4-clean / Q2-cliff picture re-verifies byte-for-byte. arXiv 2610.04403 fetched
   today in one GET (https://arxiv.org/abs/2610.04403): all four claims on the day-8
   steal card CONFIRMED on the page, including "Q4_K_M remains lexically clean at >=1B."
   and "Tokenizer vocabulary size does not predict the damage (Spearman rho=0.12);
   parameter count dominates (rho=0.72), confirmed within five of six same-tokenizer
   families." So the standing rule holds where the estate actually pins: gemma:2b Q4_0
   and qwen2.5:7b Q4_K_M sit in the clean regime; the cliff is at Q2 on sub-2B artifacts.
3. The ceiling is a PTQ ceiling, and training moves it, above 8B. arXiv 2609.39223
   QATFactory (fetched today; ALREADY BANKED by the day-1 sweep as its item 1 and
   deepened day-2 as abstract-depth v2, so this is a confirmation re-read, not a new
   bank) reports QAT/distillation in the deployment formats directly:
   Qwen3.5-9B QAD reaches 68.9 percent average accuracy under NVFP4 and 66.0 under MXFP4
   versus best-PTQ 65.4 and 56.4 (a +9.6 lift on MXFP4), with llama.cpp Q4_K as a
   first-class export target. Verbatim: "QATFactory simulates deployment-time quantization
   while performing matrix multiplications in BF16, allowing models to adapt to
   quantization noise without requiring training hardware that natively supports the
   target format." Theory side: arXiv 2609.32060 (fetched; named but never read at the
   day-2 sweep's candidate list, so this is the first estate deep read) derives the precision floor
   from a single full-precision quantity (predictive amplification G; the floor
   eta_c = Lambda/G with G^2 growing linearly in depth) and names a QAT paradox:
   "noise-aware training roughly doubles the tolerable noise of shallow networks, but
   the gain decays with depth." Residual branches scaled 1/sqrt(D) with pre-norm remove
   the depth penalty entirely.

Verdict for the estate: Q4-at-ceiling stands as the PTQ operating rule for janitor-class
(1B to 8B) artifacts, now with (a) an independent robustness caveat that any future
Q4-vs-q8 verdict must vary prompts and scoring before it is called a law, and (b) a
frontier-corroborated discriminator channel (rare-word definitional hit-rate) already
specced on the day-8 card. The rule is not metaphysical: it is a property of
training-free quantization, and QAT lifts 4-bit where a training budget exists.

## RQ2: which QAT / LoRA-on-quantized methods fill UNMEASURED grid cells without breaking T0/T1 local-first?

Two families, both read this sitting:

- QATFactory (2609.39223): open framework, NVFP4/MXFP4/Q4_K aware, exports straight to
  vLLM, needs only BF16 matmul training hardware. Held since day-1 (sweep item 1) and
  day-2 (abstract-depth v2), so the note here is census, not a new bank. Gap it leaves: its smallest evaluated
  model is Qwen3.5-9B and its stated range is 8B to 230B, so the janitor-tier cells
  (2B to 8B) remain unmeasured BY IT. OWED probe: run its Q4_K recipe on a 7B-class
  artifact and A/B against the frozen quant_ab pin contract. This is the one training
  method that speaks the estate's exact quant dialect (Q4_K is the llama.cpp family the
  janitor tier already runs).
- TerMeZO (2609.33548): fine-tunes already-ternary BitNet models of 1B to 3B parameters
  with sparse zeroth-order optimization that exploits the {-1,0,1} quantizer geometry to
  pick which latent weights to update, forward-pass only. The day-4 sweep named this
  paper a Pass-1 lead and explicitly owed its abstract fetch to the next window; today's
  read discharges that debt. Verbatim: "TerMeZO matches or
  exceeds the performance of full-parameter MeZO while substantially reducing the
  fine-tuning memory footprint." This is LoRA-on-quantized's edge cousin and it sits
  squarely inside the T0/T1 local boundary (no backprop memory, no cloud).

Sweep-level (not banked, named for the grid census): Q-PACE 2610.09183 (mixed-precision
allocation during QAT), Q-MINO 2610.00738, JustQuant 2609.33601 (4-bit activations with
plain operators), QAR 2609.21834. None read beyond listing gists this sitting.

## RQ3: of the day-8 mine's 6 unbanked cards, which carry quantization claims re-verifiable in one GET through the green arXiv door?

Exactly 1 of 6: the quantization-compression via hn card, anchored on arXiv 2610.04403.
Evidence run this sitting:

- The 6 cards are in watch/inbox/frontier_olm_2026-10-08/steal/: finetuning-adaptation,
  inference-efficiency-hn, kv-cache-context-engineering, open-local-models,
  open-local-models via reddit, quantization-compression via hn (dir listing, this
  sitting).
- arXiv-ID extraction over all 6 cards (grep -o -E over the .md files): the
  quantization card cites 2610.04403 only. The other cards' anchors are non-quant:
  finetuning-adaptation rides 2610.06851 (16 mentions), kv-cache rides 2609.26219,
  2609.39329, 2610.02766 and 2610.09827 (the last is Dual-QK, 2-bit KV: quantization-
  adjacent but a cache claim, not a weight-quant claim), open-local-models rides
  2610.09111, 2610.09772, 2610.09633, 2610.06204 (model-release claims, HF/Ollama-door
  verifiable, not arXiv), and inference-efficiency-hn cites no arXiv IDs at all.
- The one-GET re-verification (this sitting, https://arxiv.org/abs/2610.04403): claim
  (a) Q2 sub-2B semantic dissociation CONFIRMED ("Three regimes emerge at Q2: total
  collapse into unusable builds, severe semantic dissociation in sub-2B models, and
  mostly robust preservation above about 3B."); (b) param-count dominance CONFIRMED
  (rho=0.72 sentence above); (c) Q4_K_M clean at >=1B CONFIRMED verbatim; (d)
  build/provider dependence CONFIRMED ("The damage is frequency-graded,
  provider-dependent, and not calibrated by WikiText-2 perplexity: across nine
  artifact-matched ladders, near-identical Q2 penalties (44.7%/47.6%) separate an
  artifact keeping its definitions (3.6%) from one losing them (43.6%).").
- Unbanked status is a LEDGER-writer gap, not a discovery gap: memory/burns/LEDGER.jsonl
  read this sitting at 14 rows matching "quant", and per lens/burns.md the file is
  705 lines / 571,821 bytes, byte-frozen since 2026-10-07 with max ts 2026-09-28. The
  day-8 card's own overlap section states the paper is already held at sweep level
  (day-6 DIGEST.md:92 refetch; day-8 sweep 223-230), so this re-verification upgrades
  nothing except confidence: carried numbers became page-verified numbers.

## RQ4: weight-sharing and pruning for sub-8B the corpus library does not already hold

- Shelf census run this sitting (grep -o over catalog/catalog.jsonl titles, pattern
  quant|prun|compress|QAT|LoRA|weight.shar|bitnet|ternary|4-bit|low.bit, 60 displayed):
  the catalog holds quantization-adjacent titles (Align Then Correct, Differentiable
  Bit-Widths, OnlineQAT, Capability Scaling-Down Laws for LLM Compression, Behavioral
  Capacity Certificates for Quantized Language Models, Anosognosia in LLMs, Baseline
  Shape Decides the Verdict ternary re-examination) and pruning-adjacent titles (Beyond
  Truncation ensemble pruning, Artificial Structure Function Search structured pruning).
  No slimmable or width-sharing title appeared in the hits.
- NEW this sweep: IrekoGPT (2610.00426, fetched): converts pretrained LLMs into
  post-hoc slimmable models, one weight set serving nested widths, built on SliceGPT
  with projections retained unpruned, per-layer calibration across compression ratios,
  gradient-free ridge correction downstream; tested on Llama and Qwen families; code at
  github.com/aimagelab/IrekoGPT. Abstract carries no numbers beyond "preliminary results
  show improvements over naive PCA-based slimming, with the largest gains at high
  compression" - early-stage, which is exactly why it is cheap to adopt early. This
  fills the weight-sharing cell: one artifact, many widths, no per-width store.
- Companion small-LM find: Softmax Reparameterization for Output-Head Quantization
  (2609.31291, fetched; present estate-side only as a raw 09-28 cache and listing-level
  mentions, day-6 census counted 0 catalog hits): output heads dominate small-LM
  inference cost; a pre-quant
  reparameterization (subtract a scalar multiple of each vocab-row mean, chosen by
  validation KL) drops test KL 93 percent on XGLM under RTN and 73 to 77 percent on
  Phi/BLOOM/BLOOMZ under activation-weighted MSE, and a packed W4 Phi head cuts
  batch-one generation latency 10.8 percent. No retraining. This is a janitor-tier
  serving lever the library does not hold.

## Items banked (strongest first; overlap ledger inline)

CORRECTION LOG (this sitting, after the deep overlap walk): my first draft listed 7 items
including 2610.07781 and QATFactory as new finds. The per-ID watch/inbox walk proved both
were already banked: 2610.07781 carries a full day-7 treatment (register.jsonl confirmed-
find row with the same verdict quote, a steal card "Steal 1 (primary): the A/B design
rules, not a number", and a sweep deep-read "abs + full HTML"), and QATFactory was the
day-1 sweep's item 1 plus a day-2 abstract-depth v2. Both are dropped from the bank list
below; re-banking known work is waste. Banked items fall to 5.

1. 2610.11226 When Lower Reconstruction Loss Hurts: Distributionally Robust Refinement
   for Low-Bit LLM Quantization (fetched https://arxiv.org/abs/2610.11226). Overlap: no
   watch/inbox, catalog-title, or state/arxiv holding of this ID anywhere (per-ID grep
   run this sitting); the only "Reconstruction Loss" catalog row is a DIFFERENT work,
   raw cache state/arxiv/2026-10-02/2610.00983v1.txt ("The Devil Is in the
   Reconstruction Loss Scale", a same-theme cousin from 10-02, never analyzed either).
   memory/trajectory/steps.jsonl matches are sibling-seat grep-command traces, not
   holdings.
2. 2609.33548 TerMeZO (fetched). Overlap: named three times but never read - the day-4
   sweep lists it as a Pass-1 lead with "abs pages not fetched" and an explicit
   "2609.23587, 2609.22870, 2609.33548 abs fetches owed next window"
   (frontier_olm_2026-10-04/sweep/quantization-and-compression-arxiv.md:102,234,245);
   it also appears in the 09-30 x-lane sweep and the 10-03 finetuning sweeps at listing
   level only. This sitting's deep read discharges the day-4 owed fetch.
3. 2609.32060 Depth Laws for the Precision Floor (fetched). Overlap: named in the day-2
   sweep's candidate enumeration ("2609.32060 Depth Laws precision floor",
   frontier_olm_2026-10-02/sweep/quantization-compression-arxiv.md:48) with no quote,
   no read, and no estate mapping; this is the first estate deep read.
4. 2610.00426 IrekoGPT (fetched). Overlap: the per-ID grep hits ONLY this file; zero
   catalog rows, zero state/arxiv stash entries, zero prior sweeps. The one fully
   unmined item of the batch.
5. 2609.31291 Softmax Reparameterization for Output-Head Quantization (fetched).
   Overlap: raw cache state/arxiv/2026-09-28/2609.31291v1.txt (mtime
   2026-09-28T06:30:26Z) plus listing-level mentions (09-30 open-and-local sweep, 10-03
   _raw candidates, day-6 sweep overlap census "Softmax Reparameterization
   (2609.31291, 0)" counting 0 catalog hits); never deep-read before today.

Explicitly NOT banked as new: 2610.07781 (day-7 register + steal + sweep; my re-read
independently reproduced its verdict quote), 2609.39223 QATFactory (day-1 item 1, day-2
v2), 2610.04403 (day-6 DIGEST.md:92 + day-8 sweep + steal card; re-verified today, see
RQ3), 2610.09346 OnlineQAT, 2610.08164 Align Then Correct, 2610.06026 Differentiable
Bit-Widths (all three already in catalog titles). Re-banking known work is waste.

## Checks run / not run this sitting

- Ran: 12 WebFetch GETs (4 API queries + 8 abs pages), all arXiv door, zero failures.
- Ran: catalog title greps (two pattern sets), state/arxiv stash census (35 dated dirs,
  per-ID absence checks for the 6 new IDs), day-8 steal-card arXiv-ID extraction, day-8
  quant_ab SUMMARY.json read, day-1 DIGEST head read, lens questions/burns/corpus/doors
  reads, memory/burns/LEDGER.jsonl "quant" count (14).
- Ran (background, completed): memory/ recursive grep for the 6 title fragments; all 3
  hits are process traces and coincidences, not holdings: memory/trajectory/steps.jsonl
  carries sibling seats' grep COMMANDS naming QATFactory / TerMeZO / IrekoGPT / Tool-
  Failure Recovery / Softmax Reparameterization (one step already read "== catalog:
  QATFactory == 0"); the "Precision Floor" hits in memory/research_packs/
  20260808T154500Z_warning-signal-classification-research-project.md (2026-08-08,
  predating the paper) and memory/runs/quote_audit_wide_20260925/packs_concat.txt are
  fragment coincidences in unrelated text. Per-ID watch/inbox walk (background,
  completed): 2610.07781 held day-7 register/steal/sweep; 2609.39223 held day-1 + day-2
  sweeps; 2609.33548 named day-4 (owed fetch), 09-30, 10-03; 2609.31291 cache + 4
  listing mentions; 2610.00426 only this file; 2610.11226 only this file.
- Not run: no pytest, no fresh Ollama A/B, no ledger write (no writer instrument exists
  per lens/burns.md), no corpus FTS queries, no re-verification of inherited sweep
  payloads beyond what is stated above.

## Post-write scan receipt

Command: .venv/Scripts/python.exe byte scan of this file (non-ASCII lines + em/en dash
counts), 2026-10-09. Output: bytes 15012 (pre-correction draft), nonascii_lines [],
emdash 0, endash 0. A rescan after the correction log edits is owed to the fold if more
edits land; the scan instrument is the same one the lens file used.
