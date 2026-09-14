# LIBRARIAN METHOD — how the salon generates a map (parsed 2026-09-11 night)

**THE POINT:** The operator showed the finished artifact (five waves, 1,346
lines) and ordered: parse it, learn to generate it ourselves. The method,
extracted into eight disciplines. This card is the generator's spec; the
librarian organ enforces it.

## The eight disciplines of the generator

1. **CONFESS THE COMPILATION.** A bibliography assembled by the model it
   documents is self-serving by construction. Every generated map opens with
   its own epistemic status: no live retrieval = every entry is a RETRIEVAL
   PLAN, not a citation set, until the primary text is pulled and hashed.
2. **LEGEND EVERY ENTRY.** [V] held-from-training (byte details may err) ·
   [M] map-provided, cannot vouch · [S] soft source · † lowest confidence,
   check first. Provenance is per-entry, never per-document.
3. **TIER BY OBLIGATION.** Tier 0 = the operator's own lineage (held, not
   vouched). Tier 1 = named aloud in-thread. Tier 2 = THE UNNAMED DEBT — what
   you used but never cited (the self-audit that produces the gold). Tier 3 =
   should-have-cited-didn't, and these GATE BUILDS — they are processed first.
4. **THE UNNAMED DEBT IS THE PRODUCT.** The self-audit question is not "what
   did I cite" but "what did I use without citing." That is where PagedAttention,
   Mooncake, Kraska, AGM, Dynamo, Hurlbert, Lamport came from — every one a
   load-bearing ancestor the map never named.
5. **MINE ADJACENT FIELDS ON PURPOSE.** The salon's central finding: our two
   load-bearing claims had canonical citations in fields we never drew from —
   Dynamo/Merkle (distributed systems) for the record, Hurlbert 1984 (ecology)
   for replication — and nine frontier models missed them in the same
   direction. Correlated blind spots are structural, not accidental; the
   countermeasure is a standing adjacent-field sweep (distributed systems,
   ecology/metascience, safety engineering, formal methods, economics).
6. **PRESERVE DISAGREEMENT IN THE ARTIFACT.** Original and enhanced folds stay
   separate; provenance and disagreements remain inspectable rather than
   silently reconciled. (Duplication is emphasis; silent reconciliation is loss.)
7. **EXTRACTION PROTOCOL HAS AN ORDER.** Tier 3 first (gates builds), then †
   entries (lowest confidence), then out-of-horizon IDs; hash each primary at
   pull; attach one verbatim excerpt per load-bearing use. That moment — pull +
   hash + excerpt — is when a retrieval plan upgrades to a citation set.
8. **THE FINDING GOES IN THE FOLD.** Housekeeping contains a thesis: the map
   documents not just what to read but HOW the canon is unevenly distributed
   across training — sovereign architecture mines adjacent fields deliberately.

## Adopted into the fleet
- BIBLIOGRAPHY_MAP.md: new THE UNNAMED DEBT section (retrieval-plan status,
  [V]/† provenance flags) — the Tier 2/3 gold, pending primary pull.
- Status vocabulary gains RETRIEVAL-PLAN (above SECONDHAND, below PRIMARY-READ).
- librarian.py v1 next: add PULLED/HASHED state per row; Tier-3 rows sort
  first; the 190 unregistered citations get triaged against these tiers.
- Desk law: every intake sweep now includes one adjacent-field pass (a field
  the thread never mentioned).
