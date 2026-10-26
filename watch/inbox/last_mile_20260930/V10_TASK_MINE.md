# V10_TASK_MINE — grok pool oral-law mine, seat-local (no Nous spend)

**Date:** 2026-09-29 · **Seat:** GLM-5.3 via `account:zai-individual-coding-plan` (the correction lane: glm mining glm, zero API spend, `cost_usd: 0.0` on every row)
**Files owned:** `watch/inbox/last_mile_20260930/V10_TASK_MINE.md` (this receipt) + 30 new rows appended to `watch/inbox/operator_model/ORAL_LAW_INDEX.jsonl` (33 → 63 rows). No commit.

## What was done

1. **Pool enumerated.** `corpus/oral_history/seat_pools/grok_sessions/` holds 852 sessions with `summary.json` (1,065 uuid dirs, 852 with readable summaries). The top-level `session_index.jsonl` lists only the 14 cwd-level grok entries (`pool: grok`), so per-thread names were taken from each session's `summary.json` (`generated_title` + `info.id` + `updated_at`).
2. **30 diverse threads picked.** Selection: unique titles, `num_chat_messages >= 8`, cwd-group caps (16 max from the repo root pool, 6 max per `memory/runs/*` pool) so the spread covers repo-root engineering sessions, the X-harvest runs, art puzzles, spore test, game night, and `C:\Users\foste`. Zero `thread_id` overlap with the pre-existing 33 rows (asserted before append).
3. **Digests built per thread** from each `chat_history.jsonl`: user text extracted from `<user_query>` tags; assistant plain-string messages (first + last 4, clipped); user queries capped at 12 × 600 chars. Total digest corpus ~84 KB, read in full by the seat.
4. **Extraction under the falsifier law.** Each row: `{thread_name, decisions (≤3), laws_or_debts (≤3 LAW:/DEBT:), confidence}` — only claims literally present in the digest text; no inference beyond it. Same outer schema as the existing 33 rows (`thread_id`, `thread_name`, `ts`, `extracted`, `model`, `cost_usd`), plus a `pool: "grok"` marker.

## Numbers (instrument + moment named)

- **Threads processed:** 30 of 30 selected (selection instrument: `summary.json` enumeration 2026-09-29; pool holds 852 — this is a sample, not exhaustion)
- **Rows appended:** 30 (index: 33 → 63; all lines parse as JSON; no id collisions)
- **Laws extracted:** 89 `laws_or_debts` items = **60 LAW: + 29 DEBT:** (every thread yielded ≥2; max 3 per field enforced)
- **Confidence:** 26 high / 4 medium (medium = thin digests: tangents inventory, PDF digest word-cap session, engagement survey, D&D module)
- **Spend:** $0.00 — seat-local compute only, per the driving-ladder correction

## Top new law by weight

**"LAW: No fabrication — record walls per item and continue"** — carried by **7 of 30 threads** (reply-tree harvests, bookmark harvest, 2025 canon passes, Rashomon receipts, ROASTS haul): when a source door dies or a cap is hit, record the wall per item and keep going; never invent the missing rows. Genuinely new: the pre-existing 33 rows had **zero** `fabricat*` hits. Runner-up (also 7 threads): "audit from bytes/files, not doctrine or reports."

## Notable laws banked

- "Name the constraint, fix the check, keep the guardrail honest — don't delete the gate" (quota death was Mag's dirty counter, not vendor spend)
- "A green check on an empty plate is not done — `output {}` marked `ok` is false completion"
- "State lives in files and chains; processes are cattle"
- "LangGraph 'replay' re-calls the LLM — that is not a RIB"
- "Day coverage is presence, not post-exhaustion — a day that returned 10 still has more"
- "If it's a row on the surface list, it exists — don't build a twin"

## Method receipts

Scratch artifacts (selection script, digest builder, append script, digest corpus) were created at repo root during the run and **removed after the append** per the only-the-deliverable habit. The durable evidence is the 30 appended rows themselves (each carries its `thread_id` → `grok_sessions/<cwd-enc>/<uuid>/chat_history.jsonl`).
