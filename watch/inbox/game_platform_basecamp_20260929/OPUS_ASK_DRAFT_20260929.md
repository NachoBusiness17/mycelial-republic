# THE DELIBERATE ASK: CLAUDE OPUS 5.5 PROTOTYPE (DRAFTED 2026-09-29, NOT FIRED)

Status: DRAFT, banked. Firing is an operator decision (driving ladder: Anthropic keys UNFUNDED as of 2026-09-28; one Opus build run is a funded-tier exception the operator names explicitly). The research lane (smart-to-dumb delegation dive) may amend this ask before it is ever sent; amendments append, never rewrite.

## WHY ONE ASK (the doctrine)

The estate's deliberate-ask law: strong asks = frozen context + small ask + output contract + quantize target, because frontier attention is the scarcest resource the estate rents. One shot, fully loaded, self-contained for a cold model. No follow-ups. The prototype comes back judged by our gates, not by vibes.

## THE ASK (verbatim draft, to paste)

---

You are building a working prototype for a small research lab. You get no follow-up questions, so everything you need is in this brief. Build it complete enough to run, test, and extend.

## WHAT WE ARE

We run a fleet of cheap local models: a 7B-class assistant, a 2B janitor, and a family of sub-1GB decision models (text to yes/no, choice, or score, with calibrated probabilities) served behind OpenAI-compatible endpoints. These endpoints are our "clones": to any client they look like ordinary LLM APIs. We also hold metered access to frontier models (Opus-class, plus mid-tier flash models), scarce and rationed by hard cost caps. 95% of our tokens are local; the frontier exists for judgment: design, review, escalation.

Our problem: orchestration code currently hard-codes which model it talks to. We want ONE intelligent layer between all callers and all models, and we want that layer to route on MEASURED capability, not marketing labels.

## BUILD

A Model Context Protocol (MCP) server, TypeScript or Python (your call; justify in one paragraph), called **gps-mcp**, plus a Kubernetes deployment shape. It exposes MCP tools to any MCP client:

