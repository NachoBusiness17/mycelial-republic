# SWEEP: inference-efficiency via X, 2026-10-03 (evening pass)

source-fetched: 2026-10-03
Sweeper: sweep-inference-efficiency-x (frontier sweep gopher, GLM-5.3-Flash seat).
This file REPLACES the same-day earlier version written by this sweep lane's morning pass
(same path, same sweeper name), per the open-append house rule the burns lens used: the
morning pass banked CAST 2610.00321, DSpine 2609.36173, cua-speedrun 2609.40284,
DolphinBench 2609.24971, Tokenomics 2610.00954, SqueezeBits guided decoding, and llama.cpp
PR 27342; none of those are re-banked here. Every claim below cites what was read or run
this sitting.

## Door status (the X door, said straight)

- X discovery is degraded exactly as the burns lens recorded (lens/burns.md section 2):
  of ~16 WebSearch attempts aimed at x.com, roughly half died with backend 1302/429 rate
  limits and the rest returned stripped URLs (bare https://x.com, no status IDs) or
  silently widened past site:x.com. ZERO in-window post resolved to a full
  x.com/<user>/status/<id> URL from search this pass.
- The fxtwitter resolution door itself WORKS: https://api.fxtwitter.com/Adragon021/status/2062126816941469932
  returned HTTP 200 with real post JSON (Evan Ma, created Wed Jun 03 10:58:40 +0000 2026,
  X article "From Tokens to Agent Cost Design"). Door healthy; the break is search-side
  URL stripping, and that one post is out of the 30-day window so it is NOT banked.
- Per the recipe fallback, search snippets were banked as snippets and are labeled
  snippet-only below; nothing was fabricated into a resolution.
- gh CLI against github.com was the strongest door this pass (llama.cpp primaries).

## Q3 ANSWERED with a local instrument (the ask's cross-check, run this sitting)

The burns ledger silence is a TELEMETRY SPLIT, not a spend stop. The usage.jsonl
cross-check reads:

- `memory/burns/LEDGER.jsonl`: 693 lines (wc -l this sitting), tail row is the
  doctrine-owed-chase closure, no ts after 2026-09-28 (matches lens/burns.md:37-40).
- `memory/runs/hermes_burn/usage.jsonl`: 1,275 lines (wc -l), FIRST row ts
  2026-10-01T13:11:41Z (head -1) -- the instrument itself only begins 10-01.
- Per-day grep over usage.jsonl: 2026-09-28 = 0 rows, 2026-09-29 = 0, 2026-09-30 = 0,
  2026-10-01 = 236, 2026-10-02 = 5, 2026-10-03 = 1,034 (236+5+1034 = 1,275 = total).
- Cost sums (python json pass this sitting): 10-01 $37.7591 (147 ok:true / 89 ok:false),
  10-02 $1.1739 (3/2), 10-03 $25.6218 (801/233). 888 of the 1,034 10-03 rows carry
  `doubled_key:true`.

Verdict: real dollars flowed on 10-01 and 10-03 while LEDGER.jsonl stayed silent, so
spend did NOT stop. But 09-29/09-30 spend is recorded by NEITHER instrument (a true
unrecorded gap), and the 10-03 hermes_burn rows carry heavy meter noise (86 pct
doubled_key, 233 ok:false rows at zero cost). The named instruments disagree by coverage,
not by sign. The per-dispatch tank accounting probe stays OWED for the 09-29/09-30 hole.

## Pass 1 ledger (candidates considered, 34)

In-window (2026-09-03..10-03) X/web candidates: latent.space AINews Sep 24 (Tev1 0.8B
~50ms E2E on Ollama); hellogumbo/awesome-jev GitHub directory; blog.jjannet.com Kev
snippet (0.8B/4B/9B Qwen3.5, Kev-9B trails Jev by 3.5 pts, SNIPPET-ONLY, page not
reachable); AIBriefs Sep 23 (llama.cpp adds /v1/systemone); nisten/iotcoi X reposts of the
llama.cpp decision-models post (Sep 22-24, status IDs stripped by search); groq 498
Flex-Tier error code doc row; grizzlypeak/DataKern/aicentralresources Groq org-level
per-model limit pages (SNIPPET-ONLY, corroborate banked r16); laozhang.ai OpenRouter free
tier (200 RPD class); xugj520 OpenRouter 20 RPM / 50 RPD / 1000 RPD after $10 top-up;
DeepSeek V3.2 ~$0.28/$0.42 pricing corroboration rows (geekflare, goML, llm-stats);
Energy Efficiency of Locally Deployed LLMs (arXiv API read: 2608.00008v2, submitted
2026-06-12 -- OUT of window; the Sep 25 date in the search snippet contradicts the API's
submittedDate, both instruments named, not banked); mayhemcode RTX 5090 llama.cpp 1.9x
(Sep 5, web not X, unfetched); HF Daily Papers Online Draft Co-Training (Sep 6, arXiv ID
not found by search); Verification-Aware Training for Speculative Decoding 2608.30135
(Aug 31 -- OUT of window by 3 days); EdgeFM EAGLE3-style edge pipeline (date unfound);
Hydra edge-SoC workload characterization (date unfound); Ghaderi 2026 18-local-LLM energy
costs (date unfound); LLMs on a Budget power-efficient inference (date unfound).
Out-of-window: Voice Agents Research Brief (Jul 31), Hermes-on-AMD field guide (Jun 24),
Evan Ma thinking-mode post (Jun 3, resolved via fxtwitter, used for door health only),
Tarun Chitra Caching Cheaters (Aug 17), Duke Fuqua cascade piece, TowardsAI four-tier
cascade (15-50x), simo-online orchestration (Mar 8), AgentStop (Nov 2025).

## Pass 2: deep reads (fetched and read end to end this sitting)

Six reads: (1) github.com/hellogumbo/awesome-jev README (WebFetch, full page); (2)
typesafe.ai/blog/introducing-system-one-models-and-jev (WebFetch, full page, dated
Sep 15 2026); (3) ggml-org/llama.cpp PR 29818 via gh (title/state/mergedAt/files JSON +
full body); (4) docs.typesafe.ai/model-jaggedness/jev-1.13 (WebFetch, full page, "Last
reviewed 2026-10-02"); (5) ollama.com/library/tev1 (WebFetch, full page); (6) the
fxtwitter JSON probe (door health). Plus the Q3 local instrument run quoted above.

## The seam: System One decision models landed ON the estate's own stack

The week's genuinely new inference-efficiency fact is that "decision models" (Jev-class:
typed questions in, calibrated probabilities out, NO text generation) became a
llama.cpp/Ollama-native serving feature, merged upstream YESTERDAY:

- PR 29818 ggml-org/llama.cpp, state MERGED, mergedAt 2026-10-02T09:56:05Z (gh JSON):
  "llama, server: add /v1/systemone API (models: laya, julia-1, lev, openjev, kev)";
  35 files, +2139/-15; pre-converted GGUFs `ggml-org/OpenJev-GGUF`, `lev-GGUF`,
  `Laya-GGUF`, `Julia-1-GGUF`, `Kev-4B-GGUF`; body: "'Decision models' are just fancy
  wrappers around traditional embedding models (BERT/Qwen/etc)"; new
  `server_decision_context` keyed on `{arch}.decision.type` gguf metadata; parallel
  shared prompt prefix (causal models only) and vision input supported; question types in
  the test JSON: choice / noul / score. Follow-ups OPEN: PR 29832 (model-agnostic
  decision API, 2026-10-02) and PR 29321 (typed decision readout, 2026-09-27).
- TypeSafe launch blog (the Jev vendor, Sep 15): Jev "outputs all probabilities in
  parallel instead of autoregressively generating by token"; "End-to-end response time is
  70ms-500ms for TypeSafe" vs 3-329s LLM baseline; input $0.042/MTok with output tokens
  free ("too cheap to meter", vendor's own subsidization caveat); RLCD (Reinforcement
  Learning for Calibrated Decisions) instead of RLHF/RLVR; evals vs averaged GPT-6 Astra
  and Fable 5.1 predictions with disclosed team-bias caveats; type-error impossibility is
  structural (schema), not measured.
- docs.typesafe.ai/model-jaggedness/jev-1.13 (last reviewed 2026-10-02) documents the
  failure modes the estate's per-animal harness-profile law demands: "Jev is not a
  calculator"; counting error "grows with the size of the thing being counted"; score
  levels "weak in numerical calibration" (thresholds only); dates read as text; accuracy
  "falls as the state grows with content unrelated to the decision" (context rot);
  adversarial content "can move the answer"; and the judge-relevant one -- option order
  bias, the model "leans toward the option that comes first."
- ollama.com/library/tev1: "A 4B decision model from Together AI for fast classification",
  family "fine-tuned from Qwen3.5 in 4B and 0.8B sizes"; tev1:0.8b is 797MB-812MB, 256K
  context; runs on Ollama's /v1/systemone with choice/noul/score; 73.3 pct accuracy (4B)
  on Bespoke Labs public evals; 26.7K pulls, page shows "updated 2 days ago".
- hellogumbo/awesome-jev (README read): "Jev takes a state plus a set of typed questions
  (Choice, Score, Noul) and returns typed answers with calibrated probabilities in one
  request, no text generation"; early access since 2026-09-15; 1,094 entries, "last
  refreshed 2026-09-24"; gojev runs "in-process Kev via llama.cpp"; third-party latency
  claims ~230-350ms per decision are project-author claims, not benchmarks (the page says
  so itself).
- SNIPPET-ONLY (search snippet, URL degraded, no fetch possible): latent.space AINews
  Sep 24 -- "Tev1 0.8B is a Jev-like classifier running at about 50ms E2E locally on
  Ollama." Also snippet-only: JJannet's Kev sizes/3.5-pt gap.

## Answers to the five research questions

- RQ1 (does 1wv05u1's 0.8B-router result survive the question-class split; can a tiny
  router fill UNMEASURED cells at negligible cost): the sweep found corroboration of the
  SHAPE, not a new measurement. The estate's own split (readable 14/17 at 2-4 pct of
  premium dollars vs simulation 0/5, RIB_ROUTING_CLASSES) already says a router's win is
  question-class-conditional; Jev's own jaggedness doc says the router's option-order and
  state-growth biases need measuring per animal. What IS new: the transport cost of a
  router cell collapsed to ~zero -- a 797MB 0.8B decision model on the janitors' own
  Ollama runtime at ~50ms E2E (snippet), vendor-class at 70-500ms, priced at $0.042/MTok
  input with free output. Per lens/laws.md:30 (instruments-only), none of this fills a
  grid cell; it prices the experiment near $0. The blind-grade pass is still the gate.
