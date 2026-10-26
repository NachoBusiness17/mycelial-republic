# HERMES $100 — REVISED: train the low tier on our frontier thinking (2026-09-17)

*Operator redirect: "I want our frontier design and thinking full record so we can train
the low tier. Dogfood our thesis. One design spec: Sherpa maps footholds, code direction
orchestrates it cheaply through our surfaces, D iterates. That's how we should spend
the $100."*

## THE ONE BRIEF (not five)

**Design the frontier-thinking training corpus curator + the QLoRA training recipe.**

The corpus already exists (265KB research answers, 390KB imprint, 8 architect docs,
3 laws, 21 gate-proven levels with inscriptions, ~30 LINKS crosswalks, the NPC=seat
architecture, the transfer matrix, the gap analysis, the recap). What's missing is
the PAIRING: {situation → decision} instruction-tuning rows. Hermes designs the
curator script; the free lanes execute it forever.

## THE PIPELINE (Sherpa → code direction → iterate)

1. **SHERPA MAPS FOOTHOLDS** (the planning lens): the curator extracts {situation,
   constraint, decision, why, falsifier} tuples from every receipt, law, inscription,
   and architect doc. The Sherpa thesis encoded as training data: rank over brightness,
   decompose before moving, add a basis vector when stuck.

2. **CODE DIRECTION ORCHESTRATES CHEAPLY** (the free lanes execute): the trained model
   emits design DIRECTIONS (which mechanic, which inscription, which gate, which law
   applies), not code. The free lanes turn direction into code. The gate verifies.
   Cost per iteration: crumbs.

3. **D ITERATES** (the evolution loop): the model's outputs go through the same
   gate → verdict → feedback cycle as the level briefs. Gen-1 failures become
   training pairs for the next epoch. The loop that breeds levels now breeds
   the model that designs levels.

## THE $100 BREAKDOWN (Hermes designs, free lanes execute)

- **$40 — corpus curator design**: the extraction spec (which files, which fields,
  how to pair situation→decision, dedup law, quality gates) + a working prototype
  script Hermes writes against our actual receipts.
- **$35 — QLoRA recipe for gemma-2b/4b**: the exact training config (unsloth params,
  dataset format, eval design to prove the trained model beats base on held-out fleet
  decisions, hardware estimate for our Mac Studio).
- **$15 — the Sherpa planning prompt**: the system prompt that makes the trained model
  plan like the Sherpa (rank, decompose, add basis vectors) instead of hallucinate.
- **$10 — the evaluation battery**: held-out fleet decisions the model has never seen,
  scored by the same gate discipline (design verdicts are right/wrong against known
  constraints, not vibes).

## THE DOGFLOOD LOOP (after training)

```
situation → TRAINED MODEL (gemma, local, $0) → design direction
  → free lanes execute → BFS gate + tests verify
  → verdict fed back → next epoch trains better
```

The low tier doesn't need to be smart. It needs to know WHICH direction to point.
The Sherpa's thesis is the training data's shape: rank over brightness, decompose
before moving, add the missing basis vector. After one training run the fleet has
a $0 designer that speaks our register, cites our laws, and improves with every
iteration the same way the bred levels did.

## What NOT to spend on

- Meters first (the old plan) — the meters matter but they don't compound the way
  a trained model does. A meter reads one thing once; a trained model designs forever.
- More research (the free lanes own it).
- Training on generic text — the corpus is our receipts, our laws, our inscriptions.
  The model learns to be US, not to be a chatbot.

## FALSIFIER

After one QLoRA epoch on the curated corpus, give the trained model and base gemma
the same 10 held-out design situations. If the trained model doesn't produce
register-consistent, law-citing, gate-passing design directions at ≥2x base rate,
the corpus was too thin — fix the curator, not the model.
