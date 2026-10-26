# FRONTIER SWEEP: finetuning-adaptation via reddit (2026-10-11)

source-fetched: 2026-10-11

## Doors, honestly recorded

- Recipe door 1: `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` via curl -s:
  HTTP 302, 0 bytes; with -L it follows to `old.reddit.com/login/?reason=lor2` and
  returns the "Welcome to Reddit" login HTML, not JSON (DEGRADED). The WebFetch variant
  of the same URL timed out at 60s.
- Recipe fallback: WebSearch `site:reddit.com r/LocalLLaMA fine-tuning OR LoRA OR
  Unsloth October 2026` - the engine ignored the site: filter and returned Wikipedia,
  Spotify, and a non-reddit guide page. DEGRADED, unusable for thread discovery.
- Carrying door: the arctic-shift reddit archive
  (`https://arctic-shift.photon-reddit.com/api/posts/search` + `/api/comments/search`),
  the same fallback the 2026-10-10 adhoc sibling run used. HTTP 200 JSON all session.
  Door-side limits seen: 422 on partial-word/short-acronym title filters (RL, and one
  transient 422 on a valid full-word query), occasional 429 with retry backoff, and the
  `page` param returns 400 (unused; title queries carried the sweep). Instruments:
  `_ftr_sweep.py`, `_ftr_read.py` in this directory (hook-hardened per two Mimosa
  findings during authoring: pinned-host allowlist, alnum-only id validation, output
  path confined to this directory).

## Pass 1 (broad, last 30 days, 30+ candidates required)

17 title-query cells across r/LocalLLaMA, r/MachineLearning, r/LocalLLM, r/ollama
(LoRA, finetuning, fine-tuning, finetune, fine-tune, Unsloth, adapter, distill,
distillation, merging, test-time, training, RL, quantization-free, gradient) plus
score-ranked window pages (page param 400s, so window coverage rides the title cells).
Merged pool: 187 distinct posts (`_ftr_candidates.json`), 159 relevant after keyword
triage against the known-held id set. Requirement met by roughly 5x.

## Pass 2 (deep reads, end to end, 5+ required)

9 threads fetched as selftext plus full comment trees (`_ftr_read_*.md` here):
1x1fjrv (17c), 1wwk49n (12c), 1wyxukj (15c), 1widomo (32c), 1wybqq3 (5c), 1wvfz9n
(12c), 1wfo8xl (2c), 1wi9ebm (85c), 1wibfhj (9c). Read end to end by me: 1x1fjrv,
1wwk49n, 1wyxukj, 1widomo, 1wybqq3, 1wvfz9n, 1wfo8xl, 1wi9ebm. 1wibfhj fetched, NOT
read end to end. 1wi9ebm (Xiaomi MiMo 2.6 live training dashboard, 439 pts) read and
REJECTED as zeitgeist: spectatorship of a frontier lab burning $5-10/second, no
transferable mechanism; one comment-level lead kept below as unverified.

## Banked items (new, strongest first)

### 1. The ultimate guide to multi-harness RL (r/LocalLLaMA 1wwk49n, 2026-10-03, s=84, 12c)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wwk49n/the_ultimate_guide_to_multiharness_rl/
Author is Lewis (lewtun, Hugging Face post-training team), linking the guide at
huggingface.co/spaces/FineEnvs/multi-harness-rl (TRL + Harbor RL environments). The
load-bearing comment (Equivalent-Flan-1590, 9 pts): "overfitting to a single harness
format completely ruins a model's generalizability when you move it to a different
setup." Estate mapping: the JIT fine-tuning law's training set is a pitfall-bypass
corpus; this says the corpus must span harnesses/lanes or the weights bake one lane's
parsing and formatting habits. Direct input to the JIT-law dataset-construction clause
and to any future compost-ledger export.

