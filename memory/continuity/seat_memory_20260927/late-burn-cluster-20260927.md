---
name: late-burn-cluster-20260927
description: Late burn cluster 9/27 — base_url tri-scope locality sweep,
  resolver deadline bound, pointer-anchor law with rot checker, B2-133 dormant
  flag gate in 7 consumers, secret scan credential exposure, essentials pack
  off-machine backup
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Late flash-lane burn cluster 2026-09-27 (lanes B2-107, B2-133, B2-342,
B2-489, B2-490, B2-491 + the essentials pack + the secret scan).

## Key patterns born this session

**Pointer-anchor law (B2-491):** every NEW file:line pointer in a burn brief
must carry a byte anchor `path:NN[-MM]#token`. tools/pointer_rot_check.py
names rotted pointers. Born from two same-day pointer rots (providers.yaml
ollama key moved 66→84, mistral 534→550).

**Dormant flag gate (B2-133):** `mag/dormant.py` is the single reader of
`dormant: true`; seven consumers gated (fuel_feed, rotation_harness,
lane_salon, quorum_window, research_fanout, cost_truth, free_tier); 51
tests green. Operator GO flips the flag in providers.yaml and every gate
restores with no code edit.

**Resolver deadline bound (B2-489):** getaddrinfo runs on a named daemon
thread joined at 2.0s. A blackholed DNS can no longer hold the doctor
hostage. Falsifier: a monkeypatched 30s sleeper bounded to the 2s deadline
class. Three pins added.

**base_url_env tri-scope locality (B2-490):** every env-set base URL
classified across host shell / compose / k8s scopes. The repo's own .env
line 118 carries `OLLAMA_HOST=http://ollama:11434` (docker-internal name)
which the host reads as unresolvable, confirming B2-107 on the host seat.

**Secret scan credential exposure (B2-73):** 19 corpus oral-history files
carry a harvested .env dump with 18 real-shaped credentials pasted into
remote grok/codex seats. Rotation owed, operator-gated. Filed artifacts
clean; the leak is in the corpus estate, not the filed receipts.

**Essentials pack (first real off-machine backup):** 1.59 GB AES-256
encrypted + 22 MB vault supplement, OneDrive copied. The estate had NO
off-machine backup before this session.

## Operator corrections to carry

- Mixed-case .env key names are not a bug; they work on Windows and are
  "just weird stuff you don't expect." Don't normalize unless cross-platform
  breaks.
- Cerebras parked until a use is found; lane never worked once (zero
  generations ever), dormant stays true.
- The width ceiling is dynamic (depth-dependent), not constant. The frozen
  constant was the bug ("underselling our own experience is a bug").

## Session architecture pattern

The flash-lane burn proved a reusable architecture: dispatcher (every 10
min, refills to cap from queue) + swarm lanes (12 deep workers, each
owning 25 sequential briefs) + free-lane runner (external lanes in
parallel) + claim law (prevents concurrent queue edits) + checkbox law
(prevents premature flips) + restore guard (prevents stale-base erasures)
+ janitor passes (dedupe numbering collisions). This architecture handled
506 dispensed briefs across 14+ hours with 402 landed receipts.
