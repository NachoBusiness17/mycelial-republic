# Sweep: open-and-local-models via reddit - 2026-10-06

source-fetched: 2026-10-06
seat: sweep-open-and-local-models-reddit (workflow subagent)
instrument: curl with browser UA against reddit Atom RSS (feeds + 2 per-thread pulls, parsed
locally with repo venv python xml.etree), WebFetch against the safereddit.com mirror (7 thread
reads), powershell registry + wmic reads for host specs, rg/grep for overlap. Every quote below
came from a page fetched this session. Caveat on the WebFetch-side quotes: safereddit renders
pass through the fetch tool's summarizer, so those quotes are the tool's extraction of the page,
not my own byte parse; the two RSS-side quotes (1wvv6im, 1wv4zzi) are byte-verbatim from the XML
I parsed myself.

## Doors scoreboard (what worked, 2026-10-06)

| Door | Recipe | Result |
|---|---|---|
| Ask's named door: old.reddit top.json via WebFetch | `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` | DEGRADED: HTML interstitial, zero post data. Matches doors.md:46-62 and burns.md:198-200 (known dead end). |
| old.reddit top.json via curl + browser UA | same URL, `curl -A "Mozilla/5.0 ..."` | HTTP 302, 0 bytes. CLOSES the OWED at doors.md:59-60 with a negative: browser UA does not unlock old.reddit JSON. |
| www.reddit Atom RSS via curl + browser UA | `www.reddit.com/r/<sub>/top/.rss?t=month` | HTTP 200, application/atom+xml. LocalLLaMA 57,919 B; MachineLearning 84,602 B; LocalLLM 79,317 B; ollama 96,133 B (after 429 retries with 20-45 s spacing). |
| Per-thread Atom RSS via curl | `www.reddit.com/r/<sub>/comments/<id>/.rss` | 200 for 1wvv6im (94,256 B) and 1wv4zzi (91,370 B); then reddit began 429ing even at 40 s spacing. |
| safereddit.com mirror via WebFetch | `safereddit.com/r/<sub>/comments/<id>/` | WORKS for all 7 remaining thread reads (the day-5 verified recipe, open-local-language-models-reddit.md:17). |
| WebSearch site:reddit.com fallback | not used | Not needed; RSS + mirror covered everything. No fabrication of a fallback. |

Raw feeds kept at sweep/raw/ (rss_LocalLLaMA.xml, rss_MachineLearning.xml, rss_LocalLLM.xml,
rss_ollama.xml, srch_decision.xml renamed rss_-prefixed sibling srch_decision feed, srch_kolibri
feed, thr_1wvv6im.xml, thr_1wv4zzi.xml).

## Pass 1 broad sweep (130 feed entries considered, last 30 days)

- r/LocalLLaMA top-of-month: 25 entries (raw/rss_LocalLLaMA.xml), including 1wijo3e, 1wymgu6,
  1wdbvlt, 1wk979c, 1wth4iz, 1whf7ov, 1wmxfjs, 1wvz1ex, 1wepx7w, 1wlgrft, 1wcbid7, 1wj6c4l,
  1wapjaw, 1wyefkt, 1wt5f4e, 1wk9fag, 1wo6o0f, 1wa26pn, 1wi32jg, 1wkocvj, 1wbfrut, 1wtc4j9,
  1weujw6, 1wc6krf.
- r/MachineLearning top-of-month: 25 entries, including 1wavdi7, 1wea1t7, 1wl0l7j, 1wvg7yc,
  1wm9hgn, 1wgazy4, 1wakf62, 1wgzpli, 1wa8rub, 1wsejb7, 1wrqoxp, 1wdfmvq, 1wuz2s4, 1wtyl5m,
  1wks0dv, 1wp6oi3, 1wsyu8m, 1wxcd4k, 1w92eis, 1wjuki0.
- r/LocalLLM top-of-month: 25 entries, including 1wmzky1, 1wp3vnh, 1whqwdq, 1wpfxje, 1wlhh08,
  1wy1o7y, 1wuqsyy, 1wehgvc, 1wdramg, 1wgwgrf, 1wqg3ld, 1wv1u54, 1wjwxeq, 1woxb4n.
- r/ollama top-of-month: 25 entries, including 1wt0tot, 1wvxih5, 1wboy1g, 1wjnkgm, 1wx0jtb,
  1wa3zax, 1wlh7us, 1wdasar, 1wq653p, 1wd8xc7, 1wc6tka, 1wa19oj, 1wo3fyy, 1wqxbwa, 1wkl0wz,
  1w9u9oo, 1wloz92.
