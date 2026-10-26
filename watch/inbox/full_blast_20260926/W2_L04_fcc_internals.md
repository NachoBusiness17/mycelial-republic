# W2-L04: free-claude-code source internals (wave 2 retry, verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore W2-L04) · **Class:** RECEIPT / steal
**Closes:** wave-1 lane L04 (1302 death). 16 fetches, all API/raw.githubusercontent, no search. Layout: FastAPI-style local proxy in `src/free_claude_code/`, layered api/ -> application/ (routing/execution) -> providers/ (admission + adapters) -> config/. All paths relative to github.com/Alishahryar1/free-claude-code/blob/main/.

## Fallback implementation (two layers)

**Layer A, static route + dynamic failover** (application/routing.py, application/execution.py): stateless `ModelRouter._fallback_targets` builds an ordered tuple from settings.model_fallbacks (primary deduplicated). `ProviderExecutor._stream_candidates` loops (primary, *fallbacks), deep-copies the request and swaps the model per candidate. FAILOVER RULE: advance only if (a) ExecutionFailure raised while opening or on first chunk read, (b) `not candidate_committed` (ZERO chunks emitted to the client yet), (c) candidates remain. Once any chunk commits, a mid-stream failure aborts: no mid-stream provider swap. Per-chunk progress deadline (stalled provider -> 504, retryable=False); time spent opening a candidate is added back (init has its own budget).

**Layer B, per-provider admission** (providers/admission.py, the strongest file in the repo): `ProviderAdmissionController` defaults rate_limit 40/60s, max_concurrency 5. StrictSlidingWindowLimiter permit before every physical attempt; semaphore bulkhead per ProviderAttempt. **Recovery episode (their circuit-breaker equivalent):** first shared transient failure opens a `_RecoveryEpisode`; ONE execution becomes episode.leader owning the sole half-open probe, all others coalesce as waiters on a condition (no independent retries). Probe success closes the episode; failure reschedules backoff. After 5 transient attempts (UPSTREAM_TRANSIENT_TOTAL_ATTEMPTS), `terminal_until` cooldown: waiters get ProviderRecoveryExhausted immediately (zero traffic to the dying provider) until the timestamp passes. Backoff base 2.0 x 2^(attempt-1) capped 60s + jitter, floored at parsed Retry-After.

**Failure taxonomy** (core/failures.py + providers/failure_policy.py): FailureKind StrEnum (INVALID_REQUEST, CONTEXT_WINDOW_EXCEEDED, AUTHENTICATION, PERMISSION, RATE_LIMIT, OVERLOADED, TIMEOUT, UPSTREAM, UNAVAILABLE); frozen ExecutionFailure(kind, status, message, retryable). One retryability rule: retryable iff status == 429 or 500-599; auth/permission/context-window/invalid-request never retried; message markers ("rate limit", "resourceexhausted", "overloaded") mapped to statuses. 502/503/504 normalized to 529.

## Quota-storm mitigation inventory

Sliding-window limiter gating every physical call; concurrency bulkhead; leader/follower probe coalescing (N concurrent failures on a provider produce exactly ONE retry probe; the anti-thundering-herd core); exponential backoff + jitter + Retry-After floor; terminal_until hard cooldown; monotonic generation tokens so stale permits cannot act after an episode resets. NOT present: cross-provider quota budgeting, Retry-After propagation to clients, per-model cooldowns (cooldown is per provider controller).

## Adapter interface + catalog

`BaseProvider` ABC: four abstract methods (cleanup, list_model_infos, stream_messages Anthropic-SSE-out, stream_responses OpenAI-Responses-out); NO health-check method, admission owns health. Adding a built-in provider = ProviderDescriptor in config/provider_catalog.py + logo + an OPENAI_CHAT_PROFILES profile or a _load_<name> factory; a module-level assertion enforces exactly-one-construction-owner per provider id or import fails. Model cache: generation-copy pattern, NO TTL, invalidation via clear()/set_available_providers(); configured refs win collisions; startup readiness gate waits up to 30s for first discovery instead of serving a cold catalog.

## The three port-worthy mechanisms (with paths)

1. **Coordinated recovery episode + terminal cooldown** — providers/admission.py (`ProviderAdmissionController`, `_RecoveryEpisode`, constants above). One leader probe per failing provider, coalesced waiters, Retry-After-aware backoff, cooldown timestamp that short-circuits later ladder entries.
2. **Commit-semantics fallback chain** — application/execution.py `_stream_candidates` (failover only while nothing committed; per-chunk progress deadline) + application/routing.py `_fallback_targets` (stateless order, model swapped per candidate). Separates "what order to try" from "how to fail over".
3. **Typed failure taxonomy with one retryability rule** — core/failures.py + providers/failure_policy.py. Single decision point for same-provider retry vs next-rung vs abort.

## Seat note (crosswalk to OmniRoute L01)

FCC and OmniRoute independently converged on the same doctrine from opposite sides: FCC's recovery episode (one probe per dying provider, others coalesce) is OmniRoute's "lazy recovery, next real request is the probe" plus anti-thundering-herd. For the fleet: adopt leader/coalesced-waiter probing (FCC-shaped) as the runtime mechanism, and OmniRoute's 429-never-trips-breaker classification as the policy. Both are pattern-steals; FCC is AGPL-3.0 so code stays read-only for us, MIT-gated OmniRoute docs likewise pattern-only for the Python port.
