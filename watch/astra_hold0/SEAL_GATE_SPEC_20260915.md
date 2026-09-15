# SEAL GATE SPEC — HOLD 4 preconditions (frozen 2026-09-15)

Implements Astra's v2 review, "Seal repairs" paragraph, verbatim in force.
One gate, seven conditions, ALL simultaneous. Author: zcode seat (astra repair
lane, operator GO "go on astra" 2026-09-15). Status: FROZEN — desk adoption
appends the detached-manifest line.

## THE GATE

No confirmatory episode fires until every condition below holds ON THE SAME
DAY, receipted in one HOLD 4 seal log (`watch/astra_hold0/qa/HOLD4_SEAL_LOG.md`).

1. **Simultaneous lower confidence bounds, B−C above +5.** The B−C comparison
   (bundled arm vs single arm) reports ONE-SIDED lower confidence bounds for
   the score gap computed SIMULTANEOUSLY across all six families — six
   intervals, one joint procedure, multiplicity controlled (no per-family
   cherry-picking). The gate passes only if EVERY family's simultaneous lower
   bound is > +5 (0–100 scale).
2. **ONE block-aware method.** The inference method is frozen HERE, before
   HOLD 3: **paired block bootstrap over episodes, 10,000 resamples, seed
   20260915, blocks = task families (six blocks), statistic = per-family mean
   gap, joint bound = min over families of the one-sided 95% percentile
   bootstrap lower bound with Šidák adjustment (α' = 1−0.95^(1/6))**.
   "Bootstrap OR permutation" is retracted — the disjunction was the defect;
   this single method is the repair. Changing the method after any scored
   episode is a seal-breaking event.
3. **Model pins before scored calls.** Every arm's model, provider, and
   thinking level is pinned in the desk log BEFORE that family's first scored
   episode (lane rows already carded: free reasoning lane, thinking=low; the
   pins are the manifest §5 rows as-run). A mid-run model change = the
   family's episodes to date are voided to pilot status.
4. **Complete instances.** All six families authored FULL: I1 (v5), I4 (v3),
   I5 (v2+), I6 (v2+) — done; I2 and I3 remain to be authored from the adopted
   skeleton pins (A9/A10; I3's ground truth inherits SEED_001 amendment row 3's
   reconstruction receipt). A family without a complete card does not gate.
5. **Complete QA logs.** `watch/astra_hold0/qa/` holds one end-to-end
   qa_receipt log per family (I1–I6) plus twin samples (S1–S6 at HOLD 2b),
   each manually checked for API errors and tool failures before its receipt
   signs. No qa_receipt, no gate.
6. **Detached byte hashes.** `BUNDLE_RAWBYTES_SHA256` manifest v2 (2026-09-15
   section, appended below the v1 lines) carries the CURRENT raw-byte sha256
   of every bundle artifact, regenerated after the final pre-seal edit of each.
   An in-file stamp is display provenance (kit §2d); the manifest is the
   verification target. Self-referential stamping is retracted.
7. **Sham comparison spec satisfied.** SHAM_FLEET_SPEC_20260915.md conditions
   hold: normalization, ≥5 bar under matched compute, frozen comparators, twin
   law, pilots reported.

## SEQUENCE (ordered gates, retained per her camp state)

HOLD 2 desk re-audit adopts the repair rows → I2/I3 authored → HOLD 3
rehearsal (16 episodes: the six families × qa samples + desk sub-forms; no
confirmatory episodes) → twin authoring (HOLD 2b) → qa_receipts sign →
HOLD 4 seal gate (this file) → approach Astra with the sealed bundle.

## OPEN (tri-stated)

- OPEN: fleet comparator lists per family (desk freezes at HOLD 3 assembly).
- UNPROVEN: reserve feasibility for the D-arm 210s→180s amended cap under real
  episodes (her "measure whether that reserve suffices before sealing" — the
  qa runs are the measurement).
- OPEN: I2/I3 authoring (the two unauthored families).
