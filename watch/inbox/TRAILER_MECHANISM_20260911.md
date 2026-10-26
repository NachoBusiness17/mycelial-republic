# THE TRAILER MECHANISM — attachment under relative motion (self-steal, 2026-09-11)

Operator: the sport where a flatbed truck circles a track and a pack of cars must drive UP onto the moving trailer and STAY ON for a set time to win — while the truck driver actively swerves and brakes to shake them off. "I see this as a mechanism within our system somehow."

THE POINT:
- The mechanism has a name: **attachment under relative motion.** The platform does not wait for you. Boarding requires matching its speed; HOLDING requires surviving its maneuvers; winning is TIME, not arrival. Arriving is easy. Staying is the sport.
- That is the fleet's core unsolved problem, stated as a motorsport: docking with a moving reference frame and holding under active perturbation. Astra's effect-broker contract (dispatch while the destination commits, ownership epochs, UNKNOWN holds) is the trailer problem written in contracts. The night test is "stay on for a set time." The quota wall at width 20 was the pack getting shaken off.

## THE MAP (every element of the sport = one fleet organ)

| the sport | the fleet |
|---|---|
| the truck circling | the wave/loop cadence — the moving platform that never waits (ticks, tides, C1/C2 windows) |
| the truck driver's swerve | active perturbation: failures, quota walls, restarts, the adversary's counter-moves |
| the pack of cars | the lanes/sub-swarms competing for limited boardings (width band, spawn-2-per-fold) |
| boarding the ramp | docking a lane onto the cadence (matching speed = meeting the tick) |
| STAYING ON | the ownership epoch / lease: holding through the platform's maneuvers |
| the set time | the night test (8 hours), the 24-hour dead-hand drill, C1→C2 duration |
| falling off | a lane dropped by failure, quota, or restart (the width-20 wall) |
| re-ramming the ramp after a fall | the anti-pattern: halt-not-hammer forbids it (two falls = back to the shore) |
| the win | time-on-trailer = sustained verified presence through disturbance |

## WHY THIS MATTERS (the mechanism, formalized)
The night test as written measures TASKS. The trailer measures something harder and truer: **hold-time under maneuver.** A lane that completes 40 tasks in a calm window can still fall off in the first swerve. Time-on-trailer is the meter for the thing "unattended" actually means — attachment that survives the driver fighting back.

## v0 (the game-ified night test — renders for free)
wave_driver gains TRAILER MODE: each tick, a lane must dock (meet the tick with its task) and hold; the driver injects perturbations per a sealed schedule (the fixture-controller pattern — delays, restarts, quota pinches). Score = consecutive seconds-on-trailer per lane, rendered live on the wow surface: boarding attempts, holds, and falls, in real time. The set time = the registered duration; the win = stayed on through the whole sealed swerve schedule.

## FALSIFIER (the ceremony test, inherited)
Time-on-trailer must PREDICT accepted-task rate (trailer-time correlates with accepted work) — otherwise it's a metaphor wearing a meter, and the trailer goes back in the bowl. Also: perturbations must be sealed (the fixture-controller holds the schedule) or a kind truck = rigged sport.

## THE LINEAGE (it was already in the record)
- Chair 10's dead-hand drill = the 24-hour trailer run through a blackout.
- Chair 8's width-ramp = learning to board at width 2 and 4 before trying 8.
- Astra's ownership epochs = the physics of staying attached when the platform jerks.
- halt-not-hammer = the rule that separates a racer from a rammer.
- The wow surface (viz_gallery) = the grandstand, already built.

## FIRST TRAILER KIFU — run 20260911T202527Z-trailer (15 min, 3 lanes, 2 sealed swerves)
- Lane 0: 900s on-trailer · 45/45 docked · 0 falls · 100%
- Lane 1: 880s · 44/45 · 0 falls · 1 quota-pinch survived by the book (frozen tick excluded, not a fall) · 97.8%
- Lane 2: 900s · 45/45 · 0 falls · 100%
- Schedule e8678d16d983: 2 swerves fired; ZERO falls; one pinch correctly frozen out of scoring.
- VERDICT v0: the meter works. Hold-time under sealed maneuver is measurable, renderable, and honest (the pinch was scored as frozen, not as failure). Next: the falsifier probe — correlate trailer-time with accepted-task rate, and scale perturbation severity until lanes fall.
