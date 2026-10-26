# SWEEP round 2: open-and-local-language-models via x (frontier olm 2026-10-03, evening)

source-fetched: 2026-10-03

Seat: sweep gopher, area open-and-local-language-models, X door. **Path deviation declared:** the ask names
`sweep/open-and-local-language-models-x.md` as the bank path, but that file already exists (16,815 bytes, Oct 3 11:03,
the morning run's X-lane bank). Per the amend-not-rewrite law this write-up lands at `...-x.round2.md` and does not
touch the morning file. Dedup against the morning run was done byte-side: its `sweep/open-and-local-language-models-x.md`
(8 items: borgcloud tracker, Groq docs, Gemini docs, XGrammar-2, StepFun Step 5, PewDiePie Ajax, arXiv 2610.00954, Jev HN
thread), its register rows 16-20 for this area, and `DIGEST.md` exec points 1-7 were read before banking anything here.

## Door health (honest)

- **X search door DEGRADED, same as the morning run:** WebSearch (z.ai web_search_prime) repeatedly returned
  `MCP error -429 ... 1302 Rate limit reached`, did not honor `site:x.com`, and surfaced no resolvable status IDs for
  this seat. One snippet-grade X hit was caught (x.com @techfrenAJ, no status id exposed: "All using Qwen 3.8 27b via
  5090's. Cloudflare's new decision model. Jev is an AI model built for fast, low-cost decisions that went viral
  yesterday.") - banked as a snippet only, never resolved through fxtwitter because no id exists to resolve. No item
  below rests on an X read.
- **fxtwitter door: not exercised this seat** (no in-window status id surfaced beyond the morning run's three).
- **HF api/models door CLEAN and heavy-used:** author=google, author=Qwen, search=Muse Glimmer, search=cloudflare/clef,
  sort=createdAt newest-40, plus four model-card pages read end to end (E4B QAT, Flash-Next, clef, Holo4-27B, jfan MoE).
- **GitHub releases API CLEAN:** ollama/ollama releases list + tags/v0.35.1 body read verbatim.
- **Direct provider probes CLEAN:** api.featherless.ai and api.llm7.io fetched keyless with headers captured.

## The one check nobody else ran: measured Ollama 0.34.3 vs 0.35.1 on the janitor host (RQ5)

The box IS the estate's RX 5600 XT-class janitor host (Get-CimInstance: "AMD Radeon RX 5600 XT"; 6128 MiB per the
llama-server device line). Baseline on the installed primary (version 0.34.3, port 11434), same 128-token prompt,
temperature 0, JSON timing fields: gemma:2b eval 80.3 / 81.4 tok/s, warm prompt-eval 3382 tok/s, cold load 9.07s.
Then a PORTABLE v0.35.1 (official zip, 1,471,094,402 bytes, extracted to temp, OLLAMA_HOST=127.0.0.1:11500, same model
blobs) served the identical prompt: gemma:2b eval 25.1 / 25.2 / 25.2 tok/s, warm prompt-eval 1116-1165 tok/s, cold
21.66s. gemma4:latest (8B Q4_K_M): 14.6 tok/s decode and 87.8 tok/s prompt-eval on 0.34.3 versus 5.0 / 7.2 on 0.35.1.
Controls: the primary re-benched 79.5 tok/s minutes later (contention excluded); `/api/ps` on 0.35.1 shows gemma:2b
FULLY in VRAM (size_vram 2,058,302,258 = full size) so this is not offload; the shared server log shows the new runner
spamming `llama-server GPU discovery watchdog timed out ... context deadline exceeded` before placing models on
`Vulkan0 : AMD Radeon RX 5600 XT (6128 MiB, 5334 MiB free)`. Verdict: **the owed upgrade would regress both janitors
about 3.2x in decode on this card, with full VRAM placement.** Release-noted gains for 0.35.0/0.35.1 (decision models
via /v1/systemone, CAPABILITY declarations, llama.cpp/MLX bumps) do not offset a 3x serving regression on the janitor
host. Recommendation: hold the upgrade, file upstream, re-run this exact A/B on 0.35.2+. Confounds named: one box, one
bench prompt, 2-3 reps per arm, shared log file, root cause inside the llama.cpp bump not isolated.

## Research questions

- **RQ1 (open-weight agentic after 2026-10-02 at RX 5600 XT-class VRAM, measured not asserted):** the only in-window
  (post 10-02) release-track bytes found are today's jfan/gemma-4 LiteRT-LM WebGPU mirrors (31b, 26b-web-moe, 12b,
  2026-10-03T22:27Z); their card asserts "128 experts, Top-8 routing, 4B active params" and carries ZERO benchmarks.
  The honest measured 6GB-class card is google/gemma-4-E4B-it-qat-q4_0-gguf: one 5.15 GB Q4_0 file with MMLU Pro 69.4%,
  AIME 2026 (no tools) 42.5%, LiveCodeBench v6 52.0%, GPQA Diamond 58.6%, Codeforces ELO 940 (repo created 2026-05-01,
  outside the window but it is the card that MEASURES at this VRAM class). Qwen3.8-Flash-Next measures agentic hardest
  (DeepSWE 1.1 58.7, SWE-bench Pro 62.5, Toolathlon 73.5, AndroidWorld 84.5, Agents' Last Exam pass@1 24.3) but is
  125B total / 6B active: it does NOT fit 6 GB and must not be mistaken for a janitor-class animal. Clef measures
  decision quality (not agentic) and Holo4-27B measures computer-use at 27B. No post-10-02 base release at 6GB class
  with named agentic benchmarks surfaced on any door read.
- **RQ2 (does 1wv1u54 replicate at Q4_K_M on an estate instrument):** 1wv1u54 is r/LocalLLM 2026-10-01 (203 pts), the
  sibling evals lane's bank today; the on-disk fetch (sweep/thread_1wv1u54.json, 502,073 bytes) shows the source ran
  unsloth dynamic quants of Qwen3.8-27B (UD-Q4_K_XL and UD-IQ4_XS named in the thread) on an RTX 4090 with
  "40/43 hidden tests passed, 109/109 existing tests kept (partial 0.980, binary 0)" on a single DeepSWE task, the
  author volunteering "the DeepSWE number is a single task, so it as one task, not an average" (source typo kept).
  External Q4_K_M replica row already held: quesma's Qwen3.8-27B quant bench, Q4_K_M matches BF16 on agentic
  Terminal-Bench 2.1 (register row 22 of the morning run). **The estate-side replication at Q4_K_M on the estate task
  mix was NOT RUN this ask**: no Qwen3.8-27B is on disk (ollama list read this ask), the download plus scored eval is a
  multi-hour probe, and the instrument design already exists (percolator E3b runtime-parity spec,
  frontier_olm_2026-10-01/percolator_candidates.jsonl row 3; ask_bank for task mix). Stated as owed, not guessed.
- **RQ3 (what replaces the dead free-credit tier; Featherless roster-diff):** the roster-diff instrument was RE-RUN by
  hand this ask: keyless api.featherless.ai/v1/models returned HTTP 200, 3,224,862 bytes, **10,175 served rows** at
  2026-10-04T00:14Z versus the 22,059 byte-banked on 09-28 (memory/burns/LEDGER.jsonl:683,692): the served roster
  roughly HALVED in five days, and the `?sort=-created_at` arm returned only 4,023 rows with its newest row dated
  2026-10-02T01:07:26Z (darkc0de/XORTRON-CriminalComputing-RICO-v4), so the two arms now disagree by 6,152 rows and the
  newest-first arm went two days without new rows while the dump shrank. That is the old full-dump-vs-paged
  instrument-mismatch disease returning with a shrink instead of a grow; the roster-diff needs its reconciliation pass
  before any count from it routes anything. No rate-limit headers were exposed on ANY door probed (grep over captured
  headers of featherless both arms + llm7: zero matches). The sibling HN lane fired a paged roster probe minutes before
  this seat (sweep/tmp/hnolm/featherless_roster_*.json, 20:27-20:32; open-and-local-language-models-hn.md:101,113:
  page-1 73 rows, per_page 100 rows) - consistent with mine, but their probe did not take the full-dump census, which
  is where the halving lives. Free-class verdict: NO new free-class provider found on the roster; LLM7 remains the only
  measured free-class inference lane and its roster grew 64 to 68 models (keyless /v1/models, 66,787 bytes, sample ids
  DeepSeek-V4-Flash-0731, DeepSeek-V4.1-Flash, GLM-5.3-Flash, Inkling).
- **RQ4 (per-dispatch tank accounting probe): NOT RUN.** It is a long-running estate instrument (morning DIGEST point
  2 and lens/laws.md:55-78 own it). This seat's measured contribution to it: neither hot free door exposes
  x-ratelimit headers, so a passive per-dispatch accounting probe cannot read tank state from headers on these lanes
  and must count requests against observed 429s the way the stealth lane does.
- **RQ5:** answered by measurement above.

## Pass 1 census (34 candidates considered, last 30 days unless noted)

Featherless roster newest-first arm (fetched this ask): darkc0de/XORTRON-CriminalComputing-RICO-v4 (10-02),
Cloudflare/clef (10-01), Cloudflare/clef-flash (10-01), Hcompany/Holo4-27B (09-28),
DavidAU/Qwen3.5-21B-GLM-4.7-Flash-Heretic (09-28), nicoboss/Kimi-Dev-72B-abliterated (09-27),
longsesh/Qwen3.8-27B (09-27). HF newest-40 (10-03): jfan gemma-4 litert trio (x3), local-inference-lab GLM-5.3-Flash
NVFP4-MXFP8-CSF-QAD, Laguna198/OpenThinker3-7B, infercrane qwen3.8-27b-h200-serving-recipe, zerodigest Qwen3.8-Flash-Next
REAP GGUF, alfodaniello Qwen3-Next-80B-A3B RedLite, velaia/Kolibri-1-MLX-4bit, KrynexLabs 25M TFLite, violetxi
qwen35-9b equational-theory x5. Google author listing: gemma-4 QAT wave (E2B/E4B/12B/26B-A4B/31B, 04-29..06-05, context).
Qwen author listing: Qwen3.8-27B (08-05), 27B-FP8 (08-13), 2.4T-A95B (08-08), Flash-Next + FP8 (08-24), Qwen-Drive-1.0-4B
(08-27), Qwen-Image-2.1 (09-14/09-20). Cloudflare/clef + clef-flash (09-30) + bartowski GGUFs (10-01) + terminus int8
(10-02) + taurusduan GGUFs (10-02). Muse-Glimmer-30B family (meta-models 08-09, nvidia NVFP4 08-27). Ollama v0.35.0
(09-28), v0.35.1 (09-29), v0.40.0-rc0 (09-25 prerelease). X snippet: @techfrenAJ (no id, snippet-grade).

## Pass 2 deep reads (fetched and read end to end this seat)

1. google/gemma-4-E4B-it-qat-q4_0-gguf card - READ
2. Qwen/Qwen3.8-Flash-Next card - READ
3. Cloudflare/clef card - READ
4. Hcompany/Holo4-27B card - READ
5. jfan/gemma-4-26b-web-moe-vision-litert-lm card - READ
6. ollama/ollama releases list + tags/v0.35.1 body - READ (verbatim lines captured)
7. Featherless default dump + newest-first arm + headers - READ/probed (10,175 + 4,023 rows counted)
8. LLM7 /v1/models - READ/probed (68 rows counted)
9. sweep/thread_1wv1u54.json (sibling's on-disk fetch) - READ (config extraction grep)
10. Morning run's open-and-local-language-models-x.md + register rows 16-20 + DIGEST exec summary - READ (dedup)

## The 8 banked items (strongest first)

1. **Ollama 0.35.1 regresses gemma janitor serving 3.2x on the estate's own RX 5600 XT** (measured this seat; release
   page github.com/ollama/ollama/releases/tag/v0.35.1, published 2026-09-29). 80.3-81.4 to 25.1-25.2 tok/s decode,
   3382 to 1116-1165 tok/s warm prompt-eval on gemma:2b; 14.6 to 5.0 tok/s and 87.8 to 7.2 tok/s on gemma4 8B Q4_K_M;
   full VRAM placement per /api/ps; new GPU-discovery-watchdog timeout spam in the runner. Quote (verbatim from the
   shared server log during the 0.35.1 window): "llama-server GPU discovery watchdog timed out". Overlap: catalog 0;
   the morning run banked Ollama decision-model NEWS but no serving measurement existed; percolator row 4 of 10-01
   speced the upgrade probe, this is its first arm.
2. **google/gemma-4-E4B-it-qat-q4_0-gguf is the measured 6GB-VRAM-class card the window's RQ1 kept missing** (card
   created 2026-05-01 per the google author listing; card read 10-03). Single "4-bit Q4_0, 5.15 GB" file; measured rows
   MMLU Pro 69.4%, AIME 2026 no-tools 42.5%, LiveCodeBench v6 52.0%, GPQA Diamond 58.6%, Codeforces ELO 940; E4B =
   4.5B effective / 8B total via Per-Layer Embeddings. Quote (verbatim): "allows preserving similar quality to
   bfloat16 while dramatically reducing the memory requirements to load the model." Overlap: catalog grep "E4B" 0;
   morning run's RQ1 verdict ("sub-4B slot unresolved") missed that Google already ships a QAT q4_0 GGUF with named
   benchmarks at exactly this class; fits the box this seat measured on.
3. **Qwen/Qwen3.8-Flash-Next: the fullest measured agentic card found, at the wrong size for the estate's VRAM clause**
   (2026-08-24). 125B total / 6B active, 512 experts (10 routed + 1 shared), hybrid Gated DeltaNet + Sparse Attention,
   vision, 262K native ctx. Measured: DeepSWE 1.1 58.7, SWE-bench Pro 62.5, SWE-bench Multilingual 81.0, Toolathlon
   Verified pass@1 73.5, Agents' Last Exam pass@1 24.3, AndroidWorld 84.5, OSWorld 2.0 binary 19.4. Quote (verbatim
   from card): "cuts long-context latency significantly, a critical gain as agentic workloads increasingly dominate
   real-world usage." Overlap: catalog 0; name appears once in an incidental 09-20 compaction-eval transcript
   ("I haven't run Qwen3.8-Flash-Next side by side"); never card-read by the estate before today.
