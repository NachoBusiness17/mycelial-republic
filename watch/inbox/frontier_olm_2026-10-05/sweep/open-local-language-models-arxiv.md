# SWEEP: open-local-language-models via arXiv (frontier_olm 2026-10-05)

source-fetched: 2026-10-05
seat: sweep-open-local-language-models-arxiv (workflow subagent)
instrument: WebFetch on export.arxiv.org/api/query, hn.algolia.com, arctic-shift.photon-reddit.com, aleph-alpha.com, alphaxiv.org; WebSearch; local greps with rg and .venv\Scripts\python.exe.

## Method, two passes, honestly labeled

Pass 1 (broad): 6 arXiv export-API queries + 2 HN Algolia queries + 4 WebSearch passes surfaced 39 in-window candidates (2026-09-05 to 2026-10-05). Query receipts, each fetched this session: `all:"local llm"` (totalResults 170, matches doors.md), `cat:cs.CL abs:"small language model" abs:agent` (69), `abs:"function calling" abs:"small language model"` (6), `abs:"open-weight"` (1136), `abs:"open-source" abs:release` (438), `abs:"on-device" abs:LLM` (457), plus HN search_by_date on "open weights model". Pass 2 (deep): 12 items read end to end as complete abstracts + metadata via one id_list batch fetch each (`id_list=2610.02001,2609.07370,2608.22472,2609.19169,2610.00954,2610.02206,2609.36654` then `id_list=2609.13824,2609.33446,2609.31540,2610.02702,2609.33878`), plus one alphaxiv full-detail read (Mingbird), the official Kolibri release post, the Clef HN thread, and Gemma 4 / Laya spec pages via search.

**Door degradation, stated:** arxiv.org/abs, arxiv.org/html, export.arxiv.org/abs, and hn.algolia.com/api/v1/items all timed out at the 60s WebFetch limit this session (5 timeouts total). Full-paper HTML was therefore NOT readable; the deep reads are complete-abstract reads through the proven export door, not full-text reads. Axios returned 403 on the Reflection AI open-weight story (title seen on HN 2026-10-04, body unread: OWED). nbot.ai returned "Post Not Found" for a guessed Kolibri URL (my invented URL; the real one is aleph-alpha.com, fetched clean).

## Answers to the five questions

### RQ1: 90-day open-weight releases, 7B to 70B class, VRAM

