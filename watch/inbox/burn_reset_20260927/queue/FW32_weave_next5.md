# FW32_weave_next5: THE WEAVE next-5 build-order memo

**Stone:** FW-32 (FIFTY_WIDE_BOARD_20260917.md §G line 61): "THE_WEAVE next-5: pick 5 of the 48 queued mechanics by ramp law → build-order memo".
**Date filed:** 2026-09-28 · **Lane:** burn_reset Q-026 · **Cost:** $0, no paid APIs, no git commands.
**Sources read this ask:** `watch/inbox/THE_WEAVE_20260916.md` (full 246 lines) · `memory/continuity/seat_memory_20260927/gaming-weave-20260916.md` · `watch/inbox/wave_20260916/receipts/WEAVE_SYNTHESIS.md` · W1A/W2/W3/W4/N8/N10/N12 receipt headers · `dashboard/static/games/mud.html` RNG law block (lines 67-74) · `watch/inbox/WAVE_STATE_20260916.md`.

## 1. Byte state of the queue

- The doc of record is `watch/inbox/THE_WEAVE_20260916.md` §2: **106 rows: 35 SHIPPED / 23 PARTIAL / 48 QUEUED**. Reproduced by status-column grep this ask: `grep -c "| QUEUED |"` = **48**, `| SHIPPED |` = **35**, `| PARTIAL |` = **23** (raw word greps read 50/37/25 because the legend, dedup note, and prose reuse the words; the status-column instrument is the receipt's own instrument, and it reproduces the receipt exactly).
- The 48 QUEUED row ids (grep-extracted this ask): I-8, I-9, I-11, II-23, II-26, II-27, II-28, II-29, II-30, II-31, II-32, II-35, II-36, II-37, II-38, II-39, II-40, II-41, II-42, III-9..III-17, IV-8, IV-9, IV-10, IV-12..IV-15, V-7..V-15, X-1..X-5.
- **Landed since the doc was cut** (status cited from the receipts' own headers): X-1 daily shared seed → W1A `FINAL` · II-27 bones files → W2 `DONE` · II-41 souls messages v0 → W3 `DONE` (frontier carrier) · II-23 ghost personalities → W4 `DONE, both gates green` · III-16 ramp-spine rewire → N8 `COMPLETE`. The weave build-out (dozen-wide) also consumed PARTIAL rows: II-21 boon bugs (N9), II-15 puzzle-vault consumer (N10), II-14 inventory consumer (N12), V-5 LOD/spectator consumer (N11), II-16 StS consumer (W5). So the live QUEUED pool this memo picks from is **43 rows** (48 − 5 landed), of which X-4 and X-5 are ⚑ operator rows (excluded from autonomous picks per the doc's own flag).

## 2. Where the ramp stands (the law that ranks the picks)

Mark's law, verbatim (THE_WEAVE §1): *"start at tabletop perfect, mud, perfect, roguelite, perfect…"* (you do not climb until the current rung's falsifier holds). Rung II (mud-perfect) is where the fleet stands: its falsifier (`mud_play.v1` receipts off a seeded LCG) is **staged, not landed**: `dashboard/static/games/mud.html` lines 67-74 carry the RNG-law comment block ("STAGED on this vintage: the FX4 replay LCG (seedRun/runSeed + startGame(forcedSeed) wiring)"), and this ask counted **11 `Math.random` sites remaining** in the canonical file (down from the 25 the doc cites). Rung I's second half (race engine + senet/ur delta packs, row I-8) has no bytes. Descend-before-climb applies: Rung II first, Rung I's proof write second, then the climb tools.

## 3. The next-5 (ranked by ramp law, delight-per-effort, and niche weight)

