# B9 — Matthew Zenodo DOI backfill (2026-09-16)

**Lane:** B9 · **Writer:** backfill-zenodo-20260916 · **Status:** IN PROGRESS

## Source ask

Operator drop 2026-09-14 (`queue/lanes/research/inbox.jsonl`):
"Fetch remaining 4 Matthew Zenodo DOIs: 17504630, 17562815, 17586111, 17674366 —
complete the series behind capstone 17811909; register each in LINKS.jsonl."
Card: `watch/inbox/RASHOMON_SURFACE_ELEPHANT_20260914.md`.

## Dedupe check

`grep -i zenodo watch/inbox/LINKS.jsonl` (2026-09-16): only `zenodo.org/records/17811909`
(rashomon writer) and `10.5281/zenodo.22759599` (journal-window writer) present.
None of the 4 target DOIs registered → all 4 remain.

## Registrations

(appending as I go)

1. `https://doi.org/10.5281/zenodo.17504630` — **REGISTERED** (writer backfill-zenodo-20260916).
   "Emergence of Prompt-Induced Simulated Metacognitive Behaviors in a Quantized LLM via
   Entropy-Governed Hypergraph Prompting [Preprint]" — M. Steiniger, 2025. = **Valora**:
   prompt-only hypergraph framework simulating metacognition (self-reference, recursion)
   in quantized Gemma-3-27B-it on consumer hardware. Corpus slot: AI paper #9
   ("Valora V2 hypergraph prompting").

2. `https://doi.org/10.5281/zenodo.17562815` — **REGISTERED** (writer backfill-zenodo-20260916).
   "Narrative Genesis Injection and Semantic-Counter-Vectors for Simulated Metacognition
   in LLMs [Preprint]" — M. Steiniger, 2025. Lightweight in-context metacognition
   simulation via semantic-counter-vectors + custom narrative injection, on everyday
   hardware.
