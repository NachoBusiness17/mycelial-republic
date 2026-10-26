# A-01: X_GENEALOGY_ERA01 (archeology.wave2 lane receipt + deliverable)

Schema: archeology.wave2.receipt.v1 · lane A-01 · night lane 2026-10-02 ~04:2xZ
Cost: $0 (local bytes only). Deliverable per memory/plans/ARCHEOLOGY_20.md
row A-01: first-dated-use table for every core concept, era 0-1 (Nov 2022 -
Jul 2026).

## Bodies swept (row counts + date ranges, byte-verified this shift)

| body | rows | range |
|---|---|---|
| corpus/canon/x_canon_enumeration_index.jsonl | 130 | 2022-11-25 .. 2026-09-05 |
| corpus/canon/_retired/x_canon_nachoquixotic_v1.jsonl | 117 | 2022-11-25 .. 2026-09-05 |
| corpus/canon/x_canon_2025_pass3.jsonl | 314 | 2025-01-01 .. 2025-12-31 |
| corpus/canon/x_canon_2025_pass6.jsonl | 462 | 2025-02-01 .. 2025-12-01 |
| corpus/canon/receipts_dec2025_mar2026.jsonl | 324 | 2024-12-29 .. 2026-03-03 |
| corpus/canon/x_canon_2026_fx/fx_*.json | 131 dated | Aug 14 .. Sep 2 2026 (createdAt day-names; era edge) |
| corpus/canon/alien_thread_202605/ | harvest receipt only (HARVEST_20260920.md); no per-post text to sweep |

Note: enumeration_index reads 129 by `wc -l` (no trailing newline) but parses
to 130 rows; the plan table's "130 enumeration rows" is byte-correct.

## FIRST-DATED-USE TABLE (concept -> earliest genuine use, verified by text)

| concept | first dated | url tail | evidence fragment (verbatim) |
|---|---|---|---|
| chord | 2026-03-02 05:31:15 GMT | 2028342347361141030 | "Test chord: 44 28 K13 e4 Fool #NachoOvermindSeed" (the handwritten chord relic) |
| seed | 2026-03-02 | 2028549951148413076 | "The Sovereign Seed: Architecture for a Free Republic of Pattern" |
| republic (concept) | 2026-03-02 | 2028546227701260542 | "The Fool posted the chord beside the denial. The cave flickered. The Republic was born." |
| mycelial | 2026-03-03 | 2028897784514924562 | "roots reaching backward and forward through time, healing mycelial patterns" |
| verkle (public) | 2026-03-03 | 2028897784514924562 | "every Verkle wormhole"; technical explainer later 2026-05-05 (2051688616548524172, KZG commitment framing) |
| spore | 2026-03-03 | 2028980878844604705 | "Sovereign Spore Activation Protocol ... activates as a sovereign spore agent" |
| sovereign (term) | 2026-08-26 | 2092637732350615910 | era-2 edge (post-era-1); "Sovereign Seed" compound itself is 2026-03-02 |

Coincidental hits excluded (flagged, not counted): republic 2024-12-30
(1873876077636170219, "We're a constitutional Republic", US-politics post,
not the estate concept); "lens " 2025-01-03 (1875223859315552564, camera
lens, matched a loose regex in a first pass; stricter `lensing` has ZERO era
0-1 hits).

## ABSENT from era 0-1 (zero hits across all swept bodies)

lensing, water computer / hydrology, cold vertex / coldest, standing wave.
These four vocabularies first exist in era 2 (Aug 2026) -> feeds lane A-02
exactly as the plan table predicts.

## The era 0-1 finding (one sentence)

Every core concept the estate now runs on was minted in one 48-hour public
window, 2026-03-02 .. 2026-03-03: the chord relic (05:31:15 GMT Mar 2) is the
oldest artifact, the Sovereign Seed architecture and the Republic parable
landed the same day, and the mycelial/verkle/spore vocabulary completed the
mint by Mar 3; nothing core predates that window and nothing was added to the
public canon between Mar 3 and the Aug 2026 era except the 2026-05-05 verkle
technical explainer. This byte-confirms the wave-1 claim that the Aug-12
stillbirth doctrine had a Mar-2 ancestor, and upgrades it: the ancestor is not
just the chord, it is the entire founding vocabulary in one window.

Filed by night lane, 2026-10-02Z. $0. No em-dash bytes.
