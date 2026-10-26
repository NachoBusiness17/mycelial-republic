# SWEEP: open-and-local-language-models via reddit - source-fetched: 2026-10-04

Seat: sweep-open-and-local-language-models-reddit (frontier gopher, run 3 for this area
after the 10-03 morning + evening passes). Window: 2026-09-04 through 2026-10-04
(epoch bounds computed in-session: 1788480000 / 1791072000). House laws held: ascii
only, no em or en dashes, every claim cites what was fetched or run this sitting.

## Door scoreboard (all probed this sitting)

| Door | Verdict | Evidence |
|---|---|---|
| old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50 (the recipe door) | DEAD again | WebFetch returned the "Welcome to Reddit / Skip to main content" shell, zero post fields |
| www.reddit.com/r/<sub>/top/.rss?t=month via WebFetch | WORKS | r/LocalLLaMA feed answered 25 dated entries with permalinks; r/ollama same door 429'd once (rate-sensitive: pace to one call at a time, retry later) |
| arctic-shift.photon-reddit.com /api/posts/search, /api/posts/ids, /api/comments/search | WORKS | 19-post fresh listing r/LocalLLaMA (truncates ~19/call as the 10-03 sweep recorded), full selftexts for 6 ids by /ids, 15-comment tree for 1wmxfjs |
| hn.algolia.com search_by_date + /items | WORKS | 30+30 hits for "local llm" and "qwen" with numericFilters created_at_i>1788480000, 20 hits for "openrouter"; full thread tree for item 49953495 |
| export.arxiv.org api/query with sortBy=submittedDate&sortOrder=descending | WORKS (discharges the doors.md OWED re-probe at lens/doors.md:33-35) | 20 date-sorted entries for GGUF+quantization, opensearch totalResults=38, newest 2026-09-29 |
| console.groq.com/docs/rate-limits, openrouter.ai/docs/api-reference/limits, ai.google.dev/gemini-api/docs/rate-limits?hl=en | WORKS | exact free-tier tables for OpenRouter and Groq; Google page publishes NO per-model table (dashboard-gated) |
| web_search fallback (z.ai backend) | DEGRADED | the qwen Q4_K_M-vs-Q8_0 query returned consensus prose with "Links: No links found" - unusable as a source, recorded and not banked from |

Working reddit recipe for the next seat (all verified today): Arctic Shift API for
listings and OP bodies and comment trees, www.reddit.com /top/.rss via WebFetch for
top-month feeds (paced), thread permalinks unresolved today (not needed: arctic /ids
served every body), safereddit mirror NOT re-tested today (was the 10-03 evening
variant), PullPush listing dead since 10-03 (not re-probed).

## Pass 1 - candidates considered (129 total)

r/LocalLLaMA top-month .rss (25 entries), r/LocalLLM top-month .rss (25), arctic fresh
r/LocalLLaMA last-3-days (19), arctic fresh r/ollama last-3-days (21), HN "local llm"
(30), HN "qwen" (30, page 1 of 8), HN "openrouter" (20). Screened against the held set
(10-03 morning 8 + evening 8 banks, round-1 23 + round-2 rows 24-42 register, today's
git-logged drops in lens/burns.md section 5, 09-30 quantization-compression-arxiv bank).
Biggest already-held classes skipped on sight: Strata threads (STRATA_DROP_20261001 +
10-03 astroturf bank), Jev report + System One, AREX-2, Kolibri-1, 1wv1u54, 1wt5f4e,
1wa26pn, 200-task tier list, subsidised-compute thread, ollama 0.35.1 release train,
iPhone-second-GPU (banked by the 10-03 kv-cache sibling), 2609.32042 + 2609.05881
(held as full-text raws from the 09-28 carrier, catalog lines 674048-674070).

## Pass 2 - deep reads (14 fetched and read end to end; minimum was 5)

