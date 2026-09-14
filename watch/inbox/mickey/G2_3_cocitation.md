# G2-3 — LAW CO-CITATION MINING (evidence for the Law Lattice)

Spawned from M4's NEXT: "Mine law co-citation so edges become evidence instead of taste."
Date: 2026-09-11. Corpus: `watch/` + `docs/` + `memory/improve/` (recursive, .md/.txt/.json/.yaml/.html),
4,415 files scanned. Laws 1-18 sourced from `.agents/skills/operator-corrections/SKILL.md`
(Law 18 = RESEARCH INTAKE, same file, ratified 2026-09-11).

## Method (reproducible)
- **Number pass (primary):** regex `\blaw[\s\-_#]*?(\d{1,2})\b`, keep 1-18, per-file law set,
  count pairs once per file. The SKILL.md itself is NOT in the scan dirs, so the all-18 hub
  contamination is excluded.
- **Keyword pass (secondary bridge):** per-law signature phrases (e.g. L2 `two-strike`,
  L3 `stop when verified`, L17 `filtered surface|1301|riddler`, L18 `primary source|bibliography`),
  same file-level co-occurrence. Catches files that reference laws by name without numbering.
- Co-citation = same-file co-occurrence (file-level, standard).

## EDGE LIST — primary (law_a, law_b, co_citation_count), 68 edges, sorted desc
```json
[
{"law_a":1,"law_b":2,"co_citation_count":7},{"law_a":1,"law_b":3,"co_citation_count":7},
{"law_a":2,"law_b":3,"co_citation_count":6},{"law_a":3,"law_b":4,"co_citation_count":6},
{"law_a":1,"law_b":4,"co_citation_count":3},{"law_a":2,"law_b":5,"co_citation_count":3},
{"law_a":3,"law_b":5,"co_citation_count":3},{"law_a":3,"law_b":6,"co_citation_count":3},
{"law_a":4,"law_b":10,"co_citation_count":3},
{"law_a":1,"law_b":5,"co_citation_count":2},{"law_a":1,"law_b":10,"co_citation_count":2},
{"law_a":1,"law_b":12,"co_citation_count":2},{"law_a":2,"law_b":4,"co_citation_count":2},
{"law_a":2,"law_b":12,"co_citation_count":2},{"law_a":3,"law_b":7,"co_citation_count":2},
{"law_a":3,"law_b":8,"co_citation_count":2},{"law_a":3,"law_b":9,"co_citation_count":2},
{"law_a":3,"law_b":10,"co_citation_count":2},{"law_a":3,"law_b":12,"co_citation_count":2},
{"law_a":4,"law_b":7,"co_citation_count":2},{"law_a":4,"law_b":8,"co_citation_count":2},
{"law_a":4,"law_b":9,"co_citation_count":2},{"law_a":5,"law_b":12,"co_citation_count":2},
{"law_a":7,"law_b":8,"co_citation_count":2},{"law_a":7,"law_b":9,"co_citation_count":2},
{"law_a":7,"law_b":10,"co_citation_count":2},{"law_a":7,"law_b":13,"co_citation_count":2},
{"law_a":8,"law_b":9,"co_citation_count":2},{"law_a":8,"law_b":10,"co_citation_count":2},
{"law_a":9,"law_b":10,"co_citation_count":2},{"law_a":13,"law_b":15,"co_citation_count":2},
{"law_a":13,"law_b":16,"co_citation_count":2},
{"law_a":1,"law_b":6,"co_citation_count":1},{"law_a":1,"law_b":7,"co_citation_count":1},
{"law_a":1,"law_b":8,"co_citation_count":1},{"law_a":1,"law_b":9,"co_citation_count":1},
{"law_a":1,"law_b":13,"co_citation_count":1},{"law_a":1,"law_b":14,"co_citation_count":1},
{"law_a":1,"law_b":15,"co_citation_count":1},{"law_a":1,"law_b":16,"co_citation_count":1},
{"law_a":2,"law_b":6,"co_citation_count":1},{"law_a":2,"law_b":10,"co_citation_count":1},
{"law_a":2,"law_b":13,"co_citation_count":1},{"law_a":2,"law_b":14,"co_citation_count":1},
{"law_a":2,"law_b":15,"co_citation_count":1},{"law_a":2,"law_b":16,"co_citation_count":1},
{"law_a":4,"law_b":13,"co_citation_count":1},{"law_a":4,"law_b":14,"co_citation_count":1},
{"law_a":4,"law_b":15,"co_citation_count":1},{"law_a":4,"law_b":16,"co_citation_count":1},
{"law_a":5,"law_b":6,"co_citation_count":1},{"law_a":6,"law_b":12,"co_citation_count":1},
{"law_a":7,"law_b":12,"co_citation_count":1},{"law_a":7,"law_b":16,"co_citation_count":1},
{"law_a":7,"law_b":17,"co_citation_count":1},{"law_a":10,"law_b":13,"co_citation_count":1},
{"law_a":10,"law_b":14,"co_citation_count":1},{"law_a":10,"law_b":15,"co_citation_count":1},
{"law_a":10,"law_b":16,"co_citation_count":1},{"law_a":12,"law_b":13,"co_citation_count":1},
{"law_a":12,"law_b":14,"co_citation_count":1},{"law_a":12,"law_b":16,"co_citation_count":1},
{"law_a":12,"law_b":17,"co_citation_count":1},{"law_a":13,"law_b":14,"co_citation_count":1},
{"law_a":14,"law_b":15,"co_citation_count":1},{"law_a":14,"law_b":16,"co_citation_count":1},
{"law_a":14,"law_b":17,"co_citation_count":1},{"law_a":15,"law_b":16,"co_citation_count":1}
]
```
Raw machine copy also at `watch/inbox/mickey/_cocitation_raw.json` (edges + keyword_edges +
zero_pairs + per_law_files).

