# Lens of lenses: the 8 frontier-sweep areas (frontier_olm 2026-10-07)

What this is: the questions lens. It folds the five lens files banked this run
(corpus.md, laws.md, graph.md, burns.md, doors.md - all five read in full this
sitting) into exactly 8 areas of interest. Each area carries 3-5 concrete
questions refined by what the estate already holds (so the sweep does not
re-derive banked ground) and the organs it feeds. House laws held: no
fabrication, byte cites, no em-dashes, ASCII only.

Method and receipts (this sitting):

- Read in full: watch/inbox/frontier_olm_2026-10-07/lens/corpus.md (49 lines),
  laws.md (125 lines), graph.md (40 lines), burns.md (234 lines), doors.md
  (49 lines); plus memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md (91 lines) to
  check the "quantize target" phrase. Verdict: that rib's quantize target
  (RIB_DEEPSEEK_WINDOW_20261007.md:64-68) is what knowledge to compress into
  the frozen spec, NOT model quantization; it is therefore NOT used as a feed
  for the quantization area below.
- Organ existence checks, run this sitting with the repo venv:
  `./.venv/Scripts/python.exe watch/inbox/frontier_olm_2026-10-07/lens/_organ_check.py`
  -> all 20 named paths OK; second batch via `./.venv/Scripts/python.exe -c`
  -> memory/rib/RIB_GPU_LADDER_20261001.md, RIB_ROUTING_CLASSES_20261002.md,
  RIB_INFERENCE_BUDGET_20261001.md,
  RIB_MINDSWEAVE_EVAL_CONSENSUS_ILLUSION_20260810.md,
  memory/corpus/quantized_thought/instructions_frontier.jsonl, and
  memory/zknot/LATEST.md all OK. Full output in the receipt section.
- Not run this sitting: no pytest, no web probes (doors.md:42-48 already
  carries this run's door receipts), no catalog recounts (corpus.md:3-4
  carries them).

Door guidance for the sweep, from doors.md (read this sitting): HN search via
https://hn.algolia.com/api/v1/search?query=...&tags=story works through
WebFetch (doors.md:18-22); tweet fetch via
https://api.fxtwitter.com/<handle>/status/<id> works (doors.md:24-28); arXiv
export API works via curl but timed out on WebFetch (doors.md:30-33, retry
OWED); old.reddit .json is login-gated to unauthenticated fetch, no verified
recipe (doors.md:35-38, OWED).

---

## 1. open-local-language-models (open and local language models)

What we hold: local Ollama janitors are the first rung of every climb
(gemma:2b scut, gemma4 short worker; qwen2.5:7b is the fold/gauntlet local
seat, burns.md:141-143, 127), the routing grid is mostly UNMEASURED with only
deepseek-v4.1-flash fully measured (laws.md:104), and day-6 banked the
decision-model wave in estate-shaped serving (Ollama 0.35 nimble, llama.cpp
/v1/systemone, burns.md:90-91).

Questions:

1. Which open-weight models released since 2026-09-01 in the 0.5B-8B band beat
   the estate's local rungs (gemma:2b scut, gemma4 short worker, qwen2.5:7b)
   on instruction-following, tool-calling, and long-session stability, with
   instrument-measured evidence rather than vendor claims (estate law: only
   estate instruments fill verdict cells, UNMEASURED is the legal empty
   state, laws.md:48)?
2. The decision-model "rung under gemma:2b" lead stays gated behind a
   beat-embeddings baseline at >=0.880 on n>=40 (burns.md:92-94): do any
   published sub-1B router/decision models clear an embedding-baseline bar at
   that shape, or is the rung still unsupported?
3. Ollama 0.35 nimble and llama.cpp /v1/systemone were banked as estate-shaped
   serving changes (burns.md:90-91): what runtime-level features have landed
   since 2026-10-01 in the Ollama/llama.cpp lineage (sampling controls,
   speculative decoding partners, system-prompt and tool-call handling) that a
   local agentic harness should adopt?
4. Non-standard open-weights lineages link-dropped this week: ALoDLM
   open-weights diffusion LM (arXiv 2610.04198) and QUEEN chess LM 4B
   silent-expert weld (burns.md:119-122): which such lineages are
   production-viable for local agentic work in late 2026, and which stay
   research-only?
5. The frontier_thinking shelf holds 11 files (corpus.md:42,48): which recent
   papers or systems belong on it, so the sweep adds to state/arxiv's 4,998
   paper files (corpus.md:25,36-38) instead of re-deriving them?

