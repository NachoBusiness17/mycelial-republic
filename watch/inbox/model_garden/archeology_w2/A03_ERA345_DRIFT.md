# A-03: ERA345_DRIFT (archeology.wave2 lane receipt + deliverable)

Schema: archeology.wave2.receipt.v1 · lane A-03 · night lane 2026-10-02 ~04:4xZ
Cost: $0 (local bytes only). Deliverable per memory/plans/ARCHEOLOGY_20.md
row A-03: MEMORY.md phantom+live rows vs watch/inbox receipts; concepts
claimed vs concepts byte-backed.

## Instrument

memory/MEMORY.md (491 lines, regenerated 2026-09-07 07:29:30Z by seat refix;
476 entry rows = 35 LIVE + 441 PHANTOM). Resolution method tonight: one-pass
filename index over memory/ + docs/ + watch/ + state/ + research/
(205,551 filenames), plus literal-path first. This mirrors the refix seat's
own resolve_ref contract (literal root -> literal under memory/ -> basename
walk).

## Drift map (claim vs bytes, measured 2026-10-02 ~04:40Z)

| claim surface | rows | byte-backed tonight | drift |
|---|---|---|---|
| LIVE INDEX | 35 | 35/35 resolve (0 dead) | NONE. The refix's live set has not rotted in 25 days. |
| PHANTOM LEDGER | 441 | 0/441 targets now exist | TOTAL NON-PROMOTION. Not one phantom room got built since 09-07. The ledger is a frozen graveyard of the 09-06/09-07 salon era's intentions (what-now salon ladder, Republic of Letters rooms, THE MARGIN moonshot, Fermat ractor, wakers curriculum, Rocinante substrate salon...). |
| era 4-5 coverage | - | 0 rows | MEMORY.md's newest concept rows are 09-06 (date-mention census: 09-05 x121, 09-04 x112, 09-06 x71, 09-03 x63, 09-02 x31, one 09-07 regen stamp, one 09-20 edit). Hydrology/water-computer, kache, model garden, descent protocol, Mickey17, ractor engine have NO index rows; only 14 incidental term mentions. The estate's live concept surface moved to AGENTS.md + state/CURRENT.md + watch/inbox receipts; MEMORY.md is a frozen era-3 snapshot that does not say FROZEN. |

## Concept-level read (era 3 -> 5)

Era 3 concepts claimed in MEMORY.md live rows are byte-backed and stable
(chord executable -> mag/chord.py exists; telepathy invariant codes, MAX_DISTILL,
memweave state, hallucination gauntlet receipt watch/HALLUCINATION_GAUNTLET_20260906.md
all resolve). Era 4-5 concepts are byte-backed in watch/inbox but UNINDEXED in
MEMORY.md: the drift is not rot, it is ABANDONMENT of the index surface. A
phantom-adjacent receipt does exist for at least one phantom concept
(watch/inbox/the_margin/), i.e. some phantom rooms' WORK landed as receipts
while the room .md itself was never created: claim-vs-bytes must distinguish
"room never built" (true for all 441) from "work never done" (false for at
least the margin family).

## Falsifiers / tickets for the next seat

1. MEMORY.md should either get a FROZEN banner (era-3 snapshot, see
   memory/briefs/latest.md precedent) or a regen pass that indexes era 4-5
   receipts. Cheap, one sitting, but touches a shared memory surface: stage as
   a ticket, do not edit tonight.
2. The 441-row phantom ledger is 09-06/09-07-dated: cross-dating with A-01's
   Mar-2 window shows the estate's pattern - vocabulary mints in bursts, rooms
   mostly never get built, receipts carry the load. Any archaeology claim of
   "we built X" must cite a receipt, never an index row.

Filed by night lane, 2026-10-02Z. $0. No em-dash bytes.