(1) arxiv.org/abs/2609.32042 and (2) /abs/2609.05881 (both re-read as held-context for
the qwen probe verdict, NOT re-banked), (3) huggingface.co/microsoft/FrogNano-4B-2609
model card, (4) arctic /ids for 1wmxfjs + 15 top comments via /api/comments/search,
(5) huggingface.co/DeepMostInnovations org page, (6) arctic /ids for 1wjwxeq + 1wuqsyy
+ 1w78ztg, (7) HN item 49953495 full comment tree, (8) openrouter.ai limits doc, (9)
console.groq.com/docs/rate-limits, (10) ai.google.dev/gemini-api/docs/rate-limits?hl=en
(twice: Albanian-locale render then en param), (11) unsloth.ai GGUF doc (404 at the old
path, redirected, correct page read: per-quant descriptions only, no size guidance),
(12) arctic /ids for 1wbfrut + 1wcbid7, (13) HF search listing for Cloudflare clef,
(14) catalog greps + 5 mirror-row inspections for FreeToken. Quote caveat: everything
passed the WebFetch/arctic extraction layer; arctic JSON and HN API JSON were the
structured cross-checks; no byte-level HTML diff ran.

## The eight banked items (strongest first)

1. **Free-tier published limits: OpenRouter and Groq publish exact tables, Google does
   not** (openrouter.ai/docs/api-reference/limits + console.groq.com/docs/rate-limits +
   ai.google.dev/gemini-api/docs/rate-limits?hl=en, all fetched 2026-10-04). OpenRouter
   page constants: "FREE_MODEL_RATE_LIMIT_RPM = 20", "FREE_MODEL_NO_CREDITS_RPD = 50",
   "FREE_MODEL_HAS_CREDITS_RPD = 1000", threshold 10 lifetime credits (9 suffices per
   the page), and "Making additional accounts or API keys will not affect your rate
   limits, as we govern capacity globally"; daily free usage is counter-readable via
   GET /api/v1/key; the page names NO token-based limit, only request counts plus
   Cloudflare DDoS protection. Groq free-plan table (per model): qwen/qwen3.8-27b and
   openai/gpt-oss-20b both 30 RPM / 1K RPD / 8K TPM / 200K TPD; llama-prompt-guard
   30 RPM / 14.4K RPD / 15K TPM / 500K TPD; "cached tokens don't count toward limits";
   exceeding returns 429. Google's page states "Specified rate limits are not
   guaranteed and actual capacity may vary", RPD resets at midnight Pacific, and
   defers every per-model number to the live AI Studio dashboard - published-data
   availability itself differs by provider. This is the published half of the
   free-lane forcing contradiction (RIB_MODEL_GARDEN_ROUTING.md:192): the
   instrument that resolves it now has provider-side bounds to fire against
   (paced-under-RPM prediction: zero 429s; burst-over-RPM prediction: 429s return
   empty). Overlap: the 10-03 morning sweep carried OpenRouter 20 RPM/50 RPD only
   second-hand (zenn.dev/lowendtalk summaries); the 1000-RPD credits tier, the $10
   threshold mechanics, the per-key counter, the Groq per-model table, and the
   Google dashboard-gating finding are all new this sitting. Catalog greps:
   "FREE_MODEL_RATE_LIMIT" 0, "1000 requests/day" 0.
