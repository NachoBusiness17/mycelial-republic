## Verdict
steal

## Evidence
- Attempt 1, WebFetch on https://www.kedem-auctions.com/en, received 2026-10-07: "The server returned HTTP 403 Forbidden." No site bytes.
- Attempt 2, curl with browser UA on the same URL: HTTP 403, 5,504 bytes, title "Just a moment...", CSP naming challenges.cloudflare.com: Cloudflare shell, zero site bytes.
- Attempt 3, curl through r.jina.ai on the pinned lot URL: HTTP 403, 6,144 bytes, same "Just a moment..." Cloudflare shell. The shell fires before origin, so the slug is unverified at byte tier.
- web_reader rejected the lot URL client-side twice: "MCP error -400: Please Enter the Correct URL Format!" (the en-dash slug defeats its parser). No bytes from Kedem.
- Pin (byte-received from the DuckDuckGo lite SERP, 14,102 bytes, redirect link decoded once): https://www.kedem-auctions.com/en/large-collection-bibliographies-and-studies-%E2%80%93-1927-2019-%E2%80%93-dedications-authors (slug reads as a lot of offprints with author dedications, 1927-2019); second hit in the same SERP: /en/ask-about-item/163905.
- Search-summary tier only, not adopted: the listing line surfaced as "Hebraica and Judaica printed in the northern Netherlands before 1815 in the collection of the Jewish Historical Museum of Amsterdam, מאת Edward van Voolen. [ללא מקום], 1992. תדפיס. עם הקדשת המחבר" (print, with the author's dedication). No Sefer Raziel edition line appears in any surfaced lot text. Second summary-tier flag: search now binds van Voolen 1992 to Sefer Raziel Amsterdam 1701 (first edition), while the chain's snippet-tier claim is 5530/1770.

## Steal or Vacuous
- Tier verdict: stays snippet-tier. The Kedem lane is now graded, not merely untried: kedem-auctions.com is Cloudflare-challenge-gated against anonymous fetchers on all three lanes tried (plain WebFetch, browser-UA curl, reader proxy), and the pinned lot is a dedication-copy collectible listing of the printed van Voolen catalog, not a quoting text. The opening hypothesis, that auction lot prose may quote the van Voolen Sefer Raziel edition line, is unsupported by everything surfaced: zero Sefer Raziel text in the lot at any tier received.
- What the fleet adopts: (a) the Tree Doctrine provenance chain for req 23968 remains CLOSED at snippet tier, unchanged from receipts r and s; (b) the ledger gains the exact lot URL pin plus the gate fact, so no seat re-burns anonymous Kedem fetch slots: the lane needs a JS-capable logged-in browser or the printed catalog itself; (c) a summary-tier tension is flagged for the next seat, 1701 vs 5530/1770 as the van Voolen-described Raziel edition; resolving it needs the JSTOR page or the printed catalog at byte tier, not another SERP pass.
- No fabrication: fetch-shell quotes are byte-received; the lot URL is byte-received from the SERP redirect, shown percent-encoded; every catalog-content or Sefer Raziel line above is marked summary tier, none promoted.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_s.md, read in full (pointer).
- https://www.kedem-auctions.com/en, fetched 2026-10-07 via WebFetch (HTTP 403) and curl with browser UA (5,504-byte Cloudflare shell); both responses read.
- https://r.jina.ai/https://www.kedem-auctions.com/en/large-collection-bibliographies-and-studies-%E2%80%93-1927-2019-%E2%80%93-dedications-authors, fetched 2026-10-07 via curl (6,144-byte Cloudflare shell), read.
- https://lite.duckduckgo.com/lite/?q=site%3Akedem-auctions.com+%22van+Voolen%22, fetched 2026-10-07 via curl (14,102 bytes), read (pin source).
- WebSearch tool outputs for the Kedem and van Voolen queries, received 2026-10-07 (summary tier only).
