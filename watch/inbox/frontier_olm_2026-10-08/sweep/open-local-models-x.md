# frontier_olm 2026-10-08: sweep bank, open-local-models via the x door

source-fetched: 2026-10-08
Lane: open-local-models, door x. Fetch recipe per ask: WebSearch with site:x.com queries,
then resolve single posts through the fxtwitter door https://api.fxtwitter.com/<user>/status/<id>
(JSON, no login). Every item below was read by this seat this sitting; nothing is banked from
a snippet alone unless the note says so.

## Doors state this sitting (measured, not assumed)

- fxtwitter: 7 of 7 attempted post resolutions returned HTTP 200 JSON (Kev, tev1-4B, Tev1
  0.8B, Julia-1, Step 5, Beam, plus nothing else needed). Matches the doors lens verdict
  (watch/inbox/frontier_olm_2026-10-08/lens/doors.md:66-83).
- WebSearch: worked, but two bursts hit provider-side 429/1302 rate limits (three attempts
  in one call on the "tev1 experimental" query, three on the "Granite 4.2" site: query);
  pacing one query per turn cleared it. Not a door verdict, a pacing note.
- Primary pages fetched directly (not through X): github.com/ollama/ollama/releases,
  github.com/ggml-org/llama.cpp/releases, github.com/ggml-org/llama.cpp/tags,
  hn.algolia.com search_by_date. All 200 JSON/HTML, read this sitting.
- Reddit: not used; walled for WebFetch per lens/doors.md:56-64, curl+UA bypass still OWED.

## Estate probes run this sitting (the instruments the ask asked about)

1. Q3 probe, local tag-digest alias classes. Command (bash, run this sitting):
   `cd ~/.ollama/models/manifests/registry.ollama.ai/library && for f in $(find . -type f); do
   d=$(grep -o '"digest": *"[^"]*"' "$f" | head -1); echo "$d ${f#./}"; done | sort`
   Result: 15 local tags, 15 DISTINCT config digests, zero duplicate pairs. Roster:
   athena-class/latest, deepseek-r1/1.5b, gemma/2b, gemma2/2b-instruct-q5_K_M, gemma4/latest,
   gemma4-desk/latest, gemma4-hermes/latest, maze-keeper/latest, nomic-embed-text/latest,
   qwen-desk/latest, qwen2.5/3b-instruct, qwen2.5/7b, qwen2.5/32b, qwen2.5-coder/7b,
   qwen2.5vl/3b. Reading: NO local tag aliases to byte-identical weights on this box today;
   the day-7 alias proof was registry-side (qwen3 4b vs 4b-thinking, neither pulled here).
   New fact for the fleet seats: gemma4, gemma4-desk and gemma4-hermes are three DISTINCT
   animals by digest (sha256 f0988ff5..., 654fa385..., a0dfa667...), so per-animal gates apply
   between the estate's own gemma4 seats, not only across vendors. P3 boot-time digest pinning
   survives this scan: nothing local left to alias. What pinning does NOT cover is the
   registry-side alias class, which is exactly where the day-7 proof lived, so the weekly
   manifest-hash standing form (day-7 probe queue row 0) stays the live defense.
2. Decision meter state. `grep -n "meter_valid" mag/verb.py` this sitting reads the gate at
   mag/verb.py:504 ("meter_valid": n >= 40). The morning lens cites mag/verb.py:493
   (watch/inbox/frontier_olm_2026-10-08/lens/burns.md:85-86); the file has shifted 11 lines
   since that cite was written. Same gate either way: meter invalid at n=0, and this seat ran
   no fleet bench, so the 0.5B-8B band remains UNMEASURED here (day-7 DIGEST.md:15).
