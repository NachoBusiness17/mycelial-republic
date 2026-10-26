# PRE-REGISTRATION — the four-condition experiment (ADV-I-11)

Filed 2026-09-18. Status: REGISTERED, NOT RUN. Any change to rules, metrics, or
decision thresholds after data collection begins must be filed as an amendment row
below, never silently. This document exists so the fleet's #1 unrun falsifier stops
being design-shaped and starts being run-shaped.

## Hypothesis under test

H1 (shared-grounding bet): a fleet coordinated by a shared cached prefix plus typed
deltas achieves higher semantic coherence than isolated agents, and the structured
epistemic event layer adds coherence beyond what plain deltas provide.

H0 (the attacker's verdict, wave 3): the event layer is cosmetic; B approx C kills it.

## Conditions

- A COLD: isolated agents. Identical task prompts, no shared prefix, no cross-agent
  reads. Lower bound. Coordination impossible by construction.
- B WARM-STATIC: shared frozen prefix + per-agent deltas (steering tail). No typed
  event layer. This is the minimal shared-grounding bet.
- C WARM-APPEND-ONLY: B plus the typed event layer as the fleet actually runs it
  (append-only trails, gate rows, receipts; chain rows entering context only via
  compiled packs). This is the deployed shape.
- D WARM-DELETING: C plus the tombstone GC: an active view pruned of retracted
  claims, tombstone sidecar consulted at promotion, precedent-of-error retained.
  D is the counterfactual fleet. It requires building the GC boundary first (ADV-I-5).

## Materials

- Task battery: 20 unseen coordination dilemmas, written BEFORE any run, held out
  from every seat's context. Drawn from the same generator family as the RUINS GO
  gate and the pack-31 style checks, plus 10 normative-tradeoff cases written fresh
  (resource scarcity meets a proportionality clause; two lanes claim one lock;
  amendment conflicting with a receipt).
- Seats: whichever free lanes are live on the day (groq trio, cerebras, mistral,
  nemotron, zai-lite paced). 12 seats is the practical n, not 500; the scaling
  claims (I-2) are explicitly OUT of scope for v1.
- 5 agents per condition-run (a lane pod), 40 runs per condition, 160 runs total.
  Power: medium effect f=0.35 at alpha=0.05, power=0.80. If free-lane rate limits
  force fewer runs, the pre-registered minimum is 15 runs per condition; below that,
  report as pilot, never as confirmation.

## Primary metric

SCS (Semantic Coherence Score) = 1 - (mean pairwise Jensen-Shannon divergence between
final answer distributions across the pod's agents, normalized so A's mean divergence
= 1). Each dilemma ends with every agent emitting a final action choice from a closed
option set; the distributions are over those choices.

Secondary (recorded, not gating): wall-clock, cache/pack bytes shipped per run,
count of conflict rows (retractions, gate rejections) per resolved task.

## Decision rules (fixed now)

1. B approx= C (mean SCS difference < 0.05, two-sided t p > 0.10): the event layer is
   cosmetic. Action: stop building event machinery; revert fleet doctrine to B shape;
   file ADV-I-11 as CONFIRMED-H0.
2. D <= B: deletion is a net negative (GC destroys volatility information agents
   needed). Action: abandon the tombstone GC build; the chain stays the only memory.
3. A > C and A > D on SCS: the shared prefix is a correlated blindspot generator.
   Action: the warm/cold bet is dead; escalate to operator with the full receipts;
   redesign coordination from isolated-plus-broker.
4. C > B > A (the bet wins and the layer earns its keep): proceed to build the GC
   boundary and the veto oracle per the arc sequence.
5. Any other ordering: report verbatim, no post-hoc thresholding, amendment row only.

## Confounds named in advance

- Lane heterogeneity: randomize pod composition per run from the live-lane pool.
- Time-of-day effects: interleave conditions across the same hours.
- Prompt leakage between runs: fresh prompts each run, battery never in any boot pack.
- Grader circularity: SCS is computed from choice distributions by ordinary code,
  not by an LLM judge (A3 compliance).
- The G02 race: pack watermark updates are transactional with pack write in all
  conditions, so C vs D differs ONLY by tombstone pruning, not by crash behavior.

## Cost estimate

160 runs x 5 agents x ~4k tokens = ~3.2M tokens, all free lanes, paced. Realistic
elapsed: 2-3 evenings of paced firing. The expensive part is writing the 20-dilemma
battery honestly; that is one focused session before any run.

## Amendment ledger

| date | change | reason |
|---|---|---|
| 2026-09-18 | initial registration | the arc demands it run before more event-layer building |

| 2026-09-18 | amendment 1: condition D adopted as an EXTERNAL REPLICATION: M.P. Steiniger independently proposed the same test (fold his ledger into actual weights, run the transfer gate) for October; runs in parallel, gates compared | his last correspondence; credited as joint design |

| 2026-09-18 | CORRECTION of amendment 1: condition D is not a Steiniger co-design. The operator proposed the October test TO Steiniger as a test of Steinigers identity-in-model thesis (fold the fleet ledger into weights; if the model carries the house alone, his thesis wins). Condition-D alignment is ours alone; Steiniger is the named hypothesis-holder |
| 2026-09-25 | amendment 2 (battery hygiene, pre-run, zero data exists): DIL-011/012/017/018 lose their stray fifth option E (closed option sets are A-D as registered) and option order is rotated per row so the answer key is balanced 5/5/5/5 across A-D instead of 19 B / 1 A. No label set changes beyond the four dropped E distractors | R3 content review note (watch/inbox/THE50_REVIEW_R3.json): position bias a model could exploit; carried on the STATE 2026-09-20 punch list as "fix before October test". Position bias is now a named confound; fix executed by gala lane b3-the50-quality, new battery sha256 1310177db0e766ec9176bcf1327d4bd519e557b528b423c4c2480022832483e0 |
