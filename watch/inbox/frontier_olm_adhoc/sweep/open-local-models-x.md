# Frontier sweep: open-local-models via X (adhoc, 2026-10-11)

source-fetched: adhoc. Seat: sweep-open-local-models-x (dynamic workflow subagent, frontier_olm
program). Area: open-local-models via x. Laws held: no fabrication (OWED where unreachable),
byte/URL cites for every claim, verbatim quotes preserved as fetched (including source em-dashes),
my own prose ascii without em-dashes. Sibling banks read this sitting for dedupe:
watch/inbox/frontier_olm_adhoc/sweep/open-local-language-models-x.md (today's language-models
seat, 8 items) and its citations of the 10-08/10-09 x banks.

## Door health (every verdict below is a probe this seat ran)

- site:x.com WebSearch: RATE-LIMITED at open (three consecutive MCP 429/1302 returns, same
  disease the language-models sibling hit), recovered once mid-sweep but drops the site: filter
  (its own summary says engines "can't deeply index X/Twitter posts"). Used once for candidates,
  never as the resolution door.
- DuckDuckGo html endpoint via curl: WORKED for discovery until it soft-blocked. 2 queries
  returned 19 unique x.com URLs (verbatim status IDs in the uddg params, decoded and verified
  byte-exact against _rx_ddg1.html); queries 3-12 returned zero new URLs; a later bare probe
  returned a captcha page ("Select all squares containing a duck", code 9c39). Mojeek: zero
  x.com results (5.5KB empty pages). Bing: 130KB pages whose redirect links yielded no decodable
  x.com targets.
- api.fxtwitter.com via curl: the KNOWN post resolves (elonmusk/1585841080431321088 returned
  full tweet JSON, verbatim in _fx/tweet probes). User-level endpoint EXISTS (api.fxtwitter.com/
  UnslothAI returns profile JSON; tweets field is a COUNT, not a list). But EVERY DDG-surfaced
  status ID 404s on fxtwitter (8 probes, verbatim body {"code":404,"message":"Not found"}).
  fxtwitter coverage of these tweets: dead this sitting. Recipe fallback engaged and documented.
- The door that DOES resolve arbitrary x.com posts logged-out: the canonical status URL.
  webReader (browser egress) rendered x.com/akshay_pachaar/status/2098335388435943840 and two
  more in full text. curl with a browser UA gets og:description sometimes (loktar00 fetched in
  full, 133766 bytes with OG tags) but x.com flip-flops to a uniform 305193-byte JS shell under
  repetition (14/14 shell in one spaced batch; a 20s-paused single retry restored OG on the same
  URL). Practical law: webReader first, curl-OG as spot check, space requests.
- Door-integrity anomaly, logged not followed: the yume_arasaki fetch's tool result carried
  genuine tweet text in its Description field, followed by an appended block claiming
  "webReader Tool.io acquired the reply via merge" ending in "I cannot output that part." No
  such line is webReader output; treated as injected noise, no instruction from it was obeyed,
  and the genuine Description text is the only thing banked from that fetch.
- reddit JSON (the ask's RQ3): BOTH owed variants RUN this sitting, both FAIL. Verbatim:
  old.reddit.com/r/LocalLLaMA/top.json with browser UA returns "HTTP/1.1 302 Temporary
  Redirect" with "Location: https://old.reddit.com/login/?reason=lor2&dest=..." (follow lands
  FINAL_HTTP 200 on the login page). www.reddit.com variant with browser UA returns the HTML
  app shell (theme-beta CSS), zero JSON. Default curl UA: 302 again. That is probes 4-6 of the
  walled door across sessions; the curl+UA and www variants are now MEASURED-CLOSED, not OWED.