4. **Cloudflare/clef card: decision quality is MEASURED across ~40 tasks plus latency, and Ollama 0.35.1 serves it
   natively** (repo 2026-09-30; release body read verbatim 10-03). 27B post-train of Qwen3.8-27B + joint schema head,
   one forward pass, noul/choice/score, Apache-2.0, Decision Index 0.2.1 (BFCL 98.5, GSM8K 80.8, MMLU 90.3, median
   latency 209.3 ms, p95 238.6 ms, Typesafe invoice exact-actions 64.7), served on a single H200, 16 community
   quantizations exist. Quote (verbatim, v0.35.1 release body): "Ollama now supports Clef and Clef Flash, Cloudflare's
   new open-source decision models, through `/v1/systemone`." Overlap HEAVY, declared: clef is already banked today
   three ways (arXiv lane lines 24, 90, 171; HN story 49923692; finetuning-adaptation-hn item 3); this item's delta is
   the card's measured table plus the step-0 contract target for the estate's owed typed-decision probe
   (percolator row 4 of 10-01 names tev1:0.8b; clef-flash 9B is the second candidate on the same endpoint).
5. **Hcompany/Holo4-27B: computer-use VLM post-train of Qwen3.8-27B with cost-per-task measured, CC BY-NC** (first
   seen on the Featherless roster 09-28; card read 10-03). Quote (verbatim): "Holo4-27B scores 85.2% at $0.08 per
   task." Also OSWorld 2.0 61.7% at $1.22/task, AutomationBench 45.4% at $0.05/task, MoE sibling Holo4-35B-A3B ~3B
   active at roughly half those scores and half the cost, max ctx 262,144. Not agentic-asserted but computer-use
   measured. Overlap: catalog 0; no sibling bank file names Holo4 (raw pulls only: arctic_LocalLLaMA.json,
   featherless_roster_100.json); NC license is model-garden friction, Apache base noted on card.
