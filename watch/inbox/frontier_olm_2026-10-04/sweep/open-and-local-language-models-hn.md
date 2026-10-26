# SWEEP: open-and-local-language-models via HN (frontier_olm 2026-10-04)

source-fetched: 2026-10-04. Seat: sweep-open-and-local-language-models-hn. Doors used: HN Algolia
(search_by_date + search), news.ycombinator.com item threads, one primary doc (openrouter.ai limits),
one article (withhopper.com), two reddit-door probes (arctic-shift API, old.reddit .rss). No funded
credits spent. No tests run; none asked.

Honest-layers caveat: every quote below passed through the WebFetch fetch-and-answer layer; raw
JSON/HTML bytes were not retained, so quotes are fetch-layer renderings, not byte-verbatim. The
Algolia listings are the strongest byte-proxies (title/objectID/points/created_at echoed verbatim
by the answer layer and cross-checked across queries). Confidence fields carry this discount.

## Pass 1 (broad sweep, window 2026-09-04T00:00Z = created_at_i>1788480000 .. 2026-10-04)

14 Algolia queries run this session (qwen, "local llm", "open weights", ollama, gemma, gguf,
deepseek, "free tier", kimi, glm, minimax, "quantization llama.cpp" [0 hits], Qwen3.8 [relevance],
"Gemma 4", OpenRouter [relevance], "leaderboard local models", "qwen 2.5 quantization" [0 hits in
window]). 60+ candidates considered. Strongest by points: So you want to use OpenRouter 766/207
(49621546, 09-09), Qwen 3.8 Omni Flash 346/138 (49747925, 09-17), DeepSeek Harness Desktop 410/218
(49929489, 10-02), Aleph Alpha Kolibri 414/12 (49943034, 10-03), ArXiv rate-limit policy 149/76
(49926512, 10-01), Weave Router 119/41 (49911500, 09-30), Strata RTX-4090 thread 142/54 (49953495,
10-04), JevBench 153/39 (49800574, 09-22), Janus GGUF Vulkan 104/19 (49926773, 10-01), Shapelearn
Qwen3.8-27B 104/39 (49749393, 09-18), FLUX 3 Image 433/96 (49925974, 10-01), Reddit limits 62/29
(49913588, 09-30), plus consumer-VRAM singles: Run Qwen3.8-27B on 16GB (49745610, 28/10),
Swift-Qwen3.8-27B 33/17 (49727511), Gufo-Qwen3.6-35B-A3B-Q6dense on Strix Halo (49941824),
Qwen3.8-Flash-Next on 2x3090 (49703818), Shapelearn 13.1GB VRAM (49749393), Gemma 4 26B on 24GB
Mac Mini (49683450), 640tok/s Gemma 4 megakernel (49897153), MiniMax H3 on home PC (49879513),
Qwen3.8 Max cost-per-task on ArtificialAnalysis (49723164), OpenRouter Batch API half-price
(49804123), latencyradar DeepSeek-vs-OpenRouter daily latency (49904705), ibragim.dev family
leaderboard (49878767).

## Pass 2 (deep reads, end to end, this session)

Eight pages read end to end (minimum was 5): (1) Strata thread 49953495; (2) Qwen 3.8 Omni Flash
thread 49747925; (3) So you want to use OpenRouter thread 49621546; (4) Reddit limits thread
49913588; (5) Weave Router thread 49911500; (6) Janus Vulkan thread 49926773; (7) withhopper.com
Gemma megakernel article; (8) openrouter.ai/docs/api-reference/limits. Two timeouts at 60s
(49747925 first try, 49621546 twice) answered on retry per the two-attempt door budget.

