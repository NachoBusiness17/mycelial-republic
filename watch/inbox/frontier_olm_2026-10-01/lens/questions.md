# Lens-of-lenses: 8 frontier sweep areas, refined by the estate's own holdings

Banked: 2026-10-01, seat `lens-questions`. Inputs: the five lens files in this directory
(`corpus.md`, `laws.md`, `graph.md`, `burns.md`, `doors.md`), each written by a prior lens
ask this window. Every "we already hold" claim below cites the lens file that carries it;
the lens files themselves are the receipts. No new corpus, graph, ledger, or door probes
were run in this ask; anything not carried by a lens is marked OWED or omitted.

## What the lenses say we hold (the refinement base)

- **Corpus (lens/corpus.md):** 691,788 catalog rows across nine domains; agent-platform
  source (97,865 rows, incl. facebook 10,971, BerriAI 9,281, cline 3,936), LLM curricula
  (42,961: ms-genai 12,142, openai-cookbook 3,120), MMO emulation (23,765), shaders
  (21,806), mathlib4 (9,164), session/oral histories (14,859 + ghost 22,356), estate
  memory (407,098), web3 (1,381), esoterica. No pocket for bio, chips, robotics, climate,
  medicine, econ. Sweep must grep corpus before relearning agent platforms, curricula, and
  MMO domains.
- **Laws (lens/laws.md):** 37 standing laws in five groups (honesty, money, process,
  record, frontier conduct), all path:line cited. Twelve open research questions named,
  including: flock decode redesign, world-rib contract, planning-mode gate, second judge
  family, cool/heat lane map, relational memory eval, one-bug falsifier, reasoning tax.
- **Graph (lens/graph.md):** knowledge_graph.v2 has 1,787 unique ids / 825 edges, but 794
  edges are `has_invariant` attribute slugs with only 2 node-to-node resolutions; 217
  doctrines, 400 knots, 140 steals carry zero edges; all 300 case_laws collapsed onto the
  single id `law:`; 427 of 1,020 modules unlinked. The graph catalogs self-descriptions,
  not relationships: law-to-organ, knot-to-decision, case-to-precedent are the unknowns.
- **Burns (lens/burns.md):** old ledger unchanged since 09-28 (693 rows, 14 standing burn
  lanes); hermes descent window 1 closed 2026-10-01 with `usage.jsonl` at 16 rows /
  $5.9155 (13:11 to 13:53Z), 9 deliverables, A1 + C1 assembled (carrier healed turn-2
  no-echo + turn2_only; C1 includes the Ollama/transformers fork re-derivation the Descent
  Protocol paid for, receipt `watch/inbox/hermes_burn/WINDOW1_STATE.md`). Prior olm
  carriers: `frontier_olm_20260928/` (21 finds, 13 steal cards) and
  `frontier_olm_2026-09-30/` (45 sweep files, 6 steal cards; register/DIGEST still OWED).
- **Doors (lens/doors.md):** arXiv export API OPEN (Atom XML, recipe quoted in file), HN
  Algolia OPEN (JSON, recipe quoted), fxtwitter OPEN (jack/status/20, code 200),
  old.reddit.com r/LocalLLaMA top.json BLOCKED (HTML welcome page; retry via www.reddit or
  curl UA is OWED before relying on that door).

The eight areas are the estate's standing research interests; each is narrowed so the
sweep answers something the estate does not already hold, and each names the organs it
feeds.

---

## 1. open-local-language-models

**Held:** local janitors `gemma:2b` scut and `gemma4` short worker are the first rung
(AGENTS.md Commands/context); descent window 1 re-derived an Ollama/transformers fork the
estate already knew (lens/burns.md, the C1 lesson); LocalLLaMA reddit door is BLOCKED so
local-model signal must flow through the arXiv and HN Algolia doors (lens/doors.md); LLM
curricula pocket holds 42,961 rows (lens/corpus.md).