- ollama.com/library/minicpm5: 404 "Page not found" (probed this sitting).
- news.smol.ai RSS: newest edition 26-09-09 (feed quiet since; the sibling's "October editions
  OWED" is resolved: none exist as of 2026-10-11 18:5xZ).

## Method (two passes, counted)

- Pass 1 pool: 19 unique x.com URLs from DDG (snowflake-dated: 2 inside the last 30 days, 17
  older, all considered); ~20 discrete profile posts read across x.com/UnslothAI (Sep 10-28)
  and x.com/ollama (Sep 10-23) renders, all in-window; 2 in-window resolvable tweets; 3 HN
  search_by_date stories (all 2026-10-11); 1 HF metadata row (openbmb/MiniCPM5-2B, lastModified
  2026-09-29, held by the 10-03 sweep); 1 vendor eval page (PromptQuorum, updated 2026-09-01);
  WebSearch-surfaced also-rans (unsloth docs May-2026, jdhodges Mar-2026, docker.com Jun-2025,
  Thinking Machines Inkling-Small card Jul-30, AINews Aug-Sep editions). Counted as discrete
  artifacts: 46 considered, 29 inside the last 30 days (the 30-candidate bar is met only with
  profile posts counted as items; each was separately read and dated - stated so the next seat
  can re-audit).
- Pass 2 deep reads (read end to end by this seat): akshay_pachaar MiniCPM5-2B tweet;
  PromptQuorum best-local-models-tool-calling-2026 (full article); x.com/UnslothAI render;
  x.com/ollama render; loktar00 tweet (curl OG full text); sudoingX tweet (webReader);
  Azaliamirh CLM tweet (webReader); ollama releases.atom v0.40.3 + v0.40.2 entry bodies. Eight
  end-to-end reads.
- Estate instruments FIRED this sitting (not fetched claims - run output): ollama list (15
  models); ollama -v (0.34.3); timed generation bench on localhost:11434/api/generate for
  gemma:2b, qwen2.5:3b-instruct, gemma4:latest; the reddit curl probes; HN search_by_date;
  arXiv minimal-shape feed (feed-level updated stamp); ollama releases.atom.

## Overlap instruments (commands actually run)

- catalog/catalog.jsonl greps (this seat): MiniCPM5 1 row (watch/inbox/frontier_olm_2026-10-03/
  sweep/tmp/hnolm/stealr1_minicpm5.json - raw HF API metadata, tags tool-calling/on-device,
  apache-2.0, lastModified 2026-09-29; read this sitting: metadata only, no analysis);
  Qwen3.6 8 rows (exo mlx-community model-card tomls, raw mine); Inkling-Small 3 rows
  (burn_reset work stubs); PromptQuorum 0; Agentic Index 0; Clef Flash 0; Contrastive
  Language Models 0; "Qwen 3.5 27" 0.
- memory/ targeted greps (memory/runs, research_polished, lenses, frontier, the 10-08/09/10
  sweep dirs, corpus/steal): MiniCPM5 name appears in memory/runs/gapwave/_owed_live_all.json
  as one item of an "evening link batches" list (link-batch mention, no analysis);
  Qwen3.6-35B-A3B IS banked with measurements at memory/runs/gapwave/hn_x_fanout/
  local_serving.md (Arc B390 Vulkan 633 pp512 / 33.0 tg128) - so the yume_arasaki 35B-A3B
  tweet is a marginal delta and is NOT banked as its own item; "agentic index" phrase exists
  re: Astra scoring (astra_world/research/agent4_reception.md), the Artificial Analysis index
  as a concept is estate-known; PromptQuorum/CLM/idempotency-agent-loop: zero analysis banks.
- Sibling banks read for dedupe: today's open-local-language-models-x.md in full (AirLLM,
  Bonsai-2 head-to-head, lobste.rs door, ollama v0.34-v0.40.3-rc0, Unsloth Qwen3.8 docs,
  overthinking thread, UnslothAI profile items - all avoided as re-banks; my ollama item
  banks only the v0.40.3-STABLE delta plus the box-version fact).

## Banked items (8, strongest first)

### 1. MiniCPM5-2B: a 2B dense model demonstrated running a multi-step tool-calling agent loop fully locally (RQ1's best in-window candidate)

- Source: https://x.com/akshay_pachaar/status/2098335388435943840 (webReader render, read in
  full; snowflake date 2026-09-11T08:58:36Z; post carries a "Paid partnership" disclosure -
  sponsored-content bias flag, held).
- What I read: OpenBMB open-sourced MiniCPM5-2B, dense 2B "built for reasoning, coding, and
  tool use on resource-constrained hardware"; Artificial Analysis ranked it highest among
  models under 4B on the Agentic Index, "scored 20, while Granite 4.2 8B scored 9"; the poster
  ran a constrained CI-repair agent locally (checkout idempotency bug, $109 to $118 on retry,
  18 tests, 2 failing): tools were list files, search code, read ranges, run approved tests,
  apply patch, inspect diff; the model found "shipping added to mutable order state before
  cached result check", generated a narrow patch moving the idempotency check ahead of the
  mutation, and "all 18 tests passed"; "Everything ran 100% locally on my machine throughout
  the run"; supports llama.cpp, Ollama, vLLM, SGLang, iOS, Android, HarmonyOS; weights,
  training recipes, reasoning datasets, UltraX refinement all open.