Estate map: feeds the local janitor tiers and the routing grid rib
(memory/rib/RIB_MODEL_GARDEN_ROUTING.md, cited laws.md:28,104; UNMEASURED
cells decide which local rung fires before any paid dispatch).

## 2. quantization-compression (quantization and compression)

What we hold: day-6 banked a per-artifact, task-graded quant bit-ladder (0.6B
decision model bf16 0.757 / Q8_0 0.750 / Q4_K_M 0.703; VeriLoop
protected-spine IQ1_M beat uniform IQ2_S; burns.md:95-97), the 7B A/B is owed
and un-run (burns.md:97-98, 218-219), and BreadthKV / BARQ KV-side drops are
banked (burns.md:112-113).

Questions:

1. The owed qwen2.5:7b Q4_K_M vs q8_0 task-graded A/B (burns.md:97-98,
   218-219): what do published TASK-GRADED (not perplexity) quant comparisons
   at the 7B scale report as typical deltas on multi-step agentic and
   long-context reasoning work?
2. Protected-spine / mixed-precision: VeriLoop's IQ1_M protected spine beat
   uniform IQ2_S (burns.md:97): which per-layer or per-module protection
   schemes are late-2026 best practice, and which ship open implementations?
3. Does the day-6 cliff shape (bf16 0.757 -> Q8_0 0.750 -> Q4_K_M 0.703 on a
   0.6B decision model, burns.md:95-96) replicate in published sub-1B quant
   ladders, and where do IQ quants sit on that curve?
4. KV-side compression: day-6 banked BreadthKV's buy-count-before-fidelity
   (arXiv 2610.05685) and BARQ codebook-balance (arXiv 2610.04490)
   (burns.md:112-113): what is the measured late-2026 frontier for KV
   quantization/compression under local long-context serving, and which
   methods optimize for retained token count the way BreadthKV does?
5. The estate's serving reality is CPU/Vulkan (GPU ladder measured 72.97
   tok/s Vulkan vs 6.0 CPU, 12x, install-provenance tier-2 unconfirmed,
   burns.md:135-136): which quantization methods are measured best on
   CPU/Vulkan backends specifically (not CUDA) for the 2B-9B class?

Estate map: feeds the un-run 7B quant A/B on the day-6 register
(watch/inbox/frontier_olm_2026-10-06/DIGEST.md, owed list at
burns.md:216-225) and the GPU ladder rib
(memory/rib/RIB_GPU_LADDER_20261001.md, cited laws.md:115) whose FP8/MoE
trigger gate waits on real demand.

## 3. agent-memory-continuity (agent memory and continuity)

What we hold: day-6 banked the memory-continuity contract set (adoption-at-use
8-9/13 vs re-read 13/13 on arXiv 2610.03902; temporal flattening 244/381 on
2609.36457; keyed belief retirement; 40% zero-memory-call sessions;
burns.md:99-102), the one-computer steal map names Mem0/Letta/Zep
(burns.md:134), and our own knowledge graph is a measured star forest
(1,066 of 2,938 nodes orphaned; 379 of 400 knots and 190 of 217 doctrines
unattached; graph.md:30-33).

Questions:

1. Write-time vs use-time: following the banked adoption-at-use 8-9/13 vs
   re-read 13/13 and the 40% zero-memory-call finding (burns.md:99-102), what
   do newer results say about WHEN long-horizon agents should write vs re-read
   memory, and which access policies demonstrably cut zero-memory-call
   sessions?
2. Temporal flattening (244/381 answers flattened over time, arXiv 2609.36457,
   burns.md:100-101): which timestamped or recency-aware memory architectures
   demonstrably preserve temporal order in recall?
3. Open-source memory layers named in the one-computer steal map (Mem0, Letta,
   Zep; burns.md:134): which 2026 release-line designs fit a local-first,
   no-throne flock (doctrine, laws.md:90), and what are their measured
   retention/latency costs?
4. The estate graph is a star forest, not a web (graph.md:11,30): which
   automatic edge-induction methods (LLM-based KG construction,
   embedding-based linking) are MEASURED for stitching 1,000+ orphan nodes
   into a working web without fabricating edges?
5. Keyed belief retirement (cohorte, burns.md:101): how do current systems
   retire stale beliefs without deleting still-valid neighbors, and what
   falsifier shapes catch wrongful retirement?

