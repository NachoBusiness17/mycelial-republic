# sweep: swarm-orchestration via x (frontier_olm 2026-10-01)

source-fetched: 2026-10-01
Seat: sweep-swarm-orchestration-x (workflow gopher). Predecessor: `watch/inbox/frontier_olm_2026-09-30/sweep/swarm-orchestration-x.md` (read in full this ask; its 11 pass-2 reads are the dedupe baseline: arXiv 2609.34320, 2609.34198, 2609.12191, 2609.02246, 2609.02783, the dynamic-workflows cookbook, paddo.dev, claude-code#67636, codex#15379, oneaway.io, agentic-ai.readthedocs.io; none re-banked). Sibling lanes in THIS carrier (their banked items also treated as taken): `swarm-orchestration-arxiv.md` (HiveMind 2604.17111, PRIMA 2605.24775, ProgRouter 2608.25992, Beyond Symmetric Agents 2609.35875, TalkMesh 2609.30578, CED 2609.25570, ME-Decoding 2609.18723) and `swarm-orchestration-hn.md` (Magnitude, Chief of Staff, TokenOps, Relay, leaderless-MAS asks, noperator).

## Estate grounding read this ask

- `watch/inbox/frontier_olm_2026-10-01/lens/laws.md` in full: law 22 one-controller (line 41), law 34 consensus illusion measured 0/3 (line 59), Part 2 Q1 flock decode redesign (line 70), law 21 emergent-vs-deterministic per-task measured claim (line 40).
- `watch/inbox/frontier_olm_2026-10-01/lens/burns.md` in full (hermes window-1 ledger lines 15-16, 35-44).
- `memory/runs/hermes_burn/usage.jsonl` re-read this ask: `wc -l` = 16 rows; cost_usd sum by hand = 5.9155 (rows 1-16: 0.388+0.4664+0.77+0.3802+0.2466+0.2562+0.5065+0.2466+0.1862+0.4939+0.3837+0.2466+0.5754+0.3706+0.2466+0.152); per-turn banking with ts, id, model, turn, prompt/completion/reasoning tokens, channel, ok. Matches burns.md exactly.
- AGENTS.md fan-out width law (workflow children maxAttempts 0 vs Task agents maxAttempts 11, width 10 clean at 109.4M tok/h, rolling-throughput limit).

## Door health (honest)

- The X index via the Z.ai search backend held real x.com results this cycle (unlike 09-30, when it was nearly empty). Four queries fired in parallel worked, then the backend 1302/429-stormed on every subsequent parallel batch; serial small batches recovered it. This is the second independent observation of the rolling-throughput shape on this account's own sweep instrument (09-30 was the first).
- fxtwitter door: single posts and articles resolve clean as JSON (`api.fxtwitter.com/<user>/status/<id>`, and `i/status/<id>` also resolved an article with full content blocks). `x.com/i/trending/<id>` pages 404 on fxtwitter (they are aggregations, not posts) - the graceful-wrap-up item was chased to its underlying post instead. No fabrication of any un-resolved thread.
- Searches for RQ2 (flock decode) and RQ3 (controller-of-controllers) returned ZERO in-window x.com posts across 6 query shapes; the in-window X surface for those questions does not exist in the index I can reach. Named fallbacks below.

## Pass 1: candidate pool (62 considered; dates from snowflake arithmetic run this ask)

Snowflake timestamps computed for 32 ID-bearing candidates via `(id >> 22) + 1288834974657`. In-window (2026-09-01..10-01): tobyord 09-21, jev article 09-29, gmkurtzer 09-30 (read, irrelevant: consciousness debate, dropped), graceful-wrap trend 09-25 + v_shakthi 09-27, AGTPinsights 09-26, codex-await-reset 09-26, codex-extra-reset 09-26, gpt6astra reset 09-10, splunk 09-23, ritu 09-26, cisco 09-08. Out-of-window flagged: llmjunky 01-23, akshay 03-15, rohit4verse 04-07 + 04-29, maryammiradi 04-19, av1dlive 06-01 + 06-04, jarodxu7 06-04, steve_messina 06-17, addyosmani 07-03, mattrickard 07-03, claudedevs 07-21, rohonchain 07-23, yongkyun 08-19, lunarresearcher 08-21, IOSG 08-20, maarcoofdezz 08-24, neil_xbt 08-26, weeklyvoice 08-24, testingcatalog 08-29, thsottiaux 08-29, djfarrelly 06-17, akshay four-pillars 06-24, poteto 06-25, mvanhorn 06-23, posthog 08-18, cyrilxbt 08-18, marfinxx 08-30, plus non-X: arXiv 2601.07245 (Jan), suhaib consensus-hallucination post, openreview Diversity Collapse (unread, OWED).

## Pass 2: items read end to end this ask (7)

1. IOSG Ventures X article "From Benchmark Gains to Willingness to Pay: The Demand Illusion of Model Fusion" - ALL 75 content blocks via fxtwitter JSON (`_fx/_iosg_modelfusion_raw.json` cached in this dir). Out-of-window (08-20) but banked with reason: RQ2's X-native in-window surface is empty and this is the single densest flock-decode economics source the door surfaced.
2. @0xRicker "Jev Engineering: Parallel Decisions for a 300-Agent Kimi Swarm" (09-29) - ALL article blocks via fxtwitter (`_fx/_jev_article_raw.json`). 63,386 views.
3. @v_shakthi on the Claude Code graceful wrap-up (09-27) - full raw_text (1,283 chars) via fxtwitter.
4. @tobyordoxford on lambda parallelizability (09-21) - full text (274 chars) via fxtwitter.
5. @splunk Token Meter launch post (09-23) - full text via fxtwitter.
6. @RituWithAI Opik observability post (09-26) - full text (3,194 chars) via fxtwitter; DEMOTED from banking by the overlap check (estate already ran an Opik wave 09-12).
7. @AGTPinsights Codex force-reset post (09-26) - read via fxtwitter extraction (the fetch model flagged its own excerpting; the quoted opening line is its verbatim text). Weakest read of the seven, weakest item banked.

## Banked items

### 1. IOSG: The Demand Illusion of Model Fusion (2026-08-20, out-of-window flagged)
URL: https://x.com/IOSGVC/status/2090402323227099591
Quote: "Out of 100 GPQA-Diamond questions, roughly 13 would leave every candidate model wrong, giving voting, judging, or synthesis no correct answer to select."
Why it matters: independent published co-failure measurement behind the consensus-illusion rib (laws.md:59: flock consensus agreed with strong-remote 0/3 at HIGH strength). Citing Josef Chen's 67-model/21-provider study: predicted all-wrong 2.3% vs measured 5.2% on open math (2.3x), 7.9% on execution-graded code, 12.7% on GPQA-Diamond. Voting cannot fix correlated tails, so the flock decode redesign (laws.md:70) must add independent information or external verification, not more votes. Also banks: Fusion trigger-rate economics (1% -> 1.03-1.04x cost, 10% -> 1.30-1.40x, 25% -> 1.75-2.00x), tail latency concentrating on the most valuable tasks, Devin Fusion's downgrade boundary ($5.12 -> $3.00 per task at 57.0 -> 57.6, five cases -25%..-62% cost with scores +12..-27), and "verified cost per successful outcome" as the metric the per-turn usage.jsonl layer feeds.
Overlap: grep catalog.jsonl "Model Fusion" = 1 hit, and it is OUR OWN pinned survey `state/arxiv/2026-09-18/2609.19553v1.txt` ("From Parameters to Behaviors: A Survey of Model Fusion"); "Demand Illusion" = 0; "Combining Language Models" = 0; "co-failure" = 0. The article's numbers are new to the estate; the concept is partially pinned.

### 2. @0xRicker: Jev Engineering, parallel decisions for a 300-agent Kimi swarm (2026-09-29)
URL: https://x.com/0xRicker/status/2104935716492869999
Quote: "Reviewing 300 results one by one is 300 requests, each with its own network wait and its own copy of the shared context."
Why it matters: the practitioner mirror of the fan-out width law's retry half. Its six steps: find the serial review queue hiding after the parallel fan-out; split independent verdicts from comparative decisions (two stages); batch all verdicts into ONE typed call (shared context sent once, not 300 times); ask ahead with speculative branches and discard the wrong ones ("the answers you discard are cheaper than the wait"); "Measure the trips, not just the tokens" (chunking 30x30 = 10 requests as middle ground); close the loop so ONLY the misses go back in shrinking single-pass rounds (300 -> 29 -> handful), which without the single-pass review "teams run once and ship whatever the first pass produced". That last law is the estate's amend-not-rewrite / redo-only-the-failed-stage shape, published, with the Jev decision-model pricing ($0.042/M input) making rounds cheap.
Overlap: catalog "Kimi swarm" = 0, "300-agent" = 0, "0xRicker" = 0. CAVEAT: the estate holds `corpus/library/jev_steal_library/` (09-19: jev-persona-eval-harness.md maps the SAME Jev decision model onto the persona eval harness, Noul decomposition 48.3% -> 98.3%); that steal covers Jev-as-eval-harness, NOT the orchestration review shape, so this item is new work, not a re-bank.

### 3. @v_shakthi: Claude Code graceful wrap-up at the 5-hour limit (2026-09-27)
URL: https://x.com/v_shakthi/status/2104058568312029203
Quote: "A hard cutoff mid-edit leaves a half-written file and no record of what was next. A clean stop with a written remainder is usable the moment the window resets."
Why it matters: the provider-native version of checkpoint-pause-resume (PRIMA 2605.24775, banked by today's arxiv sibling): on hitting the limit, the agent draws "a small, fixed allowance drawn from the weekly limit", finishes the edit in flight, runs the tests it can, and writes the remaining work as a handoff ("the same fix still needed on the mobile path"), closing with "Wrapped up past your usage limit" plus the reset time. Tiered rollout: Pro once a week, Max and Team Premium every hit. Estate analog: the first-429-is-a-HOLD law plus receipt landing; the handoff-instead-of-broken-diff is exactly the estate's turn-2 no-echo / empty-carrier defect class named in WINDOW1_STATE.md.
Overlap: catalog "graceful wrap" = 0, "Wrapping up" = 0; memory grep hits on "graceful wrap" were this session's own trajectory rows (self-noise) and a DIFFERENT 09-30 raw context ("recovered gracefully ... re-ran"). New to the corpus.

### 4. @tobyordoxford: lambda parallelizability of agent work (2026-09-21)
URL: https://x.com/tobyordoxford/status/2102118035934879885
Quote: "People should keep tracking this as new estimates for lambda appear and (especially) when new orchestration methods increase the value of lambda for a given type of task."
Why it matters: the width-law's theoretical frame from the outside. Toby Ord's lambda is the parallelizability parameter of AI R&D tasks; the claim the estate should track is that ORCHESTRATION METHODS THEMSELVES raise lambda per task type, which is the published-adjacent version of "dispatch shape is the retry strategy": changing the shape changes how much of the work can ride the width-10 clean lane at all. Small post (274 chars, 37 likes, 1,889 views), banked as a pointer, not a measurement; it publishes no lambda estimate.
Overlap: catalog "Toby Ord" = 0, "parallelizability" = 0. New.

### 5. @splunk: Token Meter, real-time coding-agent cost tracking (2026-09-23)
URL: https://x.com/splunk/status/2102865587877597226
Quote: "Meet Token Meter, a free, open-source tool that lets you track coding agent costs in real time - right from your menu bar"
Why it matters: RQ4's practitioner frame is the estate's own question ("Is that run costing $1 or $100?"), answered with a live per-run instrument. The estate already built the deeper version (usage.jsonl per-turn rows with per-model cost + channel diagnostics; batch5's TOKEN_METER_20260906.md read the cli db's model_usage table with cache-aware billed arithmetic), so the steal is the UX/positioning: per-run cost surfaced AT RUN TIME in the operator's menu bar, not in a post-hoc ledger. The README (github, linked via splk.it shortener) was NOT fetched this ask; shortener destination unread, OWED.
Overlap: catalog "Token Meter" = 1 hit and it is OUR OWN instrument `memory/runs/batch5_20260906/TOKEN_METER_20260906.md` - a name collision, different artifact. No prior holding of the Splunk tool.

### 6. @AGTPinsights: OpenAI force-reset Codex usage limits (2026-09-26)
URL: https://x.com/AGTPinsights/status/2103963160793526718
Quote: "OpenAI just force-reset Codex usage limits for paid users today, and it's splitting the community."
Why it matters: provider-side quota governance as an orchestration hazard: resets propagated across Codex and ChatGPT Work as an outage apology (per the post, confirmed by Tibo @thsottiaux 12:16 AM ET 09-27), and the reset WIPED banked unused quota (cited case: 64% of weekly usage lost with 3 days left) with no banked-reset or opt-out. For a fleet that banks budget across windows (Hermes $220 armed, XAI credits), the named risk is: quota you assume persists can be force-reset by the provider; ledger assumptions need a re-read after any provider-side reset event. Weakest item: 3 likes, 12,595 views, and the substance beyond the opening line reached me through the fetch model's extraction.
Overlap: catalog "force-reset" = 0; the 09-30 carrier's Anthropic Sept-14 limits items are a different provider event. New.

## Verdicts per research question

- RQ1 (fan-out/retry shapes vs the estate's measured split): YES, three X-native confirmations. The Jev article's "measure the trips, not the tokens" + only-misses-go-back loop and the graceful wrap-up's spend-a-fixed-allowance-then-handoff both land on the estate's side of its own measured split (retry path and checkpoint shape beat raw width); neither publishes a tok/h envelope, so the estate's width-10 109.4M tok/h bank remains the sharpest public number I can find (same verdict as the 09-30 lane).
- RQ2 (flock/multi-model decode): the X door yielded NO in-window practitioner threads; the strongest door find is the IOSG article (out-of-window, flagged) whose co-failure numbers (2.3x, 12.7%) give the flock decode redesign its missing statistical floor: correlated failure caps what voting can recover, so a task-space decode must buy independence or verification. Combined with sibling-banked TalkMesh (GRPO hint protocol) the redesign direction is: communicate answer-space hints, verify against ground, never trust consensus strength.
- RQ3 (controller-of-controllers vs the one-controller law): NO in-window X item found across 6 query shapes; all X-native RQ3 leads are June-era and unread beyond snippet (OWED below: djfarrelly duplicate-sub-agent loop architecture, akshay maker/checker separation, addyosmani false parallelism). The one-controller law (laws.md:41) got no published challenge or confirmation through this door this cycle; the HN sibling's Chief-of-Staff thread remains the carrier's in-window RQ3 holding.
- RQ4 (per-agent-turn cost accounting): the estate's usage.jsonl (16 rows, $5.9155, per-turn, per-model, per-channel) is finer than anything the door surfaced; X practice is converging on the same primitive from the tool side (Splunk Token Meter per-run live; Opik per-call cost+trace, already known to the estate via the 09-12 wave; IOSG's "verified cost per successful outcome" is the outcome-side metric the per-turn layer feeds but no source prices per agent-turn).

## Overlap record (greps run this ask)

`grep -ic` over `catalog/catalog.jsonl`: Jev 99 (all `corpus/library/jev_steal_library/*` + KEV model-card substring noise), Kimi swarm 0, graceful wrap 0, Wrapping up 0, Toby Ord 0, parallelizability 0, Token Meter 1 (our own batch5 file), Model Fusion 1 (our pinned 2609.19553 survey), Demand Illusion 0, Combining Language Models 0, co-failure 0, Opik 12 (incl. `memory/runs/p20_pending_wave_20260912/L01_opik_hermes_design.md` + L20_opik_trajectory_reconcile - hence the Ritu item demoted), force-reset 0, 0xRicker 0, IOSG 0. `grep -ri` over `memory/` (partial, killed after the load-bearing hits): graceful wrap only in this session's trajectory rows; Model Fusion only in pinned-arXiv trajectory rows and this session's own commands. Dedupe vs both sibling lanes' item lists done at read time (no overlap found with any banked item above).

## OWED (unreachable or unread this ask; nothing asserted)

- suhaib consensus-hallucination post and openreview "When Consensus Is Not Correctness: Diversity Collapse" - surfaced by a general fallback query, never fetched.
- Splunk Token Meter README (behind splk.it shortener) - not fetched.
- RQ3 X-native in-window: none exists in the reachable index; djfarrelly "Agent Loop Architecture" (06-17, duplicate-sub-agent failure list), akshay "Four Pillars of Loop Engineering" (06-24, maker/checker separation), addyosmani "false parallelism" (07-03) are snippet-level only, out-of-window, and NOT banked.
- arXiv 2601.07245 (Multi-Model Consensus Reasoning Engine, Jan 2026) - out of window, unread.
- Raw fxtwitter JSONs cached at `watch/inbox/frontier_olm_2026-10-01/sweep/_fx/_jev_article_raw.json` and `_iosg_modelfusion_raw.json` for byte-level re-verification.
