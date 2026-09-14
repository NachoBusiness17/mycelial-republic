# G5-1 — NYQUIST FALSIFIER (mickey, spawned from G4-6's NEXT)

Date: 2026-09-10. Data: `logs/kpi.jsonl` tail — last 80MB = 2,685 rows, 2026-09-07T21:38Z → 2026-09-10T20:51Z (71.2h), all `source=summarize`, schema `mag_records_kpi.v1`.

## THE POINT

The wave protocol sanctions 18-25s idle between waves ("the wave holds"). That idle is a sampler of fleet state. Nyquist: a sampler only reconstructs change up to half its own rate. If fleet state flips faster than one transition per ~43s, the heartbeat misses transitions. Does it?

## THE MATH

- **Sampling rate (heartbeat):** 18-25s interval → fs = 2.4-3.3 samples/min (center ~2.8/min).
- **Nyquist ceiling:** recoverable change frequency = fs/2 = **1.2-1.67 changes/min** — anything flipping faster than once per 36-50s can alias between samples.
- **Measured fleet state-change rate** (state vector = n_sessions, n_complete, n_leaves, tip_root; a change = tuple moved between consecutive rows):
  - Sustained: 161 changes / 4,272 min = **0.038 changes/min** (one transition per ~26 min).
  - Peak burst: **3 changes in one rolling 60s window** (2026-09-07 22:58Z, night-wave hours) — the only minute in 71h above 1/min.
  - Longest quiet stretch: 27,893s (7.7h) with zero state change.

## VERDICT: PASSES

- Requirement: fs ≥ 2 × f_max. Sustained f_max = 0.038/min → minimum sampling = once per 13.2 min. The heartbeat samples **~37x denser than required** (margin 32-44x across the 18-25s band).
- Flagged edge: during burst minutes (>1.4 changes/min — observed once in 71h), fs < 2×f_max and intermediate transitions alias; the heartbeat sees before/after, not between. Terminal state still lands — this is a discrete state machine and sampling continues — only trajectory is lost, and trajectory is what the verkle chain and kpi.jsonl itself carry.
- **Tripwire for the falsifier:** 3+ state changes in two consecutive minutes = bursts gone sustained = tighten heartbeat to ≤10s. Until that fires, the wave holds, legally.

## SIDE FINDING

The ledger is a worse sampler than the heartbeat: median row gap 1.4s but mean 95.5s and max 27,887s — writes arrive in tight bursts with up to 7.7h dark gaps. Anything reading kpi.jsonl as a live feed inherits those gaps. The heartbeat is not the bottleneck; the summarize writer's cadence is.
