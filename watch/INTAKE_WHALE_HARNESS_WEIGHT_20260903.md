# INTAKE — WHALE: joint weight+harness optimization (Yoonho Lee X thread)

Date: 2026-09-03 | Intake seat: zcode (evaluation sub-agent)
Item: https://x.com/yoonholeee/status/2095556379520188444 (posted 2026-09-03T16:55Z)

## ITEM
X thread by Yoonho Lee (@yoonholeee, KRAFTON × KAIST × Stanford) announcing
**WHALE: Weight–Harness Alternating LEarning** — a block-ascent recipe that alternates
(1) fine-tune model weights with harness frozen (online rejection-sampling FT on
verifier-accepted rollouts), and (2) search the harness with weights frozen
(Meta-Harness as agentic proposer, Claude Opus 4.7 proposing). Core claim:
"whichever component you hold fixed is the one that caps the system."
Blog: krafton.ai/blog/whale/ | Paper: arXiv:2609.00196 (submitted 2026-08-31) | Code: github.com/krafton-ai/WHALE (public, CC BY 4.0)

## RECEIPTS
Fetched and verified:
- Root post + full 12-tweet author thread via web_reader (author follow-ups captured:
  headroom answer to Meta-Harness critics, adaptive variant, scaling bet, future
  directions incl. "co-overfits to one good harness" and training models to write
  their own harness).
- krafton.ai/blog/whale/ (WebFetch, after t.co 301 redirect): numbers confirmed —
  WHALE (0.6, 6) beats best single-component baseline by 7.67–24.38 pts and the
  prompt-restricted FST control by 4.15–13.00 across SearchQA / Math(+Python) /
  Chess Puzzles on Qwen3.5-2B/4B, mean@8. SearchQA harness-dominant: harness search
  alone matched weight-only peak with 5.79% of the rollouts (30,720 vs 530,432);
  retrieval accuracy 26.88% → 60.61%. Math model-dominant: harness-only 0.42% vs
  15.42% after weight updates; truncation 95.83% → 30.83%. Beats stagewise
  weight-then-harness by 5.32 (SearchQA) / 9.16 (Math) pts. Disclosed limitations:
  schedule sensitivity ((0.2,2) Math run destabilized, stopped), too-large budgets
  regress to stagewise failure, adaptive variant trails best hand-tuned Math by 1.87.
- arXiv:2609.00196 abstract (WebFetch): consistent with blog; authors Haechan Kim,
  Yoonho Lee, Gisang Lee, Chelsea Finn, Kangwook Lee.
- GitHub repo existence via search receipt (repo not fetched).
Not retrievable: third-party replies / community notes — X reader returned the author
thread only; searches of Reddit/HN/alphaXiv discussions found no criticism indexed yet
(paper is 3 days old). Pushback status: none found ≠ none exists.

## SCORE
F:5 P:5 C:4 W:4 N:5 = 23/25 — BUILD NOW

## READ (the honest why)
The fleet independently converged on this thesis from the other side. Our harness
doctrine (docs/ref/HARNESS_SPEC.md, event.v1 stream, governor-sole-mutator, files-as-
harness) is harness-only optimization — and WHALE's headline finding is that
harness-only plateaus (their SearchQA curve, and our own MAX_DISTILL epoch 1
INCONCLUSIVE with A=B=D floor effects: harness moved, weights never did). Their Math
result — harness search yields 0.42% until a weight update unlocks 15.42% — is the
external receipt for WHY the QLoRA campaign and Rocinante exist. Better: it hands the
Sep 3–20 campaign a concrete amendment. The campaign synthesis currently plans
stagewise (harness now, weights post-Oct-27); WHALE's controlled result says
interleaved small weight updates beat stagewise on both accuracy and rollout cost —
so the campaign should schedule harness-search windows BETWEEN QLoRA stages rather
than before all of them, and the adaptive-WHALE patience rule (switch phase when the
phase's own signal plateaus) is a free candidate law for the governor, which already
does plateau detection on lanes. Cost is honest: the steal itself is pennies (public
code, CC BY); real runs need CUDA we do not have until Rocinante (Oct 27) — that is
the only reason W and C are not 5. Skeptic's note kept attached: results are
authors' own, on 2B/4B models, 3 domains, mean@8, no independent replication; the
"will scale to large post-training runs at ~1% rollout budget" line is the author's
own bet, stated as a bet.

## TRI-STATE
- WHALE method + reported numbers: **Supported** (blog + arXiv abstract fetched and
  cross-consistent; code public). External validity on our stack: **Unproven**.
- "Either component can be the bottleneck; alternating beats stagewise": **Supported
  as reported** (controlled comparisons in paper), **Unproven** at fleet scale.
- Scaling bet (~1% budget in large post-training runs): **Unproven** (author's bet).
- Adaptive variant competitive without phase tuning: **Supported** (with disclosed
  1.87-pt Math gap).
- Community pushback / reply overturns: **Unproven** — none indexed yet; replies not
  retrievable through the reader.

## VERDICT
BUILD — band BUILD NOW (23/25). Build the steal now (free); execution is
Rocinante-gated and that gate is already the plan, not a blocker to the design work.

## ROUTE (wire)
1. File as a steal note alongside watch/STEAL_FLOW_REASONING_MODELS_20260903.md
   (pattern precedent: vendor-external confirmation of a fleet doctrine).
2. Amend watch/CAMPAIGN_SYNTHESIS_20260903.md stage design: interleave harness-search
   windows between QLoRA stages (WHALE's central result) instead of pure
   harness-now-weights-later stagewise; adopt adaptive-WHALE patience rule as the
   governor's phase-switch heuristic candidate.
3. Pin as Rocinante's first-training-run template (Oct 27): WHALE recipe on Ox Alpha
   GLM-5.3-flash public weights / Saleis LoRA line, with our gauntlets as the
   verifier and trajectory harvests (openclaw_traj.jsonl, rib logs) as rollout feed.
4. Log against MAX_DISTILL epoch 1: WHALE explains the floor effects (frozen weights)
   — epoch 2 design should alternate, not re-run weights-only.
5. No wire to salons/rooms yet — methodology receipt first, salon pass only if the
   operator wants the interleaving law debated before it touches the campaign.

## DOGFOOD
- INVARIANT PASS: reinforces receipts-over-claims (this card), cheapest-lane routing
  (read free, judge premium, run sovereign-local post-Oct-27), and sacred-cows-not-
  legacy-shit (MAX_DISTILL INCONCLUSIVE re-read as the frozen-weight cap, not garbage).
  Extends map-precedes-territory: map (harness) edits plateau without territory
  (weights) movement — the two must alternate.
- STOCKFISH PASS: lane = watch steal + campaign synthesis amendment (free lanes);
  premium judgment = one operator GO on amending the live campaign; execution lane =
  Rocinante CUDA after Oct 27. Placement succeeded on all three — no orphan opcode.
