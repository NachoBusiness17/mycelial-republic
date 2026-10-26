# BURN steering-theory 2026-09-26

## Verdict
steal

## Evidence
- tools/drift.py line 62: "referent_moved = any(d != 0 for d in dr)": the one-flip escape surface, now closed by the runner.
- tools/drift.py line 83: "a rate metric answers 'is it moving'; only corr(delta-M, delta-R) answers 'is it moving north'". Import verified live: runner logs "drift import from tools/drift.py: True"; the inline fallback exists but was not needed.
- Demo output (actual, 2026-09-26). demo2-one-flip-escape, referent correct/20 = 14,14,15,15,15 (net delta 0.05): drift.py raw verdict "INVERTED", corr -0.5748, "stop trusting the metric"; runner override "INSUFFICIENT", "noise floor: net |delta referent| 0.050 < 0.10 across window; one-flip VACUOUS escape blocked (BURN _c)". drift.py alone would have filed a kill verdict off one quantization flip.
- demo1-aligned: raw and enforced "ALIGNED", corr 1.0, net 0.35. demo3-true-vacuous: raw and enforced "VACUOUS", "flat referent, native kill stands".
- Defect caught by the demo: binary float subtraction renders 0.6-0.5 as 0.09999999999999998, so a per-delta max floor wrongly insulated a genuine 0.1 move; fixed to net window movement with a 1e-9 epsilon guard.
- Freshness: one search (entropy-based confidence routing, one year recency): nothing dated late September 2026. Nearest: UR-CoT uncertainty-routed reasoning (Feb 2026) and a Medium "What Is Jev?" piece using top-two margin or entropy as confidence. Snippet level only, no resolvable article URLs returned. Field quiet a third consecutive burn.

## Steal or Vacuous
Steal, executed. (a) tools/probe20_run.py (stdlib): append-only series at memory/runs/probe20/<lane>_<pair>_series.jsonl, drift_check verdict at >= 5 rows, cycle-ordering and probe-version-hash gates both verified (exit 2). (b) watch/inbox/PROBE20_steering_v1.jsonl seeded via the runner's --seed: 20 labeled TRUE/FALSE tasks, pair A/B registry rows carrying the pass-b fields, sha256 bfce1f28dae4c80f5f18a3eba04221270169d913ffad73e0ae776af984edc3e5 over the task lines, recomputed on every load. (c) Pair B denominator law enforced at append: total < 20 or escalated < 5 prints "POINT NOT FILED", exit 1, no row. (d) Scratch-lane end-to-end: 5 appends returned ALIGNED corr 1.0; scratch rows deleted after verification, so no synthetic rows sit under any lane name. Boundary: demo output is plumbing proof only; no lane verdict exists until a live gemma4 logprob client feeds real margins into the series.

## Falsifier
Unchanged from _c, now executable: per lane (gemma:2b, gemma4), both pairs, >= 4 cycles via repeated invocations. Kill: both pairs on both lanes return only VACUOUS, DRIFTING, or INVERTED and the confidence-as-drift-pair build is demoted VACUOUS and stops. Any ALIGNED keeps it alive. Runner INSUFFICIENT now also covers the one-flip escape (re-instrument, not filed); on pair A VACUOUS or repeated noise-floor INSUFFICIENT, re-version the probe immediately and log the refresh.

## Bibliography
- watch/inbox/BURN_steering-theory_20260925.md, _b, _c (repo, read 2026-09-26)
- tools/drift.py (repo, read 2026-09-26)
- memory/runs/gps_50/FOLD.json (repo, read 2026-09-26)
- tools/probe20_run.py, watch/inbox/PROBE20_steering_v1.jsonl (created and executed 2026-09-26)
- Web search 2026-09-26: emergentmind.com UR-CoT, medium.com Jev piece, sf.aitinkerers.org Cactus hackathon page. Snippet level only, unread beyond snippets, uncited above.

Owed, never synthesized: UR-CoT full text; the Jev/System One article URL (search returned domain roots only).