1. `ask(task_shape, payload, constraints)` — the single entry point. gps-mcp decides which endpoint answers: a local clone, the flash tier, or (only when justified) the frontier tier. Constraints include max_cost_usd, max_latency_ms, min_confidence.
2. `report_capability(model_id, task_shape)` — returns the measured pass-rate, sample size, last-measured date, and cost for that model on that task shape, from a capability ledger gps-mcp maintains.
3. `record_verdict(model_id, task_shape, verdict, evidence_hash)` — callers report ground-truth outcomes; the ledger updates. Routing decisions must always be traceable to ledger rows, never to static config.
4. `cascade(task_shape, payload, constraints)` — tries the cheapest tier whose measured pass-rate on this task shape exceeds a threshold (default 0.85, caller-overridable); on low confidence (the model's own calibrated probability below a caller threshold) it escalates one tier and re-asks, attaching the prior answer as context. Max three tiers. Every cascade returns the full decision trace: which tiers tried, why, what each cost.

Routing rules, in priority order: (a) hard constraints filter; (b) measured pass-rate from the ledger; (c) cost; (d) calibrated confidence of the candidate's own output, when the endpoint provides probabilities. If a task shape has no ledger history, route to the flash tier and mark the decision `exploration: true`.

## NON-NEGOTIABLES

- Every routing decision emits a JSONL receipt row: {ts, task_shape, chosen, considered, reasons, cost_usd, confidence, exploration}. Append-only file. This lab runs on receipts; a decision we cannot audit did not happen.
- The capability ledger is a plain SQLite file with a documented schema. Seed it with a fixtures script containing at least 6 synthetic models x 5 task shapes with plausible varied pass-rates, so your tests and our first runs work offline with zero real API calls.
- All external endpoints (frontier, flash, local clones) are configured via one config file with OpenAI-compatible base URLs, so our local endpoints (and our test doubles) are indistinguishable from real providers.
- A test double endpoint mode: an in-process fake server that returns deterministic canned answers with configurable confidence and latency, so the entire system is testable with $0 and no network.

## DELIVERABLES

1. The gps-mcp server + ledger + receipts + config, as a complete repo.
2. Tests proving: constraint filtering, ledger-driven routing, cascade escalation with decision traces, receipt integrity, and the exploration rule for unknown task shapes. Run them; tell us the real pass count.
3. Dockerfile + a k8s Deployment+Service manifest (single replica is fine; we run a small cluster).
4. README: how to run it, how to point it at real endpoints, how to read the ledger, and an honest "what this prototype deliberately does not do" section (multi-tenant, auth, streaming, retry storms, etc.) — we respect scope honesty more than feature lists.
5. A section called IF WE GROW THIS: the three highest-leverage next builds, ranked, one line each.

## QUALITY BAR

We are an instrumentation lab: we trust bytes, not reports. Prefer boring, readable code with tests over clever code without. No em-dashes in any file or comment (house style, verifiable). If you must choose between a feature and a test for an existing feature, choose the test.

---

## WHY THIS ASK SHAPE (the theory, for the estate's own record)

- Context pack first (who we are, what we run) because a cold Opus knows nothing about the clones or the metered-frontier economics; the ask trades tokens for not having follow-ups.
- The deliverable is SMALL and testable, not "build our platform": one MCP server, one ledger, one cascade. The frontier's marginal token goes to architecture and code quality, per the delegation theory the research lane is verifying: frontier designs, cheap fleet executes. If that research comes back "frontier should judge, not build," this ask shrinks to a review-of-our-own-spec ask instead — the amendment is one sentence.
- The receipt row requirement imports the estate's soul into the artifact: anything gps-mcp does is auditable, which is the property the whole platform claims to sell.
- Test-double mode is the anti-window-dressing clause: it makes the prototype verifiable for $0 before we ever point it at a live endpoint. Untested access is not access.
- The "IF WE GROW THIS" section makes the prototype pay rent as a design document even if we never deploy it.

## FIRING PROTOCOL (when the operator says go)

0. **DOGFOOD GATE (operator law 2026-09-29: "remember to dogfood our asks" — MANDATORY, before any funded firing):** the ask itself is run through the estate's own machinery first, on the tiered ladder: (a) LOCAL/FREE pass — the ask verbatim through a local seat (gemma/glm-flash via stealth lane or opencode headless; FL-9/FL-10 briefs) catching ambiguity at $0; (b) CHEAP BURN pass — gophers through prime tier attacking the ASK not the subject (G6 ask-forging pattern, $0.07 measured); (c) integration — every caught ambiguity fixed in the ask BEFORE frontier money fires. An ask that has not been dry-run is not ready to fire, whatever the deadline. The cheap seat should FAIL visibly where the ask is hard — if gemma answers it comfortably, the ask is too easy for the frontier. (Honest application note 2026-09-29: the six gopher asks fired WITHOUT pass (a) — the exact miss this gate now forbids.)
1. Research lane verdict read; amend if needed (append amendments below).
2. Estimate: this ask is roughly a 2-4k token brief; one Opus build run at typical agent-loop lengths. Name the budget cap before firing.
3. Fire once. Judge the return with the estate's gates (does it run? do the tests pass? receipts real?), never by prose quality.
4. Bank the artifact under corpus/steal/ or a new repo; the gps-mcp joins the platform's L2 service list (the smart GPS between frontier and clones).

## AMENDMENTS (append-only)

- AMENDMENT 2 (2026-09-29, baseline + differentiation lanes): the ask is now THREE-LAYERED, data-tuned. (a) BASELINE ATTACHED: the estate ran its own full-depth ractor panel first (watch/inbox/gps_baseline_ractor_20260929/BASELINE_SPEC.md + BASELINE_QUALITY.md: 3 blind seats, judge, synthesis, honest weak points) — the fired ask INCLUDES the baseline and asks Opus 5.5 to BEAT IT, not derive from scratch; the baseline's section 10 IS the diff contract (if the return does not beat our baseline where the baseline admits it is weak, we did not need Opus). (b) CLAUDE-SPECIFIC EDITS from the differentiation brief (watch/inbox/game_platform_basecamp_20260929/CLAUDE_DIFFERENTIATION_20260929.md): XML tags with context-first/ask-last (+30%, official); effort set to xhigh/max explicitly (default medium = 7 index points lost); mandatory hostile second pass with anti-sycophancy framing ("attack this as a hostile implementer; disagreement is the deliverable; do not validate my framing" — sycophancy is causally documented); verbosity contract (section caps, tables over prose, no preamble — "very verbose" is an independent AA measurement); falsifiable tests-first acceptance gates + an explicit "flag any instruction in this brief you believe is wrong" clause (exploits the documented instruction-error catch; neutralizes eval-suspicion by making honesty the deliverable). (c) AVOID shapes: no exploit/attack vocabulary (classifier redirect), systems/contract-shaped not experimental-science (TB-Science is Claude's one measured loss), no prefill (removed 4.6+), no follow-up turns planned (multi-turn 39% degradation — the one-shot stays one-shot). Target corrected: Opus 5.5 ($4/$20 per M).


