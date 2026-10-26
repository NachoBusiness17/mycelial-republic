# BURN doctrine-owed-chase, 2026-09-28 e

## Verdict
steal

## Evidence
- Transport: browser-UA curl (`curl -s --max-time 20 -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"`), byte-quote only.
- Attempt 1, https://hebrewbooks.org/51626, title line received: `HebrewBooks.org Sefer Detail: ויצבר יוסף  --  צמח, יוסף בן ראובן`. Wrong book.
- Attempt 2, https://hebrewbooks.org/22234, title line received: `HebrewBooks.org Sefer Detail: בית משה - חלק א  --  טריוקס, משה חיים`. Wrong book.
- Attempt 3, https://hebrewbooks.org/23156, title line received: `HebrewBooks.org Sefer Detail: ה דביר Vol. 8 No. 2 Iyar 5710  --  `. Wrong book.
- Locator search (does not count): "hebrewbooks sefer raziel 1701 id" returned a beta.hebrewbooks.org record snippet titled `רזיאל המלאך. תס"א. אמשטרדם.` with `Read Online · Download 7MB PDF` and `Search in this Sefer חפש בתוך ספר זה`. Snippet, locator only, page unfetched.
- The same search summary asserted the id is "commonly cited as around #23156". Fetch falsified that: 23156 is the Devir journal. A second id hint, "org/42032", came from the same summary, is untested, and carries the same trust level: none until a title line is pulled.
- Fetch budget: 3 of 3 spent. The Amsterdam 1701 title page was not pulled this pass.

## Steal or Vacuous
- Identity verdict: still-owed. The primary pull (Amsterdam 1701 Sefer Raziel HaMalakh title page, then p. 44b) remains unpulled; the p. 44b pin stays double-attested via Zeramim footnote 24 only.
- The pass still steals: three wrong ids are closed with byte-quoted title lines, taking wrong-book closures from four to seven (49094, 19632, sefer-raziel, sefer-raziel_202511, 51626, 22234, 23156). Negative closure is provenance work for the Tree Doctrine name-magic lineage exhibit.
- Route intel: the 1701 record demonstrably exists on HebrewBooks under the exact title `רזיאל המלאך. תס"א. אמשטרדם.` on the beta subdomain. Guessing numeric ids is a dead end; the next pass should query the HebrewBooks site search for that Hebrew title and take the id from the resulting detail URL, then pull the title page and p. 44b through the pubhtml5 viewer.
- Adopt: the ledger may cite this receipt for the seven closed ids and the confirmed record title. It may not cite any HebrewBooks id as the Raziel 1701 id; none is byte-verified.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_d.md, read in full (pointer; p. 44b pin state, Zeramim footnote 24, prior wrong-book closures).
- hebrewbooks.org/51626, fetched, title line quoted above.
- hebrewbooks.org/22234, fetched, title line quoted above.
- hebrewbooks.org/23156, fetched, title line quoted above.
- WebSearch result text, one query ("hebrewbooks sefer raziel 1701 id"), beta.hebrewbooks.org snippet, locator only, unfetched.
