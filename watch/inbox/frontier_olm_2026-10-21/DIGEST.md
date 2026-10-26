# FRONTIER MINE 2026-10-21 (manual, funded grok lane; Oct 19-21 window)

Receipt: 8 finds across 4 areas, all first-hand fetched (arXiv API + abstract
pages), Oct 19-21 window only. Manual lane, day 3 (workflow approval gate
still mode-1-only). Confirmation grade: abstract-level; bodies flagged where
read.

## 1. Agent memory (2 finds)

**Error-reproduction loop in agent memory** (ALFWorld/WebShop/ScienceWorld,
3 backbones): deleting a guidance rule does NOT erase the trajectories it
caused - indirect feedback through stored trajectories remains. Equal-weighted
held-out success 59.9% for raw trajectory memory vs 53.5% trajectory-as-learned,
49.0% stored abstractions, 49.3% both, 52.9% Reflexion - and LOWEST LLM-call
cost of the designs compared. The reproduction evidence is association, not
proof. Estate map: the trickster protocol's negative-egregore guard (R3) is
externally confirmed - a bad rule's trajectories persist after the rule is
deleted, exactly the caricature-depletion law. Also: the raw-trajectory arm
beating stored-abstraction arms confirms the Oct-20 Cache2LoRA come-apart
(compile drops a leg).

**Industrial ReMEmbR** (Yammine et al., Idealworks/NVIDIA): warehouse robots
encode 3-second clips on Jetson into retrieval embeddings + cached vision
tokens + video latent; raw frames stay local; shared server index searched by
content/place/time; text generated only on query. Unparsable answers 4.5% ->
1.9% with a half-size agent. Zero-shot traffic map: 71.3% balanced accuracy
on 914 frames. Estate map: this is the perimeter's memory architecture
confirmed by an industrial deployment - local capture, deferred generation,
shared index. The coldest-vertex law (robot = phone = Termux) is the same
design.

## 2. Inference efficiency (2 finds)

**AMTP** (arXiv 2610.28619, Oct 20): a ~small online controller picks the MTP
horizon BEFORE drafting by predicting rejection hazards and choosing the
horizon with the highest expected tokens-per-second. First training-free
pre-draft MTP horizon selector. Up to 4.1x vs standard decoding; matches or
beats the tuned fixed window in 8 of 10 settings. Estate map: the flash pace
law's pacing mechanism at the decode layer - the same adaptive-horizon shape
as the ten-minute self's cadence.
**BitMTP** (arXiv 2610.28500, NeurIPS 2026, repo): one ultra-low-bit model
drafts AND verifies (MTP loss co-designed with W2A8 kernels). 2.2x on
BitNet b1.58-2B, 2.0x on RTX 3090, 3.3x MBPP+ on Jetson Orin. Key finding:
"accepted-prefix dynamics" - wider compute can erase the savings from fewer
steps. Estate map: the garage fleet's spec-dec tier (the garage bench can
draft AND verify at 2-bit). The Jetson number is the phone-class proof.

## 3. Fine-tuning / adaptation (2 finds)

**MuPACE** (arXiv 2610.28072): a ~20k-param LSTM meta-trained across episodes
emits bounded schedule changes; one run matches per-task-tuned schedules on
64 problems, stays competitive on unseen 32B/27B models. The schedule is
learned, not searched. Estate map: the token-DNA sim's schedule leg - the
sim's agents need a MuPACE-class meta-scheduler, not per-task sweeps.
**AP-OPD** (arXiv 2610.28194): block-level penalty-jump detection in
on-policy distillation - "penalty-confidence tension" (penalty rises while
teacher entropy rises and top-1 falls), block-reweighting by the jump ratio.
+0.80 math Avg@k. Estate map: the percolator's penalty-jump detection is the
same shape at corpus scale - a block-level detector on the reward signal.

## 4. Swarms / markets (2 finds)

**PACT** (arXiv 2610.26671, Oxford): for routing/scheduling where the
instance is revealed by acting, agents propose short plans hung on the
environment graph at the nodes they'll demand; message passing updates plan
preferences from capacity load; each agent executes ONE step and replans.
Beats neural solvers and MARL coordinators, best zero-shot transfer to 64x
training size, beats centralized oracles that see the hidden uncertainty on
large instances. Estate map: THE SINGING NETWORK'S EXTERNAL VALIDATION -
plan-proposal + capacity-load message passing + one-step-execute-replan is
exactly the perimeter's propose/consensus/assert loop, formalized.
**Cooperative market-making desk** (arXiv 26789, LSE): quoter + risk manager
split, recurrent independent PPO on real Polymarket L2 flow (417 markets).
The shaped reward split (desk profit + post-fill markout charge) is their
best desk. HONEST LIMIT: no configuration shows positive average
end-of-episode portfolio value, one seed each. Estate map: the token-DNA
per-worker row design (each worker's own principal) is the fix for the
aggregate-scoring blind spot both papers name.

## Confirmation grade

Sweep-grade (grok-fetched from live posts + arXiv abstracts). The six arXiv
IDs are confirm targets for the next workflow-capable window.
