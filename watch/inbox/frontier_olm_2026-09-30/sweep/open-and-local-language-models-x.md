# sweep: open-and-local-language-models via X door (2026-09-30)

source-fetched: 2026-09-30
(Activity window 2026-08-31 to 2026-09-30 bounds Pass 1; the 09-28 window's already-banked items
are excluded via the dedupe baseline below. Run by subagent sweep-open-and-local-language-models-x
on the Mag Resource Harness seat. Sibling of `watch/inbox/frontier_olm_20260928/sweep/open-and-local-language-models-x.md`.)

## Door status (honest)

- `site:x.com` WebSearch: 12 queries attempted, 8 returned usable results, 4 hit the Z.ai
  search backend `MCP error -429 code 1302` rate limit (the first query of the session, the
  Qwen3.5 query, the Artemis query, and one Field-Notes chase). Per the recipe's fallback,
  degraded queries are banked as search-result snippets with their URLs and labeled as such;
  none are presented as full reads.
- fxtwitter door (`https://api.fxtwitter.com/<user>/status/<id>`): 4/4 resolutions succeeded this
  session (cline, nahid_pro09, Google, BAI_AGI), JSON with author, timestamp, text. No 403s.
  Door continuity with `watch/inbox/frontier_olm_2026-09-30/lens/doors.md:47-56` (its probe
  answer: code 200 OK).
- Two X-side targets degraded to snippet-only: the "This Week In OS AI Field Notes" editions
  (Sept 11 and Sept 25, 2026) were reachable only through reposters' profile pages
  (`x.com/LeaderX_btc`, `x.com/sentient_found`), not status IDs, so they are NOT deep-read and
  NOT banked as items; and the merve (@mervenoyann) repost about labs releasing "small model
  variants" returned a homepage-level link only. Also unresolvable: a Featherless founder
  (@Calclavia) Sep 16 post (homepage link only).
- HN door: `hn.algolia.com/api/v1/items/43905942` and `search_by_date` both fetched clean.
- arXiv door: `export.arxiv.org` Atom query fetched clean (same recipe the lens verified live
  at `watch/inbox/frontier_olm_2026-09-30/lens/doors.md:14-18`).

## Estate grounding read this session

