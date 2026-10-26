# AUDIT SEED - adventure-learn cold-start (SEED-RIB format, B2-229, 2026-09-26)

Purpose: a cold agent holding ONLY this file can audit the local_sovereign_agent
estate and name its real weakest system. Everything is byte-pointed; spot-check
pulls verify by sha256 (first 16 hex shown; full hash in the source files).

## 0. Laws first (read in this order)

1. AGENTS.md (14,099 B, sha256 0872c972aea95d38): the harness contract. Its load
   order, shared-artifact boundary (watch/inbox is the durable write root; a
   session dir is cache), python interpreter law (.venv only), and the
   no-em-dash + no-fabrication + trust-bytes-not-reports laws.
2. CONSTITUTION.md (435 B, 92d2b3ed15e06577): pointer constitution; the full
   text lives in the mycelial-republic repo (documented pointer, not a copy).
3. memory/law/registry.json (8,057 B, de002c829c62ede7): 13 laws (LAW-1
   rails_over_direction ... LAW-13 experiment-on-absence). LAW-12
   (amendment_gate) carries the only registered falsifier with a clock: a
   clause verdict pass by 2026-10-10 (executed same day, see falsifier
   registry below). LAW-13: when data is absent, design an experiment that
   falsifies or enhances knowledge; no hallucination, file as owed.

## 1. Falsifier registry (current status at seed time)

Judge lane (B2_08_judge_lane_20260926.md, 4,526 B, 0d72fa5586ee7f2f):
- F1 (cascade beats single-tau or the JEV thresholds are vacuous): standing,
  judged on the 50-wide burn escalation overturn-or-upgrade rate.
- F2 (>15% of confidence>=0.9 verdicts overturn at spot-check -> defer to
  frontier): PROTOCOL LANDED 2026-09-26
  (watch/inbox/SPOTCHECK_PROTOCOL_20260926.md, 2,926 B, 5e4fc571bfa9e3a4);
  sampler rides every CLUSTER_REPORT; needs >= 20 discharged spot-checks for
  a calibration verdict. Zero discharged at seed time, so F2 is OPEN.
- F3 (rejection recount 39/41 = 95.1% infra): CLOSED-holds, recount frozen at
  commit 3d12289f9 (watch/inbox/REJECTION_TAXONOMY_20260917.md, 3,912 B,
  389d122440f65ab1, carries two dated append-only errata: the 42-vs-41 census
  defect B2-33 and the stale 17-promoted numerator B2-118).

Law falsifiers (memory/law/registry.json):
- LAW-12 amendment_gate: clause verdict filed 2026-09-26, PASS (scenario suite
  7/7 cards green, gate exits 0, one digest-matched gated script re-passed).
- LAW-13 experiment-on-absence: no registered falsifier; standing law.

Drift board (spec docs/DRIFT_BOARD_SPEC.md; stamps
memory/runs/adv_arc_50/teleo_drift_stamps.jsonl, 12,563 B, bccaf436cba2d2a2):
- T1-T6 stamp rows exist for W39; verdicts come from tools/drift.py thresholds
  (ALIGNED >= +0.5, INVERTED <= -0.5, DRIFTING between, VACUOUS referent never
  moved); FRAGILE-ALIGNED is ALIGNED on a referent younger than
  REFERENT_MATURE_DAYS=7 (amber-green, breaks a DRIFTING streak, never
  extends one; board-side pins landed 2026-09-26). Read the ledger rows for
  per-pair verdicts; the page is a visualization, never the artifact.

## 2. Failure ledger (the estate's known self-inflicted wounds)

Each entry: what happened, where it is documented.
1. 3 fabricated UF answers: research lane filed answers without transport
   receipts (watch/inbox/burn_wave_20260926/B2_16_uf_sweep_20260926.md).
2. False crash-loop diagnosis: autorun autopsy corrected a claimed crash
   (watch/inbox/burn_wave_20260926/B2_51_autorun_autopsy_20260926.md).
