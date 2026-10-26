---
name: errno22-cage-writes
description: Cure OSError Errno 22 on lane state writes in the mag-sovereign cage. Use when any lane CYCLE_FAILs with "Exc OSError Errno 22 invalid argument" on a runner_state.json or trail write, or when a lane re-runs ~100s loops and loses completed-work records.
argument-hint: <lane-name>
---

CURE errno-22 cage state writes for lane `$0`.

## Instructions

- If `$0` is missing, ask for exactly one lane name (ls queue/lanes/).
- Evidence base (2026-10-04 roll-up, social_rsi --check): 825 windowed
  CYCLE_FAIL rows (96.9% of all lane failures) since 2026-09-25 across
  research/builder/night/prose; green pairs at builder +63s and night
  +171s after the atomic-save cure; research never greened (a second
  write site or a stale cage daemon). Packet:
  watch/inbox/social_rsi/packet_exc-oserror-errno-invalid-argument_2026-10-04.md
- GATE: no daemon restarts without naming the pid and the pickup path -
  the cage daemon must load the cured code, and a restart drops any
  in-flight cycle.

Diagnose which write site the lane hits:

```bash
grep -n "open(.*\"w\"\|O_TRUNC\|truncate" mag/lane_runner.py | grep -i "state\|trail"
tail -3 queue/lanes/<lane>/trail.jsonl
docker exec mag-sovereign python -c "import mag.lane_runner"  # does the cage import the cured module
```

The known cure (applied 2026-10-04 to _save_state, the bay_organs
pattern): never open the live state file through the bind mount with
truncating writes - write tmp + os.replace (atomic on the host side).
If the lane's writes go through a DIFFERENT site (its own scripts,
watch/march_228.py-style module-level opens), apply the same pattern
there. If the code is cured but failures persist past one daemon cycle,
the cage daemon is stale: name the pid, restart it, and verify the next
cycle lands green in the trail before calling it done.

Final response: report the lane, the write site(s) found, cure applied
or already-present, daemon pickup proof (trail row after the change),
and the before/after fail counts from
`python tools/social_rsi.py --check --days 14`.
