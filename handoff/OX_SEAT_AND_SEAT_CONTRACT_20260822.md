# OX SEAT — live + the seat-contract it designed (2026-08-22)

## The seat is live and free
- `mag/ox_seat.py` — BOUNDED chat wrapper over `stealth/ox-alpha` (OpenRouter, free frontier
  reasoning seat). Reads key from `.env`. Cost reported per call. T2+ public only (retained-log).
- Verified: HTTP 200, reasoning superb, `cost: 0`, `cached_tokens: 64/94+` (shared-prefix proof #3).
- `OPENROUTER_MODEL=stealth/ox-alpha` in `.env`; L1 lane points at it; `health.check_openrouter` ok.
- WHY a wrapper: the stock `models.providers.chat_openrouter` does an UNBOUNDED blocking call that
  HANGS on ox-alpha's heavy reasoning. The bounded wrapper (max_tokens + timeout) makes it usable.

## THE REAL FINDING about ox-alpha as a seat
- It is an EXTREMELY heavy reasoning model. Given 500 and even 1600 max_tokens, ALL of it went to
  `reasoning` and `content` stayed null (`finish_reason: length`). Final content only appears after
  reasoning completes — needs a large budget (thousands of tokens) + accepts latency.
- IMPLICATION: for design/architecture tasks, the REASONING STREAM IS THE DELIVERABLE (read
  `reasoning`); for content-bearing answers, give a big `max_tokens` (e.g. 3000-5000) + long timeout.
- This is WHY the unbounded call hung: heavy reasoning + no bound = socket hang. Always bound it.

## The seat-contract ox-alpha designed (its own answer, reasoning stream) — banked
1. ROUTING: escalate on FAILURE, never on task type. Triggers: NO_HANDLER, HANDLER_ERROR (after N=1
   retry), LOW_CONFIDENCE (<0.7), CONFLICT (two handlers disagree), AMBIGUITY_FLAG. Never escalate on
   cache hits / arithmetic / schema-valid transforms. Anti-pattern: don't route by keyword ("complex")
   — that causes drift + cost creep.
   - "The LLM proposes; determinism disposes." The seat's answer must pass validation and be committed
     by the deterministic core (sovereignty stays with the core).
2. QUOTA (minimal): per-epoch token/call cap (e.g. 50/day); max 1 escalation/task, max 2 w/ retry;
   priority P0 always, P1 at 50% budget, P2 dropped <20%; exponential backoff on 429 -> defer to
   queue (`deferred_reasoning`), never block the swarm; circuit breaker (3 fails -> open T min);
   hash(prompt+ctx) response cache — same question never costs twice.
3. REASONING-CONTINUATION: append-only reasoning ledger keyed by task_id {turn, prompt_hash, decision,
   rationale_digest, artifacts}. Carry forward: invariant goal + committed decisions + open questions.
   Drop raw transcripts; cap context ~2k; summarize older turns DETERMINISTICALLY (extractive, $0).
   Continuation BLOCK at end of each response: {next_action, assumptions[], unresolved[]} -> seed of
   next turn. Ledger beats the model on conflict (deterministic sovereignty).
4. SMALLEST FIRST STEP (~50 lines): one router with ONE trigger (NO_HANDLER); one echo test task that
   fails matching -> escalates with a fixed template -> validates response against a JSON schema ->
   commits to ledger; assert cache hit on 2nd identical call costs zero.

## Standing
- ox-alpha is a free-on-demand SEAT, not a permanent default ("use it while you can"). Bound every
  call. T2+ public only. The reasoning stream is a first-class deliverable for design work.
- The seat-contract answer above directly answers swarm thread sw-a59cb9b504 (wire the free seat as
  the escalation brain) — merge with whatever the swarm files back.
