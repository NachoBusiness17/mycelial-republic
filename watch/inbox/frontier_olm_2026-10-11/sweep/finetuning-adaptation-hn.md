# SWEEP: finetuning-adaptation via Hacker News (2026-10-11)

source-fetched: 2026-10-11. Area gopher: sweep-finetuning-adaptation-hn, dynamic-workflow
child of the frontier_olm_2026-10-11 run. House laws held: ascii only, no em or en dashes,
every claim cites what was read or run this sitting, unknowns marked OWED not guessed.

## Instrument (what actually ran)

- Door status: the HN Algolia API answered normally all sitting; zero 403s, zero degraded
  fetches, no fallback needed. WebFetch on all article and thread pages returned content.
- Pass 1: `.venv/Scripts/python.exe C:/Users/foste/AppData/Local/Temp/hn_sweep_search.py`
  (scratch urllib script, written this sitting) against `hn.algolia.com/api/v1/search_by_date`
  and `/api/v1/search`, tags=story, numericFilters=created_at_i>1789084800 (2026-09-11),
  hitsPerPage=20. A plain `curl -s` smoke test on the same API ran first and returned valid
  JSON (0 hits for the over-tight phrase "LoRA fine-tuning", which is itself instrument
  evidence: Algolia needs loose terms).
- 16 queries run: fine-tuning, finetuning, LoRA, QLoRA, Unsloth (by_date); model merging,
  weight subspace, test-time training, on-policy distillation, catastrophic forgetting
  (by_date); LoRA fine-tuning, fine-tune small model, distillation LLM, adapter fine-tuning
  (relevance); decision model, RLHF, GRPO, hypernetwork, Universal Weight Subspace, Dead
  Salmons, continual learning, lifelong learning, knowledge editing, training small language
  model, reinforcement fine-tuning (by_date).
- Instrument caveat (read from the output, not assumed): Algolia fuzzy-matches hard. "LoRA"
  and "GRPO" by_date returned mostly noise (running shoes, grok-bot stories); "Universal
  Weight Subspace" and "Dead Salmons" returned ZERO story hits in the 30-day window: HN has
  not front-paged either paper. Zero-hit is a bounded claim about tagged HN stories, not
  about the literature.
- Candidates retained, on-area, distinct HN story IDs (53, exceeds the 30 floor):
  49923692, 49995058, 49965607, 49949900, 49917734, 49912849, 49897103, 49896983,
  49889028, 49881077, 49854499, 49842063, 49836779, 49820954, 49807413, 49795171,
  49748553, 49687253, 50032037, 50034625, 50030016, 50024959, 49783349, 49778955,
  49756840, 49880342, 49727511, 49967455, 49783133, 49807276, 50037949, 50035624,
  50035362, 50034279, 50032055, 50031696, 50027132, 50025521, 50025515, 50024913,
  50024668, 50024061, 50023978, 50023679, 50023015, 50020652, 49991390, 49870984,
  49763045, 49736134, 49908550, 49803321, 49722390.