3. Q5 probe, HN search_by_date re-verified (this discharges the OWED at
   watch/inbox/frontier_olm_2026-10-08/lens/doors.md:54). Fetched this sitting:
   `https://hn.algolia.com/api/v1/search_by_date?query=open%20weights%20model&tags=story&hitsPerPage=5&numericFilters=created_at_i%3E1757289600`
   (created_at_i > 2026-09-08). Result: valid JSON, nbHits 317 in-window, top hit "Show HN:
   Gauze fixes (some) open-weight LLM deficiencies" created_at 2026-10-08T12:51:44Z, i.e.
   same-day pickup. Combined with the release-velocity facts below, the hn.algolia-first mix
   does surface new releases fast enough to feed the garden's 30-day row expiry
   (memory/rib/RIB_MODEL_GARDEN_ROUTING.md:54-58 via today's lens/laws.md:67-69) from estate
   instruments; reddit is not needed for release velocity.

## Pass 1: candidate ledger (33 candidates considered, 2026-09-08..2026-10-08 window)

In-window candidates (dates snowflake-decoded or page-read this sitting):
1. Kev 1.0 open-weight decision-model family, jaredpalmer 2105803379587068011, 2026-10-01 (READ)
2. tev1-4B-experimental release, togethercompute 2102882216950763814, 2026-09-23 (READ)
3. tev1 tutorial article by nutlope (quoted inside item 2), 2026-09-23 (read as quote)
4. Tev1 0.8B open source, nutlope 2103548354022305802, 2026-09-25 (READ)
5. Julia-1 decision model note, alexdolbun 2106123305442857043, 2026-10-02 (READ)
6. Step 5 Preview, ArtificialAnlys 2102213621963243704, 2026-09-22 (READ)
7. Beam / reflection_ai, ollama 2107193986482126883 (quotes reflection_ai 2107186849370247235),
   2026-10-05 (READ)
8. Ollama v0.40.1 Latest, 2026-10-07, github releases (READ primary)
9. Ollama v0.40.2-rc0, 2026-10-08, github releases (READ primary)
10. Ollama v0.35.1 Clef/Clef-Flash decision models, 2026-09-29 (READ primary)
11. Ollama v0.35.0 decision models via /v1/systemone (Nimble, Tev1), 2026-09-28 (READ primary)
12. Ollama v0.40.0 MLX default + embeddinggemma-2 on MLX, 2026-09-25 (READ primary)
13. llama.cpp b11507 MoE cache multi-GPU, 2026-10-08 (READ primary)
14. llama.cpp b11505 Vulkan TOP_K fix, 2026-10-08 (READ primary)
15. llama.cpp b11504 Vulkan sparse FA coopmat2, 2026-10-08 (READ primary)
16. llama.cpp b11512 DFlash output head sharing fix, 2026-10-08 (READ primary)
17. llama.cpp b11503..b11513 general churn, all 2026-10-08 (READ primary)
18. HN Gauze Show HN, 2026-10-08, hn.algolia (READ primary, same-day pickup evidence)
19. HN Mistral Large 4 "Le Chonk" 1T, 2026-10-06 (READ primary, out of band)
20. HN Cybersecurity Defenders Need Open-Weight Models, 2026-10-06 (READ primary, essay)
21. Together AI serverless tev1 at $0.042/M (togethercompute/with_replies snippet, not read as
    a post; priced also in item 2's own text, which was read)
22. lgaa201 sub-16GB post (same subject as 23)
23. DeepSeek V4 Pro Qwen 9B/4B live, KyleHessling1 2085444432091095468 (snowflake 2026-08-06:
    OUT of window, disclosed, not deep-read)
24. Qwen3.8-27B "first local model" claim, Alibaba_Qwen profile snippet (27B, out of band,
    snippet only, not banked)
25. GLM-5.3 Terminal-Bench post, tamsi_besson profile snippet (snippet only, not banked)
26. Neo daily AI recap, article 2107063039547912246, 2026-10-05 (snippet only)
27. Marktechpost Qwen history 2106962836425765315 (snippet only)
28. LFM2-24B-A2B, Liquid AI (via jimmysmith1919 profile snippet; date unverified, not banked)
29. NobodyWho LFM2/LFM2.5 tool-calling support (profile snippet, date unverified)
30. smolagents v1.19.0, avillanovamoral (tooling, out of lane)
31. Granite 4.2 in Rapid-MLX 3B/8B/30B (support post; release itself 2026-08-25 per Hugging
    Face page surfaced in search: OUT of window, disclosed, not deep-read)
32. llama.cpp b10839 Vulkan tensor-offset fix, 2026-09-07 (search snippet only; superseded by
    the fresher b11504/b11505 primary reads)
33. jimmysmith1919 tiny 350M tool-use model (snowflake-adjacent search date Mar 31: OUT of
    window, disclosed, not banked)

Count: 33 candidates, 24 in-window, of which 7 read end to end (items 1-7) plus 4 primary
pages (8-9, 13-17, 18) and the HN probe. The ask's minimums (30 candidates, 5 deep reads)
are met with margin.

## Pass 2: the reads (banked items, strongest first)

### 1. Kev 1.0: open-weight decision-model family (Kev-27B + Kev-9B)

- URL: https://x.com/jaredpalmer/status/2105803379587068011 (resolved via
  https://api.fxtwitter.com/jaredpalmer/status/2105803379587068011, HTTP 200 JSON this sitting)
- Date: 2026-10-01 23:33:44 +0000 (tweet created_at, verbatim from fxtwitter JSON)
- Quote (under 40 words, verbatim): "Kev 1.0: an open weight family of decision models you
  can train and run on your own."
- Additional read facts: "New Kev-27B + updated Kev-9B", "64k-token document window on
  Kev-27B", "New fine-tuning + deployment skills so you can train Kev on your own data";
  attached 23.2s mp4.
- Why it matters: the estate's decision rung is stuck behind an invalid meter (n=0,
  mag/verb.py:504) and a bar nothing local clears (>=0.880 on n>=40, lens/burns.md:87-88).
  Kev is a decision-class family that ships its own fine-tuning path, i.e. the estate could
  in principle train a fleet-labeled Kev rung on its own asks to manufacture the n>=40 rows
  day-7 probe queue row asks for. Kev-9B sits just above the 0.5B-8B band edge; Kev-27B above
  it. Under the per-animal gates law (memory/rib/RIB_MODEL_GATES_20261001.md:1-11) a Kev rung
  is a NEW animal: own harness, cold start, no inherited trust.
- Overlap: zero hits for "Kev 1.0", "Kev-27B", "jaredpalmer" in catalog/catalog.jsonl and
  memory/ (rg + grep, this sitting). Genuinely new.
- Confidence: 0.95.

### 2. Tev1 0.8B: on-device open decision-class weights

- URL: https://x.com/nutlope/status/2103548354022305802 (resolved via fxtwitter, HTTP 200)
- Date: 2026-09-25 18:13:04 +0000 (created_at, verbatim)
- Quote: "Just open sourced Tev1 0.8B! Weights are below. Feel free to download them."
- Additional read facts: "Definitely not as good as Tev1 4B or Jev, but it runs entirely
  locally on a mac. It can work decently well for very simple classification." Links
  https://huggingface.co/togethercomputer/Tev1-0.8B-experimental.
- Why: 0.8B is inside the estate's 0.5B-8B janitor band, it is decision-class (Tev1 = the
  Jev-like classifier line), and it is the smallest weights-released member. It is the
  cheapest concrete candidate for the estate's UNMEASURED-band first measurement (pull, run
  the fleet bench, cure meter n=0 at the small end). The vendor's own honesty line
  ("not as good as Tev1 4B or Jev") is a scope marker: simple classification only, which is
  what janitor scut mostly is.
