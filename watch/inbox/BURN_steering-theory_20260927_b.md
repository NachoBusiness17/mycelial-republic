# BURN steering-theory 20260927 b: live instrument readout

## Verdict
green

## Evidence
- Bare run: `./.venv/Scripts/python.exe tools/drift.py` exits 0, prints nothing. drift.py is a pure organ, no CLI entrypoint; its own contract: "Pure computation. Reads nothing, writes nothing. Feed it two series and honesty comes back."
- Live firing on real repo bytes: 50 rows of memory/runs/gps_50/raw.jsonl sorted by ts, drift_check(metric=completion_tokens, referent=answer_chars) returned {"verdict": "DRIFTING", "corr_dm_dr": 0.1807, "deltas_used": 49, "note": "weak coupling: the metric may have decoupled from its referent"}. tokens-vs-latency_ms returned {"verdict": "DRIFTING", "corr_dm_dr": 0.4538, "deltas_used": 49}.
- Canon series state: `ls memory/runs/probe20/` is EMPTY, zero files. The pair referents do not exist as series. Exact missing input, per the meta row of watch/inbox/PROBE20_steering_v1.jsonl (min_points 5): pair A needs rows of schema ["cycle", "margin", "correct"], pair B needs ["cycle", "escalated", "total", "overturns"], landed by tools/probe20_run.py real mode.
- Demo smoke (probe20_run.py --demo, in memory only, no files written): demo1 returned "verdict": "ALIGNED", corr_dm_dr 1.0 over 5 deltas; demo2 raw drift_check said "verdict": "INVERTED" (corr -0.5748) and the runner overrode it: "noise floor: net |delta referent| 0.050 < 0.10 across window; one-flip VACUOUS escape blocked (BURN _c)"; demo3 returned "verdict": "VACUOUS", "referent_moved": false, the native kill standing.

## Steal or Vacuous
Green for the canon instrument pair adopted earlier today: drift.py + probe20_run.py verified live. The organ computed real corr(delta-M, delta-R) numbers from real bytes, and the runner's noise-floor guard fired exactly as its docstring pre-registered, closing the one-flip VACUOUS escape pass _c found. Honesty about the self-test: the two DRIFTING verdicts above are NOT steering findings. answer_chars is not a truth referent (both series measure answer size), and the 50-row sequence crosses 10 lanes, so weak delta coupling there is lane heterogeneity, not drift. OWED: the canon steering pairs (A confidence-margin-vs-correctness, B escalate-rate-vs-overturn-rate) still have zero real cycle rows; their referent series require probe20_run.py --live against a local llama-server, which is new data collection, out of scope for this read-only pass. Fleet law confirmed byte-deep: a rate metric answers "is it moving"; only corr(delta-M, delta-R) answers "is it moving north", and the fleet currently has a verified needle with no map rows under it.

## Bibliography
- tools/drift.py (read whole)
- watch/inbox/PROBE20_steering_v1.jsonl (tail 30)
- tools/probe20_run.py (head docstring plus its captured --demo output)
- memory/runs/gps_50/FOLD.json
- memory/runs/gps_50/raw.jsonl (all 50 rows, ts-sorted for the readout)
- Web search 2026-09-27, "online drift detection LLM agents metric referent alignment 2026": thin, no exact match found. Closest hit: ZeroCoder (arXiv, Apr 2026) naming "selector drift" in LLM code-gen pipelines; search snippet only, paper not opened, unverified per the no-fabrication law.