Door probes run this session (my own instruments, not inherited): arctic-shift.photon-reddit.com
/api/posts/search?subreddit=LocalLLaMA&limit=2 ANSWERED valid JSON (fields subreddit/title/
created_utc/num_comments/score present; first titles: "PSA: if you're on an Intel hybrid CPU, run
Strata's calibrate - it nearly tripled my decode speed (IQ3_S at 256K, 16 GB card)" and "From
1x3090 to 20 DGX Sparks: my house fuses were the first bottleneck"). old.reddit.com/r/LocalLLaMA/.rss
returned the HTML welcome shell, zero feed markup (note: the 10-03 DIGEST banked variant is thread
PERMALINK .rss, which I did not probe; only the subreddit-level .rss is proven dead today).

## Answers to the ask's research questions

### RQ1 - open-weight models in the last 30 days vs the janitor fleet (gemma:2b, gemma4)

- **Strata (github.com/Niko1221/Strata), HN 49953495, 142 pts / 54 comments, 2026-10-04.** Community
  thread on running Qwen3.8-Flash-Next (125B MoE) at consumer VRAM: OP reports 124 tok/s on 4090 +
  128GB DDR5; mkl quotes the README that the Coder variant "removes half the experts" and "reaches
  91% of the full model's SWE-bench Verified score" fitting in 32GB RAM; thread skepticism is
  substantive: these "100 tok/s" projects are ~2-bit quants with no accuracy numbers ("4 bit is the
  floor"), and nsagent cites quantization-degradation literature (4-bit preserves, 2-bit damages).
  merbanan's own numbers: Q2_0 33 tok/s decode / ~600 t/s prefill at 128K on an RTX 2060 8GB;
  IQ3_XXS ~21 tok/s / ~240 t/s. Arctic-Shift archive adds today's r/LocalLLaMA PSA: Strata's
  calibrate step "nearly tripled my decode speed (IQ3_S at 256K, 16 GB card)". Estate read: the
  Flash-Next MoE at IQ3-class quants is the first candidate in this window plausibly above the
  janitor tier for short-worker tasks, but every accuracy number is self-reported and the thread
  itself supplies the teardown pattern; per laws.md the cell fills only from estate instruments.
- **Gemma 4 megakernel (withhopper.com/blog/gemma-tpu-megakernel, HN 49897153, 09-29).** Article
  read this session: Gemma 4 26B-A4B MoE (4B active, 128 experts) at 640 tok/s on TPU v5e-8 BF16 =
  3.7x vLLM 0.30 on one H100 (173 tok/s); single kernel vs 1,494 GPU kernels/token, 77% vs 21% of
  speed of light; gains shrink to 1.6x at batch 8; INT8 experts reach 760 tok/s; dense Gemma 4 31B
  95 vs 38 tok/s. The janitor-relevant fact is the SHAPE, not the TPU: a 26B-A4B Gemma runs 4B-active
  decode, janitor-class compute carrying 26B knowledge; the same MoE-at-low-active-params shape is
  what Strata exploits for Flash-Next on one GPU.
- Qwen 3.8 Omni Flash (49747925) was CONFIRMED already by the 10-02 x sibling
  (frontier_olm_2026-10-02/sweep/open-and-local-language-models-x.md: full thread walked, open-weights
  slowdown quote banked). My read adds pricing/per-task numbers only: thread cites $0.15/$0.47 per
  M in/out vs Gemini 1.5/9.0, and ArtificialAnalysis per-task $2.31 (Astra xhigh, index 53) vs $5.41
  (Qwen3.8 Max, index 45) - recorded here as context on the banked find, NOT re-banked.
- Weave Router (49911500) is ALREADY BANKED by the 10-03 evals sibling; Swift-Qwen3.8-27B (49727511)
  is ALREADY BANKED by the same sibling (Base 66.74% vs Swift 65.84%, quant-overthink note). Both
  dropped from my items; re-banking is waste.

### RQ2 - UNMEASURED routing cells fillable from public evidence without spending

- The strongest public-evidence class this window is PROVIDER-VARIANCE measurement, not leaderboard
  copy: the 766-pt OpenRouter thread documents same-model-id quality spread (article's measurement:
  "Fireworks scored 46% on TAU, a 30 point gap" below first-party; unpinned requests get truncated
  responses still billed, over-quantized weights, provider rotation silently breaking prompt caching
  and "essentially destroy[ing] cost savings"; middleware-level failures: vLLM dropping reasoning
  for GLM models, sglang dropping array args for DeepSeek; OpenRouter COO: "We are doing continuous
  benchmarking of each endpoint, for each provider"). Estate mapping: this is RIB_ROUTING_CLASSES'
  transport-is-not-quality law observed at industry scale; it says family x capability cells are
  FILLABLE from public per-provider telemetry (OpenRouter model pages expose per-provider throughput,
  latency, tool-call error rates, cache-adjusted pricing, 7-day uptime per lelandbatey), but quality
  cells (blind-grade pass) still require estate instruments - public evidence narrows, never fills.
- Fillable without spend: cost-per-task ratios (ArtificialAnalysis: Qwen3.8 Max $5.41/index 45 vs
  Astra $2.31/index 53), latency distributions (latencyradar.com daily DeepSeek-vs-OpenRouter),
  roster/limit listings (OpenRouter limits doc below, NIM 81 models already banked today).
  Genuinely requiring a live probe: any WIN/CHAMPION routing cell (blind-grade gate) and all local
  janitor cells (estate hardware only).

### RQ3 - the pending qwen A/B probe (burns.md probe 5)

Exact open comparison, from burns.md section 3 (DIGEST.md:267-274 via the 10-03 fold): probe 5 is
**qwen2.5:7b Q4_K_M vs q8_0** on the estate's own stack, re-owed UNRUN. New public evidence this
window does NOT resolve it: Algolia "qwen 2.5 quantization" in-window returns 0 hits; the nearest
public priors are already banked (r21 GGUF-metadata throughput prediction: Q4 1.29-1.49x vs Q8,
IQ2-vs-Q2 ordering flips by vendor; r22 quesma Qwen3.8-27B quant bench: Q4_K_M matches BF16 on
agentic work - a DIFFERENT model at 27B). This thread's Omni-Flash comment adds the qualitative
prior that bad quants cause overlong CoT. Under the instruments-only law (RIB_MODEL_GARDEN_ROUTING:
47-53, hand-copying a vendor number into an empty cell is fabrication), the A/B stays a live probe;
public evidence only sharpens the prior that Q4_K_M should hold and q8_0 buys accuracy only where
7B is marginal. The probe remains owed; firing it beats more mining of its subject.

### RQ4 - free-lane forcing contradiction (grid line 192): published data class

Primary doc fetched this session: openrouter.ai/docs/api-reference/limits. Published free-tier
numbers: 20 requests/minute for ALL accounts; 50 requests/day under 10 lifetime credits, 1,000/day
at >= 10 lifetime credits (granted one credit early, at 9); the tier is selected by all-time credits
purchased independent of is_free_tier; limits are GLOBAL per account (multiple keys do not raise
them); excess returns HTTP 429 with X-RateLimit-* headers; and the decisive instrument:
GET /api/v1/key returns data.free_model_daily_requests.{used,limit,remaining}. No token ceilings are
published (request-count only). Estate read: the contradiction (RIB_FREE_USAGE_POLICY "forcing free
lanes throttles them into empty 429s" vs the 09-30 census's 459 rows / zero 429s / 69h+ forced
mining) is resolvable to measured law at ZERO cost: poll data.free_model_daily_requests on the
estate's OpenRouter key during a forced window and log used/limit/remaining next to each banked row;
429-vs-remaining telemetry converts operator mood into a fillable grid cell. Note burns.md probe 3
recorded "both hot free doors expose zero rate-limit headers" - OpenRouter's doc says 429 responses
CARRY X-RateLimit-* headers; whether the estate's hot doors are OpenRouter-fronted is checkable with
one forced 429. Combined with the already-banked Groq (org-level stacked RPM/RPD/TPM/TPD) and Gemini
(RPM + input-TPM + RPD, midnight-Pacific reset) docs (10-03 register r16/r17), the published
data class is sufficient; what was missing is the estate-side logger, which is the actionable fold.

### RQ5 - Reddit door recipe (stop LocalLLaMA being an OWED door)

Three facts this session: (1) arctic-shift.photon-reddit.com API re-certified WORKING by my own
probe today (valid JSON, full post objects) - matching the 10-03 certification; (2) HN 49913588
(62 pts, 09-30, arstechnica): Reddit is restricting old.reddit.com to accounts active in 6 months,
login redirects fail intermittently, and per ChrisArchitect's comment Reddit announced RSS support
ends "on November 13, 2026" - which puts a PUBLISHED DEATH DATE on the 10-03 DIGEST's banked "thread
permalinks via .rss endpoints" variant; (3) my subreddit-level .rss probe returned the HTML shell
today. Durable recipe for doors.md: Arctic Shift archive API as the engine (search + full objects),
HN Algolia paging + arXiv sweeps as the substitute when the archive lags, and treat every
reddit.com direct path (json, www, RSS, pullpush, jina, redlib) as condemned infrastructure with a
2026-11-13 expiry on the RSS residual. OWED from this seat: one thread-permalink .rss probe before
11-13 to timestamp when the banked variant actually dies.

## Anti-rebank ledger (overlap checks run this session)

Already banked, do not re-bank: Qwen 3.8 Omni Flash thread (10-02 x sibling, CONFIRMATION with
76.8KB thread walked); Weave Router 49911500 + Swift-Qwen3.8-27B 49727511 (10-03 evals sibling,
items 4 and 6 with quotes); Aleph Alpha Kolibri (four 10-03 sweep files); StepFun Step 5 (r18);
quesma Qwen3.8-27B quant bench (r22); GGUF-metadata throughput prediction (r21); IQ3_XXS vs Bonsai
ternary (1wkorli); Groq + Gemini limit docs (r16/r17); Ollama 0.35 Jev support (09-30 sibling);
justine.lol/matmul (round 1, cert expired); SoTA Feed, DeepSeek Harness Desktop, Janus GGUF Vulkan
(10-02 quant census candidate list - Janus banked here only as a NEGATIVE: thread consensus is a
thin llama-server wrapper, no vllm/sglang benchmarks, and gunalx measured Vulkan vs SYCL "in the
same ballpark" on Intel; no adoption case for the AMD box). Catalog greps: "Strata" 6 hits all
unrelated estate files (FOUR_STRATA_SELF_STEAL, ATTIC_STRATA, STRATA_DROP DDR3); "Omni Flash",
"Weave Router", "mmoustafa", "megakernel", "JevBench", "Swift-Qwen3.8",
"free_model_daily_requests", "GGUF models via Vulkan" all 0 in catalog titles; prior-sweep overlap
was checked against the frontier_olm_2026-09-28..10-04 bank files directly (greps in-session).

## Honest limits

No funded probes, no local runs, no estate-instrument measurements were fired (none in scope for a
sensing seat). Quote fidelity is fetch-layer, not byte-level. The Strata accuracy claims and the
Gemma megakernel TPU numbers are vendor/author claims pending the funded-tier verification the
driving ladder requires before any lane promotion. The Reddit RSS end date is commenter-cited from
Reddit's announcement; the primary announcement page was not fetched. The memory-tree grep for
phrase census was cut for runtime (memory/ holds ~550k files) and replaced with bank-of-record
greps over the frontier_olm series plus catalog title greps; residual overlap risk is content-level
matches inside memory prose that no bank file indexes.