**Questions:**
1. Which open-weight families released or materially updated in Sep-Oct 2026 (Qwen,
   Llama, Gemma, Phi, Mistral, DeepSeek lines) offer a credible upgrade over gemma:2b /
   gemma4 for janitor-class local duty at 8B or below on consumer hardware, and under
   which licenses?
2. What measured evidence exists (2026 papers, issue trackers, benchmarks) that small
   open models differ in refusal/censorship behavior across runtimes (Ollama vs
   transformers), extending the C1 censorship program's E1-E3 experiment design?
3. What do current HN Algolia threads and arXiv preprints report about changes in local
   inference stacks (llama.cpp, Ollama, vLLM, MLX) in the last 60 days?
4. Which new releases ship day-0 GGUF/quant builds, and what RAM/VRAM footprints are
   reported per quant, so the sweep can hand the janitor lane a drop-in candidate?

**Estate map:** feeds the local janitor seats (gemma:2b scut, gemma4 short worker) and
the driving ladder's sensing-versus-judgment split (AGENTS.md DRIVING LADDER; lens/laws.md
money group), giving the sweep a concrete replacement-or-keep verdict for the bottom rung.

## 2. quantization-compression

**Held:** the deliberate-ask law demands a quantize target on every strong ask (AGENTS.md
Clippy bullets); the context_compression module is among the 27 top out-degree modules in
the graph (lens/graph.md); the corpus's shader/MMO/source pockets are heavy in exact
numeric and memory-bound code (lens/corpus.md), useful for compression method mining.

**Questions:**
1. Which quantization formats (GGUF K-quants, AWQ, GPTQ, EXL2/EXL3) currently give the
   best measured quality-per-byte for 2B to 8B janitor-class models on llama.cpp /
   Ollama, with benchmark citations?
2. What is the measured quality delta (task-specific, not folklore) at Q4 vs Q8 for
   current small models, stated with hardware and task conditions per the honesty law
   that a verdict without its conditions is not a verdict (lens/laws.md)?
3. Are there 2026 techniques compressing KV cache or context rather than weights
   (quantized KV, window/sink tricks) that fit a local-first harness, and what quality
   cost do they report?
4. What do frontier labs publish on distilling reasoning models into small deployable
   form factors, and which recipes are reproducible without datacenter hardware?

**Estate map:** feeds the deliberate-ask quantize target and the janitor seats' hardware
envelope, so every descent sherpa leg can size its local baseline model precisely before
any premium dispatch.

## 3. agent-memory-continuity

**Held:** ribs (47 files), warm boot, residual + registry + leaf DNA, memlance/memweave
seeding, and the graph whose edges are mostly self-descriptions (lens/graph.md); the
laws lens names "relational memory eval" and "world-rib contract" as open (lens/laws.md);
the corpus holds 407,098 estate memory rows plus 14,859 session/oral-history rows
(lens/corpus.md).

**Questions:**
1. How do frontier agent systems and the agent-platform sources already in the corpus
   (facebook, cline, BerriAI harvests, lens/corpus.md) implement persistent cross-session
   memory, and which structures map onto rib / residual / registry / leaf?
2. What evaluation methodology exists for relational (entity-relation) memory in agents
   that the estate can steal to close its own "relational memory eval" open question?
3. What memory write policies (what to keep, when to compact, how to invalidate) do
   current systems publish, as candidate material for the caches-auto-invalidate and
   chain-is-truth laws (lens/laws.md record group)?
4. What entity-resolution / dedup approaches exist for repairing knowledge-graph
   collapse of the kind the graph lens found (300 case_laws on one id `law:`,
   lens/graph.md), applicable to knowledge_graph.v2?

**Estate map:** feeds the rib system, warm boot, and the knowledge graph builder (the
collapsed law:/case_laws ids and missing law-to-organ edges in lens/graph.md), plus
memlance/memweave seeding of future seats.

## 4. swarm-orchestration