Estate map: feeds memory/knowledge_graph.json (the star-forest graph,
graph.md:3-11), mag/memlang.py (the knot hub, graph.md:18) and
mag/context_compression.py (graph.md:22), plus the operator-intent handoff
organ memory/zknot/LATEST.md (AGENTS.md boot recap; existence verified this
sitting).

## 4. swarm-orchestration (swarm orchestration)

What we hold: an 11.7M-request production trace shows logical siblings rarely
overlap in wall-clock (arXiv 2609.34432), gated on the estate's owed S10 width
A/B with the 1.25x/1.5x band rule (burns.md:103-105, 218-219); a measured
consensus illusion (flock consensus agreed with strong-remote 0/3 at strength
0.6-0.67, laws.md:89,102); a gauntlet staging falsifier trials into the
free-lane fleet at $0.00 (burns.md:123-127); ES-vs-PPO link-drop evidence
(burns.md:159-160).

Questions:

1. The 11.7M-request trace finding (logical siblings rarely overlap
   wall-clock, arXiv 2609.34432, banked burns.md:103-105): what follow-up
   measurements validate or contradict width heuristics for gated multi-agent
   fan-out on rate-limited accounts, ahead of the estate's owed S10 width A/B
   with the 1.25x/1.5x band (burns.md:218-219)?
2. Given the measured consensus illusion (0/3 at strength 0.6-0.67,
   laws.md:89,102) and the party-turn provenance contract (laws.md:94): what
   published inter-agent communication or blackboard designs demonstrably
   raise CORRECTNESS (not just agreement), and how are they measured against
   a strong-remote ground truth?
3. ES as the mesh-native dispatch/training shape (link-drop: neighborhoods
   3.9x wider, stability-plasticity 8/18 vs zero, only fitness scores travel,
   burns.md:159-160): what is the current measured state of ES vs
   gradient-based coordination for agent swarms?
4. Cheap-tier adversarial grading: the gauntlet ran dice 2/2 PASS, beat 3/4
   after a grader self-strike, and caught qwen2.5:7b contesting the hidden
   roll (burns.md:123-127): what published results cover free/cheap-tier
   falsification of expensive-tier outputs, and which reward-hacking catches
   are reported?
5. The shared inbox is the cross-surface contract
   (watch/inbox/SHARED_SURFACE_CONTRACT.json, existence verified this
   sitting): what production multi-agent systems publish failure censuses or
   taxonomies for child-run deaths (the estate's own shape is the B2-443
   workflow-child error census, AGENTS.md ask-supplied)?

Estate map: feeds tools/workflow_gate.py + memory/workflows/REGISTRY.jsonl
(both verified this sitting), the gauntlet register
watch/inbox/gauntlet/GAUNTLET_REGISTER.jsonl (burns.md:126-127), and the owed
S10 width A/B (burns.md:218-219), because dispatch shape is the estate's
retry strategy.

## 5. finetuning-adaptation (finetuning and adaptation)

What we hold: state/arxiv already banks RLVR/data-efficient RL (DE-Venus),
gradient-aligned rewards, logit-based pre-training distillation (ALRA), and
adaptive latent reasoning (RecurTrace) among 4,998 paper files
(corpus.md:25,36-38); link-drops this week added LiFT (2610.05538, extra
inference steps without retraining, ~60pct fewer params), MIRA meta-reasoning
+ token cues (2610.06851), and telegraphese register-evolution confirmation
(burns.md:119-121, 159-162).

Questions:

1. Loop-flow depth: LiFT buys extra inference steps without retraining at
   ~60pct fewer parameters (burns.md:159-160): which competing
   inference-time-depth techniques (recurrent depth, latent reasoning;
   RecurTrace already on our shelves, corpus.md:38) publish quality/cost
   curves that compete with weight-level finetuning at small scale?
2. RLVR / data-efficient RL for small local models (DE-Venus and
   gradient-aligned-reward work already banked, corpus.md:38): what are
   late-2026 minimum-data recipes for stabilizing RLVR at 2B-8B, and what
   reward-hacking guards do they ship?
3. Frontier-to-local distillation (ALRA logit-based pre-training distillation
   banked, corpus.md:38; distill-to-bus sits as an orphan doctrine,
   graph.md:30): which behavior-preserving distillation recipes into sub-8B
   models have measured AGENTIC-task results (tool use, long sessions), not
   just benchmark scores?
