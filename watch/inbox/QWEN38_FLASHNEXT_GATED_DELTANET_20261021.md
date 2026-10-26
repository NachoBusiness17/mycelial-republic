# INTEL: Qwen3.8-Flash-Next - the KV cache elimination (2026-10-21)

Source: jun (@jun1228909) tweet, Oct 21, translating the Japanese AI
community's read of Qwen's release. Model: Qwen/Qwen3.8-Flash-Next on HF,
created Aug 24 2026, 2.7M downloads, 6,392 likes, 144 files. This is real,
shipped, and heavily adopted - not vapor.

## The architecture (the self-steal target)

Of 48 layers: **36 are Gated DeltaNet** - linear attention holding history
in a FIXED-SIZE state, no growing KV cache. 12 are Sparse Attention
referencing past KV. Hidden layout: 12 x (3 x (Gated DeltaNet -> MoE) ->
1 x (Qwen Sparse Attention -> MoE)).

The quoted founder's line: "I will get rid of kvcache, just watch me do
it." The mechanism per jun's read: fixed-size state holds history;
recomputing needed KV per-query is implausible; the elimination is a
replacement by another compressed state.

## Why this lands on the estate's desk with weight

The estate's water computer holds history in fixed tanks with
delta-rule-style flow: input mixes into the tank, the tank's state is the
memory, the vessels never grow. **Gated DeltaNet IS that design in a
frontier model layer**: a fixed-size matrix state updated by a gated delta
rule - history compressed into a vessel that never expands with context
length.

The estate's own metaphor language - water computer, fixed tanks, the
record growing inside bounded vessels - turned out to be the design
direction of the post-transformer frontier. Not because anyone copied the
water computer. Because the physics of memory-per-token pushes every
scaled system toward the same shape: bounded state, delta updates,
compressed history.

The same-book program's commons has the identical shape at the idea
layer: the whole record, fixed vessels, append-only, queryable.

## The three steals

1. **The architecture validation.** The frontier just moved toward
   fixed-state, delta-rule memory. The estate's water computer design and
   the same-book commons design are on that direction's bearing. The
   design language of the house is now a research bet placed by a $1.5B-
   adjacent lab family (Alibaba/Qwen).
2. **The reader opportunity.** A model with fixed-size state reads
   UNBOUNDED context at constant memory. If Qwen3.8-Flash-Next lands on a
   free lane, it is the corpus-scale reader the same-book program wants:
   the whole record, the whole drops archive, readable without the KV
   explosion. Watch the free lanes for it.
3. **The Termux angle.** Fixed-state linear attention models are
   dramatically cheaper at inference than full attention. If the weights
   come in sizes old phones can hold, the phone mesh's COMPUTE role
   upgrades: the 1-3B-class reader limit was the binding constraint; a
   fixed-state model changes the memory math. The phone mesh spec's
   compute role re-opens.

## Falsifier

The architecture's real-world claim (unbounded context, constant memory)
is testable the moment weights or an API are accessible. If long-context
benchmarks show the fixed state degrades like every compressed-history
attempt before it (the graveyard of linear attention is long), the
architecture is another windmill. The graveyard is the prior; the 2.7M
downloads and the Qwen shipping weight are the counter-evidence. Watch
the benchmarks, not the launch.

## Sources

- jun's tweet with the Hidden Layout diagram
- HF: Qwen/Qwen3.8-Flash-Next (this sitting)
- The quoted line from the Qwen side: "I will get rid of kvcache, just
  watch me do it"
