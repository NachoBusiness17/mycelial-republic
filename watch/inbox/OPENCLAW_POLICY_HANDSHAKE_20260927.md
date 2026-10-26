# OpenClaw runtime-policy handshake: context admission <-> OpenClaw runtime

Date: 2026-09-27 · Lane: BURN_RESET_20260927_EVENING lane 9 (Dirac loops 4+5)
Status: BANKED contract, bytes-verified 2026-09-27. One invariant closes both
directions because the label set of the two loops is identical modulo direction.

## The two sides

### Side A: context admission (mag/context_admission.py, schema context_admission.v1)

What admission checks today, per the code:

- `assess()` is a deterministic, network-free preflight. It takes
  `estimated_tokens`, `context_window`, reserve budgets (tool schema + reply),
  and `repack_ratio`, and returns a band: green / amber / red / black.
- `allowed = estimated_tokens <= threshold` where
  `threshold = (context_window - reserves) * repack_ratio`. A prompt is
  admitted before dispatch, never after a provider rejection.
- Pressure and recovery leave durable receipts at
  `memory/runs/context_admission/receipts.jsonl` (measurement + ids only; no
  prompt or tool bodies).
- Admission NEVER calls a model and NEVER authorizes an effect. It answers one
  question: does the next prompt fit the configured window.

### Side B: OpenClaw runtime policy (deploy/openclaw/openclaw.container.json; live state C:\Users\foste\.openclaw\openclaw.json)

What the container policy actually constrains, per the file:

- Gateway: local mode, token auth (`OPENCLAW_GATEWAY_TOKEN` from env), fixed
  control-UI origins.
- Tools: profile `minimal` plus an explicit `alsoAllow` list
  (sessions_spawn/yield/list/history, subagents); loop detection enabled.
- Agents (`ownership: explicit`): `main` (Sancho Overseer, tools profile full,
  exec on gateway), `worker` (Bounded Worker, tools profile coding with an
  explicit deny list: gateway, nodes, message, cron, sessions_spawn, subagents,
  sessions_yield, sessions_list, sessions_history; cannot spawn secondary
  workers), `zcode` (coding profile). Subagents require an explicit agentId.
- Context policy inside the runtime: `contextLimits` char caps
  (12000/8000), cache-ttl context pruning with hard clear, safeguard
  compaction (keepRecentTokens 8000, maxActiveTranscriptBytes 4mb), mid-turn
  precheck and memory flush.
- Hooks: internal `mag-file` hook (deploy/openclaw/hooks/mag-file) files
  OpenClaw events to `/board` (host `watch/`) as `room.jsonl` rows and
  `openclaw_traj.jsonl` trajectory spans with line/byte bounds + body hash.
  Its own header states the boundary: "Does not govern." Mag DNA is read-only
  in the OpenClaw cage; hook failures are fail-open.

## The authority chain (the detour IS the contract)

Read from the code, not from doctrine alone:

1. Model text (Mag or OpenClaw seat) can only PROPOSE. Per AGENTS.md and the
   code: "Model text can propose; only the switchboard/effect broker
   authorizes effects."
2. `mag/switchboard_v2.py` is the reference monitor. Every `grant()` call runs
   `mag.policy_engine.validate_authority()` (TTL, budget, authority label,
   revocation) before a proposal reaches AUTHORIZED; require_confirmation
   effects defer to the operator inbox
   (`bridge/operator_inbox.jsonl`). State machine ends at RECEIPT_COMMITTED;
   trail: `memory/runs/switchboard/trail.jsonl`.
3. `mag/effect_broker.py` is the unified execution layer. It executes only
   when (a) `authority.status == AUTHORIZED`, (b) the effect is in
   `authority.granted_capabilities`, and (c) `policy_engine.validate_authority()`
   passes. Allowlists: fs_write paths, tool_invoke cwds, network denylist.
   Receipts: `memory/runs/effect_broker/` (ENQUEUED -> RUNNING -> COMPLETED /
   FAILED -> RECEIPT_COMMITTED).

Context admission sits UPSTREAM of dispatch and has no bypass into this chain.
An admitted prompt (allowed=true) still gets its tool-side effects authorized
only through switchboard -> effect_broker. An OpenClaw runtime policy grant
(tools profile, alsoAllow) governs what the OpenClaw agent MAY attempt inside
its cage; it never grants Mag-side effects. The two policies meet only through
the switchboard/effect-broker detour, which is why the closed loop runs
context_admission -> dirac_loop -> self_audit -> swarm_worker ->
effect_broker -> switchboard -> openclaw and back. A direct edge would be a
fabrication of authority; none was added.

## Receipt pointers, one each way

- Admission -> runtime side: `memory/runs/context_admission/receipts.jsonl`
  (admission decisions, bands, repack pressure).
- Runtime -> admission side: `watch/openclaw_traj.jsonl` +
  `watch/openclaw_traj.jsonl.bounds.meta.json` (trajectory spans, hashed,
  verifiable without replay).

## What this artifact closes

Dirac loops (operational scope, scan 2026-09-27):

- loop 4: edge `organ:context_admission->organ:openclaw`
- loop 5: edge `organ:openclaw->organ:context_admission`
- shared invariant: `1992f3960400...` (identical label set modulo direction;
  full hash banked in watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl)

Closure banks the holonomy of the real chain above. The loop stays in the
graph; the GAP status ends.
