# THE STANDING WAVE PROTOCOL — self-stolen spec (2026-09-18)

*Distilled from the union fullsend drive's own receipts (143 attempts, 88.8% ok,
16 lanes, $0) and the wave lineage (wave_20260916 → 24/7 standing drive →
self-tending cron automation-b499da5b). This is the method, extracted so any
fleet (or seat) can run one.*

## THE PROTOCOL (seven laws, each paid for by an incident)

1. **SELF-TENDING INTAKE** — the queue refuels itself: operator/any-window
   wants land in WANTS.md; the tender converts wants → queue items when
   remaining < threshold (12); then un-receipted board tasks as digs; then
   standing veins. Nobody hand-feeds the wave. *(Incident that taught it: the
   dribble failure — 155K used of a 6T window because nothing self-fed.)*
2. **LEAN FIRES** — every fire reads state files only, does one item, replies
   one line, inherits NO conversation. *(Incident: a 5.7M-token / 22-fire
   cron bleed. Context is heat; residual on disk is truth.)*
3. **LANE FALLBACK, NOT QUEUE DEATH** — attempt-2 swaps lanes (16 lanes seen
   in receipts: or-union-alpha ×2 accounts, groq family ×6 keys, zai-lite,
   mistral, nim, cohere, gemini, deepseek, together). A dead window is a
   lane-swap. *(Incident: ox-alpha 404 — its death revealed it was glm-5.3-flash
   all along; the lane map updated, the queue lived.)*
4. **RUN-LOCK + SELF-CLEARING STALENESS** — concurrent fires no-op; stale
   locks self-clear (15 min / 900s). Waves overlap safely.
5. **RECEIPT-PER-ATTEMPT** — every attempt appends a raw.jsonl row (ok, lane,
   model, chars, usage, latency, id, slug). Attempts without receipts never
   happened; the 88.8% ok-rate is computable BECAUSE failures also file.
6. **METERED GENEROSITY** — law-15 pacing on metered seats (lite_guard
   check/record before/after every zai-lite call); free lanes absorb burst.
   The wave's whole 143-attempt run cost ~173K tokens, mostly free lanes.
7. **PROMOTIONS ARE BYTE-CHECK-ONLY** — the wave digs and drafts; promotion to
   canonical stays a human gate (constitution law: mining never auto-merges).
   The wave proposes; the operator disposes.

## THE SHAPE (what a standing wave IS)

A standing wave is **a queue + a tender + a receipt ledger + a lane ladder**,
fired on a cron, reading state — never chat. Everything else (salons, radars,
censuses) are wave-shaped consumers of the same four organs.

## MEASURED (receipts, not memory)

- 143 attempts / 127 ok / 16 lanes / ~173K tokens / 120 unique ids drained of
  126 queued (UF-01..126 era) — losses concentrated in dead-window lanes,
  retried on fallback per law 3.
- The wave's own audit trail: `watch/inbox/union_fullsend_20260917/raw.jsonl`,
  `queue.jsonl` (digest-versioned, hash-registered in index_events).
