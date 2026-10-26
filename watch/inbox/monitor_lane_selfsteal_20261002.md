# MONITOR LANE SELF-STEAL - the other lane's handoff, folded (2026-10-02)

Operator order: "you just got some handoffs from the other lane not sure where
they are exactly self steal". The handoff surface (this sitting's read):
a sibling zcode seat runs a MONITOR LANE - 7 research terms polled across
HN / arXiv / OpenAlex roughly every 16 minutes, dedup memory in
watch/monitor_lane.state (hundreds of seen ids per term), heartbeat rows in
watch/room.jsonl (14,602 lines, kind monitor.lane), spool
watch/scout/MONITOR_LANE_2026-10-02.md (the payload; prior spool
MONITOR_LANE_2026-09-04.md from the lane's first life). Terms: agent swarm
concurrency, speculative decoding MLX, image to 3D WebGPU, GLM-5.3,
KV cache economics, fixed point refinement reasoning, AI game building
agents.

## Triage honesty

The 2026-10-02T00:45Z spool holds 17 "new items". By direct read, 14 are
OpenAlex keyword-match noise (named examples: a Laurent-series singularities
math paper under "fixed point refinement reasoning"; an earbud eating-pace
system under "AI game building agents"; a primary-school linguistics paper
same term). Three needles are real and load-bearing. All three verified by
live fetch this sitting (no-fabrication law; quotes from fetched pages).

## The three needles, mapped to organs

1. CRJudgeBench + Sentinel (arXiv:2609.37216, fetched 2026-10-02).
   A 1,199-instance benchmark of plausible-but-technically-invalid code
   review comments (expert-verified perturbations of real PR comments),
   359-instance test split, dataset on Hugging Face (dcloud347/
   CRJudgeBenchmark, CC BY 4.0). Their trained judge Sentinel hits 76.60
   pct accuracy, "beating GLM-5.3 by 6.13 points". ESTATE ORGANS: this is
   the ractor hostile second pass as a formal benchmark task, AND external
   measured evidence that GLM-5.3 (the operator's daily driver, our default
   judge family) is weak in the judge-the-review class - the B2-60
   same-family-reviewer caveat now has a number from strangers. STEAL
   (one sitting): pull the HF test split, run our own lens set (glm + one
   cross family) on a 50-instance slice, price our hostile pass against
   Sentinel's 76.60 pct. FALSIFIER: if our lens set matches or beats 76.60
   on the slice, the hostile pass needs no new organ; if it loses by the
   same ~6 points, the ractor engine's break pass has a measured hole.

2. Socratic pressure test v1 (Zenodo 10.5281/zenodo.23049784, fetched
   2026-10-02; the spool listed sibling DOI ...83 which lands on the same
   record v1.0.0). 8 models x 12 Python exercises x 4 pressure messages x
   2 system prompts = 768 replies; a LEAK = reply code that passes the
   exercise's own asserts, "verified in a sandboxed container - no LLM
   acts as judge". Findings: Qwen2.5-Coder 3B/7B are the big leakers
   (45/48 in one condition); GLM-5.3, Kimi K3, Gemma 4 12B, Claude Sonnet
   4.6 "returned no passing code in any of their 96 replies each";
   CodeTrain's published tutor rules cut leakage p=0.001 (7B) and p=0.035.
   ESTATE ORGANS: the ghost tournament's obedience science with a CLEANER
   instrument than ours (execution-verified, zero judge noise - our
   obey/silence meters ride model grading); the 4-message pressure ladder
   is a ready-made probe for the estate's named gap (persuasion jailbreak
   33 -> 72 pct, intake has NO persuasion scanner); the rules-cut-leaks
   result is external confirmation of the claritas-face steering doctrine.
   STEAL (one sitting): fetch github.com/InferHaven/research v1.0.0, re-run
   the 12-exercise battery against OUR animals (gemma4 local, ds flash,
   glm) with our tournament vectors as the pressure messages, judged by
   their execution instrument. FALSIFIER: if our vectors do not move leak
   rates against models their ladder moved (or vice versa), one of the two
   instruments is measuring theater; reconcile before trusting either.

3. SPLASH (arXiv:2609.37626, fetched 2026-10-02). Mid-run switching of
   attention parallelism (tensor / data / context) with median overhead
   under 0.51 pct of the step, 1.3-1.73x throughput over fixed layouts on
   B200s serving GLM-5.3; code public (SPLASH-sglang). ESTATE ORGANS: the
   VAST_LAUNCH_PLAN sovereign substrate (vLLM multi-family serving) - the
   agentic workload shift (many short asks -> few long reasonings mid-run)
   is exactly our descent/ractor load shape. STEAL (one sitting, at launch
   time): benchmark SPLASH-sglang vs plain vLLM on the rented GPU with our
   real ractor-lane traffic before committing the serving config.
   FALSIFIER: if our workload (short scut bursts + rare long judgments)
   never crosses the layout-switch boundary, SPLASH is dead weight for us
   and the plain stack stands.

## The lane's own disease (stolen with the rest)

room.jsonl monitor-poll rows from 00:45Z through 13:40Z all read
"0 new items across 0/7 terms (hn=0, arxiv=0, openalex=0,
sources_boxed_skip=openalex)" - 13 hours of blind polling. The dedup memory
in monitor_lane.state carries hundreds of seen-ids per term, so the lane now
rejects everything as already-seen, and OpenAlex is boxed (skipped) entirely.
This is the fossil-in-feed class (the 09-27 law: a consumer whose inputs
stopped moving decays silently): the lane is ALIVE (polling on schedule)
and BLIND (nothing new can ever surface until the dedup window rotates or
the terms change). MOVE for the lane's owner (not executed here - it is the
sibling's organ): rotate the dedup window (e.g. keep 7 days of seen-ids,
drop older), unbox openalex or replace it, and consider precision filters -
14/17 noise says the OpenAlex term match is too loose to be worth its
fetches. A second-order steal: the lane found these 3 needles in its FIRST
hours of life (00:45Z spool) and nothing since - early-catch-then-blind is
the same curve the OLM mine rode before --candidates.

Filed by the 10-02 boot seat, same-sitting. All three URLs fetched live this
sitting. No em-dash bytes.
