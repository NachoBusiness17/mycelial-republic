# finetuning-adaptation arxiv sweep (frontier_olm_2026-10-08)

source-fetched: 2026-10-08

Door status: export.arxiv.org API clean all session (6 queries, Atom rendered as text);
arxiv.org/abs pages clean (8 fetched); one 60s WebFetch timeout on 2610.09835 retried
successfully same sitting. No 403s, no degradation, no fallback door needed.

## Pass 1 (broad sweep)

109 named candidates considered across 6 API queries, all dated 2026-09-08..2026-10-08:
LoRA in cs.CL (30), sampler/logit-bias in cs.CL+cs.LG (16), prompt-tuning/distillation in
cs.LG (8), SLM serving/quantization (7), embedding-model retrieval (22), reasoning-token
control (25), fine-tune-vs-prompt (1), plus 2 targeted follow-ups (2610.09835, 2610.00309).
Full query set and per-item one-liners were read from the API responses this sitting; the
ones not banked below and not already held were triaged as weaker fit (speech/audio, VLM
benchmarks, diffusion LMs) or duplicate coverage of a banked item's point.

## Pass 2 (deep reads, all read end to end by me this sitting)

Eight abs pages fetched and read in full: 2610.06851 (also byte-verified against the local
mirror snapshot state/arxiv/2026-10-06/2610.06851v1.txt, identical numbers), 2609.15476,
2610.02353, 2610.07722, 2609.11310, 2610.09835, 2609.23307, 2610.00309.

## Banked items (strongest first)

### 1. Base Models Can Reason By Taking a Cue From Training Data - arxiv 2610.06851 (2026-10-05)
Wang, Dravid, Shao, Farhat, Min, Efros. Quote (byte-verified against local snapshot):
"fixing particular starting token cues makes a base model's performance competitive with
that of its reinforcement learning (RL)-trained counterparts on math and coding". Numbers:
cue ".\n\nOkay" lifts Olmo-3-7B MATH-500 pass@1 42% -> 78%; "Alright," lifts Qwen3-14B
72% -> 87%; RL training makes these cues more probable, and pinning them recovers most of
RL's gain over the base model. Causal data interventions turn an arbitrary word into a
cue; code released (github.com/sophicle/cues). Estate use: this is the published causal
proof that a decode-time token constraint (what the P6 marker-penalty logit_bias profile
is) can substitute for a training pass. It is not a soft-prompt analogy; it is a measured
36-point recovery on MATH-500 from constraining the first token alone (42 -> 78; REV 2
fix 2026-10-08: the round-1 text said 43, a phantom - grep -c '43' over the mirror
state/arxiv/2026-10-06/2610.06851v1.txt returns 0; the abstract's own numbers are 42
and 78, delta 36). Any future
marker-penalty A/B should include a first-token pin arm, and the cue-set for gemma:2b can
be mined from its own duty_fuzz twins. Overlap: catalog has exactly 1 row, the state/arxiv
2026-10-06 mirror snapshot (corpus presence, not banked mining); no memory/ or steal-corpus
hit; no sibling sweep file banks it.

### 2. Temperature Fragility and the Conditional Benefits of Truncation Sampling - arxiv 2609.15476 (2026-09-14)
La Rosa. Quote: "Six of the thirteen models lose 17 to 38 accuracy points on MMLU-Pro
between 0.7 and 1.3, and the other seven lose at most 10." Thirteen open-weight models,
GSM8K + MMLU-Pro, temperatures 0.7/1.0/1.3 in one controlled pipeline; losses come from
generations that run to the token limit or never state an answer; and where accuracy is
stable across temperature, no tested truncation sampler beats plain temperature sampling.
Estate use: the measurement protocol RQ1 needs. Sampler-level profiles (P6 class) pay
off conditionally, per model, so the gemma:2b marker-penalty A/B must first measure
temperature fragility at the deployment temperature (a duty_fuzz-style paired battery,
n>=40, four pinned choices per the QUANT_AB_SPEC discipline) - if gemma:2b is in the
stable seven, no sampler tweak should be expected to move accuracy, and the toggle stays
OFF. Loss mode named (token-limit / no-answer) is the estate's EMPTY_REASONING class.
Overlap: zero catalog rows, zero memory/ hits.