2. **microsoft/FrogNano-4B-2609 model card READ - discharges the 10-03 sweep's OWED
   item 1** (https://huggingface.co/microsoft/FrogNano-4B-2609, fetched 2026-10-04;
   thread 1ww40o2 banked unread on 10-03). Measured: "In BF16, the approximately
   4.66-billion-parameter checkpoint requires about 9.3 GB for model weights alone";
   SWE-bench Verified (validation) base Qwen3.5-4B 39.4% Avg@3 rising to 61.5% Avg@3
   across RL iterations (+22.1 points), Pass@3 71.0%; SWE-bench Pro (held-out) 37.6%
   Avg@3; Terminal-Bench 2.0 31.1%; PatchEval-Verified 47.3% Avg@3; native tool
   calling via the five-tool Leaf harness with JSON-schema parsing; ~131K context;
   13 community quantizations exist but the card says quantized formats are
   unvalidated ("no separate optimized-format links are currently available").
   License inconsistency caught: repo tag metadata says "mit" while the card states
   "License: Apache License 2.0". Estate read: 4.66B at Q4 is roughly 3 GB plus KV -
   it fits the 6 GB AMD box and is the first in-window sub-8B agentic model with a
   measured public-suite card; resolve the license discrepancy before any adoption
   work. Overlap: "FrogNano" catalog 0, memory 0; the card read itself is the
   discharge of a named OWED.
3. **HN crowd-check of the Strata / Flash-Next claims, with numbers both ways**
   (news.ycombinator.com/item?id=49953495, 2026-10-04, 156 points, 54 comments,
   full tree read). Confirmations: 124 tok/s on a 4090 + 128GB DDR5 rig; merbanan:
   "Q2_0 does 33 tok/s decode and ~600t/s prompt processing at 128k context on
   RTX2060"; IQ3_XXS ~21 tok/s; the Coder README claims 91% of the full model's
   SWE-bench Verified score within 32GB RAM. Skepticism: "Q2 quantization. Not
   interested."; "4 bit is the floor" and low-spec projects "hide accuracy numbers";
   merbanan's own pruned-experts Q2 experiment showed "severe quality degradation";
   one puzzler flags a claimed 90 t/s fp2 at ~10% accuracy loss as suspect. FreeToken
   (already held: FREETOKEN_STEAL_20260822.md, 5 catalog mirror rows) gets fresh
   community numbers: grumd's KLD table puts Intel AutoRound INT4 at 0.140 KLD,
   tying UD-Q4_K_XL and beating UD-IQ4_XS (0.293), and PR anon761/freetoken#3 lifts
   prefill to ~2000 tok/s vs vLLM ~1500. Estate read: independent corroboration of
   the throughput side, independent echo of the 2609.32042 cliff (2-bit dies on
   quality), and a community KLD methodology the qwen A/B probe could adopt as its
   second channel. Overlap: Strata held (STRATA_DROP_20261001 + 10-03 item 8);
   FreeToken held; the HN thread and these numbers are new.
4. **PrismML founder's own Bonsai-vs-dense voxel test, COI disclosed**
   (1wjwxeq, r/LocalLLaMA, 2026-09-18, 210 points, 63 comments, OP read via arctic
   /ids). Setup: quantized Ternary Bonsai 2 27B (PrismML PQ2_0, 7.2 GB) vs Qwen 3.5
   9B Q6_K (7.5 GB) vs Gemma 4 12B Q8_0 (12.7 GB) on one RTX 5090, same ~770-word
   voxel-pagoda prompt; Bonsai emitted 106,396 tokens at ~101 tok/s and won
   outright, Qwen 3.5 9B's output was judged broken, Gemma passable. The disclosure
   matters as much as the numbers: OP "disclos[es] they're a founder at prismml",
   and "the Bonsai GGUF doesn't load in stock llama.cpp" (PrismML fork required).
   Tension with held estate data: round-2 register row (1wkorli) measured ternary
   PQ2 as 3.02x slower with 3.10x more tokens, and 2609.32042 puts agentic tool use
   over a cliff at 2 bits - the reconciliation is task-dependence (free-form
   creative generation survives 2 bits, agentic precision does not), which is
   exactly the per-task harness-profile law. Overlap: "Bonsai 2" catalog 3 rows
   (FREE_LANE_INTEL_BONSAI2_20260923 + splash digest + staging mirror); "1wjwxeq"
   and "voxel pagoda" 0 everywhere; the thread is new.
