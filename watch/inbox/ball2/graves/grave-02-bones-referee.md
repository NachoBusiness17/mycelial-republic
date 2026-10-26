# GRAVE 02: queue/handoff/HANDOFF-2026-09-16-bones-referee.json

- **Filed:** 2026-09-29 by lane grave-supersede (division C, GRAVEDIGGER, ball 20260929)
- **Classification:** DONE-ELSEWHERE (machine row watch/inbox/ball2/graves/grave-supersede.jsonl)
- **Buried entry:** `queue/handoff/HANDOFF-2026-09-16-bones-referee.json` (handoff.v1, owner zcode, assignee hermes, T1-local)
- **Nothing was deleted, moved, or edited. Deletions are operator-gated.**

## What justifies the burial

Every artifact the output_contract names is on disk, dated 2026-09-16
(the handoff's own week):

- `mag/wow_bones_session.py` (11,108 bytes, 2026-09-16) - the deterministic session runner
- `tests/test_wow_bones_session.py` (6,356 bytes, 2026-09-16) - its tests
- `mag/bones_adapter.py` - the thin /bones Discord adapter; its module
  docstring cites the directive (`watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md`)
  verbatim and defines the /bones start/move/status/receipt/verbs surface

## Successor surfaces (resolving pointers)

- `mag/bones_adapter.py` - the adapter of record; docstring carries the laws
  (text-only adapter, runtime token read, guild-scoped NT-ACv2 / #game-c-overview)
- `mag/wow_bones_session.py` + `tests/test_wow_bones_session.py` - the referee kernel
- `watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md` - the directive (still on disk)

## Open work NOT buried

The adapter docstring gates the LIVE run on operator token rotation and
channel permission; whether the Sep-20 live demo fired is not claimed by
this grave. This grave retires the queue ENTRY (its build sequence is
landed); the live-demo gate stays with the directive.
