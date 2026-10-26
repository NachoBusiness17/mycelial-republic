# NIGHT EXTERNAL SCAN — agent memory / compaction frontier (2026-09-09, night run, external lane)

*Doctrine read first: `watch/inbox/rib.txt` (RenderMan RIB analogy — archives + bounds +
dereference, append-only spine, scope-stack grammar) and `watch/THE_ORCHESTRATOR_REBORN_20260909.md`
STORAGE plane. The test: "find out what other people are doing" in the exact lane where we
built archives-bounds-dereference. Verdict up front: **nobody has our doctrine whole — the
spine, the scope-stack grammar, and the chain-as-out-of-band-channel are still moats — but
three groups have MEASURED organs we only have as design.** Tri-state throughout.*

## The frontier table

| Who / what | What it does | Beats our RIB approach? | Steal? |
|---|---|---|---|
| [Slipstream](https://arxiv.org/abs/2605.08580) (Chen, Pan, Dai, Netravali, May 2026) | Compaction runs ASYNC while the agent keeps executing on the full context; a judge then validates the candidate summary against the agent's actual next steps (forward intent + key facts). **+8.8pp accuracy, -39.7% latency** on SWE-bench Verified + BrowseComp. | YES on the validation organ — measured, ours is design ("test-render" in rib.txt, zero numbers). Their async trick also buys query-awareness: the agent's continued trajectory IS the frustum. | The judge-without-latency shape. We already hold the ground truth it needs: the trajectory envelope (step_hash spine) + GROUNDING_WAVE hash chain are exactly what a validator checks against. |
| [Governance Decay + Constraint Pinning](https://arxiv.org/html/2606.22528v2) (2026) | 7 models, 1,323 episodes: compaction takes safety-constraint violations 0% → 30% (peak 59%); soft org rules decay 8.3x harder than hard norms; the SUMMARIZER is the failure, not the agent. Fix: a pinned buffer of constraints, compaction-exempt, re-injected verbatim each turn, integrity-checked — restores 0% at ~47 tokens overhead. | YES on the mitigation organ — we NAMED governance decay in rib.txt but never built the defense. Their open problem: naive pinning still fails 10-17% against forged in-stream "operator rescinds" — needs a trusted OUT-OF-BAND channel. | Constraint pinning for the ten laws (47 tokens is nothing). And note their conclusion points AT our chain — see moat 1. Treat every summarizer as an untrusted-input sink (matches our files-are-data law). |
| [SelfCompact](https://arxiv.org/abs/2606.23525) (Li et al., Jun 2026) | Model compacts ITSELF via a callable tool + a when/when-not rubric (compact at sub-task resolution, never mid-derivation). No fine-tuning. +18.1pp math, +5-9pp agentic search vs no-compaction, at 30-70% lower cost than fixed-interval. Admits: open-weight models use the tool unevenly without the rubric. | NO on cost (not our binding constraint — we ride free lanes) and its weakness is OUR population (open-weight-ish seats). But the trigger-as-tool + rubric is cleaner than any timer. | Hand workers a `compact` tool + the rib.txt rubric instead of harness-forced compaction. The rubric IS our scope-stack law in prose form — almost free to port. |
| [Parallel Context Compaction](https://arxiv.org/abs/2605.23296) (Cim, Topcu, Das, Kandemir, May 2026) | Compacts in parallel BLOCKS instead of one sequential rewrite; operators get fine-grained control over per-block summary volume. Lower wall time at matched decode volume; 4 backbones, HotpotQA/LoCoMo. NOT a Slipstream follow-up (different group) — convergent answer to the same stall problem. | NO — it fixes serving THROUGHPUT, not summary quality or constraint survival. Solves a problem we don't have at our scale (we compact rarely, spine-cron cadence). | Per-block summary budgets ("shading rate per region") — a refinement of our LOD/fidelity column, not a new organ. |
| [CompactionRL](https://arxiv.org/abs/2607.05378) (Jul 2026) | RL-trains the model to write the summaries it will rely on — joint objective over acting + summarizing. **GLM-4.5-Air +7.0 on SWE-bench Verified; GLM-4.7-Flash +5.5. Deployed in the GLM-5.2 training pipeline.** | Different axis (weights vs scaffold) — not beatable or copyable from where we sit. BUT the signal matters: OUR PRIMARY PROVIDER is baking compaction into its flagship. | Expect GLM seats to get better at surviving compaction natively; re-run our B1 REFEED-style measurements after provider updates instead of assuming static behavior. |
| [MemGPT / Letta sleep-time compute](https://www.letta.com/blog/sleep-time-compute/) ([paper](https://arxiv.org/html/2504.13171v1), MemGPT 2.0 coverage via [Fast Company](https://fastcompanyme.com/technology/why-sleep-time-compute-is-the-next-big-leap-in-ai/)) | A second agent reorganizes/consolidates memory while the main agent idles; pre-processes context against anticipated queries. Productized across all Letta agents. | PARTIAL — this is the closest thing to our spine cron + 04:00 quiet-window cadence, but they turned idle time into a MEMORY FORMATION organ, ours only keeps an INDEX warm. | The idle-window consolidation shape: run the dereference/auto-surface matcher and summary-spine reconciliation at 04:00, not just the index pass. |
| [ACON](https://openreview.net/pdf?id=7JbSwX6bNL) (OpenReview) | Failure-driven context compression — compress on/around failure signals rather than token thresholds. | UNPROVEN at our scale — we already do failure-driven extraction (corrections skill, receipts); theirs is in-window, ours is cross-session. | Steal the PHRASE, not the code: compaction triggers may key off failure events, same as our corrections loop. |
| [Rate-distortion survey](https://arxiv.org/abs/2607.08032) ("What to Keep, What to Forget", 2026) | Field map: MemGPT paging, ACON, Context-Folding (FoldGRPO), Memory-as-Action, ReSum. Frames compaction as rate-distortion: minimize distortion per bit kept. | NO — a survey; our four-plane vocabulary is already richer (frustum, bounds, grammar). | Cite it as third-party proof the field is converging on our problem statement. |
| KV-cache production ([NVIDIA NVFP4](https://developer.nvidia.com/blog/optimizing-inference-for-long-context-and-large-batch-sizes-with-nvfp4-kv-cache/), [AMD TurboQuant 4-bit](https://rocm.blogs.amd.com/artificial-intelligence/turboquant-vllm-agentic/README.html), [OpenVINO INT4](https://medium.com/openvino-toolkit/int4-kv-cache-compression-for-llm-inference-on-intel-gpu-new-in-openvino-2026-2-d71d03c27897), [survey](https://arxiv.org/html/2603.20397v1)) | 2026 converged on 4-bit KV caches shipping in ALL three vendor stacks; KV cache is 70-90% of GPU memory at 1M-token context. ThinKV ([ICLR 2026](https://arxiv.org/html/2603.20397v1), per-bib) goes further: precision BY THOUGHT IMPORTANCE. | IRRELEVANT today (we rent API lanes) — DIRECTLY relevant to Rocinante (Oct 27 local substrate). | ThinKV = "shading rate for the KV cache" — the hardware-level twin of our summary-fidelity idea. Park it in the Rocinante docket. |

## 3 steals (ranked, all buildable at $0-ish)

1. **CONSTRAINT PINNING BUFFER** (governance-decay paper). Extract the ten laws + active
   gates into a pinned, compaction-exempt buffer re-injected verbatim every turn with an
   integrity check. ~47 tokens. Closes the one hole our doctrine names and never defends.
   Natural build site: the Orchestrator v0 seat hook (pre-action gate) already compiles the
   ruleset — the pin is the same ruleset aimed at the CONTEXT instead of the ACTION.
2. **ASYNC COMPACTOR + TRAJECTORY-GROUNDED JUDGE** (Slipstream). Run compaction off the
   critical path; validate the candidate summary against the live trajectory envelope
   (step_hash spine = ground truth; GROUNDING_WAVE = cross-seat judge ledger). This turns
   our unmeasured "test-render" into a measured organ, and the hash chain makes the judge
   deterministic where theirs is another LLM.
3. **SELF-COMPACTION TOOL + RUBRIC FOR WORKERS** (SelfCompact), hardened by the governance
   finding: give bulk-lane seats a `compact` tool gated by the scope-stack rubric (never
   mid-tool-call, never mid-derivation) — plus the pinning buffer above so self-compaction
   can't eat the laws. Their uneven-usage finding on open-weight models says: rubric in the
   scaffold, not trust.

   Honorable mentions: sleep-time consolidation in the 04:00 window (Letta); ThinKV
   fidelity-by-importance for the Rocinante docket; treat GLM seats' compaction behavior as
   a MOVING target now that CompactionRL ships in GLM-5.2 training.

## 3 moats (where we stay ahead)

1. **THE CHAIN IS THE TRUSTED OUT-OF-BAND CHANNEL THE FRONTIER SAYS DOESN'T EXIST YET.**
   The governance-decay paper's stated central open problem: in-stream authority can be
   forged, pinning needs a trusted out-of-band operator channel. We already run one — the
   append-only, hash-chained verkle knot. No surveyed system has a signed, append-only
   history feeding its compaction loop. Their pinning buffer + our chain = constraint
   survival that is verifiable, not promised.
2. **APPEND-ONLY SPINE = PREFIX-CACHE ECONOMICS.** Every surveyed compactor REGENERATES
   summaries (re-tessellates; Slipstream and Parallel Compaction reduce the stall but still
   rewrite the context and invalidate cache). Our spine appends segments so cached tokens
   survive — nobody in the scan does cache-preserving compaction. This is a real advantage
   precisely because our seats live on quota-capped, per-token-metered lanes.
3. **THE SCOPE-STACK GRAMMAR + FOUR-FOLD CONVERGENCE.** Compaction legality as a MECHANICAL
   grammar rule (illegal inside open tool-call scopes) appears nowhere in the frontier —
   everyone else uses timing heuristics or model judgment (SelfCompact's own admitted
   weakness). And our doctrine exists four times independently (rib.txt, MODEL_RIB_LIBRARY,
   trajectory envelope, open-rib spine) — duplication-is-emphasis is the convergence proof
   that the design wasn't fitted to one accident.

## Does anything actually beat archives-bounds-dereference?

- **Validation: YES today.** Slipstream measured what we only sketched. Adopt, don't defend.
- **Constraint survival: YES today.** They built the pinning defense; we filed the risk.
- **Summary quality via RL: different axis** (weights, provider-side — watch it, can't adopt).
- **Losslessness, dereference economics, cache-preserving compaction, mechanical legality:
  NOBODY has them.** The frontier is converging on our problem statement (rate-distortion
  survey) and buying back frustum-awareness with LLM judges; our answer is deterministic
  metadata + a signed chain. That is the moat.

*Filed by the external-scan lane, night run 2026-09-09. Sources inline; primary arXiv IDs:
2605.08580 (Slipstream), 2606.23525 (SelfCompact), 2606.22528 (Governance Decay),
2605.23296 (Parallel Compaction), 2607.05378 (CompactionRL), 2607.08032 (survey),
2504.13171 (sleep-time compute), 2603.20397 (KV survey).*
