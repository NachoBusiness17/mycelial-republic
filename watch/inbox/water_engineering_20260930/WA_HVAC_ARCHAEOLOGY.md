# WA - HVAC ARCHAEOLOGY (lane 1/6, 2026-09-30)

## What it was
`dashboard/static/airflow_home.html` - "AIRFLOW HOME: the house is the prompt," ROOM #1 of the Game Prompt Lab, built 2026-09-07 (receipt `watch/GAME_PROMPT_LAB_20260906.md:74-90`). Mechanics: HVAC-real well-mixed zone model - 3 rooms, doors/windows/fan/wind openings, pressure transport, fresh-air dilution, conserved smoke particles ("never despawns; plume persists outside"). The flow-testing loop: logged prediction -> timed run -> verdict ("which room breathes first": west wind clears the leeward bedroom in 8.7s).

## Still runs?
Yes - as an ORPHAN. File intact, self-contained static HTML, but unlinked from `dashboard/static/games/index.html` (9 hrefs, none to it).

## Evolved into
NOT arena_operator_field.html (that is the B1a gradient game, separate lineage). The true descendant is `dashboard/static/games/maze_arena.html`: `__fluidTick` at line 793, invoked every 2 ticks, with the comment at line 842: "HVAC SELF-STEAL (airflow_home): smoke is stuff, not pixels - conserved work per island."

## Why it "died"
No kill commit - it was ABSORBED. Receipt `watch/inbox/FLUID_LENS_MANIFEST_20260913.md:40` ("HVAC SELF-STEAL MANIFESTED"): the HVAC conservation law had what the fluid maze lacked, wired in same-turn. Git entry only via bulk checkpoint d575bc168 (2026-09-14).

## The answer to the operator
The HVAC didn't die - it lives inside the maze uncredited, and the original runs unlinked. Two easy wins: (1) relink airflow_home.html in the games index; (2) port its prediction-verdict flow loop to the Mountain's water (the meter's oldest game-shaped ancestor).
