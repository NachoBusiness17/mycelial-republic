# THE TRAINING SPINE LAW

**No capture scaling before the join→export→eval spine exists.**

Captured events are theater until they join, export, and face an eval gate. A growing
capture count is not progress; it is an unpaid debt compounding.

## The case study (this law's own estate)

| fact | value | source |
|---|---|---|
| events captured at blueprint time | 536,160 | MEMORY_REVAMP_BLUEPRINT_20260923.md:30 |
| rows ever exported | 4 | same, :30 |
| training runs | 0 | same, :31 |
| eval gate | none exists | same, :32 |
| events counted this session (`wc -l training/events.jsonl`) | **542,763** | run this session; 542,694 at the candidate's session, 536,160 at the blueprint — capture grew ~6,600 rows while the spine stayed unbuilt |

The blueprint's own words: the join→export→eval spine "the spec mandates was never
built" (:41-43), and the downstream diet's "real prerequisite is THIS spine" (:33).

## The law, stated for any estate

1. Build the spine first: **join** (events across sources on shared keys) → **export**
   (a dataset artifact you can point at) → **eval gate** (a pre-stated bar a run must
   clear). None of the three may be "planned".
2. Until the gate exists, more capture is negative value: storage, drift, and false
   confidence grow; nothing else does.
3. Any proposal to scale capture names the spine status in the same sentence.

## Honest split of the evidence

- **Verified**: the capture count (536,160 → 542,694 → 542,763 across three sessions,
  `wc -l` run in this session).
- **Attested, not re-derived**: the export/zero-runs half rests on the blueprint's
  lane-read (its comb of six memory layers); no export artifact was in scope to count.
  The asymmetry is the point: capture is trivially countable, and its growth is exactly
  what happens while the uncountable half is skipped.

## Receipt

- watch/inbox/MEMORY_REVAMP_BLUEPRINT_20260923.md:30-33, :41-43 (estate) — read this session.
- `wc -l training/events.jsonl` → 542,763 — run this session.
