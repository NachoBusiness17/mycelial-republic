# GSTD.EXPLAINED: the 3B1B-style live explainer site (operator GO, 2026-10-12)

Operator: "we could do our own 3 blue one brown style website for gstd
explaining fucking everything and mag oh god yes please this will be awesome"

THE SITE: one page, scroll-driven, every claim a live diagram. Not a video
(pauseable/zoomable/checkable is the thesis) and not a doc (every number is
computed in front of you). The rail_live.html canvas is scene 1; the site is
the full arc.

## The scroll arc (each section = one live diagram, Storyline模式: progressive
revelation, the 3B1B grammar):

1. THE TICKET (cold open): gray institutional tickets accumulating; a real
   event behind them never connecting. Scroll advances the pile. Line: "a
   ticket proves a ticket exists."
2. THE RECORDS OFFICE: append-only timeline growing on scroll; a copy
   detaching and reattaching on another machine; cut to platform-records with
   the export button producing a dead bag. "An archive is not a resurrection
   service."
3. THE RAIL: the existing rail_live canvas (magatama on sine waves, noise
   control discard, SettlementMaster split) - embedded as-is, scrubbed by
   scroll position. Real settle numbers computed live.
4. SILENT FAILURES (the perimeter's receipt set, animated): three toggleable
   failure modes - opcode vanish, exchange-rate dust, gas skip - each shown
   as an ABSENCE (expected-vs-actual side by side), each with the "repair in
   the open" replay button. These are the REAL probe findings from the
   perimeter build, not hypotheticals.
5. HIGH-TRUST IS LEGIBLE DANGER: greenhouse vs field split-screen; seeds grow
   in the field, failures leave persistent marks; a seed migrates and its
   path is tracked. "Trust without danger is marketing."
6. THE MAG SECTION: the magatama companion - what it is (PSO lineage), the
   feed law (pitfall-bypass delivery), the evolution-on-demand seed law, the
   ten-minute self. The magatama from the rail becomes the narrator's avatar:
   "this is your node. you feed it. it grows."
7. THE MESH: crews, records offices, the same rail; "copying the protocol
   does not copy the economy"; the map of benches (the Garage Wizard Guild
   link lives here).
8. THE FIELD IS BUILT. BRING SEEDS. (closing; the seed repo link, the
   installer link, the guild link.)

## Tech (vislab stack, zero dependencies)

- One self-contained HTML per section, composed into one scroller (the
  shadow_walk pattern: single file, canvas + DOM overlay, no build step).
- Scroll position drives each diagram's t (the rail already proves this
  pattern works - scrub = scroll).
- Every number computed client-side from constants set at page top (the real
  settle receipts, the 85/10/5, the confirmed-find counts) - inspectable via
  view-source, which IS the trust-bytes law applied to the explainer itself.
- Magatama renderer carried from rail_live.html.
- Deploy: repo pages / the gstd site's /explained route / standalone file.

## The order of building (each is a same-sitting lane)

S1: scroller skeleton + sections 1-3 (the rail canvas moves in wholesale)
S2: section 4 (silent failures - the perimeter receipt data drives it)
S3: sections 5-6 (field/mesh + the mag section)
S4: section 7-8 + deploy + the Guild link-up
Each lands in the repo under dashboard/explained/ so the estate's own
dashboard serves it.

## Why this matters beyond the site

This is the adoption-roughener's flagship: the site explains EVERYTHING
(the token, the rail, the perimeter, the mag, the guild) in the format that
gets extended, not admired. Every section is a self-contained idea with a
visible edge. The explainer IS the adoption engine.

Also: it is the answer to Lilith's third-question thread (the Ethereum-code
leg she asked about) and Pierre's hub pitch and Doug's Gate - one site that
explains the whole shape to every counterpart without a single meeting.

## Falsifier

If the site cannot explain a section to a cold reader in under 60 seconds of
scroll, the section is rewritten. The 3B1B bar: legible, not merely accurate.
