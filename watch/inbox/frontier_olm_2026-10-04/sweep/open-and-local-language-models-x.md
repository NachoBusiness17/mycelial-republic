# SWEEP: open-and-local-language-models via x (frontier_olm 2026-10-04)

source-fetched: 2026-10-04. Seat: sweep-open-and-local-language-models-x. Doors used: WebSearch with
quoted-"x.com" queries (the site:x.com filter was NOT honored by the backend) + fxtwitter resolution
(api.fxtwitter.com, 3/3 JSON 200s) + primary pages behind the posts (ollama.com library, GitHub issue,
GitHub issue-search listing, daymora.com). No funded credits spent. No tests run; none asked.

Dedup base read BEFORE banking anything: the three sibling banks of this same carrier
(open-and-local-language-models-hn.md, -reddit.md, both fetched+read this session), the 10-03 X
morning bank + round2 bank (read in full), the 10-03 lens files (doors.md, laws.md, burns.md,
corpus.md), and the 10-02 X sibling's banked-item lines. Path note: this is the third X-lane file in
the series (10-03 morning + round2 + this one); the ask's named path was free today so no
amend-not-rewrite deviation was needed.

## Door health (honest, this session)

- **site:x.com is dead as a filter:** the z.ai web_search_prime backend ignored it on every query and
  returned open-web domains. Two of the first four batched queries failed mid-batch with the exact
  storm the burns ledger already documented: `MCP error -429: {"error":{"code":"1302","message":"Rate
  limit reached for requests"}}` (raw text captured from two tool results this session). Pacing to
  2-3 queries per batch stopped the 1302s.
- **The quoted-query workaround WORKED:** phrasing queries as `"x.com" <topic>` surfaced six real
  status URLs this session (Alibaba_Qwen x3, ItsmeAjayKV x1, ollama x2) where `site:x.com` surfaced
  zero. This is the new X-discovery recipe for doors.md; profile-level results (x.com/UnslothAI,
  x.com/ollama) surface post TEXT but no status IDs, so they stay snippet-grade.
- **Snowflake dating instrument (run this session, repo venv):** `ts = (id >> 22) + 1288834974657`
  dated all six IDs without trusting snippet dates: 2101659302792679789 = 2026-09-20T13:06:39Z;
  2102608867998007586 = 2026-09-23T03:59:53Z; 2094968708288680276 = 2026-09-02T02:00:37Z;
  2100785962414702599 = 2026-09-18T03:16:18Z; 2038835449012351197 = 2026-03-31 (out);
  2055100589428658462 = 2026-05-15 (out). Command: `./.venv/Scripts/python.exe -c` with the dict of
  ids, output shown in-session. Every candidate's window membership below rests on this, not on
  search-engine date strings.
- **fxtwitter resolved 3/3** (Max-0902, Apsara breakdown, Qwen-Image-2.1): full JSON with verbatim
  text, author, created_at, engagement, media, and links. First X-lane seat in the series to land
  in-window resolutions since the 10-03 morning run's StepFun/kaarelkaarelson pair.

## Pass 1 census (34 candidates considered, window 2026-09-04..2026-10-04 unless noted)

X/status candidates: Alibaba_Qwen/status/2094968708288680276 Qwen3.8-Max-0902 (Sep 2, 2d pre-window);
ItsmeAjayKV/status/2102608867998007586 Apsara breakdown (Sep 23); Alibaba_Qwen/status/2101659302792679789
Qwen-Image-2.1 (Sep 20); Alibaba_Qwen/status/2100785962414702599 Omni Flash (Sep 18, ALREADY BANKED by
the 10-02 X sibling - dropped); ollama profile snippet "Download or update to Ollama 0.34... 1.3 is
rolling out today with frontier performance. Ollama now supports the DeepSeek Harness." (no id,
snippet-grade, upstream releases already banked by the 10-03 round2); x.com/DeepSeek "V4 Preview is
officially live and open-sourced" (undated snippet, V4-1 Flash already banked today by the reddit
sibling); UnslothAI profile snippets (Qwen3.8-27B in Unsloth Desktop + Gemma 4 QAT highlight, no ids,
QAT wave is the 04-29..06-05 banked context).

