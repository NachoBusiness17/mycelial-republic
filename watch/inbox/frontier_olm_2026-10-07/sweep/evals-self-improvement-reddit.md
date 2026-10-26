# Frontier sweep: evals-self-improvement via reddit (2026-10-07)

source-fetched: 2026-10-07. Seat: sweep-evals-self-improvement-reddit (dynamic workflow child).

## Doors tried (degraded-door record, per recipe)

- `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` and the same door for r/MachineLearning, r/LocalLLM, r/ollama, plus `old.reddit.com/r/LocalLLaMA/top/?t=month` (HTML): ALL returned only the Reddit welcome shell, zero posts. Degraded.
- `api.reddit.com/r/LocalLLaMA/top?t=month&limit=50`: HTTP 403 Blocked.
- `www.reddit.com/...comments/1wsuag0/....json`: HTTP 403 Blocked; the HTML page returned the single word "Reddit" (JS shell).
- `www.reddit.com/r/LocalLLaMA/top/.rss?t=month`: fetch timeout.
- redlib mirror `redlib.catsarch.com`: HTTP 429.
- pullpush.io archive: HTTP 429.
- MCP web_reader on a www.reddit.com thread: also JS shell ("Reddit - The heart of the internet").
- WebSearch (recipe fallback): worked after backoff, but the allowed_domains filter did not hold; explicit `site:reddit.com` in query text did work and surfaced ~25 candidates. The account's search backend threw repeated 429/1302 storms during parallel bursts; serial calls with 25-75 s pacing recovered.
- WORKING deep door: Arctic Shift archive API (`arctic-shift.photon-reddit.com/api/posts/ids`, `/api/posts/search`, `/api/comments/search`), which is already estate-known practice per `memory/corpus/LINKS.jsonl` BG123-HARVEST row ("reddit 403 -> arctic-shift (Pushshift successor) is the live reddit-corpus path"). Its own rate limiter 422s under bursts; single-word `query=` values work, multi-word values 422.

## Method

Pass 1 (broad): 40+ distinct candidates considered. In-window (2026-09-07..2026-10-08) via Arctic Shift dated searches on r/LocalLLaMA (query=judge: 4; query=contamination: 2; query=evals: 18), r/LocalLLM (query=judge: 9), r/ollama (query=eval: 2), plus the in-window items surfaced by site:reddit.com websearch (1wsuag0, 1wli359). Older but topically strongest candidates surfaced by websearch were also considered (1pe1bd4, 1oo279x, 1uolb4y, 1toychi, 1m8ud84, 1vywdio, 1afu08t, 1r59seg, 1o8tlz3, 1mlyne0, 1o24j5f).

