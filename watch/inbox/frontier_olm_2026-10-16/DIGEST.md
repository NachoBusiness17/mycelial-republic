# FRONTIER MINE 2026-10-16 (manual, funded grok lane) - DIGEST

Receipt note: the saved olm-mine workflow could not fire - the CreateWorkflow
approval gate failed twice ("Permission request failed") with the operator off
PC. Root cause: the workflow approval gate is a mode-1-only channel (standing
channel theory S1 finding, caught in the wild). The mine ran MANUALLY through
the funded grok lane instead, at reduced width (4 areas, 8 finds, all fetched
first-hand with arXiv IDs). All claims below are grok-fetched verbatim from
the live posts/abstracts; nothing estimated.

## AREA: inference efficiency (2 finds)

1. SpecFit (arXiv 2610.15417, Oct 11): speculative decoding for OFFLOADED MoE
   - pick the ancestor-closed draft subtree maximizing tokens-per-cycle given
   the per-layer union of experts each token would pull. On Qwen3-30B-A3B:
   21.6% and 7.0% faster than EAGLE-3 with the same expert cache. Estate map:
   the janitor fleet's decode lane (inference-efficiency steal card's
   successor) - the insight is that draft length must be priced against
   EXPERT LOADING, not just accepted tokens.
2. When the KV Cache Is Slower Than the GPU (arXiv 2610.21500, Oct 15): for
   context-parallel MLA prefill, a remote KV hit took 0.88s vs 0.31s recompute
   - LMCache-style prefix caches made p99 WORSE (3.96s to 17.3s) until fixed.
   Cost model: a hit pays only above 2.53 GB/s bandwidth, with a fixed ~0.33s
   per-hit cost; prompts under ~17k tokens cannot beat recompute at any
   bandwidth. Estate map: DIRECT correction to our prefix-sticky router design
   (the tier-2 port) - the router needs this cost model (bandwidth floor +
   fixed per-hit cost + token-count threshold) BEFORE deployment, or the
   prefix-sticky lane silently regresses p99 on short prompts. Also: rank-
   partitioned sharded stores, no coordination, p99 83.32s to 0.67s on
   hit-heavy replay; changes submitted upstream to LMCache.

## AREA: fine-tuning / adaptation (2 finds)

3. LS-LoRA (arXiv 2610.11620, Oct 8): rank layers by input-output cosine
   similarity (a forward-only proxy for empirical Fisher), train LoRA ONLY in
   low-similarity layers. Better target-task performance AND substantially
   more retained commonsense than all-layer LoRA. Estate map: the JIT law's
   SELECT leg gains a no-backward-pass placement lever - the adapter placement
   question (which layers?) answered by a forward-only probe.
4. SLDR (arXiv 2610.10345, NeurIPS 2026): signed layer sensitivity - scaling
   a layer can strengthen refusal, weaken it, or do nothing - and a recovery
   LoRA toggled per-request by a representation router only for queries the
   router marks malicious. Harmful score 11.54 to 0.08 with downstream
   accuracy maintained on Llama 3.1/SST-2. Estate map: the VERIFY leg's
   serving-fidelity control, and the pattern generalizes - per-request adapter
   gating by a router is the same shape as our consensus-weighted routing.

## AREA: swarms / orchestration (2 finds)

5. A2-Failures (arXiv 2610.19342, Salesforce; 2,500+ runs, 488 scenarios, run
   logs on HuggingFace): a 20-mode failure taxonomy for agent-to-agent runs
   WITH private state and separate principals (no shared workspace, no single
   orchestrator). Headline findings: discovery follows task phrasing, not peer
   existence; NO agent checks a peer's factual claim unprompted, so the system
   inherits its least reliable participant unless the protocol checks;
   aggregate scoring misses coordination/verification/conduct failures -
   evaluation must be per-agent against that agent's own principal. Estate
   map: this is the TOKEN-DNA consensus design's external validation (the DNA
   rows ARE per-agent evaluation against own principal) and the standing
   channel theory's P2 (capacity honesty) formalized as a failure taxonomy.
6. Market-based post-training (arXiv 2610.22322, Oct 15): agents BID to act;
   bids pick participation AND assign training credit; no central coordinator.
   Learned self-orchestration beats fixed-graph coordination strategies;
   adapts faster to related tasks, scores better as population grows, loses
   less on agent dropout. Estate map: the tokenization-MCP law's training
   analog - bids are the DNA of participation, participation is a learned
   policy, and the rail settles the bid. Direct feed to the token-DNA sim's
   bidding design (R6, new).

## Confirmation grade

Honest: this manual sweep ran at sweep-grade (grok-fetched verbatim from live
posts + arXiv abstracts), NOT the saved workflow's independent-confirm pass.
The four arXiv IDs are the re-fetch targets for the next workflow-capable
window. The saves also carried real run logs (A2-Failures on HuggingFace) and
upstream commits (LMCache) - both first-hand-checkable.

## The blocker, receipted

The saved workflow could not start: CreateWorkflow approval gate failed twice
("Permission request failed") with the operator off PC. The approval gate is
mode-1-only - a standing channel theory S1 finding in the wild. Until the
approval gate has a mode-2 path (a pre-approved standing workflow, or an
operator-configured auto-approval for the standing mine), manual mines via
the funded grok lane are the daily burn's execution path.