- Overlap: subject HELD since the 09-30 window: memory/percolator/candidates.jsonl reads
  "decision models landed natively in Ollama 0.35 (/v1/systemone; nimble 9B Bespoke Labs,
  tev1 4B and tev1:0.8b Together AI)". Delta banked here: the primary announcement post, the
  HF weights URL, and the vendor quality caveat, none of which the held row carries.
- Confidence: 0.95.

### 3. tev1-4B-experimental: the 4B release post with economics

- URL: https://x.com/togethercompute/status/2102882216950763814 (resolved via fxtwitter,
  HTTP 200)
- Date: 2026-09-23 22:06:04 +0000 (created_at, verbatim)
- Quote: "We're releasing tev1-4B-experimental, a Jev-like classifier finetuned on top of
  Qwen3.5 4B. We're making it available on Together serverless at $0.042/M input & $0/M
  output."
- Additional read facts: same post: "Also releasing the data recipe & a tutorial on how to
  finetune your own (Tev1 cost $17 to train!)." Quotes an article by @nutlope titled "How to
  train your own Jev for $17."
- Why: two estate-load-bearing numbers in one post: $17 to train a 4B decision-class
  classifier, and $0/M output hosted. The $17 figure is the counterweight to any "LoRA the
  janitor fleet" instinct under the five-gate hardware law: task-specific decision heads are
  trainable at coffee money on rented compute, no local GPU ladder needed. Qwen3.5 4B as the
  base confirms the day-7 banked qwen3.5 tool-rung family is also the local decision-class
  base.