Open-web candidates screened: FunctionGemma 270M in the Ollama library; HF
blazejewicz/functiongemma-270m-it-gemma-teacher (~Sep 28); thenextlevelsoftware September 2026 roundup;
i10x.ai flash-tier roundup (GLM-5.3-Flash, DeepSeek V4.1 Flash - both already held); daymora.com rate
limits (negative, see item 6); coddykit 34-free-providers (Aug, borderline out); neura.market/bazaarlink/
f22labs/riera/aiven free-tier pages (out-of-window or snippet-grade, none fetched); Meta Muse Glimmer
30B (Aug 13, out of window); Muse Spark (Apr, out); Meta early-access program + AI Watchdog spending
agents (Sep, app-domain); Thinking Machines Inkling + Inkling-Small (Jul 15/30, out of window);
Qwen3.5 flagship (Feb/Mar, out); Qwen team departures (Mar, out); Qwen3.8-Max "what actually shipped"
(Aug 5, out); Gigazine Qwen3.8-27B (Aug 15, out); unsloth/Qwen3.8-27B-NVFP4 (Aug 19, out); smtek
GGUF mirror (Aug 21, out); YottaLabs Qwen-4 prep (rumor); xhinker Medium Qwen-Image-2.1 (Sep 22);
thursdai.news Qwen X tracker; Unsloth Dynamic 3.0 doc + HF; bartowski quantization guide; qwen
readthedocs quantized performance; greaterwrong + dataaspirant quant explainers (2024-era priors);
GitHub issue-search listing for gemma-4-26B-A4B-it-qat-UD-Q4_K_XL (50 hits across 5 pages; first page
read); llama.cpp issues #29455, #27505, #23737; koboldcpp #2493; unsloth #10656; vastai-exp #17;
rs-gallium #92; lmstudio #2153; strix-halo-guide #4; gemma4-ai.com / webscraft.org / TechEnclave SEO
pages (unfetched, snippet-grade only); remio.ai Ollama 0.32.4; releasebot.io; whichdevtool/memetik/
lmspeed/swarmlabs Groq pages (echo the already-banked Groq table, deduped).

## Pass 2 deep reads (6 fetched and read end to end this session; minimum was 5)

(1) api.fxtwitter.com/Alibaba_Qwen/status/2094968708288680276 - full JSON read; (2)
api.fxtwitter.com/ItsmeAjayKV/status/2102608867998007586 - full JSON read; (3)
api.fxtwitter.com/Alibaba_Qwen/status/2101659302792679789 - full JSON read; (4)
ollama.com/library/functiongemma - page read (description, tags, sizes, benchmarks, dates); (5)
github.com/ggml-org/llama.cpp/issues/29455 - issue read (bug, culprit PR, bisect method, status,
dates); (6) github.com/search?q=gemma-4-26B-A4B-it-qat-UD-Q4_K_XL&type=issues - first-page listing
read (10 issue rows) + daymora.com root read (negative). Quote caveat: everything passed the
WebFetch/fxtwitter extraction layer; the three fxtwitter JSONs are the structured cross-checks; no
byte-level capture was retained.

## The 6 banked items (strongest first)

1. **Qwen3.8-Max-0902 refresh announcement - a family event on the funded workhorse tier**
   (x.com/Alibaba_Qwen/status/2094968708288680276, created 2026-09-02T02:00:37Z by snowflake + tweet
   created_at, resolved via fxtwitter this session; 6,011 likes, 1,192,816 views). Verbatim:
   "Qwen3.8-Max just got upgraded. Meet Qwen3.8-Max-0902! 2.4T parameters. 1M context tokens." and
   "Pricing per 1M tokens: $2 input, $6 output. $0.17 explicit cache hit, $0.25 implicit cache hit."
   DATE CAVEAT: 2 days before the ask's 30-day window; carried because the routing consequence is
   in-window live: per the verdicts-expire law (RIB_MODEL_GARDEN_ROUTING.md:54-57, a family event =
   fingerprint/carrier/pricing change), every qwen3.8-max routing row that predates 09-02 is STALE
   until re-measured, and the estate's funded qwen3.8-max-prime lane sits exactly on this family.
   The published cache-hit pricing ($0.17/$0.25) is the cost-prior class the HN sibling named as
   fillable-without-spend; under the instruments-only law (RIB_MODEL_GARDEN_ROUTING.md:47-53) it
   feeds priors and spend planning, it does NOT fill a grid cell. Overlap: catalog grep
   "Qwen3.8-Max-0902" = 0; rg over memory/ + all frontier_olm_2026-10-0* banks = 0 for the exact
   name; nearest holding is the 10-03 round2's Qwen author-listing line "2.4T-A95B (08-08)" (the
   weights artifact, not this API refresh); no bank names the -0902 snapshot or its pricing.
