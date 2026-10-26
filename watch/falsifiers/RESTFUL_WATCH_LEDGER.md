# LAW-CANDIDATE 059 FALSIFIER LEDGER — THE RESTFUL WATCH (opened 2026-09-05)

Instrument for: `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md` (canonical card).
Window: 2026-09-05 through 2026-09-11 (7 days). Window closes end-of-day 2026-09-11.

## APPEND CONVENTION (read before writing)
- **Append-only.** Any seat appends a row the moment it catches something, citing
  evidence (file path / CONVO row id / receipt path). Never edit or delete a row.
- **Corrections are new rows** that cite the row id they correct (append-as-delete).
  A corrected row stays on the books, marked superseded by the correcting row.
- Row ids: `V-nn` = vision catch, `T-nn` = timer-caught failure, `C-nn` = correction.
- Every row MUST carry a 1-line account + an evidence path. A row without evidence
  does not count and is marked `UNEVIDENCED` in place — it never enters the tally
  until a later C-row supplies evidence.

## THE LAW (verbatim, from the canonical card)
> Time-anchored systems answer "when?" — state-anchored systems answer "what?".
> Repair is a WHAT, not a WHEN. A bug does not care what time it is; it cares
> whether someone looked. We have vision. Therefore: **fix things when you see
> them, and build so that you see them restfully** — no alarms, no 3 AM wakes,
> no clocks guarding quality.

## THE FALSIFIER RULE (verbatim, from the canonical card)
> Count bugs-caught-by-vision-pass vs bugs-caught-by-scheduled-fire for 7 days.
> Today: vision 7, scheduled 0. If scheduled fires out-catch looks over the week,
> REPAIR-ON-SIGHT dies and the cron teeth were right. Prediction: they will not.

## WHAT COUNTS AS A "TIMER-CAUGHT-FAILURE" (strict — no strawmen)
A row counts in the timer column ONLY if ALL four hold:
1. **Clock-origin:** a scheduled process (cron/automation/night-shift/watchdog
   timer) detected the defect on its own fire — not during a steering pass, not
   because a human or seat looked at its output.
2. **Novel sight:** the defect was NOT already caught, filed, or visible to any
   seat at detection time (no double-counting a look's find the timer merely
   re-reported).
3. **Repair path:** the detection led to a landed fix or a recorded disposition
   within the window (evidence: fix receipt or disposition row).
4. **Evidence:** fire log / automation id + the defect receipt it produced, cited
   in the row.
NON-counts (explicit): opportunity work a timer performs with nothing caught
(decks, seals, rotations); checks a seat ran by hand during a natural pass; a
timer that fired and found nothing; a defect a seat saw first and handed to a
timer to fix; a timer-produced report nobody read until a look tripped over it.

## THE DAY-BY-DAY TABLE
| date | vision-catches (V rows) | timer-caught-failures (T rows) | running tally (V:T) |
|---|---|---|---|
| 2026-09-05 (seed) | 7 — V-01…V-07, all evidence-cited below | 0 | **7:0** |
| 2026-09-06 | _pending — append rows below_ | _pending_ | 7:0 |
| 2026-09-07 | _pending_ | _pending_ | 7:0 |
| 2026-09-08 | _pending_ | _pending_ | 7:0 |
| 2026-09-09 | _pending_ | _pending_ | 7:0 |
| 2026-09-10 | _pending_ | _pending_ | 7:0 |
| 2026-09-11 (close) | _pending_ | _pending_ | 7:0 |

