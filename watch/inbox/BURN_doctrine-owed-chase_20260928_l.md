## Verdict
steal

## Evidence
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=1 (18,998 B): the wrapper carries zero page text. Bytes contain only the catalog heading "רזיאל המלאך -  (page 1 of 90)" and the iframe src https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_23968_1.pdf plus JS. No text block exists; the pagefeed-HTML route is empty for this item.
- https://archive.org/download/FD9301B81B1F46BBA655C5756A55D35D/ listing (195,165 B): 90 full-size .jpeg originals with UUID names. Metadata JSON (57,027 B): earliest mtime 1541317280 is FD9301B8-1B1F-46BB-A655-C5756A55D35D.jpeg, the file the item identifier itself is named for.
- That JPEG received 885,009 B, 1277x1449, sha1 1305cab055cb6aa1c51ff892c9a8fe81e089f88f = metadata sha1. Visual read of the received bytes (Read tool plus PIL crops): title-plate banner "זה ספרי רזיאל המלאך / שכחן על ישראל להלל" (approx at source res); imprint block lines "...הנחמד והיקר כמהר"ר משה(?)" then "הנכבד כבוד אברהם מנדיס" then "קיטיניו ז"ל :"; oval "באמשטרדם / נדפס בשנת זה(?) כפ"י(?) התר"ן(?) / ארם(?) לפ"ק :"; and a modern-type credit line at the foot "הרפרודוקצי(ה/ות) ... לא(מ)סטרדם" (middle token low confidence at 8x).
- Second page by mtime, 818ACE64-BFD8-4DB5-B989-0276E86863D7.jpeg, 591,790 B, 1044x1451, sha1 ad075518e44ec1e0e079c183eaf8fb914c79638c = metadata. Modern typeset page: heading "הקדמה רבעי(?) המגיה", body opens with the book's own opening formula "בזה אכתובא דקדוקי הבטויים ע"י הדא ספרא נביעיא" (approx), confirming the reset text is Raziel.

## Steal or Vacuous
- The owed imprint move is unblocked and executed. The JBIG2 blocker is dead as a class: the archive item's original JPEGs read directly with no decoder. The pagefeed-HTML theory is vacuous for this item, but the archive-JPEG route is the primary pull that works.
- Amsterdam imprint: byte-backed on the title plate, the token באמשטרדם in the oval. Printer family: byte-backed, "הנכבד כבוד אברהם מנדיס / קיטיניו ז"ל" with a משה in the line above, matching the externally cited Moses Mendes Coutinho press.
- Year 1701: the on-page date formula is present ("נדפס בשנת ... לפ"ק") but the chronogram tokens are not fully resolvable at 1277 px source width. 1701 stays externally corroborated (archive date field, HebrewBooks attribution, receipts j and k), now materially strengthened by the byte-backed Amsterdam and Coutinho imprint on the plate.
- Provenance flag: the scanned copy is a later reset reproduction with the 1701-style title plate as frontispiece, not the 1701 ink original. Ledger row as it now stands: req 23968 = Raziel HaMalakh, 90-page modern reset edition reproducing the Amsterdam Coutinho title plate (year externally dated 1701); Amsterdam byte-backed, year digits still owed at full strictness.

## Falsifier
- Pre-registered: a higher-resolution read of the oval (archive.jp2 original or a fresh HebrewBooks scan) showing a year other than 5461/תס"א in the "נדפס בשנת" formula, or any non-Amsterdam city token in the oval, falsifies the 1701-Amsterdam leg of this row and reopens the pull.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_k.md, read in full.
- https://hebrewbooks.org/pdfpager.aspx?req=23968&pgnum=1 (18,998 B).
- https://archive.org/download/FD9301B81B1F46BBA655C5756A55D35D/ (195,165 B).
- https://archive.org/metadata/FD9301B81B1F46BBA655C5756A55D35D (57,027 B).
- https://archive.org/download/FD9301B81B1F46BBA655C5756A55D35D/FD9301B8-1B1F-46BB-A655-C5756A55D35D.jpeg (885,009 B).
- https://archive.org/download/FD9301B81B1F46BBA655C5756A55D35D/818ACE64-BFD8-4DB5-B989-0276E86863D7.jpeg (591,790 B).
- Local PIL crops of the two received JPEGs.
