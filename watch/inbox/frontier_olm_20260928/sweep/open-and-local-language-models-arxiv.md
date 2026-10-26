# frontier sweep: open and local language models via arxiv

source-fetched: 2026-09-28
Area: open-and-local-language-models via arxiv. Seat: sweep gopher, Mag Resource Harness.
Feeds: tier-ladder and driving-ladder ribs (memory/rib/RIB_DRIVING_LADDER_20260928.md:14-23, free lanes sensing-only), free-resource-landscape burn lane (janitor model choice), Hermes dispatch routing (memory/frontier/allowance.jsonl), catalog acquisition (catalog/catalog.jsonl).

## Doors used and degradations (honest ledger)

- Door 1, arXiv API (export.arxiv.org): 3 parallel WebFetch calls ALL returned HTTP 429 (arXiv rate limit punishes parallel hits). Degraded to serialized curl with 4s sleeps, UA "MagResourceHarness-frontier-sweep/1.0", saving raw XML receipts. 8 queries x 40-50 results each returned HTTP 200. Raw receipts: watch/inbox/frontier_olm_20260928/sweep/_raw/q_a_toolcall.xml through q_h_smallslm.xml.
- Door 2, arXiv listing pages (arxiv.org/list/cs.CL/recent, /list/cs.LG/recent): fetched, 91,929 and 87,893 bytes, saved as list_csCL.html and list_csLG.html. NOT parsed line by line; the API results carried the pass. Listed here as fetched, not mined.
- Door 3, WebSearch site:arxiv.org: ran once ("frontier lab open weights license change September 2026 self-host"), worked clean this window (no 1302 wall hit). Surfaced the Hugging Face State-of-Open-Models post, fetched and read.
- Dead end declared: the search result "Open-weight models 2026: which to use, which license" pointed to https://slash-digital.io, but fetching it yields a Bogota design studio homepage with none of the claimed content. That source is DISCARDED, never banked.
- Pass 2 full texts: 8 papers, abs + native HTML both HTTP 200 (arxiv.org/abs/<id>, arxiv.org/html/<id>), stripped to text by watch/inbox/frontier_olm_20260928/sweep/_raw/strip_html.py via the repo venv python.

## Pass 1, broad sweep

275 unique arXiv entries dated 2026-08-29 through 2026-09-28 surfaced across the 8 queries (parse_arxiv.py output: "UNIQUE-ENTRIES 275 IN-WINDOW 275 OUT-OF-WINDOW 0"). 28 shortlisted with abstracts dumped (dump_shortlist.py, 27 of 28 found; 2609.33917 not present in any query result and never fetched). Full list in _raw output; explicit consider-list (id | date | verdict):