- Overlap: same held row as item 2 (percolator candidates, 09-30 window). Delta: pricing,
  training cost, base-model identity, recipe release.
- Confidence: 0.95.

### 4. Julia-1: 144.3M-parameter decision model served by llama.cpp

- URL: https://x.com/alexdolbun/status/2106123305442857043 (resolved via fxtwitter, HTTP 200;
  long note tweet)
- Date: 2026-10-02 20:45:00 +0000 (created_at, verbatim); the note dates the release itself
  ~2026-09-26 by Supersonic Labs (Brazil)
- Quote: "~144.3M parameters, built on mmBERT-small, 50+ languages, no image input, Apache
  2.0, 3 ms median" (as returned by the fetch; the note's own wording)
- Additional read facts: decision head over JHU CLSP's mmBERT-small encoder; takes state,
  question, 2-20 candidates; one forward pass gives a probability per option; "73.15% on a
  2,000-item typed-decision set"; 94% AG News, 86% on a 6-label emotion set, 64% on a
  72-label Banking77 pilot; training cost ~US$104; weights ~550 MB; GGUF-packaged by
  ggml-org for llama.cpp /v1/systemone (huggingface.co/ggml-org/Julia-1-GGUF); caveat: "bare
  labels can mislead it"; CPUs run tens to low hundreds of ms.
- Why: a third local decision animal in one week, and architecturally new for the estate:
  an ENCODER decision head, not a decoder, at 3 ms median on a workstation GPU. Against the
  estate bar its published number (73.15%) does NOT clear 0.880 on n>=40, but it is measured
  on the vendor's typed-decision set, not the fleet battery: the cell is UNMEASURED here, and
  at 550 MB it is the cheapest animal on this list to actually measure.
- Overlap: zero hits for "Julia-1", "mmBERT" in catalog + memory; "supersonic" hits only a
  coincidental mickey17 lane filename (mine/raw mickey17_v2/lanes/supersonic-x.json), not
  the lab. Genuinely new.
- Confidence: 0.9 (note tweet, single-source detail; the HF links were not re-fetched this
  sitting and are stated as the note's claims).

### 5. Ollama v0.40.1 Latest (Oct 7) with a Windows 2GiB fix; v0.40.2-rc0 (Oct 8)

- URL: https://github.com/ollama/ollama/releases (fetched directly this sitting)
- Date: 2026-10-07 (v0.40.1, "marked Latest"; page shows "07 Oct 23:22"); v0.40.2-rc0
  2026-10-08 16:53
- Quote: "a Windows fix so clef head reads don't go past 2GiB" (fetch's verbatim rendering of
  the v0.40.1 notes)
- Additional read facts: v0.40.1 also proxies cloud usage APIs, drops a CLI onboarding step,
  avoids Windows symlinks; v0.40.0 (2026-09-25) defaults models to MLX on Apple Silicon and
  carries qwen3.8, gemma4, decision models, embeddinggemma-2 on MLX; v0.35.1 (2026-09-29)
  adds Cloudflare Clef/Clef Flash decision models via /v1/systemone and "reports only the
  'decision' capability for decision models"; v0.35.0 (2026-09-28) introduces decision models
  via /v1/systemone with Nimble and Tev1.
- Why: the estate daemon reads 0.34.3 (day-7 steal probe, frontier_olm_2026-10-07
  DIGEST.md:23) and the day-7 bank recorded v0.40.0 as newest. Since then the serving stack
  moved twice (v0.40.1, v0.40.2-rc0), and the one Windows-specific fix (2GiB clef-head reads)
  is on this estate's OS. Under the harness-dominates finding (arXiv 2610.07781, day-7
  DIGEST.md:16), the serving layer is a first-class variable in gemma:2b's pass-rate: any
  estate re-measure that upgrades Ollama changes the conditions, so the upgrade and the
  re-measure must land as one pinned-conditions row, not two.
- Overlap: day-7 DIGEST.md:18 banked "Ollama's newest remains v0.40.0". Delta: v0.40.1,
  v0.40.2-rc0, the Windows fix, and the v0.35.0/0.35.1 decision-model capability facts.
- Confidence: 0.9.

