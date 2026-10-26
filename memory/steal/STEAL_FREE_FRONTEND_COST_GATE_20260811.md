# STEAL — FREE-FRONTEND-FIRST + API COST-GATE (protect credit) (2026-08-11)

Operator (hard): "only really one grok key is working... i only have ten dollars worth of credit...
i want you to use the supergrok front end" + "stop prompting me about it, do it from mem tools."

## The invariant stolen
FREE-FRONTEND-FIRST, COST-GATE THE API. Use the $0 browser front-end for grok; the paid token API is
GATED OFF by default and only runs on explicit override — so we never burn credit by accident.

## Self-steal (already owned)
- mag/browser_driver.ask(goal, surface="grok") — drives the supergrok/grok.com front-end over CDP
  (container browser seat ws://127.0.0.1:9222). The $0 surface.
- The paid API (call_grok) is the costly path — gate it.

## Adaptation (code, mag/grok_rightsize.call_grok_free, verified get_errors clean)
1. Try browser_driver.ask(goal, surface="grok") first -> $0 answer.
2. If front-end fails -> check GROK_ALLOW_PAID env or force_paid. By default NOT allowed ->
   return {gated_paid: True, error: "...protecting credit"}. Does NOT call the API.
3. Paid call_grok only when explicitly allowed (force_paid=True or GROK_ALLOW_PAID=1).

## Honest verification status
- VERIFIED: the gate (won't spend by default) — the code returns gated_paid:True before any API call.
- UNPROVEN: the supergrok front-end actually connecting/answering over CDP — needs the container
  browser seat up + the surface reachable. Test before claiming the free path works.
- No runtime test yet (operator steers to mem tools/ghost, terminal route cancelled).

## Lesson
Free surface first, gate the paid path, prove the free path actually answers before trusting it.
Trust bytes, not reports.