- `watch/inbox/frontier_olm_2026-09-30/lens/laws.md:23` (sensing is never judgment; "Banked is
  not verified, always. Free seat proposes; local basecamp disposes."),
  `lens/laws.md:24` (funded set: Hermes/Nous primes + grok-4.7; Anthropic unfunded).
- `lens/burns.md:57-59` (the standing-lane one-liner this lane's RQ2 points at: LLM7 free-class
  4 to 3, GLM-5.3-Flash dropped, DeepSeek 401-alive, Featherless 22,059 served rows vs 28.6k
  counter gap, Lightning lane closed FULLY DEAD).
- `lens/doors.md:29` (HN "local llm" nbHits 2916, top hit "Show HN: Clippy - 90s UI for local
  LLMs" 1122 points objectID 43905942) and `doors.md:14-18` (arXiv door recipe, verified live).
- `lens/corpus.md:23` (frontier_thinking shelf 11 files) and `lens/corpus.md:13` (state/arxiv
  3,776 rows).
- Dedupe baseline: `watch/inbox/frontier_olm_20260928/register.jsonl` (21 rows, titles read
  this session) - its OLM-adjacent items (DeepSeek V4.1 Flash, HF/NVIDIA, RWKV-7 G1j, Nemotron
  3.5 Lightning fine-tune, Qwen3.8-Flash-Next, FunctionGemma extension, sub-2B MCP tool-calling
  CPU benchmark, quantization-thresholds study, Qwen3.8 27B quantization benchmarking) are NOT
  re-banked below.

## Pass 1 - candidate sweep (33 considered, last 30 days)

1. @cline 2092666316125864191 - GLM-5.3 Flash free in Cline (2026-08-26, snowflake-decoded
   this session). DEEP-READ (fx).
2. @nahid_pro09 2102229686378213649 - GLM-5.3-Flash unlimited free on ZCode extended (09-22).
   DEEP-READ (fx).
3. @BAI_AGI 2098381710522233121 - free ends Sep 12, then 90% off pricing (09-11). DEEP-READ (fx).
4. @BAI_AGI 2095852797225017652 - free access via chat.b.ai (09-04). Snippet only.
5. @jietang 2095692002633638066 - free in ZCode 10h/day Sep 3-18 (09-04). Snippet only.
6. @zcode_ai 2095526557670596868 - GLOBAL BUILD launch (09-03). Snippet only.
7. @VaibhavSisinty 2094915717204443294 - 100M free tokens drop (09-01). Snippet only.
8. @jahooma 2093137551918051624 - GLM 5.3 Flash free, funded by developer ads (08-28).
   Snippet only.
9. @pengsonal 2092824534894186956 - $0.02 3D-visualization anecdote. Snippet only.
10. @mikenevermiss 2091091496862675337 - ZenMux free API key for GLM 5.3 (08-22). Snippet only.
11. @Google 2039736220834480233 - Gemma 4 release (2026-04-02, decoded). DEEP-READ (fx).
12. @GoogleDeepMind 2039735446628925907 - "run on your own hardware" (04-02). Snippet only.
13. @GoogleOSS 2039734605998096891 - Apache 2.0 license shift (04-02). Snippet only.
14. @natolambert 2039736104052486326 - Apache 2.0 adoption comment (04-02). Snippet only.
15. @googlegemma - Gemma 4 as Android Studio local provider (no status ID). Snippet only.
16. @cerebras article 2067643238077575514 - first GDM model on Cerebras. Snippet only.
17. @AILeaksAndNews 2039052892921794561 - Gemma 4 pre-release source leak. Snippet only.
18. "This Week In OS AI Field Notes" Sept 11 edition (via @LeaderX_btc) - under-4B #1 mention.
    Snippet only, DEGRADED.
19. "This Week In OS AI Field Notes" Sept 25 edition (via @sentient_foundation) - NASA/IBM
    Lunar Foundation Model. Snippet only, DEGRADED.
20. @0xIlyy repost - MiniCPM5-2B as on-device "notification manager". Snippet only.
21. @FeitengLi - Qwen-Image-2.1 local on 12GB VRAM via Unsloth GGUFs. Snippet only.
22. Tencent Hunyuan 4 Preview, open-source 770B MoE (Field Notes Sept 11). Snippet only.
23. @mervenoyann repost - labs "release small model variants of their frontier models".
    Homepage link only, DEGRADED.
24. @Calclavia (Featherless founder) Sep 16 post. Homepage link only, DEGRADED.
25. MiniCPM5-2B on Artificial Analysis Intelligence Index v4.2 among open models under 4B
    (cryptobriefing.com snippet). DEEP-READ of the HF model page instead.
26. Qwen3.5 family: 397B-A17B flagship + 0.8B/2B/4B dense, 256K ctx (towardsai + HF snippets).
27. Qwen3.8-Max open weights Aug 12, 2026 (aireiter.com snippet).
28. TheDrummer Artemis-31B v1.1/v1.2 + GGUFs + Featherless "New" tag. Featherless page
    DEEP-READ; release date not verified.
29. Featherless live model counter. DEEP-READ (featherless.ai/models, 2026-09-30).
30. pulse2.com - Featherless $20M raise, "more than 30,000 open models" (May 2026). Snippet only.
31. HN item 43905942 "Show HN: Clippy - 90s UI for local LLMs". DEEP-READ (items API).
32. HN search_by_date "local llm" 2026-09-27..09-30 wave (10 hits, IDs captured). DEEP-READ.
33. arXiv Atom query "on-device"+"language model", 8 newest entries. DEEP-READ.

## Pass 2 - deep reads actually executed (9 fetches, bar was 5)

1. fxtwitter cline 2092666316125864191 - verbatim: "GLM-5.3 Flash (Ox Alpha) is free in Cline.
   320B params with 18B active, beating frontier models on benchmarks." Plus fetch-surfaced
   claims: "fastest growing model in Cline history", over 11% of all Cline traffic in under a
   week; quoted Z.ai specs: MIT license, natively multimodal, 1M-token context.
2. fxtwitter nahid_pro09 2102229686378213649 - verbatim: "GLM-5.3-Flash is 100% FREE with
   UNLIMITED usage right now on ZCode (Extended)". Post says the Z.ai coding-plan promo was
   extended through October 7.
3. fxtwitter Google 2039736220834480233 - Gemma 4 release, "our most intelligent open models to
   date", built from Gemini 3 research, run on your own hardware, Apache 2.0 (2026-04-02).
4. fxtwitter BAI_AGI 2098381710522233121 - free Ox Alpha access ends Sept 12 09:59 SGT, then
   verbatim: "Input as low as $0.015/M tokens and output at $0.05/M tokens" (90% discount).
5. hn.algolia items/43905942 (Clippy) - felixrieseberg; Electron + node-llama-cpp; 98.css
   styling; multiple downloadable models; fully local. Top comments: dependency-bloat critique
   ("119 other libraries"), "Having ollama support would be useful as well!" (alkh), and a
   trademark thread: Clippy is trademarked by Microsoft (USPTO + continued use in Fluent Emoji).
6. hn.algolia search_by_date "local llm" (hitsPerPage 10, created_at_i > 1758988800) - the
   09-27..09-30 wave: "Local LLM Observability" (49908457), "I Turned 17 Hours of Video into a
   Second Brain with Local LLM" (49908095), "Pklm-sandbox - A lightweight open-source
   LogitsProcessor for local LLMs" (49885964, 09-28), "Show HN: Yengi, a local-first AI
   development environment" (49879268), "Local LLM extraction plugin for Obsidian (100%
   offline)" (49864757), "A wall that listens: the local-LLM pipeline behind an AI party in
   Vilnius" (49866154). All 1-3 points: the daily stream is pipeline/plug-in framing, not chat.
7. export.arxiv.org Atom query (all:"on-device" AND all:"language model", 8 newest) - HARISSA
   (2609.38006v1, 09-29): inference-time self-checks for local LM deployment, the local model
   decides which queries deserve extra compute and which answers to defer. IronLLM
   (2609.36860v1, 09-29): 654M-parameter edge-native model, 1.48x decoding speedup claim.
   Chinese-Jev (2609.36965v1, 09-29): small decision model, INT8 mobile deployment ~1.0s per
   decision. PhoneCLI (2609.35671v1, 09-28): app interfaces to callable commands for mobile
   agents.
8. featherless.ai/models (2026-09-30) - counter reads "Models 50,878"; popularity buckets sum
   to it: Top 2% 1,142 / Very Popular 2,803 / Popular 5,789 / Moderate 7,550 / Low 13,547 /
   Obscure 20,047. Trending "New": Qwen3.5-9B, Artemis-31B-v1.2. Most popular: Qwen3-0.6B
   (~29.6M downloads), Qwen3-VL-8B-Instruct (~16.6M), gemma-4-26B-A4B-it (~12.8M),
   gpt-oss-120b, Kokoro-82M.
9. huggingface.co/OpenBMB/MiniCPM5-2B - 2,516,756,480 params (~2.5B dense, BF16), LlamaForCausalLM,
   42 layers, GQA 16Q/2KV; created Sept 6 2026, last modified Sept 29 2026; Apache-2.0; 131,072
   ctx; EN+ZH; card: "It is a dense 2B Transformer that scales up the same training recipe,
   built for on-device, local deployment."; GGUF/MLX/LiteRT builds; tags on-device, edge-ai;
   positioned for local assistants, coding agents, tool-use, resource-constrained deployments.

## Answers to the four research questions

### RQ1 - open-weight models for the janitor/scut slots (released since 09-28?)

Honest headline: this lane found NO credible X or arXiv signal of a NEW small open-weight
model released in the 09-28..09-30 window for the janitor/scut slots. The in-window churn is
model-card updates (MiniCPM5-2B modified Sept 29), quantization/hosting moves (Artemis-31B
v1.2 tagged New on Featherless; Qwen3.5-9B also tagged New there), and papers (HARISSA,
IronLLM, Chinese-Jev, all 09-28/09-29). The standing answer for the slots remains the ladder
the estate already holds: `memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:34`
names "model ladder Qwen3-0.6B / MiniCPM5-2B / Qwen3.5-4B" - and Featherless live data
independently corroborates the rungs (Qwen3-0.6B is the single most-downloaded model on the
platform, ~29.6M downloads, fetched 09-30). Self-reported claims the funded tier must still
verify (laws.md:23: banked is not verified): cline's "320B params with 18B active, beating
frontier models on benchmarks" (vendor self-report, 08-26), cline's "fastest growing model in
Cline history" + >11% traffic share (no third-party source), MiniCPM5's "#1 among open-source
models under 4B" on AA Index v4.2 score 15 (index placement via cryptobriefing snippet; not
independently fetched), IronLLM's 1.48x decoding speedup and Chinese-Jev's ~1.0s/decision
(arXiv abstract claims, unfunded-tier unverified). Gemma 4 (Apache 2.0, 2026-04-02) predates
the window and is already in holdings discourse (DiffusionGemma 26B-A4B at
`memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:38`); its gemma-4-26B-A4B-it
variant shows 12.8M downloads on Featherless today - relevant to the estate's literal `gemma4`
short-worker slot as a capability ceiling, not a new release.

### RQ2 - what replaced the dead Lightning lane and the dropped GLM-5.3-Flash rung

GLM-5.3-Flash is not dead model-side; free access moved to agent-bundle promos, and the Sep 22
post (deep-read) says the Z.ai coding-plan promo was EXTENDED THROUGH OCTOBER 7 with unlimited
GLM-5.3-Flash on ZCode. That extends the already-held Sep 3-20 campaign
(`memory/thinking/app_reasoning.jsonl:4709`, a 09-03 session reasoning over the campaign
window) - the extension is the new fact. Replacement lanes observed this session, dated by
snowflake decode: ZCode extended unlimited (09-22), BAI_AGI 90%-off post-free pricing $0.015/M
in / $0.05/M out (09-11), Cline free lane (08-26), jahooma's ad-funded free coding agent
(08-28), ZenMux free API key (08-22). Lightning lane: NO X-side replacement signal found this
session - the lane's replacement remains OWED (the only Lightning item in the prior register
is the Nemotron 3.5 Lightning fine-tune paper, already banked 09-28). Featherless 22,059 vs
28.6k gap: NO published explanation located. Fresh byte evidence re-frames it: the live counter
read 50,878 on 2026-09-30 (buckets summing exactly), and pulse2 reported "more than 30,000" at
the May 2026 raise - the listed-models counter climbs fast enough that any snapshot pair
(22,059 served rows vs 28.6k counter) was a two-denominator artifact at one moment: served
rows (models actually served to us) vs listed models (catalog size). The estate's 22,059 number
is held in the burns lane files (grep hit: 5 catalog rows + agent_state versions); the 50,878
reading is new.

