# SWEEP: open-local-language-models via x - 2026-10-09

source-fetched: 2026-10-09

Area: open-local-language-models. Feeds the model garden lanes, the local Ollama janitor tier
(gemma:2b scut, gemma4 short worker), the model-grid census rib, and the T0/T1 local-first
consent boundary.

## Doors used and their condition

- Pass 1 broad sweep: 8 WebSearch passes with site:x.com queries (open-weights releases,
  Qwen small models, Gemma, ollama, Q4/Q8 quantization, GGUF, arXiv-adjacent, on-device,
  September releases, Qwen3.6). Two bursts hit provider-side 1302 rate limits; fixed by
  pacing (single-query batches) and interleaving local work, not by narrowing the sweep.
  Candidate pool: ~40 items surfaced, of which 19 fall inside the 2026-09-09..2026-10-09
  window; the rest (Qwen3.5 Small 03-02, Gemma 4 launch 04-02, Gemma 4 12B 06-03, Kimi K3
  quant 07-30, Q4-vs-Q5 08-15, draginol primer 08-17, Tiny Aya 02-18, Qwen3.6 family 04-x)
  were considered and rejected as out-of-window. Dates were derived from Twitter snowflake
  IDs (id >> 22 + 1288834974657, computed with .venv\Scripts\python.exe) and confirmed by
  the fxtwitter door on every deep read.
- Pass 2 deep reads: 10 posts fetched through the fxtwitter door
  (api.fxtwitter.com/<user>/status/<id>, JSON, no login). The door was HEALTHY on every
  call today - unlike 2026-10-07/10-08 when the hermes digest logged "fxtwitter timelines
  404 x2". No door fallback was needed for the seven banked items; where a post was
  link-only (akshay_pachaar, theneurondaily) the linked article body itself is NOT
  readable through the door, and those items are banked with their search-result snippets
  per the recipe fallback, flagged in their entries.
- One honest failure: the primary Saluki post by @underdogdotai could not be fetched
  because its status ID is unknown; a guessed ID 404'd. Saluki enters this sweep only via
  the TeksEdge secondary read below.

## Overlap method (run this session)

Exact-phrase greps over catalog/catalog.jsonl (1,343,390 lines) and the memory/ tree, plus
per-file term attribution:

- EmbeddingGemma: 1 catalog row = watch/inbox/gps_embed/GPS_EMBED_TRIAL.md (mtime
  2026-10-08, "EmbeddingGemma 2 x the verdict ledger (2026-10-06 lane)") + deep memory
  coverage (percolator/candidates.jsonl, runs/free_lane_fleet/ledger.jsonl 13 hits,
  runs/gps_embed/trial_results.json, trajectory/steps.jsonl 76 hits). ALREADY TRIALED BY
  THE ESTATE one day after release. The Pichai/DeepMind posts (2107501975671890211,
  2107502286758895878) were deep-read and then DROPPED as re-banking known work.
- Mistral Large 4 ("Le Chonk", 2107457414387622310, 2026-10-06): deep-read; DROPPED
  because memory/runs/x_reply_radar/out_2026-10-07.json already holds the announcement
  snippet ("Meet Mistral Large 4, aka Le Chonk. - 1T parameters, natively multimodal.
  49B active..."). One release-watch fact survives for the garden: open weights promised
  end of October (julien_c 2107463427216277644 confirms).
- Saluki / apex-flash / Rapid-MLX / Q4-KV: 0 catalog hits, 0 memory hits outside this
  session's own commands (trajectory/steps.jsonl records my in-session greps). GENUINELY NEW.
- Kolibri: catalog 0 hits; memory/runs/free_lane_fleet/ledger.jsonl already proposes a
  "Kolibri-1 GGUF pull" on the free API lanes - watched, not yet banked with benchmarks.
- Karpathy speculative-decoding article: catalog has 26 "speculative" rows (SpecQuant and
  FlexEE paper rows, a transformers-course spec-decoding main.py mtime 2026-10-04) - the
  practitioner article is new but adjacent.
- Janus: catalog's single "Janus" row is Janus-Pro (DeepSeek multimodal, unrelated name
  collision); 5 "Vulkan" rows incl an AMD Vulkan quant comparison; the Go server itself new.

## Findings against the four research questions

### RQ1 - releases since 2026-10-01 that justify touching the janitor tier

Three in-window items matter, and all three argue PER-CAPABILITY swap evidence, not a base
swap of gemma:2b/gemma4:

1. Saluki (underdogdotai, surfaced 2026-10-09 via TeksEdge): compressed Qwen3.8-27B as a
   7.89GB Apache 2.0 GGUF for stock llama.cpp. Developer-reported: tool-calling 88/120 vs
   84 for full precision; SWE-bench Verified 30/50 vs 33; math and reasoning show larger
   losses. If the numbers hold on our bench, the scut/short-worker lanes (tool-shaped
   work) are exactly where compression already wins.
2. FHILY's 38-model VRAM study (2026-09-13): on 16GB cards quantized Qwen3.8-27B variants
   score 90.8-92.7% at 10.1-12.8GB peak, beating Gemma 4 12B (87.6%) and gpt-oss-20b
   (87.4%) - a direct X-side data point that our short-worker family is already behind
   the 16GB-class frontier. The measurement recipe (16K prompt + 768 MiB headroom, peak
   VRAM per cell) is portable onto the model-grid census rib.
