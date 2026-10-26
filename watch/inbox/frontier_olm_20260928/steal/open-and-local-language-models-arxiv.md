# steal card: open-and-local-language-models-arxiv (round 1, this cycle)

date: 2026-09-29. seat: steal gopher, Mag Resource Harness. round 1 of the current cycle; previous critique: none.
confirmed finds (4, from the ask): 2609.07370, 2609.23742, 2609.25373, 2609.32042. All arXiv, September 2026.
upstream bank: watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-arxiv.md (18,307 bytes, verified on disk this session via os.path.getsize). Paper facts cite that bank as bank:N; the sweep's raw receipts live in watch/inbox/frontier_olm_20260928/sweep/_raw/.

## Displacement receipt (what was at this path before this write)

This path held an earlier-cycle card, "round 2, revised per critique", covering a DIFFERENT find set: six finds (2609.21341, 2609.07370, 2609.23742, 2609.25373, 2609.33467, 2609.05881) and explicitly excluding 2609.32042 (its line 91). This cycle's ask is round 1 over four finds including 2609.32042 and excluding 21341/33467/05881, so the ask lineage differs. That card was preserved byte-identical by move (mv, nothing deleted) to: watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models-arxiv_prior-cycle-6finds.md (verified present after the move by ls). Its deeper treatments of the three shared finds are cited below as prior-cycle:N where carried; facts I re-verified myself this session carry my own command citations instead.

## Find 1: sub-2B janitors are components, not executors (arXiv 2609.07370)

Paper: "Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B SLMs for Edge Deployment", https://arxiv.org/abs/2609.07370 (2026-09-07). bank:62.

Numbers: five UNTUNED sub-2B checkpoints, 100 MCP-style prompts, CPU FP32. Qwen2.5-1.5B 75% greedy / 79% sampling recovered-call; Qwen2.5-0.5B 72% greedy but 32% sampling; Phi-1.5 0%; only 5 of 1,000 raw responses strict-parse (best condition); 89.4% of 658 failures die at JSON recovery. Bank net answer (bank:66): nothing untuned under 2B beats a gemma-class 2B janitor per published numbers.

Steal (mechanism): a janitor earns chore autonomy through a measured reliability score, and its output path always carries a JSON recovery stage, because raw strict-parse is near zero. "Bounded local tool system component, not trusted autonomous executor" is the trust contract, matching house doctrine: local Ollama janitors first, gemma:2b scut and gemma4 short worker, remote specialist scarce (AGENTS.md:5).

Organ: gopher fleet. Verified call-path surfaces this session: the janitor-agent seat in the seat router (mag/agent_state_router.py:41-48, skills janitor/classify/state_snapshot/topic_orphan; module 5,061 bytes on disk); the afk loop's janitor call defaults to gemma:2b (mag/afk_loop.py:104, `def _ollama_ask(prompt, model="gemma:2b", timeout=60.0)`); the scribe's classification model is gemma4:latest (mag/batch_scribe.py:45); the coordinator organ is registered as "file-shaped main channel and bounded gopher coordinator" (mag/organ_map.py:411-412).