**Held:** fan-out width law (Task agents width 10 measured at 109.4M tok/h, workflow
children maxAttempts 0) and the max-concurrency standing law (AGENTS.md; lens/laws.md
process group names one controller); the "flock decode redesign" open question
(lens/laws.md); the workflow gate enforces per-item named actors, pass-off, steering, and
incremental report salvage (AGENTS.md build discipline).

**Questions:**
1. What fan-out and retry shapes do 2026 orchestration systems and papers use to survive
   provider rate limits, and how do they compare to the estate's measured split
   (maxAttempts 0 children vs maxAttempts 11 Task agents, rolling-throughput limit)?
2. What is the current state of flock / multi-model decode (cheap models voting,
   speculative ensembles, consensus decode) that the "flock decode redesign" open
   question should build on?
3. Which patterns exist for controller-of-controllers in multi-agent frameworks, and
   what failure modes do their reports name, against the one-controller law?
4. What per-agent-turn cost accounting do published swarm systems provide, comparable to
   the estate's per-turn usage banking in `memory/runs/hermes_burn/usage.jsonl`
   (lens/burns.md)?

**Estate map:** feeds the orchestrator, the fan-out width and max-concurrency laws (the
dispatch-shape retry strategy in AGENTS.md), and the flock decode redesign open question
carried in lens/laws.md.

## 5. finetuning-adaptation

**Held:** session tapes and room.jsonl are already positioned as training corpus by the
code-agent-data skill; the corpus holds 97,865 agent-platform source rows and 407,098
memory rows as raw material (lens/corpus.md); descent window 1 banked A1 + C1 programs
with an E1-E3 experiment design (lens/burns.md).

**Questions:**
1. What are current (2026) QLoRA/LoRA practice points for 2B to 8B models on a single
   consumer GPU, including data-quality gates for noisy session-derived corpora?
2. Does fine-tuning beat retrieval/prompt-stuffing for domain-jargon tasks (estate law
   vocabulary) at 2B scale, per any measured ablations the sweep can cite?
3. What synthetic-data pipelines convert agent session logs into instruction-tuning pairs
   without leaking secrets, and how do they gate provenance per row?
4. What do recent papers report on catastrophic forgetting under continual adaptation of
   small models, relevant to a rolling estate-corpus training loop?

**Estate map:** feeds the code-agent-data training-corpus organ (room.jsonl and seat
session tapes toward QLoRA), the C1 experiment program from descent window 1
(lens/burns.md), and the small-model seats on the tier ladder.

## 6. kv-cache-context-engineering

**Held:** byte-identical asks are required for cache hits per the operating playbook
(AGENTS.md); caches-auto-invalidate is a record law (lens/laws.md); the hermes carrier
defect class (turn-2 empty echo) was named and healed in window 1 (lens/burns.md,
WINDOW1_STATE.md); memweave feeds structures, not prose; `mag.cmd context-pack` is the
min-token pack.

**Questions:**
1. What prefix/prompt caching behaviors do current inference servers and APIs (llama.cpp,
   Ollama, vLLM, frontier APIs) expose, and how must asks be shaped byte-stable to hit
   them, extending the ZCode playbook's byte-identical law?
2. What measured results exist for structure-fed versus prose-fed context (summaries,
   schemas, memlang-like structures) on task quality, giving memweave doctrine numbers?
3. What are current KV-cache eviction and quantization strategies for long agent
   sessions, and what quality cost do they report at 2026 context lengths?
4. What does current literature say about long-context degradation (lost-in-the-middle
   class) at 2026 window sizes, to budget `mag.cmd context-pack` and carrier echoes?

**Estate map:** feeds `mag.cmd context-pack`, the memweave structure-feeding doctrine,
the hermes carrier (the turn-2 no-echo defect class healed in window 1, lens/burns.md),
and the byte-identical cache-hit playbook in corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md.

## 7. evals-self-improvement

