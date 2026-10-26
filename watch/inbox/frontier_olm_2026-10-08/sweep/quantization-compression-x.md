# SWEEP: quantization-compression via x (2026-10-08)

source-fetched: 2026-10-08

Area: quantization-compression. Door: X per the ask's recipe (WebSearch `site:x.com`,
single posts resolved through `https://api.fxtwitter.com/<user>/status/<id>`), plus the
arXiv export API in the minimal shape (lens/doors.md:20-39) for RQ5, plus web price
pages for RQ4. Stamp: source-fetched: 2026-10-08. Seat: sweep-quantization-compression-x.
THIS SITTING ALSO FIRED THE OWED A/B: the run receipt with the verdict lives at
`quant_ab/RECEIPT.md` in this dir (instrument `quant_ab/run_ab.py`, raw rows
`quant_ab/results_armA.jsonl` / `results_armB.jsonl`, hashes `quant_ab/BLOBS.json`).

## HEADLINE: the owed A/B ran end to end this sitting

The four-lane-re-owed qwen2.5:7b Q4_K_M vs q8_0 A/B (probe 5,
frontier_olm_2026-10-03/lens/burns.md:122), amended by the four-pinned-choices spec
(port_wave_20261007/QUANT_AB_SPEC_AMEND.md) and recorded un-run this morning
(frontier_olm_2026-10-08/lens/burns.md:205-208), is now RUN: 100 generations
(10 tool-failure-recovery tasks x 5 phrasings x 2 arms), temp 0, paired seeds, hashed
blobs. Verdict: TIE AT CEILING. Full-pipeline success 50/50 vs 50/50; strict-parse 49/50
vs 49/50 (same pair missed in both arms, markdown fences); ALL 50 output pairs
BYTE-IDENTICAL between quants; per-task spread 0.0 pp; matched-task deltas all exactly 0.
The only axis that moved: latency (median wall 3.99 s vs 7.15 s, 1.79x; decode 6.9 vs
3.0 tok/s). Both of the spec's falsifiers FIRED, exactly as its :106-110 branches
defined: the multi-prompt rule is dead weight at this task mix (banked as the first
stability datum at odds with the paper, task-mix-scoped, not a paper refutation), and
the Qwen-flat parse prior confirmed (channel demoted to rider). Nothing promotes into
configs/lanes.yaml; no lane quant changed (git status: configs/lanes.yaml unmodified).
The instrument is ceiling-bound - honest limits and the difficulty-hardened OWED are in
the receipt. Blob hashes (recomputed, match content addresses): Arm A
2bada8a7450677000f678be90653b85d364de7db25eb5ea54136ada5f3933730, Arm B
3603045b543e1c0dfb27f126a3642e7f805e480b84c4781e3d848ace971cba7a; ollama 0.34.3.

## Doors: what worked, what degraded (honest)

- fxtwitter: DEGRADED vs yesterday's 7/7. First two calls timed out at 60 s
  (TeksEdge 2103161113341026776, OpenBMB 2103107192068993094); a retry of TeksEdge
  succeeded, OpenBMB was not retried to completion (its content is covered by the
  TeksEdge read of the same announcement). bnjmn_marie and AIatMeta resolved first try.
- arXiv export API: the minimal shape WORKS with a `submittedDate:[A TO B]` range filter
  inside search_query and NO sortBy: `search_query=all:quantization+AND+submittedDate:
  [202610010000+TO+202610082359]&max_results=15` returned 134 total / 15 entries without
  the timeout doors.md:33-39 measured for sortBy variants. This extends the door recipe:
  date-windowing does not need sortBy. A plain `all:GGUF` query also worked (50 total).
- WebSearch `site:x.com`: worked but rate-limited (one query returned three 1302s before
  answering on retry; one query returned empty). Pacing needed, same as day 7.
