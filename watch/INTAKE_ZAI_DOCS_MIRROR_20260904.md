# INTAKE: Z.AI DOCS MIRROR (bulk ape order — the complete docs.z.ai corpus) — 2026-09-04

Genome: research_socratic (six steps) on L0 v1. Bulk-mirror job, not an analysis job — the
raw layer under the reference-patch work two other agents are running right now.

## ITEM
Operator order: "Ape the entire ZAI WEBSITE AND APIS." Mirror the complete z.ai developer
documentation site into `docs/ref/zai_docs_mirror/` so no seat ever byte-archaeologizes the
vendor again. Door order prescribed: llms-full.txt → llms.txt → section crawl.

## THE SIX STEPS (compact)

### 1. INGEST — what was met
- Door 1 CONFIRMED: `https://docs.z.ai/llms-full.txt` → 200, **647,819 bytes**, vendor
  Last-Modified 2026-09-03T21:55:58Z. The whole-docs single file exists and is fresh.
- Door 2: `llms.txt` → 68 page links. Door 3: `sitemap.xml` → 67 URLs (set-equal to the
  index modulo the moved rate-limit page). Door 4: per-page `.md` raw-markdown endpoints
  (Mintlify) — every page fetched as raw markdown via curl.
- openapi.json → valid JSON, 14 endpoint paths (chat completion, images sync+async, video,
  audio transcription, tokenizer, layout parsing, web search/reader, agent suite).

### 2. MAP — corpus intersections
- `docs/ref/ZAI_API_EXPERT_REFERENCE.md` = the prior hand-mined ANALYSIS layer. This mirror
  is its raw substrate — composed, not competing: interpretation on top of receipts.
