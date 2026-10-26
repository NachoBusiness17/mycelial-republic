## Verdict
steal

## Evidence
- https://archive.org/metadata/FD9301B81B1F46BBA655C5756A55D35D (57,026 B received): zero .jp2 files among the 185 listed. The item carries 90 original JPEGs plus thumbs, no book derivatives. The jp2 route named in the fire order is vacuous for this item.
- Fetch 1, the page-1 original https://archive.org/download/FD9301B81B1F46BBA655C5756A55D35D/FD9301B8-1B1F-46BB-A655-C5756A55D35D.jpeg: 885,009 B, sha1 1305cab055cb6aa1c51ff892c9a8fe81e089f88f, byte-identical to receipt-l's copy, 1277x1449. The 1277 px ceiling is the archive original's own resolution.
- Fetch 2, https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=1 (18,998 B, equal to receipts l and n): surfaced the whole-book route downloadhandler.ashx?req=23968.
- Fetch 3, https://download.hebrewbooks.org/downloadhandler.ashx?req=23968: 5,913,576 B, PDF 1.5, 90 pages. Page 1 carries one XObject: /Bg, /Image, 2736x3485, /JBIG2Decode, DeviceGray, 1 bit. The JBIG2 stream decoded in-fire with the repo venv's PyMuPDF 1.28.2 (MuPDF native JBIG2); Pillow 12.2.0 did the crops. 2.14x the archive ceiling.
- Native-resolution reads of the oval: line 1 "באמשטרדם" and line 3 "ארם לפ"ק :" now letter-clean; "זה" letter-clean. The long contested token resolves as a real word: התריו or היתריו (letters ה, then ת or ד, then ר, then ו, plus one or two yods; the ת-vs-ד call is not separable from these bytes). The short token stays letter-unresolved: exactly two glyphs, a closed bowl plus a looped arm-letter; no letter mapping is defensible. This supersedes receipt-j's "four letters with a clear pe and a yod" for that position, which does not match the two-glyph structure at native res.
- Chronogram arithmetic on the defensible letters: זה = 12; התריו = 621; היתריו = 631. Year 5461 לפ"ק requires the phrase letters to sum 461 (תס"א = 400+60+1). Even excluding the short token entirely, זה + התריו = 633, overshooting 461 by 172.

## Steal or Vacuous
- Chronogram verdict: still-owed-with-named-tooling, with the falsifier provisionally armed. Under standard mispar-hechrachi לפ"ק counting the visible letters cannot encode 5461; either the plate's chronogram counts a letter subset these bytes cannot yet adjudicate, or this reset reproduction plate (provenance flag per receipt-l) carries a renewed date formula and the falsifier fires. No year is asserted from this fire.
- Debt narrowed: the owed decode is now one short two-glyph token plus a ת/ד letter call, not the whole phrase. Named tooling for the close: a 600 dpi fresh scan of the plate, or a HebrewBooks master above the 2736 px 1-bit JBIG2, plus an independent second plate copy (a different edition scan reproducing the same plate) to disambiguate the short token.
- Route upgrades banked: the archive-jp2 theory is closed with byte-proof (no jp2 exists); the working high-resolution primary pull for req 23968 is the downloadhandler whole-book PDF, JBIG2 decoded with PyMuPDF, documented here for reuse.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_n.md, read in full (pointer).
- watch/inbox/BURN_doctrine-owed-chase_20260928_l.md, read in full.
- watch/inbox/BURN_doctrine-owed-chase_20260928_j.md, _k.md, _m.md, _i.md, read by targeted grep for chronogram, year, and printer claims.
- https://archive.org/metadata/FD9301B81B1F46BBA655C5756A55D35D (57,026 B, metadata, not counted as a content fetch).
- https://archive.org/download/FD9301B81B1F46BBA655C5756A55D35D/FD9301B8-1B1F-46BB-A655-C5756A55D35D.jpeg (885,009 B).
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=1 (18,998 B).
- https://download.hebrewbooks.org/downloadhandler.ashx?req=23968 (5,913,576 B).
- Local PyMuPDF and PIL crops of the decoded 2736x3485 bitmap (logs/burn_tmp/p1_2736.png and derivatives).