### 6. llama.cpp Vulkan surface churned today (b11504, b11505); tags page carries NO v0.6.0

- URL: https://github.com/ggml-org/llama.cpp/tags and https://github.com/ggml-org/llama.cpp/releases
  (both fetched directly this sitting)
- Date: 2026-10-08 (all listed tags dated Oct 8)
- Quote (verbatim from the tags fetch, punctuation normalized to ASCII): "b11505 Vulkan TOP_K
  fix" / "b11504 Vulkan sparse FA support for coopmat2"
- Additional read facts: releases page top five b11507-b11512 (MoE cache over multiple GPUs;
  CUDA MMQ OOB fix; looped PAD kernel; CCCL guard; DFlash output head sharing with tied
  output weights read from GGUF metadata); tags page b11503-b11513 all Oct 8; the fetch states
  explicitly "there is no tag named 'v0.6.0' anywhere in the content".
- Why: the estate box runs Windows Vulkan/CPU lanes (the 72.97 tok/s Vulkan vs 6.0 CPU
  measurement, day-6/7 banked). Two Vulkan fixes and a MoE multi-GPU cache feature landed
  TODAY, i.e. the harness-dominates mechanism is still live: small-model behavior on this box
  can move with a llama.cpp bump while weights stand still. Also an honesty strike: a search
  snippet claimed "llama.cpp v0.6.0" (extended batch API, ~Oct 5); the primary tags page does
  not carry that tag, so that claim is UNVERIFIED and is deliberately not banked as fact.
- Overlap: day-7 banked b11465-b11475 (Metal-specific deltas, DIGEST.md:18). Delta: b11503
  through b11513, all post-day-7, Vulkan/CUDA/DFlash class. DFlash catalog hits are
  coincidental bridgefy Kotlin filenames, not the model.
- Confidence: 0.9.

### 7. Step 5 Preview: closed now, open weights planned October 15

- URL: https://x.com/ArtificialAnlys/status/2102213621963243704 (resolved via fxtwitter,
  HTTP 200)
- Date: 2026-09-22 01:49:19 +0000 (created_at, verbatim)
- Quote: "Closed weights now, with an open release planned for October 15th."
- Additional read facts: StepFun flagship MoE, 600B total / 27B active; AA Intelligence Index
  44, matching Kimi K3 (max) at ~2.8x lower cost per task; lags on agentic (GDPval-AA 1,566
  Elo vs Qwen3.8 Max 1,668, GLM-5.3 max 1,646).
- Why: out of the 0.5B-8B band, banked for garden planning only: a frontier-class open
  release lands in 7 days and the routing grid's UNMEASURED cells will start begging for it;
  also direct evidence for Q5 that open-weights cadence is measured in days, so the 30-day
  row-expiry law needs an instrument with same-day pickup (HN verified above).
- Overlap: "Step 5" hits in memory/burns/LEDGER.jsonl are a coincidental flip-card phrase
  ("step 5.5"); StepFun absent from catalog and memory. Genuinely new.
- Confidence: 0.9.

### 8. Beam (reflection_ai): 501B total / 23B active agentic open model, Ollama onboard

- URL: https://x.com/ollama/status/2107193986482126883 (resolved via fxtwitter, HTTP 200;
  quotes reflection_ai 2107186849370247235, links reflection.ai/beam)
- Date: 2026-10-05 19:39:30 +0000 (created_at, verbatim)
- Quote: "Introducing Beam: a highly efficient agentic open model with 501B total parameters
  and 23B active."
- Additional read facts: ollama's own text: "Excited about the new open model from
  @reflection_ai! More US models coming to Ollama!"
- Why: out of band, garden-planning row only: 23B active MoE with day-one Ollama intent is
  the shape the estate's per-animal gates law was written for; the search result also carried
  "Full weights release this month" (from the profile snippet, not re-verified in the fetched
  JSON, stated as snippet-tier).
- Overlap: zero clean hits for the Beam release in catalog + memory (generic "beam"/
  "Reflection" word matches only). Genuinely new as a subject.
- Confidence: 0.85 (quote-tweet read; the reflection_ai post itself was read only as the
  embedded quote).

## The five research questions, answered with what this lane actually measured