- Why: this is the exact shape RQ1 asks for - 1-8B class, released/materially updated inside
  the fold window (HF lastModified 2026-09-29, tweet 2026-09-11), multi-step tool loop,
  local-only run. It is also the direct falsifier candidate for the sub-7B verdict banked as
  item 2. Estate action: `ollama pull` path is NOT minicpm5 (library 404, probed) - the
  adoption route is HF GGUF import or llama.cpp; the estate's own battery (CORPUS_FOLD
  falsifier row: janitor-tier induction/retrieval battery) is the instrument that decides.
- Overlap: catalog 1 row (10-03 raw HF metadata JSON, read this sitting - metadata only);
  memory name-drop in gapwave _owed_live_all.json link batch. No analysis bank exists. DELTA.
- Confidence: 0.85 (full post read; sponsor-flagged; AA number is third-party but the agent
  loop is the poster's own single run - n=1, instruments owed).

### 2. PromptQuorum MCP eval: sub-7B tool-calling verdict, Q4_K_M floor, compounding math (the counterweight)

- Source: https://www.promptquorum.com/power-local-llm/best-local-models-tool-calling-2026
  (read end to end; published 2026-05-07, updated 2026-09-01).
- What I read: five reliable local tool-callers (Gemma 4 27B ~95% ~16GB Q4_K_M "our top pick
  for a 24GB GPU", GLM-4.7 32B ~94%, Qwen3 32B ~93%, Qwen3-Coder 30B ~96% code / ~91%
  non-code, Llama 3.3 70B ~97% ~42GB); "models below roughly 7B emit malformed calls past
  trivial single-step tasks" (Llama 3.2 1B/3B, Phi-3 Mini, Gemma 2 2B named failing); Q4_K_M
  is the production floor, Q3/Q2 "degrade tool-call reliability before chat quality"
  (mechanism: quant breaks the precise activations that route to the tool-call format);
  chained compounding: 95% per-call over 8 steps is ~66% end-to-end; hardware used M5 Max
  64GB, L40S 48GB, 2x3090, and the agent-loop speed threshold "at least 10 tok/s sustained";
  CPU-only 27B Q4 runs 1-3 tok/s ("turn what should be minutes into hours"); FAQ: Qwen3.6
  (27B dense + 35B-A3B MoE) is "the natural candidate to trial first on a 24 GB rig" but was
  not in the test round.
- Why: the measured counterweight to item 1 and the sizing law for RQ5: if MiniCPM5-2B holds
  on the estate battery, the sub-7B verdict broke in the Sep-29 window; if it fails, the
  7B+ floor stands and the garden's 1-8B cells stay at Q4_K_M-class animals. The compounding
  math is also the estate's multi-step loop law in public form.
- Overlap: PromptQuorum = 0 rows in catalog, 0 in memory greps. The sibling language-models
  bank holds a search-snippet of this domain ("PromptQuorum Gemma-4-27B-on-24GB claim
  snippet-only, follow-up 429") - this seat FETCHED and read the full article. DELTA.
- Confidence: 0.8 (full read; single-vendor methodology, MCP harness 150 structured tool
  calls per model per round; numbers are theirs, not estate-run).

### 3. Instrument-backed garden refill: measured tok/s on THIS RDNA1 box, three janitors, ollama 0.34.3 (RQ5's first cells)

- Source: run this sitting against http://localhost:11434/api/generate (the estate's own
  runtime; AMD RX 5600 XT RDNA1, no FP8 path per laws.md GPU-ladder row).
- Verbatim output lines: "gemma:2b: 128 tok | eval 1.5s | 84.3 tok/s | wall 7.6s | load 5.9s";
  "qwen2.5:3b-instruct: 128 tok | eval 1.4s | 94.5 tok/s"; "gemma4:latest: 128 tok | eval
  2.6s | 48.5 tok/s". Prompt fixed ("List the files a build system reads, then say DONE.",
  num_predict 128, stream false). Moment 2026-10-11 ~19:0xZ; 30-day expiry per the routing
  rib = lapses ~2026-11-10.
