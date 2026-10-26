# SWEEP: open-and-local-language-models via X (area 6 of 8)

- Seat: sweep-open-and-local-language-models-x (Mag Resource Harness)
- Moment: 2026-10-02, this sitting
- Stamp: source-fetched: 2026-10-02 (every banked item was fetched and read this sitting)
- Doors used: WebSearch site:x.com (z.ai web_search_prime proxy; ~half the queries came back
  MCP 1302 rate-limit errors, retried until answered, never fabricated around), fxtwitter JSON
  via curl (recipe from lens/doors.md Door 4; WebFetch was known-dead on this host so curl was
  used from the start), hn.algolia.com API via curl and WebFetch, ollama.com/blog via WebFetch,
  direct curl door probes for PullPush / arctic-shift / redlib mirrors, and one local
  instrument (`ollama --version`).
- Anti-rebank honored: new confirmed finds below are post-10-01 or carry a genuinely new
  primary (new post id, new vendor page, new instrument run). Overlap is stated per item.

## RQ verdicts

### RQ4 (Ollama 0.35 91 ms/decision): feature verified, number stays single-source, OWED a local measurement

Three independent legs landed this sitting:

1. VENDOR PRIMARY (fetched via WebFetch, ollama.com/blog): "Ollama now supports Jev-style
   decision models" dated September 29, 2026. Exact quotes pulled from the page:
   "Ollama now supports decision models, based on TypeSafe's Jev API for fast, typed
   decisions." and "Decision models answer yes-or-no questions, choices and scores about it,
   with a probability for every option." The vendor page contains NO latency figure, NO
   Nimble/Tev1/Winnow names, and no "0.35" version number in the post title. The 91 ms number
   does not exist on the vendor primary.
2. INDEPENDENT MEASURED SECONDARIES (both resolved end to end through fxtwitter curl):
   - jurbed (Sep 30 2026, status 2105367765137969545, read in full): benchmarked the 0.35
     decision models on 718 test items; Nimble 9B caught 81 pct of attacks vs Jev-on-Venice
     89 pct, and blocks only 63 pct of instructions planted in ordinary emails vs Jev 92 pct.
     He measures ACCURACY, not latency. Verdict from his own bench: he keeps the cloud gate.
   - mertcobanov (Oct 1 2026, status 2105650451546800604, read in full): ran "ollaya 0.8.0"
     and "ollama 0.35.0" on the SAME RTX 5090 over Bespoke Labs' public benchmark (3,880
     human-labeled questions, 13 subsets, scored by bespoke's own code over HTTP per
     question). Search-result snippet of the same thread: winnow 0.773 accuracy at 60 ms per
     question, nimble best-of-ollama 0.749 at 210 ms.
   - Third latency datapoint (HN search hit, objectID 49800531, Sep 22): "Show HN: Gemma 3 4B
     as a typed decision function in Rust (47 ms/decision)". Title only; thread not opened.
3. LOCAL INSTRUMENT (run this sitting): `ollama --version` -> "ollama version is 0.34.3";
   `curl http://localhost:11434/api/version` -> status 200. The estate's own Ollama is one
   minor version short: /v1/systemone cannot exist locally until 0.35 is installed, so the 91
   ms claim can neither be confirmed nor refuted on estate hardware today.

Verdict: the decision-model FEATURE is real (vendor primary, Sep 29). The 91 ms/decision
number remains a single X account's M5 Max measurement, contradicted in generality by the
RTX 5090 rig's 210 ms for the same model. Under the instruments-only law the number is OWED
an estate measurement after an 0.35 upgrade; until then treat "91 ms" as one rig's datum, not
a law. This also lands the 10-01 steal card "Ollama 0.35 systemone port" on real ground: the
upgrade is the prerequisite step.

### RQ1 (janitor/worker slots and the Ling radar line)