2. **Apsara roadmap breakdown: Qwen4 in training, Qwen4.5/Qwen5 projected 5-10T params, Qwen3.8-Max
   self-trained 33 cycles for AA 40 to 45** (x.com/ItsmeAjayKV/status/2102608867998007586, created
   2026-09-23T03:59:53Z, resolved via fxtwitter this session; 75 likes, 8,393 views - a fan
   breakdown, treat as secondhand). Verbatim: "Qwen is improving through automated self-training.
   Alibaba says Qwen3.8-Max completed 33 iterative training cycles, raising its Artificial Analysis
   score from 40 to 45." Plus: "Qwen 4, is currently in training" and a roadmap "projected to scale
   up to 5 to 10 trillion parameters." CONFIRMATION + DELTA over the reddit sibling's banked
   1wmxfjs (Qwen-4-at-Apsara announcement whose thread carried zero specs): the roadmap tiers and
   the self-training cadence are the new content, and the cadence is the point for the estate -
   the qwen family is now on a continuous self-training refresh loop, which shortens the effective
   expiry horizon on every qwen routing row. RQ3 consequence: NONE of this touches the pending
   local qwen2.5:7b Q4_K_M-vs-q8_0 A/B (burns.md probe 5; DIGEST.md:267-274) - that target is a
   frozen 2024-2025 artifact, the motion is all in the max tier; the probe stays owed and firing it
   still beats mining its subject. Overlap: "Apsara" catalog = 0 (re-run); the announcement itself
   is the reddit sibling's item 6 today; LiveTranslate (mentioned in this post) is ALREADY
   estate-verified at memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md (catalog
   row 91d9d6680c09) - only the roadmap + 33-cycle lines are new here.
3. **llama.cpp #29455: Vulkan DeviceLost on the janitor family's own 26B-A4B QAT quant on AMD
   iGPU - culprit PR #26081, bisect-confirmed, open** (github.com/ggml-org/llama.cpp/issues/29455,
   opened 2026-09-26 by Vincent-M, read end to end this session). The reporter runs
   unsloth/gemma-4-26B-A4B-it-qat-GGUF (UD-Q4_K_XL) on a Ryzen 7 5700G iGPU; llama-server aborts
   with `vk::DeviceLostError` ("vk::Queue::submit: ErrorDeviceLost") after "radv/amdgpu: Not enough
   memory for command submission"; a manual git bisect across ~1,100 revisions pinned first bad
   commit 153d324 = PR #26081 ("llama: add default load-mode auto, which avoids mmap on iGPUs",
   dated 2026-08-11); b3df572 (parent) works; verbatim workaround: "Workaround confirmed via
   --load-mode mmap flag." Status: open, bug-unconfirmed, unassigned. Estate read: this is the
   upstream hazard class behind the 10-03 round2's measured Ollama-hold fold - any estate/consumer AMD Vulkan host that crosses PR #26081 with a 26B-A4B QAT quant can lose model load at startup;
   the flag is the cure. Same GitHub listing read this session puts the consumer-VRAM footprint of
   this exact artifact at 14.25 GB (vastai-exp #17, Aug 30, named "the primary choice" for a zh-TW
   nursing-handover project) and 14.3 GB with 22 GPU layers tolerated on a "12GB RTX 4070"
   (rs-gallium #92, Aug 11), plus a second fresh serving bug: #27505 "server: deadlock under
   sustained chat workload on Gemma 4 26B-A4B + Vulkan" (Aug 21). RQ1 consequence: the janitor
   family's own 26B MoE needs a ~14-15 GB budget - it fits 16 GB-class consumer machines, NOT the
   estate's 6 GB RX 5600 XT box (where the 10-03 round2 already measured gemma-4-E4B-it-qat-q4_0
   at 5.15 GB as the real successor). Overlap: catalog greps "load-mode mmap" 0, "DeviceLostError"
   0, "29455" 0 in sibling banks; the 10-03 round2's Ollama regression is a DIFFERENT failure
   (GPU-discovery watchdog inside the 0.35 runner, measured on a dGPU host), not this upstream
   Vulkan load bug; today's HN sibling's Janus-Vulkan and megakernel items are unrelated.
