# SHARED SURFACE LAW

Agent sessions are cache. Durable cross-surface work lands in ONE contracted shared
inbox. Work that only exists inside a session's scratch directory does not exist.

## The ruling

Every client context — editor, CLI seat, container, WSL — may read from anywhere but
must treat its own session directory as cache-only. One durable write root, one machine
contract, one validate command.

## Per-context write-root table (the estate's, as the shape to copy)

| Context | Read first | Durable write root |
|---|---|---|
| Windows host / main venv | `watch\inbox\INDEX.json` | `watch\inbox\` |
| Docker / container seat | `/board/inbox/INDEX.json` | `/board/inbox/` |
| WSL | `<host path>/watch/inbox/INDEX.json` | same directory |

## The four rules

| rule | meaning |
|---|---|
| Read the index first | Classify existing content before reuse; never re-derive what is already filed. |
| Preserve hashes and bounded pointers | Copy references, not blobs; a pointer with a hash beats a duplicate. |
| Leave a receipt before promotion | Anything moved from cache to the shared root gets a who/what/when receipt row. |
| One validate command, fails loud | `python -m shared_surface validate` (estate: `.venv\Scripts\python.exe -m mag.shared_surface validate`) — the contract file (`SHARED_SURFACE_CONTRACT.json`) is machine-checked, not prose. |

## Propose vs authorize (the capability split)

Model text can **propose**; only the switchboard / effect broker **authorizes** effects.
A chat message, a draft file, or a plan is never itself an effect — promotion to the
durable root, sends, spends, and deletions go through the one door that logs them.

## Boundary family

The estate constitution carries the same family as binding law: fork equality, data
tiers T0–T3, handoff contracts for escalation (CONSTITUTION.md:9-14, read this session).
The shared-inbox ruling itself is AGENTS.md:10-20.

## Receipt

- AGENTS.md:10-20 (estate) — cache-only ruling (:12), the write-root table (:14-18),
  contract + receipt + validate + propose/authorize split (:20) — read this session.
- CONSTITUTION.md:9-14 (estate) — the boundary-law family — read this session.
  (The candidate cited CONSTITUTION.md:11 as the echo; line 11 is the data-tiers law —
  same family, adjacent clause. Stated as read.)
