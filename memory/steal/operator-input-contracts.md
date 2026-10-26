# Steal memo — operator-input contracts (2026-08-09)
Source: steal-protocol mine of 11 cloned orchestrator repos (`mine/raw/steal_protocol`).
Law: contracts only — never duplicate DNA, never default seat.

## The strongest steal-able contract (agentswarm)
Typed operator-control channel: `ControlMsg { kind: note|cancel|approve|pause|resume }`
appended to a file (control.jsonl) and POLLED by the executor.
- note -> folded into next agent turn (operatorQueue -> consumeOperatorNotes)
- approve -> releases plan-approval gate
- pause (drain-then-suspend) vs cancel (abort) kept DISTINCT
- approval gate TIMES OUT -> proceeds autonomously (loop never blocks on operator)

## Veto/interrupt pattern (conductor + agentswarm)
- Async interrupt that can STEER, not just kill: continue-with-guidance / skip-to-agent /
  stop / cancel (conductor KeyboardListener).
- Pause-vs-cancel at natural checkpoint/round boundaries (bmas checks abort between rounds)
  -> interrupt is cheap + resumable.

## Steering-as-state (bmas) — the cleaner correction model
Operator edits board-state salience (boost/retract/mark superseded) instead of injecting
raw prose into agent context. Correction = state edit, not text interleaving.

## Timeout -> autonomous fallback = HARD INVARIANT
agentswarm (planApproved timeout), ollama-harness (prompt timeout -> auto-deny),
conductor (--skip-gates): 'no operator answer' is a first-class path; headless/autonomous
run never hangs. Adopt universally.

## Approval-as-forwarded-gate
Approvals route THROUGH a control plane/supervisor, never straight to the agent
(bmas/Hermes, conductor human_gate).

## Global kill switch (ollama-harness)
One live-state singleton (KillSwitch, reason, persisted) every permission check reads ->
veto state can't drift across sessions. Directly parallels our 'two disconnected classifiers' bug.

## Declarative budget caps (subagent-router)
Cost/token caps per task/provider/model/day/session, warn|hard modes = non-interactive
backstop complement to human veto.

## THE FIELD GAP (our differentiation)
NONE of the 11 has a true persistent OPERATOR MODEL. All are stateless input or config-only
(subagent-router delegation_profile manifest + agentswarm swarm config = closest).
=> Persistent preference/authority/user-model layer that the typed control channel READS
is the open gap across the whole field. This is what sovereign-mirror / operator-mirror
should build. Aligns with t818612ba4b (operator-mirror user-model).

## Mapping to our operator_inbox fix
- Add typed control vocabulary (note|veto|cancel|approve|pause|resume) instead of raw-text
  vague-filter.
- _is_ambiguous must CONSUME intent classes from a unified classifier (see authority-model
  research t18aff67401) so veto/pause NEVER routes to Socratic clarify.
- Pause at checkpoint, cancel hard. Approval timeout -> autonomous.
- Feed persistent operator-model (the gap) from vetoes + corrections (learnability axis).