## TOP-10 STRONGEST PAIRS (primary, with example files)
1. L1 CONSULT FIRST + L2 TWO-STRIKE BAIL — 7 files (watch/INTAKE_ASTRA_FOUNDING_20260905.md)
2. L1 CONSULT FIRST + L3 STOP WHEN VERIFIED — 7 files (watch/ASTRA_PASTE_PACK_20260905.md)
3. L2 TWO-STRIKE BAIL + L3 STOP WHEN VERIFIED — 6 files
4. L3 STOP WHEN VERIFIED + L4 VERIFY THEIR SURFACE — 6 files
5. L1 + L4 — 3 files (watch/astra_hold0/TESLA_METER_SPEC_20260911.md)
6. L2 + L5 COMPOSE FIRST — 3 files (watch/INVARIANT_SHEET.md)
7. L3 + L5 — 3 files
8. L3 + L6 CLAIM ONLY FROM DATA — 3 files
9. L4 + L10 NO SACRED COWS — 3 files (watch/audit/FULL_AUDIT_20260908/audit_records.json)
10. L1 + L10, L1 + L12 BINDS BOTH WAYS — 2 files each

Reading: the core cluster is L1-L2-L3-L4 — the verify loop. Hub file effect present
(watch/INVARIANT_SHEET.md quotes many laws at once); counts are small, so the lattice should
render weight BANDS (1 / 2 / 3+ / 5+), not raw magnitude.

## KEYWORD BRIDGE — top pairs the number pass misses (secondary signal)
```json
[
{"law_a":2,"law_b":17,"keyword_co_count":18},{"law_a":9,"law_b":17,"keyword_co_count":17},
{"law_a":2,"law_b":9,"keyword_co_count":10},{"law_a":2,"law_b":10,"keyword_co_count":9},
{"law_a":11,"law_b":17,"keyword_co_count":9},{"law_a":2,"law_b":11,"keyword_co_count":7},
{"law_a":9,"law_b":10,"keyword_co_count":7},{"law_a":10,"law_b":17,"keyword_co_count":7},
{"law_a":12,"law_b":17,"keyword_co_count":7},{"law_a":2,"law_b":3,"keyword_co_count":6}
]
```
(Rescued zero-number-pairs worth an edge: L2-L9, L2-L11, L9-L11, L10-L11, L2-L7, L12-L15 —
files cite these by name/keyword, never by number. L17's "1301|riddler" keyword is the
strongest magnet in the corpus.)