- r/LocalLLaMA search "decision model" t=month: 25 entries, including 1wjieap, 1woe70t,
  1wp0z3i, 1wvv6im, 1wouby6, 1wv4zzi, 1wpvep4, 1wcujgg, 1wybi2y, 1wl1yzq, 1wsgrma, 1wljzix,
  1wynbvq, 1wvt1m4, 1wy55p2, 1wv05u1, 1wlmkm9, 1wrz9py, 1wvqbrz, 1web1jd, 1wxloam, 1wr8d4d,
  1wsfjmb, 1wvfz9n, 1ws6bmh.
- r/LocalLLaMA search "Kolibri" t=month: 5 entries: 1wwl7y6, 1wy3y4t, 1wynppg, 1wyzdjx,
  1wyeanf.

## Pass 2 deep reads (9 threads fetched and read end to end)

1. 1wvv6im New in llama.cpp: Decision Models (r/LocalLLaMA, 2026-10-02, 121 entries in feed)
   - via curl RSS, byte-verbatim.
2. 1wv4zzi Clef: Open Weights decision model by Cloudflare (r/LocalLLaMA, 2026-10-01, 114
   entries) - via curl RSS, byte-verbatim.
3. 1wxloam Benchmarking decision models is fun - Clef Q8 vs Jev (r/LocalLLaMA, 2026-10-04) -
   via safereddit.
4. 1wyeanf I squeezed Kolibri-1 78B-A3.5B to 20.9 GiB / 2.30 bpw (r/LocalLLaMA, 2026-10-05) -
   via safereddit.
5. 1wwl7y6 Aleph-Alpha/Kolibri-1 HF release thread (r/LocalLLaMA, 2026-10-03) - via safereddit.
6. 1wqxbwa Gemma 4 e2b vs 26b numbers and lessons (r/ollama, 2026-09-26) - via safereddit.
7. 1wgzpli 44M param quantized LLM, 19.8 MB, ~1900 tok/s (r/MachineLearning, 2026-09-15) - via
   safereddit.
8. 1wyefkt How is it possible that qwen 27b is so good? (r/LocalLLaMA, 2026-10-05) - via
   safereddit.
9. 1wjwxeq Bonsai 2 27B vs Gemma 4 12B vs Qwen 3.5 9B (r/LocalLLM, 2026-09-18) - via
   safereddit.

## Answers to the five research questions

### RQ1: does a decision model beat gemma:2b per dollar on estate scut classes (L15)?

The wave is CONFIRMED as a live, cheap, production-shaped mechanism, but the per-dollar verdict
stays a LEAD: nothing I read converts it to an instrument row, and the community itself supplies
the reason the estate's battery is the missing act.

- Mechanism, byte-verbatim from the 1wvv6im feed: "Jev and alike models are standard LLMs with
  token generation ripped off and output a simple JSON for decision making/classification"
  (u/sebgggg), and "They are still llms... they are not autoregressive. Instead, they work as a
  single pass decision model" (u/anyesh). OpenJev's default base is DiffusionGemma (u/scrdest),
  and OpenRouter already uses decision models to route requests to big models (u/scrdest).
- Community epistemics matches L15 exactly, byte-verbatim: "I think there's probably around five
  people total on here who've actually used any of the competitors let alone benchmarked them on
  their own data" (u/toothpastespiders, 1wvv6im). Negative datapoints on judge-like scut: a
  workplace discussion found Jev "atrocious at 75%" accuracy as an LLM judge (u/notsosleepy), and
  Laya measured "about as good as rand()" on softball problems in u/rabbotz's own tests.
- Size/latency envelope (day-5 HN rows, still the best numbers held): 144M to 27B via
  /v1/systemone, median 3 ms at 144M to 43 ms at 27B on one RTX PRO 6000, output_tokens 0
  (watch/inbox/frontier_olm_2026-10-05/sweep/inference-efficiency-hn.md:76-84). New reddit-side
  rungs this sitting: Jeff-Qwen3.5-0.8B v1.2 claims "38x faster decisions and +8.7 points" in
  front of Qwen3.8-27B (1wv05u1, PASS-1 ONLY, unverified, vendor-style claim), Perplexity
  Decider 27B = Qwen3.8 27B fine-tune (1wvfz9n, pass-1 only), Mica v0.1 4B did 26 survival-
  Minecraft decisions (1wsfjmb, pass-1 only).
