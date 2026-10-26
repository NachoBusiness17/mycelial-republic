## Verdict
vacuous

## Evidence
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=1 (18,998 B, byte-size equal to receipt-l's record): the wrapper carries zero page text. Only catalog chrome: heading "רזיאל המלאך -  (page 1 of 90)", UI labels "חפש בתוך ספר זה" / "הורד קובץ שלם", and the iframe src "pagefeed/hebrewbooks_org_23968_1.pdf#toolbar=1&navpanes=0&statusbar=0&view=FitH". 37 Hebrew-bearing lines, all UI, no plate transcription, no OCR layer.
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=2 (19,078 B): same shape, heading "רזיאל המלאך -  (page 2 of 90)", iframe src "pagefeed/hebrewbooks_org_23968_2.pdf#toolbar=1&navpanes=0&statusbar=0&view=FitH". Zero page text. The wrapper-HTML route is empty on both probed pages.
- Third and final content fetch, the iframe target itself: https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_23968_1.pdf (138,819 B, PDF 1.7, 1 page, Creator HebrewBooks.org, CreationDate D:20261002050748, freshly generated 2026-10-02). This file DOES carry a text layer (Tj/TJ operators present, zero /Image objects) and pypdf extract_text() returns 59 characters, quoted in full exactly as emitted: "לאינטרנט והוכנס הועתק / www.hebrewbooks.org / תשס״ט חיים ע״י" (natural RTL order: copied and entered to the internet by [Chaim?] in 5769). That is the modern HebrewBooks watermark credit line, not a transcription of the title plate. No באמשטרדם token, no "נדפס בשנת" formula, no chronogram tokens anywhere in the layer.

## Steal or Vacuous
- Chronogram verdict: still-owed. The pagefeed route is vacuous for req 23968 at the text level: the req 35004 precedent (pagefeed carries text) does not transfer, because here the text layer is the scanner's watermark only, and the plate remains the same 1277 px raster receipt-l already read to its resolution ceiling. The two middle tokens between זה and ארם stay unresolvable from bytes this route can serve.
- Receipt-l's falsifier stays armed exactly as written: a higher-resolution read of the oval showing a year other than 5461/תס"א, or any non-Amsterdam city token, reopens the pull. Nothing in this pass touched the year or city evidence; Amsterdam and the Abraham Mendis Coutinho printer line remain byte-backed per receipt-l.
- Residual debt, carried forward: the year-chronogram decode for the oval "נדפס בשנת ... לפ"ק". The next working route is a higher-resolution source (an archive jp2 original or a fresh scan), not more pagefeed HTML; the pagefeed-HTML theory for this item is now closed with byte-proof, not just suspected.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_l.md, read in full.
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=1 (18,998 B).
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=2 (19,078 B).
- https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_23968_1.pdf (138,819 B), text layer extracted with the repo venv pypdf.
