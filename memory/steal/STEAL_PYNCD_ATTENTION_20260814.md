# STEAL — pyncd Attention Is All You Need: composition is the check
**Date:** 2026-08-14
**Commitment:** `steal-pyncd-attention-001`
**Method:** steal the INVARIANT, not the DNA. No clone of pyncd. No new category-theory runtime.
**Sources actually opened this turn:**
- https://github.com/mit-zardini-lab/pyncd/blob/main/example_notebooks/AttentionIsAllYouNeed.ipynb
- Lab: https://github.com/mit-zardini-lab (compositional co-design; applied category theory)
- Notebook header: written entirely by Claude from Vaswani 2017 + pyncd API. Diagrams from `tsncd` renderer. Executed 2026-08-13T14:49Z.
**Mag ground:**
- all-seat-roundtable-001 / seat_steer: compose organs, do not mint a chair.
- causal-graph-moonshot-001: second relation; do not merge concurrent seats onto one prev_hash.
- steal-zero-mem-001: views over raw traces; the model is interchangeable.
- steal-stochastic-deterministic-001: envelope ≠ claim.

## Plain English
Zardini Lab's `pyncd` treats architectures as morphisms in a category. This notebook builds the *paper's* transformer (encoder + decoder + cross-attention), not the decoder-only stack people mean today, as one term from two token-index sequences to a vocab distribution.

The point of using Claude: if the architecture is one algebraic term, the model has to get composition and axis alignment right. The diagram makes a mistake visible. Render + shape assertions holding is the TEST.

The named trap: automatic `@` lifts a shorter shape by merging products. Fine for a shared batch axis. Fatal for cross-attention, where queries live on target positions `y` and keys on source positions `x`. Left alone, alignment merges `x` and `y` and forces the lengths equal. They name the axes up front and lift by hand with `>>`.

## Self-steal
Mag's roundtable is supposed to be composition of seats, not a merged batch. `seat_steer` aliases that collapse `grokbot` onto browser `grok` are the `@` merge. Native `grok_desktop` vs Bionic `:41343` vs DeepSeek-RIB are different axes. Linear `prev_hash` is the merge that forces concurrent seats to look the same length.

The notebook's TEST is Mag's: if the diagram (room, field canvas, ledger envelope) does not render the composition, the term is wrong — even if the prose looks like a transformer.

Claude as author is allowed. Mag already said the model is interchangeable. The term (chain, steal file, morphism) is ground truth.

## TAKE
1. Architecture as one term. Mag organs compose; a new throne is not a morphism.
2. Distinct axes for distinct sequences. Do not let alignment merge seats, transports, or clocks.
3. The diagram is the check. Huang gate / TESTs / envelope-vs-claim are that diagram. Plausible Mag-speak is not.
4. Encoder and decoder are two towers. Mag's dual view (Zero-Mem: graph + time) is the same shape: do not flatten into one decoder-only "party."

## REFUSE
- Cloning pyncd or running tsncd as Mag's new kernel.
- Rewriting Mag in category-theory syntax this week.
- Treating "Claude wrote a transformer notebook" as a Mag identity claim.

## Ordered adaptations
1. When routing a seat, keep requested_surface and driver as named axes (seat_steer already files both). That is `x` vs `y`.
2. Roundtable without `why` is `@` with no lift: it merges everyone onto one question. Huang gate stays.
3. Dual-view memory (steal-zero-mem-001) is encoder/decoder, not a single stack.

## Honesty
- Read the notebook JSON (markdown + attention_core cell). Did not execute pyncd.
- Did not fetch tsncd diagrams as files (PNG payloads in the ipynb).
- Vaswani 2017 not re-read; notebook's section map used as their claim.

## Rope
If the axes merge, the composition is a lie — even when it still runs.