4. **Qwen-Image-2.1: the X primary for a candidate the banks listed but never read**
   (x.com/Alibaba_Qwen/status/2101659302792679789, created 2026-09-20T13:06:39Z, resolved via
   fxtwitter this session; 8,267 likes, 2,294,534 views). Verbatim: "Meet Qwen-Image-2.1, the most
   balanced and cost-effective image generation model in the Qwen-Image series! Now open weights!"
   Post body: 7B lightweight architecture, native RGBA layer generation/editing, up to 10 reference
   images, panoramas/infographics/try-ons; links to qwen.ai blog, github.com/QwenLM/Qwen-Image-2.1,
   HF and ModelScope repos. Overlap DECLARED: listed-not-banked three times before this read
   (10-03 round2 Qwen author listing "Qwen-Image-2.1 (09-14/09-20)"; 10-03 morning X census line;
   10-04 HN sibling candidate list via HN 49930291 "ImageGen Qwen-Image 2.1 Mac"); this seat's
   delta is the resolved primary + verbatim + official repo set. Estate rank: LOW for the routing
   organs - image-domain, not a scut/short-worker language candidate - but it is an in-window
   Apache-family open-weights 7B with 2.29M views, relevant if any estate lane ever needs local
   image generation.
5. **FunctionGemma 270M: honest window-fail for RQ1, with the library numbers nobody banked**
   (ollama.com/library/functiongemma, read this session). Verbatim: "a lightweight, open model from
   Google, built as a foundation for creating your own specialized function calling models" and
   "not intended for use as a direct dialogue model." Numbers read off the page: 270M params,
   single 301 MB tag, 32K context, 195.8K pulls, BFCL Simple 61.6 / Irrelevance 73.7, requires
   Ollama v0.13.5+, and LAST UPDATED 9 MONTHS AGO - it FAILS the ask's "released or materially
   updated in the last 30 days" clause, so it is banked as a negative, not an RQ1 hit. The recency
   illusion is the finding: a cloudron forum snippet presented FunctionGemma availability as a
   "recent update"; the library page dates it to ~Jan 2026. Estate value that survives: a 301 MB
   function-calling specialist that scores 61.6 BFCL-Simple is the shape of a scut-lane router
   sitting BELOW gemma:2b in the fleet (1/7 the VRAM), worth one estate bench IF the window clause
   is ever relaxed for the scut slot; per laws.md that decision is the operator's, not this seat's.
   Overlap: catalog "FunctionGemma" = 2 rows, both mirrors of the held arXiv 2609.25373 full text
   "Extending FunctionGemma for Practical On-Device Mobile Function Calling" (09-28 sweep raw);
   the ollama library page itself was never read by the estate before today.
6. **NEGATIVE for RQ4: the search layer's "AI API Rate Limits Explained (Sep 2026)" article does
   not exist - daymora.com is a flat-rate vendor landing page** (daymora.com, fetched this session;
   search snippet had framed it as a September 2026 explainer with RPM/TPM content). Page read:
   zero published RPM/RPD/TPM/TPD numbers, no reset windows, no provider free-tier table; the only
   free offering is Daymora's own "50 free demo requests to validate quality"; the only token talk
   is billing ("Pay per token (input + output)" vs their flat $25/month); no article date, just
   "(c) 2026 Daymora". Verdict: the published-data class for the grid-192 free-lane contradiction
   is UNCHANGED by the X door - it remains exactly what today's reddit sibling and the 10-03
   register rows banked (OpenRouter 20 RPM / 50-1000 RPD / key counter, Groq per-model
   RPM/RPD/TPM/TPD, Google dashboard-gated). The Groq-number echoes this seat's searches returned
   (30 RPM / 1K RPD / 8K TPM / 200K TPD) dedupe to those held rows, not new evidence. Caution
   banked for every future seat: a search-result "article" with a date is not a source until
   fetched; the search layer fabricates framing, the fetch layer does not.

