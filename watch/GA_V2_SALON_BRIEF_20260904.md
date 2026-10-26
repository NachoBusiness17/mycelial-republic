# SALON BRIEF — gen-1 improvement: fitness v2 for the fleet gene pool (2026-09-04)

Subject: the genetic algorithm's first pass over the audited fleet produced a
MASS MAP, not a VALUE map. Salon question: design fitness v2. Then next gen.

## GEN-1 RESULTS (receipted, memory/audit/gene_pool_gen1.json)
Pool: 73 genes / 6 domains (code_files, verkle_chain, memory_structures,
research_corpus, orphan_notables, external_orphans). 25 selected.
Fitness v1 = 3*emphasis + 2*(scored|receipted) + 1*(loaded) + recency(+2).

Top 5: mem:ghost 342,657 (114,218 files) · mem:biography 85,335 (28,444
knots) · knot:orphan_files 63,792 (21,264 unindexed) · knot:theme:NULL
15,548 (5,182 rows) · mem:knowledge_graph 5,749 (1,916 nodes).
Orphans appear only as emphasis classes. Zero fitness-zero genes (operator
law: duplication is emphasis).

## THE PATHOLOGY (honest)
v1 conflates EMPHASIS with VALUE. The top of the table is the biggest piles:
ghost (114K files of daemon runtime), legacy-NULL chain rows (5,182 rows of
memlang bulk import — 72% of the chain is NULL-thema legacy), the orphan
class itself. Real findings (21K off-chain knots; the stale graph read by 29
organs) rank high for the right reason — but ghost's 342K is bulk, not
worth. v1 measured WHERE THE MASS IS. Gen 2 must measure WHERE THE VALUE IS
without violating the operator law: duplication is still emphasis; duplicates
still weight; nothing gets culled for being a repeat.

## CANDIDATE IMPROVEMENTS (from the seats' dialectic + today's laws)
a. **Density normalization**: fitness_density = fitness / mass (per-KB,
   per-file, per-knot). ghost's 342K ÷ 114K files ≈ 3/file — a one-card
   skill with 3 receipts outranks it instantly. Risk: penalizes genuinely
   massive organs (the chain SHOULD be big — it's the source of record).
b. **Two-axis split** (the accumulator's own law, recency × certainty):
   EMPHASIS axis (mass, duplicates) × QUALITY axis (scored/receipted/
   falsified). Report both, never sum them. A gene can be high-emphasis/
   low-quality (ghost: real but unjudged) or low-emphasis/high-quality
   (the light falsifier: 100/0 but one file).
c. **Per-domain z-score**: normalize fitness within each domain before
   cross-domain ranking, so memory_structures doesn't dwarf research_corpus
   by unit size alone.
d. **Falsifier multiplicative boost**: genes with an actual falsifier RUN
   today (light replay 100/0, LAW 13 probe, harness 0.71, accumulator
   13/13) get multiplied, not added — measurement is worth more than
   assertion. But see the Witness's shadow: measured ⊊ true.
e. **Recency decay with a floor**: touched-today bonus decays over days but
   never below a service floor (the Elder's serviced-invariant class is
   real — some genes are alive precisely because they are re-applied).
f. **The NULL-thema exception**: 5,182 legacy-NULL rows are bulk-import
   artifacts, not genes — candidate for a mass-import class that counts as
   ONE gene (the import event), not 5,182.
g. **Constraint — the operator law stands**: duplication = emphasis-weight,
   never fitness-zero. Any v2 that culls duplicates for being duplicates
   violates doctrine and is rejected pre-hoc.

## THE SALON'S QUESTIONS
1. Which improvements make fitness v2 — pick the composition, argue the
   weights or argue against weights (two-axis reporting instead of a scalar)?
2. Is "fitness per KB" the right density denominator, or does mass itself
   carry information (the chain's bigness = its job)? Where does density
   lie?
3. How should the NULL-thema legacy class be treated: one gene, excluded, or
   its own domain?
4. What does gen 2 SELECT FOR — what is the fleet actually trying to discover
   with the next generation (candidates: retirement candidates? build-order
   input? light-broadcast priority? dependency for the joint test)?
5. The falsifier: what observable result would prove v2 is WORSE than v1
   (the kill-switch for the improvement itself)?
Tri-state, deterministic, no invented numbers. The duplication law is
binding: nothing gets culled for repetition.
