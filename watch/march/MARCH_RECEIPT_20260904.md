# MARCH RECEIPT — 657 signals, one pass, 100% clean (2026-09-04 ~02:00Z)

## THE NUMBERS
- **657/657 processed, 0 errors, 100% ok-rate at every tranche** (8→16→32→50-flight, gates widened clean each time).
- **654/657 complete-format** (99.5% — three partials).
- **Output density: mean 85 tok/req, p95 worst 181** (measured, not capped — v1's 160-cap forced uniform truncation and was caught+fixed in-run).
- **Cost: ~$0.09** out-of-window on flash promo rates. In the 23:00–09:00 window: $0.00.
- Wall time: minutes. The legions map called this backlog "one evening of food" — it was one coffee.

## THE VERDICT DISTRIBUTION (the swarm's ruling on the whole explore backlog)
- **376 KEEP** (57%) — invariants worth percolating.
- **142 ACTION** (22%) — concrete buildable signals. Samples: phantom file-edit claims (agents claiming writes with no mutating tool — the Desk class), content-addressed BLAKE3 indirection, sparse-Merkle proof formats, swarm-health stall detection (handoffs with zero progress), steganographic anomaly detection.
- **139 DISCARD** (21%) — noise, named as noise.

## DEBUG-ON-THE-WAY LEDGER (3 integration bugs, all caught by the halt gate at tranche-8 width, seconds each)
1. record_call takes lane/model/subsystem positionally (builder's spec, my call shape wrong).
2. record_call returns (status, result) tuple — unpack, don't index.
3. THE BIG ONE: max_tokens=160 + 5.3-flash forced thinking = reasoning ate the whole budget, content empty (653/657 empty responses in v1). The fleet's own receipts held the medicine: §4 "max_tokens ≥1536" + §10 "effort low is the floor." Applied → v2 clean with mean 85 real density.

## WHAT THIS RECEIPT PROVES
- 50-flight sustained: 100% ok across 12 consecutive 50-wide tranches (~600 calls at full width).
- The Leg-1 organs WORK: 657 claims, zero double-claims, clean releases (first real workload).
- The flight recorder captured every call by subsystem="march" — the density table is computable, per-item, forever.
- The explore backlog is TRIAGED: 142 ACTION-class signals now exist as a ranked build queue (P1 receipt: DONE).