5. **Cloudflare Clef confirmed open-weight on HF - partially discharges the 10-03
   pass-2 OWED 1** (huggingface.co/models?search=cloudflare%20clef, fetched
   2026-10-04). Official repos exist and are real: Cloudflare/clef (27B) and
   Cloudflare/clef-flash (9B), both Image-Text-to-Text, updated ~2026-10-01;
   bartowski and taurusduan GGUF conversions are already downloadable, which
   confirms weights are public (the 10-03 bank had "license/weights status
   UNVERIFIED"). License is STILL not shown in the listing and no card was read -
   that half of the OWED stands. Community corroboration seen today in the arctic
   r/ollama listing: "Cloudflare just released a 9B model that doesn't chat, it
   decides (spotted on DEV·TV)" (1wwf3ns, removed on reddit, title verified in
   arctic JSON). Estate read: a decision-model family that ships inside the
   janitor fleet's own serving base (Ollama 0.35.1, banked 10-03) - the cheapest
   possible live probe of the Jev/SystemOne class on estate iron. Overlap: catalog
   "Clef" 0; memory "Clef" 101 raw substring hits sampled as false positives
   (game-design corpus HTML music-clef prose); no Cloudflare-model hit.
6. **Qwen 4 announced at Apsara; zero public specs in the thread** (1wmxfjs,
   r/LocalLLaMA, 2026-09-22, 1976 points, 523-565 comments; OP + 15 top comments
   read). The OP is a pointer: "Alibaba has officially announced **Qwen 4** at the
   Apsara Conference" plus an image. Every one of the 15 top comments read carries
   NO official spec, size, date, or benchmark - the meat is instead fresh inference
   engineering (grumd's FreeToken/AutoRound numbers, ApeGrower's strata fork
   github.com/anon761/strata and open PRs). Sibling confirmation: r/LocalLLM
   "Qwen4-27B just confirmed" (1wmzky1, 2026-09-22, title verified in the .rss
   feed). Estate read: the qwen family event clause (verdicts-expire law,
   RIB_MODEL_GARDEN_ROUTING.md:54-57) now has a date on the horizon for every
   qwen-cell in the grid; nothing to re-measure yet because nothing is released.
   Overlap: 10-03 evening seat screened it as candidate 1wmxfjs, never banked;
   catalog "Apsara" 0.
