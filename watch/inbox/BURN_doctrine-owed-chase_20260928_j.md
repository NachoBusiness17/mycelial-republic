## Verdict
steal

## Evidence
- Fetch 1, browser-UA curl on https://hebrewbooks.org/pdfpager.aspx?req=35004&pgnum=1: 20,070 bytes, selector reads `page 1 of 124`, per-page iframe `https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_35004_1.pdf` live. Zero hits for 1701, Amsterdam, אמסטרדם, אמשטרדם in the wrapper bytes.
- Page-1 PDF pulled: 55,035 bytes, PDF 1.7, 1 page, HebrewBooks OCR text layer present. Title-page lines received (pdftotext UTF-8 layout; OCR noise marked):
  - Scan stamp, not edition: `הועתק והוכנס לאינטרנט` / `www.hebrewbooks.org` / `ע״י חיים תשס״ט` (copied to the internet by Chaim, 2009).
  - Title: `זה ספרא` / `ראיס קדמאה שנתן לו` / `רזיאל המלאך` (this is the book Raziel HaMalakh; OCR-noisy).
  - Name-magic exhibit text on p. 1: `ולכל ביח ישראל היא סגולה מעולה` ... `מי שאין זוכה ללמוד בו רק שהוא בביתו גנוז` ... `ופשכ ובהזו` [OCR of כספו וזהבו] ... `ינצל מן שריפה ומן שוד ושבר עכ״ל` (the segulah: one who cannot study it but keeps it hidden in his house, his silver and gold are saved from fire, robbery and breakage).
  - Edition statement, p. 1: `מחמת שהראשונים נבר קפו תמו נדפ ק עהר^ מחדש` (OCR-noisy: earlier printings exhausted, now printed anew) / `בבית הרפוס המשיבח והמפואר של` / `בנימין זאב רובינשטיין נראסוו.י,רדיין` (place garbled by OCR) / `. שנת תיש״ד לפ״ק.` (year 714 small count = AM 5714 = 1953/54 CE; OCR caveat).
- Fetch 3, page-2 PDF `https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_35004_2.pdf`: 1 page; bottom carries the Hungarian printer imprint (diacritics lost to OCR): `Nyomatott` / `»Rubinstein Vilmos kbnyvnyomddjdba` / `Nagyvdrad`, i.e. printed in the book-printing house of Vilmos Rubinstein, Nagyvarad (Oradea). This resolves the garbled Hebrew place string on p. 1: the city is Nagyvarad, not Amsterdam. Page 2 top also shows the publisher's hasagat-gevul clause: `איסור השגת` ... `עד משך עשר שנים להדפיס ספר זה`.

## Steal or Vacuous
- Primary pull landed. HebrewBooks req 35004 is byte-confirmed Sefer Raziel HaMalakh, 124 pages, pagefeed live, and page 1 carries the name-magic segulah passage in the book's own bytes: the Tree Doctrine exhibit can cite the scan directly.
- Provenance corrected: req 35004 is NOT the Amsterdam 1701 edition. Its own title page declares a reprint (`מחדש`, earlier printings exhausted) at the press of Binyamin Zev Rubinstein (Hungarian imprint: Vilmos Rubinstein), Nagyvarad, year string `תיש״ד` (= 1953/54, OCR caveat). No 1701 or Amsterdam string exists in any received byte. The 1701 attribution that rode the citing snippet is wrong-edition for this scan id. Ledger row: cite req 35004 as the mid-20th-century Nagyvarad reprint; the Amsterdam 1701 primary pull reverts to a separate owed source, now with the new fact that this pinned id cannot serve it.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_i.md, read in full (pinned scan id req 35004, 124 pages, pagefeed pattern, single owed primary step).
- https://hebrewbooks.org/pdfpager.aspx?req=35004&pgnum=1, fetched, 20,070 bytes, byte-quoted.
- https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_35004_1.pdf, fetched, 55,035 bytes, text layer extracted, byte-quoted.
- https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_35004_2.pdf, fetched, text layer extracted, byte-quoted.
