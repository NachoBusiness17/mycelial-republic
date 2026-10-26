# Sweep: open-local-language-models via x (2026-10-07)

source-fetched: 2026-10-07. Seat: sweep-open-local-language-models-x (dwfrun child).
House laws held: ascii only, no em or en dashes, every claim cites what was read or
ran this sitting, OWED where unreachable.

## Door health (run this sitting)

- The WebFetch tool TIMED OUT on every target tried (4 fxtwitter API calls, 2 GitHub
  release pages; each died at the 60s wall). Fallback used throughout: `curl -s -m 30/40`
  from the repo shell against api.fxtwitter.com, api.github.com, ollama.com, and
  raw.githubusercontent.com. Every deep read below rode curl, not WebFetch.
- WebSearch hit backend 429/1302 errors on parallel calls (3 of 4 in batch 2 refused);
  single paced queries succeeded. X results came back but often with truncated URLs
  (bare "x.com"), so several candidates are snippet-only with no resolvable status ID.
- Status IDs that did resolve were snowflake-decoded with the repo venv
  ((id >> 22) + 1288834974657) before any date claim was made.

## Pass 1 census (43 candidates considered; dates decoded or page-stamped)

X posts (fxtwitter-resolved where an ID existed): ollama qwen3.5 9b/4b/2b/0.8b
(2026-03-02, resolved full); ollama qwen3.5 series (03-02); grok Qwen3.5-9B OpenClaw
(03-02); ollama qwen3.5-35B-A3B preview (03-31); Alibaba_Qwen 35B-A3B LM Studio
(02-25); Raullen local inference engine (03-20); stevibe ToolCall-15 (03-25,
resolved full); ilblackdragon harness-level routing (07-11, resolved full);
Av1dlive LLMRouterBench article (07-13, unresolved article link); pbakaus skill
engineering (07-14); hrswatigupta Jev article (09-23, resolved thin: link only);
MikeLongTerm AMD CTO (09-26); DailyDoseOfDS architectures (09-26); ViC305 LFM2.5-2.6B
(08-04, resolved full); jmorgan pacman-arena Tev1/Nimble/Laya test (09-07,
SNIPPET-ONLY, no status ID); GoSailGlobal OpenClaw dashboard (02-14); hooeem GLM 5.2
local guide (06-21); 0xSero Droid BYOK (06-03); KSimback cost routing (02-16).

Releases and pages (GitHub API / ollama.com, all read this sitting): Ollama v0.34.0
(09-05), v0.34.1 (09-14), v0.34.2 (09-15), v0.34.3 (09-19), v0.34.4 (09-23), v0.40.0
(09-25 per API published_at), v0.35.0 (09-28), v0.35.1 (09-29); llama.cpp b11469
through b11476 (all 2026-10-07); ollama.com/library?sort=newest scrape (30+ model
cards incl. clef 2d, clef-flash 2d, laya 6d, tev1 5d, nimble 5d, qwen3.6 6d, qwen3.8
1w, lfm2.5, embeddinggemma-2, granite4.2, ornith-1.5, nemotron-3.5-lightning,
laguna-s-2.1, kimi-k3); ollama blog decision-models post (09-29, full); Bespoke
nimble PUBLIC_BENCHMARKS.md (full sections); ToolCall-15 README (full); sotaaz
comparison (search snippet only).

## Pass 2 deep reads (all via curl, this sitting)

1. GitHub API ollama/ollama/releases, 8 bodies read (v0.34.0 through v0.40.0).
2. GitHub API ggml-org/llama.cpp/releases, 6 bodies read (b11469-b11476).
3. ollama.com/blog/ollama-now-supports-jev-style-decision-models, full text.
4. raw.githubusercontent.com/bespokelabsai/nimble/main/docs/PUBLIC_BENCHMARKS.md,
   methodology + full results tables (38,132 bytes total doc).
5. raw.githubusercontent.com/stevibe/ToolCall-15/main/README.md, full.
6. fxtwitter full JSON: ollama/status/2028514180936908842,
   stevibe/status/2036810936594612618, ilblackdragon/status/2075928575748837532,
   ViC305/status/2084676362863034454.

## Banked items (7, strongest first)