## SEEDED DAY 1 — 2026-09-05 (the receipted day: every catch was a look, none a clock)
- **V-01 — openalex 429 starving the monitor lane.** Seat READ the lane trails
  (15-min spools of 0 items); root = keyless impolite-pool hammering; fix = mailto
  polite-pool param + per-source 3600s cooldown, verified 2x same turn.
  Evidence: `queue/handoff/zcode/CONVO.md` row `[zcode 09-05 ~16:2xZ]` ("OPENALEX
  429 ROOT-CAUSED AND PATCHED"); card row in
  `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`.
- **V-02 — pin drift (Boss window riding GLM-5.3-full).** Operator glanced at the
  picker and asked "anything pinned to 5.3 needs to be on 5.3-flash… debug"; seat
  read the config/DB to root, three layers named.
  Evidence: `queue/handoff/zcode/CONVO.md` row `[zcode 09-05 ~20:4xZ]` ("PIN-DRIFT
  BUG DEBUGGED TO ROOT"); card row in
  `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`.
- **V-03 — concurrency failover ("switch to 5.3") mid-stream on the Max seat.**
  Operator handed the envelope; seat read the stack trace; same-turn Max triage.
  Evidence: `queue/handoff/zcode/CONVO.md` row `[zcode 09-05 ~16:2xZ]` ("FAILOVER
  TRIAGE ON THE MAX SEAT"); card row 3 in
  `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`.
- **V-04 — night-watch automation death (09-04/05 class).** CronList liveness
  check during a steering pass — the class that kills automations with their
  creating window; a5e12eea verified armed, liveness now a standing pass item.
  Evidence: `queue/handoff/zcode/CONVO.md` row `[zcode 09-05 ~16:2xZ]` item (1)
  NIGHT WATCH LIVENESS + row `[zcode 09-05 ~08:5xZ]` item (4) LIVENESS ✓ CronList;
  card row 4 in `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`.
- **V-05 — inbox drift (2 stale cards).** Seat listed INBOX during failover
  triage; both stale cards dispositioned into `watch/DISPOSITIONS.json` same turn.
  Evidence: `queue/handoff/zcode/CONVO.md` row `[zcode 09-05 ~16:2xZ]` item (3)
  "INBOX ZEROED"; card row 5 in `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`.
- **V-06 — Lite 73.2M premium burn (09-04).** Operator's billing glance spotted
  73.2M tok of GLM-5.3-full on the Lite key; attribution closed: the agents
  window's pinned scheduled task; operator killed the pin on his side.
  Evidence: `queue/handoff/zcode/CONVO.md` row `[zcode 09-05 ~05:1xZ]` ("CASE
  CLOSED BY OPERATOR… 73.2M tok"); card row 6 in
  `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`.
- **V-07 — art 404 / wiring orphans.** Operator said "broken"; seat diffed nav vs
  disk (served-is-not-wired); continuation receipt wires 10 orphan surfaces, 0
  dead links after.
  Evidence: card row 7 in `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`; repair
  continuation `watch/WIRING_AUDIT_20260906.md`.
- **T rows: none.** Scheduled fires catching things on 09-05: zero (the night
  shift a5e12eea had not yet had its first fire; all seven catches predate or
  bypass any scheduled fire). Canonical statement: `watch/SELF_STEAL_RESTFUL_WATCH_20260905.md`
  — "Scheduled fires catching things today: **zero.**"

## PROMOTION GATE (decision at window close, 2026-09-11 EOD)
- **Law 059 (REPAIR-ON-SIGHT) promotes** only if ALL hold:
  1. The cumulative 7-day ratio vision:timer holds **>= 5:1** (e.g. 7:1 or
     better at seed pace; timer column needs >= 1 genuine T-row before any
     denominator exists — a 7:0 week passes on the ratio but the card's own
     prediction "they will not [out-catch]" is what is being tested).
  2. **Every row in the tally is evidence-cited** — one UNEVIDENCED row blocks
     promotion until evidenced or corrected by a C-row.
  3. **A single fabricated row kills the law** — any V or T row whose cited
     evidence does not check out when verified disqualifies promotion outright
     for the window (the instrument is worthless if the tally can be wished).
- **Inverse (falsification of the law, per the canonical card):** if scheduled
  fires OUT-CATCH looks over the week, REPAIR-ON-SIGHT dies and the cron teeth
  were right.
- Clocks keep their right-sized residue regardless of verdict: night shift stays
  as OPPORTUNITY anchor (cheap window, seals, decks) — never the repair layer;
  deadlines (Sep-8 / Sep-20 / Oct-27) stay deadlines. See canonical card,
  sections "THE DOCTRINE" and "WHAT THE CLOCKS KEEP".

## APPEND ZONE (new rows go below this line)
_(empty — day 1 seeded from receipts; next rows append here with ids V-08+/T-01+)_
