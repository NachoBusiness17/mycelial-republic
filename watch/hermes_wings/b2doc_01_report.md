# hermes docs b2 wing 01 (docs/billing-lifecycle.md)

via seat-b1 beat ext-c2ec182c6a folded=True

CODE ARCHAEOLOGY REPORT — watch/hermes_wings/b1_docs/b2doc_01.md

WHAT IT DOES
The file maps every billing/subscription state shape the gateway serves to what the terminal renders, and every typed refusal/error code to its user-facing copy and recovery action, across topup.ts, billingOverlay.tsx, subscriptionOverlay.tsx, and cli.py. It fixes poll cadences (charge settlement: 2s interval, 5-min cap; post-upgrade confirm: 2s, 15 attempts) and routes unknown codes to a default branch that still renders the server's message.

DESIGN PATTERNS
- Exhaustive dispatch table with default fallthrough — any unknown error/status/reason code still shows the server message, never a blank toast or crash.
- Fail-closed transport handling — a failed billing.state RPC (.catch(ctx.guardedErr)) opens nothing and assumes no state.
- Ambiguity-preserving failure — mid-poll revocation or transport loss reads "unconfirmed — check balance", never "failed"; reason is checked before status.

RISKS
- Hidden mutation of shared state: renderBillingError clears the billing overlay immediately on remote_spending_revoked/session_revoked — a side effect inside an error renderer.
- Duplicate scheduler: two independent 2s pollers — pollCharge in topup.ts and the UPGRADE_CONFIRM apply-poll in ResultScreen.
- Single point of failure: the "no state falls through" guarantee is maintained by hand across four files; this doc is its only enforcement.
