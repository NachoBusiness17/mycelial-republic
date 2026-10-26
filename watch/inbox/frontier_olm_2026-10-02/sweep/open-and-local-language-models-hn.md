# Sweep: open-and-local-language-models via HN (frontier_olm 2026-10-02)

source-fetched: 2026-10-02
seat: sweep-open-and-local-language-models-hn (Mag Resource Harness)
doors: hn.algolia.com API via WebFetch (recipe per lens/doors.md Door 2), news.ycombinator.com item
pages, curl cross-checks (api.pullpush.io, arctic-shift.photon-reddit.com, api.fxtwitter.com per
the doors-lens recipe), one serial WebSearch. Every banked quote below was read this sitting.

## Instruments run (exact)

- 9 Algolia queries (search_by_date + search relevance), numericFilters created_at_i>1788220800
  (2026-09-02): queries gemma, qwen, ollama, "open weights", olmo, "local llm", gemma+google,
  "ling model", "olm-x". Candidate rows considered pass 1: 50+ distinct HN items (junk included);
  nbHits per query logged in the transcript. "olm-x" = nbHits 0.
- HN item pages fetched: 49934323, 49908997.
- Primaries read end to end (pass 2, 10 reads): huggingface.co/blog/ggml-org/
  decision-models-in-llamacpp; ollama.com/blog/ollama-now-supports-jev-style-decision-models;
  github.com/zozo123/gemma-to-jev; mac-mini-m4-doc.masterfabric.co; lottia.net/notes/
  0020-increasingly-sandboxed-qwen.html; artificialanalysis.ai ant-group Ling-3.0-flash-Fin
  article; github.com/jaredpalmer/kev; huggingface.co/kouhxp/gutsy; tomshardware PewDiePie Ajax
  article; StepFun tweet full text via api.fxtwitter.com (curl 200, 4509 bytes).
- curl probes: `curl -sS -m 30 -A "mag-frontier-probe/1.0" "https://api.pullpush.io/reddit/
  search/submission/?subreddit=LocalLLaMA&size=2"` -> status:429, body "Rate limit exceeded.
  This website does not provide free scraping resources for agents."; arctic-shift
  /api/posts/search?subreddit=LocalLLaMA&limit=2 -> 200 (19,703 bytes, rows 1wvxpvh +
  1wvxph8 both created 2026-10-02T16:05Z), but adding `&title=qwen` -> 422 body
  {"data": null, "error": "Timeout. Maybe slow down a bit"} (also 422 once on a bare repeat:
  flaky, use serial spaced calls, subreddit+limit only); safereddit.com/r/LocalLLaMA -> 200
  but 4,361 bytes containing a challenge page (Cloudflare, matches the 10-01 note);
  redlib.catsarch.com -> Windows curl schannel TLS failure status:000, and WebFetch ->
  HTTP 429.
- Local instrument: `ollama --version` -> "ollama version is 0.34.3" (0.35 NOT installed;
  C:\Users\foste\AppData\Local\Programs\Ollama\ollama.exe).

## Research question verdicts

Q1 (gemma slots / Ling radar, post-10-01): NO post-10-01 Google Gemma release or license-change
story found on this door (gemma relevance query, nbHits 145, top post-10-01 hit is a namesake
apartment matcher). What IS new for the worker slot: gemma4:26b is a 25.2B-param MoE with ~4B
active per token (banked below, Gemma 4 26B item) - the first time the estate holds a concrete
variant identity for the "gemma4" worker line. Ling-3.1-flash: no post-10-01 story on HN
(nbHits 0 for olm-x, no Ling story after 10-01 in any query); the banked 10-01 radar row
(register line 6, "weights open-sourcing soon") is still the latest. Nearest in-window radar
parallel: StepFun Step 5 Preview, 600B/27B-active, open weights Oct 15 (banked below, full
tweet text via fxtwitter - a genuinely new primary; catalog StepFun hits are step-3.7 only,
memory/plans/XMODEL_BURN_20.md tracks step-3.7, not Step 5).

