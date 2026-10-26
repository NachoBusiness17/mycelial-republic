# Lens of lenses: questions for the frontier sweep

Banked 2026-09-28 by the lens-questions seat of the frontier_olm_20260928 workflow.

Inputs: the five lens files in this directory, banked by their own asks this session:

- corpus.md: catalog/catalog.jsonl one-pass count 581,477 rows, byte size matches catalog_manifest.json map_bytes 160,053,773; covered domains (LLM/agent course libraries 41,840, frontier-lab platform scrape 97,865, session oral history 14,858, shadertoy21k 21,806, mathlib4 9,164, WoW emulation stacks, memory/corpus 25 dirs, research/ 767, arxiv pulls 3,306); gaps: no bio/econ/crypto/security corpora; shelf-vs-map library discrepancy stated not reconciled.
- laws.md: memory/corpus/quantized_thought/instructions_frontier.jsonl (24 law rows, all compiled-v0.3, all "inflated echo - provenance only") plus all 45 files in memory/rib/ (2,331 lines via wc -l); compiles 33 standing research laws and 12 open questions (consensus-decode redesign, emergence A/B ledger, planning-mode gate, knot-as-CRD, rib dispatcher, cool/heat map, self-mapping fold, Windows process attribution, persona-key threshold, party transcript wiring, ram-cache drift).
- graph.md: memory/knowledge_graph.json (schema v2, ts 2026-09-28T19:47Z, 2,062 nodes / 817 edges via three venv json.load passes); context_compression is the most connected node (degree 5); knot (400), case_law (300), doctrine (217), steal (140) carry ZERO edges; 777 invariant endpoints with exactly one genuine cross-module shared law; 409 of 996 modules fully isolated; the missing edge is law-to-module.
- burns.md: memory/burns/LEDGER.jsonl 693 rows whole, 0 parse fails; whole ledger is 09-25 to 09-28; 14 standing lanes carry 221 rows all green; 455 one-shot B2-NNN items under burn_wave_20260926/; OWED: pre-rotation ledger not located.
- doors.md: arXiv export API, hn.algolia.com, and api.fxtwitter.com all answered live 2026-09-28; old.reddit.com JSON door failed (HTML shell), root cause OWED.

Each area below is one of the estate's real research interests, refined by what the lenses say we already hold, so the sweep answers what we do NOT know instead of re-deriving what we do.

## 1. open-and-local-language-models

Held: local Ollama janitors first (gemma:2b scut, gemma4 short worker) per AGENTS.md; Hermes funded tier is the only verification rung (DRIVING LADDER, AGENTS.md, receipt memory/rib/RIB_DRIVING_LADDER_20260928.md); burns lane free-resource-landscape is 35 rows all green (burns.md); the frontier-lab platform scrape (97,865 rows) and arxiv pulls (3,306) are in the corpus (corpus.md); arXiv and HN doors are live (doors.md).

Questions:

1. Which open-weight models released since 2026-08 beat gemma-class 2B janitors on agentic tool-calling at equal or smaller VRAM, per published benchmarks the estate can name-check against the catalog?
2. What licensing or deployment changes have frontier labs made since the platform scrape (97,865 rows) that change what the estate can legally self-host and self-steal into corpus?
3. Is there any free or open-weights rung that could serve as a verification surface under the driving-ladder law, or does the sensing-only rule for free lanes (AGENTS.md DRIVING LADDER) match the published consensus on free-tier reliability?
4. What does the literature say about smallest-viable local model for structured JSON tool calls, the exact chore the janitors do, and is there a benchmark the estate could run locally to re-rank the janitor fleet?

Estate map: feeds the tier ladder and driving-ladder ribs (memory/rib/), the free-resource-landscape burn lane, Hermes dispatch routing (memory/frontier/allowance.jsonl), and catalog acquisition decisions (catalog/catalog.jsonl).

## 2. quantization-compression

Held: the quantized_thought packs compile frontier laws into instructions_frontier/local/flash jsonl, but all 24 frontier law rows are marked "inflated echo - provenance only" (laws.md); context_compression is the most connected node in the knowledge graph (graph.md); deliberate-ask doctrine says pay the context tax once (AGENTS.md clippy); the corpus has 581,477 rows that could serve as offline validation data (corpus.md).

Questions:

1. Do current 2 to 4 bit weight quantization schemes preserve tool-call JSON reliability for 2B to 8B models, per published evals, and which formats does the evidence favor for Ollama-class serving?
2. Does the literature distinguish quantizing weights from compressing instructions, and does it support or refute the estate's finding that its compiled frontier instructions are echo-only (instructions_frontier.jsonl, laws.md)?
3. What lossy context-compression methods publish measured retention numbers on agentic tasks, and can the estate validate them offline using its 581,477-row catalog as ground truth?
4. What is the state of the art in prompt compression that would shrink the deliberate-ask context tax without losing the frozen RIB + output contract shape (AGENTS.md deliberate-ask)?

