# Frontier sweep: quantization-compression via arXiv (2026-10-05)

source-fetched: 2026-10-05
Area: quantization-compression. Feeds the deliberate-ask quantize-target law and the local
janitor tier's model cards (byte budget the 2B-4B workers can carry on this host; corpus lens
confirmed this shelf not yet inventoried).

## Doors used and their condition

- export.arxiv.org API (Atom): primary door, worked. Queries run this session:
  (a) all:"quantization" OR "quantized" AND ("tool calling"|"function calling"|"tool use"),
  (b) all:"GGUF", (c) all:"AWQ" AND "quantization", (d) quantization AND agent|agentic,
  (e) ("context compression"|"memory distillation"|"prompt compression") AND (agent|LLM),
  (f) id_list batch calls for dates and abstracts. First query attempt timed out once at 60s;
  re-issued reformulated, succeeded.
- arxiv.org/abs pages: worked for 2610.00025, 2609.36526, 2609.22114, 2609.25014, 2609.12686,
  2609.37590, 2609.38458 (after one timeout retry).
- arxiv.org/html full text: 2609.36526v1 read end to end (PAIR numbers below).
  arxiv.org/html/2610.00025v1 timed out at 60s (DEGRADED: no full text for the top item;
  the abs-page read stands, marked here and not upgraded to a full-text claim).
- ollama.com/library: timed out twice at 60s (DEGRADED). The RQ3 "what is downloadable on
  Ollama today" live check is therefore NOT VERIFIED this session; the estate-side RQ3
  evidence in this sweep is paper-carried only (Broken on Arrival, already banked 2026-09-28;
  JARQ; the PII/quantizer paper). Nothing is claimed about live Ollama availability.

## Pass 1 (broad sweep, 30+ candidates)