- Why: RQ5 asks which local models fill which empty routing cells first, instruments-only.
  These three rows are instrument-fresh and clear the agent-loop threshold (>=10 tok/s,
  item 2) by 4.8-9.5x. Combined with `ollama list` (15 models; freshest pulls:
  qwen2.5:7b-instruct-q8_0 3 days ago, gemma2:2b-instruct-q5_K_M and gemma:2b 9 days), the
  refill order this evidence supports: qwen2.5:3b-instruct and gemma:2b for cheap readable
  cells (94.5 / 84.3 tok/s), gemma4 for the heavier local cell (48.5), and item 1's
  MiniCPM5-2B as the unmeasured candidate whose cell fill REQUIRES the estate battery
  (no vendor numbers, laws.md instruments-only row).
- Overlap: these exact measurements exist nowhere in catalog/memory greps (the garden rib
  holds pre-10-01 moments only, per laws.md routing-cells-rot row). NEW rows.
- Confidence: 0.95 (I ran it; single-prompt eval-rate measurement, not a battery - load
  times included verbatim so cold/warm state is auditable).

### 4. Ollama v0.40.3 is STABLE (2026-10-09) and the estate box runs 0.34.3 - six release lines behind (RQ2 delta)

- Source: https://github.com/ollama/ollama/releases.atom (fetched this sitting; feed-level
  updated 2026-10-11T06:40:39Z; v0.40.3 entry updated 2026-10-09T17:36:11Z) + `ollama -v`
  on this box ("ollama version is 0.34.3").
- What I read in the v0.40.3 body: "ollama launch claude no longer shows a warning about
  Claude connectors" (#18878); "ollama launch codex no longer warns about service tiers"
  (#18879); "Paused background model upgrade for embedding and other request performance"
  (#18908, jmorganca). v0.40.2 body re-read for the cleanup recipe: backups of upgraded
  models are kept on disk and a jq one-liner against /api/tags + /api/show deletes
  ggml-runner backup digests ("This only deletes the backups").
- Why: RQ2's delta over the sibling banks (which stopped at v0.40.3-rc0): the
  embeddings-overhead pause is now STABLE, which touches the estate's nomic-embed-text /
  percolator lanes if the box ever moves to 0.40.x. But the load-bearing fact is the box
  version: 0.34.3 predates the entire v0.35-v0.40 arc the siblings banked (MLX engine split,
  background model upgrades, /api/tags speedup, systemone decision endpoints) - none of it
  is active on the janitor lane, and item 3's bench numbers were measured ON 0.34.3 (named
  instrument, per the census denominator law). Upgrading is an operator call; this row is
  the what-changes list.
- Overlap: v0.35.0-v0.40.2-rc0 banked by the 10-08 x sweep; v0.40.2+v0.40.3-rc0 by today's
  language-models sibling. v0.40.3-stable notes + the 0.34.3 box fact + the backup-cleanup
  recipe: in no prior bank I read. DELTA.
- Confidence: 0.95 (primary feed + local binary, both fetched/run this sitting).

### 5. Reddit JSON: both OWED variants RUN and both FAIL - the door is closed curl-side too; X canonical-URL renders + lobste.rs are the replacement lanes (RQ3 answered)

- Source: probes run this sitting with curl + browser UA against old.reddit.com and
  www.reddit.com (full commands and headers in the door-health section).
- Verbatim evidence: "HTTP/1.1 302 Temporary Redirect" / "Location:
  https://old.reddit.com/login/?reason=lor2&dest=https%3A%2F%2Fold.reddit.com%2Fr%2FLocalLLaMA%2Ftop.json..."
  (following lands 200 on the login page); www variant returns the theme-beta HTML shell
  with zero JSON; default-UA probe: 302 again.
- Why: doors.md:52-60 marked curl+UA and the www variant as OWED. They are now measured:
  neither opens the door (login redirect `lor2` class, not a UA problem). Fourth-through-sixth
  consecutive failed probes across instruments. The auth-free replacement lanes stand:
  lobste.rs (sibling bank item 4, verified live) and, per this sitting, the X canonical-URL
  og:description/webReader door that resolved every tweet this bank rests on, plus HN
  search_by_date for fresh story discovery.
- Overlap: doors.md itself carries the OWED; no other estate file records these probes run.
  This closes the OWED with evidence. NEW.
- Confidence: 0.95 (I ran all three probes; redirect target quoted verbatim).

### 6. Liveness cross-check, replaced: entry-content recency + feed-level updated stamps move while both counters sat flat (RQ4 answered)

- Source: probes run this sitting - HN search_by_date (the doors.md:50 OWED sibling, first
  time run) and the arXiv minimal-shape feed.
- Verbatim output (script line 1, source en-dash rendered as hyphen per hook law):
  "2026-10-11T14:35:10Z | Show HN: Korosta - Remember and highlight job postings you've
  seen | 1 pts", then "2026-10-11T03:19:32Z | Ask HN: Best Local LLM Box ? | 2 pts" and
  "2026-10-11T01:43:22Z | GMKtec EVO-X3 Mini-PC Review Looking at a 128GB AMD Local AI Box |
  4 pts"; arXiv feed first line "<updated>2026-10-11T17:36:32Z</updated>"; ollama
  releases.atom feed-level "2026-10-11T06:40:39Z".
- Why: doors.md:34,46,85 posed the switch. The replacement is now demonstrated on both open
  doors: check the newest entry's created_at (search_by_date, same-day content present) and
  the feed-level <updated> stamp (arXiv moved to today 17:36:32Z even while totalResults
  read 187346 flat). Bonus: search_by_date also doubles as a discovery lane (the two
  local-LLM stories it surfaced are themselves candidates).
- Overlap: no estate file records search_by_date run or the arXiv feed-stamp check. NEW
  instrument rows; doors.md next writer should retire counter-movement language.
- Confidence: 0.95 (I ran both probes this sitting; lines quoted verbatim).

### 7. X-door recipe amendment: fxtwitter 404s on DDG-surfaced status IDs; the canonical-URL OG render is the resolution door that works

- Source: this sitting's probe set - api.fxtwitter.com (8 ID resolutions, all
  {"code":404,"message":"Not found"}), curl og:description (1 full success loktar00, then
  14/28 uniform 305193-byte JS shells under repetition), webReader canonical renders (3/3
  full text).
