# ACTIVITY TRAIL (shared_activity.v1)

The universal append-only activity trail: every actor writes **one self-describing JSONL
line per action**. One format, appended forever, readable forever — this is the core
pattern that makes any agent fleet auditable.

## The record (exactly one line per action)

```json
{"schema": "shared_activity.v1", "id": "act-<hex12>", "ts": "<ISO-8601 UTC>",
 "seat": "<where>", "actor": "<who>", "depth": "<tier>", "goal": "<why>",
 "status": "<planned|tick|done|...>", "detail": "<one bounded line>", "task_id": <id or null>}
```

## Why it holds up

| property | mechanism |
|---|---|
| self-describing | `schema` on every line — the format evolves without breaking old readers |
| identity | `id` is a content-addressed tag (`act-<hex12>`, or a namespaced weave id) |
| who/where | `actor` (code or seat) + `seat` (surface) — both, always |
| honesty | `status` is the actor's own claim; `detail` stays one bounded line |
| append-only | nothing is edited; corrections are new lines |
| joinable | `task_id` links the action to the task registry when one exists |

## Scale receipt (the source estate)

| check | value | command (this session) |
|---|---|---|
| lines | **100,805** | `wc -l state/shared_activity.jsonl` |
| span | 2026-08-04 → 2026-09-25 (head + tail read) | `head -n 1` / `tail -n 1` |
| still appending | yes — 100,771 at the candidate's session, 100,805 now | as designed |

First line: `{"schema": "shared_activity.v1", "id": "act-df331d6fbc0f", "ts": "2026-08-04T16:07:09.716488+00:00", "seat": "api", "actor": "api", "depth": "scut", "goal": "status check", "status": "planned", ...}`
Last line (Sept 25): `{"... "id": "weave-heart-84de9b88", ..., "seat": "heart", "actor": "governor_autorun", "depth": "scut", "goal": "autorun tick", "status": "tick", "detail": "fill=0 drain=", ...}`

## Receipt

- state/shared_activity.jsonl (estate) — head, tail, and count as above — read/run this
  session. The estate's personal goal strings stay out of the seed; the format is the ship.
