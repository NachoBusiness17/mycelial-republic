# R4 — CASCADE STOPPING (the Perplexity steal, research seam)

Date: 2026-09-10. Lane R4. Organ: `mag/cascade_research.py`. Audit pattern inherited from
`mag/librarian.py` — deterministic, stdlib-only, one pass, tri-state, report on disk.

## THE STEAL

Perplexity's trick made fleet-law: rank research cheap-to-expensive, and put a HARD
STOPPING FLOOR on every tier. Never spend a dearer tier on a question a cheaper tier
already answered.

| tier | cost | surface | floor (stop condition) |
|---|---|---|---|
| 1 | $0 | invariant sheet, bibliography map, cards under watch/ + docs/ + configs/ | ≥2 independent local sources (distinct files, anchored on the corpus-rarest keyword) |
| 2 | pennies | deepseek research seam (receipt ingested via `--tier2-json`; script never holds keys) | answer hits ≥2 question terms AND union of tier-1+tier-2 independent sources ≥2 |
| 3 | frontier $ | subagent dispatch payload | OPERATOR GO only (`--go`); gate named, never paid silently (launch law amendment 5) |

Key design point found by the test itself: v1's floor counted keyword co-occurrence
only, and passed on 1,186 files of noise ("fleet"+"state" match everything).
**A floor that always passes is not a floor.** Fix: rarest-term anchoring — a file
only counts if it contains the corpus-rarest keyword (df-minimal, here "nyquist")
plus ≥2 distinct terms. Floor v2 is honest.

## TEST — "What is the Nyquist sampling rate for fleet state changes?"

Cascade trace: TIER 1 → STOP (floor met, 3 independent sources, $0). Tiers 2 and 3
never fired — that is the organ working, not skipping.

Independent sources: `watch/inbox/mickey/G4_6_adjacent.md` (Nyquist 1928 origin row),
`watch/inbox/mickey/G5_1_nyquist.md` (the measured falsifier), `watch/SELF_STEAL_CHORD_THEORY_20260903.md`.
JSON receipt: `watch/inbox/mickey/R4_cascade.json`.

## THE ANSWER (tier 1, $0)

**fs ≥ 2 × f_max.** The fleet's state vector is (n_sessions, n_complete, n_leaves,
tip_root); sustained it moves at 0.038 changes/min (one transition per ~26 min over
71.2h of kpi.jsonl), so the Nyquist minimum sampler is **one poll per 13.2 minutes**.
The sanctioned 18-25s wave heartbeat samples **~37x denser than required** (margin
32-44x across the band) — it reconstructs state change up to 1.2-1.67 changes/min,
and aliasing only threatens during sub-minute bursts (observed once in 71h), where
the heartbeat sees before/after but not between; trajectory survives in kpi.jsonl
and the verkle chain. Standing tripwire: 3+ state changes in two consecutive minutes
→ tighten heartbeat to ≤10s.

## STATE

- Built + tested: `mag/cascade_research.py` (tier 1 live, tier 2 receipt door, tier 3 GO-gated dispatch).
- Unproven residue, not open work: tier 2 seam receipt format is exercised but no real
  deepseek receipt has run through it yet; tier 3 has never fired (correctly).
- Worst-case economics: questions the corpus already owns cost $0 — the desk's
  default posture is now "tier 1 before any seam spend".