89 entries considered across the six queries above, 2026-09-05..2026-10-05 window preferred.
Notable in-pool but ALREADY KNOWN to the estate (verified by grep against
catalog/catalog.jsonl and all watch/inbox/frontier_olm_20260928/sweep/*.md and
watch/inbox/frontier_olm_2026-10-03/sweep/*.md write-ups, plus memory/ greps):

- 2609.32042 Quantization Thresholds Replicate (agentic tool use 8-bit to 2-bit): full raw
  text held since 2026-09-28 sweep (catalog rows 1f7bc87da923, 85168d3abf16; banked item 1 of
  frontier_olm_20260928/sweep/quantization-compression-arxiv.md).
- 2609.05881 Broken on Arrival (defective Ollama/GGUF registry artifacts): banked 09-28 and
  10-03 (catalog rows b812b3154581, 98707be2933a).
- 2609.32961 Beyond Token Savings (35k-run context-compression study): raw held, banked
  10-03 (catalog row 00145d157732).
- 2609.04748 Same Request Different Answer (cache-induced divergence 36.2 pct at 16-bit to
  75.0 pct at 4-bit): banked 10-03 x-sweep; catalog snapshot row c7975491d7ae.
- 2608.06564 Which Decisions Low-Bit Quantization Breaks (16 models, 400 BFCL tasks):
  banked item 6 of 10-03 quantization-and-compression-x.md.
- 2609.14864 GGUF-metadata throughput, 2609.26333 Disaggregated Quantization, 2609.14060
  AGENTQ backdoors, 2609.08318 AttnCompress, 2609.11192 FlexComp, 2609.31430 Anchored
  Context Distillation, 2609.32459 Harness Effects, 2609.32474 PC-SubMax, 2609.14976
  MemRiskBench, 2609.35465 Tetra Leech-lattice (2 prior sweep files), 2609.29875
  ICLR-reasoning-forgetting (3 prior sweep files), 2609.07901 Determinism-not-bias
  (6 catalog rows plus memory/runs/gathering_expedition/p2_2609.07901.pdf),
  2608.07169 Agent Memory Distillation (deep-read end to end by the 10-03 agent-memory
  sweep), 2609.04875 Execution-State Unlearning (deep-read by the 10-03 kv-cache sweep):
  all excluded as known.
- 2609.25014 Not All 4-bit Quantizers Are Equal (AWQ/GPTQ vs GGUF Q4_K_M; AWQ leaks none,
  GGUF Q4_K_M leaks 5.3 pct of planted records; mechanism: calibration-induced rounding in
  rare-token channels): catalog 0 and unbanked, but the 10-03 sweep explicitly judged it OUT
  of window (page date Sun 2 Aug 2026, confirmed by this session's abs fetch) and declined
  it. Prose only here: for RQ3 it is the sharpest published evidence that GGUF Q4_K_M and
  AWQ are behaviorally different models at the same bit width, so the quantize-target law
  should name the quantizer format, not just the bit width. Not re-banked against the
  prior OUT call; flagged for the operator to overrule if wanted.

Genuinely new items banked below: 8 (strongest first). Two more read and held in prose:
2608.11775 Sleeping Agent and 2609.30797 HasMem.

## Pass 2 (deep reads, 11 fetched pages read this session)

Abs pages read end to end: 2610.00025, 2609.36526, 2609.22114, 2609.25014, 2609.12686,
2609.37590, 2609.38458. API-door abstract reads: 2609.38599, 2609.01587, 2608.11775,
2609.30797. Full-text HTML read: 2609.36526v1. That is 11 reads, over the 5 floor; only
items I fetched myself are banked.

## Banked items (8, strongest first)

1. **Measuring the Microtask Eligibility Gap: When Is an Off-the-Shelf SLM Enough for an
   Agent Harness?** (2610.00025, page-dated Tue 1 Sep 2026; OUT by 4d vs the 30-day window
   start 2026-09-05, ID batch reads 2610 but the page says Sep 1: both recorded, page wins).
   NEW: catalog grep 0 rows, prior sweep files 0, memory phrase greps 0.
   Deep-read: abs page (HTML full text DEGRADED, timed out). The single most
   quantize-target-relevant item: 16 Qwen3 configurations (0.6B to 8B) swept on a 4-task
   microtask benchmark (auto-approve, memory write, tool selection, re-ranking) with
   CI-based eligibility thresholds; NONE passed; 4-bit RTN/GPTQ/AWQ moved none into
   eligibility; the gap tracks size, not precision; replicated on Llama-3.x. The useful
   shape survives anyway: a 4B re-ranker over BM25 shortlists beat BM25 alone
   (+0.047 [0.020, 0.073]) without certifying as eligible. Law shape: janitor-tier models
   should be gated as cheap helpers with their own thresholds, never as certified agents;
   and a quantize-target ask that promises agent competence from a 4-bit 2B-8B worker is
   contradicted by this evidence.
   Quote: "Agent harnesses increasingly want to run small language models (SLMs) on the
   microtasks around a frontier large language model (LLM) planner: auto-approving shell
   commands, writing memory, selecting tools, ranking past turns."

2. **Adapting Context Compression for Long-Horizon Agents with Counterfactual
   Continuations (PAIR)** (2609.36526, 2026-09-29, IN window). NEW: catalog 0, prior
   sweeps 0. Deep-read: abs page AND full-text HTML end to end. RQ4 core. Key claim:
   "compression degrades reliability before solvability": run-to-run Pass3 reliability
   collapses first while single-run accuracy barely moves. Method: for each compression
   boundary, restore the pre-compression state and roll out paired continuations
   (compressed vs not), estimating outcome hazard (terminal reward change) and interaction
   burden (extra steps); thresholds flag harmful compressions; an optimizer LLM rewrites
   sections of a fixed compression template; candidates validated end to end. Numbers
   (AppWorld test-normal, 168 tasks, GPT-5.6 Luna): PAIR 84.7 pct accuracy / 79.8 Pass3 vs
   no-compression 84.1 / 78.6 (exceeds the uncompressed baseline); prefix-conditioned PAIR
   85.9 / 80.4. OfficeBench 81.1 to 81.4 pct vs 82.1 baseline at about half the peak
   context (4K vs 7K tokens). Beats the best ACON variant by 2.1 to 10.0 pct Pass3.
   Revision lessons are literally quantized_thought compilation rules: preserve exact
   literals and goal constraints, reconcile summaries against newest evidence, never
   promote unsupported answers. Maps 1:1 onto law compilation: compile, then verify each
   compilation by counterfactual replay from the same state.
   Quote: "compression degrades reliability before solvability".

3. **An Empirical Cost Attribution of Context-Compression Gateways in Multi-Turn Coding
   Agents** (2609.22114, page-dated Wed 19 Aug 2026; OUT by 19d, marked). NEW: catalog 0,
   prior sweeps 0. Deep-read: abs page. RQ4 pricing. Three-lever cost model from a
   production gateway (Paritok) in front of Claude Code / Codex: (i) tool-schema filtering
   removes a fixed block per turn (21K to 57K tokens), scales linearly, the only
   unambiguously positive lever; (ii) content compression saves only about 2 pct of the
   cache-priced prefix per turn but compressed reads persist and are re-sent, cumulative
   savings grow quadratically (~3350 x N^2) until the context window caps it;
   (iii) recall of original bytes re-sends exactly what was compressed away, cost bounded
   but each recalled segment spends accumulated savings back. States that single-shot
   retention numbers ("86.5% of SWE-bench quality retained at a 25.7% compression rate")
   are orthogonal to multi-turn savings and should not be cited as evidence of savings.
   Quantized_thought pricing input: law compilation pays off only because compiled laws
   are short AND never recalled; any recall hook re-buys the bytes.
   Quote: "86.5% of SWE-bench quality retained at a 25.7% compression rate".

4. **FOCUS: Training-Free Decision-Preserving Context Compression for LLM Agents**
   (2609.37590, 2026-09-29, IN window). NEW to analysis: prior sweep files 0; one catalog
   row exists as an abstract snapshot only (state/arxiv daily pull), no deep-read banked
   anywhere. Deep-read: abs page. Recasts compression as causal decision preservation over
   discrete interaction units, training-free, test-time, attachable to closed models.
   Across tool-calling, QA, web, and multi-turn dialogue benchmarks: "cutting peak context
   by up to 48% and dependency by 73%" while improving task success by up to 8.9 points
   over uncompressed. The estate mirror: compression is legal when it provably does not
   change the decision set, which is what a compiled law asserts about itself.
   Quote: "cutting peak context by up to 48% and dependency by 73%".

5. **Residual Vector-based Reconstruction as Long-Context Recall Regardless of Context
   Window Size** (2609.12686, 2026-09-11, IN window). NEW: catalog 0, prior sweeps 0.
   Deep-read: abs page. Training-free recall with near-constant GPU memory as context
   grows: "reconstruct facts using parameter activations in the LLM's feed-forward
   layers": residual vectors stored per fact, deterministically re-decoded on query.
   Answers single-fact questions over 2M-token story contexts where prior methods fail.
   For the quantized_thought shelf: a third memory substrate (prompt text, KV cache, and
   now FFN activation side-records), notable because recall is deterministic and the
   side-record is tiny relative to raw text. Unverified here on our models; the abstract
   carries no tool-call/JSON tasks, so its structured-output behavior is OWED.
   Quote: "reconstruct facts using parameter activations in the LLM's feed-forward layers".

6. **PrivMeSA: Privacy-Aware Self-Evolving Multi-Agent System for Medicine via
   Local-Remote LLM Collaboration** (2609.38458, 2026-09-29, IN window). NEW: catalog 0,
   prior sweeps 0. Deep-read: abs page. The closest published analogue to the estate's
   law-compilation loop found this pass: a local agent consults a remote specialist; "a
   local lesson memory distills completed consultations into generalized clinical guidance
   and retrieves relevant lessons before transmission, so later cases reuse expertise
   without new remote exchanges"; RL balances accuracy against disclosure and
   re-identification risk over the full outbound transcript. MIMIC-IV-ED benchmark:
   +15.8 points mean task accuracy over plain delegation; personal-detail disclosure
   98.0 to 0.2 pct of cases; re-identification to ten or fewer registry patients 74 to
   0 pct. Map: episodic consults in, generalized rules out, rules retrieved before the
   next ask; the same shape as compiling a Hermes dispatch into a rib.
   Quote: "Clinical large language model (LLM) agents deployed locally can consult more
   capable remote models, but doing so risks exposing patient information."

7. **JARQ: Joint Alternating Refinement for Quantization** (2609.38599, published
   2026-09-29, updated 2026-10-02, IN window). NEW: catalog 0, prior sweeps 0.
   Deep-read: API abstract. RQ3/RQ1. Plug-in refinement for group-wise PTQ hosts (RTN,
   GPTQ, OmniQuant, AWQ): alternates a joint least-squares refit of all group scales with
   bounded Babai proposals moving many codes at once; no backprop; preserves bit width,
   groups, zero points, inference cost. Across Llama-2/3 and Qwen: lower perplexity in
   90 of 96 comparisons; 3-bit RTN perplexity cut up to 36 pct; under a minute per 7B
   block. Byte-budget input: the estate can hold the same GGUF byte budget and get a
   better model, or drop a bit at equal quality; Qwen-family coverage matters because
   Qwen3 is the janitor family.
   Quote: "Group-wise post-training quantizers for large language models round weights
   onto a grid that is not refit to the resulting integer codes."

8. **The Structure of Quantization Damage in LLMs: Why the Next Bit Should Be Spent
   Globally** (2609.01587, page/API-dated 2026-09-01; OUT by 4d, marked). NEW: catalog 0,
   prior sweeps 0. Deep-read: API abstract. RQ1 mechanism. Causal per-layer 8-bit
   interventions across 9 models, 4 families: no tested hypothesis (task circuits,
   computation locations, weight statistics) predicts which layers benefit; recovery is
   diffuse (8 of 9 models recover 75 pct of the gap with about half the layers;
   Qwen3-8B the exception). Spending the extra precision budget on finer global
   granularity beats targeted layer rescue by 21 to 52 points. Quantize-target input:
   at a fixed byte budget prefer uniform finer granularity over heroic per-layer mixes;
   and re-run the check on Qwen3-8B first because it is the held-out exception.
   Quote: "Post-training quantization (PTQ) is widely used to reduce the cost of serving
   large language models (LLMs), but its accuracy cost is uneven".

## Read and held in prose (not top-8)

- **The Sleeping Agent: What Gist-Based Context Compression Loses and Why** (2608.11775,
  2026-08-12, OUT by 24d). API abstract. SWC probe over all ten LoCoMo conversations
  (~1,935 questions): gist compression beats truncation on factual questions but hurts
  temporal ones because the abstraction prompt drops dates and times; a one-sentence fix
  lifts temporal-expression preservation 3.05 to 62.39 pct. Direct quantized_thought
  hazard: a compiled law that drops its effective-date or scope condition silently fails
  temporal lookups. Bankable later if the operator wants out-of-window RQ4 depth.
- **HasMem: Hard-Origin Adaptively Softened Memory** (2609.30797, 2026-09-25, IN window).
  API abstract. Frozen hard-prompt embeddings as verifiable origin states, controller
  resizes memory entries; MSC reconstruction-probe F1 95.3 (+4.4) at 93.6 pct of the hard
  reference positions; six configs beat rule-based re-encoding by 8.0 to 23.6 EM points.
  Solid but a memory substrate paper; lower estate leverage than the 8 above.

## RQ synthesis for the estate

- RQ1 (quality-vs-bits on 2B-8B, tool-calling/repo-editing): current instruments are
  agent-harness microtask suites (eligibility thresholds with CIs), BFCL-style
  tool-call decision sets, and long-horizon agent benches (AppWorld-class). Consensus
  forming across the banked items plus the already-banked 2609.32042 and 2608.06564:
  8-bit is safe on tool use; 4-bit is mostly safe on solvability; the first thing that
  breaks below 3 bits is reliability and decision margins, not single-shot accuracy;
  and SLM eligibility failures track size, not precision. Repo-editing-specific
  quality-vs-bits tables for 2B-4B models were NOT found in-window this pass (the
  nearest is the already-known July code-gen quantization study 2607.14181, outside
  window and already judged OUT by the 10-03 sweep).
- RQ2 (sub-8-bit and JSON/tool-call syntax): no new in-window paper measures structured
  syntax survival directly beyond the already-banked items (2609.32042: failures
  confabulate rather than mis-parse at the 3-to-2-bit cliff; 2608.06564: GGUF/GPTQ flip
  fewer tool-call decisions than plain rounding). The new mechanism evidence this pass
  is adjacent: cache+quantization divergence (banked) and quantizer-format divergence
  (2609.25014, prose). Estate shape-law hedge stays: verify tool-call shape post-quantize
  per format, not just per bit width. Nothing this pass contradicts that.
- RQ3 (downloadable GGUF/AWQ on Ollama today): NOT VERIFIED LIVE (ollama.com/library
  timed out twice). Paper-carried inputs: JARQ (same bytes, better quality, host-agnostic
  since it preserves bit width and layout), 2609.25014 (format is a behavioral choice),
  and the banked Broken on Arrival (registry artifacts can be silently defective; keep
  its acceptance test). An operator run of `ollama list` on the host would settle the
  live shelf in one command; not run here because the ask's door is the web, and the
  local probe was not sanctioned by this ask.
- RQ4 (compression mapping to quantized_thought): the week's strongest convergence is
  that compression must be verified against DECISIONS and RELIABILITY, not against
  perplexity or task-completion alone (PAIR, FOCUS, the banked Beyond Token Savings), and
  that recall re-buys bytes (2609.22114), so compiled laws must be recall-free by
  construction. Gist/lesson compilation loses date-like conditions silently (Sleeping
  Agent): compiled laws should carry their scope and effective-date fields explicitly.
  PrivMeSA is the working reference for the distill-then-retrieve loop; PAIR's
  counterfactual replay is the verification gate the estate can bolt onto
  quantized_thought compilation directly.

## Method receipts

- Overlap greps run this session against catalog/catalog.jsonl (1,096,848 lines) by title
  phrase and by exact arXiv ID for every candidate; against all
  watch/inbox/frontier_olm_20260928/sweep/*.md and watch/inbox/frontier_olm_2026-10-03/
  sweep/*.md write-ups by ID; and memory/ phrase greps (hits only in
  memory/percolator/candidates.jsonl, memory/runs/corpus_gap_research/,
  memory/runs/ds_batches/, memory/runs/fleet_round/, memory/runs/gathering_expedition/,
  memory/trajectory/steps.jsonl for the known items listed above).
- Dates pinned for all banked items via export.arxiv.org API id_list calls and abs pages;
  two items (2610.00025, 2609.22114) show ID-batch vs page-date mismatches (2610/2609
  prefixes vs Sep 1 / Aug 19 page dates); page dates recorded as authoritative, both
  flagged OUT-of-window in the items.
- Window: 2026-09-05..2026-10-05. Out-of-window banked items are individually marked
  (2609.22114 OUT 19d; 2609.01587 and 2610.00025 OUT 4d) per the ask's "prefer the last
  30 days" rather than excluded, because each is decisive for its RQ and unbanked.
