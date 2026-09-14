# gateway-durable-spawn — trail core 1

## Done

- Added the `api_gateway` service to `mag_launch.py`’s existing `build_slots()` spawn list.
- The slot runs `main.py api --host 0.0.0.0 --port 8001` and uses the existing detached supervision/logging pattern.
- No sibling spawn, Docker command, `covenant.json`, or `watch/` content was changed.

## Acceptance

```text
mag_launch parses
api spawn present
```

## Checkpoint

- completed: true
- artifacts: `mag_launch.py`, `jobs/gateway-durable-spawn/trail_core_1.md`
- failures: none
- budget_used_pct: not tracked
- next_action_one_line: stop; no further action for this seat

## Handoff

- done: API gateway durable spawn added and acceptance commands passed
- untested: live service startup and HTTP health response
- blocked: none
- resume_command: `codex exec --skip-git-repo-check -C <repo> 'read jobs/gateway-durable-spawn/seat_contract.json + latest trail_core, do next_action, run acceptance_commands, write trail_core_N'`
