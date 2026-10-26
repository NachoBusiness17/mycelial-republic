# STEAL RECEIPT — KEV MATERIALIZED (top-priority steal, night-one radar → concrete)
**ts:** 2026-09-21T19:45Z
**Specimen:** @jaredpalmer 2102048412841517495 — "Kev has now been refactored on top of
Qwen3.5. New checkpoints at 0.8B, 4B, 9B along with a fine-tuning script you can use
with Modal." + follow-up (calibration still overconfident; MLX support coming).
**Artifact:** github.com/jaredpalmer/kev — Apache-2.0, cloned to corpus/library/kev.

## What Kev is
"Small Jev-like decision models you can train and run yourself" — the operator's
decoded Jev doctrine (archerhume.com "Jev's Architecture Unmasked" is their cited
source) turned into an open model family: Qwen3.5 base + LoRA + small pointer head.
Given one shared input ("ticket"), it answers yes/no (`noul`), multiple-choice
(`choice`), and rating (`score`) questions about it in a single pass — a ROUTER as
a tiny model. API matches TypeSafe's System One SDK. Runs CUDA/ROCm/Apple Silicon;
0.8B runs anywhere. Ships frozen eval suites (decision-v1/v2, transfer-v1/v2,
public-pool) — pre-registered bars as datasets, our own law in their world.

## Why this is THE steal
Night-one Quiet Radar: "KEV top-priority steal — open trainable Jev-like decision
models on our own kifu ledger = founding hypothesis productized." The founding
hypothesis is now somebody else's shipped product — and our data is the fuel:
- **Blind probe ledger** (probes/elo.json, preference pairs) → `choice` rows
  ("this ticket, which lane wins") — direct router training diet.
- **Kifu ledgers** (walker rows, fleet steps) → `noul` rows ("was this move
  refused/gated correctly") — decision-calibration diet.
- **provider_usage + smith chart** → `score` rows (difficulty/cost ratings).
- **Walk debts + gate refusals** → frozen eval suites in their suite.py format —
  our pre-registered bars as transfer tests.

## The plug-in plan (on GO)
1. Format the diet: probe pairs + kifu decisions → their suite/ticket format
   (kev/anchors.build is the ingest surface).
2. Fine-tune Kev-0.8B on our diet (Modal script as-shipped, or hands-box 3090 at
   the night window — 0.8B is family-box-safe-ish, still night by law).
3. Serve as the JEV-router brain: Kev-0.8B answers route/no-route/rating for
   every queue task — the tier ladder becomes a learned model (RouteLLM endgame,
  KEV edition), smith-chart bars as its eval.
4. Their own warning applies to us: calibration is overconfident — our bar law
   (pre-stated thresholds) is the calibration harness; freeze evals before
   trusting it.

## Registration
- Clone: corpus/library/kev (shallow, Apache-2.0, NOTICE preserved).
- Steal ledger: KEV entry → status MATERIALIZED/CONCRETE.
- Diet map: this card. Training run: needs GO (compute + window).
