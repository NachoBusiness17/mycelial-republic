# Z20 — Free-lane check: did the FL briefs move? (2026-09-30 ~05:15 EDT)

Owner: Z20 hydrology seat. Question: brief_reaper queued 10 briefs (FL-1..FL-10) — did the stealth driver pick them up?

## 1. Queue: state/fuel/stealth_work_queue.jsonl

All 10 FL rows present, `status: queued`, `queued_ts 2026-09-30T00:19:10Z`, `source: brief_reaper`, `tier: free`. **Zero status changes** — no claimed, no sensed, no failed, no done_ts. Queue totals: 25 queued / 6 sensed / 2 expired.

## 2. Outputs: watch/inbox

**No FL outputs.** No `FL*` files in `watch/inbox/` root, none in the brief's designated landing dir `watch/inbox/game_platform_basecamp_20260929/` (last writes there: W1/W2/W3 receipts, Sep 29 evening). Nothing to digest.

## 3. Driver: alive but blocked behind one row

`state/fuel/stealth_driver.jsonl` heartbeat is current (cycle 153 at 2026-09-30T09:05Z = 05:05 EDT, ~6 min/cycle). Not a wake problem — a **head-of-line block**:

- `tools/stealth_driver.py:410 _next_work` returns the first row without `done_ts` (regardless of status). Head = `w-water-display` (sensed, no done_ts).
- The hourly verify topic (`FUNDED DONE GATE`) has returned **"verdict OWED, row stays open"** four hours straight (04:52, 05:57, 06:59, 08:02Z) — verifier found a real factual error (Taberlet et al. is 2018, banked answer said 2019) plus confirmed OWED items, so `done_ts` is never written.
- Work topic therefore re-senses the same head row every cycle across lanes (`w-water-display_hermes.md`, `_openrouter1/2/3.md`, 04:42-04:59 EDT today in `watch/inbox/burn_reset_20260927/work/`). Prior drain rate when verify says DONE was ~1 row per 1-4 h (lib-belady 15:18Z → w-schmidhuber done 01:49Z). w-water-display has been head for 7+ h.
- Starved behind it: 5 queued `w-*`, `m7`+`m008..m016`, then FL-1..FL-10 at the tail. At the healthy drain rate the FLs are ~17 rows / roughly 1-2 days away; at the current blocked rate, never.
- Lane noise en route: `inkling-small:free` 403s, `llm7/gpt-4o-mini` 400s — rotation routes around them.

## Wake state (for the record)

- `state/stealth_driver.off` does NOT exist → driver not stopped. Stop word = create that file; start = delete it and relaunch via the boot-lane line or `pythonw scripts/run_stealth_driver.py` (single-instance mutex; a second instance refuses, exit 2).
- The needed fix is not a wake: unblock the head — operator either closes `w-water-display` (accept the sensed answer with the 2018 correction noted) or patches `_next_work`/verify to advance past a row after N OWED verdicts. Operator call, not mine.

## Verdict

Driver running, rotation live, reaper landed, **FL-1..FL-10 untouched** — starved behind the w-water-display verify deadlock. Nothing sensed, nothing banked.