### 1. Bespoke nimble PUBLIC_BENCHMARKS.md: the per-dataset accuracy table the estate OWED

The 10-01 and 10-02 sweeps both recorded the OWED "13 datasets, 3,880 decisions, no
figures published" (watch/inbox/frontier_olm_2026-10-01/sweep/inference-efficiency-hn.md:24,
register row in frontier_olm_2026-10-02/register.jsonl:22). The figures ARE published,
in the repo doc the blog links, and I read them this sitting. The answer to RQ2's
shape: on the vendor's own suite, nimble-9b's best routing-shaped subset
(massive-en-US, n=350) reads 86.9 percent with 95 percent CI 82.9 to 90.0, so the
estate's 0.880 bar is STRADDLED, not cleared; jev-1.13.0 beats nimble on 8 of 13
subsets (civil_comments 81.0 vs 70.3, McNemar p 0.0000; paws 89.2 vs 82.8, p 0.0025;
boolq 89.7 vs 86.0, p 0.0708); rubric scoring collapses (helpsteer2 39.0 percent);
jev is better calibrated on 5 of the 6 subsets with ECE shown. Methodology rigor worth
stealing: label-blind seeded draws, checksummed subsets, "agreement with human
annotation, not truth" framing, and the poison-pill line that TypeSafe's own Jev
numbers ride a proprietary benchmark labeled by two frontier models. Corroborates the
sibling HN lane's JevBench read (Jev 86.6, Laya 58.4; 0.880 not cleared even by hosted
Jev). The rung stays UNSUPPORTED; estate instruments must still measure.

### 2. ToolCall-15 as a BenchLocal Bench Pack (stevibe, the estate-shaped instrument)

Previously seen only as an out-of-window Apr mention in the 10-02 quant sweep's
below-bank-line list (watch/inbox/frontier_olm_2026-10-02/sweep/quantization-compression-x.md:125).
Deep-read the current README: 5 categories x 3 scenarios (Tool Selection, Parameter
Precision, Multi-Step Chains, Restraint and Refusal, Error Recovery), 2/1/0 scoring,
temperature 0, mocked deterministic tool responses, raw traces stored per scenario for
audit, CLI runner plus BenchLocal desktop app, MIT licensed. This is the closest
public instrument to what the estate's mostly-UNMEASURED tool-calling cells need
(lens/laws.md:104; RIB_MODEL_GARDEN_ROUTING.md:47-53 instruments-only law): runnable
against any OpenAI-compatible endpoint including Ollama and llama.cpp. Adopt-shape:
run it against gemma:2b, gemma4, qwen2.5:7b, and qwen3.5:4b before any rung swap.

### 3. Ollama v0.34.3 thinking-controls advertisement (adoptable on the estate box NOW)

Release body read via GitHub API: "GET /api/show now advertises each model's thinking
controls and default", with `ollama show gemma4` returning levels false/true, default
true, and glm-5.3-flash returning values low/high/max, default max. The estate box
runs 0.34.3 (verified in frontier_olm_2026-10-01/steal/open-local-language-models via
x.md:31), so this needs no upgrade: the one-bug law (thinking omission is a MEASURED
ON state, RIB_INFERENCE_BUDGET_20261001.md:119-131) gains a queryable per-model
default instead of an assumption. Overlap: the sibling arxiv lane's Q3 answer
(frontier_olm_2026-10-07/sweep/open-local-language-models-arxiv.md:39) covers
v0.40.0/v0.35.1 and llama.cpp but NOT this feature; my greps found "api/show" only in
raw fetch JSONs, never in banked prose.

### 4. jmorgan pacman-arena: a third-party test of Tev1, Nimble, Laya (Sep 7, snippet-only)

X snippet via WebSearch: "Tested Tev1, Nimble and Laya on my pacman-arena game setup:
code ... Ollama now supports Jev-like decision models all locally." The estate banked
the VENDOR's Pac-Man demo (91ms, M5 Max, frontier_olm_2026-10-02/register.jsonl:22);
this is a different, independent practitioner running the trio on his own game harness.
SNIPPET-TIER: the search result gave no status ID and the profile URL would not
resolve, so the recipe's fallback applies (banked with URL = the search result's
truncated x.com). The raw pacman HTML in 10-06/10-07 _raw bing fetches was never
banked as an item (greps of DIGEST/register empty).

