# BURN doctrine-owed-chase, 2026-09-28 g

## Verdict
steal

## Evidence
- Transport: browser-UA curl (`curl -s --max-time 20 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"`), byte-quote only.
- Locator search (does not count): re-ran "hebrewbooks beta razial hamalach tass-a sefer raziel 1701 site:beta.hebrewbooks.org". The site-restricted query returned no direct matches. Results were Wikipedia Sefer Raziel HaMalakh, Center for Jewish Art (cja.huji.ac.il) "Raziel ha-Malakh, Amsterdam, 1701", and the beta and parent homepages. No record URL recovered; the locator route is exhausted for this query shape.
- Fetch 1, https://hebrewbooks.org/42032 (the ledger's untested hint), title line received: `HebrewBooks.org Sefer Detail: תלמוד בבלי-הלכות קטנות-פפד"מ-ת"פ  --  יהודה אריה ליב ב"ר יוסף שמואל`. Wrong book. Hint falsified on the classic domain.
- Fetch 2, https://beta.hebrewbooks.org/ homepage form bytes: `<form method="post" action="./" id="form1" onsubmit="return false">`. ASP.NET postback, no GET search endpoint, no numeric record links in the raw homepage. The homepage-form route is closed as a direct id source.
- Fetch 3, https://beta.hebrewbooks.org/42032, title line received: `HebrewBooks.org 42032 תלמוד בבלי-הלכות קטנות-פפד"מ-ת"פ  --  יהודה אריה ליב ב"ר יוסף שמואל`. Wrong book, and the same id resolves to the same title on both domains.
- Route intel byte-confirmed from the 42032 page markup: `action="./detail.aspx?req=42032"`. The canonical detail pattern is `hebrewbooks.org/detail.aspx?req=<id>`.
- Fetch budget: 3 of 3 spent.

## Steal or Vacuous
- Identity verdict: still-owed. The Raziel 1701 id is not byte-verified; the primary pull (Amsterdam 1701 Sefer Raziel HaMalakh title page, then p. 44b) remains unpulled; the p. 44b pin stays double-attested via Zeramim footnote 24 only.
- The pass still steals: the 42032 hint is falsified on both domains. Wrong-book closures now run nine: 49094, 19632, sefer-raziel, sefer-raziel_202511, 51626, 22234, 23156, 42032 classic, 42032 beta. The last two byte-prove classic and beta share one id space, so any future recovered id can be tested on either domain with one fetch.
- Route intel for the Tree Doctrine name-magic lineage exhibit: canonical detail pattern `detail.aspx?req=<id>`; the homepage search is a JS postback, not a GET; guessing numeric ids is a dead end, now proven at nine falsified.
- Adopt: the ledger may cite this receipt for the nine closures, the id-sharing proof, and the detail.aspx pattern. It may not cite any HebrewBooks id as the Raziel 1701 id; none is byte-verified.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_e.md, read in full (pointer; seven prior wrong-book closures, confirmed beta title `רזיאל המלאך. תס"א. אמשטרדם.`, untested 42032 hint).
- hebrewbooks.org/42032, fetched, title line and form action quoted above.
- beta.hebrewbooks.org/, fetched, form tag quoted above.
- beta.hebrewbooks.org/42032, fetched, title line quoted above.
- WebSearch result text, one query ("hebrewbooks beta razial hamalach tass-a sefer raziel 1701 site:beta.hebrewbooks.org"), no record URL returned.