- Pass 2 (deep, end to end, 10 items): Clef blog post + its HN thread (49923692);
  nishtahir.com build-your-own decision model + its HN thread (50037949); Mini-AGI HN
  thread (49783133, author volotat answering in-thread); Ask HN fine-tuning-worth-it
  thread (49807413); woct0rdho/transformers5-qwen3.5-recipe GitHub README (50034625);
  arXiv 2609.30652 abstract (49880342's story target); cacheverifier.com drift post
  (49889028); cactuscompute.com/needle (49748553); arXiv 2405.09673 abstract (verification
  fetch of the Biderman paper name-drop from the Mini-AGI thread).
- Quotes below are verbatim excerpts as returned by WebFetch (model-mediated extraction of
  the fetched page), not raw byte captures; confidence fields carry that honestly.

## Overlap method (run this sitting)

- `grep -i` over catalog/catalog.jsonl for each candidate's title, URL token, and HN id.
- Register greps over all four olm runs (2026-10-05, 2026-10-09, 2026-10-10 sweep/,
  adhoc) for clef, woct0rdho, cactus, mini-agi, volotat, nishtahir, deltatensors,
  cacheverifier: ZERO register rows (files verified to exist first).
- Bounded `grep -r` over memory/ (biography, biography_backup, session excluded for size;
  a first unbounded run was killed as too slow, disclosed) for the same tokens plus RLCD,
  Mini-AGI, Cactus Needle, Cloudflare Clef.
- Result highlights: catalog "Cactus" hits are game items (CactusDrink, CactusPotion,
  cactus-sour-candy), not Cactus Needle. The one woct0rdho catalog hit is a reddit twin
  capture. RLCD lives in memory only as the Jev pack's provenance guard (below).
- EXCLUDED as likely duplicate: HN 49687253 "Molt - Thermally aware QLORA fine-tuning for
  Windows laptop GPUs" (2026-09-13) is the same-name system as the adhoc register's banked
  reddit MOLT find (id 1wyvc8k, register row 2 of finetuning-adaptation). Same-authorship
  of the two postings was NOT verified this sitting, so it is excluded from the JSON bank
  rather than double-banked.

## Banked items (strongest first; full JSON mirrors these)

### 1. LoRA over GGUF: Train Qwen3.8-Flash-Next in 40G VRAM (HN 50034625, 2026-10-10)

Show HN pointing at github.com/woct0rdho/transformers5-qwen3.5-recipe. README read
first-hand this sitting. The recipe trains LoRA directly on a GGUF-quantized base kept
quantized in VRAM: torch.compile on the GGUF dequant function so full weights never
materialize, llama.cpp-style MMQ/grouped-MMQ GEMM, Unsloth-style fast LoRA backward, Liger
RMSNorm, chunked cross-entropy, 8-bit AdamW. Claimed footprints: Qwen3.6-35B-A3B in 16 GiB,
DeepSeek-V4-Flash (284B-A13B) in 90 GiB, Qwen3.8-Flash-Next (125B-A6B + 51B engram) in
40 GiB. Verbatim: "GGUF is going to replace bitsandbytes as the base model format for
low-VRAM LoRA training." Named limits, verbatim: "Currently all kernels and parameters in
this repo are tuned for Strix Halo. More work is needed to support other GPUs." No
throughput or accuracy benchmarks published (bench scripts exist, results do not).
Overlap: catalog/catalog.jsonl carries the reddit twin (frontier_olm_2026-10-09/sweep/
_txt_1x1bdvl.txt, "LoRA over GGUF ... by /u/woct0rdho", captured 2026-10-09, never
registered); zero register rows anywhere. The full README read is the new depth.
Estate value: this is the training-side design change for lora_pipeline: train in
coefficient space on a frozen quantized base, matching the module's own invariant
"the adapter is the increment, the base model is the (substrate)" (memory/
knowledge_graph.json, the 5 has_invariant edges on module:lora_pipeline.py, printed this
sitting). It is a design steal, not a runnable rig here (see RQ2).

### 2. Clef: Cloudflare decision models + RL fine-tuning platform (HN 49923692, 2026-10-01)

641 points / 218 comments. Blog post + thread both read. Clef = open (Apache 2.0)
decision models: frozen Qwen3.8-27B / Qwen3.5-9B backbones, routing head + rank-256 LoRA
adapters, plus a named method "Reinforcement Learning for Calibrated Decisions (RLCD)"
granting partial credit to adjacent ordinal choices. Weights open, data and pipeline not
published (buildbuildbuild in-thread: "Open weights, not open source."). BFCL case-exact
98.47 vs Jev 95.75; median latency 209.3 ms vs Jev 524.1 ms. Thread skeptic amluto:
"I don't think a Jev-like model is particularly useful unless you can fine tune it."
Verbatim from the post: "By freezing Qwen3.8-27B for Clef and Qwen3.5-9B for Clef-flash,
we jointly optimized the routing head alongside rank-256 low-rank adapters."
Overlap: the 10-05 run captured this exact page raw (frontier_olm_2026-10-05/sweep/
_clef.html; grepped this sitting: 239 "cloudflare", 11 "Clef-flash", 28 "decision model")
and never banked it. Zero register rows. Separate, load-bearing: memory/research_packs/
THE50_W3_T11_TYPED_DECISION_ORACLES.md:55-57 recorded that a decision-model vendor's
"RLCD" had no paper and :223-235 pinned the only prominent RLCD as Yang et al. 2307.12950
(contrastive distillation). Cloudflare's Clef is now a SECOND published RLCD
("for calibrated decisions"): the name-collision guard is now three-way, and this bank is
the first estate analysis to say so.

### 3. Cactus Needle 3: 8-29MB automation models (HN 49748553, 2026-09-18)

236 points. Page read first-hand. NOT distillation: "intelligence laddering" - one weight
set where "Every layer of Needle 3 is a sub-network with monotonically increasing capacity"
(2L to 20L usable as standalone models), 360B tokens of proprietary structured data, CQ2
2-bit quant, subnets export as 4-bit .cact. LoRA on the frozen base is the supported tune;
tuned subnets gain 18-36 points on DroidCall, and the page claims "from 4 layers up the
tuned subnetwork passes DeepSeek V4 Flash, starting at 29M parameters" (their Figure 3;
baselines f16 under vLLM, DeepSeek via cloud API). Relative claims only, no raw numbers.
Overlap: zero catalog/memory/register hits (catalog Cactus hits are game items). New.
Estate value: loudest single RQ1 datum of the sweep: narrow structured tasks are
fine-tuning-winnable at 29M parameters against a frontier generalist, via frozen base +
adapter, i.e. the JIT law's shape at the extreme small end.