Port move: adopt the released instrument (100 prompts + 1,000 responses + notebook, https://github.com/Abrar051/sml_mcp_benchmark) as the fleet's janitor trust gate: every candidate janitor gets a recovered-call score; under 70% rides supervised chores only; parse-then-verify is a required stage in the gopher chore path, never optional. Cost note carried from the prior-cycle card (prior-cycle:25, its grep evidence): no strict-versus-recovered JSON shim exists in the estate today, so this is a small net-new wrapper over the janitor Ollama call sites named above; that card's finding is carried, not re-grepped this session.

Falsifier: if gemma:2b clears 80% recovered-call on the battery, the paper's "no untuned sub-2B other than Qwen2.5 clears 80%" verdict fails on our checkpoint and the gate is overhead for us.

## Find 2: grammar-constrained chores (arXiv 2609.23742)

Paper: "Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap", https://arxiv.org/abs/2609.23742 (2026-09-20). bank:84.

Numbers: constrained decoding (Outlines, XGrammar) lifts schema validity from 78.6-92.9% to 100% across five 0.6B-4B models on 14 structured-output tasks; XGrammar overhead is 4-8 ms compile and 1.6-3.7% throughput (Outlines: 2.0-4.9 s compile, 9-13% throughput); constrained Llama-3.2-1B (0.986 content accuracy) beats unconstrained Llama-3.2-3B (0.777), though constrained-3B still beats constrained-1B (0.991); instruction-semantic failures stay CD-resistant. Practitioner line: "The cheapest reliable configuration for structured output is XGrammar with a 3-4B model."

Overlap: PARTIAL, re-verified this session by grep: catalog/catalog.jsonl:444900 row id 3507e8533740 -> state/arxiv/2026-09-22/2609.23742v1.txt, 1,191 bytes, mtime 2026-09-22; grep -c for the id returns 1. The overhead numbers, the constrained-1B-beats-unconstrained-3B result, and the practitioner line are new to the estate.

Steal (mechanism): stop buying reliability with parameters; buy it with the sampler. Schema validity is a decode-time property, enforceable at 1.6-3.7% throughput cost, so the fleet can hold the smaller model instead of scaling up for structure.

Organ: quantizer, as an EMISSION site (not a trainer). tools/thought_quantizer.py compiles memory/percolator/invariants.json into the tier files instructions_{frontier,flash,local}.jsonl (tools/thought_quantizer.py:6 and :73) and emits rows via json.dumps at tools/thought_quantizer.py:258-259. Wherever a local model drafts schema-shaped text (chore JSON, drafted instruction rows), the emission is trusted bytes with no decode-time guarantee. Honest correction this session: mag/thought_quantizer.py does not exist; the module lives under tools/ (git grep hit).

Port move: wire a grammar leg into every surface that asks a local janitor for schema-shaped output. Wiring surface is Ollama's format parameter taking a JSON schema: "Structured outputs are supported by providing a JSON schema in the format parameter" (https://raw.githubusercontent.com/ollama/ollama/main/docs/api.md, fetched this session via WebFetch). Server live-verified this session: curl http://localhost:11434/api/version returned {"version":"0.34.3"}. The prior-cycle card additionally ran a live POST with format=<schema> on gemma:2b and got a strict-parsing object (prior-cycle:33, carried, not re-run by me). Honest note: the studied engines are XGrammar and Outlines (bank:84); Ollama's enforcement is llama.cpp GBNF-class grammar decoding, not literally XGrammar. The claim ported is grammar-constrained decoding, not the library.

Falsifier: if constrained gemma:2b does NOT reach 100% schema-valid, or throughput cost exceeds 10% (well above the paper's 1.6-3.7% ceiling), the port is wrong in our stack and the quantizer keeps post-hoc validation.

## Find 3: the 270M chore specialist recipe (arXiv 2609.25373)

Paper: "Extending FunctionGemma for Practical On-Device Mobile Function Calling", https://arxiv.org/abs/2609.25373 (2026-09-21). bank:63.

Numbers: FunctionGemma 270M-it (Gemma 3 270M family, https://huggingface.co/google/functiongemma-270m-it) fine-tuned on ~9,500 synthetic schema-validated mobile-action conversations, completion-only SFT, greedy decode: end-to-end 29.3% base to 76.5% trained, 100.0% execution-aware re-scoring in-domain, 82.3% combined on Google's MobileActionsGoogle, 285.6 MB bundle, ~13 s per function-call turn on a Pixel 8 Pro.

Steal (mechanism): below gemma-class, the win is not a better general model, it is a narrow fine-tuned specialist on a fixed schema catalog. The recipe is dataset-shaped: schema-grounded synthetic conversations from the chore catalog, completion-only SFT, greedy decode. That makes it a training-data problem, which is estate home terrain: real gopher job logs already exist as candidate rows.

Organ: percolator. Candidates bank through mag/ox_percolate.py: percolate() -> NOVEL -> explore queue (mag/ox_percolate.py:10); the queue is memory/percolator/explore.jsonl, row shape {ts, source, domain, signal, canonical} (read from the file head this session; 1,720,404 bytes on disk).

Port move: file a percolator candidate: synthesize ~9,500 schema-validated estate chore conversations from real gopher job logs, LoRA a Gemma-3-270M-family checkpoint into a sub-300 MB chore specialist for one fixed chore schema. Trainer shell carried from the prior-cycle card (prior-cycle:41, verified there and file size re-verified this session): mag/lora_pipeline.py, 21,161 bytes, QLoRA 4-bit with LoRA adapters under 100 MB; its SFT spend for this purpose is NET-NEW mechanism (the pipeline shell transfers, the training data, adapter target, and eval harness are build). First target chore: the label-farm receipts chore (mag/gopher_lite.py:15), whose schema is already fixed and metered.

Falsifier: if the same SFT budget on estate chores cannot beat gemma:2b on its own narrow chore set, the recipe does not transfer and the candidate dies in the percolator.

## Find 4: the 3-bit floor and repair-as-diagnostic (arXiv 2609.32042)

Paper: "Quantization Thresholds Replicate, Failure Modes Do Not: A Three-Model Study of Agentic Tool Use in Polish from 8-bit to 2-bit", https://arxiv.org/abs/2609.32042 (2026-09-25, CC Zero). bank:65. NEW in this cycle: the prior-cycle card carried it as background only (prior-cycle:91).

Numbers: three models x six GGUF precisions on deterministic PolAgentBench: all three collapse between Q3_K_M and Q2_K (11B 0.716 to 0.045; 7B 0.463 to 0.149; PLLuM 0.224 to 0.015, paired McNemar p<0.001 each); failure modes do NOT replicate across models; a one-shot envelope-repair layer lifts the 7B from 0.448 to 0.567 at 8-bit. Benchmark CC0: https://github.com/JakubPrejzner/polagentbench.

Steal (mechanism): the cliff location is a property of quantization (replicates across models); the failure shapes are a property of the model (do not replicate). Two separable policies follow: a fleet-wide quantization floor, and a repair layer whose hit-rate distribution is itself the diagnostic that names each model's dominant defect class.

Organ: gopher fleet sizing. The fleet's models are Ollama GGUF (AGENTS.md:5); the sizing ledger exists at memory/learn/sizing.jsonl (19,663 bytes, verified this session). Local registry state verified this session: `ollama list` shows 16 artifacts (gemma:2b 1.7 GB, gemma4:latest 9.6 GB, qwen2.5:3b-instruct 1.9 GB among them); qwen3:4b is absent (grep count 0), so any qwen3:4b port needs one pull.

Port move: two rules. (1) Fleet floor: no GGUF below Q3_K_M is dispatched an agentic chore; pair with a quantcheck-style acceptance gate for every pulled artifact, per the sibling sweep find 2609.05881 "Broken on Arrival" (5 of 305 official Ollama artifacts at or under 8 GB silently solve zero of 164 tasks; https://github.com/aditi-p31/quantcheck; bank:73-74, prior-cycle:55-58 carries the tool's CLI shape). (2) Repair-as-diagnostic: log one-shot repair hit rate per model+quant into memory/learn/sizing.jsonl; the repair-class distribution is the fleet health signal.

Falsifier: if a small model at a Q2_K-class quant holds score parity with its higher-quant self on the same battery, the cliff does not bind our checkpoint and the floor law should not apply to it.

## Honest mapping gaps

These four finds feed gopher fleet, quantizer (emission site), and percolator. The sovereign mirror (configs/mirrors.json, 468 bytes, verified) and water graph (mag/water_computer.py, 32,118 bytes, verified) receive no direct port from them. Nearest adjacency: repair-as-diagnostic produces a per-model signal the water computer could route on; asserted as adjacency only, not as a port.

## The probe (one, falsifiable, this week, $0)

Grammar-on/grammar-off janitor bench on the live fleet. Everything needed is verified present: Ollama 0.34.3 live (curl /api/version this session), gemma:2b installed (ollama list, 1.7 GB), the format parameter documented (api.md fetch this session).

Run: 30 of the 100 prompts from github.com/Abrar051/sml_mcp_benchmark against gemma:2b at localhost:11434 over plain HTTP (no subprocess spawn; if any driver subprocess is used it carries CREATE_NO_WINDOW per estate law). Two arms: (a) unconstrained, (b) format=<JSON schema>. Score strict-parse rate, schema-valid rate, semantic-argument correctness, tokens/s.

Falsifiable predictions, both decidable in one afternoon:
- Find 2 predicts arm (b) reaches 100% schema-valid at under 4% throughput cost. If arm (b) misses 100% or costs more than 10%, the grammar leg is falsified for our stack.
- Find 1 predicts arm (a) strict-parses poorly (paper: 5 of 1,000 raw responses strict-parse; 89.4% of failures die at JSON recovery). If arm (a) already strict-parses above 80%, the trust gate is unnecessary overhead and 2609.07370 fails on gemma:2b.

Optional third leg on the same harness: pull one Q2_K-class quant of a small model and confirm the Q3-to-Q2 cliff (2609.32042) on our checkpoint before the floor law enters fleet policy.

## What this session verified vs carried vs OWED

Verified by running this session (2026-09-29):
1. Bank file on disk, 18,307 bytes (os.path.getsize).
2. Catalog overlap find 2: catalog/catalog.jsonl:444900, row id 3507e8533740, grep -c = 1.
3. Organ files with sizes: mag/organ_map.py, mag/agent_state_router.py (5,061), mag/afk_loop.py, mag/batch_scribe.py, mag/gopher_lite.py (10,651), mag/ox_percolate.py, tools/thought_quantizer.py, mag/lora_pipeline.py (21,161), memory/percolator/explore.jsonl (1,720,404), memory/learn/sizing.jsonl (19,663), configs/mirrors.json (468), mag/water_computer.py (32,118). Line cites verified by grep/Read: agent_state_router.py:41-48, afk_loop.py:104, batch_scribe.py:45, gopher_lite.py:14-16, lattice_loop.py:280 (num_ctx=32768), organ_map.py:411-412, ox_percolate.py:10, thought_quantizer.py:6/73/258-259. mag/thought_quantizer.py MISSING (module is tools/thought_quantizer.py).
4. Ollama live: curl /api/version = {"version":"0.34.3"}; ollama list = 16 artifacts, gemma:2b and gemma4 present, qwen3:4b absent.
5. Ollama structured outputs documented: https://raw.githubusercontent.com/ollama/ollama/main/docs/api.md (WebFetch this session); page states no minimum version.
6. AGENTS.md:5 janitor line via grep -n.
7. Displacement: prior-cycle card moved byte-identical to open-and-local-language-models-arxiv_prior-cycle-6finds.md (mv + ls verified).

Carried (cited, not re-run this session):
- Prior-cycle card's session evidence: live format=<schema> POST on gemma:2b (prior-cycle:33), JSON-recovery shim absence greps (prior-cycle:25), lora_pipeline header/LAW reads (prior-cycle:41), its round-1/round-2 review ledger (prior-cycle:65-72).
- Paper facts ride the sweep bank, which labels its own read depths (bank:58; 2609.32042 appendices tables-only, bank:113).

OWED (not run, not claimed):
- The probe has not been run; all performance predictions are the papers' numbers, not ours.
- sml_mcp_benchmark, PolAgentBench, and quantcheck not pulled or executed.
- No FunctionGemma fine-tune attempted; 270M transfer is a percolator candidate, not a result.
- XGrammar not installed or benchmarked here; the port names Ollama's format parameter (GBNF-class), not XGrammar itself.
- INDEX registration of this card in watch/inbox/INDEX.json not done by this seat (fold lane's receipt job; the prior-cycle card noted the same, prior-cycle:90).

## Receipts

Written: watch/inbox/frontier_olm_20260928/steal/open-and-local-language-models-arxiv.md, 2026-09-29, round 1 this cycle. ASCII check (em-dash, en-dash, nonascii) and char count run on this file after write via .venv/Scripts/python.exe; counts asserted only from that run.