- Price pages: bestvaluegpu.com returned HTTP 429 to WebFetch (figures below are the
  search-result's quotes of it, disclosed); compute.exchange fetched clean.

## Pass 1: candidate pool (34+ considered, window 2026-09-08..2026-10-08)

From `site:x.com` searches: bnjmn_marie 2105481856812740726 (Oct 1, 11-GGUF ladder);
TeksEdge 2103161113341026776 + OpenBMB 2103107192068993094 (Sep 24, FIT-GGUF);
TeksEdge 2106074231494852863 (Oct 2, llama.cpp decision models - ALREADY BANKED day-7
from the primary, dropped, see dedup); ossalternative 2105629053927702623 (130k stars,
low value); hackernoon 2106036143749754978 (Swift-1.5 GGUF); gurtej__gill_
2105757683467096126 (prefill vs generation quant); DataChaz 2105950330676736389;
NeoAIForecast 2104138934716690456 (Sep 27 recap); sudoingX 2049056800759042459 and
nisten 1877437609309303107 and MLStreetTalk 2040302198605943255 and LottoLabs
2045712710399304025 and HuggingModels 2047153249506259222 (out-of-window IDs);
ItsmeAjayKV 2090903849578229820 + 2081232733523861596 (borderline-old, not resolved);
analogalok 2088625914682941719 (KL chart, unresolved); draginol article 2089338779324543047
(out-of-window primer); QuantumindSSI 2075117605690458118 (out); AhmadOsman x2 (out);
FeitengLi 2097609675361710366 (Qwen3.8-27B sub-3bpw, unresolved date); Meta Muse Glimmer
2086757844544811485 + WesRoth 2086965822149280077 (RESOLVED Aug 10, out-of-window,
considered not banked); Akashi203 lossless-inference article (out-era); AlphaSignalAI
2045233520608464983 (out); support_huihui GLM-5.3-Flash GGUF (no status ID, unresolved);
0xMovez guide (low). Off-door: YouTube QPRh4Y6sdkc "Q4 vs Q8 ... Same Score, Different
Answers" (banked snippet-tier below); r/LocalLLaMA 1o5mr9j (reddit door walled per
doors.md:56-64); bestvaluegpu + compute.exchange price pages (RQ4, below); arXiv
2610.04403, 2610.06174, 2610.00983, 2610.07522, 2610.08231, 2610.07767, 2610.05265
(from the export-API listing; only the two banked below were read at abstract level
this sitting, 2610.04403 is ALREADY BANKED day-6, dropped).

## Pass 2: deep reads (fetched and read this sitting)

1. bnjmn_marie 2105481856812740726 via fxtwitter (full text) AND its linked
   kaitchup.substack.com article (preview; paywall disclosed).
2. TeksEdge 2103161113341026776 via fxtwitter (FIT-GGUF, after one 60 s timeout).
3. TeksEdge 2106074231494852863 via fxtwitter (decision models; read, then DROPPED from
   the bank as day-7-held subject).
4. AIatMeta 2086757844544811485 via fxtwitter (Muse Glimmer date check: Aug 10, out).
5. compute.exchange/blogs/h100-gpu-price-2026 (H100 price page, full read).
6. YouTube QPRh4Y6sdkc (DEGRADED: title only, no channel/date/description in what the
   fetcher got; banked snippet-tier with that disclosure).
7. arXiv export API listings (two fetches: quantization Oct 1-8 window; all:GGUF) -
   abstract-level reads for every entry quoted below.

## Answers to the five research questions

- RQ1 (run the A/B): DONE, see HEADLINE. Which janitor/lane tasks flip verdict: NONE of
  the 10 flip - every task is 5/5 on both arms; the flip count is zero and that zero is
  the finding (a ceiling tie, receipt `quant_ab/RECEIPT.md`).
- RQ2 (load-bearing pins + minimal contract): at THIS task mix only the pooled-verdict
  pin and the per-task-spread pin carry information (both others collapsed at ceiling);
  the receipt distills the minimal contract for this box: recomputed blob sha256, temp 0
  + paired seeds, pinned num_ctx/num_predict (8192/512), pooled all-pairs verdict with
  clean-intersection deltas diagnostic-only, strict channel logged never merged, per-run
  `ollama ps` logged, ollama version named. Full instrument cost: one 8.1 GB pull +
  about 10 minutes of generation, $0.
- RQ3 (per-role quant ladder vs one global choice): this run gives the first estate
  datum: at 7B on short-horizon janitor scut, Q4_K_M is latency-free money (1.79x
  faster wall, zero measured task cost, zero token inflation: 774 vs 774 output tokens).
  The ladder question therefore collapses at L0-short-horizon to "Q4 everywhere";
  the axis that could re-open it is long-horizon agentic work, where this window's
  strongest external datum lives: Marie's ladder measured +14% to +157% output-token
  inflation vs BF16 while accuracy held above 95%, and his Oct 6 update added an agentic
  coding evaluation (kaitchup preview, read this sitting). His GSQ-RCO Coder IQ1_M datum
  (coding accuracy preserved, general knowledge surrendered) is direct evidence that
  quant tolerance is ROLE-conditioned, which is the strongest public argument for a
  per-role rather than global quant policy - but on this box, at 7B janitor scope, the
  measured answer this sitting is: one global Q4 choice is not beaten by any ladder.