- The per-dollar question has a hidden harness term the sweep newly exposes: see RQ5/RQ3 below,
  fan-out width beat model quality outright in the one head-to-head I read (1wxloam). A fair
  estate battery must hold the harness constant or it will measure the wrong animal.

Verdict: still sweep-level by the day-5 law (DIGEST.md:71-81, burns.md:93-96). The estate fill
remains OWED; this sitting adds candidate rungs (0.8B-4B class) and two measured failure priors
(75% judge accuracy; rand()-level Laya) to set the falsifier bar.

### RQ2: fill the local lane's UNMEASURED cells (laws.md:88, battery 8 columns)

Not fillable from Reddit: L15 (RIB_MODEL_GARDEN_ROUTING.md:46-53) makes UNMEASURED a legal state
and vendor/community numbers never route dollars. What the sweep banks is per-cell prior
evidence for when the estate runs its battery:

- gemma:2b (floor): unchanged, no community row anywhere in what I read.
- gemma4: the e2b-vs-26b thread gives hands-on timings: sentence cleanup 100-430 ms on
  e2b-it-qat vs 250-900 ms on 26b; first call after load 0.4 s vs 8.7 s; answer with 8 cited
  sources 2-2.5 s vs 2.5-7 s; e2b needs 8 GB RAM (4.3 GB download), 26b needs 48 GB (1wqxbwa).
  Gemma 4 12B Q8_0 scored "washed out" against Bonsai 2 27B PQ2_0 and Qwen 3.5 9B on a voxel-
  pagoda one-shot (1wjwxeq), but that comparison is founder-posted and disputed in-thread.
- decision-model rung (new, candidates for the under-gemma:2b rung): Julia-1 144M, Laya 421M,
  Kev-4B, lev 4B, tev1:0.8B, nimble 9B (day-5 rows), plus this sitting's Clef 27B / clef-flash
  9B (1wv4zzi: post-trained from Qwen3.8-27B and Qwen3.5-9B respectively). A community warning
  for the battery, byte-verbatim from the 1wv4zzi feed: "The leading ones are vibe coded
  projects slapped together in a day on a 3090, based on Jev's recipe. They really shouldn't be
  used as a baseline" (u/SexyAlienHotTubWater).
- Quantization sensitivity of decision models is an open community question ("how shit does this
  get when we quantize it to anything under Q8?", u/oxygen_addiction, 1wv4zzi); the estate
  battery should include a quant arm.

### RQ3: open weights released after 2026-09-06 that pass the GPU-ladder gates on THIS host

Host measured this sitting: AMD Radeon RX 5600 XT, VRAM 6,425,673,728 bytes (registry
HardwareInformation.qwMemorySize under
HKLM\SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}), system RAM
68,667,752,448 bytes (wmic computersystem). Note: Win32_VideoController.AdapterRAM reads
4,293,918,720 (32-bit cap) and is the wrong number; the registry value is the truth here.

Gates (RIB_GPU_LADDER_20261001.md:10-24: arch, VRAM, price trigger, software, workload). On a
6 GB VRAM + 64 GB RAM host the realistic serving shape is RAM-resident GGUF with small-VRAM
offload (llama.cpp Vulkan/CPU), so the fit list from this month's releases:

- SHADOW-50M: 19.8 MB ternary 44M-param model, ~1900 tok/s on laptop CPU (1wgzpli). Trivial fit.
- Qwengram-0.8B (1wpvep4), tev1:0.8B and Jeff-Qwen3.5-0.8B (day-5 + this sitting): GB-class.
- gemma4:e4b Q4_K_M ~6.6 GB (day-5 quantization row): RAM-fits, VRAM no.
- Bonsai 2 27B PQ2_0: 7.2 GB, ~101 tok/s on an RTX 5090 in-thread, OP claims it "can easily run
  on a 3060 with decent tps" (1wjwxeq): RAM-fits on 64 GB.
- Kolibri-1 78B-A3.5B: 20.94 GiB at 2.30 bpw (1wyeanf, see RQ4): RAM-fits with 40+ GB headroom.
- Clef 27B: 18 GB download, Apache 2.0 (day-5 Clef library row): RAM-fits.
- clef-flash 9B, Qwen 3.5 9B, MiniCPM5-2B, Agents-A1-4B, ornith-1.0-9B (from the 8 GB-contender
  list in 1wqxbwa comments): RAM-fits, some partially VRAM-fit at low quant.

