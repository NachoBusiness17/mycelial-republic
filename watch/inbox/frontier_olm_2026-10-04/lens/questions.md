# Lens-of-lenses: 8 frontier areas of interest (2026-10-04)

Banked by the lens-questions seat for the frontier_olm 2026-10-04 run.

Grounding: the five banked lens files in this directory (`corpus.md`, `laws.md`, `graph.md`, `burns.md`, `doors.md`), carried as summaries in the ask; verified present by `ls watch/inbox/frontier_olm_2026-10-04/lens/` this ask (5 files, burns.md 15,188 B, corpus.md 4,784 B, doors.md 3,586 B, graph.md 5,623 B, laws.md 27,370 B). I did not re-open the underlying organs (catalog rows, rib files, knowledge_graph.json, burns ledger) in this ask; every hold below cites its lens file, and nothing here is asserted beyond what those summaries or the ask state. Em-dash count in this file: zero (repo law).

---

## 1. open-and-local-language-models

**We already hold:** the LocalLLaMA door failed today (two attempts: timeout, then a "Welcome to Reddit" HTML shell; no working recipe, OWED) while HN Algolia answered turnkey (nbHits 1094 for local llama) and arXiv answered on attempt 2 (`doors.md`); free lanes stay a SENSING-only surface with verification climbing to the funded tier (`laws.md`); the UNMEASURED routing cells and the free-lane forcing contradiction (ribs grid line 192) are ribs-open (`laws.md`); NVIDIA NIM 81 models x2 keys and OpenRouter CSV closes are banked in today's git log (`burns.md`); the corpus carries 43,603 rows of AI/agent curricula and vendor docs under corpus/library, but no evals or RL shelf (`corpus.md`).

**Questions:**
1. Which open-weight models released or materially updated in the last 30 days (via the proven HN Algolia + arXiv doors, not Reddit) beat the local janitor fleet (gemma:2b scut, gemma4 short worker) on short-worker and scut tasks at comparable consumer VRAM?
2. Which of the ribs' UNMEASURED (model, tier) routing cells can be filled from public evidence (leaderboards, OpenRouter/NIM listings) without spending funded credits, and which genuinely require a live probe?
3. The pending qwen A/B probe (`burns.md`): what is the exact open comparison, and does new public evidence on qwen variants resolve it before we spend on it?
4. The free-lane forcing contradiction (grid line 192, `laws.md`): what published data exists on free-tier rate-limit windows and token ceilings that could resolve force-free versus pay-funded routing as measured law rather than operator mood?
5. For LocalLLaMA-class intel, what is a working Reddit door recipe (or a durable substitute like HN Algolia paging + arXiv listing sweeps), so the estate's richest local-LLM community stops being an OWED door?

**Estate map:** feeds the routing organs (`mag/route_chat.py`, `mag/inference_budget.py`) by filling UNMEASURED cells and grounding the driving-ladder tier assignments, and feeds corpus intake shelves for new model documentation.

---

## 2. quantization-and-compression

**We already hold:** the reasoning-quant ladder is an open probe ranked above new mining (`burns.md`); the Schmidhuber compression-progress doctrine trio was dropped then amended, with curiosity-ranked lane selection as the theory's own reward and the sqlite+skip-list GO (compress and index, never delete) as the staged organ (`burns.md` git log); deliberate-ask law names "quantize target" as part of a strong ask (`laws.md`); the corpus is thin exactly where quant research lives (no RL/post-training shelf, maths micro-shelves of 2 to 7 rows) (`corpus.md`).

**Questions:**
1. What published quantization-versus-reasoning measurements (GGUF k-quants, AWQ, GPTQ, EXL2/EXL3 at 4 to 6 bit on reasoning-capable open models) exist to fill the reasoning-quant ladder, and do any contradict a rung the estate already banked?
2. At what KV-cache quantization levels do public measurements show measurable reasoning degradation, and does that bound how aggressively the ladder can stack weight-quant plus KV-quant?
3. Does the 2026 compression-as-progress / intrinsic-reward literature (the 0812.4360 and SICE lineage we dropped, plus successors) extend or falsify the amended curiosity-scored lane-selection candidate now in the percolator?
4. For the operator's actual hardware, which quant format and bit-width do current community measurements rank best for the janitor fleet's task mix, and is that ranking stable across model families?

