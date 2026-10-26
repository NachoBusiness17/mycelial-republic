# ball2 / attention-ledger: the attention market's trade ledger is wired and has settled its first trades

Lane: gala ball 2026-09-29, division B, attention-ledger. Date: 2026-09-29.
Start material: `watch/inbox/burn_reset_20260927/flash50/w4-03.md` + `w4-37.md` (both read in full this session).

## The owed work

w4-03 (2026-09-28) measured the market dead: `memory/attention_feedback.jsonl` ABSENT, zero trades ever, despite `POST /api/v1/attention-feedback` at `dashboard/rest.py:5242` and the full pricing desk in `mag/attention_ranker.py`. w4-37 named the failure theorems: T2 (contract drift: two vocabularies, good/bad vs the ranker's five signals, silently zeroed price discovery) and the missing ledger. Wave5 (commit dbe5f682c) fixed the vocabulary inside `mag/feedback.py` only; the REST surface still called `record_feedback` raw, nothing anywhere pinned a retried POST to one append, and the read path had no public name. This lane closed the remaining gap.

## What changed (all edits this session)

1. `mag/attention_ranker.py`
   - `_find_cast()` (:63): settle-once scan of the trade ledger by cast_id. Full-file scan on purpose; a bounded window would let a retry double-append once newer trades pushed the original row out (ledger is tiny: zero rows in 54 days).
   - `record_feedback()` (:87): new keyword-only `cast_id` idempotency key. With cast_id: a replay returns `{"ok": True, "duplicate": True, "event": <original>}` and appends nothing. Without: legacy semantics, every cast is a distinct trade. The row gains `cast_id` only when keyed, so historical row shape is unchanged for readers.
   - `read_feedback()` (:122): the public read path (the private `_feedback` logic, already consumed by `build_ranked_attention()`, now named for audits and any other consumer of cast history). `_feedback` kept as the name `build_ranked_attention` consumes so existing monkeypatch surfaces keep working.
2. `mag/feedback.py`
   - `normalize_signal()` (:60): ONE alias definition (thumbs spellings to the five-signal vocabulary), now used by `capture()` and imported by the dashboard handler, so no surface can resurrect the w4-37 Receipt 6 two-vocabulary drift.
3. `dashboard/rest.py`
   - `h_attention_feedback()` (:869): casts normalize through `normalize_signal` (a thumbs POST no longer 400s) and pass `cast_id` through, so a retried POST settles once. Unknown signals still 400 loudly.
4. `tests/test_attention_feedback_ledger.py` (new, 7 tests): zero-double-append, replay-wins-even-when-retry-disagrees, unkeyed cast = distinct trade, five-signal vocabulary in rows, real cast feeds the next `build_ranked_attention()` pass (+4 and feedback display, via the public read path), dashboard POST normalizes thumbs + replays idempotently through `rest.dispatch`, unknown signal 400s with zero rows.

## Finish-line proof (raw output: `watch/inbox/gala_20260925/ball-20260929/lanes/attention-ledger.check.txt`)

- pytest: `.venv\Scripts\python.exe -m pytest tests/test_attention_feedback_ledger.py tests/test_attention_feedback_contract.py tests/test_attention_ranker.py -v` → 18 passed (7 new + 8 wave5 contract + 3 ranker), exit 0.
- Ratchet: `.venv\Scripts\python.exe tools\violation_ratchet.py check --changed` → `RATCHET: PASS` (no unregistered debt), exit 0, NEW=0. (Its GROWTH lines name `mag/corpus_acquire.py` and `tools/stealth_driver.py`: pre-existing registered debt from sibling lanes landing concurrently on the shared tree, files this lane never touched.)
- LIVE POST against a real server instance on scratch port 8791 (started from this lane's edited code via `from dashboard.server import run; run(port=8791)`; the operator's live lab on :8765 was left untouched):
  - Before: `memory/attention_feedback.jsonl` ABSENT (w4-03's state, re-verified at lane start); feed: repo:handoff P0 84, four P1 74/66, roadmap P2 71, all `feedback: []`.
  - POST #1 (first trade ever): `{"item_id":"repo:handoff","signal":"useful","source":"ball-attention-ledger","cast_id":"ball-attention-ledger-20260929-01"}` → HTTP 200, row appended.
  - POST #2, same cast_id (the retried POST) → HTTP 200, `"duplicate": true`, original event returned, nothing appended.
  - POST #3: thumbs `"good"` on `roadmap:v5:xrpl_read_tools`, cast_id `-02` → HTTP 200, normalized to `useful` in the ledger.
  - Ledger after: exactly 2 rows (`ROW_COUNT=2`), both `attention_feedback.v1`, both five-signal vocabulary, cast_ids present.
  - Next build consumed the casts: repo:handoff 84 → 88 with `feedback: ["useful"]`; roadmap item 71 → 75 with `feedback: ["useful"]`; all other items byte-unchanged.

## The first trades, declared

Both casts are this lane's own honest signals: the P0 `repo:handoff` item is the operative context every ball lane ran on (uncommitted wave5 tree, no upstream), and the roadmap P2 gate was read while planning this work. They are replay-safe by cast_id and remain on the permanent ledger, which is the point: the market is now falsifiable.

## Honest limits

- The settle-once guarantee is check-then-append inside one process: the dashboard server is the operative writer and single-process appends are serialized by the handler thread; a cross-process race (CLI pipe + dashboard appending the same cast_id at the same instant) is not locked. The ledger's real volume (2 rows) makes this a registered residual, not a live risk; the named-mutex pattern from wave5 stealth-tools is the known fix if volume ever justifies it.
- `mag/feedback.capture()` (CLI pipe) does not pass cast_id: CLI gestures are intentional trades, idempotency keys are an HTTP-retry concern. The pipe's wave5 contract tests are untouched and green.
- The check transcript is a shared-tree snapshot: sibling lanes were landing changes during this window (ratchet scope moved 33 → 34 files between runs). Nothing in those diffs intersects the four files this lane edited.
- Not run: the full test suite (the ask named the finish-line checks, not a full burn; suite scale is the operator's pre-push call).

## Decision ledger

Closes the w4-03/w4-37 owed work "the market has a pricing desk and zero trades": the trade ledger now exists, has its first two settled trades, a retried POST can no longer double-append, thumbs casts can no longer be silently rejected at the dashboard surface, and the next ranking pass provably consumes real casts. The decision this changes: attention-market wiring moves from "rails untested, absence of trades uninformative" (w4-37 T2) to "trades settle once and reprice the feed," so future zero-trade states are honest apathy readings, not broken rails.
