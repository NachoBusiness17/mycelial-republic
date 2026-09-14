# WATCHER FALSIFIER COUNTER v0 — receipt (2026-09-05, finished in-session)

**Provenance:** built by the A2 background worker (spawned 03:54Z per RAMP 2), which
DIED at 04:20Z on "user concurrency limit exceeded" (the collision that produced
correction law 16) before filing its receipt. The counter was complete and working —
the zcode seat verified and filed it in-session (one builds, one verifies — here one
also finishes what the collision killed).

**What exists:**
- `mag/falsifier_counter.py` — read-only pass over breadcrumbs + activity stores;
  classifies each breadcrumb's lifecycle {closed | seen | open | expired}, emits
  weekly close rate + median time-to-action + per-lane breakdown; appends typed
  rows to `memory/falsifier/close_rate.jsonl` (schema falsifier.close.v1, dedup,
  append-only). $0, no model calls, silent-fail per row.
- Verified run (09-05 ~04:5xZ): `python mag/falsifier_counter.py` →
  crumbs=3 activity_rows=47,325 → closed=0 seen=3 expired=0,
  close_rate(week)=0.0, lanes day_work 0/1, economist 0/1, night 0/1.
  An earlier pass (04:05Z, pre-death) recorded one day_work breadcrumb closed at
  96 min time-to-action via CONVO-match.

**Falsifier baseline (the card's promise, now instrumented):** the stigmergy card
watch/DEEP_SELF_STEAL_STIGMERGY_20260905.md committed to "breadcrumb→action close
rate over a week." First measurement: **0/3 closed this pass (one 96-min close seen
in an earlier pass — matcher strictness between passes is itself a v0.1 item).**
The week-long measurement is now live; the number to beat is whatever the week shows.

**Tri-state:** counter runs on the live store = Supported (verified twice). Close-rate
matcher strictness consistency across passes = **Unproven → Supported (09-05 ~05:1xZ
in-session: `--selftest` found built by the deceased worker and verified — 10/10 PASS
incl. known-rate 4/6=0.6667, a mismatch case where the counter REFUSES a lying input
("expired despite claimed ACTED"), window discipline, ledger dedup across 3 passes,
append-only, seen→closed upgrade)**. Week-long close-rate trend = pending by design.

**Falsifier for the counter itself: SHIPPED AND VERIFIED.** `python
mag/falsifier_counter.py --selftest` — synthetic temp store with known rates; the
counter must (and does) print the known numbers and disagree with a fabricated
mismatch case. A counter that cannot disagree with its input is not a counter.

**Re-run:** `python mag/falsifier_counter.py`