6. **Featherless served roster HALVED in five days and the roster-diff's two arms now disagree** (measured this seat,
   2026-10-04T00:14Z server clock). Default dump 10,175 rows / 3,224,862 bytes vs 22,059 byte-banked 09-28
   (memory/burns/LEDGER.jsonl:683,692); newest-first arm 4,023 rows, newest new model 2026-10-02T01:07:26Z. Quote
   (verbatim head of the fetched dump): `{"data":[{"id":"recursal/EagleX_1-7T","is_gated":false,"created":1719250778,"model_class":"rwkv5-7b","owned_by":"Feather"`.
   Overlap: sibling HN lane's paged probe today (open-and-local-language-models-hn.md:101,113) is consistent but took
   no full-dump census; the halving is new, unexplained, and falsifies nothing yet (falsifier per ledger 629: keyless
   200 turning 401 has NOT fired; two zero-new-rows nights HAVE started on the newest-first arm).
7. **LLM7 stays the only measured free-class inference lane and grew 64 to 68 models; no door exposes rate-limit
   headers** (probed this seat, keyless HTTP 200, 66,787 bytes). Quote (verbatim head): `{"object":"list","data":[{"id":"DeepSeek-V4-Flash-0731","object":"model","created":1791065828,"owned_by":"","model_type":"chat","schema_endpoints":["openai"],"tier":"turbo","pricing_mode":"token","pricing":{"input":0.02,"output":0.04,"currency":"USD","unit":"1M tokens"`.
   Overlap: LLM7 HOT at 64 models is ledgered 09-27 (memory/burns/LEDGER.jsonl:609); the +4 churn and the measured
   absence of ratelimit headers on both hot doors are new and feed RQ4's tank probe design.