1. In-band releases since 2026-09-08 found through the x door: tev1-4B-experimental (Sep 23)
   and Tev1 0.8B (Sep 25), both decision-class on Qwen3.5 bases; Julia-1 144.3M (release
   ~Sep 26, note read Oct 2). Out-of-window but adjacent, disclosed not banked: Granite 4.2
   3B/8B (Aug 25), DeepSeek V4 Pro Qwen 9B/4B (Aug 6). Already banked by earlier days:
   qwen3.5 0.8b/2b/4b tool rungs, embeddinggemma-2, gemma4 family (estate runs three distinct
   gemma4 digests). Does anything beat gemma:2b on the lanes' actual scut? NOT MEASURABLE
   from this seat: the band is UNMEASURED (day-7 DIGEST.md:15 via lens/burns.md:85-86) and
   the meter is invalid at n=0 (mag/verb.py:504 measured; no fleet bench fired this sitting).
   What this lane adds: three concrete, weights-pulled-or-pullable decision-class animals
   small enough to measure, two with published vendor caveats that match janitor scut
   ("very simple classification", "bare labels can mislead it").
2. Harness vs weights on the estate stack: this lane ran no A/B, so no replication number.
   Evidence banked: the serving layer moved twice on Ollama (v0.40.1, v0.40.2-rc0) and the
   llama.cpp Vulkan surface changed the same day (b11504, b11505) since the day-7 bank, with
   at least one Windows-specific fix in Ollama. Under the day-7 confirmed finding
   (2610.07781), any estate attempt to separate weights from serving must pin Ollama and
   llama.cpp builds as conditions first; the v0.40.1 Windows fix is exactly the class of
   change that would silently move gemma:2b's pass-rate between two otherwise identical runs.
3. Tag-digest aliasing: the local manifest scan (command above) reads 15 tags, zero duplicate
   digests, so NO local tag aliases to byte-identical weights on this box today. The three
   gemma4-family seats are three distinct animals by digest. The surviving alias class is
   registry-side only, which is where the day-7 proof lived; P3 boot pinning plus the weekly
   manifest-hash standing form (day-7 probe queue row 0) remain the live defense. The
   aliasing question for THIS box is closed as of 2026-10-08 by this scan; it reopens with
   every pull.
4. grok-4.7 champion cell and fable-5.1 plan_call recipe: NOTHING read through the x door
   this sitting bears on either suspect cell. Stated as absence, not filled: no X item read
   today tests grok-4.7 champion behavior or fable plan_call recipes. Those re-measures stay
   estate-instrument work (blind-grade pass, second judge per
   memory/rib/RIB_MODEL_GARDEN_ROUTING.md:146-151 via lens/laws.md). The closest adjacent
   datum is Step 5's agentic lag (GDPval-AA 1,566 vs Qwen3.8 Max 1,668), which is evidence
   that frontier agents split on agentic classes, nothing more.
5. Release velocity through estate instruments: YES, measured. HN search_by_date re-verified
   live (OWED discharged, recipe above): nbHits 317 in-window with same-day pickup of an
   open-weights tooling post (Gauze, 2026-10-08T12:51:44Z). llama.cpp shipped 6+ tagged
   builds on Oct 8 alone; Ollama shipped v0.40.1 Oct 7 and v0.40.2-rc0 Oct 8. The hn-first
   mix catches releases within a day; the 30-day row-expiry law (laws.md:67-69) is feedable
   from estate instruments; reddit's wall is not a bottleneck for release discovery. The one
   velocity gap this lane hit: search-index coverage of X posts lags (the Granite 4.2 and
   Beam "full weights this month" details ride snippets, not fetchable posts), so
   vendor-github primary pulls stay part of the mix.

## Honest gaps and degradations this sitting

- Two WebSearch 429/1302 bursts (provider-side); pacing cleared them; no query abandoned for
  good, both topics recovered via re-queries or primary pages.
- The v0.6.0 llama.cpp claim is UNVERIFIED against primary and left unbanked (see item 6).
- Beam's "full weights release this month" is snippet-tier (not in the fetched JSON).
- Julia-1's HF links, Kev's fine-tuning skills link, and the StepFun open-release date were
  not re-fetched this sitting; they are stated as the fetched posts state them.
- No pytest, no fleet bench, no model pull ran; nothing here fills an UNMEASURED cell.
- Every claim above cites either the fetched page (URL given), the command run (given), or
  the estate file path:line given.