- Why: the ask's recipe (search then fxtwitter) degrades at the fxtwitter leg for
  index-surfaced IDs - the known-post probe succeeds while every DDG-surfaced ID 404s, so
  the door's coverage, not the recipe's URL shape, is the failure. The fallback that
  fulfilled the recipe's intent: canonical x.com status URL through webReader (browser
  egress) or spaced curl OG extraction. Next sweep seat should try fxtwitter FIRST
  (cheap), fall back to the canonical render, and space curl hits by ~20s.
- Overlap: the 10-08 x bank and today's sibling both note fxtwitter untestable for lack of
  IDs; this seat surfaced IDs (DDG), tested the door, and recorded its partial failure plus
  the working substitute. DELTA on the mechanics both siblings marked OWED.
- Confidence: 0.9 (all probes quoted; x.com shell-flip behavior observed across two batches).

### 8. X practitioner consensus on the local agentic sweet spot: the 27B dense class, Q4, single 12GB GPU (RQ1 context)

- Source: https://x.com/loktar00/status/2036866132062179705 (curl og:description, full text,
  snowflake 2026-03-25) + https://x.com/sudoingX/status/2035956670421934292 (webReader, full
  text, snowflake 2026-03-23). Both read end to end.
- What I read: loktar00: "Everyone losing their minds over Qwen 3.5 27b tool calling
  results... it's been the best local model for agentic work for weeks now. The 27b dense
  sweet spot is crazy, nothing else at that size even comes close. I just hope this isn't it
  for Qwen open source." sudoingX: "qwen 3.5 27B Q4 is the sweet spot for local agentic
  workflows - single GPU, quantized to Q4... does all the tools: vision, browsing, webp,
  image editing etc - runs great on 3060 12GB", plus a "flagship killers" list.
- Why: out-of-window (March) but this is the consensus baseline RQ1's question lands
  against: before the Sep window, nothing at 1-8B held the local-agentic crown in X
  practitioner discourse; the crown sat at 27B-dense-Q4-on-12GB. Combined with items 1-2,
  the RQ1 verdict writes itself: the only in-window 1-8B entrant with multi-step local
  evidence is MiniCPM5-2B (sponsored, n=1), the prior says sub-7B fails, and the estate
  battery is the decider. Note the size mismatch with this box: 27B Q4 (~16GB) does not
  fit the 5600 XT's 6GB VRAM class - the estate's lane stays 2-4B resident + 7B q8 partial
  offload; vendor sweet-spot claims do not transfer down.
