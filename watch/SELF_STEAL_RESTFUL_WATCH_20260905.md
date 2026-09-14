# SELF-STEAL: THE RESTFUL WATCH (2026-09-05)

Trigger — operator, after the pin-drift debug and its proposed cron teeth:
"why have things anchored to time — we have vision — we should just fix things when we
see them, restfully."

Law-candidate 059 (prose → promotion is the operator's). Working name: **REPAIR-ON-SIGHT.**

## THE PRINCIPLE
Time-anchored systems answer "when?" — state-anchored systems answer "what?". Repair is
a WHAT, not a WHEN. A bug does not care what time it is; it cares whether someone
looked. We have vision. Therefore: **fix things when you see them, and build so that
you see them restfully** — no alarms, no 3 AM wakes, no clocks guarding quality.

## THE RECEIPTS — every catch today was a look, none was a clock
| Bug caught today | Caught by | Caught by a timer? |
|---|---|---|
| openalex 429 starving the monitor lane | seat READ the lane trails (15-min spools of 0) | no |
| pin drift (Boss window, 5.3-full) | operator glanced at the picker; seat read the DB | no |
| concurrency failover (the "switch to 5.3") | operator handed the envelope; seat read the stack trace | no |
| night-watch automation death (09-04/05 class) | CronList liveness check during a steering pass | no |
| inbox drift (2 stale cards) | seat listed INBOX during failover triage | no |
| Lite 73.2M premium burn (09-04) | operator's billing glance | no |
| art 404 / wiring orphans | operator said "broken"; seat diffed nav vs disk | no |

Scheduled fires catching things today: **zero.** The night shift hasn't even had its
first fire. The clock-based defenses are all still UNSUPPORTED — not failed, just never
the one that actually saw.

## THE FAILURE HISTORY OF THE TIME ANCHORS (the pattern, not the anecdote)
- Scheduler died silently twice → CronList liveness law exists BECAUSE the clock hides
  its own death. A time anchor's failure mode is silence.
- Recurring automations die with their creating window (birthmark law) — the 09-04 card
  caught night automations deleted 30 minutes before their fire. The clock died; nobody
  heard it.
- The day-work flywheel burned premium for days on a 5.3 pin (LAW-056 fireball). The
  timer didn't just miss the bug — the timer WAS the bug.
- Today's concurrency failover: the "switch to 5.3" happened to THIS window mid-stream.
  No timer saw it. The operator's eyes + one hand-carried envelope saw it in minutes.
Time anchors have one property clocks can't lose: they fire blind. And everything that
fired blind this week either died quietly or burned money quietly.

## THE DOCTRINE (what changes)
1. **Steering passes are the scheduler.** Every natural pass (morning brief, any triage,
   any intake) carries the state checks: pin audit, CronList count, INBOX depth, lane
   trail tails. The checks ride EXISTING looks — that is restful. Zero new timers.
2. **Clocks demote to opportunity anchors, never repair anchors.** The night shift
   stays — but as "the cheap window" (decks rotation, seal ritual, quiet-lane work),
   not as the thing that catches bugs. If the 23:00 fire dies (again), nothing repair-
   class is lost, because repair never lived there. Seals are additive (delete-as-
   append): a missed seal is re-sealable, so it can ride a clock; a missed REPAIR
   compounds, so it must ride sight.
3. **Restful = the watchman, not the alarm.** The record keeps the schedule; the seat
   keeps the watch. Fix what you see; arrange to see more; refuse to schedule seeing.
4. **Anchors of state we can add later (all event-shaped, none time-shaped):** the
   pin_audit organ exits nonzero → the flag rides the NEXT natural pass (no timer);
   inbox depth in the brief; trail-tail staleness in the brief. The hooks fired today
   (example-plugin noting tool calls) are already the right shape — the harness
   whispering on events, not on hours.

## WHAT THE CLOCKS KEEP (right-sized, not abolished)
- 23:00/02:00/05:00 night shift: OPPORTUNITY (cheap/quiet window for decks + seal), not
  the repair layer. Its step-0 pin audit is a bonus look, not the load-bearing one.
- Sep-20 / Sep-8 / Oct-27 walls: these are DEADLINES (human-meaningful time), not
  watchdogs. Deadlines are fine; they don't pretend to see.

## FALSIFIER (a week, countable)
Count bugs-caught-by-vision-pass vs bugs-caught-by-scheduled-fire for 7 days. Today:
vision 7, scheduled 0. If scheduled fires out-catch looks over the week, REPAIR-ON-SIGHT
dies and the cron teeth were right. Prediction: they will not.

THE CROP: the one thing vision genuinely cannot do yet is see while the seat sleeps —
the 02:00 fire and the night shift still carry the hours nobody looks. Until a seat
dreams (the night shift's real job), the clocks hold the cheap hours and the lamps.
Restful does not mean unwatched; it means nothing wakes anyone unless the looking
finds something worth waking for.
