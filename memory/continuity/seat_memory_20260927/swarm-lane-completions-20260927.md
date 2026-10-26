---
name: swarm-lane-completions-20260927
description: 9/27 flash-lane burn swarm completions FINAL — all 12 lanes + 12 swarm + deep lanes done, 506 dispensed / 402 landed, ~1.4B witnessed tokens, honest spectrum incl DECLINED, width-24 proven dynamic, QUEUE restore war pattern codified
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Swarm lane completions 9/27 FINAL — the flash-lane burn completed its entire queue. All 12 original swarm lanes plus the 12-lane wave finished. 506 briefs dispensed total, 402 landed with receipts, plus 200+ self-fed briefs created and executed by the lanes themselves. ~1.4B witnessed tokens across all agents.

## Final tally

- **SW-00**: 25/25 at 95.1M tokens. 23 landed, 2 owed on byte-proven blockers.
- **SW-01**: 25/25 at 81.9M tokens. Includes one fully disclosed self-inflicted incident with estate restoration.
- **SW-02**: 25/25 at 116M tokens (heaviest single lane). 19 LANDED, B2-312 REJECTED-by-falsifier, B2-125 BLOCKED-as-owed, B2-344 disposition+fired falsifier, B2-266 no-erratum (premise stale), B2-194 staged-pending-operator.
- **SW-03**: 25/25 at 69M tokens. 23 LANDED with receipts, 2 OWED-DORMANT condition-unmet.
- **SW-05**: 25/25 at 80.1M tokens. Full spectrum: 19 LANDED, 2 PARTIAL/OWED, 1 BLOCKED-AT-SOURCE, 1 PROVEN (junction BYTE_DUPLICATE_MOUNT), 1 UNDECIDABLE-OWED, 1 DECLINED (refused to file a brief whose claim didn't reproduce). Committed 6d417abd5 (18 landed critical files).
- **SW-07**: 25/25 at 70M tokens. QUEUE truncation incident caught and rebuilt from git bytes. Arm C 200-leg killed at 66min/1-of-30, filed OWED with frozen bars.
- **SW-08**: 24/24 at 93.6M tokens. Falsifiers fired live on 7 briefs, standing constant-1-error test disease fixed, QUEUE restore war caught/deduped/gated.
- **SW-10**: 24/24 at 86.2M tokens. Honest partials under 1302 throttling named as owed.
- **SW-11**: 24/24 at 76M tokens. Board truncated and restored.
- **SW-04/06/09**: died to 1302 cluster, briefs requeued and re-dispatched.

**Total witnessed across all agents: ~1.4B tokens.**

## Honest verdict spectrum

Lanes filed the full range: LANDED, PARTIAL/OWED, BLOCKED-AT-SOURCE, PROVEN, UNDECIDABLE-OWED, DECLINED, REJECTED-by-falsifier, NOT-CLEAN, OWED-DORMANT. The fleet's verdict vocabulary is rich enough to say no.

## QUEUE.md restore war pattern

Five lanes independently caught QUEUE.md truncation or stale-restore incidents (SW-02, SW-05, SW-07, SW-08, SW-10). Each rebuilt from git+lanelog bytes. The pattern is structural: concurrent self-feed appends + whole-file restores = the hot board cannot survive multi-lane concurrent writes without a claim-and-rebase protocol. The B2-250 claim law + B2-343 restore guard codify the fix.

## Recurring patterns

- Board-restore incidents: QUEUE.md truncated or restored by concurrent writers in SW-02, SW-05, SW-07, SW-08, SW-10. Each caught and rebuilt from git+lanelog bytes.
- Fabricated placeholder hashes caught by lanes' own falsifiers (B2-342 caught its own draft hash, B2-106 caught its own unverified number, B2-179 caught an unverified byte count).
- Self-feed numbering collisions live at every scale: three dedupe passes + claim law + checkbox law still didn't stop new collisions. The claim convention is structural, not a bug.
- The DECLINED verdict is the honesty apex: SW-05 refused to file a brief whose claim didn't reproduce under probe, spending the lane's time on the proof instead of the paper.

## Deep-lane thesis proven

Unbounded lanes produce results bounded briefs cannot: B2-476 hill rebuild (all-six HILL at 0.932/0.935 vs section-best 0.914), B2-472 chain census on production bytes (zero real chains), B2-357 scout pin (backward-compatible at 52 real). Queue composition should weight deep lanes when the work matters.
