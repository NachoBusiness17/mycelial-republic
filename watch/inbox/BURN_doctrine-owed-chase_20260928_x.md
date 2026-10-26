## Verdict
steal

## Evidence
- Catalog constraint (receipt w, req 23968): Pub. Date gloss "1701", Hebrew year field "תסא" (400+60+1 = 461, +5000 = 5461 anno mundi), zero occurrences of 5530, 1770, or תק"ל in the 27,414 received bytes.
- Fresh reads from the native bitmap logs/burn_tmp/p1_2736.png (2736x3485, mode L) via ink projection plus 10x/12x nearest-neighbor crops (ct_line2_full, ct_W1_right, ct_W2_mid, ct_W3_mid, ct_SH_token, ct_LG_token, ct_line3_full in logs/burn_tmp/):
  - Line 2 (prose band top 2639-2643, bottom 2666-2674) reads right to left: נשלם בשנת זה סע [long token]. Letter inventory: נ(50) ש(300) ל(30) ם(40) | ב(2) ש(300) נ(50) ת(400) | ז(7) ה(5) | ס(60) ע(70) | ת(400) ו(6) D(4 or 30) ר(200) ו(6) ר(200). Receipt p's token reads re-confirmed at 12x (samekh closed bowl with top-left entry, ayin knob into enclosed counter-bowl, tav symmetric double full-depth legs, thin vav strips, two resh-like glyphs); D stays the single residual call (dalet vs lamed).
  - Fifth band-breaker receipt p never names: the lamed of נשלם, cluster x1641-1735, top 2626 against the prose top band 2639-2643.
  - Line 3 (band 2694-2756) reads: ארם לפ"ק : Letters: א(1) ר(200) ם(40) | ל(30) פ(80) ק(100). The aleph of ארם is resolved at 6x (diagonal stroke with head knob).
- Subset-sum (exhaustive, in-fire, PyMuPDF 1.28.2 + PIL 12.2.0 repo venv): target 461 is reachable from the plate inventory. With D=dalet: 2,114 subsets hit 461. With D=lamed: 1,934 subsets hit 461. Canonical witness present in BOTH states: tav(400) + samekh(60) + aleph(1) = 461 = 5461 = 1701, tav from the oversized long-token head, samekh from the oversized short token, aleph from ארם on line 3, independent of the D call. The oversized-only arithmetic (530 excluding D, 534 with dalet, 560 with lamed) is confirmed as receipt p states it; it is an artifact of a four-glyph window that never inventoried the line 2 prose words or line 3.

## Steal or Vacuous
- Genuine chronogram confirmed at 5461, in fleet canon terms. The plate carries the exact letter sequence the catalog year field spells (תסא), and line 3 closes with לפ"ק (minor era), the marker declaring a gimatria year counted without the millennium, which is the 5461 convention. Plate and catalog say the same thing: 1701. The decoder's oversized-only band-break heuristic was the error: its window missed the aleph of ארם and the prose-band letters, so it could only reach the phantom 5530/5534/5560 family. Receipt-o's 633 overshoot arithmetic and receipt-p's 5530-family year gate are superseded. Tree Doctrine provenance for req 23968 closes with one face: primary pull plate and catalog tier agree on 1701, the 1701-vs-5530 conflict is resolved at both tiers, and no seat re-burns a slot re-litigating this page.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_w.md, read in full (catalog corroboration).
- watch/inbox/BURN_doctrine-owed-chase_20260928_p.md, read in full (decoder letter reads and band metrics).
- logs/burn_tmp/p1_2736.png, native JBIG2 page-1 bitmap, re-read via ink projection and 10x/12x nearest-neighbor crops.
- logs/burn_tmp/full23968.pdf page 1 (5,913,576 B, image xref 99), the primary pull the bitmap decodes from.