4. Register/style adaptation: telegraphese register-evolution independently
   confirmed (LLMs relearn historical compression, burns.md:161-162): what
   results exist on steering or finetuning models into compressed registers
   without capability loss?
5. Training for reasoning-channel reliability (MIRA meta-reasoning + token
   cues, 2610.06851, burns.md:119-121): which training-side interventions
   reduce the empty-content/hidden-burn failure mode (the estate's
   EMPTY_REASONING disease, laws.md:34-36)?

Estate map: feeds the state/arxiv shelf (4,998 files, corpus.md:25) whose
RLVR/distillation/latent-reasoning coverage the sweep must not re-derive, and
the descent protocol's cheap-first SHERPA + prior-art-sweep legs (laws.md:53-55)
which draw on these levers before any premium spend.

## 6. kv-cache-context-engineering (KV cache and context engineering)

What we hold: BreadthKV buy-count-before-fidelity and BARQ codebook-balance
banked (burns.md:112-113); a live CONTEXT-PACK-layer propagation gap found in
dogfood (burns.md:151-153); module:context_compression.py is a degree-7 graph
hub (graph.md:22); the harness holds a byte-identical-ask cache-hit law
(corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md, AGENTS.md ask-supplied);
the corpus runs 1,195,926 catalog rows behind an FTS5 index (corpus.md:8).

Questions:

1. KV compression for agentic serving: what is the measured late-2026
   frontier (H2O lineage, sink/sliding hybrids, MLA-style, quantized KV)
   under LONG AGENTIC SESSIONS specifically, and which methods optimize
   retained token count the way banked BreadthKV does (burns.md:112-113)?
2. Prompt-cache correctness: the harness's byte-identical-ask cache-hit law
   (ZCODE_OPERATING_PLAYBOOK, AGENTS.md ask-supplied): what do providers and
   local runtimes document in late 2026 about cache invalidation semantics
   (exact-prefix rules, TTLs, interaction with reasoning channels)?
3. Compaction that preserves continuity: dogfood just logged a
   CONTEXT-PACK-layer propagation gap (burns.md:151-153): which
   compaction/summarization schemes demonstrably preserve task-critical state
   across compaction boundaries, with measurements rather than anecdotes?
4. Long-context vs retrieval at local scale: with 1,195,926 catalog rows
   behind an FTS5 index (corpus.md:8; FTS daily task, AGENTS.md ask-supplied),
   when does long-context ingestion beat retrieval for local 7B-class models
   per published measurements?
5. The Turing castle reading frames the context pack as a tour guide that can
   drop pages (the d01 shed finding, burns.md:160-161): what published work
   MEASURES information loss in guide/summary-style context abstraction
   against full-context baselines?

Estate map: feeds mag/context_compression.py (degree-7 hub, graph.md:22), the
context-pack layer (mag.cmd context-pack, AGENTS.md ask-supplied) whose
propagation gap is live, and the corpus FTS retrieval organ.

## 7. evals-self-improvement (evals and self-improvement)

What we hold: consensus is measured illusory (0/3 agreement with strong-remote
at strength 0.6-0.67, laws.md:89); ember is the sole judge family and a second
judge is owed (laws.md:105), with a first judge2 re-look banked (12 rows, 0
flips, $0.0202, self-contamination disclosed, burns.md:105-106); the ask-bank
is thin (20 asks, want 100+ contamination-blind, laws.md:106); the PHANTOM
catch against our own ledger (164.5M headline vs summed 16,403,718 tokens,
burns.md:107-109); a dead benchmark_bridge fallback caught (always True,
burns.md:114).

Questions:

1. Multi-judge calibration: given the measured consensus illusion (0/3 at
   strength 0.6-0.67, laws.md:89) and the owed second judge (laws.md:105):
   which published multi-judge protocols raise agreement-with-TRUTH rather
   than agreement-with-each-other, and what do they cost per verdict?
2. Contamination-blind ask banks: the estate holds 20 asks and wants 100+
   provably-unseen (the D6 inversion: plain-sight verdicts invert when asks
   are hidden, laws.md:106): which contamination-resistant benchmark
   construction methods (held-out generation, canaries, dynamic/live evals)
   are current best practice?
3. Numeric/citation faithfulness: our lint's PHANTOM-NUMBER class caught the
   164.5M headline by summing usage.jsonl to 16,403,718 (burns.md:107-109):
   what published tools or methods check LLM outputs for numbers and
   citations actually present in their named sources?