### 2. Hierarchos-Native: Rust + Vulkan training backend, LoRA/PEFT, no CUDA (r/LocalLLaMA 1widomo, 2026-09-16, s=33, 32c)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1widomo/i_built_a_native_vulkan_training_backend_for_143/
Native Vulkan compute training stack: forward/backward, AdamW, LoRA/PEFT fine-tuning,
143 canonical transformer architectures (Llama, Qwen, Gemma, Mistral, DeepSeek, Phi,
OLMo, Granite...), SafeTensors interchange, developed and tested on AMD RDNA 3 (ROG
Ally). Verbatim: "If native training stacks like this can mature enough, there is
potentially room for ML training infrastructure that is substantially less tied to a
single vendor compute ecosystem." Estate mapping: the estate box is AMD RX 5600 XT
(RDNA1, gfx1010, RIB_GPU_LADDER_20261001.md:7-8) and the GPU ladder says ignore
DeepGEMM on it; this is a DIFFERENT ladder rung, a vendor-neutral local weight
adaptation lane that touches none of the five NVIDIA gates. Author's own caveats: not
a CUDA/PyTorch replacement, needs benchmarking and independent validation; RDNA3
tested, RDNA1 untested (probe OWED). Comment claims "Gemma4 support with complete
under 2e-7 logit parity" (author, 3 pts).

### 3. Catalyst: verified hypergradients over the whole training process (r/ollama 1wfo8xl, 2026-09-14, s=4, 2c)

URL: https://www.reddit.com/r/ollama/comments/1wfo8xl/50_ai_hyperparameters_500_training_steps_one/
Rank-2 LoRA fine-tuning compiled as one Rust function; 50 training-policy controls;
differentiates through 3 complete 500-step runs; independent verification at 2N+1 = 101
points with central differences; REFUSES the result when derivatives and the numerical
verifier disagree. One bounded update then improved 5/5 unseen seeds, held-out mean
validation loss -27.8%. Verbatim: "One small update, based only on sensitivities
measured across three development seeds, transferred positively to every stochastic
training seed that had been kept untouched." Two law-shaped nuggets: (a) "a
hypergradient from one training trajectory can partly be telling you something about
that trajectory" - the sensitivity map changed materially at 3 seeds (ema_decay went
near-irrelevant to #2); (b) the honest control: local random search at the same
objective-evaluation budget produced a LOWER final loss - the value is the sensitivity
map (17 of 50 controls carried 90% of elasticity; 23 near-zero), not the optimization.
CPU-only, 546s on one core. Zero traction thread, architecturally exact for the
estate's trust-bytes discipline: measure, verify independently, refuse, one bounded
move, held-out test.

### 4. MaRN: coefficient training attempt that failed its own baseline (r/MachineLearning 1x1fjrv, 2026-10-09, s=16, 17c)

