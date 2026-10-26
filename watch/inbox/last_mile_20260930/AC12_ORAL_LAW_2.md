# AC12_ORAL_LAW_2 — grok pool oral-law mine, second tranche (no API spend)

**Date:** 2026-09-29 · **Seat:** GLM-5.3 via `account:zai-individual-coding-plan` (glm mining glm, seat-local, `cost_usd: 0.0` on every row)
**Files owned:** this receipt + 30 new rows appended to `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` (63 → 93 rows). No commit.

## What was done

1. **Pool re-enumerated.** `corpus/oral_history/seat_pools/grok_sessions/` holds 852 sessions with `summary.json`. Note the message count lives at the TOP level of `summary.json` (`num_chat_messages`), not under `info` — a first pass read it under `info` and wrongly showed zero candidates.
2. **30 NEW threads picked** (zero `thread_id` overlap with the pre-existing 63 rows, asserted before append): unique titles, `num_chat_messages >= 8`, cwd-group caps as in V10 (16 repo-root, 6 per `memory/runs/*` pool; round-robin trim to 30). Spread: repo-root engineering (Vast wedge/deal hunts, render-farm playbook, primitives audit, connector salon, steering harness, spore delta), 7 x_bookmark_harvest shift threads, 4 salon-attacker siblings on the same fleet brief, 4 Villains Guild / daylight runs, art/cipher/spore/memory-recovery one-offs, 1 false-completion specimen. Selection manifest + digests in `%TEMP%\ac12_scratch\` (scratch, removed after append).
3. **Same digest recipe as V10** (user text from `<user_query>` tags, 12 x 600 chars; assistant plain-string first + last 4, clipped 800): 54,602 bytes, read in full by the seat.
4. **Same falsifier law**: every decision/law string literally traceable to digest text; ≤3 per field; same outer schema + `pool: "grok"`, model `account:zai-individual-coding-plan/GLM-5.3 (seat-local AC12 mine, no API spend)`.

## Numbers (instrument + moment named)

- **Threads processed:** 30 of 30 selected (selection instrument: `summary.json` enumeration 2026-09-29; pool 852 — sample, not exhaustion)
- **Rows appended:** 30 (index 63 → 93; all lines parse; 93 unique ids, no collisions)
- **Laws extracted this batch:** 73 `laws_or_debts` = **64 LAW: + 9 DEBT:** (every thread yielded ≥1; max 3 per field)
- **Confidence:** 28 high / 2 medium (medium = thin digests: spore jailbreak reply, empty-output mine specimen)
- **Running index total:** **250 laws_or_debts = 183 LAW + 67 DEBT** over 93 rows (pre-V10 33 rows: 88; V10 30 rows: 89; AC12 30 rows: 73)
- **Spend:** $0.00

## New top law by birth count

**"Receipts/locator before verdict"** is now the index's top law family: carried by **20 of 93 threads** (8 from this batch — the five salon-attacker siblings on the GLM-5.3 cache brief alone contributed "receipts, not the brief's own numbers", "a locator, not a gloss", "a FALLS without a locator is a mistrial", "verify against Mag disk rather than the prompt", "grep hitting the gloss is not enough"). This overtakes V10's co-leaders (no-fabrication 7 threads; audit-from-bytes 7). No-fabrication grows to 6 thread-births on the literal `fabricat` token plus the harvest family's "from retrieved posts only" (5 more threads).

## Notable new laws banked

- "A file that landed with a .png name but JPEG bytes must be converted before the save is claimed — claim saves from bytes on disk, not the generation receipt"
- "Kill-and-requeue is cheap only when the unit is independent, overwrites a known path, and does not re-download; killing a box that still owes the 120GB pull is the mismatch"
- "A curl pull with no speed floor and no timeout is a dead TCP session, not a slow host (331 MB / 90 min)"
- "Connectors are compiled ribs, not a fourth syscall — secrets stay in the adapter; results become event.v1 receipts"
- "Weights don't carry memory — recoverable continuity is transcripts plus the files they named"
- "DEBT: empty-findings JSON on a mine task is false completion (the `{"seams":[]}` specimen, 2026-08-17)"

## Method receipts

Scratch (selection script, digest builder, extraction rows) lived in `%TEMP%\ac12_scratch\` and is deleted after this append; durable evidence is the 30 appended rows, each carrying `thread_id` → `grok_sessions/<cwd-enc>/<uuid>/chat_history.jsonl`.
