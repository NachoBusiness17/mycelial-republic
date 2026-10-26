# X INTEL: shared memory in looped transformers (2026-10-05)

Operator drop: "https://x.com/arXivBangers/status/2106990575883096532"

## Verified at the primary

arXiv 2610.02383v1 (2026-10-01): "The Surprising Effectiveness of Shared
Memory in Looped Transformers" - Monea, Ramji, El-Kurdi, Lastras, Artzi,
Godey, Fernandez Astudillo (IBM Research + Cornell NLP lineage), fetched
from the arXiv API this session. The tweet's claim is ACCURATE to the
abstract: pretraining looped language models where ONLY THE FIRST
RECURSION WRITES THE KV CACHE and later recursions read it (a small
private window retained) - their Looped Prediction Transformer and a
hybrid, at five recursions, reach 1.12-1.82 LOWER validation perplexity
on FineWeb-Edu than same-size standard transformers while using 76-79%
LESS CONTEXT MEMORY, across 150M-1B parameters.

## Why it matters to the estate

CONTEXT MEMORY IS THE LOCAL BOTTLENECK. The estate's hardware doctrine
(the DDR3+12GB lattice serving, the DeepSeek cache-persistence law, the
3090-class vast rungs, the Pixel body) keeps hitting the same wall:
context KV cache size, not compute. A looped model that writes its cache
ONCE and re-reads it across recursions holds roughly 4x the context in
the same VRAM at the 1B class. Concrete doors:

1. THE MYTHOS HARDWARE TABLE GAINS A FAMILY: beside qwen3-4b and
   gpt-oss-20b on the vast-box menu, the looped-small class (LPT-style)
   becomes the "context-per-GB" candidate - relevant the moment a
   local model must hold long receipts/trails in context.
2. The Strata/RAM-as-lattice line: cache-write-once + read-many is
   architecturally friendly to the slow-RAM fast-GPU split (the hologram
   plate is written once; recursions are lookups).

## Honest limits

This is a PRETRAINING result on FineWeb-Edu perplexity at 150M-1B - no
instruct tuning, no agentic or long-context downstream evals, no repo
named in the abstract. Promising primitive, unproven downstream: WATCH
class, not adopt. The loop echo (weights re-applied across recursions =
the architecture cousin of the estate's process loops) is a rhyme, not a
mechanism - filed as one line, no more.

No action fired; no clone (paper, not repo).

fetched: 2026-10-05
Writer: zcode-53-strategy-window