## Answers to the ask's research questions (this door's slice)

- **RQ1 (in-window open weights vs the janitor fleet):** this seat READ no in-window open-weight
  language model that beats gemma:2b/gemma4 at comparable consumer VRAM. The window's movements
  found via X are: a 2.4T API refresh (item 1), roadmap promises (item 2), a 7B image model
  (item 4), and a window-fail 270M router (item 5). The janitor family's own scaling path
  (26B-A4B QAT at ~14-15 GB, item 3) fits 16 GB-class consumer machines, not the estate's 6 GB
  box; the 6 GB-class measured successor remains the 10-03 round2's gemma-4-E4B QAT q4_0. The
  un-read SEO bench pages (gemma4-ai.com, webscraft.org, TechEnclave) are NOT evidence: snippet
  numbers only, pages never fetched, named here so nobody mistakes them for reads.
- **RQ2 (UNMEASURED cells from public evidence):** one new public cost datum (Max-0902 pricing,
  item 1) joins the fillable-prior class; nothing fills a cell - the instruments-only law stands.
  The routing action this door surfaces is not a new cell but a STALING: the -0902 snapshot plus
  the 33-cycle self-training cadence (item 2) put every pre-09-02 qwen row on notice.
- **RQ3 (qwen A/B):** unchanged and still owed. New public evidence is all max-tier (items 1-2);
  the A/B's qwen2.5:7b local target is untouched by it. bartowski's guide and qwen readthedocs
  surfaced as generic Q4_K_M/Q8 priors in search snippets - I did NOT fetch those pages, so they
  are named as leads, not evidence. Probe verdict: fire it; the only addition this window justifies
  is the reddit sibling's smoke-gate pre-step (2609.05881 broken-artifact check on both arms).
- **RQ4 (free-lane forcing vs pay-funded):** no new published numbers from the X door; one
  fabrication-shaped negative banked (item 6). The resolution instrument remains estate-side:
  poll GET /api/v1/key data.free_model_daily_requests during a forced window (reddit sibling's
  fold) - published bounds exist, the logger does not.
- **RQ5 (durable LocalLLaMA-class doors):** the X leg's recipe is now concrete and re-runnable:
  quoted-"x.com" queries (NOT site:x.com) at 2-3 queries per batch (4-wide batches triggered 1302s
  twice this session), snowflake-epoch dating of every surfaced ID
  (`(id >> 22) + 1288834974657`, run in the repo venv this session), then fxtwitter resolution
  (3/3 this session). The four-leg stack for LocalLLaMA-class intel is: HN Algolia paging + arXiv
  sortBy sweeps + Arctic Shift archive API (all proven by siblings) + this quoted-X recipe; the
  Reddit RSS residual carries a published 2026-11-13 death date (HN sibling, arstechnica thread).

## Honest limits

Quotes are fetch-layer renderings (fxtwitter JSON / WebFetch extraction), not byte-captured HTML;
the three fxtwitter responses are the structured cross-checks that ran. The GitHub cluster rows in
item 3 (#17, #92, #27505) are SEARCH-LISTING snippets; only #29455 was read end to end. Items 1-2
carry vendor/fan claims (2.4T params, 33 cycles, AA 40-45) that are unverifiable from this seat and
priced accordingly (confidence, not assertion). bartowski + qwen-readthedocs pages were NOT fetched.
The memory-side rg was scoped to memory/ + the frontier_olm_2026-10-0* banks with binary/type
exclusions - a full 550k-file census was not run (the 10-03 round2 hit the same wall). No funded
probes, no local benches, no estate instruments fired; none in scope for a sensing seat. No
em-dashes anywhere in this file; catalog-title em-dashes normalized per the 10-03 morning seat's
convention.
