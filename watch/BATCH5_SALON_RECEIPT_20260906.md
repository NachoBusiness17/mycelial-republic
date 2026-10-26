# BATCH5 SALON RECEIPT — 2026-09-06 (~01:30–02:00Z)

Operator orders executed: (1) 24h dig — orphans + unwired + boot-clean; (2) drive every live window via mechanisms; (3) burn down the untouched quota; (4) 5-wide batches, 4 workers × 4 sub-items, 10-step salon over the mag blackboard; (5) ramp +5 toward 30–50, ceiling 50, gophers, see what breaks; (6) self-steal all swarm research; (7) vision agents watching so we can steer; (8) dogfood rare organs for data.

## The machine that ran

14 subagents fired from one seat in 3 waves + salon, all coordinated over the mag blackboard (seq 109–150), every bash step sealed to the trajectory stream (38→~250 steps today), every receipt grounded at file level before verdicts applied. Worker deaths: 1 (R5, provider 1210 image-parse — autopsied by v1, routed around, no work lost).

| Wave | Width | Outcome |
|---|---|---|
| 1 (w1–w4) | 4 | all done clean |
| 2 (r1–r5) | +5 → 9 | 4 done, R5 died on vision (1210) |
| 3 (s1–s5) | +5 → 11 live peak | all done clean |
| 3b (v1, r5b) | re-fire | both done |

Measured cost: ~14.1M subagent tokens / ~185 tool calls / workers 4–12.6 min each. Billed ≈ 1.5–2M (96% cache-read share). At 6 waves/day → ~40–100M billed to Sep 20 (inside pool; meter model reconciles to vendor at 0.5%).

## What the dig found (all tri-state, evidence in cards)

- **51/65 sessions orphaned** (no chain knots in 24h). S3 resolved why: the sanctioned backfill (`backfill-sessions`, mag/records.py) indexes the grok stream only — ZERO `sess_` ids in its 116 dry-run holes. Fix = ~100-line adapter, spec in watch/KNOT_BRIDGE_20260906.md. Chain untouched tonight.
- **271/280 recent cards undisposed** → S1 dispositioned 40 (14→54 rows, 0 unclear), pool 275→238, pheromone marks the resume point (INTAKE_ACADEMIA_).
- **Unwired surfaces**: 24 raw orphans → W2 wired 10, S2 wired 8 more incl. maze_arena (nav.js 40→59 links, 0 dead, node-syntax-checked, backups nav.js.bak-batch5*). Leftovers are variants/internal. S2 also fixed game/steal_tools data-JS 404s.
- **Boot was fat and stale**: state/CURRENT.md frozen since Aug 9 (REFRESHED), INBOX done-but-sitting (ARCHIVED), MEMORY.md 521 lines/156.5KB with 377 over-budget lines (TRIMMED to 80.7KB, 0 violations, topic files untouched, backups *.pre_trim_20260906.bak). **mag/boot_check.py is the new clean-boot organ** — one command, 8 probes, verified live.
- **Watcher death explained**: integral Mag lab (pid 9608) exited 22:51Z; in-cage supervisor wedged by ghost-pid adoption from a stale state file, so the cage never took over the heartbeat. NOT the sanctioned watchdog; Docker never died. Re-arm = `docker compose restart mag` (OPERATOR HANDS — flagged, not fired). Side casualty: mag-ollama Exited(255) ~26h, uninvestigated.
- **Windows driven**: R2 censused all 9 sidebar windows from the db and filed drive rows (WINDOW_DRIVE_20260906.md + room row). Bard + Elder live and healthy; Recap stuck in X-oauth attempt-12 loop (parked per drive row); Builder/Android idle 13h (sidebar age = window-open age, not activity). The room shows the mesh responding: B1+B2+B3 landed same-turn on operator GO at 01:40Z.

## The ramp doctrine (watch/RAMP_DOCTRINE_20260906.md)

- **50-concurrent is now MEASURED, not just operator-stated**: 09-04 probe — c=80 → exactly 50 succeed, instant 1302s, flat latency below. Per key. Our knob: `MODEL_CONCURRENCY["max-flash-5x"]` (mag/concurrency_gate.py:56, currently 5, lease-file slots).
- Ladder 4→9→…→49→50 armed; breakage = 1302/1305 storm >10%, worker death >20%, p50 >2×1.7s; two-strike = step down one rung and file. Tonight peaked at 11 concurrent: zero 1302s, zero throttle — ceiling not approached.
- **Gophers: refused-by-absence** — subagents have no Agent tool; width is a salon-side dial. Parent keeps all writes (DELEG-POLICY shape).
- **Economics corrected**: 24h = 457.5M raw but only ~19.4M billed (96.2% cache reads are quota-free); we run at ~12.5M billed/day vs the 40M/day pool-drain pace (~29%); width 25 is the first rung crossing 40M/day at every bound. Weekly credits 3,579/10,000 (35.8%) at last read — fresh meter paste will upgrade to Supported. Clamp correction: 1,228/day live DISPUTES memory's 1,400/day.

## Vision watch (operator: "vision agents watching so we can steer")

- R5's death autopsied: board PNG is valid; the vision-exp parser rejects PNG-as-sent, JPEG re-encode passes; **the mag vision MCP executes in-cage (/app) — host paths fail before any provider call**. Organ verified working after fix (watch/VISION_WATCH_20260906.md).
- Standing eye = `python -m mag.swarm_snapshot` ($0 local qwen eye, ~60s) — banked run 20260906T014838Z with digest + 3 steering signals; eye hallucinated one number, digest anchors numbers to files (code owns numbers, eye owns patterns).
- Adoption path for 24/7 watching = night-shift protocol amendment (23/2/5 already armed) — operator word gates it (law 13: cite laws before arming runtimes).

## Rare-organ dogfood (honest)

- Alive + useful: overseer, topic_index (705 cards/3,819 topics), read_receipts (603 swept), seal (verified:true; .ots missing on disk = defect filed), grounding_wave (GROUND posted), swarm_snapshot + local eye.
- Stamp-only: scan_probe/scan_grid ($0 tamper-stamps for ledgers). **Broken ingestion**: scan_measure + mean_field (2-strike bails, inputs preserved) — repair before next use. Research route: async, nothing public on our 50-limit — it's first-party publishable measurement.

## Queue deltas

CLOSED: grok canon harvest read/score (S5: 6/6 SUPPORTED, 215/215 replies cited, doctrine 4/1/1, verdict CLOSE; one handoff = fxtwitter second door over replies before falsifier use). OPENED: knot adapter build (~1-2h, $0), vision PNG→JPEG patch in swarm_snapshot static mirror, scan_measure/mean_field ingestion repair, disposition sweep batch B (238 remaining), wave 4 of the ladder (+5 → 16).

## Falsifier (48h, from BURN_DOWN_PLAN_20260906.md)

Billed >3M/day AND credits <50% at 6PM = throttle to 4 waves; credits >50% at day-end 2 days = cadence doubles; zero waves in 48h = the plan is vapor, delete it.

*Salon: 10 steps, all on the blackboard + these files. Everything above is grounded against bytes on disk; nothing is claimed from memory of a receipt.*