### RQ3 - what the HN local-LLM wave says about thresholds for the estate's local tier

From the Clippy deep-read (1122-point thread): the winning UX shape is a toy shell over a real
engine - Electron + node-llama-cpp + 98.css, fully local, zero cloud calls, simple config,
multiple downloadable models. Three transferable thresholds: (1) Ollama interop is table
stakes - the most feature-requested comment is verbatim "Having ollama support would be useful
as well!" and the estate's local tier already rides Ollama; (2) dependency restraint is a
review criterion in this community (the top criticism catalogs bundled libraries as bloat) -
relevant to any estate dashboard shipping heavy JS; (3) TRADEMARK: the thread's dig found
Clippy is an active Microsoft trademark (USPTO records + continued use in Fluent Emoji). The
estate brands its standing reminders "Clippy" (AGENTS.md Clippy section) - that is the same
name surface the thread flags; per the counsel-triage law (`memory/rib/RIB_LAWYER_BOOT_20260904.md:8-30`)
this deserves a COUNSEL verdict line, filed here as UNVERIFIED-RISK, not CLEAN. Capability-side,
the 09-27..09-30 search_by_date wave shows the local tier's job framing has moved from chat
toy to pipeline component (observability, video-to-second-brain, LogitsProcessor sandbox,
offline Obsidian extraction, a party-wall listening pipeline): the estate's janitor lanes fit
the wave's shape already; the UX lesson is to keep the operator-facing surface toy-simple and
the engine swappable.