3. Cantina apex-flash-1 (2026-10-01): first open-weights security model post-trained on
   real paid vulnerabilities, plus an abliterated variant. A candidate for the security
   lane where T0/T1 consent law keeps work local - the model is a garden row candidate
   pending a size check (the post names no parameter count).

The commoditization backdrop: kimmonismus (2026-10-04) on Aleph Alpha Kolibri - 78B total /
3.46B active, Apache 2.0, AIME 96.9%, GPQA 84.3%, SWE-bench 66.4% behind Qwen3.6's 73.8% -
"It increasingly looks as though any 'moat' - especially with small models - is
evaporating". This matches the arXiv lane's RQ1 verdict this same sweep cycle
(open-local-language-models-arxiv.md): internalize scut into fine-tunes of the CURRENT
tier rather than swapping bases.

### RQ2 - does the qwen2.5:7b Q4-vs-q8 TIE AT CEILING generalize?

The X door says: not globally. Two independent reads:
- FHILY: GPQA drops 49.0 (6-bit) to 45.0 (3-bit) - a 4-point capability-specific cliff
  while aggregate scores stay high; and "Q4 KV can cost roughly 17-29% of decode speed
  depending on the model" - the KV-cache axis is a separate, speed-shaped cost the tie
  never measured. Also the load-shape trap: a 15.9GB Q4_K_M file peaks at 17.3GB under
  16K context - "the difference between the model fitting and the workload fitting".
- Saluki: compression can BEAT full precision on tool-calling (88 vs 84) while losing on
  math/reasoning in the same model. The ceiling is per-capability and moves with
  compression axis (weights-only vs KV vs compression-training), corroborating the
  arXiv lane's four-paper verdict (domain/family/metric axes, 2609.18005 et al.).
  Family generalization stays UNMEASURED on X too - nobody posted a Gemma-4-family
  equivalent of the FHILY Qwen table this window; that cell needs our own A/B run.

### RQ3 - wire the arXiv door into model-garden intake

X-side evidence the trigger should ALSO watch X, not only arXiv: Saluki (a weights drop
with immediate GGUF availability) and apex-flash-1 (an open-weights release) were
announced on X first; neither has an arXiv paper. A release-watch intake that regexes
"open weights|GGUF|Apache 2.0|on-device" from a small X account list (Alibaba_Qwen,
GoogleAI, GoogleDeepMind, MistralAI, UnslothAI, cantinasecurity) would have caught both
in-window releases days earlier than sweep cadence. The fxtwitter door makes this a
no-login JSON pull - same one-hop shape as the arXiv trigger proposed by the arXiv lane.

### RQ4 - serving shelves vs fresh pulls

On X this window: Janus (MIT Go binary serving local GGUF via llama.cpp's Vulkan runner,
AMD/Intel/Nvidia - 2026-10-02) and Rapid-MLX 0.15.6 (point at any HF checkpoint, serve on
Mac, wire into Codex/Claude Code; "Typed, on-device decisions (routing, triage, scoring)
instead of generated chat" - 2026-10-05). Both are serving-layer, not model weights:
they belong on the serving shelf next to corpus/library/lmcache-src/ rather than the mine
shelf. The estate already holds Vulkan-side quant comparisons in catalog (5 rows) - the
Janus pull would extend the AMD cell specifically. Karpathy's speculative-decoding
article (2026-10-08) argues the small tier's next job: draft model for spec decode of the
specialist tier - article body unread through the door, OWED.

## The seven banked items (strongest first)

1. FHILY VRAM/quant study 2026-09-13 - x.com/Oluwaphilemon1/status/2099124227320266961
2. Saluki compressed Qwen3.8-27B 2026-10-09 - x.com/TeksEdge/status/2108348214764011947
3. apex-flash-1 2026-10-01 - x.com/cantinasecurity/status/2105803415012205023
4. Kolibri benchmarks 2026-10-04 - x.com/kimmonismus/status/2106669429320761788
5. Rapid-MLX 0.15.6 2026-10-05 - x.com/iotex_io/status/2107140322837078480
6. Karpathy spec-decode article 2026-10-08 - x.com/akshay_pachaar/status/2108252095380140203
7. Janus GGUF Go server 2026-10-02 - x.com/theneurondaily/status/2106029852042375577

## OWED / follow-ups

1. Saluki primary post (@underdogdotai) - resolve the real status ID and read it; the
   88/120 tool-calling claim is developer-reported via TeksEdge only.
2. apex-flash-1 parameter count + GGUF availability - the announcement names neither;
   garden-row decision blocked on it.
3. Karpathy article body (x.com/i/article/2108246386538094592) - door cannot read
   articles; needs the browser door or a second source.
4. Janus GitHub repo - locate and verify the MIT license + Vulkan runner claims from the
   snippet; the Neuron roundup body was not readable.
5. Release-watch: Mistral Large 4 open weights "end of October" (radar already holds the
   announcement; the garden wants the drop itself).
6. FHILY's measurement recipe (16K prompt + 768 MiB headroom, peak VRAM) as a candidate
   scorecard column for the UNMEASURED model-grid cells.