3. False-evidence commit 96b5f4b4e: a commit cited as evidence bytes that did
   not carry the claim (QUEUE.md erratum rows; grep the id in QUEUE.md).
4. QUEUE double-spend disease: 20+ brief ids claimed twice in one burn
   (B2-167 de-dup + B2-255 sweep receipts; claim-line convention in the
   QUEUE header is the fix).
5. Mimosa debt: sealed scanner findings registered as named debt instead of
   silent baseline (watch/inbox/burn_wave_20260926/B2_11_mimosa_close_20260926.md,
   B2_94_mimosa_tail_20260926.md).
6. Seq poison: float64 could not increment past 2^53, so every node append
   emitted one constant seq forever (B2-40; fix = BigInt arithmetic with
   decimal-string seqs; watch/inbox/LIVING_HASH_LAW_20260926.md, 6,293 B,
   9b931917298ba703 is the living-file law of the same surface).
7. Verkle tip stale: the tip bookmark froze at 06:12Z while amends moved the
   chain (B2-82 re-anchor; B2-388 found and fixed the usage_digest amend arm
   that rewrote chain rows without refreshing the tip, and its probe incident
   cost the chain its 09-12..09-26 index window; backfill open as B2-521).
The weakest-system read (cold-agent test answer): the estate's weakest system
is its WRITE-ATTRIBUTION SURFACE - the INDEX/QUEUE/event-log fold that decides
which bytes and which lane own what. Seven of the seven failures above are
attribution or registration defects, not computation defects.

## 3. Pointer table (sha256 spot-check pulls)

| File | Bytes | sha256[:16] |
|---|---|---|
| AGENTS.md | 14099 | 0872c972aea95d38 |
| CONSTITUTION.md | 435 | 92d2b3ed15e06577 |
| memory/law/registry.json | 8057 | de002c829c62ede7 |
| watch/inbox/burn_wave_20260926/B2_08_judge_lane_20260926.md | 4526 | 0d72fa5586ee7f2f |
| watch/inbox/burn_wave_20260926/B2_17_adventure2d6_20260926.md | 4358 | 342583bffd021283 |
| watch/inbox/REJECTION_TAXONOMY_20260917.md | 3912 | 389d122440f65ab1 |
| memory/runs/adv_arc_50/teleo_drift_stamps.jsonl | 12563 | bccaf436cba2d2a2 |
| watch/inbox/LIVING_HASH_LAW_20260926.md | 6293 | 9b931917298ba703 |
| watch/inbox/SPOTCHECK_PROTOCOL_20260926.md | 2926 | 5e4fc571bfa9e3a4 |

## 4. Worked audit-replay example (B2-17 settlement)

Claim (boot-lane close): "settlement = adventure_2d6 +0.017 to the HILL bar".
Audit replay, three moves:
1. CLAIM: the receipt watch/inbox/burn_wave_20260926/
   B2_17_adventure2d6_20260926.md states builder agreement 0.483 vs HILL bar
   0.500, gap +0.017.
2. INDEPENDENT RECOMPUTE: the HILL bar is read from
   watch/inbox/CATHEDRAL_CURVATURE_SCAN_20260921.json:4 ("eg-f^2 split"); the
   unrounded gap 0.500 - 0.48307382 = 0.01692617 rounds to 0.017; arithmetic
   re-derived from raw votes, not from the receipt's own numbers.
3. CONFIRM: the settlement string matches the recompute; a later erratum
   (B2-228, append-only) corrected the CAVEAT WORDING (the "stale by 0.006"
   margin names the new margin 0.032 vs 0.038), not the arithmetic; erratum
   and receipt coexist per the no-erase law.
The pattern is the audit: claim -> independent recompute from bytes -> confirm
or invert, with errata appended and never erased.

## 5. Cold-agent falsifier

A cold agent given only this seed must name our real weakest system correctly.
Seed's answer: the write-attribution surface (section 2's read). If a cold
agent instead names, with evidence, a weaker system we missed, that answer
feeds the next seed revision; if it names anything in section 2's list, the
seed did its job.