**Held:** percolator + 47 invariants + verkle chain loop is the continual-learning cycle
(frontier-researcher skill); the violation ratchet is self-steal with exit-2 blocking
(AGENTS.md); the laws lens names "second judge family", "one-bug falsifier", "cathedral
tiebreaks", and the unmeasured emergence-compounding signal as open (lens/laws.md); the
descent protocol's falsifier is spend theater (lens/laws.md process group); a duel
harness exists in the tree (tests/test_duel_harness.py per the AGENTS.md census bullet).

**Questions:**
1. What does 2026 evidence say about LLM-as-judge reliability and bias, and about using
   a second judge family to debias, answering the estate's "second judge family" open
   question?
2. What duel/arena methodologies (pairwise, Elo, Bradley-Terry, style control) do current
   eval systems use for cheap-versus-premium model comparison, applicable to the duel
   volume leg named in the window 1 close (lens/burns.md)?
3. What falsifiable self-improvement loops exist in literature or frameworks whose
   success metric is banked artifacts, matching the descent protocol's anti-spend-theater
   falsifier?
4. What benchmark-contamination detection methods are current, so estate evals stay
   honest under the trust-bytes law?
5. What measurable definitions of emergence avoid the consensus illusion flagged in the
   laws lens frontier-conduct group, usable for the emergence-compounding open question?

**Estate map:** feeds the percolator + invariants + verkle chain loop (frontier-researcher
cycle), the workflow gate's scenario suite, the duel harness lane, and the claims-desk
tri-state verdicts in lens/laws.md honesty group.

## 8. inference-efficiency

**Held:** the tier/driving ladder routes cheap-first, with descent leg 1 demanding a
~$0.001 sherpa baseline before any $0.4+ premium ask (AGENTS.md DESCENT PROTOCOL;
lens/laws.md money group); "reasoning tax" and "cool/heat lane map" are open questions
(lens/laws.md); the tokenomics module sits in the graph's top out-degree band
(lens/graph.md); window 1 ledger closed at $5.9155 across 16 usage rows (lens/burns.md).

**Questions:**
1. What are current measured costs and latencies of reasoning/thinking tokens across the
   funded lanes (glm-5.3-prime, qwen3.8-max-prime, grok-4.7) and open models, to
   quantify the "reasoning tax" open question with numbers?
2. Which techniques (speculative decoding, draft models, batching, thread pinning)
   measurably speed local Ollama-class janitors on consumer hardware, and what
   throughput do they report?
3. What routing frameworks choose cheap-versus-premium per task with measured accuracy
   deltas, as candidates for the cool/heat lane map open question?
4. What is published on provider concurrency/rate-limit envelopes and prefix reuse that
   can be compared against the estate's rolling-throughput finding (width 10 clean,
   15-16 untested, AGENTS.md fan-out law)?
5. What throughput-per-dollar benchmarks exist in 2026 for small-model serving stacks
   (llama.cpp vs vLLM vs Ollama) on the hardware class the estate actually runs?

**Estate map:** feeds the tier/driving ladder (ollama to free lanes to flash to
primes/grok), the hermes_burn ledger and per-turn usage banking
(`memory/runs/hermes_burn/usage.jsonl`, lens/burns.md), and the tokenomics module flagged
at max out-degree in lens/graph.md.

---

## Sweep conduct notes (from the doors lens)

- Use the OPEN doors and their banked recipes: arXiv export API and HN Algolia
  (lens/doors.md quotes both recipes verbatim); fxtwitter for X posts.
- The old.reddit r/LocalLLaMA door is BLOCKED as probed; retry via www.reddit.com or a
  curl user-agent is OWED before any LocalLLaMA-dependent find is claimed.
- Grep `catalog/catalog.jsonl` pockets before relearning agent platforms, LLM curricula,
  and MMO domains (lens/corpus.md); the nine held domains are listed in the refinement
  base above.
- Per lens/burns.md, the `frontier_olm_2026-09-30/` register/DIGEST is still OWED; if
  this sweep's finds supersede those steal cards, close that debt in the same landing.
