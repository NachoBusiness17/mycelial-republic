# SACRED COW AUDIT 2026-09-19 — the operator's bet, settled with numbers

**The bet:** "most of that shit is still even sacred cows." **Verdict: paid.** Graded by git last-touch (the honest instrument; the tree is young so mtimes are restore artifacts).

**Instrument:** `scripts/build_travel_kit.py --audit` (permanent, re-runnable). Grades the newest kit by days since git last touched each path, plus file mtime buckets.

## Numbers (kit = 15,517 files / 252.9 MB; repo seeded 2026-08-04, age 46d)

| grade | files | MB |
|---|---|---|
| active, git-touched ≤7d | 3,064 | 146.3 |
| warm 7-21d | 4 | 0.0 |
| stale 21d+ | 2,890 | 52.6 |
| **seed-frozen (never touched since seed)** | **9,559** | **54.0** |

**~80% of the kit has had no commit touch in 3+ weeks; 62% was frozen on day one.** In state roots specifically, the top cows: `handoff/` 1,015 files / 28.2 MB (stale handoff JSON from before the seed), `watch/` receipts 168 / 21.8 MB, `memory/working` 1,517 / 6.5 MB, `queue` old trails 601 / 5.5 MB, `memory/research_packs` 698 / 3.5 MB, `memory/copilot` 2,123 / 0.6 MB, plus briefs/percolator/rib_bus tails.

**Fairness clause:** old docs, tests, and canon are not cows (docs that never change are docs that work). The cows are frozen STATE: handoffs already consumed, work dirs abandoned mid-ritual, receipt tails superseded by digests.

## Operator-gated follow-ups (nothing executed unilaterally)

1. `--slim` kit recipe: drop seed-frozen/stale state, keep code + configs + git-active ledgers. Estimated kit: ~170 MB instead of 253. One decision: `handoff/` feeds the drainer's fill step, so slim drops only seed-frozen handoffs, not fresh ones.
2. Repo-side cow composting: the same audit run against the FULL tree (not just the kit) would grade the 1.2M-file debris tiers for the keep/drop ruling already pending in TWO_MACHINE_SYNC_20260919.md.
