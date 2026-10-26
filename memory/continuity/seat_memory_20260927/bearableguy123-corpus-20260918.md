---
name: bearableguy123-corpus-20260918
description: BearableGuy123 identified + harvested 2026-09-18 — XRP anonymous riddler (u/bearableguy123, X @BearableGuy123); 92 submissions 2016-2025, 275 comments 2016-2019, 14 real decodable images (CORRECTED from 64 — 57 were Reddit permalink HTML pages saved as .jpg, quarantined); Reddit JSON 403 → arctic-shift is the live Reddit-corpus path; vision census: Distracted Boyfriend meme with COINBASE/BTC/XRP = meme-grammar found; called-shot ledger = 0 dated claims (image-only confirmed)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_c424b80a-5f44-4511-bcdb-8dcec10fdce9
---

Operator: "bring in bearable guy shit if you can find it" (2026-09-18, alongside
"dozens of sources with this shit, steal them"). Identified via web search:
**BearableGuy123** = anonymous XRP-community riddler — cryptic artwork,
hidden-message images, numerology drops (the $589 genre), Christmas Eve "space
riddles"; u/bearableguy123 on Reddit (moderates Ripple subreddits), X
@BearableGuy123. Same anonymous-riddle genre as Q and Mr Pool — third sibling
corpus. NOTE: speculation corpus, entertainment register, never financial advice.

**Harvest complete (`watch/inbox/bearableguy_export/`):**
- submissions.jsonl: 92 rows, span 2016-10-29 → 2025-12-24.
- comments.jsonl: 275 rows, 2016-10-29 → 2019-06-23 (he went image-only after).
- media_full/: **CORRECTED 2026-09-19 — 14 real decodable images (NOT 64).**
  57 downloads were Reddit permalink HTML pages saved as .jpg (link posts with
  no media_metadata, no galleries); quarantined to html_error_quarantine/.
  The downloader treated every submission.url as a media task when it matched
  reddit hosts; comment-page URLs served HTML. See CORRECTION.json.

**Transport steal (reusable):** www/old.reddit.com JSON APIs now 403/block
scripted access. **arctic-shift (arctic-shift.photon-reddit.com/api) is the
live Pushshift successor** — `posts/search?author=X&limit=100&before=<epoch>`
paginates cleanly (descending; use `before` cursor, NOT `after` — after=0
400s). SSRF-guarded urllib pattern used throughout.

**Puzzle frame (operator's, all parts of a larger puzzle):** three sibling
corpora now in the estate spanning 2016→2026 — Q drops (6,242 posts 2017-2022),
Mr Pool (3,663 msgs 2023-2026), BearableGuy123 (2016-2025, reddit artwork).

**VISION CENSUS (vision_census.jsonl):** 14 real decodes — awq436 = **Distracted
Boyfriend meme with COINBASE/BTC/XRP labels** = BG123's grammar is meme-templates
as market-narrative statements. The "57 systematically silent-decline" finding
was WRONG: those files were HTML pages, not images. The vision model was
correct that there was nothing to see.

**Cadence pass:** BG123 is the QUIET image riddler — ~1 post/month for 9 years,
zero dated claims in text (image-only confirmed by ledger v1 = 0). Vision
pass is PRIMARY for this corpus.

**PERMALINK STATUS (final, 2026-09-19):** the 57 link posts are OUT OF REACH
by current tooling — arctic-shift per-id lookups return empty on all
2016-era ids (the posts are comment-permalink pages, not direct media; no
media_metadata, no galleries). PERMALINK_STATUS.json filed; recoverable
corpus stands at 14 decodable artworks. Page-level browser fetches are the
only remaining path, if ever wanted.

Related: [[qdrop-corpus-harvest-20260918]], [[mrpool-telegram-export-pending]],
[[riddle-triad-cadence-20260918]], [[time-travel-called-shot-steal-20260918]]