### 5. LFM2.5-2.6B, post-trained inside real harnesses (Aug 4) + lfm2.5 8B-A1B in Ollama

ViC305 post read in full: dense hybrid 2.6B built as an on-device agent, "Post-trained
inside real harnesses people actually run, including Hermes (@NousResearch), OpenClaw,
and Pi", 34T pretrain, 128K context, day-one llama.cpp/MLX/vLLM/SGLang/ONNX. The Ollama
library card for lfm2.5 (read this sitting) says "LFM2.5-8B-A1B, an edge model built
for fast, reliable tool calling on consumer hardware". DATE CAVEAT: the 2.6B drop is
2026-08-04, OUTSIDE the 30-day window; the library card carries no visible date.
Overlaps: the 10-02 sweep banked only MLX-Serve's speed mention of LFM2.5
(frontier_olm_2026-10-02/sweep/open-and-local-language-models-x.md:60-64); the model
itself was never banked as a rung candidate. UNMEASURED on the estate box; a worker
rung candidate for the 0.5B-8B band per RQ1, cells stay empty until instruments run.

### 6. qwen3.5 small sizes as tool-calling rung candidates (March landing, estate never measured them as rungs)

Ollama's own post (read in full): "All models support native tool calling, thinking,
and multimodal capabilities in Ollama" for qwen3.5 9b/4b/2b/0.8b. The estate verified
Qwen3.5-4B GGUF exists (frontier_olm_2026-10-01/DIGEST.md:41, abliterate lane) and
holds an April quants comparison (DIGEST.md:70, pre-window), but no banked row ever
measured qwen3.5:4b or 0.8b as a TOOL-CALLING rung against qwen2.5:7b or gemma:2b.
With ToolCall-15 (item 2) the A/B is one pull away. UNMEASURED stands.

### 7. SOTAAZ pre-registered label-bias rerun on laya 0.3.7 (published TODAY)

Reached by following the sotaaz domain from a search snippet; the article the snippet
described (Nimble 95.6 percent TREC numbers) was NOT the page I found, so those
numbers stay OWED below. What I did find and read
(https://sotaaz.com/post/decision-model-label-bias-en, datePublished
2026-10-07T08:34:21Z): a pre-registered rerun of arXiv 2610.02586 on two laya 0.3.7
checkpoints with the authors' own TREC and AG News sets. Verbatim: "Changing one line
of prompt rendering made predictions identical whatever the labels were called. When
labels contradicted the definitions, laya's TREC accuracy fell from 88.6% to 22.2%".
Load-bearing for RQ2: laya is the exact 421M rung in the estate's held decision
ladder, and this adds a failure axis the 0.880 accuracy gate does not cover
(label-vs-definition sensitivity), plus a one-line prompt-rendering mitigation worth
folding into the estate bake-off. Overlap: grep for 2610.02586 and "labels override
definitions" over frontier_olm_2026-10-0* and state/arxiv returned zero hits;
"label bias" appears only in raw fetch JSONs and session logs, never banked prose.

## Same-day sibling overlap (do not re-bank)

The arxiv lane (frontier_olm_2026-10-07/sweep/open-local-language-models-arxiv.md:39)
banked TODAY: llama.cpp b11474 GLM5Next MTP speculative decoding, b11472 temp-zero
greedy selection, b11475 Metal probability-collapse fix for Clef on /v1/systemone
(billing 0.28 Metal vs 0.977 CPU), and "no Ollama release after 10-01". I fetched and
read the same release bodies independently; my numbers agree; I am NOT re-banking them
as items. The HN lane (open-local-language-models-hn.md) banked Strands Decider 2B,
Jeff-Code 0.8B gating, the synthpop 575,442-call calibration audit, Strata MoE
throughput, and localjev DiffusionGemma. My earlier sweeps (10-01/10-02/10-05) hold
the nimble/tev1/laya/kev/Clef decision-model landing, the 91ms conditions, and the
latency ladder; none of that is re-banked here.

## Per-question verdicts

