# AH12_ORAL_LAW_4 — grok pool oral-law mine, fourth tranche (no API spend)

**Date:** 2026-09-30 · **Seat:** GLM-5.3 via `account:zai-individual-coding-plan` (glm mining glm, seat-local, `cost_usd: 0.0` on every row)
**Files owned:** this receipt + 30 new rows appended to `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` (123 → 153 rows). No commit.

## What was done

1. **Pool re-enumerated.** `corpus/oral_history/seat_pools/grok_sessions/` still holds 852 sessions with `summary.json`; `num_chat_messages` read at the TOP level (AD5 gotcha held). After excluding the 123 indexed `thread_id`s: 762 fresh; with `num_chat_messages >= 8`: 209; eligible (unique title, chat file present): 169. The eligible fresh pool has shrunk to **2 groups** (repo-root 150, `x_bookmark_harvest_20260905` 19) — `game_prompt_lab` was exhausted by AD5.
2. **30 NEW threads picked** (zero `thread_id` overlap with all 123 pre-existing rows, asserted before append). V10 cwd-group caps (16 repo-root, 6 per `memory/runs/*` pool) yielded only **22**, so **8 stretch repo-root threads** (24 repo-root total) were drawn to honor the 30-thread mission count — same documented-stretch move as AD5, widened because the pool keeps shrinking. Spread: repo-root engineering (six PDF-digest siblings + infographic render case, memlang shared-registry design, fleet salon, Vast economics + throughput deep-research, EXP-BRAIN-01 packer, council runner, CoT-distillation SOTA witness, GGUF boot playbook, systems-reliability review, generational correctness audit, 3090 model upgrade, BLUEPRINT + SELF extractions, elder cross-exam, two Socratic council rounds), 6 x_bookmark_harvest threads (live-lane hunt, two shift harvests, the three reply-fetch verbatim threads).
3. **Same digest recipe as V10/AC12/AD5** (user text from `<user_query>` tags, 12 x 600 chars; assistant plain-string first + last 4, clipped 800): **49,194 bytes, read in full by the seat**. Note: the two `01a0464e-*` extraction sessions carry no `<user_query>` tags (API-run seats) — their digests are assistant-only.
4. **Same falsifier law**: every decision/law string literally traceable to digest text; ≤3 per field; same outer schema + `pool: "grok"`, model `account:zai-individual-coding-plan/GLM-5.3 (seat-local AH12 mine, no API spend)`.

## Numbers (instrument + moment named)

- **Threads processed:** 30 of 30 selected (selection instrument: `summary.json` enumeration 2026-09-30; 139 fresh-eligible remain unmined — sample, not exhaustion)
- **Rows appended:** 30 (index 123 → 153; all lines parse; 153 unique ids, no collisions)
- **Laws extracted this batch:** 74 `laws_or_debts` = **70 LAW: + 4 DEBT:** (every thread yielded ≥1; max 3 per field)
- **Confidence:** 26 high / 4 medium (medium = three PDF-digest siblings whose record ends on the trim notice with no DONE visible, + the BLUEPRINT lineage thread whose digest is assistant-only)
- **Running index total:** **380 laws_or_debts = 307 LAW + 73 DEBT** over 153 rows (recounted from the file with the `laws_or_debets` typo-key fallback; pre-V10 33 rows: 88; V10: 89; AC12: 73; AD5: 56; AH12: 74)
- **Spend:** $0.00

## Leaderboard

**"Receipts/locator before verdict" stays #1 and accelerates.** This batch adds **12 thread-births** (memlang design "from that code only... names real files", salon "actual stack, not a generic architecture lecture", Vast "every number has a URL", throughput "cited public benches" disclosure, SOTA witness "sourced, not recalled", boot dossier "grounded in this fleet's actual stall", systems review "cites real code, not the summary", audit "regression list from bytes, not memory", cross-exam "from those receipts, not from either seat's story" + "Reed-Solomon is not in the repo", both Socratic rounds "read as bytes", roundtable reading the three source docs first). Instrument note: on this tranche's keyword pattern (`locator|receipt|bytes, not|from disk|actual (stack|receipts|flaws|stall|machinery)|has a URL|sourced, not|read as bytes|from bytes|not from memory|cites real code`) the family reads **51/153** threads (AD5's wider-pattern read was 34/123); the hand-curated family moves 28/123 → 40/153 (+12). No-fabrication gains 4 births on the index-keyword instrument (`fabricat|invented|without inventing`: 18/153).

## Notable new laws banked

- "LAW: High consensus strength does NOT predict correctness — cross-exam is an independent witness, not agreement theater" (elder-vs-GLM hosting cross-exam)
- "LAW: Fact-check module claims against the repo — 'Reed-Solomon is not in the repo (GLM's [F] is false)'"
- "LAW: A green exit code is not acceptance — read the written bytes back against the contract" (council runner)
- "LAW: For 100 queens on one 24GB card the limiter is KV cache, not HTTP clients — cap the orchestrator at max-num-seqs"
- "LAW: One resident model is a VRAM law — a 19GB 'smarter' resident can starve the KV cache that fan-out lives on"
- "LAW: Doctrine already hurt the measured baseline (0.71 to 0.56) — score drain traces before swapping residents"
- "LAW: A named tweet may itself be a reply — find the real root conversation before listing replies"
- "LAW: 'If no replies exist, say none found' — the none verdict ships with the tool-result table"

## Notable specimens

- **The reply-count-without-body pair** (tid `01a0766e-5871…` + `01a07670-e1bf…`): the tweet showed Replies=1 yet no body came back from any probe; chased through parent thread, `in_reply_to`, and the author timeline; verdict "None found" delivered with the per-tool result table. Third member of the honest-zero family after the AC12 `{"seams":[]}` and AD5 empty-findings twins.
- **Id-typo recovery** (tid `01a07727-44e8…`): the ask named `2096608384795488652`, which failed (missing `conversation_id`); the seat named the thread's real conversation id `2096604548869533890` and completed the fetch — locator repair, not a shrug.
- **event_stream.py TOCTOU** (tid `01a04850-f58d…`): `last_event` then append with no lock, hashes computed over `"hash": null`, emit treated as commit — "the tape is not what happened".
- **READY-before-first-token** (tid `01a045d8-b55c…`): success predicate matched `health` inside `health-wait`.
- **New DEBT specimens:** 3 PDF siblings ending on the trim notice with no visible DONE (false-completion-adjacent), + the SELF distill folder whose source transcript is absent so the distill cannot be checked against its source.

## Method receipts

Scratch (selection script, digest builder, rows module, append script, digest corpus) lived in `%TEMP%\ah12_scratch\` and is deleted after this append; durable evidence is the 30 appended rows, each carrying `thread_id` → `grok_sessions/<cwd-enc>/<uuid>/chat_history.jsonl`.