Estate map: feeds the quantized_thought compile packs (memory/corpus/quantized_thought/), the context_compression hub node in memory/knowledge_graph.json, the context-pack generator (mag/context_pack.py), and the deliberate-ask ribs.

## 3. agent-memory-continuity

Held: the spine is residual + registry + leaf = filed workdays (docs/DNA.md via prior banked censuses); the verkle chain and registry are live organs; session oral history is 14,858 rows in the catalog (corpus.md); the graph shows knot, case_law, and doctrine nodes carrying zero edges and all 300 case_law nodes sharing the single unaddressable id law: (graph.md); the ribs hold open questions on knot-as-CRD and self-mapping fold (laws.md).

Questions:

1. What do 2026 agent-memory architectures (episodic retrieval, graph memory, hierarchical summarization) do that the residual-registry-leaf spine does not, and is any of it adoptable without a new substrate?
2. Is there a published CRD or merge-friendly log design that would make the knot multi-writer safe, closing the rib open question knot-as-CRD (laws.md)?
3. How do peer systems link doctrine to the code that enforces it, given the estate's graph has a missing law-to-module edge and cannot answer "which doctrine does this code enforce?" (graph.md)?
4. What published longitudinal studies mine session transcripts to predict next-session success, and can the 14,858-row oral history corpus support an equivalent estate-side study?
5. Which verifiable append-only memory log designs (merkle/verkle chained) are published outside the estate's own chain, and do any beat the current repair-and-verify loop?

Estate map: feeds the verkle chain and registry, memory/knowledge_graph.json, memory/continuity/ seat memory, the biographer (mag.cmd ask and brief), and the rib spine (memory/rib/).

## 4. swarm-orchestration

Held: fan-out width law is measured (workflow children maxAttempts 0 and max_concurrency 3 or less on the z.ai account; Task agents clean at width 10 banking 109.4M tok/h, receipts watch/inbox/gala_20260925/AFTERPARTY_CLOSE_20260926.md B2-476 and watch/inbox/burn_wave_20260926/B2_443_dwf_error_census_20260926.md per AGENTS.md); max-concurrency standing law records 50 workflow children running clean for hours; 14 standing burn lanes carry 221 green rows (burns.md); the rib dispatcher is an open question (laws.md); the MCP bridge design is banked but R1 through R5 are unimplemented (recent commit 93b5a96d7 message).

Questions:

1. What dispatch shapes do peer fleets use under provider rate caps, and is retry-on-shape (maxAttempts 0 children, main-session retries) matched or beaten by any published design?
2. Is there a published inter-agent handoff or dispatch protocol that answers the rib open question rib dispatcher (laws.md) better than the current burn-lane + rib_bus pattern?
3. What MCP multi-server orchestration patterns are current, given the estate's bridge design extends three organs (tools.TOOL_MAP, ROLE_TOOLSETS in mag/mcp_server.py, effect_broker authority chain) and has not been built?
4. How do published workflow engines do mid-run steering (reviewer feedback revising in-flight asks), the shape the workflow gate already enforces as dogfood?
5. What do peers report as failure modes for 50-wide concurrent agent fan-out, and does the estate's first-contact-as-HOLD signal rule (AGENTS.md max-concurrency law) match or diverge?

Estate map: feeds the workflow gate (tools/workflow_gate.py), rib_bus doctrine (memory/rib_bus/), the fan-out and max-concurrency ribs, mesh/panel organs (chan rows, wants), and the MCP bridge rollout.

## 5. finetuning-and-adaptation

Held: the fleet's training-data doctrine is code-agent-data (room.jsonl rows and seat session tapes are the training corpus for successors, .agents/skills/code-agent-data/SKILL.md); memory/agent_corpus/ is the organ; the 581,477-row catalog and 14,858-row oral history are the mining source (corpus.md); the funded tier is glm-5.3-prime / qwen3.8-max-prime with about 180 to 220 dollars of Nous credits (AGENTS.md, burns.md); no published finetuning run of the fleet's own tapes is known to this lens.

Questions:

1. What QLoRA or LoRA recipes do published tape-to-model pipelines use to turn agent session logs into a fine-tuned small model, and at what data scale do they report first gains?
2. What corpus cleaning gates (dedup, PII scrub, provenance tags, quality scoring) do published pipelines run that the corpus-grade judging doctrine lacks?
3. Do published results show a fine-tuned 2B local model beating a prompted frontier model on narrow agentic chores, the janitor workload shape, and by how much?
4. Is synthetic distillation from the funded tier into local weights cost-effective within the estate's credit budget, per published distillation cost curves?
5. Has anyone published a continual-adaptation loop where the model's own filed workdays become the next training set, the estate's DNA cycle, and what did they learn?

Estate map: feeds memory/agent_corpus/ and the code-agent-data doctrine, the catalog as mining source (catalog/catalog.jsonl), the ollama janitor fleet, and the percolator candidate loop (memory/percolator/).

## 6. kv-cache-and-context-engineering

