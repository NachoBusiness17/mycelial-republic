# Frontier sweep: kv-cache-context-engineering via arXiv

source-fetched: adhoc · swept 2026-10-10 · seat: sweep-kv-cache-context-engineering-arxiv

## Door status

- `export.arxiv.org/api/query` returned HTTP 429 when hit with parallel queries at open; the door
  recovered when driven serially and delivered 90 entries across 4 queries (prefix cache, context
  management + agent, token-aware/token efficiency, Model Context Protocol).
- WebSearch `site:arxiv.org` fallback used per recipe while the API cooled; it surfaced the
  June/Oct items (TokenPilot, ReFold) before the API did.
- Full-text reads went through the web-reader lane (arxiv.org/html); `2609.38706v1` threw one
  MCP -500 on first attempt and served fine on retry. No fabrication: every quote below was
  copied from a page this seat fetched.

## Pass 1 census

~90 API entries + ~12 search candidates inspected; well over 30 within the last 30 days
(2026-09-10 to 2026-10-10). Already-held work excluded after catalog grep (see Overlap):
ReFold (2610.07863), ContextRender (2609.37743), StateComp (2609.27298), CoBPE /
"More Than Words" (2610.05597), Continuous Context Management (2609.35540) - the estate
already holds these five; banking them again would be waste.

## Overlap method (run this sitting)

- grep of `catalog/catalog.jsonl` for exact candidate titles (`grep -o -i -E` over the "title"
  fields, patterns: RR-Evict, ReFold:, ContextRender, TokenPilot, StateComp, Fancy Eviction,
  CADOC, Tessera, Memory Canonicalization, Compositional Tokenization, CoBPE, Preserving
  Provenance, Agent-Controlled Forgetting, Continuous Context Management, Cache-History,
  Request Order Matters, Hierarchical Structure and Functional Landscape) returned hits only
  for ReFold, ContextRender, StateComp, CoBPE, Continuous Context Management (all excluded
  from this bank) plus `mag_tesseract.ico` filename noise.
- Recursive grep of `memory/` for the 8 banked titles and arXiv IDs returned only
  `mag_tesseract.ico` path-string false positives inside `memory/agent_sessions/orc-*.json`
  transcripts; no genuine hits.
- Conclusion: all 8 items below are genuinely new to the estate.

## Banked items (strongest first)

### 1. RR-Evict: Fine-Grained Prefix Cache Eviction beyond LRU for Agentic LLM Serving
arXiv 2609.32278 (v1 2026-09-26, v2 2026-10-02) · Pan, Wu, Hu, Qiang, Yu, Ding (UCSD) · READ END TO END

Names the recency synchronization failure: an agent's accesses refresh its cached blocks
together, so LRU eviction concentrates on a few agents' private histories and a returning,
fully-evicted agent recomputes nearly its whole context (TTFT outlier). Fix: visit agents
round-robin and evict a small tail chunk from each idle trajectory, so more agents keep
reusable prefixes; needs no arrival or tool-latency prediction. Implemented in SGLang;
conversational + SWE-bench coding agents, colocated and PD-disaggregated.
Measured: "Compared with LRU, RR-Evict reduces P99 TTFT by up to 75.4% and P99 uncached
prompt tokens by up to 65.7%." Coding-agent PD case: P99 TTFT -60.7%, uncached tokens -60.8%.
Honest limitation: short idle intervals only, HBM not tiered storage; recency-tiering
unevaluated. Estate fit: the Hermes relay and any local janitor restart loop re-prefills whole
histories exactly this way; round-robin tail eviction is the cheap policy upgrade.

### 2. When Fancy Eviction Fails: Rethinking Cache Replacement For LLM Prefix Reuse
arXiv 2609.28870 (v1 2026-09-24, v2 2026-10-01) · Liu, Yu, Yang (Harvard) · READ END TO END

The measured eviction-policy verdict the burns.md re-audit wants: 20B+ processed tokens from
two production traces (327.5K requests / 10.5B tokens / 7 days, heavily agentic; 515.8K
requests / 9.7B tokens / 130.9 days), 14 eviction algorithms, HBM-constrained and memory-pool
settings. Finding: "Prefix reuse is dominated by the regular pacing of active sessions, making
recency unusually predictive" - LRU is a robust baseline; frequency-aware policies collapse;
even Belady leaves real headroom, so better eviction is still on the table. Median
intra-session interval 8.2s; 99.7% of gaps under 22 min. Multi-turn history = 37.6% of blocks
but 70.2% of accesses; system prompts 4.4% of blocks / 18.4% of accesses; top 10% of sessions
hoard 76.2% of KV bytes. Practical: partial-node RandomCompute eviction cuts avg TTFT 19.9%
and lifts prefill throughput 18.8% on a real vLLM H200. Design principles: recency baseline +
quick demotion for one-hit floods + compute-aware partial eviction + capacity-adaptive
granularity (session vs block). Note the productive tension with RR-Evict: both reject
frequency/learning-based policies; RR-Evict redistributes across agents, this paper keeps LRU
and changes granularity.

### 3. Preserving Provenance in Shared KV Caches for LLM Serving
arXiv 2609.38706 (2026-09-30) · Song, Cao, Zheng, Zhang, Cheng (Griffith/NUS/Macquarie) · READ END TO END

The direct answer to burns.md:171-172's provenance re-audit: names provenance-blind reuse -
shared KV tiers keyed by token content alone let semantically different contexts collide.
"Cross-adapter collisions reduce accuracy from 0.94 to 0.64, incompatible KV representations
reduce reasoning accuracy to zero, and salt omission enables 93% prompt identification from
timing." Fix: bind per-request + per-worker provenance into lookup AND store keys via a
canonical descriptor + differential checker; hit-path overhead within 0.34 ms, under run-to-run
variation, legitimate cross-worker sharing preserved. Estate fit: any future shared KV tier
for the janitor fleet must key on provenance, not content hash alone; the 93% timing
identification is also a privacy argument for per-tenant salts.