Q2 (Qwen supply-dry confirmation + substitutes): NO post-10-01 confirmation found. The 09-30
banked thread (r/LocalLLaMA 1wrez7j) remains the latest supply-dry evidence; serial WebSearch
found no newer thread (first sub-call 429/1302'd, second returned none). What the door DID
show: the small-Qwen supply line is actively used in the wild post-09-30 - gutsy-0.8b
(fine-tuned from Qwen3.5-0.8B), Kev-0.8B/4B/9B (Qwen3.5 bases, Apache-2.0), PewDiePie's Ajax
(Qwen3.5-9B fine-tune, Tom's Hardware 10-02). Substitutes in the narrow regime where
small-model-with-tools wins (model_garden/DUMB_AGENT_FRONTIER_DIG.md verdict): the typed
decision-model family is now the strongest substitute class - 144M to 27B, llama.cpp-native
(llama.cpp blog, banked item 1), CPU-runnable at 0.8B (gutsy), 47 ms/warm on an M1 Pro at 4B
(gemma-to-jev). Caveat banked with gutsy: on CPU its JevBench hard tier runs 4.2 s median -
decision models are fast on GPU, slow on long-policy CPU states.

Q3 (olm-x free rung before Oct 7): HN carries nothing ("olm-x" nbHits 0). From our own bytes:
the rung is GLM-5.3-Flash free on ZCode, discovered via a promotional X post (@nahid_pro09,
"GLM-5.3-Flash is 100% FREE with UNLIMITED usage right now on ZCode (Extended)"), explicitly
NOT an official z.ai page (09-30 register line 15 + DIGEST:75, OWED-1..4 open). Worth a probe
slot? As a workflow lane: no - commit af3336029 measured the offpeak-idle plan DEAD for
workflow subagents (7/7 lanes failed, chat-only), and DeepSeek off-peak is the live free lane
(lens/burns.md:104-106). As a chat-surface rung through Oct 7: keep, costs nothing, but its
verification OWEDs (official-page confirmation, billing-side terms) are still open and this
sweep did not spend on them.

Q4 (Ollama 0.35 91 ms/decision Nimble/Tev1 verification): STATUS UNCHANGED - single-source.
The verbatim claim, now with its conditions from the primary itself: "Nimble 9B averaged 91ms
per decision in the Pac-Man example below when running locally on an M5 Max." Its accuracy
context is "Mean accuracy across 13 public data sets with human labels, covering 3,880
decisions" with NO figures published (matches the 10-01 OWED). Second primary for the CLASS
yes, for the NUMBER no: llama.cpp's decision-models post (banked item 1) publishes its own
median table (Julia-1 3 ms, Laya 5 ms, Kev-4B 12 ms, lev 36 ms, OpenJev 43 ms, one RTX PRO
6000) and never mentions Nimble or Tev1; gemma-to-jev gives 47 ms/warm on an M1 Pro with Gemma
3 4B; Kev-4B does six questions in 41.5 ms on an L40S (corpus/library/kev model cards, already
held, re-read this sitting). HN thread 49908997 has zero comments; 49934323 has one (pointing
to gutsy). Local instrument check: 0.34.3 installed, /v1/systemone needs 0.35, so the estate
cell stays EMPTY per the instruments-only law (memory/rib/RIB_MODEL_GARDEN_ROUTING.md:48-53);
the quiet-window upgrade + three-arm bake-off steal card (10-01 DIGEST:127) is still the named
instrument, and this sweep did not touch the shared janitor host.

Q5 (reddit fallbacks): PullPush has turned agent-hostile by policy - 429 with the explicit
message "Rate limit exceeded. This website does not provide free scraping resources for
agents. Please contact the administrator on Discord if you're interested in a paid scraping
service." (fetched this sitting). Arctic Shift ANSWERS: 200 with full post JSON for
r/LocalLLaMA (subreddit+limit params only; extra params trip a 422 "Timeout. Maybe slow down a
bit"; one bare repeat also 422'd - it is serial-and-slow, not dead). Redlib mirrors: safereddit
serves a Cloudflare challenge page (200, 4,361 bytes), redlib.catsarch.com TLS-fails from
Windows curl and 429s WebFetch. Recipe restored: arctic-shift.photon-reddit.com/api/posts/
search?subreddit=LocalLLaMA&limit=N, serial with multi-second spacing, and /api/posts/ids for
known thread ids; WebSearch site:reddit.com serial remains the backup. The r/LocalLLaMA
surface is partially restored through Arctic Shift only.

## Anti-rebank statement

Overlap greps run this sitting against catalog/catalog.jsonl (all lines, needle scan, 6.6 s)
and memory/ (md/jsonl/json/txt, excluding memory/runs, 107.8 s): 'decision-models-in-llamacpp',
'gemma-to-jev', 'Gemma 4 26B', 'gemma4:26b', 'gutsy' -> ZERO hits (genuinely new). Already
held, therefore NOT re-banked: Nimble/Tev1 91ms (10-01 register line 2; memory/percolator/
candidates.jsonl '91ms'), Ling-3.0-flash-Fin (watch/INTAKE_ANT_LING_FIN_20260903.md, catalog
line 447016; my artificialanalysis read adds only benchmark texture), Kev model cards
(corpus/library/kev/docs/model-cards/kev-4b*.md, catalog lines 27798-27799), 'Heretic' memory
hits are Chesterton texts (false positives), 'Ajax' catalog hit is boss_rajaxx.cpp (false
positive). The Ollama-blog item below banks only the verification pass + claim conditions, not
the 10-01 claim row.

## OWED from this sweep

1. Estate-cell measurement of decision models (ollama 0.35 upgrade + /v1/systemone conformance
   + llama.cpp Julia-1/gutsy arm) - gated on a quiet window for the shared janitor host.
2. Ling-3.1-flash open-sourcing: re-probe after Oct 15 (StepFun's open-weights date) - if
   StepFun ships on the 15th, the Ling 3.1 radar likely moves the same week.
3. Arctic Shift /api/posts/ids pull of the banked-but-unrecoverable day-1 trio (10-01 fold's
   unconfirmed items) - now feasible through the restored door.
4. Qwen supply-dry post-10-01 confirmation: not found on HN or serial WebSearch; a title-scan
   of r/LocalLLaMA via Arctic Shift spaced calls is the next instrument.