### 3. Does Every User Need a Private LoRA? Decoupling Personalization from Per-User Adaptation - arxiv 2610.02353 (2026-10-01)
Sui, Malla, Choi, Choi (LINEUP). Quote: "Each target user optimizes only eight scalars,
while all shared components remain fixed." A shared bank of reusable low-rank
personalization factors plus per-user codes of eight scalars beats private-LoRA baselines
(the baseline config carries 4.19M per-user parameters) on all 12 metrics across six
personalization tasks, including an 11.4% LaMP-3 RMSE reduction, with finite-step
risk bounds. Estate use: the shape proof for RQ3. A per-seat adaptation shed does not
need to be a per-seat LoRA; the ReFold pattern (sha-addressed stubs, reversible restore)
transfers cleanest when the per-seat delta is eight scalars over a frozen shared bank.
"Personalization capacity allocation" is the frame any per-seat adapter ask should
arrive in. Overlap: zero catalog rows, zero memory/ hits.

### 4. Does Steering Break Your Model? (SteerScope) - arxiv 2610.07722 (2026-10-06)
Yang et al. Quote: "no evaluated activation steering method achieves higher efficacy
without incurring greater composite side effects." 23 methods across 4 families
(prompting, LoRA, SFT as baselines), 15 metrics, two model scales; activation steering
does not beat the Prompt Steering baseline on the efficacy/side-effect Pareto; under OOD
prompts side effects worsen through instruction relevance and fluency declines. Estate
use: RQ1/RQ2 ladder evidence. The cheapest intervention rung (prompt/sampler class) is
not dominated by heavier weight-level rungs on any measured axis here; combined with the
estate-held finding that serving-layer choices dominate small-model outcomes (lens/
burns.md, arXiv 2610.07781 already banked), the eliminate-before-frontier ordering for
adaptation asks is prompt/sampler -> soft-prompt -> shared-bank delta -> LoRA, each rung
needing its own measured failure before the next unlocks. Overlap: 1 catalog row, the
state/arxiv 2026-10-07 mirror snapshot; no memory/ or sibling-sweep hit.

### 5. Your Model Already Knows Don't Teach It, Learn to Ask It (soft prompting) - arxiv 2609.11310 (2026-09-10)
Gare et al. Quote: "LoRA at matching rank drops NaturalBench VQA accuracy by 35% relative
(56% at largest rank); soft prompting leaves pretrained performance unchanged." One to
three learned tokens (~7,168 parameters) match the best LoRA config on Roboflow20-VL
10-shot with over 20,000x fewer trained parameters; tokens transfer to a newer model
without retraining (+0.8 mAP on Qwen3.5-9B) and can be verbalized into readable prompts.
Caveat honestly noted in the paper: soft prompting is harder to optimize, higher variance
across seeds. Estate use: the rung between sampler profiles and LoRA in the RQ4 map.
It stores as exactly the shed shape ReFold wants (a few KB blob, base untouched, restores
by construction since the backbone never moved), and cross-generation transfer is the
property the estate's qwen3 tag-aliasing law cares about. VLM-primary, so treat as
mechanism prior, not task prior, for gemma:2b. Overlap: 1 catalog row, the state/arxiv
2026-09-11 mirror snapshot; no memory/ or sibling-sweep hit.

### 6. A Deafening Silence: Catastrophic Forgetting Lives in the Output Embeddings of Tokens the Data Never Speaks - arxiv 2610.09835 (2026-10-07)
Han, Song, Park. Quote: "forgetting concentrates selectively in the output embeddings of
tokens rarely seen in the new corpus". Cause: persistent one-sided softmax gradients on
unseen-vocabulary rows that Adam's second-moment normalization amplifies into full-sized
updates; fix is raising Adam's epsilon only for the output projection, removing
39.4%-67.9% of forgetting across seven stable configurations (160M-12B, four families),
79.8% combined with replay, and rescuing released-head LoRA from a 23x forgetting surge.
Critical for the estate: post-hoc editing of drifted rows recovers under 5% of forgetting;
the defense must run during training. Estate use: doubles for RQ2 and RQ3. RQ2: if a
gemma:2b finetune is ever gated through the five-gate law, this single-line epsilon
setting is a mandatory recipe item, and the failure mode it names (rarely-seen tokens
drifting) is exactly the marker-token vocabulary the P6 profile penalizes. RQ3: it is
also the boundary of the restore door - you cannot repair drifted rows after the fact,
so reversibility must come from never touching the base (ReFold's sha-addressed stub
discipline), not from post-hoc correction. Overlap: 1 catalog row, the state/arxiv
2026-10-08 mirror snapshot; no memory/ or sibling-sweep hit.