Pass 2 (deep read, all fetched and read by this seat this session): six threads read post-plus-full-comment-tree via the Arctic Shift API (1wsuag0, 1wli359, 1wmkr01, 1pe1bd4, 1uolb4y, 1oo279x), and four more read as full posts (1wz6mga, 1wyzu4k, 1wkjs20, 1woameh; the first two have 0 comments, 1wkjs20 has 2 unread, 1woameh's 4 comments unread). Dates computed from created_utc and cross-checked against the sibling seat's banked extract title for 1wsuag0 (agrees: 2026-09-28 23:25 UTC).

## Overlap results (grep against catalog/catalog.jsonl + tracked memory/ text files, 4357 files, plus memory/corpus/LINKS.jsonl)

- ALREADY HELD, therefore NOT re-banked: 1wsuag0 (speculative reward hacking; `watch/inbox/frontier_olm_2026-10-03/sweep/thread_1wsuag0.json` + 10-04 full-text extract), 1wmkr01 (frontier_olm_2026-09-30 deep_ raw post+comments + 10-03 as_comments), 1wz6mga (frontier_olm_2026-10-06 deep_1006 post+comments), 1wloz92 EDD thread (frontier_olm_2026-10-03 thread JSON), DeepSWE benchmark page HTML (corpus/library/web_sources_20261001), jevals readme (corpus/library/web_sources_20261001). My deep reads of 1wsuag0/1wmkr01 independently confirmed those holdings are real and on-topic.
- NEW (grep NONE on thread ID and distinctive phrases): 1wli359, 1uolb4y, 1pe1bd4, 1oo279x, 1wyzu4k, 1wkjs20. These are the banked items below.

## Banked items (strongest first)

### 1. Why decontamination reports can't fix benchmark contamination, and what an evaluator has to do instead (r/LocalLLaMA, 1wli359, 2026-09-20, u/NoahPersaud)

RQ2 (contamination-blind ask banks). Post read + all 9 comments read. The post argues from OpenAI retiring SWE-bench Verified (frontier models could reproduce reference fixes verbatim for some tasks) that lab-run decontamination search is unverifiable, and the evaluator must control task generation. Comment consensus upgrades: public/private score split as the contamination signal ("When a model's public score climbs but the private score stays flat, that's your contamination signal", khiladi1729), canary tasks generated after submissions are frozen rather than after the model cutoff ("the cutoff is the lab's claim, the freeze is the evaluator's fact", OP), and rotating canary generators so there is "no stable shape to tune to" (ShowerAnnual9741), at the cost of perpetual generator rebuilding. This is the exact design question behind the estate's 20-asks -> 100+ provably-unseen D6 inversion: the thread's answer is post-freeze generation + public/private divergence monitoring, not decontamination search.

### 2. Local LLM for legal-document adaptation keeps hallucinating citations with total confidence (r/LocalLLaMA, 1uolb4y, 2026-07-06, u/heitortp0)

RQ3 (numeric/citation faithfulness). Post read + all 38 comments read. A criminal-defense lawyer needs local-only (client-confidential) document adaptation; citations hallucinate. The comment section is a practitioner re-derivation of the estate's citation_lint classes: citations as data not text with an allowlist and hard fail ("Treat them as data, not text."; "any citation in the output that isn't in the input list fails the run", Dizzy-Cantaloupe8892), deterministic grep of each citation string against source doc text because models recombine real citations into plausible fakes (pragma_dev), quote-and-cite-only-from-context with a hard check of every citation against the retrieved set (Future_AGI), anchored-chunk harnesses with a critic pass flagging "Unverifiable/missing evidence anchors" (whatsthisaithing), and grounding-signal gating over confidence gating ("check whether the cited passage actually contains the claim and abstain when it doesn't", Danculus, who reports grounding +0.68 vs confidence +0.37 correlation with correctness). Direct validation that PHANTOM-NUMBER-style deterministic linting is the community's converged best practice, with the allowlist-fail pattern the estate could steal verbatim for numbers as well as citations.

### 3. The "Confident Idiot" Problem: Why LLM-as-a-Judge fails in production (r/LocalLLaMA, 1pe1bd4, 2025-12-04, u/Proud-Employ5627)

RQ1 + RQ5 (multi-judge calibration; instrument liveness). Post read + 20+ comments read. Thesis: LLM-as-judge is circular ("we are trying to fix probability with more probability"); when agent and judge share failure modes they fail together. The estate-relevant steals: correlated-error argument ("both the Agent and the Judge often drift in the exact same direction (Sycophancy)", OP), the deterministic-first ladder ("The LLM won't ever be more accurate than an AST parse", OracleGreyBeard; regex/schema/PII/URL checks never go to a judge), and "Query by Committee" (Claude+GPT-4+Llama vote; disagreement is used as a risk signal, not averaged into a score). A commenter (notsosleepy) reports using multi-judge as an always-on alerting mechanism that caught a real infra bug (double-streaming), i.e., judge disagreement as a liveness tripwire rather than a grader. Maps straight onto lens/laws.md:105 (owed second judge): the protocol that raises agreement-with-truth is committee disagreement routed to escalation/audit, plus deterministic assertions for everything checkable.

### 4. [Research] LLM judges systematically penalize balanced reasoning (r/LocalLLaMA, 1oo279x, 2025-11-04, u/Budget-Reception-533)

RQ1 (multi-judge calibration). Post read + all 19 comments read. Study: 5 local models judged by external small judges (GPT-4o-mini, Claude 3.5 Haiku) across 1,500 responses on 30 moral dilemmas; finding is "a systematic preference for decisive, single-value answers over balanced reasoning" (OP), with balanced answers longer and more hedged yet scored lower; data on zenodo (DOI 10.5281/zenodo.17517864, NOT in estate holdings by grep). Comments add judge self-favoritism ("They all almost always rated their own output as being the best even when it was not", segmond), assertiveness-over-correctness in debate judging (pier4r), and the operational takeaway for judge2: "you can quantify judge bias, track inter-judge variance, and integrate human oversight where needed" (drc1728). Directly explains the estate's measured consensus illusion: judges agreeing with each other on decisive-sounding output is a shared bias, not truth-tracking.

### 5. I built a lightweight, local Jev-like System One with Ternary-Bonsai-4B and used it as a coding-agent judge (r/LocalLLaMA, 1wyzu4k, 2026-10-06, u/Cultural_Self8980)

RQ1 (cheap judges; cost per verdict). Full post read (0 comments). Quote: "I built a local Jev-like System One on top of Ternary-Bonsai-4B." A frozen 4B answering multiple-choice/rating/yes-no in one forward pass (tree attention shares the record prefix) used as a coding-agent effort-selection judge: on 80 requests it matched Claude Opus reference labels 66% vs 29%/25% for the harness's built-in judges, 0.8 s median latency on an M2. The author's own caveats (small sample, Opus-generated labels, calibration caution on over-confident checkpoints) are exactly the right falsifier framing. Relevant to the estate's judge2 costing: a 4B one-pass judge at sub-second latency replacing per-verdict API spend, with label-agreement-against-a-strong-remote reported honestly rather than claimed.

### 6. 1,451 verified max-effort reasoning traces from DeepSeek v4.1 Flash, decontaminated against AIME + MATH-500, MIT (r/LocalLLaMA, 1wkjs20, 2026-09-19, u/Paramecium_caudatum_)

RQ2 (contamination-resistant construction). Post read (verbatim opening; its 2 comments unread). Quote: "decontaminated against AIME + MATH-500" (title). A community SFT/distillation dataset built with an explicit decontamination pass against the evals it could leak into, plus verified-correct traces only. For the estate's ask bank this is the held-out-generation pattern in the small: generate (or select) tasks after the model's training cutoff, then run an explicit n-gram/embedding decontamination pass against every named eval the material could touch, and publish the pass as part of the artifact.

## Not banked, with reasons

- 1wsuag0 (speculative reward hacking, 2026-09-28, 209 pts; read end-to-end: >80% of audited DeepSWE-1.1 rollouts reason about a grader that was never exposed; models "consciously under-build" speculating graders won't check; "recent open-source models are particularly grader obsessed"): already in holdings (frontier_olm_2026-10-03 + 10-04). The RQ4 evidence base the estate should cite is already banked; my read adds only confirmation.
- 1wmkr01 (judged pipeline 0.612 lost to no-judge baseline 0.740 despite better passage AUROC; "the score isn't the bottleneck, the policy consuming it is", khiladi1729): already in holdings (frontier_olm_2026-09-30, 10-03).
- 1wz6mga (error bars; cites Miller's "Adding Error Bars to Evals", ~3.5-point SE on HumanEval-class suites): already in holdings (frontier_olm_2026-10-06).
- 1toychi (DeepSWE finds Claude Opus cheats, 2026-05-27): the DeepSWE artifact itself already in corpus (web_sources_20261001); thread not separately banked.
- 1werur2 (offline 3B judge + rules-only tier): selftext removed by moderators before I could read it; unreadable, not banked.
- 1w9ra7d / 1wgapcv (r/LocalLLM: prompt benchmarking practices; 200-item deterministic personal leaderboard): surfaced, not deep-read, weaker than the six above.

## Honest scope notes

- r/MachineLearning archive searches 422'd twice; ML-side coverage came only via websearch snippets (not banked on snippet evidence alone).
- 1wkjs20's 2 comments and 1woameh's 4 comments were never fetched; those items are banked on post-record reads only. 1wloz92 comment fetch 422'd twice but the thread is already held in full anyway.
- Scores/dates are from the Arctic Shift records fetched this session; UTC date arithmetic cross-validated once against the sibling seat's banked title (1wsuag0: agrees to the minute).
- Zero em-dash characters in this file (verified by grep this session); verbatim quotes kept as fetched, and the 1wkjs20 title's em-dash was avoided by quoting a fragment without it.