- Gemma: NO post-10-01 Gemma release or license change found. HN 30-day filter
  (created_at_i > 1788364800, i.e. after Sep 2 2026) returned 122 gemma story hits; the top
  10 are all project showcases, none is a release or license announcement. X-side Gemma
  searches were rate-limited (1302) on repeated attempts; the hits that did come back date
  the Gemma 4 12B launch to earlier (vLLM day-0 post, out of window). The janitor KEEP
  verdict (burns.md:104-106) stands unthreatened by anything found.
- In-window touch on the worker slot: ddalcu (Oct 1 2026, status 2105683218548559919, read in
  full): MLX-Serve 26.10.1 ships speed across the board, "Gemma 4, Qwen, LFM2.5, Spark,
  Bonsai 2 all faster, output byte-identical to 26.9.6 (across 18 models)", plus a new
  experimental path where GGUF models run on their own Zig+Metal MLX engine instead of the
  llama.cpp fallback, and drafting on by default. Apple-Silicon serving only; no license or
  weights change.
- Ling radar line: the AntLingAGI announcement (Sep 30 2026, status 2105335205741596911,
  resolved and read in full) says verbatim: "Meet Ling-3.1-flash: ~560B total params, ~25B
  active/token, up to 1M-token context. We plan to open-source the model soon." So the
  ~560B/25B-active radar line is CONFIRMED as announced but its weights are NOT out; second-
  aries (benchlm.ai, aiweekly.co, orcarouter.ai via search snippets) describe a three-stage
  rollout: free 256K trial, paid 1M service, open weights last. Meanwhile the SAME vendor
  already ships open weights one rung down the line: Ling-3.0-flash 124B/5.1B-active
  (BF16 + FP8) and Ling-3.0-tiny 7.9B/1.3B-active (25 on the Artificial Analysis index), per
  the InclusionAI and ArtificialAnlys posts surfaced in search. The radar line's actionable
  rung today is 3.0-flash/3.0-tiny, not 3.1-flash.

### RQ2 (Qwen small-model supply drying): nuanced confirmation, one misattribution corrected

- CONFIRMATION (new primary, HN item 49747925 "Qwen 3.8 Omni Flash", 346 points, Sep 17
  2026, full thread fetched as 76.8 KB JSON and walked): user vinzenzu: "Qwen 3.8 Max was
  open-weight released, as was Qwen 3.8 Flash Next. I still agree that they aren't as
  aggressively releasing the open-weights models as before, but there hasn't been a major
  release they haven't published the weights for yet afaik" (links to
  huggingface.co/Qwen/Qwen3.8-2.4T-A95B). In-window, and it sharpens the trend: the drying is
  in cadence and hosted small tiers, not in total weight cessation.
- CORRECTION: the search layer claimed the same thread says "Flash Lite getting discontinued
  in October". Reading the actual comment (user testycool): "I had a production image
  processing using Gemini 2.5 Flash Lite (which is getting discontinued in October)". The
  October discontinuation is GOOGLE's Gemini 2.5 Flash Lite, NOT Qwen. The prior summary was
  a misattribution; struck here so it does not propagate.
- Out-of-window context carried, not banked as new: Qwen Code OAuth free tier discontinued
  2026-04-15 (qwenlm.github.io docs via search snippet); alex_prompter's Qwen3.5-0.8B/2B/4B/9B
  mass drop is dated Mar 2 2026, outside the window.
- Substitutes in the narrow regimes: the same HN thread gives the local-serving regime data:
  Qwen3.8 Flash Next needs ~128 GB and DDR5 to be quick (one user: ~25 t/s on an old gaming
  box, "very strong, even at 3 bit quant"; another: RTX 4090 + DDR5 about 30 t/s, $3000-class
  setup); Qwen3.8 27B "relatively easy to run"; llama.cpp support for Flash Next still WIP
  (Iolaum). Plus the ddalcu Oct 1 MLX-Serve speedups (+66 pct Qwen3.8 27B with drafter on
  M5 Ultra). For the estate's narrow regimes the honest substitute remains gemma4 + typed
  decision endpoints, not a hosted Qwen small tier.

### RQ3 (the olm-x free rung before Oct 7): worth the probe slot; one new lane candidate with a conflict