- RQ4 (GPU-ladder price triggers): NEITHER FIRED. Trigger 1 (24GB+ Blackwell under
  ~$1200, lens/laws.md:189-191): the only 24GB+ Blackwell consumer card is the RTX 5090
  32GB; Oct 2026 readings: $4,999 new at B&H / $3,822 used on eBay, best new street
  $2,399.90 (PCGuide Oct 6 via search), roughly 136-145% above MSRP (TechPowerUp via
  search; bestvaluegpu page itself 429'd, figures are the search result's quotes of it).
  No 24GB+ Blackwell card is under $1,200. Trigger 2 (used H100 under ~$4,000):
  compute.exchange (read this sitting, article Apr 24 2026, figures late-2025/early-2026):
  used non-refurbished "$15,000-$28,000", market described as tight, only a FORWARD-LOOKING
  10-20% Blackwell pressure claim; Oct 2026 search corroboration: stabilized ~$18-22k
  (GPUnex) / $22-25k (Mercatus). Even the optimistic floor is about 4x the trigger.
  VERDICT: quant-versus-card economics do NOT flip for the RX 5600 XT box; the quant
  ladder (and this A/B's Q4 floor) stays the right lane; re-check the trigger, do not
  assume it.
- RQ5 (2026-10 releases that sharpen/contradict the A/B design BEFORE it fired - it
  fired this sitting, so these bank as post-hoc sharpeeners and next-run design inputs):
  arXiv 2610.00983 "The Devil Is in the Reconstruction Loss Scale" (Oct 1): sequential
  PTQ suffers "Optimization Imbalance" across stages under MSE; RMSE variants fix it via
  "implicit gradient normalization" - i.e. the EXPORTER's loss choices move the artifact,
  which is exactly the export-cast rider's warning (spec leg 6) and justifies the
  recomputed-hash pin this run used. arXiv 2610.06174 "Anosognosia in LLMs" (Oct 5):
  LLMs "fail to self-report their quantization state" while internal representations
  carry method-specific fingerprints - behavioral channels (this A/B's design) are the
  right instrument, and a fingerprint side-channel could later verify which quant a
  deployment ACTUALLY runs (the tag-digest aliasing law's external twin). 2610.04403
  "Saying, Not Knowing" (Oct 3) already held (day-6 bank) independently says the same
  from the eval side: WikiText-2 perplexity does not calibrate quant damage.

## Dedup / overlap ledger (greps run this sitting)

Instrument: `rg -i -l` per key phrase over `catalog/catalog.jsonl`, `memory/`,
`watch/inbox/` (today's run dir excluded), plus the earlier combined grep. Results:

- bnjmn_marie: AUTHOR HELD - catalog/catalog.jsonl has a row and
  frontier_olm_2026-10-02/unconfirmed_bnjmn_marie_20260914.md banks his Sep 14 post
  ("Quantized Qwen3.8 27B for agentic coding: Same Score, 42 Different Outcomes",
  run-variance finding, UNCONFIRMED-as-post-10-01 label dispute). My item is a DIFFERENT
  post (2105481856812740726, Oct 1, the 11-quant accuracy+token-efficiency ladder);
  increment = the ladder numbers, not the author. Relationship stated, not re-banked.
- FIT-GGUF: 0 hits anywhere. NEW.
- "Saying, Not Knowing" / 2610.04403: HELD day-6 (frontier_olm_2026-10-06 sweep files +
  DIGEST). DROPPED from my bank.
- /v1/systemone decision models: HELD day-7 (quantization-compression-hn.md:100-103,
  :183-184 + DIGEST.md:17-18 incl. the b11475 Metal bug). TeksEdge Oct 2 tweet DROPPED
  as a re-bank; it only confirms currency of the day-7 find.
- Muse Glimmer: 0 hits, but RESOLVED OUT-OF-WINDOW (Aug 10) - considered, not banked.
- YouTube "Same Score, Different Answers" / bestvaluegpu: 0 hits. NEW (snippet-tier).
- Qwen3.8 Flash Next (the model): appears in day-4/5 HN-reddit harvests as release
  noise; the Oct 1 ladder POST is the new increment.
- Estate-internal anchors not re-derived: day-7 sweep
  (quantization-compression-x.md items 1-8: JakeKAllDay KV bits, KLD tiers,
  zettelkastten compendium, EVO-X3, Qwen-Image-2.1, Unsloth 500M, Fermonroyh,
  above_spec), VeriLoop ladder, BreadthKV, the 10-03 card's RATIO/STEPQuant/Minima
  banks, and the 2610.07781 four-pinned-choices source (all per
  frontier_olm_2026-10-07/lens/burns.md sections 2a-2b, read this sitting).

## Banked items (strongest first; quotes verbatim from pages fetched this sitting)

See the six items in the submitted register payload; each carries its own overlap note.
Snippet-tier disclosures: item 6 (YouTube) is title-verified only, body never read;
the RTX 5090 price figures in item 3 are the search result's quotes (page 429'd), while
the H100 half of item 3 is a full page read.

## Falsifier / caveats

- The A/B verdict is a CEILING TIE on an easy task mix; it does not certify Q4_K_M for
  harder tasks (quant_ab/RECEIPT.md limitations 1-2).
- fxtwitter degraded (2 of 6 calls timed out); OpenBMB's FIT-GGUF post was never
  resolved - its content is covered via the TeksEdge read of the same announcement.
- arXiv abstracts were read via the export-API listing, not full texts; the two banked
  arXiv items are abstract-level banks, flagged in their confidence.
- No pytest, no lane config change; every web claim above traces to a URL fetched this
  sitting or an explicit snippet/429 disclosure; every run claim traces to a file in
  quant_ab/ written by the commands quoted in the receipt.