1. 2609.07370 | 09-07 | DEEP: sub-2B MCP-style tool-call benchmark, estate-janitor core
2. 2609.23742 | 09-20 | DEEP: constrained decoding x scale, structured JSON chore
3. 2609.25373 | 09-21 | DEEP: FunctionGemma 270M mobile function calling
4. 2609.32042 | 09-25 | DEEP: GGUF Q8-to-Q2 agentic tool use, VRAM envelope law
5. 2609.33467 | 09-27 | DEEP: cheap/open verifiers for post-training
6. 2608.30005 | 08-30 | DEEP: SLMs as rubric judges
7. 2609.21341 | 09-18 | DEEP: 39 local models driving a database agent
8. 2609.05881 | 09-05 | DEEP: silently defective GGUF artifacts in registries
9. 2609.28003 | 09-23 | hold: graph memory for SLM tool agents, structural errors taxonomy
10. 2609.33141 | 09-27 | hold: on-device NL-to-action caches, classifier-centric
11. 2609.27669 | 09-23 | hold: SLM KGQA path-faithfulness
12. 2609.24985 | 09-21 | hold: critical-state diagnosis for multi-turn tool RL
13. 2608.30250 | 08-31 | hold: workflow DAG generation with non-reasoning LLMs (janitor class)
14. 2609.10962 | 09-10 | hold: unrepaired MCP registry census (24,135 servers) vs tool-use benchmarks
15. 2609.23959 | 09-21 | hold: calibrated one-pass scam screening, SLM (JevLite)
16. 2609.26550 | 09-22 | hold: JEV-as-a-judge, accept-when-confident escalate-when-unsure
17. 2609.33955 | 09-27 | hold: LLM-judge measurement systems for multi-turn agents
18. 2609.29333 | 09-24 | hold: where LLM graders break, 171 configs
19. 2609.33812 | 09-27 | hold: run-to-run variance of coding agents on open weights, 584 runs
20. 2609.32021 | 09-25 | hold: hidden tool-call backdoors in open-weight agents (supply-chain)
21. 2609.32638 | 09-26 | hold: open-weight LLMs as synthetic survey populations
22. 2609.13559 | 09-11 | hold: carbon-aware routing for function calling, edge-cloud
23. 2609.13470 | 09-11 | hold: SLM orchestration dynamics
24. 2609.05736 | 09-04 | hold: harness selection for fixed-model tool agents
25. 2609.07280 | 09-07 | hold: CTI merging with SLMs (stealth-adjacent)
26. 2609.09476 | 09-08 | hold: functional tokens vs readable schemas, vehicle SLM function calls
27. 2609.05395 | 09-04 | hold: KOPA-Bench, multi-step tool calls over Korean public APIs, on-prem mandate
28. 2609.30258 | 09-24 | drop: gradient inversion (wrong id pulled into shortlist; the DAG paper is 2608.30250)
29. 2609.33965 | 09-27 | drop: token energy methodology, off-area
30. 2609.21341 companion | n/a | 2609.32459 harness effects in SWE agents, noted via 21341 related work
31. 2609.19425 | 09-16 | drop: fast tree-search self-improvement, off-area
32. 2609.11133 | 09-10 | drop: disaggregated serving power control, off-area
33. 2609.28653 | 09-23 | drop: retrieval actions, weak fit
34. 2609.29191 | 09-26 | drop: redaction framework, weak fit

That is 34 considered explicitly on top of the 275 triaged by title/date in the parse output.

## Pass 2, deep reads

Read depths, honestly labeled. END TO END = full narrative text read this seat (intro through conclusion, appendices are tables): 2609.07370, 2609.23742, 2609.21341, 2609.25373, 2609.32042. CORE-READ = abstract, intro, methods, results, discussion read; appendices and parts of later sections not read: 2609.33467, 2608.30005, 2609.05881.

### Q1: open-weight models beating gemma-class 2B janitors on agentic tool-calling at equal or smaller VRAM