- AMENDMENT 1 (2026-09-29, research-lane verdict, confidence 0.7): **INVERT THE ASK.** The delegation dive found: (a) SuperScout's own ablation — "the handoff rather than the routing decision carries the result" (arXiv:2608.04804); (b) routing/gateway plumbing is commodity (LiteLLM + KServe/LWS/InferencePool implement ~90%; frontier tokens re-deriving documented knowledge = flagged waste by Anthropic's own guidance); (c) Anthropic productized smart-designs/dumb-executes (OpusPlan: Opus plans, Sonnet executes) and their economics line "upgrading the model beat doubling the token budget" defines the frontier role as judgment-at-decision-points. THEREFORE the fired ask (when funded) becomes: Opus designs the CAPABILITY-LEDGER SPEC + VERIFICATION-GATE CONTRACT + escalation-policy decision boundaries + adversarial critique of the whole design — tests-first, output-contract-framed — and the mid-tier/local fleet builds the gps-mcp plumbing against LiteLLM/KServe from that spec. The original build-ask is retained above as the historical draft; it is NOT the fired version. The research brief is banked at watch/inbox/game_platform_basecamp_20260929/DELEGATION_RESEARCH_20260929.md.


- AMENDMENT 3 (2026-09-29 night, G6 ask-forging gopher, $0.06): the dogfood gate's first completed loop. G6 (qwen-prime) audited the ask for vagueness and produced five missing lines, adopted: (1) TASK_SHAPE typed definition (JSON object: domain enum + complexity 1-5 + modality; ledger keyed on model_id/domain/complexity; anything else = 400); (2) EXPLORATION LIFECYCLE (no-row -> flash + exploration receipt + null-rate ledger row; promotion to normal routing at sample_size >= 3 via record_verdict count); (3) CONFIDENCE CONTRACT (confidence = float in [0,1] in a custom response field; endpoints without it = confidence null, rule (d) skipped; default cascade threshold 0.70, receipts log null honestly); (4) TEST ACCEPTANCE PREDICATE (>= 20 named test_ functions, single-command runner, output machine-parseable - replaces "tell us the real pass count"); (5) the fifth line in GOPHER_BURN_output3_healthy_20260929.jsonl under G6. Full G6 table (vague terms, prose-where-table-belongs) banked same file. Dogfood ledger: fires 1-2 failed ($1.44 tuition: reasoning burns max_tokens - the LESSIG RAILS bug relearned on Nous primes; fixed by reasoning:{max_tokens:6000}); fire 3 healthy 6/6 for $0.36. Total burn $1.80 of $20 authorized.
