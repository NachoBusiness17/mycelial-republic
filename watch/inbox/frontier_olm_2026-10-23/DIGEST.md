# FRONTIER MINE 2026-10-23 (manual, funded grok lane; Oct 21-23 window)

Receipt: 8 finds across 4 areas, all first-hand fetched (arXiv API +
abstracts), Oct 21-23 window. Manual lane, day 5. Confirmation grade:
abstract-level; RoleFly body read beyond abstract. Note: no papers dated Oct
23 yet (the API returned empty for the 23rd as of sweep time).

## 1. Agent memory / shared memory (2 finds)

**Muffin** (arXiv 2610.31355): an orchestrator sends hard queries to several
agents; a shared buffer carries intermediate findings ASYNCHRONOUSLY; each
agent's private reasoning stays LOCAL. Best accuracy in 17 of 20 settings;
vs multi-agent debate: +19.2 accuracy points with 77.4% fewer tokens and no
full-trace sharing. Estate map: this is the standing channel theory's signal
class confirmed - asynchronous shared buffer beats synchronous full-trace
sharing on both accuracy and cost. The pheromone bus's design (deposit,
decay, partial signals) is the same shape.

**AMV-Guard** (arXiv 2610.31446): "When Is a Memory Safe Enough to Act On?"
- extract the memory premises a candidate action rests on, then choose
proceed/verify/abstain by bounded value of information. A check is worth
paying for only if it can change the next action. Same address passes for a
routine shipment, requires confirmation for a valuable one. On ToolSandbox:
verification cost -33.9%, safe-proceed recall 100%, harmful-gate rate 0%,
proceed coverage 38.83% -> 44.17%. AppWorld transfer: -21.3% cost with small
recall/success drop. Estate map: this is the AMV-Guard value-of-information
gate as the token-DNA sim's consensus threshold mechanism - the gate doesn't
check everything; it checks only what could change the next action. The
perimeter's verify/hold order (the trickster's finding) is the same law.

## 2. Inference efficiency (2 finds)

**ValuSpec** (arXiv 2610.31338): before the target verifies a speculative
tree, drop low-quality branches; threshold from the target's greedy
trajectories on a calibration split; no parameter training; accepted tokens
must match greedy. Up to 2.38x end-to-end in retrieval-based tree settings;
2.78x when dropped onto EAGLE-3. Estate map: the janitor fleet's spec-dec
tier (the inference-efficiency card's successor).
**HAWK** (arXiv 2610.29873): prefill on GPU, decode on NPU; KV moves by
RDMA into NPU-laid-out buffers. Within 7.88% of GPU-only on performance,
1.26x power efficiency, 1.72x cost efficiency. Estate map: heterogeneous
compute = the garage fleet's actual topology (desktop GPU + laptop iGPU +
phone NPU). The KV-layout-matching-the-NPU insight is the coldest-vertex
port spec.

## 3. Fine-tuning / adaptation (2 finds)

**AOPD** (arXiv 2610.31563): on-policy distillation weighting a teacher
action by its counterfactual advantage for the CURRENT student, estimated
from ordinary student rollouts + terminal rewards + teacher importance
weights. No extra rollouts, no process reward model. Qwen3-1.7B from a 4B
math teacher: highest pass@1 on Open-Thoughts (78.4), AIME24 (35.0), AMC
(65.1). Estate map: the ten-minute self's compile leg - the counterfactual
advantage estimator is the percolator's next lever.
**Mostly Reading** (arXiv 2610.31017): one LoRA per document, then two
probes (open-book vs cloze). A random other-document adapter keeps 82% of
the specialist's open-book gain but only 2% of its cloze gain. At 16+
documents, correctly scaled merges keep 87-89% open-book and 12-16% cloze.
Adapter selection by weight-space proximity or text embedding is
indistinguishable from RANDOM. Four silent errors each produced a clean
wrong result. Estate map: the ten-minute self's COMPILE leg gets its
honest-limit paper - the compile door drops the cloze leg (the recall leg)
unless jointly trained, which is the Cache2LoRA come-apart confirmed by a
second lab. The four silent errors are the dead-salmon discipline's reason
for existing.

## 4. Swarms / markets (2 finds)

**RoleFly** (arXiv 2610.30429): the collaboration graph changes DURING the
run by atomic edits and on-demand role synthesis. Single-Edit Counterfactual
Policy Optimization credits the tokens that made each edit. Average 67.1
across seven benchmarks, first on five, 4.7 points above W4S. Estate map:
the singing ractors' evolution law - the collaboration graph itself is
editable mid-run, and the edit credit is counterfactual. This is the
repo-as-game's tech tree, formalized.
**Matching Tasks to Agents** (arXiv 2610.31002): mechanism-design proof -
one principal, agents with private types setting both success probability
and effort cost, principal pays only on success. Optimal mechanism has a
Myerson-style form running in polynomial time for single tasks; worst-case
profit vs full information is tightly Theta(1/(NK)); with multiple tasks an
optimal mechanism may NOT EXIST, but a polynomial-time approximation exists
for constant agents. Estate map: the token-DNA sim's payment mechanism - the
paper proves the optimal contract is tractable for single tasks but MAY NOT
EXIST for multiple tasks, which is the perimeter's multi-task settle design
question formalized.

## Confirmation grade

Sweep-grade (grok-fetched from arXiv abstracts). Eight arXiv IDs are confirm
targets for the next workflow-capable window.