- RQ2 (rate-limit shapes post-bank): NO new in-window primary found; search returned only
  snippet corroborations of the banked r16 shape (Groq org-level, per-model; DataKern
  snippet: "rate limits are per-model, at the organization level"; aicentralresources
  ~30 RPM free-tier row). The owed limit-kill census probe over queue/lanes/*/trail.jsonl
  was NOT run this session (stated, not skipped silently).
- RQ3 (burns silence): answered above with the usage.jsonl cross-check -- telemetry
  split, spend resumed, 09-29/09-30 unrecorded, 10-03 rows 86 pct doubled_key noise.
- RQ4 (deepseek thinking re-scope moving an ask-class to mid tier): no external X primary
  surfaced in-window; the estate's 53f56d0f3 re-scope stands as the operative fact and
  the cost-per-blind-point measurement remains an estate instrument not run this session.
  External corroboration of DeepSeek mid-tier pricing (~$0.28/$0.42 per MTok snippets)
  is consistent with the routing grid's existing mid-tier rows; nothing new banked.
- RQ5 (what helps the gemma janitors on RX 5600 XT; what falls under ignore-DeepGEMM):
  the decision-model readout head is the week's direct hit -- it is embedding-model
  based (BERT/Qwen wrappers per PR 29818), runs on the janitors' existing llama.cpp/
  Ollama runtime at 0.8B-4B, and its speed comes from parallel probability readout, NOT
  from FP8/MoE kernels, so it sits entirely OUTSIDE the standing ignore-DeepGEMM verdict
  (lens/laws.md:90, GPU ladder RIB_GPU_LADDER_20261001). Speculative-decoding papers in
  the 29-day window were covered by the morning lane (CAST, DSpine); Verification-Aware
  Training 2608.30135 is 3 days out of window; no in-window RDNA/RX 5600 XT spec-dec
  primary was found on the X door.

## Overlap ledger (grep evidence, run this sitting)

- `systemone` 0 hits catalog, 0 memory; `tev1` 0/0; `RLCD` 0/0; `jaggedness` 0/0;
  `gojev` 0/0; `awesome-jev` 0/0 (catalog grep + the memory-wide grep for
  `jev-style|systemone|jev classifier` which returned nothing).
- `jev` 112 catalog hits -- the estate HOLDS a Jev library (corpus/library/
  jev_steal_library/: persona-eval-harness.md Sep 19 with the Choice/Score/Noul taxonomy,
  4-option Choice 48.3 pct vs decomposed Nouls 98.3 pct; consolidated bibliography
  108,926 bytes). What it does NOT hold: the llama.cpp endpoint (PR merged 2026-10-02,
  postdates all holdings), Tev1, Kev-as-GGUF, RLCD, the pricing/latency claims, and the
  jaggedness failure modes. This sweep banks only those new parts.
- `0.042` (569 hits) and `193.6` (216 hits) are substring noise (Bernoulli et al.);
  checked at detail level, not the TypeSafe numbers.

## Not run / not found (no fabrication)

- No in-window X post resolved to a full status URL; snippets banked as snippets with
  degraded URLs, per recipe. The one full-URL post found (Adragon021) is Jun 3, out of
  window, used for door health only.
- blog.jjannet.com (Kev sizes), grizzlypeaksoftware.com, production-cloud-docs.wiline.com
  and layer3labs.io all 404'd or never surfaced exact paths; their numbers are carried as
  snippet-only claims, never asserted as read.
- The limit-kill census probe, the tank-accounting probe for 09-29/09-30, and the
  cost-per-blind-point remeasure are estate instruments this session did NOT fire.
- The 29-day arXiv spec-dec/early-exit/KV window was largely covered by this lane's
  morning pass; nothing there is re-banked.