### 4. Request Order Matters: Cache-History Sensitivity in Selective KV-Cache Reuse for Rolling Agents
arXiv 2610.05833 (2026-10-05) · Gu, Guan, Huang, Rao, Shah, Capetz (Capital One) · READ END TO END

Rolling agents (retain most docs, evict old, append new) break exact prefix caching; selective
KV reuse with partial recomputation is the standard fix - and it is history-dependent: an
unchanged prompt can answer differently depending on which requests preceded it. Measured on
Qwen3-8B / LMCache 0.5.1 / vLLM 0.23.0, 7,735 rolling updates, 84-doc ~7.5K-token prompts:
at a matched 5% recomputation budget, document-aligned recomputation cuts answer variation
across request orders from 69.0% (CacheBlend token top-k) to 26.1%, lifts fidelity to full
prefill by 34.5-52.5 pp, both policies ~5.7x median TTFT speedup. Ablation: "contiguity is
the main factor associated with robust selective recomputation" - single-window doc-aligned
best (92.8% fidelity). Cache-reset control shows clean-cache evaluation hides this entirely.
Estate fit: evaluation law for any cache-reuse experiment the estate runs - never measure from
a cold cache; and prefer document/window-aligned recomputation over token top-k.

### 5. Agent-Controlled Forgetting for Tool-Using Agents: Reversible Context Curation in Practice
arXiv 2610.10590 (2026-10-06) · Franke (Muenster) · READ END TO END

The compaction-boundary experiment for R4: replace old tool results with agent-written notes,
keep an archive for reversible recovery (context_apply/context_recover with atomic batch
validation; user/system/assistant messages never touched). Central case (running on the same
GLM family the estate drives, z-ai/glm-5.3-flash via TensorX): "the method ended with 231,951
provider-reported prompt tokens versus 912,492 under retained history" - 50% fewer cumulative
input tokens, USD 1.28-1.44 vs USD 4.38 - but 185 vs 121 requests and 17% longer wall time.
Second workload (planroom): no savings, 6% MORE prompt tokens (notes overhead exceeds
discarded results). Adverse browser-continuation result: 63% fewer tokens but quality 4/12 vs
6/12. Honest single-author exploratory study; explicitly flags Anthropic's context-editing
(threshold tool-result clearing with placeholders + cache invalidation) as the unevaluated
baseline. Verdict for the estate: workload dependence is the law - forgetting pays only where
tool results are large and rarely revisited; archive-with-recover beats blind summarize.

### 6. CADOC: Cache-Aware Dynamic Object Context for Long-Horizon Agents
arXiv 2609.37012 (2026-09-29) · Yao, Zhou, Xu (SJTU) · abstract-level read

Bridges R3 and R1: replaces structured objects with compact Cards (replacing = full object
rewrite, cheaper than diff-style edits) and - the distinctive move - schedules the edits to
preserve prefix-cache reuse, since naive history editing breaks caching. Abstract claims
"reduces input cost by approximately 40% on average while maintaining task performance close
to full context." Estate fit: direct input for the skills_pack.py 287-node hub redesign -
case-law nodes as Cards with cache-aware edit scheduling.

### 7. The KV Cache Working Set: Online Capacity Planning for LLM Inference Systems
arXiv 2609.27746 (2026-09-23) · Li, Wang, Ruan, Li, Gong (Tongji + Ant Group) · abstract-level read

Defines the working set as "the minimum cache capacity required to achieve a target hit rate"
and computes it online with KVSET (Mattson-stack-based); validated on three production traces,
estimates closely matching measurements; explicitly motivated by agentic workloads. Estate
fit: answers how much KV RAM/SSD the janitor fleet needs for a 90% hit-rate target before
buying hardware, not after.

### 8. Understanding the Hierarchical Structure and Functional Landscape of the MCP Ecosystem
arXiv 2610.05319 (v1 2026-10-04, v2 2026-10-08) · Tang, Chen, Xiao (Tsinghua) · abstract-level read

MCPacific: "collects 368,754 MCP server listings corresponding to 124,267 unique servers" and
"statically extracts 1,328,233 tool specifications from these servers in seven languages";
98.5% of tools have at least one alternative, yet about a quarter of capabilities are
single-tool. Estate fit for mcp_tokenization_law_20261010: the corpus + redundancy map for
choosing token-cheap tool schemas; where 98.5% overlap exists, schema token budgets can be
negotiated downward by substitution.

## Honest gap on R2

No paper in this 30-day window directly measures tokenization-aware context budgeting for
JSON-heavy MCP traffic (the mcp_tokenization_law card's exact ask). The closest work is
already in our catalog (CoBPE, 2610.05597). MCPacific gives the ecosystem substrate; the Feb
2026 "MCP Tool Descriptions" line (surfaced by search, not fetched this sitting - OWED, not
asserted) is the next lead to verify.

## Estate feeds

- mag/skills_pack.py (287-degree hub): CADOC Cards + RR-Evict-style edit scheduling.
- mag/context_compression.py + compaction lane: Agent-Controlled Forgetting's archive-recover
  boundary and its planroom counterexample; StateComp/CCM already held.
- burns.md:171-172 provenance re-audit: item 3 is the citation; content-hash-only KV keys are
  the anti-pattern, 0.94-to-0.64 and zero-accuracy collisions the measured stakes.
- Evaluation law for any future cache experiments: item 4's cold-cache control.