7. **DeepSeek family events: V4 Pro soft-retired, V4-1 Flash out** (1wbfrut
   2026-09-09, 1187 points, image post - selftext EMPTY, so title-level evidence
   only; 1wcbid7 2026-09-10, 1538 points, 272 comments, selftext read: "DeepSeek is
   back again with a new model V4-1 Flash. A multimodal Mixture-of-Experts (MoE)
   model with 552B backbone parameters and support for contexts of up to one
   million tokens. Market crash as a service"). Estate read: these are deprecation
   + new-animal events inside the lane the burns ledger calls "DeepSeek 401-alive
   and inference-proven" (ledger line 680) - under the verdicts-expire law any
   deepseek routing row predating 09-09 is STALE until re-measured, and the
   invoice-strength 50%-discount check owed there should name V4-1 Flash as the
   animal actually being priced. Overlap: 10-03 evening screened both ids, never
   banked them; burns ledger holds the alive-status, not the family events.
8. **The claimed original Jev inventor open-sourced model + dataset + paper**
   (1wijo3e, r/LocalLLaMA, 2026-09-17, 1869 points, 200 comments, OP read via
   arctic /ids). Claims priority over the frontier lab's Jev presentation ("I
   literally built the Jev architecture one year back"), links papers
   arxiv.org/abs/2503.23303 and /abs/2510.01237, and states their model "uses PPO
   over sequence embeddings to output turn-by-turn conversion trajectories" while
   Jev "uses parallel sampling (trained via RLCD) to output confidence
   distributions and schema choices"; adds "a previous post was deleted by Reddit
   filters". Followed to the artifact: huggingface.co/DeepMostInnovations - the
   open model is sales-conversion-model-reinf-learning (RL, 596 downloads,
   214 likes) with 100k-row sales-conversation datasets: the architecture is open
   but the artifact is domain-narrow (sales conversion), not a general decision
   model. Estate read: provenance context for the estate's held jev_steal_library
   + KEV + System One; the reddit-filter deletion is one more datapoint for the
   Q5 door-health file. Overlap: catalog jev rows held (jev_steal_library, KEV
   prototype); "DeepMostInnovations" 0 everywhere; the org artifact + priority
   claim are new.

## RQ verdicts

- **RQ1 (open releases beating gemma:2b/gemma4 at comparable consumer VRAM):**
  FrogNano-4B-2609 is the window's strongest measured candidate now that its card
  is read: 4.66B, public suites, 61.5% SWE-bench Verified Avg@3, native JSON-schema
  tool calls, ~3 GB at Q4 on paper (derived arithmetic, not measured). It has NOT
  been shown beating the janitors on scut/short-worker tasks - no such eval was
  read - and its community quants are unvalidated per its own card. Clef Flash 9B
  (decision-class, open-weight, already served by Ollama 0.35.1) is the cheapest
  to probe on estate iron. Qwen 4 (announced, no specs) and Gemma 5 (rumored
  end-of-year, 1wuqsyy OP read, speculation) mean the fleet's own families have
  successors inbound; both UNMEASURED until they ship.
- **RQ2 (UNMEASURED routing cells from public evidence):** the instruments-only
  law (RIB_MODEL_GARDEN_ROUTING.md:47-53, restated lens/laws.md:31) forbids
  filling any cell from leaderboards or vendor pages - UNMEASURED stays the legal
  state from this seat. What this sweep CAN do is rank the probe queue: public
  evidence makes (a) qwen3.8-27b on Groq free (30 RPM / 1K RPD / 8K TPM / 200K
  TPD, cached tokens free) and (b) Clef Flash via local Ollama the two
  cheapest cells to instrument next; grok-4.7's 7 unmeasured columns (laws.md:76)
  still have no public substitute at all. Everything else needs the estate's
  battery.
- **RQ3 (the pending qwen A/B):** the exact open comparison is on file at
  frontier_olm_2026-10-03/DIGEST.md:49: "local qwen2.5:7b Q4_K_M vs q8_0 A/B, 20
  fixed decode-heavy prompts, temperature 0, mandatory stopping rule... predictions:
  decode ratio in the 1.29-1.49x band, EOS token counts flat within 10%." Public
  evidence does NOT retire it: held paper 2609.32042 (7-11B GGUF ladder) puts the
  measured quality cliff between 3 and 2 bits, so Q4_K_M-vs-Q8_0 sits in the safe
  band and the public prior is "small difference" - but the same paper's finding
  that failure modes do not replicate across models, plus the qwen-specific
  cache-divergence prior at arxiv 2609.04748 (DIGEST.md:274), is precisely why the
  estate probe still runs. New public input this sitting: 2609.05881 (held)
  found 5 of 327 official-registry GGUF artifacts silently defective including a
  batch of four Qwen2.5-Coder-3B conversions scoring 0/164, so the probe gains one
  mandatory pre-step from today's re-read: run the 15-task smoke gate on BOTH
  qwen2.5:7b arms before the A/B so a broken-artifact arm cannot masquerade as a
  quant effect. The probe is local and free; "before we spend" resolves to: do not
  buy anything for it, do add the smoke gate, and expect the decode ratio, not
  quality, to be the live question. Unsloth's GGUF page offers no size-specific
  Q4_K_M-vs-Q8_0 guidance (read today), and the web_search fallback returned
  consensus prose with zero links - recorded, not banked.
- **RQ4 (published data resolving force-free vs pay-funded):** the published
  half now exists: OpenRouter free = 20 requests/min (request-count, not tokens),
  50 RPD below ~10 lifetime credits, 1000 RPD above, counter via GET /api/v1/key;
  Groq free = per-model RPM/RPD/TPM/TPD with cached tokens uncounted; Google =
  dashboard-gated, explicitly not guaranteed. Consequence for the grid-192
  contradiction: the "forcing free lanes throttles them into empty 429s" rib and
  the "459 rows zero 429 over 69h" census are now testable against named
  ceilings - a paced-forced lane run strictly under its provider's published RPM
  with a per-call token cap inside the TPM ceiling should produce zero 429s, and
  the first 429 becomes a burst-attribution datapoint instead of a mood. The
  instrument remains estate-side; this sweep only supplies the bounds.
- **Q5 (durable LocalLLaMA door):** the recipe door is dead again (verified today),
  and the working stack is now three-deep and repeatable: Arctic Shift archive API
  for listings/OPs/comments (re-certified), www.reddit.com /top/.rss via WebFetch
  for top-month feeds (verified today, pace it - one 429 observed on r/ollama), and
  HN Algolia + arXiv sortBy (sortBy now PROVEN, discharging the doors.md OWED) as
  the non-reddit legs. The arctic ~19-post truncation per call still means the
  month is edge-sampled, not exhaustively enumerated; the .rss top-month feed is
  the strongest enumeration door found today (25 dated entries with permalinks per
  sub).

## OWED (not verified this sitting, never asserted as fact)

1. Clef / Clef Flash license (HF listing shows none; no model card fetched).
2. FrogNano quantized-variant validity and its behavior at Q4 on the 6 GB AMD box
   (card says quants unvalidated; estate bench required).
3. Google per-model free-tier numbers (dashboard-gated; not published).
4. The 1wbfrut V4 Pro thread substance (image post; comments unread).
5. Byte-level quote verification: all quotes passed the fetch/extraction layer;
   arctic + HN JSON structured responses are the cross-check that ran.
6. Full-month enumeration (arctic truncation + single .rss page per sub; mid-month
   interior unsampled beyond what the .rss top feed carries).
7. Qwen 4 / Gemma 5 actual releases and specs (announced/rumored only).

## Machine receipts

- Epoch bounds: .venv/Scripts/python.exe datetime.fromtimestamp/isocalendar run this
  sitting: 2026-09-04T00:00Z = 1788480000, 2026-10-04T00:00Z = 1791072000,
  2026-10-03T00:00Z = 1790985600.
- Overlap greps (commands as run): `grep -ic "<phrase>" catalog/catalog.jsonl` for
  "Quantization Thresholds Replicate" (2), "PolAgentBench" (0), "Broken on Arrival"
  (2), "quantcheck" (0), "FrogNano" (0), "Clef" (0), "Apsara" (0), "Bonsai 2" (3),
  "voxel pagoda" (0), "FREE_MODEL_RATE_LIMIT" (0), "Orpheus" (0),
  "1000 requests/day" (0), "FreeToken" (5, all FREETOKEN_STEAL_20260822.md mirrors,
  inspected), "Gemma 5" (0), "Runner 1.0.0" (0); `rg -il` over memory/ (excluding
  .mimosa) for "FrogNano" (0), "DeepMostInnovations" (0), "1wjwxeq" (0),
  "sales-conversion-model" (0), "49953495" (0), "Clef" (101 raw substrings, 3
  sampled = game-design corpus HTML false positives); recursive grep
  for "2609.32042|2609.05881|quantcheck" over memory/ + watch/inbox returned the
  held raws + ARXIV_REGISTER + 09-30 sweep (connection already drawn there).
- Door call count this sitting: WebFetch 17 (2 dead-door probes, 15 answered or
  redirected-then-answered), WebSearch 1 (degraded, no links), arctic via WebFetch
  5, catalog greps 2 batches, 1 recursive grep backgrounded then answered.
