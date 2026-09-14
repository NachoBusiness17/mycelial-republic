# WAVE_DRIVER_SPEC — the orchestrator loop, self-stolen (2026-09-11)

Operator order: "this needs to be a loop... some sort of orchestrator intelligently directing the lanes, keeping them churning and genetically evolving, feeding that evolution to the standing wave. Self steal."

THE POINT:
- Every piece of this orchestrator already exists in the fleet or came back verified in today's steal wave. What's missing is only the WIRING: one in-cage driver that ticks the loop, and one shared steering file so the seats talk to each other without the operator's fingers.
- The driver = lane_runner's daemon pattern + the night-shift cron slots + lane H's recipe + lane C's router + lane F's liveness. No new host runtime (law 13/11 cited below). The "next" keystroke becomes an inbox row; the tick is the keystroke.
- The displays get their feeder: each tick writes overseer.json + burn-board data, so the static dashboard, live.html, and the native Subagents panel all show the same churn the operator is already watching.

## THE LOOP (one tick, five beats)

1. **LOOK** — read state: trail.jsonl ages per lane · failure_kb top signature (the janitor's old sight, restored) · lane census + spawn counts · auth_tracks quota/clamp state · `watch/steers.jsonl` (operator GOs + the other seat's rows). Stateless + usage available = tight loop (law 9).
2. **JUDGE** — the router: stall-check (STALLED_HOURS=2.0, lane_runner's own) · halt-not-hammer (2 consecutive lane failures → escalate ONE operator-inbox row → stop that lane; lane H's mandatory antidote to the Replit/OpenClaw incident class) · quota gate (law 15 reserve-patience + 1400 clamp; pre-call cost estimate per lane G) · spawn caps (MAX_SPAWN_DEPTH=3, concurrent ≤8, child never exceeds parent permissions — lane C's Claude-Code-verified trio).
3. **ACT** — exactly one of: SPAWN (2-per-fold, the genetics line) · RESUME (`--resume <session_id>` checkpoint chain; parity test on a Lite lane first) · NUUDGE (drop one gated task row into `queue/lanes/<lane>/inbox.jsonl` — this IS the "next" keystroke) · FOLD (extract genetics, amend the next generation's specs) · REPORT (board write + morning-report row).
4. **RECORD** — every tick appends its own trail row + WAVE_LEDGER + overseer.json. **The driver meters the meters and carries its OWN heartbeat with a TTL** — its death must be loud (lane F's lease pattern; the 3.4-day silent heartbeat never recurs).
5. **YIELD** — sleep. Ticks fire from the EXISTING night-shift cron slots (23:00/02:00/05:00, census item 3, never yet fired — the sanctioned host) plus an on-fold immediate tick. In-cage, docker-exec only, no window, no TTY.

## GENETICS (feeding the standing wave)
On each FOLD: extract what changed — amendments that fixed failures (cycle-1's 0/6 → landing row is the proof pattern), lane timings, which masks produced signal (zero-shared-context convergence = keep). Write them into the next generation's prompts via steer-file injection — the janitor's old remediation trick (steer_agent.md injection), restored with a live lane behind it. Evolution flows: lanes → fold → genetics → next spawn. The standing wave cycle (6+1 tender) is the chassis; the driver is its heartbeat.

## THE SEAT LOOP (both seats, file-borne)
`watch/steers.jsonl` is the shared steering surface — proven by STEER-MESH-001/002 (cross-window takes landed via file drop). The protocol, now standing:
- Each seat APPENDS claims / findings / answers / GO-requests as rows (`[task] [directive] [target] [ttl]`).
- Each seat READS the other's rows on BOOT, on FOLD, and on every driver tick.
- The operator's twice-pasted boot receipt becomes a steers row the loop picks up automatically — the paste was the loop failing; the file is the loop holding.
- Anti-collision: CLAIM-before-work rows (`[directive: claim]`), one writer per row, answers reference the row id.

## DISPLAYS (watching the churn)
Tick writes → `dashboard/static/overseer.json` (overseer strip on live.html) + burn-board data → the operator watches the native Subagents panel, live.html, or the burn board — same truth, three surfaces. The displays were built as attempts to see the system; this is the feeder they were waiting for.

## LAWS CITED (law 13 teeth)
- docker-not-desktop / in-cage only: driver runs as a lane under lane_runner's cadence + container restart policy — NO second supervisor, NO host scheduled task (laws 11, 16; fireball era).
- one-sense-one-instance: ONE driver; lanes are stateless children.
- loopback only; every dispatch receipted to the chain (files + chain over processes).

## BUILD ORDER (from the verified pieces)
1. `mag/wave_driver.py` — tick beats 1-5, reusing lane_runner primitives (~150 lines; the recipe is lane H's).
2. Steer-row reader/writer into the driver's LOOK/RECORD (the seat loop).
3. Heartbeat-with-TTL + loud-death row into failure_kb (lane F).
4. Halt-not-hammer + spawn caps constants (lane C).
5. One Lite-lane parity test of `--resume` before the first unattended night.
6. First armed night = the night-shift slots, max-ticks-per-night cap, morning report as the receipt.

Receipts: mag/lane_runner.py (daemon, STALLED_HOURS, gated inbox, LAW-058) · watch/CRON_CENSUS_REINTERPRET_20260911.md (night shift = driver host) · watch/steers.jsonl (mesh format) · STEAL_WAVE_FOLD_20260911.md lanes A/C/D/F/H · watch/inbox/SELF_STEAL_RACTOR_PANEL_20260911.md (the gopher-ractor metamorphosis = this driver's soul, Dec-2025 canon compiled).