### 7. Semantic Candidate-Job Matching: A Comparative Evaluation of Dense Embedding Models in Hybrid Retrieval - arxiv 2609.23307 (2026-09-20)
Yashwant et al. Quote: "structured English search text and language-specific keywords
through LLM-based parsing". Evaluates EmbeddingGemma (base), EmbeddingGemma fine-tuned
with Cached Multiple Negatives Ranking Loss, and MPNet in a hybrid vector + full-text
pipeline fused by reciprocal rank fusion. Honest scope limit, verbatim from the page:
the authors "state this scope explicitly rather than implying the full framework was
measured" - Recall@K/MRR/nDCG are defined but not reported on the abstract page. Estate
use (RQ5): the only 30-day paper found evaluating EmbeddingGemma variants at all. It
names the defensible non-router use shape for the banked EmbeddingGemma 2 (lens/
burns.md:132): a domain-adaptive Cached-MNRL fine-tune feeding hybrid retrieval, i.e.
offline batch embed + train, not always-on resident inference. Against the RAM-cache
residency law, nothing measured here justifies keeping the model hot; GPS-embed's router
use is already dead on string keys (100.0% vs 99.05, lens/burns.md:129-131). Banked at
low strength because the page carries no retrieval numbers; do not cite it for
quantitative claims. Overlap: "Candidate-Job Matching" zero catalog rows; "embeddinggemma"
case-insensitive hits 9 catalog rows, all the estate's own 10-07 EmbeddingGemma banking
(models/ + receipts), not this paper; no memory/ hit on the title.

### 8. Tokenized Key-Gated Adapter Routing (Locket) - arxiv 2610.00309 (2026-09-28)
Shaaban, Elmahallawy. Quote: an "invalid or absent token triggers a privacy-preserving
adapter that redacts or sanitizes sensitive content". One learned keyed entry token is
bound to exactly one lightweight LoRA adapter via sequence-level hard routing; each
adapter encodes an access policy; with a correct key, perplexity is comparable to
fine-tuning on raw data (Enron, ECHR, Yelp; Qwen3 1.7B/8B, Llama-3.2 1B/3B, Gemma-2-2B).
No numeric values on the abstract page. Estate use (RQ3): the fail-closed semantics the
ReFold restore door needs when it holds adapter deltas - a wrong or missing restore key
must route to a safe default adapter, never to corruption or silent wrong-delta
application. Gemma-2-2B in the model list puts the pattern on the estate's rung.
Banked lowest: security framing, no numbers on page. Overlap: zero catalog rows, zero
memory/ hits.

## RQ-by-RQ synthesis

RQ1 (marker-penalty logit_bias toggle; sampler-level as adapter substitute). Yes, with a
measurement gate. The mechanism class is published and causal: one pinned token recovers
36 points of RL-trained reasoning (2610.06851; 42 -> 78 on Olmo-3-7B, the phantom-43 fix
above), and the estate already holds the
serving-layer-dominates prior plus the 10-07 banked Harness Repair finding that
thinking-off beat capped thinking in 5/9 cells (watch/inbox/frontier_olm_2026-10-07/
sweep/inference-efficiency-arxiv.md item 1, not re-banked here). But the benefit is
conditional on temperature fragility (2609.15476): the A/B that decides the P6 default
is a paired battery at the deployment temperature with four pinned choices, n>=40; if
gemma:2b is temperature-stable, OFF stays correct and the toggle is cheap insurance, not
an accuracy lever. SteerScope adds that no heavier steering rung beats the prompt/sampler
rung on the side-effect Pareto (2610.07722).

RQ2 (is any LoRA/PEFT pass justified under the five-gate law). No, not yet, on public
evidence: the lighter rungs are not measured-exhausted (sampler unmeasured at deployment
temperature, soft-prompt never tried - 2609.11310 shows ~7k params matching LoRA without
forgetting), and the heavier rungs do not dominate on side effects (2610.07722). If a
gate ever passes, two recipe laws travel with it: Adam-epsilon-on-output-projection only,
during training (2610.09835 - post-hoc row repair recovers <5%), and per-seat state as
scalars over a shared bank rather than a private LoRA (2610.02353).

