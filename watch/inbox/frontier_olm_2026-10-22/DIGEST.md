# FRONTIER MINE 2026-10-22 (manual, funded grok lane; Oct 20-22 window)

Receipt: 8 finds across 4 areas, all first-hand fetched (arXiv abstracts +
code repos), Oct 20-22 window. Manual lane, day 4. Confirmation grade:
abstract-level; the MemoryTax study and the tau2-bench pre-registered test
carry body-level detail from the fetch.

## 1. Agent memory (2 finds)

**PerMIT** - checked-gate sharing for persistent memory: an ownership gate
theorem plus logged endorsements that become community-confirmed, so later
users skip re-verification. Estate map: the endorsement model is the
adoption ledger's trust mechanism - sightings become community-confirmed
rows, skipping redundant audit. Direct steal for the adoption ledger's
design.

**MemoryTax** (arXiv 2610.29823): one LoCoMo conversation (419 turns, 152
questions), four memory methods (full context, BM25, Mem0, Zep) x three
coding agents across three models. Mem0 beats full context ONLY with the
weakest model (GPT-4o-mini); Mem0's build cost alone exceeds a full-context
rollout; a stronger reader does not recover what a weaker writer left out;
with Claude Opus 5.5, Pi scores 99% at less than half the cost of full
context. The one miss was a wrong answer key, and part of the lead was photo
captions only the agents could read. Estate map: the memory-vs-no-memory
decision is MODEL-CONDITIONAL, not universal - the token-DNA sim's routing
table needs this shape (memory system choice as a routed decision, not a
constant). And the honesty frame (a short study claiming no general
replacement) is the dead-salmon discipline in the field.

## 2. Inference efficiency (2 finds)

**AKV - Cache Engineering for Agents** (arXiv 2610.28577, code): the agent
edits its LIVE KV cache with drop (exclude selected cache from later
attention) and repos (fix position encodings of what remains). Token
trajectory NOT rewritten, so retained context is not re-prefilled. Key
insight: identical token sequences can have different cache states, so
PREFIX MATCHING IS NOT ENOUGH for cache reuse. Tool-response rolling-drop:
+1.7 points avg, -27.7% cost vs threshold-triggered summarization; up to
1.2x output throughput, 1.5x P95 latency speedup; recursive policy search
cuts another 7.1%. Estate map: the KV env contract (tier-1 port, cleared)
gains a second law - the prefix-match cache reuse assumption breaks under
agent cache editing. The standing channel theory's pipe class just got a
new failure mode: two identical token sequences with different cache states
are different channels. Direct input to the context pack's schema-placement
law.

**Stratified Sparse Attention** (arXiv 2610.28441): deterministic top-k +
sampled residual corrected by inclusion probability. 94% of dense attention
recovered at 50x sparsity, 2.96x FlashInfer decode at 1M context. Estate
map: the attention-budget organ for long-context fleet work.

## 3. Fine-tuning / adaptation (2 finds)

**MuPACE** (arXiv 2610.28072): RE-CONFIRMED from the Oct 21 sweep, now with
the transfer claim verified (meta-trained at 16 layers, transfers to
64-layer Qwen3-32B and Qwen3.8-27B). The token-DNA sim's schedule leg
stands.
**NormTune** (arXiv 2610.29134): PEFT produces much smaller weight-update
norms than full fine-tuning; NormTune scales up layers whose update norm is
small. Adding to rank-8 LoRA/Bone/MoRA: +24.24/+11.33/+16.21% average
accuracy across reasoning benchmarks; at rank 256, matches full
fine-tuning. Estate map: the token-DNA sim's COMPILE leg gains a
norm-rescaling lever - the "PEFT underperforms full FT" gap is a norm
artifact, fixable post-hoc. The ten-minute self's weights can be
norm-rescaled instead of retrained.

## 4. Swarms / multi-agent (2 finds)

**ToM2Vec** (arXiv 2610.29934, code): each agent carries a fixed budget of
continuous tokens trained to match the partner's actual thoughts; the tokens
condition the agent's own reasoning at test time without seeing those
thoughts. Consistent gains over base and trained/prompted baselines across
5 benchmarks. Text theory-of-mind DROPS performance; the latent budget
transfers cross-family (including GPT-5.4). Improves direct answers about
partner beliefs/desires/next actions. Estate map: the token-DNA consensus
design's theory-of-mind leg - latent partner-modeling tokens beat textual
theory-of-mind, and they transfer cross-family. The magatama's "absorb by
shape" law confirmed in the latent-budget format.
**Does Multi-Agent Collaboration Pay When Agents Serve Users?** (arXiv
2610.27655, pre-registered, ~7950 conversations, tau2-bench): multi-agent
WORSE in 12 of 13 valid cells vs single agent, fitted gain -28 points
(95% CI [-44,-12]), 5.5x the cost at best ties, no reduction in wrongful
writes, turns other failures into budget exhaustion. The 45% saturation
rule NOT confirmed in this dual-control setting. Estate map: THE CONSENSUS
GATE'S EXTERNAL FALSIFIER - multi-agent coordination does not pay when
agents serve users in tau2-bench. This is the dead-salmon control for the
singing network: if the perimeter's multi-agent consensus does not beat
compute-matched single-agent on held-out tasks, the perimeter is the
negative result. The paper's own conclusion is narrower than "multi-agent
never pays" - and so is ours: the perimeter must SHOW compute-matched
evidence or it is the negative result.

## Confirmation grade

Sweep-grade (grok-fetched from arXiv abstracts). The eight arXiv IDs are
confirm targets for the next workflow-capable window. The MemoryTax study
and the tau2-bench pre-registered test carry body-level detail from the
fetch.