**Estate map:** feeds the compressor organ (`context_compression.py`, the graph's real hub per `graph.md`) and the staged sqlite+skip-list ledger, and feeds the reasoning-quant ladder probe that `burns.md` ranks above new mining.

---

## 3. agent-memory-and-continuity

**We already hold:** the knowledge graph is structurally hollow: 2,086 nodes but only 2 of 825 edges join two real nodes, 794 has_invariant edges dangle, 1,057 knowledge nodes (50.7%) have zero edges, all 400 knots are content-less stubs, all 300 case_law share the empty id `law:`, and the `maps_to` builder never fires (`graph.md`); zknot rewrites LATEST.md at logon from the last 3 sessions; warm boot loads chain tip + Vercel URLs + session brief into warm_state.json (`laws.md`/AGENTS.md load order); the estate is framed as the two-module agent (A = receipt/compression machinery, B = lane selection) with the missing wire being intrinsic reward (`burns.md` git log); oral history is 14,862 catalog rows (`corpus.md`).

**Questions:**
1. Given 1,057 unlinked knowledge nodes and 400 content-less knots (`graph.md`), what does frontier memory-graph practice (GraphRAG, Zep/Letta-lineage temporal stores) say recovers retrieval value first: linking passes, pruning, or regeneration from source rows?
2. What identity/dedup schema do current memory stores use to keep precedent rows individually addressable, as the cure for 300 case_law rows collapsing onto the shared empty id `law:` (`graph.md`)?
3. What published memory-consolidation schedules (sleep-time compute, offline reflection passes) map onto a logon-rewrite window like zknot's, without the consolidation itself drifting the way census carriers drift within hours?
4. For the two-module framing (compress module A, select module B, missing intrinsic wire), what 2025-2026 memory-selection reward designs (surprise, compression gain, retrieval hit-rate) have been measured end-to-end on harness-like workloads?
5. What do current agent-continuity results say about warm-start context size versus retrieval: is the warm_state.json brief-plus-tips shape above or below the measured knee where retrieval starts beating stuffing?

**Estate map:** feeds the memory organs (memory/rib, zknot, warm_state.json, the knowledge graph builder `mag/knowledge_graph.py`) and the percolator's candidate pipeline, because the graph lens shows the graph is the estate's thinnest held organ.

---

## 4. swarm-orchestration

**We already hold:** the fan-out width law (workflow children maxAttempts 0, keep max_concurrency at 3 or less; Task agents ride the main retry path, measured clean at widths 3, 6, 10, 12 with width 10 banking 109.4M tok/h) and the max-concurrency standing law (50 workflow children plus crons ran clean; first rate-limit contact is HOLD, not a width cut) are compiled law (`laws.md`); the flock decode redesign is a ribs-open question (`laws.md`); the corpus holds 25,413 rows of WoW-emulator/playerbot code (azerothcore 10,356, mod-playerbots 5,019, vmangos 4,397, tortoise 3,767, evennia 1,579), a literal bot-swarm codebase (`corpus.md`); night-shift lanes landed 2026-10-04 (AGENTS.md census delta).

**Questions:**
1. The flock decode redesign (ribs-open, `laws.md`): what swarm or multi-agent decode architectures in current literature address flock-shaped generation, and does any published result match the estate's flock shape closely enough to steal?
2. Which coordination mechanisms in the 25,413-row playerbot corpus (formation keeping, role assignment, leader election, threat tables) transfer to lane orchestration, and are any already reimplemented unknowingly in the lane runners?
3. What do current multi-agent frameworks publish about retry-as-orchestration versus retry-as-transport, given the estate's proven split (workflow children die on first 429, Task agents retry 11 times)?
4. What published swarm throughput-versus-width curves exist to compare against the measured 109.4M tok/h at width 10 envelope, so the untested 15-16 rung can be estimated before anyone risks a 429 storm?

**Estate map:** feeds the lane organs (queue/lanes builder/day_work/research runner_state + trail, night-shift lanes) and the workflow gate's dispatch-shape law, with the playerbot corpus as the in-house reference swarm.

---

## 5. finetuning-and-adaptation

**We already hold:** the corpus has no RL/post-training shelf at all (`corpus.md`), making this the estate's least-held area with the most organ demand; the improve loop scouts daily and files candidates through the percolator with a human promote gate; training/events.jsonl and training/loop_gaps.jsonl track loop events and gaps; the funded tier is Hermes primes (glm-5.3-prime, qwen3.8-max-prime) with local janitors beneath (`laws.md`); the Schmidhuber amend established that defects-found-per-lane was rigged by construction because severity lanes target known defects (`burns.md`).

**Questions:**
1. Which 2026 RLVR/GRPO-style post-training results on small (2 to 4B) local models are strong enough to justify building the missing post-training shelf, and what should that shelf's first 50 rows be?
2. What distillation cost/quality data exists for distilling funded-tier primes (glm-5.3-prime, qwen3.8-max-prime) into local janitors, and is a local-distill experiment worth the setup at our scale?
3. Which training/loop_gaps.jsonl gaps are closable by published fine-tuning or adapter recipes versus by context engineering the estate already holds, so the improve loop stops filing candidates the corpus cannot support?
4. What adapter (LoRA/QLoRA) practice do current local-model maintainers recommend for consumer VRAM, and does any of it match adapter receipts the estate already banked, or is this entirely unheld ground?
5. The Schmidhuber amend's metric-validity lesson (`burns.md`): what evaluation-design literature names the severity-lane confounding pattern and its standard cure, so future self-finetuning metrics are not rigged by construction?

**Estate map:** feeds the improve loop (`mag.cmd improve`, memory/improve/, percolator candidates, training/events.jsonl + loop_gaps.jsonl) and would seed the missing post-training shelf in the corpus catalog.

---

## 6. kv-cache-and-context-engineering

**We already hold:** lmcache serving source is in the corpus at 2,331 rows (`corpus.md`); context_compression.py is the knowledge graph's real top node, and the only two real edges in the graph run readable_first to context_compression/corpus_expand (`graph.md`); context-pack is the standing min-token seat pack and deliberate-ask law charges a context tax once (`laws.md`/AGENTS.md); seven inference-budget carriers sit unwired (`laws.md`); the reasoning-quant ladder probe is open (`burns.md`).

**Questions:**
1. Which lmcache KV offload/transfer features in the 2,333-row in-corpus source are unwired into the estate's serving path, and what does the upstream 2026 changelog add beyond what we hold?
2. What published context-compression results (LLMLingua lineage, KV eviction policies, soft-prompt compression) give measured compression-rate-versus-quality curves to benchmark context_compression.py against, now that the graph names it the real hub?
3. Of the seven unwired inference-budget carriers (`laws.md`), which are KV/context-shaped, and which frontier techniques (prefix caching, prompt-cache reuse) make them wireable without paid dispatch?
4. What do current context-rot and long-context degradation results set as the packing-density floor, below which context-pack should retrieve rather than compress?
5. Does KV quantization interact with the reasoning-quant ladder's rungs (the ladder probe in `burns.md`) in a way that changes which combined configuration is safe for reasoning workloads?

**Estate map:** feeds the compression and serving organs (context_compression.py, corpus_expand, mag.cmd context-pack, the lmcache shelf) and the inference-budget carriers that `laws.md` marks unwired.

---

## 7. evals-and-self-improvement

**We already hold:** the judge noise-floor probe is open and outranks new mining (`burns.md`); the corpus has no evals/benchmarks shelf (`corpus.md`); the estate already runs a dense self-measurement culture: census patrol with collected-versus-executed denominator law, violation ratchet, citation lint with PHANTOM-NUMBER detection, self-steal meter, workflow gate with self-improvement as a ledger fact; the pending DG1 adjudication is one of the 16 ribs-open questions (`laws.md`); the Schmidhuber amend recorded a rigged-metric catch (curiosity-ranked versus severity-ranked on defects-found-per-lane) (`burns.md`).

**Questions:**
1. What published LLM-as-judge variance and noise calibrations (position bias, verbosity bias, k-rater agreement floors) give an adoptable floor for the open judge noise-floor probe, so lane grading stops resting on unmeasured judge reliability?
2. Which benchmark suites for local and small models (reasoning, agentic tool use, instruction following) are gaming-resistant enough to seed the missing evals shelf, and which of those can be run on the janitor fleet at all?
3. What does the evaluation-design and reward-misspecification literature call the severity-lane confounding the Schmidhuber amend caught (`burns.md`), and what is the standard cure we can cite for future self-improvement metrics?
4. The ratchet and citation-lint gates are regression ratchets over prose and code: what do frontier harnesses publish about baseline-ratchet design (accept-by-name debt, drift patrol) that the estate has not already implemented?
5. The pending DG1 adjudication (`laws.md`): what evidence class does the holding rib require, and can frontier sources supply that class, or is DG1 blocked on an internal measurement nobody has scheduled?

**Estate map:** feeds the improve loop's grader and candidate gates (memory/improve/, percolator promote gate), the gate organs (violation ratchet, citation lint, census patrol), and the DG1 adjudication the ribs hold open.

---

## 8. inference-efficiency

**We already hold:** seven inference-budget carriers sit unwired and the UNMEASURED routing cells are ribs-open (`laws.md`); tank accounting and the qwen A/B are open probes outranking new mining (`burns.md`); the driving ladder names the funded workhorses (Hermes primes, grok-4.7) with local Ollama janitors beneath and free lanes SENSING-only (`laws.md`); the 03:00Z drain bug ("hoarding funded budget while free lanes grind") is recorded operator doctrine (`laws.md`); mag/inference_budget.py and mag/route_chat.py are the live routing organs (both modified in the working tree per the session git status); width-10 throughput 109.4M tok/h is measured (`laws.md`).

**Questions:**
1. Tank accounting probe (`burns.md`): what per-lane token/spend accounting schemas do current harnesses publish, and which fits the hermes_burn usage ledger (memory/runs/hermes_burn/usage.jsonl) without a schema migration?
2. Which UNMEASURED routing cells are fillable from public cost/latency data (OpenRouter stats, NIM listings, leaderboards) versus requiring funded live probes, and what is the minimal funded probe set?
3. What do published model-router and cascade designs (RouteLLM lineage, cascade/serving hybrids) measure for savings at quality parity, and do those curves match the estate's tier ladder well enough to wire the seven unwired carriers?
4. Is there published evidence on free-tier token ceilings and rate-window decay that resolves the free-lane forcing contradiction (grid line 192, `laws.md`) into measured law?
5. For the local janitor fleet on consumer hardware, what serving configurations (batching, quant, Ollama/vLLM tuning, KV offload via the in-corpus lmcache source) measurably lift tok/s without a hardware change?

**Estate map:** feeds the spend and routing organs (mag/inference_budget.py, mag/route_chat.py, the driving-ladder receipt trail, hermes_burn usage ledger) and closes the tank-accounting probe `burns.md` ranks as open.
