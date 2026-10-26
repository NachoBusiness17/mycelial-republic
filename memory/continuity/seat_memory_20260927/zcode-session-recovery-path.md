---
name: zcode-session-recovery-path
description: How to recover content from a vanished z.code window — rollout
  jsonl + ReadSessionContext cross-session
metadata:
  node_type: memory
  type: reference
  originSessionId: sess_0014179a-6f14-415b-b3dd-21996c202983
---

Vanished z.code windows leave their full transcript at `~/.zcode/cli/rollout/model-io-sess_<id>.jsonl` (one file per session; the session id is in the filename). Any seat can pull a summary via `ReadSessionContext` with that session id — verified 2026-09-14 when the FORGE DAEMON window (sess_712a3b7b-d5dc-4946-9ad1-1a8e677a5d83) disappeared but its work had already been filed to `watch/inbox/` per the shared-surface rule (see [[shared-inbox-index-fold-stale]]).

**How to apply:** When a window dies, start with a fleet check: `docker ps` — the Mag fleet lives in containers (mag-sovereign/mag-worker/mag-redis) and is almost always fine; the *host* supervisor being dead is by design (`state/DOCKER_ONLY`; restore = `docker compose restart mag`, never a second host supervisor via `mag.cmd lab`). Then check (1) which `model-io-sess_*.jsonl` files were written minutes before, (2) grep for topic keywords (they're plain JSONL of message objects), (3) ReadSessionContext for a clean summary, (4) point the operator at the inbox artifacts rather than the cache transcript. File a `SESSION_RECOVERY_*` RECEIPT in watch/inbox; commit the checkpoint. A window closing ≠ work lost if the inbox convention held. Full wake-order runbook: `watch/inbox/SHERPA_NEXT_US_20260914.md`.
