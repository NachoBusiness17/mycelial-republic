# ZCODE PROTOCOL BRIDGE — RECON (2026-09-03, for the reopen-build)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: `session/updateRuntimeModelConfig` is the reopen key for the zero-quota coding-plan door via zcode.cjs app-server — UNPROVEN (read from bundle bytes; bridge build never executed end-to-end) · falsifier: the app-server rejects updateRuntimeModelConfig post-OAuth, or the bridge fails at handshake/framing

Goal: drive the coding-plan provider (zero-quota door) through the app the runtime
already trusts. The standalone CLI headless path is BLOCKED (see
`mag/seat_dispatch.py` zcode-cli verdict); the app-server is the sanctioned surface.

## What the recon found (all from `resources/glm/zcode.cjs` bytes)
- Command: `zcode.cjs app-server --stdio --surface terminal|desktop` — a stdio
  protocol server ("ZCode Protocol"). The desktop runs THREE of them right now.
- Wire format: JSON events + requests. Event names seen: `session.created`,
  `session.resumed`, `session.updated|upserted|titleUpdated|persisted|closed|removed`,
  `turn.started|completed|failed|terminal`, `turn.steerQueued|steerDrained`,
  `response.created`, `part.started`, `checkpoint.created`, `automation.create`.
- Request namespace (client→server), partial map: `session/subscribe`,
  `session/stop`, `session/usage`, `session/subagents`, `session/setThoughtLevel`,
  `session/cancelBackgroundTask`, **`session/updateRuntimeModelConfig`** ← the one.
- **`session/updateRuntimeModelConfig` is the reopen key**: the protocol can SET the
  runtime model config per session — exactly the resolution the standalone CLI lacks
  (`requireRuntimeModelConfig` throws because only the exe runtime builds the
  coding-plan provider post-OAuth).

## The build (next session, organ-forge candidate)
1. Spawn `zcode.cjs app-server --stdio` from Python (subprocess, line-JSON framing —
   confirm framing: JSONL vs LSP headers, by feeding one request).
2. Handshake: find the initialize/open request (grep `initialize`, `session/open`,
   or protocol version strings) — capture one real session's traffic from the desktop
   if allowed, else probe.
3. `session/updateRuntimeModelConfig` with the coding-plan family; then open a turn,
   send a prompt, collect `turn.completed` + response parts.
4. Wrap as a `zcode-bridge` seat in `seat_dispatch.py` HEADLESS (same contract as
   openclaw/opencode seats), then engine Z points at it → zero-quota plan door reopens,
   T2 (N=4 throttle) becomes runnable.

## Fallback lane meanwhile (LIVE tonight)
opencode seat, model zai/glm-4.7, 2× campaign quota, non-resident (contract inlined
per beat — `CHURN_RESIDENT=0`), engine Z rung 1 of the 1-2-4-8 ladder.

## Owed organ fixes (filed tonight, scanner-blocked)
- reconciler `launch()` must write the child pid into the lockfile (empty lockfiles
  = double-launch window; Mimosa blocked the patch on path-construction hygiene —
  retry via organ forge with `os.path.join`-built names + `_contained` everywhere).
- `requeue`/`starved_slots` need a state-file grace period (mtime age > N minutes)
  — young engines get requeued mid-run tonight's verify showed the hazard.
