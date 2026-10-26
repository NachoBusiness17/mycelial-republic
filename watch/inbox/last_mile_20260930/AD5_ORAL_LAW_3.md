# AD5_ORAL_LAW_3 — grok pool oral-law mine, third tranche (no API spend)

**Date:** 2026-09-29 · **Seat:** GLM-5.3 via `account:zai-individual-coding-plan` (glm mining glm, seat-local, `cost_usd: 0.0` on every row)
**Files owned:** this receipt + 30 new rows appended to `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` (93 → 123 rows). No commit.

## What was done

1. **Pool re-enumerated.** `corpus/oral_history/seat_pools/grok_sessions/` still holds 852 sessions with `summary.json`; `num_chat_messages` read at the TOP level per the AC12 gotcha (not under `info`). After excluding the 93 indexed `thread_id`s: 792 fresh; eligible (unique title, `num_chat_messages >= 8`, chat file present): 236.
2. **30 NEW threads picked** (zero `thread_id` overlap with all 93 pre-existing rows, asserted before append). V10 cwd-group caps (16 repo-root, 6 per `memory/runs/*` pool) yielded only 28 — the eligible pool has shrunk to 3 groups (repo-root 205, `x_bookmark_harvest_20260905` 25, `game_prompt_lab` 6). The remaining 2 were drawn from repo-root (18 total) to honor the 30-thread mission count; documented stretch, spread preserved. Spread: repo-root engineering (dashboard/GIL diagnoses, orchestrator audit, code reviews, ox-alpha reverse-engineer, business thesis, agent identity), 6 x_bookmark_harvest shift threads, all 6 remaining `game_prompt_lab` fleet-brief attackers, 3 HIVE PDF-digest siblings.
3. **Same digest recipe as V10/AC12** (user text from `<user_query>` tags, 12 x 600 chars; assistant plain-string first + last 4, clipped 800): 49,055 bytes, read in full by the seat.
4. **Same falsifier law**: every decision/law string literally traceable to digest text; ≤3 per field; same outer schema + `pool: "grok"`, model `account:zai-individual-coding-plan/GLM-5.3 (seat-local AD5 mine, no API spend)`.

## Numbers (instrument + moment named)

- **Threads processed:** 30 of 30 selected (selection instrument: `summary.json` enumeration 2026-09-29; 792 fresh remain unmined — sample, not exhaustion)
- **Rows appended:** 30 (index 93 → 123; all lines parse; 123 unique ids, no collisions)
- **Laws extracted this batch:** 56 `laws_or_debts` = **54 LAW: + 2 DEBT:** (every thread yielded ≥1; max 3 per field)
- **Confidence:** 25 high / 5 medium (medium = thin digests: line-cook story, Mirror Sea proposal, ox-alpha short sibling, first HIVE sibling with DONE not visible)
- **Running index total:** **306 laws_or_debts = 237 LAW + 69 DEBT** over 123 rows (pre-V10 33 rows: 88; V10: 89; AC12: 73; AD5: 56). Note: 3 pre-existing rows are `skip` rows and 2 older rows carry a `laws_or_debets` typo key alongside `laws_or_debts` — both counted via fallback.
- **Spend:** $0.00

## Leaderboard

**"Receipts/locator before verdict" stays the runaway #1.** This batch adds **8 thread-births**: the full remaining `game_prompt_lab` sextet on the GLM-5.3 cache fleet brief ("source bytes, not the gloss", "count the chain from disk", "cites bytes, not echo", "the court scores receipts, not the lab's story", "the court only admits locators", "locators first, verdicts second") plus the business-thesis and agent-identity threads. Instrument note: on a tight law-string keyword pattern (`locator|receipt|bytes, not|from disk|…`) the family reads 34/123 threads (26/93 on pre-existing rows vs AC12's hand-curated 20/93 — the keyword instrument is wider than the curated family; +8 this batch either way). No-fabrication/retrieved-only gains 4 births (the shift-harvest threads 1-4 all carry the literal "No fabrication" contract).

## Notable new laws banked

- "LAW: Output is never cache-discounted — sell below list on output tokens and you lose money on the only token that is generation" (business-thesis pressure test)
- "LAW: Multiplexing one account's cache discount is account-sharing, not a product"
- "LAW: An unapplied patch is not a fix — check the fix on disk against the server actually serving" (wave short-circuit patch existed but was never applied to `dashboard/server.py`)
- "LAW: A file rewired on disk is not the running system — probe the live port and module mtimes" (port 8765 was Docker-owned, not the local Python process)
- "LAW: A hollow extract is not the record — pull the filed brief and continuity from disk" ("DNA's test: 'What was I doing?' answers from files, not scroll — the pasted record fails that test")
- "LAW: A disagreement without a counter-artifact is a mistrial — struck from the record, with the striker noted"
- "DEBT: Planned to load the operator-corrections skill despite the prompt's 'Do NOT load any framework'" (third HIVE PDF sibling)
- "DEBT: Empty findings arrays on every turn — shape with no content is false completion" (**second** empty-findings specimen, tid `01a0102f-b9bb…`, n=60; twin of the AC12 `{"seams":[]}` specimen tid `01a01032-c147…` — the false-completion debt now has a matched pair)

## Method receipts

Scratch (selection script, digest builder, rows module, append script, digest corpus) lived in `%TEMP%\ad5_scratch\` and is deleted after this append; durable evidence is the 30 appended rows, each carrying `thread_id` → `grok_sessions/<cwd-enc>/<uuid>/chat_history.jsonl`.
