# G3-2 — LAW CO-CITATION WIRE-UP (consumed G2-3's evidence, edges lost their taste)

Date: 2026-09-11. File: `dashboard/static/viz_lattice_test.html`.
Source: `watch/inbox/mickey/G2_3_cocitation.md` + `_cocitation_raw.json` (4,415-file corpus scan).

## What changed
- **Taste edges deleted.** The old 34-edge `EDGES` array ("chain order plus semantic links" —
  pure vibes) is gone. Replaced by two measured arrays: `PRIMARY_EDGES` (same-file "law N"
  number co-citation) and `KEYWORD_EDGES` (signature-phrase bridges the number pass misses,
  e.g. XVII via "1301|riddler").
- **Edge width = evidence.** `bandWidth()` bands count at 1 / 2 / 3 / 5+ (0.8 / 1.6 / 2.6 / 4 px),
  per the card's own advice to render bands, not raw magnitude. Spring force also scales with
  count — heavier evidence pulls tighter.
- **Dashed = keyword-bridged.** Pairs with keyword evidence but zero numbered co-citation
  render dashed. Included: the card's top keyword-only pairs (L2-L17 18, L9-L17 17, L11-L17 9,
  L10-L17 7) + the rescued zero-number pairs (L2-L9, L2-L11, L9-L11, L10-L11, L2-L7, L12-L15)
  + L17-L18 (3) so L18 renders keyword-bridged, not empty, per the card's wiring notes.
  Pairs already solid from the number pass stay solid (keyword only corroborates).
- **Isolated-node rule shipped.** Any node with zero edges in the union renders standalone:
  dashed ring, no glow, dimmed core, always-labeled with " — no co-citation in corpus".
  Data-driven: currently **zero nodes qualify** (the honest union covers all 18 laws — L11
  hangs on 4 dashed keyword bridges, L18 on one).
- **Legend added** (top-right panel): width bands 5+ / 3-4 / 2 / 1, dashed = keyword-bridged,
  dashed-circle = isolated. Header sub + footer rewritten to cite the corpus scan and the
  solid/dashed distinction.

## Evidence-based edge count (verified by node script, not eyeballed)
- **67 solid** primary edges + **11 dashed** keyword bridges = **78 edges**.
- 0 duplicate pairs; max primary count 7 (L1-L2, L1-L3); max keyword count 18 (L2-L17).
- All 18 laws have at least one edge; isolated set empty after the union.

## Data note (tri-state: DISPUTED headline, SUPPORTED list)
G2-3's headline says "68 edges" but its own embedded JSON (and `_cocitation_raw.json`)
sums to **67** (2@7 + 2@6 + 5@3 + 23@2 + 35@1). I embedded the raw JSON faithfully — 67.
Card arithmetic off-by-one; the machine copy is the truth and it is what shipped.

## Verify
`node --check` on the extracted inline script: PASS. Edge/degree counts above computed from
the shipped file, not the card.
