# INTAKE CARD — "How Microservices Communicate" infographic (2026-09-04)

> **[AUDIT-TYPED 2026-09-08]** status: PROSE · claims: the fleet already runs the infographic's reliability kit (breaker = dispatch breaker, idempotency = claim CAS fix), with real gaps only in timeout/fallback organs and contract versioning — SUPPORTED (panel-by-panel mapping to named filed organs) · falsifier: the named counterpart organs (claim CAS fix, dispatch breaker) are not found in repo/board, or a gap item ships as an organ contradicting "not tonight"

**Paste**: https://x.com/AIwithSumit/status/2095755417683112207
**Score**: 8/25 — **REMEMBER** (honest re-find: the fleet already runs this
textbook; repetition-is-emphasis)

## Receipt
Interview-prep infographic, 8 panels: sync vs async comms, message broker vs
event bus, service discovery, reliability patterns (retry / circuit breaker /
timeout / fallback / idempotency), security, observability. Correct but
standard — no novelty for us. Interview-prep genre = content-shaped-like-
teaching, zero new surface.

## Why it still earns a card: the fleet passes its own exam
Mapping the panels onto our organs — this is a self-check we didn't plan:
- **Circuit breaker** = the dispatch circuit breaker born from the board
  runaway incident (filed 09-03).
- **Idempotency** = EXACTLY the claim-organ CAS fix (the split-brain bug is
  an idempotency violation: repeated requests causing duplicate actions).
  Industry panel 6 names our Leg-1 shopping list verbatim.
- **Event bus / broker** = room.jsonl + steer bus; **discovery** = seat
  registry; **observability** = flight recorder v0 + event_stream typed rows;
  **secrets** = loopback-only + never-echoed law.
- Gaps the panel names that we DON'T have as code: **timeout/fallback as
  first-class organs** (we do ad-hoc backoff), **contract versioning**
  ("keep contracts stable and versioned" — our schema drift is tribal).

## Routing
1. **REMEMBER**: panel 6 = industry confirmation that Leg 1 (claim organ =
   idempotency, dispatch breaker = circuit breaker) is the standard kit, not
   our invention. Cite in the Leg-1 gate argument.
2. **REMEMBER**: two named gaps for the someday-shelf — timeout/fallback as
   organs, contract versioning. Not starved, not tonight.
3. **No BUILD.**