- 2609.07370 (Beyond Fluent Generation): five UNTUNED sub-2B checkpoints on 100 MCP-style prompts, CPU, FP32: Qwen2.5-1.5B 75% greedy / 79% sampling recovered-call; Qwen2.5-0.5B 72% greedy but 32% sampling; Phi-1.5 0%; Pythia-1.4B max 3%; TinyLlama-1.1B-Chat max 7%. Strict whole-response JSON: only 5 of 1,000 raw responses parse without recovery (best condition). 89.4% of 658 failures die at JSON recovery. CPU probe: Qwen2.5-1.5B 7,960 MiB RSS / 30.782 s mean latency; Qwen2.5-0.5B 3,637 MiB / 10.627 s. Verdict: no untuned sub-2B checkpoint other than Qwen2.5 clears 80%; family and instruction tuning dominate parameter count. Repo with 100 prompts + 1,000 responses: https://github.com/Abrar051/sml_mcp_benchmark
- 2609.25373 (FunctionGemma): FunctionGemma 270M-it (Gemma 3 270M family, https://huggingface.co/google/functiongemma-270m-it) fine-tuned on ~9,500 synthetic schema-validated mobile-action conversations: end-to-end accuracy 29.3% base to 76.5% trained; execution-aware re-scoring 100.0% (every remaining strict error is a recoverable optional-boolean omission); combined model 82.3% on Google's MobileActionsGoogle. 285.6 MB .litertlm bundle on a Pixel 8 Pro, ~13 s per function-call turn. Verdict: a sub-gemma-2B SPECIALIST beats untuned gemma-class janitors on its own narrow chore; the recipe (schema-grounded synthetic data, completion-only SFT, greedy decode) is stealable for estate chores.
- 2609.21341 (database agent): 39 open-weight models via Ollama, 8,199 runs, 2,100 model-attributed losses; 75.7% of losses came from runs that had invoked at least one tool (transport 36.2% largest class, capability 17.3% smallest). Per-model locked cells of 30: qwen3:4b 30/30, qwen3.6:35b 30/30, qwen3.5:27b 30/30, qwen3-coder:30b 30/30, gpt-oss:20b 30/30, granite4.2:3b 28/30, gemini-3.5-flash-lite 28/30 (hosted control), deepseek-r1:8b 27/30, llama3.1:8b 23/30, qwen3.5:2b 16/30, qwen3:1.7b 12/30. Five server-side fixes moved six models by 6 to 21 cells of 30. Verdict: capability-threshold framing is wrong at this scale; qwen3:4b is the cheapest full-lock agent in their corpus; harness repairs lift small models more than size does. This is the estate's own effect-broker/switchboard doctrine, field-proven by strangers.
- 2609.32042 (quantization): three Polish models x six GGUF precisions, deterministic PolAgentBench: all three collapse between Q3_K_M and Q2_K (11B 0.716 to 0.045; 7B 0.463 to 0.149; PLLuM 0.224 to 0.015, paired McNemar p<0.001 each); failure modes do NOT replicate across models; a one-shot envelope-repair layer lifts the 7B from 0.448 to 0.567 at 8-bit because its dominant defect is mechanically repairable. Verdict: deployment law for the janitor fleet: never below 3-bit for agentic work; keep a repair layer; repair-as-diagnostic tells you which failure class your model has. Repo (CC0): https://github.com/JakubPrejzner/polagentbench
- Net answer: nothing untuned under 2B beats a gemma-class 2B janitor per published numbers; the wins at equal or smaller VRAM come from (a) narrow function-calling specialists (270M fine-tuned), (b) harness and server repairs, (c) staying at or above 3-bit quantization. Qwen2.5-1.5B is the only untuned sub-2B checkpoint above 70% in the 07370 corpus; qwen3:4b and granite4.2:3b are the cheapest agent-grade models in the 21341 corpus.

### Q2: licensing and deployment changes since the 97,865-row frontier-lab scrape

- The lens corpus.md file holding the 97,865-row scrape was NOT located in this session (find over maxdepth 3 found no lens corpus file; grep for 97,865/97865 in catalog/catalog.jsonl returns only coincidental id substrings like "e97865d2e9f8"). The 97,865 figure is carried here from the ask itself, not re-verified against the file.
- Hugging Face, "State of Open Models: Summer 2026 Observations" (2026-08-14, https://huggingface.co/blog/state-of-open-models-summer-2026), fetched and read: "Of 178 Chinese releases above 20B parameters this year, 59% carry Apache 2.0 and 22% carry MIT"; "Kimi K3 and Qwen 3.8 2.4T starting to include some non-commercial restrictions and revenue share requirements to their licenses"; "on the American side of the same size band, 29% is Apache or MIT, 41% sits under custom terms and 30% declares nothing at all"; "Whatever these releases are for, it is not licence revenue". Landscape: Kimi-K3 ~2.8T, Qwen 3.8 Max 2.4T, DeepSeek-V4-Flash ~284B in GGUF; sub-1B models take 83% of all-time downloads; Qwen has 151,448 hub derivatives, 2.6x Meta.
- A reader comment on that post claims Kimi models bar companies above $20M/year revenue from serving without Moonshot authorization. UNVERIFIED comment, not banked as fact; flagged as a reason to read the actual license text before any pull of Kimi-family weights.
- 2609.05881 (Broken on Arrival): 327 quantized GGUF artifacts executed (305 official Ollama library at or under 8 GB across 15 lines, plus 22 community HuggingFace): five silently defective official artifacts (four Qwen2.5-Coder-3B conversions, one phi3.5-mini) solve zero of 164 tasks while independent conversions of the same models work, 1.6% of official artifacts. Two community conversions fail on CUDA yet pass on Metal (backend-dependent). Surface statistics cannot catch two of the defect classes. quantcheck acceptance-testing tool released: https://github.com/aditi-p31/quantcheck
- Actionable law for the estate: license text must be read per release, not per family (terms are tightening at the top of the market), and every GGUF pulled into the janitor fleet should pass a quantcheck-style acceptance gate before catalog trust. Both fit the existing catalog acquisition flow.

### Q3: is there a free or open-weights verification rung, or does sensing-only match consensus?

- 2609.33467 (A Cheap Verifier is Good Enough): 11k H100 GPU-hours; Qwen3 trainees 1.7B-8B; golden verifiers Claude Opus 4.6, Gemini 3.1 Pro, GPT-5.5; 52 verifiers screened. "Expensive verifiers need not outperform inexpensive ones, and open-weight Gemma verifiers produce strong training outcomes." The fixed open-weight pick (Gemma 4 26B) captures 95% of available training uplift at a 98.8% grading-cost reduction vs the golden protocol; self-hosted, it grades a HealthBench rollout in ~0.51 H100-seconds. BUT: weak verifiers harm (Qwen3 1.7B trained with LFM2 24B fell below the no-training baseline), higher agreement does not consistently rank verifiers, and one self-judge case collapsed despite F1 ~0.76.
- 2608.30005 (SLM judges): Qwen3-1.7B with a trained linear probe head (frozen backbone, labels from GPT-4o) reaches 0.835 criterion macro-F1, beats its own 8B generative judge baseline as a GRPO reward (policy 0.643 vs 0.594) at 10.7x less judge time; 0.805 macro-F1 with only 100 training questions; holds 0.741 under generator shift. Probe readout beats generative and logprob readouts at every size.
- Consensus read against the driving-ladder law (memory/rib/RIB_DRIVING_LADDER_20260928.md:14-23): the literature does NOT say open-weights cannot verify; it says cheap verifiers verify well WHEN (a) they are calibrated against a stronger reference (probe heads trained on funded-tier labels), (b) the task is criterion-level and decomposable, and (c) weak or unsupervised rungs are excluded because they actively harm. That is the same shape as the estate's law: sensing feeds judgment, judgment verifies (rib line 21-23). Sensing-only for FREE stealth LANES stands; open-WEIGHTS run locally are not free stealth lanes, they are a different surface, and the evidence supports using Gemma/Qwen-class open weights as calibrated grader rungs under funded-tier supervision, never as final adjudicators. The JEV-as-a-judge accept-when-confident, escalate-when-unsure pattern (2609.26550, abstract read) is the published grammar for the escalation edge.

### Q4: smallest viable local model for structured JSON tool calls, and a benchmark the estate can run

- 2609.23742: constrained decoding (Outlines, XGrammar) lifts schema validity from 78.6-92.9% to 100% across five 0.6B-4B models on 14 structured-output tasks; XGrammar overhead is 4-8 ms compile and 1.6-3.7% throughput, Outlines 2.0-4.9 s compile and 9-13% throughput. Constrained Llama-3.2-1B (0.986 content accuracy under XGrammar) beats unconstrained Llama-3.2-3B (0.777), but constrained-3B still beats constrained-1B (0.991), and instruction-semantic failures (multi-step function calling) stay CD-resistant. Practitioner line: "The cheapest reliable configuration for structured output is XGrammar with a 3-4B model."
- 2609.25373: at 270M the only viable shape is a narrow fine-tuned specialist on a fixed schema catalog (100% function-name accuracy after SFT; execution-aware 100%).
- Locally runnable instruments for the janitor re-rank, all released by the deep-reads: (1) SLM-ToolCall-100 notebook + CSVs, 100 prompts, 5 tools, recovered-vs-strict scoring, https://github.com/Abrar051/sml_mcp_benchmark ; (2) PolAgentBench, deterministic 67-task suite + 46-rung arithmetic ladder, CC0, commit-stamped, https://github.com/JakubPrejzner/polagentbench ; (3) the 21341 protocol: cells of five consecutive passes scored in one sitting, refused-call argument capture, serving-context cap, swap watching, dataset + scorer + figure-verifier at doi 10.57967/hf/10485 ; (4) quantcheck for artifact acceptance before any of the above. The 21341 confound section (12B model holding 51 GB at 262,144-token context on a 64 GB box; capped at 32,768 the same 3B cell went 0/5 to 5/5) is a direct warning for any local Ollama re-rank the estate runs: cap context and read the serving engine's context column, or the numbers lie.

## Banked items (strongest first, 8)

1. 2609.21341 What Stops a Small Language Model From Driving a Database Agent (2026-09-18, CC BY 4.0)
2. 2609.07370 Beyond Fluent Generation: CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B SLMs (2026-09-07, CC BY 4.0)
3. 2609.23742 Constrained Decoding Eliminates Structural Failures in Small LLMs but Reveals a Scale-Dependent Semantic Gap (2026-09-20, CC BY 4.0; estate holds a 1,191-byte abstract snapshot, catalog id 3507e8533740)
4. 2609.25373 Extending FunctionGemma for Practical On-Device Mobile Function Calling (2026-09-21)
5. 2609.32042 Quantization Thresholds Replicate, Failure Modes Do Not (2026-09-25, CC Zero)
6. 2609.33467 A Cheap Verifier is Good Enough: LLM Post-training is Robust to Erroneous Rewards (2026-09-27, CC BY-SA 4.0)
7. 2609.05881 Broken on Arrival: Silently Defective LLM Artifacts in Public Model Registries (2026-09-05)
8. Hugging Face State of Open Models: Summer 2026 Observations (2026-08-14, fetched; the Q2 licensing evidence)

2608.30005 (SLM judges) read and banked in prose above; displaced from the top-8 list by the Q2 licensing evidence, not by weakness.

## Overlap census (commands actually run)

- grep -c -i "<phrase>" catalog/catalog.jsonl over 15 phrases: all 0 except "Constrained Decoding Eliminates" = 1.
- The 1 hit: catalog row id 3507e8533740, path local_sovereign_agent/state/arxiv/2026-09-22/2609.23742v1.txt, 1,191 bytes, mtime 2026-09-22. That is an abstract-scale snapshot another lane already pulled; the full-text findings (XGrammar overheads, 3-4B practitioner line, hollow-rescue phenomenon) are new to the estate.
- grep -c "<id>" catalog/catalog.jsonl for the other 7 arXiv ids: 0 rows each.
- grep -ril over memory/: every phrase matches only memory/trajectory/steps.jsonl, which is THIS session's own journal (self-referential, not estate holdings). No genuine memory/ overlap.
- OWED: the lens corpus.md file (97,865-row scrape) not located in this session; the figure rides from the ask.

## OWED / not verified

- Kimi K3 and Qwen 3.8 license TEXTS not read from primary sources; only the HF blog summary plus one unverified reader comment. Before any Kimi/Qwen-top-end pull, read the license file itself.
- slash-digital.io article unverifiable (homepage mismatch), discarded.
- 2609.32042 appendices and 2608.30005 appendices not read line by line (tables only skimmed); all claims taken from narrative sections read.
- The two arXiv listing pages fetched but not mined; the API queries served pass 1.
- The 07370 benchmark covers simulated single-call chores, not full MCP protocol (its own stated limitation, read in section 1 and 6); do not bank it as an MCP-protocol benchmark.

## Receipts

Raw receipts: watch/inbox/frontier_olm_20260928/sweep/_raw/ (8 query XMLs, 8 abs HTML, 8 full-text HTML + txt, list_csCL.html, list_csLG.html, parse_arxiv.py, dump_shortlist.py, strip_html.py). All fetches curl with a declared UA, serialized with 4s sleeps after the initial 429s. Parsed with .venv/Scripts/python.exe (no bare python). Bank file written 2026-09-28.
