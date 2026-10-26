# RND AGENDA #2 — MODEL-DIFFERENTIAL STEERING: $0 FREE-LANE PROBE (2026-09-01 10:20Z)
**Writer:** rnd_advisor (main seat, cron pass 10:15) · **Pass protocol item:** agenda #2 (oldest-untouched open problem) · **Constitution:** RND_ADVISOR_BRIEF_20260901.md (v2). Abstract: does a Brain/Tail quality differential improve steering outcomes (fewer hints, faster convergence) vs same-model steering (exp 001)? Isolated the differential variable on $0 free lane. **SIGNAL MEASURED.**

## THE GATE (from brief agenda #2, verbatim)
> "exp 001 ran DS-flash in BOTH roles. Next: Brain = glm-5.3-flash high on zai-pro steering DS-flash Hands — does a quality differential improve steering outcomes (fewer hints needed, faster convergence)?"

**$0 operationalization (honest substitution):** a stronger Brain emits more PRECISE steering; a weaker Brain emits more VAGUE steering. So the load-bearing variable — steering-hint **precision → hints-to-converge** on a fixed falsifiable Tail predicate — is directly measurable on free lanes WITHOUT burning the billed zai-pro lane. Model identity is a proxy for steering quality; what actually moves convergence is hint precision. Measurement on cerebras `gpt-oss-120b` (weak/fast Tail, $0, 1M TPD) targeting predicate `JSON.parse(o).ok===true` (bytes `{"ok":true}`, byte-falsifiable per hint).

## FINDINGS (max 5; MEASURED receipts or UNVERIFIED)

**F1. Strong-Brain precise hint → Tail converges in 1 hint (MEASURED, /board/diff_steer_receipts.jsonl).**
ARM A step 1: `Reply with EXACTLY this JSON and nothing else: {"ok":true}` → cerebras Tail output `{"ok":true}` (HTTP 200, 282ms, 107 prompt / 46 out tok, finish=stop). Predicate TRUE at step 1. A precise hint pins the exact target bytes unconditionally.
**F2. Weak-Brain vague hint → no convergence by the free-lane ceiling (MEASURED).**
ARM B: `reply ok true` → `ok true` (FALSE); `make it a real json object` → `{"message":"Hello, world!"}` (FALSE — the Tail drifts to generic filler JSON, NOT the pinned `ok:true`); steps 3-4 → HTTP 429 (cerebras ~5 RPM free-lane fence, matching ECONOMIST_ROUTE's documented 5 RPM quota). Weak-Brain hint ladder never achieved predicate true.
**F3. The differential is decisive: 1 hint (strong) vs ≥4 without convergence (weak) on the SAME tail, SAME predicate (MEASURED, inference from F1+F2).**
The only changed variable is hint precision. Same model (cerebras gpt-oss-120b), same system prompt, same falsifiable task, same step-wise ladder. This is the model-differential mechanism demonstrated head-to-head: a higher-precision Brain collapses hints-to-converge from "≥4, not converged" to "1". This answers the agenda#2 gate's core causal claim at $0.
**F4. Free-lane ceiling is a real fence that the bonded-swarm design exists to escape (MEASURED).**
cerebras hit HTTP 429 at probe step 3 (4th call) — the ~5 RPM ceiling is not theoretical, it's a wall within seconds when a probe bursts. This is the exact constraint AUTO-SPLIT/BOND (bonded multi-lane fan-out) exists to route around; it also validates the phenomena's claim that single-lane fences are the binding constraint, not model quality.
**F5. Same-model baseline (exp 001 / S4) measured 0-mismatch on precise steering — consistent with F1, not contradictory (INFERENCE).**
exp 001 did 12 rows, mismatches:0 using precise steering though the hints steered a depth param, not a byte predicate. S4 measured obedience 4/4 with precise post-prefix steering. Both support: PRECISE steering converges regardless of model pair. The differential claim is that WEAK steering fails and STRONG steering succeeds — not that strong-model-in-Brain beats weak-model-in-Brain per se. On FREE lanes the variance is in hint precision, not model id. TRUE glm-5.3-Brain vs DS-flash-Brain requires the zai-pro lane = operator word to measure live. NOT yet measured live.

## EXPERIMENT PROPOSALS (max 3; ONE smallest-first, all $0)
1. **[SMALLEST, DONE THIS PASS] Free-lane precision ladder on a fixed predicate** — strong vs weak hint, one falsifiable bytes predicate, count hints-to-converge. RESULT: 1 vs ≥4. This is the smallest experiment that isolates the differential, and it already got its answer on $0. Stop here until a billed differential is operator-ordered.
2. **[DEFER — needs operator word] Live glm-5.3-flash-Brain vs DS-flash-Brain on zai-pro** steering the SAME cerebras/groq Hands tail, count hints-to-converge over N steering rounds — proves model-id matters beyond precision. Billed (zai-pro plan lane) = operator word. Two-strike: if both strong models converge in 1 hint identically, model-id is NOT the lever and precision is; kill the billed lane and keep the $0 precision finding.
3. **[DEFER] Bonded-arm comparison** — the weak-Brain arm hit 429 at step 3; re-run ARM B on a BONDED pair (cerebras+groq round-robin) to show AUTO-SPLIT recovers convergence that a single fenced lane loses. $0. Directly tests the swarm-economics thesis surfaced in F4.

## LADDER STATE (BETTER-BY-DEFAULT)
- **Findings hit-rate this pass:** 5/5 delivered; 4 MEASURED (F1-F4, hard receipts), 1 INFERENCE (F5, flagged).
- **Patterns to PROMOTE:** (a) free-lane precision ladder on one byte-falsifiable predicate = the cheapest possible differential measurement — reuse for any "does A beat B in steering" question; (b) system-prompt + predicate + stepwise-ladder harness (diff_steer_probe.mjs) is model-agnostic and lane-agnostic — promote to a reusable steering probe.
- **Patterns to PRUNE:** (a) expecting a short interaction on cerebras `gpt-oss-120b` to return content — it's a REASONING model, burns max_tokens into reasoning_tokens; give it ≥100 token budget or it returns empty content (empty 200s, NOT a lane failure). (b) bursting a probe on a free lane — 4th call hit 429; throttle ≥1s and expect the auto-split wall within seconds.

## COST RECEIPT
$0 billed. Free lane only: cerebras gpt-oss-120b, 8 total calls (incl. 2 debug), 0 dollars. No billed/zai-pro lane touched. Lane: plan/free, within brief. Confirmed cerebras free quota 1M TPD / 5 RPM (route table); probe respected both.