- ZCode (@zcode_ai, official account, via search snippet): "That's Round 3: 100M free
  GLM-5.3-Flash tokens, 10,000 more packs." The free rung is actively being re-upped, not
  wound down, going into the Oct 7 close.
- Independent quality evidence (HN item 49747925 thread): user Systemerror7A69 starts on
  "a relatively cheap model (GLM 5.3 flash for me)" and stays; user alfiedotwtf: "GLM-5.3
  Flash has been my goto since it came out. Only failed once when it lost context"; user
  barrenko routes image-based PDF pages to glm flash 5.3. Three independent users treating
  the model class as a reliable cheap workhorse is the confirmation that the probe slot buys
  real inference, not a toy.
- NEW LANE CANDIDATE with a measured conflict: nahid_pro09 (Sep 22 2026, status
  2102390398685716740, read in full): "MiMo V2.6 Flash & DeepSeek V4.1 Flash are 100% FREE
  right now in token harbor" with openAI-compatible base URL and :free model ids. But the
  estate's own 09-25 quote-audit concat (memory/runs/quote_audit_wide_20260925/
  inbox_concat.txt, byte-checked this sitting) recorded "tokenharbor has no DeepSeek at all".
  Instrument run this sitting: GET https://tokenharbor.ai/v1/models -> 401 {"error":{"message":
  "Invalid or revoked API key...","code":"invalid_api_key"}}; the /api/v1/models path 404s
  into an HTML shell. So the host is alive, the API door exists, the free-roster claim is
  unverifiable without an account, and the roster is demonstrably unstable (Sep 22 post vs
  Sep 25 audit). Worth one keyed probe only if the estate already holds or cheaply mints a
  token; not worth an account mint on today's evidence.

### RQ5 (reddit fallback doors): arctic-shift is the live one, paced; PullPush alive but hostile; redlib dead from this network

Exact commands and outputs, all run this sitting:

- arctic-shift.photon-reddit.com: `curl -sS -m 25 ... "https://arctic-shift.photon-reddit.com/
  api/posts/search?subreddit=LocalLLaMA&limit=2&sort=desc"` -> status 200, 19,703 bytes, valid
  JSON with fresh posts (ids 1wvxpvh "Alternative to Nvidia spark?" and 1wvxph8 "New benchmark
  on LMs fixing bugs before users run into them", created_utc 1790957158/1790957134 = today).
  But it rate-throttles hard: the immediate second call and a 20-second-later retry both
  returned 422 with body {"data":null,"error":"Timeout. Maybe slow down a bit"}. Working
  recipe: ONE arctic-shift query per cooldown window of a minute or more; a title= filter
  never got through the throttle in three tries (the qwen title-search stayed 422).
- PullPush: `curl -sS -m 25 ".../reddit/search/submission/?subreddit=LocalLLaMA&size=2&sort=desc"`
  -> 429 (191 bytes), retried minutes later -> 429 again. Host alive, answers every time, but
  it is rate-limiting this network IP on the search path. Not a working fallback today.
- redlib mirrors, five probed: redlib.perennialte.ch -> 403 (5,554 bytes; still 403 with a
  full Chrome UA); redlib.private.coffee -> 307 then 403 with a __goaway_challenge anti-bot
  cookie page; libreddit.privacydev.net -> 502; redlib.catsarch.com and
  redlib.privacyredirect.com -> TLS handshake failure (schannel SEC_E_UNSUPPORTED_FUNCTION,
  status 000); redlib.arcnore.dev -> DNS resolution failure (curl exit 6). Verdict: the
  redlib fallback row in the doors map is dead from this network and should be downgraded in
  lens/doors.md.
- The primary r/LocalLLaMA JSON door stays auth-walled per doors.md (302 reason=lor2, not
  re-probed this sitting; no new instrument, so no new claim).

## Candidate census (Pass 1)

36 candidates considered from the last 30 days (or as door probes): jurbed main + follow-up
posts, AntLingAGI 3.1-flash announcement, InclusionAI Ling-3.0-flash/3.0-tiny weight posts,
ArtificialAnlys Ling 3.0 Flash and Tiny posts, shawnchauhan1 Ling pricing post, benchlm.ai /
aiweekly.co / orcarouter.ai Ling secondaries, zahareus 91 ms post (original claim, id still
unresolved), ethereaglehq systemone post, mertcobanov RTX 5090 bench, AI Top 20 Sep 30
article, lmoroney and Michael47242613 Ollama posts, ollama.com vendor blog, ddalcu MLX-Serve,
wtogami Qwen3.8-Flash pricing, soumithchintala Qwen 3.5 on Tinker, jacksmies Qwen usage,
nahid_pro09 tokenharbor, Ray Fu free-API article, zcode_ai Round 3, EvoLink FlashX/Oct 6
discounts, hanrui_w Nebius day-one, Routeway unified API, HN items 49737236 (Open-jev),
49879676 (Gevva0), 49800531 (Rust typed decision 47 ms), 49897153 (640 tok/s megakernel),
the 122-hit HN gemma 30-day listing, HN item 49747925 (Qwen 3.8 Omni Flash thread), plus
instrument runs: ollama version check, tokenharbor probes, arctic-shift/PullPush/redlib
probes. Out-of-window items (alex_prompter Mar 2 Qwen3.5 drop, vLLM Gemma 4 12B day-0,
emollick Gemma posts) were read only as context, never banked.

Pass 2 deep reads (end to end, 8 total): jurbed, AntLingAGI, nahid_pro09, mertcobanov,
ddalcu (all via fxtwitter curl, full tweet JSON parsed), ollama.com/blog (WebFetch, full
page), HN item 49747925 (76,864 bytes JSON, all comments walked), HN gemma 30-day listing.

## Overlap ledger

- catalog/catalog.jsonl (871,790 lines): 0 hits for "Nimble|Tev1", "Ollama 0.35",
  "Ling-3.1", "InclusionAI", thread id 1wrez7j, "MLX-Serve", "tokenharbor", "systemone";
  7 hits for "PullPush|arctic-shift|redlib" (the doors-lens fallback map, mapped but never
  run before this sitting); 503 lines mention gemma (estate-core, expected).
- memory/: "Nimble|Tev1" in 5 files (memory/agent_sessions/orc-t*.json x2,
  memory/continuity/seat_memory_20260927/*.md x3, all 10-01-fold residue);
  "Ling-3.1" in memory/trajectory/steps.jsonl (10 hits, the radar row);
  "PullPush" in 5 files incl memory/runs/gapwave/hn_x_fanout/corpus_sources.md;
  "tokenharbor" in memory/runs/quote_audit_wide_20260925/inbox_concat.txt (4 occurrences,
  byte-checked: the 09-25 audit's "tokenharbor has no DeepSeek at all") and in
  memory/trajectory/steps.jsonl (this sitting's own command log).
- Nothing banked below re-confirms a section-2 burns.md row without naming the delta.

## OWED (carried, not asserted)

1. The 91 ms/decision number: OWED an estate measurement on estate hardware after an
   Ollama 0.34.3 -> 0.35 upgrade. Nothing here upgrades the claim to law.
2. The zahareus original 91 ms post id: never resolved (search snippets carried the claim;
   the post itself was not opened). Two attempts via search did not surface the status id.
3. tokenharbor free roster: OWED a keyed probe (model list with a real token) before the
   MiMo/DeepSeek :free claim is believed; today's evidence (Sep 22 post vs Sep 25 audit
   conflict) says the roster moves.
4. Ling-3.1-flash open weights: OWED a watch (the vendor says "soon"; no date). When it
   lands, it re-opens the radar line's routing cells.
5. arctic-shift title-filtered search: OWED a paced retry (the throttle beat three tries);
   the Qwen-supply post census inside r/LocalLLaMA is unfinished.
6. The search-layer 1302 rate limits on site:x.com queries (roughly every other query):
   several Gemma-specific X searches never returned; the null result on post-10-01 Gemma
   news is backed by the HN 30-day filter and by the X hits that did answer, not by an
   exhaustive X census.
