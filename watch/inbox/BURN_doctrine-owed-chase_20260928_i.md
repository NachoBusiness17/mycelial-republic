# BURN doctrine-owed-chase, 2026-09-28 i: Sefer Raziel snippet route

## Verdict
steal

## Evidence
- WebSearch, two queries, surfaced in a markfoster.net "Translations of the Zohar" resource page the direct citation "hebrewbooks.org/pdfpager.aspx?req=35004&pgnum=7", presented as a HebrewBooks scan of Sefer Raziel HaMalakh. Locator only; markfoster.net itself was not fetched.
- Fetch 1 of 3, browser-UA curl on https://hebrewbooks.org/pdfpager.aspx?req=35004&pgnum=7, title line received verbatim: `רזיאל המלאך -  (page 7 of 124)` (Raziel HaMalakh). Body bytes include the download link `https://download.hebrewbooks.org/downloadhandler.ashx?req=35004` labeled "9MB PDF" and the per-page iframe `https://beta.hebrewbooks.org/pagefeed/hebrewbooks_org_35004_7.pdf`; the page selector runs 1 through 124.
- Grep of the full 20,150-byte response for 1701, Amsterdam, אמסטרדם, אמשטרדם: zero hits. The pdfpager page carries no edition-year string.
- Fetch 2 of 3, https://www.hebrewbooks.org/bookdetails.aspx?req=35004: received `<h2>Object moved to <a href="/error.html?aspxerrorpath=/bookdetails.aspx">here</a></h2>`; redirect followed within attempt 3 to a 720-byte "Error Page". Details route dead; budget spent at 3.

## Steal or Vacuous
- The snippet route delivered exactly what the state predicted: a live numeric HebrewBooks id (req 35004) whose byte-received title line reads רזיאל המלאך. Scan identity is pinned: Sefer Raziel HaMalakh, 124 pages, downloadable 9MB PDF, per-page feed live at the pagefeed URL pattern. This id is distinct from the closed wrong-book ids (49094, 19632, sefer-raziel, sefer-raziel_202511); this closure is a title match, not another wrong book.
- Still-ambiguous: the Amsterdam 1701 edition identification of req 35004. Zero year strings in the received bytes; the 1701 attribution rides the citing snippet only. The title page (page 1 at the pagefeed pattern) is the primary pull that would settle it, now a single known URL.
- Ledger adopt: cite HebrewBooks req 35004 as the live scan id for the name-magic lineage exhibit. Do not cite it as byte-confirmed Amsterdam 1701 until the page-1 pull lands.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_d.md, read in full (double-attested p. 44b pin, wrong-book census).
- watch/inbox/BURN_doctrine-owed-chase_20260928_h.md, read in full (lane separation).
- WebSearch result text, two queries, locator only.
- https://hebrewbooks.org/pdfpager.aspx?req=35004&pgnum=7, fetched, byte-quoted.
- https://www.hebrewbooks.org/bookdetails.aspx?req=35004, fetched, redirect to error page received.
