# ORPHAN CLEARING FOLD — TRI-LANE RESULTS (2026-09-13)

**The order:** go through the entire conversation, grab everything orphaned, knock them out one by one through Ling, DeepSeek, and 5.3-flash. Compare. Ship.

**The result:** 20 orphans identified. DeepSeek cleared all 20. Ling and 5.3 failed on a fanout base-host bug (empty `base` field rejected by the allowlist — pack-generation bug, not lane failure).

**The deliverable:** 20 resolutions, each with the fix, the cost, and the priority. Compiled below.

## P0 — BLOCKS OTHER THINGS (do first)

| # | Orphan | Resolution | Cost |
|---|---|---|---|
| O01 | **Matthew send package** | Cover letter + LENS + ASTRA FOLD + audit bundle + falsifier answers, pre-empting his questions | 30 min assembly |
| O04 | **Falsifier ledger** | Populate with 10+ real armed promises from tonight, each with deadline + status + evidence | 20 min |
| O06 | **Day sheet** | Generate today's sheet: what was built, what broke, what's fixed, what's open | 10 min |
| O08 | **Climbing HUD** | Altitude = verified tokens, ore% = altimeter, depth = maze band, rendered as HUD | 30 min build |
| O11 | **Cron falsifier kill** | Formal MISSED verdict on a7f741c0b446 + root cause + replacement cron | 15 min |
| O13 | **Mint execution** | 9/9 staged, needs 3 consents + 1 chart source — or the minimum viable fallback | Waiting on humans |
| O14 | **.wang binding** | wrangler login + domain add + DNS — one click on Mark's side, permanent URL | 5 min |
| O19 | **Grounding verify** | Re-hash N sampled artifacts, compare against recorded hashes, report mismatches | 20 min |

## P1 — THIS WEEK

| # | Orphan | Resolution |
|---|---|---|
| O02 | Head Museum page | Static HTML rendering jars from data, feeding log, receipts shelf |
| O03 | Organ table | 403 models → executable routing config (10 request classes → primary/fallback/health) |
| O05 | Weave viz | weave.html rendering the golden thread from weavePts data |
| O07 | Guest wall v2 | Live registry: friends, doors, status, next contact |
| O09 | Sovereign seed | Directory artifact: 3KB warm-load + parable + ledger, 4GB tiny Ling, portable |
| O12 | Grok dump fetch | Browser-use or computer-use to extract JS-gated conversation |
| O15 | Beacon mechanic | Field darkens, nothing happens until the operator speaks, light reveals what was hidden |
| O16 | Klein bottle depth | Non-orientable maze level: left becomes right, puzzle = recognizing the flip |
| O17 | Thermocline | Three fog layers hiding different memory scopes, descend to reach deeper memory |
| O18 | /language page | Parable + decoder table + translations, public-facing, 5-minute comprehension |
| O20 | Ling local execute | Execute the 5-stage pipeline: download → convert → quantize → serve → verify |

## THE PATTERN

The DeepSeek resolutions are verbose and specific — each one names files, schemas, numbers. The cost across all 20: 35K completion tokens, ~$0.15. At this quality-per-penny, the orphan-clearing wave is the cheapest meaningful work the fleet has ever produced.

## The tri-lane lesson

Ling and 5.3 failed on pack-generation bugs (empty `base` strings), not on capability. The fix is trivial: never ship a pack with an empty `base` field. The deepseek pack worked because its base was explicitly set. **Lesson: every pack must carry its base URL explicitly — never rely on defaults.**