### RQ4 - the repeatable arXiv harvest, and which state/arxiv rows are stale

The repeatable harvest ALREADY EXISTS in-repo: `mag/arxiv_harvest.py` - RECORD via the same
Atom API the lens door verified (`mag/arxiv_harvest.py:35-36,63-65`, categories cs.AI, cs.LG,
cs.CL, newest-first), MASSAGE to per-day digest.jsonl deduped against prior days
(`mag/arxiv_harvest.py:105-125`), MINE via a flash pass scoring titles against INTEREST_MAP
(`mag/arxiv_harvest.py:43-52,128+`). Run as `python -m mag.arxiv_harvest [MAX_PER_CAT]`
(`mag/arxiv_harvest.py:20`). It is live: HARISSA (2609.38006) is already in today's harvest -
`catalog/catalog.jsonl:690817` points at
`state/arxiv/2026-09-30/2609.38006v1.txt`, mtime 2026-09-30T06:31:00Z. Byte census run this
session (`ls state/arxiv/*` + per-dir counts): 26 day-partitions, 2026-09-05..2026-09-30,
summing to exactly 3,776 files (matches `lens/corpus.md:13`); of those, 26 are digest.jsonl
and 3,750 are paper .txt files. The stale/hole finding: NINE day-partitions (09-08, 09-12,
09-13, 09-14, 09-15, 09-19, 09-20, 09-26, 09-27) hold ONLY a 0-line digest.jsonl (verified by
`wc -l` = 0 on three of them) - those days contributed zero rows; the harvest has holes, not
aged rows (all content is <= 26 days old). Structural gap for THIS area: INTEREST_MAP
(`mag/arxiv_harvest.py:43-52`) scores falsifiers/caching/orchestration/game-benchmarks/
provenance/training/serving - it has NO small/on-device-LM term, so model-release-adjacent
papers for the janitor tier are under-captured by the MINE pass (HARISSA landed only via the
general cs.CL sweep). Cheapest fill: add an interest-map line for on-device/small models and
rerun; backfill the nine hole-days with the doors.md:14-18 recipe. Whether MINE drops feed the
frontier_thinking shelf (11 files, `lens/corpus.md:23`) was NOT verified this session - the
link between research-inbox drops and that shelf is asserted by the ask, not confirmed by a
path I read.

