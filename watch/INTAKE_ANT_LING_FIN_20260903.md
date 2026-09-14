# INTAKE — Ant Ling open-sources Ling-3.0-flash-Fin + FinFIRST benchmark (2026-09-03)

## ITEM
https://x.com/AntLingAGI/status/2095533696808051001 — X post by Ant Ling AGI (Ant Group's
open-model team, aka InclusionAI), posted 2026-09-03 ~15:25 local. Open-source release of:
1. **Ling-3.0-flash-Fin** — finance-enhanced model on the Ling-3.0-flash base; claimed
   124B-total / 5.1B-active MoE, 256K context, weights on Hugging Face
   (inclusionAI/Ling-3.0-flash-Fin) + ModelScope; free API on OpenRouter for ~1 month.
2. **FinFIRST** (Financial Information Retrieval, Sourcing and Traceability) — expert-built
   benchmark for financial search agents, co-designed with CICC (China International Capital
   Corporation) investment-banking staff; claimed V1 = 123 expert-authored tasks, 701 atomic
   criteria, 12,300 rubric points; evaluated under a unified ReAct agent with web search /
   visit / python tools.

## RECEIPTS
- Root post + first follow-up FETCHED via web_reader (x.com 403 bypassed — full text +
  thread retrieved). Engagement: 77K views, 115 bookmarks, 4 quotes — modest traction for
  a "major" open release.
- Replies captured: one reply (Robin @heyrobinx) = pure hype ("solid choice… practical,
  transparent, and production ready"). No pushback, no community notes on the root thread.
- Corroboration sweep: TechNode (08-28 launch announcement, "open-source next week"),
  IT之家, PingWest, ifeng (50+ finance professionals involved in FinFIRST design), AIbase;
  independent provider listings already live: OpenRouter (free tier) and Novita —
  corroborates the open-weights/free-API claim independently of the vendor.
- Critique search: NO methodological critique, rebuttal, or leaderboard challenge found
  (searched EN + CN). Nearest peer work: FinSearchComp (arXiv 2509.13160, has open
  OpenReview criticism threads), Finance Agent Benchmark (arXiv 2508.00828), SnorkelFinance,
  Fin-Eva (Ant's own earlier benchmark). FinFIRST is 1 day old — critique vacuum expected,
  not evidence of quality.
- Corpus sweep: memory index + watch/ checked. ZERO finance-domain arcs. Adjacent organs:
  INTAKE_RUBRIC_20260903 (rubric-graded evals), fuel_feed FREE_LANES (provider swapping),
  QLoRA campaign (training, not finance), campaign salon eval harness. Degraded-lane note:
  zai-lite token EXPIRED 401 + openclaw lane 3x transport-dead as of 09-03 — the free-lane
  roster has holes TODAY.

## SCORE
F:3 P:2 C:4 W:3 N:2 = 14/25 — BUILD WINDOWED

- FIT 3: The OpenRouter free endpoint bolts onto the existing FREE_LANES swap-by-model
  pattern (no new substrate — fuel_feed already does provider pinning). The rubric-graded
  benchmark methodology maps onto intake/rubric + salon eval organs. Raw weights would need
  new inference substrate (not proposed).
- PULL 2: Finance domain advances nothing live (no trading/finance arc). Only pulls: free
  -lane diversification (serves a standing law) and rubric-decomposition as coverage-thesis
  datapoint. QLoRA Stages 2-5, shadow fields, Rocinante untouched.
- COST 4: Reading the benchmark = free. Free OpenRouter tier = pennies. Open weights = no
  license surprise reported. Cost only appears if we build a lane adapter (~one session).
- WINDOW 3: Not feeding a starved lane this instant, BUT the free-lane roster is degraded
  right now (zai-lite 401, openclaw dead) — a second free provider is a real fallback
  candidate for the next lane audit, not someday-docket.
- NOVELTY 2: Finance-tuned open MoE is a crowded pattern (FinGPT, FinRobot, FinSearchComp,
  Fin-Eva). The rubric-point-count transparency (12,300 graded points) is mildly fresh;
  the vendor-grades-its-own-model shape is not.

## READ
This is a competent vendor launch, not a signal the fleet needs. The model is a small-active
MoE (5.1B active) with a free tier — which makes it a plausible spare tire for the swarm's
bulk lanes, and that is the only reason it scores as high as it does. The benchmark is the
interesting artifact: decomposing 123 tasks into 701 atomic criteria and 12,300 graded rubric
points is exactly the continuous-coverage move our intake/rubric and QLoRA eval organs are
moving toward, and it comes with CICC's expert-authoring pedigree. But it is a self-benchmark:
the vendor wrote the rubric and the leaderboard, released it day-one alongside its own model,
and no third party has replicated anything — receipts-over-claims says treat all accuracy
numbers as marketing until an outside eval lands. Domain misalignment caps it: we run no
finance arcs, so even a genuinely good model here has no organ to serve. Hold as a named
fallback and a methodology note; do not build.

## TRI-STATE
- "Open-sourced Ling-3.0-flash-Fin + FinFIRST" — **Supported** (post fetched; TechNode,
  IT之家, PingWest, ifeng; independent OpenRouter/Novita listings live).
- "124B total / 5.1B active MoE, 256K context" — **Supported** (corroborated across
  OpenRouter, Novita, Reddit r/machinelearningnews; originally vendor-sourced).
- "FinFIRST V1: 123 tasks / 701 atomic criteria / 12,300 rubric points, CICC-designed" —
  **Unproven** (vendor self-report; outline corroborated — CICC partnership, 50+ finance
  professionals — but counts unaudited; zero third-party replication found; no community
  notes found; the only captured reply is hype).
- "Model performance/leaderboard results" — **Unproven** (self-benchmark; standard
  ReAct+tools eval harness is a fair design, but the grader and the graded share a vendor).
- Reception strength — **Supported thin**: 77K views / 115 bookmarks / 1 hype reply captured.

## VERDICT
**BUILD (WINDOWED)** — 14/25. No wire today. Two standing steals if ever pulled:
(a) ling-3.0-flash-fin free tier as candidate spare lane in the next fuel_feed/FREE_LANES
audit while zai-lite is 401-dead; (b) FinFIRST's task→atomic-criteria→rubric-point
decomposition as a methodology reference for the QLoRA eval harness + coverage organs.
Decays to REMEMBER if untouched after one lane-audit cycle.

## ROUTE
No wire. Filed to lane-audit backlog (spare-lane candidate note) and this card as the
rubric-methodology pointer. No seat, no salon, no build task spawned. Revisit trigger:
zai-lite re-auth fails a second time, OR a third-party eval of FinFIRST publishes.
