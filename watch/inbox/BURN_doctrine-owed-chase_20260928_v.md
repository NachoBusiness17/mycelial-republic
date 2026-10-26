## Verdict
steal

## Evidence
- Attempt 1, browser-UA curl on https://nli-primo.hosted.exlibrisgroup.com/PrimoWebServices/xservice/search/brief?institution=NLI&vid=NLI&query=any,contains,Sefer%20Raziel%20HaMalakh: curl wrote "HTTP_CODE=000 SIZE=0 CONTENT_TYPE=" and exited 1. No response bytes of any kind; zero catalog bytes.
- Attempt 2, browser-UA curl on https://www.nli.org.il/en/search-all?query=Sefer%20Raziel%20HaMalakh: "HTTP_CODE=403 SIZE=6877 CONTENT_TYPE=text/html; charset=UTF-8"; response header "Server: cloudflare"; body: <title>Checking your browser...</title>, <span id="challenge-error-text">Enable JavaScript and cookies to continue</span>, and challenge config "cType: 'managed'", "cZone: 'www.nli.org.il'". A Cloudflare managed challenge shell; zero catalog bytes.
- Attempt 3, browser-UA curl on https://nli-primo.hosted.exlibrisgroup.com/primo_library/libweb/webservice?verb=Search&institution=NLI&vid=NLI&query=any,contains,Sefer%20Raziel: transport lines "* Could not resolve host: nli-primo.hosted.exlibrisgroup.com" then "* Could not resolve: nli-primo.hosted.exlibrisgroup.com:443". Zero bytes; the named primo host does not resolve on this lane in either shape.
- No catalog record for Sefer Raziel HaMalakh Amsterdam 1770, or any printing, was received at byte tier in this pass.

## Steal or Vacuous
- Conflict verdict: UNRESOLVED. The NLI lane produced no catalog record for a separate Amsterdam 1770 Sefer Raziel printing. Absence of a received record is not contradiction, so the 5530/1770 chronogram decode stays unrefuted and the 1701-first / 5530-1770 tension stands. The Tree Doctrine provenance chain for req 23968 stays CLOSED at snippet tier, unchanged from receipt u and its predecessors.
- Fleet adopts gate facts so no seat re-burns slots: (a) nli-primo.hosted.exlibrisgroup.com is DNS-dead on this lane in both named shapes (PrimoWebServices xservice brief and primo_library webservice verb=Search); (b) www.nli.org.il serves a Cloudflare managed challenge to browser-UA curl, so it is a JS shell to anonymous non-JS fetch, the same class as the WorldCat shell banked in receipt u. The lane is shape-blocked, not exhausted: a real browser context, a resolvable alternate NLI or Bibliography of the Hebrew Book API hostname, or the printed van Voolen catalog remain the honest ways to settle which Amsterdam edition line van Voolen catalogued.
- Steal because deterministic refusals with recorded bytes are reusable estate facts; vacuous would be attempts returning nothing recordable. No fabrication: only the quotes above are adopted, each tied to its attempt; every 1770 claim stays summary tier, none promoted by this pass.

## Bibliography
- watch/inbox/BURN_doctrine-owed-chase_20260928_u.md, read in full (pointer).
- https://nli-primo.hosted.exlibrisgroup.com/PrimoWebServices/xservice/search/brief?institution=NLI&vid=NLI&query=any,contains,Sefer%20Raziel%20HaMalakh, fetched 2026-10-07 via browser-UA curl (transport failure, HTTP 000, zero bytes).
- https://www.nli.org.il/en/search-all?query=Sefer%20Raziel%20HaMalakh, fetched 2026-10-07 via browser-UA curl (403 Cloudflare managed challenge), response read.
- https://nli-primo.hosted.exlibrisgroup.com/primo_library/libweb/webservice?verb=Search&institution=NLI&vid=NLI&query=any,contains,Sefer%20Raziel, fetched 2026-10-07 via browser-UA curl (DNS failure, zero bytes).
