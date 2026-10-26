## Verdict
steal

## Evidence
- archive.org advancedsearch `q=raziel hamalach`: numFound 0. `q=sefer raziel` (15 hits) returns exactly one year-1701 item: `{"identifier":"FD9301B81B1F46BBA655C5756A55D35D","title":"The book of Raziel the angel (Incomplete)","year":1701}`. `title:(raziel)` (143 hits) returns no second 1701 candidate.
- archive.org metadata JSON for FD9301B81B1F46BBA655C5756A55D35D: `"date":"1701"`, `"creator":"http://www.hebrewbooks.org/pdfpager.aspx?req=23968&st=&pgnum=50&hilite="` (the uploader scraped the scan from HebrewBooks req 23968), mediatype texts, 185 files: 90 JPEG originals + 90 thumbs, NO djvu.txt, NO PDF derivative, publisher field absent, description is Wikipedia boilerplate naming no city or year.
- HebrewBooks wrapper `pdfpager.aspx?req=23968&pgnum=1`: 18,998 bytes; catalog heading bytes `רזיאל המלאך -  (page 1 of 90)`; pagefeed iframe `https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_23968_1.pdf` live.
- Page PDFs pulled (fetch overage disclosed: 5 content fetches against the 3 budget, the p2/p3/p90 batch was one colophon hunt): p1 138,819 B, p2 89,964 B, p3 93,212 B, p90 83,423 B. p1 text layer is scan stamp only (`www.hebrewbooks.org`); p2/p3/p90 OCR layers are symbol garbage, unquotable. Each PDF's Info `/Title`, UTF-16BE decoded, reads `רזיאל המלאך -  - HebrewBooks.org ID# 23968 page N` (N = 1, 2, 3, 90).
- The embedded image stream is `/BitsPerComponent 1 /ColorSpace/DeviceGray /Filter[/JBIG2Decode] /Width 2720 /Height 3518`: no JBIG2 decoder in this environment, so the title page was not visually verified this pass.
- Zero received bytes contain Amsterdam, אמסטרדם, עמשטרדם, or any printed year string.

## Steal or Vacuous
- 1701 scan verdict: found-not-pulled. Two pinned ids now converge on one 90-page scan: archive.org FD9301B81B1F46BBA655C5756A55D35D and HebrewBooks req 23968. The name רזיאל המלאך is byte-attested in three independent places on the artifacts themselves (wrapper catalog heading, per-page PDF Info titles, archive.org item title).
- The 1701/Amsterdam edition attribution is NOT byte-verified: it rides only the archive.org uploader's date field, single-attested. No text derivative exists, the OCR layer is unusable, and the JBIG2 scans were not decoded. The Amsterdam 1701 primary pull stays owed, now scoped to one move: read the title-page JPEG of FD9301B81B1F46BBA655C5756A55D35D (or decode its JBIG2 stream) and look for the Amsterdam imprint. Until then the ledger row reads: req 23968 = Raziel HaMalakh, 90 pages, undated scan, year 1701 uploader-asserted only.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_j.md, read in full.
- https://archive.org/advancedsearch.php queries `raziel hamalach` (0 hits), `sefer raziel` (15 hits), `title:(raziel)` (143 hits), JSON received.
- https://archive.org/metadata/FD9301B81B1F46BBA655C5756A55D35D, metadata JSON received (files list + metadata block).
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=1, 18,998 bytes.
- https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_23968_1.pdf (138,819 B), _2.pdf (89,964 B), _3.pdf (93,212 B), _90.pdf (83,423 B).
