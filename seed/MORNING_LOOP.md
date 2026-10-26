# MORNING LOOP — the daily rhythm, as a recipe

The estate runs a fixed morning cadence so the day starts with readings, not scrolling:

| when | what | how |
|---|---|---|
| hourly | **cooker**: `python engines/cooker.py fire --due` | cron/schtasks — burns every free-lane refill automatically |
| every 15 min | **lane supervisor**: `python engines/../mag/lane_supervisor.py probe` (or copy it up) | cron/schtasks — lanes self-heal, your phone only rings on a no-failover class |
| daily | **spine walk**: `python engines/spine_walk.py <your-folder>` | cron — the index regenerates, never hand-maintained |
| daily | **smith chart**: `python engines/estate_smith_chart.py --no-plot` | read the meters; a bar crossed = a fix, not a paragraph |
| daily | **key audit**: `python engines/key_law.py --audit` | exits nonzero naming any undeclared or dead lane |
| daily | **task wall**: `python engines/task_wall.py --budget-minutes 15` | burns free lanes on YOUR chores (configs/chores.json) |

Windows: `schtasks /Create` or PowerShell `Register-ScheduledTask`. Linux: cron lines.
The point is not the schedule — it is that the machine opens the day before you do,
and your first hour goes to the people who matter.
