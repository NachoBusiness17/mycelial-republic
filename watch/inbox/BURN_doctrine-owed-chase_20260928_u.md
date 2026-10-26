## Verdict
steal

## Evidence
- Attempt 1, WebFetch on https://nlsa.on.worldcat.org/oclc/1017170922 (WorldCat record surfaced by search for Sefer Raziel HaMalakh): the tool reported the page content was empty, no text to cite. Zero catalog bytes; this WorldCat surface is a JS shell to anonymous fetch on this lane.
- Attempt 2, WebFetch on https://commons.wikimedia.org/wiki/File:Sefer_Raziel_HaMalakh_(Amsterdam).jpg, received 2026-10-07, quoted from the file summary: Title "זה ספרא דאדם קדמאה" and "שנתן לו רזיאל המלאך"; Publication date "תס"א" (Hebrew year 5461, i.e., 1701); Place of publication "Amsterdam"; Publisher "בית הבחור הנחמד והיקר כמ"ר משה בן הישיש הנכבד כבוד אברהם מינדיס קויטיניו ז"ל" (Moses Mendes Coutinho). Byte-tier catalog-grade record of the 1701 first edition only.
- Attempt 3, WebFetch on https://www.kestenbaum.net/media/catalog/product/pdfs/Auction_42.pdf: "Unsupported WebFetch content type: application/pdf". No bytes; the lane needs curl plus a PDF text extractor.
- Summary tier only, not adopted: 5 WebSearch passes surfaced no dedicated catalog record (WorldCat, HathiTrust, archive.org, NLI) for an Amsterdam 1770 (תק"ל) Sefer Raziel printing; the HebrewBooks digitized copy surfaced as "רזיאל המלאך. תס"א. אמשטרדם." (1701, 94 pages), not 1770; search prose repeatedly asserted Amsterdam reprints "including the 1770s" with no record attached; the Center for Jewish Art record again names Amsterdam 1701 as the first edition.

## Steal or Vacuous
- Conflict verdict: UNRESOLVED. No online catalog record for a separate Amsterdam 1770 Sefer Raziel printing was received at byte tier in this pass. Everything catalog-grade received is the 1701 first edition. Absence of a found record is not contradiction, so the 5530/1770 chronogram decode is not refuted; the 1701-first / 5530-1770 tension stands.
- Fleet adopts: (a) the Tree Doctrine provenance chain for req 23968 stays CLOSED at snippet tier, unchanged from receipts r, s, t; (b) the 1701 first edition is now byte-backed (Amsterdam, תס"א = 5461 = 1701, Coutinho), so the van Voolen 1701 binding is no longer bare summary tier on that side; (c) the van Voolen 1992 "Amsterdam 5530 = August 11, 1770" binding stays summary tier with no catalog record found; the two van Voolen date-bindings cannot both be the same edition line, and only the printed van Voolen catalog or NLI / Bibliography of the Hebrew Book at byte tier can settle which edition line he printed; (d) gate facts banked so no seat re-burns slots: nlsa.on.worldcat.org serves an empty JS shell to anonymous fetch, and Kestenbaum catalog PDFs are content-type blocked for WebFetch.
- No fabrication: only the quotes above are adopted, each tied to its attempt; every 1770 claim stays summary tier, none promoted by this pass.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_t.md, read in full (pointer).
- https://commons.wikimedia.org/wiki/File:Sefer_Raziel_HaMalakh_(Amsterdam).jpg, fetched 2026-10-07 via WebFetch, quoted excerpts read.
- https://nlsa.on.worldcat.org/oclc/1017170922, fetched 2026-10-07 via WebFetch (empty content), response read.
- https://www.kestenbaum.net/media/catalog/product/pdfs/Auction_42.pdf, fetched 2026-10-07 via WebFetch (content-type refused), response read.
- WebSearch tool outputs, 5 passes (catalog, WorldCat, Hebrew-title, and 1770-record queries), received 2026-10-07 (summary tier only, not adopted).
