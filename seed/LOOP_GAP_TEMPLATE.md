# LOOP GAP TEMPLATE (mag_loop_gap.v1)

A gap log with two ideas that make it earn its disk space: **dedupe hashes** (recurrence
counting for free) and a **bidirectional lifecycle reconciler** (catches waste, not just
absence).

## The record (one JSONL line per detected gap)

```json
{"schema": "mag_loop_gap.v1", "ts": "<ISO UTC>", "ts_unix": <float>,
 "name": "<gap name>", "detail": "<one bounded line>", "where": "<detector location>",
 "kind": "<missing_capability|lifecycle_gap|lifecycle_waste|missing_seat>",
 "dedupe": "<hash(name + where)>", "stack": "<which loop found it>"}
```

## The four kinds

| kind | direction | example (real row) |
|---|---|---|
| `missing_capability` | gap: needed, absent | test gap, unit fixture |
| `missing_seat` | gap: a seat that should exist | "browser seat not wired — allowlist only scaffold" |
| `lifecycle_gap` | "should be ON but is OFF" | `lifecycle_gap:lab` — service down |
| `lifecycle_waste` | "should be OFF but is STILL ON" — the direction most detectors lack | `lifecycle_waste:drainer` — loop burning tokens while idling |

Waste is the cost half of the same law: absence loses capability, waste loses money —
one reconciler (desired-vs-actual diff, fed by the lifecycle endpoint) emits both.

## The dedupe-hash rule

`dedupe = hash(name + where)`. Identical gaps collapse to one key; recurrence is then a
`grep -c`, not a prose memory:

| real key | recurrences (this session) |
|---|---|
| browser seat not wired (`9dbe58099056d6a9`) | **16** |
| drainer burning tokens (`c6106f660fed3962`) | recurring since 2026-08-06; 101 `lifecycle_waste` rows total |

Count distinct keys for the gap taxonomy; count rows per key for the burn rate.

## Receipt

- training/loop_gaps.jsonl (estate) — head read this session; `wc -l` → **298**;
  `grep -c lifecycle_waste` → 101; `grep -c 9dbe58099056d6a9` → 16 — all run this session.
  Example rows above are verbatim from the file.
