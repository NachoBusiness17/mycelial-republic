# DESK VERDICT — HOLD 1 (2026-09-11)

*The pair test: two subagents, same frozen contract (INSTANCE_SEED_001's linkage
audit, packet-only inputs), independent, blind.*

## RESULT: CONVERGED ON SOUND — **CLIMB**

| Check | Worker A | Worker B | Agree |
|---|---|---|---|
| rows_checked | 7,379 | 7,379 | ✓ (same sha256 47c97c27…) |
| resolved | 7,367 | 7,367 | ✓ |
| missing | 12 | 12 | ✓ |
| verdict | DISPUTED | DISPUTED | ✓ |
| anomaly (dict-repr row 2513) | caught | caught | ✓ |
| rubric score | 11/11 | 11/11 | ✓ |

Divergence (documented, not scored): ambiguous_filenames — A counted 3,773
(live-vs-2026-08-25-backup duplication), B counted 0. Procedural reading of one
unscored field. TEMPLATE AMENDMENT for HOLD 2: define ambiguity scope in one line
(does P4 duplication count?).

## TWO BONUS FINDINGS

1. Both workers measured **7,379 rows** — the seed froze at 7,377. The +2 are
   post-repair appends: the chain's flow is confirmed by two independent audits.
   The desk key re-derives at review time, exactly as designed.
2. Worker B's anomaly: 6 filenames resolve only to 0-byte NTFS ADS ghosts, and
   row 72's artifact exists only in the 09-02/04/05 backup snapshots — both
   flagged for the recovery fold's queue, census unchanged per scope lock.

## GATE

HOLD 1: **PASSED.** The ladder climbs. HOLD 2 (author the six irreducible + six
sham instances from the deck) is file-work authoring — launches gated on the
coldest vertex read per the hold ladder.