### 4. Mini-AGI: dynamic continual learning on 8GB VRAM (HN 49783133, 2026-09-21)

277 points / 80 comments; thread read with author volotat answering in it. Mechanism per
the author: batch-1 gradient training on a 32K-char continuous stream, MoE with experts
added/pruned dynamically, experts swapped disk/VRAM, and the cure for forgetting is LR
asymmetry - verbatim volotat: "slowing down the LR or the trunk, while keeping the LR of
the experts is enough to eliminate most of the forgetting." Hardware: RTX 3070 Laptop,
8GB. Held-out loss 0.8012 at ~5% through a 7.8B-char corpus; 176 experts at step 191,447.
Skeptics in-thread: abeppu (forgetting only delayed), synctext ("lacks any substance. No
relation to related work, no description of algorithm, no ablation study, just
hand-waving."), lostmsu (dense 8M baseline does 1.15 bpb on enwik9 vs this 1.8), and
jmatthews' partial replication: "Most of your claims prove out but the lever is
essentially Biderman et als 'learn less forget less.'" I verified that name-drop
first-hand: arXiv 2405.09673 is "LoRA Learns Less and Forgets Less" (Biderman et al.,
TMLR featured, Aug 2024): LoRA underperforms full fine-tuning on target domains
(programming, math) while preserving out-of-domain performance.
Overlap: zero catalog/memory/register hits for Mini-AGI, volotat, 49783133. New.
Estate value: the living-weights falsifier (RIB_LIVING_WEIGHTS_BY_NATURE) demoed on
garage hardware, and the community response is a free course in what a credible
continual-learning claim must carry (benchmarks, ablations, baselines).

### 5. Ask HN: When is fine-tuning a small LLM worth it? (HN 49807413, 2026-09-22)

14-comment thread read end to end. Payoff conditions named by practitioners: style
imitation where few-shot fails (muzani: examples work "but at this point, you might as
well fine-tune it"); plentiful imperfect data (speedgoose on chess: "chess data is
plentiful and because my aim was to not have perfect answers"); privacy/on-device
(dsjakupov); fast iteration on a 1B before climbing (carlos_rpn). Non-payoff: RL-trained
game strategy ~20,000 hands on Qwen3.5:2b only matched "decently written procedural game
logic" (spottedmarley); thin proprietary datasets "disappointing"; general classification
usually loses to prompted bigger models. The load-bearing line, verbatim spottedmarley:
"building the LoRa is the easy part" - dataset generation was the biggest time sink.
Overlap: zero hits for the title or id. New.
Estate value: the JIT law's "dataset is the pitfall-bypass corpus" is exactly the part
practitioners name as the bottleneck, and the estate's compost ledger is a structural
answer to it. The hearts result independently re-confirms engine-owns-truth.

### 6. RSI via On-Policy Distillation: DCE+SRCL (arXiv 2609.30652, HN 49880342, 2026-09-28)

Abstract read first-hand. Two parts: Dynamic Co-Evolution (privileged teacher co-evolves
with student across rounds) + Self-Refined Concise Learning (train on shorter verified
rewrites of the model's own outputs to counter verbosity). Key move for the estate:
on-policy self-distillation needs no external teacher - "a second frozen copy of the
student model, now given the ground truth in its context, serves as the teacher."
Qwen3-8B: 65.97% Average@12, +35.62pp over frozen-teacher OPSD; output length -7.80%.
Stated limit: frozen teacher "can prevent the teacher from incorporating the improvements
learned by the student during training."
Overlap: catalog holds the ingest stub state/arxiv/2026-09-28/2609.30652v1.txt (title +
abstract only, no analysis), the same stub pattern the adhoc register's DIAL-OPD/SGUID
rows disclose. Zero register rows. The full read is this sweep's.
Estate value: a weight-adaptation path whose training signal is the estate's own verified
receipts as ground truth plus a frozen self-copy: no premium judge in the loop, which
matters for RQ3's cheap-first leg.

### 7. Build your own decision model + thread (nishtahir.com, HN 50037949, 2026-10-10)

419 points / 95 comments; article and thread read. Qwen3-1.7B, single-pass constrained
decoding over A-E option tokens, quick finetune on CommonsenseQA (1,221-sample holdout):
accuracy 0.5938 -> 0.6241, macro F1 0.5844 -> 0.6234, then temperature scaling (T ~ 3.80)
for calibration. Hardware not stated in the article. Failure named by the author: severe
overconfidence (0.9978 on an ambiguous question; the 0.90-1.00 confidence bin is only ~70%
accurate pre-calibration). Thread's strongest methodological critique, verbatim shawntan:
"you're overfitting to the test set" if any part of the system is tuned against reported
results, and "How Jev manages to claim calibrated probabilities is beyond me. Calibrated
to what?" roger_ identifies the fix as Platt scaling.
Overlap: zero hits for nishtahir or 50037949; the decision-model wave generally is
unbanked by prior olm runs. New.
Estate value: two dead-salmon-class hygiene rules for the JIT law's instrument section
(per-student pitfall census): calibrate on held-out data, and pre-register the test set
before tuning anything against it.

### 8. Fine-tuning turned actively harmful: drift monitoring (cacheverifier.com, HN 49889028, 2026-09-29)

Vendor blog (CacheVerifier, hosted semantic-cache verification; disclosed as such). Read
end to end. Failure: a verifier fine-tuned on an earlier slice of comcastcares
customer-support traffic degraded as the traffic drifted - verbatim: "a model that used to
improve on the stock verifier started approving more wrong answers than it caught."
Gray-zone positive rate moved ~5x over the window. Detection shipped: chunked two-proportion
z-test, Page-Hinkley change-point test, and a two-sample KS test on the verifier's own
score distribution versus a baseline captured at fine-tune time. Also stated: fine-tuning
needed "a few hundred to ~1,000 examples" and held up on 3 of 4 benchmarks pre-drift.
Overlap: zero hits for cacheverifier or the id. New.
Estate value: the time-shifted failure mode for ANY JIT fine-tune built from the compost
ledger: pitfalls get bypassed and stop recurring, so the corpus distribution moves under
the model; a frozen adapter at time T is the same trap. Vendor post = sensing-grade
evidence only; the detector trio is the steal, not the product.

## RQ1: the 8 adhoc finds vs the JIT law: evidence-backed or operator coinage?

Verdict: EVIDENCE-BACKED on mechanism and conditions, BOUNDED in three ways the law card
does not yet carry, and still NOT estate-falsified (the card's own falsifier - a
pitfall-bypass-trained model beating prompt-only on held-out pitfalls - remains unrun).
Restate-then-refine, per find, with this sweep's additions:

- Mechanism (weights beat same-food retrieval): aTTT's same-text comparison (adapter
  update 54.3% vs in-context 49.3%, register row 4) supports the law's "zero context cost,
  arrives mid-thinking" claim. DPPM (row 6) takes it further: the delivery mechanism need
  not be a training run at all; a Doc-to-LoRA hypernetwork compiles history into adapters
  in a forward pass and beats full context. This sweep adds Clef: frozen backbone +
  rank-256 adapters is now a production default at Cloudflare scale with open weights,
  and Cactus Needle 3: a 29M-parameter tuned subnet passing DeepSeek V4 Flash on a narrow
  tool-call suite. The law's shape is now industry practice, not operator coinage.
- The when-clause (fine-tune when a pitfall RECURS): Agentic-TTT (row 5) measured the
  gate - without a compute penalty the policy overuses TTT; the Ask-HN thread gives the
  practitioner version (fine-tune for recurring narrow shape + plentiful data; prompting
  wins general cases). Restated and quantified.
- The food (pitfall-bypass corpus): "building the LoRa is the easy part" (Ask-HN,
  spottedmarley) names dataset creation as the bottleneck; DIAL-OPD + SGUID (rows 7-8)
  quantify that selection/curation decides whether the loop improves or degrades. The
  law's dead-salmon rider (card lines 30-31) is therefore supported, not contradicted.
- THREE NEW BOUNDS this sweep adds to the card:
  1. LEARNS-LESS bound: jmatthews' Mini-AGI replication names Biderman et al. 2405.09673
     (verified first-hand this sitting): LoRA under-learns the target domain vs full
     fine-tune while protecting out-of-domain competence. The JIT law's adapter path
     should expect under-learning on hard skills (code, math) and buy forgetting-protection;
     MedGemma's narrow oncology QA (register row 1) is the favorable case.
  2. SERVING bound: the MedGemma find's own merge-loss (83.8% agreement, ~2x alpha/r
     effective scale under Unsloth, 17-37% of delta elements erased by bf16 merge) says
     the law needs a serving clause: keep the adapter unmerged (DeltaTensors pattern,
     below) or accept the loss.
  3. DRIFT bound: CacheVerifier (above): a fine-tune frozen at time T degrades as the
     failure distribution moves; the compost corpus is explicitly time-shifting (bypassed
     pitfalls stop recurring).
So: the law is now evidence-backed coinage, i.e. a law with external replication; what it
still lacks is the estate's own falsifier run. That unrun falsifier is the honest gap.

## RQ2: does Universal Weight Subspace change lora_pipeline design, and is it compatible with the GPU-ladder ignore-DeepGEMM state?

- What the graph holds today (printed this sitting from memory/knowledge_graph.json,
  full edge texts repr'd): module:lora_pipeline.py carries 5 has_invariant edges,
  including "law in weight space - the adapter is the increment, the base model is the"
  (stored truncated mid-sentence in the graph itself; I did not guess the completion),
  "LAW: Output is a LoRA adapter, not a full model. Weights are <100MB, easy to
  distribute.", and "LAW: Never upload training data. Training is local or on rented GPU
  with encrypted disk." (full text verified this sitting). lens/graph.md:22 gives degree
  5; lens/graph.md:30 records that doctrine->module edges are zero graph-wide.
- unisub (arXiv 2512.05117, banked first-hand in watch/inbox/unisub_drop_20261010/CARD.md,
  which I read this sitting) claims shared low-dimensional spectral subspaces WITHIN shared
  architectures, coefficient-training, up to 100x compression, data-free merging. Its own
  card carries the honest caveats: preprint, within-architecture only, no replication.
- DESIGN ANSWER: yes, it changes the design target, and the HN sweep independently shows
  the direction is already being built: (a) store/train in increment space, never merged
  weights: the GGUF-over-LoRA recipe trains on a frozen quantized base; DeltaTensors
  (HN 49783349, item page read; repo github.com/AaravGaurdev/deltatensors) stores weight
  deltas as .wdelta files with chained history - their own example: a 953 MB Qwen2.5-0.5B
  fine-tune stored as a 294 MB delta, reconstruction changing perplexity 19.11 -> 19.22
  (lossy, disclosed); (b) exchange coefficients, not data: the estate's lora_pipeline laws
  (adapter-not-full-model, never upload training data) already encode exactly this. unisub
  upgrades the increment law from doctrine to (claimed) spectral structure; DeltaTensors
  and the GGUF recipe are working instances. What lora_pipeline lacks is not the law but
  the wiring (zero doctrine->module edges) and the delta-native storage format.
- COMPATIBILITY ANSWER (run against RIB_GPU_LADDER_20261001.md, read this sitting): the
  box is AMD RX 5600 XT (RDNA1, gfx1010; no MFMA, no FP8; rib lines 4-8). Gate 1 (SM90/
  SM100 arch) fails outright for DeepGEMM-class runtimes, so the standing "ignore DeepGEMM
  on this box" verdict (rib lines 25-31) is untouched by everything in this sweep: the
  GGUF recipe uses llama.cpp MMQ kernels, not DeepGEMM, and gate 4 (CUDA 12.8+/NVRTC) is
  not triggered. But the recipe is NOT a runnable rig here: its kernels are explicitly
  tuned for AMD Strix Halo ("More work is needed to support other GPUs"), and its smallest
  listed footprint (16 GiB) exceeds this box's VRAM class. Compatibility verdict: the
  DESIGN steals are box-compatible (coefficient-space storage, unmerged adapters, delta
  chains: all software-side); the GGUF training recipe itself is a porting job that also
  needs rented-or-borrowed silicon per the module's own never-upload/local-or-rented law.
  unisub's probe (spectral-decay overlap of two public LoRA deltas) remains the cheap
  falsifier and needs no new hardware.

## RQ3: evidence threshold for a premium turn on actual weight adaptation (descent cheap-first leg)

The descent protocol's leg 1 (SHERPA cheap-first + prior-art sweep, AGENTS.md descent
section; memory/rib/RIB_THE_DESCENT_PROTOCOL_20261001.md:30-56 per lens/laws.md:40) makes
a premium weight-adaptation turn premature TODAY, because the estate-side food does not
exist as bytes yet. Threshold, grounded in what this sitting read:

1. CORPUS AS BYTES: the compost ledger + burn-verdict rows must be exported as a
   controlled detected-pitfall + working-bypass pair set (the JIT card's pitfall-bypass
   corpus, card lines 11-13). Size anchor from the CacheVerifier read: "a few hundred to
   ~1,000 examples" sufficed to train a verifier that held up pre-drift on 3 of 4
   benchmarks. Below that, no turn.
2. CHEAP LOCAL PROBE PASSED: a 0.5-1.7B LoRA run on free/cheap lanes (the Ask-HN
   thread's own ladder: iterate on a 1B first) must show the corpus trains at all.
   "Building the LoRa is the easy part" cuts both ways: the estate's corpus advantage is
   real, but the first run will surface dataset-format problems that should burn free
   compute, not premium turns.
3. A NAMED DECISION POINT RETRIEVAL MISSED: the aTTT shape (same text as injection 49.3%
   vs adapter 54.3%) is the proof shape required: one pitfall class where in-context
   delivery measurably fails and the adapter demonstrably fixes it. Without that pair,
   GPS strings-are-coordinates still wins at the estate's scale.
4. PRE-REGISTERED CONTROLS: dead-salmon hygiene before any "the tune worked" verdict
   (label-shuffled corpus arm, random-init control, held-out pitfalls fixed BEFORE
   tuning; shawntan's "Calibrated to what?" is the in-thread warning).
Also relevant: RSI-OPD's self-distillation (frozen self-copy + ground truth in context)
means the eventual first weight turn may not need a premium teacher at all - the estate's
own verified receipts are the training signal. Premium budget buys judgment and
adversarial eval, not the training pass. Net: no premium turn is justified by the current
8 confirmed rows alone; rows 4, 5, 6 (aTTT, Agentic-TTT, DPPM) are the ones that would
justify one once legs 1-3 above exist.

## RQ4: Dead Salmons: applicable to estate adaptation failure modes, or pure landscape?

APPLICABLE, with three concrete carriers read this sitting (plus the drop card's own
mapping, which I read first-hand):
1. EVAL-SET OVERFITTING: shawntan's critique in the 50037949 thread - tuning any part of
   the system against reported results means "you're overfitting to the test set"; the
   JIT law's instrument (per-student pitfall census, card lines 36-41) can overfit its
   own held-out pitfalls exactly this way. Guard: fix the held-out set before any tuning,
   calibrate on separate data.
2. DISTRIBUTION DRIFT: the CacheVerifier failure ("approving more wrong answers than it
   caught" as traffic moved) is the time-shifted-corpus trap for compost-fed fine-tunes.
   Guard: keep a baseline sample captured at train time and run the detector trio
   (z-test, Page-Hinkley, KS on score distribution) before trusting a stale adapter.
3. SILENT DEGRADATION IN SERVING: the adhoc MedGemma find (merge eats 17-37% of delta
   elements; effective scale ~2x off under Unsloth) is dead-salmon-shaped: plausible
   serving numbers attached to a degraded model. Guard: post-merge agreement check, or
   never merge (DeltaTensors pattern).
4. COMMUNITY-SCALE NEGATIVE CONTROLS: the Mini-AGI thread is the dead-salmon method
   applied by crowd: synctext's "no relation to related work ... just hand-waving",
   seanhunter's illegal-move dissection, lostmsu's dense baseline. The estate's version:
   every fine-tune claim gets a random-init or label-shuffle control arm before banking.
Pure-landscape verdict: NO. The paper's lesson (explanations need random-net controls)
transfers to every "the adapter learned the pitfalls" claim the estate might make.

## DeltaTensors (supporting read, not in the JSON 8)

HN 49783349 (2026-09-21, 1 point, zero comments - thin signal, hence supporting only).
"compresses fine-tuned model checkpoints by storing the weight difference from the base
model"; "chained deltas for model version history"; works post-hoc on full fine-tunes,
"no LoRA needed". Quantified artifact: 953 MB -> 294 MB, ppl 19.11 -> 19.22 on
reconstruction. Connects unisub (coefficient storage) to the MedGemma merge-loss bound:
delta-native storage avoids the merge entirely. Zero overlap hits (deltatensors,
AaravGaurdev). New.

## Anti-rebank + OWED

- Do not re-bank: the adhoc register's 8 finetuning rows (rows cited by register position
  above), the MOLT reddit find (HN 49687253 excluded as likely twin), the Jev pack's RLCD
  guard (THE50_W3_T11), unisub + Dead Salmons + AIRLLM drop cards (banked 2026-10-10,
  first-hand).
- The decision-model wave (Cloudflare Clef 49923692, Microsoft-Decision-1 50024913,
  THX-01 50023978/50027132, Jiwo 49967455, Liquid d1 50025515, the nishtahir guide
  50037949 and its spawn) is this window's dominant adjacent wave; this bank covers Clef
  + nishtahir only. Microsoft-Decision-1, THX-01, and Liquid d1 were candidate-listed,
  NOT deep-read, and are therefore unbanked by law.
- OWED (not done this sitting): no estate fine-tune corpus export was attempted; no
  unisub probe run; Microsoft-Decision-1 / THX-01 / Liquid d1 / Mini-AGI repo README
  (only the thread read) remain first-hand-unread; the HN MOLT vs reddit MOLT
  same-authorship check; a full-repo byte read of the woct0rdho recipe (README only
  this sitting).
- Door health: no 403s or degraded fetches; Algolia by_date + relevance and all WebFetch
  calls returned content. No fallback path was exercised.
