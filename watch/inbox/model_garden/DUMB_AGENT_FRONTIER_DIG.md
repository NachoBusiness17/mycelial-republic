# DUMB_AGENT_FRONTIER_DIG - tool-augmented small models vs the bare frontier, external evidence 2025-2026

**Lane:** DIG-1 (EXTERNAL RESEARCH) · **Date:** 2026-10-01 · **Method:** web sweep, every claim
citation-backed, primary sources preferred over roundups; roundups used only where they surface
primary numbers and are marked as such.
**Operator thesis under test:** "the MCP server gives dumb agents frontier capabilities."
**Honest framing of what was testable:** the external literature tests two separable claims:
(a) tools/scaffolds move capability more than model scale (the scaffold lever), and
(b) SMALL (1-9B, or small-active-param MoE) models plus tools reach or beat large bare models.
Claim (a) is strongly supported. Claim (b) is supported in narrow regimes (function calling,
GUI grounding, grounded retrieval) and NOT supported for raw multi-tool orchestration and
long-horizon reliability, where small models still trail hard. MCP-specific measured deltas are
thin: the ecosystem is large, the rigorous small-model-with-MCP measurements are few.

## Verdict table

| # | Source (cite) | Sweep | One-line finding | Verdict | Condition |
|---|---|---|---|---|---|
| S1 | [arXiv 2601.11327, Univ. Amsterdam, 2026-01-16](https://arxiv.org/html/2601.11327v1) | 1 | On GAIA (165 val Qs), Qwen3-4B-Instruct WITH tools scores 18.18% vs Qwen3-32B WITHOUT tools at 12.73%; agentic configs beat no-tool configs at every scale | SUPPORTS | same-family controlled comparison; absolute scores low (best overall: 32B agentic 25.45%); planner-only thinking helps smalls, full thinking destabilizes tool orchestration |
| S2 | [Particula Tech blog, 2026-03-25](https://particula.tech/blog/agent-scaffolding-beats-model-upgrades-swe-bench) | 1 | Six frontier models sit within ~1 pt on SWE-bench Verified while the same model (Opus 4.5) swings 45.9% to 55.4% on SWE-bench Pro purely by scaffold (SEAL vs Claude Code); Sonnet 4.5 on a custom scaffold (52.7%) beat Opus 4.5 on Anthropic's own scaffold (52.0%); "22+ pt scaffold swing vs ~1 pt model swap" | SUPPORTS | the 42-78% swing is secondhand (Nate B. Jones, no model named); this is the frontier-parity regime, not small-vs-frontier |
| S3 | [mini-swe-agent (OpenReview)](https://openreview.net/revisions?id=9NwKJw0H4e) + [launch thread](https://www.reddit.com/r/Anthropic/comments/1m8zgfk/100_lines_of_python_is_all_you_need_a_radically) | 1 | A ~100-line scaffold resolves 65% (later 70.6%) of SWE-bench Verified, competitive with heavyweight proprietary harnesses | SUPPORTS | the model under it is a cheap mid-tier API model, not a 1-9B local; evidence for the HARNESS lever, not the small-model lever |
| S4 | [SAIL, EMNLP Findings 2023](https://aclanthology.org/2023.findings-emnlp.242.pdf) | 1 | Search-augmented SAIL-7B reached 103% of GPT-3.5-Turbo performance (the lineage result for "small + search beats bigger bare") | SUPPORTS | 2023, GPT-3.5-era target, not today's frontier |
| S5 | [Arch-Agent 7B claims (r/OpenAI)](https://www.reddit.com/r/OpenAI/comments/1li3o2v/archagent_blazing_fast_7b_llm_that_outperforms) + [TraceBench](https://openreview.net/pdf?id=ZPkI4eVlm5) | 1/4 | A 7B function-calling finetune self-reports beating GPT-4.1 / o3-mini / DeepSeek-v3 on multi-step agentic workflows; the only independent read found (TraceBench) scores it ~0.39 | MIXED | self-reported wins vs weak independent evidence; no standalone paper located |
| S6 | [SealQA, arXiv 2506.01062, ICLR 2026](https://arxiv.org/html/2506.01062v2) | 1/3 | On noisy search results (Seal-0), tool-equipped frontier models collapse (o3 17.1%, o4-mini 6.3%); GPT-4.1 48.0%, o3-mini 56.7%, no open model above 50% | MIXED | tools do not fix reasoning under conflicting evidence; hurts the thesis's universality, and hits EVERY size |
| S7 | [MCP-Bench, Accenture, arXiv 2508.20453, NeurIPS 2025 workshop](https://github.com/Accenture/mcp-bench) | 2 | 20 models over 28 real MCP servers: gpt-5 0.749, o3 0.715, gpt-oss-120b 0.692 (open, ~5B active params, 0.057 behind gpt-5), gpt-oss-20b 0.654, llama-3.1-8b 0.428 | MIXED | the best evidence BOTH ways: small-active-param open models ride MCP near frontier; true 8B smalls sit 0.32 behind on raw MCP tool use |
| S8 | [MCP-Atlas, arXiv 2602.00933](https://arxiv.org/abs/2602.00933) + [Scale leaderboard](https://labs.scale.com/leaderboard/mcp_atlas) + [open-weight roundup](https://agyn.io/blog/top-open-weight-llms-2026) | 2 | 36 production MCP servers, 220 tools, 1000 tasks; leading open-weight model reported at 76.0 on MCP Atlas (81.1 MCP Mark Verified) vs closed leaders ~85+, at ~80% lower cost than Claude Opus | MIXED | open-weight narrows but does not close the MCP gap; snapshot scores vary by source and date, verify on the live Scale board |
| S9 | [RAG-MCP, arXiv 2505.03275, 2025-05-06](https://arxiv.org/abs/2505.03275) + [Writer engineering note](https://writer.com/engineering/rag-mcp) | 2 | Tool-selection accuracy exceeds 90% under ~30 candidate tools but collapses to 13.62% baseline at large MCP pools; retrieving tools per query triples it to 43.13% and cuts prompt tokens >50% | MIXED | the fix works and is still under 50%: "many MCP servers + one dumb agent" fails without tool retrieval; model identities not stated on the abstract page |
| S10 | [MCP Tool Descriptions Are Smelly, arXiv 2602.14878](https://arxiv.org/html/2602.14878v1) | 2 | Audit of 103 MCP servers (856 tools): many tool descriptions are poorly written, compounding selection errors | MIXED | cuts BOTH ways: server quality (not model IQ) carries capability, which supports the thesis mechanism, and bad servers drag even frontier models down |
| S11 | [Zuplo State of MCP survey, Dec 2025 (via Firecrawl)](https://www.firecrawl.dev/blog/best-mcp-servers-for-developers) | 2 | 72% of MCP users expect usage to increase; 70% already run 2+ servers | CONTEXT | adoption fact, no capability delta; listed for ecosystem scale only |
| S12 | [r/mcp local-LLM thread](https://www.reddit.com/r/mcp/comments/1kbj267/local_small_llm_which_can_still_use_mcp_servers) + [Ollama tools-capable list](https://ollama.com/search?c=tools) + [local agent model ranking](https://localaimaster.com/blog/best-ollama-models-for-agents) | 2 | Practitioner consensus 2025: small tool-calling models (Qwen3-8B most cited, Cogito, Llama 3.x) drive MCP servers reliably through bridge layers; Qwen3 8B (Apache 2.0) ranked top small agent | SUPPORTS | qualitative, self-reported reliability, no controlled deltas |
| S13 | [arXiv 2603.17872, 2026-03-18](https://arxiv.org/html/2603.17872v1) | 3 | Llama-3.1-8B + tiered retrieval/verification pipeline (LangGraph, CRAG grading, claim-level verification, refusal circuit breaker): groundedness 78.8-86.4%, hallucination down to 13.6-15.5% on factual sets (TimeQA 83.7% win rate, TruthfulQA 84.9% grounded) | SUPPORTS | the win is the VERIFICATION LOOP, not bare tools; hallucination still hits 33.1% on MMLU Global Facts; judge was Gemma3-27B |
| S14 | [CloudWalk, 2025-09-22](https://www.cloudwalk.io/ai/rag-tool-calling-and-the-fight-against-hallucinations) | 3 | Tool-calling generators are MORE prone to hallucination if not grounded; hybrid RAG + API pattern recommended; cites Tian et al. 2024 fine-tuning: 53% fewer factual errors (biographies), 50% (medical Q&A) at 7B | MIXED | tools alone do not reduce fabrication; grounding discipline does |
| S15 | [Mem0 grounded memory](https://mem0.ai/blog/reducing-hallucinations-llms-with-grounded-memory) | 3 | Vendor-reported 95%+ hallucination reduction with grounded memory | SUPPORTS | vendor claim, methodology not independently verifiable from the page |
| S16 | [Search Arena, ICLR 2026](https://proceedings.iclr.cc/paper_files/paper/2026/file/4476dd7320e0eba63961990d73525064-Paper-Conference.pdf) | 3 | Combining web search with LLMs measurably improves groundedness and freshness (preference-arena methodology) | SUPPORTS | arena preference, not accuracy audit |
| S17 | [BFCL V4, Gorilla team, ICML 2025](https://gorilla.cs.berkeley.edu/leaderboard.html) + [VentureBeat 2024-07](https://venturebeat.com/business/groq-open-source-llama-ai-model-tops-leaderboard-outperforming-gpt-4o-and-claude-in-function-calling) | 4 | Open-weight models have topped the Berkeley Function Calling Leaderboard over GPT-4o/Claude (Groq-served Llama 3.1 405B, 2024); the leaderboard now spans multi-turn and agentic calling | SUPPORTS | 405B is open but NOT small; the small-model version of this claim is S18 |
| S18 | [ToolACE, arXiv 2409.00920](https://arxiv.org/abs/2409.00920) + [HF card](https://huggingface.co/Team-ACE/ToolACE-8B) | 4 | ToolACE-8B (Llama-3.1-8B base) trained on synthetic function-calling data hit SOTA on BFCL v1 AST and Exec, rivaling GPT-4-class models; relevance detection 89 | SUPPORTS | BFCL v1 is saturating (see S19); single-call + relevance strength, not long-horizon agency |
| S19 | [Databricks, unpacking function-calling evals](https://www.databricks.com/blog/unpacking-function-calling-eval) | 4 | BFCL shows saturation: Llama3-70B-Instruct outperformed GPT-4o in nearly every category except relevance detection; self-reported results differ from independent runs | MIXED | eval-integrity caution on the very numbers that support the thesis |
| S20 | [UI-TARS, arXiv 2501.12326](https://arxiv.org/abs/2501.12326) + [GitHub](https://github.com/bytedance/ui-tars) + [VentureBeat](https://venturebeat.com/technology/bytedances-ui-tars-can-take-over-your-computer-outperforms-gpt-4o-and-claude) | 4 | ByteDance UI-TARS-72B outperformed Claude Computer Use on OSWorld (24.6 vs 22.0); UI-TARS-1.5-7B hit 49.6 on ScreenSpot-Pro and ~50 on OSWorld, beating GPT-4o-class on GUI grounding, runnable locally on consumer GPUs | SUPPORTS | domain-specific (GUI grounding); the family's own 72B still beats its 7B; OSWorld ~50 is parity with 2025-era frontier computer-use, not 2026-era |
| S21 | [Qwen3-Coder-30B-A3B, HF card (2025-07-31, Apache 2.0, 30.5B total / 3.3B active)](https://huggingface.co/Qwen/Qwen3-Coder-30B-A3B-Instruct) + [swebench.com](https://www.swebench.com) + [hands-on week test](https://medium.com/@pixipace/i-ran-qwen3-coder-locally-for-a-week-instead-of-paying-75-for-claude-heres-what-i-got-wrong-90371c1367ce) | 4/5 | A 3.3B-active MoE coder lands ~60.4% SWE-bench Verified (EntroPO + R2E scaffold), listed shoulder-to-shoulder with Claude 3.5 Sonnet (~60.2%); a scaffold study lifted its resolve rate 27.5% to 56.9%; ~11x cheaper per input token than Claude Opus; but a week-long hands-on test concluded it did NOT replace Claude Opus (~48% vs ~72% practical agentic gap) | MIXED | the single best "small-active-param + scaffold" existence proof AND the honest ceiling, both in one model |
| S22 | [Inference.net pricing comparison](https://inference.net/content/llm-api-pricing-comparison) + [Layer3Labs pricing chart](https://www.layer3labs.io/ai-model-pricing) | 5 | Same task ranges $0.04 to $25.00 per M tokens depending on model tier, a ~625x spread | SUPPORTS | price is not capability; the spread is the arbitrage the thesis exploits |
| S23 | [SWE-Edit, arXiv 2604.26102](https://arxiv.org/html/2604.26102v1) | 5 | Scaffold-level edit improvements raised resolve rate 2.1% while CUTTING inference cost 17.9% | SUPPORTS | small effect, clean sign: harness work buys capability and saves money simultaneously |
| S24 | [Sierra tau-bench + pass^k](https://sierra.ai/uk/blog/tau-bench-shaping-development-evaluation-agents) + [taubench.com](https://taubench.com) + [long-horizon eval gap](https://tianpan.co/blog/2026/04/10/long-horizon-evaluation-gap-agent-benchmarks) | caution | pass^k: agent success compounds DOWN over repeated runs; models with strong pass^1 collapse at higher k through per-turn tool-call and state-tracking errors; the long-horizon literature flags smaller models as hit hardest | MIXED | the small-model-hardest claim came via secondary summary, primary per-size pass^k tables not yet pulled; treat as the standing refuting pressure, not a landed refutation |
| S25 | [AI Thinker Lab](https://aithinkerlab.com/stop-paying-the-intelligence-tax-how-small-language-modelssmls-cut-ai-bills-by-90) + [AI MagicX](https://www.aimagicx.com/blog/ai-pricing-war-llm-cost-collapse-business-strategy-2026) | 5 | Fine-tuned smalls claimed to match frontier on SPECIFIC tasks at ~90-95% lower cost; fine-tuning capex $50k-200k per run | MIXED | vendor/blog tier sources, capex excluded from the headline savings |
| S26 | [Towards Data Science, choosing small vs frontier](https://towardsdatascience.com/how-to-choose-between-small-and-frontier-models) | 5 | Frontier-quality API prices fell ~80% from early 2025 to early 2026 | MIXED | the economic moat of small+tools shrinks as frontier prices collapse; the argument must ride capability-per-dollar at the routing layer, not headline price |

Tally: **26 sources. SUPPORTS 13 · MIXED 12 · REFUTES 0 · CONTEXT 1.**
Zero outright refutations found, but S7, S9, and S24 together form real refuting PRESSURE
(see honest state below). No source was found that shows a 1-9B model with tools matching a
2026 frontier model on an unconstrained long-horizon agentic benchmark.

## Per-sweep honest state

### Sweep 1: small+tools vs large-bare benchmarks
The controlled same-family evidence is the strongest in the corpus: S1 (Amsterdam, Jan 2026)
runs Qwen3 4B through 32B with and without tools on GAIA and finds tool augmentation the most
reliable gain at every scale, with 4B+tools beating 32B-bare. The scaffold-lever evidence (S2,
S3) is stronger still but mostly at the frontier or mid-tier: scaffolds move 5-22 points,
model swaps at the frontier move ~1. The small-model-specific claims (S5 Arch-Agent) are
self-reported with weak independent confirmation. Condition for the whole sweep: "beats the
frontier bare" is demonstrated against same-family or last-generation frontier (GPT-3.5,
GPT-4.1, Claude 3.5 Sonnet, o3-mini), never against the current top rung bare.

### Sweep 2: MCP specifically
MCP-specific MEASURED small-model deltas are thin, this is the weakest evidence zone. What
exists: MCP-Bench (S7) shows small-active-param open models (gpt-oss-120b, ~5B active) riding
MCP to within 0.057 of gpt-5, while true 8B sits at 0.428; MCP-Atlas (S8) shows open-weight
within ~10 points of closed leaders at ~80% lower cost; RAG-MCP (S9) shows the failure mode
(prompt bloat: 13.62% selection accuracy at large tool pools, tripled to 43.13% by retrieving
tools instead of loading them). Practitioner evidence (S12) confirms the capability floor
exists (Qwen3-8B class drives MCP servers) but without controlled deltas. Verdict: MCP elevates
mid-small open models toward frontier on tool-use tasks; it does NOT carry 8B-class models to
frontier MCP competence, and server-side description quality (S10) is itself a capability
carrier.

### Sweep 3: the fabrication fix
The external pattern matches the estate's "senses not oracles": grounding plus verification,
not tool access alone. S13 is the cleanest instrumented result (8B + tiered retrieval +
claim-level verification + refusal breaker: groundedness 78.8-86.4%), S14 states the inverse
(ungrounded tool-callers hallucinate more), S16 shows search improves groundedness at arena
scale. Condition everywhere: the hallucination floor only drops when the loop can REFUSE or
re-verify; on adversarial or noisy evidence (S6 SealQA) every size class degrades.

### Sweep 4: function calling / computer use for small models
The most mature supporting zone. Function calling is functionally solved at 8B for the
single-and-multi-turn calling shape: ToolACE-8B (S18) SOTA'd BFCL v1 over GPT-4-class in 2024,
and open models have repeatedly topped BFCL over closed ones (S17). GUI/computer use has a
clean small-model win (S20: UI-TARS-1.5-7B beats GPT-4o-class on ScreenSpot-Pro and reaches
~50 OSWorld locally). The honest ceiling is S21: the best small-active-param agentic coder
(Qwen3-Coder-30B-A3B, 3.3B active) is Claude-3.5-Sonnet-class on SWE-bench Verified, an
era behind, and its scaffold lifts (27.5% to 56.9%) show the scaffold lever again. BFCL
saturation (S19) means "beats GPT-4o on BFCL" is a weaker claim than it sounds.

### Sweep 5: economics
The arbitrage is real and large (S22: up to 625x per-token spread; S21: ~11x cheaper than
Opus at Sonnet-era capability; S23: scaffold work that SAVES money while adding capability).
Two cautions: the fine-tune-to-frontier cost claims (S25) are vendor-tier and exclude capex;
and frontier prices fell ~80% in the same window (S26), so the economic case must be made at
the routing layer (route cheap, escalate rare) rather than on headline price.

## The honest state of the evidence

1. **Supported core:** tools and scaffolds are now a bigger capability lever than model-scale
   at the margin, and small/small-active models with tools beat LARGER bare models in
   same-family controlled tests (S1) and match last-generation frontier (S4, S18, S20, S21).
2. **The thesis's own words need repair:** "the MCP server gives dumb agents frontier
   capabilities" holds for mid-small open models (gpt-oss-class, 3.3B-active MoE) on
   well-scoped tool pools. It does NOT hold for 8B-class models on raw MCP orchestration
   (S7: 0.428 vs 0.749), and it inverts at large tool pools (S9) unless the harness retrieves
   and prunes tools. The dumb-agent claim survives only with a smart HARNESS.
3. **The fabrication angle is real but conditional:** grounding fixes hallucination when
   paired with verification and refusal (S13); tool access alone makes it worse (S14).
4. **Long-horizon reliability is the unfixed gap:** pass^k compounding (S24) means per-turn
   small-model error rates dominate over long trajectories; nothing in the 2025-2026 corpus
   shows a 1-9B tool-agent matching current frontier on long-horizon reliability.
5. **For Mag:** the external evidence endorses the estate's shape (local janitors first,
   specialist dispatch rare) with three specifics: keep janitor tool pools narrow (single-digit
   tools, S9/S10), wrap them in verification loops with refusal breakers (S13/S14), and treat
   scaffold work as the cheap capability lever (S2/S3/S23). gemma:2b-class scut should stay on
   trivial single-tool lanes; the 3-8B class is the floor for real MCP tool use (S7, S12).

**Instrument note:** all numbers above are as reported by the cited pages at sweep time
(2026-10-01); leaderboard rows (SWE-bench, BFCL, MCP-Atlas, MCP-Bench) move weekly and several
came via search-result summaries of the live boards rather than direct board reads; S2's
42-78% swing and S5's Arch-Agent wins are the two weakest links in the chain and are marked
accordingly. No em-dashes were used in this file (estate law).