- **Kolibri 1 (Aleph Alpha, released 3 October 2026).** Apache 2.0, full weights on Hugging Face (Aleph-Alpha/Kolibri-1). Spec: 78.1B total, 3.46B active per token (sparse MoE), context "supports context lengths of up to 1M tokens" (16k pretrain, 256k longest trained, 1,048,576 via vLLM flags). The post names vLLM serving plus `--kv-cache-dtype fp8` but gives NO self-host VRAM figure; vendor-stated hardware stops at "trained on 768 B200 GPUs". At 3.46B active the per-token compute is janitor-class; the 78B total means weights need roughly 40GB+ at 4-bit (my arithmetic, not a source). This is the first sovereign-European Apache entry in the ladder's specialist slot at near-janitor serving cost. Source: https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/
- **Clef and Clef-flash (Cloudflare, ~1 October 2026, HN 638 pts).** Open-weight Jev-style decision models post-trained from Qwen bases; per HN comments quoting the model card, "Clef-Flash is post-trained from Qwen/Qwen3.5-9B", Clef reported as Qwen3.8-27B base (comment-sourced, sizes not vendor-verified this session); 32K context, image input. Decision models at 9B/27B are a new rung between scut and worker. Source: HN item 49923692 via hn.algolia.com search API.
- **Laya (Convai Innovations, ~28 September 2026).** 421M non-autoregressive decision model, Apache 2.0, ~32.8 ms p50, weights on HF (convaiinnovations/laya). Not 7B-70B, but it is a downloadable scut-tier replacement candidate for classification-shaped sensing calls. Source: WebSearch (runware.ai and HF surfaced).
- **Gemma 4 family (Google, April 2026: outside the 90-day window but it is the family the estate's `gemma4` janitor name maps to).** E2B (~8GB RAM), E4B (~16GB RAM), 12B (16GB VRAM, laptop class), 26B MoE (32GB+), 31B dense (~71GB BF16, one H100; 4-bit fits modest hardware). Source: ai.google.dev Gemma 4 model overview via WebSearch.
- **Qwen3.5-9B: ~8.3GB VRAM at Q4_K_M (~5.5GB weights)** per willitrunai via WebSearch. Qwen3.5-397B-A17B (Feb 2026, outside window) is the family flagship; Qwen3.8 checkpoints are named as real in the estate's own 10-02 sweep (`watch/inbox/frontier_olm_2026-10-02/sweep/quantization-compression-reddit.md`) and in arXiv 2610.02702's evaluated set (Qwen3.5-4B, Qwen3.6-27B, Llama-3.1-8B).
- **Reflection AI release (2026-10-04, Axios "Powerful open model is set to shake up AI race")**: door 403'd; sizes and license unverified, OWED.
- **Quantization side of VRAM:** NVFP4 "Schur Replay" (arXiv 2609.36654, 2026-09-29) hits 99.35% and 100.84% BF16 recovery on Qwen3.5-397B-A17B and Llama-3.3-70B-Instruct while keeping "only the active layer resident" during quantization, cutting per-layer export time 15.17x vs ModelOpt. Estate note: our banked 3-bit cliff law for agentic replay (`memory/percolator/candidates.jsonl:15`, 11B 0.716 to 0.045) still gates what "recovery" means off-benchmark.

**Ladder verdict:** the 90-day window moved the specialist tier down to ~3.5B-active MoE (Kolibri) and minted a decision-model rung (Laya 421M, Clef-flash 9B, Clef 27B). The janitor-first shape survives but the "remote specialist scarce" assumption weakens: a 78B-total MoE with 3.46B active is self-hostable on a single fat GPU at 4-bit and carries a 1M context.

### RQ2: who beats the gemma:2b scut and gemma4 short-worker on tool-call-shaped tasks

- **arXiv 2609.07370 (2026-09-07), sub-2B MCP-style tool calling on CPU:** five open-weight models (Phi-1.5, Pythia-1.4B, TinyLlama-1.1B-Chat, Qwen2.5-0.5B, Qwen2.5-1.5B) on 100 prompts. "Only 5 of 1,000 raw responses parsed directly as JSON". Qwen2.5-1.5B reached 75% greedy / 79% sampled reliability (7,960 MiB, 30.78s mean latency); Qwen2.5-0.5B 72% greedy but 32% sampled (3,637 MiB, 10.63s); Phi-1.5 scored 0%, Pythia and TinyLlama at most 7%. Direct gemma:2b vs Qwen comparison is NOT in this paper; the honest ladder move is: at the scut footprint, Qwen2.5-1.5B-Instruct is the only sub-2B family in this benchmark that tool-calls reliably at all, and any sub-2B janitor needs schema validation + constrained generation wrapped around it.
- **arXiv 2608.22472 (2026-08-23), IFFC:** Instruction-Followed Function Calling delegates the tool call from the main model to a smaller dedicated model in plain instruction-following format; it beats native and prompt-based function calling, "remains robust under aggressive quantization, allowing efficient on-device deployment without notable accuracy loss". This is a mechanism the harness can adopt to let gemma:2b keep its janitor seat while a quantized small model owns the tool-call lane.
- **HESP (arXiv 2609.33446, 2026-09-27):** five models 7B-72B, 7,272 audited episodes of local alert triage. HESP "raised Qwen2.5-7B from 0.125 to 1.000 verified completion"; controller-side stopping took Llama-3.1-8B from 0 to 0.917. Probing and stopping are separate failure modes; both belong in the harness, not the weights.
- **Mingbird (arXiv 2610.02001, 2026-10-01):** on the estate-adjacent model `gemma4:e2b` (Ollama tag; ~5B total, ~2.3B active), Mingbird averaged 0.821 vs 0.017-0.271 for goose/opencode/agent-mini on the same 18 tasks; tau2-bench 278 tasks 0.856 vs 0.791 and 0.737; frontier probe 0.997-0.478 across harnesses with good scaffolds within 0.072 of each other. The janitor's weakness is the harness, measurably.
- **Local judge caution (arXiv 2609.13824, 2025-09-12):** LLaMA-3-8B and Qwen2.5-7B local judges hit r=0.275/0.340 vs humans while self-consistency read 97.3%/92.3%. Do not let a consistent janitor grade its own work.
- **Dual local judges that work (arXiv 2609.33878, 2026-09-27, ICDMW SENTIRE 2026):** Muse Glimmer 30B + Gemma 4 31B with ordered confidence gates (0.86, 0.80) labeled at 96.88% purity at 81.7% coverage, beating either alone by 2+ points; higher reasoning effort gave no clear F0.5 gain at 1.8-5.0x latency.

### RQ3: freshest arXiv on small local models as agent executors vs hosted-API agents

The 170-hit "local llm" feed and the 69-hit SLM-agent feed converge on one thesis this month: the harness, the checks, and the controller decide local-agent success, not raw weights. Evidence read this session: Mingbird (harness swap moves gemma4:e2b 0.017 to 0.821), HESP (controller moves Qwen2.5-7B 0.125 to 1.000), Touchstone (arXiv 2609.31540, 2026-09-25: seven 1-8B SLMs with task-specific deterministic checks reach 98.6% conflict detection and 93.8% intent translation while escalating only 16-17%, and the paper's rule is "keep inference local when precise low-cost checks exist, escalate otherwise"). Against that, Tokenomics of Agentic SLM Ensembles (arXiv 2610.00954, 2026-10-01) shows the ceiling: an SLM ensemble with SLM-judge feedback reaches 97.34% IFEval strict, "beating the strongest standalone baseline (gpt-5.4) by 5.81 percentage points at lower cost", paid for in test-time tokens and orchestration. SiliconBench (arXiv 2609.19169, 2026-09-12) adds the serving reality: nine Apple Silicon engines tested on Qwen3/Qwen3.5/Gemma 4 chat+agent serving; "Only three stacks passed completion, fidelity, and model-coverage gates"; explicit memory budgets did not guarantee headroom; packed prefill-decode kept first-token latency lower under load; tensor parallel over Thunderbolt RDMA scaled while pipeline parallel over TCP regressed. Also noted: KaliBench (2610.02206, already banked in our corpus) fine-tunes an 8B to match a 685B MoE on CLI tool translation while no off-the-shelf open-weight config exceeded 42% exact-command accuracy.

### RQ4: the r/LocalLLaMA JSON recipe (doors.md OWED)

CLOSED, with prior-art credit. Working recipe verified this session via WebFetch, no credentials, JSON returned:

```
https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=LocalLLaMA&limit=3
```

Response: `{"data": [ ... ]}` array of post objects, newest first; first three posts carried created_utc 1791211099 / 1791210800 / 1791210427 (2026-10-05, same-day). Negative result, also new: appending `&sort=desc&sort_type=score` (or `&sort=top`) returns HTTP 400 Bad Request on this endpoint, twice probed; the minimal param set is what works. `www.reddit.com/r/LocalLLaMA/top.json?t=day&limit=3` returned HTTP 403 Blocked (confirms doors.md's old.reddit HTML interstitial and the 10-02 sweep's 403). PullPush (`api.pullpush.io/reddit/search/submission/`) answered 429 Too Many Requests, alive but throttled. Prior art the estate already holds: `memory/corpus/LINKS.jsonl` BG123-HARVEST (2026-09-18): "arctic-shift (Pushshift successor) is the live reddit-corpus path", and the corpus-harvest skill ships an arctic-shift path; the 10-02 sweep used it via curl with 15s spacing (422 without). This session's delta: the WebFetch-shaped minimal recipe plus the sort-param 400 trap, now written down for the doors.md owner to fold in.

### RQ5: do the mine/raw rows answer current best-local-model questions, and the staleness boundary

No, and the boundary is now measured. My scan (`watch/inbox/frontier_olm_2026-10-05/sweep/_mineraw_scan.py`, run with `.venv\Scripts\python.exe`, output captured this session): mine/raw is 103,033 files, 5,732,628,350 bytes across five dirs (agent_platform 75,279 files; agent_bleeding_edge 15,759; mesh_comm 5,685; steal_protocol 4,494; narrative_corpus 1,816), 56,613,548 raw lines counted. It is cloned GitHub repositories (a2aproject/A2A, Aider-AI/aider, briar, getzep/zep, et al.), i.e. agent/LLM engineering code, exactly as the lens seat counted it: "Scraped `mine/raw` 97,865 rows" (`watch/inbox/frontier_olm_2026-10-05/lens/corpus.md` section 1, catalog-row denominator; my disk-file denominator reads 103,033 at a later moment). File mtimes run 2026-08-05T12:56:55Z (oldest) to 2026-09-09T23:41:33Z (newest). Therefore the corpus's freshest possible signal from this shelf is 2026-09-09, 26 days before today: Kolibri (10-03), Clef (10-01), Laya (~09-28), the Reflection story (10-04), and every paper banked above dated after 09-09 are invisible to it. And by kind it was never a model-eval corpus (lens title hits: agent 2,323, llm 1,007, mcp 875 in code files): it answers "what agent code exists", not "which model is best". The 97,865-vs-103,033 delta is a denominators note for the lens seat, not an error claim: different instruments (catalog rows post-exclusion vs os.walk files), different moments.

## Banked items (8, strongest first)

1. **Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks** (arXiv 2610.02001, 2026-10-01). Overlap: title string already in catalog, `state/arxiv/2026-10-02/2610.02001v1.txt` (banked 10-02); this sweep's add is the per-model numbers and the gemma4:e2b harness-swap delta.
2. **Can You Check That? The Checkability Boundary for Local LLM Network Automation** (arXiv 2609.31540, 2026-09-25). Overlap: `state/arxiv/2026-09-28/2609.31540v1.txt` in catalog.
3. **HESP: Separating What to Probe from When to Stop in Local LLM Alert-Triage Agents** (arXiv 2609.33446, 2026-09-27). Overlap: no hits in catalog.jsonl or memory/ for "HESP" as title (only a false-positive WoW boss file `boss_hydromancer_thespia.cpp`).
4. **Beyond Fluent Generation: A CPU Reliability Benchmark for MCP-Style Tool Calling in Sub-2B Small Language Models** (arXiv 2609.07370, 2026-09-07). Overlap: `watch/inbox/frontier_olm_20260928/sweep/_raw/full_2609.07370.txt` + lsa_reboot_staging copy in catalog.
5. **SiliconBench: Speed, Memory, and Fidelity for LLM Serving on Unified-Memory Desktops** (arXiv 2609.19169, 2026-09-12). Overlap: no catalog or memory hits for "SiliconBench".
6. **Kolibri: A Sovereign Open-Weight Model** (Aleph Alpha, 2026-10-03, https://aleph-alpha.com/en/blog/kolibri-has-landed-a-sovereign-open-weight-model/). Overlap: no catalog or memory hits for "Kolibri".
7. **Small Reasoning Models are Instruction Followers in Function Calling (IFFC)** (arXiv 2608.22472, 2026-08-23). Overlap: no hits for "Instruction-Followed Function Calling" or "IFFC" in catalog or memory.
8. **Beyond Leaderboards: Tokenomics of Agentic Small Language Model Ensembles** (arXiv 2610.00954, 2026-10-01). Overlap: no hits for "Tokenomics of Agentic" in catalog or memory.

Bench alternate (ninth by strength, cut by the 8-item cap): KaliBench 2610.02206, already banked at `state/arxiv/2026-10-02/2610.02206v1.txt`.

## OWED carried forward

1. Reflection AI open-weight release details (Axios 403; HN title-only).
2. Full-text reads of the 12 deep-read papers (arxiv/html and items doors timed out this session; abstracts are complete).
3. Kolibri self-host VRAM: vendor publishes none; a measured GGUF/vLLM number is owed before it enters the ladder table.
4. Clef/Clef-flash base-model sizes rest on HN comments quoting model cards; vendor page unfetched.

## Commands run this sitting (receipts)

- WebFetch x2 arXiv queries ("local llm" 170; id_list 7+5), plus 4 more queries (69/6/1136/438/457 totalResults).
- WebFetch probes: www.reddit.com top.json (403), arctic-shift with sort params (400 x2), arctic-shift minimal (200 JSON), pullpush (429), HN search x3, HN items x2 (timeout), aleph-alpha.com post (200), axios (403), alphaxiv (200), nbot.ai guessed URL (Post Not Found).
- `rg` greps over catalog/catalog.jsonl and memory/ for 10 title strings (4 real hits, all prior intake captures; 1 false positive).
- `.venv\Scripts\python.exe watch\inbox\frontier_olm_2026-10-05\sweep\_mineraw_scan.py` (mine/raw staleness scan, exit 0).
