# CYCLE BRIEF NEXT - v1 landing receipt (2026-09-30)

Owner: ZCode seat (mission: "the flywheel's morning composer goes v1 - it
becomes the STEERING surface"). Tool: `tools/cycle_brief.py` (343 lines).
Live artifact: `watch/inbox/CYCLE_BRIEF_20260930.md` (14,203 bytes, verdict
RED, 3 climb pitches, 115 lines, regenerated at run time). Em-dash count in
this file: 0.

## The six mission items, all landed

1. ANIMAL PROFILES - `tools/animal_profiles.py --distill` embedded at dawn:
   7 animals, observation kinds + newest ts + source counts; the stale-row
   law rides below it.
2. DOCTRINE SCORECARD - `tools/doctrine_arbiter scorecard` embedded; EXPIRED
   items matched by item-row shape (two-space indent + status column, NOT
   substring - the SUMMARY line also says EXPIRED) and named for retirement
   (operator gate, never auto-removed). Empty ledger renders an HONEST-GAP
   plus a seeding mission; ledger-empty vs EXPIRED select different missions.
3. QUOTA + RECOMMENDATION - the HOLD/GO head plus a derived "today's shape:
   X-wide staggered" line parsed from the instrument's own hold-line bytes
   (stagger 6-8 / clean 8-12 / RED-at-19 laws), mapped by day verdict:
   RED = 6-8 staggered floor, AMBER = recover toward clean range, GREEN =
   proven clean width. STAGGERED, never at-once is unconditional.
4. CLIMB QUEUE - next 3 pitches parsed from THE_LENSING section 4 PRIORITY
   ORDERING (the post-lensing reorder, the newest execution order); each row
   carries a receipt-probed status + the lens's own gate text verbatim-order.
5. MISSIONS (SEEDS v1) - pre-written paste-ready prompts per lane: 3 climb
   missions (P6 STRANGER-PREP, P3 BUILD-RAIL-REDUCED, P2 TRANSPORT-
   INTEGRITY), a doctrine mission (seed-on-empty / retire-on-EXPIRED), and
   MISSION ANIMAL-OBSERVE (walls-to-observations with sources). Every
   mission names sources, falsifier, receipt path.
6. Ran live on today's bytes - see the artifact above.

## Defects found and fixed while landing (receipts)

- v0 quota bug: the brief shelled `tools/quota_ledger_report.py`, a library
  module with no `__main__`, so EVERY v0 brief printed "[quota report empty -
  HONEST-GAP]" while the real CLI lived in `tools/quota_ledger.py`. Cause
  named in the fix comment; the section now parses the real report.
- ATTENTION exits: quota (RED), anomaly (rows), doctrine (EXPIRED) exit
  non-zero WITH the full report on stdout; `_run` previously kept only the
  last 300 chars. Now keeps all stdout, marker-first, and `_strip_markers`
  drops the marker from display.
- doctrine_arbiter split mid-flight (sibling lane landed
  `tools/doctrine_arbiter_core.py` during this session): script-form calls
  died with ModuleNotFoundError. All subprocess calls now use `python -m
  tools.<name>` (module form survives file splits). This is now the standing
  invocation law for brief-integrated tools.
- gate_digest.py currently crash-writes (OSError 22 on GATE_DIGEST.md); the
  brief falls back to the standing GATE_DIGEST.md artifact and says so.

## Live read of 2026-09-30 (the steering state)

- Day verdict RED, live AMBER: 349 fires, 7 wall moments (26 lanes dead
  1302/1308), peak width 26. Recommendation: 6-8-wide staggered.
- Doctrine: 2 VINDICATED (rib-driving-ladder-duel 0.611 >= 0.55;
  spec-parity-standing parity True), 1 PENDING (spec-anomaly-clean, measured
  98 vs <= 0, deadline 2026-10-07 - the likely first EXPIRED/retire candidate
  unless the 98 anomaly rows shrink to 0).
- Climb queue: P6 BLOCKED ON OPERATOR DOOR (Adam's GitHub username); P3 and
  P2 landed-but-open per the lens's demands.
- Oldest operator gate: the Adam invite (0d 11h at digest generation).

## Next (owed, by owner's next seat)

- CLIMB_RECEIPTS probes are pinned to last_mile_20260930 paths; when the
  route advances past P6/P3/P2 the probe map needs its next receipts (the
  parse degrades to HONEST-GAP, never fabrication).
- C3 (stealth triage auto) and C5 (drop-ledger per-item coupling) from
  SNOWBALL_PLAN remain the un-landed couplings for v2.
- gate_digest write bug is its owner's defect, named above for the gate
  digest seat.