URL: https://www.reddit.com/r/MachineLearning/comments/1x1fjrv/i_built_marn_a_pytorch_library_for_training/
PyTorch library optimizing a compact latent through a fixed orthogonal projection
instead of weights - the same coefficient-training shape unisub (arXiv 2512.05117,
unisub_drop_20261010) claims as an application. The comment tree caught it: 91.80% on
MNIST is linear-classifier territory ("92% accuracy on MNIST is what you get with a
linear classifier", 12 pts), and the author conceded: "update: you were right to point
it out, there was a bug, I'll be updating the OP, thanks." Commenter: "This idea is
very similar to LoRa, no?" Estate mapping: the caution datum for the unisub probe -
before believing any low-dim-parameterization result, gate on the plain-training
baseline on the same architecture; a plausible-looking compression number can be a
bug. Dead-salmon class, weight-space substrate.

### 5. Perplexity Decider 27B: open-weights decision-model finetune (r/LocalLLaMA 1wvfz9n, 2026-10-02, s=68, 12c)

URL: https://www.reddit.com/r/LocalLLaMA/comments/1wvfz9n/perplexity_decider_27b_open_weights_decision/
No selftext; category signal plus comment criticism. Top comment (fgk55555, 20 pts):
"Oof, needing to run prefill on 27B for a decision is going to be rough." Third
decision-model release named in-window (ImaJev sibling-held; comments also name
Cloudflare clef and liquid/d1, not open weight). Estate mapping: the estate's
decision-model meter rows (n>=40, OWED per frontier_olm_2026-10-11/lens/burns.md:242)
already encode the prefill-cost instinct; the market is converging on dedicated
decision models while the estate's own law says decisions want the small tier.

## Already held (verified this session, NOT re-banked; the dedup that mattered)

- 1wybqq3 (1.5B bash finetune, 400k synthetic) and 1wyxukj (trust a community
  fine-tune): my pass-2 reads CONFIRM the 10-08 run's bank
  (frontier_olm_2026-10-08/sweep/finetuning-adaptation-reddit.md:120-127,150-157)
  comment for comment, including the "most community made fine tunes perform worse
  overall than the base" prior and the Qwen2.5-Coder-1.5B SFT-gains observation. The
  catalog grep found them only as 10-08 raw scrape artifacts (catalog.jsonl ids
  0b5f237688f3, dda79ec97d2a); the analysis lives in the 10-08 bank. No new bank.
- Adhoc register reddit finds (MedGemma 1wywscq, MOLT 1wyvc8k, AgileRL 1wdjk0y), PCSS
  1wdhb24, Weyaxi verl handbook, and sibling-held 1wv05u1, 1wtqpjt, 1wsgrma, 1wu9zkn,
  1wgii3h, 1x1bdvl: excluded from banking up front via the adhoc register
  (frontier_olm_adhoc/register.jsonl, 8 finetuning-adaptation rows grepped this
  session) and the 10-10 adhoc sweep's already-held list.
- Overlap instruments: full-file grep of catalog/catalog.jsonl for 20 patterns and all
  9 thread ids (all 0 except the two 10-08 raw artifacts above); recursive grep of the
  four sibling olm run dirs for the bank candidates and key phrases (Hierarchos,
  multi-harness, MaRN, hypergradient, Catalyst): only scratch contact - 1widomo in
  adhoc/sweep/_tmp_a3.json (raw pool), 1wfo8xl in the 10-08 raw pool and the 10-09
  candidate list (frontier_olm_2026-10-09/sweep/finetuning-adaptation-reddit.md:16,
  listed as an r/ollama micro-thread, never analyzed), 1wwk49n in the 10-10 rss
  scratch (rss_s_multiagent.xml). All three analyzed and banked here for the first
  time. The full memory/ recursive grep was stopped for runtime (biography alone is
  577k rows); bounded greps covered memory/rib, the lens files, and knowledge_graph.
  This limitation is stated, not papered over.

## Research-question verdicts

RQ1 (8 confirmed finds vs the JIT fine-tuning law, lens/burns.md:104 and :153-154):
the law is now EVIDENCE-BACKED BY PROXY but with amendments, no longer pure operator
coinage. Count over the 8 adhoc rows: 5 REFINE (aTTT 2607.03441 runs the law's own
falsifier design on matched update text - in-context injection 49.3% scores BELOW the
50.7% no-TTT baseline while the same text as adapter update scores 54.3%; Agentic-TTT
2610.12002 supplies the gate the law implies and measures the overuse failure without
a compute penalty, the published twin of the 03:00Z drain law; MedGemma adds the
merge/serving verification clause - Unsloth effective-scale ~2x alpha/r, bf16 merge
rounding erases 17-37% of delta elements; DIAL-OPD and SGUID quantify the curation
half - token selection beats teacher scale, under 25% of retrieved skills carry
useful signal); 1 pushes back (DPPM 2610.11776: a frozen Doc-to-LoRA hypernetwork
beats Full Context and Mem0 on personalization benchmarks at 4B, against the law's
mapping-2 claim that retrieval wins at small scale - delivery-channel ordering is
regime-dependent, not universal); 2 RESTATE plumbing (MOLT, AgileRL). The estate's
OWN falsifier run (controlled pitfall-bypass corpus from the compost ledger vs
prompt-only on held-out pitfalls, fine_tuning_jit_law_20261010/CARD.md:43-45) has NOT
run, so the law is self-proven by nobody; it is externally corroborated, amended with
a serving-verification clause, a gate clause, and a regime caveat on mapping 2.

RQ2 (unisub vs lora_pipeline degree 5, lens/graph.md:22; GPU-ladder compatibility,
lens/laws.md:110): lora_pipeline's five invariants were verified this session by a
knowledge_graph.json edge dump (module:lora_pipeline.py has_invariant: adapter is the
increment / schema v1 / never upload training data / output is a LoRA adapter not a
full model / adapter reinforces the identity vector). Unisub's coefficient-training
application does NOT break any of the five - coefficients are still an adapter
representation and the card itself sizes the design change spec-class
(unisub_drop_20261010/CARD.md:44-49: GUILD MECHANIC spec-class, PROBE one evening,
falsifier = top-k principal directions of two public LoRA deltas must align better
than chance). The probe is SVD over adapter deltas, CPU-class, runs on this box
regardless of GPU ladder. Compatibility with "ignore DeepGEMM on this box": YES,
untouched - the five gates (RIB_GPU_LADDER_20261001.md:10-31) govern FP8/MoE serving
adoption on SM90+ NVIDIA silicon; post-training subspace math and a Vulkan LoRA lane
touch none of them. New from this sweep: Hierarchos-Native (item 2) is the first
in-window vendor-neutral LoRA training lane, i.e. the ladder's NVIDIA-only frame has
a second escape hatch - untested on RDNA1, probe OWED, and the MaRN episode (item 4)
says any such probe gates on the plain-training baseline first.

RQ3 (evidence threshold for a premium weight-adaptation turn under the descent
protocol's cheap-first leg, AGENTS.md:37): the 8 rows clear the PRIOR-ART-SWEEP leg -
they ARE it - and establish published mechanism evidence (aTTT matched-text +5
points; Agentic-TTT gate 0.256 to 0.510 utility; DPPM beating full context). They do
NOT clear the SHERPA cheap-first leg, because the estate-side baseline still does not
exist on disk. The threshold for a premium turn is therefore concrete: (1) the
compost-ledger pitfall-bypass corpus exported as a training set, (2) one local or
rented-GPU LoRA run under the lora_pipeline laws (local-or-rented-GPU, adapter
output), with the held-out pitfall differential vs prompt-only measured and the
serving/merge step probe-verified per the MedGemma clause, (3) only then a premium
turn, buying JUDGMENT on the result (grading whether the effect is real and whether
merge-scale loss is Unsloth's or the task's), never the training itself. A premium
weight-adaptation turn fired today would fail the descent protocol's own
spend-theater falsifier: cheap first, ~$0.001 local/deepseek baseline before any
$0.4+ ask.

RQ4 (Dead Salmons applicability, lens/burns.md:147-148): APPLICABLE, not pure
landscape - it names three concrete estate adaptation failure modes. (1) Phantom
pitfalls: a pitfall never detected under controls makes dead-salmon dataset rows;
this is the JIT-law card's own rider (fine_tuning_jit_law_20261010/CARD.md:30-31) and
SGUID's under-25%-useful number is its quantified version. (2) The ten-minute-self
fold-vs-prompt-only comparison (RIB_TEN_MINUTE_SELF_20261010 falsifier, via
frontier_olm_2026-10-11/lens/laws.md:107) needs the paper's negative-control arm -
a shuffled-bypass corpus and/or random-init model run - or a fold win is a plausible
explanation without a control. (3) Measurement-level dead salmon: MedGemma's
merge-scale loss went unseen until identity probes (7/7 vs 0/4) - the serving stack
silently eating a tune is exactly the plausible-looking-report disease, caught by a
control, not by a report. Already wired: the unisub probe falsifier and the
citation-lint PHANTOM-NUMBER parallel. OWED: wiring the mandatory negative-control
arm into the suppression-topology lane (operator GO pending) and into any fold
evaluation instrument before it fires.

## Considered and dropped (read, not banked)

- 1wi9ebm Xiaomi MiMo 2.6 live training dashboard (439 pts): zeitgeist, spectatorship;
  one comment-level lead (NandaVegg, 7 pts): GLM-5's paper reportedly describes final
  post-training as "creating many domain expert post-train variations and 'merged'
  them into one final model via synthetic datasets" - unverified against the paper,
  left as a lead, never asserted.
- 1wibfhj (MiMo post-training livestream): fetched, NOT read end to end.
- r/LocalLLM: zero relevant rows through every surviving title query this session -
  door-side under-sampling, same negative the adhoc run recorded.

## OWED (never asserted as done)

- Hierarchos-Native on RDNA1 (RX 5600 XT): untested anywhere in the thread; cheapest
  first instrument for any future weight-adaptation turn.
- The unisub probe (SVD overlap of two public LoRA deltas) still unrun.
- Catalyst repo github.com/lovettsendit/catalyst not independently verified:
  self-reported numbers, score 4, no external replication in the comment tree.
- Decider 27B: no eval table exists in-thread (no selftext); banked as category
  signal only.
- TRL + Harbor multi-harness guide body at huggingface.co/spaces/FineEnvs/
  multi-harness-rl not fetched this session (the reddit thread is what was read);
  reading the guide is the next cheap step if the compost-export lane forms.

Scratch receipts: `_ftr_sweep.py`, `_ftr_read.py`, `_ftr_candidates.json` (187 posts),
`_ftr_read_*.md` (9 threads).