## Overlap record (greps actually run this session)

- "GLM-5.3-Flash" in catalog/catalog.jsonl: 29 hits (held, expected - it is a dropped estate
  rung). Campaign Sep 3-20 held at `memory/thinking/app_reasoning.jsonl:4709,5718`.
- "MiniCPM5" in memory/: held at `memory/research_packs/THE50_W3_T11_TYPED_DECISION_ORACLES.md:34,260`
  (already in the estate's model ladder) + gapwave/corpus_selfsteal/mickey17 mentions. NOT
  re-banked as new.
- "HARISSA" in catalog: 1 hit, `catalog/catalog.jsonl:690817` (today's own harvest). The
  esoterica pg*.txt hits are the spice word, false positives.
- "90s UI for local LLMs" in memory/: 1 hit in `memory/trajectory/steps.jsonl:37342` - that is
  THIS session's own echoed command (session_id sess_dwf-dwfrun-...-actor_3_4), a false
  positive, not a prior holding.
- "Artemis-31B": only the same self-echo - genuinely new to holdings.
- "22059"/"22,059": 5 catalog rows + agent_state version files (the burns lane's own numbers).
- "26B-A4B": held at `THE50_W3_T11_TYPED_DECISION_ORACLES.md:38,278` (DiffusionGemma).
- Cline "11% of all traffic" / "fastest growing model in Cline": no hits - new.

## OWED (not done, stated)

- Published explanation for the Featherless 22,059 vs 28.6k pair: not found; live counter
  (50,878, 09-30) recorded instead.
- Lightning-lane replacement: no X-side signal found this session.
- "This Week In OS AI Field Notes" status IDs (both September editions): unresolvable through
  this lane's search results; content snippet-only.
- Artemis-31B v1.2 release date: not verified (HF/Reddit snippets only; reddit door is closed
  per `lens/doors.md:31-45`).
- MiniCPM5 "#1 under 4B, AA Index v4.2, score 15": third-party snippet, page not fetched.
- The MINE-pass -> frontier_thinking shelf link: not verified.

## Steal candidates for the estate (proposals, sensing-tier)

1. Add a small/on-device-LM line to INTEREST_MAP in `mag/arxiv_harvest.py:43-52` and rerun -
  makes the existing harvester capture this area's papers (HARISSA-class routing research).
2. Read HARISSA out of `state/arxiv/2026-09-30/2609.38006v1.txt` and prototype its
  self-check/defer gate as the scut lane's escalation predicate (cheapest capable tier =
  paper-shaped version of the driving ladder).
3. File the Clippy-trademark note against the estate's "Clippy" standing-reminders branding
  (counsel triage, UNVERIFIED-RISK).
4. Wire the GLM-5.3-Flash Oct 7 extension window into the runner's fold/judgment lane the way
  the Sep 3-20 window was wired (`memory/thinking/app_reasoning.jsonl:4709` shows the
  in-window routing plan); it expires Oct 7.
5. Funded-tier verification queue: cline's 320B/18B + "beating frontier" + 11%-traffic claims;
  IronLLM 1.48x; Chinese-Jev ~1.0s/decision.
