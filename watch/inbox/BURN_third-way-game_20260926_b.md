# BURN receipt: third-way-game, 2026-09-26 (_b)

## Verdict
steal

## Evidence
- "The GRACE line schema is named owed, not fabricated." (BURN_third-way-game_20260926.md, item 2). This pass closes that debt.
- The line being superseded: "log every grace roll as `GRACE t=<mm:ss> d1= d2= total= pass=`; the two sequences must match roll for roll, and totals ≥7 must sit at the 2d6 rate (15/36, about 41.7%) with no smoothing." (BURN_third-way-game_20260925.md, Seed audit)
- Canon guard the logging must respect: "The luck shrine must never narrate purpose into a grace roll." (STORYTELLER_SIX_RACTOR_20260925.md, Unstuck chair). The schema logs mechanics only: no destiny field, no narrative.
- Web: TWO fresh searches run 2026-09-26 (RNG audit / drop-rate telemetry; provably-fair seed-hash logs). Every attempt returned HTTP 429 (z.ai error 1302, the plan's concurrency cap). OWED, nothing fetched. The search layer's general-knowledge outline (commit-reveal, hashed server seeds) was treated as unread and uncited per the no-fabrication law.

## Steal or Vacuous
Steal. Two artifacts landed:

1. watch/inbox/THIRD_WAY_GRACE_SCHEMA.json - JSON Schema (draft 2020-12, additionalProperties=false) for the shrine's per-roll GRACE line. Nine fields, all required: seat (string), t (ISO-8601 UTC, pattern-pinned to Z), pair_id (string), seed_hash (64 lowercase hex, sha256 of the session seed, never the seed itself), mode (peeked|unpeeked), improbable_spent (number >= 0), roll_total (integer 2..12), outcome (miss|pass|grace), grace_pool_id (string). outcome is documented mechanically: miss under 7, pass at 7 plus, grace via the pool. This supersedes the free-form 20260925 GRACE line the way the VOW schema locked VOW-TAKEN.
2. watch/inbox/BURN_third-way-game_20260926.md - addendum section appending the schema-consistency rule to that receipt: peeked and unpeeked rolls MUST log identical field sets; the seed audit compares distributions across the shared fields only; both legs of a pair share one pair_id and one seed_hash.

Design note: the field set is deliberately narrative-free (canon guard above) and distribution-comparable (the audit needs identical shapes on both legs, which is why mode is a field rather than a separate log).

## Falsifier
Pre-registered, F9-grace-audit: in the two seed-matched 20-minute runs, every GRACE line must validate against THIRD_WAY_GRACE_SCHEMA.json. Any schema-invalid line, any field-set divergence between the peeked and unpeeked legs, or any divergence between the two same-seed roll sequences voids the Unpeeked Seed claim and the shrine ships as peeked until fixed (extends the 20260925 seed falsifier). Totals >= 7 must sit at 15/36 with no smoothing across the shared fields. A raw seed appearing in any log line voids the pair outright.

## Bibliography
- watch/inbox/STORYTELLER_SIX_RACTOR_20260925.md (read)
- watch/inbox/BURN_third-way-game_20260925.md (read)
- watch/inbox/BURN_third-way-game_20260926.md (read, extended with addendum)
- watch/inbox/THIRD_WAY_GRACE_SCHEMA.json (created this pass)
- Web search 2026-09-26, two queries, all attempts HTTP 429 / error 1302: OWED, not read, not synthesized.