RQ3 (ReFold sheds -> adapter/checkpoint deltas). Transfers, with two laws learned here.
The shed shape is right: per-seat deltas as tiny scalars over a frozen shared base
(2610.02353) restore trivially because the base never moved; hot-swap at INT4 is
measured at 1.7 ms at 8B by the sibling-banked AO-DA (2610.09772, banked today in
sweep/open-local-models-arxiv.md, not re-banked). What breaks the restore door: (a)
post-hoc repair of drifted rows is measured near-useless (<5%, 2610.09835), so
reversibility must be address-the-original-bytes, never reconstruct-after-drift;
(b) the restore key must fail closed to a safe default adapter, not to wrong-delta
application (2610.00309); (c) AO-DA's both-arms-collapse-at-4B says every shed restore
test must run at the 2B rung, not be assumed from 8B proofs.

RQ4 (curriculum techniques with zero estate instruments). From this sweep's census plus
the estate's own surface: LoRA is the listing-dominant technique (30 fresh cs.CL papers
in 30 days) and has zero estate runner; prompt-tuning/soft-prompt (2609.11310, 2609.30935
EoupCT soft-prompt continual learning) zero instruments; distillation (2610.00332
worst-case-constrained RL distillation, 2609.12913 distilled compact retrievers) zero
instruments; sampler-level profiles exist (P6) but its A/B is unrun. The
eliminate-before-frontier map any adaptation ask must carry, cheapest first: sampler
profile (instrument exists, measurement owed) -> soft-prompt (~7k params, shed-native)
-> shared-bank scalar codes -> LoRA -> SFT; each rung opens only on the previous rung's
measured failure at n>=40.

RQ5 (non-router use justifying a resident embedding model). Nothing measured in 30 days
justifies resident-inference. The only EmbeddingGemma paper found (2609.23307) shapes an
offline use (Cached-MNRL domain fine-tune feeding hybrid RRF retrieval) and reports no
retrieval numbers; the GPS router leg is dead on the estate's own falsifier (string keys
100.0% vs 99.05). Against the RAM-cache residency law the defensible roles are offline
batch embed at mint time (duty_fuzz contamination pairs, corpus FTS cross-checks) and
teacher for a distilled compact retriever (the 2609.12913 shape), none of which need the
model hot.

## Overlap census (commands actually run this sitting)

- Single pass grep of 14 candidate titles against catalog/catalog.jsonl (1,266,929 rows):
  hits only for state/arxiv mirror snapshots (What Does a Harness Repair x0, Base Models
  Can Reason x1, Does Steering Break Your Model x1, Decoupling Logic from Persona x1,
  A Deafening Silence x1, Soft Prompting for Few-Shot x1, Probe the Harness x1) plus 9
  lowercase "embeddinggemma" rows that are the estate's own 10-07 banking. Snapshot rows
  inspected directly: they are zone=lsa listing mirrors, corpus presence, not banked
  mining (path shape local_sovereign_agent/state/arxiv/<date>/<id>v1.txt).
- grep -rli of all 8 banked titles/phrases over memory/, corpus/steal/, and the
  frontier_olm_2026-10-0{6,7,8} dirs: matches only in memory/trajectory/steps.jsonl
  (sibling actors' own grep command echoes, not holdings), the 10-07 sibling sweep
  (banks 2610.05533, so it is excluded here and cited as prior), and today's
  open-local-models sweep (banks 2610.09772, likewise excluded and cited).
- Byte cross-check: state/arxiv/2026-10-06/2610.06851v1.txt read in full; abstract
  numbers identical to the fetched abs page.

## Honest limits

- 2609.23307 and 2610.00309 abstract pages carry no quantitative results; both are
  banked explicitly as shape/mechanism priors and must not be cited for numbers.
- 2609.11310 is vision-language-primary; its transfer claim to a text janitor fleet is
  mechanism-level, not task-level.
- All quotes come from arxiv abs pages fetched this sitting (plus one local mirror
  snapshot); PDF bodies were not fetched, so quoted claims are abstract-scope.
