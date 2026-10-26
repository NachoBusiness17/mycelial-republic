# sweep: open-and-local-language-models via X door (2026-09-28)

source-fetched: 2026-09-28
(Activity window 2026-08-29 to 2026-09-28 bounds what this lane enumerated; the fetches themselves
executed 2026-09-29 in the re-run of this lane. Run by subagent sweep-open-and-local-language-models-x
on the Mag Resource Harness seat.)

## Door status (honest)

- Pass-1 `site:x.com` WebSearch queries were DEGRADED exactly as the sibling lanes reported: 9 direct
  probes each returned at most 1-8 results, mostly homepage-level `https://x.com` links with no status
  IDs, and 3 probes hit `MCP error -429 / code 1302` rate limits mid-batch. NOT fabricated as success.
- Recovery (the recipe's sanctioned path): mined smol.ai AINews issues that embed real x.com/status
  URLs (fetched end to end this session: 26-09-10-not-much 144,771 bytes; 26-08-31-not-much 122,326;
  26-09-01-claude-mythos-51 193,875; 26-09-04-collusionwiki 120,285; 26-09-08-navier-stokes 134,570;
  all saved under `sweep/_raw/smol_*.html`), then resolved single posts through the fxtwitter door
  `https://api.fxtwitter.com/<user>/status/<id>`. fxtwitter resolved 15/16 cleanly with verbatim text
  and creation timestamps (raw JSON in `sweep/_raw/fx_*.json`). The 1 failure: MiniMax M2.1
  (2007843119832695114) resolved with EMPTY text (media-only post); not used.
- X articles (x.com/i/article/...) were read through the mcp web_reader door after fxtwitter returned
  only the article link: zaibatsu 2087025327734227092 (full text) and fastino 2088303137182679378
  (full text, 4,978 words) both read end to end.
- One target 404'd: openclawunboxed.com/free-model-stack ("Page not found" via web_reader). The
  search snippet ("power-ranks every free OpenRouter model") is therefore UNVERIFIED and is NOT
  banked. A sibling search-snippet for the same domain listed an Apr 18 post ("stop chasing one local
  model... a role split"), also not resolved. Listed under OWED.
- WebSearch on the Z.ai hosted backend threw 3 rate-limit errors (1302) this session; batches were
  kept small after the first hit and no further limits surfaced.

## Estate grounding done this session

- `wc -l catalog/catalog.jsonl` = 674,146 rows (2026-09-29, this session). Note: the lens corpus.md
  recorded 581,477 at manifest snapshot 2026-09-28T07:33:37Z (watch/inbox/frontier_olm_20260928/lens/corpus.md:14);
  the catalog has grown ~92.7k rows between instruments. Different moments, named per the census law.
- Frontier-lab platform scrape confirmed: `mine/raw/`, 97,865 rows, agent_platform 72,329 +
  agent_bleeding_edge 14,468 + mesh_comm 5,297 + steal_protocol 4,118 + narrative_corpus 1,653
  (watch/inbox/frontier_olm_20260928/lens/corpus.md:15, counted by the lens itself).
- The fold register (watch/inbox/frontier_olm_20260928/register.jsonl, 23 confirmed finds) was read
  this session; its items most adjacent to this lane: arXiv 2609.25373 (FunctionGemma extension),
  2609.07370 (sub-2B MCP tool calling), 2609.21341 (what stops an SLM from driving a database agent),
  The Register "Open weights are not open source" (2026-09-15), the MistralAI free-tier reddit thread,
  "A Cheap Verifier is Good Enough" (2609.33467). None of my 8 banked items duplicate those.
- DeepSeek V4.1-Flash is ALREADY HELD deeply: `watch/inbox/DESK_DSV41FLASH_20260911.md` (operator
  link-drop, 78 lines) verified the 51-page tech report: 552B total, 8B active prefill / 16B decode,
  causal encoder-decoder, Engram hashed n-gram memory, MIT license, 890 bytes/token KV. Plus 9 lane
  files under `watch/inbox/v41_paces/`. This lane therefore banks V4.1-Flash items ONLY where they
  add something the desk does not hold (see item 1).

## RQ answers (evidence read this session)

### RQ1. Open-weight models since 2026-08 beating gemma-class 2B janitors on agentic tool-calling at equal or smaller VRAM

- The one DIRECT in-window, name-checkable ranking of open models on agentic work is arena.ai's Agent
  Arena post (x.com/arena/status/2094566204488962483, fxtwitter-verified, Aug 31): Qwen3.8-Flash-Next
  "#7 among open models (#24 overall) with +2.4% net improvement across 8.7K+ real-world agentic
  sessions", sitting behind DeepSeek V4 Flash (High) #6 and GLM-5.3 (Max) #5. It ranks real sessions,
  not tool-call JSON accuracy, and does not publish VRAM class per rank; use as a routing prior, not
  a janitor verdict.
- RWKV-7 G1j (BlinkDL, Aug 31, fxtwitter-verified): "RWKV-7 G1j (100% RNN) release ... much better at
  agent/coding/STEM and everything." HF repo BlinkDL/rwkv7-g1 read via HF API this session: license
  apache-2.0, 22,917 downloads, files rwkv7-g1j-1.5b / 2.9b / 7.2b / 13.3b, all ctx16384, dated
  2026-08-31. The 1.5B/2.9B sizes are the exact gemma-2B class; a pure-RNN runtime holds O(1) memory
  per token, so long janitor sessions stop paying KV-cache growth. HONEST CAVEAT: the "much better at
  agent/coding" line is the author's claim; zero published agentic-benchmark rows for G1j were found
  this window; weights are .pth (PyTorch), so llama.cpp/Ollama compatibility is unverified here. It
  enters the fleet only through the estate's own battery (the gemma:2b 60-inference scut battery,
  abliterate-p1 census) before any trust.
- Out-of-window but direct (date stated, Aug 14): Fastino's Nemotron 3.5 Lightning writeup
  (x.com/i/article/2088303137182679378, read end to end) is the strongest published tool-calling
  fine-tune recipe found: Recipe I = 27,542 real-harness BFCL trajectories, LoRA rank 32, 2e-4,
  2 epochs, overall 48.00% -> 71.18%, single-turn 51.42% -> 81.88%, multi-turn moved <0.5 point;
  their lesson "Treat single-turn calls and multi-turn state as separate curricula." Their MedAgentBench
  agentic result (16.67% -> 90.00% pass@1, n=300) shows the failure is "the interface, the function
  selection, argument construction, and multi-step state the harness scores, and a specialist adapter
  supplied exactly that", not model knowledge. Released models Apache 2.0. Nemotron 3.5 Lightning is a
  30B/3B-active MoE (article's own numbers), i.e. NOT smaller than gemma-2B; the stealable part is the
  recipe shape (single-turn curriculum for janitors) and the proof that 3B-active class models are
  trainable into reliable tool callers by a 340-experiment agent sweep.
- FunctionGemma (270M) would be the theoretical VRAM floor for the janitor chore, but the base release
  is Dec 2025 (googleaidevs/status/2001703478436184540 era), and its Sep 2026 extension paper
  (arXiv 2609.25373) is already in the fold register. NOT re-banked. One NEW adjacent fact for the
  RQ4 answer, from the Unsloth docs page read end to end (unsloth.ai/docs/models/tutorials/functiongemma):
  BF16 fits in 550MB RAM on CPU, Google says it is intended to be fine-tuned, "not recommended to go
  lower than 4-bit" at 270M, QAT recovers ~70% accuracy for phone deployment at ~50 tok/s on Pixel 8 /
  iPhone 15 Pro, and multi-turn tool calling needs the dedicated notebook (community analyses put
  base multi-turn equivalence at 10-39% before fine-tuning, jangwook.net Feb 2026, snippet level).
- Conclusion: nothing published this window shows a <=2B model BEATING gemma-class on agentic
  tool-calling with benchmark numbers; the candidates (RWKV-7 G1j 1.5B/2.9B, Qwen3.5-4B at the edge
  per NVIDIA Robotics, FunctionGemma 270M for the narrow chore) all arrive as claims or as
  wrong-scale-but-trainable, and the estate's own census (register: 2609.07370, 2609.21341) already
  says harness variables dominate at this scale. The gap is honest: the cell "open <=2B model with
  published agentic tool-call win over gemma-2B" is EMPTY as of this sweep.

### RQ2. Licensing / deployment changes since the 97,865-row frontier-lab scrape that change what the estate can self-host and self-steal

- THE deployment-stack event of the window: Georgi Gerganov, Sep 4 (x.com/ggerganov/status/2095897173376618881,
  fxtwitter-verbatim, 597 likes): "Hugging Face has been acquired by NVIDIA ... Going forward,
  llama.cpp/ggml will stick to its founding principles. One of the most important qualities of the
  project is to be hardware-agnost[ic]." Every local weight the estate pulls transits HF; the hub is
  now NVIDIA-owned, while the runtime that serves janitors (llama.cpp under Ollama) publicly commits
  to hardware-agnostic independence. No license text changed by this, but supply-chain risk and the
  self-steal path (corpus acquisition from HF) now have a different owner on the other end.
- DeepSeek V4.1-Flash shipped MIT-licensed open weights (Sep 10) with day-0 Ollama cloud rollout
  (x.com/ollama/status/2098188014119985406, fxtwitter-verbatim: "starting with Max and Team
  accounts"). The desk already holds the architecture; the NEW licensing-adjacent fact this lane adds
  is ValsAI's independent rank (item 1) and the distribution channel (Ollama cloud tiers), which
  matters for the Oct 27 substrate decision (local weights vs Ollama cloud).
- Meta's licensing reversal (Muse Glimmer, 30B dense, Apache 2.0, agentic-tuned, 24GB VRAM; zaibatsu
  article x.com/i/article/2087025327734227092 read end to end: "The license is the part worth sitting
  with. Most open-weight releases at this scale arrive wrapped in a custom license carrying
  acceptable-use clauses, revenue thresholds, or naming requirements.") is ALREADY HELD by the estate
  almost verbatim: memory/runs/mickey17_v2/lanes/meta-fair-agents.json describes "Muse Glimmer, a 30B
  Apache-2.0 open-weight model tuned for the local agent tool-use loop that fits quantized on a single
  24-32 GB GPU - a direct candidate for the estate's local worker tier." NOT re-banked; the article
  adds only the license commentary quote.
- The definitional fight (open weights vs open source; OpenMDW license with NVIDIA as contributor) is
  banked by the HN sibling lane (open-and-local-language-models-hn.md:26). Cross-referenced, not
  re-banked. FunctionGemma derivatives inherit the Gemma License (restrictive vs MIT/Apache), noted
  above from the search snippet; treat as OWED (model card license field not read directly).

### RQ3. Any free or open-weights rung as a VERIFICATION surface, or does the DRIVING LADDER sensing-only rule match consensus?

- No in-window X-door item directly tests free-tier VERIFICATION quality. What the window does
  corroborate, all snippet-level unless noted: OpenRouter `:free` variants are "often lower-quality
  quantized or rerouted versions" (ofox.ai snippet), free plans cap at 50 requests/day under $10
  credit (HF forums snippet), and the estate's own register already banks the Mistral free-tier
  uncertainty thread (reddit 1whurp8). My attempt to read the strongest-looking free-model ranking
  (openclawunboxed.com/free-model-stack) hit a 404, so the pro-free-ranking case stays UNVERIFIED.
- The closest read-in-full evidence remains indirect: the register's "A Cheap Verifier is Good Enough"
  (2609.33467) argues verification needs a CHEAP model, not a FREE one, and this lane's Fastino read
  shows even a 3B-active paid-class model needs a specialist adapter before its verdicts are tool-call
  reliable. Published consensus as sampled this window therefore SUPPORTS the AGENTS.md DRIVING LADDER
  shape (free lanes sense, funded tier verifies), and adds one refinement: the sensing surface is
  degraded in exactly the ways a sensing surface can tolerate (quantized, rate-capped), while the
  verification rung wants cheap-paid or local fine-tuned, never free-stealth.
- A local open-weights verification rung is NOT excluded by anything found: RWKV-7 G1j (Apache 2.0)
  and a Qwen3.5-4B-class edge model (NVIDIA Robotics tutorial, fxtwitter-verbatim) are the two
  candidates a local BFCL-style battery could trial as cross-family verifiers, per the HN sibling
  lane's router-math caveat that the judge must be a different family than the judged model.

### RQ4. Smallest viable local model for structured JSON tool calls, and a local re-rank benchmark for the janitor fleet

- Smallest PUBLISHED structured-call model: FunctionGemma 270M (Gemma 3 270M base, dedicated call
  format `<start_function_call>call:name{...}`, BF16 in 550MB CPU RAM, ~50 tok/s on a phone;
  Unsloth docs read end to end). With the caveats above: single-turn chore only until fine-tuned,
  4-bit quant floor at 270M, and its extension paper is estate-held (register 2609.25373). The estate
  could fine-tune it on its own 60-prompt scut battery per Google's "intended to be fine-tuned"
  design and the day-zero Unsloth notebook.
- The re-rank benchmark the estate can run locally TODAY, assembled from what this lane read:
  BFCL-style function-calling cases (the Fastino recipe consumed 27,542 real-harness trajectories and
  published the curriculum split), evaluated with the estate's own scut battery as the environment
  (gemma:2b 60-inference x3 census already exists as the instrument and the P2 gate), plus the
  register's constrained-decoding finding (2609.23742: schema validity to 100% via constrained
  decoding at 1.6-3.7% throughput cost) as the fixed serving condition so the re-rank measures MODEL
  delta, not grammar delta. Candidates to re-rank against gemma:2b: RWKV-7 G1j-1.5B/2.9B, Qwen3.5-4B,
  FunctionGemma-270M (fine-tuned single-turn). Fastino's split is the design law to copy: single-turn
  call accuracy and multi-turn state are separate curricula and must be scored separately, or the
  janitor's 82% single-turn number will hide a flat multi-turn reality.

## Banked items (8, strongest first)

1. ValsAI closes the desk's UNPROVEN K3 row: DeepSeek V4.1 Flash is the new #1 open-weight on the
   Vals Index, beats Kimi K3, $0.30/test (Sep 10). watch/inbox/DESK_DSV41FLASH_20260911.md:46 flags
   "beating K3" UNPROVEN and asks to tri-state it from Figure 1a; this is independent third-party
   corroboration, new to the estate.
2. ggerganov: Hugging Face acquired by NVIDIA; llama.cpp/ggml stay hardware-agnostic (Sep 4). Zero
   prior estate holdings for the event; the estate's whole local stack depends on both.
3. RWKV-7 G1j open weights, Apache-2.0, 1.5B/2.9B/7.2B/13.3B ctx16k (Aug 31). New gemma-class-size
   RNN candidate for the janitor re-rank; claim-level on agent/coding until the estate's own battery
   runs.
4. Fastino Nemotron 3.5 Lightning agent-run fine-tune (Aug 14, OUT OF WINDOW, date stated): Recipe I
   BFCL 48% -> 71.18%, single-turn 51.42% -> 81.88%, multi-turn <0.5pt; single-turn vs multi-turn as
   separate curricula; adapters Apache 2.0. The reusable recipe for janitor specialization.
5. arena.ai Agent Arena open-model ranking on 8.7K+ real agentic sessions (Aug 31): Qwen3.8-Flash-Next
   #7 open, DeepSeek V4 Flash (High) #6, GLM-5.3 (Max) #5. Name-checkable external routing prior.
6. NVIDIA Robotics Jetson edge fine-tune tutorial (Aug 31): Unsloth QLoRA -> GGUF -> llama.cpp on
   Jetson; Nemotron 3.5 Lightning on AGX Thor, Qwen3.5-4B on Orin Nano. Documents Qwen3.5-4B as an
   edge-scale artifact and the vendor path for on-device janitor specialization.
7. ollama: DeepSeek-V4.1-Flash rollout on Ollama cloud, Max/Team first (Sep 10). Deployment-surface
   fact absent from the desk file; bears on local-weights vs Ollama-cloud for the Oct 27 substrate.
8. zizhpan: DeepSeek-V4-Flash-Vision-Exp weights open on HF (Aug 31). Separate open-weights vision
   checkpoint from the V4.1 line the desk holds; catalog 0.

## Pass-1 candidate ledger (34 considered; window 2026-08-29..09-28 unless noted)

X-resolved verbatim via fxtwitter this session (raw JSON in sweep/_raw/): ValsAI 2098125164072554545,
ollama 2098188014119985406, rasbt 2098142625819672603, ggerganov 2095897173376618881, zizhpan
2094386230675062836, NVIDIARobotics 2094480283135316182, ollama 2094622506720391454 ("ollama launch
muse", Sep 1), Alibaba_Qwen 2094968708288680276 (Qwen3.8-Max-0902, 2.4T, API-only, NOT open weights,
dropped from banked items), kimmonismus 2097286327909675477 (V4.1 beta, Sep 8), arena 2094566204488962483,
ash_csx 2088307712534663180 (Aug 14 thread, folded into item 4), BlinkDL_AI 2094785763129151677,
ArtificialAnlys 2098148674203488422 ("At just 552B parameters ... costing ~4x less per token", Sep 10;
matches the desk's 552B, CONTRADICTS smol's 763B-total recap, reported as a source conflict),
MiniMax_AI 2007843119832695114 (EMPTY text, dead end), TheValueist 2050758319837454598 (May 2026,
off-topic). smol-issue-mined X URLs considered, not resolved: finkd Muse Code GA trio 2094500475710099945/698/738,
alexandr_wang 2094502557129543774, ArtificialAnlys 2098148681962913915 / 2098148684185972758,
harvey 2097372371195953272 (GLM-5.2 SFT 46->60%, Qwen3.5-122B-A10B GRPO 30->63%), eliebakouch
2098223948127183261 (already the desk's own source, 2097931464344015347), vllm_project 2098214992755765758,
stochasticchasm V4.1 architecture reads, teortaxesTex V4.1 series. Non-X read or snippet: zaibatsu
Muse Glimmer article (Aug 11, OUT OF WINDOW, read end to end, already held by mickey17 lane), fastino
X article (Aug 14, read end to end), unsloth.ai FunctionGemma docs (read end to end, May 2026-updated),
smol 26-09-10 Apple-Silicon section (Qwen3.8-Flash-Next MLX-serve 1M ctx on M5 Max 128GB, in-window,
reddit-sourced; considered, not banked: serving-engine detail), smol 26-08-31/09-01/09-04/09-08 issues,
DeepSeek V4 Flash 112GB local-box post (ShawnMarck, snippet, no status ID resolved), arcprize V4 Flash
ARC-AGI post (snippet, no ID), googleaidevs/osanseviero/ollama FunctionGemma posts (Dec 2025, out of
window), jangwook.net FunctionGemma multi-turn analysis (Feb 2026, snippet), Franklin multi-model
article 2049181031551340950 (Apr 28 2026, OUT OF WINDOW, read end to end, vendor marketing for a
gateway product, cite-with-interest only), openclawunboxed free-model-stack (404), ofox.ai GLM free
analysis (snippet), HF forums free-plan caps (snippet), icunucmi "partial brain" post (Apr 2026,
off-topic), "How to Run Claude Code Locally" (Jan 2026, stale), darraghcurran Fin webinar article
(model-version drift, snippet), dair_ai papers-of-week article (not resolved), NVIDIA-HF acquisition
news coverage (corroborated by ggerganov primary).

## Overlap greps actually run this session

Commands: `grep -ci "<phrase>" catalog/catalog.jsonl` and `grep -ril "<phrase>" memory/ | head -3`
(two background batches over the 674,146-row catalog; raw outputs in the session transcript). Results:
V4.1-Flash catalog 11 (desk + v41_paces lanes) HELD; "V4.1 Flash" catalog 3 + openrouter-probes-20260918
HELD; Muse Glimmer catalog 0 but memory/runs/mickey17_v2/lanes/meta-fair-agents.json HELD (exact
"direct candidate for the estate's local worker tier" language); FunctionGemma catalog 1
(corpus_gap_research ARXIV_REGISTER, = register 2609.25373) HELD; Nemotron 3.5 catalog 0, memory hits
incidental (agent session transcript, scout_findings, an unrelated Aug 8 research pack) NEW;
Gerganov catalog 0, memory hits incidental (biography residual, burns LEDGER, improve candidates)
NEW-for-the-event; "Vals Index" catalog 0, memory trajectory-only NEW; Qwen3.8-Flash-Next catalog 0,
memory biography/compaction incidental (known-by-name, no benchmark row) NEW-as-finding;
"Agent Arena" catalog 0, memory hits are game-arena senses (capability_manifest, framework_map,
knowledge_graph) NEW; rwkv7-g1 catalog 0 NEW; "RWKV-7 G1j" catalog 0, memory 0 NEW; G1j catalog 0,
memory only orchestrator session transcripts (incidental) NEW; DeepSeek-V4-Flash-Vision catalog 0,
memory only session transcripts NEW; "launch muse" catalog 0 NEW; Muse Code catalog 1 + mickey17
meta-week lane KNOWN (not banked by this lane); openclawunboxed catalog 0. Sibling-lane cross-check:
grep -ril rwkv/ggerganov/V4.1 over sweep/*.md + register.jsonl + DIGEST.md found "RWKV"/"RWKV 8B"
only as bare names in evals-self-improvement-reddit.md:16 (a listing, not an item) and the nrehiew
V4.1 post already verbatim in quantization-compression-x.md:65 (different post, not re-banked).

## OWED / not verified this session

- RWKV-7 G1j on ANY published agentic/tool-calling benchmark: none found; author-claim only. Its
  llama.cpp/Ollama runnability: unverified (.pth weights seen in the HF file list; no GGUF conversion
  status checked).
- Agent Arena per-model VRAM class and methodology page: not read (post links out; not fetched).
- ArtificialAnlys 552B vs smol-recap 763B total-parameter conflict: both posted Sep 10; unresolved
  here. The estate's desk-verified number from the primary tech report is 552B total.
- openclawunboxed free-model-stack content: 404; the "power-ranks every free OpenRouter model" claim
  and the Apr 18 role-split post remain UNVERIFIED.
- ofox.ai and HF-forums free-tier claims: search-snippet level, pages not read.
- Qwen3.5-4B existence rests on NVIDIA Robotics' own post; no model card pulled.
- FunctionGemma model-card license field: not read directly (Gemma License per search snippet).
- smol.ai issues after Sep 10 (Sep 11-28): the /issues archive page truncated at Sep 10 and the RSS
  head only carried 26-09-09; the late-September X corpus (Kimi K3 open-weight questions, MiniMax M3,
  any license changes after Sep 10) is UNDER-SAMPLED this lane. The NVIDIA/HF acquisition and the
  26-09-04 issue partially cover Sep 4-8; Sep 11-28 came only through targeted search snippets.

## Receipts (raw artifacts, all this session)

sweep/_raw/fx_*.json (16 fxtwitter resolutions), sweep/_raw/smol_26-09-10.html (+ 4 sibling issues),
sweep/_raw/hf_rwkv7g1.json (HF API read of BlinkDL/rwkv7-g1: license apache-2.0, 4 G1j files).
