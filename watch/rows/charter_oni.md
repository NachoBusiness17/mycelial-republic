# CHARTER ONI — attack lane — 2026-08-31
Calibration: ½ multipliers receipted; I read code+payload, did not execute.

## M1 — HOLD
Command IS runnable. Schema (lane/ok/cost_usd/latency_s/task) matches `cmd_record` (second/dup def shadows first harmlessly). Emits `kind:outcome` row; verkle best-effort, can't crash the pipe. **FIX:** PASS greps "the marker (receipted acceptance, codex_jobs)" but the row carries only `task_head` — row0.json task has no marker token, so on a fresh host grep fails. Amend PASS to literal marker (task contains `codex_jobs`) and assert it in row0.json.

## M2 — HOLD/AMEND
Bypass writer is real: `blackboard_post` writes bb-*.json directly, `UNMESHED "legacy direct write"` — no switchboard dependency to kill. So "kill switchboard → board writes fail-closed" is testable only for the pinned-guard; non-pinned writes keep flowing → test bends no wire (trivial PASS) or exposes the bypass (architecture FAIL). **FIX:** Five Tests target the real invariant: switchboard alive ⇒ pinned decision/conflict minted only via proposal; dead ⇒ such mints deny. Classify blackboard_post in/out of test explicitly.

## M3/M4/M5 — HOLD (M2-gated, no standalone crack).

## Kill criteria
**Weakest milestone: M2** — test file absent AND its central test is contradicted by the shipped bypass writer. **Unobservable criterion: K2** — no standing cache-hit meter in ledger/fuel feed; `cache_hit_rate` is passive per-call bool; the `<90% sustained` branch is confirmable only via on-demand A/B probe (needs live remote + key) or the z.ai portal — outside the cage. Kill switch can't be passively pulled.

**Weakest link:** M2's fail-closed test is invalidated by the bypass writer it polices.
