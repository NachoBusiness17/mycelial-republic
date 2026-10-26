# Sweep: quantization-compression via x - 2026-10-05

Area: quantization-compression via x. All items below were fetched and read by this seat during
this ask; every note opens with the stamp source-fetched: 2026-10-05. Quotes are verbatim from
the fetched pages.

## Door status (honest)

- The X door degraded this cycle: every `site:x.com` WebSearch came back rate-limited
  (MCP error -429 / code 1302) or returned zero x.com hits (X is largely unindexed).
  One late retry surfaced a single x.com result ("Tool calling is where quantization breaks
  first. Makes sense: tool use requires precise JSON generation and structured reasoning.")
  but the link was a bare `https://x.com` with no user/status ID, so the fxtwitter door
  (https://api.fxtwitter.com/<user>/status/<id>) could not be invoked. Per recipe fallback the
  snippet is banked here with its URL and is NOT counted as a read item. Never resolved.
- unsloth.ai/blog/qwen3.5 (GGUF tool-calling chat-template fix) returned HTTP 403 to WebFetch;
  not read, not banked.
- Workaround door that DID work: the arXiv API
  (export.arxiv.org/api/query, quantization x tool-calling/agentic, sorted by submittedDate)
  returned 435 total hits, 30 most recent read as the candidate pool; a second query covered
  agent context compression (20 more). Candidate pool: 50+ from the last 30 days, plus the
  earlier search results. Pass 2 deep reads: 10 pages fetched end to end.

## Overlap sweep (what the estate already holds)

`grep -r -l -i` over catalog/catalog.jsonl, memory/, watch/inbox/ plus a per-file
`grep -o -E` attribution run found the three strongest-looking quantization papers ALREADY
banked: 2609.32042 (Quantization Thresholds Replicate; 10 hits in catalog.jsonl, plus the
2026-10-02/03/04 x-sweeps and today's HN sweep), 2609.04748 (Cache-Induced Divergence;
catalog.jsonl + 10-03 sweep), 2608.06564 (Low-Bit Quantization Breaks; 10-03 sweep).
Re-banking them is waste, so they are dropped from the item list even though this seat read
2609.32042 and 2609.04748 end to end this cycle. The eight items below all read zero hits on
their titles/IDs in the same grep and are genuinely new to the estate.

## Items (strongest first)

1. **Measuring the Microtask Eligibility Gap: When Is an Off-the-Shelf SLM Enough for an Agent
   Harness?** - arXiv:2610.00025 (Hu, Ramachandran; fetched page says submitted 2026-09-01).
   The estate's janitor-tier question asked straight: Qwen3 0.6B/1.7B/4B/8B on four harness
   microtasks (shell-command auto-approval, memory writes, tool selection, turn ranking),
   16 (task, size) configs, CI-gated thresholds anchored to a non-LLM baseline: 0/16 pass,
   replicated on Llama-3.x (12/12 ineligible) and across 112 prompt paraphrases. 4-bit
   RTN/GPTQ/AWQ "does damage that depends on model size and moves no configuration into
   eligibility" - "the gap tracks model size more than precision." One non-eligibility win:
   "a 4B re-ranker over a BM25 shortlist beats BM25 (+0.047 [0.020, 0.073])". Reads directly
   onto the gemma:2b scut / gemma4 worker tier: certify microtasks against a cheap baseline
   before promoting any local janitor, and do not expect the 4-bit quant to be the deciding
   factor either way.

2. **Agent Memory Distillation: Empowering Small LLM Agents with Hierarchical Teacher Memory**
   - arXiv:2608.07169 (Kim, Kim, Hwang; 2026-08-07). Training-free distillation of teacher
   trajectories into three memory strata - workflow / subtask / function - with proactive
   injection at task start and reactive retrieval on tool-call errors. Students 4B-8B; 4B
   gains most: AppWorld +27.2p, BFCL V3 +11.2p, ToolSandbox +3.4p; "Subtask memory contributes
   the largest gains." This is the closest public mechanism to the quantized_thought
   law-compilation practice: compiled rules from bigger-model runs handed to the small tier,
   measured. Suggests the estate's law packs are a BFCL-class lever for the 2B-4B workers.

3. **The Sleeping Agent: What Gist-Based Context Compression Loses and Why** -
   arXiv:2608.11775 (Kyrkewood; 2026-08-12). Sleep-inspired Salience-Weighted Consolidation as
   a diagnostic on 1,935 matched LoCoMo questions: gist compression beats truncation on
   factual/multi-hop but consistently fails temporal questions because "the gist abstraction
   prompt preserves relational and event structure while discarding dates and times." The
   one-sentence prompt fix lifts temporal-expression preservation "3.05% to 62.39%"
   (+0.314 judge accuracy, CI [0.254, 0.375]) without touching entity/event preservation.
   Direct recall-cost answer for RQ4: law/summary compilation must carry timestamps or it
   silently loses the when.

4. **Adapting Context Compression for Long-Horizon Agents with Counterfactual Continuations**
   - arXiv:2609.36526 (Min et al.; 2026-09-29). PAIR reruns the same agent state with vs
   without each compression event to find the harmful ones and patch the compression template.
   Key law-shaped finding: "compression degrades reliability before solvability" -
   cross-run consistency breaks before task success does, and damage "concentrates at isolated
   compression events". For the estate: when folding context, gate on run-to-run reliability,
   not on one-shot task completion.

5. **Mix-Quant: Quantized Prefilling, Precise Decoding for Agentic LLMs** - arXiv:2605.20315
   (Lu et al.; 2026-05-19). NVFP4 4-bit prefill + BF16 decode for long-context multi-turn
   agents: prefill "exhibits substantial quantization redundancy" so task performance is
   largely preserved with "up to a 3x speedup during prefilling", while quantizing the whole
   pipeline degrades. Practical shape for the estate's Ollama hosts: keep the decode path
   high-precision even when inputs are compressed.

6. **Small Reasoning Models are Instruction Followers in Function Calling (IFFC)** -
   arXiv:2608.22472 (Taheri et al.; 2026-08-23). Delegates function-calling logic to a small
   model in ordinary instruction-following mode instead of native tool-call syntax; beats NFC
   and prompt-based FC, and "maintains robust performance under aggressive quantization" for
   edge use. Counterpoint to the eligibility-gap paper and a candidate tool-call-shape law:
   if the janitor tier keeps breaking JSON tool syntax, move the syntax burden to plain
   instruction following.

7. **Ollama library shelf, live pull (RQ3)** - https://ollama.com/library, fetched 2026-10-05.
   Within the last 30 days the library carries: qwen3.5 updated "18 hours ago" with sizes
   "0.8b, 2b, 4b, 9b, 27b, 35b, 122b"; gemma4 5 days ago with "e2b, e4b, 12b, 26b, 31b"
   ("designed to deliver frontier-level performance at each size", vision/tools/thinking/
   audio); qwen3.6 (27b, 35b) 4 days ago; tev1 (0.8b, 4b); clef-flash 9b; qwen3.8-flash-next;
   deepseek-v4.1-flash 3 weeks. The listing exposes parameter variants and tag counts (qwen:
   379 tags), not per-quant labels, but Ollama serves GGUF only and default tags are Q4_K_M
   class; AWQ is a vLLM-format, not an Ollama format. The gemma4 e2b/e4b and qwen3.5 0.8b/2b
   entries are the concrete byte-budget candidates for the janitor model cards.

8. **tencent/Hunyuan-1.8B-Instruct-AWQ-Int4 model card (RQ1/RQ3)** -
   https://huggingface.co/tencent/Hunyuan-1.8B-Instruct-AWQ-Int4 (repo 2025-07-31, modified
   2025-09-02; outside the 30-day window, kept as shelf evidence). 1.8B AWQ Int4 (W4A16) via
   AngelSlim, ~1.3 GB file; AWQ "computes a scaling coefficient s to expand the numerical
   range of important weights". Scale context for the janitor tier: BFCL v3 by size is 49.8
   (0.5B) / 58.3 (1.8B) / 67.9 (4B) / 70.8 (7B), tau-Bench 14.4 / 18.2 / 30.1 / 35.3. Honest
   gap: the card's quant benchmark covers DROP/GPQA/OlympiadBench/AIME only - no tool-call
   numbers for the AWQ build itself, which matches the estate's rule that quantized variants
   need their own tool-call battery before promotion.

## Answers to the four research questions (sourced above)

- **Q1 (quality-vs-bits on 2B-8B, tool-calling/repo-editing):** the measurement frontier has
  moved from aggregate benchmark deltas to decision-level margins (2608.06564, held) and
  per-microtask CI-gated eligibility (2610.00025); scale-referenced tool-call numbers for the
  1.8B class sit at BFCL v3 58.3 / tau-Bench 18.2 (Hunyuan card). No fetched paper reports a
  4-bit vs 8-bit repo-editing (SWE-bench-class) table for 2B-8B models; that cell stays
  unmeasured in the public corpus this cycle.
- **Q2 (does sub-8-bit break tool-call syntax/JSON):** yes below 4 bits and it is decision-
  selective: whether-to-call-a-tool collapses toward inaction at 3 bits while which-tool
  selection survives (2608.06564, held); GGUF cliff sits between 3-bit and 2-bit (2609.32042,
  held); 4-bit serving plus prefix caching diverges tool trajectories on 75% of episodes
  (2609.04748, held); and the mitigations are architectural - IFFC-style instruction-following
  delegation holds under aggressive quantization (2608.22472).
- **Q3 (runnable quantized variants today):** Ollama = GGUF only, default Q4_K_M-class tags;
  qwen3.5 0.8b/2b/4b, gemma4 e2b/e4b are live pulls as of 2026-10-05 (item 7); AWQ stays a
  vLLM-side format (Hunyuan card as the worked example). The estate's tool-call shape laws
  should be re-run per quant tag, not per family: failure modes do not transfer across
  precisions (2609.32042's core claim, held).
- **Q4 (compression for long-lived agent context vs quantized_thought):** distill compiled
  memories, not raw summaries - hierarchical teacher memory is training-free and nets +11-27
  points on the small tier (2608.07169); carry timestamps in every compiled law (2608.11775);
  gate folds on reliability-before-solvability (2609.36526); and keep decode precision high
  even when context is compressed (2605.20315). Measured recall costs: temporal preservation
  3.05% to 62.39% under gist compression without the fix; hidden reacquisition cost (retrieval
  calls 21.0 to 63.9, arXiv:2608.16370, seen in feed listing only, not deep-read).

## Method receipt

Commands/shapes run this ask: WebSearch (8 queries, most rate-limited 1302; results attributed
above), WebFetch on 11 URLs (10 read to completion; unsloth.ai 403; one arXiv abs fetch timed
out once and succeeded on retry), arXiv API two queries (30 + 20 entries read from feed),
`grep -r -l -i` wide overlap pass (137 files matched the union pattern, dominated by the
estate's own quantized_thought law files) followed by per-file `grep -o -E` attribution over
catalog/catalog.jsonl + the five prior quantization-compression sweeps + memory/corpus/LINKS.jsonl.
