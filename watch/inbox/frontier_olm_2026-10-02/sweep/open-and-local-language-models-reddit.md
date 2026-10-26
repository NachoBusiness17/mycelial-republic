# Sweep: open-and-local-language-models via reddit

source-fetched: 2026-10-02
seat: sweep-open-and-local-language-models-reddit (Mag Resource Harness)
area: open-and-local language models via reddit; feeds the janitor KEEP verdict, the DeepSeek
off-peak lane, the cheapest-capable routing cells, and the follow-up door recipes.

## Doors (all probed this sitting, 2026-10-02)

| Door | Verdict today | Evidence |
|---|---|---|
| old.reddit.com/r/*/top.json | AUTH-WALLED (unchanged) | WebFetch returned the "Welcome to Reddit" login shell on all three subs (LocalLLaMA, LocalLLM, ollama); matches the 302-to-login `reason=lor2` curl record in `watch/inbox/frontier_olm_2026-10-02/lens/doors.md:40-56` |
| arctic-shift.photon-reddit.com | ALIVE, primary recipe | paginated 7,816 unique posts across 4 subs via `/api/posts/search`; comments via `/api/comments/search?link_id=<id>`; posts via `/api/posts/ids?ids=...` |
| api.pullpush.io | DEGRADED (429) | WebFetch 429 at sweep start; curl retry ~40 min later also `status:429` (exact: `curl -sS -m 30 -o /dev/null -w "status:%{http_code}" "https://api.pullpush.io/reddit/search/submission/?subreddit=LocalLLaMA&after=1788307200&size=5"`) |
| redlib mirrors | DOWN from this network | catsarch: WebFetch 429, curl schannel `SEC_E_UNSUPPORTED_FUNCTION`; perennialte.ch: 403; artemislena.eu: curl schannel `SEC_E_INTERNAL_ERROR`; privacyredirect.com: connection closed |
| WebSearch (site:reddit fallback) | RATE-LIMITED (1302) | every attempt this sitting returned 429/1302 per the account's burst behavior; no results ever surfaced |
| hn.algolia.com | ALIVE | used for the olm-x chase (below) |

### The recipe that restores r/LocalLLaMA (the doors-lens OWED item)

`/api/posts/search` params: `subreddit`, `after` (YYYY-MM-DD), `limit` (100/page max observed),
`sort` asc/desc, `sort_type` only `default|created_utc` (the API's own error body, verbatim:
`'sort_type' must be one of default, created_utc`; there is NO score sort and NO free-text `q`
param: `{"data":null,"error":"Unknown query parameter: 'q'"}`). Top-of-month is therefore
rebuilt by paginating `after=2026-09-02` with `before=<oldest-1>` and ranking by score locally
(script kept at `%TEMP%\arctic_sweep.py`, stdlib only, ran clean: LocalLLaMA 2,674 posts,
ollama 573, LocalLLM 3,936, MachineLearning 633). Thread deep-read = `/api/posts/ids?ids=`
plus `/api/comments/search?link_id=<id>&limit=100`. PullPush and all four redlib mirrors
failed from this network today; arctic-shift is the one live reddit surface.

## Per-question verdicts

**Q1 (gemma slots / Ling-3.1-flash radar, post-10-01):** No open-weight release or license
change touching gemma:2b/gemma4 found anywhere in the 30-day window (2,674 LocalLLaMA +
3,936 LocalLLM titles scanned); gemma-adjacent post-10-01 material is usage threads
(`1wvihh4` Gemma 4 31b on 32GB, `1wv0gyv` Qwen 27B vs Gemma 4 31B, `1wuqsyy` "Gemma 5 -
what to expect", all listing-read). The Ling-3.1-flash radar line is CONFIRMED on shape
(560B A25B) and still CLOSED-WEIGHT as of 10-02, open-source "planned soon"; three threads
triangulate it (items 1-2 below). The estate-side KEEP verdict for gemma:2b/gemma4
(`watch/inbox/frontier_olm_2026-10-02/lens/burns.md:104-106`) is field-corroborated, not
re-litigated, by item 4.

**Q2 (Qwen small-model supply drying + substitutes):** No post-10-01 thread restating the
supply-drying trend itself was found in the window's top lists (the trend was banked from
`1wrez7j` in the 09-30 fold per `lens/burns.md:70-71`). What the window DOES show is the
substitute side: the 27B class exploded (Qwen4-27B confirmed 09-22, `1wmzky1`, 2,006 points
listing-read; UkisAI Swift-Qwen3.8-27B `1wg7dd5`; fine-tune pile `1wv1ico`; Bonsai 2 27B
`1wlsaoq`; KAT-Coder-V2.5 35B-A3B `1wut9cr`), with the hardware floor named (`1wa19oj`
0.7 tok/s on 5060 Ti, listing-read). In the narrow small-model-with-tools regimes, the
field evidence splits the tier: gemma4 e4b survives tool-calling where Qwen Coder models
fail (item 4), a production 400-agent fleet routes deterministic loop work to a 4B and
conversation to 27B (item 5), and the new decision-model class (~0.5B-4B, constrained
outputs, millisecond answers) is the fresh substitute mechanism (item 3 + item 8). Ollama
Cloud is simultaneously retiring small/older roster entries (item 6), which is supply churn
on the hosted side, not the weights side.

**Q3 (olm-x free rung before Oct 7 close):** NOT ANSWERED from reddit this sitting. Title
search for `olm` across all three subs in-window: 0 rows. HN algolia's only hits for
"olm-x" are "oLMX" (a different llama.cpp-adjacent runtime) in a comment on the Unsloth
Dynamic 3.0 GGUFs story. WebSearch returned 429/1302 on every attempt. The Oct 7 close and
the "worth a probe slot" call therefore still rest only on the estate's own folds
(`lens/burns.md:186-187`, citing `frontier_olm_2026-09-30/DIGEST.md:83` and
`frontier_olm_2026-10-01/DIGEST.md:117-121`). What the rung serves remains OWED. Adjacent
find: Ling-3.1-flash has its own fresh free surface (Novita via Vercel AI Gateway, two-week
free trial, 256K context, item 1) which is a better-characterized probe target than olm-x
is today.

**Q4 (Ollama 0.35's 91 ms/decision Nimble/Tev1):** PARTIALLY VERIFIED, mechanism only. The
second primary exists and is strong: the official ggml-org blog "Decision models in
llama.cpp" (2026-10-02, fetched end to end) ships `/v1/systemone` (PR #29818) with models
Julia-1 144M / Laya 421M / Kev-4B / lev 4B / OpenJev 27B and a measured median-latency
table on RTX PRO 6000: 3 / 5 / 12 / 36 / 43 ms. It never mentions Nimble, Tev1, or Ollama.
So: "small constrained decision models answer in single-digit-to-tens of ms" is now
two-primary; the SPECIFIC 91 ms/decision Nimble/Tev1 figure from the 10-01 fold row 2
(`lens/burns.md:85-86`) remains SINGLE-SOURCE. No local instrument run was made this
sitting (the estate's Ollama 0.35 systemone-port steal card is specced, not fired, per
`lens/burns.md:97-99`); under the instruments-only law the 91 ms claim stays unverified,
not confirmed.

**Q5 (fallback doors):** ANSWERED, see door table. The r/LocalLLaMA surface is restored
through arctic-shift; PullPush is rate-limited (not proven dead; it answered for the 09-28
fold, raw files at `catalog` row `cab22182a596` = `watch/inbox/frontier_olm_20260928/sweep/_raw/pullpush_test.json`);
all four probed redlib mirrors are down from this network; old.reddit .json is still
auth-walled. Update the door recipes to arctic-shift-first.

## Banked items (full quotes and overlaps)

### 1. Ling-3.1-flash: closed weights, open-source "planned soon", scores + a fresh free trial surface

Thread `1wuyq9b` (r/LocalLLM, 2026-10-01 12:56 UTC), fetched via `/api/posts/ids` +
comments (8 read). Verbatim selftext: "Ant Ling plans to open-source Ling-3.1-flash soon.
Current access is through Novita on Vercel AI Gateway, with a two-week free trial offering
256K context." Same post: CyberGym 87.9, Terminal-Bench 4.0 40.4, and two long coding
demonstrations (17-hour Lua-to-x86-64 ELF compiler, 178/182 tests; Pyright 1.1.400 kept all
2,279 checks). Comments size it at ~500B with "You need 384 GB ram". Overlap: catalog +
memory grep for `ling-3\.1` = 0 hits; the 10-01 fold holds only the release radar row
(`lens/burns.md:84-85`). New: post-10-01 primary, access terms, and scores.

### 2. Ling-3.1-flash shape confirmed at 560B A25B; hands-on verdict prefers GLM 5.3 flash

Thread `1wuuqpp` (r/LocalLLaMA, 2026-10-01 09:16 UTC), selftext + 21 comments read.
Verbatim: "Made the hardest instrument to play with Ling 3.1 Flash 560B A25B (coming soon).
It's kinda crazy that 'flash' is in the 500B category these days, but hey, it works." Top
comment (jaykayenn, 6 pts): "great for the meat and potatoes, but gets kinda dumb once in a
while. GLM 5.3 flash is more grounded and consistent. Kinda close to DS 4.1, but still goes
into silly loops." Overlap: confirms the ~560B/25B-active radar shape banked 10-01 row 6;
the comparative verdict against the estate's own workhorse tier (GLM-5.3-flash) is new.

### 3. Decision models in llama.cpp: the second primary for the ms-class decision mechanic

Official ggml-org blog (2026-10-02), fetched end to end via WebFetch:
https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp . Verbatim: a decision
model "reads the input once, and its answer is always one of your options, with a
probability attached." Latency table (median, RTX PRO 6000): Julia-1 144M = 3 ms, Laya 421M
= 5 ms, Kev-4B = 12 ms, lev 4B = 36 ms, OpenJev 27B = 43 ms. Ships via `/v1/systemone`,
llama.cpp PR #29818; no mention of Ollama, Nimble, or Tev1. Companion reddit thread `1wvv6im`
(r/LocalLLaMA, 10-02, 33 comments read) adds the mechanic's lineage: "What Jev and those
competitors are are structured output predictors... the default model of OpenJev is just
DiffusionGemma" (scrdest) and "Literally starting seeing Jev-likes within 24 hours"
(Conexion). Overlap: `nimble|tev1` grep on catalog + memory = 0 hits; 10-01 fold row 2
(Ollama 0.35) is the first primary, this is the independent second. The 91 ms figure itself
stays unverified (no local instrument run this sitting).

### 4. Gemma4 E4B still wins the low-end tool-calling regime (janitor-slot field evidence)

Thread `1wv7o4s` (r/LocalLLM, 2026-10-01 18:45 UTC), selftext + 24 comments read. Verbatim:
"Gemma4 E4B Q8_0 runs very fast with up to a 100k context, and produces better results than
things that run considerably more slowly." and "Pretty much every other model I've tried,
including Qwen Coder models just fail to successfully call tools and/or run super slowly."
Commenter wadrasil runs three small models routed together and reports "Having 3 smaller
models with larger context working together ad hoc works a lot better than 1 big model."
Overlap: the KEEP verdict is already ruled twice (`lens/burns.md:104-106`); this is new
post-10-01 field corroboration that the e4b worker slot still has no clearer successor on
11 GB-class hardware, not a re-litigation.

### 5. Production 400-agent fleet splits regimes: 4B for the loop, 27B for conversation

Thread `1wt0tot` (r/ollama, 2026-09-29, 189 pts, selftext + 35 comments read). Stack:
Qwen3-4B Q4_K_M 4k context runs the main agent loop; abliterated Qwen3.8-27B handles rich
one-on-one; ~2.5s avg per call; low-priority reflections shed under queue pressure. OP in
comments: "The 4B does goals, trades, reflection, the plausibility checks... Gemma or
Mistral at the small tier is worth a benchmark." Commenter suggests a decision-model
classifier for the deterministic characters (KroniklyOnline). Overlap: `model_garden/
DUMB_AGENT_FRONTIER_DIG.md` already banked "small-model-with-tools wins only in narrow
regimes" (`lens/burns.md:124-126`); this is an in-the-wild instance plus a named gemma-at-
small-tier benchmark suggestion the estate can answer cheaply.

### 6. Ollama Cloud retirement wave: small/old roster entries cut for capacity

Thread `1wigesu` (r/ollama, 2026-09-17, official reply quoted in comments, 19 read).
Verbatim (Ollama staff comment): "As newer, more powerful models become available on
Ollama's cloud, we're retiring older, less powerful models to free up capacity for new
ones." Retired 2026-09-25: `deepseek-v4-flash:0731` -> `deepseek-v4.1-flash`, `glm-5.1` ->
`glm-5.3`, `qwen3.5:397b` -> `glm-5.3-flash` / `deepseek-v4.1-flash`. Overlap: the burns
ledger's free-resource section (`lens/burns.md:24-35`) covers Lightning/Chutes/SiliconFlow/
Scaleway and the DeepSeek window; hosted-roster retirement churn is new. The estate's local
ollama janitors are unaffected directly; the hosted free-rung map ages fast.

### 7. Door recipe: arctic-shift restores the reddit surface (OWED answered)

Working endpoint today: `https://arctic-shift.photon-reddit.com/api/posts/search` (params
and limits in the door table above). Verbatim API error that fixed the recipe: `'sort_type'
must be one of default, created_utc`. Overlap: `pullpush` 23 + `redlib` 7 catalog rows are
the 09-28 fold's raw door files; `arctic-shift` 0 rows in catalog and memory. The doors
lens left the reddit JSON recipe OWED (`doors.md:56`); this closes it with a tested recipe.

### 8. Post-10-01 open-weights decision-model wave (48 hours, five releases) - LISTING-READ

From the post-10-01 listings (titles/scores read from the arctic-shift listing fetch, thread
bodies NOT read): `1wv4zzi` "Clef: Open Weights decision model by Cloudflare" (10-01);
`1wv51nt` "NIRNAY: 450M decision model beats Jev on Banking77, runs on CPU" (10-01);
`1wuyrt2` "Vev: Jev-like decision models with vision - 4B/9B, local inference, open
weights" (10-01); `1wvfz9n` "Perplexity Decider 27B: Open weights decision model fine tune
of Qwen3.8 27B" (10-02); `1wvtc1j` "CalDec v1 - Fully Open Decision Model for Personal
Assistants" (10-02). Overlap: none of these thread ids appears in catalog or memory;
`caldec` catalog hit is a false positive (`CanonicalDecomposition.lean`). The wave timing
(days after llama.cpp's systemone PR) independently supports item 3's "Jev-likes within 24
hours" comment. Flagged listing-read: treat as leads, not verified finds.

## Anti-rebank statement

Per `lens/burns.md:174-180`: none of the eight items above re-banks a 09-28/09-30/10-01
confirmed find. Item 2 confirms the 10-01 radar row with a new primary; item 4 corroborates
the KEEP verdict with new field evidence; items 1, 3, 5-8 carry new thread ids or a new
primary. Known dead ends not rediscovered: Lightning/Chutes/SiliconFlow/Scaleway, KVarN's
unsourced clause, Ollama 0.35's unpublished 13-dataset benchmark.

## Instrument receipts

- `curl -sS -m 30 "https://arctic-shift.photon-reddit.com/api/posts/search?subreddit=LocalLLaMA&after=2026-09-02&limit=5&sort=desc&sort_type=score"` -> `{"data":null,"error":"'sort_type' must be one of default, created_utc"}`
- Sweep script (stdlib urllib, host-whitelisted): `%TEMP%\arctic_sweep.py`, ran via repo venv, output 7,816 unique posts, zero fetch failures.
- Post-10-01 listing script: `%TEMP%\arctic_post1001.py` (100 LocalLLaMA + 32 ollama + 100 LocalLLM rows).
- Deep-read script: `%TEMP%\arctic_deepread.py` (8 threads; `1wuw5oh` self-removed, 0 comments).
- PullPush retry: `curl -sS -m 30 -o /dev/null -w "status:%{http_code}" ...` -> `status:429`.
- Redlib: four mirrors, four distinct failures (429 via WebFetch; schannel UNSUPPORTED_FUNCTION; 403; schannel INTERNAL_ERROR; UND_ERR_SOCKET).
- HN algolia: `curl -sS "https://hn.algolia.com/api/v1/search?query=olm-x&hitsPerPage=8"` -> oLMX runtime comment noise.
- olm title search: 0 rows x 3 subs (command in transcript).
- A first Write of the sweep script was blocked by the Mimosa security hook (SSRF flag) and was rewritten host-whitelisted with stdout-only output; two background findstr greps mis-fired under bash (2.7 GB junk logs) and were deleted.