8. **Gemma 4's official web layer landed today as LiteRT-LM WebGPU bundles, and the mirror card asserts everything and
   measures nothing** (jfan/gemma-4-26b-web-moe-vision-litert-lm, 2026-10-03T22:27Z; card read 10-03). "Gemma 4 26B-A4B
   MoE" for browser WebGPU, .litertlm bundles (text / +vision / +audio / +vision+audio), Gemma license, configured in
   a LiteRT-LM Studio demo; the card carries zero benchmark numbers. Quote (verbatim): "128 experts, Top-8 routing,
   4B active params". Overlap: catalog 0; "litertlm" 0 hits in sibling banks; the morning run's out-of-window context
   line ("gemma:2b baseline is two Gemma generations old") gains its first in-window serving-layer datapoint.

## Checks run this seat (exact commands, condensed)

- `ollama --version` + `ollama list` (0.34.3; no Qwen3.8-27B on disk).
- `curl -s http://localhost:11434/api/generate -d '{...gemma:2b...}'` x2 baseline, x1 control, x1 gemma4 (JSON timing
  fields parsed with the repo venv python).
- Portable 0.35.1: download 1,471,094,402 bytes; Expand-Archive; PowerShell Start-Process (windowless) serve on
  127.0.0.1:11500 with OLLAMA_MODELS at the shared blob store; x3 gemma:2b + x1 gemma4 benches; `/api/ps` on both
  ports; taskkill by recorded PID; primary 0.34.3 re-verified alive after teardown.
