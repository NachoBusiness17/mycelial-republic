## Verdict
steal

## Evidence
- PyMuPDF 1.28.2 (repo venv) on logs/burn_tmp/full23968.pdf: page 1 rect 492.5 x 627.3 pt, image xref 99 at 2736 x 3485 filling the page (5.556 px/pt), so zoom 8 is 1.44x upsampling; the native JBIG2 decode p1_2736.png is the byte ceiling. Fresh render chase_line23_z8.png (1009 x 289, clip zoom 8) shows the same structures; all reads are from 8x/12x nearest-neighbor crops of the native bitmap (chase_glyphA/C/D/F_12x, chase_shortL/R_12x, chase_cmp_short2/long2/D).
- Ink-projection metrics: line 2 prose glyphs sit in the band top 2639-2643, bottom 2666-2674; four glyphs break that band: glyph D x1213-1233 (top 2623, tall), glyph F x1248-1286 (bottom 2681, deep), short-token right x1367-1400 (bottom 2684, deep), short-token left x1320-1364 (width 44 vs prose max 30). Line 3 has zero oversized glyphs.
- Short token resolved: right glyph a closed round bowl with top-left entry stroke matching the samekh of "מנדס" in the title printer line; left glyph a top-left head knob with diagonal into a wide bottom-right enclosed counter-bowl matching the ayin of "נעלם". Token reads "סע" (60 + 70), both oversized.
- Long token resolved: rightmost glyph is tav, not he: symmetric double full-depth legs plus a bar extending past the left leg, while the "זה" he reference shows asymmetric legs. Then vav (thin 8 px strip, not a yod), then glyph D (bar plus descending diagonal matching the big-line dalet reference but with a much taller left serif; lamed and tet references ruled out; the single residual letter call, dalet vs lamed), then resh (matches "ארם" resh), vav, resh. Token reads "תודרו[ר]".
- Receipt-o's "התריו or היתריו" is refuted at max zoom: no he at token start, the yods are vavs, the tav sits first, and there is a second resh receipt-o missed. Its 633 overshoot arithmetic is superseded.
- Arithmetic: 5461 (תס"א) requires likut 461 = 400 + 60 + 1. No defensible marking of the resolved letters reaches it. The four band-breaking oversized letters give 530 excluding D, 534 with D as dalet, 560 with D as lamed, i.e. years 5530/5534/5560 (1769/70, 1773/74, or 1799/1800 CE).

## Steal or Vacuous
- Chronogram verdict: decoded-and-refuted. The owed two-glyph token is read ("סע") and the old tav/dalet call is dissolved by the refutation; 5461 is refuted on these bytes. Receipt-o's falsifier fires: the reset reproduction plate (provenance flag per receipt-l) carries a renewed date formula, most plausibly 5530/5534/5560, exact year gated on the one residual call (D: dalet vs lamed).
- Banked: ink-projection glyph metrics as the likut detector (band-breaking letters are the count letters); the whole-book downloadhandler PDF plus native JBIG2 decode remains the working primary pull for req 23968.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_o.md, read in full (pointer).
- logs/burn_tmp/full23968.pdf page 1 (5,913,576 B, image xref 99, 2736 x 3485 JBIG2), rendered via PyMuPDF 1.28.2.
- logs/burn_tmp/p1_2736.png and the chase_* derivative crops in logs/burn_tmp/ (cartouche, line23 1x/nn6x/z8, per-word 8x, per-glyph 12x, comparison sheets, printer_2x).
- logs/burn_tmp/hi_oval_1x.png (prior seat's crop, read for orientation).
- logs/burn_tmp/metadata.json (archive item FD9301B81B1F46BBA655C5756A55D35D, title "The book of Raziel the angel (Incomplete)", date 1701).
