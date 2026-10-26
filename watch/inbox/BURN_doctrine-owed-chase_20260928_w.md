## Verdict
steal

## Evidence
- Attempt 1, browser-UA curl on https://hebrewbooks.org/detail.aspx?req=23968: transport line "HTTP_CODE=200 SIZE=27414 CONTENT_TYPE=text/html; charset=utf-8"; 27,414 bytes received. One identical re-fetch to a local path after a shell path mismatch (2 of 3 attempts, remote 200 both times).
- Title bytes: page element `<title>HebrewBooks.org Sefer Detail: רזיאל המלאך`; detail row "כותר | רזיאל המלאך" (Raziel HaMalakh).
- Place bytes: `מקום דפוס</td> <td class="detailcontent"> <span id="cpMstr_lblHebPlace" class="detailtext">אמשטרדם</span>` (Amsterdam).
- Year bytes, Hebrew: `שנת דפוס</td> <td class="detailcontent"> <span id="cpMstr_lblHebDate">תסא</span>`. English gloss: `Pub. Date</td> <td class="detailcontent"> <span id="cpMstr_lblDate" class="detailtext">1701</span>`. Decode by arithmetic: תסא = 400+60+1 = 461, plus the millennium = 5461 anno mundi = 1700/01 CE, consistent with the gloss.
- Embedded catalog JSON bytes: `'hebrewTitle': decodeURIComponent('רזיאל המלאך'), 'hebrewAuthor': decodeURIComponent(''), 'cityOf': decodeURIComponent('אמשטרדם'), 'hebrewYear': 'תסא'`.
- Other rows: "Pages דפים | 90"; "Source מקור | Chabad-Lubavitch Library ספריית חב"ד ליובאוויטש".
- Zero occurrences of "5530", "1770", or תק"ל in the 27,414 received bytes.

## Steal or Vacuous
- Corroboration grade: the detail page's own catalog metadata states Pub. Date 1701 (תסא), so it corroborates the 1701 first edition, not the 5530/1769-70 decode. The 1701-vs-5530 conflict is resolved at catalog tier: for req 23968 the catalog's edition-year field says תסא/1701, while the plate chronogram 5530 (byte-backed from the title plate in prior receipts) remains a plate-level reading the catalog does not adopt as this scan's edition year.
- Steal in fleet canon terms: deterministic catalog bytes received on the transport that passes, recorded verbatim, and reusable. The Tree Doctrine provenance chain for req 23968 now carries both faces at byte tier, plate says 5530, catalog says 1701, and no seat re-burns a slot re-fetching this page. Vacuous would have been a challenge shell or zero bytes; neither happened. No fabrication: only the quotes above are adopted; the chronogram decode stays summary tier from its own receipt.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_v.md, read in full (pointer).
- https://hebrewbooks.org/detail.aspx?req=23968, fetched 2026-10-07 via browser-UA curl (HTTP 200, 27,414 bytes), response read in full.