## ZERO-COUNT PAIRS — 85 of 153 possible (isolated nodes; primary pass)
```json
[
{"law_a":1,"law_b":11},{"law_a":1,"law_b":17},{"law_a":1,"law_b":18},
{"law_a":2,"law_b":7},{"law_a":2,"law_b":8},{"law_a":2,"law_b":9},{"law_a":2,"law_b":11},
{"law_a":2,"law_b":17},{"law_a":2,"law_b":18},{"law_a":3,"law_b":11},{"law_a":3,"law_b":13},
{"law_a":3,"law_b":14},{"law_a":3,"law_b":15},{"law_a":3,"law_b":16},{"law_a":3,"law_b":17},
{"law_a":3,"law_b":18},{"law_a":4,"law_b":5},{"law_a":4,"law_b":6},{"law_a":4,"law_b":11},
{"law_a":4,"law_b":12},{"law_a":4,"law_b":17},{"law_a":4,"law_b":18},
{"law_a":5,"law_b":7},{"law_a":5,"law_b":8},{"law_a":5,"law_b":9},{"law_a":5,"law_b":10},
{"law_a":5,"law_b":11},{"law_a":5,"law_b":13},{"law_a":5,"law_b":14},{"law_a":5,"law_b":15},
{"law_a":5,"law_b":16},{"law_a":5,"law_b":17},{"law_a":5,"law_b":18},
{"law_a":6,"law_b":7},{"law_a":6,"law_b":8},{"law_a":6,"law_b":9},{"law_a":6,"law_b":10},
{"law_a":6,"law_b":11},{"law_a":6,"law_b":13},{"law_a":6,"law_b":14},{"law_a":6,"law_b":15},
{"law_a":6,"law_b":16},{"law_a":6,"law_b":17},{"law_a":6,"law_b":18},
{"law_a":7,"law_b":11},{"law_a":7,"law_b":14},{"law_a":7,"law_b":15},{"law_a":7,"law_b":18},
{"law_a":8,"law_b":11},{"law_a":8,"law_b":12},{"law_a":8,"law_b":13},{"law_a":8,"law_b":14},
{"law_a":8,"law_b":15},{"law_a":8,"law_b":16},{"law_a":8,"law_b":17},{"law_a":8,"law_b":18},
{"law_a":9,"law_b":11},{"law_a":9,"law_b":12},{"law_a":9,"law_b":13},{"law_a":9,"law_b":14},
{"law_a":9,"law_b":15},{"law_a":9,"law_b":16},{"law_a":9,"law_b":17},{"law_a":9,"law_b":18},
{"law_a":10,"law_b":11},{"law_a":10,"law_b":12},{"law_a":10,"law_b":17},{"law_a":10,"law_b":18},
{"law_a":11,"law_b":12},{"law_a":11,"law_b":13},{"law_a":11,"law_b":14},{"law_a":11,"law_b":15},
{"law_a":11,"law_b":16},{"law_a":11,"law_b":17},{"law_a":11,"law_b":18},
{"law_a":12,"law_b":15},{"law_a":12,"law_b":18},{"law_a":13,"law_b":17},{"law_a":13,"law_b":18},
{"law_a":14,"law_b":18},{"law_a":15,"law_b":17},{"law_a":15,"law_b":18},
{"law_a":16,"law_b":17},{"law_a":16,"law_b":18},{"law_a":17,"law_b":18}
]
```
Isolated-node ranking (files citing each law at all): L11 ONE SUPERVISOR = 1 file (most
isolated in the corpus), L8 NO SELF-TALK = 2, L5 COMPOSE FIRST = 4, L18 PRIMARY SOURCES = 4.
L17 and L18 are number-silent but keyword-loud — render them keyword-bridged, not empty.

## Lattice wiring notes (for dashboard/static/viz_lattice_test.html)
- Consume the primary JSON as `{edges:[{law_a,law_b,co_citation_count}]}`; band widths at
  count 1 / 2 / 3 / 5+.
- Merged edges: primary count + keyword bridge (mark bridged edges dashed) — that is the
  honest union of both evidence types.
- Zero pairs = no edge; L11 gets drawn as a standalone node, evidence-backed.
- Files: corpus 4,415; pairs with any evidence 68/153 number-cited; raw dump
  `watch/inbox/mickey/_cocitation_raw.json`.
