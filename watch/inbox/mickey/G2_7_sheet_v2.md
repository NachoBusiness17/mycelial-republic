# MICKEY G2-7 — INVARIANT SHEET V2 (scite steal: refutation column)

2026-09-10 · zcode seat · changes + comparison vs v0. Full report: `watch/INVARIANT_SHEET_V2.md`.
v0 report left frozen as the repetition-only baseline: `watch/INVARIANT_SHEET.md`.

## WHAT CHANGED (mag/invariant_surface.py v0 → v2)

- STEAL SOURCE: `watch/inbox/steal_research_pipeline/BOT_B_claims.md` — scite's whole product
  is classifying DISAGREEMENT; our corpus had no disagreement detector, only accumulation.
  BOT B's exact diagnosis: "Percolator counts repeats but never counts refutations."
- v2 binds the percolator-style repeat count as `agreement_count` (unchanged semantics:
  duplication is emphasis) and adds a REFUTATION column on top. No edits to
  mag/percolator.py — the sheet is the surface that reads its output shape.
- CONTRADICTION DETECTION (deterministic, no model in the loop): a line carrying a
  negation marker (not, never, isn't, don't, wrong, false, disputed, refuted, fails,
  without, no, ...) is a NEGATIVE line. Two lines share a SUBJECT when they overlap on
  >=2 salient tokens (stopwords + domain filler stripped) covering >=40% of the smaller
  side. Each negative line on the same subject scores its own repetition count AGAINST
  the positive line — a contradiction repeated is emphasis too. Direction is one-way:
  negative refutes positive (laws like "never retry" refute positive "retry with backoff").
- NEW COLUMNS: `agreement_count`, `refutation_count`, `net_score = agreement − refutations`.
  RANK KEY: net_score (was raw frequency). Net can go negative — a negative net is a
  disputed claim, left visible on purpose.
- NEW SECTION: CONTROVERTED — lines with agreement >=2 AND >=1 refutation, ranked by how
  hard they're contested. These are the live debates.
- NEW SECTION: MOVEMENT vs v0 — rank deltas (repetition-only rank → net_score rank).
- BUGS FOUND WHILE BUILDING: (1) generic tokens (card/line/file) drove spurious subject
  matches — added a domain-stopword layer; (2) the report was sweeping its own output
  into the corpus on re-runs — output file now excluded from the walk.

## RUN NUMBERS (600 files walked, 8.3s, stdlib only)

- 1,612 unique invariant lines; 452 negative lines; 360 positive lines caught >=1
  refutation; 30 CONTROVERTED.
- Buckets (unique → surfaced): LAW 106→20, VERDICT 781→20, FALSIFIER 194→12, MEASURED 531→20.

## TOP CONTROVERTED (live debates)

1. `[agree=3 vs refute=12 · net=-9]` "per family references (the SUPPORTED tri-state row
   above...)" — the Astra condition-arithmetic family; hardest-contested line in the corpus.
2. `[a=3 r=4 · net=-1]` CAMP STATE v0+v1 pinned verbatim, **SUPPORTED** (ASTRA_CAMPAIGN_LOG).
3. `[a=3 r=4 · net=-1]` "second witness auto-demotes to UNPROVEN; witnesses partitioned
   across seats" — the promotion/demotion rule itself is contested ground.
4. `[a=2 r=7 · net=-5]` I4 falsifier re-run cluster (contested denominators).
5. `[a=2 r=6 · net=-4]` "The knot store holds 21,264 knots" — the DISPUTED→13,678
   correction lives right next to it; v0 ranked this purely by repetition.

## WHO MOVED vs v0

- DOWN 9 (MEASURED #6→#15): "(94% PASS), rotation 0.950, tesuji ~310 cells vs 200 bar,
  MAX_DISTILL epoch-1..." — repetition made it look consensual; refutations pulled it down.
- DOWN 8 (FALSIFIER #11→#19): Falsifier F-H0 (3 consecutive desk rejections of seed...).
- DOWN 5 (LAW #4→#9): "Ollama local (exploratory tip — cheap, always on)" — flagged as
  contested against the no-default-senses law cluster.
- UP 4 (VERDICT #20→#16, #21→#17): "data is UNPROVEN, never Supported (corrections law 6)"
  and "Disagreements that survive adoption are preserved as explicit DISPUTED lines" —
  the tri-state discipline lines survive refutation pressure and rise.
- Pattern: v0 rewarded volume; v2 rewards volume that survives disagreement. Migration
  rows from ANSWER_2.md dominate the top because they carry both SUPPORTED rows and the
  DISPUTED lines that attack them — exactly the debate signal scite charges for.

## FALSIFIER (honest limits)

- Negation-marker + token-overlap is a cheap classifier: it will false-positive on lines
  that merely share vocabulary ("family", "witness") and miss semantic contradictions
  worded without markers. Expect precision, not recall. Next step if the operator GOs:
  few-shot a free lane (BOT B's proposal) to classify supports/contradicts/mentions for
  the CONTROVERTED shortlist only — ~30 calls per run, pennies.