4. Self-improvement without reward hacking: the gauntlet loop runs falsifier
   trials at $0.00 with a grader self-strike and a caught hidden-roll contest
   (burns.md:123-127): what evidence exists that adversarial self-play
   grading improves agents on measurable tasks without the agent learning to
   game the grader?
5. Instrument liveness: a dead benchmark_bridge fallback (always True) was
   caught in day-6 (burns.md:114): what patterns or instruments detect
   silently-dead eval harnesses (fallback masking, always-pass gates) before
   their numbers route dollars?

Estate map: feeds the improve loop (memory/improve/ + mag.cmd improve,
AGENTS.md ask-supplied), the ask bank behind the duel harness (laws.md:106),
the judge2 workstream (laws.md:105), and tools/citation_lint.py (verified this
sitting).

## 8. inference-efficiency (inference efficiency)

What we hold: routing by question-class (question explains 36.3 pct of score
variance vs family 3.6 pct; cost-per-blind-point is the champion metric,
laws.md:47) over a mostly-UNMEASURED grid (only deepseek-v4.1-flash filled,
laws.md:104); the inference-budget law (EMPTY_REASONING terminal, never refire
the same params, laws.md:34-36); cheap-seat shoulders law (laws.md:66); the
hermes_burn 402 wall (key2 credits aged out, haiku workhorse rung,
burns.md:196-198); the owed DeepSeek invoice-strength discount check
(burns.md:222-223).

Questions:

1. Cost-per-blind-point routing: with the grid mostly UNMEASURED
   (laws.md:104) and question-class the dominant variance term (laws.md:47):
   what published late-2026 cost/quality routing measurements (cascade
   small-to-big, deferral policies, model-routing benchmarks) can serve as
   priors before the estate measures its own cells?
2. Reasoning-channel budget steering: hidden reasoning eats the completion
   budget and EMPTY_REASONING is terminal-never-refire (laws.md:34-36): what
   provider/runtime mechanisms for reasoning-length steering (thinking
   budgets, effort parameters, reasoning caps) exist in late 2026, and which
   are measured against empty-content failures?
3. Cheap-seat shoulders economics (cheap seats own ask-forging, judge-two,
   and assembly, laws.md:66): which published multi-tier dispatch patterns
   (draft-verify, cheap assembly plus premium judgment) report measured
   savings without quality loss?
4. Local throughput: the GPU ladder measured Vulkan 72.97 tok/s vs CPU 6.0
   (12x) and gates FP8/MoE adoption on real demand (burns.md:135-136;
   laws.md:115): what are measured late-2026 throughputs for 7B-class MoE vs
   dense on CPU/Vulkan stacks, and what is FP8 support status in the
   llama.cpp/Ollama lineage?
5. Batch/offpeak economics: the ds_workhorse batch lane (AGENTS.md
   ask-supplied; tools/ds_workhorse.py verified this sitting) and the owed
   DeepSeek invoice-strength discount check (burns.md:222-223): what
   batch/offpeak pricing and throughput shapes do providers publish that the
   lane runner should encode?

Estate map: feeds the routing ribs
(memory/rib/RIB_MODEL_GARDEN_ROUTING.md + RIB_MODEL_GATES_20261001.md +
RIB_ROUTING_CLASSES_20261002.md, cited laws.md:28,37,47), the hermes_burn
usage ledger (memory/runs/hermes_burn/usage.jsonl, verified this sitting),
and tools/ds_workhorse.py.

---

## Receipt (what was verified, what was not)

Verified this sitting:

- Read in full: the five lens files + memory/rib/RIB_DEEPSEEK_WINDOW_20261007.md.
- Organ existence: 27 paths checked OK across two venv runs (20 in
  _organ_check.py, 5 ribs/jsonl + memory/zknot/LATEST.md in the -c batch);
  zero MISSING. Commands and outputs quoted in the Method section above.
- The RIB_DEEPSEEK_WINDOW quantize-target disambiguation
  (RIB_DEEPSEEK_WINDOW_20261007.md:64-68): it is knowledge compression, not
  model quantization; not used as a quant-area feed.

Not run this sitting: pytest, web fetches, catalog recounts, routing-cell
probes. Those instruments' latest receipts live in the lens files cited
above. Nothing in this file is asserted from memory of other sessions; every
holding cites the lens file and line it came from, and the lens files carry
their own primary receipts.