- Q1: NO in-window instrument-measured beat of gemma:2b / gemma4 / qwen2.5:7b surfaced
  through the X door. Candidates that exist one pull away: qwen3.5 4b/2b/0.8b (item 6,
  March), lfm2.5 8B-A1B (item 5), qwen3.6 (library card 6 days old, "thinking
  preservation", but only 27b/35b sizes visible on the page I read, outside the band).
  UNMEASURED is the legal state of every cell (lens/laws.md:48).
- Q2: rung stays UNSUPPORTED, now on three independent legs: the vendor's own suite
  straddles 0.880 at routing shape (item 1); JevBench (sibling HN lane) shows even
  hosted Jev at 86.6; and the new label-bias axis (item 7) shows a 421M decision
  model can fall from 88.6 to 22.2 percent when labels contradict definitions, a
  failure the accuracy gate alone does not screen. The estate's planned three-arm
  bake-off (rule floor, gemma:2b, tev1:0.8b; 50 items,
  frontier_olm_2026-10-01/steal/open-local-language-models via x.md:79-83) remains
  the only path to a filled cell; the meter n=0 problem (DIGEST.md:11) is unchanged.
  The estate-held reddit raw (arctic_LocalLLaMA.json:11669, read this sitting as
  overlap context) already carries a practitioner bake-off with the same shape: Jev
  hosted 78.9 to 81.3 percent on commit-type/file-routing tasks, a stock Qwen3.5-4B
  reading option logits beating a purpose-trained 395M ModernBERT, and confidence
  gates that do not transfer between tasks or models.
- Q3: nothing NEW since 2026-10-01 in Ollama beyond the sibling-banked v0.35.1/v0.40.0
  set; llama.cpp same-day items are sibling-banked. My unique add is v0.34.3's
  thinking-controls advertisement (item 3), which predates 10-01 but was never banked
  and is adoptable on the current box.
- Q4: the X door surfaced no new non-standard lineage with runtime evidence this
  window (Nemotron-Labs-TwoTower and Inkling appeared as name-drops only, no resolvable
  posts; both stay leads). ALoDLM and QUEEN remain held (lens/burns.md:119-122).
- Q5: no new frontier_thinking shelf candidate cleared the bank line from this door;
  the strongest instrument-shaped steal this sweep produced is ToolCall-15 (item 2),
  which belongs in the estate's instrument drawer rather than the paper shelf.

## Not run / OWED (do not assert)

- Bespoke suite: tev1 rows NOT in the doc I read (only nimble-9b and jev-1.13.0
  tables); tev1:0.8b public per-dataset numbers are OWED.
- The sotaaz comparison with "Nimble 95.6 percent TREC vs Jev 89.0, and 76.0 vs 85.7
  on a 4,599-question reasoning-heavy benchmark": search-snippet only, the article
  URL was never returned and the sotaaz post pages I could reach do not carry those
  numbers. OWED: find and read the actual article before citing any of its figures.
- jmorgan pacman-arena: status ID unknown, post not resolved. Av1dlive LLMRouterBench
  article: link unresolved.
- No estate-box measurements were run this sitting (no ollama commands, no
  ToolCall-15 execution); every cell verdict above is UNMEASURED by estate instruments.
- Licenses: nimble/tev1 license terms still unread (carried OWED from the 10-01 steal,
  line 88); Clef Apache 2.0 is held via the 10-02 finetuning sweep.

## Receipt

Commands run this sitting: curl against api.fxtwitter.com (5 posts, 4 resolved full, 1
thin), api.github.com (2 release lists, 14 bodies), ollama.com (blog index, 2 posts,
library index, 4 model pages), raw.githubusercontent.com (2 files); WebSearch (9
queries, 4 with usable X results, several 429-refused and rerun paced); snowflake
decode via ./.venv/Scripts/python.exe; overlap greps over catalog/catalog.jsonl
(combined single-pass: 120 raw hits, 2 non-session paths, both already-known),
watch/inbox/frontier_olm_2026-10-0*/, and memory/ (per-term). Files read this sitting:
the three 10-07 lens files (burns 234 lines, laws 125 lines, corpus 48 lines), the
sibling arxiv and HN sweep files, and the 10-01/10-02/10-05 overlap sites quoted above.