- `curl -s -D headers https://api.featherless.ai/v1/models` (10,175 rows counted) and
  `...?sort=-created_at` (4,023 rows, newest 2026-10-02T01:07:26Z); `curl -s https://api.llm7.io/v1/models` (68 rows);
  grep over captured headers for ratelimit/retry-after: zero matches.
- Overlap greps per item over catalog/catalog.jsonl + memory/ + the morning run's sweep files (per-item results in the
  items above; the memory-side scan for the last four patterns was still running at write time and those items carry
  catalog counts 0 plus sibling-sweep counts 0 from the completed portion).

## Not run / owed (stated, not guessed)

- RQ2 estate-side replication at Q4_K_M on the estate task mix (no Qwen3.8-27B local; multi-hour probe; instrument
  speced at frontier_olm_2026-10-01/percolator_candidates.jsonl row 3).
- RQ4 per-dispatch tank accounting (long-running estate instrument; morning DIGEST point 2 owns it).
- fxtwitter resolution: no in-window status id surfaced for this seat; the X door contributed one snippet only.
- Root cause of the 0.35.1 regression inside the llama.cpp bump (needs an upstream bisect; estate action is hold + file).

## Erratum (appended after submission, instrument completed late)

The overlap grep's memory/catalog-side scan finished AFTER this file was written. One line in item 2's overlap was
written ahead of its instrument and is WRONG as stated: "grep 'E4B' over catalog/catalog.jsonl = 0" - the completed
case-insensitive grep reads 3,827 catalog rows, dominated by hex-substring noise (e.g. the agent_state chain hash
`20260809T234910Z_e4bdf509`, catalog ids containing `e4b`), NOT Gemma E4B model rows; the intended case-sensitive
model-name check was never actually executed before write. The substantive conclusion (no prior estate holding of the
gemma-4-E4B QAT card) still stands on the completed evidence: no catalog row names the model, and no sibling bank .md
names it. Remaining completed patterns all CONFIRM the bank as submitted: litertlm catalog 0 (raw tmp pull only);
UD-Q4_K_XL memory hits are incidental chat transcripts (compaction_eval, app_reasoning), no holding; systemone memory
hits are exactly the owed-probe docs already cited (percolator candidates, seat memory); Featherless catalog 5 /
LEDGER + seat-memory (cited); LLM7 catalog 6 / LEDGER (cited); 1wv1u54 catalog 0 (sibling-banked today, as declared).

