# BURN doctrine-owed-chase, 2026-09-28 f

## Verdict
steal

## Evidence
- Transport: browser-UA curl (`curl -s --max-time 20 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"`), byte-quote only.
- Attempt 1, `https://hebrewbooks.org/books?name=%D7%A8%D7%96%D7%99%D7%90%D7%9C%20%D7%94%D7%9E%D7%9C%D7%90%D7%9A`, received 1,245 bytes, body title line: `404 - File or directory not found.` IIS error page. The `/books?name=` search shape is dead on this transport.
- Attempt 2, `https://beta.hebrewbooks.org/search?query=%D7%A8%D7%96%D7%99%D7%90%D7%9C%20%D7%94%D7%9E%D7%9C%D7%90%D7%9A`, received 1,245 bytes, identical body title line: `404 - File or directory not found.` The beta `/search?query=` shape is dead too.
- Attempt 3, `https://hebrewbooks.org/42032`, received 27,643 bytes, title line: `HebrewBooks.org Sefer Detail: תלמוד בבלי-הלכות קטנות-פפד"מ-ת"פ  --  יהודה אריה ליב ב"ר יוסף שמואל`. Wrong book. The string `רזיאל` occurs 0 times in the received bytes (grep count 0).
- This falsifies the second untested id hint from receipt e ("org/42032") exactly as the first hint ("around #23156", the Devir journal) was falsified before it. Both numeric hints in the ledger now carry byte-quoted disproofs.
- Fetch budget: 3 of 3 spent. The site-search pin did not land; the Raziel 1701 numeric id remains unverified.

## Steal or Vacuous
- Identity verdict: still-owed. The primary pull (Amsterdam 1701 Sefer Raziel HaMalakh title page, then p. 44b) remains unpinned; the p. 44b pin stays double-attested via Zeramim footnote 24 only.
- The pass still steals: two site-search routes are closed with byte-quoted 404s, and wrong-book closures rise from seven to eight (49094, 19632, sefer-raziel, sefer-raziel_202511, 51626, 22234, 23156, 42032). Numeric-id guessing is now fully retired for the Tree Doctrine name-magic lineage exhibit: every hint ever recorded has a title-line disproof.
- Route intel: direct numeric-id fetch on hebrewbooks.org returns real Sefer Detail pages under browser-UA curl (27,643 bytes for 42032), so the closing instrument is healthy; only the search entry points are dead. Next pass should take the search form's true action and parameter straight from the site's own homepage bytes, or obtain the beta record's URL bytes from a locator, then spend one fetch on the id and close via the title line. One clean fetch closes this pin once the id surfaces.
- Adopt: the ledger may cite this receipt for the eight closed ids, the two dead search shapes, and the falsified 42032 hint. It may not cite any HebrewBooks id as the Raziel 1701 id; none is byte-verified.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_e.md, read in full (pointer; confirmed beta record title, seven prior wrong-book closures, falsified 23156 hint, untested 42032 hint).
- hebrewbooks.org/books?name=<URL-encoded רזיאל המלאך>, fetched, 404 body quoted above.
- beta.hebrewbooks.org/search?query=<URL-encoded רזיאל המלאך>, fetched, 404 body quoted above.
- hebrewbooks.org/42032, fetched, title line quoted above.
