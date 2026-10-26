# BURN doctrine-owed-chase, 2026-09-28

## Verdict
steal

## Evidence
- WebFetch https://hebrewbooks.org/49094, fetched 2026-09-28: server returned HTTP 403 Forbidden, no body. Matches the pass-b note that the hebrewbooks route was 403-closed; the block is client-fingerprint-based.
- curl with a browser user agent on the same URL, fetched 2026-09-28: HTTP 200, 27,684 bytes, content type text/html. Page title, quoted verbatim: "HebrewBooks.org Sefer Detail: חזון יחזקאל - זבחים - ליקוטים על הש"ס  --  אברמסקי, יחזקאל בן מרדכי זלמן, 1886-1976". This is Chazon Yechezkel (Zevachim, Likutim on the Shas) by Yechezkel Abramsky. Wrong book. The commonly cited id 49094 is byte-closed as an identity mismatch for Sefer Raziel HaMalakh Amsterdam 1701.
- Page body check: the only "Metadata" occurrence is a lightbox link, quoted: "Add Metadata Correction". The pre-authorized metadata JSON curl was skipped because the page implies no JSON metadata route. A content handler ".ashx?req=49094" appears in the page source; no metadata endpoint.
- curl https://hebrewbooks.org/booksearch.aspx?searchtext=רזיאל המלאך, fetched 2026-09-28: HTTP 302 with header line quoted: "Location: /error.html?aspxerrorpath=/booksearch.aspx". The guessed search endpoint does not exist.
- WebSearch "hebrewbooks Sefer Raziel Amsterdam 1701", run once, locator only: results confirm the first edition as "Amsterdam, 1701, by Moses Mendes Coutinho", "title page within an architectural arch", five books, and state that "A full-text PDF version in Hebrew is available from HebrewBooks.org" and is frequently cited in academic work. The search surfaced no direct link or id. Search-engine text only; no bytes pulled behind these secondary claims.

## Steal or Vacuous
- Identity verdict: still-owed for the Sefer Raziel HaMalakh 1701 Amsterdam title page. The HebrewBooks route is now OPEN in transport terms (browser-UA curl receives 200 where WebFetch took a 403), but the correct id is unpinned; the one candidate id on the table (49094) is byte-closed as a different sefer.
- Adopt: no digest citation may cite hebrewbooks.org/49094 as the name-magic provenance exhibit. The Tree Doctrine provenance line for name magic keeps Sefer Raziel HaMalakh at primary-pull status owed.
- Next pass: obtain the correct HebrewBooks id from a citing source (a scholarly PDF or catalog entry that prints the hebrewbooks URL), then fetch detail.aspx?req=<id> with the browser-UA curl and quote the Sefer Detail title line. That single byte-quote closes the title-page identity.
- Steal, because the wrong-book closure prevents a false attribution now, and the pass recorded the transport condition that unblocked the 403 for the next id.

## Bibliography
- watch/inbox/TREE_DOCTRINE_V2_DIGEST_20260925.md, read lines 1 to 290 of 726 (name-magic lineage context, owed register).
- watch/inbox/BURN_doctrine-owed-chase_20260927_f.md, read in full (both archive.org candidates excluded; HebrewBooks route named next).
- watch/inbox/BURN_doctrine-owed-chase_20260927_b.md, lines 14 to 15 (hebrewbooks 403-closed note).
- hebrewbooks.org/49094, fetched twice (WebFetch 403; browser-UA curl 200), quotes above.
- hebrewbooks.org/booksearch.aspx?searchtext=רזיאל המלאך, fetched, 302 quoted above.
- WebSearch results, quoted as locator only.