Nothing this month requires the price-trigger hardware rungs (24 GB Blackwell under $1200 etc.,
laws.md Q15); the DG1 mating-to-MoE workload-gate adjudication stays open. The arch gate note:
RDNA1 Vulkan in llama.cpp is the software path; the estate has Vulkan/QAT hazards pre-banked on
Gemma 4 (day-5 family map row).

### RQ4: does the Kolibri pull fit and serve on this host

- Fit: YES on RAM. Measured this sitting from 1wyeanf: full 384-expert IQ2_XS-variant runs
  "20.94 GiB" at "2.30 bpw" with "90.5% top-token agreement" vs a Q8_0 reference requantized
  from BF16 (~156 GB); a 365-expert pruned variant is 19.99 GiB and lost "only about 0.07% of
  all expert selections"; byte-verbatim: "375 of the 950 removed experts were never selected at
  all". That last number is the sparse-MoE knowledge-from-spend split (burns.md:82-83) made
  concrete: massive expert redundancy. Against 64 GB RAM, 21 GB leaves 2/3 free.
- Serve: precedent in-thread on WORSE hardware than ours: u/stefanfis runs Q4_K_M GGUF on dual
  RTX 3060 12GB + 32 GB DDR4 at "PP: 350 t/s / Generation: ~27 t/s" (1wwl7y6). Our host has 2x
  the RAM and the active-parameter count (3.46B) is CPU-servable. Software gate: llama.cpp
  needs "a patch" per u/GreenHell, and the architecture is "Very conventional" per u/Marcuss2.
- Gating: the ask's premise "download-gated" is NOT confirmed by what I read: the release thread
  shows Apache 2.0 and no gate reports (1wwl7y6). I did not fetch the HF repo page, so gate
  status stays UNVERIFIED, not asserted either way.
- The day-5 falsifier stands ready: fixed 30-prompt tool-call set vs qwen2.5:7b and gemma:2b,
  pass >= 20/30 vs fail <= 15/30 (DIGEST.md:90). Expectation setter from this sitting: Kolibri's
  tool calling is its measured weak spot, BFCL 39.8 vs 58.2 for GLM-4.7 Flash
  (u/tejaskumarlol, 1wwl7y6), consistent with the day-5 teardown's BFCL 39.8. For JANITOR
  tool-call scut the prior is now negative; for long-context read/classify scut (1M context
  claim, 262,144 native) the prior is positive.

### RQ5: does HAD replicate on our harness shape (harness limitation vs model limitation)

The e2b-vs-26b thread is a field replication of "capability moves through the fixed harness"
(burns.md:84, HAD 2610.02858), on exactly the estate's disease list:

- Small-model "limitations" cured HARNESS-side, no model swap: missed self-corrections fixed by
  a "deterministic pre-pass for correction triggers like 'actually,' 'make that,' 'no wait,'
  'I mean,' plus prompt examples" (1wqxbwa); cleanup models answering dictated questions
  instead of transcribing fixed by a length/drift guard with rule-based fallback; invented
  dates fixed by removing date work from the model ("Don't let models do dates", deterministic
  parser); malformed JSON and repetition fixed by salvage parsing and loop guards; empty
  digests from llama.cpp were reasoning tokens consuming the budget, fixed with
  --reasoning-budget 0. That last one is the estate's own EMPTY_REASONING terminal-class law
  (L29) appearing as a stranger's bug report.
- The harness-terms counterpoint, from 1wxloam: in OSRS PvP duels, Clef 27B Q8 on an RTX 5090
  beat Jev 1.13 six matches to three 1v1, then "Clef has won just 1 of 22 matches" against a
  self-play-trained bot, and per u/bonerfleximus "Something from that test is that 21 normal
  bots stomped the Clef bot"; his framing, byte-verbatim: "that's comparing single decisions at
  a time. Jev can process 1000s of decisions about state in a single request." Harness width
  (fan-out) beat model quality outright. The estate's HAD battery should add a width arm or it
  under-measures the harness term.