| # | Pick | Row | Rung | Effort | Why this one now | Falsifier inherited |
|---|---|---|---|---|---|---|
| 1 | **Finish the mud seeded LCG + `mud_play.v1` receipts** | II-26 | II | patch (the wiring is already staged at mud.html:67-74; 11 `Math.random` sites left by this ask's count) | THE enabling patch: half of Rung II (unidentified items, level grammar, infighting, replay QA, litigable bones) is blocked on it. Highest delight-per-effort in the entire queue because it makes every other pick arguable. | same seed + inputs → byte-identical `mud_play.v1` receipt; one-flip divergence names the INPUT_FORK frame (toy's law) |
| 2 | **StS intent telegraphs for ALL mud enemies** | II-40 | II | patch (bosses only today; the telegraph grammar is already shipped and P-LEGAL-asserted on the toy) | Rung II's P-LEGAL debt: the estate's own referee law says no hit without a same-enemy telegraph; ordinary mud enemies still violate it. Small delta on shipped bytes. | P-LEGAL sweep over ordinary encounters: zero hits from untelegraphed enemies on any tape |
| 3 | **Unidentified items** | II-28 | II | patch (the 4-rarity affix inventory loop is shipped; hiding affixes until first equip is a presentation + flag change) | Rogue's identification is the oldest delight-per-line mechanic in the table and it rides furniture that already exists (R2 orphan #3, consumed by N12). | a fresh run sees `?` affixes; first equip reveals and the reveal is receipted; seed-replay shows the same reveal order |
| 4 | **Inversion shrine** | II-36 | II | build, but one function over the existing `visionPoly` (torch occlusion shipped, no asserting lane) | THE_WEAVE §5's own bench calls it "the estate's most original unwired mechanic"; it is Rung II's sovereign-niche-adjacent stone (perception inversion as law, not effect). | the inverted polygon flips exactly at the circle boundary; torch-hidden enemies sleep inside it, wake outside it; one harness lane each way |
| 5 | **Frontier seeded LCG port + receipts** | III-14 | III | patch (same pattern as pick 1; 21 sites per the doc) | The climb: once Rung II's receipts land, frontier is the next rung and it needs the same enabling patch. Descend-law satisfied by doing it in mud's image: one LCG law, two skins. | `frontier_play.v1` byte-identical replay; seeded death 3-phase; grudge chronicle reproducible from the seed |

**Not picked, said out loud:** IV-15 / V-8 (niche 2 and 3 full forms) stay queued behind their rungs: the ramp law forbids building Rung IV/V full forms while Rung II's falsifier is unheld. I-8 (race engine + senet/ur packs) is the Rung I second-half proof and is the very next write if a tabletop-tier lane opens before II-26 does; it lost the #5 slot to III-14 only because II-26→III-14 is one pattern applied twice, and pattern-twice beats pattern-once per the ramp's own economics. X-2 hygiene bundle remains the preamble lane (ops, not per-game work).

## 4. Build order (serial, each unblocks the next)

1. II-26 mud receipts → unblocks replay QA for everything below.
2. II-40 telegraphs (asserted against the now-replayable tapes).
3. II-28 unidentified items (receipted reveals).
4. II-36 inversion shrine (two lanes: inside/outside the circle).
5. III-14 frontier LCG + `frontier_play.v1`.

All five: $0, local bytes, local relay, no paid APIs. Every pick names its consumer before it is built (wire law): consumers are the existing mud/frontier harnesses (`scripts/test_mud_fifty.js`, frontier lanes) plus the receipt chain.

## 5. Honesty notes

- The "43 remain" arithmetic is derived, not byte-counted per-row against the live HTML: it subtracts the five receipted DONE/COMPLETE lane landings from the doc's own 48. A row-by-row re-audit of mud.html bytes per mechanic was NOT run this ask (out of scope for a build-order memo; the receipts are the evidence of record).
- mud.html's current `Math.random` count (11) is this ask's byte count of the canonical `dashboard/static/games/mud.html` at 2026-09-28; the doc's "25 sites" describes the 09-16 vintage. The gap (25→11) is attributed to the W-lane RNG work and later passes; a per-site attribution was not mined.

*FW-32 stone closed 2026-09-28. Receipt: `watch/inbox/burn_reset_20260927/queue/Q-026.md`.*
