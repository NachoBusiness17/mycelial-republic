---
name: flash-burn-institutional-meters-and-resolver-bound-20260927
description: B2-469 institutional cluster dated meters (LAW-13 operationalized
  as DATED_METERS.jsonl, NOBS=dated row or silence-voids-scoring) + B2-489
  resolver getaddrinfo deadline-bounded at 2s daemon thread (blackhole DNS can't
  hold doctor hostage)
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Two burn findings landed 2026-09-27 early AM:

**B2-469 institutional cluster dated meters**: LAW-13 (experiment-on-absence) operationalized as `tools/meter_patrol.py` — the daily census cron now appends one dated row per rubric class to `watch/inbox/DATED_METERS.jsonl`, each row either RECEIPT (boundary-true candidate pointer) or explicit NOBS (no observation, silence ≠ evidence of absence). Four frozen classes from the window 21/22 rubric. EBS/MOEX tokens case-sensitive with word boundaries (bars the "ebs inside website" substring disease). Falsifier: any post-2026-09-26 window-scoring citing "no receipt" for items 1-4 without naming DATED_METERS voids itself. Wired into the MagCensusPatrolDaily 08:30 cron.

**B2-489 resolver deadline bound**: `mag/doctor.py _host_resolves` now runs getaddrinfo on a named daemon thread joined at `_RESOLVE_TIMEOUT_S = 2.0`. Blackholed DNS can no longer stall the examine() report. Falsifier reproduced (30s sleeper → bounded to 2s class), 20 pins green. Live trap run 4.12s with DOWN none(locality) intact. Companion: B2-490 swept all other base_url_env overrides for the same seat-scope trap (OLLAMA_HOST docker-name on host = the live trap, SAELIS_BASE_URL dormant silent, VAST_OPENAI_BASE_URL non-11434 port reads REMOTE-UNVERIFIED).

Related: [[flash-lane-burn-session-20260927]], [[experiment-on-absence-law]]
