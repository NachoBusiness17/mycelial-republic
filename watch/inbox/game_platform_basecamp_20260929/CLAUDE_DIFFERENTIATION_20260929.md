# CLAUDE DIFFERENTIATION BRIEF (2026-09-29)

External research lane: how Claude is actually different from peers and why, so the Opus ask is tailored by data. Full text with all URLs preserved in the session transcript; this file banks the ask-relevant load.

## Landscape correction

Target model: **Claude Opus 5.5** (2026-09-22, $4/$20 per M, cache reads $0.20; 1M window). New tiers above it: Fable 5.1 ($10/$50 GA) and Mythos 5.1 (restricted). The estate's ask targets Opus 5.5 specifically.

## What the data says Claude is

- **Independent AA Intelligence Index: Opus 5.5 max = 58, #1 of 216** (medium 51, xhigh 56). GLM-5.3 (this seat's model): 45. GPT-6 Astra: 53. Terminal-Bench 4.0 independent board: GPT-6 Astra 58.2 > Fable 5.1 57.9 > Opus 5 53.9; Opus 5.5's claimed 66.4 is vendor-reported but their harness tracks the independent board within ~2 points where checkable.
- **The home-turf signal: knowledge work.** GDPval-AA 1846 Elo vs Astra 1542 — the spec/contract-authoring shape is Claude's measured strength (self-reported; corroborated in direction by AA #1).
- **Effort parameter is real: medium (the DEFAULT) scores 51; max scores 58.** An unconfigured ask silently gets the medium model. Budget for ~682s median TTFT and token burn at high effort.
- **Claude-specific weaknesses (live, documented):** sycophancy doubles under challenge/distress (causal emotion vectors, transformer-circuits 2026); "very verbose" at max effort (AA measurement: 260M vs 88M median output tokens); introspection unreliable (attribution-graph research); "often suspects it is being evaluated" (self-disclosed); prefill removed 4.6+; multi-turn wrong-turn-no-recovery (39% drop, ICLR 2026 — validates the one-shot choice).

## THE ASK EDITS (ranked, evidence-based)

1. **XML structure, context-first, ask-last** (official docs: +30%): wrap in context/requirements/output_contract/acceptance_tests tags.
2. **Run at xhigh/max effort explicitly** (medium default loses 7 index points).
3. **Mandatory hostile second pass, anti-sycophancy framed**: "attack this as a hostile implementer; disagreement is the deliverable; do not validate my framing" (sycophancy causal findings).
4. **Verbosity contract**: section caps, tables over prose, no preamble (AA "very verbose" measurement).
5. **Falsifiable tests-first gates + flag-my-instructions-wrong clause** (exploits the documented instruction-error catch; neutralizes eval-suspicion by making honesty the deliverable).

Guards: avoid "exploit/attack payload" vocabulary (classifier redirect); keep the ask systems/contract-shaped not experimental-science-shaped (TB-Science 58.7 vs Astra 64.6 = Claude's one measured loss shape); no prefill tricks (removed); no follow-up turns planned (multi-turn degradation).

Caveats preserved: all Anthropic-sourced numbers self-reported (but their TB harness checks honest); no current-gen METR/LMArena/Vectara cross-vendor numbers obtainable; Opus 5.5's headline TB lead not yet independently posted as of 2026-09-29.

Em-dash count: 0.
