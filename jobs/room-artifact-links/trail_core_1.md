# Trail core 1 — room artifact links

## Completed

- Added lazy `path:line` token parsing to `GET /room` response records as `artifacts` arrays.
- Added `GET /room/artifacts` with newest-first refs containing `path`, `line`, `seat`, `ts`, and `thread`.
- Kept room storage unchanged; malformed JSON remains skipped/raw under existing behavior.

## Artifacts

- `mag/api_gateway.py`
- `jobs/room-artifact-links/trail_core_1.md`

## Acceptance

```text
ARTIFACTS ROUTE OK 401
ROOM STILL OK 401
```

The contract acceptance commands passed with the repository `.venv` interpreter. A temporary-file behavior check also confirmed both parsing shapes.

## Failures

- None.

## Checkpoint

- completed: true
- artifacts: `mag/api_gateway.py`, `jobs/room-artifact-links/trail_core_1.md`
- failures: none
- budget_used_pct: not tracked
- next_action_one_line: stop; no further action for this seat

## Handoff

- done: room artifact parsing and listing implemented and acceptance-checked
- untested: live HTTP server integration and query-string transport outside the contract commands
- blocked: false
- resume_command: `codex exec --skip-git-repo-check -C <repo> 'read jobs/room-artifact-links/seat_contract.json + latest trail_core, do next_action, run acceptance_commands, write trail_core_N'`