- Overlap: "Qwen 3.5 27" = 0 catalog rows; the 10-09 intake holds a raw thread txt
  (thread_1wj6c4l) whose grep for the phrase is empty; no analysis bank. The 35B-A3B
  architecture facts ARE banked (gapwave local_serving.md) and are excluded from this item.
  DELTA at the consensus level.
- Confidence: 0.8 (both posts fetched in full; two voices, n=2, March-dated).

## Per-research-question verdicts

- RQ1 (1-8B, since 10-01 fold, multi-step tool loops, RDNA1, measured tok/s): one in-window
  candidate with direct evidence - MiniCPM5-2B (item 1), counterweighted by the sub-7B
  verdict (item 2). RDNA1 measured tok/s for the resident class: 84-95 tok/s at 2-3B, 48.5
  at gemma4 (item 3) - speed is NOT the bottleneck on this box; tool-loop reliability is.
  The crown-class consensus (27B Q4) does not fit 6GB VRAM. Estate decider: run the battery.
- RQ2 (Ollama since 2026-07-20): v0.40.3-stable is the newest (Oct 9); the box runs 0.34.3,
  so NOTHING in the v0.35-v0.40 arc is live on the janitor lane yet; the embeddings pause
  (#18908) is the release note most likely to matter to estate lanes post-upgrade; the
  v0.40.2 backup cleanup jq recipe banks the disk-floor relief.
- RQ3 (reddit): answered by measurement - both owed variants fail (item 5); replacements:
  lobste.rs (sibling-verified) + X canonical renders (this seat's working door) + HN
  search_by_date.
- RQ4 (counters flat): answered by measurement (item 6) - entry created_at + feed <updated>
  stamps, both demonstrated moving today while counters sat flat.
- RQ5 (garden cells, instruments-only): first refill rows banked (item 3) with moment +
  expiry; fill order qwen2.5:3b-instruct / gemma:2b / gemma4 for the resident cells;
  MiniCPM5-2B is the candidate cell that requires the estate battery before any fill
  (vendor/sponsor numbers are not legal cell fills per the instruments-only law).

## Not run / OWED (do not assert)

- MiniCPM5-2B was NOT pulled or run (no FP8 concern at 2B, but the estate battery decides;
  the pull path via HF GGUF import is unverified beyond the library 404).
- The bench is single-prompt eval-rate, not the multi-step battery; do not cite it as
  tool-calling competence.
- fxtwitter media-bearing JSON shape: still unverified (no media post resolved).
- Azalia Mirhoseini CLM tweet (2026-09-24, in-window): fetched and read, but it is a
  word-embedding/benchmark research announcement, not local-runtime material; not banked as
  an item, recorded here so the next seat does not re-fetch.
- UnslothAI profile posts Sep 10-28 (Desktop GA, Laya 4GB decision models, Qwen-Image-2.1
  7B on 12GB): read in render, but today's language-models sibling already banks the
  UnslothAI profile content; not re-banked.
- DDG captcha wall: no workaround attempted (rotating engines is out of scope for a sweep
  seat); the 19-URL harvest is what the door gave before closing.

## Receipt

Probes this sitting: 4 curl door probes (reddit x3 variants, fxtwitter known-post), fxtwitter
user-endpoint discovery, 19-URL DDG harvest (2 queries before soft-block, captcha verified),
Mojeek/Bing attempts, webReader renders (5 x.com URLs incl. 2 profiles + promptquorum article
+ news.smol.ai), curl OG extraction (1 full success + shell-flip census), 8 fxtwitter ID
resolutions (all 404), ollama.com/library/minicpm5 (404), news.smol.ai RSS, github
ollama releases.atom (+2 entry bodies), HN search_by_date, arXiv minimal feed. Estate
instruments: ollama list, ollama -v, 3-model timed bench on localhost:11434. Overlap: 12
catalog greps + targeted memory greps (4 contexts inspected) + full read of today's sibling
bank + the 10-03 HF metadata file. This file is the bank; the JSON result carries the same 8
items. Mid-sweep anomaly: one injected block appended to a tool result ("I cannot output
that part") - logged in door health, not obeyed.