- Strong form, from SHADOW-50M (1wgzpli): deterministic "inline circuits" ([calc] tags: "A fixed
  circuit at the readout takes over and fills in the correct digits in the same token stream")
  lift a 44M model to winning arithmetic/dates/retrieval demos while losing "every standard
  benchmark" to a same-class Llama-style model ("Supra beats SHADOW on every standard benchmark
  I tested"). This is L21 (deterministic grammar stays deterministic) embodied, plus a draft-
  model result: 19.7 to 28.5 tok/s for Qwen3-32B in llama.cpp.

## Ladder implications (feeds queue/lanes + memory/frontier/allowance.jsonl)

1. The under-gemma:2b rung now has named, pullable candidates at 0.8B-4B (tev1:0.8B,
   Jeff-Qwen3.5-0.8B, Kev-4B, Mica 4B, clef-flash 9B) all servable through the SAME
   /v1/systemone face llama.cpp already ships; the estate battery can sweep them without new
   harness code.
2. The janitor harness should grow the four cures the field keeps rediscovering: deterministic
   pre-pass for correction triggers, length/drift guard with rule fallback, salvage parsing,
   reasoning-budget-0 for digest-class asks. Three of the four are estate laws already; the
   pre-pass is the new steal.
3. Kolibri stays lead-until-measured, with the pull now ~21 GB RAM-fitted and a negative prior
   on tool-call scut.
4. Fan-out width is a harness variable, not a model variable: any head-to-head that varies
   models across different serving shapes is measuring the wrong thing.

## Overlap ledger (instrument: grep -c on catalog/catalog.jsonl; rg on memory/ excluding
memory/trajectory/** which is this run's own log; rg on the day-5 register + DIGEST)

- catalog: all 9 thread IDs 0 hits; "Clef" 2, "Bonsai" 121, "decision model" 15, "Kolibri" 0,
  "systemone" 0, "SHADOW-50M" 0.
- memory/: "Kolibri" 0 hits; "Clef" hits are corpus literature (treble clef), not the model.
- Day-5 union (watch/inbox/frontier_olm_2026-10-05/register.jsonl + DIGEST.md): decision-model
  wave banked as 5 sweep-level rows (llama.cpp blog, Ollama 0.35 blog, Ollaya HN, Clef library
  page, Clef HN thread) with JevBench numbers and latency tables; Kolibri banked from the vendor
  blog with BFCL 39.8/Terminal-Bench 27.7 and a named unrun falsifier; HAD 2610.02858 banked
  with a named unrun head-to-head; Bonsai 2 release thread deep-read.
- Per item: 1wvv6im NEW (the reddit discussion, not the blog); 1wv4zzi PARTIAL (clef-flash base
  = Qwen3.5-9B, vibe-coded-baseline warning, quant-under-Q8 question are new deltas over the
  day-5 Clef rows); 1wxloam NEW; 1wyeanf PARTIAL (20.94 GiB measured + expert-redundancy counts
  new over the vendor-blog item); 1wwl7y6 PARTIAL (local serving numbers + BFCL confirmation
  new); 1wqxbwa NEW; 1wgzpli NEW; 1wyefkt NEW; 1wjwxeq PARTIAL (head-to-head is a different
  thread from the banked 1wj6c4l release thread; gemma4-12B quality datapoint new).

## OWED / not run this sitting

- The estate battery itself (RQ1/RQ2 fills): fetching evidence does not fill L15 cells; the
  probes stay with the day-5 probe order (DIGEST.md:83-92).
- Kolibri gate status on the HF repo page: not fetched; unverified either way.
- BFCL leaderboard page: inherited day-5 timeout; not retried (same door, same timeout risk).
- Jeff-Qwen3.5-0.8B "38x faster + 8.7 points", Perplexity Decider 27B, Mica 4B Minecraft,
  1wynbvq Civ-V bench (GLM-5.3 ahead of Opus-5.5, Qwen-3.8-27B "holds up"), 1wy55p2 Clef Flash
  plays Snake: PASS-1 ONLY, named so the next pass knows they exist; none verified beyond
  title.
- arXiv submittedDate and hn search_by_date recipes (the ask's doors.md:28-29, 42-44 OWEDs):
  not exercised this sitting; the ask's primary door for this seat was Reddit and Reddit
  coverage completed without them. They remain OWED from doors.md.
- Quotes from the 7 safereddit reads pass through the fetch tool's summarizer; the two RSS-side
  threads are byte-verbatim. A byte-exact re-pull of any safereddit quote before promotion is
  the honest next step.
