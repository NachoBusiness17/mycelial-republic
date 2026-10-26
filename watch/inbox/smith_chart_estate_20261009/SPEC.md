# SMITH CHART OF THE ESTATE - the Turing-castle water computer, instrumented - 2026-10-09

Operator order: "this is our turing castle water computer help me smutchart it
and not handwave." The disk smith charted one pipe. This spec charts the
castle. Every metaphor below maps to a NAMED instrument with a NUMBER - that
is the no-handwave contract.

## The water-computer mapping (metaphor -> organ -> measured by -> state)

| Water metaphor | Estate organ | Instrument | State |
|---|---|---|---|
| Reservoirs (storage tanks) | disk buckets (.zcode, ollama, HF, repo, docker vhdx, pagefile.sys file) | tools/disk_smith.py daily 08:50 + 15GB floor | LIVE |
| Pressure (head) | RAM commit + pagefile allocation vs usage | estate_smith PRESSURE block (psutil virtual_memory + swap; allocated-vs-used split is the balloon gauge) | v1 tonight |
| Pumps (doing work) | models + seats: ollama serve, python seats, node, docker | estate_smith COMPUTE block (per-exe CPU-seconds stock + RSS + proc count) | v1 tonight |
| Flow rate (liters/day) | tokens/day, events/day, ledger rows/day | estate_smith FLOW block (events + burn LEDGER rows last 24h) + hermes usage ledger | v1 tonight |
| Leakage (loss to ground) | exhaust: bytes written that are not durable work | estate_smith LOSS block (zcode_cache delta between smith rows = disk-flow; junk ratio from audit = loss class) | v1 tonight |
| Valves (flow control) | caps + retention + floors: per-call stdout cap, 7d retention, 15GB floor | LAW_PACK L1/L2 + smith alerts | law landed, code queued |
| Level sensors (alarms) | attention.md alerts + exit 1 tripwires | smith alerts + estate_smith alerts (ram avail < 8GiB, free < 15GB, pagefile file > 40GB) | v1 tonight |
| Resonance (standing wave health) | budget vs actual: GB/day expected vs smith delta; burn rate vs window | estate_smith RESONANCE block (rates from consecutive rows) | v1 tonight (rates land day 2+) |
| The castle walls (defense in depth) | gates: ratchet, citation lint, workflow gate, Mimosa, secret scan | pre-commit/pre-push surfaces (already live) | LIVE (external to chart; chart reads their pass counts later) |

## v1 instrument (tonight, receipt-space)

watch/inbox/smith_chart_estate_20261009/estate_smith.py - single process,
psutil + tiny file tails only, NO disk walks (the one-disk-process bound):
appends one JSON row to estate_smith.jsonl with the six blocks, prints a
compact panel + alerts. Deltas computed vs the prior row (rates need >= 2 rows).

## Promotion path (not handwaved, queued)

1. tools/estate_smith.py + tests (assert block shapes, alert thresholds,
   delta math on synthetic rows) - rides the post-P4 build queue with L2/L8.
2. MagEstateSmithDaily 09:05 (after the disk smith 08:50, one process at a
   time preserved by stagger).
3. RIB_STANDING_WAVE_BUDGET amendment: this panel is the rib's instrument
   surface (the wave's gauges, not just its budget).
4. FLOW upgrade: parse hermes usage.jsonl + REGISTRY.jsonl into per-lane
   token/day; COMPUTE upgrade: cpu-time DELTAS per seat across rows (true
   pump-hours); LOSS upgrade: durable-bytes (git diff stat) vs
   exhaust-bytes ratio per day.

## What the chart is FOR (the one sentence)

A water computer you cannot gauge is a flood waiting for a screenshot; this
panel makes every seat's pressure, flow, and leakage a number on a wall, so
the next storm shows up as a rising gauge months before it shows up as 6.1GB
free.