- **Crop closure convergence**: INTAKE_ZAI_DEVPACK_MEMORY_20260903 card named its own unfetched
  crop (cache.md, devpack/faq, usage-policy, mcp/*, tool subpages) — ALL of it is inside this
  mirror now. Two lanes, same organ; that card's crop is closed.
- thinking-mode / cache / function-calling / struct-output / stream-tool mirrored verbatim
  (6.9KB–33.9KB each) — the raw feed for the in-flight reference-patch agents.
- claude-zai door page (`scenario-example/develop-tools/claude`, 9,355 bytes) on the shelf.

### 3. ASSERT — steel-man, one sentence
One llms-full.txt fetch is ~90% of the entire docs site and the llms.txt index lists every
page, so mirroring is a two-fetch job plus clean-up.

### 4. ATTACK — strongest counter-case (evidence attached)
- **Cause 1 — the vendor maps are provably incomplete.** llms-full.txt contains ZERO
  scenario-example content; llms.txt and sitemap.xml both omit the whole section. Link-graph
  closure over the 74 fetched pages exposed 12 more page-shaped paths absent from BOTH
  vendor indexes (retired-model guides: glm-4.5/4.6/4.7/5/5.1, glm-4-32b-0414-128k, VLMs
  glm-4.5v/glm-4.6v/autoglm-phone-multilingual, glm-image, cogview-4, cogvideox-3) — all 12
  probed 200 and fetched. 18 of the final 86 pages (21%) are invisible to the vendor's own
  maps. The index-only approach would have shipped a 79%-complete mirror wearing a 100% label.
- **Cause 2 — a page can move out from under its URL.** `api-reference/rate-limit` now 307s
  to `z.ai/manage-apikey/rate-limits` (console docs, HTML-only, no .md door); llms-full
  carries the same page as an empty 7-line stub. Concurrency-by-tier table survives only in
  `devpack/usage-policy.md` (mirrored).

[SOCRATIC] Assumption attacked: that the vendor's published index is the site's complete
surface. Instrument: three-source union (llms.txt ∪ sitemap ∪ live link closure) + $0
probing. What survives: 86 pages is the complete .md-exposed surface as far as three
independent discovery methods converge; residual incompleteness is bounded by the probe
method (name-guessing), not by the vendor's maps.

### 5. MEASURE — falsifiers run
- **Coverage: 86/86 pages mirrored — 100%.** 85 pages full vendor content, 1 documented gap
  (rate-limit stub + pointer; see CORRECT). Plus openapi.json (14 paths) and raw door
  captures. Final fetch log: 90 fetches, 90×200 (`_raw/fetch_log.txt`). Vendor markdown on
  disk: 1,080,016 bytes; tree 2.2MB.
- $0 RUN: HTML-masquerade census — zero mirrored files are HTML in disguise; zero files <300B
  except the documented stub.
- $0 RUN: openapi.json parses, 14 paths.
- Kill condition for "86 is complete": any docs.z.ai URL with a 200 .md body not in INDEX.md,
  or a new llms-full.txt Last-Modified adding pages → mirror is stale, refresh pass required.

### 6. CORRECT — public correction
- "llms-full.txt is 90% of the job" — **Supported** on byte volume (647KB of 1.08MB mirrored);
  **Disputed** as sufficient — it silently omits 21% of pages and one page it lists is an
  empty stub. Correction recorded: index-trust is a tri-state claim, never a given.
- "The vendor index lists every page" — **DISPUTED**, evidence: 18 unlisted pages fetched.
- "The mirror is the complete .md-exposed docs surface" — **Supported** (three-method
  convergence, 86/86, receipts in `_raw/fetch_log.txt`), residual risk named in THE CROP.
- "api-reference/rate-limit content" — **DISPUTED availability** (page moved vendor-side);
  endpoint-level numbers **Unproven** until the console HTML page is mined.

## THE MIRROR (artifact)
- Tree: `docs/ref/zai_docs_mirror/{guides,api-reference,devpack,scenario-example,legal-agreement,help,release-notes}/**.md` + `openapi.json`
- Index: `docs/ref/zai_docs_mirror/INDEX.md` — provenance header, 86 page lines (source URL,
  local path, size, one-line note), gap lines, license note (internal fleet use, copyright z.ai)
- Raw doors: `_raw/llms_index.txt`, `_raw/llms_full.txt`, `_raw/sitemap.xml`, `_raw/crawl_urls.txt`,
  `_raw/fetch_log.txt` (90×200), `_raw/link_closure.py` (the discovery tool, reusable)
- Priority sections verified byte-real: api-reference 18/18 (chat-completion 44.1KB), guides/capabilities
  7/7, devpack 18/18 incl. both notices (glm-5.3-flash campaign + plan revision), scenario-example 6/6

## SCORE (5 axes, 0–5)
- FIT 5 — a NEW shelf organ, honestly so: raw vendor truth as local files, composed with the
  wall-ledger law (the vendor's own words become walls we own). It is the substrate under the
  analysis layer, not a rival to it. Infrastructure every lane already reads.
- PULL 4 — unblocks four live consumers: the provider-reference patch (two agents analyzing
  thinking-mode/cache/fc/struct-output now have the raw layer), fuel_feed lane config, the
  claude-zai door page, and the isolation-law surface (routing/auto-routing claims now checkable
  against local bytes).
- COST 5 — $0 API spend, ~90 fetches, one pass, one evening.
- WINDOW 4 — landed while vendor docs are fresh (llms-full modified the day before the mirror);
  the open window is refresh cadence — no watcher owns re-crawl duty yet.
- NOVELTY 4 — the corpus is vendor-known, but the ghost-page discovery (18 pages absent from
  both vendor maps), the rate-limit move, and the reusable link-closure tool are new residue.
**TOTAL 22/25 → BUILD band.**

## VERDICT (three verbs, exhaustive)
- **BUILD (done this pass)**: the mirror + INDEX.md + door captures + closure tool. This card is the record.
- **CALIBRATE (routed, next seats)**: fold the raw layer into ZAI_API_EXPERT_REFERENCE.md —
  the in-flight reference-patch agents are the calibrators; openapi.json's 14 paths want folding
  into the reference's endpoint table. Rate-limit endpoint numbers want one hand-mine of the
  console HTML page.
- **REMEMBER**: the provenance law lands in INDEX.md (source, date, doors, license) — a mirror
  without provenance is just copy-paste; and the finding that vendor indexes undercount their
  own site by ~20% is now on record for every future "the docs say" argument.

## ROUTE
- Reference-patch agents (running now): pull from `docs/ref/zai_docs_mirror/guides/capabilities/*` — raw layer is on the shelf, no more vendor fetches needed.
- fuel_feed owner: pricing.md, rate-limit pointer (devpack/usage-policy.md for concurrency), devpack notices — all local now.
- Watcher candidate: a re-crawl line keyed on llms-full.txt Last-Modified — when it changes, re-run `_raw/crawl_urls.txt` + link-closure pass. No automation built this pass (fleet services stay in Docker, loopback-only; this would be a watchdog line, not a scheduled task).
- No bolt-on consumer to build. The shelf is the product.

## TWO COUNTERS
- FORBIDS: byte-archaeology against docs.z.ai — fetch the mirror first; a live vendor fetch is
  only licensed for refresh deltas and the one console-HTML gap. Also forbids trusting any
  single vendor index (llms.txt, sitemap) as a completeness claim.
- PAID RENT: four live workstreams get their raw layer today; the reference-patch agents stop
  paying fetch tax per page; every future lane error gets checked against local bytes, not a
  CDN round-trip.

## THE CROP (visibly incomplete)
- NOT mirrored: `z.ai/manage-apikey/*` console docs (rate-limits, my-plan) — HTML-only host,
  no .md door; needs a hand-mine if endpoint-level rate numbers matter to a lane.
- NOT proven exhaustively: that the scenario-example and model-guide ghost sets are complete —
  discovery was probe-based (guessed names + link closure); an exhaustive check needs scraping
  the JS-rendered nav tree, which this seat did not attempt (two-strike law respected in advance).
- NOT built: refresh cadence automation (owner + trigger unnamed — operator to assign the watcher).
- NEXT LENS: the reference-patch agents (calibration), then the fuel_feed owner (lane economics
  from local pricing/notices), then whoever holds the watchdog surface for the re-crawl line.

## RECEIPT (room row)
`2026-09-04 | zcode | INTAKE_ZAI_DOCS_MIRROR_20260904 | full docs.z.ai mirror landed: 86/86 pages + openapi.json, 1.08MB vendor markdown, llms-full door confirmed; vendor indexes proven 21% incomplete (18 ghost pages found by link closure); 1 gap = rate-limit moved to console HTML | verdict BUILD 22/25`