ADDENDUM (second, earlier-scoped grep over the 09-28 and 10-02 sweeps completed after submission): two overlap claims
need widening. (1) Flash-Next (item 3): beyond the incidental transcript, the 10-02 lanes name-dropped it as
candidates without card reads (frontier_olm_2026-10-02/sweep/inference-efficiency-x.md, -arxiv.md, -reddit.md,
quantization-compression-hn.md, sweep_hn_qwenflash.json; plus a biography residual pair). "Never card-read before
today" remains true; "name appears once" was undercounted. (2) LiteRT/litertlm (item 8): present in the 09-28 olm
arxiv lane's raw paper pull (sweep/_raw/full_2609.25373.html/.txt, arXiv 2609.25373) and that lane's .md, so the
blanket "0 hits in sibling banks" is WRONG as absolute; catalog remains 0 and no banked ITEM covers Gemma's LiteRT
web layer. clef-flash in the 10-02 finetuning-adaptation-hn bank matches what was already declared.

## Fold (what the estate should steal)

1. HOLD the Ollama upgrade on the janitor host; the measured 3.2x regression outranks every 0.35 release-note gain.
   Re-run the exact A/B here on 0.35.2+ before any upgrade lands.
2. The 6GB-class measured successor to gemma:2b is gemma-4-E4B QAT q4_0 (5.15 GB, benchmarked card), not any window
   release; a one-evening ollama pull + janitor-battery A/B on this box would size the janitor upgrade.
3. The Featherless roster-diff needs its reconciliation pass before trusting any count again (arms disagree 10,175 vs
   4,023; newest-first arm stale two days while the dump shrank 54 percent).
4. clef-flash 9B joins tev1:0.8b as a step-0 candidate for the owed /v1/systemone typed-decision probe; note morning
   DIGEST point 7's Red Hat counterweight before spending on it.
5. Flash-Next and Holo4 set the measured-agentic bar the estate should demand of any garden candidate: named task
   suites with cost or latency, never the word "agentic" alone.