Held: the ZCode operating playbook verified byte-identical asks for cache hits against harness source (corpus/steal/ZCODE_OPERATING_PLAYBOOK_20260925.md per AGENTS.md); memweave doctrine says feed structures not prose (.agents/skills/memweave/SKILL.md); context-pack is the min-token seat pack (mag.cmd context-pack); ram-cache drift is an open rib question (laws.md); context_compression is the graph's most connected node (graph.md).

Questions:

1. What published prompt-cache design patterns for agent loops (stable prefixes, append-only context, byte-identical asks) go beyond what the ZCode playbook already verified, and are there measured hit-rate numbers?
2. Does the literature give evidence that structure-not-prose context injection (memweave) measurably improves attention fidelity or cache behavior, and what experiment would replicate it estate-side?
3. What is the current state of KV-cache quantization and offload for llama.cpp or Ollama-class serving of 2B to 8B models, and does it change the janitor model choice or context budget?
4. What mechanism explains KV or ram-cache drift across long agent sessions in published reports, and can it close the rib open question ram-cache drift (laws.md) with a cited cause?
5. What context-window engineering do published long-horizon agents use at the 100k-plus turn scale, and what transfers to the estate's compaction-amend loop?

Estate map: feeds mag/context_pack.py, the memweave and memlance doctrine skills, the prompt-cache laws inherited from ZCode's playbook, janitor serving configs, and the warm boot path (mag/hermes_warm_boot.py).

## 7. evals-and-self-improvement

Held: the percolator plus invariants plus verkle chain is the continual-learning cycle (frontier-researcher skill, .agents/skills/frontier-researcher/SKILL.md); the graph shows 777 invariant endpoints with exactly one genuine cross-module shared law and 409 of 996 modules isolated (graph.md); the census carrier tripwire, ratchet, and scenario suite are machine-enforced (AGENTS.md build discipline, tools/census_drift_patrol.py, tools/violation_ratchet.py, tools/workflow_gate.py); emergence A/B ledger and planning-mode gate are open rib questions (laws.md); test census 2,303 collected / 352 files (2026-09-27 census per AGENTS.md).

Questions:

1. What eval instruments do published self-improving agent systems use to prove a promoted invariant actually changed behavior, and does the percolator promote gate have an equivalent or a gap?
2. Is there a published A/B ledger design for emergence claims that answers the rib open question emergence A/B ledger (laws.md)?
3. Which published benchmarks target regression-catching evals for agent loops (drift, staleness, fabrication), and how do the estate's tripwires (census drift patrol, violation ratchet, workflow gate scenarios) compare in coverage?
4. What failure modes do published continual-learning loops report when verification is skipped or self-graded, and does the driving-ladder verify-at-funded-tier rule match the reported evidence?
5. Can published code-to-doctrine linking methods (doc-to-code traceability, spec mining) auto-derive the missing law-to-module edge the graph lens found absent (graph.md)?

Estate map: feeds memory/percolator/ (explore.jsonl, invariants.json), the frontier-researcher organ, the test census carriers (tools/census_drift_patrol.py), the violation ratchet, and the workflow gate scenario suite.

## 8. inference-efficiency

Held: the measured envelope is 109.4M tok/h at width 10 with zero surfaced 1302s (fan-out law receipts per AGENTS.md); janitors are gemma:2b and gemma4 on local Ollama (AGENTS.md); shadertoy21k (21,806 rows) is the GPU-adjacent corpus (corpus.md); consensus-decode redesign, cool/heat map, and Windows process attribution are open rib questions (laws.md); burn lanes are green (burns.md).

Questions:

1. What speculative or consensus decoding schemes are current for small local models, and does any published design answer the rib open question consensus-decode redesign (laws.md)?
2. Which serving stack gives the best tokens-per-second on Windows for 2B to 8B models (llama.cpp builds, Ollama forks, vLLM local), per recent public benchmarks the estate can replicate?
3. What published profiling methods attribute GPU, RAM, and process cost to specific agent lanes on Windows, and would one close the rib open question Windows process attribution (laws.md)?
4. What activity or energy profiling maps cool versus heat work per lane, answering the rib open question cool/heat map (laws.md), and is there a tool that works without kernel drivers?
5. Are there 2026 kernel or quantization wins that change the throughput economics of the measured 109.4M tok/h envelope, or is dispatch shape still the binding constraint?

Estate map: feeds the ollama janitor lanes, the GPU-adjacent corpus (shadertoy21k in catalog/catalog.jsonl), burn-wave throughput measurement (memory/burns/LEDGER.jsonl), and Hermes dispatch economics (memory/frontier/allowance.jsonl).

## Sweep notes from the doors

doors.md says the arXiv export API and hn.algolia.com doors are proven working as of 2026-09-28, so the sweep can fetch both directly; the old.reddit.com JSON door failed and any reddit question above must route around it or re-probe it first. Corridor gaps the sweep should not re-derive: the catalog's own holdings (corpus.md), the 33 standing laws (laws.md), the graph's zero-edge islands (graph.md), and this week's 221 green lane rows (burns.md). OWED items inherited: reddit door root cause, pre-rotation burn ledger, shelf-vs-map library reconciliation.
