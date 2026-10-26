## Verdict
steal

## Evidence
- Pointer receipt-p: "glyph D x1213-1233 (top 2623, tall)" (BURN_doctrine-owed-chase_20260928_p.md:6) and "the single residual letter call, dalet vs lamed" (:8), candidates "530 excluding D, 534 with D as dalet, 560 with D as lamed" (:10).
- All reads this pass are from logs/burn_tmp/p1_2736.png (the native JBIG2 decode of full23968.pdf page 1 per receipt-p, 2736 x 3485), measured via PIL/numpy (repo venv, glyph_settle.py) at 8x/12x nearest-neighbor zoom; labeled sheet banked as settle_D_vs_refs_8x.png.
- Glyph D (x1213-1233) row projection: head knob y2623-2626 (w4-6), thin stem w3-4 down y2627-2638, i.e. 16 rows above band top 2639; wide bar y2640-2645 (w17-19); narrow leg w2-6 descending from the bar's right end x1233 down-left to x1224-1228, foot y2666.
- Lamed control 1, the prose word nishlam on the same line (x1665-1687): head y2626, stem w5-8, bar y2643-2650 (w17-20), leg from x1686 down-left to x1677-1681, foot y2670. Lamed control 2, the lamed of lefi"q line 3 (x1411-1432): same four phases, bar y2711-2717 (w18-20), leg x1432 down to x1422-1426. All three share the same ~9 px leftward leg drift. D matches the lamed signature in every phase.
- Dalet control, the oval word b'amsterdam (x1250-1305): roof bar begins at the letter's first rows (y2502-2522, width to 56, the full letter), zero ascender, thick straight leg below. Oval resh (x1315-1369) and the long token's resh (x1187-1208): same bar-at-top build, no ascender. D's 16-row ascender is un-dalet; 5534 is dead.
- Marking test (chronogram likut counts only letters marked beyond their class): D bottom 2666 sits on the line baseline (prose bottoms 2666-2674), total h44 vs the same-line lamed h45, width 21 vs 23; D's top excess over the prose lamed is 3 px (2623 vs 2626), serif scale. A lamed always breaks the band (the nishlam lamed breaks it identically), so receipt-p's band-break detector over-fired on D. The three date letters are marked: tav bottom 2681 (+11 below baseline norm 2670), samekh bottom 2684 (+14), ayin width 37 vs prose max ~31.
- Arithmetic: likut = tav 400 + samekh 60 + ayin 70 = 530, year 5530 = 1769/70 CE. 5560 rejected: D carries no marking beyond its class norm.

## Steal or Vacuous
- Chronogram verdict: year pinned. Glyph D is settled LAMED by same-plate paleographic control (two same-size lameds, dalet and resh roof-bar controls), and the likut pins 5530 on the reset reproduction plate (provenance flag per receipt-p); 5461 stays refuted on these bytes.
- Banked: the class-norm marking test (count a letter only when it violates its own class norm; band-break alone over-fires on lamed) as an upgrade to the ink-projection likut detector; artifacts settle_D_vs_refs_8x.png and glyph_settle.py in logs/burn_tmp/.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_p.md, read in full (pointer).
- logs/burn_tmp/p1_2736.png (native decode of full23968.pdf page 1, image xref 99 per receipt-p), measured via glyph_settle.py.
- logs/burn_tmp banked crops viewed: chase_glyphD_12x.png, chase_cmp_D.png, chase_cmp_long2.png, chase_line23_z8.png, chase_line3_10x.png, chase_printer_2x.png, chase_overview.png, chase_cartouche_1x.png.
- New artifacts this pass: settle_D_vs_refs_8x.png, settle_printerzone_1x.png, settle_printerzone2_1x.png, settle_mendes_line_2x.png, settle_mendes_line1_2x.png, glyph_settle.py.
