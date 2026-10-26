# X INTEL: the imcaiden scraping-craft guide (2026-10-05)

Operator drop: "https://x.com/imcaiden/status/2106610698906476878"

## What it is

@imcaiden (21.4K followers; "I don't have delusions of grandeur, I have an
actual recipe for grandeur"), 2026-10-04 05:01 UTC, ~25K views with a
striking 1,239 bookmarks (2x the likes - people are FILING this one): a
long-form craft guide on scraping with understanding instead of defaulting
to browser automation. The technique list:

1. HAR diffing - reverse-engineer a site's query model from captured
   traffic instead of guessing endpoints
2. AST analysis of bundled JS (Babel/Acorn) - read what the frontend
   actually calls
3. Source recovery from exposed .js.map files
4. Mining hydration payloads (__NEXT_DATA__, Nuxt, RSC flight data) for
   the pre-rendered data the site already computed
5. Union-schema inference from varied JSON responses (handle the shape
   variance, do not crash on it)
6. Reconstructing the frontend's response transformations (the API shape
   vs what the UI shows)
7. Incremental acquisition - ETags / timestamps: do not re-pull what did
   not change
8. Multi-source reconciliation (with a jab at deduplicating entities by
   name alone)
9. Observability checks for SILENT data-quality failures

Thesis: "there's a LOT more to scraping than making a browser click
buttons" - understand the pipeline before automating it.

## Estate mapping (real doors, not poetry)

- PULL OVER DUMP, scraping edition: technique 4 is the estate's law in
  web form - take the data the site already computed (hydration payload)
  instead of driving a browser to recompute it. The corpus-harvest skill
  and the X radar should try payload mining BEFORE any headless-browser
  fallback.
- DATA IS A HIDDEN COST, scraping edition: technique 7 (ETag/timestamp
  incremental acquisition) is the operator's data-cost law applied to
  harvesting - the daily OLM sweeps and catalog refreshes re-transfer
  bytes that did not change; conditional GETs would shrink that leg.
- THE CENSUS LAW, scraping edition: technique 9 (silent data-quality
  failure checks) is the drift-patrol doctrine for scraped data - a
  scraper that quietly starts collecting empty pages is the scraping
  twin of the phantom index.
- Schema inference (technique 5) feeds the kit's laws.schema instinct:
  when a source returns union shapes, infer the union and validate
  against it instead of crashing or over-fitting one variant.
- Technique 3 (.js.map recovery) is a one-time unlock per site: when a
  bundle ships its map, the site's real API contract falls out.

## Action

None fired. The doors above fold into the estate's next
corpus-harvest/radar revision when one is touched for other reasons
(wire-when-touched, no dedicated burn for a craft list).

Writer: zcode-53-strategy-window
fetched: 2026-10-05
