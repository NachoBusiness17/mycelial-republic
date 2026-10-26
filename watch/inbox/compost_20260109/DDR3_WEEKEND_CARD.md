# DDR3 WEEKEND CARD - the frozen upcycle-survivor recipe (2026-10-09)

The upcycle hope (7B dense -> linear/SSM at home) was killed 2026-10-01 by
cluster-class arithmetic (compost ledger row `upcycle-linear-conversion`, git
4d67a7283 verdict 6: 150B tokens = ~579 consumer-GPU-days even at 2 pct MoE
upcycling), and its own autopsy named the one surviving door:
**ddr3-body-is-the-training-tier**. This card freezes that door's recipe so
the next idle weekend runs it instead of re-deriving it - the descent
protocol's prior-art sweep applied to our own compost (COMPOST_MAP.md section
5, revival 3).

Source of record (every number below traces to it unless marked ESTIMATE):
`watch/inbox/spiking_wide/upcycle-economics.md` (the upcycle autopsy lane
receipt, GO 2) + `watch/inbox/wave_20260916/receipts/B10_MLP_KV_CACHE_PRIORART.md`
(the eval bar, B11-verified) + `watch/inbox/STRATA_DROP_20261001.md` (the
hardware). Paper of record: arXiv 2403.17887 "Unreasonable Ineffectiveness of
the Deeper Layers" (the R2 recipe: angle-similarity depth prune + QLoRA heal).

## Inputs

| Input | Value | Source |
|---|---|---|
| Hardware | the DDR3 body: $200 used box + 64GB DDR3 + used 12GB GPU, ~$300 total | STRATA_DROP_20261001.md |
| Base model | a 7B-class base, chosen by its collapse band, not vibes: paper collapse points are ~45-55 pct cut (Llama-2), ~35 pct (Mistral-7B), ~25 pct (Phi-2), ~20 pct (Qwen) | upcycle-economics.md R2 row (arXiv 2403.17887) |
| Prune ratio | 20-35 pct of layers (stay below the chosen base's collapse point) | upcycle-economics.md GO 2 |
| Heal | QLoRA, 5000 steps, batch 16 | upcycle-economics.md section 2 GO row |
| Token budget | 164-328M tokens (5000 steps x batch 16 = 328M; C4 or the estate's own residual corpus) | upcycle-economics.md section 2 GO row |
| Wall-clock | ~30-45 GPU-h at a derived 2-3k tok/s consumer QLoRA rate - ESTIMATE, unconfirmed on-box | upcycle-economics.md section 2 GO row (derived) |
| VRAM fit | 7B at 4-bit ~3.5GB weights, the only full recipe plausibly inside the 12GB GPU - ESTIMATE, on-box confirmation owed | upcycle-economics.md section 2 (derived from R2's 17.5GB half-pruned 70B at 4-bit) |
| GPU spend | $0 marginal (the estate's own box; the 4GB AMD box cannot run this shape - "NO: below every published training shape") | upcycle-economics.md section 2 table |

## Steps (one weekend)

1. PRE-STEP (one sitting, the 4GB AMD box, $0, run FIRST - it is the
   falsifier): GO 1 from the autopsy - Gromov-style angle-similarity layer
   probe on the janitor tier (gemma:2b / gemma4), quantized forward passes,
   drop 2-4 layers, requant, score on the estate's own eval cards
   before/after. No heal. Banks "how many layers does the janitor actually
   need" (upcycle-economics.md GO 1).
2. Pick the base by collapse band (Inputs table); depth-prune 20-35 pct of
   layers by angle-similarity (SAP method, arXiv 2403.17887).
3. QLoRA-heal 5000 steps, batch 16, on the 164-328M token slice.
4. Score: MMLU/BoolQ near-flat is the paper's expected band below the
   collapse point (upcycle-economics.md R2 row; the heal restores C4 loss,
   lifts QA only modestly - do not expect QA gains).
5. Run the recall card against R0 SWA+4-sinks (the bar below).

## Eval bar (vs SWA+4-sinks)

**The pruned model must hold near-flat MMLU/BoolQ vs its unpruned teacher AND
beat R0 SWA+4-sinks on the estate's own long-context recall card - else the
surgery bought nothing the free incumbent does not already give.** R0 is
training-free, 0 GPU-h, recovers 99 pct short-context quality and beats every
post-trained linearization 2-10x on long-context recall (B10 receipt, B11
verified, arXiv:2608.28444); at 4K NIAH the linearizations recover 1-6 pct of
full attention vs SWA's 17-25 pct. A conversion only earns its surgery by
buying constant-state long-context serving (the 3:1 hybrid form is the only
form that clears the recall bar - the pure form never does).

## Falsifier (pre-registered, from the autopsy's decision ledger)

Run the PRE-STEP first: if a 20-35 pct layer cut WITHOUT heal degrades the
estate's own eval cards by more than ~5 pct (upcycle-economics.md section 5),
the convert-don't-train lane is dead at every estate budget tier - healing is
then proven necessary but only affordable on cloud - and this card's weekend
collapses to no-go before any GPU-hour is spent.

## Closeout (bank either way)

- PASS: the estate's first measured conversion at ~$0 GPU spend - the
  cheapest per capability point that fits one weekend (upcycle-economics.md
  section 4); file the receipt, update this card's ESTIMATE rows with
  measured tok/s and GB, and the DDR3 body is proven as the training tier,
  not just an inference pager.
- FAIL (misses the recall bar or the MMLU band): R0 SWA+4-sinks stays the
  incumbent; file the corpse as a compost ledger row with this card as
  killer_bytes - the pre-registered falsifier makes the kill cost one
  receipt, not a re-derivation.
- Either way the numbers land in a receipt and the card is consumed: it
  exists so nobody re-derives the recipe (the estate-already-solved-it law,
  AGENTS.md DRIVING LADDER).

Revival lineage: compost ledger row `upcycle-linear-conversion`
(revival_condition: a hybrid clears the recall bar on its own, or GPU-days
become free); COMPOST_MAP.md section 5 revival 3. Falsifier for the card
itself: a second idle weekend that re-derives the prune/heal numbers instead
of running this card = the card failed to freeze; fix the card, not the
operator's memory.
